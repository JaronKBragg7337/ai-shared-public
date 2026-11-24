# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-10-23

Checked the Claude Code changelog, platform.claude.com release notes, anthropic.com/news, and web search for anything
dated since the 2026-10-22 file in this folder (which covered Claude Duet's launch and the new versioned API
2026-10-21).

- **October 22 — Claude Code 2.1.309: bypass-permissions mode now blocks `rm`/`rmdir` instead of asking.**
  [Changelog](https://code.claude.com/docs/en/changelog)
  In the Desktop app and VS Code, when a session is running in bypass-permissions mode (no approve prompts) and hits
  a dangerous `rm`/`rmdir`, it used to stop and ask. Now it refuses the command outright and gives a rewrite hint,
  so an unattended session keeps going instead of hanging on a prompt nobody's there to answer. Also: `claude
  ultrareview` now needs "workspace trust" to run (asks once on a terminal, or scripts must pass `--trust-workspace`
  or set `CLAUDE_CODE_DISABLE_ULTRAREVIEW_TRUST_CHECK=1`); worktree git clones no longer fetch objects one-by-one on
  demand; the dataviz skill now also checks APCA text-contrast, not just WCAG; the `/claude-api` skill can manage
  OpenTelemetry destinations with service-account keys now, and builds Managed Agents teams on the newer
  `multiagent_20261001` setup by default.
  for Jaron: the `rm`/`rmdir` change fits exactly how this crew runs — unattended AIs with bypass permissions never
  get stuck waiting on a delete prompt that never comes, they just skip the delete and move on. No script of ours
  calls `ultrareview` headlessly today (checked), so that trust-check change doesn't break anything here, but if
  anyone ever automates it, it'll need `--trust-workspace`.

- **October 22 — Claude Models on Google Cloud (Anthropic-managed) + Opus 5.5 fast mode there.**
  [Platform release notes](https://platform.claude.com/docs/en/release-notes/overview)
  A new way to reach the Claude API billed and access-controlled through a Google Cloud project instead of
  Anthropic's own console, with Opus 5.5's fast mode now available there too.
  for Jaron: nothing for us — this setup runs on Anthropic's own API/console, not Google Cloud Marketplace billing.

- **October 22 — Anthropic donated Agent Skills (the Skills standard) to the new Agentic AI Foundation.**
  [Anthropic news](https://www.anthropic.com/news)
  The open format behind Skills (what this setup's `.claude/skills/` folders use — code-review, runpod, dataviz,
  etc.) moves from an Anthropic-owned spec to a neutral foundation; 70+ tools including ChatGPT, Cursor, GitHub
  Copilot and VS Code already read the same format.
  for Jaron: nothing to change now — just means the skills we've already written are more likely to keep working
  the same way even if we move work to a different AI tool later.

- **Checked and ruled out:** the Anthropic IPO-filing story and the reported $80B first-half loss (both circulating
  today) are business/finance news, not a product change — skipped per this scout's scope. No new model, no
  Cowork feature, no plan/pricing/usage-limit change dated since October 21.

Nothing urgent. The bypass-permissions `rm` fix is the one worth knowing about; everything else is "nothing for us"
or already covered.
