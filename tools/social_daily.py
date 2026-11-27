# Company socials, every day, no human steps (Jaron 10/17: "any new show made gets posted on all social medias, and the news every day").
#   pythonw social_daily.py news   - today's Heartbeat News headlines short -> TikTok, YouTube (Short), X       (task ~8:00 AM, after the 7 AM show)
#   pythonw social_daily.py show   - the next show in state/social-queue.json -> every platform it isn't on yet  (task ~6:00 PM)
#   add --dry  to print what would post without posting.
# Posts go through Postiz (hosted, its approved TikTok/YouTube/X apps); the Postiz CLI must be signed in (postiz auth:login) with the
# three company channels connected. Log: state/social-posts.log.
# 11/24: when a platform has no door (Postiz gave us no channel there and our own keys are not on file) the log says so once a
#   day and Jaron gets ONE buzz when that begins, not one a day. Our own site still gets every post, also with no outside door at all.
# 11/24 (Postiz's $29 was declined): a second door, our own posting straight to X and YouTube (tools/direct_post.py).
#   state/social-path.json says which door each platform uses, e.g. {"x": "direct", "youtube": "direct", "tiktok": "paused"}:
#     "postiz" (the default, also with no file) = Postiz while it still has the channel; the day Postiz drops it, our own door
#                takes over by itself, if its keys are on file.     "direct" = our own door.     "paused" = skip that platform.
#   add --direct to send X and YouTube through our own door for this run (with --dry it prints the exact requests, sends nothing).
#   TikTok has no door of our own (its posting API needs an app TikTok has reviewed), so without Postiz it is paused.
import sys, os, json, subprocess, datetime, urllib.request, shutil, tempfile, hashlib
from zoneinfo import ZoneInfo

AI = "C:/Users/lilli/AI-Shared"; SITE = "C:/Users/lilli/Projects/heartbeat-observatory"
QUEUE = AI + "/state/social-queue.json"; LOG = AI + "/state/social-posts.log"
YOUTUBE_VERIFIED = True    # Jaron verified the channel 2026-10-19 8:24 AM (lifts the 15-min upload cap)
YOUTUBE_DAILY_CAP = 3  # 11/12: back to 3. Pip's reports: the 5 PM show upload already failed ~15 times (Oct 29-Nov 11) on YouTube's daily limit even at 3, so the real Postiz/YouTube allowance is lower. Shorts backfill paused until fixed.
PACIFIC = ZoneInfo("America/Los_Angeles")  # YouTube API quota resets at midnight Pacific.
X_MAX = 3 * 3600 - 60  # Premium on @HeartbeatObserv since 10/17 (was 139 s without it); longer videos get a trimmed copy for X only
DRY = "--dry" in sys.argv
# node + the CLI script directly (not the .cmd shim: cmd.exe mangles line breaks and emoji in captions)
POSTIZ = [shutil.which("node") or "node", os.path.expandvars(r"%APPDATA%\npm\node_modules\postiz\dist\index.js")]
NOW = datetime.datetime.now()
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
NOWIN = 0x08000000   # CREATE_NO_WINDOW: no console flashes from the scheduled task (10/16 rule)
PATH_FILE = AI + "/state/social-path.json"   # which door each platform uses (see the top of this file)
FORCE_DIRECT = "--direct" in sys.argv
POSTIZ_HAS = {}   # the channels Postiz has right now; the fallback when our own door fails before anything was sent
SHUT = []         # the platforms with no door at all in this run (filled by route(); a platform set to "paused" is not in it)


def log(m):
    line = NOW.strftime("%Y-%m-%d %H:%M ") + m
    open(LOG, "a", encoding="utf-8").write(line + "\n"); print(line, flush=True)


def env():
    d = {}
    for l in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8"):
        if "=" in l and not l.lstrip().startswith("#"):
            k, v = l.strip().split("=", 1); d[k] = v.strip().strip('"')
    return d


def once_a_day(key):
    flag = os.path.join(tempfile.gettempdir(), "social_daily_" + key + NOW.strftime("%Y%m%d"))
    if os.path.exists(flag): return False
    open(flag, "w").close(); return True


