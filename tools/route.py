#!/usr/bin/env python3
"""Choose a job runner using the hand-editable state/routing.json role table."""
import argparse
import json
import os
import shlex
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "state" / "routing.json"


def unknown(source="unavailable"):
    return {"used_pct_5h": None, "used_pct_week": None, "resets": None,
            "source": source, "as_of": None}


def meters():
    """Read local usage snapshots and manual readings. No secret values are printed."""
    out = {"codex": unknown("Codex rollout logs"), "reserve": unknown("Codex reserve meter not exposed"),
           "claude": unknown("Claude usage sources"), "grok": unknown("Grok usage sources"),
           "deepseek": unknown("Control Room setting")}
    try:
        from usage import codex as read_codex, claude as read_claude
        c = read_codex()
        if "five_hour_used_pct" in c:
            out["codex"] = {"used_pct_5h": c.get("five_hour_used_pct"), "used_pct_week": c.get("weekly_used_pct"),
                            "resets": {"5h": c.get("five_hour_resets_at"), "week": c.get("weekly_resets_at")},
                            "source": "latest rate_limits event in ~/.codex/sessions/**/rollout-*.jsonl",
                            "as_of": c.get("as_of")}
        k = read_claude()
        out["claude"] = {"used_pct_5h": (k.get("five_hour") or {}).get("est_used_pct"),
                         "used_pct_week": (k.get("week") or {}).get("est_used_pct"),
                         "resets": None, "source": "local Claude token logs estimate; low-trust",
                         "as_of": k.get("as_of")}
    except Exception:
        pass
    try:
        snap = json.loads((ROOT / "state" / "usage-live.json").read_text(encoding="utf-8"))
        c = snap.get("codex", {})
        if out["codex"].get("used_pct_5h") is None and "five_hour_used_pct" in c:
            out["codex"] = {"used_pct_5h": c.get("five_hour_used_pct"), "used_pct_week": c.get("weekly_used_pct"),
                            "resets": {"5h": c.get("five_hour_resets_at"), "week": c.get("weekly_resets_at")},
                            "source": "latest rate_limits event in usage-live.json (Codex rollout JSONL)", "as_of": c.get("as_of")}
        claude = snap.get("claude", {})
        if claude and out["claude"].get("used_pct_5h") is None:
            out["claude"] = {"used_pct_5h": (claude.get("five_hour") or {}).get("est_used_pct"),
                             "used_pct_week": (claude.get("week") or {}).get("est_used_pct"),
                             "resets": None, "source": "usage-live.json local token estimate; low-trust",
                             "as_of": claude.get("as_of")}
    except (OSError, ValueError):
        pass
    try:
        text = (ROOT / "state" / "claude-usage.md").read_text(encoding="utf-8")
        import re
        rows = re.findall(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2} ET) \| 5h: (\d+(?:\.\d+)?)% \| week: (\d+(?:\.\d+)?)% \| resets: ([^|]+) \| source: (.+)", text)
        if rows:
            stamp, p5, pw, reset, src = rows[-1]
            out["claude"] = {"used_pct_5h": float(p5), "used_pct_week": float(pw), "resets": reset.strip(),
                             "source": "manual reading (" + src.strip() + "); low-trust", "as_of": stamp}
    except OSError:
        pass
    # Jaron's Grok readings can be old or refer to Cursor spend rather than the Grok CLI meter.
    # Without an explicit current reading the percentage remains unknown.
    out["grok"] = unknown("state/grok-usage.md is historical; Grok CLI has no account usage/status command (help inspected)")
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        from settings import _rows
        raw = _rows().get("deepseek_daily_budget_usd")
        if raw is None:
            out["deepseek"] = unknown("Control Room deepseek_daily_budget_usd via tools/settings.py; row unavailable")
        else:
            budget = float(raw)
            out["deepseek"] = {"used_pct_5h": None, "used_pct_week": None, "resets": None,
                               "source": "Control Room deepseek_daily_budget_usd via tools/settings.py; budget $" + str(budget),
                               "as_of": datetime.now(timezone.utc).isoformat(), "paused": budget == 0}
    except Exception as exc:
        out["deepseek"] = unknown("Control Room setting unavailable: " + type(exc).__name__)
    return out


