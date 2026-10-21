# The Necklace - remade as a real film (idea -> started 2026-09-26 9:15 PM)

Jaron, 9/26 after watching the Three.js version on Heartbeat TV with his partner (it lagged, mostly on her Android): "I would love for
the necklace to actually be based on the book and look way better then the blocky fake look. Biggest thing is realistic
character. Everything needs this. From the worlds, games, loft, and shows."

## What exists
- The book: `C:\Users\lilli\iCloudDrive\The necklace_.txt` (15 chapters, ~11,500 words; Ch.1 "Rum and Regret in Rosetown" ...
  Ch.15 "The Unveiling Tide"). Characters: Jalen Creed, Mateo, Maya, Leo; the Weaver (the necklace).
- Screen language: `Projects/the-necklace-show/PRODUCTION_BIBLE.md` (present reality = grounded Caribbean salt-worn; object
  memory starts macro on the witness object; no generic blue-flash magic). Keep this; drop the blocky Three.js look.
- The current Three.js show stays live (TV mode) until the film replaces it.

## Why this book matters (Jaron, 2026-09-26 9:42 PM - his words, lightly trimmed)
Origin: third grade, told to pick any superpower. Everyone picked the same things - invisible, teleport - always for some
benefit. He wanted one power that could still do all of those: "Could you be invisible literally no but you can delete camera
footage. Can you teleport inside of a bank vault no but you can touch it and see what the code is." And underneath it: "I've
always loved history. There is times of the past that I wish I could be there. I always loved reenactments."

The power: whoever wields the necklace and touches anything sees everything that thing has ever seen.