def buzz(msg, once_key):
    """One plain line to Jaron's phone, at most once a day per key. True if it went out."""
    if not once_a_day(once_key): return False
    try:
        topic = env().get("NTFY_TOPIC")
        if topic:
            urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/" + topic, data=msg.encode(), method="POST"), timeout=20)
            return True
    except Exception: pass
    return False


def pz(*args):
    r = subprocess.run([*POSTIZ, *args], capture_output=True, text=True, encoding="utf-8", timeout=900, creationflags=NOWIN)
    out = (r.stdout or "") + (r.stderr or "")
    i = min([k for k in (out.find("{"), out.find("[")) if k >= 0], default=-1)   # the CLI prints a header line before the JSON
    try: return json.loads(out[i:]) if i >= 0 else out
    except Exception: return out


def channels():
    """{'tiktok': id, 'youtube': id, 'x': id} for the connected company channels, or {} if Postiz isn't signed in."""
    got = pz("integrations:list")
    if not isinstance(got, list): return {}
    m = {}
    for it in got:
        ident = (it.get("identifier") or it.get("providerIdentifier") or "").lower()
        if it.get("disabled"): continue
        key = "x" if ident in ("x", "twitter") else ("tiktok" if ident.startswith("tiktok") else ident)
        if key in ("tiktok", "youtube", "x"): m[key] = it["id"]
    return m


def said(ps):
    """['tiktok', 'x'] -> 'X and TikTok'"""
    l = [{"x": "X", "youtube": "YouTube", "tiktok": "TikTok"}[p] for p in ("x", "youtube", "tiktok") if p in ps]
    return ", ".join(l[:-1]) + " and " + l[-1] if len(l) > 1 else "".join(l)


def route(ch):
    """Which door each platform uses: {platform: its Postiz channel id, or "direct" for our own door (tools/direct_post.py)}.
    ch = what Postiz has right now ({} when Postiz is off). A platform with no usable door is left out, so it is skipped,
    and it is named in SHUT."""
    import direct_post as D
    try: path = json.load(open(PATH_FILE, encoding="utf-8"))
    except Exception: path = {}
    POSTIZ_HAS.clear(); POSTIZ_HAS.update({p: c for p, c in ch.items() if c != "dry"})
    out = {}; SHUT.clear()
    for p in ("tiktok", "youtube", "x"):
        ours = p != "tiktok" and (DRY or D.have(D.X_KEYS if p == "x" else D.YT_KEYS))   # is our own door ready for it?
        want = "direct" if FORCE_DIRECT and p != "tiktok" else path.get(p, "postiz")
        if want == "paused":
            if not DRY and once_a_day("paused-" + p): log(f"{p}: paused in state/social-path.json - skipped")
        elif want == "direct" and ours: out[p] = "direct"
        elif p in ch:
            out[p] = ch[p]
            if want == "direct" and not DRY and once_a_day("notready-" + p): log(f"{p}: our own door is not ready (keys missing) - still using Postiz")
        elif ours:
            out[p] = "direct"
            if not DRY and once_a_day("failover-" + p): log(f"{p}: Postiz no longer has this channel - using our own door (tools/direct_post.py)")
        else: SHUT.append(p)
    if SHUT and not DRY and once_a_day("nodoor-" + "-".join(SHUT)):
        why = []
        if "x" in SHUT or "youtube" in SHUT: why.append("our own keys for " + said([p for p in SHUT if p != "tiktok"]) + " are not on file (one-time sign-ins: RECONNECT.md part 13)")
        if "tiktok" in SHUT: why.append("TikTok has no door of our own (its posting API needs a reviewed app)")
        log("no door today for " + said(SHUT) + ": Postiz gave us no channel there (lapsed, cancelled, signed out or down); " + "; ".join(why))
    return out


