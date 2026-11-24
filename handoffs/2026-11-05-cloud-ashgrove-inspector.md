# HANDOFF: Ashgrove building inspector + roof fixes (cloud session)

- **Date/time:** 2026-11-05, ~2:30 AM ET
- **From:** Claude Code (cloud session https://claude.ai/code/session_012aQqdkjPpCyfVWMeHzVtZj)
- **Project:** Ashgrove (World 3, `world3/`). Build order #2 (games README, 11/4) and W-17 in SITE-BACKLOG.
- **Repo/branch:** jaronkbragg7337/heartbeat-observatory @ `cloud/ashgrove-inspector`. PR to main: https://github.com/JaronKBragg7337/heartbeat-observatory/pull/32 (ready for review). **Not merged**: Claude on the MSI checks it and merges.

## What I did
1. **Built `tools/inspector/`** (site repo). `node tools/inspector/inspect.js ashgrove` boots the real town generator in Node and records every triangle it emits. It tags each one with its building and asset id, then MEASURES each building:
   - **roof closure:** sky rays find holes; side rays into the attic band find gaps;
   - **stairs:** landing in front of the first step and past the last, plus headroom over every tread (IRC numbers);
   - **doorways:** clear floor on both sides, and what's in the way;
   - **rooms:** flood-walked with the player's own collision, then rated no way in / blocked by furniture / cramped / ok;
   - **parts:** float/bury, plus furniture clipping walls or other furniture.

   It writes `tools/inspector/reports/ashgrove/`: a README summary, one `Bxx.md` per building, INVENTORY.md (built / planned / in files but never shown), and report.json.
2. **Ran it before and after.** BEFORE.md is the same inspector run against the old render code.

   | measure | before | after |
   |---|---|---|
   | buildings passing every check | 2 / 49 | 11 / 49 |
   | roof gaps | 96 (446 m²) | 0 |
   | stairs with no landing at the first step | 22 / 22 | 0 |
   | stairs short of headroom | 22 / 22 | 0 |
   | doorways obstructed | 4 | 0 |
   | rooms with no way in | 35 | 0 |
   | rooms cramped (< 35% walkable floor) | 46 | 43 (open) |
   | furniture clipping walls | 62 | 60 (open) |
3. **Fixed** (world3/town/render/):
   - **Gables:** the end walls stopped at the wall-top pitch line, and the roof sits over*pitch higher. That left a see-through wedge up both rakes of every gable house. They now reach the roof underside.
   - **Shed roofs** (split-levels, diner) had nothing closing the side wedges or the high back. Up to 78 m² per house was open. They are closed now.
   - **"Object blocking the view up the stairs"** (Jaron reported it twice): it was the storey band board, ONE box the size of the whole footprint, so it was a slab capping every stairwell. The inspector measured 0.12 m of headroom over the top treads. It is now four perimeter strips that look the same from outside.
   - **Stairs started 0.09 m from the hall end wall,** so the first step was AT the wall. Each run now slides along its hall to get a 0.95 m landing at the foot, clear of any door opening onto its side. In the short Townhouse hall, the living-room and bedroom doors slide onto the landing instead.
   - **Stairwell hole overshot the top tread by 5 cm.** A player falls through that slot, and it is why the whole upper floor of every Cape Cod/Townhouse was unreachable.
   - **Chapel steeple stood inside the nave, on the front door,** so nobody could enter the chapel. It now rises from the wall tops.
   - **The boundary fence ran straight through B11 Cottage and B38 Townhouse** (rooms with no way in). It now breaks around houses.
   - Cache-bust `?v=2026-11-05-inspector` on the four changed files in both `world3/index.html` and `world3/town/index.html`.
4. `world3/town/tools/walkable.js` now exports its flood so the inspector uses the same walk (no copy). `tools/baseline.js` EXPECTED moved: assets 4288, colliders 3114 (+4 fence runs), staticTris 861018 (2,142 fewer than before, so the phone budget got lighter, not heavier).

## Verified vs assumed
- **Verified (cloud container):**
  - All the town's own harnesses are green: baseline (all contract lines hold), walkable (0 rooms unreachable, was 33), slice, ambient, growth, resources, layers.
  - Inspector before/after as in the table.
  - `/world3/` and `/world3/town/` load in headless Chromium (SwiftShader) at 1280x800 and 390x844. Both build 50 buildings with no sideways scroll. The only console errors are `/_vercel/insights/script.js` (404, exists only on Vercel) and the Supabase CDN (blocked by the sandbox). None come from page code.
  - Before/after evidence is `tools/inspector/reports/ashgrove/evidence/*-before-after.png`: orthographic end elevations painted from the measured triangles. Camera screenshots were unusable, because at SwiftShader frame rates the town's camera rig never framed a building.
- **Assumed / not verified:**
  - The look and fps on a real iPhone. Triangles went down slightly, so the budget should hold, but nobody has looked on a device.
  - `advance.js` needs Supabase env vars and was not run.

## Still open (reported per building in the inspector reports)
- **Kitchens and dining rooms are cramped** (5–7% walkable in Colonials, Farmhouses, Cape Cods). Cause: `T.clearDoorways` (render/furniture.js) slides a counter run OFF its wall into the room. Counter + range + fridge then make a barrier with a 0.4 m slot. I tried "slide only along the wall", but it removed 25 counter runs and 53 items, so I reverted it. The real fix is to shorten a counter run around the door zone instead of moving it.
- **60 furniture-into-wall clips.** Mostly the F02 item in WC/bath/laundry, poking into the wall behind it.
- Stair runs still have **no colliders** (the 8/6 compromise in buildings.js). Now that every run has a landing at its foot, per-step colliders could be retried; walkable.js will say whether the upper floors stay reachable.
- The chapel's ridge runs across its 12 m width, so the front is one 12.5 m tall roof plane. That's odd for a chapel; it's a design call for Jaron.

## World 2 and Town Square (read-only)
`node tools/inspector/inspect.js world2` and `townsquare` open each page in headless Chromium. They serve three@0.182.0 from npm, because the sandbox can't reach jsdelivr. The run catches the live scene, bakes every visible mesh to triangles, and reports roof holes (pits in a sky heightfield), floating parts and unreferenced files. Those worlds expose no building records, so the stair, door and room checks can't run there yet. The next step is an adapter that reads `world2/city.js`'s lot/kit data. **Not yet proven:** in the cloud sandbox neither page reached its first `renderer.render` within 3 minutes (SwiftShader, CDN blocked apart from a local three). So there's no World 2 / Town Square report yet. The read-only run is light CPU work with no GPU needed. Run it on the MSI only outside the 2:40 AM news render window: `npm i three@0.182.0` in tools/inspector, then `node tools/inspector/inspect.js world2`.

## Things that looked wrong (flagging)
- `baseline.js` claimed `twoStoreyWalkable 22/22` while `walkable.js` said 33 rooms were unreachable. The baseline's climb check proves the ramp, not that you can reach the ramp.
- The 8/6 comment in buildings.js blamed the dark for the "object blocking the stairs". The object was a real slab.
- The live `/world3/` page in the browser builds 50 buildings (B50 from catch-up growth). Headless builds 49. Growth buildings weren't inspected separately, but they use the same generator.

## Exact next step for the next AI
1. MSI Claude: review and merge the PR, then deploy. Walk B12 (Tudor) up its stair and B04 (chapel) through its door on a phone.
2. Fix the kitchen counters in `T.clearDoorways` (shorten, don't move), then rerun `node tools/inspector/inspect.js ashgrove`. The target is 0 cramped kitchens.
3. Write `tools/inspector/world2.js` against city.js lots, so World 2's remake gets the same roof/stair/room checks while it's being built.