## Series vision (Jaron) - the book is the seed of a franchise
- The kids point at the branches: **Leo** acts like an FBI agent, **Maya** like an archaeologist.
- FBI branch: you can SEE what happened but still have to PROVE it - cases where you know the truth and can never prove it.
  Built-in suspense. (Matches the production bible's "truth before proof".)
- Archaeology branch: meet history from the viewpoint of what survived it.
- Future / digital branch: touch a safe and see every code ever entered; touch a camera and know what it saw (and how to
  remove it); touch a keyboard and see how a system was set up - so you know how to take it apart.
- Every activation broadcasts the Weaver's location to the Seekers - the cost of every use.

## Film notes from reading the full book (Claude Code)
- Ages (Ch.12): Maya is 17, Leo is 8. MetaHuman is built for adults - an 8-year-old Leo is the hardest character; test early.
- Episode 1 = Ch.1 "Rum and Regret in Rosetown": one set (the Rusty Anchor, night, Caribbean dive bar), two adult men (Jalen,
  Mateo), all dialogue - the best first test for photoreal people. Ch.2 (the stillness, the 1708 lockbox, the skeleton, the
  galleon vision) is the first big effects episode.
- Recurring: the Sea Serpent (30 ft sailboat), the Serpent's Shadow (black yacht), Elias Thorne (pale eyes, wrist device),
  Naia (Keeper of Forgotten Tides), Lysandra Vale, Dr. Corven Hale, Grandma Debbie's mahogany tree, the triple-ring spiral.
- The copy Jaron sent 9/26 is identical to the iCloud text above.
- Epic sign-in: Jaron will do it when a step needs it - tell him the exact screen.

## Plan
- Tool: **Unreal 5.8 + MetaHuman** (installed on the MSI: MetaHumanCharacter, MetaHumanAnimator, MetaHumanGenerator,
  PythonScriptPlugin, MovieRenderPipeline). MetaHuman = photoreal people, which Blender/Three.js can't match by script.
  Project: `C:\Users\lilli\Projects\necklace-unreal` (NecklaceFilm.uproject). Sets can come from Blender (the ocean/rock work).
- Deliver as pre-rendered episodes (video) on Heartbeat TV, one chapter per episode, like The Keeper's Light. Video plays
  smoothly on any phone - the lag was real-time 3D, not video.
- Voices: needs a voice decision for characters (the bible says no synthetic voices "masquerading as cast" - captions-led until
  then). Open: which TTS/voice actors, or captions only.
- First milestone: one photoreal character (Jalen) in the Rusty Anchor bar, 20-30 s test shot, before committing to all 15.

## Unknowns being probed
- Whether MetaHuman creation/rigging can run fully by script headless (some steps may call Epic's cloud and need the Epic
  account signed in on the MSI).

## Probe result (9:25 PM 9/26)
Unreal 5.8 headless + Python sees 242 MetaHuman classes: MetaHumanCharacterEditorSubsystem + MetaHumanCharacterFactoryNew
(create characters by script), skin/eyes/makeup/wardrobe/groom settings, MetaHumanCharacterAutoRiggingRequestParams and
TextureRequestParams (these two call Epic's cloud - expect to need the Epic account signed in), MetaHumanAudioTrack /
FaceAnimationSolver (speech-driven faces), and Movie Render Queue for final frames. Next: build Jalen by script in a real (GPU)
editor session, render a still, then the 20-30 s bar test shot.

## Voices - decided 2026-09-26 9:47 PM (Jaron: "Real voices please that would be awesome.")
- Engine: Chatterbox (Resemble AI, MIT licence) on the MSI GPU, in `C:\Users\lilli\Projects\necklace-voices\.venv`
  (reuses the system PyTorch 2.6 + CUDA). ~45 s model load, then a few seconds per line. Per-line `exaggeration` = emotion.
- First test: Mateo's two opening lines (default voice, ~120 Hz male, natural pace) sent to Jaron as mateo-test.mp3.
- Next: a distinct voice per character (Jalen, Mateo, Thorne, Naia, Lysandra, Hale, Maya 17, Leo 8) - seeded from synthetic
  reference voices, never cloned from a real person. The audio then drives the MetaHuman faces (MetaHumanAudioTrack).
- This supersedes the production bible's "captions-led until recordings are supplied" - Jaron chose real-sounding AI voices.

## Episode 1 progress (9/26 night, while Jaron was out)
- Script: `C:\Users\lilli\Projects\necklace-voices\ch01.json` - 13 lines, the book's own dialogue (1 line adapted from narration:
  Jalen naming Maya and Leo). Voices: Jalen = Kokoro am_michael seed -> Chatterbox; Mateo = am_onyx seed -> Chatterbox, then
  pitched down (~100 Hz vs Jalen ~120 Hz) with a warmer EQ so the two men never blur. `voices.py` rebuilds all lines in ~2 min.
- `ep01/dialogue.wav` + `ep01/cues.json` (start/end of every line - drives the MetaHuman lip-sync and the edit);
  `ep01/ch01-scene.mp3` = radio-play mix sent to Jaron (88 s).
- Shot plan (to shoot once Epic sign-in + MetaHuman skin data are in):
  1. Exterior establishing: harbor at night, the Rusty Anchor's lit doorway, waves on pilings (Blender/ocean pipeline).
  2. Interior wide: the bar, murmur, Jalen alone with a sweating glass (condensation macro).
  3. Mateo slides onto the stool - two-shot. Lines 1-4.
  4. Jalen's monologue - slow push-in on Jalen, cutaways to Mateo listening. Lines 5-8 (on "Maya"/"Leo", brief warm flash
     of two faces in his memory - the only "memory" imagery in Ep1, no magic yet).
  5. Lines 9-11 over-the-shoulder; line 12-13 Mateo close-up, grip on the shoulder.
  6. Jalen steps out into the humid night; the warning lingers - end on the dark sea (sets up Ch.2).
- Blockers (Jaron): Epic sign-in (Chrome window open on the MSI); MetaHuman texture-synthesis data (Epic Launcher optional
  content for UE 5.8 - "skin editing will be disabled" without it).
- 10:54 PM Jaron: "Jalen's voice is perfect" -> LOCKED (Kokoro am_michael seed -> Chatterbox, ep01/ref_jalen.wav is the master
  reference; reuse it for every episode). Mateo: he noticed the test clip (Chatterbox default voice) differs from the scene
  (am_onyx seed, pitched down) - OPEN: which Mateo he prefers. "Love the sound of how the scene will be."
- 11:02 PM Jaron picked the bar-scene Mateo -> LOCKED (necklace-voices/cast/). Both leads' voices final.
- 1:38 AM 9/27 Jaron approved Jalen's look: sun-worn sailor, early 40s, dark hair, stubble, lean build ("That's about what I
  would've gone for too"). Mateo per the book: older, weathered, salt-and-pepper beard. UE updated 5.8.0 -> 5.8.3 (Jaron OK'd);
  MetaHuman optional data + iOS/Android/Windows platform support downloading (15.6 GB). build_character.py ready.
