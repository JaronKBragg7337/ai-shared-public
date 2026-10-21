#!/usr/bin/env python3
"""
live-board.py - the free half of Live Wire. Written 2026-09-25 by Claude Code (Jaron: Grok Bot burns more usage than it earns;
anything that is not money or Grok-only info moves off Grok).

Every live game on Polymarket US, with the real score from ESPN's free scoreboards, the current price, and what changed since
the last run. No AI, no key, no cost. A Windows task runs it every 5 minutes. Live Wire (Grok) reads ONE file -
state/live-board.md - and only spends its own usage deciding on the games flagged at the top.

Flags (the three shapes of edge in agents/grok-bot/LIVE-WIRE.md):
  FINISHED, BOOK OPEN   ESPN says the game is over, the price still sits between 10c and 90c.
  SCORE MOVED, PRICE FLAT   the score changed since the last run and the price moved less than 2c.
  LEADER UNDER 50c      the side that is ahead is priced under 50c.
This script never trades and never decides. It is a scoreboard.

Run with the polymarket-us venv python:
    runtime\\polymarket-us-agent-venv\\Scripts\\python.exe tools\\live-board.py
"""
from __future__ import annotations

import json
import os
import re
import urllib.request
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
OUT_MD = os.path.join(ROOT, "state", "live-board.md")
OUT_JSON = os.path.join(ROOT, "state", "live-board.json")
LIVE_WINDOW_H = 6          # a market whose game started within this many hours counts as possibly live

# slug prefix -> ESPN scoreboard path
# keyed by the slug's SECOND part (aec-mlb-..., asc-mlb-...-neg-1pt5 and tsc-mlb-...-7pt5 are all "mlb")
LEAGUES = {
    "mlb": "baseball/mlb", "atp": "tennis/atp", "wta": "tennis/wta", "nfl": "football/nfl",
    "cfb": "football/college-football", "nba": "basketball/nba", "wnba": "basketball/wnba",
    "nhl": "hockey/nhl", "cbb": "basketball/mens-college-basketball", "unl": "soccer/uefa.nations",
    "epl": "soccer/eng.1", "mls": "soccer/usa.1", "ucl": "soccer/uefa.champions", "uel": "soccer/uefa.europa",
}


def league(slug):
    parts = slug.split("-")
    return LEAGUES.get(parts[1]) if len(parts) > 1 else None


def espn(path):
    url = f"https://site.api.espn.com/apis/site/v2/sports/{path}/scoreboard"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        return json.load(urllib.request.urlopen(req, timeout=20))
    except Exception:
        return {}


def competitions(board):
    """Flatten ESPN's two shapes: team sports (events[].competitions) and tennis (events[].groupings[].competitions)."""
    for ev in board.get("events", []):
        for c in ev.get("competitions", []) or []:
            yield c, ev
        for g in ev.get("groupings", []) or []:
            for c in g.get("competitions", []) or []:
                yield c, ev


def name_of(comp):
    return (comp.get("athlete") or {}).get("displayName") or (comp.get("team") or {}).get("displayName") or comp.get("displayName") or ""


