import json, os, glob
base = r"C:\Users\lilli\AI-Shared"
# recent trail lines mentioning satya
paths = [
    os.path.join(base, "state", "desk-trade.md"),
]
for p in paths:
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        hit = [ln.rstrip() for ln in lines if "satya" in ln.lower()][-15:]
        print("=== satya trail (last 15) ===")
        for ln in hit:
            print(ln[:300])
# open positions files
for pat in ["*position*", "*positions*", "*book*", "*ledger*"]:
    for p in glob.glob(os.path.join(base, "state", pat)):
        print("FILE", p)
# tools that list open
for name in ["desk-open.py", "desk-book.py", "desk-positions.py", "live-board.py", "desk-status.py"]:
    p = os.path.join(base, "tools", name)
    print("TOOL", name, "EXISTS" if os.path.exists(p) else "missing")
