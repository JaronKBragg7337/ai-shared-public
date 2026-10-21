# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-10-19

Checked code.claude.com changelog, GitHub releases, anthropic.com/news, and web search for anything dated since the
2026-10-18 file in this folder (which covered four research posts and found no product changes on the 17th/18th).

- **October 17 — Claude Code, Claude's web chat/Cowork, and the API all got noticeably faster to first response.**
  Two changes: every turn's conversation is now gzip-compressed before it's sent (biggest win on long contexts/pasted
  logs), and cloud sessions now start warming up the moment you begin typing instead of after you hit send. Measured
  results: Claude Code's typical (p90) wait before the first word appears dropped from 4.07s to 1.33s (~3x), cloud
  session startup from 16.99s to 6s, web chat/Cowork from 3.36s to 2.17s, and the API from 1.53s to 1.01s.
  [AICoder writeup](https://aicoder.com/news/news-20261017-claude-code-3x-faster-first-token-gzip-cloud-prewarm) /
  [cryptobriefing](https://cryptobriefing.com/anthropic-claude-code-latency-cut/)
  for Jaron: no setup change needed — every Claude Code session on the MSI (and chat/Cowork) should just feel snappier
  starting now, especially on long sessions with lots of pasted content.

- **October 18 — Claude Code 2.1.303.** Anthropic's own release notes just say "bug fixes and reliability improvements"
  with no itemized list this time. [GitHub release](https://github.com/anthropics/claude-code/releases/tag/v2.1.303)
  for Jaron: nothing to act on — routine patch, no new feature or limit change.

- **October 18 — Anthropic Public Benefit Fund announced.** Subject to stockholder approval, Anthropic is committing
  5% of its shares (growing by 2% per 50% rise in company value, at the board's discretion) to a new wholly-owned fund
  dedicated to public benefit — on top of earlier commitments, bringing total shares earmarked for public good to
  roughly 20%. [Anthropic news](https://www.anthropic.com/news/public-benefit-fund)
  for Jaron: company governance/ownership news, not a product or plan change — nothing for us.

- **Reminder, not new: the one-time free usage-limit reset to try Claude Opus 5.5 (reported here on 10/9) expires
  October 22, 2026.** Available once to every Pro, Max, and Team subscriber. [Claude support](https://support.claude.com/en/articles/17274727-artifact-usage-promotion)
  for Jaron: if nobody's used that free reset yet on whichever plan the MSI runs, it goes away in 3 days — worth
  claiming before then, otherwise it's left on the table for no reason.

No new models, no new pricing, no new Cowork/connector/MCP/scheduled-task features found dated since October 17.
