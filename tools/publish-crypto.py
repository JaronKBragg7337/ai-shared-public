#!/usr/bin/env python3
"""
publish-crypto.py - the crypto up/down lane, in the open, at heartbeatobservatory.com/live-systems/crypto/ (Jaron 2026-10-23).

Writes one row (id = 'crypto') to the same public table the crew page uses (Supabase public.crew_snapshot, public read,
select-only; the service key stays here on the MSI). No AI, no cost. Run by publish-crew.py every 5 minutes (task "Crew Publish"),
or by hand:  python tools/publish-crypto.py   (CRYPTO_DRY=1 prints a summary and writes nothing)

Reads, all local files and public-by-design tables:
  state/twin-crypto-paper.jsonl   every bot's call (by, lens, side, price, size, why) and its paper result
  state/crypto-consensus.jsonl    every crew decision (who called what, traded or passed, why)
  state/crypto-correlation.json   24 h coin correlation
  Supabase desk_trades            the lane's live fills and resolutions (slug contains -updown-)
  Supabase desk_account           open positions (value)
  Control Room rows               crypto_lane_start, crypto_phase1_loss_usd, crypto_phase2_loss_usd, crypto_stop_account_usd, ...

Privacy: Jaron's own hand trades (actor jaron-*, and anything before the lane start) are never published. Only the lane's
own fills (actor auto:*) are. Every string passes the same mask as the crew page.
"""
import json, os, re, sys
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import executor as X  # noqa: E402

PAPER = os.path.join(ROOT, "state", "twin-crypto-paper.jsonl")
DECISIONS = os.path.join(ROOT, "state", "crypto-consensus.jsonl")
CORR = os.path.join(ROOT, "state", "crypto-correlation.json")
LENS_DEFAULT = {"darios-twin": "momentum", "satya-twin": "fair price", "jarons-twin": "contrarian check"}
LENS_TEXT = {
    "momentum": "Rides the move since the window opened: price vs the open, the last 5 and 15 minutes.",
    "fair price": "Trades where the market price is off the board's fair odds; if they agree it still has to pick a side on hourly and daily.",
    "contrarian": "Looks for the reason the obvious side is wrong: crowd lean (futures funding), order-book walls, open interest.",
    "contrarian check": "Looks for the reason the obvious side is wrong: crowd lean (futures funding), order-book walls, open interest.",
}
EMPTY_BOOK = re.compile(r"empty|no book|no ask|no bid|no price|no quote|book (?:went|was|is) (?:empty|blank)|unpriced", re.I)
TF_NAME = {"15m": "15 minutes", "1h": "1 hour", "1d": "1 day"}


def jsonl(path):
    out = []
    try:
        for l in open(path, encoding="utf-8"):
            l = l.strip()
            if l:
                try:
                    out.append(json.loads(l))
                except ValueError:
                    pass
    except OSError:
        pass
    return out


def by_of(r):
    return r.get("by") or "jarons-twin"        # rows with no "by" are Jarons Twin's (the log began with it)


def name_of(bid):
    return " ".join(p.capitalize() for p in bid.split("-") if p)


def setting(key, default):
    try:
        from settings import setting as s
        v = s(key, default)
        return v if v is not None else default
    except Exception:
        return default


def lane_actor(a):
    """The lane's own orders only: auto:* actors. Jaron's hand trades (jaron-manual) never go public."""
    return bool(a) and a.startswith("auto:")


def paper_summary(calls):
    """Per bot: calls / passes / empty-book passes / paper record, in total and split by window type. Paper money, not real."""
    bots = {}
    for r in calls:
        b = by_of(r)
        if r.get("excluded"):      # 10/23 honest paper: calls on an empty book are never counted
            bots.setdefault(b, {"id": b, "name": name_of(b), "lens": "", "last_call": "", "calls": 0, "passes": 0, "empty_book": 0,
                                "open": 0, "won": 0, "settled": 0, "pnl": 0.0, "by_tf": {}})["empty_book"] += 1
            continue
        d = bots.setdefault(b, {"id": b, "name": name_of(b), "lens": "", "last_call": "", "calls": 0, "passes": 0, "empty_book": 0,
                                "open": 0, "won": 0, "settled": 0, "pnl": 0.0, "by_tf": {}})
        d["lens"] = r.get("lens") or d["lens"] or LENS_DEFAULT.get(b, "")
        d["last_call"] = max(d["last_call"], r.get("at") or "")
        tf = d["by_tf"].setdefault(r.get("tf") or "?", {"calls": 0, "passes": 0, "empty_book": 0, "open": 0, "won": 0, "settled": 0, "pnl": 0.0})
        if r.get("side") == "pass":
            for t in (d, tf):
                t["passes"] += 1
                if EMPTY_BOOK.search(r.get("why") or ""):
                    t["empty_book"] += 1
            continue
        for t in (d, tf):
            t["calls"] += 1
            if "result" in r:
                t["settled"] += 1
                t["won"] += r["result"] == "win"
                t["pnl"] = round(t["pnl"] + float(r.get("pnl") or 0), 2)
            else:
                t["open"] += 1
    for d in bots.values():
        d["pnl"] = round(d["pnl"], 2)
        d["lens_text"] = LENS_TEXT.get(d["lens"], "")
    return bots


