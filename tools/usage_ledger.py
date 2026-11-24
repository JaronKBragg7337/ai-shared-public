#!/usr/bin/env python3
"""Daily local AI usage, with a resumable, prompt-free SQLite cache.

Run: python tools/usage_ledger.py
Optional: --as-of YYYY-MM-DD, --days 14, --rebuild, --home PATH,
          --claude-main PATH, --output-dir PATH

Source logs are only opened for reading. Claude streaming blocks replace the
same message's counters with their maxima, never add another API message.
Codex's reader lives in usage.py. No API calls, pricing guesses, or raw prompt
excerpts are needed. Job names are controlled-vocabulary summaries of prompts;
unrecognized text, paths, credentials and arbitrary values are never copied.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from usage import codex_ledger_event, codex_session_files

ROOT = Path(__file__).resolve().parents[1]
CLAUDE_SESSION = "6cacb0b9-dd02-46b4-88e9-fcea9022ace0"
TZ_NAME = "America/Indiana/Indianapolis"
VERSION = 1
NUMBERS = ("input_tokens", "cached_tokens", "output_tokens", "cache_write_tokens",
           "fresh_input_tokens", "reasoning_tokens")

# Only these literal words can become a job name. A redaction regex alone cannot
# guarantee that an unfamiliar password in someone's first prompt stays private.
TOPICS = (
    (r"usage|ledger|token|rate.limit", "Usage ledger"),
    (r"world\s*2|world2", "World 2"), (r"ashgrove|world\s*3|world3", "Ashgrove"),
    (r"cosmos", "Cosmos"), (r"roof|roofing", "Roofs"),
    (r"news|headline|broadcast", "News"), (r"sapling", "Sapling"),
    (r"mailbox|inbox", "Mailbox"), (r"heartbeat|observatory", "Heartbeat"),
    (r"website|webpage|landing.page|site", "Website"),
    (r"game|town|city|building", "Games and buildings"),
    (r"video|render|unreal|episode|channel", "Video"),
    (r"audio|voice|sound|music", "Audio"), (r"image|photo|texture|sprite", "Images"),
    (r"artifacts?", "Artifacts"), (r"social|postiz|youtube|twitter", "Social posts"),
    (r"trading|trade|crypto|market|polymarket", "Markets"),
    (r"payment|bill|subscription|budget|money", "Bills and subscriptions"),
    (r"safety|iran|pentagon|fortress", "Safety watch"),
    (r"science|brain|physics|space|phobos", "Science"),
    (r"cloud|gpu|runpod", "Cloud tools"),
    (r"git|commit|pull.request|repository|repo", "Repository"),
    (r"phone|mobile|iphone", "Phone layout"),
    (r"test|verify|verification|audit", "Checks"),
    (r"document|readme|handoff|report", "Notes and reports"),
    (r"connector|api|server|mcp|tool", "Tools"),
    (r"login|auth|account|key|secret", "Account setup"),
    (r"desktop|windows|disk|cpu|computer|msi", "Computer"),
    (r"plan|backlog|sweep|task", "Planning"),
    (r"kimi|claude|codex|grok|model|agent", "AI work"),
)
KINDS = ((r"fix|repair|debug|broken|resolve", "Repair"),
         (r"review|inspect|check|test|verify|audit", "Check"),
         (r"research|find|search|investigate|compare", "Research"),
         (r"build|create|implement|add|write|make", "Build"),
         (r"update|edit|change|clean|organize", "Update"))


def digest(value):
    return hashlib.sha256(str(value).encode("utf-8", "replace")).hexdigest()


def job_label(prompt):
    """Summarize a first prompt without exporting any of its literal values."""
    text = str(prompt or "")[:1600].lower()
    topics = []
    for pattern, label in TOPICS:
        match = re.search(r"\b(?:" + pattern + r")\b", text)
        if match:
            topics.append((match.start(), label))
    kinds = [(m.start(), label) for pattern, label in KINDS
             if (m := re.search(r"\b(?:" + pattern + r")\b", text))]
    kind = min(kinds)[1] if kinds else "Other"
    subjects = [label for _, label in sorted(topics)[:3]]
    return (" / ".join(subjects) if subjects else "Unlabelled work"), kind


def model_name(value):
    value = str(value or "unknown")
    if re.fullmatch(r"(?:claude|gpt|codex|kimi|moonshot|grok|qwen|o[1-9])[-a-zA-Z0-9._/: ]{0,85}", value):
        return value
    return "unknown"


def number(value):
    if isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0:
        return int(value)
    return None


def timestamp(value):
    try:
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value / 1000 if value > 100_000_000_000 else value, timezone.utc)
        result = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return result.replace(tzinfo=timezone.utc) if result.tzinfo is None else result
    except (ValueError, TypeError, OverflowError, OSError):
        return None


def text_content(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content if isinstance(b, dict)
                         and b.get("type") in ("text", "input_text") and isinstance(b.get("text"), str))
    return ""


@dataclass
class Source:
    kind: str
    path: Path
    companions: tuple = ()

    @property
    def key(self):
        return digest(str(self.path.resolve()).lower())

    def signature(self):
        result = []
        for path in (self.path,) + self.companions:
            try:
                stat = path.stat()
                result.append([stat.st_size, stat.st_mtime_ns])
            except FileNotFoundError:
                result.append(None)
        return result


def discover(home, main):
    sources, notes = [], []
    groups = (("claude_main", [main] if main.is_file() else []),
              ("claude_builder", list(main.with_suffix("").joinpath("subagents").glob("*.jsonl"))),
              ("codex", [Path(p) for p in codex_session_files(home)]),
              ("kimi", list((home / ".kimi-code" / "sessions").glob("**/agents/*/wire.jsonl"))),
              ("grok", list((home / ".grok" / "sessions").glob("*/*/usage.json"))))
    for kind, paths in groups:
        if not paths:
            notes.append(f"{kind.replace('_', ' ')}: no readable local logs found.")
        for path in sorted(paths):
            companions = tuple(path.parent / name for name in
                               ("chat_history.jsonl", "summary.json", "events.jsonl")) if kind == "grok" else ()
            sources.append(Source(kind, path, companions))
    return sources, notes


class Ledger:
    def __init__(self, cache, tz):
        cache.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(cache, timeout=30)
        self.db.row_factory = sqlite3.Row
        self.tz = tz
        version = self.db.execute("PRAGMA user_version").fetchone()[0]
        if version != VERSION:
            for table in ("files", "usage", "activity"):
                self.db.execute(f"DROP TABLE IF EXISTS {table}")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS files (
          id TEXT PRIMARY KEY, kind TEXT, signature TEXT, offset INTEGER,
          head TEXT, tail TEXT, state TEXT);
        CREATE TABLE IF NOT EXISTS usage (
          file TEXT, event TEXT, day TEXT, job TEXT, model TEXT, at REAL,
          input_tokens INTEGER, cached_tokens INTEGER, output_tokens INTEGER,
          cache_write_tokens INTEGER, fresh_input_tokens INTEGER, reasoning_tokens INTEGER,
          in_between INTEGER, PRIMARY KEY(file,event));
        CREATE TABLE IF NOT EXISTS activity (
          file TEXT, job TEXT, day TEXT, ai TEXT, role TEXT, name TEXT, kind TEXT,
          first REAL, last REAL, humans INTEGER DEFAULT 0,
          PRIMARY KEY(file,job,day));
        CREATE INDEX IF NOT EXISTS usage_day ON usage(day);
        CREATE INDEX IF NOT EXISTS usage_job ON usage(file,job);
        """)
        self.db.execute(f"PRAGMA user_version={VERSION}")
        self.db.commit()
        self.stats = Counter()

    def clear(self, key):
        for table in ("usage", "activity"):
            self.db.execute(f"DELETE FROM {table} WHERE file=?", (key,))
        self.db.execute("DELETE FROM files WHERE id=?", (key,))

    @staticmethod
    def initial(source):
        ai, role = {"claude_main": ("Claude", "main"), "claude_builder": ("Claude", "builder"),
                    "codex": ("Codex", "session"), "kimi": ("Kimi", "session"),
                    "grok": ("Grok Build", "session")}[source.kind]
        return {"ai": ai, "role": role, "job": source.key[:12], "name": "Unlabelled work",
                "kind": "Other", "model": "unknown", "named": False, "sequence": 0,
                "in_between": False, "builder_agents": [], "builder_tools": [],
                "bad_lines": 0, "missing_timestamps": 0, "missing_message_ids": 0}

    def name_job(self, key, state, prompt, replace=False):
        if not state["named"] or replace:
            state["name"], state["kind"] = job_label(prompt)
            state["named"] = True
            self.db.execute("UPDATE activity SET name=?,kind=? WHERE file=? AND job=?",
                            (state["name"], state["kind"], key, state["job"]))

    def observe(self, key, state, dt, human=0):
        if dt is None:
            return
        day, epoch = dt.astimezone(self.tz).date().isoformat(), dt.timestamp()
        self.db.execute("""INSERT INTO activity VALUES (?,?,?,?,?,?,?,?,?,?)
          ON CONFLICT(file,job,day) DO UPDATE SET first=MIN(first,excluded.first),
          last=MAX(last,excluded.last), humans=humans+excluded.humans""",
                        (key, state["job"], day, state["ai"], state["role"], state["name"],
                         state["kind"], epoch, epoch, human))

    def record(self, key, state, event_id, dt, counters, model=None):
        if dt is None:
            state["missing_timestamps"] += 1
            return
        self.observe(key, state, dt)
        values = [number(counters.get(field)) for field in NUMBERS]
        # Keep one API message even if its streaming content arrives in many lines.
        updates = ",".join(f"{field}=CASE WHEN {field} IS NULL THEN excluded.{field} "
                           f"WHEN excluded.{field} IS NULL THEN {field} ELSE MAX({field},excluded.{field}) END"
                           for field in NUMBERS)
        self.db.execute(f"""INSERT INTO usage VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
          ON CONFLICT(file,event) DO UPDATE SET {updates},
          in_between=MAX(in_between,excluded.in_between)""",
                        (key, digest(event_id), dt.astimezone(self.tz).date().isoformat(), state["job"],
                         model_name(model or state["model"]), dt.timestamp(), *values, int(state["in_between"])))

    def mark_between(self, key, state):
        state["in_between"] = True
        self.db.execute("UPDATE usage SET in_between=1 WHERE file=? AND job=?", (key, state["job"]))

    def claude(self, source, state, obj, offset):
        key, main = source.key, source.kind == "claude_main"
        kind = obj.get("type")
        message = obj.get("message") or {}
        if not isinstance(message, dict):
            return
        dt = timestamp(obj.get("timestamp"))
        content = message.get("content")
        prompt = text_content(content)
        if kind == "user":
            notification = "<task-notification>" in prompt
            if main:
                result = obj.get("toolUseResult")
                if isinstance(result, dict) and result.get("agentId"):
                    agent_hash = digest(result["agentId"])
                    if agent_hash not in state["builder_agents"]:
                        state["builder_agents"].append(agent_hash)
                    self.mark_between(key, state)
                if notification:
                    ids = re.findall(r"<(?:task-id|tool-use-id)>([^<]+)</", prompt)
                    if any(digest(i) in state["builder_agents"] + state["builder_tools"] for i in ids):
                        self.mark_between(key, state)
            is_tool = isinstance(content, list) and any(isinstance(b, dict) and b.get("type") == "tool_result" for b in content)
            if prompt.strip() and not is_tool and not notification and not obj.get("isMeta") and not obj.get("isCompactSummary"):
                if main:
                    state["sequence"] += 1
                    state["job"] = digest(f"{key}:{state['sequence']}")[:12]
                    state["named"], state["in_between"] = False, False
                self.name_job(key, state, prompt)
                self.observe(key, state, dt, human=1)
            else:
                self.observe(key, state, dt)
        elif kind == "assistant":
            if main and isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use" and block.get("name") in ("Agent", "Task", "TaskOutput"):
                        if block.get("name") in ("Agent", "Task") and block.get("id"):
                            h = digest(block["id"])
                            if h not in state["builder_tools"]:
                                state["builder_tools"].append(h)
                        self.mark_between(key, state)
            state["model"] = model_name(message.get("model"))
            usage = message.get("usage")
            mid = message.get("id")
            if isinstance(usage, dict) and mid:
                fresh = number(usage.get("input_tokens")) or 0
                write = number(usage.get("cache_creation_input_tokens")) or 0
                read = number(usage.get("cache_read_input_tokens")) or 0
                self.record(key, state, mid, dt, {"input_tokens": fresh + write + read,
                            "cached_tokens": read, "cache_write_tokens": write,
                            "fresh_input_tokens": fresh, "output_tokens": number(usage.get("output_tokens"))})
            elif isinstance(usage, dict):
                state["missing_message_ids"] += 1
            self.observe(key, state, dt)

    def codex(self, source, state, obj, offset):
        reader_state = state.setdefault("codex", {})
        for event in codex_ledger_event(obj, reader_state):
            kind = event["type"]
            if kind == "prompt":
                self.name_job(source.key, state, event["text"], replace=True)
                self.observe(source.key, state, timestamp(event.get("timestamp")), human=1)
            elif kind == "model":
                state["model"] = model_name(event["model"])
            elif kind == "usage":
                self.record(source.key, state, f"{offset}:codex", timestamp(event.get("timestamp")), event, event.get("model"))
        # Copied parent history in forks is not this session's work or duration.
        ordinal = obj.get("ordinal")
        if not isinstance(ordinal, int) or ordinal >= reader_state.get("history_boundary", 0):
            self.observe(source.key, state, timestamp(obj.get("timestamp")))

    def kimi(self, source, state, obj, offset):
        kind, dt = obj.get("type"), timestamp(obj.get("time"))
        if kind == "turn.prompt":
            self.name_job(source.key, state, text_content(obj.get("input")))
            self.observe(source.key, state, dt, human=1)
        elif kind == "usage.record":
            u = obj.get("usage") or {}
            fresh, read, write = (number(u.get(k)) for k in ("inputOther", "inputCacheRead", "inputCacheCreation"))
            counters = {"input_tokens": sum((fresh or 0, read or 0, write or 0)), "cached_tokens": read,
                        "cache_write_tokens": write, "fresh_input_tokens": fresh, "output_tokens": number(u.get("output"))}
            state["model"] = model_name(obj.get("model"))
            identity = json.dumps([obj.get("time"), obj.get("agentId"), state["model"], counters], sort_keys=True)
            self.record(source.key, state, identity, dt, counters)
        self.observe(source.key, state, dt)

    def grok(self, source, state):
        for path in source.companions[:1]:
            if path.is_file():
                with path.open(encoding="utf-8") as fh:
                    for line in fh:
                        try:
                            obj = json.loads(line)
                        except ValueError:
                            state["bad_lines"] += 1
                            continue
                        if obj.get("role") == "user" and not obj.get("synthetic"):
                            prompt = text_content(obj.get("content"))
                            if prompt:
                                self.name_job(source.key, state, prompt)
                                break
        with source.path.open(encoding="utf-8") as fh:
            data = json.load(fh)
        turns = data.get("turns") or []
        if not turns and isinstance(data.get("session"), dict):
            turns = [dict(data["session"], endedAt=data.get("updatedAt"), turnNumber="session")]
            state["approximate_date"] = True
        for index, turn in enumerate(turns):
            dt = timestamp(turn.get("endedAt"))
            models = turn.get("modelUsage") or {turn.get("primaryModelId", "unknown"): turn}
            for model, usage in models.items():
                if not isinstance(usage, dict):
                    continue
                counters = {dest: number(usage.get(src)) for dest, src in
                            (("input_tokens", "inputTokens"), ("cached_tokens", "cachedReadTokens"),
                             ("output_tokens", "outputTokens"), ("cache_write_tokens", "cacheCreationTokens"),
                             ("reasoning_tokens", "reasoningTokens"))}
                if counters["input_tokens"] is not None and counters["cached_tokens"] is not None:
                    counters["fresh_input_tokens"] = max(0, counters["input_tokens"] - counters["cached_tokens"] - (counters["cache_write_tokens"] or 0))
                self.record(source.key, state, f"{turn.get('turnNumber', index)}:{model}", dt, counters, model)
        summary = source.path.parent / "summary.json"
        if summary.is_file():
            with summary.open(encoding="utf-8") as fh:
                meta = json.load(fh)
            if not state["named"]:
                self.name_job(source.key, state, meta.get("generated_title") or meta.get("session_summary"))
            for field in ("created_at", "updated_at"):
                self.observe(source.key, state, timestamp(meta.get(field)))

    @staticmethod
    def edges(path, offset):
        with path.open("rb") as fh:
            head = hashlib.sha256(fh.read(min(4096, offset))).hexdigest()
            fh.seek(max(0, offset - 4096))
            tail = hashlib.sha256(fh.read(min(4096, offset))).hexdigest()
        return head, tail

    def scan(self, source, rebuild=False):
        signature = source.signature()
        if signature[0] is None:
            self.stats["unreadable_files"] += 1
            return
        key, encoded = source.key, json.dumps(signature)
        old = self.db.execute("SELECT * FROM files WHERE id=?", (key,)).fetchone()
        if old and old["signature"] == encoded and not rebuild:
            self.stats["reused_files"] += 1
            return
        offset, state = 0, self.initial(source)
        if old and not rebuild and source.kind != "grok":
            previous = json.loads(old["signature"])
            if signature[0][0] > previous[0][0] and self.edges(source.path, old["offset"]) == (old["head"], old["tail"]):
                offset, state = old["offset"], json.loads(old["state"])
                self.stats["appended_files"] += 1
        if not offset:
            self.clear(key)
            self.stats["rescanned_files"] += 1
        if source.kind == "grok":
            self.grok(source, state)
            self.stats["bytes_read"] += sum(item[0] for item in signature if item)
            offset = signature[0][0]
        else:
            parser = self.claude if source.kind.startswith("claude") else getattr(self, source.kind)
            limit = signature[0][0]
            with source.path.open("rb") as fh:
                fh.seek(offset)
                while fh.tell() < limit:
                    start = fh.tell()
                    line = fh.readline(limit - start)
                    self.stats["bytes_read"] += len(line)
                    if not line.endswith(b"\n"):
                        break  # A writer is still finishing this record; retry it next run.
                    offset = fh.tell()
                    try:
                        obj = json.loads(line)
                    except (ValueError, UnicodeError):
                        state["bad_lines"] += 1
                        continue
                    if isinstance(obj, dict):
                        parser(source, state, obj, start)
        head, tail = self.edges(source.path, offset)
        self.db.execute("INSERT OR REPLACE INTO files VALUES (?,?,?,?,?,?,?)",
                        (key, source.kind, encoded, offset, head, tail, json.dumps(state)))

    def report_rows(self, since, through):
        rows = []
        for activity in self.db.execute("SELECT * FROM activity WHERE day>=? AND day<=?", (since, through)):
            records = self.db.execute("SELECT * FROM usage WHERE file=? AND job=? AND day=?",
                                      (activity["file"], activity["job"], activity["day"])).fetchall()
            by_model = defaultdict(list)
            for record in records:
                by_model[record["model"]].append(record)
            if not by_model:
                by_model["unknown"] = []
            for model, entries in by_model.items():
                row = {"date": activity["day"], "ai": activity["ai"], "role": activity["role"],
                       "job_id": activity["job"], "job_name": activity["name"], "work_kind": activity["kind"],
                       "model": model, "source_id": activity["file"][:12], "records": len(entries),
                       "human_messages": activity["humans"] if len(by_model) == 1 else None,
                       "logged_span_seconds": round(activity["last"] - activity["first"], 1) if len(by_model) == 1 else None,
                       "first_seen": datetime.fromtimestamp(activity["first"], timezone.utc).isoformat(),
                       "last_seen": datetime.fromtimestamp(activity["last"], timezone.utc).isoformat()}
                row.update(totals(entries))
                between = [entry for entry in entries if entry["in_between"]]
                row["claude_in_between"] = totals(between) if between else None
                rows.append(row)
        return sorted(rows, key=lambda r: (r["date"], (r["input_tokens"] or 0) + (r["output_tokens"] or 0), r["job_id"]), reverse=True)


