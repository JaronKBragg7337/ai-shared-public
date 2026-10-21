# Who captures what from X (sorted out 10/15/2026 ~9:45 PM, after Jaron caught a duplicate)

| Job | Who runs it | When | Writes to | Status |
|---|---|---|---|---|
| Jaron's own X activity (posts, replies, quotes, reposts, word for word) | Grok APP scheduled task "X watch /jaron" (Grok chat, writes via the Grok Machine connector) | daily 9:00 PM | Projects/watch/jaron-x/YYYY-MM-DD.md | KEEP - the original, files since 9/24 (gaps: 9/25, 10/4, 10/10-10/13) |
| (same job, duplicate) | Sams Twin routine "jaron-x-daily" (Grok Bot) | 9:06 PM | same folder | PAUSE/DELETE - created 10/15 when the Grok app task messaged Sams Twin as "main Grok" |
| AI + politics X digest | Link (Grok Bot) | 9:33 AM | research/ai-x-watch/YYYY-MM-DD.md | KEEP - different job |
| X sentiment for trades | Sams Twin x-desk | (inactive since 10/1) | state | stays inactive |

## New finding (10/15)
A Grok APP scheduled task can message Grok Bot bots (it messaged Sams Twin with no sender tag, so Sams saw it as if Jaron typed
it). Grok chat also says it can message Grok Bots directly. So a Grok chat task can drive the bots, which is useful but unlabeled.
Bots should ask "who is this?" when an untagged message gives orders.

## Gaps worth knowing
- The jaron-x folder is missing 10/10-10/13 (and 9/25, 10/4): the 9 PM task didn't write those nights.
- Tonight's capture found only 5 items (low). Sams' profile scroll was checking for missed items.

## DECIDED 10/15 9:54 PM (Jaron)
Keep both, as a pipeline: the Grok APP 9 PM task "X watch /jaron" messages Sams Twin each night (signed, so Sams knows the
source); Sams Twin does the profile scroll and writes/fixes the day's file. Sams Twin stays INACTIVE (no routines of its own,
jaron-x-daily deleted) and answers requests only. Why: keeps a Grok-app-task -> Grok-Bot pipeline in daily use, to find what
else it can do. Parallel to explore: ChatGPT scheduled tasks can't use Desktop Commander; a scheduled chat task that pings
something the MSI listens to (webhook/ntfy) could be the same kind of bridge.
