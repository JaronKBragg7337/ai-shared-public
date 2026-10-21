import urllib.request, json
def get(url):
    return json.loads(urllib.request.urlopen(url, timeout=20).read().decode())
out = []
for d in ["20261010", "20261011"]:
    data = get(f"http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard?dates={d}&limit=300")
    for ev in data.get("events", []):
        name = (ev.get("name") or "") + (ev.get("shortName") or "")
        if any(x in name for x in ["Boise", "Fresno", "Hawaii", "Hawai'i", "Arizona State"]):
            comp = ev["competitions"][0]
            st = comp["status"]["type"]
            teams = " ".join(
                f"{t['team']['abbreviation']}{t['score']}"
                for t in sorted(comp["competitors"], key=lambda x: 0 if x.get("homeAway") == "away" else 1)
            )
            out.append(f"{d} {ev.get('shortName')} | {st.get('detail')} | {teams} | {st.get('state')} id={ev['id']}")
            for t in comp["competitors"]:
                out.append(f"  side {t.get('homeAway')} {t['team']['abbreviation']}")
            try:
                sd = get(f"https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event={ev['id']}")
                wpa = sd.get("winprobability") or []
                if wpa:
                    last = wpa[-1]
                    out.append(f"  WP home={last.get('homeWinPercentage')} away={last.get('awayWinPercentage')}")
                else:
                    out.append("  no WP")
            except Exception as e:
                out.append(f"  WP err {e}")
text = "\n".join(out)
print(text)
open(r"C:\Users\lilli\AI-Shared\state\_satya_espn_out.txt", "w", encoding="utf-8").write(text)
