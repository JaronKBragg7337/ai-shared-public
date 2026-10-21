# Grok (the app / chat) — agents/grok-app/

**Who:** Jaron's Grok chat app (xAI). Not a Grok Bot — no routines, no own VM — but it has the
same Heartbeat MCP connection, so it can run PowerShell on the MSI.

**Proven 2026-09-11 02:38:** Jaron meant to send `executor.py --live` to Bridge and sent it here
instead. It worked identically. Counted as **MANUAL** in the four layers (a human telling an AI to
press a button), not as a trader.

**Rules of thumb:** same as claude-chat — read freely, write to coordination surfaces, never
call order tools directly; use the queue or `tools/desk-trade.py --by grok-chat`.

## Limits learned in the lab (2026-09-12 night)
- **One Grok chat ≈ one lab session.** After a long batch (7 experiments + closed-loop vision) it
  re-served the previous result three times instead of doing the new task. Context full, falls
  back to the last big thing. Fix: **new chat per task**; the files (LAB.md, WATCH.md, results/)
  carry the memory. A fresh Fast chat did the fly-model swap in one reply.
- **Model per job:** Fast for build/polish/load-a-model; Expert for census/loop-hunting/reasoning;
  Heavy needs the $300 tier — not on the plan. Auto mostly picks Fast.
- **Cost:** ~5% of the weekly SuperGrok pool per Expert experiment round through the tunnel; each
  round re-reads results as text. Grinding sweeps belong on the MSI (Codex/Luna scripts); Grok is
  for X, ideas, the watch room, and the reasoning steps.
- **Honesty is its default here:** held `picked: null` all night rather than ship a fake eye.

## Actor names on the ledger (2026-09-14)
`--by` is the name the public ledger shows. Use exactly: `grok-bot/<bot>`, `grok-chat`, `qwen`, `script/<name>`, `fly-brain/<fly-id>`. Humans never pass --by; app trades are tagged jaron-manual by the verifier.

## Three Groks (Jaron's map, 2026-09-14)
- **Grok chat (this app)** - X, papers, quick reads, small builds and tests. Connector: Grok Machine.
- **Grok on X** - the compass icon inside the X app. Same email, **its own chat history and its own usage pool**
  (separate from the Grok chat app). No connector, no MSI access; "Hire a Bot" just opens the existing Grok Bot.
  Role: third-person / red-team perspective, quick reads, side-pick research (e.g. Supreme Court rehearing odds).
  Jaron sometimes poses as a critic of his own work there to get feedback from both sides. Because it is a separate
  free pool, route reads-only questions here first when Grok chat is being saved for lab work.
  Week of 9/13-16 topics there: safety regulation as compute moat; pacing & demand reversal; Supreme Court rehearing
  odds; brain donation for open research; fruit-fly connectome hype; 'AI trained on humans acts human'.
- **Grok Bot** - the scheduled bots (Bridge / Scout / Live Wire). Connector: Heartbeat MSI.