- 2:00-2:20 AM 9/27: MetaHuman optional data installed (5.8 GB: TextureSynthesis, Presets, Grooms, Clothing, BodyTextures).
  build_character.py ran: skin committed (u .55 v .45 rough 1.08); textures + auto-rig FAILED with "Login Failed" - the editor
  uses an Epic device-code (PIN) sign-in: it opens a Chrome page to CONFIRM, polls ~5 min (authorization_pending), then
  EOS_Auth_PinGrantExpired. Needs a human at the MSI to click Confirm while the build waits. Separate from the launcher login.
  Next time: Jaron says ready -> run build -> he confirms in Chrome within 5 min -> token should persist for later builds.
- 8:00-8:15 AM 9/27: Jalen rigged (Epic sign-in confirmed by Jaron 7:32; token now cached - rebuilds need nobody) and BUILT
  at CINEMATIC quality (BP_Jalen + baked face/body textures). portrait.py renders via Movie Render Queue (NewProcess executor;
  PIE executor ended instantly). Front portrait renders with real eyes/anatomy BUT skin is flat clay-gray: T_Head_BC exports
  uniform (95,95,95) even with preview_material_type=EDITABLE and synthesized textures ready before build. Open technical issue:
  how the build pipeline (pipeline_type / baked output) picks up the synthesized skin. Also still to do: face shape (presets),
  grooms (hair/stubble), wardrobe. Not shown to Jaron until he looks like Jalen.
- 8:20 AM lead for the gray skin: build runs a TextureGraph bake (LogTextureGraphEngine run mode, many FTG_AsyncTaskManager
  "UnRegisterTask: Task not registered" warnings) that produces MI_Face_Skin_Baked_LOD* + T_Head_BC = flat 95 gray. Synthesized
  textures are ready before build (1 tick). Next experiments: (1) build a fresh untouched character with defaults - gray too?
  (2) run the build editor with a visible/non-unattended session or -RenderOffscreen off, in case the bake needs the GPU path;
  (3) pipeline_type OPTIMIZED vs CINEMATIC; (4) skip bake: check whether BP_DefaultPipeline has a non-baked (runtime texture)
  option. Pipelines: CINEMATIC (default) / OPTIMIZED / UEFN. Keep GPU work off 9:30-10:30 (news).
- 8:20-8:48 AM: Epic's own example scripts found at Engine/Plugins/MetaHuman/MetaHumanCharacter/Content/Python/examples
  (modify_skin, download_textures, assembly, sculpt_face, add_grooms, add_clothing, spawn_metahuman_actor...). Fix #1 applied:
  close each edit session (remove_object_to_edit) - synthesized face textures now persist (9). Baked T_Head_BC STILL flat gray
  (MI_Face_Skin_Baked_LOD0 'Basecolor Original' = T_Flat_White_C placeholder). Tried: same-session build, separate sessions,
  post-build tick wait (tick log missing), non-unattended editor (editor closed itself via CloseEditor at tick 4 - unexplained).
  build2.py / build3.py in the project. Next: OPTIMIZED pipeline; build a fresh default character to see if it is gray too;
  ask Codex; last resort = one manual 'Assemble' click in the Creator UI by Jaron to compare.
- 8:37-8:53 AM: more findings. face_texture_index 5 made the face download return nothing (0.1 s) - use 3 (4.6 s real
  download; face pores/wrinkles now render). Codex consulted (read-only): said build must happen while the object is still
  added for edit and to verify synthesized_face_textures_info BASECOLOR before building - applied (build5.py), BASECOLOR entry
  present but empty struct {}. Materials are right (MI_Body_Baked -> T_Body_BC which IS colored 130/90/73; 'Use Virtual Texture'
  = False) yet the MRQ render (NewProcess executor) shows every skin gray -> suspect the render process, not the asset.
  Non-unattended GUI editor closes itself within seconds (CloseEditor) - blocks in-editor screenshots. Next: (a) export via
  MetaHumanCharacterExportBlueprintLibrary.export_dcc and render in Blender/Cycles; (b) PIE executor again now that textures
  exist; (c) ask Jaron for a 2-min look in the Creator UI.
