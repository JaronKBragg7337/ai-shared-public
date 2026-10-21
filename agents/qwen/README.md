# Qwen (local model) — agents/qwen/

**Who:** `qwen3.5:4b` on Ollama at `127.0.0.1:11434`, on the MSI. The only agent bound by no third
party's terms. Jaron's rules only: no lawbreaking, no substantial deletion without his approval.

**How it reaches this workspace:** it doesn't, on its own. A harness runs its tool calls:
- `python tools/qwen-bridge.py "<question>"` — list/read/write inside AI-Shared (writes to
  inbox/ state/ handoffs/ logs/ events/ projects/ by default; see Q-002 before narrowing).
- `runtime/polymarket-us-agent/remote_bridge.py` (task `Qwen Remote Bridge`) — the persistent
  OpenClaw agent behind `/qwen` on the site. Currently `run_enabled=false` (idle by design).
- `tools/proposer.py --researcher qwen` — usable as a research backend. Tested 2026-09-11:
  answers everything, rates everything "medium", always finds a trade. Not the default.

**Role:** OPEN — Jaron decides (TODO #2). Idle-by-design is fine; idle-by-neglect is not.
Do not assign it the fly brain; that is Jaron's own conversation.

**Quirks:** thinking mode eats the whole output budget on long prompts (`think: false` +
`num_ctx 8192` in proposer.py). Misread order books 2026-09-10 (0.01 vs 0.11). Tool results
must carry `tool_name` or it drifts (fixed in qwen-bridge.py).
