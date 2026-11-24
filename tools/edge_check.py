"""Edge vs outcome (Jaron 10/22, from RYY's trading log idea): do the traders' own estimates mean anything?
Reads the Supabase view edge_check (placed trades that carried a --p estimate, joined to their settlement) and writes
state/edge-check.md: per edge bucket, how many trades, what they estimated, how often they actually won, and the money.
Runs weekly (task "Edge Check", Mondays 6 AM). Small samples say little - the table shows the count so nobody over-reads it."""
import os, json, urllib.request, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
env = {}
for l in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8"):
    if "=" in l and not l.startswith("#"): k, v = l.strip().split("=", 1); env[k] = v.strip()
key = env["SUPABASE_SERVICE_ROLE_KEY"]
req = urllib.request.Request(env["SUPABASE_URL"].rstrip("/") + "/rest/v1/edge_check?select=*&order=edge_bucket",
                             headers={"apikey": key, "Authorization": "Bearer " + key})
rows = json.loads(urllib.request.urlopen(req, timeout=30).read())
order = ["15+ points", "8-15 points", "0-8 points", "negative"]
rows.sort(key=lambda r: order.index(r["edge_bucket"]) if r["edge_bucket"] in order else 9)
total = sum(r["trades"] for r in rows)
lines = [f"# Edge vs outcome - {datetime.date.today()} (tools/edge_check.py, weekly)", "",
         "Settled trades where the trader gave its own probability (--p). Edge = its estimate minus the price paid.",
         f"Sample: {total} trades. Under ~100 this is a hint, not proof.", "",
         "| Edge the trader claimed | Trades | Its average estimate | Actually won | Average price | Money |",
         "|---|---|---|---|---|---|"]
for r in rows:
    lines.append(f"| {r['edge_bucket']} | {r['trades']} | {float(r['avg_estimate']):.0%} | {float(r['won_rate']):.0%} | "
                 f"{float(r['avg_price']):.2f} | ${float(r['pnl_usd']):+.2f} |")
lines += ["", "Read it: if 'Actually won' tracks 'Its average estimate', the estimates are honest. If big-edge trades don't win",
          "more than small-edge ones, the edge numbers are noise. Only about 1 in 4 trades carries --p today."]
open(os.path.join(ROOT, "state", "edge-check.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))
