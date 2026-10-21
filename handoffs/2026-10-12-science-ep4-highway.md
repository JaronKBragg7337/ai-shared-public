# Handoff - 2026-10-12 - Science 8.4 "How a highway disappears" (Claude Fable 5.1)

## What shipped
- **Science, episode 8.4 "How a highway disappears"** - 254 s (4:14), 1280x720 H.264/AAC on the Science channel (CH 8), sort 3
  after the three existing science episodes. Files in the site repo: `/tv/science/science-ep4-highway-disappears.mp4`, poster
  `.jpg`, vertical 9:16 cut `-vertical.mp4` (720x1280, full length, letterboxed over a blurred copy, captions under the picture).
- One stretch of a central-Indiana interstate (3+3 lanes, paved shoulders, grass median, storm-drain inlet, exit sign, guardrail,
  tree lines, concrete overpass) seen from the same seven camera positions as a single STAGE number runs 0 -> 6:
  year 0 clean / first summer (unmowed shoulders lean over the edge line) / first fall (leaf litter, the drain buried) /
  first winter (snow, overcast, bare trees) / years 2-5 (cracks + moss, thin soil, puddles, the hero pothole, grass creeping in)
  / years 5-20 (shrubs and saplings, paint gone, sign rusting and leaning, burrow at the shoulder, grass fire mentioned not shown)
  / years 20-50 (young forest over the lanes, slabs heaved, rebar out of the spalled overpass).
  Mid-episode: a 34 s Pillow cutaway "What one winter does to a crack" (road layers, water, freeze, thaw, cycle counter with an
  ESTIMATE tag, then the two mechanisms side by side: 9 % expansion vs ice growth fed through liquid channels, Style et al. 2023).
  Cream-paper look, not the navy cards (monetization guard: own visuals per episode).
- Narration: Kokoro bm_george, 11 segments (script.json). Captions, stage labels (YEAR 0 ... YEARS 20-50+) and a source line per
  stage burned in with libass; every timeline number is spoken and shown as an estimate. End card lists the sources.
- Everything is script-built in `AI-Shared/projects/science-channel/ep4-highway-disappears/`: `build.py` (Blender 5.1 scene:
  procedural asphalt shader with paint/cracks/moss/dirt/water, shape-key potholes + heave + puddles, geometry-nodes grass /
  leaf litter / saplings, blob trees, sign, drain, overpass; a param table P maps STAGE to every material and modifier),
  `shots.py` (the shot plan shared by build/diagram/finish), `diagram.py` (Pillow passages), `finish.py` (captions, mix,
  12->24 fps interpolation of the Blender runs, vertical cut, poster), `SOURCES.md` (claim-by-claim table), `codex-factcheck.log`.
  Site commits 2bff21b / 05e09a1 / 1855527; tv_items row 767b51cd-3eff-4e8c-a508-fcc1baaf7f6b (science, approved, sort 3).
  Frames: `C:/Users/lilli/Renders/highway-ep4/frames` (odd frames from Blender, every frame for the Pillow passages; resumable).

## Render
- Cycles OptiX on the RTX 4060, 32 samples adaptive (0.06) + OptiX denoise, 1280x720, 24 fps timeline. Blender rendered every
  second frame (2,496 frames) and finish.py motion-interpolates to 24 fps (slow pans, nothing swaying - clean). 2,496 frames in 3 h 01 min (10:31-13:32; 2.9 s/frame at year 0, 4-6 s/frame once the
  grass is tall and the saplings are in). Pillow passages ~2 min, finish (interpolation + encodes) ~10 min.
  Transparent bounces 256 (the bare winter canopies went black at 48 - deep tree lines exhaust it).

## Weakest shots (honest)
1. **The trees.** Canopies are displaced icospheres with noise holes; at tree-line distance they pass, but the years 5-20 shrubs
   on the lanes read as green boulders and the sign shot sits under one. A real tree generator (Sapling add-on / particle leaves)
   is the fix; framed as far as the story allowed.
2. **The spalling overpass.** Noise-masked flakes with rust streaks and rebar rods: reads as "damaged concrete" but the flake
   edges are soft; close-up (shot 16) would benefit from real displacement.
