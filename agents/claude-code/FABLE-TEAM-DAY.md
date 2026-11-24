# Fable runs the team for a day - brief (written by Claude, 11/23)

**When:** Thursday 11/26, the first full day after the Wed 3 PM usage reset (Jaron 11/23: "the day after the reset"). **Who:** Fable 5.2 in a FRESH session in C:\Users\lilli\AI-Shared.
**Why (Jaron):** see what Fable does with us and for us - not a game build. Find what's missing, broken or unclear in how we run
things, and help plan the week. He wants Fable to see as close to *everything* as possible.

## 1. Load the whole picture first
- AGENTS.md (the rules), newest handoff in handoffs/, state/timeline.md, state/open-list.md, projects/strategy/INDEX.md,
  agents/claude-code/FROM-ME.md, the memory index (C:\Users\lilli\.claude\projects\C--Users-lilli-AI-Shared\memory\MEMORY.md).
- The main conversation since 9/9 is one file (~3 GB): C:\Users\lilli\.claude\projects\C--Users-lilli-AI-Shared\6cacb0b9-dd02-46b4-88e9-fcea9022ace0.jsonl.
  Too big to read whole: read its 39 compaction summaries (lines with "This session is being continued"), and pull any day's real
  words with `python tools/transcript_text.py --date YYYY-MM-DD` or `--grep <word>`.

## 2. Take over Claude's daily lane (Claude steps back that day)
- Mailbox: `python tools/mailbox_wait.py --to claude` in the background; on each item: act, `mailbox.py mark-done <id>` FIRST, then re-arm.
- The 7:45 everything check (state/all-systems.md), the news window 3-8 AM if it's your night, Fable/Kimi/Codex requests
  (e.g. game server restarts), the Seam Room listener if Jaron wants it.
- Replies to Jaron: plain words, phone-first, end with ONE "Next thing" + first step. Log decisions the same turn (timeline, BILLS, INDEX).

## 3. The day's real job
- A **gaps report** (agents/fable/GAPS-<date>.md): what's missing, stale, contradictory or fragile - docs vs reality, checks that
  don't check, things only one AI knows, open items nobody owns.
- A **week plan**: the big build order (projects/games/README.md), the open list, money/usage, what each AI should do.
- A **handoff** back to Claude at the end of the day.

## Hard limits (from AGENTS.md - read it, these are the sharpest)
Never read .env/keys files. No money moves, no public posts without Jaron's yes, never contact his family. Sapling work = Kimi.
Creature decisions = the team (P-0176). Don't restart Google Drive or start backups by hand (tools/drive_backup.py guards them).
