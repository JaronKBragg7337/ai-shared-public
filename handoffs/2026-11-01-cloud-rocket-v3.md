# Handoff 2026-11-01 - cloud session (Opus): Rocket v3 = Moon + satellites + space station

Who: a cloud Claude Code session (Opus 5.5), started by Jaron's routine on the expiring cloud credit. Anthropic models only, no other AI tools.
Where: heartbeat-observatory branch `cloud/rocket-v3`, **PR #28 (draft, NOT merged):**
https://github.com/JaronKBragg7337/heartbeat-observatory/pull/28

## What I built (games/rocket/)
- **The Moon**, Kerbal-style scale with real rules: radius 200 km, gravity 1/6, 12,000 km out, goes around clockwise
  (same way a rocket leaning right goes), always shows the planet one face. Patched conics: inside its pull only the
  Moon's gravity bends your path.
- **Goal ladder continues:** Come home safe (now unlocks a 3rd stage) -> Fly past the Moon (legs) -> Land on the Moon
  (flag with your name, planted and saved) -> Come home from the Moon (satellites) -> Put a satellite in orbit (relays)
  -> Build a ring of 3 relay satellites (telescope + station parts) -> Start a space station -> Dock a new part ->
  Grow your station to 4 parts. Then free play.
- **Satellites** (weather / relay / telescope, one-line job each) and the **station** are saved with their orbits and
  stay up between flights (Kepler orbits on a saved sky clock). Map shows them, relay links (green = can see each other),
  the station; 3D shows them when near, with name tags.
- **Helpers on:** one context button at a time (To the Moon, Land on the Moon, Plant flag, Fly home, Release satellite,
  Start the station, Go to station). The helper really flies (points + engine); a green line says what it is doing.
  Flight still has at most X, Map, one action button, speed.
- **Do it yourself:** live slider hints for every new moment (ghost Moon timing, stop when the path reaches the Moon's
  pull, aim lower, brake/burn/stop for landing, fly-home arrow, dock range). Dock button lines you up within 40 km /
  40 m/s. Far out in space the DIY engine runs at 15% so small taps can aim.
- Map: Moon, its orbit and pull, path into the pull (purple), "Burn when the Moon is here", "Meets the Moon here",
  closest pass, "Hits the Moon here", Home X.
- Old saves migrate (v1/v2 -> v3). A save that already came home gets the 3rd stage and the Moon as next goal.
- `?dev=1` = separate test save with parts unlocked (never touches real progress). Use it to review fast.
- New files: missions.js (helpers, predictions, hints), save.js (goals + migration), test/*.mjs. physics.js grew.

## Test results
- `node games/rocket/test/missions.test.mjs`: **53/53 pass** (~4 s). Flies every new goal in Helpers-on AND Do-it-yourself
  (scripted kid uses only slider + Burn/Stop + the buttons the game shows): Moon flyby + home, Moon landing + flag + home,
  satellites, relay ring (still a ring 3 days later), station core, 3 docks (2 helper, 1 DIY), save migration, orbit maths.
- `node games/rocket/test/files.test.mjs`: index.html refs, module imports and element ids all resolve. `node --check` OK.
- I also played it in **headless Chromium at 390x844** (three.js served locally): full helper Moon trip (landed 1.7 m/s,
  flag "Jaron", home, goals saved), 6 satellite/station flights (ring + dock worked), DIY Moon transfer + aim by hints.
  No page errors. Those runs found ~10 real bugs, all fixed in the PR commits.
- Last browser check: DIY Moon landing following only the on-screen hints -> touchdown 2.1 m/s, 1,821 kg fuel left, no errors.
- A full DIY round trip in the browser hit the 30-min background limit during descent (headless runs at real time there); the
  pieces each passed (transfer, aim, landing) and the full DIY round trip passes in the node test.

## Not verified (main session: please check at phone size)
- Real iPhone: touch, frame rate (headless ran ~10 fps), how long trips feel at 60 fps, sound, label readability.
- Hangar with 7 parts in 4 columns at 375 px (looked OK at 390 px).
- Looks: Moon ground (craters, planet-shine on the night side), station shapes, flag size.
- DIY is harder than Helpers-on by design; whether a real kid can follow the landing hints (burn/stop timing) needs a real try.

## Main session must check before merging
1. Open the Vercel preview of PR #28 at phone width; try `?dev=1` (Moon goals) and a normal visit (old save carries over).
2. Helper Moon trip: To the Moon -> Land on the Moon (time slows in the Moon's pull so the button can be tapped) -> Plant flag -> Fly home.
3. One satellite release and one dock.
4. Merge only if it feels right; I did not touch main.

## MSI connector
Heartbeat_MAI connector worked: start line appended to state/timeline.md; done line + mailbox note sent at the end.
