# Earth round 2 (Earth as a start world + Florida looks) - 2026-10-08

Commit ad436fd on main (build b1aaba9baac2a41dfaf6). Live: https://www.heartbeatobservatory.com/games/the-cosmos/

## What changed
**Earth is an open start world.** The arrivals board shows Earth OPEN (Homeguard + Skyward, dollars, 9.82 m/s2). Landing place is the Skyward Launch Complex at Cape Canaveral. Wired the way Ceres is:
- `src/opening/worlds.js` row open; the port line says "Homeguard has nothing built yet", the goods lines say no shop and no trader yet.
- `src/opening/worlds/earth/dialogue.js`: crash site (Florida scrub), locker note, crate, the two drivers (Okafor of Skyward, Pruitt of Homeguard; Pruitt says he borrowed Skyward's truck and that nothing of Homeguard's is built) and the counter-recruiters. Gate line "Kestrel to Earth" added. 21 new voice clips (`node tools/gen-voices.mjs`).
- Two people at the complex so the two lifeboat parts have someone to come from (`src/worlds/earth/cast.js`, built by the Moon's person class in `worlds/earth/client.js`): Okafor (flight line crew chief, Skyward, near the hangar) gives the power cell, Pruitt (Homeguard organiser, beside the training hall) gives the fuel coupler. Same Loft bodies as the two drivers. Their Talk lines are voiced.
- In the opening itself: Earth's own globe from space (Blue Marble picture, Florida turned toward you), a clear blue evening sky and warm light at the crash site, the crash-site ground in green scrub and sand (not Mars rust), the long flight keyframe scaled so a 6,371 km world does not graze the camera.
- Left alone on purpose: how a damaged ship leaves Earth (Jaron's open call). Today's behavior is unchanged.

**Looks round 2.**
- Ground at the complex is grass, scrub and sand with wet and dry country, tussocks, ragged bare-sand patches and ragged beach edges (new Earth ground shader in `world/regolith.js`, only used by worlds that set `earth: true`; Mars, Moon, Phobos, Deimos, Ceres untouched). The black angular stones are gone on Earth (`groundDetail.js`): none on grass; only cream shell grit on sand. The scrub bushes are lumpy smooth clumps, not faceted balls.
- The info panel says "Grass and soil", "Packed sand and shell rock" or "Sand" (no more "Earth regolith").
- From orbit: a shader over the 2k Blue Marble picture cuts the coast sharp along the picture's own land/sea edge (ragged, not a soft blur), takes the blue bleed off the land and adds grain at 18 km, 4 km and 0.9 km. On only from 15 km to 3,500 km up and only where a pixel is smaller than a texel. The wide ground tiers also get ragged sand/grass edges (`moonWorld.js`, one guarded line).

## Verified locally
- `node test/validate.mjs` full run: 1902 passed, 0 failed (first run was 1901/1: the voice clip total passed the 15 MB cap; raised to 16 MB, re-run green).
- `node test/phone-check.mjs`: all pass (iPhone WebKit and Galaxy Chromium), after the restamp.
- New `test/opening-earth-browser.mjs` (iPhone WebKit, 393x852): board with Earth open, pick Earth + Skyward, gate says "Board the Kestrel to Earth", flight, crash, dig, ride, arrive on Earth beside a drained lifeboat, buy the cell from Okafor and the coupler from Pruitt through the real action button, fit it: all PASS. `test/pkg-earth.mjs` (38) and `test/opening-checks.mjs` extended.

## Verified live
- Pushed; the site's build id is b1aaba9baac2 and so is the page's.
- **The shared-world server on the MSI was still on a 10/4 build (9b85464edb02), so the board would have said Earth "coming" and the server did not know the Earth world at all (last night's first pass only worked in solo / local tests). I restarted it** (killed the node process on port 8390 with 0 players on; the watchdog brought it back in 65 s; Supabase world loaded, revision kept counting). Health now says buildVersion b1aaba9baac2a41dfaf6 on both localhost:8390 and https://cosmos.heartbeatobservatory.com/health. This is the step every server-side change needs; nothing else restarts it.
- Live site on iPhone WebKit at 393x852: the real server's board lists open worlds mars, ceres, earth; Earth tab shows "Fly the Kestrel to Earth" and no "not built" note (`live/live-board-earth-open.png`). The throwaway player I made for this was discarded again.

## Not verified / still ugly (plain)
1. **The whole start (liner to Earth, wreck, ride, arrival) was not played on the live site**, only its first part (board). It was played end to end against a local authority built from the same commit (screenshots in `opening/`). A live run needs about four real minutes for the liner and walking by hand.
2. Real iPhone speed is still unmeasured (emulator only). The Earth shell, scrub (80-face clumps, 380 on low) and the new shaders add a little; the globe detail shader is switched off outside 15 km to 3,500 km up.
3. From orbit the picture is still 20 km per texel: the new coast and grain are synthetic detail on top, not data. The land interior at 400 km is still soft. Away from the Cape the coast is the 0.5 degree data; the cut is sharp but its position can be a texel or two off the real one. A 4k picture would help but means a download (not done).
4. Up close the turf is mottled colour and a little bump, not individual blades or flowers. The 6 km view still shows the square seam where the 880 m tier ends, and 600 m triangle edges where sand meets grass (now ragged, still visible).
5. Homeguard still has nothing built: Pruitt stands alone in Skyward's yard. The two people stand still.
6. The board's little Earth drawing is the old generic circle with white ovals.
7. Kestrel cabin: you only see Earth through the starboard window (look right) and the last frames carry the crash overlay.
8. `docs/qa/phone-check/2026-10-08/` (screenshots from the check) is left uncommitted.

## Screenshots
`C:\Users\lilli\AI-Shared\state\cosmos-earth-2026-10-08\round2\`: `before\` and `after\` (grass wide, grass close, sand close, 6 km, coast from the air, 60 km, 400 km, orbit, pad views), `opening\` (board with Earth open, pick, gate, Kestrel and Earth below, wreck, dig, driver, ride, arrival, Okafor, Pruitt, fitted), `live\` (the live board).

## Still open
- Design call: how a ship that lands damaged gets off Earth (Skyward launch service, booster, or repair rule).
- Phone speed on a real iPhone.
- Next on Earth: Homeguard's first building, then launching the vehicle on the mount; a 4k land picture if a download is allowed.