3. **The winter trees** are brown twig stubs through 50 % holes - honest (bare) but thin; and the leaf litter is flat pentagons
   (fine from the drain camera, cardboard-ish in the lane close-up).
Also: the grass is one clump mesh scaled, no wind; the burrow is a mound and a hole; no animals shown (narrated only).

## Fact check
Codex read-only fact check (`codex exec -s read-only ... "Fact-check SOURCES.md and the script"`): most claims CONFIRMED (Pripyat 8,980 seedlings/ha, 9 % expansion, the 2023 ice-growth paper, asphalt 20-yr design life, paint life, rust volume 2-6x, AASHTO 75 yr, Heyne 11/30 yr, Kleinschroth 4/20 yr, Pripyat empty since 1986). Four WRONG, all fixed before shipping: "every road already has hairline cracks" (now "the small cracks a road a few years old already has"), "each swing works the crack open" (now "each one that catches water in the crack"), "fire ... saplings come back stronger" (now species-dependent: sumac resprouts, young cottonwood often does not), and the author order of the 2023 paper (Gerber, Wilen, Dufresne & Style, PRL 131, 208201 - not "Style et al."). UNSURE items (the 25-40 cycle count, early potholes, 50-year endpoint, pavement "not by much") were softened and are spoken/shown as estimates; the 25-40 count is still the weakest number in the script (no published Indianapolis count found - Purdue's tool exists but its page gives no values). Full log in the episode folder; Codex's one-line verdict: core mechanisms and case-study numbers sound, the Indiana timelines are estimates.

## Verified
- Locally: all 2,496 Blender frames + 1,104 Pillow frames present, no render errors; spot-checked frames at 5, 50, 100, 110, 150,
  176, 230, 249 s of the final (titles, stage labels, source lines, captions clear of the diagram); 16:9 file 254.0 s 1280x720
  h264/aac faststart 56.5 MB; vertical 254.0 s 720x1280 29.4 MB; poster 1280x720 jpg.
- Supabase row inserted and returned (767b51cd, science, approved, sort 3). Git: 1855527 pushed to main (GitHub warns the
  mp4 is 53.8 MB > its 50 MB recommendation; it pushed fine, same as earlier big episodes).
- Live (14:05): /tv/science/science-ep4-highway-disappears.mp4 -> 206 video/mp4, 56,502,698 bytes = local; vertical and jpg
  206 too. https://www.heartbeatobservatory.com/tv/?ch=8.4 at 375 px: tunes to "CH 8.4 · Science · 4 on this channel", the
  video plays (currentSrc = the new file, 1280x720, duration 254, readyState 4, no media error, not paused), no horizontal
  scroll, guide lists 8.1-8.4.
- Unverified: a real iPhone Safari (only the desktop-app WebKit-ish pane at 375 px); phone-speaker audio mix; the vertical cut
  is in the repo but not linked from any page.

## r2 (same day, after Jaron watched it - he loved it)
- Cutaway labels brought in line with the corrected narration: "Each swing that catches water works the crack a little wider."
  (was "Every swing works the crack a little wider and deeper."), and the "Below 32 F: ice grows..." label now appears only while
  the thermometer reads below 32 F (same for the thaw label, >= 32). Only diagram.py + finish.py re-run; same file names
  re-uploaded (landscape + vertical), site 7e4c0bd; verified live by byte size (56,501,648) and 206 range replies.

## r3 (10/13, vertical only)
- 9:16 title card relaid: the two-line title ("How a highway / disappears") was drawn over the italic subtitle. finish.py now
  lays the vertical title card separately (kicker higher, explicit two-line title, subtitle three lines below at 30 px).
  Checked the other cards: stage label + source line sit in the top blur band, captions below the picture - no overlaps.
  `python finish.py --vertical-only` (no Blender, no landscape re-encode); same file name overwritten; verified live by byte size.

## Next
- If Jaron likes it: Earth channel (CH 17) seed is used; the next "what reclaims" episode could be a house or a parking lot with
  the same scene machinery (build.py's P table + shots.py are reusable).
- Trees: try Blender's Sapling Tree Gen (bundled add-on, scriptable) for the lane saplings before the next outdoor episode.
