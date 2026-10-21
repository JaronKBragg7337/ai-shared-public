import sys, json, subprocess
sys.path.insert(0, r"C:\Users\lilli\AI-Shared\tools")
import executor as X
m = X.Mcp()
slugs = [
    "aec-cfb-aubrn-tenn-2026-10-03",
    "aec-cfb-ohio-kentst-2026-10-03",
    "aec-cfb-pur-ill-2026-10-03",
    "aec-cfb-lou-ncst-2026-10-03",
    "aec-cfb-oregst-colst-2026-10-03",
    "aec-cfb-cah-unlv-2026-10-03",
    "aec-cfb-mary-nebr-2026-10-03",
    "aec-cfb-uk-sc-2026-10-03",
    "aec-cfb-vir-flst-2026-10-03",
    "tsc-cfb-alaam-jackst-2026-10-03-total-51pt5",
    "tsc-cfb-alaam-jackst-2026-10-03-total-52pt5",
]
print("---BBO---")
for s in slugs:
    bid, ask, short = X.best_ask(m, s)
    print(s, "bid", bid, "ask", ask, "short", short)

print("---DRY---")
runs = [
    # exit Auburn NO to lock ~99
    ["--slug", "aec-cfb-aubrn-tenn-2026-10-03", "--side", "no", "--size", "10", "--exit",
     "--why", "LOCK: TENN24-AUB14 2:00 4Q ESPN TENN WP99.1 Tigers ask~0.01; close #1046 near settle",
     "--kill", "already exiting"],
    # Ohio exit if book still open
    ["--slug", "aec-cfb-ohio-kentst-2026-10-03", "--side", "yes", "--size", "10", "--exit",
     "--why", "FINAL OHIO13-KENT10 settled win; exit #1035/#1039/#1044 if book still open",
     "--kill", "already exiting"],
    # PUR YES
    ["--slug", "aec-cfb-pur-ill-2026-10-03", "--side", "yes", "--size", "10",
     "--why", "PUR16-ILL7 ~12:09 4Q ESPN PUR WP79.7 vs Boilermakers ask check gap",
     "--kill", "ILL ties/leads or PUR WP<60"],
    # LOU NO fade
    ["--slug", "aec-cfb-lou-ncst-2026-10-03", "--side", "no", "--size", "10",
     "--why", "LOU28-NCSU31 ~3:03 4Q ESPN NCSU WP89.5 vs Cardinals ask check fade",
     "--kill", "LOU leads or NCSU WP<70"],
    # ORST
    ["--slug", "aec-cfb-oregst-colst-2026-10-03", "--side", "yes", "--size", "5",
     "--why", "ORST14-CSU7 E1Q ESPN ORST WP67.6 vs Beavers ask check",
     "--kill", "CSU ties/leads"],
]
py = r"C:\Users\lilli\AI-Shared\tools\desk-trade.py"
for args in runs:
    cmd = [sys.executable, py, "--by", "grok-bot/satya-twin", "--dry-run"] + args
    print("CMD", " ".join(args[:6]))
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    out = (p.stdout or "") + (p.stderr or "")
    print(out[-800:])
    print("====")
