# Games inventory — 2026-09-22

Produced by Codex on GPT-6 Luna at Jaron's ask, read-only, nothing changed or merged. Saved here by Claude Code because it
existed only in a chat and a screenshot, and it answers a question that has been costing Jaron real work: which copy is real.

## The two findings that matter

**1. GitHub is the canonical copy. G: is stale.** In every row where the copies differ, GitHub is newest or tied. G:'s
Parkworks is 23 commits behind production; G:'s SYL branch is 2 behind. Nothing found G: ahead of anywhere. So the games have
the same answer AI-Shared already gave for documents: one home, and the private local folder is scratch. The home is
github.com/JaronKBragg7337.

**2. Twenty-one playable things exist that nobody can reach from the site.** Thirteen complete games have source, assets and
builds present but no route on heartbeatobservatory.com — the checked candidate routes return 404. Eight more (the Free Game
Hub minigames) are live on GitHub Pages but not linked from the site at all. This is not a remake problem. The games are
built. They are unlisted.

## Live on heartbeatobservatory.com (6 titles, 7 pages)

| Game | Route | Note |
|---|---|---|
| The Cosmos | /games/the-cosmos/ | deployed files match GitHub main |
| Fable Survival | /games/fable-survival/ | site has a compiled build; source is the standalone repo |
| SYL — Space You Land | /games/syl/ | /PCGames/syl/ is a legacy desktop experiment, on hold |
| Parkworks Tycoon | /games/parkworks/ | deployed bundle matches the current build |
| Rustfall | /games/rustfall/ | deployed bundle matches the current build |
| President Sim | /games/president-sim/ and /games/president-sim/classic.html | 3D is current; classic is the older edition |

## Built, complete, and unreachable (13)

Air Vehicles / Vector 35 VTOL Test Range · MindGames · Robot Evolution Lab (MEC-01) · Signal Drift · Wasteland Commons ·
The Necklace Show · Rift Clash · Cyber-Trench Overdrive · Frontier Empires · New Age of War · Northstar Addressable World ·
Pirate World: Sea of Fortune · The Defender 3D

All have a newest copy identified and a most-complete copy identified. All return 404 on the checked candidate route. Rift
Clash also 404s on its GitHub Pages URL.

## Live somewhere else, unlinked (8)

Free Game Hub: TRACE, Roll & Reach, The Loop, LATTICE, FLUX, DRIFT, SENTINEL, TWIST — playable now at
https://jaronkbragg7337.github.io/Free-Game-Hub/ and not listed on heartbeatobservatory.com.

## Not a game yet

Kurearthis — only a README was found; no runnable copy located. SpaceYouLand and SYL-Testing-pvp are SYL-adjacent
experiments (an Unreal project and a multiplayer testbed), not the canonical SYL source, and have no listing.

## What this changes

The cheapest next move is not building. It is listing. Each unreachable game needs a page under /games and a tile on the
games index; the artifact it points at already exists. Nothing in this list requires Supabase, so none of it is blocked by
the outage.

Verified by Codex: folder contents, repo tips, branch differences, selected build hashes, GitHub state, current Games and
PCGames listings, route responses, byte matches for selected deployed files. Not verified: gameplay quality, and any route
outside the ones checked.

## UPDATE, same evening (Codex on GPT-6 Luna, read-only, nothing changed)

The "unreachable" count above was too pessimistic. Nine of those thirteen games are **already live on the internet**, on
GitHub Pages or Vercel. They are simply not linked from heartbeatobservatory.com. Combined with the eight Free Game Hub
minigames, **seventeen playable games are online right now and invisible from the site.**

The site already serves `games/<slug>/index.html` as a route, so no rewrite is needed. Each of the nine needs one new HTML
file that frames the existing build, plus a block in `games/index.html`. No game files move.

Live already, needs a wrapper page (9):
- MindGames — jaronkbragg7337.github.io/MindGames/
- Robot Evolution Lab — jaronkbragg7337.github.io/robot-evolution-lab/
- Signal Drift — jaronkbragg7337.github.io/signal-drift/
- The Necklace Show — jaronkbragg7337.github.io/the-necklace-show/
- Northstar Addressable World — jaronkbragg7337.github.io/northstar-addressable-world/
- The Defender 3D — jaronkbragg7337.github.io/the-defender-3d/
- Cyber-Trench Overdrive — cyber-trench-overdrive.vercel.app (use the stable address; the repo's preview link redirects to a sign-in)
- Rift Clash — rift-clash.vercel.app (bots work with no server; networked multiplayer needs a game server running)
- Wasteland Commons — wasteland-commons.vercel.app (page responds; its production relay still needs a server-only key and a
  two-client check, so treat multiplayer as unproven)

Needs a build first (3):
- Frontier Empires — `npm run build`, copy dist. Vite base is already relative. No backend needed. Portraits optional.
- Air Vehicles — `npm run build`, copy dist. Change the Vite base to relative first.
- Pirate World: Sea of Fortune — build, copy dist, change base. **Blocked:** the app requires Supabase and its configured
  project is paused. This is the free-tier two-project limit showing up in a game, exactly as suspected.

Not a browser game (1):
- New Age of War — an Unreal project with no packaged build. An informational page is the only honest route today.

Caveat Codex named: it checked that those deployments respond, but did not play them inside the wrappers or at phone width.

Target is GitHub `main` for the site. The G: checkout is on a non-main branch with unrelated local edits — more evidence that
G: is scratch, not home.

## DONE, and two unlisted pages explained (2026-09-23)

All nine wrapper pages were built by Codex overnight and are live on the public site — checked with no login: mindgames,
signal-drift, rift-clash, the-defender-3d, wasteland-commons all return 200 at heartbeatobservatory.com/games/<slug>/.
The games directory on main went from 6 entries to 18. No game code was touched.

Two pages appear in that directory that no inventory listed, both accounted for by Jaron 2026-09-23:
- `syl-test` — old, a small test of his, not the canonical SYL.
- `orbit-salvage` — built by Luna during the break. Jaron's verdict: disappointing, he had expected a 3D game. Kept, not
  promoted. Nobody needs to re-investigate either one.

Still open from the list above: Frontier Empires and Air Vehicles need a build; Pirate World is blocked on a paused Supabase
project; New Age of War is Unreal with no browser build.