def lane_fills(env, start):
    rows = X.sb_all(env, "desk_trades?select=id,kind,at,slug,side,price,cost_usd,pnl_usd,actor&slug=like.*-updown-*&at=gte." + start)
    return [r for r in rows if lane_actor(r.get("actor"))]


def window_end(slug):
    m = re.search(r"-updown-(15m|1h|1d)-(\d{4})-(\d\d)-(\d\d)-(\d{2})(\d{2})z$", slug or "")
    if not m:
        return None, None
    tf = m.group(1)
    start = datetime(int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5)), int(m.group(6)), tzinfo=timezone.utc)
    return tf, start + {"15m": timedelta(minutes=15), "1h": timedelta(hours=1), "1d": timedelta(days=1)}[tf]


def coin_of(slug):
    m = re.search(r"-(btc|eth|sol|xrp)-updown-", slug or "")
    return m.group(1) if m else "?"


def build():
    env = X.secrets()
    now = datetime.now(timezone.utc)
    start = str(setting("crypto_lane_start", "2026-10-22")).strip()
    start_day = start[:10]
    if len(start) <= 10: start += "T00:00:00Z"
    calls = jsonl(PAPER)
    decisions = jsonl(DECISIONS)
    fills = lane_fills(env, start)

    # ---- trades: one line per window the lane traded
    dec_by_slug = {}
    for d in decisions:
        if d.get("outcome") == "traded":
            dec_by_slug.setdefault(d["slug"], d)
    call_why = {}
    for r in calls:
        call_why[(r["slug"], by_of(r))] = r
    by_slug = {}
    for f in fills:
        s = by_slug.setdefault(f["slug"], {"slug": f["slug"], "cost": 0.0, "first": f["at"], "fills": 0, "pnl": None, "result_at": "", "side": ""})
        if f["kind"] == "fill":
            s["cost"] += float(f.get("cost_usd") or 0)
            s["fills"] += 1
            s["first"] = min(s["first"], f["at"])
            s["side"] = s["side"] or f.get("side") or ""
        elif f["kind"] == "resolution":
            s["pnl"] = (s["pnl"] or 0.0) + float(f.get("pnl_usd") or 0)
            s["result_at"] = max(s["result_at"], f["at"])
    trades = []
    for slug, s in by_slug.items():
        if not s["fills"]: continue      # resolution of a position bought before the lane start = old lane
        tf, end = window_end(slug)
        dec = dec_by_slug.get(slug) or {}
        called = {}
        for bot, sd in (dec.get("calls") or {}).items():
            r = call_why.get((slug, bot)) or {}
            called[bot] = {"side": sd[0], "size": sd[1], "why": (r.get("why") or "")[:220]}
        side = dec.get("side") or ("down" if s["side"] == "no" else "up" if s["side"] == "yes" else "")
        if s["pnl"] is not None:
            status = "won" if s["pnl"] > 0 else "lost" if s["pnl"] < 0 else "even"
        elif end and end > now:
            status = "open"
        else:
            status = "settling"
        trades.append({"at": s["first"], "coin": coin_of(slug), "tf": tf, "slug": slug, "side": side, "cost": round(s["cost"], 2),
                       "status": status, "pnl": None if s["pnl"] is None else round(s["pnl"], 2), "ends": end.isoformat() if end else "",
                       "reason": dec.get("reason") or "", "calls": called,
                       # real money per trade, from the ledger via crypto_decide.reconcile_fills
                       "fill_price": (dec.get("fill") or {}).get("price"), "shares": (dec.get("fill") or {}).get("shares"),
                       "fees": (dec.get("fill") or {}).get("fees"), "exit": dec.get("exit"), "hold_pnl": dec.get("hold_pnl")})
        if dec.get("final_pnl") is not None and trades[-1]["pnl"] is None: trades[-1]["pnl"] = round(dec["final_pnl"], 2)
        if trades[-1]["pnl"] is not None:
            p_ = trades[-1]["pnl"]; trades[-1]["status"] = "won" if p_ > 0 else "lost" if p_ < 0 else "even"
    trades.sort(key=lambda t: t["at"], reverse=True)

    settled = [t for t in trades if t["pnl"] is not None]
    pnl = round(sum(t["pnl"] for t in settled), 2)

    # ---- open positions (value from the live account read)
    acct = (X.sb(env, "GET", "desk_account?select=balance_usd,buying_power,positions,updated_at&id=eq.polymarket-us") or [{}])[0]
    open_value, open_n = 0.0, 0
    for p in acct.get("positions") or []:
        if "-updown-" in (p.get("slug") or ""):
            open_value += float(p.get("value") or 0)
            open_n += 1
    total_positions = sum(float(p.get("value") or 0) for p in acct.get("positions") or [])
    cash = float(acct.get("balance_usd") or 0)
    open_cost = round(sum(t["cost"] for t in trades if t["status"] in ("open", "settling")), 2)

    # ---- phase status (same numbers crypto_decide.py uses)
    p1, p2 = float(setting("crypto_phase1_loss_usd", 999)), float(setting("crypto_phase2_loss_usd", 10))
    stop_acct = float(setting("crypto_stop_account_usd", 30))
    acct_value = round(cash + total_positions, 2)
    if acct_value <= stop_acct:
        mode, note = "stopped", f"Account is at ${acct_value:.2f}, at or under the ${stop_acct:g} floor: the crypto lane places nothing."
    elif pnl - open_cost <= -p2:
        mode, note = "stopped", f"Worst case is down ${-(pnl - open_cost):.2f} (settled {pnl:+.2f}, ${open_cost:.2f} still open; limit ${p2:g}): stopped to talk it over."
    elif pnl - open_cost <= -p1:
        mode, note = "phase 2", f"Crypto is down ${-pnl:.2f} (past ${p1:g}): Jarons Twin trades alone until it reaches ${p2:g} down."
    else:
        mode, note = "phase 1", f"Crew consensus trades. Crypto is {'+' if pnl >= 0 else '-'}${abs(pnl):.2f}; phase 2 starts at ${p1:g} down."

    # ---- decisions
    last_dec = [{"at": d.get("at"), "coin": d.get("coin"), "tf": d.get("tf"), "outcome": d.get("outcome"), "mode": d.get("mode"),
                 "note": (d.get("note") or d.get("reason") or "")[:200], "side": d.get("side") or ""}
                for d in decisions if d.get("outcome") == "traded" or ("no agreement" in (d.get("note") or "") or "disagree" in (d.get("note") or "")) or "tie" in (d.get("note") or "")][-30:][::-1]
    n_traded = sum(d.get("outcome") == "traded" for d in decisions)

    summary = paper_summary(calls)
    # newest calls per bot, for the "latest calls" list
    latest = [{"at": r["at"], "by": by_of(r), "coin": r.get("coin"), "tf": r.get("tf"), "side": r.get("side"), "price": r.get("price"),
               "size": r.get("size"), "result": r.get("result"), "pnl": r.get("pnl"), "why": (r.get("why") or "")[:200],
               "empty_book": bool(r.get("side") == "pass" and EMPTY_BOOK.search(r.get("why") or ""))}
              for r in sorted(calls, key=lambda r: r["at"], reverse=True)[:40]]

    try:
        corr = json.load(open(CORR, encoding="utf-8"))
    except Exception:
        corr = {}
    caps = setting("crypto_bot_caps", {})
    if isinstance(caps, str):
        try:
            caps = json.loads(caps)
        except ValueError:
            caps = {}
    max_open = float(setting("crypto_max_open_usd", 25))
    decouple = float(setting("crypto_decouple_corr", 0.5))
    return {
        "updated": now.isoformat(timespec="seconds"),
        "since": start_day,
        "money": {"settled_pnl": pnl, "settled_n": len(settled), "wins": sum(t["pnl"] > 0 for t in settled), "losses": sum(t["pnl"] < 0 for t in settled),
                  "open_value": round(open_value, 2), "open_n": open_n, "open_cost": open_cost,
                  "account_value": acct_value, "cash": round(cash, 2)},
        "phase": {"mode": mode, "note": note, "phase1_loss": p1, "phase2_loss": p2, "stop_account": stop_acct},
        "limits": {"max_open": max_open, "decouple_corr": decouple, "caps": caps},
        "trades": trades[:60],
        "bots": sorted(summary.values(), key=lambda b: b["id"]),
        "latest_calls": latest,
        "decisions": {"last_at": max([d.get("at") or "" for d in decisions if d.get("mode") == "LIVE"] or [""]),
                      "total": len(decisions), "traded": n_traded, "passed": len(decisions) - n_traded, "recent": last_dec},
        "correlation": {"at": corr.get("at"), "hours": corr.get("window_hours"), "pairs": corr.get("pairs") or {},
                        "max_with_others": corr.get("max_with_others") or {}},
        "rules": rules_text(max_open, decouple, caps, p1, p2, stop_acct),
    }


