# Handoff - 2026-10-13 - Science 8.5 "How a commercial roof dies" (Claude Fable 5.1)

## What shipped
- **Science, episode 8.5 "How a commercial roof dies"** - 313 s (5:13), 1280x720 H.264/AAC on the Science channel (CH 8), sort 4.
  Site files: `/tv/science/science-ep5-commercial-roof.mp4` (22.7 MB), poster `.jpg`, vertical 9:16 cut `-vertical.mp4`
  (720x1280, full length, 17.4 MB). Live: https://www.heartbeatobservatory.com/tv/?ch=8.5
  Site commit d270eaf; tv_items row 2d91a048-3937-4b3c-acb4-f44711775688 (science, approved, sort 4).
- One Indiana warehouse, two roofs side by side from the same eight camera positions as a STAGE number runs 0 -> 5:
  an older pre-engineered metal building (gable 1:12, exposed-fastener Galvalume-type panels with real rib geometry and ~2,700
  geometry-nodes screws that back out, rust, get replaced/encapsulated and coated) and a flat addition with a white single-ply
  membrane (seams every 10 ft, dirt/chalk/algae, ponding in a birdbath low spot and around a clogged drain, fishmouths,
  punctures, cracked curb flashing, RTUs on curbs, dome strainers, pipe boots, gas line on sleepers, walkway pads, hatch,
  parapet, scuppers, wall flashing at the gable). Plus a small interior under the deck for the stain/drip shot.
  Stages: year 0 / years 1-5 / years 5-15 / the leak (overcast, wet) / restoration steps (wash, patch, screws, primer, fabric)
  / coated white.
- Three Pillow passages in the cream-paper look (own visuals per episode = monetization guard): "One summer day on an
  exposed-fastener metal roof" (air vs panel temperature, the 40 ft panel growing/shrinking, the screw hole wearing oval,
  5,500 cycles = arithmetic), "Where the water goes" (cutaway: membrane / cover board / 2x polyiso / steel deck / bar joist,
  water spreading, R-value meter with ESTIMATE tag, deck rust, ceiling stain), "Why the coating is white" (reflectance bars
  new/aged/dark with ranges, DOE 150 F vs ~50 F cooler thermometers, what it buys). End card lists sources.
- Narration: Kokoro bm_george, 13 segments (script.json). Captions, stage labels (YEAR 0 ... AFTER RESTORATION) and a source
  line per stage burned in with libass; every lifespan/timing spoken and shown as a typical range or estimate. Generic product
  types only (metal, TPO/PVC/EPDM, silicone/acrylic); no employer, no brand recommended.
- Folder `AI-Shared/projects/science-channel/ep5-commercial-roof/`: `build.py` (Blender 5.1 scene, param table P), `shots.py`,
  `diagram.py`, `finish.py` (captions, mix, 12->24 fps interpolation, two static shots stretched to fit the re-voiced
  narration, vertical cut, poster), `script.json`, `SOURCES.md` (claim-by-claim table + what changed after Codex),
  `codex-factcheck.log`, `tts.mjs` / `tts-some.mjs`. Frames: `C:/Users/lilli/Renders/roof-ep5/frames` (odd frames from Blender,
  every frame for the Pillow passages; resumable).

## Render
- Cycles OptiX on the RTX 4060, 32 samples adaptive (0.06) + OptiX denoise, 1280x720, every 2nd frame (2,508 Blender frames),
  interpolated to 24 fps in finish.py. **About 75 min of actual GPU time** (1.0-1.4 s/frame on the close-ups and the coated
  stage, up to ~8.7 s/frame on the stage-2 hero shots with the semi-transparent ponds). Wall clock 03:30-07:34 because the
  **MSI idle-slept for ~2 h 50 min** (frames stop 04:11, resume 07:00) - keep-awake was requested for the session afterwards;
  next long render: request keep-awake before launching. Pillow passages ~3 min, finish.py 15 min. Well under the 3.5 h budget.

## Fact check (Codex, read-only, web search) - 9 WRONG, all fixed before shipping, incl. on-screen labels and diagrams
- "An exposed-fastener roof cannot" accommodate movement -> "most exposed-fastener roofs have no allowance for it" (some
  through-fastened systems use factory-slotted holes). Also in the heat diagram.
- "Rust around every hole" -> "around the holes where the washers have failed"; screw-rust explanation -> plain zinc-plated vs
  long-life fasteners (narration + YEARS 5-15 label).
- "Two choices / depends on one thing" -> patch, recover, coat or replace; a coating depends first on moisture, then deck,
  adhesion, drainage (narration + THE CHOICE label).
- "Every loose screw gets a larger one" -> tighten or replace; oversized where holes wore out. "Each screw head ... fabric" ->
  heads sealed over; laps, seams, penetrations reinforced, often with fabric. "Two coats" -> one or two by product.
