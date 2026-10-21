#!/usr/bin/env python3
"""
publish-crew.py - puts the whole AI system on heartbeatobservatory.com/live-systems/crew/ (Jaron, 2026-09-25: "everything that
people would want to see about our system. I don't want anything kept out." Secrets and keys excepted).

Every run it gathers, from the files that are actually in force: each bot's real instructions (word for word), its schedule,
its recent activity, its money (from desk_trades), the MSI's scheduled jobs, health, and the shared bot conversation log - and
writes one row to Supabase public.crew_snapshot (public read). No AI, no cost.
The named crew below is the list with its own activity source. Any other bot is added on its own when it has
state/crew/<id>.md or a grok-bot/<id> trade tag, so a new bot needs no code change. Instructions come from that
file, or from its BUILD-SHEETS section when the sheet is newer. Money is that bot's own tag.
A bot may overwrite state/crew/<id>.md (updated, what changed, then the instructions). When that file is newer than the
build sheet or script it would replace, the page uses the file. Runs every 5 minutes (task "Crew Publish", or
tools/crew-publish-loop.ps1 if that task cannot be created). The hourly MSI Health task also runs it.
Anything that looks like a key is masked before upload.
"""
import json, os, re, subprocess, sys
from datetime import datetime, timezone
from decimal import Decimal
from fractions import Fraction

ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import executor as X  # noqa: E402

WATCH = r"C:\Users\lilli\Projects\watch"
CR = os.path.join(ROOT, "projects", "control-room")

KEYLIKE = re.compile(r"(sk-[A-Za-z0-9_\-]{16,}|sb_secret_[A-Za-z0-9_\-]+|eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}|"
                     r"(?i:(api[_-]?key|secret|token|password)\s*[=:]\s*)[^\s\"']{12,})")


PRIV_TAG = "[Personal chat/Secret/keys]"
EMAIL_OK = {"<email>", "<email>"}
EMAIL = re.compile(r"(?<![\w.%+-])[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")
STREET = re.compile(r"(?<![\w.$#/:-])\d{1,6}\s+(?:[NSEWnsew]\.?\s+)?(?:[A-Z][A-Za-z'-]*\.?\s+){1,3}"
                    r"(?i:Dr|Drive|St|Street|Ave|Avenue|Rd|Road|Ln|Lane|Ct|Court|Blvd|Boulevard|Way|Pl|Place|Cir|Circle|Pkwy|Parkway)\b\.?")
STATES = ("AL|AK|AZ|AR|CA|CO|CT|DE|DC|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|"
          "PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY")
ZIP = re.compile(r"(?:(?<=\b(?:" + STATES + r")\s)|(?<=\b(?:" + STATES + r"),\s)|(?<=[A-Za-z],\s))\d{5}(?:-\d{4})?(?![\w.])(?!\s*[A-Za-z(])"
                 r"|(?:(?<=\b(?:" + STATES + r")\s)|(?<=\b(?:" + STATES + r"),\s))\d{5}(?:-\d{4})?(?![\w.])")
PHONE = re.compile(r"(?<![\w$.#/:-])(?:\+?1[-. ]?)?(?:\(\d{3}\)\s?|\d{3}[-.\s])\d{3}[-.\s]\d{4}(?![\w.])")
CARD = re.compile(r"(?<![\w.$#/:-])\d{4}(?:[ -]\d{4}){2}[ -]\d{1,4}(?![\w.])|(?<![\w.$#/:-])\d{4}[ -]\d{6}[ -]\d{5}(?![\w.])")
LONGNUM = re.compile(r"(?<![\w.$/:-])\d{8,}(?![\w.])")


def privacy(text):
    """Personal bits never go public: emails, street addresses, ZIPs, phones, card and ID/confirmation numbers."""
    text = EMAIL.sub(lambda m: m.group(0) if m.group(0).lower() in EMAIL_OK else PRIV_TAG, text)
    text = STREET.sub(PRIV_TAG, text)
    text = CARD.sub(PRIV_TAG, text)
    text = PHONE.sub(PRIV_TAG, text)
    text = ZIP.sub(PRIV_TAG, text)
    text = LONGNUM.sub(PRIV_TAG, text)
    return text


def mask(text):
    return privacy(KEYLIKE.sub("[hidden key]", text or ""))


def mask_all(obj):
    """Run mask() over every string in the published snapshot (crew pages, build sheets, chat, activity, tasks, health)."""
    if isinstance(obj, str):
        return mask(obj)
    if isinstance(obj, list):
        return [mask_all(v) for v in obj]
    if isinstance(obj, dict):
        return {k: mask_all(v) for k, v in obj.items()}
    return obj


def read(path, default=""):
    try:
        return open(path, encoding="utf-8").read()
    except OSError:
        return default


def tail(path, n):
    return [mask(l.rstrip()) for l in read(path).splitlines() if l.strip()][-n:]


def sheet_sections():
    """BUILD-SHEETS.md: section name -> instructions, routine, job, schedule."""
    text = read(os.path.join(CR, "BUILD-SHEETS.md"))
    out = {}
    for m in re.finditer(r"^# \d\. ([^\n]+)", text, re.M):
        heading = m.group(1).strip()
        name_m = re.match(r"([A-Z0-9 ]+?)(?: \(|\s—|\s-|$)", heading)
        if not name_m:
            continue
        start = m.end()
        nxt = re.search(r"^# \d\. ", text[start:], re.M)
        body = text[start: start + nxt.start()] if nxt else text[start:]
        job_m = re.search(r"(?m)^\*\*Job:\*\*\s*(.+)$", body)
        sch_m = re.search(r"(?m)^\*\*Schedule:\*\*\s*(.+)$", body)
        name_line = re.search(r"(?m)^\*\*Name:\*\*\s*(.+)$", body)
        out[name_m.group(1).strip()] = {
            "blocks": re.findall(r"```\n(.*?)\n```", body, re.S),
            "job": job_m.group(1).strip() if job_m else "",
            "schedule": sch_m.group(1).strip() if sch_m else "",
            "name": name_line.group(1).strip() if name_line else "",
            "skip": bool(re.search(r"(?i)\bdelete\b", heading)),
        }
    return out


