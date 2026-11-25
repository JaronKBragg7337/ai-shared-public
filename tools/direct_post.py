"""direct_post.py - our own posting straight to X and YouTube, no Postiz in between (Fable, Tue 11/24/2026).

Why: Postiz ($29 a month) was declined on 11/24 and there is no money for it. This sends the same daily content
through each platform's own door instead:
  X        POST /2/tweets on api.x.com; a video goes up first, in pieces. X charges per post: $0.015, or $0.20
           when the text has a link in it (docs.x.com/x-api/getting-started/pricing, read 11/24/2026).
  YouTube  the Data API's videos.insert. Free, 100 uploads a day. Since 11/2/2026 uploads from our own
           unreviewed app are no longer locked private (Google's revision history, read 11/24/2026).
  TikTok   no door of our own yet: its posting API only publishes for an app TikTok has reviewed. Paused.

Keys (names only here; the values live in ~/.secrets/keys.env and arrive through Key Drop,
heartbeatobservatory.com/admin/keys/, tabs "X" and "YouTube"):
  X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET     the X card (four boxes, tested together before saving)
  YOUTUBE_CLIENT_ID, YOUTUBE_CLIENT_SECRET                      the YouTube card (two boxes)
  YOUTUBE_REFRESH_TOKEN                                         written here after Jaron's one sign-in on his phone
This file never prints, logs or returns a key value.

It only ever posts as @HeartbeatObserv and only ever uploads to the channel @heartbeatobservatory. Keys for any
other account are refused. X spending is counted here and stops at X_MONTH_CAP_USD a month.

It tells the AI side by itself, through the AI mailbox (sender "direct-post"): when a card's keys land, when the first
real post on a platform has gone out, and when a platform starts failing (once per stretch of failures, not per post).
That goes to the AI that built this door (BUILDER); Claude is added when a post could not go out at all. So Jaron
never has to pass any of it on.

  python tools/direct_post.py status       which keys are on file (names only) and what is ready
  python tools/direct_post.py check        asks X and YouTube "who am I?"; reads only, posts nothing
  python tools/direct_post.py selftest     checks the request signing against X's published example
  python tools/direct_post.py x "text" [video.mp4]                        DRY RUN: prints the exact requests
  python tools/direct_post.py youtube video.mp4 "title" "description"     DRY RUN as well
Add --live to really post. The daily jobs post through tools/social_daily.py; nothing is ever posted as a test.
"""
from __future__ import annotations

import base64
import datetime
import functools
import hashlib
import hmac
import importlib.util
import json
import os
import re
import secrets
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEC = Path(os.path.expanduser("~")) / ".secrets"
KEYFILE = SEC / "keys.env"
PENDING = SEC / "youtube-signin.json"      # a sign-in waiting for Jaron's tap; short-lived, so it sits with the keys
X_SEEN = SEC / "x-verified.json"           # which X keys were already checked to be @HeartbeatObserv
STATE = ROOT / "state" / "direct-post.json"    # no secrets: who we post as, this month's X count
PATH_FILE = ROOT / "state" / "social-path.json"    # which door each platform uses (read by tools/social_daily.py)
COMMITTED = False      # set just before the one request that makes a post exist; tools/social_daily.py only falls back to
                       # Postiz while this is still False, so a post can never go out twice
SAFETY_NET = False     # tools/social_daily.py sets this True while Postiz could still take a post our door could not start
BUILDER = "fable"      # the AI that built this door; it is mailed when keys land, at the first real post, when a door starts failing
LOG = ROOT / "state" / "social-posts.log"

X_USER = "HeartbeatObserv"                 # the only X account this tool posts as
YT_HANDLE = "@heartbeatobservatory"        # the only YouTube channel this tool uploads to
X_KEYS = ("X_API_KEY", "X_API_SECRET", "X_ACCESS_TOKEN", "X_ACCESS_SECRET")
YT_APP_KEYS = ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET")
YT_KEYS = YT_APP_KEYS + ("YOUTUBE_REFRESH_TOKEN",)

X_API = "https://api.x.com"
X_PRICE = {"post": 0.015, "post with a link": 0.20}     # dollars per post, X's price list as read 11/24/2026
X_MONTH_CAP_USD = 3.00                     # our own stop: about 200 plain posts; a normal month is about 55
X_TEXT_LIMIT = 280                         # the same length Postiz allowed us
X_VIDEO_MAX_S = 125 * 60 - 60              # X's API limit for a Premium account is 125 minutes (20 without Premium)
X_CHUNK = 4 * 1024 * 1024                  # X: pieces of at most 5 MB
LINK = re.compile(r"https?://|\b[\w-]+\.(?:com|org|net|gov|edu|io|ai|co|tv|news|social|app|dev|info|me|us|uk)\b", re.I)

GOOGLE_TOKEN = "https://oauth2.googleapis.com/token"
GOOGLE_DEVICE = "https://oauth2.googleapis.com/device/code"
YT_SCOPE = "https://www.googleapis.com/auth/youtube"     # the phone sign-in only offers this one and "read only"
YT_API = "https://www.googleapis.com/youtube/v3"
YT_UPLOAD = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"
YT_CHUNK = 16 * 1024 * 1024                # YouTube: pieces must be a multiple of 256 KB
FORM = {"Content-Type": "application/x-www-form-urlencoded"}


PASSED_ON = "The AIs were told just now; nothing for you to pass on."


class PostError(RuntimeError):
    """Something a platform refused, in plain words. Never carries a key."""


# ---------------------------------------------------------------- small helpers

def keys() -> dict:
    out = {}
    try:
        for line in open(KEYFILE, encoding="utf-8"):
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.strip().split("=", 1)
                out[k] = v.strip().strip('"')
    except OSError:
        pass
    return out


