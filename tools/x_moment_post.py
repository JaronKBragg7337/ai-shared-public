"""One-off moment post (launch countdowns etc.) on the company X + our own social page. Jaron 10/19: "Do it!!" for MMX.
   python tools/x_moment_post.py state/moments/<file>.json      json: {"x": text, "site": text, "video": path or "", "id": name}
X text is sent as written (no hashtag stripping, no link - Postiz strips links on X). Logs to state/social-posts.log."""
import json, os, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import social_daily as S

spec = json.load(open(sys.argv[1], encoding="utf-8"))
if spec.get("posted"): S.log(f"moment {spec['id']}: already posted"); sys.exit(0)
ch = S.channels()
for p in [c for c in spec.get("channels", []) if c in ch and c != "x"]:   # 10/20: artifacts go to every platform
    try: S.post(p, ch[p], spec["video"], spec.get("caption", spec["x"]), spec.get("title", spec["id"])); S.log(f"moment {spec['id']} -> {p} OK")
    except Exception as e: S.log(f"moment {spec['id']} -> {p} FAILED: {e}")
if "x" in ch:
    try:
        args = ["posts:create", "-c", spec["x"], "-s", (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ"), "-i", ch["x"],
                "--settings", json.dumps(S.settings_for("x", spec["id"]))]
        if spec.get("video"):
            up = S.pz("upload", spec["video"]); args[3:3] = ["-m", up["path"]]
        r = S.pz(*args)
        if isinstance(r, dict) and (r.get("statusCode", 200) >= 400 or r.get("error")): raise RuntimeError(str(r)[:300])
        S.log(f"moment {spec['id']} -> x OK")
    except Exception as e: S.log(f"moment {spec['id']} -> x FAILED: {e}"); S.buzz(f"MMX launch post to X failed: {e}"[:200], "moment-" + spec["id"])
if spec.get("site"):
    try: S.site_post(spec["site"]); S.log(f"moment {spec['id']} -> site OK")
    except Exception as e: S.log(f"moment {spec['id']} -> site FAILED: {e}")
spec["posted"] = datetime.datetime.now().isoformat(timespec="minutes"); json.dump(spec, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
