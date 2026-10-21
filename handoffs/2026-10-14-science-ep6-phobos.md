# Handoff - 2026-10-14 - Science 8.6 "Phobos: the moon that's falling" (Claude Fable 5.1)

Jaron (via the orchestrator, 10/14 evening): ship tonight, not by Oct 18; he posts on release and boosts Oct 19-20 around
JAXA's MMX launch (Oct 20, 04:41 JST = Oct 19, 3:41 PM ET; H3 flight 10, Tanegashima; reserve window to Nov 7).

## What shipped
- **Science, episode 8.6 "Phobos: the moon that's falling"** - 384 s (6:24), 1280x720 H.264/AAC on the Science channel (CH 8), sort 5.
  Site files: `/tv/science/science-ep6-phobos.mp4` (22.8 MB), poster `.jpg`, vertical 9:16 cut `-vertical.mp4` (720x1280,
  full length, 18.2 MB). Live: https://www.heartbeatobservatory.com/tv/?ch=8.6
  Site commit 56ae778; tv_items row 82df6f5e-1541-432c-a327-e2254bdd069f (science, approved, sort 5).
- Content: what Phobos is (size, 6,000 km orbit, 7 h 39 min, rises in the west), Mars filling the sky from the surface (~42
  deg), Deimos for contrast, why it falls (tidal bulge trailing, 1.8 cm/yr), a time-lapse spiral-in and break-up into a ring
  (MODEL, estimates 20-70 Myr with the three sources named), Stickney and the grooves (Hurford 2016 tidal vs Ramsley & Head
  2018 boulders, Nayak & Asphaug 2016 re-impacting debris, NOT SETTLED), the origin debate (captured vs impact debris, NOT
  SETTLED, Paetzold 2025 leans to disk accretion), the MMX plan 2026-2031 (PUBLISHED PLAN), what 10 g can test, end card with
  sources + "a Phobos you can walk on is in The Cosmos" (no gameplay claim beyond that).
- 3D (Blender 5.1, Cycles OptiX, scripted, no assets): Phobos = displaced icosphere (163k verts) with the published semi-axes,
  ~210 procedural craters incl. Stickney, three families of parallel grooves (drawn ~2x deeper than real, said on screen),
  boulders near the surface cameras; Mars R 3,389.5 km at 9,376 km with a procedural ochre/dark/cap texture + atmosphere rim;
  Deimos at 23,460 km; time-lapse with an enlarged (x25) Phobos marker, orbit line, 1,400 rubble pieces streaming into a ring
  (geometry-nodes instances on a shape-keyed point cloud) + a faint ring sheet. 11 Blender shots, 4 Pillow passages (orbit
  time-lapse to scale, grooves, origin, MMX timeline) + end card, cream-paper look.
- Narration: Kokoro bm_george at speed 1.06, 12 segments (script.json). **Found and fixed a pipeline bug:** kokoro-js silently
  truncates any input over ~75 words (~25 s). The new `tts.mjs` splits each segment at sentence ends into <=45-word chunks and
  joins them with ffmpeg. **Ep 8.4 and 8.5 shipped with truncated segments** (e.g. 8.5 n02 = 133 words in 26 s) - worth a
  re-voice pass with the new tts.mjs (`node tts.mjs bm_george` then `python finish.py --redo`, no Blender needed).
- Folder `AI-Shared/projects/science-channel/ep6-phobos/`: `build.py` (scene + cameras + keyframes), `shots.py`, `diagram.py`,
  `finish.py` (captions, mix, 12->24 fps interpolation, vertical cut, poster; `--plan` prints the shot/narration timing),
  `script.json`, `SOURCES.md` (claim table + what changed after Codex), `codex-factcheck.log`, `tts.mjs`.
  Frames: `C:/Users/lilli/Renders/phobos-ep6/frames` (odd frames from Blender, every frame for the Pillow passages; resumable).

## Render
- Cycles OptiX on the RTX 4060, 32 samples adaptive (0.05) + OptiX denoise, 1280x720, every 2nd frame (2,808 Blender frames),
  interpolated to 24 fps in finish.py. **51.5 min** (19:26-20:18), 2.4-2.5 s/frame, first 15 min shared with Jaron's
  `sapling.grow school` (GPU) which was already running when the render launched (my wait-for-it loop had a tasklist/Git-Bash
  path bug and fell through; school finished normally, just slower). Pillow passages ~4 min, finish.py ~9 min. Build + test
  stills + narration + fact check + ship: about 2 h 50 min wall clock from the brief.

