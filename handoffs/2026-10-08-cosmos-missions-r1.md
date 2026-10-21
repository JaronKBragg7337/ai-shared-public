# The Cosmos: missions round 1 (jobs, stories, hiring desks) - 2026-10-08 night

Commits on main: 370eeb6 (missions), 7cc722c (graphics context, job pointer, HUD text), 1225c0b (job pointer side, pointer lock). Live site and MSI server both on build 4889df7d4c5a5aa2b86a (server restarted at 0 players, /health shows the build, Supabase).
Gap list (written first, with an "after" table): state/cosmos-gaps-2026-10-08.md. Builder doc: games/the-cosmos/docs/MISSIONS.md.

## Gap list top 10 (what a new player hits first)
1. Earth: a fitted lifeboat cannot leave Earth (no engineer seat to route power; nav says "Route more power"). **Open design call, not touched.**
2. The NEXT line said "Ceres has no job board yet" on Earth and the Moon too. Fixed.
3. No jobs at all on Ceres, Earth, Moon. Built.
4. Mars: one tower job and the Phobos survey; 14 of 15 port people say one line. 5 jobs added.
5. No storylines anywhere. First pass built (one thread per start world).
6. Hiring only at the Mars Crew Hall; the World sheet printed Mars hall text everywhere. Desks built on Earth, Ceres, Moon hub; sheet fixed.
7. Joining a faction only by sheet buttons. Now each faction's first job is its oath job: finishing it joins or switches you.
8. Faction "shifts" are a bare sheet button (unchanged; jobs are the witnessed way now).
9. No freight contracts (still thin: jobs carry and hand over loads; no repeating board, no player freight).
10. Preparing the ship: fuel free, hull heals free, parts have no use. Left alone (bible: "priced later"; needs a number from Jaron).
Also: no shop on Earth (missing); Homeguard has nothing built (first footing now).

## What was built (all start-to-finish playable; no accept screen, no hand-in button)
Engine: server/missions.mjs checks position, hold, supplies, hopper and ship; saved in the world record; survives a restart; a player is sent only their own jobs. Talk panel: "Is there paid work for me?" -> the offer in the person's words (voiced) -> "I'll take it". The story speaks in the ship log as steps finish. The goal arrow, the NEXT line and a Jobs block at the top of World / crew follow the active job.
Mars, The Quiet Band (neutral): Shift notes (carry the folder runner, supply desk, Salvage trader, runner; 70 cr). A part for the weather mast (buy 2 parts, bring to the weather officer; 150). A hand on the flight deck (sign a hand at the Crew Hall; 140). The survey band (fly to Phobos, take the cargo module's recorder, fly home, tower; 240). The long glass (see the unnamed light; choose open band or sealed book; 300).
Earth, Cold Fuel (Earth only, no launch): Walk the line (Skyward oath; 150). Ask politely (Pruitt, Quintero, Okafor; 120). A footing for the first wall (Homeguard oath: dig a 300 kg cartload, carry it to the stakes; a visible footing grows with every cartload anyone brings; 150). A hand for the countdown (hire at Quintero's desk; 140). Cold fuel (finale: "a slow leak, nobody's name" is the joint answer, "put Dale's name on it" the competing one; 300).
Ceres, Salt and Water: Ore for the foundry (Ironclad oath: 1 t of ore, land, foreman; 160). Salt for the filters (Greenhaven oath; 150). The strike notice (carry the notice Roth, Marta, back; choose strike or hold; 260). Hands for the Works (hire at the flight office; 140).
Moon, The Two-Way Run: Do not touch (walk 1.1 km to the first footprints; 90). Rations for Shackleton (Fortis oath: buy 6 food, fly to Shackleton; 200). A sealed tray (Technos oath: carry to Daedalus; 200). The two-way run (4 parts from the Technos fab to the Fortis quartermaster; joint; 320).
Desks: Quintero (new person on Earth), the flight office (Ceres), the arrivals guide (Moon hub): six hands each, a notice board beside each. A hand signs on at once and comes aboard the landed ship; dismissing works anywhere and puts them back on the list. Faction jobs move the world's balance and home strength (F4) and the player's standing (F5).

## Tests and results
- node test/validate.mjs: 1982 passed, 0 failed (includes new test/pkg-missions.mjs: 80 checks on the real authority with real purchases, real flights Mars-Phobos-Mars and between the Moon's three landings, real digging, refusals, restart, privacy, desks). After the two later small commits the full validate was not rerun; pkg-missions (80/80) and phone-check (33/33) were.
- test/missions-browser.mjs (iPhone WebKit, real local server, real screens): Mars lookout choice, Earth line check and pay, desk hire, panels inside 393x852. All behaviours passed; one wrong expectation in the test itself was fixed afterwards and not rerun in full. Screenshots: games/the-cosmos/docs/qa/missions/.
- test/context-restore-browser.mjs: lost then restored context keeps normal graphics (pass). A context that never returns still falls back to safe mode (twoplayer-browser pass).
- Playtester on live: Earth+Skyward 15+5 min, state/playtest/2026-10-09_00-10/REPORT.md (0 blockers, 0 serious). Earth+Skyward phone 30 + desktop 5 on build 3744d95, state/playtest/2026-10-09_00-44/REPORT.md (0 blockers, 2 serious: the bot re-tapping the World / crew panel, and "context not restored", see below). Mars default 15+5 on 3744d95, state/playtest/2026-10-09_01-24/REPORT.md (1 blocker: an uncaught pointer-lock refusal from random tapping, FIXED in 1225c0b; "stuck walking to the Shift runner / Lookout" in the tower cab looks like the bot's steering). The live Earth run showed the new NEXT line working after the boat was fitted. Not rerun on the final build 4889df7.

## Also done (coordinator's priority bug)
- A lost WebGL context no longer restarts the game into safe mode: it waits for the browser to give the context back (three.js rebuilds) and falls back only if it does not return in 12 s (25 s if the page was hidden) or is lost three times in a minute. Verified on live in iPhone WebKit: lost then restored in 14 ms, frames continue, no banner. The playtester's "never drew again" still fires on the heavy Earth scene (its restore step waits 4 s and only 'lost' was seen; software rendering is slow there). Not reproduced on Mars. UNVERIFIED on a real iPhone and on a heavy scene.
- HUD NEXT/dim text 10 -> 12 px. Not done: the unlabeled input, touch keys overlapping World / crew on desktop, "fetch failed" in the opening dig (not found), pinch-zoom lock.

## Verified: local / live / not
Local: everything above. Live: site and server on the new build, Earth and Mars playtests, the NEXT line, context restore in WebKit. Not verified: a live player taking a job by hand (the playtester does not take jobs; the local browser test did), voices playing on a phone, Ceres and Moon jobs in a browser (headless only), the Earth footing prop in a screenshot, real iPhone speed.

## Not decided / not built
How a ship leaves Earth (gap 1): Earth jobs avoid it, a new Earth player still cannot fly away. Fuel and repair pricing; repeating freight board; an Earth shop; Ceres voices (their pitches are text); the main arc (first crossing, first contact, Europa); Callisto, Wanderhome and Corsair jobs; faction switch rules beyond the oath (labels, licenses, once per season) belong to F7.

## What's next
The playtester should learn to take a job (talk, "I'll take it", walk the steps). Then: repeating jobs per desk, an Earth dealer, fuel prices once Jaron names a number, Ceres voices, a second Homeguard building after the footing.

Still open for Jaron: the Earth launch call; fuel and repair pricing.
