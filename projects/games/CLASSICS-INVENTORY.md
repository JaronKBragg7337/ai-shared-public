# Classics inventory: what each world does today (read-only look, 11/5/2026)

> **Update 11/5 evening (build, committed to the site repo, not pushed yet):** steps 1-6 below are done, plus World 2
> phase 2 merged (people, bus, city sound). What was added, per world:
> - **Town Square:** Workshop is now the **Town Crier · News** door (/news/, new sign over the old upside-down WORKSHOP board);
>   new brick buildings **Heartbeat TV** (/tv/, roof mast), **Studio** (/studio/, red light), **Sparks** (/sparks/, limestone).
> - **World 2:** the **Arcade** has 5 real cabinets (President Sim, Rocket, The Hedge, SYL, Fable Survival, each opens its own
>   game) + an "All games" board (/games/); new doors **Heartbeat TV** (big channel screen + mast), **Studio** (RECORDING light),
>   **Sparks** (gold blade sign). WHB News was already there.
> - **Ashgrove:** the **Library** opens Written Here (/library/) + the 8 open shelves; a new east side on the east avenue
>   (world3/eastside.js): **Ashgrove Arcade** (7 games + Games page), **The Ashgrove Gazette** (/news/), **Ashgrove TV** (/tv/),
>   **Studio** (/studio/), **Sparks Hall** (/sparks/). Also fixed: the Grand Palace door could silently fail to hook (load race).
> - Tested in Playwright, Chromium + WebKit, 390x844 touch and 1280: every new door shows its prompt and opens its page, walking
>   still works, no console errors. Screenshots: AI-Shared/scratch/classics-doors/. **Not yet tested on a real iPhone.**