- 9:56 AM 9/27 Jaron's look at the Creator UI (photo): Jalen shows REAL skin colour there (warm, sun-darkened; "definitely what
  I pictured Jalen as"). Status panel: Texture Sources up to date; Face albedo/normal/cavity 2k + anim maps; Body 2k; Body Type
  Parametric; Rig State: Joints Only (full face rig = "Create Full Rig" button - needed for lip-sync later). Grey strips = default
  top underwear (show_top_underwear). => character is correct; the colour is lost in ASSEMBLY/bake or render. Next: compare UI
  Assembly settings vs build_meta_human params.
- 9:59 AM Jaron's second photo: the Creator shows a "Missing Project Settings!" warning - needs [/Script/Engine.RendererSettings]
  r.GPUSkin.Support16BitBoneIndex=True, r.GPUSkin.UnlimitedBoneInfluences=True, r.SkinCache.CompileShaders=True ("SKM_Face needs
  the project settings listed above. Related assets may not display properly") - never seen in headless logs; prime suspect for
  the gray renders. UI Assembly = "UE Cine (Complete)", root /Game/MetaHumans, Bake Materials on, Scalable Normals off.
  Jaron clicking "Enable Missing" (+ restart), then re-build + render.
- 10:09 AM Jaron (seeing Jalen in the Creator): "I wish my worlds and players had this realistic look." Paths logged: (1) MetaHuman
  game LODs exported with baked skin -> glTF -> Three.js NPCs/player avatars (verify MetaHuman licence terms for use outside UE
  first); (2) Unreal builds as downloadable PC games (PCGames section); (3) Pixel Streaming (cloud GPU cost - later). Order agreed
  to propose: finish Jalen + Ep.1 pipeline first, then realistic players for worlds + news anchors.
- 10:15 Jaron clicked Assemble in the Creator (needed 10 GB free RAM - closed Chrome/ChatGPT/Edge/Slack) -> "assembly
  succeeded" -> /Game/MetaHumans/Jalen (133 files, saved via Save All). Its T_Head_BC is ALSO grayscale (35-122) while T_Body_BC is
  coloured - so a grayscale face BC is normal; colour comes from the material at render time. Render of the UI-assembled BP is
  still clay-gray with the same look since 8:03 -> REAL CAUSE (10:30 theory): the MRQ NewProcess render process doesn't wait for
  the MetaHuman skin shaders, so it draws the DEFAULT material (the first render even showed its gray checker). Fix: render only
  after the editor has compiled + cached the shaders (Jaron's editor was "Finishing Shader Compilation" at 10:29), and/or make
  the render wait for shader compilation.
- 10:33 AM: shader theory DISPROVED - render inside a full editor (PIE executor, launched via -ExecCmds "py ..." which does not
  auto-quit) is identical gray. Eyes (irises) render with correct colour; only SKIN (face + body) is gray, for both the scripted
  build and the UI "Assemble" output. Creator preview shows correct skin. Next: search Epic forums for assembled MetaHuman gray
  skin (subsurface profile / Substrate / material parameter tint applied at runtime by the MetaHuman component?), compare the
  level's BP component settings vs the Creator preview actor, ask Codex with these facts. Launch trick: -ExecCmds="py <file>"
  keeps the GUI editor open (ExecutePythonScript sends QUIT_EDITOR after the script).

### 2026-09-27 10:36 - gray skin root cause
Not LODs, not textures, not the render process. The log said it plainly: the MetaHuman skin material fails to compile on
shader model 5 (`maximum ps_5_0 sampler register index (16) exceeded`, "Default Material will be used"). The project was
running D3D12 at SM5. Fixed by targeting SM6 in `Config/DefaultEngine.ini`:
`[/Script/WindowsTargetPlatform.WindowsTargetSettings] +D3D12TargetedShaderFormats=PCD3D_SM6`. Lesson: grep the log for
"Failed to compile Material" before theorizing.
**Correction, 10:47 - solved.** The sampler error *was* the cause, but through the bake, not the render: MetaHuman bakes the
face base color by rendering through `M_skin_unified_UI`, and on SM5 that material failed to compile, so `T_Head_BC` baked pure
gray (measured chroma 0; body texture was fine). After switching to SM6, a fresh Cinematic build (`build_sm6.py` ->
`/Game/MetaHumansSM6/Jalen`) bakes warm skin, and the portrait renders in real color. `portrait*.py` now default to that folder.
The old `/Game/MetaHumans/Jalen` (gray) stays as a fallback. Saturation Post-Bake = 0 on the old build was a red herring (left at 0).

### 2026-09-27 11:20 - Jalen's skin tone: DECIDED (Jaron)
Keep the medium, mixed tone of render 2 (`/tv/drafts/jalen-color-2.jpg`, Creator skin u=0.58 v=0.48). Do **not** go darker or lighter.
Why: Jalen's kids (Maya, Leo) and later stories - including other people's series built on this first book - should be free to
go either way; a strongly defined tone would push them to match it "because of bloodline." The book text sets no skin tone for
Jalen (the "pale" lines are about fear, or Thorne's eyes), so this doesn't conflict with following the text.
Jaron 11:21: the setting reads Caribbean, so a medium-brown, mixed tone (not pale, not very dark) fits the place and still
leaves both directions open. Render 2 is that tone.

### 2026-09-27 - The Rusty Anchor set (Ep 1, ch.1 "Rum and Regret in Rosetown")
Built by script: `sets/rusty_anchor.py` (Blender -> baked colour/roughness/normal/metal atlases -> GLB) + `sets/harbour_night.py`
(night harbour seen through the windows). Unreal side: `necklace-unreal/shot_ep1_001.py` imports the GLB, lights the room
(60 W-bulb pendants at 2300 K, back-bar wash, red RUM neon, moonlight, light haze), puts Jalen on his stool and renders shot 001.
**Real-world sizes (Jaron's rule: a ship is ship-sized, a shack is shack-sized):** room 10 x 7 m, ceiling 3.2 m, bar counter
1.07 m high x 0.65 m deep x 5.6 m, stools 0.76 m seat, tables 0.75 m, chairs 0.45 m seat, bottles 0.24-0.33 m, highball 0.14 m,
door 2.1 m, windows 0.95-2.25 m, life ring 0.76 m across. The Sea Serpent (book: "thirty-foot sailboat") must be built at 9.1 m.
Seated cheat: no sitting animation ships with MetaHuman, so Jalen stands 13 cm low behind the counter line; the camera never
sees below it (standard film practice). Book gives the setting: small Caribbean port, night, English + Creole, insects, waves on pilings.
Shot 001 still posted 2026-09-27: heartbeatobservatory.com/tv/drafts/necklace-ep1-shot001.jpg (40 mm, f/2, 2300 K pendants,
Jalen turned 18 deg off-lens with Epic's sad idle loop on body + face). Render: `SHOT_FRAMES=72 ... shot_ep1_001.py`.

### 2026-10-12 - Episode 1, Part 1 SHIPPED (Blender, not Unreal) - `ep1/`
The Unreal/MetaHuman lane is still blocked on the Epic sign-in + the gray-skin bake, so Part 1 was made the proven Keeper's Light
way: `ep1/build.py` builds the whole scene by script in Blender 5.1 (runs `sets/rusty_anchor.py` for the bar at real sizes, adds
a night harbour outside: Ocean-modifier water, pilings, a pitched tin roof, string lights, the quay outside the street door) and
puts the Loft's MetaHuman people in it: isaiah = Jalen (skin lifted toward the decided medium tone, brown field shirt), walter =
Mateo (beard darkened to salt-and-pepper), jorge/sunita/aoi/zuri/ada = the patrons. Sit pose from the glb (`Sit` action), arms
re-aimed onto the counter, head turns keyed per line. Cycles OptiX, 64 samples + denoise, 1280x720, 24 fps, 116 s = 2784 frames,
~4-6 s/frame on the 4060. `audio.py` = the bed (insects, waves on the pilings, murmur, the laugh the book mentions, pad);
narration = Kokoro bm_george reading the book's own sentences (`script.json`, `tts_narr.mjs`); dialogue = the locked
Chatterbox cast from necklace-voices/ep01. `finish.py` burns captions/titles (.ass, libass), mixes, encodes 16:9 + a 9:16 cut.
Honest limits: the people are the phone-weight LOD (1024 px faces, no lip rig) - so no shot holds on a talking mouth; dialogue
plays over the listener, the wide along the bar, and the doorway. Two glTF gotchas: the importer leaves armatures in QUATERNION
rotation mode (set XYZ before rotation_euler) and bone tails are junk (use the next joint's head). Forward is -Y.
