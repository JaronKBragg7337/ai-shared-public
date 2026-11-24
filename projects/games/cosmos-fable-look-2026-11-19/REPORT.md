# Report: The Cosmos look pass (Fable 5.2, 2026-11-19)

Branch: `fable/cosmos-look-2026-11-19` in worktree `C:\Users\lilli\Projects\ho-fable-cosmos` (commit 10f47520, NOT pushed).
Ranked list: `LOOK-PLAN.md`. Shot script: `shoot.mjs` (needs the game served on port 4380).

## What I fixed
The helmet lamp was stuck on at full power on Phobos (and every other world that is not Mars), in full sunlight.
It measured "how deep in a hole are you" against Mars while you stood on Phobos, which reads as thousands of km
underground. Result: a tan glow 24 m wide that followed you and washed out the ground at your feet.
Now the depth is read on the world you stand on. On moons the lamp comes on at night or in a dug hole.
One file: `games/the-cosmos/src/main.js` (11 lines).

## Before / after (same camera, same sun)
- `shots/before/09-phobos-eye-rocks-phone-webkit.png` -> `shots/after/09-phobos-eye-rocks-phone-webkit.png` (clearest: tan foreground becomes grey rock)
- `shots/before/10-phobos-underfoot-*` -> `shots/after/10-phobos-underfoot-*`
- `shots/before/08-phobos-eye-pad-*` -> `shots/after/08-phobos-eye-pad-*`
- `shots/before/11-phobos-third-walk-*` -> `shots/after/11-phobos-third-walk-*`
- `07-phobos-landed-ship`, `03-mars-open-ground` (Mars should look unchanged)
- `*-live.png` = real clock. Phobos was in night during this pass; the lamp still comes on there (after shot shows it).

## Verified locally
- iPhone WebKit 390x844 and desktop Chromium 1440x900: no page errors, no sideways scroll (scrollWidth = innerWidth).
- Lamp reads 0 in daylight on Mars, Phobos, Ceres and the Moon (iPhone WebKit); still on at Phobos night.
- Two 404s in the console are site files that only exist on the live site (`/_vercel/insights/script.js`, `/hb-editor.js`); same before and after.
- `node test/validate.mjs`: the full run stopped at one UI tap timeout in the parity check (a shop talk button) while my other browser sessions were loading the machine. That check alone (`node test/_parity-ui-only.mjs`) passes 4/4 with the fix and 4/4 without. The full validator was NOT re-run to a clean finish, so its total is unknown.

## Not verified
- Not live: nothing is pushed or deployed. The build stamp (build.json / ?v= in index.html) was not regenerated.
- No real iPhone; Playwright WebKit on Windows only.
- Lamp inside a dug hole on a moon: logic only, no screenshot.
- `node test/phone-check.mjs` was not run.
- Problem 5 (square patch from space) was seen with the review camera, not a real flown approach.

## Still wrong (biggest first)
1. Player walks Phobos and Mars in a T-shirt, jeans and no helmet, with an Earth walk in near-zero gravity.
2. Phobos day still looks like a soft grey sand dune: no hard shadows, wind ripples, too pale, no real boulders.
3. Earlier reviews used a pinned high sun; with the real clock about half of Phobos visits are near-black night.
4. Square detail patch visible on Phobos from space; Mars is a dim flat disc in Phobos's sky; stars in Mars's daytime sky.
