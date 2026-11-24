"""Crypto up/down PAPER trades for the three twins (Jaron 10/22; crew lane approved 10/22 6:30 PM). No money moves here -
this only writes a log. Every hourly and daily window gets a call from each bot on every coin; "pass" is allowed (logged,
not scored). 15-minute windows are optional. One call per bot per window. The live crew trade is made by crypto_decide.py.

    python tools/crypto_paper.py call <slug> up|down|pass --by darios-twin|satya-twin|jarons-twin --price 0.55 --size 3 --why "..."
    python tools/crypto_paper.py exit <slug> --by BOT --why "..." [--pct 100]   sell an open position before the close (your call)
    python tools/crypto_paper.py due [--by BOT]   hourly/daily windows open right now that BOT has not called yet
    python tools/crypto_paper.py settle           score finished windows (Kraken price at end vs start), rewrite the summary
Rows with no "by" are Jarons Twin's (the log began with it). Each row also has a "lens" (momentum / fair price / contrarian).
Log: state/twin-crypto-paper.jsonl (one line per call). Summary: state/twin-crypto-paper.md. Task "Twin Crypto Settle" runs
settle every 15 min. Kraken stands in for CF Benchmarks (what Polymarket settles on), so a hair-close finish can differ."""
import argparse, json, os, sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import crypto_view as CV  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
LOG = os.path.join(ROOT, "state", "twin-crypto-paper.jsonl")
SUMMARY = os.path.join(ROOT, "state", "twin-crypto-paper.md")
BOTS = ("darios-twin", "satya-twin", "jarons-twin")
LENS = {"darios-twin": "momentum", "satya-twin": "fair price", "jarons-twin": "contrarian"}
PAIR = {"btc": "XBTUSD", "eth": "ETHUSD", "sol": "SOLUSD", "xrp": "XRPUSD"}


def coin_of(slug):
    return next(c for c in PAIR if f"-{c}-updown-" in slug or slug.startswith(f"cpc-{c}-"))


def rows():
    return [json.loads(l) for l in open(LOG, encoding="utf-8")] if os.path.exists(LOG) else []


def save(all_rows):
    with open(LOG, "w", encoding="utf-8") as f:
        for r in all_rows: f.write(json.dumps(r) + "\n")


def by_of(r):
    return r.get("by") or "jarons-twin"


def cmd_call(a):
    w = CV.window(a.slug)
    if not w: sys.exit("not an up/down slug")
    tf, start, end = w
    now = datetime.now(timezone.utc)
    if not (start <= now < end): sys.exit("that window is not open right now")
    # 10/23 (Twin): an old no-book row must not lock the window - only real calls count as "already called"
    # a pass doesn't lock the window either: a later real call replaces the bot's own earlier pass (Twin 10/23)
    if any(r["slug"] == a.slug and by_of(r) == a.by and r.get("excluded") != "no book" and r["side"] != "pass" for r in rows()):
        sys.exit(f"{a.by} already called this window")
    if len(a.why.strip()) < 15: sys.exit("--why is the point - say what you saw")
    if tf not in CV.enabled_tfs(): sys.exit(f"{tf} windows are switched off right now (Control Room crypto_15m_enabled / crypto_1d_enabled) - nothing to call")
    excluded = None
    if a.side == "pass":
        a.price, a.size = a.price or 0.0, 0.0
    else:
        # 10/23 honest paper: a call is scored only at a price that existed - the real ask for the side at call time.
        try:
            up_ask, down_cost, _ = CV.book_prices(CV.V.Mcp(), a.slug)
            real = up_ask if a.side == "up" else down_cost
        except Exception as e:
            sys.exit(f"could not read the book ({type(e).__name__}) - try again")
        if real is None:
            sys.exit(f"NO SELLERS for {a.side.upper()} on {a.slug} right now - nothing logged, the window stays open. "
                     f"Re-check in a minute or two and call again if the edge is still there.")
        else:
            # 10/23 (Twin): the market moves between your board read and your call. If your side now costs more than 3c above the
            # price you saw, the edge you saw may be gone - refused, nothing logged; re-read the board and call again if it's still good.
            if a.price and real > a.price + 0.03:
                sys.exit(f"REFUSED: you saw {a.price:.2f}, the real ask is now {real:.2f} (+{(real - a.price) * 100:.0f}c). Not logged. "
                         f"Re-read the board; call again only if the edge is still there.")
            if a.price and abs(a.price - real) > 0.005: print(f"note: you said {a.price}, the real ask is {real:.2f} - scored at {real:.2f}")
            a.price = real
    r = {"at": now.isoformat(timespec="seconds"), "slug": a.slug, "coin": coin_of(a.slug), "tf": tf, "side": a.side,
         "price": a.price, "size": a.size, "why": a.why.strip(), "start": start.isoformat(), "end": end.isoformat(),
         "by": a.by, "lens": a.lens or LENS[a.by]}
    if excluded: r["excluded"] = excluded
    if r["side"] != "pass":   # a real call replaces this bot's own earlier pass on the window
        keep = [x for x in rows() if not (x["slug"] == a.slug and by_of(x) == a.by and x["side"] == "pass")]
        save(keep)
    with open(LOG, "a", encoding="utf-8") as f: f.write(json.dumps(r) + chr(10))
    print(f"paper {a.by} {tf} {r['coin'].upper()} {a.side.upper()} @ {a.price} ${a.size} - logged")


