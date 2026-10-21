#!/usr/bin/env python3
"""
proposer.py - keeps the approve queue FED. Screen -> price-blind research -> edge math -> row.

WHY, from Jaron 2026-09-11:
    "Only one thing showed for me to approve ... I wanted things more frequently than that."
    "If I wanna go look 30 minutes later, an hour later, I want there to be more things there
    for me to approve."
    "That's the thing I want AI to just look at, see it, and then just do it. If it still needs
    an approve button that's fine."

    The pipeline was starved, not the market: 500 open markets, ~200 pass the liquidity screen
    on any given night. Nobody was running the screen unless someone typed at Bridge in a chat.
    This runs it on a schedule. Bridge and Scout keep doing the same job by hand whenever they
    like - whoever proposes first, proposes. Same table, same page, same approve button.

THE TWO HALVES, KEPT APART (estimation isolation - see ESTIMATION-ISOLATION.md)
    SCREEN (this file, dumb):   open, not crypto, ask 0.10-0.90, spread <= 2c, sorted by volume.
    RESEARCH (a model, blind):  gets the QUESTION, the resolution text, headlines with dates, and
                                background. NEVER the price, spread, book, or which side is cheap.
                                Returns probability + confidence + drivers + kill triggers.
    EDGE (this file, dumb):     yes-edge = p - ask ; no-edge = bid - p. Must beat the spread AND
                                MIN_EDGE. Size by confidence. Insert row. verifier.py re-checks the
                                numbers within 5 min; Jaron taps; executor.py places.

RESEARCHER BACKENDS (--researcher)
    deepseek  DeepSeek API, OpenAI-compatible. Needs DEEPSEEK_API_KEY in ~/.secrets/keys.env.
              Jaron funded $20 on 2026-09-11. Cheap enough to run every couple of hours.
    codex     `codex exec` read-only. Uses the Codex subscription. Slower, no extra cost.
    qwen      Local Ollama qwen3.5:4b. Free, always on. Weakest reader - see 2026-09-10 misreads.
    Default: deepseek if the key is present, else codex.

EVERY ESTIMATE IS LOGGED to state/scout-estimates.md whether or not it becomes a proposal.
That file is the calibration record (TODO #3). When markets resolve, compare.

USAGE
    python tools/proposer.py                     # dry run: research + math, prints, inserts nothing
    python tools/proposer.py --commit            # inserts proposals into trade_proposals
    python tools/proposer.py --commit --max 8 --researcher codex

Run with the polymarket-us venv python (it has the polymarket_us client):
    runtime\\polymarket-us-agent-venv\\Scripts\\python.exe tools\\proposer.py --commit
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SECRETS = os.path.join(os.path.expanduser("~"), ".secrets", "keys.env")
MCP = "http://127.0.0.1:8765/mcp"
OLLAMA = "http://127.0.0.1:11434"
LOG = os.path.join(ROOT, "state", "proposer.md")
ESTIMATES = os.path.join(ROOT, "state", "scout-estimates.md")
SENTI_REQ = os.path.join(ROOT, "inbox", "sentiment-requests.json")   # for Bridge: what X thinks about these
DECLINED = os.path.join(ROOT, "state", "proposer-declined.json")   # slug -> when a researcher refused

# ---- the screen (dumb, numeric, from TRADING.md) ---------------------------------------
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.realpath(__file__)))
from settings import setting  # Control Room values (/admin/control/), built-in default if unreachable
MAX_SPREAD = setting("deepseek_max_spread", 0.02)
PRICE_LO, PRICE_HI = 0.10, 0.90
EXCLUDE_CATEGORIES = {"crypto"}          # PolyBench: LLMs lose worst here, with high confidence
MIN_EDGE = setting("deepseek_min_edge", 0.03)                          # edge must beat spread AND this floor (model noise guard)
SIZE_BY_CONFIDENCE = {"low": setting("deepseek_size_low_usd", 2.0), "medium": setting("deepseek_size_medium_usd", 4.0), "high": setting("deepseek_size_high_usd", 8.0)}   # raised 2026-09-11 03:20 after Jaron funded $100; $1 "didn't like it". He can still edit per row.
RECENT_DAYS = 3                          # do not re-propose the same slug within this window
MIN_HOURS_TO_END = 1                     # skip markets that end within this many hours
PER_CATEGORY_CAP = 3                     # spread candidates across categories per run
# Jaron 2026-09-12: for these, the research states what it sees and JARON picks the side on the
# page (both prices shown). Sports / culture / plain finance stay pre-picked by the arithmetic.
SIDE_OPEN_WORDS = ("politic", "election", "midterm", "senate", "house", "president", "congress", "governor",
                   "geopolit", "tariff", "sanction", "fed ", "fomc", "cpi", "macro",
                   "openai", "anthropic", "google", "gemini", "grok", "xai", "deepseek", "meta ai", "llama",
                   "nvidia", "amd", "intel", "tsmc", "chip", "gpu", "semiconductor", "ai model", "ai coding", "frontier")


def side_open(c, ev):
    hay = " ".join(str(x) for x in (c.get("category"), c.get("question"), c.get("outcome"), c.get("title"),
                                     ev.get("tags"), ev.get("event_title"))).lower()
    return c.get("category") in ("politics", "macro", "technology") or any(w in hay for w in SIDE_OPEN_WORDS)
# Jaron 2026-09-11 08:36, after a morning of table tennis: "Those are trades I like. Quick. Not
# weeks later. Both are important though." So: half of each run from markets that settle within
# SOON_HOURS (games today, this week's data prints), half from the long book.
SOON_HOURS = 48
MAX_DAYS_TO_SETTLE = setting("max_days_to_settle", 14)   # Jaron 2026-09-25: short-term only on Polymarket; same number as desk-trade.py
SOON_SHARE = 0.5


def log(m):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {m}"
    print(line, flush=True)
    try:
        with open(LOG, "a", encoding="utf-8", newline="\n") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def secrets() -> dict:
    out = {}
    if os.path.exists(SECRETS):
        with open(SECRETS, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    out[k.strip()] = v.strip().strip('"').strip("'")
    return out


def sb(env, method, path, body=None):
    url = f"{env['SUPABASE_URL'].rstrip('/')}/rest/v1/{path}"
    key = env["SUPABASE_SERVICE_ROLE_KEY"]
    req = urllib.request.Request(
        url, data=json.dumps(body).encode() if body is not None else None, method=method,
        headers={"apikey": key, "Authorization": f"Bearer {key}",
                 "Content-Type": "application/json", "Prefer": "return=representation"})
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = r.read()
        return json.loads(raw) if raw else []


class Mcp:
    def __init__(self):
        self.sid = None
        self._rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                   "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                              "clientInfo": {"name": "proposer", "version": "1"}}})

    def _rpc(self, payload):
        h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        if self.sid:
            h["Mcp-Session-Id"] = self.sid
        req = urllib.request.Request(MCP, data=json.dumps(payload).encode(), headers=h)
        with urllib.request.urlopen(req, timeout=120) as r:
            if r.headers.get("Mcp-Session-Id"):
                self.sid = r.headers["Mcp-Session-Id"]
            raw = r.read().decode("utf-8", "replace")
            for line in raw.splitlines():
                if line.startswith("data: "):
                    return json.loads(line[6:])
            return json.loads(raw) if raw.strip() else None

    def call(self, name, args):
        r = self._rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                       "params": {"name": name, "arguments": args}})
        try:
            return r["result"]["content"][0]["text"]
        except Exception:
            return json.dumps(r)


# ---- screen -----------------------------------------------------------------------------

def fetch_open_markets(pages=5):
    from polymarket_us import PolymarketUS   # venv python only
    c = PolymarketUS(timeout=30.0)
    out = []
    for i in range(pages):
        r = c.markets.list({"closed": False, "active": True, "limit": 100, "offset": i * 100,
                            "orderBy": ["volume"], "orderDirection": "desc"})
        ms = r.get("markets") or []
        out += ms
        if len(ms) < 100:
            break
    return out


def fetch_event_index(pages=6):
    """market slug -> where it lives: event slug/title, category path, app URL.
    Jaron 2026-09-11: he could not tell what sport a proposal was or where to find it in the app."""
    from polymarket_us import PolymarketUS
    c = PolymarketUS(timeout=30.0)
    idx = {}
    for i in range(pages):
        try:
            r = c.events.list({"closed": False, "active": True, "limit": 100, "offset": i * 100,
                               "orderBy": ["volume"], "orderDirection": "desc"})
        except Exception:
            break
        evs = r.get("events") or []
        for e in evs:
            labels = []
            for t in e.get("tags") or []:
                if t.get("label") and t["label"] not in labels:
                    labels.append(t["label"])
            info = {"event_slug": e.get("slug"), "event_title": e.get("title"),
                    "category": e.get("category"), "tags": " › ".join(labels[:5]),
                    "market_url": f"https://polymarket.us/event/{e.get('slug')}" if e.get("slug") else None}
            n_out = len(e.get("markets") or [])
            for m in e.get("markets") or []:
                if m.get("slug"):
                    idx[m["slug"]] = dict(info, market_type=m.get("sportsMarketType") or m.get("marketType"),
                                          n_outcomes=n_out)
        if len(evs) < 100:
            break
    return idx


def screen(markets, skip_slugs):
    now = datetime.now(timezone.utc)
    cands = []
    for m in markets:
        if m.get("category") in EXCLUDE_CATEGORIES or m.get("closed") or not m.get("active"):
            continue
        if m.get("slug") in skip_slugs:
            continue
        b = (m.get("bestBidQuote") or {}).get("value")
        a = (m.get("bestAskQuote") or {}).get("value")
        if not (b and a):
            continue
        b, a = float(b), float(a)
        if not (PRICE_LO <= a <= PRICE_HI) or round(a - b, 4) > MAX_SPREAD:
            continue
        end = m.get("endDate")
        try:
            end_dt = datetime.fromisoformat(end.replace("Z", "+00:00")) if end else None
        except ValueError:
            end_dt = None
        if end_dt and end_dt - now < timedelta(hours=MIN_HOURS_TO_END):
            continue
        gs = m.get("gameStartTime")
        gs_future = False
        if gs:
            try:
                gs_dt = datetime.fromisoformat(gs.replace("Z", "+00:00"))
                delta_h = (gs_dt - now).total_seconds() / 3600
                if -8 <= delta_h < MIN_HOURS_TO_END:
                    continue        # in progress or about to start: Live Wire's territory, not pre-match research
                gs_future = delta_h >= MIN_HOURS_TO_END
                # older than 8h = a futures market with a stale gameStartTime (NFL 2027), not a game
            except ValueError:
                pass
        # Which outcome does the long side (the one you buy at the ask) represent? For Yes/No
        # markets the title carries it ("No Change", "James Talarico (D)"); for sports moneylines
        # the long side is a team or fighter and the title is empty. The researcher MUST know
        # which outcome it is estimating - "Yes" alone means nothing for "Canelo vs Mbilli".
        long_side = next((sd.get("description") for sd in m.get("marketSides", []) if sd.get("long")), None)
        outcome = long_side if long_side and long_side != "Yes" else (m.get("title") or "Yes")
        # Same-name ambiguity (Jaron 2026-09-11): "Pysmennyi Yevhen vs Masko Yevhen" - if the two sides
        # share a first or last name, a researcher or a bot can attach the thesis to the wrong side.
        sides = [sd.get("description", "") for sd in m.get("marketSides", [])]
        if len(sides) == 2:
            a_toks = {t.lower() for t in sides[0].split() if len(t) > 2}
            b_toks = {t.lower() for t in sides[1].split() if len(t) > 2}
            if a_toks & b_toks:
                continue
        # For sports the venue's endDate is ~2 weeks AFTER the game (settlement window); the real
        # "when do I know" is gameStartTime + a few hours. Use that when present.
        # only single-game markets (moneyline/spread/total) settle at game time; futures like tec-wnba-champion carry a
        # gameStartTime (finals start) but settle weeks later - use endDate for those (2026-09-26)
        settles = m.get("gameStartTime") if gs_future and m["slug"].startswith(("aec-", "asc-", "tsc-", "atc-")) else end
        cands.append({"slug": m["slug"], "category": m.get("category"), "bid": b, "ask": a, "outcome": outcome,
                      "settles": settles, "gameStartTime": m.get("gameStartTime"),
                      "spread": round(a - b, 4), "question": m.get("question") or m.get("title"),
                      "title": m.get("title"), "description": (m.get("description") or "")[:1500],
                      "endDate": end, "outcomes": m.get("outcomes")})
    # two horizons: SOON (settles within SOON_HOURS - quick feedback, Jaron's favourite) and LONG.
    def hours_left(c):
        try:
            return (datetime.fromisoformat(c["settles"].replace("Z", "+00:00")) - now).total_seconds() / 3600
        except (TypeError, ValueError, AttributeError):
            return 1e9
    # Jaron 2026-09-25: Polymarket pays this month's bills - nothing that settles more than MAX_DAYS_TO_SETTLE out.
    cands = [c for c in cands if hours_left(c) <= MAX_DAYS_TO_SETTLE * 24]
    soon = [c for c in cands if hours_left(c) <= SOON_HOURS]
    long_ = [c for c in cands if hours_left(c) > SOON_HOURS]
    for c in soon:
        c["horizon"] = "soon"
    for c in long_:
        c["horizon"] = "long"

    def round_robin(lst):
        by_cat = {}
        for c in lst:
            by_cat.setdefault(c["category"], []).append(c)
        out, i = [], 0
        while True:
            added = False
            for cat, group in by_cat.items():
                if i < len(group) and i < PER_CATEGORY_CAP:
                    out.append(group[i]); added = True
            if not added:
                break
            i += 1
        return out
    # interleave so a --max of 6 yields ~3 soon + ~3 long (whichever exists)
    a_list, b_list = round_robin(soon), round_robin(long_)
    picked = []
    while a_list or b_list:
        if a_list:
            picked.append(a_list.pop(0))
        if b_list:
            picked.append(b_list.pop(0))
    return picked, len(cands)


# ---- research (price-blind) -------------------------------------------------------------

PROMPT = """You are an independent forecaster. You are given ONE prediction-market question with its
resolution rules, recent headlines WITH DATES, and background. You are deliberately NOT given any
market price, odds, or what anyone else thinks - estimate from the evidence alone.