def rules_text(max_open, decouple, caps, p1, p2, stop_acct):
    cap = max(caps.values()) if caps else 3
    return [
        "Three bots look at the same coins (Bitcoin, Ethereum, Solana, XRP), each through its own lens. They only make calls, UP or DOWN. A script, not the bots, places the trade.",
        "15-minute windows are a free ball: the first bot to call a side takes it and the trade goes in within a minute. No agreement needed, and a bot may pass.",
        "Hourly and daily windows get a live trade on every coin, every window. No passing. The crew majority picks the side: 2 or 3 agree and that side wins, at the average of their sizes. If only 1 vs 1, the bot with the better settled record on that window type decides, at half size.",
        f"Each bot's size is capped at ${cap:g} per call (the cap moves $1 up after a winning week and $1 down after a losing one).",
        f"No more than ${max_open:g} at risk across crypto at once. A coin that moves on its own (24 h correlation under {decouple:g} with every other coin) counts alone, with its own ${max_open:g}.",
        "Freshness: a call older than 5 minutes on a 15-minute window, or 10 minutes on an hourly one, counts as a pass. One live position per window, ever.",
        "Price guard: the trade script checks the book, the spread and the size before it places anything, and refuses a bad price.",
        f"Phase 1 is the crew consensus. If crypto alone is down ${p1:g}, phase 2 starts: Jarons Twin trades alone. If crypto alone is down ${p2:g}, everything stops. Game wins or losses never count here.",
        f"A separate floor stops crypto only if the whole account falls to ${stop_acct:g}. These numbers live in the Control Room and change without a rebuild.",
        "Sports are Saturday only. Crypto runs every day, all hours.",
    ]