EXITS = os.path.join(ROOT, "state", "crypto-exits.jsonl")


def cmd_exit(a):
    """Jaron 10/23: any bot may SELL an open crypto position before the close, whenever it judges it right (swing profit once
    Polymarket catches up, or cut a loser). Its own call - no rule. Sells through desk-trade.py's --exit path (capped to the shares
    held). The fill and P&L are matched into state/crypto-consensus.jsonl by crypto_decide.reconcile_fills."""
    import subprocess
    if CV.window(a.slug) is None: sys.exit("not an up/down slug")
    if len(a.why.strip()) < 15: sys.exit("--why is the point - say what you saw")
    mcp = CV.V.Mcp()
    p = (mcp.call("polymarket_positions", {}).get("positions") or {}).get(a.slug)
    held = float((p or {}).get("netPositionDecimal") or 0)
    if not p or abs(held) < 0.01:   # 10/23 (Twin): no live position -> sell your PAPER call at the real bid, scored as an exit
        all_rows = rows()
        mine = [r for r in all_rows if r["slug"] == a.slug and by_of(r) == a.by and r["side"] in ("up", "down") and "result" not in r
                and "exit_px" not in r and not r.get("excluded")]
        if not mine: sys.exit(f"no live position and no open paper call of yours on {a.slug} - nothing to sell")
        r = mine[-1]
        if getattr(a, "target", None):   # 10/23 (Twin): a paper target RESTS - filled later by check_targets(), not sold now
            r["target"] = a.target; r["target_why"] = a.why.strip(); save(all_rows)
            print(f"PAPER TARGET SET ({a.by}): {r['side'].upper()} bought {r['price']:.2f}, auto-sell resting at {a.target:.2f}"); return
        up_ask, down_cost, md = CV.book_prices(mcp, a.slug)
        bid = (md.get("bestBid") or {}).get("value")
        sell = float(bid) if (r["side"] == "up" and bid) else (1 - float(up_ask)) if (r["side"] == "down" and up_ask) else None
        if sell is None: sys.exit("nobody is buying that side right now - can't sell the paper call")
        r.update(exit_px=round(sell, 2), exit_at=datetime.now(timezone.utc).isoformat(timespec="seconds"), exit_why=a.why.strip(),
                 result="exit", pnl=round(r["size"] / r["price"] * sell - r["size"], 2))
        save(all_rows)
        print(f"PAPER EXIT ({a.by}): {r['side'].upper()} bought {r['price']:.2f}, sold {sell:.2f} -> ${r['pnl']:+.2f}")
        return
    side = "yes" if held > 0 else "no"
    shares = abs(held) * a.pct / 100
    up_ask, down_cost, md = CV.book_prices(mcp, a.slug)
    bid = (md.get("bestBid") or {}).get("value")
    px = float(bid) if (side == "yes" and bid) else (1 - float(up_ask)) if (side == "no" and up_ask) else 0.5
    usd = max(0.5, round(shares * max(px, 0.05) * 1.3 + 0.2, 2))        # desk-trade turns dollars into shares; it caps at the shares held
    cmd = [sys.executable, os.path.join(os.path.dirname(os.path.realpath(__file__)), "desk-trade.py"), "--by", "crew-consensus", "--slug", a.slug,
           "--side", side, "--size", f"{usd}", "--max-size", "50", "--exit", "--why", f"[{a.by} exit, {a.pct:g}%] {a.why.strip()}"]
    if getattr(a, "target", None):   # 10/23: resting auto-sell at a target price (Polymarket's "Auto sell if you're up")
        cmd += ["--target", f"{a.target}"]; usd = max(usd, round(shares * a.target * 1.3 + 0.2, 2)); cmd[cmd.index("--size") + 1] = f"{usd}"
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=240, cwd=ROOT)
    text = ((out.stdout or "") + (out.stderr or "")).strip()
    ok = out.returncode == 0 and '"placed": true' in text.lower()
    with open(EXITS, "a", encoding="utf-8") as f:
        f.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "slug": a.slug, "by": a.by, "pct": a.pct,
                            "why": a.why.strip(), "placed": ok}) + chr(10))
    print(("EXIT PLACED" if ok else "EXIT NOT PLACED") + f" ({a.by}, {side.upper()} side, about {shares:.2f} shares): " + " / ".join(l for l in text.splitlines() if l.strip())[-300:])