def save_keys(values: dict, what: str) -> None:
    """Put key values where the tools read them, the way tools/key_drop.py does: backup first, a note above a new name."""
    if KEYFILE.exists():
        shutil.copy(KEYFILE, str(KEYFILE) + ".bak-" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    lines = KEYFILE.read_text(encoding="utf-8").split("\n") if KEYFILE.exists() else []
    while lines and not lines[-1].strip():
        lines.pop()
    for name, value in values.items():
        for i, line in enumerate(lines):
            if line.startswith(name + "="):
                lines[i] = name + "=" + value
                break
        else:
            lines += [f"# {what} - added {datetime.date.today()} by tools/direct_post.py", name + "=" + value]
    KEYFILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def have(names, k=None) -> bool:
    k = keys() if k is None else k
    return all(k.get(n) for n in names)


def log(msg: str) -> None:
    line = datetime.datetime.now().strftime("%Y-%m-%d %H:%M ") + msg
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except OSError:
        pass
    print(line, flush=True)


def buzz(msg: str) -> None:
    """One plain line to Jaron's phone. Only for things he has to do or was waiting to hear."""
    try:
        topic = keys().get("NTFY_TOPIC")
        if topic:
            urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/" + topic, data=msg.encode("utf-8"), method="POST",
                                                          headers={"Title": "Our own posting"}), timeout=20)
    except Exception:
        pass


def tell(subject: str, body: str, to: tuple | None = None) -> bool:
    """One AI-mailbox message from this tool (docs/MAILBOX-FOR-AIS.md), so an AI looks at the first live steps and Jaron never
    has to pass on "it is connected" or "it failed". Goes to the builder unless `to` names others. Never raises, never
    carries a key. True if at least one went out."""
    sent = False
    try:
        spec = importlib.util.spec_from_file_location("hb_mailbox", ROOT / "tools" / "mailbox.py")   # "mailbox" is also a standard-library name
        box = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(box)
        for name in to or (BUILDER,):
            try:
                box.request("POST", data={"from_ai": "direct-post", "to_ai": name, "subject": subject[:90], "body": body[:1800]})
                sent = True
            except Exception:
                pass
    except Exception:
        pass
    return sent


