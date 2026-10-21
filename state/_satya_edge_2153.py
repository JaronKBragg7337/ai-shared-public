import json, urllib.request, ssl, subprocess
ctx = ssl.create_default_context()
H = {"User-Agent": "Mozilla/5.0"}

def get(u):
    req = urllib.request.Request(u, headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=25, context=ctx).read())

sb = get("https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?groups=80&limit=200")
keys = ("ohio", "kent", "toledo", "ball", "auburn", "tennessee", "purdue", "illinois", "maryland", "nebraska", "louisville", "nc state", "virginia", "florida state", "cal", "unlv", "bowling", "miami (oh", "marshall", "eastern michigan")
for e in sb.get("events", []):
    name = e.get("name", "")
    low = name.lower()
    if not any(k in low for k in keys):
        continue
    comp = e["competitions"][0]
    st = comp["status"]["type"]
    status = st.get("detail") or st.get("description")
    state = st.get("state")
    rows = [(c.get("homeAway"), c["team"].get("abbreviation"), c.get("score")) for c in comp["competitors"]]
    print(state, "|", status, "|", name, "|", rows, "| id", e.get("id"))

# dry-run books for Satya open + candidates
probes = [
    ("aec-cfb-aubrn-tenn-2026-10-03", "no"),
    ("aec-cfb-ohio-kentst-2026-10-03", "yes"),
    ("aec-cfb-fl-missr-2026-10-03", "no"),  # FLA YES is 0.09, so NO FLA ~0.90? wait FLA trailing - NO Florida = bet Missouri
    ("aec-cfb-ohiost-iowa-2026-10-03", "yes"),
    ("aec-cfb-pur-ill-2026-10-03", "yes"),
]
print("---DRY---")
for slug, side in probes:
    p = subprocess.run(
        ["python", r"C:\Users\lilli\AI-Shared\tools\desk-trade.py",
         "--by", "grok-bot/satya-twin", "--slug", slug, "--side", side,
         "--size", "10", "--why", "probe", "--kill", "probe", "--dry-run"],
        capture_output=True, text=True, timeout=90,
    )
    out = (p.stdout or "") + (p.stderr or "")
    print("PROBE", slug, side)
    print(out[:500])
    print()