def guess_kind(job, kinds):
    low = job.lower()
    for kind in ("judgment", "looks", "build", "research", "chore"):
        if any(word in low for word in kinds[kind].get("keywords", [])):
            return kind
    return "chore"


def command(agent, job, workdir, run=False, kind=None):
    wd = str(Path(workdir or ROOT).resolve())
    if agent["provider"] == "codex":
        args = ["codex", "exec", "-m", agent["model"], "-C", wd, job]
        return args, shlex.join(args)
    if agent["provider"] == "grok":
        args = ["grok", "-p", "--model", agent["model"], "--cwd", wd]
        if run and kind == "build":
            args.append("--always-approve")
        args.append(job)
        return args, shlex.join(args)
    return None, f"Claude Agent tool, model {agent['model']} (Claude launches it)"


def available(agent_id, cfg, readings):
    agent = cfg["agents"][agent_id]
    if agent.get("blocked") or agent_id == "fable":
        return False, "blocked: Fable requires Jaron's prior approval"
    if agent_id in cfg.get("paused", []):
        return False, "paused in routing.json"
    meter = readings.get(agent.get("meter"), unknown())
    if meter.get("paused"):
        return False, "paused by its zero daily budget"
    limits = cfg.get("thresholds", {})
    for key, limit_key in (("used_pct_5h", "used_pct_5h"), ("used_pct_week", "used_pct_week")):
        value = meter.get(key)
        if value is not None and limit_key in limits and value > limits[limit_key]:
            return False, f"{key} {value}% exceeds {limits[limit_key]}%"
    return True, "under configured limits" if meter.get("used_pct_5h") is not None else "meter unknown; threshold cannot be checked"


def route(job, kind=None, workdir=None, run=False, fake_meters=None):
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    if any(word in job.lower() for word in ("trade", "trading", "bet", "wager", "polymarket")):
        raise RuntimeError("trading jobs are never routed by this tool")
    guessed = kind or guess_kind(job, cfg["kinds"])
    if guessed not in cfg["kinds"]:
        raise ValueError(f"unknown kind: {guessed}")
    readings = fake_meters if fake_meters is not None else meters()
    if guessed == "judgment":
        pick, why = "claude-opus", "judgment and orchestration stay with Claude Opus"
    else:
        pick = None
        why = ""
        for candidate in cfg["kinds"][guessed]["candidates"]:
            ok, reason = available(candidate, cfg, readings)
            if ok:
                pick, why = candidate, reason
                break
        if pick is None:
            raise RuntimeError(f"no available candidate for {guessed}")
    agent = cfg["agents"][pick]
    args, cmd = command(agent, job, workdir, run, guessed)
    print(f"Kind: {guessed}" + (" (explicit)" if kind else " (guessed)"))
    print(f"Pick: {agent['label']} - {why}")
    print("Meters:")
    for name in sorted({cfg["agents"][c].get("meter") for c in cfg["kinds"][guessed]["candidates"]}):
        print(f"  {name}: {json.dumps(readings.get(name, unknown()), ensure_ascii=False)}")
    print(f"Command: {cmd}")
    if run:
        if args is None:
            print("Claude is started by its parent agent; --run only starts Codex/Grok.")
        else:
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            run_dir = ROOT / "state" / "route-runs"
            run_dir.mkdir(parents=True, exist_ok=True)
            log = run_dir / f"{stamp}-{pick}.log"
            with log.open("w", encoding="utf-8") as fh:
                subprocess.Popen(args, cwd=workdir or ROOT, stdout=fh, stderr=subprocess.STDOUT,
                                 creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
                                 start_new_session=(os.name != "nt"))
            with (ROOT / "state" / "route-log.md").open("a", encoding="utf-8") as fh:
                fh.write(f"{datetime.now(timezone.utc).isoformat()} | {job.replace('|', '/')} | {guessed} | {agent['label']} | {why}\n")
            print(f"Started in background; log: {log}")
    return pick


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("job")
    ap.add_argument("--kind", choices=["looks", "build", "chore", "research", "judgment"])
    ap.add_argument("--dir", dest="workdir")
    ap.add_argument("--run", action="store_true")
    ns = ap.parse_args()
    try:
        route(ns.job, ns.kind, ns.workdir, ns.run)
    except (ValueError, RuntimeError) as exc:
        print(f"route: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
