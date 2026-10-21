# Claude Chat (phone app) — agents/claude-chat/

**Who:** Jaron's Claude app on his phone (Haiku 4.5 / whichever model he picks). Not Claude Code.

**How it reaches this workspace:** custom connector **"Heartbeat MAI"** (his typo for MSI) →
`https://mcp.heartbeatobservatory.com/mcp` → the Heartbeat Machine MCP on the MSI (49 tools:
PowerShell, files, processes, screen, Ollama). Added 2026-09-11 02:20. Same route Grok Bot uses.

**What it should and should not do:**
- Read anything here. Write to coordination surfaces (inbox/ state/ handoffs/). Check the desk.
- **Never place a Polymarket order directly.** It has the shell, so it *could* call the local
  MCP's order tools. An API order with no proposal behind it shows on the public ledger as
  **"AI, outside the queue"** in red. If it wants a trade: insert a `trade_proposals` row and let
  the queue run, or use `tools/desk-trade.py --by claude-chat ...` which leaves a trail.
- Anthropic policy for Claude here: build, verify, monitor — not execute trades (OPERATING-MAP.md).

**Start with:** `INDEX.json` → `TODO.md` → `handoffs/` newest first.
