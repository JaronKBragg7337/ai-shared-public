# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-10-14

Checked code.claude.com changelog, anthropic.com/news, support.claude.com release notes, and general web search for anything dated October 13-14, 2026. Prior files in this folder (through Oct 12) said "nothing new" — these are genuinely new since then.

- **October 14 — Claude Code 2.1.299.** New in this release: idle compaction for long conversations (200K+ tokens) — it auto-compacts BEFORE the prompt cache expires instead of after, so a long-running session loses less context on reconnect. Also new: `/effort` and `/fast` commands to set session defaults from the agent view, a safe-mode indicator in the agents peek panel, `CLAUDE_CODE_DISABLE_FILE_MENTIONS` env var, `CLAUDE_CODE_ATTRIBUTION_HEADER` env var to control the commit attribution block, plus 16 improvements and 131 bug fixes (Windows, MCP, plugins, cloud sessions). [Claude Code changelog](https://code.claude.com/docs/en/changelog)
  for Jaron: the idle-compaction change is the one that matters here — Claude Code sessions (like this one) that sit open for weeks should now hold onto context better across idle gaps instead of losing more of it when the cache lapses. No action needed, it's automatic.

- **October 13 — Anthropic published "Redesigning Source Control at Anthropic": they built their own version control system, Scion, to replace Git internally.** Daily code merges from Claude went from ~2,500/day in May to 30,000+/day by September — git couldn't keep up because it assumes offline-capable clients, while Scion assumes an always-connected server that agents hit for history/blame/merges via API instead of a local checkout. Closed-source, internal only, not released. [Anthropic engineering blog via search coverage]
  for Jaron: nothing for us directly — it's Anthropic's own internal tooling, not something available to use — but it's a real data point on how fast agentic coding volume is scaling at Anthropic itself.

- **October 14 — Anthropic opened a Singapore office and signed an MOU with the Singapore government.** Business/international-expansion news, not a product change. [Anthropic news](https://www.anthropic.com/news)
  for Jaron: nothing for us.

- **October 14 — Anthropic held a pre-IPO investor day for Q3 financials**, part of reported IPO preparation (no confirmed listing date). Not a product change.
  for Jaron: nothing for us, just background — worth knowing Anthropic is moving toward a possible IPO, no action needed.

No new models, no plan/usage/limit changes, no pricing changes, and no new Cowork-specific features found since Oct 13.