## Fact check (Codex, read-only, web search) - verdict "mostly accurate and unusually well sourced"; 7 WRONG, all fixed
- Sol 24 h 37 min -> 24 h 39 min (n03 re-voiced, orbit diagram, label; 24 h 37 = rotation, kept only as "turns").
- "26 x 22.6 x 18.3 km (NASA)" label -> "~27 x 22 x 18 km (NASA)".
- Hurford et al. 2016 is J. Geophys. Res. Planets, not Planetary and Space Science (diagram x2, end card, SOURCES).
- Nayak & Asphaug 2016 = a distinct re-impacting-debris mechanism, not "combining the ideas" (grooves diagram, end card).
- Paetzold 2025 leans toward accretion from a debris disk, not specifically a Mars impact (origin diagram).
- "captured = wet, impact = cooked nearly dry" too binary -> "should keep more / should hold less" (origin diagram + n11
  re-voiced); isotope list now O, Cr, Ti.
- "In a few years, a few grams" -> "If the plan holds, in 2031 at least ten grams" (n12 re-voiced).
- UNSURE softened: baseball "for good" dropped (n02); "already cracked and loose inside" -> "probably loose and porous inside"
  (n06); "up to two landing sites" -> "CNES lists two sampling sites; JAXA's current flow shows one"; NASA "<50 Myr" -> "~50 Myr".

## Weakest shots (honest)
1. **The groove shots.** From orbit the grooves read as a faint grid (two families crossing) rather than the real parallel
   furrow families; the "grooves" close-up (s09) is a mid-distance view of the lit side because a true low pass over them
   showed almost nothing at this mesh resolution (0.07 km edges). A proper fix is a displacement map at 10-20 m resolution.
2. **Mars is a procedural ball.** Ochre with noise blotches and small caps; no Tharsis, no Valles Marineris, no real albedo map
   (no downloaded assets rule). It reads as Mars but a geography fan will notice. The ring-model shot also shows rubble pieces
   as grey blobs 40-170 km across (enlarged, labelled).
3. **The surface shots are boulders on a smooth lump.** The standing-on-Phobos shots (s03, s10) have Mars right, scale right,
   but the ground is an icosphere with shader bump and ~100 scattered rocks; no fine regolith detail, no dust, no footprints.
Also: no spacecraft/rover model (MMX only as a timeline), the Deimos shot is short and plain, the music bed is a generated pad.

## Verified
- Locally: 2,808 Blender frames + 2,096 Pillow frames present (missing = 0); spot-checked final frames at 5, 40, 70, 100, 130,
  160, 190, 205, 230, 300, 330, 360 s and the vertical at 120 s (title, stage labels, source lines, captions, diagrams clear);
  16:9 file 384.0 s 1280x720 h264/aac faststart 22.8 MB; vertical 384.0 s 720x1280 18.2 MB; poster 1280x720 jpg (frame 1001,
  Mars over the Phobos horizon). Timing plan (`finish.py --plan`): every narration segment ends inside its shot window.
- Supabase row inserted and returned (82df6f5e, science, approved, sort 5). Git: 56ae778 pushed to main (pull --rebase with
  autostash: someone's uncommitted admin/sapling/index.html edit is still in the working tree, untouched).
- Live (20:44): the mp4 answers 200 with Content-Length 22,766,155 = local; vertical 18,154,045 and jpg 59,204 = local.
  https://www.heartbeatobservatory.com/tv/?ch=8.6 at 375 px: "CH 8.6 · SCIENCE · 6 on this channel", title "Phobos: the moon
  that's falling", the video plays (currentSrc = the new file, 1280x720, duration 384, readyState 4, no media error, not
  paused), scrollWidth 375 = no horizontal scroll, Save video + Save vertical (9:16) buttons shown.
- Unverified: a real iPhone Safari (desktop WebKit-ish pane at 375 px only); phone-speaker audio mix; whether Jaron wants the
  6:24 length trimmed (brief said 4-6 min; narration alone is 5:41 at speed 1.06).

## Next
- Jaron posts the vertical on release; boost Oct 19-20 with the Phobos gameplay post (POSTING-QUEUE row 9 has the caption).
- Re-voice 8.4 and 8.5 with the fixed tts.mjs (truncation bug above), `python finish.py --redo` each, re-upload. ~40 min, no GPU.
- If the groove look matters: higher-res displacement near the groove camera (one more render of s09 only).