def doors_report(ch):
    """Tell Jaron ONCE when a platform loses its door, and note in the log when it has one again. What he was told is kept in
    state/direct-post.json ("shut"). Before 11/24 the job stopped when Postiz gave no channels, so our own site feed went quiet
    too, and it buzzed every day to reconnect Postiz: wrong advice once Postiz is let go on purpose."""
    import direct_post as D
    s = D.state(); told = dict(s.get("shut") or {})
    back = [p for p in told if p not in SHUT]
    new = [p for p in SHUT if p not in told]
    for p in back: del told[p]
    if [p for p in back if p in ch]: log("a door is back for " + said([p for p in back if p in ch]))
    sent = False
    if new:
        fix = []
        if "youtube" in SHUT: fix.append("YouTube: the free one-time sign-in, about 10 minutes (RECONNECT.md part 13 A)")
        if "x" in SHUT: fix.append("X: the X keys, about $5 of X credits once (part 13 B)")
        if "tiktok" in SHUT: fix.append("TikTok: no door of our own yet")
        msg = (f"Socials: no post goes to {said(SHUT)} right now. Postiz gave us no channel there (lapsed, cancelled or signed out). "
               + (f"{said(list(ch))} and our own site still get every post. " if ch else "Our own site still gets every post. ")
               + ". ".join(fix) + ". You get this once, not every day.")
        sent = buzz(msg, "nodoor-" + "-".join(new))
        if sent:
            for p in new: told[p] = NOW.strftime("%Y-%m-%d %H:%M")
            log("told Jaron once: no door for " + said(new))
    if back or sent:
        s["shut"] = told; D.save_state(s)


def duration(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f], capture_output=True, text=True, creationflags=NOWIN)
    try: return float(r.stdout.strip())
    except Exception: return 0.0


def cover_copy(f):
    """TikTok takes the FIRST frame as the cover (10/19: the Earth 17.1 cover was a dark brown square because the episode fades in
    from black). If the first frame is dark, put a 0.3 s still of the brightest early frame (the title card) in front."""
    try:
        def lum(t):
            r = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", str(t), "-i", f, "-frames:v", "1", "-vf", "scale=32:-1,format=gray", "-f", "rawvideo", "-"],
                               capture_output=True, creationflags=NOWIN).stdout
            return sum(r) / max(len(r), 1)
        if lum(0) > 40: return f
        best = max((1.0, 2.0, 3.0, 4.0, 6.0), key=lum)
        out = os.path.join(tempfile.gettempdir(), "tt_" + os.path.basename(f))
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(best), "-i", f, "-i", f, "-filter_complex",
                        "[0:v]trim=end_frame=1,loop=loop=8:size=1,setpts=N/FRAME_RATE/TB,fps=30[c];[1:v]fps=30[m];[c][m]concat=n=2:v=1:a=0[v];"
                        "anullsrc=r=48000:cl=stereo,atrim=duration=0.3[s];[1:a]aresample=48000[ma];[s][ma]concat=n=2:v=0:a=1[a]",
                        "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20", "-c:a", "aac", "-movflags", "+faststart", out], check=True, creationflags=NOWIN)
        return out
    except Exception:
        return f


def x_copy(f):
    if duration(f) <= X_MAX: return f
    out = os.path.join(tempfile.gettempdir(), "x_" + os.path.basename(f))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-t", str(X_MAX), "-i", f, "-vf", "fade=t=out:st=%d:d=1.5" % (X_MAX - 1.5),
                    "-af", "afade=t=out:st=%d:d=1.5" % (X_MAX - 1.5), "-c:v", "libx264", "-crf", "21", "-c:a", "aac", "-movflags", "+faststart", out], check=True, creationflags=NOWIN)
    return out


def fetch(url):
    out = os.path.join(tempfile.gettempdir(), os.path.basename(url.split("?")[0]))
    urllib.request.urlretrieve(url, out); return out


def settings_for(p, title):
    # Checked against `postiz integrations:settings` 10/17 (saved: state/postiz-settings-tiktok.txt). TikTok: DIRECT_POST publishes
    # (UPLOAD only drops it in the inbox); video_made_with_ai = TikTok's AI label (Jaron's rule, 10/13); title max 90.
    if p == "tiktok":
        return {"title": title[:90], "content_posting_method": "DIRECT_POST", "privacy_level": "PUBLIC_TO_EVERYONE", "duet": True,
                "stitch": True, "comment": True, "autoAddMusic": "no", "brand_content_toggle": False, "brand_organic_toggle": False,
                "video_made_with_ai": True}
    if p == "youtube":
        return {"title": title[:100], "type": "public", "selfDeclaredMadeForKids": "no"}
    return {"post_type": "post", "who_can_reply_post": "everyone", "made_with_ai": True}