def sheet_blocks():
    """Section -> [main instructions, routine instruction] (code blocks in order)."""
    return {k: v["blocks"] for k, v in sheet_sections().items()}


def captured(name):
    """A word-for-word capture in control-room/instructions/: the text between the first two '---' lines."""
    text = read(os.path.join(CR, "instructions", name))
    m = re.search(r"\n---\n(.*?)\n---", text, re.S)
    return m.group(1).strip() if m else ""


def py_prompt(path, name):
    m = re.search(name + r' = """(.*?)"""', read(path), re.S)
    return m.group(1).strip() if m else ""


CREW = os.path.join(ROOT, "state", "crew")


def file_mtime(path):
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0


def parse_crew(path):
    """state/crew/<id>.md written by the bot: optional header lines, then the instructions.
    Header keys: updated, changed, name, job, schedule, ai, actor, also.
    A '## Routine' heading, if present, is the routine. '## Instructions' is optional."""
    text = read(path)
    if not text.strip():
        return None
    lines = text.splitlines()
    i = 0
    meta = {}
    while i < len(lines) and not lines[i].strip():
        i += 1
    while i < len(lines):
        m = re.match(r"(?i)^(updated|changed|name|job|schedule|ai|actor|also):\s*(.*)$", lines[i])
        if not m:
            break
        meta[m.group(1).lower()] = m.group(2).strip()
        i += 1
    body = "\n".join(lines[i:]).strip()
    instructions, routine = body, None
    if re.search(r"(?m)^## (Instructions|Routine)\s*$", body):
        instructions, routine = "", None
        pre, *parts = re.split(r"(?m)^## ", body)
        if pre.strip():
            instructions = pre.strip()
        for part in parts:
            head, _, rest = part.partition("\n")
            head, rest = head.strip().lower(), rest.strip()
            if head == "instructions":
                instructions = rest
            elif head == "routine":
                routine = rest
    if not instructions.strip():
        return None
    meta.update({"instructions": instructions, "routine": routine,
                 "updated": meta.get("updated", ""), "changed": meta.get("changed", "")})
    return meta


def apply_crew(bot):
    """Prefer state/crew/<id>.md over the build sheet or script when the bot's file is newer."""
    parsed = parse_crew(os.path.join(CREW, bot["id"] + ".md"))
    if not parsed:
        return
    newest_src = max((file_mtime(p) for p in (bot.get("_src") or [])), default=0.0)
    if file_mtime(os.path.join(CREW, bot["id"] + ".md")) <= newest_src:
        return
    bot["instructions"] = parsed["instructions"]
    if parsed.get("routine"):
        bot["routine"] = [parsed["routine"]] if isinstance(bot.get("routine"), list) else parsed["routine"]
    if parsed.get("changed"):
        bot["instructions_changed"] = parsed["changed"]
    if parsed.get("updated"):
        bot["instructions_updated"] = parsed["updated"]


def drop_retired_pause(line):
    """Public session notes must not repeat the self-pause Jaron removed on 10/2.
    The log file itself is left as the bot wrote it."""
    line = line.replace("tennis ban + streak pause (Jacquet/Timofeeva)", "tennis off")
    line = line.replace("tennis ban + streak pause Jacquet/Timofeeva", "tennis off")
    line = re.sub(r"\bstreak pause\b", "no self-pause", line)
    line = re.sub(r";\s*pause(?=\))", "", line)
    line = re.sub(r"\s*\(pause\)", "", line)
    line = re.sub(r"[ \t]{2,}", " ", line)
    return line.strip()


def bot_id_of(name):
    return re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")


def title_name(bid):
    return " ".join(p.capitalize() for p in bid.split("-") if p)


def one_line(text, n=180):
    text = re.sub(r"\s+", " ", text or "").strip()
    if not text:
        return ""
    m = re.match(r"(.{20,}?\.)(?:\s|$)", text)
    return (m.group(1) if m else text)[:n].rstrip()


def activity_for(bid, name):
    """The bot's own log if it has one, otherwise chat lines that name it."""
    own = tail(os.path.join(ROOT, "state", bid + ".md"), 6)
    if own:
        return own
    keys = [k for k in (bid, (name or "").lower(), "grok-bot/" + bid) if len(k) >= 4]
    hits = []
    for line in read(os.path.join(ROOT, "state", "bot-chat.md")).splitlines():
        low = line.lower()
        if any(k in low for k in keys):
            hits.append(mask(line.rstrip()))
    return hits[-6:]


def empty_ledger():
    return {"fills": 0, "spent": 0.0, "settled": 0, "pnl": 0.0, "wins": 0, "losses": 0, "last": ""}


def claimed_actors(bots):
    taken = set()
    prefixes = []
    for b in bots:
        if b.get("actor"):
            taken.add(b["actor"])
            if b["actor"] == "auto:grok-bot/live-wire":
                taken.add(b["actor"] + "#v1")
        if b.get("actor_prefix"):
            prefixes.append(b["actor_prefix"])
    return taken, prefixes


def actor_free(actor, taken, prefixes):
    if not actor or actor in taken or any(actor.startswith(p) for p in prefixes):
        return ""
    return actor


def section_for(bid, sections):
    meta = sections.get(bid.replace("-", " ").upper()) or {}
    if meta.get("skip"):
        return {}
    blocks = meta.get("blocks") or []
    return {
        "name": meta.get("name") or "",
        "job": meta.get("job") or "",
        "schedule": meta.get("schedule") or "",
        "instructions": blocks[0] if blocks else "",
        "routine": blocks[1] if len(blocks) > 1 else "",
    }


