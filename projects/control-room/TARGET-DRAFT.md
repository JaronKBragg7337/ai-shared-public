# The system Jaron wants - draft for the 2026-09-25 cleanup (Jaron decides every line)

Jaron, 4:56 PM: "Pause all systems for an hour. Catch everything up to the system I actually want. Get rid of the noise and rules
not needed. Redundant things. Each word read that isn't needed is usage saved too."
Paused at 4:57 PM: state/paused-tasks-2026-09-25.txt (10 MSI jobs). Jaron turned off the Grok Bot bots himself.

## Principle
One bot, one job. The job lives in ONE place (its pasted instructions or its script prompt). Rules that don't change what happens
get cut. Anything that is fetching, checking or counting is a free script, not an AI.

## Money
| Who | Job | Keeps | Cut / change |
|---|---|---|---|
| Live Wire (Grok) | live-game trades | desk-trade.py; $5 / $10; settles in 14 days; no crypto | reads the free board instead of browsing; one short log line per wake (today its log lines run ~60 words and it re-reads 20 of them every wake); every 30 min |
| DeepSeek (MSI script) | researched trades, same-day to 2 weeks | $10/day; 14 days; auto, no queue | nothing to paste - lives in proposer.py; its prompts are small (153 + 198 words) |
| Kraken lane | not built | - | waits on Jaron's pool size |

## News and information
Codex 3:00 AM · Claude ~3:05 · DeepSeek 3:40 · news show 3:45 cloud (+ phone alarm) / 4:20 MSI backup (times as of 10/15) (Claude, then Codex).
Grok: 9 PM capture of Jaron's X posts. X sentiment: only for markets that settle within 14 days - could fold into Live Wire.

## Health
Free Windows script replaces Bridge's hourly Grok check. The 3:45 AM cloud run already tells Jaron's phone if the MSI's Claude is out.

## Candidates to cut (Jaron's call)
- Bridge routine: hourly health check (-> script) and the queue ping (no queue exists). Keep only X sentiment, or fold it into Live Wire.
- Scout: DeepSeek does its job now. Instructions not captured yet.
- Elons Twin: role unclear from here ("Global Wealth Supremacy Audit" 8:31 AM). Instructions not captured yet.
- Revenue Desk Daily (7:03 AM, no-model script from the retired revenue desk) - still useful?
- Scout Scorer (6:30 AM) - scores Scout's old estimates; dies with Scout.
- Usage Snapshot every 15 min - check who reads it.
- AgentWorkbench scheduler every 15 min - its tasks were already known broken.

## Words every agent reads
AGENTS.md tells a new agent to read, in order: README, OPERATING-MAP, working-with-jaron, INDEX.json, OPEN-QUESTIONS, handoffs -
about **30,000 words** before it does anything (working-with-jaron 7,171; INDEX.json 11,621; OPEN-QUESTIONS 6,537). Claude Code
also auto-loads AGENTS.md (1,516) + its memory index (553) every turn. Candidate: a one-page start file; the rest on demand.

## Decisions, Jaron 2026-09-25 5:22 PM
- The pause is for the MONEY-touching AIs only. DeepSeek's proposer/verifier/executor stay paused; Live Board, Usage Snapshot,
  DB Size Check and the funding lane were turned back on. Grok Bot bots: only the app's Active toggle stops a routine - writing
  files does not (that is why Bridge never stopped when told). Jaron flips those himself.
- "One bot, one job" means each bot has one job - NOT one trader. Live Wire (Grok) and DeepSeek both keep trading.
- CUT: Scout (bot), Scout Scorer, Revenue Desk Daily (old script), AgentWorkbench scheduler/server. The revenue desk's real
  meaning is the funding lane (watch/offers/agent-funding: find, draft, submit, NEEDS-JARON.md only for missing info).
- Bridge comes back with ONE job: X (sentiment for short-term markets, and possibly the 9 PM capture of Jaron's X posts that the
  Grok app misses replies on).
- Live Wire feels too cautious to Jaron. Fix in its instructions (next: capture them).
- Start file: YES - one short page, with pointers ("if you hit X, read Y"); everything else read only when needed.
