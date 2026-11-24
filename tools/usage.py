#!/usr/bin/env python3
"""
usage.py - read AI usage off the MSI's own disk so every agent can see it. No logins, no APIs.

WHY (Jaron, 2026-09-12): "I wonder if ... AIs can see it in real time?" For two of them, yes:
    Codex   writes its rate limits into every session log:  ~/.codex/sessions/**/rollout-*.jsonl
            -> "rate_limits": {"primary": {"used_percent": 70, "window_minutes": 300, "resets_at": ...},
                               "secondary": {"used_percent": 11, "window_minutes": 10080, ...}}
            That is the same number the phone shows (as USED; the app shows REMAINING).
    Claude  writes per-turn token counts into ~/.claude/projects/<project>/<session>.jsonl.
            The percentage is computed server-side and is NOT on disk, so this reports what can be
            measured: tokens in the last 5 h and 7 d, and the burn rate. Jaron's screenshots are
            the calibration - see state/usage-snapshots.md.
    Grok Bot / Grok app / ChatGPT phone: nothing on disk. Screenshots only.

OUTPUT
    state/usage-live.json  (machine)  and a one-line summary on stdout (human / desk.py).
    Run every 15 min by the Windows task 'Usage Snapshot'.
"""

from __future__ import annotations

import glob
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HOME = Path.home()
OUT = Path(__file__).resolve().parent.parent / "state" / "usage-live.json"

# Claude calibration: work tokens that corresponded to 100% of each window, derived from Jaron's
# /usage screenshots (state/usage-snapshots.md). 2026-09-12 12:50: 5h showed 55% at ~1.98M work
# tokens -> 3.6M per 100%; weekly showed 56% at ~48.5M -> 87M per 100%. Re-derive when a new
# screenshot disagrees by more than ~10 points. These are ESTIMATES, always labelled as such.
CLAUDE_5H_FULL = 3_600_000
CLAUDE_WEEK_FULL = 87_000_000


def tail_lines(path, nbytes=400_000):
    with open(path, "rb") as fh:
        fh.seek(0, 2)
        size = fh.tell()
        fh.seek(max(0, size - nbytes))
        return fh.read().decode("utf-8", "replace").splitlines()


def codex_session_files(home=HOME):
    """Shared discovery for the live meter and the daily ledger, oldest first."""
    found = []
    for path in (Path(home) / ".codex" / "sessions").rglob("rollout-*.jsonl"):
        try:
            found.append((path.stat().st_mtime_ns, path))
        except OSError:
            continue
    return [path for _, path in sorted(found)]


def _codex_counts(value):
    """Read only token fields; missing input/output means usage is unknown."""
    if not isinstance(value, dict):
        return None
    keys = ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens")
    counts = {}
    for key in keys:
        number = value.get(key)
        counts[key] = number if isinstance(number, int) and not isinstance(number, bool) and number >= 0 else None
    return counts if counts["input_tokens"] is not None and counts["output_tokens"] is not None else None