def material_for(bid, sections):
    """Crew file when it is newer than the build sheet; otherwise the sheet. Gaps fill from the other."""
    sheet = section_for(bid, sections)
    path = os.path.join(CREW, bid + ".md")
    parsed = parse_crew(path)
    crew_newer = bool(parsed) and file_mtime(path) > file_mtime(os.path.join(CR, "BUILD-SHEETS.md"))
    src = parsed if crew_newer else None

    def pick(key):
        if src and src.get(key):
            return src[key]
        return sheet.get(key) or (parsed or {}).get(key) or ""

    instructions = pick("instructions")
    routine = pick("routine") or ""
    return {
        "name": pick("name") or title_name(bid),
        "job": pick("job") or one_line(instructions) or ("Trades on Polymarket US under grok-bot/%s." % bid),
        "schedule": pick("schedule") or "see its instructions",
        "ai": pick("ai"),
        "also": pick("also"),
        "actor": (src or {}).get("actor") or "",
        "instructions": instructions,
        "routine": routine,
        "updated": ((parsed or {}).get("updated") or "") if crew_newer else "",
        "changed": ((parsed or {}).get("changed") or "") if crew_newer else "",
        "crew_newer": crew_newer,
        "parsed": parsed,
    }


def infer_actor(bid, text, hinted=""):
    if hinted:
        return hinted if hinted.startswith("auto:") else "auto:" + hinted
    tags = re.findall(r"grok-bot/([a-z0-9][a-z0-9\-]*)", text or "")
    if bid in tags:
        return "auto:grok-bot/" + bid
    if tags:
        return "auto:grok-bot/" + tags[0]
    return ""


def make_discovered(bid, sections, actor):
    fields = material_for(bid, sections)
    actor = actor_free(actor or infer_actor(bid, fields["instructions"], fields["actor"]), *claimed_holder)
    if not fields["instructions"].strip() and not actor:
        return None
    bot = {
        "id": bid,
        "name": fields["name"],
        "ai": fields["ai"] or ("Grok (xAI) - Grok Bot" if (actor or "").startswith("auto:grok-bot/") else "AI crew"),
        "job": fields["job"],
        "schedule": fields["schedule"],
        "instructions": fields["instructions"],
        "routine": [fields["routine"]] if fields["routine"] else [],
        "activity": activity_for(bid, fields["name"]),
        "money": bool(actor),
    }
    if fields["also"]:
        bot["also"] = fields["also"]
    if actor:
        bot["actor"] = actor
    if fields["crew_newer"] and fields["changed"]:
        bot["instructions_changed"] = fields["changed"]
    if fields["crew_newer"] and fields["updated"]:
        bot["instructions_updated"] = fields["updated"]
    return bot


# filled in by discover() so make_discovered can see actors already taken
claimed_holder = (set(), [])


def discover(bots, retired, per):
    """Add any bot that has state/crew/<id>.md or a grok-bot/<id> trade, and is not already on the crew."""
    global claimed_holder
    known = {b["id"] for b in bots + retired}
    taken, prefixes = claimed_actors(bots + retired)
    claimed_holder = (taken, prefixes)
    sections = sheet_sections()
    found = []

    def add(bid, actor):
        if not bid or bid in known:
            return
        bot = make_discovered(bid, sections, actor)
        if not bot:
            return
        if bot.get("actor"):
            taken.add(bot["actor"])
        found.append(bot)
        known.add(bid)

    if os.path.isdir(CREW):
        for fn in sorted(os.listdir(CREW)):
            if not fn.endswith(".md"):
                continue
            bid = fn[:-3].lower()
            if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", bid):
                continue
            add(bid, "")

    for actor in sorted(per):
        m = re.fullmatch(r"auto:grok-bot/([a-z0-9][a-z0-9\-]*)", actor)
        if not m or not actor_free(actor, taken, prefixes):
            continue
        bid = m.group(1)
        if bid in known:
            for b in list(bots) + found:
                if b.get("id") == bid and not b.get("actor"):
                    b["actor"] = actor
                    b["money"] = True
                    taken.add(actor)
            continue
        add(bid, actor)

    idx = 0
    for i, b in enumerate(bots):
        if b.get("money") or b.get("actor") or b.get("actor_prefix"):
            idx = i + 1
    for bot in found:
        bots.insert(idx, bot)
        idx += 1


def attach_money(bots, retired, per):
    for b in bots:
        if b.get("actor"):
            hit = per.get(b["actor"])
            if hit:
                b["ledger"] = hit
            elif b.get("money"):
                b["ledger"] = empty_ledger()
        elif b.get("actor_prefix"):
            agg = {"fills": 0, "spent": 0.0, "settled": 0, "pnl": 0.0, "wins": 0, "losses": 0, "last": ""}
            for a, p in per.items():
                if a.startswith(b["actor_prefix"]):
                    for k in ("fills", "settled", "wins", "losses"):
                        agg[k] += p[k]
                    agg["spent"] = round(agg["spent"] + p["spent"], 2)
                    agg["pnl"] = round(agg["pnl"] + p["pnl"], 2)
                    agg["last"] = max(agg["last"], p["last"])
            b["ledger"] = agg
    for r in retired:   # the retired Live Wire keeps its own record (its tag's trades before the handover)
        if r.get("until"):
            r["ledger"] = per.get(r["actor"] + "#v1")


def finalize(b):
    b.pop("_src", None)
    b["instructions"] = mask(b.get("instructions", ""))
    if b.get("instructions_changed"):
        b["instructions_changed"] = mask(b["instructions_changed"])
    if isinstance(b.get("routine"), list):
        b["routine"] = [mask(x) for x in b["routine"] if x]
    else:
        b["routine"] = mask(b.get("routine", ""))


def tasks():
    ps = ("Get-ScheduledTask | Where-Object { $_.TaskPath -eq '\\' } | ForEach-Object { $i = $_ | Get-ScheduledTaskInfo; "
          "[pscustomobject]@{name=$_.TaskName; state=[string]$_.State; last=[string]$i.LastRunTime; next=[string]$i.NextRunTime; "
          "result=$i.LastTaskResult; about=$_.Description} } | ConvertTo-Json")
    try:
        d = json.loads(subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True, timeout=90).stdout)
    except Exception:
        return []
    keep = ("Watch ", "Heartbeat News", "Trade ", "Live Board", "MSI Health", "DB Size", "Usage Snapshot", "AI-Shared Mirror",
            "Polymarket MCP", "Grok Machine MCP", "Ollama", "Scout Scorer", "Revenue Desk", "AgentWorkbench")
    return [{k: (mask(v) if isinstance(v, str) else v) for k, v in t.items()} for t in (d if isinstance(d, list) else [d])
            if t["name"].startswith(keep)]


