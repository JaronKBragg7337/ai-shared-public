"""Safety signal - one plain level so Jaron's network knows when to get ready (Jaron 11/1).
Not about odds, about safety: AIs never hold something back to "protect" him. If it's real, it's known.

Levels 0-5 (Jaron 11/3: escalation can SKIP levels; the level is the HIGHEST box ticked, never an average or a mood).
CHECKLIST - observable facts only. When unsure between two levels, take the higher one ("fearful over oblivious").
  0 CALM        no box below ticked
  1 WATCH       [ ] real conflict/tension abroad involving the US or allies (strikes, threats, closures), same targets as before
  2 NEW TARGETS [ ] a side names, adds or updates targets (new countries, new bases, new kinds of target), US or ALLIES
                [ ] direct fire between US/allied forces and an adversary, still contained to one area
                [ ] a state fuel/energy emergency in Indiana
              -> top off gas, check the supplies list, make sure everyone in the network can reach the group
  BASELINE RULE (Jaron 11/3 1:54 PM): attacks that have gone on for weeks in the same hot zone (Houthis vs Saudi
  shipping in the Red Sea, mines/tankers around Hormuz) are BACKGROUND: they keep it at 1-2. Level 3 needs something
  NEW against that baseline. If you can't tell new from background, count it as new.
  3 WIDENING    [ ] an attack actually LANDS on US or allied MILITARY forces, bases or ships outside the original zone
                [ ] a NEW place: an attack inside a country not hit before, or outside the usual sea lanes
                [ ] a NEW kind of target: land infrastructure (refineries, power plants, big oil hubs), not ships at sea
                [ ] a clear step up: many hits in one day, or one huge one (like the 2019 Abqaiq strike)
                [ ] a national fuel/price shock (e.g. long Hormuz closure + sharp US gas spike, rationing talk)
                [ ] a major-outlet report that a side is preparing CHEMICAL/BIOLOGICAL weapons use against US or
                    allies, even if disputed (added 11/3; confirmed steps or any use = 4)
              -> gas full, some cash on hand, supplies checked, test-message the whole network
  4 GET READY   [ ] any DHS NTAS bulletin/alert, or a credible named threat to the US homeland
                [ ] an attack or major cyberattack on US soil anywhere (grid, pipelines, water, comms)
                [ ] nuclear threat moves from words to steps (doctrine change + mobilization or a test)
              -> supplies packed, vehicles ready, meeting point confirmed, everyone checked in
  5 MOVE        [ ] an attack, alert, or evacuation/shelter order for Indiana or the Midwest
                [ ] regional grid, fuel or phone networks failing
              -> run the transportation plan now; head to the meeting point

Use:
  python tools/safety_signal.py set 2 "boxes ticked + why, with sources"   # any AI (Satya runs this)
  python tools/safety_signal.py check                        # free DHS NTAS feed; raises to 4 on any active alert
  python tools/safety_signal.py show
Every level CHANGE buzzes Jaron's phone (ntfy: high at 2, urgent at 3+). Same level = no buzz. History: state/safety-signal.md
"""
import json, os, sys, urllib.request, re
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.path.join(ROOT, "state", "safety-signal.json")
LOG = os.path.join(ROOT, "state", "safety-signal.md")
NAMES = {0: "CALM", 1: "WATCH", 2: "NEW TARGETS", 3: "WIDENING", 4: "GET READY", 5: "MOVE"}
TODO = {0: "Nothing to do.", 1: "Nothing to do yet. Stay aware.",
        2: "Top off gas, check the supplies list, make sure everyone in the network can reach the group.",
        3: "Gas full, some cash on hand, supplies checked, test-message the whole network.",
        4: "Supplies packed, vehicles ready, meeting point confirmed, everyone checked in.",
        5: "Run the transportation plan now. Head to the meeting point."}


def load():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except Exception:
        return {"level": 0, "why": "", "at": ""}


def buzz(level, why):
    topic = [l.split("=", 1)[1].strip() for l in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8-sig")
             if l.startswith("NTFY_TOPIC=")][0]
    body = f"{TODO[level]}\n\nWhy: {why}"
    hdr = {"Title": f"Safety signal: {level} {NAMES[level]}", "Priority": "urgent" if level >= 3 else ("high" if level == 2 else "default"),
           "Tags": "rotating_light" if level >= 3 else ("warning" if level == 2 else "eyes")}
    urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/" + topic, data=body.encode("utf-8"), headers=hdr),
                           timeout=20)


def set_level(level, why, who):
    cur = load()
    now = datetime.now().strftime("%Y-%m-%d %I:%M %p")
    json.dump({"level": level, "why": why, "at": now, "by": who}, open(STATE, "w", encoding="utf-8"), indent=1)
    if not os.path.exists(LOG):
        open(LOG, "w", encoding="utf-8").write("# Safety signal history (newest last)\n\n" + __doc__.split("Use:")[0] + "\n")
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"- {now} | {level} {NAMES[level]} | {who} | {why}\n")
    if level != cur.get("level"):
        buzz(level, why)
        print(f"changed {cur.get('level')} -> {level}, buzzed")
    else:
        print(f"still {level} {NAMES[level]} (logged, no buzz)")
    try:  # 11/14: rebuild the PRIVATE signal page (projects/safety-signal-page/; Claude republishes the private artifact)
        import subprocess
        subprocess.Popen([sys.executable, os.path.join(ROOT, "tools", "signal_page.py")],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass


def check_ntas():
    import subprocess  # dhs.gov 403s Python's urllib but serves curl
    xml = subprocess.run(["curl", "-s", "-f", "-m", "30", "https://www.dhs.gov/ntas/1.1/feed.xml"],
                         capture_output=True, text=True, check=True).stdout
    alerts = re.findall(r"<alert\b[^>]*>", xml)
    cur = load()
    if alerts and cur.get("level", 0) < 4:
        set_level(4, "DHS NTAS has an active bulletin/alert: " + alerts[0][:300] + " https://www.dhs.gov/national-terrorism-advisory-system", "ntas-feed")
    else:
        print(f"NTAS alerts: {len(alerts)}; level stays {cur.get('level', 0)}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "set":
        set_level(int(a[1]), a[2], os.environ.get("SIGNAL_BY", "ai"))
    elif a and a[0] == "check":
        check_ntas()
    else:
        c = load(); print(f"{c.get('level',0)} {NAMES[c.get('level',0)]} - {c.get('why','')} ({c.get('at','')})")