- IBC citation -> 2018 s.1511.3.1 / 2021 s.1512.2.1 (label, end card, SOURCES).
- 0.55 aged reflectance described as a value used by some programs, not "the standard" (SOURCES only).
- UNSURE softened: "dozens of feet" -> "well beyond the hole"; "wet for years" -> "wet for a long time"; "adds 10-20 yr" ->
  "carries a 10-20 yr warranty" and the last label is AFTER RESTORATION (was YEARS 15-35); EPDM ~15-30 yr "sources vary widely";
  "usual leak points" -> "common"; "most acrylics need positive drainage".
- Codex verdict: mostly sound and well-qualified; revise the absolutes above (done). Seven segments re-voiced.

## Weakest shots (honest)
1. **The restoration steps read as colour changes, not work.** Washing is dirt fading, priming is grey spots, the patch is a
   faint square near the drain, the coating is a white wipe; no crew, no sprayer, no cut-out. The fastener shot does show the
   backed-out screws straighten and the sealant blobs appear, but the fabric strips on the laps are subtle.
2. **The membrane damage is small on screen.** Fishmouths are a 40 cm white tab seen from 5 m; punctures are dark dots near
   the RTU that only read in the curb shot; the curb cracks are voronoi lines on the flashing (and the parapet base flashing
   gets the same crack pattern in the hatch shot, which looks like a cracked wall).
3. **Backgrounds are placeholder.** Blob trees, white box warehouses on the horizon, a plain lot; the interior is a bare room
   with one rack, the stain is faint and the droplet is tiny.
Also: no people anywhere (narrated service tech only); the metal roof is one Galvalume tone (no paint chalking option);
the ponds are flat glossy planes (no ripple, no tide-line debris).

## Trade claims Jaron should eyeball (he is the roofer)
- Exposed-fastener screws in the flats at purlin lines 12 in o.c. along the panel, purlins 5 ft apart; end lap at mid-slope on a
  ~49 ft eave-to-ridge run; gable 1:12 on a pre-engineered building; box gutters + downspouts; ridge cap.
- "Plain zinc-plated screw heads often rust before the panel does; long-life fasteners hold up better."
- Thermal movement: 1/4 in per day / 1/2 in per year on a 40 ft panel (ΔL = 6.5e-6 x 480 in x ΔT; labelled estimate).
- Membrane: 10 ft rolls, seams along the long axis, one end lap; 60 mil; cover board over two staggered polyiso layers on steel
  deck; drains in tapered sumps with cast-iron dome strainers; a birdbath away from the drains; 1/4:12 design slope; NRCA 48 h.
- Fishmouths at seams, punctures from HVAC service near the unit, curb flashing cracking at corners; condensate line to a
  splash block; gas line on sleepers; walkway pads hatch -> units.
- Restoration order: IR survey after sunset + core cuts -> wet areas cut out and replaced -> drains cleared -> power wash ->
  screws tightened/replaced (oversized where wallowed) -> wire-brush + rust-inhibiting primer -> heads sealed, laps/seams/
  penetrations reinforced with fabric in sealant -> adhesion test -> silicone or acrylic at 20-40 mils dry (10-20 yr warranty).
- Silicone tolerates ponding but is not shown as dirt-attracting/slippery; acrylic "needs a dry roof and warm weather to cure".
- "Usually for well under the cost of a tear-off" (no number given); "a maintained roof can be coated again".
- The "<25 % wet" line shown as a rule of thumb; coating cannot fix wet insulation, deck damage or slope.

## Verified
- Locally: 2,508 Blender frames + 2,256 Pillow frames present (missing = 0); spot-checked final frames at 5, 50, 70, 120, 160,
  185, 215, 240, 260, 300 s and the vertical at 100 s (titles, stage labels, source lines, captions clear of the diagrams);
  16:9 file 313.0 s 1280x720 h264/aac faststart 22.7 MB; vertical 313.0 s 720x1280 17.4 MB; poster 1280x720 jpg.
- Supabase row inserted and returned (2d91a048, science, approved, sort 4) - first attempt failed the note length check
  constraint; shorter note used. Git: d270eaf pushed to main (pull --rebase clean).
- Live (07:53): the mp4 answers 206 video/mp4 with Content-Length 22,700,562 = local; vertical 17,390,623 and jpg 53,529 = local.
  https://www.heartbeatobservatory.com/tv/?ch=8.5 at 375 px: "CH 8.5 · Science · 5 on this channel", the video plays
  (currentSrc = the new file, 1280x720, duration 313, readyState 4, no media error, not paused), scrollWidth 375 = no
  horizontal scroll, Save video + Save vertical (9:16) buttons shown.
- Unverified: a real iPhone Safari (desktop-app WebKit-ish pane at 375 px only); phone-speaker audio mix; the vertical cut is
  only reachable through the Save vertical button.

## Next
- Jaron's accuracy pass on the trade list above; anything he flags = edit script.json/finish.py labels, re-voice the segment
  (`node tts-some.mjs nXX`), `python finish.py --redo` (no Blender needed unless the scene changes).
- If a crew is wanted in the restoration shots: MetaHuman/Blender people are the realism rule (realistic-characters memory);
  that is a new build, not a tweak.
