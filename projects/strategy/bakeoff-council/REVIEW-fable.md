# Review, round 1 - Claude Fable 5.1 (read all four codebases, 2:05 AM)

## 1. Keep / drop, per build

**Sonnet (bedroom-sonnet/app.js, modes.js, history.js)** - keep as the base.
- `applyView()` + `hist.trackAt(t)`: the scene is a pure function of history + time. Scrub, film, replay and audio fall out of one function. The fourth piece done right.
- `analyzeGait()`: foot plants read from the clip's real low points, `gait.yOff` keeps soles on the floor. Honest feet.
- `U.maskMin/Max` + `buildMadeProps()`: the torn nightstands/headboard/bed-foot are cut out of the seen mesh and replaced by made props. That is the right tear fix. His v3 "PATCHED from own pixels" should replace the plain-colour props.
- `visitTasks()`: the man reacts to the unlock and walks in; `history.js words()/story()`; the continuity supervisor (`modes.js continuity()`); `shots.json`.
- Drop: nothing structural. Five bottom tabs are a lot at 375 px; fold Fable's demo sheet in.

**Kimi (bedroom-kimi/index.html)** - keep the picture.
- `buildClosure()`: walls at opacity .22, floor .48, so the ORIGINAL photo stays dominant - exactly what Jaron saw and wanted. Rule for the unified build: the seen picture is the hero, made closure is a veil.
- `EventHistory(seed)`: the page boots from `history.json`, so file and live state are one object; `history.download()`.
- Per-door `textSprite('D2 · NOT SEEN')` labels; the "Why?" trace (footstep -> sound cause).
- Drop: the teal annex box + point light, MeshStandard made surfaces.

**Sol (bedroom-sol/index.html)**
- `inside()`/`updateWalls()`: "Step inside / overview" cutaway toggle. `setLens()`: amber=made, blue=rebuilt lens over everything.
- Causal chain: every event carries `cause` + `children`; `mcp_server.py causal_chain`. `motion_sample.sole_min_y`: feet-on-floor measured, not claimed.
- The listening alcove (Jaron liked it) and the lamp care log.
- Drop: the made shell hiding the photo (he "barely used the real picture").

**Fable (bedroom-fable/index.html)** - mine, honestly.
- `startDemo()/stepDemo()`: game walks him through the door (`goVia`), movie = 3 cuts over the replay, music = tempo from footstep intervals, show = `narrate()` lines from events + `speechSynthesis`. Merge into Sonnet's modes.
- `seenMat` `cut` uniform: on unlock the dark alcove pixels go translucent so the made room shows through the real doorway. Dollhouse camera (inward-facing walls, orbit from outside).
- `hb-vision/bake/fable/rec.mjs`: fixed-step 1080x1920 recorder on the MSI GPU (816 frames in 66 s, lock-aware). Use it for every site video.
- Drop: my made room and textures. The "scattered" picture: both frames at equal weight and a far camera, so frame 25 double-images frame 1 and the frame-1 floor noise reads as rubble.

## 2. What I'd do differently
One anchor frame: frame 1 is the picture, frame 25 only where frame 1 has holes. Camera closer and lower, like Kimi. Tears: Sonnet's PATCHED pixels, not my triangle filter. Second room: furnished like Sonnet's study, lit like Sol's alcove, every made object with its own history line (Sol's care log).

## 3. Unified shape (Jaron's verdict respected)
Base: **Sonnet app.js + history.js**. Then, in order:
1. Seen picture: Kimi's veil opacities + anchor-frame rule + Sonnet v3 patches. Check on the phone before anything else.
2. Door 2: Sonnet's study, lit like Sol's alcove, with Fable's doorway cut-through. D1/D3 stay locked.
3. History format: Sonnet's `hb-history/1` + Sol's `cause/children` + Kimi's seeded boot/download. One `AI-README`, one MCP (Sol's four tools).
4. Modes: Sonnet's Witness + continuity; Fable's movie cuts, beat-from-steps, narrated show with voice; Sol's step-inside and lens as view toggles.
5. Fable's `rec.mjs` for the video.

## 4. New uses worth demoing
Kimi's "Why?" causal trace (step -> sound -> cause); Sol's care log (object memory = roofing job records); Sol's sound guide (accessibility by ear); Kimi's AI-video quality check (foot slide, loop mismatch as numbers); Sonnet's continuity supervisor as a product for shows.

- Claude Fable 5.1
