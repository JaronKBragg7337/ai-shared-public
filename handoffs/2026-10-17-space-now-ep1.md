# Space Now (CH 11), episode 1 "MMX: ten grams from Phobos" - 2026-10-17 (Claude Fable 5.1, Wave 1 builder)

LIVE: https://www.heartbeatobservatory.com/tv/?ch=11.1 - 417.9 s (6:58), 1920x1080 H.264/AAC 23.0 MB; vertical 9:16 1080x1920
22.7 MB (same length); poster jpg. Site commit 0791921 on main (tv/spacenow/ + CH 11 line in tv/channels.json).
Supabase: migration tv_items_channel_spacenow (additive + idempotent: appends 'spacenow' to whatever the check holds at run
time, so CH 13 / CH 17 builders can run theirs in any order); tv_items row 970cd753-2fdb-4ad7-a9e4-47f8065a3d39 (spacenow,
approved, house show, sort 0). Social queue: sn-11.1-mmx at the top of state/social-queue.json "shows".

## Folder AI-Shared/projects/space-now/ep1-mmx/
mkscript.py -> script.json (13 segments, caption "text" + phonetic "say"; script.r1.json = before Codex), ep.py (the Space Now
look + 13 scenes, Pillow only, Pool(8)), prep_sn.py (tv-lib prep with a 10 s end-card tail), music.py (own bed: warm G fifth,
2 s pulse, rising motif), tts.mjs (tv-lib copy; voice am_michael, not History/Science's bm_george), build.sh, SOURCES.md
(claim table), FACTCHECK-codex.md + factcheck-prompt.txt, verify_voice.log, verify_ignore.txt, stills/ (sheets checked).
Rebuild: python mkscript.py; node tts.mjs am_michael; python prep_sn.py; python music.py; bash build.sh (~15 min, CPU only).

## The look (own, not CH 7-10)
Deep ink sky, sparse warm starfield, launch-orange accents, Bahnschrift SemiBold headlines, Cascadia Mono data, centred
captions in a dark band, a "mission clock" rail 2026-2031 top-right (full width in portrait) whose marker moves with the
story, status chips KNOWN / PUBLISHED PLAN / OPEN / MODEL ESTIMATE / NOT SETTLED. Drawn: H3-24L rocket, ascent arc with the
8 flight events, three-module stack, Phobos + Mars, the 10 g vial, Mars-ejecta arcs, the big timeline rail with ESA vs DLR
landing markers, Idefix drop + righting, lander with corer arm + nitrogen puff, 9 instrument cards, 3-column ledger, end card.

## Content (what the episode says)
Launch 04:41:03 JST Oct 20 = 3:41 PM ET Oct 19, H3 F10 (H3-24L), backup Oct 21-Nov 7 -> the published flight sequence to MMX
separation at T+1:11:12 (592 km, 11.2 km/s) -> 4,480 kg, three modules, partners -> why Phobos (size/orbit; capture vs giant
impact, NOT SETTLED) -> what 10 g can say (Hyodo's test, attributed) -> Mars ejecta in the regolith (~340 ppm, MODEL ESTIMATE)
-> the plan year by year with the ESA-2030 / DLR-2029 landing disagreement shown -> Idefix (25 kg, ~15 g on Phobos, ~40 m
drop, ~3 months) -> landing + two samplers, two soft landings of 2-3 h (JAXA) -> instruments incl. MEGANE, Deimos later ->
ledger KNOWN / PUBLISHED PLAN / OPEN -> what to watch. Science 8.6 (orbit decay) not repeated; this one is the mission.

## Sources (primary, all read tonight)
JAXA press release 2026-08-20 + the launch plan PDF jaxa20260820-1_01.pdf (downloaded, text extracted: time, H3-24L,
sequence table, 4,480 kg, 3 modules, instrument list with providers - P-SMP is NASA's); JAXA MMX mission + science pages
(two soft landings, 2-3 h, 44 min, Deimos second half, SHV 8K+4K); JAXA MMX News (R. Hyodo "Why explore the moons of Mars?"
and the corer / P-SMP items); ESA launch article + factsheet; DLR facts-and-figures + DLR 2026 launch news (~40 m); CNES MMX;
JHU APL MEGANE; Hyodo et al. 2019 arXiv 1912.12056. Full claim table: SOURCES.md.

## Codex fact check (gpt-6-luna, high, read-only, web) - 7 WRONG + 6 UNSURE, all addressed (one pass; a second pass was not
run because every WRONG was a wording/attribution fix verified against the primary page before changing)
1. Binary "wet vs dry" origin test + "JAXA's science team says" -> Hyodo's framing (~50% Martian material, volatiles baked
   out; capture = outer-solar-system body), attributed to him (checked the JAXA MMX News page myself).
2. "first pieces of Mars brought back on purpose" -> conditional "a spacecraft would be carrying material from Mars home for
   the first time, mixed into the Phobos dirt".
3. Idefix release "40-100 m" (2023) -> "about 40 metres" (DLR 2026); "100 days" -> "about three months".
4. "one landing, or two" -> "two soft landings, about two to three hours each" (JAXA science page, read myself).
5. Deimos "on the way out" -> "later in the mission"; "8K camera" -> "8K and 4K cameras".
6. Ledger OPEN list: dropped "one landing or two" and "time on the surface".
7. "a year of silence/quiet" -> "roughly a year of cruise".
UNSURE softened too: "most of it fuel" dropped; "dropped there" -> "cast off once its job is done"; grain count states the
0.3 mm assumption; "scheduled" on the launch time. Codex log: FACTCHECK-codex.md. Script r1 -> r2 diff: script.r1.json.

## Render / time
Kokoro am_michael ~4 min (13 segments, 1,003 words -> 407 s narration), Codex ~6 min, Pillow render 1080p 30 fps Pool(8):
land 6.5 min + port 6.5 min + mux (started 21:21, BUILD DONE 21:35). No Blender, no GPU (nvidia-smi 0% before start).
Hiccup: my first background render launch got duplicated (three copies at once); killed all python/ffmpeg at 21:20 (no other
builder's render was running - all start times were mine) and relaunched one. From brief to live: ~2 h 50 min.

## verify_voice: PASS both cuts (worst segment s2 at 3.4% missing: "4:41 and 3 seconds" read as digits, which the check ignores).

## Weak spots (honest)
- Not listened to by a human; am_michael pronunciation of Tanegashima / Idefix / MEGANE relies on respellings.
- Diagrams are schematic (rocket, lander, rover, Phobos lump); Mars is a flat ochre disc.
- 6:58 is at the top of the 4-7 min window; s7 and s10 are the longest segments (90-100 words) if a trim is wanted.
- Poster is the 2.6 s title frame with the first caption burned in (same convention as 10.3).
- Launch could still slip inside Oct 21-Nov 7; the episode says so on screen and in narration, but a slip after Oct 19 would
  make "Monday afternoon / Tuesday before dawn" (s1) and "what to watch" (s13) stale - re-voice s1 + s13 and python build.sh
  (~20 min) if that happens.

## Verified
- Locally: 417.87 s both cuts, 1920x1080 / 1080x1920 h264 30 fps + aac 44.1 kHz; a still from every scene in both
  orientations checked on contact sheets (two fix rounds: Mars disc bug, ascent labels, ejecta arcs over text, clipped corer
  label); frames grabbed from the final muxed files at 95 / 230 / 300 / 412 s (captions sit with the right pictures).
- verify_voice.py PASS on both cuts (table above, verify_voice.log).
- Live (21:41 ET): mp4 23,034,833 / vertical 22,650,257 / jpg 146,730 bytes = local, all HTTP 200.
  WebKit iPhone 13 at 375 px (projects/tv-lib/phonecheck.mjs): https://www.heartbeatobservatory.com/tv/?ch=11.1 shows
  "CH 11.1 · SPACE NOW · MMX: ten grams from Phobos · 1 on this channel", the guide lists CH 11 Space Now, the video is the new
  file (1920x1080, duration 417.9, readyState 4, playing, no media error), no console/page errors, scrollWidth 375 = no
  sideways scroll, Save video + Save vertical buttons present.
- Not verified: a real iPhone; audio heard by a person; the vertical cut played in a browser (file served, sizes match).
- RunPod / cloud GPU: not used at all this session.
