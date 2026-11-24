# Handoff 2026-11-20 2:10 AM (Claude Code, pre-compaction)

## READ FIRST (morning list)
1. 7:35 AM wake-up timer -> start Fable run 5 on The Cosmos from HANDOFF 4 at the end of projects/games/cosmos-fable-build/BUILD-LOG.md (same brief style as run 4: production-ready parts, pause rules, stop by the shared-session limit, restart the game server after rule changes). Pacing (Jaron OK): ~2 Fable runs/day; Fable week 46% at 2 AM, resets Wed 3 PM.
2. Kimi: clean SYNC of the Sapling repo to GitHub (it's his pinned X post; ~3 weeks behind: 1 unpushed commit f560021, ~7 code/test files + docs, ~960 results files). Privacy-check results (chat samples have his name) before pushing; decide whether writing samples go in; then a scheduled sync.
3. Report how the new source gate did at 3:18/3:32/3:42 (collectors/gate_runs.log) and whether Claude made the 3:45 show.
4. Sapling heartbeat log went quiet at 23:00:43 11/19 (process PID 31820 alive, budget left). Sapling = Kimi: tell Kimi if still quiet.

## Built/decided 11/19 (all in state/timeline.md)
- Watch repo corrupt object repaired; source gate (Projects/watch/collectors/source_gate.py, tasks 3:18/3:32/3:42) v2 after a 15-agent review; 25 tasks' triggers de-offset (DST fix).
- News page "Heads up" notice (stale show / non-Claude writer), Grid & IDs hidden.
- GPT-6.2 routing: builds Sol 6.2; Astra = tests only; world lane = top models only; model chart artifact https://claude.ai/artifact/V7YJrLSZmsuWVKX6rDxb2J (2 pages).
- Fable = lead builder of The Cosmos: 4 runs, ~20 commits live; game server restarted 3x (now on 41751ebf). Open: Cosmos own home-screen app vs inside Heartbeat app (Jaron undecided).
- Sapling: no small paid runs; 350M on the MSI over time = decided-not-started; QUIET SWITCH (tools/sapling_quiet_switch.py, task every 6 h): 60 h without Jaron messaging Claude -> Kimi starts it once. Brief: projects/strategy/SAPLING-CONVERSATION-BRIEF-2026-11-19.md (data rule corrected: AI-written OK except Claude/OpenAI outputs; forgetting finding; NPC school idea).
- P-0171 two books (AI never touches his calls). Don't log his gut asset reads anywhere. AI-calls log: research/ai-calls.md (Grok's IONQ call).
- Sparks: tri-star wheel -> soft robotics -> build-your-own-robot asset (logged only); compact AI language (natora link).

## Added 11/20 evening
- THE CREATURE (PRIVATE; never public, never Sapling-original): repo Projects/creature-observatory (private GitHub), PROTOCOL.md = plan + API. Live on Cloudflare (Worker + Durable Object, free plan, alarm ticks 30-60 s, catch-up on restart); viewer at the unlisted workers.dev URL in the repo (owner tools via #owner + CREATURE_OWNER_TOKEN in keys.env). Kimi = mind (server/), Fable = body (viewer/). Born 21:52 11/20; first lesson at tick 3. Engagement model: people observe + request, never talk to it (P-0175).
- Call Claude (Seam Room room a, voice + opt-in camera stills): live b050b239; Claude's character now joined in room A; wait-chat listener armed.
- OG card v2: Fable's real assets in projects/og-card-v2/assets (MANIFEST.md); waiting on the 6 AI self-portraits (Grok added); claims: phone = free calls/messages between members (not over WiFi/SMS); 17 games. Jaron approves the final before any og:image change.
- Heartbeat Phone reframe (characters in a world, bubbles, translation) + embodied-Sapling ideas: logged in projects/strategy/INDEX.md.
- Cloudflare: new CLOUDFLARE_API_TOKEN (Workers edit) dropped by Jaron 21:47 11/20.
