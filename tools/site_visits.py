# Who visited heartbeatobservatory.com (Vercel Web Analytics, read with VERCEL_TOKEN from keys.env).
#   python site_visits.py [days=7]     -> visitors/pageviews by day, top pages, where they came from, devices
# 10/17: the Vercel connector tool says "Web Analytics not found"; the REST API with our own token works (as on 9/24).
import sys, os, json, datetime, urllib.request, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import settings as S

TOKEN = S._env()["VERCEL_TOKEN"]; P = "prj_orgo96MzBTVphGIchOjNz5qMAZyh"; T = "team_wRRkvds3StkwIDpMebzrXSdA"
days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
until = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
since = until - datetime.timedelta(days=days + 1)
fmt = lambda d: d.strftime("%Y-%m-%dT00:00:00Z")


def q(path, **kw):
    kw.update(projectId=P, teamId=T, since=fmt(since), until=fmt(until))
    url = "https://api.vercel.com/v1/query/web-analytics/visits/" + path + "?" + urllib.parse.urlencode(kw, doseq=True)
    return json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"Authorization": "Bearer " + TOKEN}), timeout=30).read())


def rows(by, limit=10):
    d = q("aggregate", by=by, limit=limit).get("data", [])
    return d if isinstance(d, list) else d.get("groups", d.get("rows", []))


tot = q("count")["data"]
print(f"Last {days} days: {tot.get('visitors')} visitors, {tot.get('pageviews')} page views")
for title, by in (("By day", "day"), ("Top pages", "requestPath"), ("Came from", "referrerHostname"), ("Devices", "deviceType"), ("Countries", "country")):
    print("\n" + title + ":")
    for r in rows(by, 12):
        k = r.get(by) or r.get("key") or r.get("group") or next((str(v)[:10] for kk, v in r.items() if kk not in ("visitors", "pageviews") and v), None) or "(direct / none)"
        print(f"  {str(k)[:48]:48} {r.get('visitors', '')} visitors  {r.get('pageviews', '')} views")

# Heartbeat TV: what actually played (our own anonymous tally, table tv_watches - 10/17)
try:
    e = S._env(); k = e["SUPABASE_SERVICE_ROLE_KEY"]
    url = e["SUPABASE_URL"].rstrip("/") + "/rest/v1/tv_watches?select=ch,title,seconds&at=gte." + fmt(since) + "&limit=5000"
    w = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"apikey": k, "Authorization": "Bearer " + k}), timeout=30).read())
    agg = {}
    for r in w:
        a = agg.setdefault((r["ch"], r["title"]), [0, 0]); a[0] += 1; a[1] += r["seconds"]
    print(f"\nHeartbeat TV ({len(w)} plays):")
    for (ch, t), (n, s) in sorted(agg.items(), key=lambda x: -x[1][1])[:15]:
        print(f"  CH {ch:6} {t[:40]:40} {n} plays  {s // 60} min watched")
except Exception as ex:
    print("\nHeartbeat TV tally unavailable:", ex)
