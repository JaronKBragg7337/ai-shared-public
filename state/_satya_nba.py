import urllib.request, json
data=json.loads(urllib.request.urlopen("http://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard", timeout=15).read().decode())
for ev in data.get("events",[]):
  comp=ev["competitions"][0]; st=comp["status"]["type"]
  if st.get("state")!="in": continue
  teams=" ".join(f"{t['team']['abbreviation']}{t['score']}" for t in sorted(comp["competitors"], key=lambda x:0 if x.get("homeAway")=="away" else 1))
  print(ev.get("shortName"), "|", st.get("detail"), "|", teams, "id", ev["id"])
  for t in comp["competitors"]:
    print(" ", t.get("homeAway"), t["team"]["abbreviation"])
  try:
    sd=json.loads(urllib.request.urlopen(f"https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={ev['id']}", timeout=12).read().decode())
    wpa=sd.get("winprobability") or []
    if wpa:
      last=wpa[-1]
      print(" WP", {k:last.get(k) for k in ("homeWinPercentage","awayWinPercentage","tiePercentage") if k in last or True})
      print(" keys", list(last.keys())[:15])
  except Exception as e:
    print(" err", e)
