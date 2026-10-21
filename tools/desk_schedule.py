"""
desk_schedule.py - the trading desk's weekly schedule, read from the Control Room (system_settings key `desk_schedule`).

One JSON setting says which kind of game may get NEW positions, when, and at what size cap. desk-trade.py enforces it;
`desk.py rules` prints it in plain words; desk-schedule-watch.py buzzes Jaron's phone when it is time to switch bots on/off.
Nothing about this lives in any bot's instructions. If the setting can't be read or parsed, load() returns None and the
callers do NOT block (a network blip never freezes the desk).

Shape (times are local to "tz"; a window whose `to` is not after its `from` runs past midnight into the next day, and its
`days` name the day it STARTS; "24:00" is midnight):
  {"tz": "America/Indiana/Indianapolis",
   "global_closed": {"from": "02:00", "to": "11:00"},          # no new positions then, for every lane
   "quiet": {"from": "00:00", "to": "07:00"},                  # phone buzzes wait until after this
   "evening_report": "21:00",
   "lanes": [{"name": "college football", "sports": ["cfb"], "remind": true,
              "windows": [{"days": ["fri","sat"], "from": "11:00", "to": "02:00", "cap_usd": null}]}, ...]}
A lane's sports are the second word of a Polymarket US slug (aec-cfb-..., astatc-nfl-..., cpc-btc-...). Any slug whose
sport is in no lane is OFF. A window's cap_usd of null/missing = normal size (the other Control Room caps still apply).
"""
import json
import os
import sys
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

KEY = "desk_schedule"
DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
DAYNAMES = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def load():
    """The schedule dict from the Control Room, or None if unreadable/unset/invalid (callers then don't block)."""
    try:
        from settings import setting
        v = setting(KEY, "")
        if isinstance(v, str):
            v = json.loads(v) if v.strip() else None
        if isinstance(v, dict) and isinstance(v.get("lanes"), list):
            return v
    except Exception:
        pass
    return None


# ---- time -----------------------------------------------------------------------------------------------------------
def _us_eastern_offset(utc):
    """Indianapolis follows US Eastern daylight rules (since 2006). Used when the python has no tz database (the venv)."""
    y = utc.year
    d = datetime(y, 3, 8)                      # second Sunday of March, 2:00 local standard = 07:00 UTC
    start = (d + timedelta(days=(6 - d.weekday()) % 7)).replace(hour=7)
    d = datetime(y, 11, 1)                     # first Sunday of November, 2:00 local daylight = 06:00 UTC
    end = (d + timedelta(days=(6 - d.weekday()) % 7)).replace(hour=6)
    naive = utc.replace(tzinfo=None)
    return timedelta(hours=-4) if start <= naive < end else timedelta(hours=-5)


def local_now(sched=None, utc=None):
    """Naive datetime in the schedule's timezone (default Indianapolis)."""
    utc = utc or datetime.now(timezone.utc)
    tz = (sched or {}).get("tz") or "America/Indiana/Indianapolis"
    try:
        from zoneinfo import ZoneInfo
        return utc.astimezone(ZoneInfo(tz)).replace(tzinfo=None)
    except Exception:
        return (utc + _us_eastern_offset(utc)).replace(tzinfo=None)


def _m(hhmm):
    h, mi = str(hhmm).split(":")
    return int(h) * 60 + int(mi)


def _in_span(frm, to, wd, minute, days=None):
    """Is (weekday wd, minute-of-day) inside a span starting on one of `days` (all days if None)?"""
    f, t = _m(frm), _m(to)
    ok = lambda d: days is None or DAYS[d] in days
    if t > f:
        return ok(wd) and f <= minute < t
    return (ok(wd) and minute >= f) or (ok((wd - 1) % 7) and minute < t)


# ---- lanes ----------------------------------------------------------------------------------------------------------
def sport_of(slug):
    s = (slug or "").lower()
    if "-btc-" in s or "bitcoin" in s:
        return "btc"
    p = s.split("-")
    return p[1] if len(p) > 1 else ""


def lane_for(sched, slug):
    sp = sport_of(slug)
    for ln in sched["lanes"]:
        if sp in [x.lower() for x in ln.get("sports", [])]:
            return ln
    return None


def is_open(sched, lane, local):
    """(open?, cap_usd or None) for this lane at this local time."""
    # Weekly review leaves a benched lane's normal windows intact for recovery, but only
    # opens them during an explicit $1 re-test or to maintain the minimum lane floor.
    if lane.get("benched") and not lane.get("bench_open", False):
        return False, None
    wd, minute = local.weekday(), local.hour * 60 + local.minute
    g = sched.get("global_closed")
    if g and _in_span(g["from"], g["to"], wd, minute):
        return False, None
    best = None
    hit = False
    for w in lane.get("windows", []):
        if _in_span(w["from"], w["to"], wd, minute, [d.lower() for d in w.get("days", DAYS)]):
            hit = True
            c = w.get("cap_usd")
            if c is not None and (best is None or float(c) < best):
                best = float(c)
    return hit, best


