"""Key drop, MSI side (Jaron 10/19: "something on my website where I can paste keys ... then I won't be needed at the MSI").
heartbeatobservatory.com/admin/keys/ encrypts each pasted key in the browser with the MSI's public key (state/keydrop_public.b64);
only ~/.secrets/keydrop_private.pem (never leaves this machine) can open it. This script (task "HB Key Drop", every 1 min):
  1. fetches waiting drops (service role), 2. decrypts, 3. backs up the old file and writes the new value where the tools read it,
  4. tests it read-only, 5. wipes the encrypted payload from the database and marks the row done/failed, 6. buzzes Jaron.
Never prints or logs a key value."""
import os, json, base64, datetime, shutil, subprocess, time, urllib.request, hashlib, hmac, urllib.parse, socket
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HOME = os.path.expanduser("~"); SEC = os.path.join(HOME, ".secrets")
ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
LOG = os.path.join(ROOT, "state", "key-drop.log")
NOWIN = 0x08000000


def env():
    e = {}
    for l in open(os.path.join(SEC, "keys.env"), encoding="utf-8"):
        if "=" in l and not l.startswith("#"): k, v = l.strip().split("=", 1); e[k] = v.strip()
    return e


E = env(); URL = E["SUPABASE_URL"].rstrip("/") + "/rest/v1/key_drops"; SR = E["SUPABASE_SERVICE_ROLE_KEY"]
H = {"apikey": SR, "Authorization": "Bearer " + SR, "Content-Type": "application/json"}


def log(m):
    open(LOG, "a", encoding="utf-8").write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M ") + m + "\n")


def buzz(m):
    try: urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/" + E["NTFY_TOPIC"], m.encode(), {"Title": "Key drop"}), timeout=15)
    except Exception: pass


def req(method, url, body=None):
    r = urllib.request.Request(url, json.dumps(body).encode() if body is not None else None, H, method=method)
    return json.loads(urllib.request.urlopen(r, timeout=30).read() or "null")


def decrypt(blob):
    priv = serialization.load_pem_private_key(open(os.path.join(SEC, "keydrop_private.pem"), "rb").read(), None)
    aes = priv.decrypt(base64.b64decode(blob["k"]), padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return json.loads(AESGCM(aes).decrypt(base64.b64decode(blob["iv"]), base64.b64decode(blob["ct"]), None))


def backup(path):
    if os.path.exists(path): shutil.copy(path, path + ".bak-" + datetime.datetime.now().strftime("%Y%m%d-%H%M"))


def set_env(path, values):
    lines = open(path, encoding="utf-8").read().split("\n") if os.path.exists(path) else []
    for k, v in values.items():
        for i, l in enumerate(lines):
            if l.startswith(k + "="): lines[i] = k + "=" + v; break
        else: lines.append(k + "=" + v)
    open(path, "w", encoding="utf-8").write("\n".join(lines).rstrip("\n") + "\n")


def kraken_test(k, s):
    data = {"nonce": str(int(time.time() * 1000))}; post = urllib.parse.urlencode(data); path = "/0/private/Balance"
    sig = base64.b64encode(hmac.new(base64.b64decode(s), path.encode() + hashlib.sha256((data["nonce"] + post).encode()).digest(), hashlib.sha512).digest()).decode()
    r = json.loads(urllib.request.urlopen(urllib.request.Request("https://api.kraken.com" + path, post.encode(), {"API-Key": k, "API-Sign": sig, "User-Agent": "hb-keydrop"}), timeout=20).read())
    if r.get("error"): raise RuntimeError("Kraken said: " + ", ".join(r["error"]))
    return "Kraken answered (balance check OK)"


def polymarket_restart():
    # 10/19: "schtasks /End" did NOT stop the running service (started 10/17 outside the task), so it kept the old key and the
    # balance check passed on the OLD key; it broke when Jaron revoked it. Now: stop exactly the process listening on 8765 (by
    # PID, never by name), start the task, and require a NEW process before calling it done.
    ps = ("$c = Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1; "
          "if ($c) { Stop-Process -Id $c.OwningProcess -Force }")
    old = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1).OwningProcess"],
                         capture_output=True, text=True, creationflags=NOWIN).stdout.strip()
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, creationflags=NOWIN)
    time.sleep(3); subprocess.run(["schtasks", "/Run", "/TN", "Polymarket MCP"], capture_output=True, creationflags=NOWIN)
    for _ in range(20):
        time.sleep(3)
        try: socket.create_connection(("127.0.0.1", 8765), timeout=3).close(); break
        except OSError: pass
    else: raise RuntimeError("the Polymarket service didn't come back after the new key - old key file is backed up")
    new = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-NetTCPConnection -LocalPort 8765 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1).OwningProcess"],
                         capture_output=True, text=True, creationflags=NOWIN).stdout.strip()
    if old and new == old: raise RuntimeError("the Polymarket service did not restart, so it may still be on the old key")
    out = subprocess.run(["python", os.path.join(ROOT, "tools", "desk.py"), "account"], capture_output=True, text=True, timeout=120, creationflags=NOWIN)
    txt = (out.stdout + out.stderr).lower()
    if out.returncode or "available to trade" not in txt: raise RuntimeError("Polymarket service is up but the balance check failed")
    return "Polymarket service restarted with the new key; balance check OK"


