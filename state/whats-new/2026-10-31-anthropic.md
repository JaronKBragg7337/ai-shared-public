# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-10-31

Searched for changes since 2026-10-30. No new models, plan/limit changes, promos or pricing changes found. One new Claude Code release.

- **Claude Code 2.1.316 (Oct 31):** Source: https://code.claude.com/docs/en/changelog
  - **Fast mode for Opus 4.8 is deprecated (Oct 30) and removed Nov 30, 2026.** After that, fast-mode requests on Opus 4.8 return an error instead of falling back. Anthropic recommends moving to Opus 5.5.
  - New env vars: `CLAUDE_CODE_SUBAGENT_EFFORT` (effort level subagents run at), `CLAUDE_CODE_DISABLE_ULTRATHINK` (turns off the "ultrathink" keyword).
  - Cloud sessions: form card for MCP form requests; "Catching up..." line when you switch back to a session. 34 bug fixes (incl. shell commands left running after exit on macOS/Linux).
  - Team/Enterprise admin items (gateway pooled budgets, server-managed settings) - not relevant.
  for Jaron: if any script or session is pinned to Opus 4.8 fast mode, switch it to Opus 5.5 before Nov 30 or it will error. `CLAUDE_CODE_SUBAGENT_EFFORT` could cheaply lower effort for helper agents and save usage.

Nothing else new.
