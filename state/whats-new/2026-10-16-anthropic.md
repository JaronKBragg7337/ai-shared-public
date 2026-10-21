# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-10-16

Checked code.claude.com changelog, GitHub releases, anthropic.com/news, and web search for anything dated since the 2026-10-15 file in this folder (which already covered Docs/Slides/Design going default on the 15th). No new entry dated the 16th yet — it's early morning Fort Wayne time.

- **October 15 — Claude Code 2.1.301** (51 changes). Worth knowing: a "Get more usage" link now shows right in the usage-limit banner on Pro/Max plans; context-window switching got automatic conversation summarization (less lost when a long session flips models); LaTeX math now renders in VS Code; a new env var (`CLAUDE_CODE_RETRY_WATCHDOG_MAX_USAGE_LIMIT_WAIT_MS`) lets unattended/headless runs give up on a request instead of waiting out a far-off usage reset; plus OpenTelemetry additions and 37 bug fixes (worktrees, model aliases, disk-space errors, rendering). [Claude Code changelog](https://code.claude.com/docs/en/changelog) / [GitHub release](https://github.com/anthropics/claude-code/releases/tag/v2.1.301)
  for Jaron: the retry-watchdog env var matters for any unattended/scheduled Claude Code run (like this scout job or other automated tasks on the MSI) — it stops a headless session from sitting frozen waiting for a usage reset that's hours away. Nothing to change today; flagging it since routine/cron-style jobs are exactly where this would bite.

- **October 15 — Anthropic published "An update on independent evaluators."** METR now has staff-level access inside Anthropic (office space, systems, tools) to assess frontier models and will publish its own risk-assessment results; SecureBio and Accenture are also evaluators, more in talks (including Hugging Face). Ties back to the White House Accord on Super Intelligence Anthropic signed. [Anthropic news](https://www.anthropic.com/news/an-update-on-independent-evaluators)
  for Jaron: not a product change, nothing to do — just governance/safety-oversight news from Anthropic itself.

No new models, no pricing changes, and no new Cowork-specific features found since the 15th.
