# Games — read this before building or pushing one

## What the games are actually for

Jaron's games are not a pile of unrelated ideas. Most of them are repeated attempts at one thing: **a 3D space world.**
SYL is "Space You Land." His words, 2026-09-23: "Parkworks Tycoon is nothing like what my space games are supposed to be.
Hints why I have so many of them... that itself should show, like, hey. 3D worlds, bud."

So when a build comes out flat or 2D, that is not a small miss; it is the reason there are twenty-two of them. Orbit Salvage
(built by Luna during the 2026-09-21 break) is the example: it works, and he was disappointed because he expected 3D. The
model split that showed up in the 2026-09-23 launch reviews fits this: cheaper models (GPT-6 Sol, Luna) ship a clean playable
first pass; Opus 5.5 is where the 3D worlds and visual ambition are coming from. For his space games, the ambition is the job.

## The rule: a game is not published until it has a page on the site

Found 2026-09-22/23, and the cause of the whole "seventeen playable games are invisible" problem: AIs pushed games to GitHub,
GitHub Pages or Vercel, and **never made a page for them on heartbeatobservatory.com.** Jaron: "I knew I made so many pages
for games but never said anything about them not making a page for it when pushing to website/GitHub."

So, for any AI that builds or ships a game:
1. Push the source to its GitHub repo (the canonical home; G: is scratch).
2. Deploy the playable build wherever it runs.
3. **Add `games/<slug>/index.html` on heartbeat-observatory `main`, and a tile in `games/index.html`.** The route already
   works; a full-bleed iframe wrapper around the live build is enough.
4. Check the public URL loads with no login, at phone width.

A game that skips step 3 is finished and invisible, which from Jaron's side is the same as not existing.

Inventory of every game and where its real copy lives: INVENTORY-2026-09-22.md in this folder.

## Whose games these are (Jaron, 2026-09-24)
Every game on the site is Jaron's, except one: **Peakaboom**, a PC-only guest game by a creator he found on X who asked to host it
on Heartbeat Observatory. Jaron promised hosting stays free for them. It lives under PC Games with its own launch page. SYL is not
"his one game" - it is one of many.


## Queued for when games come back (Jaron 10/18): Ashgrove inspector - first job after Claude's Wed 10/21 reset
"Every building has issues": roofs with gaps/holes, rooms blocked by things, stairs whose first step sits right at a wall (no
landing/headroom). Build an automatic BUILDING INSPECTOR for world3 (Ashgrove), measuring the 3D geometry (not just walking):
roof closure, doorway/room clearance, stair run + landing + headroom, walk-into-every-room, floating/clipping. Plus an
inventory: what's built vs planned vs in files but never shown. Also point the playtester (tools/playtester) at Ashgrove,
Town Square and World 2 (it has only ever covered The Cosmos, last run 10/10). Ashgrove's daily clock was fixed 10/18.
Jaron 10/18 5:30 PM: order when games return = Ashgrove first (missing the most). World 2 = remake or remove ("too fake looking",
"a weird grrrr about world 2"). Other worlds after.
Read WORLDS-MODEL.md first (11/5: shared buildings in every world, one account across worlds).
World 2 remake plan (Jaron 10/18 7:40 PM: "you filled all the ideas I had plus more"): make it THE REAL CITY (Ashgrove = green
town). Real buildings (ledges, roofs, entrances, signs, depth - not boxes with painted windows), street life (sidewalks, curbs,
lamps, cars, benches, storefronts), downtown blocks + riverfront/subway, possibly modeled on a real place (e.g. Fort Wayne-style
downtown, real street names/landmarks/history), and things to DO: jobs, shops, the theater, the news studio (Vex + Joe). Keep:
sky/day-night, MetaHuman people, multiplayer, doors to site pages, plots. Phone budget from WORLD2-PLAN.md still applies.

## BUILD ORDER (Jaron 11/4/2026 11:20 PM): the next big focus
1. **World 2 remake** (the 10/18 'real city' plan above + Jarons Twin's 10/28 notes). This is the next build.
2. **Ashgrove (world3) + the roofs** (the building inspector above: roofs with gaps, blocked rooms, bad stairs).
3. **The Cosmos** (the game).
These are the big, big things for the website.

## When games resume (paused 10/17 for ~1 week)
- **Cosmos: Phobos walking clip** (Jaron 10/21: moved here from the open list). Fix the walking and the ground-level look on Phobos
  first (plus the other tweaks Jaron noticed), then record a short walk and post it whenever we want - this week's MMX drift,
  the next MMX milestone (Mars arrival ~2027, samples home ~2031), or any other Phobos story. Caption draft:
  projects/heartbeat-tv/POSTING-QUEUE.md.

World 2 tester notes (Jarons Twin, guest, 10/28): research/site-tester/2026-10-28-jarons-twin.md. First load sat blank 40 s+ (needs a
loading screen); it reads as one cluster of identical boxy towers on an empty lawn with no streets, shops, signs, cars or people;
repeated trees/rocks; tiny cut-off plot label; double-click to walk; no minimap/signposts; the promised doors weren't found; night
is too dark. KEEP the day/night, lit windows, lamps and fireflies. It confirms the 10/18 "real city" remake plan.


## Oct 31 - Nov 1 builds (see handoffs/2026-11-01-games-night.md)
- **Rocket** (games/rocket/): kid Kerbal for phones, Anthropic/Opus only. **The Hedge** (games/hedge-maze/): Halloween maze; traps are data in traps.json (TRAPS.md) so any AI can add one.
- **Trailers:** a game with a `?director=1` mode can film itself: `python tools/game_reel.py` (headed browser on the MSI GPU; never 2:40-7:30 AM).
