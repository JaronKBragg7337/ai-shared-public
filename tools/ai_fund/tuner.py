"""AI Fund Desk - hourly judgement ("every hour make a judgement call to improve it"). Built 2026-11-15, Claude Code.

A cheap AI (DeepSeek Flash via the API; Codex Luna as fallback) reads the compact results and may change ONLY the bounded
keys in projects/ai-fund/config.json -> "tunable". This script, not the AI, enforces every limit:
  * key must be in "tunable"; value clamped to "bounds"
  * at most max_daily_move per key in any 24 hours (weights: 2 points)
  * a weight may be RAISED only once per 7 days per sleeve (cuts any hour) - Fable's asymmetry
  * weights may not sum above 1 - min_reserve; at most 3 changes per hour; at most 24 AI calls per day
Changes take effect on the NEXT run (no same-bar look-ahead). Every call -> state/ai-fund/tuner-log.jsonl; every accepted
change -> projects/ai-fund/CHANGELOG.md + state/ai-fund/changes.jsonl. Claude is not the tuner (provider-terms line in
watch/CLI-SEATS.md); Claude only built the harness. The frozen twin (untuned copy) is the control: if the tuned fund
does not beat it after 6 months, the weekly review should switch the tuner off.
"""
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CFG = os.path.join(ROOT, "projects", "ai-fund", "config.json")
CHANGELOG = os.path.join(ROOT, "projects", "ai-fund", "CHANGELOG.md")
TLOG = os.path.join(ROOT, "state", "ai-fund", "tuner-log.jsonl")
CHANGES = os.path.join(ROOT, "state", "ai-fund", "changes.jsonl")
SECRETS = os.path.join(os.path.expanduser("~"), ".secrets", "keys.env")


def _env():
    out = {}
    try:
        for line in open(SECRETS, encoding="utf-8"):
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return out


def _jsonl(p):
    if not os.path.exists(p):
        return []
    out = []
    for line in open(p, encoding="utf-8"):
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def _get(cfg, key):
    a, b = key.split(".", 1)
    return cfg[a][b]


def _set(cfg, key, v):
    a, b = key.split(".", 1)
    cfg[a][b] = v


def compact(summary, cfg):
    s = summary
    bt = s["backtest"]
    rows = []
    for x in s["sleeves"]:
        m, b = x["metrics"], x["backtest"]
        rows.append({"sleeve": x["name"], "weight": x["weight"], "status": x["status"], "half_size": x["scale"] < 1,
                     "fwd_return": m["total"], "fwd_maxdd": m["maxdd"], "fwd_days": m["days"], "fwd_trades": x["trades"],
                     "bt_ann": b.get("ann"), "bt_maxdd": b.get("maxdd"), "bt_sharpe": b.get("sharpe"),
                     "bt_p_beat_bench": b.get("p_beat"), "bench": x["bench"], "verdict": x["verdict"]})
    recent = _jsonl(CHANGES)[-6:]
    return {
        "now": s["updated"], "forward_days": s["fund"]["days"],
        "fund_fwd": {k: s["fund"].get(k) for k in ("total", "maxdd", "dd")}, "twin_fwd": {k: s["twin"].get(k) for k in ("total", "maxdd")},
        "bench_fwd_total": {n: b["total"] for n, b in s["bench"].items()},
        "backtest_ann": {"fund": bt["fund"]["ann"], "fund_3x_costs": bt["fund_stress3x"]["ann"],
                         **{n: b["ann"] for n, b in bt["bench"].items()}},
        "sleeves": rows, "voltarget": cfg["voltarget"], "bounds": cfg["bounds"],
        "max_daily_move": cfg["max_daily_move"], "min_reserve": cfg["min_reserve"],
        "recent_changes": recent, "data_flags": s["freshness"]["flags"][:5],
    }


PROMPT = """You are the hourly tuner of a PAPER-ONLY simulated fund (no real money, nothing is traded). Make one judgement
call for this hour about its bounded config. You may only change these keys: {keys}. Bounds: {bounds}. A script enforces
every limit: at most {mdm} per key per 24h, weight raises only once per 7 days per sleeve (cuts any time), weights sum
<= {cap}, at most 3 changes. Changes apply next hour.
Rules of judgement: forward data younger than ~60 days is mostly noise; backtest numbers were chosen with hindsight and
are weak evidence; a frozen untuned twin is the control you are measured against, so churn that does not clearly help
makes you lose to it. Holding is a valid decision. Cutting a sleeve that is breaking down, or with broken data, is fine.
Reply ONLY with JSON: {{"decision": "hold" | "change", "changes": [{{"key": "...", "to": number, "reason": "short"}}],
"note": "one plain sentence for the owner's dashboard"}}
STATE: {state}"""