Today is {today}.

QUESTION: {question}
MARKET TITLE: {title}
OUTCOME BEING ESTIMATED: "{outcome}" (the market resolves YES if this outcome happens)
RESOLUTION RULES:
{description}

RECENT HEADLINES (check the dates - do not treat old news as current):
{news}

BACKGROUND:
{reference}

Reply with ONLY a JSON object, no prose, exactly these keys:
{{"probability": <0.00-1.00 that the outcome resolves YES>,
  "confidence": "low"|"medium"|"high",
  "drivers": "<2-3 sentences: the evidence that moved you>",
  "kill_triggers": "<1-2 sentences: what would make you revise sharply>"}}
Calibration matters more than boldness. If the evidence is thin, say so with a wide (low) confidence
and a probability near your honest base rate - do not round to 0.05 or 0.95 without a reason."""


# ---- THE RESEARCH SPLIT (decisions/RESEARCH-SPLIT.md) -----------------------------------
# No model is asked to forecast. It is asked ordinary questions about the evidence; the
# number is assembled below by arithmetic anyone can read. Jaron's design, 2026-09-11.

FACTS_PROMPT = """You are a careful research assistant. Summarize what the material below says about ONE
question. Do not predict anything and do not give odds - just organize the evidence.

Today is {today}.

TOPIC: {question}
THE SPECIFIC THING BEING ASKED ABOUT: "{outcome}"
HOW THE QUESTION WOULD BE SETTLED:
{description}

