# Handoff 2026-10-01 6:50 PM (Claude Opus) - The Cosmos sprint + the job router

## In flight right now
- **Luna 6 publishing multiplayer** (ho-sol, branch cosmos-mp, brief Projects/LUNA-BRIEF-publish-multiplayer.md, report
  Projects/luna-publish-report.md): validate, commit, rebase on main, push, start the authority server on the MSI
  (localhost:8390, scheduled task), test via https://cosmos.heartbeatobservatory.com (tunnel route Jaron added 4:06 PM).
  Supabase SQL already applied by Claude (10 cosmos_* tables, RLS, server-only RPCs) to the Heartbeat project.
  When done: read the report, tell Jaron briefly, multiplayer test with Lilith/his son.
- **Luna 6 building the router** (AI-Shared/projects/router/LUNA-BRIEF-router.md -> tools/route.py, state/routing.json,
  usage readers, tests). When done: dry-run it, then use it for every job handed to another AI.
- **Timer 7:33 PM** (session-only): Sonnet starts the fleet - hostiles become real crewed walkable ships players can also use
  (DECISIONS.md 10/1 5:59 PM). Route it (looks -> Sonnet).
- **Darios Twin**: Grok Bot weekly reset ~6:34 PM; check grok-money.py shows trades again.

## Live today (heartbeat-observatory main)
8afa199 tower elevator/people/climbing/dirt -> 5b17b01 comms officer, money, traders, quest, phone buttons, local save ->
98dd86d space travel (Phobos/Deimos) -> c05f13d speed-up in climb/landing + pilot Talk panel.

## Decided today (projects/syl/DECISIONS.md has the full entries)
Money/wages (numbers builder-only in SPOILER file), currencies, tradable regolith, server-held shared world, phone buttons,
multiplayer now, "many, not one" (own ship + pad per player, crew hall), fleet of real ships, trailer movie in ~1 week and
promote within the month.

## Meters and money
Claude: session resets ~7:30 PM; Jaron bought two 15-credit packs today; he thinks Claude should go to the $100 Max plan
(his tap). Codex: banked reset used 6:13 PM (one left, expires Oct 29); weekly full. Grok Bot: reset 6:34 PM; Darios Twin is
Primary Bot; Sams Twin inactive. Grok Build CLI updated to 1.0.46 and verified (grok 4.7).

## Rules learned today
- Route by role (memory: route-jobs-to-other-ais). Luna 6 = chores with full access; Claude only orchestrates/reviews cheaply.
- A wait-loop matching process command lines must not match itself (it did: 20 min lost).
- Sol's sandbox can't commit; Luna with danger-full-access can.