def x_limit(cid):
    """X's post length for this channel as Postiz knows it (280 free; long posts once Postiz sees the checkmark, 10/23)."""
    try: return int((pz("integrations:settings", cid).get("output") or {}).get("maxLength") or 280)
    except Exception: return 280


def x_text(text, tags=None, limit=280):
    """X post: the hook, cut at a whole sentence (never mid-word), then where to watch. No hashtags by default - Jaron 10/19 +
    Grok check: X's ranking doesn't use them (Musk 12/2024 "please stop using hashtags"); they only file a post under a search
    tag. A queue item can keep a few with "x_tags" when people search that exact event (MMX launch day)."""
    import re
    NL = chr(10)
    lines = [l for l in text.split(NL) if l.strip()]
    keep = [l for l in lines[1:] if not l.startswith(("Full", "Watch", "Made", "#"))]
    body = NL.join([lines[0]] + (keep if limit > 280 else keep[:1]))   # verified account: the whole story, not just the hook
    tail = NL + NL + "Full show + sources, free: link in our bio" + (NL + " ".join(tags) if tags else "")   # Postiz strips links on X
    room = limit - 40 - len(tail)   # 40 spare: emoji count 2 on X (10/18 "too long" at 280)
    if len(body) > room:
        cut = [m.end() for m in re.finditer(r"[.?!]['\")]?(?=\s|$)", body) if m.end() <= room]
        body = body[:cut[-1]] if cut else body[:room].rsplit(" ", 1)[0] + "…"
    return body.rstrip() + tail


def youtube_room(cid, news_short=False):
    """Count Postiz uploads/attempts for this Pacific day; fail closed if unavailable.

    Reserve one slot for the daily news short until it has been scheduled. Other
    upload tools and other channels sharing a Google project are outside this cap.
    """
    now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=3)
    day = now.astimezone(PACIFIC).date()
    start = datetime.datetime.combine(day, datetime.time.min, PACIFIC).astimezone(datetime.timezone.utc)
    end = datetime.datetime.combine(day + datetime.timedelta(days=1), datetime.time.min, PACIFIC).astimezone(datetime.timezone.utc)
    result = pz("posts:list", "--startDate", start.isoformat(), "--endDate", (end - datetime.timedelta(milliseconds=1)).isoformat())
    if not isinstance(result, dict) or not isinstance(result.get("posts"), list):
        raise RuntimeError("YouTube cap: cannot check Postiz schedule; deferred")
    posts = [p for p in result["posts"] if (p.get("integration") or {}).get("id") == cid
             and p.get("state") in ("QUEUE", "PUBLISHED", "ERROR")
             and start <= datetime.datetime.fromisoformat(p["publishDate"].replace("Z", "+00:00")) < end]
    has_news = any((p.get("content") or "").startswith("Heartbeat News for ")
                   and "Two AI anchors" not in (p.get("content") or "") for p in posts)
    reserved = 0 if news_short or has_news else 1
    if len(posts) + reserved >= YOUTUBE_DAILY_CAP:
        raise RuntimeError(f"YouTube cap: {len(posts)} attempts/scheduled, {reserved} news slot reserved; deferred")


