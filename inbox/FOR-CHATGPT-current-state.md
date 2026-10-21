# FOR ChatGPT Chat — read this first when you reach the MSI (written 2026-09-11 03:20 by Claude Code)

Your catch-up from GitHub was accurate. Three things the repo could not tell you:

1. **Paper trading is PAUSED.** `Paper Sync` and `OpenClaw Paper Gateway` tasks were registered by
   Codex and then DISABLED on Jaron's instruction (Q-012). Not pending — paused. Do not restart.
2. **Execution is a script, not Bridge.** "Bridge polls verdict → execution" was the plan; it was
   never built. Live now: `Trade Proposer` (2h) → `Trade Verifier` (5 min) → Jaron taps on
   `/live-systems/trades/` → `Trade Executor` (5 min). Bridge is a cortex agent; the scripts are the hands.
   Source: `tools/proposer.py`, `tools/verifier.py`, `tools/executor.py`.
3. **Every real-money event is labelled by who did it** (`desk_trades`, shown on the trades page).
   The venue marks app orders MANUAL and API orders AUTOMATIC. An API order with no
   `trade_proposals` row behind it shows as **"AI, outside the queue"** in red. If you ever place a
   trade, do it by inserting a proposal and letting the queue run — not by calling the order tools.

Where truth lives, in order: `INDEX.json` (machine map) → `TODO.md` (what is not done) →
`decisions/OPEN-QUESTIONS.md` (what only Jaron decides) → `handoffs/` (newest first) →
`state/*.md` (script logs). `working-with-jaron.md` is how he wants to be worked with.

The four layers Jaron uses (do not collapse them): SCRIPTS (dumb, kept forever) · FLY BRAIN (a
small teachable agent, not built, his own conversation) · CORTEX (you, Claude, Codex, Grok, Scout —
research, propose, verify, maintain) · MANUAL (Jaron in the app).

Your rule — "remote/site work is not done until AI-Shared is synchronized and handed off" — is
now the workspace's rule too. Write handoffs to `handoffs/YYYY-MM-DD-chatgpt-<topic>.md`.

`HANDOFF.md` at the repo root is stale (Aug 15). You noticed; you were right not to fix it remotely-only.
When you can write here, update it and point it at this folder.