def totals(entries):
    result = {}
    for field in NUMBERS:
        values = [entry[field] for entry in entries]
        known = [value for value in values if value is not None]
        result[field] = sum(known) if known else None
        if len(known) != len(values):
            result[field + "_partial"] = True
    if result["input_tokens"] and result["cached_tokens"] is not None and not result.get("cached_tokens_partial") and not result.get("input_tokens_partial"):
        result["percent_cached"] = round(100 * result["cached_tokens"] / result["input_tokens"], 1)
    else:
        result["percent_cached"] = None
    return result


def weekly(rows, as_of):
    weeks = []
    for age in (0, 7):
        end, start = as_of - timedelta(days=age), as_of - timedelta(days=age + 6)
        chosen = [r for r in rows if start.isoformat() <= r["date"] <= end.isoformat()]
        ai_rows = []
        for ai in ("Claude", "Codex", "Kimi", "Grok Build"):
            items = [r for r in chosen if r["ai"] == ai]
            entry = {"ai": ai, "jobs": len({r["job_id"] for r in items}), **totals(items)}
            entry["unmeasured_jobs"] = len({r["job_id"] for r in items if r["input_tokens"] is None})
            ai_rows.append(entry)
        between = [r["claude_in_between"] for r in chosen if r["claude_in_between"]]
        weeks.append({"start": start.isoformat(), "end": end.isoformat(), "totals": ai_rows,
                      "claude_in_between": totals(between)})
    return weeks