def state() -> dict:
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_state(s: dict) -> None:
    STATE.write_text(json.dumps(s, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


def use(platform: str, door: str) -> None:
    """Tell the daily jobs which door a platform uses from now on ("direct", "postiz" or "paused")."""
    try:
        p = json.loads(PATH_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        p = {}
    p[platform] = door
    PATH_FILE.write_text(json.dumps(p, indent=1) + "\n", encoding="utf-8")


def live_result(platform: str, worked: bool, note: str) -> None:
    """Runs after every real post through our own door (never after a dry run). It mails the AI side at the two moments that
    matter: the first post that works on a platform, and the moment a platform starts failing - once for the whole stretch
    of failures, not once per post. What was already told is kept in state/direct-post.json ("live"). Never raises."""
    try:
        s = state()
        live = s.get("live") if isinstance(s.get("live"), dict) else {}
        mine = dict(live.get(platform) or {})
        name, now = {"x": "X", "youtube": "YouTube"}[platform], time.strftime("%Y-%m-%d %H:%M")
        if worked:
            since = mine.pop("failing_since", None)
            mine.pop("failing_why", None)
            if since:
                log(f"direct {platform}: works again (it had been failing since {since})")
            if not mine.get("first_ok"):
                where = f"https://x.com/{X_USER}/status/{note}" if platform == "x" else f"https://youtu.be/{note}"
                look = "the text, the video plays, the made-with-AI mark" if platform == "x" else "title, description, it is public, the video plays"
                if tell(f"{name}: the first real post through our own door went out",
                        f"{now}: tools/direct_post.py made its first real post on {name}: {where}\n"
                        f"Nobody has looked at it yet. Please open it once and check it the way a viewer sees it ({look}), then "
                        "tell Claude in one line. From here on a post only writes a line in state/social-posts.log."):
                    mine["first_ok"] = now
        elif not mine.get("failing_since"):
            hard = COMMITTED or not SAFETY_NET
            if not hard:
                what = ("Nothing had been sent and Postiz still has this channel, so the daily job hands this one to Postiz "
                        "(the next log line says how that went).")
            elif COMMITTED:
                what = (f"It stopped at or after the step that makes the post exist, so it may or may not be up on {name}. "
                        "Nothing else was tried, so nothing can be doubled.")
            else:
                what = f"This post did not go out on {name}: there was no second door for it."
            if tell(f"{name}: our own door failed" + ("" if hard else ", Postiz took this one"),
                    f"{now}: a real post through tools/direct_post.py failed on {name}.\nWhat was said: {str(note)[:400]}\n{what}\n"
                    f"You get this once. No more mail about {name} until a post has worked there again. Log: state/social-posts.log.",
                    (BUILDER, "claude") if hard else (BUILDER,)):
                mine["failing_since"], mine["failing_why"] = now, str(note)[:200]
        live[platform] = mine
        s["live"] = live
        save_state(s)
    except Exception:
        pass


def live_note(platform: str, s: dict, ready: bool) -> str:
    """For `status`: how the real posts through this door are going."""
    m = (s.get("live") or {}).get(platform) or {}
    if m.get("failing_since"):
        return f"; FAILING since {m['failing_since']} ({m.get('failing_why', '')[:90]})"
    if m.get("first_ok"):
        return f"; first real post worked {m['first_ok']}"
    return "; no real post through it yet" if ready else ""


def watched(platform: str):
    """Wraps x_post / yt_upload: every real result goes to live_result. The post's own outcome is passed on untouched.
    COMMITTED starts at False for each real post; SAFETY_NET holds for one post only (the caller sets it right before)."""
    def wrap(fn):
        @functools.wraps(fn)
        def run(*a, **kw):
            if kw.get("dry"):
                return fn(*a, **kw)
            globals()["COMMITTED"] = False
            try:
                out = fn(*a, **kw)
            except Exception as e:
                live_result(platform, False, str(e))
                globals()["SAFETY_NET"] = False
                raise
            globals()["SAFETY_NET"] = False
            live_result(platform, True, str(out))
            return out
        return run
    return wrap


def hget(headers: dict, name: str) -> str:
    return next((v for k, v in headers.items() if k.lower() == name.lower()), "")


def send(method: str, url: str, headers: dict | None = None, body: bytes | None = None, *, dry: bool = False,
         fake=None, show_body: str | None = None, quiet: bool = False, timeout: int = 300):
    """One request. Returns (status, headers, answer) where the answer is the parsed JSON, or text.
    Dry run: prints the request exactly as it would go out (callers pass every secret by its NAME), sends nothing,
    and hands back `fake` so the steps after it can be shown too."""
    headers = dict(headers or {})
    if dry:
        if not quiet:
            print(f"  {method} {url}")
            for k, v in headers.items():
                print(f"      {k}: {v}")
            if show_body is not None:
                print(f"      body: {show_body}")
            elif body is not None:
                print("      body: " + body.decode("utf-8", "replace"))
        return 200, {}, ({} if fake is None else fake)
    req = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status, got, raw = r.status, dict(r.headers.items()), r.read()
    except urllib.error.HTTPError as e:
        status, got, raw = e.code, dict(e.headers.items()), e.read()
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise PostError(f"could not reach {urllib.parse.urlsplit(url).netloc} ({type(e).__name__})") from None
    text = raw.decode("utf-8", "replace")
    try:
        return status, got, json.loads(text) if text.strip() else {}
    except ValueError:
        return status, got, text


# ---------------------------------------------------------------- X

def pct(s) -> str:
    return urllib.parse.quote(str(s), safe="-._~")


def oauth1(method: str, url: str, k: dict, query: dict | None = None, *, show: bool = False,
           nonce: str | None = None, stamp: int | None = None) -> str:
    """The Authorization line X wants (OAuth 1.0a, HMAC-SHA1). `query` = the address's own ?name=value pairs; they are
    part of what gets signed. A JSON body or a file is not. show=True writes the keys' NAMES instead of using them."""
    if show:
        return ('OAuth oauth_consumer_key="<X_API_KEY>", oauth_nonce="<fresh random text>", oauth_signature="<made at send '
                'time from this request with X_API_SECRET and X_ACCESS_SECRET>", oauth_signature_method="HMAC-SHA1", '
                'oauth_timestamp="<the time>", oauth_token="<X_ACCESS_TOKEN>", oauth_version="1.0"')
    o = {"oauth_consumer_key": k["X_API_KEY"], "oauth_nonce": nonce or secrets.token_hex(16),
         "oauth_signature_method": "HMAC-SHA1", "oauth_timestamp": str(stamp or int(time.time())),
         "oauth_token": k["X_ACCESS_TOKEN"], "oauth_version": "1.0"}
    pairs = sorted((pct(a), pct(b)) for a, b in {**o, **(query or {})}.items())
    base = "&".join([method.upper(), pct(url.split("?")[0]), pct("&".join(f"{a}={b}" for a, b in pairs))])
    signing_key = pct(k["X_API_SECRET"]) + "&" + pct(k["X_ACCESS_SECRET"])
    o["oauth_signature"] = base64.b64encode(hmac.new(signing_key.encode(), base.encode(), hashlib.sha1).digest()).decode()
    return "OAuth " + ", ".join(f'{pct(a)}="{pct(b)}"' for a, b in sorted(o.items()))


def x_said(status: int, d) -> str:
    said = ""
    if isinstance(d, dict):
        said = d.get("detail") or d.get("title") or "; ".join(
            str(e.get("message") or e.get("detail") or "") for e in d.get("errors", []) if isinstance(e, dict))
    elif isinstance(d, str):
        said = d
    said = re.sub(r"\s+", " ", said or "").strip()[:220]
    hint = {401: "X did not accept the keys", 402: "X wants API credits first (buy them in the X developer console)",
            403: "X refused it", 429: "X says too many requests for now"}.get(status, "X answered an error")
    return f"{hint} ({status})" + (f": {said}" if said else "")


def x_whoami(k: dict, *, dry: bool = False) -> dict:
    """Which account these keys post as, and whether the app may write. Reads only."""
    url = X_API + "/2/users/me"
    status, got, d = send("GET", url, {"Authorization": oauth1("GET", url, k, show=dry)}, dry=dry,
                          fake={"data": {"username": X_USER, "id": "DRY"}})
    if status != 200:
        raise PostError(x_said(status, d))
    data = d.get("data", {}) if isinstance(d, dict) else {}
    return {"username": data.get("username", ""), "id": data.get("id", ""),
            "access": "read-write" if dry else hget(got, "x-access-level")}


def x_fingerprint(k: dict) -> str:
    return hashlib.sha256((k.get("X_API_KEY", "") + "|" + k.get("X_ACCESS_TOKEN", "")).encode()).hexdigest()[:20]


def x_must_be_ours(k: dict) -> None:
    """Before posting: these keys must have been seen to belong to @HeartbeatObserv. Checked once per set of keys."""
    try:
        if json.loads(X_SEEN.read_text()).get("keys") == x_fingerprint(k):
            return
    except (OSError, ValueError):
        pass
    me = x_whoami(k)
    if me["username"].lower() != X_USER.lower():
        raise PostError(f"the X keys on file belong to @{me['username'] or '?'}, not @{X_USER}; nothing posted")
    X_SEEN.write_text(json.dumps({"keys": x_fingerprint(k), "username": me["username"], "seen": time.strftime("%Y-%m-%d %H:%M")}))


def x_month(add: float = 0.0, *, kind: str = "") -> dict:
    """This month's X count and estimated cost (our own tally; X's console has the real bill)."""
    s = state()
    month = datetime.date.today().strftime("%Y-%m")
    m = s.get("x_month") if isinstance(s.get("x_month"), dict) and s["x_month"].get("month") == month else {"month": month, "posts": 0, "usd": 0.0}
    if add:
        m["posts"] += 1
        m["usd"] = round(m["usd"] + add, 3)
        m["last"] = f"{time.strftime('%Y-%m-%d %H:%M')} {kind} ${add:.3f}"
        s["x_month"] = m
        save_state(s)
    return m


def multipart(fields: dict, file_field: str, data: bytes) -> tuple[bytes, str]:
    boundary = "hb" + secrets.token_hex(12)
    out = b""
    for name, value in fields.items():
        out += f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode()
    out += (f'--{boundary}\r\nContent-Disposition: form-data; name="{file_field}"; filename="piece.mp4"\r\n'
            "Content-Type: application/octet-stream\r\n\r\n").encode() + data + f"\r\n--{boundary}--\r\n".encode()
    return out, f"multipart/form-data; boundary={boundary}"


def x_upload(video: str, k: dict, *, dry: bool = False) -> str:
    """Send a video to X in pieces and wait until X has finished processing it. Returns X's number for the video."""
    size = os.path.getsize(video)
    kind = "video/quicktime" if video.lower().endswith(".mov") else "video/mp4"
    url = X_API + "/2/media/upload/initialize"
    status, _, d = send("POST", url, {"Authorization": oauth1("POST", url, k, show=dry), "Content-Type": "application/json"},
                        json.dumps({"media_type": kind, "total_bytes": size, "media_category": "tweet_video"}).encode(),
                        dry=dry, fake={"data": {"id": "<the video number X answers with>"}})
    if status not in (200, 201, 202) or not isinstance(d, dict) or not d.get("data", {}).get("id"):
        raise PostError("video upload did not start: " + x_said(status, d))
    media_id = str(d["data"]["id"])
    pieces = max(1, -(-size // X_CHUNK))
    url = f"{X_API}/2/media/upload/{media_id}/append"
    with open(video, "rb") as f:
        for i in range(pieces):
            if dry:
                first, last = i * X_CHUNK, min(size, (i + 1) * X_CHUNK) - 1
                if i in (0, pieces - 1):
                    send("POST", url, {"Authorization": oauth1("POST", url, k, show=True), "Content-Type": "multipart/form-data; boundary=<random>"},
                         dry=True, show_body=f"segment_index={i}, media=<bytes {first:,} to {last:,} of {os.path.basename(video)}>")
                elif i == 1:
                    print(f"      ... {pieces - 2} more pieces like it (segment_index 1 to {pieces - 2}) ...")
                continue
            body, ctype = multipart({"segment_index": str(i)}, "media", f.read(X_CHUNK))
            for attempt in range(4):
                try:
                    status, _, d = send("POST", url, {"Authorization": oauth1("POST", url, k), "Content-Type": ctype}, body)
                except PostError:
                    status, d = 599, "no answer"
                if status < 300:
                    break
                if status < 500 and status != 429:
                    raise PostError(f"video piece {i + 1} of {pieces}: " + x_said(status, d))
                time.sleep(5 * (attempt + 1))
            else:
                raise PostError(f"video piece {i + 1} of {pieces} would not go through: " + x_said(status, d))
    url = f"{X_API}/2/media/upload/{media_id}/finalize"
    status, _, d = send("POST", url, {"Authorization": oauth1("POST", url, k, show=dry)}, dry=dry,
                        fake={"data": {"processing_info": {"state": "succeeded"}}})
    if status not in (200, 201):
        raise PostError("video upload did not finish: " + x_said(status, d))
    info = (d.get("data") or {}).get("processing_info") if isinstance(d, dict) else None
    url, query = X_API + "/2/media/upload", {"command": "STATUS", "media_id": media_id}
    if dry:
        send("GET", f"{url}?command=STATUS&media_id={media_id}", {"Authorization": oauth1("GET", url, k, query, show=True)}, dry=True,
             show_body="(asked again every few seconds until X says the video is processed)")
    deadline = time.time() + 20 * 60
    while info and info.get("state") in ("pending", "in_progress") and not dry:
        if time.time() > deadline:
            raise PostError("X was still processing the video after 20 minutes")
        time.sleep(min(max(int(info.get("check_after_secs", 5)), 1), 30))
        status, _, d = send("GET", url + "?" + urllib.parse.urlencode(query), {"Authorization": oauth1("GET", url, k, query)})
        if status != 200:
            raise PostError("asking X about the video: " + x_said(status, d))
        info = (d.get("data") or {}).get("processing_info") if isinstance(d, dict) else None
    if info and info.get("state") == "failed":
        raise PostError("X could not process the video: " + str((info.get("error") or {}).get("message", ""))[:160])
    return media_id


@watched("x")
def x_post(text: str, video: str | None = None, *, ai: bool = True, dry: bool = False) -> str:
    """Post to X as @HeartbeatObserv. Returns the post's number."""
    k = keys()
    if not dry and not have(X_KEYS, k):
        raise PostError("X keys are not on file yet (Key Drop, tab X)")
    kind = "post with a link" if LINK.search(text) else "post"
    month = x_month()
    if dry:
        print(f"X, as @{X_USER}: one {kind} = ${X_PRICE[kind]:.3f}. Our tally this month: {month['posts']} posts, "
              f"about ${month['usd']:.2f} of the ${X_MONTH_CAP_USD:.2f} stop. Keys on file: {'yes' if have(X_KEYS, k) else 'NOT YET'}.")
    elif month["usd"] + X_PRICE[kind] > X_MONTH_CAP_USD:
        raise PostError(f"X stop reached: about ${month['usd']:.2f} spent this month, the stop is ${X_MONTH_CAP_USD:.2f} (tools/direct_post.py)")
    if not dry:
        x_must_be_ours(k)
    body = {"text": text}
    if video:
        body["media"] = {"media_ids": [x_upload(video, k, dry=dry)]}
        if ai:
            body["made_with_ai"] = True          # X's own "this media was made with AI" mark (Jaron's label rule)
    url = X_API + "/2/tweets"
    globals()["COMMITTED"] = not dry
    status, _, d = send("POST", url, {"Authorization": oauth1("POST", url, k, show=dry), "Content-Type": "application/json"},
                        json.dumps(body, ensure_ascii=False).encode("utf-8"), dry=dry, fake={"data": {"id": "DRY"}})
    if status not in (200, 201) or not isinstance(d, dict) or not d.get("data", {}).get("id"):
        raise PostError(x_said(status, d))
    post_id = str(d["data"]["id"])
    if not dry:
        x_month(X_PRICE[kind], kind=kind)
        log(f"direct x: posted {post_id} ({kind}, ${X_PRICE[kind]:.3f})")
    return post_id


# ---------------------------------------------------------------- YouTube

def g_said(status: int, d) -> str:
    if isinstance(d, dict):
        e = d.get("error")
        if isinstance(e, dict):
            reason = ((e.get("errors") or [{}])[0] or {}).get("reason", "")
            return f"Google answered {status}: " + re.sub(r"\s+", " ", str(e.get("message", "")))[:220] + (f" [{reason}]" if reason else "")
        if e:
            return f"Google answered {status}: {e}" + (f" ({str(d['error_description'])[:140]})" if d.get("error_description") else "")
    return f"Google answered {status}"


def yt_token(k: dict, *, dry: bool = False) -> str:
    """A fresh one-hour pass from Google, made from the sign-in Jaron did once."""
    if dry:
        send("POST", GOOGLE_TOKEN, FORM, dry=True, show_body="client_id=<YOUTUBE_CLIENT_ID>&client_secret=<YOUTUBE_CLIENT_SECRET>"
             "&refresh_token=<YOUTUBE_REFRESH_TOKEN>&grant_type=refresh_token")
        return "<the one-hour pass Google answers with>"
    status, _, d = send("POST", GOOGLE_TOKEN, FORM, urllib.parse.urlencode({
        "client_id": k["YOUTUBE_CLIENT_ID"], "client_secret": k["YOUTUBE_CLIENT_SECRET"],
        "refresh_token": k["YOUTUBE_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode())
    if status != 200 or not isinstance(d, dict) or not d.get("access_token"):
        gone = isinstance(d, dict) and d.get("error") == "invalid_grant"
        raise PostError(("the YouTube sign-in is no longer good; send the YouTube card on the Key Drop page again. " if gone else "") + g_said(status, d))
    return d["access_token"]


def yt_whoami(token: str, *, dry: bool = False) -> dict:
    """Which channel this sign-in uploads to. Reads only (1 of 10,000 free units a day)."""
    status, _, d = send("GET", YT_API + "/channels?part=snippet&mine=true", {"Authorization": "Bearer " + token}, dry=dry,
                        fake={"items": [{"id": "DRY", "snippet": {"title": "Heartbeat Observatory", "customUrl": YT_HANDLE}}]})
    if status != 200 or not isinstance(d, dict):
        raise PostError(g_said(status, d))
    item = (d.get("items") or [{}])[0]
    sn = item.get("snippet", {})
    return {"id": item.get("id", ""), "title": (sn.get("title") or "").strip(), "handle": (sn.get("customUrl") or "").strip()}


def clip_bytes(s: str, limit: int) -> str:
    return s.encode("utf-8")[:limit].decode("utf-8", "ignore")


@watched("youtube")
def yt_upload(video: str, title: str, description: str, *, privacy: str = "public", ai_label: bool | None = None,
              category: str = "22", dry: bool = False) -> str:
    """Upload a video to the Heartbeat Observatory channel. Returns YouTube's id for it (youtu.be/<id>).
    ai_label: None leaves YouTube's "altered or synthetic content" mark as it was with Postiz (not set)."""
    k = keys()
    if not dry and not have(YT_KEYS, k):
        raise PostError("YouTube keys are not on file yet (Key Drop, tab YouTube, then the phone sign-in)")
    clean = lambda s: s.replace("<", "(").replace(">", ")")          # YouTube refuses < and > in titles and descriptions
    meta = {"snippet": {"title": clean(title)[:100], "description": clip_bytes(clean(description), 4900), "categoryId": category},
            "status": {"privacyStatus": privacy, "selfDeclaredMadeForKids": False}}
    if ai_label is not None:
        meta["status"]["containsSyntheticMedia"] = bool(ai_label)
    size = os.path.getsize(video)
    if dry:
        print(f"YouTube, channel {YT_HANDLE}: free, 100 uploads a day. Keys on file: {'yes' if have(YT_KEYS, k) else 'NOT YET'}.")
    token = yt_token(k, dry=dry)
    me = yt_whoami(token, dry=dry)
    if me["handle"].lower() != YT_HANDLE:
        raise PostError(f"the YouTube sign-in is for the channel '{me['title'] or '?'}' ({me['handle'] or 'no handle'}), not {YT_HANDLE}; nothing uploaded")
    status, got, d = send("POST", YT_UPLOAD, {"Authorization": "Bearer " + token, "Content-Type": "application/json; charset=UTF-8",
                                              "X-Upload-Content-Length": str(size), "X-Upload-Content-Type": "video/mp4"},
                          json.dumps(meta, ensure_ascii=False).encode("utf-8"), dry=dry)
    session = "<the upload address YouTube answers with>" if dry else hget(got, "Location")
    if status != 200 or not session:
        raise PostError("YouTube would not start the upload: " + g_said(status, d))
    pieces = max(1, -(-size // YT_CHUNK))
    if dry:
        send("PUT", session, {"Authorization": "Bearer " + token, "Content-Type": "video/mp4", "Content-Length": str(min(size, YT_CHUNK)),
                              "Content-Range": f"bytes 0-{min(size, YT_CHUNK) - 1}/{size}"}, dry=True,
             show_body=f"<the first {min(size, YT_CHUNK):,} bytes of {os.path.basename(video)}>; then {pieces - 1} more pieces the same way; "
                       "the last one is answered with the new video's id")
        return "DRY"
    at, tries_left, video_id = 0, 8, ""
    with open(video, "rb") as f:
        while not video_id:
            f.seek(at)
            piece = f.read(YT_CHUNK)
            if at + len(piece) >= size:
                globals()["COMMITTED"] = True
            headers = {"Authorization": "Bearer " + token, "Content-Type": "video/mp4",
                       "Content-Range": f"bytes {at}-{at + len(piece) - 1}/{size}"}
            try:
                status, got, d = send("PUT", session, headers, piece, timeout=600)
            except PostError:
                status, got, d = 599, {}, "no answer"
            if status in (200, 201) and isinstance(d, dict) and d.get("id"):
                video_id = d["id"]
            elif status == 308:                                   # "got it so far": the Range line says up to which byte
                m = re.search(r"-(\d+)$", hget(got, "Range"))
                at = int(m.group(1)) + 1 if m else 0
            elif status == 401 and tries_left:
                tries_left -= 1
                token = yt_token(k)
            elif status in (500, 502, 503, 504, 599) and tries_left:      # a hiccup: ask how far it got, then carry on
                tries_left -= 1
                time.sleep(10 * (8 - tries_left))
                try:
                    status, got, d = send("PUT", session, {"Authorization": "Bearer " + token, "Content-Range": f"bytes */{size}"}, b"")
                except PostError:
                    continue
                if status in (200, 201) and isinstance(d, dict) and d.get("id"):
                    video_id = d["id"]
                elif status == 308:
                    m = re.search(r"-(\d+)$", hget(got, "Range"))
                    at = int(m.group(1)) + 1 if m else 0
            else:
                raise PostError(f"YouTube stopped the upload at byte {at:,} of {size:,}: " + g_said(status, d))
    log(f"direct youtube: uploaded {video_id} ({size / 2**20:.0f} MB, {privacy})")
    return video_id


# ---------------------------------------------------------------- the one-time YouTube sign-in (Jaron's phone)

def yt_signin_start(k: dict | None = None, *, attempt: int = 1) -> str:
    """Ask Google for a short code and buzz it to Jaron. He opens the address on his phone, types the code, picks the
    Heartbeat Observatory channel and taps Allow. No password ever comes near the MSI or an AI."""
    k = keys() if k is None else k
    status, _, d = send("POST", GOOGLE_DEVICE, FORM, urllib.parse.urlencode({"client_id": k["YOUTUBE_CLIENT_ID"], "scope": YT_SCOPE}).encode())
    if status != 200 or not isinstance(d, dict) or not d.get("device_code"):
        err = d.get("error") if isinstance(d, dict) else ""
        if err in ("invalid_client", "unauthorized_client"):
            raise PostError("Google does not accept this Client ID for a phone sign-in. In the Google console the client has to be "
                            "the kind 'TVs and Limited Input devices'. Make it again as that kind and send both values again.")
        raise PostError("the YouTube sign-in could not start: " + g_said(status, d))
    wait = int(d.get("expires_in", 1800))
    pend = {"device_code": d["device_code"], "url": d.get("verification_url") or d.get("verification_uri") or "https://www.google.com/device",
            "expires_at": time.time() + wait, "attempt": attempt}
    PENDING.write_text(json.dumps(pend))
    buzz(f"YouTube sign-in, one time: open {pend['url']} on your phone, type the code {d['user_code']}, pick the Heartbeat Observatory "
         f"channel, tap Allow. The code works for {wait // 60} minutes.")
    log(f"direct youtube: sign-in code sent to Jaron's phone (try {attempt}); waiting for his tap")
    return "sent"


def signin_tick() -> str | None:
    """Called every minute by tools/key_drop.py. If a sign-in is waiting, ask Google once whether Jaron has tapped Allow."""
    if not PENDING.exists():
        return None
    p, k = json.loads(PENDING.read_text()), keys()
    if time.time() > p["expires_at"]:
        PENDING.unlink()
        buzz("The YouTube sign-in code ran out before it was used. Nothing changed. For a new code, send the YouTube card on the Key Drop page again.")
        log("direct youtube: the sign-in code ran out unused")
        return "ran out"
    status, _, d = send("POST", GOOGLE_TOKEN, FORM, urllib.parse.urlencode({
        "client_id": k.get("YOUTUBE_CLIENT_ID", ""), "client_secret": k.get("YOUTUBE_CLIENT_SECRET", ""),
        "device_code": p["device_code"], "grant_type": "urn:ietf:params:oauth:grant-type:device_code"}).encode())
    err = d.get("error") if isinstance(d, dict) else ""
    if status != 200:
        if err in ("authorization_pending", "slow_down"):
            return "waiting"
        PENDING.unlink()
        if err == "access_denied":
            buzz("YouTube sign-in: it was cancelled, so nothing changed. For a new code, send the YouTube card on the Key Drop page again.")
        else:
            told = tell("YouTube sign-in did not finish",
                        f"{time.strftime('%Y-%m-%d %H:%M')}: Jaron's phone sign-in for our own YouTube uploads ended without a pass. "
                        f"{g_said(status, d)[:300]}\nNothing was saved and nothing changed: YouTube still posts the way it did before. "
                        "His phone told him the AIs know, so he is not expecting to pass it on.", (BUILDER, "claude"))
            buzz("YouTube sign-in did not work (" + g_said(status, d)[:120] + "). Nothing changed. " + (PASSED_ON if told else "Tell Claude."))
        log("direct youtube: sign-in ended without a pass: " + g_said(status, d)[:160])
        return "no"
    PENDING.unlink()
    try:
        me = yt_whoami(d["access_token"])
    except PostError as e:
        told = tell("YouTube sign-in went through, but the channel check failed",
                    f"{time.strftime('%Y-%m-%d %H:%M')}: Jaron tapped Allow, then YouTube would not say which channel the sign-in is for: "
                    f"{str(e)[:300]}\nNothing was saved and nothing changed. His phone told him the AIs know.", (BUILDER, "claude"))
        buzz("YouTube sign-in went through, but YouTube would not say which channel it is (" + str(e)[:140] + "). Nothing saved. "
             + (PASSED_ON if told else "Tell Claude."))
        log("direct youtube: signed in but the channel check failed: " + str(e)[:200])
        return "no"
    if me["handle"].lower() != YT_HANDLE or not d.get("refresh_token"):
        again = p.get("attempt", 1) < 3
        buzz(f"That sign-in was for '{me['title'] or 'an account with no channel'}' ({me['handle'] or 'no handle'}). I need the Heartbeat "
             f"Observatory channel ({YT_HANDLE}). Nothing was saved." + (" A new code is coming." if again else " Send the YouTube card again to retry."))
        log(f"direct youtube: sign-in was for another channel ({me['handle'] or me['title'] or 'none'}); not saved")
        if again:
            yt_signin_start(k, attempt=p.get("attempt", 1) + 1)
        return "wrong channel"
    save_keys({"YOUTUBE_REFRESH_TOKEN": d["refresh_token"]}, "YouTube upload sign-in (Jaron's phone, one time)")
    s = state()
    s["youtube"] = {"channel_id": me["id"], "title": me["title"], "handle": me["handle"], "signed_in": time.strftime("%Y-%m-%d %H:%M")}
    save_state(s)
    use("youtube", "direct")
    log(f"direct youtube: signed in, channel {me['title']} ({me['handle']}); YouTube now goes through our own door")
    buzz(f"YouTube is connected: {me['title']}. Our own uploads are ready and switched on. You are done.")
    tell("YouTube sign-in is done: our own YouTube door is on",
         f"{time.strftime('%Y-%m-%d %H:%M')}: Jaron finished the phone sign-in. Uploads now go through tools/direct_post.py to "
         f"{me['title']} ({me['handle']}). Nothing has been uploaded yet. To do now: python tools/direct_post.py check (it only "
         "reads), then tell Claude in one line. The first real upload sends its own mail.")
    return "connected"


# ---------------------------------------------------------------- what Key Drop calls

def drop_x(v: dict) -> str:
    """The X card: four boxes. Tested together BEFORE anything is saved."""
    k = {"X_API_KEY": v.get("api_key", ""), "X_API_SECRET": v.get("api_secret", ""),
         "X_ACCESS_TOKEN": v.get("access_token", ""), "X_ACCESS_SECRET": v.get("access_secret", "")}
    k = {n: str(x).strip() for n, x in k.items()}
    if not all(k.values()) or any(re.search(r"\s", x) for x in k.values()):
        raise PostError("all four X boxes are needed, with no spaces inside")
    me = x_whoami(k)
    if me["username"].lower() != X_USER.lower():
        raise PostError(f"these keys post as @{me['username'] or '?'}, not @{X_USER}. Nothing saved.")
    if me["access"] and "write" not in me["access"]:
        raise PostError("these keys can only READ. In the X console set the app's permissions to 'Read and write', then make a NEW "
                        "Access Token and Secret and send all four boxes again. Nothing saved.")
    save_keys(k, "X posting, our own (no Postiz)")
    X_SEEN.write_text(json.dumps({"keys": x_fingerprint(k), "username": me["username"], "seen": time.strftime("%Y-%m-%d %H:%M")}))
    s = state()
    s["x"] = {"username": me["username"], "id": me["id"], "access": me["access"] or "not told", "keys_since": time.strftime("%Y-%m-%d %H:%M")}
    save_state(s)
    use("x", "direct")
    log(f"direct x: keys saved, posting as @{me['username']} ({me['access'] or 'access not told'}); X now goes through our own door")
    tell("X keys landed: our own X door is on",
         f"{time.strftime('%Y-%m-%d %H:%M')}: Jaron's X card passed its check and is saved. Posts to X now go through "
         f"tools/direct_post.py as @{me['username']} (access: {me['access'] or 'not told'}). Nothing has been posted yet. To do now: "
         "python tools/direct_post.py check (it only reads), then tell Claude in one line. The first real post sends its own mail.")
    return f"X keys work: our own posting as @{me['username']} is ready and switched on."


def drop_youtube(v: dict) -> str:
    """The YouTube card: two boxes. Saved, then the sign-in code goes to Jaron's phone."""
    cid, secret = str(v.get("client_id", "")).strip(), str(v.get("client_secret", "")).strip()
    if not cid.endswith(".apps.googleusercontent.com"):
        raise PostError("the Client ID box should end with .apps.googleusercontent.com; check which value went in which box")
    if not secret or re.search(r"\s", cid + secret):
        raise PostError("both YouTube boxes are needed, with no spaces inside")
    k = {"YOUTUBE_CLIENT_ID": cid, "YOUTUBE_CLIENT_SECRET": secret}
    yt_signin_start(k)                    # also proves Google knows this client and that it is the right kind
    save_keys(k, "YouTube upload, our own (no Postiz)")
    return "YouTube keys saved. One step left: the sign-in code was just sent to your phone."


# ---------------------------------------------------------------- command line

def status() -> None:
    k, s = keys(), state()
    print("Keys on file (names only):")
    for n in X_KEYS + YT_KEYS:
        print(f"  {n:24} {'yes' if k.get(n) else 'no'}")
    m = x_month()
    print(f"X: {'READY' if have(X_KEYS, k) else 'not ready (Key Drop, tab X)'}"
          + (f"; posting as @{s['x']['username']}" if s.get("x") else "")
          + f"; our tally this month: {m['posts']} posts, about ${m['usd']:.2f} of the ${X_MONTH_CAP_USD:.2f} stop" + live_note("x", s, have(X_KEYS, k)))
    yt = ("READY" if have(YT_KEYS, k) else "waiting for the phone sign-in" if PENDING.exists()
          else "client keys on file, sign-in not done" if have(YT_APP_KEYS, k) else "not ready (Key Drop, tab YouTube)")
    print(f"YouTube: {yt}" + (f"; channel {s['youtube']['title']} ({s['youtube']['handle']})" if s.get("youtube") else "")
          + live_note("youtube", s, have(YT_KEYS, k)))
    print("TikTok: no door of our own (its posting API needs an app TikTok has reviewed); paused when Postiz is off")


def check() -> int:
    k, bad = keys(), 0
    if have(X_KEYS, k):
        try:
            me = x_whoami(k)
            ok = me["username"].lower() == X_USER.lower() and "write" in (me["access"] or "write")
            print(f"X: keys post as @{me['username']}, access '{me['access'] or 'not told'}' -> {'OK' if ok else 'NOT OK'}")
            bad += not ok
        except PostError as e:
            print("X:", e)
            bad += 1
    else:
        print("X: keys not on file yet")
    if have(YT_KEYS, k):
        try:
            me = yt_whoami(yt_token(k))
            ok = me["handle"].lower() == YT_HANDLE
            print(f"YouTube: sign-in uploads to '{me['title']}' ({me['handle']}) -> {'OK' if ok else 'NOT OK'}")
            bad += not ok
        except PostError as e:
            print("YouTube:", e)
            bad += 1
    else:
        print("YouTube: keys or sign-in not on file yet")
    return 1 if bad else 0


def selftest() -> int:
    """X's own published signing example (docs: "Creating a signature"). The keys in it are X's sample ones, not ours."""
    k = {"X_API_KEY": "xvz1evFS4wEEPTGEFPHBog", "X_API_SECRET": "kAcSOqF21Fu85e7zjz7ZN2U4ZRhfV3WpwPAoE3Z7kBw",
         "X_ACCESS_TOKEN": "370773112-GmHxMAgYyLbNEtIKZeRNFsMKPR9EyMZeS9weJAEb", "X_ACCESS_SECRET": "LswwdoUaIvS8ltyTt5jkRh4J50vUPVVHtR2YPi5kE"}
    query = {"include_entities": "true", "status": "Hello Ladies + Gentlemen, a signed OAuth request!"}
    want = {"https://api.twitter.com/1.1/statuses/update.json": "hCtSmYh+iHYCEqBWrE7C7hYmtUk=",
            "https://api.twitter.com/1/statuses/update.json": "tnnArxj06cWHq44gCs1OSKk/jLY="}
    good = 0
    for url, signature in want.items():
        line = oauth1("POST", url, k, query, nonce="kYjzVBB8Y0ZFabxSWbWovY3uYSQ2pTgmZeNu2VS4cg", stamp=1318622958)
        got = urllib.parse.unquote(re.search(r'oauth_signature="([^"]+)"', line).group(1))
        print(f"  {url}: {'matches' if got == signature else 'DIFFERENT'} X's published signature")
        good += got == signature
    body, ctype = multipart({"segment_index": "0"}, "media", b"abc")
    shape = body.count(b"Content-Disposition") == 2 and body.endswith(b"--\r\n") and ctype.split("boundary=")[1].encode() in body
    print(f"  file-piece body: {'well formed' if shape else 'BROKEN'}")
    print("selftest:", "PASS" if good == len(want) and shape else "FAIL")
    return 0 if good == len(want) and shape else 1


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    live = "--live" in sys.argv
    what = args[0] if args else "status"
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        if what == "status":
            status()
        elif what == "check":
            return check()
        elif what == "selftest":
            return selftest()
        elif what == "x" and len(args) >= 2:
            print("posted:" if live else "DRY RUN, nothing sent. This is exactly what would go out:")
            print("  ->", x_post(args[1], args[2] if len(args) > 2 else None, dry=not live))
        elif what == "youtube" and len(args) >= 4:
            print("uploaded:" if live else "DRY RUN, nothing sent. This is exactly what would go out:")
            print("  ->", yt_upload(args[1], args[2], args[3], privacy="private" if "--private" in sys.argv else "public", dry=not live))
        elif what == "youtube-signin":
            print(yt_signin_start())
        else:
            print(__doc__)
            return 2
    except PostError as e:
        print("STOPPED:", e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
