"""Good-news and too-quiet buzzes for the crypto lane (Jaron 10/22: "we've only talked about it going down").
Runs every 10 minutes (task "Crypto Notify"). Each buzz fires once:
  - the FIRST real crypto trade placed
  - the lane's settled money crosses +$10, +$25, +$50, +$100, +$200 (and the $100 base doubling)
  - too quiet: no real crypto trade in 3 hours between 9 AM and 1 AM ET (at most once per 6 h) - something may be stuck
Downside buzzes (phase change, stop, $65) live in crypto_decide.py. State: state/.crypto-notify.json."""
import json, os, subprocess, sys, time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import importlib.util as _u
_s = _u.spec_from_file_location("crypto_decide", os.path.join(HERE, "crypto_decide.py")); CD = _u.module_from_spec(_s); _s.loader.exec_module(CD)
from settings import setting  # noqa: E402

STATE = os.path.join(ROOT, "state", ".crypto-notify.json")
MILESTONES = [10, 25, 50, 100, 200]


def buzz(title, line):
    subprocess.run([sys.executable, os.path.join(HERE, "ntfy-say.py"), title, line], timeout=30)


def main():
    st = json.load(open(STATE)) if os.path.exists(STATE) else {}
    placed = [json.loads(l) for l in open(CD.DECISIONS, encoding="utf-8")] if os.path.exists(CD.DECISIONS) else []
    placed = [d for d in placed if d.get("placed") and d.get("mode") == "LIVE"]
    if placed and not st.get("first"):
        d = placed[0]
        buzz("Crypto lane: first real trade", f"{d['coin'].upper()} {d['tf']} - {d.get('note', '')[:120]}")
        st["first"] = d["at"]
    since = str(setting("crypto_lane_start", "2026-10-22"))[:10]
    try:
        pnl = CD.crypto_lane_pnl(since)
        for m in MILESTONES:
            if pnl >= m and str(m) not in st.get("hit", []):
                buzz("Crypto lane is UP", f"crypto lane settled money +${pnl:.2f} (passed +${m})")
                st.setdefault("hit", []).append(str(m))
    except Exception:
        pass
    now = datetime.now(timezone.utc)
    et_hour = (now.hour - 4) % 24
    last = max((d["at"] for d in placed), default=None) or since + "T23:00:00+00:00"
    quiet_h = (now - datetime.fromisoformat(last)).total_seconds() / 3600
    # 11/13: crypto routines are paused on purpose (Jaron); quiet is expected, so no buzz until they are turned back on.
    if False and (et_hour >= 9 or et_hour < 1) and quiet_h >= 3 and time.time() - st.get("quiet_at", 0) > 6 * 3600:
        buzz("Crypto lane quiet", f"no real crypto trade in {quiet_h:.0f} h - bots may not be calling or agreeing; Claude will check")
        st["quiet_at"] = time.time()
    json.dump(st, open(STATE, "w"))


if __name__ == "__main__":
    main()
