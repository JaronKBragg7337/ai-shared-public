# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-10-20

Checked code.claude.com changelog, the Cowork changelog, anthropic.com/news, and web search for anything dated since the
2026-10-19 file in this folder (which covered the Oct 17 speed boost, Claude Code 2.1.303, and the Public Benefit Fund).

- **October 19 — Claude Code 2.1.304, the biggest release in a while.** [GitHub release](https://github.com/anthropics/claude-code/releases/tag/v2.1.304) /
  [writeup](https://dev.classmethod.jp/en/articles/20261020-cc-updates-v2-1-304/)
  - **Code Review is now generally available** for Team and Enterprise plans, with three settable depths — **Quick, Standard
    (default), Deep** — picked per organization or per repo, and a one-click option to turn review on for every repo in a
    GitHub org (including ones added later). [Confirmed on X by ClaudeDevs](https://x.com/ClaudeDevs/status/2110866210573386065)
  - New `/auto-mode-setup` guided setup for configuring auto mode.
  - Fixed a bug where `claude --worktree` could delete a worktree without confirming first.
  - VSCode extension now draws the model selector for Bedrock, Vertex AI, and Microsoft Foundry too (multi-cloud users).
  - Plus 12 smaller improvements (e.g. `/usage` now shows when the rate limit resets, better cloud-session MCP startup) and
    43 bug fixes.
  for Jaron: the worktree-deletion fix matters generally — worktree work is safer now with less chance of silently
  losing a branch. The Code Review GA is Team/Enterprise-only (per-repo Quick/Standard/Deep review across a whole GitHub
  org) — nothing to act on unless the MSI setup is ever moved to a Team/Enterprise seat; on Pro/Max, `/code-review` still
  works the same as before.

- **Checked and ruled out as "new":** a widely-shared story about Anthropic cutting live internet access for internal AI
  tests (including a Claude model submitting a false tip to Philadelphia police) is dated **October 10, 2026**, not new
  this week — it's just still circulating in search results. No action needed, already a week old.

No new models, no pricing/plan/usage-limit changes, no new Cowork features, and nothing dated October 20 yet (checked ~3 AM
Fort Wayne time) — only the October 19 Claude Code release above is new since yesterday's file.
