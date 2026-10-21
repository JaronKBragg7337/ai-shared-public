# Codex — PAPER ONLY OpenClaw integration, 2026-09-10

## Installed and running

- Agent/profile `polymarket-paper`, display name `PAPER ONLY — Polymarket Simulator`.
- Separate gateway `127.0.0.1:19789`, separate config/state/session directory
  `C:\Users\lilli\.openclaw-polymarket-paper`, separate workspace beneath that directory.
- MCP registry key `polymarket-paper`, namespaced tools `polymarket-paper__*`.
  Command: `C:\Users\lilli\AI-Shared\tools\paper-trader\.venv\Scripts\pm-trader.exe mcp`.
- `PM_TRADER_HOME=C:\Users\lilli\AI-Shared\tools\paper-trader\data`;
  default account database `data\default\paper.db`. Claude dashboard must read THIS path.
- AtLogOn task `OpenClaw Paper Gateway`, MSI\lilli interactive, battery allowed,
  unlimited execution time, IgnoreNew, 999 one-minute failure retries. Launcher waits
  for Ollama API and supervises clean gateway exits (OpenClaw's config-restart mechanism).
  No Startup shortcut. Stdio MCP is a client-owned child, started on demand, not a daemon.
- Own persistent local gateway authentication token; no live token or credentials copied.
  Do not publish the profile config. Automatic heartbeats disabled; no autonomous trading
  prompt/loop created. Existing shared Ollama is used without changing its configuration.

## Independently corrected storage mismatch

Installed version 0.1.8 ignored PM_TRADER_HOME; CLI used PM_TRADER_DATA_DIR and MCP
hard-coded ~/.pm-trader. The requested data folder was empty. Patched CLI/MCP to honor
explicit paper root, including multi-account lookup, and preserved the original SQLite
database with SQLite backup. Original `C:\Users\lilli\.pm-trader\default\paper.db`
retained. No account reset, funding, or user-account trade was performed.

Local source commit `f4c5da1` in tools/paper-trader/src, Codex attribution, MIT retained.
Not pushed to upstream. 629 non-live tests passed, 42 live tests deselected. Three new
root-selection tests added. An upstream reinstall could overwrite this local patch.

## Verified locally

- OpenClaw config validation; direct MCP handshake and OpenClaw MCP probe both found
  30 simulator tools (OpenClaw additionally synthesizes four resource/prompt helpers).
- Tool policy removed exec/read/write/session/gateway tools from the paper agent. Only
  paper tools remain behind OpenClaw search/describe/call. This is application-level
  separation, NOT an OS sandbox: both services still run as the same Windows user.
- Paper /healthz and Ollama API respond; paper task running. check-paper.ps1 passes.
- Live ports 8765, 18789, 11434 healthy; postboot-check.ps1 passes. Live config SHA256
  unchanged before/after: D7D2997AB5F9C2CA6094E5A0D0D37F1BEE3D4A36EFA27131FA9AA41B6A43239E.
  No live agent configuration, identity, scheduled task, source, or service was modified.
- Qwen inference tested without execution tools. First test hit paper gateway restart
  and used embedded fallback. Qwen invented names: `buy_market`, `sell_market`,
  `resolve_market`, and confused its session UUID with agent ID. Corrected paper-only
  tool notes to describe actual discovery. Second test completed via gateway, made one
  successful `tool_search` call, zero failures, and said exactly:
  "The exact discovered tool name is: **polymarket-paper__get_tags**".
  Do not erase the first failure or extrapolate reliability from the second success.

## Boundaries and next owner

Remote verification: none; this wiring is MSI-local. Simulator market-data APIs are public
network reads, not "no market contact". No dashboard or live site changes by Codex; Claude
Code owns that work and has inbox/FOR-CLAUDE-paper-agent-paths.md.

Unverified: new paper task across an actual reboot; model-driven fills, execution accuracy,
slippage/performance, unattended behavior, and the dashboard. Jaron explicitly said not to
trade anything, so no observation run was started. Start a paper session only on his next
explicit direction. Record market estimates/positions outside shared coordination memory.

Separate configuration was chosen to meet the no-live-config-change constraint. No shared
layout was moved. INDEX.json records this addition. To inspect without repairs, run
tools/paper-trader/check-paper.ps1 and existing tools/postboot-check.ps1.
