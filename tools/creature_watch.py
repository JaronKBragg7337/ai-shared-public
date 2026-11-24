"""creature_watch.py - look in on her every 30 minutes so nobody has to catch trouble by luck (11/21 10 PM).

Jaron found the crystal loop only because he happened to ask "how is she doing" at the right time. This watcher is the
team's standing eye. It only READS her (GET /state, GET /events) - it never changes her or her world.

It logs an "uh-oh" first (tools/firsts.py -> Jaron's phone + Claude's mailbox) once per episode when:
  - she stays starving (hunger >= 0.95) or exhausted (energy <= 0.05) across two checks in a row,
  - one action on one thing is >= 85% of her last ~200 ticks of actions (at least 60 of them) - a loop like the crystal,
  - her tick has not moved between two checks (she may be frozen).
When the problem clears, the episode resets so a new one can alert again. State: state/creature-watch.json.
Task "Creature Watch" runs it every 30 min. Her decisions stay the team's; this only makes sure we notice.
"""
import json, subprocess, sys, urllib.request
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://creature-observatory.acsassociation7337.workers.dev"
STORE = ROOT / "state" / "creature-watch.json"


def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "creature-watch"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def uh_oh(what, why, proof):
    subprocess.run([sys.executable, str(ROOT / "tools" / "firsts.py"), "add", "--project", "creature", "--kind", "uh-oh",
                    "--checked", "--by", "creature-watch", "--what", what, "--why", why, "--proof", proof],
                   capture_output=True, timeout=120, stdin=subprocess.DEVNULL)


def main():
    prev = json.loads(STORE.read_text(encoding="utf-8")) if STORE.exists() else {}
    s = get("/state")
    tick, mood = s["tick"], s["mood"]
    ev = get(f"/events?since={max(0, tick - 200)}&limit=500")
    ev = ev if isinstance(ev, list) else ev.get("events", [])
    acts = [e.get("detail", "") for e in ev if e.get("type") in ("touched", "ate", "slept", "woke")]
    now = datetime.now().isoformat(timespec="seconds")
    active = {}

    starving = mood.get("hunger", 0) >= 0.95
    exhausted = mood.get("energy", 1) <= 0.05
    if (starving or exhausted) and prev.get("low_last_check"):
        active["low"] = ("She is stuck " + ("starving" if starving else "") + (" and " if starving and exhausted else "")
                         + ("exhausted" if exhausted else "") + " for over 30 minutes",
                         "Her body is at its limit across two checks in a row; something may be keeping her from eating or resting",
                         f"GET /state tick {tick} at {now}: hunger {mood.get('hunger'):.2f}, energy {mood.get('energy'):.2f}, curiosity {mood.get('curiosity'):.2f}")
    if len(acts) >= 60:
        top, n = Counter(acts).most_common(1)[0]
        if n / len(acts) >= 0.85:
            active["loop"] = (f"She keeps doing one thing over and over: \"{top}\" ({n} of her last {len(acts)} actions)",
                              "A loop like the crystal one: one action is crowding out everything else",
                              f"GET /events since tick {tick - 200} at {now}: {n}/{len(acts)} actions were \"{top}\"; mood {json.dumps(mood)}")
    if prev.get("tick") == tick:
        active["frozen"] = ("Her clock has not moved in 30 minutes",
                            "She may be frozen (no ticks), not just quiet",
                            f"GET /state tick stayed {tick} between checks ({prev.get('at')} -> {now})")

    fired = set(prev.get("fired", []))
    for key, (what, why, proof) in active.items():
        if key not in fired:
            uh_oh(what, why, proof)
            fired.add(key)
            print("uh-oh:", what)
    fired &= set(active)          # a cleared problem can alert again next time
    STORE.write_text(json.dumps({"at": now, "tick": tick, "low_last_check": starving or exhausted,
                                 "fired": sorted(fired), "mood": mood}, indent=1), encoding="utf-8")
    print(f"tick {tick} mood {mood} active {sorted(active)}")


if __name__ == "__main__":
    main()