# ---- known kinds of keys: how to recognize them, what they're called, how to test them (read-only calls only) ----
def _get(url, headers, data=None):
    r = urllib.request.Request(url, data, {"User-Agent": "hb-keydrop", **headers}); return urllib.request.urlopen(r, timeout=20).status


KNOWN = {   # name: (label, prefixes, test)
    "ANTHROPIC_API_KEY": ("Anthropic (Claude) API", ("sk-ant-",), lambda v: _get("https://api.anthropic.com/v1/models", {"x-api-key": v, "anthropic-version": "2023-06-01", **({"anthropic-workspace-id": E["ANTHROPIC_WORKSPACE_ID"]} if E.get("ANTHROPIC_WORKSPACE_ID") else {})})),
    "OPENAI_API_KEY": ("OpenAI API", ("sk-proj-", "sk-svcacct-", "sk-"), lambda v: _get("https://api.openai.com/v1/models", {"Authorization": "Bearer " + v})),
    "XAI_API_KEY": ("xAI (Grok) API", ("xai-",), lambda v: _get("https://api.x.ai/v1/models", {"Authorization": "Bearer " + v})),
    "DEEPSEEK_API_KEY": ("DeepSeek API", ("sk-",), lambda v: _get("https://api.deepseek.com/models", {"Authorization": "Bearer " + v})),
    "PERPLEXITY_API_KEY": ("Perplexity API", ("pplx-",), None),
    "GITHUB_TOKEN": ("GitHub token", ("ghp_", "github_pat_", "gho_"), lambda v: _get("https://api.github.com/user", {"Authorization": "Bearer " + v})),
    "RUNPOD_API_KEY": ("RunPod (cloud GPU)", ("rpa_",), lambda v: _get("https://api.runpod.io/graphql?api_key=" + v, {"Content-Type": "application/json"}, b'{"query":"{ myself { id } }"}')),
    "VERCEL_TOKEN": ("Vercel (website hosting)", (), lambda v: _get("https://api.vercel.com/v2/user", {"Authorization": "Bearer " + v})),
    "SUPABASE_ACCESS_TOKEN": ("Supabase management token", ("sbp_",), lambda v: _get("https://api.supabase.com/v1/projects", {"Authorization": "Bearer " + v})),
    "SUPABASE_SERVICE_ROLE_KEY": ("Supabase service key (full database access)", ("sb_secret_",), None),
    "SUPABASE_PUBLISHABLE_KEY": ("Supabase public key (safe to share)", ("sb_publishable_",), None),
    "STRIPE_SECRET_KEY": ("Stripe", ("sk_live_", "sk_test_", "rk_live_"), None),
    "NTFY_TOPIC": ("Phone alerts topic (ntfy)", (), None),
    # 11/24: our own posting to X and YouTube (tools/direct_post.py). They arrive as two cards with several boxes each
    # (X_POSTING, YOUTUBE_UPLOAD below) and are tested together there before anything is saved.
    "X_API_KEY": ("X posting, our own: API key", (), None),
    "X_API_SECRET": ("X posting, our own: API key secret", (), None),
    "X_ACCESS_TOKEN": ("X posting, our own: access token", (), None),
    "X_ACCESS_SECRET": ("X posting, our own: access token secret", (), None),
    "YOUTUBE_CLIENT_ID": ("YouTube upload, our own: client ID", (), None),
    "YOUTUBE_CLIENT_SECRET": ("YouTube upload, our own: client secret", (), None),
    "YOUTUBE_REFRESH_TOKEN": ("YouTube upload, our own: the one-time phone sign-in (made on the MSI, never pasted)", (), None),
}