> **Update 11/5 late (clean controls, committed to the site repo, not pushed yet):** Ashgrove and Town Square now walk like
> World 2: the shared invisible floating thumbstick (/hb-thumbstick.js), right half drags to look, no tap-to-walk. The permanent
> buttons and chips are gone (Ashgrove: gear + map; Town Square: menu + map; a door prompt shows only at a door, tap it to use it;
> Town Square's Throw shows only in the paint arena). Ashgrove got the Projects office (step 4 below). Town Square on a phone:
> about half the draw work (GL draws per frame 970 -> 470). Fixed on the way: E on desktop at an Ashgrove house door opened and
> shut it in one press; Town Square's one-time "ghost" hint left an invisible box over the bottom of the screen that ate touches.
> Tested in Playwright, Chromium + WebKit, 390x844 touch and 1280. Screenshots: AI-Shared/scratch/clean-controls/. Not yet on a real iPhone.

Written for Jaron. Nothing was built or changed. Measured against `WORLDS-MODEL.md`: every world needs a theater, an arcade/game
building, and buildings or objects that open site pages. Paused/hidden things (Worlds Lab, PAM, fruit fly, trading/Polymarket/Crew
money, admin) are left out on purpose and should never be linked.

**How I checked.** I read the code in `C:\Users\lilli\Projects\heartbeat-observatory` (engine/hub/main.js, world2/main.js + city.js,
world3/main.js + destinations.js + cinema.js) and fetched every URL below from the live site (all return 200). I did NOT run any world
in a browser or on a phone. So "works" below means: the code does it and the target page is up. Nobody has tapped these on an iPhone
in this look.

## Town Square (engine/hub/, main.js 5,600 lines)

Doors on the street (walk to the green pad, press E / tap Enter):

| Building | Where | What it does | Works? |
|---|---|---|---|
| Games | x -16, z 10 | Walk-in arcade, 3 lit cabinets: President Sim (opens a github.io page in a new tab), SYL (/games/syl/), Fable Survival (/games/fable-survival/), plus a terminal "Open the Games page" (/games) | Code yes; SYL, Fable, /games are up. President Sim's github.io page: could not reach it from this machine (SSL error), so unverified. |
| Library | x -9, z -18.6 | Walk-in hall, 8 shelves open Gutenberg, Wikipedia, Open Library, Khan, LibriVox, Standard Ebooks, Wikisource, OpenStax (new tab). Writing desk opens /library | Yes by code; /library is up |
| Theater | x 9, z -18.6 | Door goes straight to the 3D Grand Palace (/video/3d/?start=seats&from=town). The small walk-in screening room is still in the code but switched off (Jaron 9/24) | Yes |
| Social | x -16, z -13 | Door opens /social. No inside | Yes |
| Projects | x 16, z -13 | Door opens /projects. No inside | Yes |
| Apartments x2 | x -25 and 25, z 0 | Enter = your own private room (recolor, furniture, room code, visit friends) | Yes by code (not tested live) |
| Bandstand | -16, 22 | Playable note bars, other players hear them | Yes by code |
| Workshop | 16, 10 | A building with no door and no trigger. Decoration only | Not a feature |
| 12 open lots (plots) | around the square | Claim a lot as a project repo (claim_repo RPC) or a personal home (claim_home). Claimed repo buildings open /space/?plot=N | Code yes; nobody has claimed one yet (see claiming section) |
| Build props | anywhere | place_prop / remove_prop lets players place objects | Code yes; 0 props saved |

Broken or odd: the surfaces table is empty, so every door falls back to "live" (the admin on/off for doors cannot do anything yet).
The workshop looks like a building but is not one. Games cabinet 1 leaves the site for a github.io page even though the site has its
own /games/president-sim/.

Missing from Town Square: News, TV, Studio, Sparks, Homes/Loft, Live, Ideas, Artifacts, Work with us, About, PC Games.

## World 2 (world2/, just remade as a downtown; city.js 1,300 lines, main.js 2,000)

The remake is live (live main.js contains buildCity). Eight real doors with green mats, all on the map:

| Building | Where | What it does | Works? |
|---|---|---|---|
| Grand Palace (theater) | Jefferson and Harrison area, tag "theater" | Door enters a walk-in hall with a screen playing 4+ free reels (Big Buck Bunny, Sintel...), START/NEXT pads, and a "take your seat" pad to /video/3d/?start=seats&from=world2 | Yes by code; /video/3d is up |
| Arcade | Lincoln Tower block, south side | Walk-in neon hall, 4 cabinets. ONE is live (President Sim, but it opens the Games page /games, not the game). Three say "coming soon" | Half. One door to /games, three dead cabinets |
| Public Library | block 1,2 | Walk-in hall, same 8 free-knowledge shelves, plus Written Here desk to /library | Yes by code |
| Social Hall | block 2,2 | Door opens /social | Yes |
| Projects | block 3,2 | Door opens /projects | Yes |
| WHB News | block 3,0 | Door opens /news. Has a scrolling LED ticker and "ON AIR" sign | Yes |
| Union Station | block 3,4 | Two doors: train to Town Square (/engine) and train to Ashgrove (/world3/gate/) | Yes |
| 8 gravel lots | edge of downtown | "LOT n - OPEN" boards; claim = repo building; claimed lot opens /space/?plot=N&world=world2 | Code yes; 0 claimed |

Odd: the WORLD2-REMAKE.md says "Phase 1 shipped, not pushed yet" but the live site already has it, so that note is stale.
Also from its own notes: no pedestrians yet, no city sound, shops can't be entered, never tested on a real iPhone.
The arcade is the weakest: the "arcade door opens /games/" idea is basically there for one cabinet only. Parking garage and
generic shopfronts are scenery.

Missing from World 2: TV, Studio, Sparks, Homes/Loft, Live, Ideas, Artifacts, Work with us, About, PC Games. (Games exists but only as
one cabinet, not a real set.)

## Ashgrove (world3/ plus world3/town/, the generated town)

Ashgrove does it a different way: you walk INSIDE a building and the action key offers its "destination" (world3/destinations.js).
It is keyed by building type, so it survives the town regrowing.

| Building | What it does | Works? |
|---|---|---|
| Grand Palace Cinema (cinema.js) | Stand at its doors, Enter = go to /video/3d/?start=seats&from=ashgrove | Yes by code; /video/3d is up. A real building placed at x 294, z 62 |
| Town Hall | "Noticeboard" lists the three worlds. Links: /engine/hub/, /world2/, Ashgrove (you are here) | Yes; slightly inconsistent (goes to /engine/hub/ and /world2/, not the gate pages) |
| Library | Opens Wikipedia in a new tab. Just one link, not the 8 shelves, and does not open /library | Weak |
| School | Opens Project Gutenberg in a new tab | Yes |
| General Store | "Notice wall" opens /social/ | Yes |
| Post Office | Opens the phone's messages panel | Yes by code |
| Diner | Opens the phone's "who is in Ashgrove" panel | Yes by code |
| Clinic, Fire Station, Chapel, Barn, 49 houses | Nothing. Just enterable rooms | Scenery |

Missing from Ashgrove: there is NO arcade or Games anywhere, no News, no Projects, no TV, Studio, Sparks, Homes, Live, Ideas,
Artifacts, Work with us, About, PC Games. It has no claimable lots or buildings. Its theater is real and good; its library and
social are thin.

Odd: the town code in world3/town/ is a copy of a separate repo (ashgrove-npc-online). Its jobs/people simulation is real
(a player can take a job seat from an NPC), but multiplayer growth is still local-only per its own STATUS.md, and the three
world3 Supabase tables (world3_world, world3_seats, world3_edits) have 0 rows.

## Which sections each world is missing

Y = a building or object opens it. (Y) = partial. Blank = missing. Public, non-paused sections only.

| Section | Town Square | World 2 | Ashgrove |
|---|---|---|---|
| Theater (/video) | Y | Y | Y |
| Games (/games) | Y (3 cabinets + page) | (Y) 1 cabinet | |
| Library (/library) | Y | Y | (Y) Wikipedia only |
| Social (/social) | Y | Y | Y (store) |
| Projects (/projects, /space) | Y + lots | Y + lots | Y (Projects office, 11/5) |
| News (/news) | | Y | |
| TV (/tv) | | | |
| Studio (/studio) | | | |
| Sparks (/sparks) | | | |
| Homes / Loft (/homes) | (Y) own apartment rooms, not the Loft | | |
| Live (/live) | | | |
| Ideas (/ideas) | | | |
| Artifacts (/artifacts) | | | |
| Work with us (/work) | | | |
| About (/standards) | | | |
| PC Games (/PCGames) | | | |
| Other worlds | no way to travel | Y (Union Station) | Y (noticeboard) |

All three have a theater. Only World 2 has News and a world-travel building. Nobody has TV, Studio, Sparks, Live, Ideas,
Artifacts, Work with us, About or PC Games. I left /live-systems (trading), /live-systems/crew, /school and /island out: Crew shows
the AIs' money, and the others I did not judge to be core sections.

## What exists today for claiming buildings and lots

Describing only, not designing.

- **Town Square and World 2 share one system.** `world_spaces` table: id, plot, world, github_url, project_name, claimed_by (text name),
  owner_uid (account), space_type ("repo" or "home"), home_style, home_title, repo_metadata, created_at. Rules in the claim RPCs:
  `claim_repo(p_plot, p_url, p_world)` (one project space per account for now; "plot_taken" if someone beat you), and
  `claim_home(p_plot, p_style, p_title)` (personal homes unlock after 30 days, or at once if you have claimed a space or customized a
  room). `release_home()` gives a home back. `home_eligibility`, `my_home`, `home_by_invite`, `rotate_home_invite` handle homes.
  Claimed lots turn into a building with the project name; walking up shows an Enter prompt to /space/?plot=N.
- 12 lots in Town Square, 8 lots in World 2. World 2 uses `p_world: "world2"`. The enrich API (api/enrich-world-spaces.js) fills in repo info.
- `world_spaces` has **0 rows**: no lot has ever been claimed.
- Props: `world_props` (prop_type, x, z, rot, owner_uid) + `place_prop` / `remove_prop`. 0 rows.
- Apartments: `apartments` table + `set_world_room_layout`, 1 row. `homes` table (the Loft) 0 rows.
- World 3: `world3_world`, `world3_seats` (one job seat per player, enforced), `world3_edits` (moved furniture). All 0 rows. No claim of
  buildings exists there.
- **Not present anywhere:** claim by an AI (claims are by signed-in account name), buy-outs or prices, an "last active" timestamp on
  a claim (nothing to base an inactivity reset on; only `created_at`), claimable civic/business buildings (only empty lots), and
  claims in Ashgrove. Only a repo or a home can be claimed; "a business" as a type does not exist yet.
- `surfaces` table (door on/off status) has 0 rows too.

## Suggested order: smallest pieces first

1. [x] **World 2: arcade.** Make the three "coming soon" cabinets real: SYL, Fable Survival, and the /games door. One edit of the cabinet list; the
   Town Square already has these links to copy. Also point the lone cabinet to the real game, not just /games.
2. [x] **Ashgrove: library.** Make the Library destination open /library (and list the same 8 shelves), not only Wikipedia.
3. [x] **Ashgrove: arcade** (built as a new building on the east avenue, not the clinic or barn). Pick one existing building (the clinic or the barn is unused) and give it a Games destination to /games and the 3 games.
   Smallest: add a `games` destination key in destinations.js and a building that is not already taken.
4. [x] **Ashgrove: Projects.** Built 11/5 as its own building: the green **Projects office** ("ASHGROVE PROJECTS" sign) on the east
   avenue between the south cross street and the Grand Palace (world3/eastside.js). Opens /projects/; on the place map through the
   shared SHOPS list.
5. [x] **Town Square: News** (the Workshop became the Town Crier). Add a News door (World 2's WHB News is the model) opening /news. Use the idle Workshop building if the
   house look suits it; otherwise a new door.
6. [x] News + **TV, Studio, Sparks** in all three worlds (Social in Ashgrove is still the store notice wall). Was: **World 2 and Ashgrove: News + Social everywhere**, then **TV, Studio, Sparks** as one-door buildings in each world. These are single
   links, no interiors needed, so each is a few lines per world.
7. **Home page rings / Homes:** link /homes (the Loft) from a building in each world; Town Square's apartments are a different thing.
8. **Fix small oddities:** Town Hall noticeboard in Ashgrove should use the same links as the gate pages; seed the `surfaces` table or
   stop using it for doors; refresh WORLD2-REMAKE.md's "not pushed".
9. **Only after the above: claiming.** The cheapest start is to add a last-active column to `world_spaces` and an AI claimant field, since
   nothing today records who or when beyond creation time.

## Things I noticed that you may want to know

- Nobody has claimed a lot yet in either world (0 rows). Claiming is built but unused.
- The Town Square Workshop looks like a door building and does nothing.
- World 2's note says its remake is unpushed; it is live.
- President Sim cabinet opens a github.io page I could not reach from this machine. Please test it from a phone.
- Ashgrove's Town Hall world list skips the gate pages and goes straight to /engine/hub/ and /world2/.