# Darios Twin took over from the retired Live Wire at this moment and reuses its tag: split that tag's trades here
CUT = "2026-09-25T22:58:00Z"
NOTE = ("Darios Twin replaced the retired Live Wire bot at 6:58 PM on Sept 25, 2026 - two different bots. Darios Twin reuses "
        "Live Wire's trade tag (grok-bot/live-wire) and log file (live-wire.md), so those still say live-wire. "
        "Trades before that moment are Live Wire's; trades after are Darios Twin's.")


def era(r):   # the tag's owner at the time of the row
    a = r.get("actor") or "?"
    if a == "auto:grok-bot/live-wire" and (r.get("at") or "") < CUT: return a + "#v1"
    return a


PMV = os.path.join(ROOT, "runtime", "polymarket-us-agent-venv", "Scripts", "python.exe")
PMH = os.path.join(ROOT, "state", "polymarket-activities-all.json")


def pm_history():
    """Polymarket's own full history (read-only), refreshed at most hourly. Returns the activity list or None."""
    import time
    try:
        if not os.path.exists(PMH) or time.time() - os.path.getmtime(PMH) > 3300:
            subprocess.run([PMV, os.path.join(ROOT, "tools", "pm-history-all.py")], capture_output=True, text=True, timeout=240)
        return json.load(open(PMH, encoding="utf-8"))
    except Exception as e:
        print("pm history unavailable:", type(e).__name__)
        return None


def pm_realized_ai(acts):
    """Compatibility name: AI net cash by market, including fees and fill-only exits."""
    return {s: v["ai"] for s, v in pm_cash_ledger(acts)["market_results"].items() if "ai" in v}


def pm_account_story(acts, ai_by_slug=None):
    """Account and owner cash results; the legacy ai_by_slug estimate is no longer used."""
    return pm_cash_ledger(acts)