def next_pacific_early():
    """11/17: Postiz's YouTube uploads fail every afternoon/evening ET with 'daily upload quota exhausted' (19 errors
    Oct 26-Nov 17, all at ~5 PM or ~10 PM ET) while the early-morning ones (7:15 ET = 4:15 AM PT) never fail, so the shared
    quota runs out during the Pacific day. Show uploads to YouTube are scheduled for 12:20 AM Pacific, right after the reset."""
    now_pt = datetime.datetime.now(datetime.timezone.utc).astimezone(PACIFIC)
    t = datetime.datetime.combine(now_pt.date() + datetime.timedelta(days=1), datetime.time(0, 20), PACIFIC)
    return t.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def post(platform, cid, video, text, title, x_tags=None, news_short=False, early=False):
    if cid == "direct":   # our own door: straight to X / YouTube, right away. In a dry run it prints the exact requests, sends nothing.
        import direct_post as D
        D.COMMITTED = False
        D.SAFETY_NET = not DRY and platform in POSTIZ_HAS   # for our door's own mail to the AIs: is Postiz still behind a failed start?
        try:
            if platform == "x": D.x_post(x_text(text, x_tags, D.X_TEXT_LIMIT), video, dry=DRY)
            else: D.yt_upload(video, title, text, category="25" if news_short else "22", dry=DRY)   # 25 = News & Politics (11/26)
            return "dry" if DRY else datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        except Exception as e:
            # While Postiz still has the channel it is the safety net, but only if our door stopped BEFORE the one request
            # that makes the post exist (D.COMMITTED), so nothing can go out twice.
            if DRY or D.COMMITTED or platform not in POSTIZ_HAS: raise
            log(f"{platform}: our own door failed before anything was sent ({str(e)[:160]}) - using Postiz this time")
            cid = POSTIZ_HAS[platform]
    if DRY:
        preview = x_text(text, x_tags) if platform == "x" else (text if platform == "youtube" and title.endswith(" #Shorts") else text[:60])
        log(f"DRY {platform}: {os.path.basename(video)} | {title} | " + preview.replace(chr(10), " / ")); return "dry"
    if platform == "youtube":
        # Serialize this script's news/show runs through the check and creation.
        import msvcrt
        with open(os.path.join(tempfile.gettempdir(), "hb-social-youtube.lock"), "a+b") as lock:
            lock.seek(0)
            msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)
            try:
                youtube_room(cid, news_short=news_short)
                return post_uploaded(platform, cid, video, text, title, x_tags, when=next_pacific_early() if early else None)
            finally:
                lock.seek(0)
                msvcrt.locking(lock.fileno(), msvcrt.LK_UNLCK, 1)
    return post_uploaded(platform, cid, video, text, title, x_tags)


def post_uploaded(platform, cid, video, text, title, x_tags=None, when=None):
    up = pz("upload", video)
    path = up.get("path") if isinstance(up, dict) else None
    if not path: raise RuntimeError(f"upload failed: {str(up)[:300]}")
    when = when or (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    if platform == "x": text = x_text(text, x_tags, x_limit(cid))
    r = pz("posts:create", "-c", text, "-m", path, "-s", when, "-i", cid, "--settings", json.dumps(settings_for(platform, title)))
    # 10/18: a rejected X post came back as a dict {statusCode: 400, message: "post is too long"} and was logged "OK"
    if isinstance(r, dict) and (r.get("statusCode", 200) >= 400 or r.get("error")): raise RuntimeError(str(r)[:300])
    if isinstance(r, str) and ("rror" in r or "fail" in r.lower() or "statusCode" in r): raise RuntimeError(r[:300])
    return when


def first_run_schema(ch):
    flag = AI + "/state/postiz-settings-schema.json"
    if os.path.exists(flag): return
    json.dump({p: pz("integrations:settings", cid) for p, cid in ch.items()}, open(flag, "w"), indent=1)
    log("saved Postiz settings schema -> state/postiz-settings-schema.json (check the TikTok AI-label key name)")


SITE_ACCOUNT = "2d8c79fd-8aee-432e-a543-6e87350fbce4"   # @heartbeatobservatory, the Official account on heartbeatobservatory.com/social (10/17)


def site_post(text):
    """Post to our own social page as the Official account (Jaron 10/17: the feed should never look dead)."""
    if DRY:
        log("DRY site: " + text[:80].replace(chr(10), " / ")); return "dry"
    e = env(); url = e["SUPABASE_URL"].rstrip("/") + "/rest/v1/posts"; k = e["SUPABASE_SERVICE_ROLE_KEY"]
    body = json.dumps({"author_id": SITE_ACCOUNT, "author_handle": "heartbeatobservatory", "body": text[:2000]}).encode()
    urllib.request.urlopen(urllib.request.Request(url, data=body, method="POST", headers={"apikey": k, "Authorization": "Bearer " + k,
                           "Content-Type": "application/json", "Prefer": "return=minimal"}), timeout=30).read()
    return NOW.strftime("%Y-%m-%d %H:%M")



def site_video_file(path):
    """Upload a stable public copy of the clip; fall back to a frame for oversized clips."""
    if DRY: return "https://example.com/dry.mp4"
    e = env(); key = e["SUPABASE_SERVICE_ROLE_KEY"]
    def upload(source, kind):
        with open(source, "rb") as f: data = f.read()
        name = "social/" + hashlib.sha256(data).hexdigest() + (".jpg" if kind == "image/jpeg" else ".mp4")
        base = e["SUPABASE_URL"].rstrip("/") + "/storage/v1/object/"
        req = urllib.request.Request(base + "news-video/" + name, data=data, method="POST", headers={"apikey": key, "Authorization": "Bearer " + key, "Content-Type": kind, "x-upsert": "true"})
        urllib.request.urlopen(req, timeout=180).read()
        return base + "public/news-video/" + name
    if os.path.getsize(path) <= 49 * 1024 * 1024:
        try: return upload(path, "video/mp4")
        except Exception as exc: log("site video upload failed; using poster: " + str(exc)[:120])
    poster = os.path.join(tempfile.gettempdir(), "social-poster-" + hashlib.sha256(path.encode()).hexdigest()[:16] + ".jpg")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "2", "-i", path, "-frames:v", "1", poster], check=True, creationflags=NOWIN)
    return upload(poster, "image/jpeg")


