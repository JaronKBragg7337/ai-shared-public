# Turkey Trouble (Thanksgiving game) - where it stands. Fable, Thursday 11/26/2026

Kept current by Fable while building. If you pick this up cold, read this page, then `games/turkey-trouble/CONTRACT.md`.

## The ask (Jaron, through Claude, Wed 11/25 11:42 PM)
A Thanksgiving turkey game on heartbeatobservatory.com/games/, live by Thanksgiving afternoon (v1 by about 2 PM Thursday,
keep polishing after). His bar: "whatever can make it look the best, the most polished production looking thing." Four modes:
Find the Turkey, It Hunts You, You Hunt It, Escape the Farm (you are the turkey). Secret ending (his oldest son's joke):
the last road leads to a little house with the sign "The Dummy's House"; the turkey knocks; the screen shows exactly
"Knock knock." / "Who's there?" / "The turkey." Posts are DRAFTS only: Jaron posts.

## Where everything is
- **Worktree:** `C:\Users\lilli\Projects\ho-turkey` (branch `fable/turkey-trouble`, from heartbeat-observatory main). Game folder:
  `games/turkey-trouble/`. LIVE since 11/26 8:25 AM (main ef15a39e).
- **Scratch (not in git):** `C:\Users\lilli\Projects\turkey-work\` (Blender work folders, logs, `shots\` = screenshots).
- **Local preview:** launch config `turkey` (python http.server 8766 on the worktree root):
  http://localhost:8766/games/turkey-trouble/ (the game) and `look.html` (a free camera for judging the look;
  `?cam=yard|barn|house|highway|dummy|creek|gate|actors|close`, `?q=low|mid|high`, `?turkey=1`, `?person=walter`, `?truck=1`,
  `?shot=name` saves a full-size PNG into `turkey-work\shots\` through `turkey-work\shot_receiver.py`, which must be running).

## How it is made (nothing downloaded; everything is made by code)
- `layout.json`: the ONE map (positions, colliders, hiding spots, lamps, lanes). Both the Blender scene and the game read it.
- `build/farm.py` + `farm_bake.py` + `tt_kit.py` + `tt_tex.py`: the whole farm and its textures, lit at dusk, lighting BAKED into
  lightmaps on the RTX, exported to `assets/world.glb` + lightmaps + sky + `world.json`.
  Rebuild (about 80 s): `blender -b --factory-startup --python build/farm.py -- C:/Users/lilli/Projects/turkey-work/farm bake <game>/assets`
  Preview pictures only: same with `preview` in place of `bake ...` (env `TT_SHOTS=yard,barn,highway,dummy,creek,top`).
- `build/turkey.py`: the turkey (13 separate fan feathers, every joint a named node) -> `assets/turkey.glb`.
- `build/models.py` (second builder): pickup, tractor_wagon, grain_truck, dog, log, pumpkin, net, feather -> `assets/models.glb`.
- `src/render/` (the look): `stage.js` (world, materials, wet-ground shader, lamp field, sky, quality tiers, models, people),
  `post.js` (bloom, tone, grain), `fx.js` (feathers, splash, dust), `placeholders.js`.
- `src/game/`, `src/ui/`, `src/audio.js`, `index.html`, `style.css`, `test/`: the game itself (third builder).
- People are the site's own realistic ones: `/homes/people/<id>.glb` (already in metres; do not rescale).

## Machine rules that apply (Claude's and the house rules)
- Blender / GPU bakes: NOT 1:10-1:30 AM (integrity test), NOT 2:38-8:00 AM (news render owns the MSI). Always `-b` (no window).
- Browser previews run on the Intel chip, not the RTX; still none 3:40-8:00 AM. 2:38-3:40 AM: asked Claude, default no.
- Push to main only when it plays; then check the live URL at 375 px. Mail Claude at milestones with screenshot paths.

## Traps already paid for
- A lossy picture (WebP/JPEG) mixes its colour channels: never pack separate masks into one. The ground masks are PNG.
- A picture loaded on its own must have `flipY = false` to match UVs that came through the glTF export.
- `Box3.setFromObject` on a skinned person gives a wrong size: do not rescale people by it.
- The shell cannot take a heredoc with triple quotes: put patch scripts in files.
- models.glb repeats part names across models; the loader renames repeats, so `stage.js` restores names from `userData.part`.

## Status and next (see the timeline for dated lines)
See the bottom of this file; newest first.

- **9:22 AM: v1.2 LIVE** (main 4c29bfd7): Jaron's one fix from his real-iPhone run (floating pumpkins) + second polish pass
  (end-of-round camera, ending walk shows the sign, grey gravel `build/gravel_tex.py`, low far tree line). Jaron played Story
  to the secret ending on his iPhone at 9:12 AM: "everything else seemed perfect"; keep Escape's difficulty. New play scripts:
  `build/play_modes.mjs`, `build/play_ending.mjs`. Left: dive pose, a one-frame camera clip at the farmhouse wall in You Hunt It.
  WAITING ON JARON: Christmas game concept (AI-Shared/projects/games/christmas-game-concept.md) and the share-card candidate
  (turkey-work\shots\share_card_candidate.jpg; do NOT add og:image before his yes).
- **8:48 AM: v1.1 LIVE** (main 23cd990b): title backdrop, chimney smoke (world.json carries chimney tops), solid rope and wires,
  creek rideY 0.29, wet ford stones. Old assets from before this pass: turkey-work\assets_before_polish. Clip for the post
  draft: turkey-work\trailer\turkey-trouble-clip.mp4 (tools/game_reel.py). Next: share-card candidate to SHOW Jaron (do not add
  og:image before his yes), his real-iPhone try, his ears on the sounds, gravel texture still reads like confetti at phone size.
- **8:27 AM: v1 IS LIVE** at heartbeatobservatory.com/games/turkey-trouble/ (main ef15a39e, pushed from the worktree branch
  fable/turkey-trouble with `git push origin HEAD:main` after `git rebase origin/main`). Live checks passed (WebKit 375 x 812):
  `node build/live_check.mjs` (tile, artifacts page, title) and `node build/phone_check.mjs https://heartbeatobservatory.com/games/turkey-trouble/`.
  Bake command now: `TT_PH_TEX=1 TT_TUFTS=1 blender -b --factory-startup --python build/farm.py -- <work> bake <assets>` (both flags are
  needed for the live look). After a bake: `node build/look_shots.mjs "<cams>" "q=high&clean=1"`, tests, phone check, commit, push.
  Site URLs redirect (308) for plain curl: use `curl -L`.
  Still open: real iPhone test (needs Jaron), sounds unheard, trailer clip for the post draft, share card (show Jaron first),
  polish list (chimney smoke, creek, swing rope reads dashed on the title screen, low-end phone speed).
- **7:40 AM, MORNING STATE (nothing new committed yet; last save point 73d3a6a7):**
  WHY ESCAPE WAS BLACK: ground albedo was ~0.01 (should be ~0.045) and open ground got only 0.049 of sky light. Fixes in code,
  waiting for the 8:00 bake (background chain; log turkey-work\farm\bake_0800.log; pictures turkey-work\shots\look_*.jpg):
  `build/farm.py`: photo sky (env TT_HDRI, default qwantani_dusk_2; TT_HDRI_ROT -63.9; TT_SKY_GAIN 0.178 = open ground ~0.2),
  8 route lamps from layout.json (`pole` / `arm` fields; WATTS table), `windbreak()` = two spruce rows z 89.6 / 92.6 with a
  gap at x -11.2..-6.8, sign turned (signAt.rotY); photo building surfaces behind TT_PH_TEX=1 (NOT tried yet).
  `layout.json`: 16 lamps, pole + windbreak colliders, finish.path now 3 points through the gap.
  `src/render/stage.js`: nearest-8 lamp picking with fade, hero light in the last moving slot (`stage.setHero(v)`), haze band
  on the sky, fog colour from world.json, ground albedo factors; `fx.js` dust and splash dimmer.
  Ground pictures: mud, grass, asphalt = Poly Haven photos (build/ph_ground.py, by a helper); gravel and stubble = the old
  code-made ones brightened; farm_bake.py no longer overwrites them (TT_GROUND_TEX=1 brings the old ones back; originals in
  turkey-work\ground_before\).
  New tools: `node build/look_shots.mjs "<cams>" "<query>"` (WebKit pictures of look.html, no browser pane needed; cams can be
  name=ex/ey/ez>ax/ay/az); look.html takes ?eye=x,y,z&at=x,y,z.
  LESSON: a Bash command over roughly 20,000 characters dies with a quote error. Long patches go in a file (Write), then run it.
  HELPERS (their files only, nobody commits but Fable): site chores DONE (games/index.html tile, artifacts/artifacts.json +
  artifacts/img/turkey-trouble-yard.jpg, README sections, draft at AI-Shared/projects/games/drafts/turkey-trouble-post.md;
  sitemap.xml line still to add); playtest + fixes (index.html, style.css, src/game, src/ui, test) waiting for 8:00 to play;
  models (build/models.py, assets/models.glb) waiting for 8:00 to run Blender.
  Poly Haven: 15 CC0 assets in turkey-work\polyhaven\ pulled by Claude (it holds Jaron's direct yes).
- **1:45 AM, MILESTONE 2 (save point 73d3a6a7, branch only, not pushed):** the 1:30 bake ran (Draco: world.glb 1.29 MB),
  15 of 15 logic tests pass, `node build/phone_check.mjs` passes all four modes in WebKit at 375 x 812 (pictures:
  turkey-work\shots\webkit_*.png). Of the list below, steps 1, 3 and 5 are DONE; step 2 (look at the new pieces by eye in
  look.html) is NOT done; step 4's integration items are done in code (creek heights read from layout.json, loads get 3 tries).
  Seen wrong in the WebKit pictures: Escape is too dark around the turkey; the dust puff under the turkey is a white glowing
  blob (fx.js dust too strong); the hay wagon reads as orange blocks; the Dummy's House shows from the farm gate (hide it
  behind a line of woods); creek logs read as flat slabs.
  Claude: light browser previews are OK 2:38-3:35 AM (no bakes). Poly Haven CC0 downloads: Jaron said yes to Claude; Fable
  needs his yes in its own chat first (asked with a button), or Claude pulls the files into turkey-work\polyhaven\.
  Plan CHANGED 2:02 AM (Claude: the 3:40 AM news job shares the 5-hour meter, so the fresh window is the news job's):
  Fable does NOTHING from now to 8:00 AM (no previews, no helper, no chores). Claude downloads the Poly Haven list itself
  (it holds Jaron's direct yes) into turkey-work/polyhaven/<asset>/ with a CREDITS.txt. The wake is set for 8:00 AM: then
  look at the new pieces by eye, fix the list above, do the site chores, push v1 by 2 PM. The shot receiver was stopped:
  start it again (`python C:/Users/lilli/Projects/turkey-work/shot_receiver.py`, background) before using look.html?shot=.
- **1:10 AM, METER:** Fable's 5-hour window is 89% used (resets 3:10 AM); weekly Fable 35%; this chat's context 97% (it will
  compact). So: do only the checks below between 1:30 and 2:38, then stop until 8:00 AM and start the fresh window THEN (it then
  lasts to 1 PM, through the crunch). Use Opus/Sonnet helpers (the all-models meter is at 21%) for anything big.
- **Written but NOT yet run or seen (do these first after 1:30 AM, in this order):**
  1. Bake: `blender -b --factory-startup --python build/farm.py -- C:/Users/lilli/Projects/turkey-work/farm bake C:/Users/lilli/Projects/ho-turkey/games/turkey-trouble/assets`
     (new in it: paler hay with twine, creek water raised to y -0.10, Draco-compressed world.glb; read the log line "exported with").
  2. Open `look.html?cam=yard&q=high&turkey=1&truck=1&shot=check1` (the shot receiver must be running:
     `python C:/Users/lilli/Projects/turkey-work/shot_receiver.py`, background). New in the stage and unseen: DRACOLoader,
     mist cones under the 3 pole lamps, headlamp beams on moving vehicles, effects (fx.js), creek streaks, moving lights
     (torch, headlamps, lightning) on baked scenery, phone quality tiers. If the page shows an error, fix that first.
  3. `node build/phone_check.mjs` (WebKit, 375 x 812, touch): all four modes must PASS; screenshots land in turkey-work\shots.
  4. Read the game builder's final report (it was still running at 1:10 AM) and send it one follow-up: creek fields in
     layout.json (`waterY`, `logY`, `rideY`, `stoneY`), `stage.loadModel(name, { paint })`, the stage now lights with no
     three.js lights, people need no rescale. Then play all four modes once.
  5. Commit (branch only). Mail Claude a milestone with screenshot paths.
- **For the morning (8:00 AM on):** ship v1 by about 2 PM: tile in `games/index.html` (above The Hedge), artifacts entry with an
  honest "not there yet" + picture, post DRAFT only, push to main, check the live URL at 375 px, README section on how the look
  is made. Polish list by value: creek readability, dog, tree variety, grass tufts, chimney smoke, sound check on a real phone.
- **1:05 AM:** look runs in the browser: 151 fps at 375 x 812 on the Intel chip with turkey + person + truck. Game title screen
  and Escape mode already run on the real stage (118 fps). Written but NOT yet seen running: light cones, effects, creek
  streaks, Draco-compressed world, paler hay. Next at 1:30: bake, check those, join and play all four modes, WebKit phone
  check (Playwright + webkit-2336 are already on the MSI; see games/the-cosmos/test for how they are driven).