def codex_ledger_event(obj, state):
    """Normalize one rollout line for usage_ledger.py; state is safe to cache.

    Input includes cached tokens, and output includes reasoning tokens. Both
    token_usage_record and token_count describe the same running totals: emit
    only their increase, never add the last usage on top of a cumulative total.
    Raw prompt text is returned transiently, never retained in state. The caller
    must turn it into a safe label before writing reports or a cache.
    """
    if not isinstance(obj, dict) or not isinstance(obj.get("payload"), dict):
        return []
    payload = obj["payload"]
    kind = obj.get("type")
    timestamp = obj.get("timestamp")
    try:
        timestamp = datetime.fromisoformat(str(timestamp).replace("Z", "+00:00")).isoformat()
    except (TypeError, ValueError):
        timestamp = None
    events = []
    if kind == "session_meta":
        # Fork files include another session_meta inside copied parent history.
        if not state.get("session_seen"):
            state["session_seen"] = True
            own_id = payload.get("id")
            if isinstance(own_id, str) and re.fullmatch(r"[0-9a-fA-F-]{32,36}", own_id):
                state["session_id"] = own_id
            boundary = payload.get("subagent_history_start_ordinal")
            if isinstance(boundary, int) and boundary >= 0:
                state["history_boundary"] = boundary
            elif payload.get("forked_from_id"):
                state["fork_baseline_pending"] = True
            events.append({"type": "session", "timestamp": timestamp, "id": state.get("session_id")})
        return events

    # The first visible user prompt is useful even in copied fork history. A
    # later, readable child prompt replaces it; encrypted task bodies stay out.
    ordinal = obj.get("ordinal")
    inherited = isinstance(ordinal, int) and ordinal < state.get("history_boundary", 0)
    if (not state.get("prompt_seen") or state.get("prompt_inherited") and not inherited):
        text = None
        if kind == "response_item" and payload.get("type") == "message" and payload.get("role") == "user":
            content = payload.get("content")
            if isinstance(content, str):
                chunks = [content]
            elif isinstance(content, list):
                chunks = [block.get("text", "") for block in content if isinstance(block, dict)
                          and block.get("type") in ("input_text", "text")]
            else:
                chunks = []
            usable = [chunk for chunk in chunks if isinstance(chunk, str) and chunk.strip()
                      and not chunk.lstrip().startswith(("# AGENTS.md instructions", "<environment_context>",
                                                         "<permissions instructions>", "<INSTRUCTIONS>"))]
            text = "\n".join(usable)
        elif kind == "event_msg" and payload.get("type") == "user_message":
            text = payload.get("message")
        if isinstance(text, str) and text.strip():
            state["prompt_seen"] = True
            state["prompt_inherited"] = inherited
            events.append({"type": "prompt", "timestamp": timestamp, "text": text})
    if inherited:
        return events

    if kind == "turn_context":
        model = payload.get("model")
        if isinstance(model, str) and re.fullmatch(r"(?:gpt-|codex|o[1-9])[a-zA-Z0-9._/-]{0,80}", model):
            if model != state.get("model"):
                state["model"] = model
                events.append({"type": "model", "timestamp": timestamp, "model": model})
        return events

    total = last = None
    if kind == "token_usage_record":
        # Copied records can belong to another thread even in older fork logs.
        if payload.get("thread_id") and state.get("session_id") and payload["thread_id"] != state["session_id"]:
            return events
        total = _codex_counts(payload.get("thread_token_usage"))
        last = _codex_counts(payload.get("usage"))
    elif kind == "event_msg" and payload.get("type") == "token_count":
        info = payload.get("info")
        if isinstance(info, dict):
            total = _codex_counts(info.get("total_token_usage"))
            last = _codex_counts(info.get("last_token_usage"))
    if total is None:
        # Without cumulative totals or a response ID, repeat last-usage events
        # cannot be distinguished safely. Leave them unknown, not invented.
        return events
    previous = state.get("totals")
    state["totals"] = total
    if state.pop("fork_baseline_pending", False):
        return events
    if previous == total:
        return events
    if previous is None:
        delta = total
    elif any(total[key] < previous[key] for key in ("input_tokens", "output_tokens")):
        # Compaction/reset can lower counters. Only the logged latest response
        # is safe to charge here; the new total becomes the next baseline.
        state["counter_resets"] = state.get("counter_resets", 0) + 1
        if last is None:
            return events
        delta = last
    else:
        delta = {key: (max(0, value - previous[key]) if value is not None and previous.get(key) is not None else None)
                 for key, value in total.items()}
    if delta["input_tokens"] == 0 and delta["output_tokens"] == 0:
        return events
    events.append({"type": "usage", "timestamp": timestamp, "model": state.get("model", "unknown"),
                   "input_tokens": delta["input_tokens"], "cached_tokens": delta["cached_input_tokens"],
                   "output_tokens": delta["output_tokens"], "reasoning_tokens": delta["reasoning_output_tokens"],
                   "tokens_known": True})
    return events


def codex():
    files = codex_session_files()
    best = None
    for f in reversed(files[-8:]):
        for line in reversed(tail_lines(f)):
            if '"rate_limits"' not in line:
                continue
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            rl = None
            stack = [obj]
            while stack and rl is None:
                cur = stack.pop()
                if isinstance(cur, dict):
                    if "rate_limits" in cur and isinstance(cur["rate_limits"], dict):
                        rl = cur["rate_limits"]
                    else:
                        stack.extend(cur.values())
                elif isinstance(cur, list):
                    stack.extend(cur)
            if rl and rl.get("primary"):
                ts = obj.get("timestamp") or datetime.fromtimestamp(os.path.getmtime(f), timezone.utc).isoformat()
                best = {"read_from": os.path.basename(f), "as_of": ts,
                        "five_hour_used_pct": (rl.get("primary") or {}).get("used_percent"),
                        "five_hour_resets_at": _iso((rl.get("primary") or {}).get("resets_at")),
                        "weekly_used_pct": (rl.get("secondary") or {}).get("used_percent"),
                        "weekly_resets_at": _iso((rl.get("secondary") or {}).get("resets_at")),
                        "credits": rl.get("credits")}
                break
        if best:
            break
    return best or {"error": "no rate_limits found in recent Codex sessions"}