def site_media_text(text, url):
    if not url or not url.startswith("https://") or not url.lower().split("?")[0].endswith((".mp4", ".jpg", ".jpeg", ".png", ".webp")):
        raise ValueError("site media must be a public video or image URL")
    marker = "\n\nMedia: " + url
    return text[:2000-len(marker)] + marker

def site_text(caption, link):
    """The platform caption with a real clickable link (our own page links are fine here)."""
    out = [l for l in caption.split(chr(10)) if not l.startswith(("Full episode", "Full show", "Watch free"))]
    while out and not out[-1].strip(): out.pop()
    tags = out.pop() if out and out[-1].startswith("#") else ""
    return chr(10).join(out).rstrip() + chr(10) + chr(10) + "Watch it free: " + link + (chr(10) + tags if tags else "")


def do_news(q, ch):
    news_index = env()["SUPABASE_URL"].rstrip("/") + "/storage/v1/object/public/news-video/index.json"
    idx = json.loads(urllib.request.urlopen(news_index + "?t=" + NOW.strftime("%H%M%S"), timeout=30).read())
    today = NOW.strftime("%Y-%m-%d")
    ep = next((e for e in idx.get("episodes", []) if e["date"] == today), None)
    if not ep or not ep.get("short"): log(f"news: no short for {today} yet - skipped"); return
    done = q.setdefault("news_done", {}).setdefault(today, {})
    tl = json.loads(urllib.request.urlopen(ep["timing"], timeout=30).read()) if ep.get("timing") else {}
    head = ""
    try:
        import ast
        g = tl["segments"][0]["graphic"]; g = ast.literal_eval(g) if isinstance(g, str) else g; head = g.get("title", "")
    except Exception: pass
    day = NOW.strftime("%A, %B %#d")
    text = (f"Heartbeat News for {day}. 📰\n{head}.\n\nFull show + every source, free: heartbeatobservatory.com/news\n"
            "Made with AI by Heartbeat Observatory · AI Robot Vex and Alien Joe are characters\n#news #worldnews #dailynews #AI")
    title = f"Heartbeat News, {day}: {head}"[:100]
    short = fetch(ep["short"])
    for p in q["news"]["platforms"]:
        if p in done or p not in ch: continue
        try: done[p] = post(p, ch[p], x_copy(short) if p == "x" else short, text, title, news_short=(p == "youtube")); log(f"news {today} -> {p} " + ("(dry)" if DRY else "OK"))
        except Exception as e: log(f"news {today} -> {p} FAILED: {e}")
    if "site" not in done:
        try: done["site"] = site_post(site_media_text(site_text(text, "https://www.heartbeatobservatory.com/news/"), ep["short"])); log(f"news {today} -> site OK")
        except Exception as e: log(f"news {today} -> site FAILED: {e}")
    # the whole show as a regular YouTube video (Jaron 10/17: Shorts hook people, the full video is where they watch it all).
    # Made on the MSI by make_vertical.py: H logo, the full 16:9 show, the cream card.
    full = f"C:/Users/lilli/Projects/necklace-unreal/NewsAudio/{today}/vertical/youtube.mp4"
    # YouTube caps unverified channels at 15 min (10/17: the 20-min show "Upload failed: Video too long" even though Postiz
    # said published). Set YOUTUBE_VERIFIED = True once the channel is verified at youtube.com/verify.
    if os.path.exists(full) and not YOUTUBE_VERIFIED and duration(full) > 15 * 60 - 5:
        if "youtube_full" not in done: log(f"news {today} -> youtube FULL skipped: {duration(full) / 60:.0f} min, channel not verified (15 min cap)")
        done["youtube_full"] = "skipped (unverified, over 15 min)"
    if "youtube_full" not in done and "youtube" in ch and os.path.exists(full):
        stories = [g.get("headline", "") for g in tl.get("segments", []) if g.get("kind") in ("story", "breaking") and g.get("headline")]
        desc = (f"Heartbeat News for {day}. Two AI anchors, AI Robot Vex and Alien Joe, read the day's news from captures by several "
                "AIs on both sides of the world. Every source is linked on the site.\n\nIn this show:\n"
                + "".join(f"- {h}\n" for h in stories[:25])
                + "\nFull rundown + every source, free: heartbeatobservatory.com/news\nNew show every day by 8 AM Eastern.\n"
                "Made with AI by Heartbeat Observatory. Vex and Joe are characters.\n#news #worldnews #AI")
        try: done["youtube_full"] = post("youtube", ch["youtube"], full, desc, f"Heartbeat News, full show: {day}"); log(f"news {today} -> youtube FULL " + ("(dry)" if DRY else "OK"))
        except Exception as e: log(f"news {today} -> youtube FULL FAILED: {e}")


