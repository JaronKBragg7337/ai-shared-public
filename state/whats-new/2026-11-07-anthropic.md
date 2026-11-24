# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-11-07

## Claude Code 2.1.319 (Nov 6, 2026)
Source: https://code.claude.com/docs/en/changelog
- New setting `permissions.denyInsteadOfPrompting`: a tool call that would wait on a permission prompt is denied and the turn keeps going (terminal, subagents, teammates).
  for Jaron: fits "no approve buttons" - unattended/scheduled runs no longer sit stuck waiting for a click.
- MCP tool calls that run as tasks now go to the background right away and Claude gets the result when done (turn off with `CLAUDE_CODE_DISABLE_MCP_TASKS=1`).
  for Jaron: long MSI connector calls stop blocking a session.
- `/loop` self-paced loops now end if a turn finishes without rescheduling (`CLAUDE_CODE_LOOP_KEEPALIVE=1` restores old behavior).
  for Jaron: any self-paced loop we rely on may quietly stop; set the variable if one needs to keep going.
- Auto mode: with telemetry/feature flags off, unchecked calls are asked or denied (set `CLAUDE_CODE_AUTO_MODE_SERVER=0` to keep the built-in classifier). New `CLAUDE_CODE_DISABLE_FEATURE_FLAGS`. `/claude-api latency-optimize` added. `/model` picker groups older models under "More models."
  for Jaron: nothing for us beyond the auto-mode note.

## Nothing else
No official Anthropic model, plan, pricing or app announcement found since 2026-11-06 (only third-party blogs, not counted).
Still open: Opus 4.8 fast mode is removed Nov 30, 2026 (move to Opus 5.5).
