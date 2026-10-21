# Control Room - inventory (2026-09-25, Claude Code)

Why: Jaron wants to see and change his system himself, like the site editor ("hearing it in a chat vs going in and changing it
is different... makes it memorable"). And: "Too many rules. AIs freak out." This is every knob and rule that actually changes
what the money AIs do, where each one lives, and where two places disagree. Next step: the admin page where each row is a tap.

## Trading rules that can STOP a trade (the ones that make AIs freeze)
| Rule | Value | Lives in | Who it binds | Notes |
|---|---|---|---|---|
| Max spread | 5c | tools/desk-trade.py | Live Wire | |
| Max spread | 2c | tools/proposer.py | DeepSeek | **disagrees** with Live Wire's 5c; v1 Live Wire routine also said 2c |
| Settles within | 14 days | desk-trade.py AND proposer.py | both | same value in two files |
| Max size | $10 | desk-trade.py `--max-size` | Live Wire | |
| Default size | $5 / $10 hard disagreement | Grok Bot app (pasted instructions) | Live Wire | not on the MSI - only editable in Grok Bot |
| Max 3 open live positions | 3 | Grok Bot app | Live Wire | |
| "Streak" sizing ($10 only after 3 non-losing) | 3 | Grok Bot app (Live Wire routine) | Live Wire | in its routine instructions (corrected 2026-09-25: not self-invented) |
| Quiet unless loss > $5 | $5 | Grok Bot app | Live Wire | |
| Trade sizes by confidence | $2 / $4 / $8 | proposer.py | DeepSeek | |
| Min edge | 3c (8c for the "split" method) | proposer.py | DeepSeek | |
| DeepSeek daily budget | $10 | tools/verifier.py | DeepSeek | |
| Price may move | 1c | verifier.py, executor.py | DeepSeek | |
| Approval expires | 6 h | executor.py | DeepSeek | |
| No crypto | - | proposer.py, Grok Bot app | both | |
| Claude/Codex never trade | - | desk-trade.py | everyone | provider terms (Anthropic/OpenAI) - keep |
| Board flags | 3 kinds | tools/live-board.py | Live Wire | hints only - corrected 4:39 PM after it treated "0 flagged" as "no trade" |

## Schedules (Windows tasks on the MSI)
(times as of 2026-10-15; heavy jobs run 3-6 AM) Watch Codex Writer, Kimi First Light, MSI Reader, Whats New Scouts, Funding Lane 3:00 AM · Watch DeepSeek Reader 3:40 · HB Rendered News 3:50 · Heartbeat News Writer 4:20 (backup; Claude, then Codex) · Login Watch 5:50 · AI Budget Report Mon 5:30 · Desk Weekly Review Mon 5:35
· Trade Proposer every 2 h · Trade Verifier + Trade Executor every 5 min · Live Board every 5 min · Usage Snapshot every 15 min ·
DB Size Check hourly · Scout Scorer 6:30 · Revenue Desk Daily 7:03 (a no-model script; the approve-queue version is retired) ·
AI-Shared Mirror 4:30 AM to Google Drive.
Elsewhere: Claude "watch-collect" ~3:00-3:10 AM (Claude app) · cloud news routine 3:45 AM (claude.ai) · Grok Bot routines (Grok Bot app:
Live Wire, 9 PM X capture, Bridge health).

## Repaired while inventorying
- AgentWorkbench-Scheduler / -Server: pointed at an old PowerShell folder (7.6.3.0) after PowerShell updated itself; failing every
  15 min since. Now use the stable pwsh alias. Running.
- AI-Shared Mirror shows result 1 - that is robocopy's "files copied" code, not a failure.

## For the Control Room page
One row per rule above: plain sentence, current value, a tap control, "who obeys this", history + undo. Scripts read their numbers
from one Supabase table instead of their own copies. Rules that live only in the Grok Bot app get a "copy this into Grok Bot"
button until Grok can read them from the table itself.

## Monday 9/28 review - add (9/27)
- Grok Bot usage: 44% after 3 days (Jaron's screenshot 8:52 AM 9/27). Decide cadence (every 30 min at :22/:52) vs pool.
- Money language: report SETTLED profit, OPEN-position value and WITHDRAWABLE cash as three separate numbers, always.
