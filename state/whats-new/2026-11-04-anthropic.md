# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-11-04

Searched for changes since 2026-11-03. No new models, plan/limit changes, promos or pricing changes found. One new Claude Code release.

- **Claude Code 2.1.318 (Nov 4):** Source: https://code.claude.com/docs/en/changelog
  - `claude auth status` shows when your claude.ai sign-in expires; `claude -p` JSON includes `credential_expires_at`; a warning prints starting 10 days before the sign-in ends.
  - Cloud sessions: new "No repository" option starts a cloud session on an Anthropic-hosted environment without picking a repo.
  - Background subagents push a shell command to the background after 3 minutes (keeps prompt cache alive).
  - `--continue` no longer loses earlier conversation after a malformed tool call's retries run out.
  - Claude Code no longer auto-installs the IDE extension from an IDE terminal (use `/ide`).
  - Gateway/AWS/mods items: not relevant.
  for Jaron: the sign-in expiry warning helps our headless scheduled tasks avoid a surprise logout; "No repository" cloud sessions are handy for quick research jobs.

Still open from before: Opus 4.8 fast mode is removed Nov 30, 2026 (move to Opus 5.5).
