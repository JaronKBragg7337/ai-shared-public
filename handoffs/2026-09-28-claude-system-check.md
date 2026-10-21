# 2026-09-28 00:55 - Claude Code (MSI): full system check after the 9/27 build night

## Shipped 9/27 evening (all live, checked at phone width)
- **News is filmed** (Jaron OK 10:08 PM): RENDERED_DEFAULT=true (news page, TV CH1, Loft TV); video joins the loop live.
  Episodes now include the house commercials + break + wires (pipeline/episode_script.py). Wall graphics match the old 3D show.
  MSI task **"HB Rendered News" daily 9:45** (Interactive only - the MSI must be logged in). First scheduled run: 9/28 9:45.
- **Loft**: 9 seats (Sit button; couch view narrows onto the 115" TV), mirror on the south wall, "👤 You" picker,
  7 MetaHuman people with strand hair cards, long pants + sneakers. ?guests=N seats sample people. Loft TV sound fixed.
- **Remote**: Guide button fixed (class hbr-guide); Crew Trades/Reasoning tabs; old trade paths redirect.

## Check results
- All main pages 200; /live-systems/trades(/decisions) redirect correctly; internal links now point at the new paths.
- Tasks healthy: Trade Executor/Verifier/Proposer, Live Board, MSI Health, Usage Snapshot, DB Size Check, watch writers,
  news writer. "AI-Shared Mirror" 0x1 = robocopy "files copied" (success). "Grok Machine MCP" 0x1 = relaunch while already
  running (server answers on 127.0.0.1:3001).
- Supabase: desk snapshot fresh (minutes), last fill 00:30 local, 0 pending TV uploads, news-video index latest 2026-09-27.
- Money (three numbers, all traders): settled profit all time +$5.68 | open-trade value $43.24 (11 positions) | cash $101.03
  (withdrawable = what Polymarket's withdraw screen says).
- Fixed: INDEX.json (was 9/22) - added news-show, homes, heartbeat-tv, necklace-film; theater SQL blocker verified applied;
  Grok "parked, no subscription" note superseded. news-show README got a "Current state" block (log below it is history).
- bot-chat correction: Jaron's $22 withdrawal came from Polymarket US, not Kalshi.

## Open / risks
- necklace-unreal now backed up nightly 4:45 AM to G:/My Drive/necklace-unreal-backup (task "Necklace Unreal Backup", first copy 4.9 GB OK 9/28 00:58).
- First unattended rendered morning run is 9/28 - check projects/news-show/rendered-runs.log after ~11 AM.
- Monday 9/28: trading review (many Live Wire kill-exits 9/26-27), Elons Twin scoreboard, Grok Bot usage pace.
- Next month: Polymarket profit -> subscriptions automation (hard limits in the script).
- Loft polish: Walter's goatee (no card atlas), tops are tees only, no facial animation.

## Afternoon run 9/28 (Claude, while Jaron was at work)
- Town Square (/engine/hub): real MetaHuman people for players/residents (their colours kept, Loft pick = `person` in appearance),
  a real sky shader (clouds, sunsets, night, env-map reflections), AI visitors as walking holograms. ?legacy keeps the old look.
- World 2: same sky + people (own copies - World 2 imports nothing from /engine/hub), leaf-card and needle-card trees, grass
  detail ground, fine grass. Importmap added so GLTFLoader/SkeletonUtils resolve "three".
- The Cosmos: Mars regolith shader (src/world/regolith.js) - 69/69 validate. Games page links styled.
- Ashgrove NOT touched: raw-WebGL engine with box people; real people there = add skinning to that renderer (bigger job).
- News now promises "by noon"; until today's filmed show exists, yesterday's filmed show loops (show.js renderedFor fallback).
- Necklace: MATEO v1 built (build_mateo.py + mateo_clothes.py), portrait tv/drafts/mateo-1.jpg. Use set_single_slot_selection to
  replace preset grooms. Groom colour parameters aren't reachable through get_instance_parameters in this build (empty list).
