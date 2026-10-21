# News desks on heartbeatobservatory.com/social (Jaron 10/17: "Make the desks").
# Three AI accounts (label "AI") post today's Heartbeat News stories one at a time, in our own words, linked to the real outlets:
#   First Light Desk  - Asia, Middle East, Russia, Africa, Pacific (the other side of the world)
#   Wire Desk         - breaking, markets, tech, A.I., cyber, space, science
#   Watch Desk        - everything else (US, world, health, people, sports, weather)
# Accounts are named after OUR desks, never after an outlet (no impersonation). One post per run; the task runs hourly
# 8 AM-10 PM, so the feed fills through the day without one account flooding it (X's own ranker halves repeat authors).
#   pythonw desk_posts.py [--dry]        state: state/desk-posts.json   log: state/social-posts.log
import sys, os, json, ast, datetime, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import social_daily as sd

AI = "C:/Users/lilli/AI-Shared"
STATE = AI + "/state/desk-posts.json"
ACCTS = json.load(open(AI + "/state/desk-accounts.json"))
DRY = "--dry" in sys.argv
EAST = ("MIDDLE EAST", "ASIA", "CHINA", "RUSSIA", "KOREA", "JAPAN", "INDIA", "PAKISTAN", "AFRICA", "PACIFIC", "OCEANIA", "IRAN",
        "YEMEN", "ISRAEL", "GAZA", "TAIWAN", "SAUDI", "SEOUL", "TOKYO", "BEIJING", "UKRAINE")
WIRE = ("MARKET", "BUSINESS", "ECONOM", "OIL", "CRYPTO", "TECH", "A.I", "AI", "CHIP", "CYBER", "SPACE", "SCIENCE")


def parse(v):
    if isinstance(v, str):
        try: return ast.literal_eval(v)
        except Exception: return v
    return v


def desk_for(g):
    cat = (g.get("category") or "").upper()
    words = set(cat.replace("/", " ").replace(",", " ").split())
    if any(w.startswith(k) for w in words for k in WIRE): return "wiredesk"   # whole words ("UKRAINE" is not "AI"); category decides first
    if any(k in cat for k in EAST): return "firstlight"
    if cat in ("WORLD", "WORLD NEWS", "INTERNATIONAL") and any(k in (g.get("headline") or "").upper() for k in EAST): return "firstlight"
    if g.get("kind") == "breaking": return "wiredesk"
    return "watchdesk"


def text_for(g):
    gr = parse(g.get("graphic")) or {}
    bullets = [b for b in (gr.get("bullets") if isinstance(gr, dict) else []) or [] if b][:3]
    src = [s for s in (parse(g.get("sources")) or []) if isinstance(s, dict) and s.get("url")][:3]
    lines = [g.get("headline", "").strip()]
    lines += ["- " + b for b in bullets]
    if g.get("status") in ("claim", "mixed"): lines.append("Some of this is a claim, not confirmed - who said what is in the sources.")
    if src: lines += ["", "Sources:"] + [f"{s.get('name', 'source')}: {s['url']}" for s in src]
    lines += ["", "On today's Heartbeat News: https://www.heartbeatobservatory.com/news/"]
    return "\n".join(lines)[:2000]


def post_as(uid, text):
    if DRY: return "dry"
    e = sd.env(); k = e["SUPABASE_SERVICE_ROLE_KEY"]
    body = json.dumps({"author_id": uid, "body": text}).encode()
    urllib.request.urlopen(urllib.request.Request(e["SUPABASE_URL"].rstrip("/") + "/rest/v1/posts", data=body, method="POST",
        headers={"apikey": k, "Authorization": "Bearer " + k, "Content-Type": "application/json", "Prefer": "return=minimal"}), timeout=30).read()
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


def main():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    idx = json.loads(urllib.request.urlopen("https://www.heartbeatobservatory.com/news/episodes/index.json", timeout=30).read())
    if idx.get("latest") != today: sd.log(f"desks: today's episode not out yet (latest {idx.get('latest')})"); return
    ep = json.loads(urllib.request.urlopen(f"https://www.heartbeatobservatory.com/news/episodes/{today}.json", timeout=30).read())
    stories = [g for g in ep.get("segments", []) if g.get("kind") in ("story", "breaking", "weather", "sports") and g.get("headline")]
    try: st = json.load(open(STATE))
    except Exception: st = {}
    done = st.setdefault(today, {})
    last = st.get("_last_desk")
    todo = [g for g in stories if g.get("id", g["headline"]) not in done]
    if not todo: sd.log("desks: all of today's stories are posted"); return
    # rotate: prefer a story whose desk didn't post last time
    pick = next((g for g in todo if desk_for(g) != last), todo[0])
    desk = desk_for(pick)
    when = post_as(ACCTS[desk], text_for(pick))
    done[pick.get("id", pick["headline"])] = {"desk": desk, "at": when}
    st["_last_desk"] = desk
    for d in [d for d in st if not d.startswith("_") and d < today][:-7]: st.pop(d)   # keep a week
    if not DRY: json.dump(st, open(STATE, "w"), indent=1)
    sd.log(f"desks: {desk} posted '{pick['headline']}'" + (" (dry)" if DRY else ""))
    if DRY: print(text_for(pick))


if __name__ == "__main__":
    try: main()
    except Exception as e: sd.log(f"desks CRASH {e}")
