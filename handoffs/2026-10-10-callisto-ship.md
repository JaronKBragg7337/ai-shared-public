# Callisto ship, 2026-10-10 (Claude Sonnet 5.5)

Callisto (built by Kimi K3, Moonshot, branch kimi/callisto) is live in The Cosmos. Build `ac9cf3851c91bc8dbacb`, site and MSI server both confirmed on it (server restarted at 0 players, /health shows the build).

## What Kimi got right
The whole structure: real numbers for the moon and orbit, the Valhalla Camp (Archive, Standing Array, dishes, shed, five real people), the prospectors' camp 1.2 km north, sealed site and dead relay, five-job thread, start-world wiring (opening words, lifeboat parts from both sides), 44 voice clips, globe from the USGS mosaic, tests (pkg-callisto 30/30, browser 10/10), honest notes in the def. Shared-file edits were small and named; none broke other worlds (full validate 2012/0).

## What I fixed
1. Ground was bright grey-white: Kimi's `groundAt` returned clean ice for the TOP metre (backwards). Now a dark dust skin (0.8 to 1.3 m) sits over the ice, which is dug up as the job says. pkg-callisto check corrected to match.
2. Jupiter was a plain beige ball. The game's plain far-world Jupiter ball (`space/farWorlds.js`) was drawn over Kimi's banded one, and the banded one had its pole pointed at the camera. Hid the plain ball in Callisto's frame (`OWN_SKY`), turned the spin axis across the line of sight, stretched colour and contrast in the shader. Bands and Great Red Spot now read at its true 4.4 degrees.
3. Stones: dust-stained brown-grey, one in six clean ice (groundDetail.js), not black.
4. Live playtest blocker "floating off the ground on a moon": the wall push in the camp multiplied ALL velocity axes by 0.2 each frame, so a jumper at a wall hung in the air in low gravity. New `bleedSideways` (moon/place.js) keeps the fall. Applied on Callisto and the same copy-pasted bug on Moon, Earth, Ceres (this is also what the earlier moons-local7/8/9 playtests were flagging). Not changed: shipSystem hull push (blockedVel).
5. Quartermaster counter blocked the whole shed front, so Tomas Grey was 3 m away behind it. Split with a 4 m gap.
6. Callisto's people now carry `layout.BOXES` (incl. prospectors' huts) so the playtester's route planner sees the walls.
7. Buildings (flat purple boxes): left as they are, acceptable first pass.

## Verified
- Local: full `node test/validate.mjs` 2012 passed / 0 failed (three runs). Kimi's 1 fail (Mars gangway timing) did NOT repeat in any of my three full runs and the opening browser step passed each time: a flake. `node test/phone-check.mjs` 33 PASS 0 FAIL (iPhone WebKit + Galaxy Chromium), each time. pkg-callisto 30/30, callisto-browser 10/10.
- Live: site build.json and cosmos.heartbeatobservatory.com/health both `ac9cf3851c91`.
- Playtest on live (`play.mjs --start callisto`): run 1 (18 min iPhone + 5 desktop) found 1 blocker (floating) + 2 serious (stuck at counter, Archive wall). After fixes: run 3 (16 min iPhone) = 0 blockers, 0 serious, 10 small. It talked to the Director, Tomas Grey and Odette on Callisto. Reports: `state/playtest/2026-10-10_02-14/REPORT.md` (final), `state/playtest/2026-10-09_23-59/REPORT.md` (first).
- Not verified: Callisto opening played end to end on a real phone by a person; the Mars-side desktop "graphics context lost, never drew again" finding (desktop run was Mars, seen in earlier reports too, not Callisto).

## Screenshots
Before (Kimi's): `heartbeat-observatory/games/the-cosmos/docs/qa/2026-10-10/callisto-before/` (phone-jupiter, phone-camp, phone-camp-pad, phone-sealed-site).
After: `heartbeat-observatory/games/the-cosmos/docs/qa/2026-10-10/callisto/` (same names, plus archive, array, relay, prospectors, talk).

## Still open
- Bram Okonkwo is 1.2 km away; the bot's 240 s budget runs out about 90 m short. Bot limit, not a defect. Make it 360 s or let it teleport to the port.
- Valhalla's rings not carved; orbit phase fitted, not from Horizons (Kimi's notes).
- `phone-check` still runs the Mars opening, not Callisto's.
- Callisto buildings still flat violet boxes; an Archive/Array detail pass would help.
- Playtester finding on all worlds: "Dig tap in the opening made no cut", frame-time spikes (headless software render), 404 for `homes/people/undefined.jpg` when talking to someone (a person without a portrait id: worth chasing).
- Possible slight softening of Jupiter's terminator (hard line).

## Rating of Kimi's work (for the router)
Good build, B+: complete, honest, well tested and correct on all structure and wiring, but looks were unchecked against its own screenshots (bright ground from an inverted layer, plain Jupiter) and it copied the Moon's wall-push bug; fine for big builds with a looks-review and a live playtest after.
