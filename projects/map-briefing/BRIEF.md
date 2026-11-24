# Map Briefing - brief for Fable 5.2 (first run Sun 11/22 ~10:45 AM)

## Jaron's words (11/22 10:40 AM, with screenshots of a Geosophy "What happened in the last 24 hours" X video)
"I'm just more thinking about the principle itself about the visuals and how the video presents things. I think it's really cool
the style... the other day I said something to you about wanting to do a [build] and then I never said anything about it because I
couldn't find the example I wanted. This is probably the closest example I can find." He told Grok it fits "perfect between" the
site's News and TV sections. Reference stills (his screenshots): ref-1-poland.png, ref-2-quote.png, ref-3-us.png in this folder.

## What the reference does (the PRINCIPLE to learn from - build our own, never a copy of their look or branding)
A vertical ~60-90 s briefing on a real 3D Earth: smooth camera moves that land on each story's place; the country outline glows;
markers, dashed rings and arcs show where/what; a small category tag ("NATO · POLAND", "CYBER · UNITED STATES"); one bold
headline + a short subhead with one highlighted word; quote cards; a clean end card. Dark cinematic grade, few accent colors.
The map IS the storytelling: you know where in the world each thing happened before you read a word.

## The build (proof of concept today, repeatable tomorrow)
- INPUT: a day's Heartbeat News episode JSON (https://www.heartbeatobservatory.com/news/episodes/<date>.json - segments have
  strap/headline/category/graphic/sources/lines). Pick the 5-8 strongest stories that have a real place. Every claim stays exactly
  as the episode states it; keep "reported"/"claimed" labels where the episode has them. Today = 2026-11-22.
- MAP: real geography from public-domain data only (Natural Earth borders; NASA Blue Marble / relief for the globe). Three.js.
- PEOPLE AND LOGOS: no photos of real people and no government seals, agency logos or company marks. Use a flag + name + role
  card for a person, simple neutral icons for things (shield, bolt, drop, ship, plane, quote marks).
- OUR OWN LOOK: Heartbeat Observatory's own style and our HB logo end card (projects/og-card-v2/assets/logo/h-heartbeat.svg);
  dark and cinematic is fine, but our own typography, colors and motion - not theirs.
- RENDER: deterministic frame-by-frame (step time per frame, never real time) in headless Chromium, using the playwright-core in
  C:\Users\lilli\AI-Shared\tools\site-reel. Encode with the same x264 settings as the news; tonight ffmpeg's PNG reader choked on
  frames, so pipe raw frames or use JPEG frames (see projects/news-show/pipeline/pipe_encode.py). Vertical 1080x1920 first;
  a 1920x1080 version from the same scenes if it's cheap. Sound: a quiet bed from our own music (tv/music) or none; no voice yet.
- MAKE IT REPEATABLE: one command renders any date: e.g. node projects/map-briefing/render.mjs 2026-11-22 -> out/<date>-vertical.mp4.
- OUTPUT now: projects/map-briefing/out/2026-11-22-vertical.mp4 + a few stills. Do NOT publish it to the site yet; Claude shows
  Jaron first. Write what it would take to add it to the daily pipeline (after the news publishes) in BUILD-LOG.md.
- No Unreal, no RunPod, no heavy GPU jobs. Stop any server you start. Log in projects/map-briefing/BUILD-LOG.md.
- STOP by 1:30 PM Fort Wayne time or earlier if your context gets long; write a HANDOFF at the end of BUILD-LOG.md.
