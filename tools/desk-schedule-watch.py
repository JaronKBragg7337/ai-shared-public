"""
desk-schedule-watch.py - phone reminders for the desk schedule. Run every 15 minutes by the Windows task "Desk Schedule Watch".
Reads Control Room `desk_schedule` (via desk_schedule.py), buzzes Jaron's phone through ntfy ONCE per change:
  ON  - "Turn Darios + Satya ON in the Grok app - college football opens at 11 AM"   (sent up to 30 min before a lane opens)
  OFF - "Turn Darios + Satya OFF - nothing open until Fri 11 AM"
Only lanes marked remind:true count. Buzzes during quiet hours wait until they end. Once a day after `evening_report`,
if anything settled today, a second buzz gives settled profit per bot. State: state/desk-schedule-watch.json.
    python desk-schedule-watch.py --dry      print what it would buzz, send nothing, write nothing
"""
import json, os, sys, urllib.request
from datetime import datetime, timedelta, timezone
HERE = os.path.dirname(os.path.realpath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import desk_schedule as DS
STATE = os.path.join(ROOT, "state", "desk-schedule-watch.json")
BOTS = "Darios + Satya"
DRY = "--dry" in sys.argv


def push(title, msg):
    if DRY:
        print(f"[would buzz] {title}: {msg}"); return
    t = [l.split("=", 1)[1].strip() for l in open(os.path.expanduser("~/.secrets/keys.env"), encoding="utf-8-sig") if l.startswith("NTFY_TOPIC=")][0]
    urllib.request.urlopen(urllib.request.Request("https://ntfy.sh/" + t, data=msg.encode(), headers={"Title": title}), timeout=20)


def load_state():
    try: return json.load(open(STATE, encoding="utf-8"))
    except Exception: return {}


def save_state(st):
    if not DRY:
        json.dump(st, open(STATE, "w", encoding="utf-8"))


def remind_lanes(sched):
    return [l for l in sched["lanes"] if l.get("remind")]


def open_lanes(sched, t):
    return [l for l in remind_lanes(sched) if DS.is_open(sched, l, t)[0]]


def on_off_message(sched, now):
    """(state, message): ON if a reminder lane is open now or opens within 30 minutes."""
    soon = open_lanes(sched, now + timedelta(minutes=30))
    cur = open_lanes(sched, now)
    if soon or cur:
        lanes = soon or cur
        opening = [l for l in soon if l not in cur]
        if opening:
            l = opening[0]
            t = DS.next_open(sched, l, now - timedelta(minutes=1))
            when = DS.h12(t) if t else "soon"
            return "ON", f"Turn {BOTS} ON in the Grok app - {l['name']} opens at {when}"
        return "ON", f"Turn {BOTS} ON in the Grok app - {' + '.join(l['name'] for l in lanes)} open now"
    nxts = [(DS.next_open(sched, l, now), l) for l in remind_lanes(sched)]
    nxts = [x for x in nxts if x[0]]
    if not nxts:
        return "OFF", f"Turn {BOTS} OFF in the Grok app - nothing open on the schedule"
    t, l = min(nxts, key=lambda x: x[0])
    return "OFF", f"Turn {BOTS} OFF in the Grok app - nothing open until {DS.when(t, now)}"


def evening(sched, now, st):
    ev = sched.get("evening_report")
    if not ev or now.strftime("%Y-%m-%d") == st.get("report_day") or now.hour * 60 + now.minute < DS._m(ev):
        return
    try:
        import executor as X
        env = X.secrets()
        day0 = now.replace(hour=0, minute=0, second=0, microsecond=0)
        off = datetime.now(timezone.utc).replace(tzinfo=None) - DS.local_now(sched)
        start = (day0 + off).replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        rows = X.sb(env, "GET", f"desk_trades?select=actor,pnl_usd&kind=eq.resolution&actor=like.auto:*&at=gte.{start}")
    except Exception as e:
        print("evening report: could not read results:", str(e)[:100]); return   # try again next run
    st["report_day"] = now.strftime("%Y-%m-%d")
    if not rows:
        return
    per = {}
    for r in rows:
        who = (r.get("actor") or "?").split("/")[-1]
        per[who] = per.get(who, 0.0) + float(r.get("pnl_usd") or 0)
    tot = sum(per.values())
    body = ", ".join(f"{k} {'+' if v >= 0 else '-'}${abs(v):.2f}" for k, v in sorted(per.items(), key=lambda kv: -kv[1]))
    push("Desk results today", f"Settled today: {body}. Total {'+' if tot >= 0 else '-'}${abs(tot):.2f} ({len(rows)} bets).")


def main():
    sched = DS.load()
    if not sched:
        return
    now = DS.local_now(sched)
    st = load_state()
    state, msg = on_off_message(sched, now)
    q = sched.get("quiet")
    quiet = bool(q) and DS._in_span(q["from"], q["to"], now.weekday(), now.hour * 60 + now.minute)
    if state != st.get("state") and not quiet:
        push(f"Grok bots {state}", msg)
        st["state"] = state
    elif DRY:
        print(f"[no buzz] now {state} (announced {st.get('state')}, quiet={quiet}): {msg}")
    evening(sched, now, st)
    save_state(st)


if __name__ == "__main__":
    main()