def test_key(name, v):
    k = KNOWN.get(name)
    if not k or not k[2] or not v: return None
    try: k[2](v); return "works"
    except urllib.error.HTTPError as e: return f"rejected ({e.code})" if e.code in (401, 403) else f"answered {e.code}"
    except Exception as e: return "couldn't check (" + type(e).__name__ + ")"


def guess_name(v):
    """No name given: match the prefix; when two kinds share one (OpenAI and DeepSeek both start sk-) the test decides."""
    cands = [n for n, (_, pre, _) in KNOWN.items() if any(v.startswith(x) for x in pre)]
    cands.sort(key=lambda n: -max(len(x) for x in KNOWN[n][1] if v.startswith(x)))
    for n in cands:
        if KNOWN[n][2] is None or test_key(n, v) == "works": return n
    return None


def describe(path):
    """name -> (filled, the comment text above it) for a KEY=value file."""
    out, notes = {}, []
    for l in open(path, encoding="utf-8").read().split("\n"):
        if l.startswith("#"):
            t = l.lstrip("# ").strip()
            if t and not set(t) <= set("-= "): notes.append(t.strip("- ").strip())
            continue
        if "=" in l:
            k, val = l.split("=", 1)
            if k.strip().replace("_", "").isalnum(): out[k.strip()] = (bool(val.strip()), " ".join(notes[-3:])[:220])
            notes = []
    return out


