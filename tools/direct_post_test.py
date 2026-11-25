"""direct_post_test.py - checks tools/direct_post.py without the internet and without the real keys.

  python tools/direct_post_test.py        every line should say ok; the last line says ALL OK

How: the one function that talks to the internet (direct_post.send) is swapped for a stand-in that plays X's and
Google's parts and writes down every request. The key file, the state files and the log are pointed at a
throwaway folder first, so nothing real is read or changed. The "keys" in here are made-up test words.
The tool's phone buzz and its own mail to the AIs are swapped for lists as well, so a test never sends either.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import direct_post as D

TMP = Path(tempfile.mkdtemp(prefix="hb-direct-test-"))
D.KEYFILE, D.PENDING, D.X_SEEN = TMP / "keys.env", TMP / "youtube-signin.json", TMP / "x-verified.json"
D.STATE, D.PATH_FILE, D.LOG = TMP / "direct-post.json", TMP / "social-path.json", TMP / "posts.log"
BUZZED = []
D.buzz = BUZZED.append
TOLD = []                                                 # (subject, to whom, body) of every mail the tool would send to the AIs
REAL_TELL = D.tell
STUB_TELL = lambda subject, body, to=None: TOLD.append((subject, tuple(to or (D.BUILDER,)), body)) or True
D.tell = STUB_TELL                                        # never a real mail from a test
D.time.sleep = lambda s: None

FAKE_X = {"X_API_KEY": "test-api-key", "X_API_SECRET": "test-api-secret", "X_ACCESS_TOKEN": "test-token", "X_ACCESS_SECRET": "test-token-secret"}
FAKE_YT = {"YOUTUBE_CLIENT_ID": "test-client.apps.googleusercontent.com", "YOUTUBE_CLIENT_SECRET": "test-client-secret"}
results = []


def ok(name: str, good: bool, detail: str = "") -> None:
    results.append(bool(good))
    print(f"  {'ok  ' if good else 'FAIL'} {name}" + (f"  [{detail}]" if detail and not good else ""))


def write_keys(d: dict) -> None:
    D.KEYFILE.write_text("# test keys\nNTFY_TOPIC=test-topic\n" + "".join(f"{k}={v}\n" for k, v in d.items()), encoding="utf-8")


def refused(fn, *a, **kw) -> str:
    try:
        fn(*a, **kw)
    except D.PostError as e:
        return str(e)
    return ""


class World:
    """Plays X and Google. Settings say how they behave; `calls` remembers every request."""

    def __init__(self):
        self.calls, self.x_user, self.x_access, self.x_post_status = [], "HeartbeatObserv", "read-write", 201
        self.x_init_status, self.status_asks = 200, 0
        self.yt_handle, self.yt_bytes, self.yt_hiccup_at, self.device = "@heartbeatobservatory", b"", None, "authorization_pending"

    def send(self, method, url, headers=None, body=None, *, dry=False, fake=None, show_body=None, quiet=False, timeout=300):
        headers = headers or {}
        self.calls.append((method, url, dict(headers), body))
        if url.endswith("/2/users/me"):
            assert headers["Authorization"].startswith("OAuth ") and 'oauth_signature="' in headers["Authorization"]
            return 200, {"x-access-level": self.x_access}, {"data": {"username": self.x_user, "id": "42"}}
        if url.endswith("/2/media/upload/initialize"):
            return self.x_init_status, {}, ({"data": {"id": "777"}} if self.x_init_status == 200 else {"detail": "no"})
        if "/append" in url:
            assert b'name="segment_index"' in body and b'name="media"' in body
            return 204, {}, {}
        if url.endswith("/finalize"):
            return 200, {}, {"data": {"processing_info": {"state": "pending", "check_after_secs": 1}}}
        if "command=STATUS" in url:
            self.status_asks += 1
            return 200, {}, {"data": {"processing_info": {"state": "succeeded" if self.status_asks >= 2 else "in_progress", "check_after_secs": 1}}}
        if url.endswith("/2/tweets"):
            return self.x_post_status, {}, ({"data": {"id": "999"}} if self.x_post_status == 201 else {"detail": "Forbidden"})
        if url == D.GOOGLE_DEVICE:
            return 200, {}, {"device_code": "dev-code", "user_code": "ABCD-EFGH", "verification_url": "https://www.google.com/device", "expires_in": 1800, "interval": 5}
        if url == D.GOOGLE_TOKEN:
            text = body.decode()
            if "grant_type=refresh_token" in text:
                return 200, {}, {"access_token": "pass-1"}
            if self.device == "ok":
                return 200, {}, {"access_token": "pass-2", "refresh_token": "test-refresh"}
            return 428, {}, {"error": self.device}
        if "/channels?" in url:
            return 200, {}, {"items": [{"id": "UCtest", "snippet": {"title": "Heartbeat Observatory ", "customUrl": self.yt_handle}}]}
        if url == D.YT_UPLOAD:
            json.loads(body)
            return 200, {"Location": "https://upload.example/session-1"}, {}
        if url == "https://upload.example/session-1":
            rng = headers.get("Content-Range", "")
            if rng.startswith("bytes */"):                       # "how far did you get?"
                return 308, ({"Range": f"bytes=0-{len(self.yt_bytes) - 1}"} if self.yt_bytes else {}), ""
            first, rest = rng[len("bytes "):].split("-")
            last, total = rest.split("/")
            assert int(first) == len(self.yt_bytes), f"piece starts at {first}, expected {len(self.yt_bytes)}"
            if self.yt_hiccup_at is not None and int(first) == self.yt_hiccup_at:
                self.yt_hiccup_at = None
                self.yt_bytes += body[: len(body) // 2]          # half of it arrived, then the line dropped
                return 503, {}, "backend error"
            self.yt_bytes += body
            assert int(last) == len(self.yt_bytes) - 1
            if len(self.yt_bytes) == int(total):
                return 201, {}, {"id": "vid123"}
            return 308, {"Range": f"bytes=0-{len(self.yt_bytes) - 1}"}, ""
        raise AssertionError("unexpected request: " + method + " " + url)


def fresh() -> World:
    w = World()
    D.send = w.send
    for f in (D.STATE, D.PATH_FILE, D.X_SEEN, D.PENDING):
        if f.exists():
            f.unlink()
    BUZZED.clear()
    TOLD.clear()
    D.COMMITTED = D.SAFETY_NET = False
    D.tell = STUB_TELL
    return w


video = TMP / "clip.mp4"
video.write_bytes(os.urandom(9 * 1024 * 1024 + 123))            # 3 pieces for X (4 MB each)
big = TMP / "show.mp4"
D.YT_CHUNK = 1024 * 1024                                          # small pieces so the test file can stay small
big.write_bytes(os.urandom(3 * 1024 * 1024 + 4567))             # 4 pieces for YouTube

print("X")
w = fresh(); write_keys(FAKE_X)
pid = D.x_post("Hello from the test.", str(video))
urls = [c[1] for c in w.calls]
ok("post with a video: who-am-I, start, 3 pieces, finish, 2 status asks, then the post",
   pid == "999" and urls[0].endswith("/users/me") and sum("/append" in u for u in urls) == 3 and w.status_asks == 2 and urls[-1].endswith("/2/tweets"), str(urls))
sent = json.loads(w.calls[-1][3])
ok("the post carries the text, the video number and the made-with-AI mark", sent == {"text": "Hello from the test.", "media": {"media_ids": ["777"]}, "made_with_ai": True}, str(sent))
ok("the pieces add up to the file", hashlib.sha256(b"".join(c[3].split(b"\r\n\r\n", 2)[2].rsplit(b"\r\n--", 1)[0] for c in w.calls if "/append" in c[1])).digest() == hashlib.sha256(video.read_bytes()).digest())
ok("tally: 1 post, $0.015", D.x_month()["posts"] == 1 and abs(D.x_month()["usd"] - 0.015) < 1e-9)
ok("marked as sent (no fallback after this point)", D.COMMITTED is True)
before = len(w.calls); D.x_post("Second one, text only.")
ok("second post does not ask who-am-I again", not any(c[1].endswith("/users/me") for c in w.calls[before:]) and "made_with_ai" not in json.loads(w.calls[-1][3]))
D.x_post("With a link https://www.heartbeatobservatory.com/news/")
ok("a post with a link is counted at $0.20", abs(D.x_month()["usd"] - 0.23) < 1e-9, str(D.x_month()))
s = D.state(); s["x_month"]["usd"] = D.X_MONTH_CAP_USD - 0.01; D.save_state(s)
ok("the monthly stop refuses the next post", "stop reached" in refused(D.x_post, "over the stop"))
w = fresh(); w.x_user = "SomebodyElse"
ok("keys of another account are refused, nothing posted", "not @HeartbeatObserv" in refused(D.x_post, "hi") and not any(c[1].endswith("/2/tweets") for c in w.calls))
w = fresh(); w.x_init_status = 403
msg = refused(D.x_post, "hi", str(video))
ok("an upload refused by X stops before the post, and says so", "did not start" in msg and D.COMMITTED is False and not any(c[1].endswith("/2/tweets") for c in w.calls), msg)
w = fresh(); D.KEYFILE.write_text("NTFY_TOPIC=test-topic\n")
ok("no keys on file: refused in plain words", "not on file" in refused(D.x_post, "hi"))

print("X card from Key Drop")
box = {"api_key": "test-api-key", "api_secret": "test-api-secret", "access_token": "test-token", "access_secret": "test-token-secret"}
w = fresh(); D.KEYFILE.write_text("NTFY_TOPIC=test-topic\n")
note = D.drop_x(box)
ok("good keys: saved under the four names, door switched to our own", D.have(D.X_KEYS) and json.loads(D.PATH_FILE.read_text())["x"] == "direct" and "ready" in note, note)
ok("the note and the log never contain a key", not any(v in note + D.LOG.read_text() for v in box.values()))
w = fresh(); D.KEYFILE.write_text("NTFY_TOPIC=test-topic\n"); w.x_access = "read"
ok("read-only keys: refused, nothing saved", "only READ" in refused(D.drop_x, box) and not D.have(D.X_KEYS))
w = fresh(); w.x_user = "SomebodyElse"
ok("another account's keys: refused, nothing saved", "Nothing saved" in refused(D.drop_x, box) and not D.have(D.X_KEYS))
ok("a missing box: refused", "four X boxes" in refused(D.drop_x, {**box, "access_secret": ""}))

print("YouTube")
w = fresh(); write_keys({**FAKE_YT, "YOUTUBE_REFRESH_TOKEN": "test-refresh"}); w.yt_hiccup_at = 1024 * 1024
vid = D.yt_upload(str(big), "A <test> title", "Line one\nLine two")
meta = json.loads(next(c[3] for c in w.calls if c[1] == D.YT_UPLOAD))
ok("upload in pieces, through one dropped line, arrives whole", vid == "vid123" and w.yt_bytes == big.read_bytes())
ok("title, description and settings as planned", meta == {"snippet": {"title": "A (test) title", "description": "Line one\nLine two", "categoryId": "22"},
                                                         "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False}}, str(meta))
w = fresh(); w.yt_handle = "@someoneelse"
ok("a sign-in for another channel: refused, nothing uploaded", "nothing uploaded" in refused(D.yt_upload, str(big), "t", "d") and not w.yt_bytes)

print("YouTube card from Key Drop and the phone sign-in")
w = fresh(); D.KEYFILE.write_text("NTFY_TOPIC=test-topic\n")
ok("a Client ID of the wrong shape: refused", "apps.googleusercontent.com" in refused(D.drop_youtube, {"client_id": "oops", "client_secret": "x"}))
note = D.drop_youtube({"client_id": FAKE_YT["YOUTUBE_CLIENT_ID"], "client_secret": FAKE_YT["YOUTUBE_CLIENT_SECRET"]})
ok("good values: saved, a code is buzzed, a sign-in is waiting", D.have(D.YT_APP_KEYS) and D.PENDING.exists() and "ABCD-EFGH" in BUZZED[-1] and "google.com/device" in BUZZED[-1], str(BUZZED))
ok("the code is not kept on disk and not in the log", "ABCD-EFGH" not in D.PENDING.read_text() + D.LOG.read_text())
ok("not tapped yet: keeps waiting", D.signin_tick() == "waiting" and D.PENDING.exists())
w.device = "ok"; w.yt_handle = "@someoneelse"
ok("tapped, but for another channel: not saved, a new code goes out", D.signin_tick() == "wrong channel" and not D.have(D.YT_KEYS) and D.PENDING.exists() and "new code" in BUZZED[-2], str(BUZZED[-2:]))
w.yt_handle = "@HeartbeatObservatory"
ok("tapped for the right channel: sign-in saved, door switched, he is told he is done",
   D.signin_tick() == "connected" and D.have(D.YT_KEYS) and not D.PENDING.exists() and json.loads(D.PATH_FILE.read_text())["youtube"] == "direct" and "You are done" in BUZZED[-1], str(BUZZED[-1:]))
ok("nothing waiting: the every-minute check does nothing", D.signin_tick() is None)
w = fresh(); write_keys(FAKE_YT); D.yt_signin_start()
p = json.loads(D.PENDING.read_text()); p["expires_at"] = time.time() - 5; D.PENDING.write_text(json.dumps(p))
ok("a code that ran out: cleared, and he is told how to get a new one", D.signin_tick() == "ran out" and not D.PENDING.exists() and "ran out" in BUZZED[-1])

print("The daily script's safety net (tools/social_daily.py)")
sys.argv = ["social_daily.py", "news"]
import social_daily as S
S.log = lambda m: None
S.once_a_day = lambda key: False          # no once-a-day marker files from a test
taken = []
S.post_uploaded = lambda platform, cid, video, text, title, x_tags=None, when=None: taken.append((platform, cid)) or "via-postiz"
w = fresh(); write_keys(FAKE_X); w.x_init_status = 403
S.POSTIZ_HAS.clear(); S.POSTIZ_HAS.update({"x": "postiz-x-id"})
r = S.post("x", "direct", str(video), "Line one.\nLine two.", "title")
ok("our door fails before sending while Postiz still has the channel: Postiz takes this one", r == "via-postiz" and taken == [("x", "postiz-x-id")], str(taken))
w = fresh(); w.x_post_status = 403; taken.clear()
try:
    S.post("x", "direct", str(video), "Line one.\nLine two.", "title"); raised = False
except Exception:
    raised = True
ok("our door fails AT the sending step: no second try through Postiz", raised and not taken)
w = fresh(); S.POSTIZ_HAS.clear(); w.x_init_status = 403
try:
    S.post("x", "direct", str(video), "Line one.\nLine two.", "title"); raised = False
except Exception:
    raised = True
ok("Postiz gone and our door fails: the failure is reported, as before", raised)
D.PATH_FILE.write_text(json.dumps({"x": "direct", "youtube": "postiz", "tiktok": "paused"}))
S.PATH_FILE = str(D.PATH_FILE); write_keys(FAKE_X)
ok("doors: X ours, YouTube Postiz, TikTok paused", S.route({"x": "px", "youtube": "py", "tiktok": "pt"}) == {"x": "direct", "youtube": "py"})
D.PATH_FILE.unlink()
ok("doors with no file: all Postiz, as before today", S.route({"x": "px", "youtube": "py", "tiktok": "pt"}) == {"tiktok": "pt", "youtube": "py", "x": "px"})
ok("doors when Postiz has dropped everything: X through ours (keys on file), the rest skipped", S.route({}) == {"x": "direct"})

print("When a platform has no door (tools/social_daily.py)")
lines, told, ran = [], [], []
S.log = lines.append
S.once_a_day = lambda key: True                             # the real one is swapped out, so still no marker files
S.buzz = lambda msg, key: told.append(msg) or True          # never a real buzz from a test
S.first_run_schema = lambda ch: None
S.do_news = lambda q, ch: ran.append(dict(ch))              # the step that also posts to our own site
S.QUEUE = str(TMP / "queue.json")
Path(S.QUEUE).write_text('{"news": {"platforms": ["tiktok", "youtube", "x"]}, "shows": []}', encoding="utf-8")
write_keys({}); S.channels = lambda: {}                     # no keys of ours on file, and Postiz gives us nothing
S.main()
ok("no outside door at all: the job still runs, so our own site gets its post", ran == [{}], str(ran))
ok("... he is told once, in plain words, with the free fix",
   len(told) == 1 and "no post goes to X, YouTube and TikTok" in told[0] and "Our own site still gets every post" in told[0]
   and "part 13 A" in told[0] and "once, not every day" in told[0], str(told))
ok("... and the log names the platforms and the reason", any("no door today for X, YouTube and TikTok" in l and "part 13" in l for l in lines), str(lines))
S.main()
ok("the next run, still no door: no second buzz", len(told) == 1 and len(ran) == 2, str(told))
write_keys({**FAKE_YT, "YOUTUBE_REFRESH_TOKEN": "test-refresh"}); S.main()
ok("after the YouTube sign-in: YouTube posts through our own door, no new buzz, the log says a door is back",
   ran[-1] == {"youtube": "direct"} and len(told) == 1 and any("a door is back for YouTube" in l for l in lines), str(ran[-1]) + str(lines[-3:]))
S.channels = lambda: {"x": "px", "tiktok": "pt", "youtube": "py"}; S.main()
ok("Postiz answers again: every door back, nothing left marked",
   D.state().get("shut") == {} and ran[-1] == {"tiktok": "pt", "youtube": "py", "x": "px"}, str(D.state()))
write_keys({}); S.channels = lambda: {"youtube": "py"}; S.main()
ok("only X and TikTok lose their door: one buzz, and it says YouTube still posts",
   len(told) == 2 and "no post goes to X and TikTok" in told[1] and "YouTube and our own site still get every post" in told[1]
   and "part 13 A" not in told[1] and "part 13 B" in told[1], str(told[-1:]))
S.buzz = lambda msg, key: False                             # the buzz itself does not go out
S.channels = lambda: {}; S.main()
ok("a buzz that did not go out is not counted as told (it is tried again on a later run)", "youtube" not in D.state().get("shut", {}), str(D.state()))
D.PATH_FILE.write_text(json.dumps({"tiktok": "paused"})); lines.clear(); S.channels = lambda: {}; S.route(S.channels())
ok("a platform paused on purpose is not reported as having no door", S.SHUT == ["youtube", "x"] and not any("TikTok" in l and "no door today" in l for l in lines), str(S.SHUT) + str(lines))
D.PATH_FILE.unlink()

print("Telling the AI side by itself (the AI mailbox)")
import contextlib, io
w = fresh(); write_keys(FAKE_X)
with contextlib.redirect_stdout(io.StringIO()):
    D.x_post("A dry run.", dry=True)
ok("a dry run tells nobody and marks nothing", not TOLD and "live" not in D.state(), str(TOLD) + str(D.state()))
D.x_post("The first real one.")
ok("the first real post on X: one mail, to Fable only, with the post's address",
   len(TOLD) == 1 and TOLD[0][1] == ("fable",) and "first real post" in TOLD[0][0] and "https://x.com/HeartbeatObserv/status/999" in TOLD[0][2], str(TOLD))
D.x_post("The second real one.")
ok("the posts after it: no more mail", len(TOLD) == 1, str(TOLD))
w.x_init_status = 403
refused(D.x_post, "This one cannot start.", str(video)); refused(D.x_post, "Nor this one.", str(video))
ok("X starts failing with no second door: ONE mail for the whole stretch, to Fable and Claude, with the reason, and it says the post did not go out",
   len(TOLD) == 2 and TOLD[1][1] == ("fable", "claude") and "our own door failed" in TOLD[1][0] and "did not start" in TOLD[1][2]
   and "did not go out" in TOLD[1][2] and bool(D.state()["live"]["x"].get("failing_since")), str(TOLD[1:]))
w.x_init_status = 200
D.x_post("It works again.")
ok("a post works again: no mail, the log says so, the mark is cleared",
   len(TOLD) == 2 and "works again" in D.LOG.read_text() and not D.state()["live"]["x"].get("failing_since"), str(D.state()))
w.x_post_status = 403
refused(D.x_post, "This one fails at the sending step.")
ok("a new stretch of failures gets its own mail; stopped at the sending step, it says the post may or may not be up",
   len(TOLD) == 3 and TOLD[2][1] == ("fable", "claude") and "may or may not be up" in TOLD[2][2], str(TOLD[2:]))
w = fresh(); write_keys(FAKE_X); w.x_init_status = 403; taken.clear()
S.POSTIZ_HAS.clear(); S.POSTIZ_HAS.update({"x": "postiz-x-id"})
S.post("x", "direct", str(video), "Line one.\nLine two.", "title")
ok("our door cannot start while Postiz still has the channel: the mail goes to Fable only and says Postiz took this one",
   len(TOLD) == 1 and TOLD[0][1] == ("fable",) and "Postiz took this one" in TOLD[0][0] and taken == [("x", "postiz-x-id")], str(TOLD) + str(taken))
S.POSTIZ_HAS.clear()
w = fresh(); write_keys(FAKE_X); D.tell = lambda subject, body, to=None: False
D.x_post("The mailbox is down.")
ok("a mail that did not go out is not counted as told", not D.state().get("live", {}).get("x", {}).get("first_ok"), str(D.state()))
D.tell = STUB_TELL; D.x_post("The mailbox is back.")
ok("... it goes out with the next post instead", len(TOLD) == 1 and "first real post" in TOLD[0][0], str(TOLD))
w = fresh(); write_keys({**FAKE_YT, "YOUTUBE_REFRESH_TOKEN": "test-refresh"})
D.yt_upload(str(big), "A title", "A description")
ok("the first real YouTube upload: one mail to Fable with the video's address",
   len(TOLD) == 1 and TOLD[0][1] == ("fable",) and "https://youtu.be/vid123" in TOLD[0][2], str(TOLD))
w = fresh(); D.KEYFILE.write_text("NTFY_TOPIC=test-topic\n"); D.drop_x(box)
ok("the X card lands: Fable is told at once, and the mail carries no key",
   len(TOLD) == 1 and TOLD[0][1] == ("fable",) and "X keys landed" in TOLD[0][0] and "@HeartbeatObserv" in TOLD[0][2]
   and not any(v in TOLD[0][0] + TOLD[0][2] for v in box.values()), str(TOLD))
w = fresh(); write_keys(FAKE_YT); D.yt_signin_start(); w.device = "ok"; D.signin_tick()
ok("the YouTube sign-in is finished: Fable is told at once, and the mail carries no key",
   len(TOLD) == 1 and TOLD[0][1] == ("fable",) and "sign-in is done" in TOLD[0][0] and "Heartbeat Observatory" in TOLD[0][2]
   and not any(v in TOLD[0][0] + TOLD[0][2] for v in ("test-refresh", "pass-2", "dev-code", FAKE_YT["YOUTUBE_CLIENT_SECRET"], FAKE_YT["YOUTUBE_CLIENT_ID"])), str(TOLD))
w = fresh(); write_keys(FAKE_YT); D.yt_signin_start(); w.device = "expired_token"
r = D.signin_tick()
ok("a sign-in that fails for a reason he cannot fix: the AIs are mailed, and his buzz no longer asks him to tell anyone",
   r == "no" and len(TOLD) == 1 and TOLD[0][1] == ("fable", "claude") and "nothing for you to pass on" in BUZZED[-1] and "Tell Claude" not in BUZZED[-1],
   str(TOLD) + str(BUZZED[-1:]))
w = fresh(); write_keys(FAKE_YT); D.yt_signin_start(); w.device = "expired_token"; D.tell = lambda subject, body, to=None: False
D.signin_tick(); D.tell = STUB_TELL
ok("... and if that mail cannot go out, the buzz still says who to tell", "Tell Claude" in BUZZED[-1], str(BUZZED[-1:]))
root = D.ROOT; D.ROOT = TMP                                  # no mailbox tool in the throwaway folder, so nothing can be sent
ok("the mail step itself never raises, and says so when nothing went out", REAL_TELL("test", "test") is False)
D.ROOT = root

import shutil
shutil.rmtree(TMP, ignore_errors=True)
print("ALL OK" if all(results) else f"{results.count(False)} FAILED of {len(results)}")
sys.exit(0 if all(results) else 1)