def mask_all(obj, mask):
    if isinstance(obj, str):
        return mask(obj)
    if isinstance(obj, list):
        return [mask_all(v, mask) for v in obj]
    if isinstance(obj, dict):
        return {k: mask_all(v, mask) for k, v in obj.items()}
    return obj


def main(mask=None):
    data = build()
    if mask is None:
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("publish_crew_mask", os.path.join(HERE, "publish-crew.py"))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mask = mod.mask
        except Exception:
            mask = lambda s: s  # noqa: E731
    data = mask_all(data, mask)
    if os.environ.get("CRYPTO_DRY"):
        m = data["money"]
        print("settled", m["settled_pnl"], "n", m["settled_n"], "open value", m["open_value"], "open n", m["open_n"], "phase", data["phase"]["mode"])
        print("trades", len(data["trades"]), "bots", [(b["id"], b["calls"], b["passes"], b["empty_book"], b["won"], b["settled"], b["pnl"]) for b in data["bots"]])
        print("decisions", data["decisions"]["total"], data["decisions"]["traded"], "latest", len(data["latest_calls"]))
        return data
    env = X.secrets()
    import urllib.request
    key = env["SUPABASE_SERVICE_ROLE_KEY"]
    body = [{"id": "crypto", "data": data, "updated_at": data["updated"]}]
    req = urllib.request.Request(env["SUPABASE_URL"].rstrip("/") + "/rest/v1/crew_snapshot?on_conflict=id",
                                 data=json.dumps(body).replace(chr(92) + "u0000", "").encode(), method="POST",
                                 headers={"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json",
                                          "Prefer": "resolution=merge-duplicates,return=minimal"})
    urllib.request.urlopen(req, timeout=45).read()
    print("crypto published", len(json.dumps(data)), "bytes,", len(data["trades"]), "trades,", len(data["bots"]), "bots")
    return data


if __name__ == "__main__":
    main()