def inventory(force=False):
    """Names only (never values) -> key_inventory table + state/KEYS.md, whenever a key file changed."""
    files = {"keys.env": os.path.join(SEC, "keys.env"), "kraken.env": os.path.join(SEC, "kraken.env"), "Polymarket.txt": os.path.join(SEC, "Polymarket.txt")}
    stamp = os.path.join(ROOT, "state", "key-inventory.stamp")
    sig = "|".join(f"{f}:{os.path.getmtime(p):.0f}" for f, p in files.items() if os.path.exists(p))
    if not force and os.path.exists(stamp) and open(stamp).read() == sig: return
    now = datetime.datetime.now(datetime.timezone.utc).isoformat(); rows = []
    for f in ("keys.env", "kraken.env"):
        if not os.path.exists(files[f]): continue
        vals = {}
        for l in open(files[f], encoding="utf-8"):
            if "=" in l and not l.startswith("#"): k, v = l.strip().split("=", 1); vals[k] = v.strip()
        for name, (filled, note) in describe(files[f]).items():
            label = KNOWN.get(name, (name.replace("_", " ").title(),))[0]
            if name.startswith("KRAKEN"): label = "Kraken " + ("API key" if name.endswith("API_KEY") else "private key")
            st = (test_key(name, vals.get(name, "")) or "saved") if filled else "empty"
            rows.append({"name": name, "label": label, "what": note, "file": f, "filled": filled, "status": st, "tested_at": now, "updated_at": now})
    kr = [r for r in rows if r["name"].startswith("KRAKEN_")]
    if len(kr) == 2 and all(r["filled"] for r in kr):
        kv = {}
        for l in open(files["kraken.env"], encoding="utf-8"):
            if "=" in l and not l.startswith("#"): k, v = l.strip().split("=", 1); kv[k] = v.strip()
        try: kraken_test(kv["KRAKEN_API_KEY"], kv["KRAKEN_PRIVATE_KEY"]); st = "works"
        except Exception as e: st = "failed: " + str(e)[:60]
        for r in kr: r["status"] = st
    if os.path.exists(files["Polymarket.txt"]):
        rows.append({"name": "POLYMARKET", "label": "Polymarket US trading (key id + secret)", "what": "Used by the trading service on port 8765 (desk.py / desk-trade.py).",
                     "file": "Polymarket.txt", "filled": True, "status": "in use", "tested_at": now, "updated_at": now})
    inv = URL.replace("key_drops", "key_inventory")
    urllib.request.urlopen(urllib.request.Request(inv, json.dumps(rows).encode(), dict(H, Prefer="resolution=merge-duplicates"), method="POST"), timeout=30)
    names = ",".join('"' + r["name"] + '"' for r in rows)
    req("DELETE", inv + "?name=not.in.(" + urllib.parse.quote(names) + ")")
    md = ["# Keys on the MSI (names only - generated by tools/key_drop.py, " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + ")",
          "Values live in ~/.secrets (keys.env, kraken.env, Polymarket.txt); read the value there when you need it. New keys arrive",
          "through heartbeatobservatory.com/admin/keys/ (Key Drop), so Jaron never has to tell you a key exists: check this list first.", "",
          "| Name | What | File | Status |", "|---|---|---|---|"]
    md += [f"| {r['name']} | {r['label']}: {r['what'][:120]} | {r['file']} | {r['status']} |" for r in rows]
    open(os.path.join(ROOT, "state", "KEYS.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    open(stamp, "w").write(sig)


def my_fingerprint():
    return hashlib.sha256(base64.b64decode(open(os.path.join(ROOT, "state", "keydrop_public.b64")).read().strip())).hexdigest()[:16]


def handle(row):
    fp = (row.get("blob") or {}).get("fp")
    if fp and fp != my_fingerprint():   # the page locked it with a different key than ours: the page may have been tampered with
        buzz("KEY DROP ALARM: a key was locked with the wrong lock key - the page may have been changed. Don't send keys; tell Claude.")
        raise RuntimeError("lock fingerprint mismatch - the page used a key that isn't the MSI's")
    v = decrypt(row["blob"]); t = row["target"]
    if t == "kraken":
        k, s = v.get("api_key", "").strip(), v.get("private_key", "").strip()
        if not k or not s: raise RuntimeError("both Kraken boxes are needed")
        res = kraken_test(k, s)                       # test BEFORE replacing the working key
        p = os.path.join(SEC, "kraken.env"); backup(p); set_env(p, {"KRAKEN_API_KEY": k, "KRAKEN_PRIVATE_KEY": s}); return res
    if t == "polymarket":
        k, s = v.get("key_id", "").strip(), v.get("secret", "").strip()
        if not k or not s or " " in k + s: raise RuntimeError("both Polymarket boxes are needed (no spaces)")
        p = os.path.join(SEC, "Polymarket.txt"); backup(p); open(p, "w", encoding="utf-8").write(k + "\n" + s + "\n")
        try: return polymarket_restart()
        except Exception:
            os.remove(p)                               # fall back to the old key file the service used before
            polymarket_restart(); raise
    if t == "env":
        name = row.get("env_name") or ""
        if name in ("X_POSTING", "YOUTUBE_UPLOAD"):   # 11/24: one card, several boxes (the page's X and YouTube tabs)
            import direct_post                         # it tests the values together, saves them itself, never logs one
            return direct_post.drop_x(v) if name == "X_POSTING" else direct_post.drop_youtube(v)
        val = v.get("value", "").strip()
        if not val: raise RuntimeError("the value box was empty")
        if not name: name = guess_name(val) or ""
        if not name: raise RuntimeError("couldn't tell what this key is - send it again with a name")
        p = os.path.join(SEC, "keys.env"); backup(p)
        txt = open(p, encoding="utf-8").read() if os.path.exists(p) else ""
        if not any(l.startswith(name + "=") for l in txt.split("\n")):   # a new key gets a comment line so every AI knows what it is
            open(p, "a", encoding="utf-8").write(("" if txt.endswith("\n") else "\n") + f"# {KNOWN.get(name, (name,))[0]} - added from Jaron's phone (Key Drop) {datetime.date.today()}\n")
        set_env(p, {name: val}); st = test_key(name, val)
        return f"saved as {name}" + (f"; test: {st}" if st else "")
    raise RuntimeError("unknown target")


def main():
    rows = req("GET", URL + "?status=eq.waiting&select=id,target,env_name,blob&order=created_at")
    for row in rows or []:
        label = row["target"] if row["target"] != "env" else row.get("env_name")
        try: note, status = handle(row), "done"
        except Exception as e: note, status = str(e)[:200], "failed"
        req("PATCH", URL + "?id=eq." + row["id"], {"blob": None, "status": status, "note": note, "done_at": datetime.datetime.now(datetime.timezone.utc).isoformat()})
        log(f"{label}: {status} - {note}"); buzz(f"{label or 'key'}: {status}. {note}")
    try:                                               # 11/24: is a YouTube sign-in waiting for Jaron's tap? Ask Google once.
        import direct_post
        direct_post.signin_tick()
    except Exception as e: log(f"direct_post sign-in check: {type(e).__name__}: {str(e)[:120]}")
    inventory(force=bool(rows))


if __name__ == "__main__":
    try: main()
    except Exception as e: log(f"CRASH {type(e).__name__}: {str(e)[:200]}")