def codex_segments(max_files=12):
    """Per-session model segments from the Codex rollout files: which model ran, from when to when, and the
    5-hour / weekly % at the first and last rate-limit reading inside that segment. This is how a mid-job model
    switch (Astra -> Sol Light, Astra -> Luna) gets its own row in state/task-costs.jsonl without Jaron screenshotting
    the switch. Reads lines as text (some rollout lines are not single JSON objects)."""
    import re
    files = codex_session_files()[-max_files:]
    out = []
    for f in files:
        segs = []
        cur = None
        with open(f, "r", encoding="utf-8", errors="replace") as fh:
            for line in fh:
                ts = re.search(r'"timestamp":"([^"]+)"', line)
                ts = ts.group(1) if ts else None
                m = re.search(r'"model":"(gpt-[^"]+)"', line)
                if m:
                    model = m.group(1)
                    if cur is None or cur["model"] != model:
                        cur = {"model": model, "start": ts, "end": ts, "five_hour_pct": [None, None], "weekly_pct": [None, None]}
                        segs.append(cur)
                    else:
                        cur["end"] = ts or cur["end"]
                if cur is not None and '"rate_limits"' in line:
                    prim = re.search(r'"primary":\{[^}]*"used_percent":([0-9.]+)', line)
                    sec = re.search(r'"secondary":\{[^}]*"used_percent":([0-9.]+)', line)
                    if prim:
                        v = float(prim.group(1))
                        if cur["five_hour_pct"][0] is None: cur["five_hour_pct"][0] = v
                        cur["five_hour_pct"][1] = v
                    if sec:
                        v = float(sec.group(1))
                        if cur["weekly_pct"][0] is None: cur["weekly_pct"][0] = v
                        cur["weekly_pct"][1] = v
                    if ts: cur["end"] = ts
        if segs:
            for s in segs:
                a, b = s["five_hour_pct"]
                s["five_hour_spent_pts"] = round(b - a, 1) if (a is not None and b is not None and b >= a) else None
            out.append({"session": os.path.basename(f), "segments": segs,
                        "switched": len({s["model"] for s in segs}) > 1})
    return out

def _iso(epoch):
    try:
        return datetime.fromtimestamp(int(epoch), timezone.utc).isoformat()
    except (TypeError, ValueError, OSError):
        return None


def claude():
    files = glob.glob(str(HOME / ".claude" / "projects" / "*" / "*.jsonl"))
    now = time.time()
    five_h, week = now - 5 * 3600, now - 7 * 86400
    tot5 = totw = 0
    out5 = outw = 0
    turns5 = turnsw = 0
    latest = 0.0
    for f in files:
        if os.path.getmtime(f) < week:
            continue
        try:
            with open(f, "r", encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    if '"usage"' not in line:
                        continue
                    try:
                        obj = json.loads(line)
                    except ValueError:
                        continue
                    ts = obj.get("timestamp")
                    try:
                        t = datetime.fromisoformat(str(ts).replace("Z", "+00:00")).timestamp()
                    except (TypeError, ValueError):
                        continue
                    u = (obj.get("message") or {}).get("usage") or obj.get("usage")
                    if not isinstance(u, dict):
                        continue
                    # what the server bills against the window is dominated by output + uncached input;
                    # cache reads are cheap. Count "work" as output + input + cache_creation.
                    work = int(u.get("output_tokens", 0)) + int(u.get("input_tokens", 0)) + int(u.get("cache_creation_input_tokens", 0))
                    if t >= week:
                        totw += work; outw += int(u.get("output_tokens", 0)); turnsw += 1; latest = max(latest, t)
                    if t >= five_h:
                        tot5 += work; out5 += int(u.get("output_tokens", 0)); turns5 += 1
        except OSError:
            continue
    return {"note": "Claude's window % is server-side; these are tokens measured from local logs across Chat/Cowork/Code sessions on this machine, and the % is an ESTIMATE calibrated from Jaron's screenshots (state/usage-snapshots.md).",
            "as_of": datetime.fromtimestamp(latest, timezone.utc).isoformat() if latest else None,
            "five_hour": {"turns": turns5, "work_tokens": tot5, "output_tokens": out5,
                          "est_used_pct": round(100.0 * tot5 / CLAUDE_5H_FULL, 1)},
            "week": {"turns": turnsw, "work_tokens": totw, "output_tokens": outw,
                     "est_used_pct": round(100.0 * totw / CLAUDE_WEEK_FULL, 1)}}


def main():
    snap = {"read_at": datetime.now(timezone.utc).isoformat(), "codex": codex(), "codex_segments": codex_segments(), "claude": claude(),
            "not_visible": ["grok-bot", "grok-app", "chatgpt-phone"]}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(snap, fh, indent=1)
    c, k = snap["codex"], snap["claude"]
    if "error" in c:
        cs = c["error"]
    else:
        # Codex only writes rate limits when it runs; if the 5h reset time has passed since the last
        # session, the window has rolled over and the true figure is ~0% until Codex runs again.
        try:
            rolled = datetime.fromisoformat(c["five_hour_resets_at"]) < datetime.now(timezone.utc)
        except (TypeError, ValueError):
            rolled = False
        if rolled:
            c["five_hour_used_pct_note"] = "window reset since last Codex session; effectively fresh"
            cs = f"5h window RESET at {str(c['five_hour_resets_at'])[11:16]}Z (last reading {c['five_hour_used_pct']}% before it) | weekly {c['weekly_used_pct']}% used (resets {str(c['weekly_resets_at'])[:10]})"
        else:
            cs = f"5h {c['five_hour_used_pct']}% used (resets {str(c['five_hour_resets_at'])[11:16]}Z) | weekly {c['weekly_used_pct']}% used (resets {str(c['weekly_resets_at'])[:10]})"
    print(f"CODEX  {cs}")
    print(f"CLAUDE ~{k['five_hour']['est_used_pct']}% of 5h used (est., {k['five_hour']['work_tokens']:,} work tokens / {k['five_hour']['turns']} turns) | ~{k['week']['est_used_pct']}% of week (est.)")
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