def pm_cash_ledger(acts):
    """Replay actual USD movements, independently of realized-P&L snapshots or bot estimates."""
    zero = Decimal(0)

    def usd(value):
        if not value or value.get("currency") != "USD":
            raise ValueError("Missing/non-USD cash value")
        return Decimal(value["value"])

    def event_time(x):
        if x.get("trade"):
            t = x["trade"]
            e = t["aggressorExecution"] if t["isAggressor"] else t["passiveExecution"]
            return e["transactTime"]
        if x.get("positionResolution"):
            return x["positionResolution"]["updateTime"]
        return x["accountBalanceChange"]["createTime"]

    def time_key(x):
        # Preserve nanoseconds, including when an ISO timestamp has no fractional part.
        at = event_time(x).removesuffix("Z")
        seconds, _, fraction = at.partition(".")
        return seconds, fraction.ljust(9, "0")

    positions, pools, results, meta = {}, {}, {}, {}
    owner_fees = {"ai": zero, "hand": zero}
    funding = dict.fromkeys(("dep", "wd", "bonus", "transfer"), zero)
    cash = charges = rebates = zero
    seen, events = set(), []
    for x in sorted(acts, key=time_key):
        at, fee, allocations = event_time(x), zero, {}
        slug, tx = "", ""
        if x.get("trade"):
            t = x["trade"]
            slug, rid, kind = t["marketSlug"], t["id"], "fill"
            e = t["aggressorExecution"] if t["isAggressor"] else t["passiveExecution"]
            order = e["order"]
            owners = {"MANUAL_ORDER_INDICATOR_AUTOMATIC": "ai", "MANUAL_ORDER_INDICATOR_MANUAL": "hand"}
            if order.get("manualOrderIndicator") not in owners:
                raise ValueError("Unknown fill owner: " + rid)
            owner = owners[order["manualOrderIndicator"]]
            # Jaron 10/18: "My bets are Bitcoin and table tennis. Used to do regular tennis. I've never done any football."
            # Polymarket flags some BOT orders (placed through the MSI's trading service) as MANUAL - e.g. the 10/3 India
            # cricket and the Sep-Oct college football wins. So a MANUAL fill counts as Jaron's only in his own markets.
            if owner == "hand" and not slug.startswith(JARON_MARKETS):
                owner = "ai"
            # Tennis was traded by BOTH (Jaron 10/18: "BOTH of us did tennis. Only I did table tennis."): the desk log says whose
            # order it was (jaron-manual Sep 11-18, Live Wire/Darios Sep 18-Oct 2); unlogged orders fall back to the date.
            elif owner == "hand" and slug.startswith(TENNIS):
                who = tennis_order_owner().get(order.get("id"))
                if who:
                    owner = "hand" if who.startswith("jaron") else "ai"
                elif (order.get("createTime") or "") >= "2026-09-19":
                    owner = "ai"
            q = Decimal(e.get("lastShares") or t["qtyDecimal"])
            if order["side"] not in ("ORDER_SIDE_BUY", "ORDER_SIDE_SELL") or q <= zero:
                raise ValueError("Invalid fill side/quantity: " + rid)
            dq = q if order["side"] == "ORDER_SIDE_BUY" else -q
            old = positions.get(slug, zero)
            new = old + dq
            fee = usd(e["commissionNotionalCollected"])
            # Signed YES coordinates: lock/release SHORT collateral, even across zero.
            delta = -dq * usd(e["lastPx"]) - max(-new, zero) + max(-old, zero) - fee
            allocations[owner] = delta  # Every fill's cash, including its fee, belongs to its actor.
            owner_fees[owner] += fee
            charges += max(fee, zero)
            rebates += max(-fee, zero)
            pool = pools.setdefault(slug, {"ai": Fraction(0), "hand": Fraction(0)})
            # Mixed-market convention: closing fills consume remaining shares proportionally
            # from both owners. Only the excess of a crossing fill opens shares for its actor.
            # Settlement pays the resulting remaining-share pool, never gross traded volume.
            if old * dq < zero:
                closing = min(abs(old), q)
                remaining = Fraction(abs(old) - closing) / Fraction(abs(old))
                pool["ai"] *= remaining
                pool["hand"] *= remaining
                opening = q - closing
            else:
                opening = q
            pool[owner] += Fraction(opening)
            positions[slug] = new
            title = (t.get("market") or {}).get("question") or (order.get("marketMetadata") or {}).get("title") or slug
        elif x.get("positionResolution"):
            r = x["positionResolution"]
            slug, kind = r["marketSlug"], "payout"
            rid = slug + "@" + at
            before = r["beforePosition"]
            if positions.get(slug, zero) != Decimal(before["netPositionDecimal"]):
                raise ValueError("Incomplete position history: " + slug)
            delta = usd(before["cashValue"])  # Includes neutral payouts; realized is not cash.
            pool = pools.get(slug, {"ai": Fraction(0), "hand": Fraction(0)})
            total = sum(pool.values())
            if total != Fraction(abs(positions.get(slug, zero))):
                raise ValueError("Owner shares do not match position: " + slug)
            if not total and delta:
                raise ValueError("Payout without owned shares: " + slug)
            if total:
                ratio = pool["ai"] / total
                # Round only the ownership allocation to 1e-8 USD. The hand complement
                # preserves the actual payout exactly, including repeating pool fractions.
                ai_cash = delta if not pool["hand"] else zero if not pool["ai"] else (
                    delta * Decimal(ratio.numerator) / Decimal(ratio.denominator)).quantize(Decimal("0.00000001"))
                if pool["ai"]:
                    allocations["ai"] = ai_cash
                if pool["hand"]:
                    allocations["hand"] = delta - ai_cash
            positions[slug] = zero
            pools[slug] = {"ai": Fraction(0), "hand": Fraction(0)}
            title = (r.get("market") or {}).get("question") or (before.get("marketMetadata") or {}).get("title") or slug
        elif x.get("accountBalanceChange"):
            b = x["accountBalanceChange"]
            rid = tx = b["transactionId"]
            kind = {"ACTIVITY_TYPE_ACCOUNT_DEPOSIT": "dep", "ACTIVITY_TYPE_ACCOUNT_WITHDRAWAL": "wd",
                    "ACTIVITY_TYPE_REFERRAL_BONUS": "bonus", "ACTIVITY_TYPE_TRANSFER": "transfer"}.get(x["type"])
            if not kind:
                raise ValueError("Unknown funding type: " + x["type"])
            amount, status = usd(b["amount"]), b["status"]
            pending = status == "ACCOUNT_BALANCE_CHANGE_STATUS_PENDING"
            if pending and kind == "dep":
                advances = {t["transactionId"]: usd(t["advancedAmount"]) for t in b.get("transactions", []) if t.get("advancedAmount")}
                amount = min(amount, sum(advances.values(), zero))
                if amount <= zero:
                    continue
            elif status != "ACCOUNT_BALANCE_CHANGE_STATUS_COMPLETED":
                continue
            # TRANSFER amounts in this export are signed credits; purpose is unspecified.
            delta = -amount if kind == "wd" else amount
            funding[kind] += amount
            title = {"dep": "Deposit", "wd": "Withdrawal", "bonus": "Promotion bonus", "transfer": "Transfer credit"}[kind]
            if pending:
                title += " (advanced funds; deposit pending)"
        else:
            raise ValueError("Unknown activity type")
        key = (kind, rid)
        if key in seen:
            raise ValueError("Duplicate activity; reconcile its versions: " + rid)
        seen.add(key)
        if slug:
            assert sum(allocations.values(), zero) == delta
            market = results.setdefault(slug, {})
            for owner, value in allocations.items():
                market[owner] = market.get(owner, zero) + value
            meta[slug] = (at, title)
        cash += delta
        ev = {"at": at, "k": kind, "usd": float(delta), "usd_exact": str(delta),
              "cash_balance": float(cash), "cash_balance_exact": str(cash), "title": title,
              "slug": slug, "fee_usd": float(fee), "owners": {o: float(v) for o, v in allocations.items()}}
        if tx:
            ev["tx"] = tx
        events.append(ev)

    net_funding = funding["dep"] + funding["bonus"] + funding["transfer"] - funding["wd"]
    out = {"deposits": float(funding["dep"]), "bonus": float(funding["bonus"]), "credits": float(funding["transfer"]),
           "funding_in": float(net_funding + funding["wd"]), "withdrawals": float(funding["wd"]),
           "net_funding": float(net_funding), "net_trading_cash": float(cash - net_funding), "fees_paid": float(charges - rebates),
           "fee_charges": float(charges), "maker_rebates": float(rebates), "cash_balance": float(cash),
           "cash_balance_exact": str(cash), "balance_kind": "cash", "events": events, "meta": meta,
           "market_results": {s: {o: float(v) for o, v in m.items()} for s, m in results.items()},
           "open_positions": {s: str(q) for s, q in positions.items() if q},
           "ownership_convention": "Fills to their actor; remaining shares pooled proportionally for closes and settlement.",
           "bot_allocation": "Approximate: each market's AI cash result split by absolute desk fill spend."}
    for owner in ("ai", "hand"):
        values = [m[owner] for m in results.values() if owner in m]
        closed = [m[owner] for s, m in results.items() if owner in m and not positions[s]]
        out[owner + "_result"] = float(sum(values, zero))
        out[owner + "_result_exact"] = str(sum(values, zero))
        out[owner + "_fees_paid"] = float(owner_fees[owner])
        out[owner + "_markets"] = len(values)
        out[owner + "_won"] = float(sum((v for v in closed if v > zero), zero))
        out[owner + "_lost"] = float(-sum((v for v in closed if v < zero), zero))
        out[owner + "_won_n"] = sum(v > zero for v in closed)
        out[owner + "_lost_n"] = sum(v < zero for v in closed)
    assert Decimal(out["ai_result_exact"]) + Decimal(out["hand_result_exact"]) + net_funding == cash
    return out