def tiktok_fill(q, ch, skip_id):
    """Today's show was already on TikTok, so post the next show that never went there (Jaron 10/27: TikTok gets
    something every day). If every show is already on TikTok, log it so a TikTok-only promo gets made."""
    for o in q["shows"]:
        if o["id"] == skip_id or "tiktok" in o.get("done", {}): continue
        f = os.path.join(SITE, o["file"])
        if not os.path.exists(f): continue
        try: o.setdefault("done", {})["tiktok"] = post("tiktok", ch["tiktok"], f if DRY else cover_copy(f), o["caption"], o["title"], o.get("x_tags")); log(f"show {o['id']} -> tiktok (fill) " + ("(dry)" if DRY else "OK"))
        except Exception as e: log(f"show {o['id']} -> tiktok (fill) FAILED: {e}")
        return
    log("tiktok fill: every queued show is already on TikTok - make a TikTok-only promo (site commercial)")


def show_short_file(show):
    source = os.path.join(SITE, show["file"])
    stem, _ = os.path.splitext(source)
    return stem + "-short.mp4"


def ensure_show_short(show):
    """Make this show's missing cut on demand, or leave it retryable if it fails."""
    short = show_short_file(show)
    if os.path.isfile(short): return True
    if DRY:
        log(f"DRY show {show['id']}: would make {short}")
        return True  # post() only prints during a dry run
    try:
        cutter = os.path.join(os.path.dirname(os.path.abspath(__file__)), "make_short_cuts.py")
        result = subprocess.run([sys.executable, cutter, "--id", show["id"]], capture_output=True,
                                text=True, encoding="utf-8", errors="replace", timeout=3600, creationflags=NOWIN)
        if result.returncode or not os.path.isfile(short):
            details = (result.stderr or result.stdout).strip()[-500:]
            log(f"show {show['id']} -> youtube SHORT cut failed: {details or 'no output file'}")
            return False
        log(f"show {show['id']}: made youtube SHORT cut")
        return True
    except (OSError, subprocess.SubprocessError) as e:
        log(f"show {show['id']} -> youtube SHORT cut failed: {e}")
        return False


def post_show_short(show, ch, backfill=False, cut_ready=False):
    """Post an existing or newly made cut; failures stay eligible for a later run."""
    short = show_short_file(show)
    if not cut_ready and not ensure_show_short(show): return False
    title = show["title"][:92].rstrip() + " #Shorts"  # keep the suffix within YouTube's 100-character limit
    caption = show["caption"].rstrip() + "\n\nFull episode on the channel + heartbeatobservatory.com"
    try:
        result = post("youtube", ch["youtube"], short, caption, title)
        show.setdefault("done", {})["youtube_short"] = result
        log(f"show {show['id']} -> youtube SHORT" + (" (backfill)" if backfill else "") + (" (dry)" if DRY else " OK"))
        return True
    except Exception as e:
        log(f"show {show['id']} -> youtube SHORT FAILED: {e}")
        return False


