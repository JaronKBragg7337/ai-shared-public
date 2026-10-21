# The Cosmos: gaps between the design and the game, 2026-10-08 (before the missions round)

Written first, before building. Every line below was checked in the code or by running it, not taken from older notes.
Design = BIBLE-v3 (sections 4, 8.4, 8.5, 10, 11, 12), DECISIONS (10/1 "tower people become quest-givers", "people to hire live in a crew hall"),
the builder rules (mechanics witnessable without a menu, no approve buttons, every place has one thing worth finding).
Status words: **missing** (nothing there), **broken** (there and wrong), **thin** (there, too small to carry play), **fine**.
Ranked by what a new player hits first, after the opening.

## The ranked list (what a new player hits, in order)

| # | Where | What the design says | What the game does today | Status |
|---|---|---|---|---|
| 1 | Earth: leaving | A small ship can go anywhere, slowly (4.6 "cooperation unlocks bigger things, never access"). | A fresh, fitted lifeboat on Earth cannot lift (lift 52 kN class engines vs Earth weight) and the lifeboat has no engineer seat, so the only way to route power (the `power` action) does not exist for it. The nav computer answers "Route more power to engines". Run by hand: with engines forced to 100 it flies Earth to Mars orbit in about 800 game seconds. This is the open design call (how a ship leaves Earth). NOT decided or touched this round. | **broken** (Earth only; open call) |
| 2 | Every world but Mars: the NEXT line | After the boat is fitted the player is told the next step. | The status card says "Ceres has no job board yet. Dig ore or salt..." on **Earth and the Moon too** (the text is not per world). On Earth there is nothing to dig and sell. | **broken** (text), **missing** (content) |
| 3 | Ceres, Earth, Moon: jobs | Port jobs first, then the factions' jobs (10.1 step 6). Tower people and port workers are quest-givers (DECISIONS 10/1). | No job board, no quest-giver, no paid errand on Ceres, Earth or the Moon. Ceres: dig and sell only. Moon: sell ice and buy supplies only. Earth: nobody to sell to. | **missing** |
| 4 | Mars: jobs | A board of jobs; port workers give quests. | One tower quest ("A tonne for the foundation", 400 marks), the Phobos core samples (300 cr each), the Phobos salvage module (150 cr), raider bounties (25 cr). The "Survey Office" is a name; the jobs board is a text tab in the nav computer. 14 of 15 port people only say one line. | **thin** |
| 5 | Storylines (all worlds) | A main arc with the same shape on every world (10.2): the pair, the first ship, the first crossing, the alien-looking ship, per-faction chains that end in an unlock. | None. No story step exists anywhere in code. The alien-looking ship is not in the game; the Phobos distress beacon is the only authored story beat. | **missing** |
| 6 | Hiring off Mars | People to hire wait in the crew hall and walk out to meet you (8.5). Crew costs a signing fee and a wage. | Hiring works only at the Mars Crew Hall. The `hire` and `meet` actions refuse everywhere else. The World/crew sheet prints "walk to the crew hall door, north of the main pad" and the Mars candidates on Earth, Ceres and the Moon too. The status card sends a Ceres pilot "fly home to Marineris" to hire. A player who starts on another world has to fly 1.1 to 1.65 AU first to get any crew. | **missing** (off Mars), **broken** (the sheet text) |
| 7 | Joining a faction | "Taking a faction's job is joining, slowly; there is no sign-up form" (10.2). A switch is one job done in the open (13.2). | Join only by two buttons in the World/crew sheet (a menu), or the Moon's two recruiters. No recruiter on Ceres (Ironclad), Earth (Skyward, Homeguard) or Callisto. Taking a job never joins you. | **thin** |
| 8 | Faction "shifts" | Jobs help one side or both; the board says which in plain words; mechanics are witnessed in the place (17). | `role-work` is two buttons in a sheet with a 20 second cooldown. It moves the balance and pays, but no place, no person, no task. | **thin** (works, not witnessable) |
| 9 | Freight and cargo contracts | Hauling is the job (9, 11.3); "a hold of freight", convoys, parts to joint projects. | No freight contract exists. The hold carries dug matter and salvage; nothing is picked up from a person and delivered to another for pay. Joint and home projects take `parts` through a sheet button only. | **missing** |
| 10 | Preparing the ship | Upkeep is real: fuel, repairs, docking (8.4). A repair page and a parts shop (DECISIONS). | Fuel: free and automatic on any pad (free flight only; a course flies free). Hull: heals itself at 0.5 percent a second on the ground, free. Parts: a supply item with no use except joint-project buttons and the Occator desk. Ammunition and oxygen are inventory only. There is no repair page. | **thin** (design says "priced later"; left alone) |
| 11 | The crew doing things | Hire a pilot, captain, navigator, gunners, comms, engineer. Talk to whoever is flying to give orders. | Six posts, no engineer post. Orders: fly to, hunt, supply run (Mars depot only), roam, land, hold, return. The comms officer only reads the account. Gunners work. Crew can be fired only at the Mars port. | **thin** |
| 12 | Flying: lift, travel, land | Take-off, the long-range drive, arrival. | Course planner, the drive with time compression, arrival sequence, landing on every built world: verified in validate (Mars, Phobos, Deimos, Ceres, Moon x3, Earth). Free flight with fuel works. Big transports/bulkers need the heavy-drive unlock (not built). Fuel not priced. | **fine** (Earth excepted, see 1) |
| 13 | Earth: a trader and a shop | Every port has a dealer, water, food, fuel, parts. | Earth has two people and no shop. "No shop and no trader yet" is written on the board. Nothing on Earth sells or buys. | **missing** |
| 14 | Homeguard on Earth | Homeguard's cities, sea walls, farms; its organiser stands in a yard. | Nothing built. Pruitt stands alone in Skyward's yard (known from last round). | **thin** (needs a first building) |
| 15 | Voices | Every speaking line gets a voice (builder brief). | Works (Kokoro clips, validated). New lines must be voiced and the clip cap raised. | **fine** (tool exists) |

