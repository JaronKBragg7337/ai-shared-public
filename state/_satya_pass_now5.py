import urllib.request, json

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def show(label, url, keys):
    print("===", label, "===")
    try:
        data = get(url)
    except Exception as e:
        print("ERR", e)
        return
    evs = data.get("events") or []
    print("events", len(evs))
    for ev in evs:
        name = ev.get("name") or ev.get("shortName") or ""
        comp = (ev.get("competitions") or [{}])[0]
        status = (comp.get("status") or {}).get("type", {})
        detail = status.get("detail") or status.get("description") or ""
        state = status.get("state")
        comps = comp.get("competitors") or []
        bits = []
        for c in comps:
            t = c.get("team", {})
            ab = t.get("abbreviation") or t.get("shortDisplayName") or "?"
            p = (c.get("probability") or {}).get("winPercentage")
            s = f"{ab}={c.get('score')}"
            if p is not None:
                try:
                    pf = float(p)
                    s += f" WP={pf if pf > 1 else round(pf * 100, 1)}"
                except Exception:
                    s += f" WP={p}"
            bits.append(s)
        line = " / ".join(bits) + f" | {state} {detail} | {name}"
        low = line.lower()
        if any(k in low for k in keys) or state == "in":
            tag = "HIT" if any(k in low for k in keys) else "LIVE"
            print(f"{tag}: {line}")

base = "https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
keys = ["pitt", "virginia", "hokie", "penn", "northwestern", "liberty", "delaware", "montana", "idaho", "bobcat", "nittany"]
for u in [base, base + "?dates=20261002", base + "?dates=20261003", base + "?groups=80"]:
    show(u.replace(base, "cfb"), u, keys)

print("=== soccer ===")
for label, url in [
    ("cnl", "https://site.api.espn.com/apis/site/v2/sports/soccer/concacaf.nations.league/scoreboard"),
    ("friendly", "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.friendly/scoreboard"),
]:
    show(label, url, ["jamaica", "suriname", "guatemala", "colombia", "paraguay", "martinique", "honduras", "salvador"])
