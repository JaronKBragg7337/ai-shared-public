import urllib.request, json
# NFL scoreboard via ESPN CDN sometimes works with UA
urls = [
 "https://cdn.espn.com/core/nfl/scoreboard?xhr=1&limit=100",
 "https://site.web.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard",
]
for u in urls:
  try:
    req = urllib.request.Request(u, headers={"User-Agent":"Mozilla/5.0"})
    raw = urllib.request.urlopen(req, timeout=15).read()
    d = json.loads(raw)
    ev = d.get("content", d).get("sbData", d).get("events") or d.get("events") or []
    if not ev and "scoreboard" in d.get("content", {}):
      ev = d["content"]["scoreboard"].get("events", [])
    print("URL", u, "events", len(ev))
    for e in ev:
      c = e["competitions"][0]
      teams = sorted(c["competitors"], key=lambda x: x["homeAway"], reverse=True)
      s = " - ".join(f"{t['team']['abbreviation']} {t.get('score','?')}" for t in teams)
      print(f"{e.get('shortName')} | {s} | {c['status']['type']['detail']}")
  except Exception as ex:
    print("FAIL", u, type(ex).__name__, ex)