def fmt(value):
    return "—" if value is None else f"{value:,}"


def token_cells(row):
    cells = [fmt(row[key]) + ("*" if row.get(key + "_partial") else "") for key in NUMBERS[:3]]
    cells.append("—" if row["percent_cached"] is None else f"{row['percent_cached']:.1f}%")
    return " | ".join(cells)


def markdown(report):
    lines = ["# Daily AI usage ledger", "", f"Owner: Jaron. Days use Fort Wayne time ({TZ_NAME}).",
             "In = all input, including cache reads and cache writes. Cached = cache reads only.",
             "Job names are safe topic summaries of the first prompt; short IDs keep separate jobs apart.",
             "— means not logged. * means a partial total. Tokens show usage, not a dollar bill or a cheapest-AI ranking.",
             "Claude in-between is already included in Claude totals: turns that launch or receive builder work.", ""]
    for day in report["days"]:
        lines.extend([f"## {day['date']}", "", "| AI | Job | Model | In | Cached | Out | % cached |",
                      "| --- | --- | --- | ---: | ---: | ---: | ---: |"])
        for row in day["rows"]:
            ai = row["ai"] + (" " + row["role"] if row["ai"] == "Claude" else "")
            job = f"{row['work_kind']}: {row['job_name']} [{row['job_id'][:8]}]"
            lines.append(f"| {ai} | {job} | {row['model']} | {token_cells(row)} |")
        if not day["rows"]:
            lines.append("| No local activity found | — | — | — | — | — | — |")
        if day["claude_in_between"]:
            lines.append(f"| Claude in-between | Included above; best effort | — | {token_cells(day['claude_in_between'])} |")
        lines.append("")
    lines.extend(["## Weekly totals per AI", "", "The two weeks below each cover seven days, ending on the report date.", ""])
    for week in report["weeks"]:
        lines.extend([f"### {week['start']} through {week['end']}", "",
                      "| AI | Jobs | In | Cached | Out | % cached |",
                      "| --- | ---: | ---: | ---: | ---: | ---: |"])
        for row in week["totals"]:
            lines.append(f"| {row['ai']} | {row['jobs']} | {token_cells(row)} |")
        lines.append(f"| Claude in-between (included) | — | {token_cells(week['claude_in_between'])} |")
        lines.append("")
    lines.extend(["## What was counted", "",
                  "- Claude: each message ID once, using its largest recorded counters as streaming finishes. Human turns exclude tool results, summaries and automatic task notices.",
                  "- Codex: changes in session token totals, grouped by model. Copied parent history is excluded when the log marks it. Reasoning is part of output, never added twice.",
                  "- Kimi: usage.record entries in Kimi Code wire logs; context-size measurements and parent summaries are excluded.",
                  "- Grok Build: per-model turn records; session totals are not added again. Turns are dated when they ended.",
                  "- The JSON includes cache writes, fresh input, human-message counts and logged time spans. Spans include idle time and are not hours worked.",
                  "- A job crossing midnight is split by the timestamps of its usage records. A single response belongs to the day it was logged.",
                  "- No prices or subscription percentages are converted into money. Different jobs and model tokenizers need care when comparing efficiency.", ""])
    lines.extend(f"- {note}" for note in report["notes"])
    stats = report["scan"]
    lines.extend(["", f"Scan: {stats.get('reused_files', 0)} unchanged files reused; {stats.get('appended_files', 0)} appended files; "
                  f"{stats.get('rescanned_files', 0)} full file reads; {stats.get('bytes_read', 0):,} bytes read; {stats['seconds']:.2f} seconds.", ""])
    return "\n".join(lines)