RECENT HEADLINES (with dates - note when something is old):
{news}

BACKGROUND:
{reference}

Answer with ONLY a JSON object, exactly these keys:
{{"for": [{{"fact": "<one dated fact that points TOWARD the thing happening>", "date": "<YYYY-MM-DD or unknown>", "strength": <1 weak, 2 solid, 3 decisive>}}],
  "against": [{{"fact": "<one dated fact that points AWAY from it>", "date": "...", "strength": <1-3>}}],
  "key_people": ["<name - role, if relevant>"],
  "absences_or_obstacles": ["<injuries, suspensions, legal blocks, deadlines, anything in the way>"],
  "pushback": "<who is resisting this and how hard, or 'none seen'>",
  "base_rate": {{"value": <0.00-1.00 only if the material itself states how often this kind of thing happens, else null>, "source": "<where that came from, or 'not in material'>"}},
  "freshest_date": "<the most recent date in the material>"}}
Rules: only facts that appear in the material. Empty lists are fine. Old news is weak evidence
about now - lower its strength. Never include a probability of your own."""


def sentiment_hint(slug):
    """Optional Grok/X sentiment, if a Grok Bot has written one: state/sentiment/<slug>.json
    {"lean": "for"|"against"|"split", "strength": 1-3, "at": iso, "note": "..."}. Used only if
    fresh (24h). The channel that fills this is not built yet - see RESEARCH-SPLIT.md."""
    path = os.path.join(ROOT, "state", "sentiment", f"{slug}.json")
    try:
        d = json.load(open(path, encoding="utf-8"))
        at = datetime.fromisoformat(d["at"].replace("Z", "+00:00"))
        if datetime.now(timezone.utc) - at < timedelta(hours=24):
            return d
    except Exception:
        pass
    return None


def parse_facts(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except ValueError:
        return None
    if "for" not in d and "against" not in d:
        return None

    def clean(lst):
        out = []
        for x in lst or []:
            if isinstance(x, dict) and x.get("fact"):
                try:
                    st = int(x.get("strength", 1))
                except (TypeError, ValueError):
                    st = 1
                out.append({"fact": str(x["fact"])[:220], "date": str(x.get("date", "unknown"))[:10],
                            "strength": min(max(st, 1), 3)})
        return out[:8]
    br = d.get("base_rate") or {}
    try:
        brv = float(br.get("value")) if br.get("value") is not None else None
        if brv is not None and not (0.0 < brv < 1.0):
            brv = None
    except (TypeError, ValueError):
        brv = None
    return {"for": clean(d.get("for")), "against": clean(d.get("against")),
            "key_people": [str(x)[:80] for x in (d.get("key_people") or [])][:6],
            "obstacles": [str(x)[:120] for x in (d.get("absences_or_obstacles") or [])][:6],
            "pushback": str(d.get("pushback", ""))[:200],
            "base_rate": brv, "base_rate_source": str(br.get("source", ""))[:120],
            "freshest": str(d.get("freshest_date", ""))[:10]}


SPLIT_STEP = 0.06          # how far one net point of evidence moves the number
SPLIT_MIN_EDGE = 0.08      # the assembled number is coarser than a model's - demand more edge


def assemble(c, facts, today_iso, senti=None):
    """Prior from the market's shape (or a base rate the model READ), shifted by net evidence.
    Every input is returned so the row can show its work."""
    n = c.get("n_outcomes") or 0
    if facts["base_rate"] is not None:
        prior, prior_why = facts["base_rate"], f"base rate in material ({facts['base_rate_source']})"
    elif n >= 3:
        prior, prior_why = max(1.0 / n, 0.05), f"1 of {n} outcomes in this event"   # floor 5%: big events bundle props, not just outcomes
    else:
        prior, prior_why = 0.5, "binary question, no base rate read"
    f_pts = sum(x["strength"] for x in facts["for"])
    a_pts = sum(x["strength"] for x in facts["against"])
    net = f_pts - a_pts
    s_pts = 0
    if senti:
        s_pts = int(senti.get("strength", 1)) * (1 if senti.get("lean") == "for" else -1 if senti.get("lean") == "against" else 0)
        net += s_pts
    p = min(max(prior + SPLIT_STEP * net, 0.03), 0.97)
    fresh = False
    try:
        fresh = (datetime.fromisoformat(today_iso[:10]) - datetime.fromisoformat(facts["freshest"])).days <= 14
    except ValueError:
        pass
    agree = (senti is not None) and ((s_pts > 0) == (f_pts - a_pts > 0))
    if abs(net) >= 5 and fresh and (senti is None or agree):
        conf = "high"
    elif abs(net) >= 3:
        conf = "medium"
    else:
        conf = "low"
    why = (f"prior {prior:.2f} ({prior_why}); for {f_pts} pts / against {a_pts} pts"
           + (f"; X sentiment {senti.get('lean')} {s_pts:+d}" if senti else "")
           + f" -> net {net:+d} x {SPLIT_STEP} -> p {p:.2f}")
    return {"p": round(p, 3), "confidence": conf, "net": net, "why": why,
            "drivers": ("FOR: " + "; ".join(f"{x['fact']} ({x['date']}, {x['strength']})" for x in facts["for"][:3]) + " | "
                        "AGAINST: " + "; ".join(f"{x['fact']} ({x['date']}, {x['strength']})" for x in facts["against"][:3]))[:700],
            "kill": ("obstacles: " + "; ".join(facts["obstacles"][:3]) + (" | pushback: " + facts["pushback"] if facts["pushback"] else ""))[:400]}


def gather(mcp, c):
    q = f"{c['question']} {c['outcome']}" if c["outcome"] not in c["question"] else c["question"]
    try:
        news = mcp.call("research_news", {"query": q, "limit": 8})
    except Exception as e:
        news = f"(news lookup failed: {e})"
    try:
        ref = mcp.call("research_reference", {"topic": q})
    except Exception as e:
        ref = f"(reference lookup failed: {e})"
    # what the researcher was actually shown - stamped on the row so the page can say "live check"
    dates = sorted(set(re.findall(r"20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]", news)))
    n_head = len(re.findall(r"(?m)^\s*[-*]", news))
    c["evidence"] = (f"live check: {n_head or 'some'} headlines" + (f", newest {dates[-1]}" if dates else ", undated")
                     + f"; background {'yes' if ref and 'failed' not in ref[:40] and len(ref) > 200 else 'no'}")
    return news[:4000], ref[:2500]


def ask_deepseek(env, prompt):
    body = {"model": "deepseek-v4-pro", "temperature": 0.2,   # 2026-09-26: "deepseek-chat" now silently maps to Flash; trade research gets Pro
            "messages": [{"role": "user", "content": prompt}],
            "response_format": {"type": "json_object"}}
    req = urllib.request.Request("https://api.deepseek.com/chat/completions",
                                 data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {env['DEEPSEEK_API_KEY']}"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["choices"][0]["message"]["content"]


def ask_codex(env, prompt):
    out = os.path.join(os.environ.get("TEMP", ROOT), "proposer-codex-last.txt")
    subprocess.run(["codex", "exec", "-s", "read-only", "--skip-git-repo-check", "-C", ROOT,
                    "-o", out, "-"], input=prompt, text=True, encoding="utf-8",
                   capture_output=True, timeout=600)
    with open(out, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def ask_qwen(env, prompt):
    # think=False: with thinking on, the 4b model spends its whole output budget thinking and
    # returns empty content on a long prompt. num_ctx raised so headlines + rules fit.
    body = {"model": "qwen3.5:4b", "stream": False, "format": "json", "think": False,
            "options": {"num_ctx": 8192, "num_predict": 700, "temperature": 0.2},
            "messages": [{"role": "user", "content": prompt}]}
    req = urllib.request.Request(f"{OLLAMA}/api/chat", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)["message"]["content"]


BACKENDS = {"deepseek": ask_deepseek, "codex": ask_codex, "qwen": ask_qwen}


def parse_estimate(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
        if d.get("probability") is None:
            # Codex (OpenAI policy) returns null and declines on election questions. Not a bug
            # here - a box on that researcher. DeepSeek and Grok/Scout do not have it.
            return {"declined": str(d.get("drivers", ""))[:200]}
        p = float(d["probability"])
        conf = str(d.get("confidence", "low")).lower()
        if conf not in SIZE_BY_CONFIDENCE:
            conf = "low"
        return {"p": min(max(p, 0.0), 1.0), "confidence": conf,
                "drivers": str(d.get("drivers", ""))[:800],
                "kill": str(d.get("kill_triggers", ""))[:400]}
    except Exception:
        return None


def record_estimate(c, est, backend, decision):
    new = not os.path.exists(ESTIMATES)
    with open(ESTIMATES, "a", encoding="utf-8", newline="\n") as fh:
        if new:
            fh.write("# Scout estimates - calibration record\n\n"
                     "One line per estimate, whether or not it became a proposal. When a market resolves,\n"
                     "come back and score it. Format: date | slug | researcher | p | confidence | ask at the time"
                     " | decision | ends\n\n")
        fh.write(f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')}Z | {c['slug']} | {est.get('method','direct')}/{backend} | "
                 f"p={est['p']:.2f} | {est['confidence']} | ask={c['ask']:.2f} | {decision} | ends {str(c.get('endDate'))[:10]}\n")


# ---- edge + row -------------------------------------------------------------------------

def decide(c, est):
    p, bid, ask, spread = est["p"], c["bid"], c["ask"], c["spread"]
    yes_edge = p - ask
    no_edge = bid - p                      # buying NO costs (1 - bid); fair for NO is (1 - p)
    if yes_edge >= no_edge:
        side, edge, entry = "yes", yes_edge, ask
    else:
        side, edge, entry = "no", no_edge, round(1 - bid, 4)
    floor = SPLIT_MIN_EDGE if est.get("method") == "split" else MIN_EDGE
    if edge <= spread or edge < floor:
        return None, f"pass: best edge {edge:+.3f} ({side}) vs spread {spread:.3f}, floor {floor:.2f}"
    if est.get("method") == "split":
        # The assembled number knows nothing about the market's consensus, so on any market far
        # from its prior it "sees" edge in the fade direction - that is the PolyBench losing
        # pattern, not information. Only trade WITH the evidence, and only when there is some.
        net = est.get("net", 0)
        if abs(net) < 3:
            return None, f"pass: evidence too thin (net {net:+d}) to act on, even with edge {edge:+.3f}"
        if (side == "yes") != (net > 0):
            return None, f"pass: edge {edge:+.3f} points {side} but the evidence points the other way (net {net:+d})"
    return {"side": side, "edge": round(edge, 4), "entry_price": entry,
            "size_usd": SIZE_BY_CONFIDENCE[est["confidence"]]}, f"PROPOSE {side} edge {edge:+.3f}"


def run(a):
    env = secrets()
    for k in ("SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"):
        if not env.get(k):
            raise SystemExit(f"{k} missing from {SECRETS}")
    backend = a.researcher or ("deepseek" if env.get("DEEPSEEK_API_KEY") else "codex")
    if backend == "deepseek" and not env.get("DEEPSEEK_API_KEY"):
        raise SystemExit("DEEPSEEK_API_KEY is empty in keys.env - paste it after the = sign, or use --researcher codex")
    log(f"=== proposer start | method={a.method} | researcher={backend} | {'COMMIT' if a.commit else 'DRY RUN'} | max={a.max} ===")

    since = (datetime.now(timezone.utc) - timedelta(days=RECENT_DAYS)).strftime("%Y-%m-%dT%H:%M:%SZ")
    recent = sb(env, "GET", f"trade_proposals?select=slug&proposed_at=gte.{since}")
    open_rows = sb(env, "GET", "trade_proposals?select=slug&placed=eq.false&verdict=in.(pending,approved)")
    skip = {r["slug"] for r in recent + open_rows}
    # A researcher that refused a question (Codex on elections) will refuse it again next run;
    # do not burn a call on it for RECENT_DAYS. DeepSeek/Grok can still take it by hand.
    declined = {}
    if os.path.exists(DECLINED):
        try:
            declined = json.load(open(DECLINED, encoding="utf-8"))
        except (OSError, ValueError):
            declined = {}
    cutoff = time.time() - RECENT_DAYS * 86400
    if a.method == "direct":   # the split never asks for a forecast, so a refusal does not apply to it
        skip |= {slug for slug, meta in declined.items() if meta.get("by") == backend and meta.get("at", 0) > cutoff}
    markets = fetch_open_markets()
    picked, total = screen(markets, skip)
    events = fetch_event_index()
    n_soon = sum(1 for c in picked if c.get("horizon") == "soon")
    log(f"open markets {len(markets)} | pass screen {total} | skipping {len(skip)} recent | researching up to {a.max} "
        f"(soon-settling available: {n_soon}, long: {len(picked) - n_soon})")

    mcp = Mcp()
    today = mcp.call("today", {})
    proposed = 0
    # Leave Bridge a list of what we are researching, so its next hourly wake can write
    # state/sentiment/<slug>.json (what X is saying). Next proposer run picks those up.
    try:
        reqs = {}
        if os.path.exists(SENTI_REQ):
            reqs = json.load(open(SENTI_REQ, encoding="utf-8"))
        cutoff = time.time() - 2 * 86400
        reqs = {k: v for k, v in reqs.items() if v.get("requested_at", 0) > cutoff}
        for c in picked[: a.max]:
            if not sentiment_hint(c["slug"]):
                reqs[c["slug"]] = {"question": c["question"], "outcome": c["outcome"], "category": c["category"],
                                   "ends": c.get("endDate"), "requested_at": time.time(),
                                   "write_to": f"state/sentiment/{c['slug']}.json"}
        with open(SENTI_REQ, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(reqs, fh, indent=1)
    except OSError as e:
        log(f"could not write sentiment requests: {e}")
    for c in picked[: a.max]:
        news, ref = gather(mcp, c)
        c["n_outcomes"] = events.get(c["slug"], {}).get("n_outcomes")
        t0 = time.time()
        est = None
        if a.method in ("split", "both"):
            prompt = FACTS_PROMPT.format(today=today[:200], question=c["question"], outcome=c["outcome"],
                                         description=c["description"] or "(none given)", news=news, reference=ref)
            try:
                raw = BACKENDS[backend](env, prompt)
            except Exception as e:
                log(f"{c['slug']}: researcher failed ({e})")
                continue
            facts = parse_facts(raw)
            if not facts:
                log(f"{c['slug']}: could not parse facts from researcher: {raw[:160]!r}")
                if a.method == "split":
                    continue
            else:
                est = assemble(c, facts, today[:10], sentiment_hint(c["slug"]))
                est["method"] = "split"
                log(f"  {c['slug']}: {est['why']}")
                if a.method == "both":
                    # 'both' = the split is the strict, rare signal; if it passes, ALSO ask the
                    # direct method so the queue is not empty and the two methods can be scored
                    # against each other at resolution (state/scout-estimates.md keeps both).
                    row_s, why_s = decide(c, est)
                    if row_s:
                        pass                      # split found something - use it
                    else:
                        log(f"  {c['slug']}: split -> {why_s}; trying direct")
                        record_estimate(c, est, backend, "pass")
                        est = None
        if est is None and a.method in ("direct", "both"):
            prompt = PROMPT.format(today=today[:200], question=c["question"], title=c["title"] or c["outcome"], outcome=c["outcome"],
                                   description=c["description"] or "(none given)", news=news, reference=ref)
            try:
                raw = BACKENDS[backend](env, prompt)
            except Exception as e:
                log(f"{c['slug']}: researcher failed ({e})")
                continue
            est = parse_estimate(raw)
            if est and "declined" not in est:
                est["method"] = "direct"
                if a.method == "both":
                    est["confidence"] = "low"     # the direct number is the weaker signal here: smallest size
        if not est:
            log(f"{c['slug']}: could not parse estimate from researcher: {raw[:160]!r}")
            continue
        if "declined" in est:
            log(f"{c['slug']} [{c['category']}]: {backend} DECLINED to estimate - {est['declined'][:120]}")
            declined[c["slug"]] = {"by": backend, "at": time.time(), "why": est["declined"][:160]}
            with open(DECLINED, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(declined, fh, indent=1)
            continue
        row, why = decide(c, est)
        log(f"{c['slug']} [{c['category']}] p={est['p']:.2f} {est['confidence']} book {c['bid']:.2f}/{c['ask']:.2f} -> {why} ({time.time()-t0:.0f}s)")
        record_estimate(c, est, backend, why.split(":")[0].split(" ")[0])
        if not row:
            continue
        payload = {
            "slug": c["slug"], "question": f"{c['question']} — {c['outcome']}" if c["outcome"] != c["question"] else c["question"],
            "side": row["side"], "entry_price": row["entry_price"], "bid": c["bid"], "ask": c["ask"],
            "spread": c["spread"], "scout_probability": est["p"], "scout_confidence": est["confidence"],
            "edge": row["edge"], "size_usd": row["size_usd"], "open_interest": None,
            "rationale": (f"[split: {backend} facts, script math] {est['why']} || {est['drivers']}" if est.get("method") == "split"
                          else f"[{backend}, price-blind] {est['drivers']}"),
            "kill_criteria": est["kill"], "verdict": "pending",
            "proposed_by": f"proposer-script/{est.get('method','direct')}/{backend}",
            "outcome": c["outcome"],
            "no_price": round(1 - c["bid"], 4),
            "side_open": side_open(c, events.get(c["slug"], {})),
            "vantages": backend,
            "settles_at": c.get("settles"),
            "evidence": c.get("evidence"),
            **{k: v for k, v in events.get(c["slug"], {}).items() if k != "n_outcomes"},   # n_outcomes is for the prior, not a column
        }
        if "category" not in payload or not payload.get("category"):
            payload["category"] = c["category"]
        if a.commit:
            r = sb(env, "POST", "trade_proposals", payload)
            log(f"  -> inserted proposal #{r[0]['id'] if r else '?'}: {row['side']} {c['slug']} @ {row['entry_price']:.2f} ${row['size_usd']:.2f}")
        else:
            log(f"  -> DRY RUN would insert: {json.dumps(payload)[:300]}")
        proposed += 1
    log(f"=== done: {proposed} proposal(s) {'inserted' if a.commit else 'would be inserted'} ===")


def main():
    ap = argparse.ArgumentParser(description="Screen markets, research price-blind, propose when edge beats spread.")
    ap.add_argument("--commit", action="store_true", help="insert rows (default is dry run)")
    ap.add_argument("--max", type=int, default=6, help="candidates to research per run")
    ap.add_argument("--researcher", choices=sorted(BACKENDS), help="deepseek | codex | qwen")
    ap.add_argument("--method", choices=["split", "direct", "both"], default="both",
                    help="split = facts from a model, number from arithmetic. direct = ask the model for a probability. "
                         "both (default) = split first; if it passes, direct at the smallest size, so the queue stays fed and the two can be scored.")
    try:
        run(ap.parse_args())
    except SystemExit:
        raise
    except Exception:
        import traceback
        log("CRASH: " + traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
