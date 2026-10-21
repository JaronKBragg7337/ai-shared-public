# Earth, first pass (WD-EARTH) - 2026-10-08

Commit 99aeecc on main (build 7708894ea8ebfa10775a). Live: https://www.heartbeatobservatory.com/games/the-cosmos/?dev=1&solo=1&body=earth

## What got built
- **Earth is a real world now**, not a placeholder (`games/the-cosmos/src/worlds/earth/`). Real radius, mass (gravity 9.82), day, tilt, JPL orbit, sea-level air, blue sky. Nav lists it; the real server flies Mars to Earth by the long drive and lands the ship on the pad (tested).
- **Real land and sea, from data.** Whole globe heights and sea floor from AWS Open Data Terrain Tiles (SRTM + GEBCO + ETOPO1), baked small (about 280 kB) at half a degree, plus a 200 m window over Cape Canaveral with the real coast, Banana and Indian Rivers, Merritt Island and the shelf. Land colour from NASA Blue Marble. Credited in credits.json; baker is `tools/bake-earth.mjs`.
- **Looks like Earth.** Blue sky gradient, clouds (a deck you stand under, a cloud shell from orbit), a drawn sea (waves, glint, sand showing through the shallows), blue limb of air, the whole globe lit by the Sun with a night side. Sun runs on Earth's real day (local noon at the Cape is about 17:10 UTC).
- **Skyward Launch Complex at the Cape**, a few hundred metres east of Launch Complex 39A, Atlantic about 700 m east: painted pad, Range Control (countdown clock), training hall, flight-line hangar, 58 m assembly hall with chevrons, crawlerway, launch mount with flame trench, 96 m service tower with swing arms, a vehicle on the mount, lightning masts, two cold-fuel spheres, tank farm, windsocks, floodlights, palms and scrub. No people (skipped on purpose; no blocky ones).
- Voices: 12 new course-line clips generated. Tests: `test/pkg-earth.mjs` (31 checks, includes the real authority flying Mars to Earth to orbit), `test/earth-browser.mjs` (phone WebKit screenshots).

## Verified locally
- `node test/validate.mjs`: 1891 passed, 3 failed on the first full run; all 3 were older checks that assumed Earth was a placeholder. Fixed those four test lines (opening-checks, freeflight-checks, worlds-orbits-checks, pkg-longrange). Re-ran the fast suites (worlds, space, freeflight, opening, longrange, earth): all green. I did NOT re-run the whole 32 minute validate after the four test edits.
- `node test/phone-check.mjs`: all pass (iPhone WebKit and Galaxy Chromium).
- Screenshots at phone width (393x852): pad, north, west, tower, shore, from the air, approach at 6 km, 60 km, 400 km, from orbit.

## Verified live
Pushed, waited for the build id to appear, then loaded `?dev=1&solo=1&body=earth` on the live site in iPhone WebKit: stands on Earth, no page errors, complex, sea, sky all render. Four shots in `live/`.

## Shortfalls, ugly, unverified (plain)
1. **Real iPhone speed not measured.** Only the emulator. Kept light (low tier: 240 palms, 380 scrub, one 2k texture, about 3 extra draw calls for life), but the Earth shell and tiers are heavy like the Moon's. Needs one look on the phone.
2. **The Sun is the game's Sun, not Earth's calendar.** A frame can only turn about Mars's pole, so the day length and local noon are right but the Sun's height is off by season (about 37 degrees at Cape noon today; real is about 55; in February it would be near overhead). Night and day follow the real clock.
3. **The stock Meridian can barely leave Earth.** 46 t x 9.82 = 452 kN of weight; her lift at default power is 300 kN. With engines routed to the limit and an undamaged hull she makes 540 kN and can lift (tested). With a hull under 50 percent she cannot. The bible says Earth is the hard launch, but a player who lands damaged is stuck: needs a Skyward launch service, a booster or a repair rule (a design call, not mine). Logged here, not fixed.
4. **Coast and mountains away from the Cape are half-degree smooth** (55 km cells). Sand and green boundaries are blocky from 5 to 60 km up (colour per ground vertex). Snow ground shows green near the poles. The Earth ground has no biome colours beyond green, sand.
5. **The little dark stones on the grass** are the shared ground-pebble system (Mars-coloured, in main.js); I did not touch it. They look out of place on Florida grass.
6. Frame turns about Mars's pole, so Earth's tilt is data only.
7. Ship cannot yet be refuelled or launch anything on the mount; the vehicle on the mount is scenery. Earth is not yet a start world (OPENING2 steps not done).
8. Hangar interior is bare; training hall and Range Control have a floor, desks and nothing else.

## Files
- New: `src/worlds/earth/{def,terra,earth-data,layout,client,complex,sea,globe,life}.js`, `assets/earth/earth-2k.jpg`, `tools/bake-earth.mjs`, `test/pkg-earth.mjs`, `test/earth-browser.mjs`, 12 voice clips.
- Edited: `credits.json`, `src/worlds/_client-manifest.js`, voices manifest and lines, four test files (see above), stamp files.

## Screenshots
`C:\Users\lilli\AI-Shared\state\cosmos-earth-2026-10-08\` (ground-east-sea, ground-north-complex, ground-west-vab, ground-toward-tower, ground-pad-view, shore-looking-out, shore-along-coast, air-complex, air-pad-from-sea, air-coast, approach-6km, approach-60km, approach-400km, orbit-3000km, orbit-far; `live\` = the same build on the real site; `wip\` = earlier tries).

## Still open
- Design call: how does a ship that lands hurt get off Earth (item 3)?
- Phone speed test on a real iPhone.
- Next packages: Homeguard side, start-world steps, people, more launch sites, launching the vehicle on the mount.
