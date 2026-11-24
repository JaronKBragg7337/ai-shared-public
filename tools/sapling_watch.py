"""sapling_watch.py - look in on Sapling every 30 minutes, read-only (11/22 4:20 AM).

Sapling crashed at 7:35 PM 11/21 and sat down for 8.5 hours before anyone noticed. This watcher only READS Sapling's relay
(127.0.0.1:7338/api/state). It never starts, stops or changes Sapling (Sapling jobs stay Kimi's).

It logs an "uh-oh" first (tools/firsts.py -> Jaron's phone + Claude's mailbox) once per episode when:
  - Sapling CRASHED (last_stop.kind == "crash") and is still down, or
  - it is down for two checks in a row for any other reason, outside the news window (3:45-6:30 AM, when the render stops it
    on purpose), and the stop was not the owner's own stop file, or
  - the relay itself does not answer for two checks in a row.
The episode resets when Sapling is running again. State: state/sapling-watch.json. Task "Sapling Watch", every 30 min.
"""
import json, subprocess, sys, urllib.request
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STORE = ROOT / "state" / "sapling-watch.json"


def uh_oh(what, why, proof):
    subprocess.run([sys.executable, str(ROOT / "tools" / "firsts.py"), "add", "--project", "sapling", "--kind", "uh-oh",
                    "--checked", "--by", "sapling-watch", "--what", what, "--why", why, "--proof", proof],
                   capture_output=True, timeout=120, stdin=subprocess.DEVNULL)


def heartbeat_alive():
    """True if a 'sapling.heartbeat run' python process exists (read-only process list)."""
    try:
        out = subprocess.run(["powershell", "-NoProfile", "-Command",
                              "(Get-CimInstance Win32_Process -Filter \"Name like 'python%'\" | Where-Object { $_.CommandLine -like '*sapling.heartbeat*' } | Measure-Object).Count"],
                             capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL).stdout.strip()
        return out.isdigit() and int(out) > 0
    except Exception:
        return False


def main():
    prev = json.loads(STORE.read_text(encoding="utf-8")) if STORE.exists() else {}
    now = datetime.now()
    in_news = (now.hour == 3 and now.minute >= 45) or 4 <= now.hour < 6 or (now.hour == 6 and now.minute < 30)
    active, state = {}, {"at": now.isoformat(timespec="seconds")}
    try:
        with urllib.request.urlopen("http://127.0.0.1:7338/api/state", timeout=20) as r:
            d = json.loads(r.read().decode("utf-8"))
        running = bool(d.get("running"))
        stop = d.get("last_stop") or {}
        state.update(running=running, tick=d.get("tick"), stop_kind=stop.get("kind"), stop_who=stop.get("who"))
        alive = heartbeat_alive()
        state["process_alive"] = alive
        if not running and alive:
            # 11/22 1:45 PM false alarm: a heavy job starved the CPU, so Sapling's control room timed out while the heartbeat was
            # alive and still ticking. Process alive + slow answer = "slow", only an uh-oh if it stays that way on the next check.
            if prev.get("slow_last_check"):
                active["slow"] = ("Sapling is alive but not answering for over 30 minutes",
                                  "Its heartbeat process exists but its control room keeps timing out (hung, or starved by a heavy job)",
                                  f"/api/state at {state['at']}: running false, hb_error {str(d.get('hb_error'))[:120]}, heartbeat process alive")
            state["slow_last_check"] = True
        elif not running:
            stale = isinstance(stop.get("tick"), int) and isinstance(d.get("tick"), int) and d["tick"] - stop["tick"] > 10
            # 11/22 9:15 PM false alarm: Sapling CHOSE to stop at 8:18 PM (rest 0.98) and this watcher called it "down". Its own
            # stop is sleep (Jaron 10/26): tools/wake.py in projects/sapling wakes it at the first check after midnight. So a
            # self-stop is fine until 1 AM the next day; after that it should have woken, and that IS an uh-oh.
            stop_day = str(stop.get("ts") or "")[:10]
            self_sleep = stop.get("who") == "self" and not stale
            if stale:   # 11/22: the heartbeat can vanish with no stop record; the last stop note is then an old one
                active["vanished"] = (f"Sapling stopped with no stop record (last tick {d.get('tick')})",
                                      "Its heartbeat process is gone but it never wrote why; the newest stop note is older",
                                      f"/api/state at {state['at']}: running false, tick {d.get('tick')}, newest stop note {json.dumps(stop)[:200]}")
            elif self_sleep and (stop_day >= now.strftime("%Y-%m-%d") or now.hour < 1):
                state["asleep"] = f"chose to sleep at {stop.get('ts')}; its own wake starts it after midnight"
            elif self_sleep:
                active["no_wake"] = ("Sapling chose to sleep and didn't wake up after midnight",
                                     "Its own wake (task Sapling Wake) should start it at the first check after midnight",
                                     f"/api/state at {state['at']}: running false, self-stop at {stop.get('ts')}, tick {stop.get('tick')}")
            elif stop.get("kind") == "crash":
                active["crash"] = (f"Sapling crashed and is down (tick {stop.get('tick')})",
                                   "Its heartbeat stopped on an error and did not come back by itself",
                                   f"/api/state at {state['at']}: running false, last_stop {json.dumps(stop)[:300]}")
            elif prev.get("running") is False and not in_news and stop.get("who") != "owner":
                active["down"] = ("Sapling has been down for over 30 minutes",
                                  "Not running across two checks, outside the news window, and not an owner stop",
                                  f"/api/state at {state['at']}: running false, hb_error {str(d.get('hb_error'))[:160]}")
    except Exception as e:
        state.update(running=None, relay_error=str(e)[:160])
        if prev.get("relay_error"):
            active["relay"] = ("Sapling's relay is not answering",
                               "Two checks in a row could not reach 127.0.0.1:7338, so its page can't show anything",
                               f"{state['at']}: {str(e)[:200]}")
    fired = set(prev.get("fired", []))
    for key, (what, why, proof) in active.items():
        if key not in fired:
            uh_oh(what, why, proof)
            fired.add(key)
            print("uh-oh:", what)
    state["fired"] = sorted(fired & set(active))
    STORE.write_text(json.dumps(state, indent=1), encoding="utf-8")
    print(json.dumps(state))


if __name__ == "__main__":
    main()