## What this round builds (in order)

1. A mission engine that is **server-held, no accept button, no hand-in button**: a person tells you the job in the Talk panel and you reply "I'll take it" (their dialogue, not an approve screen); steps finish by arriving, carrying, landing, hiring; pay arrives with the last step and the story speaks while you do it. Every step is checked by the authority (position, hold, ship), saved in the world record, and survives a refresh. (items 3, 4, 5, 8, 9)
2. Story threads: **Mars** (the Quiet Band, neutral, five jobs), **Earth** (Skyward and Homeguard threads, a joint finale with a choice), **Ceres** (Ironclad and Greenhaven), **Moon** (Fortis and Technos Prime). Each ends in an unlock or a beat the bible promises (the alien-looking ship is only ever glimpsed in a log, never caught). (items 2, 3, 5, 7, 14)
3. A **job board and hiring desk** on Earth, Ceres and the Moon hub (a dispatcher at each: a person, with a notice board that lists the jobs and the hands for hire). Crew sign on at the desk and come aboard the landed ship. (items 3, 6, 13 partly)
4. The NEXT line and the World/crew sheet speak per world and follow the active job. (items 2, 6)

## Left alone on purpose (named so they are not lost)
- **How a ship leaves Earth** (item 1). Earth jobs in this round are all on Earth. Cross-world jobs are on Mars, Ceres and the Moon.
- Fuel and repair pricing (item 10): needs a number from Jaron; the bible says "priced later" and a stranded new player is worse than a free refill.
- A walkable Homeguard building (item 14) and an Earth shop (item 13): a mission can deliver the first load for them, the building itself is a build package.

## After the missions round (same night, 2026-10-08)

| # | Item | Now |
|---|---|---|
| 1 | Earth: leaving | **unchanged on purpose** (open design call). Earth jobs never ask for a launch. |
| 2 | NEXT line per world | **fixed**: follows the active job, then the job a person here offers, per world; no more "Ceres has no job board" on Earth and the Moon. |
| 3 | Jobs on Ceres, Earth, Moon | **built**: 3 to 5 jobs each (Ceres 4, Earth 5, Moon 4), plus a notice board and hiring desk on each. |
| 4 | Mars jobs | **built**: 5 more (the Quiet Band), on top of the tower job and the Phobos survey. |
| 5 | Storylines | **first pass**: one thread per start world, each ends in a choice or a thing found. The main arc (first crossing, first contact, the Europa find) is not built. |
| 6 | Hiring off Mars | **built**: Earth (Quintero), Ceres (the flight office), the Moon hub (the arrivals desk); six hands each; dismiss works anywhere. The World / crew sheet is honest about it. |
| 7 | Joining by working | **built**: each faction's first job is its oath job; finishing it joins or switches you. The Join buttons remain. |
| 8 | Role shifts | unchanged (still a sheet button). Jobs are the witnessed way now. |
| 9 | Freight contracts | **thin**: jobs carry and hand over loads (supplies, hold matter, a hopper), but no repeating freight board and no player-to-player freight. |
| 10 | Preparing the ship | unchanged (fuel and repairs free). Jobs make the player buy parts, food, load ore, hire hands: the first honest reasons to prepare. |
| 11 | Crew doing things | unchanged beyond hiring off Mars. |
| 12 | Flying | fine; jobs use real flights (Mars to Phobos and back, the Moon's three landings). |
| 13 | Earth shop | still missing (a mission can name one: Okafor says "nothing here sells"). |
| 14 | Homeguard building | **first step**: Pruitt's footing job lays a visible footing that grows with each cartload anyone carries. |
| 15 | Voices | 16 new pitches voiced; Ceres people still have no voices. |
