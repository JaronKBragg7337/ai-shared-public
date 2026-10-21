# ChatGPT Chat (phone / web app) — agents/chatgpt-chat/

**Who:** Jaron's ChatGPT app, GPT-5.6 Sol. Owns **Habitat** (`/live-systems/habitat/`) and the
Habitat iPhone 3D fix — deliberately its own; do not touch (see PARKED in TODO.md).

**How it reaches this workspace:** Desktop Commander Remote — `https://mcp.desktopcommander.app`,
device **MSI**, scheduled task `Desktop Commander Remote` (registered 2026-09-11 03:21). Tools load
per conversation; if they are missing, start a fresh chat. Also has GitHub, Drive, Supabase, Vercel
connectors — GitHub is canonical for site code; this folder is the coordination layer.

**Its own rule, adopted by the workspace 2026-09-11:** *remote/site work is not "done" until the
corresponding AI-Shared state is synchronized and handed off.* Handoffs go to
`handoffs/YYYY-MM-DD-chatgpt-<topic>.md`.

**First read:** `inbox/FOR-CHATGPT-current-state.md` (three corrections to what the repo says).

**Usage:** Sol has a rolling 5-hour window plus weekly caps. Jaron called it "basically unlimited";
it is generous, not free. Good for long research passes.

## Measured 2026-09-13 — what ChatGPT Chat (GPT-5.6 Sol) can be delegated
- **Separate usage pool** from Codex/ChatGPT Work (Astra). Do not accept its "hand to Work" offer — that pool is shared
  with Codex.
- **Can:** 20–27 min connector sessions on the MSI; read Fly-Lab/AI-Shared; design a sound experiment on its own (froze
  the ground with a SHA-256, match-level holdout, flat = no dopamine, watcher-v1 valence as built-in control, causal
  replay on recorded timestamps); refuse to infer numbers from partial runs. Owns `C:\Users\lilli\Fly-Lab-2`.
- **Cannot:** keep a process alive past its session. Its two ground_school.py runs (started via Desktop Commander) never
  executed — venv stub at 0 CPU. Claude Code relaunched the identical command detached (`Start-Process … -WindowStyle
  Hidden`, stdout to results\*.log). **Rule: long runs it designs get launched by Claude Code or a scheduled task; it
  designs and analyses.**
- **Quirks:** a finished message may lack the bottom buttons (copy by selecting); long-reasoning prompts timed out
  during the 9/9–9/13 OpenAI capacity crunch — lower the reasoning setting for reads.
- **Patience rule (Jaron, 2026-09-13 14:45):** it will show "Streaming interrupted", "Reasoning failed", or sit on
  "Thinking" looking dead — and then a complete message lands 13–27 minutes later. Wait 20–40 min before assuming a run
  is lost or re-sending. Re-sending mid-run is what creates duplicates.
- **Posture test (Jaron, 2026-09-13 18:00, X-app Grok/ChatGPT chat):** on the pacing draft, ChatGPT's caution level
  tracked whether the thesis threatened frontier-model economics, not the evidence — defensive until a line kept frontier
  models "what small systems are for," then supportive. It acknowledged this when shown. Its own rule, keep it: a
  correction with a competing explanation is substance; "soften that" without one is posture. Jaron's rule: the factual
  corrections inside a defensive message are still corrections — keep the substance, discard the posture. **Applies to
  Claude too (Anthropic wrote the pacing letter): watch for the same shift.**
