# Handoff 2026-11-01 ~1:15 AM CST - games night (Jaron: "a perfect example of flow, cost and timing")

## FIRST after compaction: re-arm `python tools/mailbox_wait.py` (background). Main-session mode stays on.

## Shipped Oct 31 - Nov 1 (all live, Anthropic-built: Claude Opus 5.5 main session + Opus subagents)
- Rocket game: heartbeatobservatory.com/games/rocket/ (site repo games/rocket/: index.html, game.js, physics.js, style.css).
  v1 hangar/launch/clouds/space; v2 stages, orbit, map path (orange=lands, green=orbit, arrows, Start flag, mini-planet),
  come home + heat shield, 1x/10x/50x; v2.1 flight guide (before/now/why/tip, stops repeating after 3 flights) + Do-it-yourself
  mode (unlocks after first orbit). Plan: projects/games/rocket-game/PLAN.html. Next: satellites, space stations, the Moon (v3).
  Rule: rocket game = Anthropic models only, Opus-led (Jaron 10/31).
- The Hedge (Halloween maze): heartbeatobservatory.com/games/hedge-maze/ (games/hedge-maze/). 35x35 maze, 5.4 m hedges, fog,
  the Eye + shadow creatures, lantern checkpoints, arches + LINE OF SIGHT (hedges block the Eye: "Hidden in the hedge's shadow"),
  joystick-stick fix, live title flight behind a see-through card, ?director=1 scripted trailer mode, ?dev=1 test panel.
  Traps are DATA: traps.json + TRAPS.md (any AI adds traps without code). 30 traps: Jaron's loop + Claude, Terra, Gemini, Kimi,
  Satya, Darios, Pips Twin, Jarons Twin. Helper to merge an AI's JSON: projects/games/hedge-maze/merge_traps.py
  (only Jaron's loop runs; other loops become signs). HOLD: Jaron's "taste of the Eye" intro idea (open-list) - don't change until he says.
- Trailer recorder: tools/game_reel.py -> any game with a director mode films itself (HEADED Chromium on the MSI GPU + ffmpeg).
  Refuses 2:40-7:30 AM (news GPU window) unless --force-time. Headless/canvas capture DON'T work (black/0 bytes) - don't retry those.
  No game audio captured (adds generated ambience). Output state/moments/media/.

## Posts (company @HeartbeatObserv)
- Rocket post on X (1:04 AM): guide, DIY, satellites/stations/Moon next, "Built by Claude Opus 5.5 (Anthropic)".
- Hedge reel (61 s) on X + TikTok (1:08 AM). YouTube POSTED 2:32 AM (was deferred by cap guard) -> done: youtube-only after
  2 AM CST (S.post('youtube', ...) - do NOT rerun x_moment_post, it would repost X). Specs: state/moments/*.json.
- Credit rule (Jaron): name the models (main builder + each AI's part); shows many AIs working together, not AI-as-sports-teams.

## The flow that worked (do it again)
1. Jaron's idea -> I write ONE rich brief -> an Opus subagent builds + tests at 375px in the built-in browser, commits, does NOT push.
2. I review (quick phone-size look), push, poll the live URL until it's up, buzz Jaron (tools/watch_reply.py).
3. Jaron plays on his real iPhone; his notes -> next brief within minutes. Build times: 20-35 min per agent.
4. Parallel agents only on different folders; push with `git fetch; git push` (no autostash rebase while another agent edits).
5. Ask other AIs for content as small JSON (CLIs: kimi, codex terra, agy for Gemini - agy needs "no tools" in the prompt;
   twins via mailbox at their 8/12/4/8 checks). Parse with the outermost-array scan.
- Cost: whole night of builds ~23% of the weekly Claude limit.
- Clocks fell back Nov 1 2 AM -> 1 AM CST (extra hour before the 2:45 GPU cutoff).

## Also today
- MSI crash 5:14 AM 10/31 (CLOCK_WATCHDOG_TIMEOUT during a slow all-core encode after the render). News recovered 9:09 AM;
  encode switched to -preset veryfast. Check vents for cat hair (Jaron's long-haired cat).
- Ashgrove Settings label: fixed + Darios PASS at true 375px (verify loop closed).
- Claude Duet: Jaron has it (2nd free limit reset in BILLS.md). It reads stale emails as open work - check live state first.
- Principles P-0118 (patience), P-0119 (perspectives = possibilities, not votes). Memories: auto-reload fine, doesn't buy for
  himself (suits later for meetings), many perspectives, post credits.