def atomic_write(path, content):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(content, encoding="utf-8", newline="\n")
    temporary.replace(path)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--claude-main", type=Path)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "state")
    parser.add_argument("--as-of", type=date.fromisoformat)
    parser.add_argument("--days", type=int, default=14)
    parser.add_argument("--rebuild", action="store_true")
    args = parser.parse_args(argv)
    if args.days < 14:
        parser.error("--days must be at least 14 so both weekly totals are complete")
    try:
        tz = ZoneInfo(TZ_NAME)
    except Exception:
        parser.exit(1, "Fort Wayne time-zone data is unavailable; install Python tzdata and retry.\n")
    as_of = args.as_of or datetime.now(tz).date()
    main_path = args.claude_main or args.home / ".claude" / "projects" / "C--Users-lilli-AI-Shared" / (CLAUDE_SESSION + ".jsonl")
    start = time.perf_counter()
    sources, notes = discover(args.home, main_path)
    ledger = Ledger(args.output_dir / "usage-ledger" / "cache.sqlite", tz)
    active = {source.key for source in sources}
    with ledger.db:
        for row in ledger.db.execute("SELECT id FROM files").fetchall():
            if row["id"] not in active:
                ledger.clear(row["id"])
    for source in sources:
        try:
            with ledger.db:
                ledger.scan(source, args.rebuild)
        except (OSError, ValueError, sqlite3.Error):
            # Exception text can contain raw log content or sensitive paths.
            notes.append(f"{source.kind.replace('_', ' ')} file {source.key[:8]} could not be read; omitted from this report.")
            with ledger.db:
                ledger.clear(source.key)
            ledger.stats["unreadable_files"] += 1
    rows = ledger.report_rows((as_of - timedelta(days=args.days - 1)).isoformat(), as_of.isoformat())
    days = []
    for age in range(args.days):
        day = (as_of - timedelta(days=age)).isoformat()
        chosen = [r for r in rows if r["date"] == day]
        between = [r["claude_in_between"] for r in chosen if r["claude_in_between"]]
        days.append({"date": day, "rows": chosen, "claude_in_between": totals(between) if between else None})
    diagnostics = Counter()
    coverage = Counter()
    for file in ledger.db.execute("SELECT kind,state FROM files"):
        coverage[file["kind"]] += 1
        state = json.loads(file["state"])
        for field in ("bad_lines", "missing_timestamps", "missing_message_ids", "approximate_date"):
            diagnostics[field] += state.get(field, 0)
        diagnostics["codex_counter_resets"] += state.get("codex", {}).get("counter_resets", 0)
    for field, count in diagnostics.items():
        if count:
            notes.append(f"{field.replace('_', ' ')}: {count:,}; coverage may be incomplete.")
    notes.append("Local files covered: " + "; ".join(f"{k.replace('_', ' ')} {v}" for k, v in sorted(coverage.items())) + ".")
    ledger.stats["seconds"] = round(time.perf_counter() - start, 3)
    report = {"version": VERSION, "owner": "Jaron", "timezone": TZ_NAME, "as_of": as_of.isoformat(),
              "generated_at": datetime.now(timezone.utc).isoformat(), "days": days, "weeks": weekly(rows, as_of),
              "notes": notes, "coverage": dict(coverage), "diagnostics": dict(diagnostics), "scan": dict(ledger.stats)}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    atomic_write(args.output_dir / "usage-ledger.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    atomic_write(args.output_dir / "usage-ledger.md", markdown(report))
    ledger.db.close()
    print(f"Usage ledger written: {len(rows):,} daily job/model rows; {len(sources)} source files; "
          f"{ledger.stats['seconds']:.2f}s; {ledger.stats.get('unreadable_files', 0)} unreadable files.")
    return 1 if ledger.stats.get("unreadable_files") else 0


if __name__ == "__main__":
    sys.exit(main())
