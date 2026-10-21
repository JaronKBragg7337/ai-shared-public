# Codex → Claude Code: paper wiring, 2026-09-10

Paper agent/profile: polymarket-paper. Display label: PAPER ONLY — Polymarket Simulator.
Separate OpenClaw gateway planned at loopback 19789; live gateway/config untouched.
MCP server key: polymarket-paper; tool prefix polymarket-paper__.
Data root: C:\Users\lilli\AI-Shared\tools\paper-trader\data
Account: default; SQLite path data\default\paper.db.

IMPORTANT independently verified mismatch: installed source ignores PM_TRADER_HOME;
CLI recognizes PM_TRADER_DATA_DIR, but MCP hard-codes ~/.pm-trader. Requested data folder
was empty; database exists at C:\Users\lilli\.pm-trader\default\paper.db.
Codex is fixing both CLI/MCP to honor PM_TRADER_HOME and preserving the original database
through SQLite backup into the requested root, without reset or trades. Dashboard must
use the explicit root above, not the old implicit home. No financial state copied here.

No live credentials/configs touched. Dashboard remains yours. Do not start an autonomous
trading loop during this wiring task: Jaron explicitly said not to trade anything.

COMPLETE: gateway 19789 healthy; AtLogOn task OpenClaw Paper Gateway running; MCP probe
confirmed 30 tools; 629 non-live tests pass. SQLite backup complete and original retained.
Source patch committed locally f4c5da1 (not upstream). Qwen successfully used tool_search
after an initial hallucinated-name failure. Full evidence and limits are in
handoffs/2026-09-10-codex-paper-agent.md. No dashboard fields/schema prescribed by Codex.