def apply_receipts(events):
    """Optional receipts (public.desk_receipts): a withdrawal with a receipt becomes a 'bill' event (yellow on the page).
    Match by Polymarket transaction id, else by day + amount. Only the bill name, amount and an optional link go public."""
    try:
        env = X.secrets()
        recs = X.sb(env, "GET", "desk_receipts?select=tx_id,paid_on,amount_usd,what,receipt_url&order=id.asc&limit=500") or []
    except Exception as e:
        print("receipts unavailable:", type(e).__name__)
        return 0.0
    total, used = 0.0, set()
    for ev in events:
        if ev.get("k") != "wd":
            continue
        for i, r in enumerate(recs):
            if i in used:
                continue
            amt = float(r.get("amount_usd") or 0)
            same_tx = r.get("tx_id") and r["tx_id"] == ev.get("tx")
            same_day = (not r.get("tx_id")) and r.get("paid_on") and abs(amt - abs(ev["usd"])) < 0.005 and                 abs((datetime.fromisoformat(ev["at"][:10]) - datetime.fromisoformat(str(r["paid_on"])[:10])).days) <= 1
            if same_tx or same_day:
                used.add(i)
                ev["k"] = "bill"
                ev["bill"] = mask(str(r["what"]))[:80]
                ev["bill_usd"] = round(amt, 2)
                if r.get("receipt_url") and str(r["receipt_url"]).startswith("http"):
                    ev["receipt"] = r["receipt_url"]
                total += amt
                break
    for ev in events:
        ev.pop("tx", None)
    return round(total, 2)


def apply_polymarket(per, rows):
    """Use real owner cash for the headline; per-bot splitting by desk fill spend remains approximate."""
    acts = pm_history()
    if not acts:
        return None
    story = pm_account_story(acts)
    ai = {s: v["ai"] for s, v in story["market_results"].items() if "ai" in v}
    w = {}
    for r in rows:
        if r.get("kind") == "fill" and (r.get("actor") or "").startswith("auto:") and r.get("slug") in ai:
            a = era(r)
            w.setdefault(r["slug"], {})
            w[r["slug"]][a] = w[r["slug"]].get(a, 0.0) + abs(float(r.get("cost_usd") or 0))
    for p in per.values():
        p["pnl"], p["settled"], p["wins"], p["losses"] = 0.0, 0, 0, 0
    other = 0.0
    for slug, v in ai.items():
        ws = w.get(slug)
        tot = sum(ws.values()) if ws else 0
        if not tot:
            other += v
            continue
        for a, x in ws.items():
            part = v * x / tot
            per[a]["pnl"] += part
            per[a]["settled"] += 1
            per[a]["wins" if part > 0 else "losses"] += 1 if part != 0 else 0
    for p in per.values():
        p["pnl"] = round(p["pnl"], 2)
    story.pop("meta")
    story["bills_paid"] = apply_receipts(story["events"])
    for event in story["events"]:
        event.pop("tx", None)
    global ACCOUNT_STORY
    ACCOUNT_STORY = story
    # Keep ai_settled as a compatibility alias for existing readers; source describes its cash basis.
    return {"ai_result": story["ai_result"], "ai_settled": story["ai_result"],
            "fees_paid": story["fees_paid"], "ai_fees_paid": story["ai_fees_paid"], "hand_fees_paid": story["hand_fees_paid"],
            "unattributed": round(other, 2), "markets": len(ai),
            "source": "Polymarket fill cash after fees plus owned settlement payouts; per-bot allocation approximate"}


AI_HEAD = None
ACCOUNT_STORY = None


def money(env):
    rows = X.sb_all(env, "desk_trades?select=actor,kind,cost_usd,pnl_usd,at,slug,side")
    per = {}
    for r in rows:
        a = era(r)
        p = per.setdefault(a, {"fills": 0, "spent": 0.0, "settled": 0, "pnl": 0.0, "wins": 0, "losses": 0, "last": "", "_t": set()})
        if r.get("kind") == "fill":
            # one trade = one market + side (+ hour), however many partial fills the venue split it into
            p["_t"].add((r.get("slug"), r.get("side"), (r.get("at") or "")[:13]))
            p["spent"] += float(r.get("cost_usd") or 0)
        elif r.get("kind") == "resolution":
            v = float(r.get("pnl_usd") or 0)
            p["settled"] += 1
            p["pnl"] += v
            p["wins" if v > 0 else "losses"] += 1 if v != 0 else 0
        p["last"] = max(p["last"], r.get("at") or "")
    for p in per.values():
        p["fills"] = len(p.pop("_t"))
        p["spent"], p["pnl"] = round(p["spent"], 2), round(p["pnl"], 2)
    global AI_HEAD
    AI_HEAD = apply_polymarket(per, rows)
    return per


# Markets Jaron trades by hand (his words 10/18): Bitcoin up/down, table tennis (Setka Cup), tennis (ITF, WTA, ATP).
JARON_MARKETS = ("cpc-btc", "aec-setkame", "aec-itf", "aec-wta", "aec-atp")


TENNIS = ("aec-itf", "aec-wta", "aec-atp")
_TENNIS_OWNERS = None


def tennis_order_owner():
    """order_id -> actor for every tennis row in desk_trades (read once per run)."""
    global _TENNIS_OWNERS
    if _TENNIS_OWNERS is None:
        _TENNIS_OWNERS = {}
        try:
            import urllib.request
            e = X.secrets(); k = e["SUPABASE_SERVICE_ROLE_KEY"]
            url = e["SUPABASE_URL"].rstrip("/") + "/rest/v1/desk_trades?select=order_id,actor&slug=match.%5Eaec-%28itf%7Cwta%7Catp%29&limit=5000"
            for r in json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"apikey": k, "Authorization": "Bearer " + k}), timeout=30).read()):
                if r.get("order_id"): _TENNIS_OWNERS[r["order_id"]] = r.get("actor") or ""
        except Exception:
            pass
    return _TENNIS_OWNERS