def ask_deepseek(prompt, model):
    e = _env()
    body = {"model": model, "temperature": 0.2, "max_tokens": 700, "response_format": {"type": "json_object"},
            "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request("https://api.deepseek.com/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json", "Authorization": f"Bearer {e['DEEPSEEK_API_KEY']}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        j = json.load(r)
    return j["choices"][0]["message"]["content"], j.get("usage", {}), f"deepseek:{j.get('model', model)}"


def ask_codex(prompt):
    out = os.path.join(os.environ.get("TEMP", ROOT), "ai-fund-tuner-codex.txt")
    subprocess.run(["codex", "exec", "-m", "gpt-6-luna", "-c", "model_reasoning_effort=low", "-s", "read-only",
                    "--skip-git-repo-check", "-C", ROOT, "-o", out, "-"], input=prompt, text=True, encoding="utf-8",
                   capture_output=True, timeout=300, shell=(os.name == "nt"))
    return open(out, encoding="utf-8", errors="replace").read(), {}, "codex:gpt-6-luna"


def parse(text):
    a, b = text.find("{"), text.rfind("}")
    return json.loads(text[a:b + 1])


def validate(cfg, proposal, now):
    accepted, rejected = [], []
    hist = _jsonl(CHANGES)
    day_ago, week_ago = now - timedelta(hours=24), now - timedelta(days=7)
    cap = 1 - cfg["min_reserve"]
    for ch in (proposal.get("changes") or [])[:cfg["tuner"]["max_changes_per_hour"]]:
        k, why = ch.get("key"), str(ch.get("reason", ""))[:200]
        try:
            to = float(ch.get("to"))
        except (TypeError, ValueError):
            rejected.append({"key": k, "why": "not a number"})
            continue
        if k not in cfg["tunable"]:
            rejected.append({"key": k, "why": "not a tunable key"})
            continue
        lo, hi = cfg["bounds"][k]
        to = round(min(hi, max(lo, to)), 4)
        cur = _get(cfg, k)
        if abs(to - cur) < 1e-6:
            continue
        mdm = cfg["max_daily_move"].get(k, cfg["max_daily_move"].get(k.split(".")[0]))
        moved = sum(abs(h["to"] - h["from"]) for h in hist if h["key"] == k and datetime.fromisoformat(h["at"]) > day_ago)
        room = max(0.0, mdm - moved)
        if room <= 1e-9:
            rejected.append({"key": k, "why": f"already moved {moved:.3f} in 24h (limit {mdm})"})
            continue
        if abs(to - cur) > room:
            to = round(cur + (room if to > cur else -room), 4)
        if k.startswith("weights.") and to > cur:
            if any(h["key"] == k and h["to"] > h["from"] and datetime.fromisoformat(h["at"]) > week_ago for h in hist):
                rejected.append({"key": k, "why": "weight raises only once per 7 days"})
                continue
            if sum(cfg["weights"].values()) - cur + to > cap + 1e-9:
                rejected.append({"key": k, "why": f"weights would exceed {cap:.0%}"})
                continue
        _set(cfg, k, to)
        rec = {"at": now.isoformat(timespec="seconds"), "key": k, "from": cur, "to": to, "reason": why}
        hist.append(rec)
        accepted.append(rec)
    return accepted, rejected


def hourly(summary, cfg_loaded=None):
    now = datetime.now(timezone.utc)
    cfg = json.load(open(CFG, encoding="utf-8"))           # raw file (keeps _about etc.); engine clamps on load anyway
    tc = cfg["tuner"]
    today = now.strftime("%Y-%m-%d")
    calls = [r for r in _jsonl(TLOG) if r.get("at", "").startswith(today) and r.get("called")]
    rec = {"at": now.isoformat(timespec="seconds"), "called": False}
    if len(calls) >= tc["max_calls_per_day"]:
        rec.update({"decision": "skip", "note": f"daily AI call cap ({tc['max_calls_per_day']}) reached"})
        _append(TLOG, rec)
        return rec
    prompt = PROMPT.format(keys=cfg["tunable"], bounds=json.dumps(cfg["bounds"]), mdm=json.dumps(cfg["max_daily_move"]),
                           cap=1 - cfg["min_reserve"], state=json.dumps(compact(summary, cfg), separators=(",", ":")))
    try:
        text, usage, who = ask_deepseek(prompt, tc["model"])
    except Exception as e:   # noqa: BLE001
        rec["deepseek_error"] = str(e)[:160]
        try:
            text, usage, who = ask_codex(prompt)
        except Exception as e2:   # noqa: BLE001
            rec.update({"decision": "error", "note": f"no AI reachable: {e2}"[:200]})
            _append(TLOG, rec)
            return rec
    rec.update({"called": True, "by": who, "tokens": usage.get("total_tokens")})
    try:
        prop = parse(text)
    except Exception:   # noqa: BLE001
        rec.update({"decision": "error", "note": "reply was not JSON", "raw": text[:300]})
        _append(TLOG, rec)
        return rec
    accepted, rejected = validate(cfg, prop, now)
    rec.update({"decision": "change" if accepted else "hold", "asked": prop.get("decision"),
                "note": str(prop.get("note", ""))[:300], "accepted": accepted, "rejected": rejected})
    if accepted:
        tmp = CFG + ".tmp"
        json.dump(cfg, open(tmp, "w", encoding="utf-8"), indent=2)
        os.replace(tmp, CFG)
        for a in accepted:
            _append(CHANGES, {**a, "by": who})
        with open(CHANGELOG, "a", encoding="utf-8") as f:
            for a in accepted:
                f.write(f"- {a['at'][:16].replace('T', ' ')} UTC | {who} | {a['key']} {a['from']} -> {a['to']} | {a['reason']}\n")
    _append(TLOG, rec)
    return rec


def _append(p, obj):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj) + "\n")


if __name__ == "__main__":
    s = json.load(open(os.path.join(ROOT, "state", "ai-fund", "summary.json"), encoding="utf-8"))
    print(json.dumps(hourly(s), indent=1))
