# AI budget report - 2026-10-19 07:15 ET (tools/ai-budget.py)

Step 1 of Jaron's plan (9/29): measure cost, usage and output per AI next to what the trader earns. Step 2 (after ~1-2
months of data): the report recommends next month's plans. Step 3: the system pays and changes plans itself.

## Money

- Monthly bills on record: $214 (Claude (Anthropic) $100, ChatGPT / Codex (OpenAI) $20, Grok (xAI) $30, Kimi $39, Supabase $25)
- Trader's settled profit this month: -$27.30
- Target (Jaron): Claude >= $100 plan, ChatGPT/Codex >= $100 plan, Grok next tier up (or highest), + Supabase $25, Cursor $6

## Each AI this month

| AI | plan | usage (latest) | commits this month |
|---|---|---|---|
| Claude | Max $100 $100 | 66% of the week (estimate from local logs) | 7273 |
| Codex | Plus $20 $20 | 16% of the week (meter), resets 2026-10-25 | 1005 |
| Grok | SuperGrok $30 | 0% of the week on 2026-10-01 (reset 6:34 PM ET (weekly reset; on-demand $15 test was one-time) (Jaron screenshot 3:45 PM said resets in 2h49m)) - Jaron's reading | 0 |

Commits by model: Claude Sonnet 5.5 4792, Claude Opus 5.5 1714, Claude Fable 5.1 690, Grok Build 4.7 456, Codex GPT-6.1 Sol 380, Codex GPT-5.6 Luna 304, Codex GPT-6 Luna 228, Codex 93, Claude Opus 5 39, Kimi k2.5 38, Grok Build 38, Claude 38

## What the numbers say (automatic, plain rules)

- Codex is at 16% of its week: lots of room left - point more work at it before paying for more.
- Grok is at 0% of its week: lots of room left - point more work at it before paying for more.

Grok Bot's own usage is not readable by a script; add each reading to state/grok-usage.md.