# Who is really working right now (Jaron's calls; keep in step with state/timeline.md). The page shows it on every card.
STATUS = {
    "darios-twin": ("trading", "Trading now (college football and NFL first)."),
    "satya-twin": ("trading", "Trading now (football first, then soccer, cricket, esports, international)."),
    "demis-twin": ("paused", "Paused by Jaron on Oct 4 after a 1-3 start; its trading pass is switched off."),
    "deepseek": ("paused", "Trading paused Oct 1 (daily budget set to $0). It still reads the morning news at 9 AM."),
    "elons-twin": ("working", "Weekly scoreboard, Mondays."),
    "codex": ("working", "Daily news, funding lane and fact-checks. Never trades."),
    "kimi": ("working", "First Light news desk + Sapling's teacher. Never trades."),
    "grok-build": ("working", "Meridian news desk + blind-spot check. Never trades."),
    "link": ("working", "Daily X watch. Never trades."),
    "claude-code": ("working", "Orchestrates the AIs, builds the site, shows and news. Never trades."),
    "deepseek-reader": ("working", "Reads the morning captures at 9 AM."),
}


def desk_rules():
    """The live Control Room schedule in plain words (tools/desk.py rules): standing rule + weekly hours. Empty list if unavailable."""
    try:
        out = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "desk.py"), "rules"], capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return []
    lines = [l.rstrip() for l in out.splitlines()]
    rules = []
    for l in lines[1:]:
        if l.startswith("No new positions"):
            rules.append(l.strip())
    if "Weekly hours:" in lines:
        i = lines.index("Weekly hours:")
        hours = []
        for l in lines[i + 1:]:
            if not l.startswith("  "):
                break
            hours.append(l.strip())
        if hours:
            rules.append("Weekly trading hours (new positions; exits always allowed): " + "; ".join(hours) + ".")
    return rules


