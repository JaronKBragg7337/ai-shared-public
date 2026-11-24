# HANDOFF: World 2 remake, Phase 2 (street life + the performance floor)

- **Date/time:** 2026-11-05, about 1:10-2:20 AM ET
- **From:** Claude Code (cloud, scheduled run)
- **Project:** World 2 remake  |  **Repo/branch:** JaronKBragg7337/heartbeat-observatory @ `cloud/world2-phase2`
- **PR:** https://github.com/JaronKBragg7337/heartbeat-observatory/pull/33 (opened as a **draft**, NOT merged; mark it ready, phone-check it, then merge)

## What I did
- **People** (`world2/life.js`, new):
  - an instanced sidewalk crowd built from a shaped human figure (not boxes), with optional long hair, coat or skirt;
  - the walk cycle runs in the vertex shader, and the shadow pass walks too;
  - 2 draw calls, a near/far LOD and frustum culling;
  - 150 people on desktop, 96 on phones, 60 on lite, kept near the camera;
  - they stay on sidewalks, cross only on crosswalks, wait on red and look both ways;
  - cars and buses yield to people on crosswalks.
- **Buses:** the Downtown Loop, 2 buses on a two-block loop. They stop 9 s at a new shelter in front of Union Station on Jefferson.
- **Sound:**
  - WebAudio, all synthesized, started only by a tap and never in the gate preview;
  - quiet by default, with a remembered 🔊 Sound button under the minimap;
  - layers: traffic hum, river, footsteps, birds by day, crickets at night, crosswalk ticks and chirps.
- **Performance:**
  - far-chunk LOD by index range: detail triangles are dropped beyond 95 m with no extra draw calls;
  - small metal/dark trim no longer casts shadows.
- **KTX2 was skipped on purpose.** The city textures are drawn on a canvas at load, so nothing is downloaded. The reasoning is in WORLD2-REMAKE.md.
- **Version stamp:** `2026-11-05-phase2` on BUILD, the main.js `?v=`, and the city.js and life.js imports.
- WORLD2-REMAKE.md has a new "Phase 2 as built" section with the before/after numbers.

## Where it lives (exact)
- Code: `world2/life.js` (new), `world2/city.js`, `world2/main.js`, `world2/index.html`, plus `WORLD2-REMAKE.md`.
- I did not touch `realcity/` or `/worlds-lab/`.
- Screenshots and test scripts: `AI-Shared/scratch/world2-remake/phase2/`.
  - `shots/`: day and night at 390 and 1280, including the close-ups `close-day.png` and `close-night.png`.
  - `scripts/`: `func.cjs` (functional checks), `fast.cjs` (draw calls and triangles), `views.cjs` (screenshots), `close.cjs`.
  - The scripts route three.js from a local copy, because the cloud can't reach jsdelivr. On the MSI, remove the `page.route` for three.

## Verified vs assumed
- **Verified:** Playwright Chromium with SwiftShader (software GL), at 390x844 and 1280x800, day and night.
  - Zero console errors.
  - One-click enter and one-tap walk.
  - All 8 door prompts; the Arcade walk-in; the Lot 1 prompt.
  - The map opens with 21 places.
  - The Sound button toggles and persists.
  - The gate preview loads.
  - Crowd audit: 600 s fast-forwarded, 0 people in the street or inside a wall.
  - Bus audit: over 240 s, each bus stopped at the station 4-5 times, and all 16 cars kept moving.
  - Draw calls and triangles, Phase 1 → Phase 2:
    - phone street: 111 → 112 calls, 341k → 339k tris;
    - desktop aerial: 215 → 219 calls, 361k → 353k tris (by day);
    - the worst case is the desktop night aerial: 386k tris, 221 calls;
    - textures unchanged at 17.9 MB.
    - The full table is in WORLD2-REMAKE.md.
- **Not verified:**
  - **WebKit.** Its download is blocked in the cloud container, so it didn't run here. Run `func.cjs webkit 390 844 0.78` on the MSI when it's idle (after the news render).
  - Frame times on a real GPU or phone. Software-GL frame times are meaningless.
  - Two-client multiplayer. I didn't touch that code, but it wasn't re-run.
  - The sound, by ear. Headless can't listen.

## Flags (my eyes)
- **Crowd density.** One person every ~13 m on desktop and ~20 m on phones. If Jaron wants busier streets, raise `COUNT` in `buildCrowd` and watch the triangles: each near person is 1.1k, each far person 0.45k.
- **The bus shelter's glass** uses the facade glass texture, so it reads dark blue. That's fine, but a plain glass material would look cleaner.
- **Pedestrians at unsignalled corners** cross after looking. Cars yield to them, but cars on the car loops only check people ahead in their own lane.
- **The 10/28 iPhone check** is still the real gate for Phases 1 and 2.

## Exact next step for the next AI
- Claude on the MSI:
  1. Mark PR #33 ready.
  2. Open the Vercel preview on a phone: walk spawn → courthouse → Union Station (bus stop) → the theater at night; tap Sound; check the doors.
  3. Merge.
  4. Then Phase 2b: MetaHumans near the player (desktop only), people sitting on benches, and more car models.
