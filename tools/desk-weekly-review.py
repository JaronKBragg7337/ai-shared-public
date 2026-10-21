#!/usr/bin/env python3
"""Weekly explore/exploit review for the Polymarket desk schedule.

Read-only market and settlement inputs; writes only the Control Room desk_schedule row,
its local backup/report, and one ntfy notice on a non-dry run. Never touches orders.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
STATE = os.path.join(ROOT, "state")
HISTORY = os.path.join(STATE, "desk-schedule-history")
REPORTS = os.path.join(STATE, "desk-review")
ACTIVITIES = os.path.join(STATE, "polymarket-activities-all.json")
VENV = os.path.join(ROOT, "runtime", "polymarket-us-agent-venv", "Scripts", "python.exe")
KEY = "desk_schedule"

sys.path.insert(0, TOOLS)
import desk_schedule as DS


def secrets():
    out = {}
    path = os.path.join(os.path.expanduser("~"), ".secrets", "keys.env")
    try:
        for line in open(path, encoding="utf-8-sig"):
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return out


def sb(env, method, path, body=None):
    url = f"{env['SUPABASE_URL'].rstrip('/')}/rest/v1/{path}"
    key = env["SUPABASE_SERVICE_ROLE_KEY"]
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
        method=method, headers={"apikey": key, "Authorization": f"Bearer {key}",
        "Content-Type": "application/json", "Prefer": "return=representation"})
    with urllib.request.urlopen(req, timeout=45) as response:
        raw = response.read()
        return json.loads(raw) if raw else []


def parse_time(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except (ValueError, TypeError):
        return None


def activities():
    # Refresh from the entire Polymarket US history, using its dedicated client venv.
    p = subprocess.run([VENV, os.path.join(TOOLS, "pm-history-all.py")], cwd=ROOT,
                       capture_output=True, text=True, timeout=300)
    if p.returncode:
        raise RuntimeError("full Polymarket history refresh failed: " + (p.stderr or p.stdout)[-500:])
    with open(ACTIVITIES, encoding="utf-8") as f:
        return json.load(f)


def live_markets():
    # proposer.fetch_open_markets requires polymarket_us, which is installed in VENV.
    code = ("import sys,json,datetime;sys.path.insert(0,'tools');import proposer;"
            "now=datetime.datetime.now(datetime.timezone.utc);out=[];"
            "ms=proposer.fetch_open_markets(pages=10);"
            "[(out.append({'slug':m.get('slug',''),'gameStartTime':m.get('gameStartTime')})) "
            "for m in ms if m.get('slug') and m.get('gameStartTime') and not m.get('closed') "
            "and 0 <= (now-datetime.datetime.fromisoformat(m['gameStartTime'].replace('Z','+00:00'))).total_seconds()/3600 <= 8];"
            "print(json.dumps(out))")
    p = subprocess.run([VENV, "-c", code], cwd=ROOT, capture_output=True, text=True, timeout=180)
    if p.returncode:
        raise RuntimeError("live market scan failed: " + (p.stderr or p.stdout)[-500:])
    return json.loads(p.stdout)


def settled_by_market(acts):
    # Match publish-crew.py: automatic shares / all shares times Polymarket's
    # per-market realized position resolution (which includes fees).
    shares, resolutions = defaultdict(lambda: [0.0, 0.0]), {}
    for item in acts:
        trade = item.get("trade")
        if trade:
            execution = trade.get("aggressorExecution") if trade.get("isAggressor") else trade.get("passiveExecution")
            execution = execution or {}
            qty = float(execution.get("lastShares") or 0)
            row = shares[trade.get("marketSlug") or ""]
            row[1] += qty
            indicator = ((execution.get("order") or {}).get("manualOrderIndicator") or "")
            if indicator.endswith("AUTOMATIC"):
                row[0] += qty
        resolution = item.get("positionResolution")
        if resolution:
            after = resolution.get("afterPosition") or {}
            realized = after.get("realized") or {}
            slug = resolution.get("marketSlug")
            if slug:
                resolutions[slug] = (float(realized.get("value") or 0),
                                     parse_time(resolution.get("updateTime")))
    out = {}
    for slug, (value, at) in resolutions.items():
        ai, total = shares.get(slug, (0.0, 0.0))
        if at and total > 0 and ai > 0:
            out[slug] = (value * ai / total, at, DS.sport_of(slug))
    return out


def lane_stats(schedule, settled, now):
    result = defaultdict(lambda: {"7d": 0.0, "21d": 0.0, "weeks": [0.0, 0.0, 0.0]})
    cut7, cut21 = now - timedelta(days=7), now - timedelta(days=21)
    # Three completed Monday-Sunday weeks, newest first.
    monday = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=now.weekday())
    windows = [(monday - timedelta(days=7 * (i + 1)), monday - timedelta(days=7 * i)) for i in range(3)]
    sport_lane = {s.lower(): ln["name"] for ln in schedule.get("lanes", []) for s in ln.get("sports", [])}
    for slug, (pnl, at, sport) in settled.items():
        lane = sport_lane.get(sport, sport or "unknown")
        d = result[lane]
        if at >= cut7:
            d["7d"] += pnl
        if at >= cut21:
            d["21d"] += pnl
        for i, (start, end) in enumerate(windows):
            if start <= at < end:
                d["weeks"][i] += pnl
    return result


def cap_snapshot(lane):
    if "original_caps_usd" not in lane:
        lane["original_caps_usd"] = [w.get("cap_usd") for w in lane.get("windows", [])]
    return lane["original_caps_usd"]


def set_lane_caps(lane, caps):
    for i, window in enumerate(lane.get("windows", [])):
        original = caps[i] if i < len(caps) else caps[-1] if caps else None
        # A finite stored cap may never be raised. None means the original schedule
        # allowed normal sizing; a $1 test remains an explicit temporary limit.
        window["cap_usd"] = 1 if lane.get("benched") else original


def set_test_windows(lane):
    lane["windows"] = [{"days": list(DS.DAYS), "from": "00:00", "to": "24:00", "cap_usd": 1}]


def sport_name(sport):
    names = {"ncaab": "college basketball", "ncaams": "college soccer", "ncaaws": "college soccer",
             "mlb": "baseball", "nhl": "hockey", "wnba": "women's basketball", "nba": "basketball"}
    return names.get(sport, sport.upper() if sport in {"nfl", "mlb", "nhl", "nba", "wnba", "cfb"} else sport.upper()) + " (test)"


def decision(schedule, settled, markets, now):
    stats = lane_stats(schedule, settled, now)
    lanes = schedule["lanes"]
    by_name = {l["name"]: l for l in lanes}
    kept, benched, retesting, new = [], [], [], []

    # Evaluate lanes already on the bench. A previous review's bench_open marks the
    # completed retest week and is evaluated before scheduling the next one.
    for lane in lanes:
        lane["bench_open"] = False
        if lane.get("benched"):
            d = stats[lane["name"]]
            was_retest = bool(lane.get("bench_open_previous")) or bool(lane.get("bench_open"))
            # Older state uses the last review's `bench_retest` marker.
            was_retest = was_retest or bool(lane.get("bench_retest_last_week"))
            if was_retest and d["7d"] > 0 and d["21d"] >= 0:
                caps = lane.get("original_caps_usd", [])
                lane["benched"] = False
                lane.pop("benched_date", None)
                lane["bench_weeks"] = 0
                lane["bench_retest_last_week"] = False
                lane.pop("bench_reason", None)
                set_lane_caps(lane, caps)
                kept.append((lane["name"], d["7d"]))
                continue
            lane["bench_weeks"] = int(lane.get("bench_weeks", 0)) + 1
            lane["bench_retest_last_week"] = False
            if lane["bench_weeks"] % 3 == 0:
                lane["bench_open"] = True
                lane["bench_retest_last_week"] = True
                set_lane_caps(lane, lane.get("original_caps_usd", []))
                lane["windows"] = lane.get("bench_windows") or lane.get("windows", [])
                for w in lane["windows"]:
                    w["cap_usd"] = 1
                retesting.append((lane["name"], d["21d"]))
            else:
                for w in lane.get("windows", []):
                    w["cap_usd"] = 1
            continue

        caps = cap_snapshot(lane)
        d = stats[lane["name"]]
        if len(d["weeks"]) == 3 and all(x < 0 for x in d["weeks"]) or d["21d"] < -15:
            lane["benched"] = True
            lane["benched_date"] = now.date().isoformat()
            lane["bench_reason"] = "three completed negative weeks" if all(x < 0 for x in d["weeks"]) else "21-day net below -$15"
            lane["bench_weeks"] = 0
            lane["bench_windows"] = [dict(w) for w in lane.get("windows", [])]
            lane["bench_open"] = False
            lane["bench_retest_last_week"] = False
            for w in lane["windows"]:
                w["cap_usd"] = 1
            benched.append((lane["name"], d["21d"]))
        else:
            lane.pop("benched", None)
            lane.pop("bench_open", None)
            lane.pop("bench_retest_last_week", None)
            # Restore only at or below each lane's stored original cap.
            set_lane_caps(lane, caps)
            kept.append((lane["name"], d["7d"]))

    sports = sorted({DS.sport_of(m.get("slug", "")) for m in markets} -
                    {s.lower() for l in lanes for s in l.get("sports", [])} - {"", "undefined"})
    for sport in sports:
        lane = {"name": sport_name(sport), "sports": [sport], "remind": False,
                "windows": [{"days": list(DS.DAYS), "from": "00:00", "to": "24:00", "cap_usd": 1}],
                "original_caps_usd": [1], "new_test": True}
        lanes.append(lane)
        by_name[lane["name"]] = lane
        stats[lane["name"]] = stats.pop(sport, {"7d": 0.0, "21d": 0.0, "weeks": [0.0, 0.0, 0.0]})
        new.append((lane["name"], stats[lane["name"]]["7d"]))

    # Keep at least three lanes enabled; use the best 21-day bench performers first.
    available = [l for l in lanes if not l.get("benched") or l.get("bench_open")]
    floor_opened = []
    bench_pool = sorted((l for l in lanes if l.get("benched") and not l.get("bench_open")),
                        key=lambda l: (-stats[l["name"]]["21d"], l["name"]))
    while len(available) < 3 and bench_pool:
        lane = bench_pool.pop(0)
        lane["bench_open"] = True
        lane["floor_open"] = True
        lane["windows"] = lane.get("bench_windows") or lane.get("windows", [])
        for w in lane["windows"]:
            w["cap_usd"] = 1
        available.append(lane)
        floor_opened.append((lane["name"], stats[lane["name"]]["21d"]))
    for lane in lanes:
        if lane.get("benched") and lane.get("bench_open"):
            for w in lane.get("windows", []):
                w["cap_usd"] = 1
        lane.pop("floor_open", None)
    return {"stats": stats, "kept": kept, "benched": benched, "retesting": retesting,
            "new": new, "floor_opened": floor_opened, "live_sports": sports}


def report_text(review_date, result, dry):
    fmt = lambda x: f"{'+' if x >= 0 else '-'}${abs(x):.2f}"
    lines = [f"# Desk weekly review — {review_date}", "", f"Mode: {'dry run' if dry else 'applied'}",
             "", "Settled automatic bot P&L by lane (Polymarket realized settlement split by AUTOMATIC share):", "",
             "| Lane | 7 days | 21 days | Last 3 completed weeks (newest first) |", "|---|---:|---:|---:|"]
    for name, d in sorted(result["stats"].items()):
        lines.append(f"| {name} | {fmt(d['7d'])} | {fmt(d['21d'])} | " + " / ".join(fmt(v) for v in d["weeks"]) + " |")
    for key, title in (("kept", "Kept active"), ("benched", "Benched"), ("retesting", "Re-testing at $1"),
                       ("floor_opened", "Opened to maintain 3-lane floor"), ("new", "New $1 test lanes")):
        lines += ["", f"## {title}"]
        lines += [f"- {name}: {fmt(pnl)} 7-day net" if key != "floor_opened" else f"- {name}: {fmt(pnl)} 21-day net"
                  for name, pnl in result[key]] or ["- None"]
    lines += ["", "## Live new-sport scan", "", ", ".join(result["live_sports"]) if result["live_sports"] else "No unassigned sports with live games found.",
              "", "Global no-new-positions window retained: 2:00–11:00 AM Indianapolis time.",
              "The review reads resolved markets only and never places, cancels, or changes orders.", ""]
    return "\n".join(lines)


def push(msg):
    topic = secrets().get("NTFY_TOPIC")
    if not topic:
        raise RuntimeError("ntfy topic unavailable")
    req = urllib.request.Request("https://ntfy.sh/" + topic, data=msg.encode(),
        headers={"Title": "Desk weekly review"})
    with urllib.request.urlopen(req, timeout=20) as r:
        r.read()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    now = datetime.now(timezone.utc)
    date = DS.local_now().date().isoformat()
    schedule = DS.load()
    if not schedule:
        raise SystemExit("desk_schedule setting unavailable or invalid")
    acts = activities()
    settled = settled_by_market(acts)
    markets = live_markets()
    result = decision(schedule, settled, markets, now)
    keep_net = sum(x[1] for x in result["kept"])
    bench_net = sum(x[1] for x in result["benched"])
    summary = (f"Desk review: Keep {len(result['kept'])} ({'+' if keep_net >= 0 else '-'}${abs(keep_net):.2f}), "
               f"Benched {len(result['benched'])} ({'+' if bench_net >= 0 else '-'}${abs(bench_net):.2f}), "
               f"Re-testing {len(result['retesting'])} at $1, New test: "
               f"{', '.join(n for n, _ in result['new']) or 'none'}")
    decision_lines = [f"DRY RUN — {summary}"]
    decision_lines += [f"  Keep: {', '.join(n for n, _ in result['kept']) or 'none'}",
                       f"  Bench: {', '.join(n for n, _ in result['benched']) or 'none'}",
                       f"  Re-test: {', '.join(n for n, _ in result['retesting']) or 'none'}",
                       f"  Floor opens: {', '.join(n for n, _ in result['floor_opened']) or 'none'}",
                       f"  New live-sport tests: {', '.join(n for n, _ in result['new']) or 'none'}"]
    print("\n".join(decision_lines))
    os.makedirs(REPORTS, exist_ok=True)
    text = report_text(date, result, args.dry_run) + "\n## Dry-run output\n\n```text\n" + "\n".join(decision_lines) + "\n```\n"
    with open(os.path.join(REPORTS, date + ".md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    if args.dry_run:
        return

    env = secrets()
    rows = sb(env, "GET", f"system_settings?select=key,value&key=eq.{KEY}")
    if not rows:
        raise RuntimeError("desk_schedule Control Room row not found")
    old = rows[0]["value"]
    if isinstance(old, str):
        old = json.loads(old)
    os.makedirs(HISTORY, exist_ok=True)
    backup = os.path.join(HISTORY, now.strftime("%Y%m%d-%H%M%S") + ".json")
    with open(backup, "w", encoding="utf-8") as f:
        json.dump(old, f, indent=2)
    sb(env, "PATCH", f"system_settings?key=eq.{KEY}", {"value": schedule})
    import settings
    settings._cache.update(at=0.0, rows=None)
    verify = DS.load()
    if not verify or len(verify.get("lanes", [])) != len(schedule.get("lanes", [])):
        raise RuntimeError("Control Room schedule write could not be verified")
    push(summary)
    print("Applied schedule. Backup:", os.path.relpath(backup, ROOT))
    print("Report:", os.path.relpath(os.path.join(REPORTS, date + ".md"), ROOT))


if __name__ == "__main__":
    main()
