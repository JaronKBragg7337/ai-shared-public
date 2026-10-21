# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-10-17

Checked code.claude.com changelog, GitHub releases, and anthropic.com/news for anything dated since the 2026-10-16 file in this folder (which covered Claude Code 2.1.301 and the independent-evaluators post). It's early morning Fort Wayne time, so today is thin — one release landed late on the 16th that the 10-16 file missed.

- **October 16 — Claude Code 2.1.302** (70+ changes). Worth knowing: fork subagents (background subagents that don't block your main conversation) are now ON by default on all platforms; a new env var `CLAUDE_CODE_AUTO_MODE_MODEL` lets you pick which model runs the client-side auto-mode classifier; `/config` got an idle-compaction toggle; images over 128 MB are now refused instead of silently eating memory; and `/design-sync` / `/design-login` now show a notice that **standalone Claude Design is closing December 14, 2026**. [Claude Code changelog](https://code.claude.com/docs/en/changelog) / [GitHub release](https://github.com/anthropics/claude-code/releases/tag/v2.1.302)
  for Jaron: the Design shutdown notice is the one to flag — if any AI on the crew has used standalone Claude Design (separate from Docs/Slides, which stay) for site graphics, that workflow goes away Dec 14. Nothing to do today, just don't build a new habit around standalone Design. Everything else is background plumbing, no action needed.

- **October 16 — Anthropic research post: "Claude reveals ECDSA curve origins."** A research writeup, not a product change — Claude helped work out historical origins of some ECDSA cryptographic curve parameters. [Anthropic research](https://www.anthropic.com/research/ecdsa-curve-origins)
  for Jaron: nothing for us — pure research post, no app/API change.

No new models, no plan/usage/limit changes, no pricing changes, and nothing dated October 17 yet (checked ~3 AM Fort Wayne time).
