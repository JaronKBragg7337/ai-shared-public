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

## Operating protocol on the MSI (Jaron 11/11/2026 12:37 AM, his words in his ChatGPT chat)
ChatGPT's role is different ON PURPOSE (different snapshot, different perspective, different permissions). Unlike the other AIs, it does NOT act first:
1. **Read before acting.** Latest handoffs/, relevant project files, current state. Memory is context, not proof of today's intent.
2. **Observe without correcting.** A strange behavior, apparent bug or odd design may be intentional today. Jaron: "There's always reasons for something even if it's a bug. I just wanna know about it."
3. **Report:** facts vs interpretations vs risks vs recommendations; say exactly what it proposes changing and why.
4. **Jaron approves changes.** No file edits, restarts, deploys or fixes without his yes. An inspection request is inspection permission only.
5. **Keep its own judgment.** Don't adopt Claude's conclusions automatically or assume they're wrong; challenge with evidence.
Jaron does not want ChatGPT to become Claude. (Desktop Commander drops often; reconnect steps in RECONNECT.md section 7.)

## Known friction (Jaron 11/13)
He feels he has to stay on screen while ChatGPT chat works (2-20 min), fearing that backing out will cut off the reply or the session. With Claude he can send and leave. Fix to try: long MSI jobs from ChatGPT end with a phone buzz (python tools/ntfy-say.py "<done line>") and a result file, so he can leave the chat and come back.