def backfill_show_short(q, ch, eligible):
    return  # 11/12 paused: YouTube daily limit already hit at 3/day (Pip). Re-enable after the limit is understood.
    """At most one previously published show's Short per Pacific day, oldest upload first."""
    if "youtube" not in ch: return
    day = datetime.datetime.now(datetime.timezone.utc).astimezone(PACIFIC).date().isoformat()
    if q.get("youtube_short_backfill_day") == day: return
    # Queue order isn't publication order; existing YouTube timestamps begin with ISO dates.
    candidates = sorted((s for s in eligible if "youtube_short" not in s.get("done", {})),
                        key=lambda s: s["done"]["youtube"])
    for s in candidates:
        if not ensure_show_short(s):
            continue  # a missing or too-short source must not block all later shows
        if post_show_short(s, ch, backfill=True, cut_ready=True):
            q["youtube_short_backfill_day"] = day
        return  # one attempt, including when quota is full


def do_show(q, ch):
    today = NOW.strftime("%Y-%m-%d")
    # Capture existing uploads before this run; a new upload's own Short is separate from backfill.
    eligible = [s for s in q["shows"] if "youtube" in s.get("done", {}) and "youtube_short" not in s.get("done", {})]
    for s in q["shows"]:
        if s.get("not_before", "") > today: continue
        todo = [p for p in ("tiktok", "youtube", "x") if p not in s.get("done", {}) and p in ch]
        if "site" not in s.get("done", {}) and (todo or not s.get("done")):
            todo.append("site")
        if not todo: continue
        f = os.path.join(SITE, s["file"])
        if not os.path.exists(f): log(f"show {s['id']}: file missing {s['file']} - skipped"); continue
        for p in todo:
            if p == "site":
                try: s.setdefault("done", {})["site"] = site_post(site_media_text(site_text(s["caption"], s.get("link", "https://www.heartbeatobservatory.com/tv/")), site_video_file(f))); log(f"show {s['id']} -> site OK")
                except Exception as e: log(f"show {s['id']} -> site FAILED: {e}")
                continue
            try:
                video = f if DRY else (x_copy(f) if p == "x" else (cover_copy(f) if p == "tiktok" else f))
                s.setdefault("done", {})[p] = post(p, ch[p], video, s["caption"], s["title"], s.get("x_tags"), early=(p == "youtube"))
                log(f"show {s['id']} -> {p} " + ("(dry)" if DRY else "OK"))
                if False and p == "youtube" and "youtube_short" not in s["done"]:   # 11/12 paused (YouTube daily limit)
                    post_show_short(s, ch)
            except Exception as e: log(f"show {s['id']} -> {p} FAILED: {e}")
        if "tiktok" in ch and "tiktok" not in todo and "tiktok" in s.get("done", {}):
            tiktok_fill(q, ch, s["id"])   # Jaron 10/27: TikTok never skips a day
        backfill_show_short(q, ch, eligible)
        return   # one show a day
    held = [s for s in q["shows"] if s.get("not_before", "") <= today and [p for p in SHUT if p not in s.get("done", {})]]
    log("show: queue is empty - add new shows to state/social-queue.json"
        + (f" ({len(held)} show{'s' if len(held) > 1 else ''} still wait{'' if len(held) > 1 else 's'} for a door to {said(SHUT)})" if held else ""))
    backfill_show_short(q, ch, eligible)


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "news"
    ch = route({"tiktok": "dry", "youtube": "dry", "x": "dry"} if DRY else channels())
    if not DRY:
        doors_report(ch)
        postiz = {p: c for p, c in ch.items() if c != "direct"}
        if postiz: first_run_schema(postiz)
    # With no outside door at all the run goes on: our own site still gets its post (Jaron 10/17: the feed should never look dead).
    q = json.load(open(QUEUE, encoding="utf-8"))
    (do_news if what == "news" else do_show)(q, ch)
    if not DRY: json.dump(q, open(QUEUE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    try: main()
    except Exception as e: log(f"CRASH {e}")