def cmd_due(a):
    now = datetime.now(timezone.utc)
    called = {r["slug"] for r in rows() if by_of(r) == a.by}
    mcp = CV.V.Mcp()
    missing = []
    for coin, (pair, query) in CV.COINS.items():
        sym = coin.upper()
        for q in (f"{sym} hourly up or down", f"{sym} daily up or down"):
            for ev in mcp.call("polymarket_search", {"query": q}).get("events") or []:
                for mk in ev.get("markets") or []:
                    w = CV.window(mk.get("slug") or "")
                    if w and w[0] in ("1h", "1d") and w[1] <= now < w[2] and mk.get("tradeable") and mk["slug"] not in called \
                            and mk["slug"] not in missing:
                        missing.append(mk["slug"])
    print("\n".join(["DUE (look at these - call only if you see an edge, otherwise pass):"] + missing) if missing else "nothing due - every open hourly/daily window has a call")


def check_targets():
    """Fill resting PAPER auto-sell targets when the real bid for that side reaches the target (runs with settle)."""
    all_rows = rows(); hit = 0
    open_t = [r for r in all_rows if r.get("target") and "result" not in r and datetime.fromisoformat(r["end"]) > datetime.now(timezone.utc)]
    if not open_t: return 0
    mcp = CV.V.Mcp()
    for r in open_t:
        try:
            up_ask, down_cost, md = CV.book_prices(mcp, r["slug"])
            bid = (md.get("bestBid") or {}).get("value")
            sell = float(bid) if (r["side"] == "up" and bid) else (1 - float(up_ask)) if (r["side"] == "down" and up_ask) else None
        except Exception:
            continue
        if sell is not None and sell >= r["target"]:
            r.update(exit_px=r["target"], exit_at=datetime.now(timezone.utc).isoformat(timespec="seconds"), exit_why="auto-sell target hit",
                     result="exit", pnl=round(r["size"] / r["price"] * r["target"] - r["size"], 2)); hit += 1
    if hit: save(all_rows)
    return hit


