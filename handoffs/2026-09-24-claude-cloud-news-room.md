# HANDOFF — Heartbeat News (the news room): live

- **Date/time:** 2026-09-24 ~19:45 ET
- **From:** Claude (Claude Code cloud session; AI-Shared, MSI live checks and the Windows task through the Heartbeat MAI connector)
- **Project:** projects/news-show  |  **Repo/branch:** JaronKBragg7337/heartbeat-observatory @ main (bbda093, 7f1b9dc)  |  **Live URL:** https://www.heartbeatobservatory.com/news/

## What I did
- **/news/**: its own page with a TV set; inside, a Three.js newsroom built in code: curved 3.0 m anchor desk (top 0.80 m) with an
  LED fascia, 7 x 3 m LED wall (14 x 6 cabinets of 0.5 m) showing each story's graphic, portrait monitors (world clocks, channel
  mark), hologram globe, pillars, truss with nine fresnels and haze, night skyline. Floor mirror on desktop only.
- **Anchors**: AI Robot Vex (panelled robot, visor face, LED-bar mouth, antenna, VX-01 decals, tie plate) and Alien Joe (big-cranium
  alien in a suit and tie). Mouths follow the voice (measured from the audio for the synth, from word timing for device voices),
  blinks, eye darts, head turns to the camera or the co-host, small hand gestures.
- **Shots**: crane open, wide, two-shot, singles, cross angles, wall shot; mid-line cuts on long lines; the wall goes out of focus
  behind singles (fake depth of field).
- **Broadcast package** (own brand, "HBN / Heartbeat News" - not Fox's marks, per AGENTS.md "don't import a reference's
  branding"): lower thirds with the story's SOURCES under the headline, name bars, BREAKING slam, over-the-shoulder box, stingers,
  ticker, ET clock, "ON AIR" bug (not "LIVE": it is a loop), captions (CC), full screen, Grid & IDs debug layer (asset IDs, metres).
- **Show**: loops all day and tunes in by the clock like a channel; the next day's episode swaps in at the next story break (page
  polls every 10 min). A "From the wires" segment is built on the page from the live Perplexity headlines (/api/news).
- **Tonight's episode**: news/episodes/2026-09-24.json from codex + deepseek + claude captures of 9/24: 14 stories, ~10 min.
- **Voices (free)**: Vex = eSpeak rendered in code in a Web Worker (vendored meSpeak, GPL) through a studio chain: robot ring-mod,
  metal comb, bit crush, radio, echo, bass/presence/treble, and "size" (formant, via render-then-resample). Joe = the device's own
  speech voice (natural, varies by phone). SAM was NOT used: its copyright holder still exists, status unclear.
- **Voice Studio** (admins only, is_admin()): per-anchor channel strip: engine, device voice, character, pitch, speed, volume, size,
  tone, effects, and look (colours). Live preview, Test voice, Save for everyone -> news_anchor_settings.
- **Home page**: "News" tab in the nav (stays visible on phones), hero button, directory row (added by the page even without a DB row).
- **Daily writer**: Claude cloud routine trig_01EnWaDLFxBZjQVYZmCNKjCT, daily 9:40 ET, follows news/WRITER.md, runs
  news/tools/check-episode.mjs, pushes to main. Backup: Windows task "Heartbeat News Writer" 10:20 on the MSI
  (projects/news-show/run_news.ps1) - skips at no cost if the episode is already on main; otherwise runs claude -p and pushes.

## Where it lives (exact)
- Repo: news/ (index.html, news.css, show.js director, studio3d.js scene, voices.js + voice-worker.js, studio-panel.js, episodes/,
  WRITER.md, tools/check-episode.mjs, vendor/), index.html (tab), supabase/news-anchor-settings-APPLY-ME.sql.
- AI-Shared: projects/news-show/2026-09-24-news-anchor-settings.sql, run_news.ps1, runs.log.
- MSI checkout used by the backup task: C:\Users\lilli\Projects\heartbeat-observatory.

## Verified vs assumed
- Verified live (MSI, real site, headless): desktop Chromium 46 fps, 0 errors; tap for sound -> Vex's synth rendered in the worker,
  played, mouth level 0.2-0.95 following it; Android (Pixel 7 profile) 60 fps, 0 errors, Joe's device voice spoke with his mouth
  moving; iPhone profile (WebKit): page, studio, rundown, ticker, clock all up, no sideways scroll at 390 px, 0 errors. Home page
  tab + hero button + directory row on all three. Backup task's "already written" path ran and logged.
- Verified locally (cloud Chromium, software GL): every shot framed, graphics, captions, synth path.
- NOT verified: sound on a real iPhone (the Windows WebKit test build has no Web Audio and no voices; the page now keeps the show's
  pace when a device can't make sound); real-iPhone frame rate (Windows WebKit draws in software, 6 fps there); how the voices
  actually SOUND - no one has listened yet; the routine's push to main (first run 9/25 9:40) - if refused, the MSI backup covers;
  the backup's claude -p path; admin Save (needs the SQL).

## Blocked / needs a human
- SQL above -> Claude Code on the MSI applies it (Supabase MCP). Until then the Voice Studio can't save for everyone.
- Jaron: listen and tune the voices in the Voice Studio (sign in as admin, the Studio is under the rundown). Open questions stay
  open: tone (straight vs comedy; tonight is straight with character), paid voices later.

## Exact next step for the next AI
- Apply 2026-09-24-news-anchor-settings.sql; then 9/25 after 9:40 check that news/episodes/2026-09-25.json landed on main and
  runs.log says why if not.

## 2026-09-25 follow-up: Vex's first words low and quiet (commit 83ef6d2, live)
- Measured before changing anything: eSpeak output and the whole effects chain are level from the first word (first 1.2 s vs
  rest of each line 0.082/0.082 and 0.090/0.085; compressor ~0.3 dB). No gain or effects ramp in our code.
- Cause (most likely, not reproducible without a real phone): the device voice (Joe) makes phones duck the page's audio and
  fade it back after; Vex usually starts right after Joe, inside that fade. Every Vex line also called speechSynthesis.cancel()
  on an idle engine.
- Fix: Vex's lines only cancel the device voice if it is actually busy; a synth line waits until the device voice is idle and
  700 ms past its last line (about +0.25 s pause after Joe, nothing after Vex) and resumes the audio context if suspended.
  Joe's code path is byte-identical.
- If Jaron still hears it on his phone: compare the Voice Studio "Test voice" for Vex (no Joe before it). Full level there but not
  in the show = still the device fade -> raise DEVICE_RELEASE_MS in news/voices.js. Low there too = something on that phone's
  Web Audio path; next step is testing on that device.
