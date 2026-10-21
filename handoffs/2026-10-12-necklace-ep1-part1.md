# Handoff - 2026-10-12 - The Necklace, Episode 1 Part 1 shipped to Heartbeat TV (Claude Fable 5.1)

## What shipped
- **"The Necklace · Ep. 1 Rum and Regret in Rosetown · Part 1"** - 116 s, 1280x720 H.264/AAC, on the Shows channel
  (tv_items id d58d859f-fe9d-4d12-8361-d586e61b307c, approved, house show). File: `/tv/shows/necklace-ep1-part1.mp4`,
  poster `/tv/shows/necklace-ep1-part1.jpg`, vertical 9:16 cut `/tv/shows/necklace-ep1-part1-vertical.mp4` (720x1280, 116 s,
  letterboxed over a blurred copy, captions under the picture - for Shorts/TikTok, not on TV).
- The opening of chapter 1, the book's own text: narration = the first three paragraphs + "He gestured with his glass toward the
  open doorway..." (Kokoro bm_george, speed 1.0, same setup as the TV episodes); dialogue = lines 1-4 from the locked Chatterbox
  cast (Jalen am_michael seed, Mateo am_onyx seed + pitch/EQ). Captions for everything, titles at 2.5-9.5 s, end card with
  "From the book by Jaron Bragg · Part 2 follows".
- Shots: 1 exterior from the water (the Rusty Anchor on pilings, string lights, tin roof) - 2 room wide from the street door -
  3 Jalen with the sweating glass, focus pulls to his face - 4 pilings + water, low - 5 track past the patrons to Jalen - 6 Mateo
  walks in from the door (over Jalen's shoulder) - 7 two-shot from behind the bar - 8a/8b over-the-shoulder listener shots for
  lines 1-3 - 8c the wide along the bar for the "gestured toward the doorway" line - 9 the open doorway, bruised twilight, sea.
- Everything is script-built: `AI-Shared/projects/necklace-film/ep1/` (build.py, audio.py, finish.py, script.json, tts_narr.mjs,
  caps.ass). Frames at `C:/Users/lilli/Renders/necklace-ep1p1/frames` (2784 png, resumable). README in necklace-film/ updated.

## Render times
- Blender 5.1, Cycles OptiX on the RTX 4060, 64 samples adaptive + OptiX denoise, 1280x720, 24 fps. 2784 frames in 4 h 11 min
  (2.2 s/frame exterior, 4-6 s/frame interior with the haze volume). Scene build ~90 s. Kokoro narration ~1 min, finish ~6 min.

## What looks weakest (honest)
1. **Faces in the listener close-ups (8a Jalen profile, 8b Mateo profile)** - the Loft people are the phone-weight LOD (1024 px
   face textures, no face rig): skin reads flat up close and no mouth moves. Framed around it (dialogue plays on the listener,
   the wide and the doorway) but it is still the ceiling of this cast. Fix = export the real Jalen MetaHuman (Unreal lane,
   needs the Epic sign-in + the SM6 bake we solved 9/27) with a face rig, or a higher-LOD glb export from loft_people.py.
2. **Mateo's beard** - the Goatee helmet mesh reads as a grey blob under the lip in the two-shot (7). Darkened to 0.35, still
   a blob. Needs a card/groom beard or a different preset.
3. **The pilings cutaway (4)** - pilings are plain dark cylinders under a black dock, the water is the only thing moving; it
   reads as a mood plate, not a real harbour. Also the back-bar bottles are plain coloured lathes with white labels when a
   shot gets close (3). Both are set-dressing passes (`sets/rusty_anchor.py`).
Also: Jalen is isaiah (lean, beard, short hair) with the skin lifted toward the decided medium tone - close, not the approved
Jalen render (u .58 v .48). Bodies sit with legs hidden behind the counter on purpose (no sit-down animation exists).

## Verified
- Locally: all 2784 frames rendered, no errors in the log; the mp4 is 116.0 s 1280x720 h264/aac faststart (18.2 MB), the
  vertical cut 116.0 s 720x1280 (10 MB); captions/titles checked on burned stills (title card, narration, dialogue, vertical).
  Spot-checked frames 750, 1000, 1720, 1900, 2400 of the final render.
- Supabase row inserted and returned. Git: commit fd6506f pushed to main.
- Live: see the end of this file (filled in after the deploy check).

## Next part
- **Part 2 = Jalen's story** (lines 5-11: the picket fence, Maya and Leo, the Sea Serpent, "running is the only way") - same
  scene, same scripts: add the lines to CUES in finish.py, new head keys in build.py, re-render only the shots that change.
  The warm flash of Maya and Leo's faces (bible: the only memory imagery in Ep 1) needs two more people (a 17-year-old and an
  8-year-old - the Loft presets are adults; the 8-year-old is the hard one, flagged in the README).
- Part 3 = lines 12-13 (the warning), paying, stepping out into the humid night, end on the dark sea.
- Before Part 2: 20 min on the beard and the bottles; and test exporting one higher-LOD person from loft_people.py.

## Live check (04:35, after the Vercel deploy)
- https://www.heartbeatobservatory.com/tv/shows/necklace-ep1-part1.mp4 -> 206 video/mp4 (range requests work); poster jpg 200.
- https://www.heartbeatobservatory.com/tv/?ch=2.4 at 375 px: tunes to "CH 2.4 · Shows · 4 on this channel", the video element plays
  (1280x720, duration 116, no media error, readyState 4), title and poster frame visible. Listed in the on-screen guide.
- Unverified: real iPhone Safari (only the desktop-app WebKit-ish pane at 375 px); the audio mix on phone speakers; the vertical
  cut is in the repo but not linked anywhere yet.