def next_open(sched, lane, local, horizon_days=8):
    """Local datetime (15-minute steps) when this lane next opens, or None."""
    t = local.replace(second=0, microsecond=0)
    t -= timedelta(minutes=t.minute % 15)
    if is_open(sched, lane, t)[0]:       # already open: find when it closes first, then the next open
        for _ in range(horizon_days * 96):
            t += timedelta(minutes=15)
            if not is_open(sched, lane, t)[0]:
                break
    for _ in range(horizon_days * 96):
        t += timedelta(minutes=15)
        if is_open(sched, lane, t)[0]:
            return t
    return None


def next_close(sched, lane, local, horizon_days=8):
    t = local.replace(second=0, microsecond=0)
    t -= timedelta(minutes=t.minute % 15)
    for _ in range(horizon_days * 96):
        t += timedelta(minutes=15)
        if not is_open(sched, lane, t)[0]:
            return t
    return None


# ---- words ----------------------------------------------------------------------------------------------------------
def h(hhmm):
    x = _m(hhmm)
    if x in (0, 1440):
        return "midnight"
    hr, mi = x // 60, x % 60
    return f"{(hr % 12) or 12}{'' if mi == 0 else f':{mi:02d}'} {'AM' if hr < 12 else 'PM'}"


def h12(dt):
    s = dt.strftime("%I:%M %p").lstrip("0").replace(":00", "")
    return s


def when(dt, now):
    if dt.date() == now.date():
        return f"today {h12(dt)}"
    if dt.date() == (now + timedelta(days=1)).date():
        return f"tomorrow {h12(dt)}"
    return f"{DAYNAMES[dt.weekday()]} {h12(dt)}"


def _daystr(days):
    idx = sorted(DAYS.index(d.lower()) for d in days)
    if len(idx) == 7:
        return "every day"
    if len(idx) > 2 and idx == list(range(idx[0], idx[0] + len(idx))):
        return f"{DAYNAMES[idx[0]]}-{DAYNAMES[idx[-1]]}"
    return "/".join(DAYNAMES[i] for i in idx)


def describe_windows(lane):
    parts = []
    for w in lane.get("windows", []):
        c = w.get("cap_usd")
        span = "all hours" if (_m(w["from"]), _m(w["to"])) == (0, 1440) else f"{h(w['from'])}-{h(w['to'])}"
        parts.append(f"{_daystr(w.get('days', DAYS))} {span}" + (f" ${c:g} cap" if c is not None else ""))
    return "; ".join(parts) or "never"


def refusal(sched, slug, now_local):
    """None if a NEW position in this slug is allowed right now, else ONE plain line for the bot."""
    lane = lane_for(sched, slug)
    if lane is None:
        sp = sport_of(slug) or "this market"
        return f"refused: {sp} is not on the desk schedule, so it is off (open lanes: `python tools/desk.py rules`)."
    ok, _ = is_open(sched, lane, now_local)
    if ok:
        return None
    nxt = next_open(sched, lane, now_local)
    g = sched.get("global_closed")
    why = (f"no new positions {h(g['from'])}-{h(g['to'])}" if g and _in_span(g["from"], g["to"], now_local.weekday(), now_local.hour * 60 + now_local.minute)
           else f"{lane['name']} is closed {DAYNAMES[now_local.weekday()]} {h12(now_local)}")
    return (f"refused: {why} (open {describe_windows(lane)}). "
            + (f"Next open: {DAYNAMES[nxt.weekday()]} {h12(nxt)}." if nxt else "No open time on the schedule."))


def lane_cap(sched, slug, now_local):
    """Dollar cap from the lane's current window, or None."""
    lane = lane_for(sched, slug)
    return is_open(sched, lane, now_local)[1] if lane else None


def rules_text(sched, now_local):
    lines = [f"DESK RULES - {DAYNAMES[now_local.weekday()]} {now_local:%Y-%m-%d} {h12(now_local)} Indianapolis time (from the Control Room; new positions only - exits are always allowed)"]
    g = sched.get("global_closed")
    if g:
        lines.append(f"No new positions {h(g['from'])}-{h(g['to'])}, any market.")
    rows = []
    for ln in sched["lanes"]:
        ok, cap = is_open(sched, ln, now_local)
        label = "OPEN" if ok else "closed"
        size = "" if not ok else (f", cap ${cap:g}" if cap is not None else ", normal size")
        bit = f"  {ln['name']:18} {label}{size}"
        if ok:
            c = next_close(sched, ln, now_local)
            bit += f" - closes {when(c, now_local)}" if c else ""
        else:
            n = next_open(sched, ln, now_local)
            bit += f" - opens {when(n, now_local)}" if n else ""
        rows.append((bit, ln))
    lines += [r[0] for r in rows]
    lines.append("Weekly hours:")
    for ln in sched["lanes"]:
        lines.append(f"  {ln['name']}: {describe_windows(ln)}")
    lines.append("Anything not listed is off. Other caps (BTC, long shots) still apply. A refusal says why: move on.")
    # next change anywhere
    best = None
    for ln in sched["lanes"]:
        ok, _ = is_open(sched, ln, now_local)
        t = next_close(sched, ln, now_local) if ok else next_open(sched, ln, now_local)
        if t and (best is None or t < best[0]):
            best = (t, ln, ok)
    if best:
        lines.append(f"Next change: {best[1]['name']} {'closes' if best[2] else 'opens'} {when(best[0], now_local)}.")
    return "\n".join(lines)
