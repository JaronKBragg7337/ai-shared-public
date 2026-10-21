#!/usr/bin/env python3
"""
score-estimates.py - grades every estimate in state/scout-estimates.md once its market resolves.

WHY
    Jaron, 2026-09-11: "We can't judge till we have enough data." This is the judging. Every
    researcher (split / direct / scout / qwen) writes its number to scout-estimates.md at the
    time; this comes back later, looks up how the market actually settled, and scores it.
    Brier score: (p - outcome)^2, lower is better, 0.25 = coin-flip guessing.

WHAT IT WRITES
    state/scout-scores.md - one table per method, plus the per-estimate rows it scored.
    Re-run any time; it re-scores everything (idempotent).

USAGE
    runtime\\polymarket-us-agent-venv\\Scripts\\python.exe tools\\score-estimates.py
"""

from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from datetime import datetime

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
EST = os.path.join(ROOT, "state", "scout-estimates.md")
OUT = os.path.join(ROOT, "state", "scout-scores.md")

LINE = re.compile(r"^(\d{4}-\d\d-\d\d \d\d:\d\d)Z \| (\S+) \| (\S+) \| p=([\d.]+) \| (\w+) \| ask=([\d.]+) \| (\w+) \| ends (\S+)")


def resolved_outcome(client, slug):
    """1.0 if the long side won, 0.0 if it lost, None if not settled yet."""
    try:
        r = client.markets.list({"slug": [slug]})
        m = (r.get("markets") or [None])[0]
    except Exception:
        return None
    if not m or not m.get("closed"):
        return None
    prices = m.get("outcomePrices") or []
    outcomes = m.get("outcomes") or []
    long_side = next((sd.get("description") for sd in m.get("marketSides", []) if sd.get("long")), None)
    try:
        if long_side and long_side in outcomes:
            v = float(prices[outcomes.index(long_side)])
        else:
            v = float(prices[0])
    except (ValueError, IndexError, TypeError):
        return None
    if v >= 0.99:
        return 1.0
    if v <= 0.01:
        return 0.0
    return None      # closed but not cleanly settled (voided / 50-50)


def main():
    from polymarket_us import PolymarketUS
    c = PolymarketUS(timeout=30.0)
    if not os.path.exists(EST):
        print("no estimates yet"); return
    rows = []
    for line in open(EST, encoding="utf-8"):
        m = LINE.match(line.strip())
        if m:
            rows.append({"at": m.group(1), "slug": m.group(2), "method": m.group(3), "p": float(m.group(4)),
                         "conf": m.group(5), "ask": float(m.group(6)), "decision": m.group(7), "ends": m.group(8)})
    cache, scored = {}, []
    for r in rows:
        if r["slug"] not in cache:
            cache[r["slug"]] = resolved_outcome(c, r["slug"])
        o = cache[r["slug"]]
        if o is None:
            continue
        r["outcome"] = o
        r["brier"] = (r["p"] - o) ** 2
        r["market_brier"] = (r["ask"] - o) ** 2      # what the price at the time would have scored
        scored.append(r)
    by = defaultdict(list)
    for r in scored:
        by[r["method"]].append(r)
    lines = [f"# Scout scores - written {datetime.now().strftime('%Y-%m-%d %H:%M')} by tools/score-estimates.py",
             "", f"{len(rows)} estimates on file, {len(scored)} resolved so far. Brier: lower is better; 0.25 = guessing.",
             "The 'market' column is what the price at the time would have scored - the bar to beat.", "",
             "| method | n | brier | market brier | beat the market? |", "|---|---|---|---|---|"]
    for meth, lst in sorted(by.items()):
        b = sum(x["brier"] for x in lst) / len(lst)
        mb = sum(x["market_brier"] for x in lst) / len(lst)
        lines.append(f"| {meth} | {len(lst)} | {b:.3f} | {mb:.3f} | {'YES' if b < mb else 'no'} |")
    lines += ["", "## Scored estimates", "", "| when | slug | method | p | conf | ask | outcome | brier |", "|---|---|---|---|---|---|---|---|"]
    for r in sorted(scored, key=lambda x: x["at"]):
        lines.append(f"| {r['at']} | {r['slug']} | {r['method']} | {r['p']:.2f} | {r['conf']} | {r['ask']:.2f} | {int(r['outcome'])} | {r['brier']:.3f} |")
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join(lines[:12]))


if __name__ == "__main__":
    main()
