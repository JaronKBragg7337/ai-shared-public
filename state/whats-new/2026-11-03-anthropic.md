# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-11-03

Searched for changes since 2026-11-02. No new models, plan/limit changes, promos or pricing changes confirmed. One new Claude Code release.

- **Claude Code 2.1.317 (Nov 3):** Source: https://code.claude.com/docs/en/changelog
  - `/schedule` warns when a new cloud scheduled task picks up connectors you didn't ask for, and says how to remove them.
  - Asks before a web/shell tool call sends your account email over the network.
  - Subagents on a different model than the main chat now use that model's own effort level.
  - `claude -p` now exits 1 with an error if a full disk/quota loses the transcript (before it exited 0).
  - `claude auth status` no longer risks signing you out on a slow token refresh. 62 fixes total.
  - Read tool returns file content on re-read (no more "file unchanged" stub).
  - Admin/gateway/OpenTelemetry items: not relevant.
  for Jaron: the sign-out fix and the `/schedule` connector warning are small wins for our scheduled tasks; nothing urgent.

- Unverified, not a product change: secondary sites repeat that Anthropic's IPO is planned for November. No official source confirmed.
  for Jaron: nothing for us.

Still open from before: Opus 4.8 fast mode is removed Nov 30, 2026 (move to Opus 5.5).
