import json, urllib.request
eid = "401856715"
sj = json.load(urllib.request.urlopen(
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=%s" % eid,
    timeout=12))
c = (sj.get("header", {}).get("competitions") or [{}])[0]
comps = c.get("competitors") or []
detail = c.get("status", {}).get("type", {}).get("detail", "")
scores = " ".join("%s=%s" % (x["team"]["abbreviation"], x.get("score")) for x in comps)
wp = sj.get("winprobability") or []
hwp = wp[-1].get("homeWinPercentage") if wp else None
home = next(x for x in comps if x["homeAway"] == "home")
away = next(x for x in comps if x["homeAway"] == "away")
print(detail, scores, "home", home["team"]["abbreviation"], hwp, "away", away["team"]["abbreviation"], None if hwp is None else 1-float(hwp))
# also TEX
eid2 = "401856717"
sj2 = json.load(urllib.request.urlopen(
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=%s" % eid2,
    timeout=12))
c2 = (sj2.get("header", {}).get("competitions") or [{}])[0]
comps2 = c2.get("competitors") or []
detail2 = c2.get("status", {}).get("type", {}).get("detail", "")
scores2 = " ".join("%s=%s" % (x["team"]["abbreviation"], x.get("score")) for x in comps2)
wp2 = sj2.get("winprobability") or []
hwp2 = wp2[-1].get("homeWinPercentage") if wp2 else None
home2 = next(x for x in comps2 if x["homeAway"] == "home")
away2 = next(x for x in comps2 if x["homeAway"] == "away")
print(detail2, scores2, "home", home2["team"]["abbreviation"], hwp2, "away", away2["team"]["abbreviation"], None if hwp2 is None else 1-float(hwp2))
# TENN
eid3 = "401856713"
sj3 = json.load(urllib.request.urlopen(
    "https://site.api.espn.com/apis/site/v2/sports/football/college-football/summary?event=%s" % eid3,
    timeout=12))
c3 = (sj3.get("header", {}).get("competitions") or [{}])[0]
comps3 = c3.get("competitors") or []
detail3 = c3.get("status", {}).get("type", {}).get("detail", "")
scores3 = " ".join("%s=%s" % (x["team"]["abbreviation"], x.get("score")) for x in comps3)
wp3 = sj3.get("winprobability") or []
hwp3 = wp3[-1].get("homeWinPercentage") if wp3 else None
print("TENN", detail3, scores3, "ARK WP", hwp3, "TENN WP", None if hwp3 is None else 1-float(hwp3))
