# Brief for every Wave 1 episode builder (Claude Code, 2026-10-17 9 PM)
You are building the FIRST episode of a NEW Heartbeat TV channel, end to end, and shipping it live. No human approval step.

Read first (copy their method, they are the proven pipeline):
- projects/heartbeat-tv/CHANNEL-PLAN.md (channel rules) and LAUNCH-SLATE-2026-10.md (your line)
- handoffs/2026-10-16-still-unknown-ep3.md + projects/still-unknown/ep3-vibration-stone/ (Pillow + Blender loops, build.sh)
- handoffs/2026-10-12-open-questions-ep1.md (how a NEW channel was added: site guide, Supabase tv_items row, the channel check
  migration widened) and handoffs/2026-10-14-science-ep6-phobos.md
- projects/tv-lib/ (build.sh, tvlib.py, tts.mjs Kokoro voices, verify_voice.py)

Must-haves:
1. Script: accurate, sources on screen, disputes labeled, claims vs established clearly separated, both sides where real.
   Never branded as Jaron's idea. 4-7 minutes. Its own channel look (like CH9 and CH10 each have one), warm and readable.
2. Fact-check gate: send the script to Codex before rendering:
   codex exec -m gpt-6-luna -c model_reasoning_effort=high -s read-only --skip-git-repo-check -C <your ep folder> "<fact-check prompt + script>"
   Fix every WRONG it finds (cite what you changed in your handoff). A second pass if it found more than 3.
3. Render: prefer Pillow/CPU. The GPU is shared - NO Blender/GPU renders between 2:45 AM and 7:30 AM (the daily news is filmed
   in Unreal then). Kokoro voice, then python projects/tv-lib/verify_voice.py must PASS before shipping.
4. Outputs: 16:9 mp4, 9:16 vertical cut (letterbox over blur, captions under the picture, like the others), poster jpg.
5. Ship: put files under the site repo tv/<channel-folder>/ (C:\Users\lilli\Projects\heartbeat-observatory), add the channel +
   item exactly the way CH9/CH10 were added (guide + Supabase; Supabase project ygjpnvrwhkrowkrskftk, service key in
   ~/.secrets/keys.env - names only, never print values). OTHER BUILDERS ARE ADDING CHANNELS TONIGHT: make any constraint/migration
   change additive and idempotent; `git pull --rebase` right before every push; touch only your own files + the shared guide lines.
6. Check it LIVE at phone width (iPhone WebKit, e.g. node with C:/Users/lilli/.codex/runtime/unfinished-island/node_modules/playwright):
   heartbeatobservatory.com/tv/?ch=<n>.1 plays, no errors, no sideways scroll.
7. Add it to the TOP of C:\Users\lilli\AI-Shared\state\social-queue.json "shows" (same fields as the others: id, title, file =
   the vertical path, caption in the house template - hook question + emoji, 1-2 sentences, "Full episode + sources, free:
   heartbeatobservatory.com", "Made with AI by Heartbeat Observatory · <Channel>, Episode <n>.1", hashtags, done: {}).
8. Write handoffs/2026-10-1X-<channel>-ep1.md (what shipped, sources, Codex fixes, render time, anything weak) and append one
   line to state/timeline.md. Mark your line LIVE in LAUNCH-SLATE-2026-10.md.
NEVER kill processes by name (no `taskkill /IM python.exe`, no killing all python/ffmpeg/node): the MSI runs Sapling's
heartbeat, the Polymarket trading service and other builders as python. Kill only PIDs you started yourself.
Never: post to social media yourself, touch games, touch Sapling, leave a cloud GPU on, put a ?tag on any shared link.
Report back: live URL, length, Codex fixes count, verify_voice result, anything you could not finish.
