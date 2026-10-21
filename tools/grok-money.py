# What Grok Bot's trader earns per day / week / month, next to how active it was (Jaron 9/28: "how much is made a week and
# month while it has usage, then how many days it goes without" -> is a bigger Grok subscription worth it?).
#   money:    desk_trades rows tagged auto:grok-bot/live-wire (Live Wire v1 until 9/25 22:58Z, Darios Twin after)
#   activity: lines per day in state/live-wire.md (one per routine pass/trade) - a day with none = the pool ran dry or it was off
#   usage:    Jaron's own readings of the Grok usage meter, appended to state/grok-usage.md ("date | % used | resets in")
# Prints a table and writes state/grok-money.md.  Days are Fort Wayne (Eastern) days.
import os, re, sys, collections
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import executor as X  # noqa: E402
import trade_pnl as P  # noqa: E402

ET = timezone(timedelta(hours=-4))          # EDT; fine until Nov 1
CUT = "2026-09-25T22:58:00Z"


def day_of(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(ET).date()


rows = X.sb_all(X.secrets(), "desk_trades?select=actor,kind,action,cost_usd,pnl_usd,at,slug,side,quantity&actor=like.auto:grok-bot*")
market_stats = P.market_pnl(rows)
D = collections.defaultdict(lambda: {"fills": 0, "spent": 0.0, "settled": 0, "pnl": 0.0, "active": 0})
for r in rows:
    d = D[day_of(r["at"])]
    if r["kind"] == "fill":
        d["fills"] += 1; d["spent"] += abs(float(r.get("cost_usd") or 0))
    elif r["kind"] == "resolution":
        d["settled"] += 1
for m in market_stats.values():
    for day, value in m["sales_by_day"].items():
        D[datetime.fromisoformat(day).date()]["pnl"] += value
    for day, value in m["settlement_by_day"].items():
        D[datetime.fromisoformat(day).date()]["pnl"] += value
for line in open(os.path.join(ROOT, "state", "live-wire.md"), encoding="utf-8-sig"):
    m = re.match(r"(\d{4}-\d{2}-\d{2})[ T](\d{2}):(\d{2})", line)
    if m:
        dt = datetime.fromisoformat(f"{m[1]}T{m[2]}:{m[3]}:00+00:00").astimezone(ET).date()
        D[dt]["active"] += 1

usage = {}
up = os.path.join(ROOT, "state", "grok-usage.md")
if os.path.exists(up):
    for line in open(up, encoding="utf-8"):
        m = re.match(r"(\d{4}-\d{2}-\d{2}).*?\|\s*(\d+)%", line)
        if m:
            usage[m[1]] = m[2] + "%"

days = sorted(D)
first, last = days[0], max(days[-1], datetime.now(ET).date())
out = ["# Grok Bot trader: money vs activity (made by tools/grok-money.py - rerun any time)", "",
       "Profit = realized sell proceeds minus average cost of shares sold, plus P&L on shares held through settlement.",
       "Log lines = routine passes + trades written that day; usage = Jaron's reading of the meter.",
       "0 means Grok Bot did nothing that day (usage ran out, or it was switched off). Usage = Jaron's reading of the meter.", "",
       "| day | log lines | fills | traded (buys+sells) | settled | profit | usage |", "|---|---|---|---|---|---|---|"]
d = first
wk = collections.defaultdict(lambda: [0.0, 0, 0]); mo = collections.defaultdict(lambda: [0.0, 0, 0])
while d <= last:
    x = D.get(d, {"fills": 0, "spent": 0.0, "settled": 0, "pnl": 0.0, "active": 0})
    out.append(f"| {d:%a %m-%d} | {x['active']} | {x['fills']} | ${x['spent']:.2f} | {x['settled']} | {'+' if x['pnl'] >= 0 else '-'}${abs(x['pnl']):.2f} | {usage.get(str(d), '')} |")
    k = d - timedelta(days=d.weekday())
    for b, key in ((wk, k), (mo, d.strftime("%Y-%m"))):
        b[key][0] += x["pnl"]; b[key][1] += 1 if x["active"] or x["fills"] else 0; b[key][2] += 1
    d += timedelta(days=1)
fmt = lambda v: f"{'+' if v >= 0 else '-'}${abs(v):.2f}"
out += ["", "| week of (Mon) | settled profit | active days / days | profit per active day |", "|---|---|---|---|"]
for k in sorted(wk):
    p, a, n = wk[k]
    out.append(f"| {k:%m-%d} | {fmt(p)} | {a} / {n} | {fmt(p / a) if a else '-'} |")
out += ["", "| month | settled profit | active days / days | profit per active day |", "|---|---|---|---|"]
for k in sorted(mo):
    p, a, n = mo[k]
    out.append(f"| {k} | {fmt(p)} | {a} / {n} | {fmt(p / a) if a else '-'} |")
# the two systems separately (Jaron 9/28: the old Live Wire barely traded under rules other AIs added; the money is the new
# Darios Twin system, started at the 9/25 handover - judge Grok by that era, not the 17-day total)
era = {"Live Wire (v1, until 9/25 22:58Z)": [0.0, 0, 0, set()], "Darios Twin (since 9/25 22:58Z)": [0.0, 0, 0, set()]}
for label, before_cut in (("Live Wire (v1, until 9/25 22:58Z)", True), ("Darios Twin (since 9/25 22:58Z)", False)):
    subset = [r for r in rows if (r["at"] < CUT.replace("Z", "")) == before_cut]
    sm = P.market_pnl(subset)
    e = era[label]
    e[0] = sum(m["realized_sales"] + m["settlement"] for m in sm.values())
    e[1] = sum(r["kind"] == "fill" for r in subset)
    e[2] = sum(r["kind"] == "resolution" for r in subset)
    e[3] = {day_of(r["at"]) for r in subset if r["kind"] == "fill"}
out += ["", "| system | settled profit | fills | settled trades | days it traded | profit per trading day |", "|---|---|---|---|---|---|"]
for k, (p, f, n, ds) in era.items():
    out.append(f"| {k} | {fmt(p)} | {f} | {n} | {len(ds)} | {fmt(p / len(ds)) if ds else '-'} |")
# by sport, new system only (9/29: weekday tennis was where the losses came from; football carried the weekends)
sp = collections.defaultdict(lambda: [0, 0, 0.0])
new_rows = [r for r in rows if r["at"] >= CUT.replace("Z", "")]
new_stats = P.market_pnl(new_rows)
for r in new_rows:
    if r["kind"] != "resolution": continue
    sl = r.get("slug") or ""
    k = "tennis" if ("-atp-" in sl or "-wta-" in sl) else (sl.split("-")[1] if "-" in sl else "?")
    sp[k][0] += 1
for sl, m in new_stats.items():
    k = "tennis" if ("-atp-" in sl or "-wta-" in sl) else (sl.split("-")[1] if "-" in sl else "?")
    sp[k][2] += m["realized_sales"] + m["settlement"]
    sp[k][1] += m["realized_sales"] + m["settlement"] > 0
out += ["", "| Darios Twin by sport | settled trades | won | profit |", "|---|---|---|---|"]
for k, (n, w_, v) in sorted(sp.items(), key=lambda x: -x[1][2]):
    out.append(f"| {k} | {n} | {w_} | {fmt(v)} |")
tp = sum(m["realized_sales"] + m["settlement"] for m in market_stats.values())
ta = sum(1 for x in D.values() if x["active"] or x["fills"])
money = P.account_money()
out += ["", f"All time since {first}: realized + settlement P&L {fmt(tp)} over {ta} active days ({fmt(tp / ta) if ta else '-'} per active day)."]
if money:
    out.append(f"Money: profit {fmt(tp)}; open value ${money['open_value']:.2f}; cash ${money['cash']:.2f} (shared account snapshot {money['updated_at']}).")
else:
    out.append(f"Money: profit {fmt(tp)}; open value and cash unavailable (no saved account snapshot).")
out.append("Open value and cash are whole-account figures; profit above is actor-filtered to auto:grok-bot/live-wire.")
open(os.path.join(ROOT, "state", "grok-money.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print("\n".join(out))
