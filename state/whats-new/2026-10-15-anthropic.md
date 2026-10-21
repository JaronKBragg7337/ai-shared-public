# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-10-15

Checked code.claude.com changelog, anthropic.com/news, support.claude.com, and web search for anything dated since the 2026-10-14 file in this folder. Haiku 5.5, the Mods plugin system itself, the Cowork cloud move, and the Max-plan API credits are all older (Oct 1-7) and already logged in earlier files — not repeating them here.

- **October 14 — Claude Code 2.1.300.** The same day as the 2.1.299 idle-compaction release already logged yesterday, Anthropic shipped a second build (2.1.300, 59 bug fixes) that expands the Mods plugin API: mods can now draw text in the prompt box that never enters the actual prompt (`virtualText`), show an agent's transcript in the main view, react to prompt text changing without a typed edit (recalled history/undo/plugin fill), rewrite prompts inside `agent.spawn` for workflow agents, read bytes of attached images/documents, and read session sign-in/org/email via `$.session.identity()`. [Claude Code changelog](https://code.claude.com/docs/en/changelog)
  for Jaron: this is plumbing for people writing their own Claude Code plugins, not something to use directly — the one piece worth knowing is `$.session.identity()`, which means a mod could in theory check which login a session is on. No action needed.

- **October 15 — Claude Docs, Slides, and Design turn on by default today** for anyone who hadn't already enabled them. Flagged as upcoming in the Oct 12 file; it's now live. [Anthropic support](https://support.claude.com)
  for Jaron: nothing to do — these are already out of beta and just stop requiring a manual toggle. Worth knowing if a page/slide-builder feature ever shows up unprompted in a Claude chat.

No new models, no plan/usage/limit changes, no pricing changes, and no new Cowork-specific features found since the 14th.
