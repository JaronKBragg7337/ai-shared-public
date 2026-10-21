# Company socials, every day, no human steps (Jaron 10/17: "any new show made gets posted on all social medias, and the news every day").
#   pythonw social_daily.py news   - today's Heartbeat News headlines short -> TikTok, YouTube (Short), X       (task ~8:00 AM, after the 7 AM show)
#   pythonw social_daily.py show   - the next show in state/social-queue.json -> every platform it isn't on yet  (task ~6:00 PM)
#   add --dry  to print what would post without posting.
# Posts go through Postiz (hosted, its approved TikTok/YouTube/X apps); the Postiz CLI must be signed in (postiz auth:login) with the
# three company channels connected. Log: state/social-posts.log. If Postiz isn't ready, one ntfy buzz a day says so, nothing else.
import sys, os, json, subprocess, datetime, urllib.request, shutil, tempfile

AI = "C:/Users/lilli/AI-Shared"; SITE = "C:/Users/lilli/Projects/heartbeat-observatory"
QUEUE = AI + "/state/social-queue.json"; LOG = AI + "/state/social-posts.log"
YOUTUBE_VERIFIED = True    # Jaron verified the channel 2026-10-19 8:24 AM (lifts the 15-min upload cap)
X_MAX = 3 * 3600 - 60  # Premium on @HeartbeatObserv since 10/17 (was 139 s without it); longer videos get a trimmed copy for X only
DRY = "--dry" in sys.argv
# node + the CLI script directly (not the .cmd shim: cmd.exe mangles line breaks and emoji in captions)
POSTIZ = [shutil.which("node") or "node", os.path.expandvars(r"%APPDATA%\npm\node_modules\postiz\dist\index.js")]
NOW = datetime.datetime.now()
try: sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception: pass
NOWIN = 0x08000000   # CREATE_NO_WINDOW: no console flashes from the scheduled task (10/16 rule)


def log(m):
    line = NOW.strftime("%Y-%m-%d %H:%M ") + m
    open(LOG, "a", encoding="utf-8").write(line + "\n"); print(line, flush=True)


def env():
    d = {}
    for l in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8"):
        if "=" in l and not l.lstrip().startswith("#"):
            k, v = l.strip().split("=", 1); d[k] = v.strip().strip('"')
    return d


def buzz(msg, once_key):
    flag = os.path.join(tempfile.gettempdir(), "social_daily_" + once_key + NOW.strftime("%Y%m%d"))
    if os.path.exists(flag): return
    open(flag, "w").close()
    try:
        topic = env().get("NTFY_TOPIC")
        if topic: urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/" + topic, data=msg.encode(), method="POST"), timeout=20)
    except Exception: pass


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


def x_text(text, tags=None):
    """X post: the hook, cut at a whole sentence (never mid-word), then where to watch. No hashtags by default - Jaron 10/19 +
    Grok check: X's ranking doesn't use them (Musk 12/2024 "please stop using hashtags"); they only file a post under a search
    tag. A queue item can keep a few with "x_tags" when people search that exact event (MMX launch day)."""
    import re
    NL = chr(10)
    lines = [l for l in text.split(NL) if l.strip()]
    body = lines[0] + (NL + lines[1] if len(lines) > 1 and not lines[1].startswith(("Full", "Watch", "Made", "#")) else "")
    tail = NL + NL + "Full show + sources, free: link in our bio" + (NL + " ".join(tags) if tags else "")   # Postiz strips links on X
    room = 240 - len(tail)   # shorter while the account is under review; emoji count 2 on X (10/18 "too long" at 280)
    if len(body) > room:
        cut = [m.end() for m in re.finditer(r"[.?!]['\")]?(?=\s|$)", body) if m.end() <= room]
        body = body[:cut[-1]] if cut else body[:room].rsplit(" ", 1)[0] + "…"
    return body.rstrip() + tail


def post(platform, cid, video, text, title, x_tags=None):
    if DRY:
        log(f"DRY {platform}: {os.path.basename(video)} | {title} | " + (x_text(text, x_tags) if platform == "x" else text[:60]).replace(chr(10), " / ")); return "dry"
    up = pz("upload", video)
    path = up.get("path") if isinstance(up, dict) else None
    if not path: raise RuntimeError(f"upload failed: {str(up)[:300]}")
    when = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    if platform == "x": text = x_text(text, x_tags)
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
        try: done[p] = post(p, ch[p], x_copy(short) if p == "x" else short, text, title); log(f"news {today} -> {p} " + ("(dry)" if DRY else "OK"))
        except Exception as e: log(f"news {today} -> {p} FAILED: {e}")
    if "site" not in done:
        try: done["site"] = site_post(site_text(text, "https://www.heartbeatobservatory.com/news/")); log(f"news {today} -> site OK")
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


def do_show(q, ch):
    today = NOW.strftime("%Y-%m-%d")
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
                try: s.setdefault("done", {})["site"] = site_post(site_text(s["caption"], s.get("link", "https://www.heartbeatobservatory.com/tv/"))); log(f"show {s['id']} -> site OK")
                except Exception as e: log(f"show {s['id']} -> site FAILED: {e}")
                continue
            try: s.setdefault("done", {})[p] = post(p, ch[p], x_copy(f) if p == "x" else (cover_copy(f) if p == "tiktok" else f), s["caption"], s["title"], s.get("x_tags")); log(f"show {s['id']} -> {p} " + ("(dry)" if DRY else "OK"))
            except Exception as e: log(f"show {s['id']} -> {p} FAILED: {e}")
        return   # one show a day
    log("show: queue is empty - add new shows to state/social-queue.json")


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "news"
    ch = channels()
    if not ch and DRY: ch = {"tiktok": "dry", "youtube": "dry", "x": "dry"}
    if not ch:
        log("Postiz not signed in or no channels connected - nothing posted")
        buzz("Socials: Postiz isn't connected yet, so today's posts didn't go out. Steps: AI-Shared/RECONNECT.md 'Postiz'.", "noauth"); return
    if not DRY: first_run_schema(ch)
    q = json.load(open(QUEUE, encoding="utf-8"))
    (do_news if what == "news" else do_show)(q, ch)
    if not DRY: json.dump(q, open(QUEUE, "w", encoding="utf-8"), indent=2, ensure_ascii=False)


if __name__ == "__main__":
    try: main()
    except Exception as e: log(f"CRASH {e}")

