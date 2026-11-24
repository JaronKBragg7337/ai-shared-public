"""Upload each *-short.mp4 to Postiz and schedule it on the YouTube channel (public, #Shorts). usage: python post_shorts.py <hours_between> [start_iso]"""
import json, os, subprocess, sys, datetime, re
from plans import PLANS
P = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) if False else None
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(os.path.dirname(HERE)); ROOT = os.path.dirname(PROJ)
YT = "cmvcfuzny1h5ulu0yl77gu5vj"
ORDER = ["coral", "dark", "gob", "ai", "earth", "mmx", "vib", "hwy", "sci5", "sci6", "oq2", "oq3", "oq4", "h5", "an", "su4", "su5"]
QID = dict(coral="su-10.2-coral-castle", dark="su-10.1-dark-energy", gob="lp-22.1-gobekli", ai="ae-13.1-consciousness", earth="ea-17.1-oxygen",
           mmx="sn-11.1-mmx", vib="su-10.3-vibration-stone", hwy="sci-8.4-highway", sci5="sci-8.5-commercial-roof", sci6="sci-8.6-phobos",
           oq2="oq-9.2-no-brain", oq3="oq-9.3-birthplace", oq4="oq-9.4-gravity", h5="hist-7.5-1816", an="an-19.1-death", su4="su-10.4-voynich", su5="su-10.5-wow")
FIX = {"mmx": "Japan's MMX mission is heading to a moon of Mars. What for? \U0001F680\nIt plans to land on Phobos twice and bring at least 10 grams home in 2031. Here is what is known, what is planned, and what is still open.",
       "sci6": "Mars' moon Phobos is falling. \U0001F311\nIt laps Mars three times a day, slips 1.8 cm closer every year, and in a few tens of millions of years it becomes a ring or a crater field."}
q = {i["id"]: i for i in json.load(open(os.path.join(ROOT, "state", "social-queue.json"), encoding="utf8"))["shows"]}
hours = float(sys.argv[1]); t0 = datetime.datetime.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
only = sys.argv[3].split(",") if len(sys.argv) > 3 else ORDER
log = os.path.join(HERE, "posted.json"); posted = json.load(open(log)) if os.path.exists(log) else {}
def pz(*a):
    r = subprocess.run(["node", "C:/Users/lilli/AppData/Roaming/npm/node_modules/postiz/dist/index.js", *a], capture_output=True, text=True, encoding="utf8")
    if r.returncode: raise SystemExit("postiz failed: %s\n%s" % (a[:2], r.stdout[-800:] + r.stderr[-800:]))
    return r.stdout
def js(t): return json.loads(t[t.index("{"):])
for n, k in enumerate(ORDER):
    if k not in only or k in posted: continue
    pl = PLANS[k]; f = os.path.join(PROJ, pl["dir"], pl["out"]); it = q[QID[k]]
    cap = FIX.get(k) or it["caption"].split("\n\nFull episode")[0]
    body = cap + "\n\nFull episode + sources, free: heartbeatobservatory.com\nMade with AI by Heartbeat Observatory\n#Shorts " + " ".join(re.findall(r"#\w+", it["caption"].replace("#learnontiktok", "").replace("#sciencetok", "")))
    title = (it["title"] + " #Shorts")[:100]
    when = (t0 + datetime.timedelta(hours=hours * ORDER.index(k))).strftime("%Y-%m-%dT%H:%M:%S.000Z")
    up = js(pz("upload", f)); path = up["path"]
    out = pz("posts:create", "-c", body, "-s", when, "-i", YT, "-m", path, "--no-shortLink", "--settings", json.dumps({"title": title, "type": "public", "selfDeclaredMadeForKids": "no"}))
    print(k, when, out[-400:].replace("\n", " "))
    posted[k] = dict(when=when, title=title, out=out[-600:], media=path)
    json.dump(posted, open(log, "w"), indent=1); print(k, when, "ok")