def cmd_settle(a):
    check_targets()
    now = datetime.now(timezone.utc)
    all_rows = rows()
    for r in all_rows:   # old empty-book rows (priced at the bot's own fair number) are excluded, not rescored
        if "NO BOOK" in r.get("why", "").upper() and not r.get("excluded") and r["side"] != "pass": r["excluded"] = "no book"
    for r in all_rows:
        if r.get("excluded") or "result" in r or r["side"] == "pass" or datetime.fromisoformat(r["end"]) > now: continue
        s = CV.price_at(PAIR[r["coin"]], datetime.fromisoformat(r["start"]))
        e = CV.price_at(PAIR[r["coin"]], datetime.fromisoformat(r["end"]))
        if s is None or e is None: continue
        went = "up" if e >= s else "down"
        win = went == r["side"]
        r.update(result="win" if win else "loss", went=went, open_px=s, close_px=e,
                 pnl=round((r["size"] / r["price"] - r["size"]) if win else -r["size"], 2))
    save(all_rows)
    ex = [r for r in all_rows if r.get("excluded")]
    all_rows = [r for r in all_rows if not r.get("excluded")]   # tables below never count excluded rows
    done = [r for r in all_rows if "result" in r]
    lines = [f"# Crypto twins - up/down PAPER trades (updated {now:%Y-%m-%d %H:%M} UTC)", "",
             "No money moves here. Hourly + daily: a call (or a logged pass) every window from each bot. 15 min: optional. "
             "Kraken stands in for CF Benchmarks.", "",
             "## By bot (lens)", "| Bot | Lens | Calls | Passes | Settled | Won | Paper money |", "|---|---|---|---|---|---|---|"]
    for b in BOTS:
        t = [r for r in all_rows if by_of(r) == b]; d = [r for r in t if "result" in r]
        lines.append(f"| {b} | {LENS[b]} | {sum(r['side'] != 'pass' for r in t)} | {sum(r['side'] == 'pass' for r in t)} | {len(d)} | "
                     f"{sum(r['pnl'] > 0 for r in d)}/{len(d)} | ${sum(r['pnl'] for r in d):+.2f} |")
    # 10/22 (Jaron/Twin): calls on an EMPTY book used the bot's own fair price - no real trade was possible there. Shown apart.
    nb = [r for r in done if "NO BOOK" in r.get("why", "").upper()]
    if nb:
        lines.append(f"\nOf these, {len(nb)} settled calls were on an EMPTY book (priced at the bot's own fair price, no real fill possible): "
                     f"{sum(r['pnl'] > 0 for r in nb)}/{len(nb)} won, ${sum(r['pnl'] for r in nb):+.2f}. "
                     f"Real-book record = the totals minus these.")
    lines += ["", "## By window", "| Window | Calls | Settled | Won | Paper money |", "|---|---|---|---|---|"]
    for tf in ("15m", "1h", "1d"):
        t = [r for r in all_rows if r["tf"] == tf and r["side"] != "pass"]; d = [r for r in t if "result" in r]
        won = sum(r["pnl"] > 0 for r in d)
        lines.append(f"| {tf} | {len(t)} | {len(d)} | {won}/{len(d)} | ${sum(r['pnl'] for r in d):+.2f} |")
    # Twin 10/22 #4: hit rate + money by coin and by the price paid (is 0.78 actually cheap?)
    def table(title, key, keys):
        out = ["", f"## By {title}", f"| {title} | Settled | Won | Paper money |", "|---|---|---|---|"]
        for k in keys:
            d = [r for r in done if key(r) == k]
            if d: out.append(f"| {k} | {len(d)} | {sum(r['pnl'] > 0 for r in d)}/{len(d)} | ${sum(r['pnl'] for r in d):+.2f} |")
        return out
    band = lambda r: "under 0.50" if r["price"] < 0.5 else "0.50-0.70" if r["price"] < 0.7 else "0.70-0.90" if r["price"] < 0.9 else "0.90+"
    lines += table("coin", lambda r: r["coin"].upper(), ["BTC", "ETH", "SOL", "XRP"])
    lines += table("price paid", band, ["under 0.50", "0.50-0.70", "0.70-0.90", "0.90+"])
    lines += ["", "## Last 15", "| When (UTC) | Bot | Coin | Window | Call @ price | Result | Why |", "|---|---|---|---|---|---|---|"]
    for r in all_rows[-15:][::-1]:
        res = (f"{r['result']} ({r.get('went', 'sold @%.2f' % r.get('exit_px', 0))}) ${r['pnl']:+.2f}") if "result" in r else ("open, target %.2f" % r['target'] if r.get('target') else "open")
        lines.append(f"| {r['at'][5:16]} | {by_of(r)} | {r['coin'].upper()} | {r['tf']} | {r['side']} @ {r['price']} | {res} | {r['why'][:90]} |")
    open(SUMMARY, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print(f"settled {len(done)} of {len(all_rows)}; summary -> state/twin-crypto-paper.md")


def main():
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)
    c = sp.add_parser("call"); c.add_argument("slug"); c.add_argument("side", choices=["up", "down", "pass"])
    c.add_argument("--by", choices=BOTS, default="jarons-twin"); c.add_argument("--lens", default=None)
    c.add_argument("--price", type=float, default=None); c.add_argument("--size", type=float, default=3); c.add_argument("--why", required=True)
    e = sp.add_parser("exit"); e.add_argument("slug"); e.add_argument("--by", choices=BOTS, required=True)
    e.add_argument("--pct", type=float, default=100); e.add_argument("--why", required=True)
    e.add_argument("--target", type=float, default=None, help="auto-sell target price for your side (0-1); rests until it fills")
    d = sp.add_parser("due"); d.add_argument("--by", choices=BOTS, default="jarons-twin"); sp.add_parser("settle")
    a = ap.parse_args()
    {"call": cmd_call, "exit": cmd_exit, "due": cmd_due, "settle": cmd_settle}[a.cmd](a)


if __name__ == "__main__":
    main()