def tokens(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode()   # Turkiye == Türkiye
    return {t for t in re.findall(r"[a-z]+", s.lower()) if len(t) > 2}


def score_of(c, is_tennis):
    comps = c.get("competitors", [])
    st = (c.get("status") or {}).get("type") or {}
    rows = []
    for x in comps:
        if is_tennis:
            sets = [int(l.get("value", 0)) for l in x.get("linescores", []) or []]
            rows.append({"name": name_of(x), "sets": sets})
        else:
            rows.append({"name": name_of(x), "score": x.get("score")})
    leader = None
    if is_tennis and len(rows) == 2:
        a, b = rows[0]["sets"], rows[1]["sets"]
        won = [sum(1 for i in range(min(len(a), len(b))) if (a[i] > b[i] and (a[i] >= 6 or i < len(a) - 1))),
               sum(1 for i in range(min(len(a), len(b))) if (b[i] > a[i] and (b[i] >= 6 or i < len(b) - 1)))]
        text = " | ".join(f"{r['name']} {' '.join(map(str, r['sets']))}" for r in rows)
        cur = (a[-1] - b[-1]) if a and b else 0
        if won[0] != won[1]:
            leader = rows[0]["name"] if won[0] > won[1] else rows[1]["name"]
        elif cur:
            leader = rows[0]["name"] if cur > 0 else rows[1]["name"]
    else:
        text = " - ".join(f"{r['name']} {r.get('score')}" for r in rows)
        try:
            s = [float(r.get("score") or 0) for r in rows]
            if len(s) == 2 and s[0] != s[1]:
                leader = rows[0]["name"] if s[0] > s[1] else rows[1]["name"]
        except ValueError:
            pass
    return {"state": st.get("state"), "detail": st.get("detail") or st.get("description"), "text": text, "leader": leader,
            "names": [r["name"] for r in rows]}


def main():
    from polymarket_us import PolymarketUS
    c = PolymarketUS(timeout=30.0)
    now = datetime.now(timezone.utc)
    live = []
    for i in range(10):
        ms = c.markets.list({"closed": False, "active": True, "limit": 100, "offset": i * 100,
                             "orderBy": ["volume"], "orderDirection": "desc"}).get("markets") or []
        for m in ms:
            gs = m.get("gameStartTime")
            try:
                g = datetime.fromisoformat(gs.replace("Z", "+00:00")) if gs else None
            except ValueError:
                g = None
            if g and now - timedelta(hours=LIVE_WINDOW_H) < g < now:
                live.append(m)
        if len(ms) < 100:
            break

    boards = {}
    for m in live:
        path = league(m["slug"])
        if path and path not in boards:
            boards[path] = espn(path)

    prev = {}
    if os.path.exists(OUT_JSON):
        try:
            prev = {r["slug"]: r for r in json.load(open(OUT_JSON, encoding="utf-8")).get("games", [])}
        except (OSError, ValueError, KeyError):
            prev = {}

    games = []
    for m in live:
        slug = m["slug"]
        sides = [s.get("description") for s in m.get("marketSides", [])]
        long_side = next((s.get("description") for s in m.get("marketSides", []) if s.get("long")), sides[0] if sides else "?")
        try:
            bbo = c.markets.bbo(slug)
            bbo = bbo.get("marketData") or bbo
            bid = float(((bbo.get("bestBid") or bbo.get("bestBidQuote") or {}) or {}).get("value") or 0) or None
            ask = float(((bbo.get("bestAsk") or bbo.get("bestAskQuote") or {}) or {}).get("value") or 0) or None
        except Exception:
            bid = ask = None
        if bid is None or ask is None:
            bid = float((m.get("bestBidQuote") or {}).get("value") or 0) or None
            ask = float((m.get("bestAskQuote") or {}).get("value") or 0) or None
        mid = round((bid + ask) / 2, 3) if bid and ask else None

        path = league(slug)
        score = None
        if path:
            q = m.get("question") or m.get("title") or ""
            vs = re.search(r"(?:event|match)?\s*([A-Z][^,?]+?) vs\.? ([A-Z][^,?]+?)(?: scheduled| in |\?|$)", q)
            want = [tokens(s) for s in sides if s not in ("Yes", "No") and not re.match(r"^[+-]?\d|Over|Under", s or "")]
            if len(want) < 2 and vs:
                want = [tokens(vs.group(1)), tokens(vs.group(2))]
            if len(want) < 2:
                w = re.search(r"Will (.+?) win against (.+?) in", q)
                want = [tokens(w.group(1)), tokens(w.group(2))] if w else want
            best, best_hits, best_rank = None, 0, -1
            for comp, ev in competitions(boards.get(path, {})):
                names = " ".join(name_of(x) for x in comp.get("competitors", []))
                have = tokens(names)
                hits = sum(1 for w in want if w & have)
                # doubleheaders: same two teams twice on ESPN. Prefer the game in progress, then upcoming, then finished
                # (fixed 2026-09-25 after CHC-BOS game 1's final showed on game 2's market).
                rank = {"in": 2, "pre": 1}.get(((comp.get("status") or {}).get("type") or {}).get("state"), 0)
                if hits > best_hits or (hits == best_hits and hits and rank > best_rank):
                    best, best_hits, best_rank = comp, hits, rank
            if best is not None and best_hits >= min(2, len(want)):
                score = score_of(best, path.startswith("tennis"))

        flags = []
        p = prev.get(slug)
        if score and mid is not None:
            long_toks = tokens(long_side)
            if long_side in ("Yes", "No"):
                w = re.search(r"Will (.+?) win", m.get("question") or "")
                long_toks = tokens(w.group(1)) if w else set()
                if long_side == "No":
                    long_toks = set()
            if score["state"] == "post" and 0.10 < mid < 0.90:
                flags.append("FINISHED, BOOK OPEN")
            if p and p.get("score") and p["score"].get("text") != score["text"] and p.get("mid") is not None \
                    and abs(mid - p["mid"]) < 0.02:
                flags.append("SCORE MOVED, PRICE FLAT")
            if score["leader"] and score["state"] == "in":
                leader_is_long = bool(tokens(score["leader"]) & long_toks) if long_toks and re.match(r"^[A-Za-z]", long_side or "") and not re.match(r"^(Over|Under)", long_side) else None
                if leader_is_long is True and mid < 0.50:
                    flags.append("LEADER UNDER 50c")
                elif leader_is_long is False and mid > 0.50:
                    flags.append("LEADER UNDER 50c")
        games.append({"slug": slug, "sides": sides, "long": long_side, "bid": bid, "ask": ask, "mid": mid,
                      "score": score, "flags": flags, "prev_mid": p.get("mid") if p else None,
                      "question": (m.get("question") or m.get("title") or "")[:140]})

    games.sort(key=lambda g: (-len(g["flags"]), g["slug"]))
    stamp = now.strftime("%Y-%m-%d %H:%M UTC")
    json.dump({"at": stamp, "games": games}, open(OUT_JSON, "w", encoding="utf-8"), indent=1)
    lines = [f"# Live board - {stamp}",
             "Free scoreboard for Darios Twin (tools/live-board.py, every 5 min). Price = the FIRST side's (YES/long) bid/ask.",
             f"{len(games)} games in progress on Polymarket US; {sum(1 for g in games if g['flags'])} flagged.", ""]
    for g in games:
        sc = g["score"]
        price = f"{g['bid']:.2f}/{g['ask']:.2f}" if g["bid"] and g["ask"] else "no book"
        move = ""
        if g["prev_mid"] is not None and g["mid"] is not None:
            d = g["mid"] - g["prev_mid"]
            move = f" ({'+' if d >= 0 else ''}{d:.2f} since last)"
        flag = f"**{' + '.join(g['flags'])}** | " if g["flags"] else ""
        score_txt = f"{sc['text']} [{sc['detail']}]" if sc else "no ESPN score (ITF/other - check the page)"
        lines.append(f"- {flag}`{g['slug']}` | {g['long']} {price}{move} | {score_txt}")
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines[:12]))


if __name__ == "__main__":
    main()