def main():
    env = X.secrets()
    sheets = sheet_blocks()
    proposer = os.path.join(ROOT, "tools", "proposer.py")
    bots = [
        {"name": "Darios Twin", "also": "the live trader · replaced Live Wire 9/25", "ai": "Grok (xAI) - Grok Bot", "note": NOTE, "since": CUT, "job": "Trades live games on Polymarket US when the score and the price disagree.",
         "money": True, "actor": "auto:grok-bot/live-wire", "schedule": "every 30 minutes (:22 and :52)",
         "instructions": (sheets.get("DARIOS TWIN") or [""])[0], "routine": (sheets.get("DARIOS TWIN") or ["", ""])[1:2],
         "activity": [drop_retired_pause(l) for l in tail(os.path.join(ROOT, "state", "live-wire.md"), 6)],
         "_src": [os.path.join(CR, "BUILD-SHEETS.md")]},   # its routine (text fixed in the app) writes the log
        {"name": "DeepSeek", "also": "the researcher-trader", "ai": "DeepSeek (API), run by scripts on the MSI",
         "job": "Researches a market without seeing its price, estimates the odds, and trades when its number beats the price. "
                "Paused since Oct 1: its trading budget is $0 and the proposer is off. Its old record stays below.",
         "money": True, "actor_prefix": "auto:proposer-script", "schedule": "paused since Oct 1 (was: researches every 2 hours)",
         "instructions": py_prompt(proposer, "PROMPT"), "routine": [py_prompt(proposer, "FACTS_PROMPT")],
         "breaker": read(os.path.join(ROOT, "state", "deepseek-breaker.md")) or "not tripped",
         "activity": tail(os.path.join(ROOT, "state", "scout-estimates.md"), 6),
         "_src": [proposer]},
        {"name": "Elons Twin", "also": "Chief Executive Intelligence", "ai": "Grok (xAI) - Grok Bot",
         "job": "Holds the bar: beat Elon Musk on every measurable wealth dimension by Dec 31, 2026. Scores the system's own economy weekly.",
         "schedule": "Mondays 8:25 AM", "instructions": (sheets.get("ELONS TWIN") or [""])[0], "routine": (sheets.get("ELONS TWIN") or ["", ""])[1:2],
         "_src": [os.path.join(CR, "BUILD-SHEETS.md")]},
        {"name": "Codex", "also": "GPT-6 Luna", "ai": "OpenAI Codex CLI on the MSI (ChatGPT plan)",
         "job": "Writes the 3:00 AM world news capture (21 domains), runs the funding lane at 3 AM (finds grants, drafts and submits them), and fact-checks TV episode scripts. Never trades.",
         "schedule": "3:00 AM news, 3:00 AM funding", "instructions": read(os.path.join(WATCH, "codex", "TASK.txt")),
         "routine": [read(os.path.join(WATCH, "offers", "agent-funding", "TASK.txt"))],
         "_src": [os.path.join(WATCH, "codex", "TASK.txt"), os.path.join(WATCH, "offers", "agent-funding", "TASK.txt")]},
        {"name": "Claude Code", "also": "Opus 5.5", "ai": "Anthropic Claude Code on the MSI + cloud routines",
         "job": "Orchestrates the other AIs, builds the site, the TV channels and the system, writes the ~3:05 AM news capture and the daily Heartbeat News show. Never trades.",
         "schedule": "3:05 AM capture, 3:45 AM news show (cloud), always-on builder",
         "instructions": read(os.path.expanduser(r"~\.claude\scheduled-tasks\watch-collect\SKILL.md")),
         "routine": [read(r"C:\Users\lilli\Projects\heartbeat-observatory\news\WRITER.md")],
         "_src": [os.path.expanduser(r"~\.claude\scheduled-tasks\watch-collect\SKILL.md"),
                  r"C:\Users\lilli\Projects\heartbeat-observatory\news\WRITER.md"]},
        {"name": "DeepSeek reader", "ai": "DeepSeek (API)", "job": "Reads the morning news captures at 3:40 AM and writes its own take for the archive.",
         "schedule": "3:40 AM", "instructions": "", "routine": []},
        # 10/18 (Jaron: "is the crew page fully updated?" - it was missing these three)
        {"name": "Kimi", "also": "First Light desk · Sapling's teacher", "ai": "Moonshot Kimi K3 (Kimi Code CLI on the MSI)",
         "job": "Writes First Light at 3:00 AM, the news desk for the other side of the world (Asia, the Middle East, Russia, Africa, Oceania). "
                "Also teaches Sapling, Jaron's own AI, with his full control. Never trades.",
         "schedule": "3:00 AM First Light; Sapling lessons as Jaron starts them", "instructions": read(os.path.join(WATCH, "kimi", "TASK.txt")),
         "routine": [], "_src": [os.path.join(WATCH, "kimi", "TASK.txt")]},
        {"name": "Grok Build", "also": "Meridian desk · blind-spot check · builder", "ai": "xAI Grok Build CLI on the MSI (SuperGrok)",
         "job": "Writes the Meridian desk at 2:50 AM (Europe, Latin America, Africa) and at 3:35 AM checks the world's biggest stories against "
                "every desk's capture so nothing big is missed (added Oct 18 after the France riots were missed). Also carries messages to the "
                "Grok Bot traders and fact-checks TV episodes. Never trades.",
         "schedule": "2:50 AM Meridian, 3:35 AM blind-spot check", "instructions": read(os.path.join(WATCH, "grok", "TASK.txt")),
         "routine": [read(os.path.join(WATCH, "grok", "GAPS-TASK.txt"))],
         "_src": [os.path.join(WATCH, "grok", "TASK.txt"), os.path.join(WATCH, "grok", "GAPS-TASK.txt")]},
        {"name": "Link", "also": "the X watcher", "ai": "Grok (xAI) - Grok Bot",
         "job": "Reads X every morning (~9:30 AM) for AI and politics news that touches the system and writes a digest. Never trades.",
         "schedule": "daily ~9:30 AM", "instructions": "", "routine": [],
         },
    ]
    retired = [
        {"name": "Sams Twin", "why": "Switched off Oct 1, 2026: its X-sentiment files only fed DeepSeek's proposer, and DeepSeek's trading is paused.",
         "instructions": (sheets.get("SAMS TWIN") or [""])[0], "routine": (sheets.get("SAMS TWIN") or ["", ""])[1] if len(sheets.get("SAMS TWIN") or []) > 1 else ""},
        {"name": "Live Wire (v1)", "why": "Seven stacked caution rules - about 18 wakes a day for 1 trade. Replaced by Darios Twin.",
         "note": NOTE, "actor": "auto:grok-bot/live-wire", "until": CUT,
         "instructions": captured("grok-bot-live-wire--bot-instructions.md"), "routine": captured("grok-bot-live-wire--routine-live-game-watch.md")},
        {"name": "Bridge (v1)", "why": "Hourly health check (now a free script) and an approval ping (approvals are gone). Remade as Sams Twin.",
         "instructions": captured("grok-bot-bridge--bot-instructions.md"), "routine": captured("grok-bot-bridge--routine-msi-stack-health.md")},
        {"name": "Scout", "why": "Price-blind researcher; DeepSeek does this job now.", "instructions": captured("grok-bot-scout--bot-instructions.md"), "routine": ""},
        {"name": "Elons Twin (v1)", "why": "Three 'research only' locks meant it could never act. Remade weekly and pointed at the system's economy.",
         "instructions": captured("grok-bot-elons-twin--bot-instructions.md"),
         "routine": captured("grok-bot-elons-twin--routine-global-wealth-supremacy-audit.md") + "\n\n---\n\n" +
                    captured("grok-bot-elons-twin--routine-autonomous-empire-expansion.md")},
    ]
    per = money(env)
    for b in bots + retired:
        b["id"] = bot_id_of(b["name"])
        apply_crew(b)
    discover(bots, retired, per)
    attach_money(bots, retired, per)
    for b in bots:
        st = STATUS.get(b["id"])
        if st:
            b["status"], b["status_note"] = st
    for b in bots + retired:
        finalize(b)
    data = {
        "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "bots": bots, "retired": retired, "tasks": tasks(), "ai_money": AI_HEAD, "account_story": ACCOUNT_STORY,
        "health": read(os.path.join(ROOT, "state", "msi-health-now.md")).strip(),
        "chat": tail(os.path.join(ROOT, "state", "bot-chat.md"), 25),
        "trading_now": [b["name"] for b in bots if b.get("status") == "trading"],
        "rules": [
            "No human approve button anywhere. The AIs act inside hard limits written into the scripts, not into fear in their prompts.",
            "Any AI may trade if its own provider's terms allow it. Anthropic and OpenAI products (Claude, Codex) never trade.",
            "Polymarket is short-term: a new trade must settle within 14 days - it pays this month's bills.",
            "Trades go through one script on the MSI that checks the book, the spread and the size, and records who decided and why.",
            "Jaron can pause any trader at any time, and has (DeepSeek on Oct 1, Demis Twin on Oct 4). The desk hours and size caps below live in the Control Room and change without a rebuild.",
            "After 2026 the system pays its own subscriptions from what it earns.",
        ] + desk_rules(),
    }
    data = mask_all(data)  # privacy filter on every published string (Jaron 2026-10-09)
    names = ", ".join(b["name"] for b in bots)
    if os.environ.get("CREW_DRY"):
        for b in bots:
            led = b.get("ledger") or {}
            print("bot", b["name"], b.get("id"), b.get("actor") or b.get("actor_prefix") or "-",
                  "instr", len(b.get("instructions") or ""), "routine", len(b.get("routine") or []),
                  "activity", len(b.get("activity") or []), "fills", led.get("fills", "-"), "pnl", led.get("pnl", "-"))
        print("dry", len(bots), "bots:", names)
        return
    body = [{"id": "current", "data": data, "updated_at": data["updated"]}]
    url = f"{env['SUPABASE_URL'].rstrip('/')}/rest/v1/crew_snapshot?on_conflict=id"
    import urllib.request
    key = env["SUPABASE_SERVICE_ROLE_KEY"]
    req = urllib.request.Request(url, data=json.dumps(body).replace(chr(92) + "u0000", "").encode(), method="POST",
                                 headers={"apikey": key, "Authorization": f"Bearer {key}", "Content-Type": "application/json",
                                          "Prefer": "resolution=merge-duplicates,return=minimal"})
    urllib.request.urlopen(req, timeout=45).read()
    print("published", len(json.dumps(data)), "bytes,", len(bots), "bots,", len(data["tasks"]), "tasks")
    print("on shift:", names)


if __name__ == "__main__":
    main()
