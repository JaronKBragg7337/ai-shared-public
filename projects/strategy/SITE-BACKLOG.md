# SITE BACKLOG: every live page, its code, and the plans already logged for it

Written 2026-11-05 (cloud Fable 5.1, read-only sweep, Jaron's ask 11/4 11:15 PM). Companion: `state/backlog.json` (the same pieces as a flat list; a scheduler hands out S pieces one at a time).

**How to use this file**
- One section per area. Each page: what it is, status (live / half-built / paused), then **Planned next**: only pieces that were already logged somewhere, each with its source file and date. Nothing here is a new plan.
- Piece lines are machine-readable: `- [S] id | title | source: file (date) | fits: role | blocked_by: x`. S = one short job an AI can do in one sitting from that row plus the files it names. M = about half a day. L = multi-session build.
- "fits" uses the roles in `state/routing.json` + `state/models.md`: **looks/build** = Sonnet 5.5 / Sol 6.1 / Grok 4.7 / Opus (3D, visuals, big systems); **chore** = Luna 6 (small fixes, data, checks, docs); **episode** = Claude Sonnet/Fable write and build, Codex fact-checks, Grok watches video; **Opus only** = the rocket game (Jaron 10/31: Anthropic only); **Kimi only** = anything Sapling.
- Sources are files in ai-shared unless prefixed `site:` (heartbeat-observatory repo). Dates are the day the plan was logged, not today.
- Jaron's build order (projects/games/README.md "BUILD ORDER", 11/4 11:20 PM): 1 World 2 remake, 2 Ashgrove + the roofs, 3 The Cosmos. Those are L pieces for the main sessions; the sweeps hand out the S pieces around them.

## Paused on purpose, do not work on
- **Worlds Lab (/worlds-lab/): DROPPED from attention (Jaron 11/5 1:03 AM).** It was built opposite to what he asked; even mentioning it is noise for him. Do not work on it, do not hand out its pieces, do not bring it up in replies or reports for a long while. Not deleted.
Jaron's words (timeline 11/4 11:15 PM): PAM and the fruit fly brain pages stay paused; hidden pages are not the focus.
- **/pam/**: paused (Jaron 11/4). Also hidden from the home directory (`site:index.html` #hb-hidden-cards, 9/24).
- **Fruit fly brain**: /live-systems/flies/, /live-systems/flies/brain/, /live-systems/flies/school/ (+ /school/ rewrites), /lab/hidden/ fly test pages, projects/fly-brain. Paused since 9/21 (state/whats-next.md), Jaron 11/4.
- **Private creature logic**: projects/strategy/CREATURE-NEEDS.md, CREATURE-BRIEF.md, THE-FLASH files. Parked 10/28 4:40 PM, PRIVATE (timeline 10/28 4:30 PM "protect it"). Not the same thing as the public growing pet at /lab/pet/ (Jaron 11/3 11:30 PM correction).
- **BIG BUILD (hb-core) step 8**: paused by Jaron 10/28 4 PM until the creature needs analysis (state/open-list.md).
- **Polymarket / trading pages**: trading is down; /live-systems/trades redirects to /live-systems/crew/trades/; paper trading paused since Q-012 (9/11). /live-systems/paper, /live-systems/revenue, /live-systems/crypto, /live-systems/habitat: do not build on them.
- **Hidden from the public (describe, never promote)**: home directory hides Qwen (/qwen/), Revenue Desk, "The World" (/engine card), PAM (`site:index.html` #hb-hidden-cards). noindex pages: /lab/bakeoff/, the seven /lab/bedroom* copies, /lab/necklace/, /lab/studio-pro/, /preview/* (also robots.txt Disallow), /work/sample/*. Admin pages behind login: /admin/ (+control, keys, mailbox, remote, sapling, video-drop).
- **Sapling** (/admin/sapling/, the local model): Kimi only (Jaron 11/1). Not a sweep item for any other AI.
- **Holds Jaron set**: The Hedge Eye tuning (HOLD until he re-tests, open-list 11/1); voice-AI-team guide page unannounced (timeline 10/28 8:43 PM); First Light paid feeds NOT NOW (open-list 12); market analyst show comes only WITH long-term trading (CHANNEL-PLAN 10/20); drama show "not now" (CHANNEL-PLAN 10/20); AI reality TV waits on character pitches (10/30).
- **Not a build yet, wait for Jaron**: political status site beyond the current power map; usage-rescue help; air time capsule; Studio Lot + asset library; growing creature placement; "AI plays like a player" and the chat-app play study (open-list 10/31: "no build until he names it").

## Usage savings and organization (Jaron: the most useful things right now)
**Jaron 11/4 11:51 PM: timeline split (and other file moves for usage) NOT now; usage is plentiful. Raise again only if weekly usage runs tight.**
Measured 11/5 on the clones (numbers are approximate; 1 token per 4 bytes). LIST ONLY: nothing was moved or deleted. Every move below needs Jaron's yes; the dated-truth-line edits do not.

**Where the tokens go, every session**
| File | Lines | Size | ~Tokens | Who is told to read it |
|---|---|---|---|---|
| state/timeline.md | 1,519 | 418 KB | 104k | AGENTS.md "after a context compaction" (78 lines Sept, 1,085 Oct, 176 Nov) |
| INDEX.json | 823 | 91 KB | 23k | its own core_files list; ~40 of 50 keys are September narrative; has a BOM so json.load fails |
| decisions/OPEN-QUESTIONS.md | 539 | 48 KB | 12k | INDEX.json read_first |
| working-with-jaron.md | 509 | 44 KB | 11k | INDEX.json read_first |
| state/open-list.md | 99 | 26 KB | 6.5k | AGENTS.md; 20 of 99 lines are DONE or [x] (18 percent) |
| state/bot-chat.md | 970 | 209 KB | 52k | rule says last 30 lines; cat-by-habit risk |
| state/live-wire.md, desk-trade.md, executor.md, verifier.md | 2.7k to 92k | 0.5 to 8 MB | 120k to 4M each | nobody; one accidental cat ends a session |
Two read-first lists disagree: INDEX.json core_files (about 55k tokens) vs AGENTS.md + PROMPT-UNIFIED.md ("read AGENTS.md only", about 1.5k). An AI that trusts INDEX.json pays 20x more.

**Scratch committed to ai-shared**: state/ has 394 top-level entries, 140 of them .py; 219 tracked `state/_*` scratch files (92 `_satya_*`, 39 `_tmp_*`, 24 bridge-poly-*.b64/.ps1, 20 `_desk-*`, 10 `_espn*`, 9 `*.err`); `.gitignore` ignores `state/_tmp-*` (hyphen) while the files use `_tmp_` (underscore). Logs: executor.md 8.1 MB, verifier.md 6.5 MB, proposer.md 0.9 MB, live-wire.md 0.8 MB, state/fly-brain/log.2026-09-13-bloated.md 33 MB (escapes the ignore pattern). Together 49 MB = 78 percent of state/. Backups duplicating git: three state/*.rewritten-* (1 MB), cosmos-world-backup (285 KB), handoffs/INDEX-2026-09-28-before-check.json (85 KB), two JARONS-MAP-*-before.md, AGENTS-2026-09-26-before-slim.md, handoffs/pending-merge (resolved 9/10). Root clutter: tmp-jt-board.txt, tmp-jt-board-err.txt (0 B), INDEX.json.notes.md (0 B), terra-world-ui.patch, D/kimi.md, the "From Jaron" folder. On the MSI only (untracked): scratch/terra-mailbox-site and scratch/terra-mailbox-work are two full 2 GB copies of the site repo (4.1 GB total).

**Site repo weight**: 4.1 GB on disk (pack 1.94 GiB). tv/ 1.3 GB of mp4 with every episode committed twice (16x9 + -vertical, about 600 MB of twins). games/the-cosmos/docs/qa = 549 MB, 996 PNG screenshots referenced by nothing (largest single waste). lab/bedroom x7 = 35 MB; SYL x3 = 6 MB; render/assets 83 MB; three unreferenced og-*.jpg; bubble-legacy.js; mp-fix-report.md at root; sql/ (1 file) beside supabase/ (14, four named *-APPLY-ME.sql).

**Plans logged in two places that disagree** (fix with one dated line each):
1. TV live channels: CHANNEL-PLAN.md "Live" line says 1 to 8; state/open-list.md 13 says 7 to 22 by 10/21; tv/channels.json has 15. CHANNEL-PLAN episode lists for 9 and 10 stop at 10.3.
2. World 2: site TODO.md ("STATE June 11", "NOW: World 2 Phase 6b-6e") and WORLD2-PLAN.md ("source of truth") vs projects/games/README.md 10/18 remake plan + 11/4 BUILD ORDER. Nothing in the site repo points to ai-shared.
3. History numbering: 7.6/7.7 called "7.2/7.3" in CHANNEL-PLAN.md and two 10/25 handoff names.
4. Science 8.7: Kimi's 10/28 outline reserved it for the physics pour; it shipped as Antarctica.
5. Channel 15 Builders: cancelled 10/17 (LAUNCH-SLATE) and redefined 10/30 (CHANNEL-PLAN) with no un-cancel note.
6. projects/strategy/INDEX.md header says "Updated 2026-10-27" with entries through 11/4.
7. AGENTS.md "Current focus (10/17): games paused ~1 week" on the one page every AI reads, three weeks later.
8. state/whats-next.md declares itself past in its first line and still lists "MUST form the LLC" (done).
9. INDEX.json (10/21): lists logs/ and events/ (do not exist), inbox "Currently empty" (196 KB), 6 agents vs 11 agents/ folders (no Kimi, Sol, Fable, Sonnet, Luna, twins), 11 projects vs 54 folders, Qwen named 47 times though dropped 9/30, 8 of 21 open_blockers marked resolved inside their own text.
10. handoffs/pending-merge/README.md says 959f289 "only needs pushing"; INDEX.json says Codex pushed it (9/10).
11. PROMPT-UNIFIED.md still lists /qwen/ as a page to check and carries the September trading rule plus its retraction; OPERATING-MAP, working-with-jaron and INDEX.json do the same (old rule + retraction + new rule, three reads for one fact).
12. Stale sweep: tools/stale_sweep.py runs weekly and wrote state/STALE-CANDIDATES.md (43 candidates, 11/1) but no STALE-SWEEP file exists after 10/21; two candidate lists expired unread.
13. projects/tesseract/ is empty while strategy INDEX names projects/tesseract/README.md as the home. projects/fw-sites/round2-previews.md says the previews are "NOT committed" (they are).
14. 16 of 54 projects/ folders hold one file or none (14 single IDEA/PLAN files, revenue-desk and tesseract empty).

**Old worktrees in C:\Users\lilli\Projects that look finished** (list only, never delete; check `git status --porcelain` and `git log origin/main..HEAD` in each first):
- 48 ho-* folders (9/28 to 10/4) = the 10/3 Cosmos /goal batch; timeline records F1 a02892f, F2 a578f0b, F0+F3 25b3443, F4+F5 5131c8f, cargo f90f98b, SH14/15 15b0f5e, Ceres 63f8b0e, Moon c3a20b83, identity fc9a6ca all LIVE. Three had uncommitted work when stopped: ho-dig (commit 7853540 not pushed), ho-sol (saved uncommitted at the Codex limit), ho-fix1 (56 files uncommitted): bundle those before any removal.
- ho-studio-codex / -fable / -kimi / -merge / -mybeats / -save (10/24 to 10/26): Studio round 1, merged via ho-studio-merge; /studio/ is live.
- the-necklace-show, necklace-voices, necklace-unreal (9/26 to 9/28): Necklace ep 1 done. trailer (10/2): Cosmos trailer delivered. padcheck, perf, syl-survey (9/30 to 10/3): research, done. fly-school (9/17): paused. agent-workbench (6/21): pre-dates ai-shared. heartbeat-observatory-kimi (10/9): Kimi's clone. key-drop (10/20): shipped.
- About 200 loose files in Projects\ (cargo-*.log, grok-*.log, GROK-BRIEF-*.md, LUNA-BRIEF-*.md, luna-*.log/.md/.done, SOL-BRIEF-*.md, ho-sol-run*.log, ho-f2-*.txt, phone-check*.log, shoot*.log, validate-final*.log, run-*.sh), all 9/30 to 10/7: briefs and logs for that batch.
- Unknown (no timeline hits): control-demo-worktree, heartbeat-social-fix (10/28), livi-organism (10/8). Likely finished but recent: hb-admin-phone-fix, hb-signup-fix, heartbeat-terra-release, heartbeat-world-ui (10/30). Active, do not touch: sapling, watch, hb-core, hb-vision, hb-render, hb-render-research, heartbeat-observatory, ai-shared-public, heartbeat-build-recaps.
- Verdict: about 56 of 74 folders plus the loose files look finished.

**Organization pieces** (ranked by saving; moves wait for Jaron's yes):
  - [S] U-01 | Split state/timeline.md by month (timeline-2026-09.md, -10.md), keep timeline.md = November + a 10-line "where the rest is". Saves ~90k tokens per post-compaction read | source: usage audit (11/5), AGENTS.md read rule | fits: chore: Luna 6 | blocked_by: Jaron OK (moves text)
  - [S] U-02 | One read-first list: INDEX.json read_first and core_files point at AGENTS.md only (as PROMPT-UNIFIED already does); working-with-jaron and OPEN-QUESTIONS stay in the "read ONLY when" table. Saves ~25k tokens per session for INDEX followers | source: INDEX.json, AGENTS.md, PROMPT-UNIFIED.md (11/5 audit) | fits: chore: Luna 6 | blocked_by: -
  - [M] U-03 | Rewrite INDEX.json as a ~60-line index (purpose, folders that exist, agents that exist, read_first = AGENTS.md), move the ~40 September narrative keys to handoffs/INDEX-history-2026-09.json, drop the BOM. Saves ~20k tokens per read | source: INDEX.json (updated 10/21), state/STALE-CANDIDATES.md (11/1: 12 open candidates in INDEX.json) | fits: chore: Luna 6 | blocked_by: Jaron OK
  - [S] U-04 | Move the 20 DONE / [x] lines out of state/open-list.md into state/open-list-done-2026.md and reflow lines under 120 chars. Saves ~1.2k tokens per read, makes "the top one" findable | source: state/open-list.md (11/5 count) | fits: chore: Luna 6 | blocked_by: Jaron OK
  - [S] U-05 | Stop tracking the six logs (executor.md, verifier.md, proposer.md, desk-trade.md, live-wire.md, state/fly-brain/log.2026-09-13-bloated.md, 49 MB): move to a logs-archive outside the clone or a release asset, keep a 200-line tail + one-line pointer, add names to .gitignore. Removes the multi-million-token accidental cat | source: usage audit (11/5) | fits: chore: Luna 6 | blocked_by: Jaron OK (moves files)
  - [S] U-06 | Archive the 219 `state/_*` scratch files, bridge-poly-*, test-fly-*, *.err, *.rewritten-*, _tmp_lw/, saved html to state/_archive-2026-11/ and fix .gitignore (`state/_*`, `*.b64`, `*.err`, `*.rewritten-*`). Saves ~5 MB per clone and ~2k tokens on every `ls state` | source: usage audit (11/5), .gitignore `state/_tmp-*` typo | fits: chore: Luna 6 | blocked_by: Jaron OK (moves files)
  - [S] U-07 | Archive state/whats-next.md, handoffs/pending-merge/, the four *-before* backups and INDEX-2026-09-28-before-check.json into handoffs/_archive/ (all in git already); keeps the "newest handoff" listing clean | source: usage audit (11/5) | fits: chore: Luna 6 | blocked_by: Jaron OK (moves files)
  - [S] U-08 | Dated truth lines: CHANNEL-PLAN "Live" line = channels.json; strategy INDEX "Updated" date; AGENTS.md focus block; site TODO.md / WORLD2-PLAN.md / HANDOFF.md top note pointing to ai-shared projects/games/README.md; Channel 15 un-cancel note; History 7.6/7.7 labels | source: disagreements 1 to 7 above | fits: chore: Luna 6 | blocked_by: -
  - [S] U-09 | Replace layered corrections with the current rule in PROMPT-UNIFIED.md, OPERATING-MAP.md, working-with-jaron.md, INDEX.json hard_rules (old rule + "superseded" + new rule = three reads); drop /qwen/ from PROMPT-UNIFIED's page checks | source: disagreement 11 above | fits: chore: Luna 6 | blocked_by: Jaron OK (edits his rule files)
  - [S] U-10 | Make the weekly stale_sweep land somewhere a bot reads (newest handoff or open-list #0) and work the 43 candidates from 11/1 (12 in INDEX.json, 8 in OPEN-QUESTIONS, 5 dead paths) | source: state/STALE-CANDIDATES.md (11/1), state/STALE-SWEEP-2026-10-21.md | fits: chore: Luna 6 | blocked_by: -
  - [S] U-11 | Root clutter: tmp-jt-board*.txt, INDEX.json.notes.md (0 B), terra-world-ui.patch, D/kimi.md (belongs in research/world-2030-2033/), the "From Jaron" folder: move to scratch or history | source: usage audit (11/5) | fits: chore: Luna 6 | blocked_by: Jaron OK (moves files)
  - [S] U-12 | Fold the 14 single-file projects/ folders into one projects/IDEAS/ folder (or IDEAS.md) and remove the two empty ones; halves the project listing | source: usage audit (11/5) | fits: chore: Luna 6 | blocked_by: Jaron OK (moves files)
  - [M] U-13 | Site repo: move games/the-cosmos/docs/qa (549 MB, unreferenced) out of git and stop committing -vertical.mp4 twins (~600 MB; host in Supabase storage or a release). Saves ~1.1 GB per fresh clone and stops the pack growing per episode | source: usage audit (11/5) | fits: chore: Luna 6 (plan), Jaron approves | blocked_by: Jaron OK (moves files)
  - [S] U-14 | Site repo tidy: archive four of the seven lab/bedroom* copies (L-23), two of three SYL copies (G-26, G-33), three unreferenced og-*.jpg, bubble-legacy.js, hb-editor-source.js, mp-fix-report.md; merge sql/ into supabase/ (~40 MB) | source: usage audit (11/5) | fits: chore: Luna 6 | blocked_by: Jaron OK (moves files)
  - [S] U-15 | MSI: delete nothing, but list the 4.1 GB of scratch/terra-mailbox-site + terra-mailbox-work (two full site clones, untracked) and the 56 finished worktrees for Jaron's one yes; bundle ho-dig, ho-sol, ho-fix1 first | source: MSI listing (11/5), state/timeline.md 10/3 ship lines | fits: chore: Luna 6 | blocked_by: Jaron OK
  - [S][DONE 11/5] U-16 | Add state/cosmos-watchdog.lock-style ignores for every machine-written file that keeps showing in git status (state/.crypto-wake-last, connector-hits.json, msi-health-*.json, usage-live.json, live-board.*) or commit them from one nightly job only | source: MSI git status (11/5: 12 modified state files between nightly saves) | fits: chore: Luna 6 | blocked_by: -
Rough total if all done: ~55 MB per ai-shared clone, ~1.1 GB per site clone, ~140k fewer tokens per session for an AI that obeys the current read lists.

## Looks broken or wrong (seen in passing, outside the job)
- /tv/science/ and every /tv/<channel>/ URL 404 live (no index.html in the channel folders); only /tv/?ch= works. Harmless unless shared as a link.
- No sitemap.xml (404). robots.txt only disallows /preview/.
- The MSI site checkout has uncommitted changes to games/the-cosmos/build.json, index.html and src/core/buildVersion.js plus three untracked keepers-light social verticals and two untracked cosmos QA folders (git status 11/4). A `git reset --hard` already wiped Cosmos edits once (timeline 11/1 12:18 PM); commit or stash them.
- /live/ shows one finished event (MMX 10/19) while a news commercial still advertises the page.
- The Cosmos MSI authority-server watchdog died unnoticed twice (10/11 to 10/26, 10/31 to 11/4).
- The daily 3:45 AM cloud news writer ran on the cloud credit that expired 11/5 2:59 AM; the local 4:20 AM backup writer should cover it (confirm today).
- ep7 Antarctica Part 1 is live with six known visual mismatches and is not in the posting queue; 7.6, 7.7, 8.5, 8.7, 9.2 to 9.4, 10.4, 10.5, 19.1 are unposted on some or all platforms.
- Keeper's Light social verticals are queued and partly posted but the files are not in the site repo.
- artifacts.json has no entries for the Seam Room, Arena, Pet, Tesseract, Power Map, Necklace view.
- /render/ public title is "hb-render phone test"; /api/render-anything answers 503 until a key is set.
- api/enrich-world-spaces is scheduled twice (GitHub Action hourly + Vercel cron daily) and the live URL answers 401 without the bearer (expected).
- projects/tesseract/ is empty while the strategy INDEX points at projects/tesseract/README.md.
- Open-list items already done but unchecked: Hedge title card (11/1), rocket satellites + stations (v3, 11/1).
- The `.gitignore` entry `state/_tmp-*` never matches the `_tmp_` files it was meant for.
- INDEX.json has a UTF-8 BOM; `json.load` fails without utf-8-sig (any tool reading it the plain way breaks).

## Games
Index: /games/ (17 tiles) + /PCGames/. Rule (projects/games/README.md 9/22): a game is not published until it has games/<slug>/index.html + a tile, checked at phone width with no login. Games were formally PAUSED 10/17 (timeline 10/17 20:55); the Oct 31 to Nov 1 Rocket + Hedge night was a new-games sprint. Big build order (11/4): World 2, Ashgrove, The Cosmos.

### The Hedge (/games/hedge-maze/)
- What: Halloween 3D hedge maze with a searchlight Eye in the sky, two shadow creatures, lantern checkpoints and 30 traps loaded from traps.json (any AI can add one). Built by Opus subagents 10/31 to 11/1.
- Status: live
- Planned next:
  - [S] G-01 | Confirm the title-card flight is live on a phone and tick the open-list box (timeline says shipped 6d80df9, open-list still unchecked) | source: state/open-list.md (11/1), state/timeline.md (2026-11-01 1:32 AM) | fits: chore: Luna 6 | blocked_by: -
  - [S] G-02 | Retire the "Halloween, new" / "New tonight (working title)" tile wording; ask Jaron for the permanent name | source: site:games/index.html (2026-11-01) | fits: chore: Luna 6 | blocked_by: Jaron picks the name
  - [S] G-03 | Add a trap: one JSON entry per TRAPS.md, merged with projects/games/hedge-maze/merge_traps.py (only Jaron's loop runs; other loops become signs) | source: site:games/hedge-maze/TRAPS.md, handoffs/2026-11-01-games-night.md (11/1) | fits: chore: Luna 6 or any AI | blocked_by: -
  - [S] G-04 | "Taste of the Eye" intro tuning (Eye finds you early, backs off ~20 s). HOLD until Jaron re-tests | source: state/open-list.md (11/1 12:53 AM) | fits: Opus | blocked_by: HOLD, Jaron re-test
  - [M] G-05 | Re-cut a director-mode reel when a new post is wanted: python tools/game_reel.py on the MSI GPU, never 2:40 to 7:30 AM | source: handoffs/2026-11-01-games-night.md (11/1) | fits: chore: Luna 6 (MSI) | blocked_by: -
- Notes: game audio is not captured in reels (ambience bed is generated).

### Rocket (/games/rocket/)   RULE: Anthropic models only, Opus-led (Jaron 10/31 10:40 AM)
- What: kid-friendly phone-first Kerbal-style rocket game: hangar, one lean slider, real physics, goal ladder clouds to space to orbit to Moon to satellites to a station; flight guide and Do-it-yourself mode; saves on device. v3 live 11/1 (cloud PR #28), goal fix confirmed on Jaron's iPhone 11/1 9 PM.
- Status: live
- Planned next:
  - [S][DONE 11/5] G-06 | Tick the open-list "ROCKET later: satellites + space stations" item (done in v3) | source: state/open-list.md (11/1 1:18 AM), handoffs/2026-11-01-cloud-rocket-v3.md | fits: chore: Luna 6 | blocked_by: -
  - [S] G-07 | Two calls for Jaron: a pilot in the capsule (little astronaut) and the game's real name (page title "Heartbeat Rocket", tile says working title) | source: projects/games/rocket-game/PLAN.html (10/31), state/open-list.md (10/31) | fits: Opus only | blocked_by: Jaron decision
  - [S] G-08 | Real-iPhone checks the cloud could not do: touch + fps on the Moon trip, hangar 7 parts at 375 px, label readability, sound | source: handoffs/2026-11-01-cloud-rocket-v3.md "Not verified" (11/1) | fits: Opus only | blocked_by: Jaron plays
  - [S] G-09 | Tilt-the-phone as an optional lean control (plan: slider first, tilt as option) | source: projects/games/rocket-game/PLAN.html (10/31) | fits: Opus only | blocked_by: -
  - [M] G-10 | Looks pass on v3: Moon ground (craters, planet-shine), station shapes, flag size | source: handoffs/2026-11-01-cloud-rocket-v3.md (11/1) | fits: Opus only | blocked_by: -
  - [M] G-11 | DIY landing hints: real-kid try of burn/stop timing, tune if not followable | source: handoffs/2026-11-01-cloud-rocket-v3.md (11/1) | fits: Opus only | blocked_by: -
  - [M] G-12 | Rocket director-mode trailer (?director=1 + tools/game_reel.py); video beat still image on X (164 vs 56 views) | source: state/open-list.md GAME TRAILER MODE (11/1 1:40 AM), state/timeline.md (2026-11-01 9:00 AM) | fits: Opus only (game), Luna 6 (recording on MSI) | blocked_by: -
  - [L] G-13 | Advanced mode (more parts, real gauges, plan your own turn and staging), then Hard mode (near-Kerbal: full parts, 3D steering, maneuver planning) | source: projects/games/rocket-game/PLAN.html "Three ways to play" (10/31), state/timeline.md (2026-10-31 3:23 PM) | fits: Opus only | blocked_by: -

### The Cosmos (/games/the-cosmos/)
- What: the real space game (SYL became this; one game = The Cosmos, DECISIONS 9/30). Three.js, server-authoritative multiplayer (MSI authority server), Mars Marineris Port, Phobos/Deimos, Ceres, the Moon, Earth, Callisto, 18 story jobs, real-scale Solar System. 2482 files.
- Status: paused (live, playable; no build since Callisto 10/10; Jaron 10/17: games paused; 11/4 build order puts it third)
- Planned next:
  - [S][DONE 11/5] G-14 | Keep the MSI authority server alive: the watchdog died unnoticed twice (10/11 to 10/26, 10/31 to 11/4); add it to the MSI health buzz | source: state/timeline.md (2026-10-26 4:31 PM, 2026-11-04 7:22 AM) | fits: chore: Luna 6 | blocked_by: -
  - [S][DONE 11/5] G-15 | Chase the 404 for homes/people/undefined.jpg when talking to a person with no portrait id | source: handoffs/2026-10-10-callisto-ship.md (10/10) | fits: chore: Luna 6 | blocked_by: -
  - [S] G-16 | Small UI debts from the QA pass: pinch-zoom locked, one unlabeled input, touch keys overlapping World/crew on desktop, "fetch failed" in the opening dig, no notice when the connection drops | source: handoffs/2026-10-08-playtester-qa-upgrade.md (10/8) | fits: chore: Luna 6 | blocked_by: -
  - [S][DONE 11/5] G-17 | Fix the stale README intro "This worktree is awaiting publication" and audit projects/syl/STALE-AUDIT-2026-10-04.md items | source: site:games/the-cosmos/README.md, projects/syl/STALE-AUDIT-2026-10-04.md (10/4) | fits: chore: Luna 6 | blocked_by: -
  - [S] G-18 | Two numbers only Jaron can give: how a damaged ship leaves Earth (Skyward assist / repair / earn it / stays stuck) and fuel + repair prices; then wire them | source: state/open-list.md items 5 and 11, handoffs/2026-10-08-cosmos-missions-r1.md (10/9) | fits: Jaron, then chore: Luna 6 | blocked_by: Jaron decision
  - [S] G-19 | Jaron decision: lost-WebGL-context restart policy on iPhone when backgrounded (now waits 12 s / 25 s) | source: handoffs/2026-10-08-playtester-qa-upgrade.md finding 1 (10/8) | fits: Jaron | blocked_by: Jaron decision
  - [M] G-20 | Phobos walking clip: fix walking and ground look on Phobos, record a short walk, post on any MMX story; Codex brief ready in projects/cosmos-phobos-2026-10-18/PROMPT.txt | source: projects/games/README.md "When games resume" (10/21), state/timeline.md (2026-10-21 6:12 PM) | fits: looks: Sol 6.1 or Sonnet 5.5 | blocked_by: games resume (build order 3)
  - [M] G-21 | Callisto follow-ups: Archive/Array building detail (flat violet boxes), Valhalla rings, orbit phase from Horizons, phone-check for Callisto's opening, playtester walk budget | source: handoffs/2026-10-10-callisto-ship.md "Still open" (10/10) | fits: looks: Sonnet 5.5 | blocked_by: games resume
  - [M] G-22 | Playtester learns to take a job; repeating jobs per desk; Earth dealer/shop; Ceres voices; second Homeguard building | source: handoffs/2026-10-08-cosmos-missions-r1.md "What's next" (10/9), site:games/the-cosmos/docs/MISSIONS.md | fits: looks: Sonnet 5.5 | blocked_by: games resume
  - [L] G-23 | Remaining bible build order: Moon start in the opening, Greenhaven on Ceres, stations, F6 seasons, F7 licenses/factions/PvP, shipyard shop with thumbnails, free flight system-wide, heavy drive, Sun scaling; main arc (first crossing, first contact, Europa) | source: handoffs/2026-10-03-cosmos-build-ready.md (10/4), handoffs/2026-10-08-cosmos-missions-r1.md | fits: looks/build: Sonnet 5.5 / Sol 6.1, Fable art direction | blocked_by: build order 3
  - [L] G-24 | New trailer: the opening changed 10/3 and the 10/1 "trailer within the month" never happened; docs/trailer/capture.mjs + shots.json exist | source: handoffs/2026-10-01-evening-cosmos-and-router.md, projects/syl/DECISIONS.md (10/3) | fits: looks: Fable + Sonnet 5.5 | blocked_by: build order 3
- Notes: idea NOT approved, do not build: API AIs as faction leaders (projects/syl/DECISIONS.md 10/3 11:42 PM). Uncommitted edits to games/the-cosmos/build.json, index.html and buildVersion.js sit in the MSI checkout (git status 11/4); check before any Cosmos push.

### SYL, Space You Land (/games/syl/)
- What: the older Three.js SYL V1, mirrored from the SYL-Full-Game repo (last mirror 8/15). Superseded by The Cosmos (DECISIONS 9/30).
- Status: live (dormant)
- Planned next:
  - [S][DONE 11/5] G-25 | Reword the tile and page copy: it still says "the authority-first rebuild proceeds in the open"; say SYL's story lives on in The Cosmos and this is the earlier V1 kept playable | source: site:games/index.html, projects/syl/DECISIONS.md (9/30) | fits: chore: Luna 6 | blocked_by: -
  - [S] G-26 | Decide: keep as a playable museum piece, or move to PC Games legacy; three SYL routes exist (/games/syl/, /games/syl-test/, /PCGames/syl/) | source: site:HANDOFF.md (2026-08-15), projects/games/INVENTORY-2026-09-22.md | fits: Jaron | blocked_by: Jaron decision

### Fable Survival (/games/fable-survival/)
- What: mobile survival prototype (scavenge, build, fight infected) with Heartbeat realtime presence; compiled Vite build vendored, source in its own repo.
- Status: live (dormant since 8/15)
- Planned next:
  - [S] G-27 | Phone-width smoke check; confirm the in-game feedback panel still posts and presence still connects after the Supabase table moves | source: site:games/fable-survival/index.html, projects/games/INVENTORY-2026-09-22.md (9/22) | fits: chore: Luna 6 | blocked_by: -

### Parkworks Tycoon (/games/parkworks/)
- What: mobile park management game; cloud saves via hb-save-backend.js; vendored build from parkworks-tycoon (tools/vendor-to-heartbeat.mjs).
- Status: live (dormant)
- Planned next:
  - [S] G-28 | If ever refreshed: use the vendor script only; a hand copy drops hb-save-backend.js and cloud saves stop silently | source: site:games/parkworks/README.md | fits: chore: Luna 6 | blocked_by: -

### Rustfall (/games/rustfall/)
- What: post-apocalyptic wasteland with robots, vehicles, a rebuildable mech, snap-together base; press L for the inspection layer. Runs on Heartbeat's Supabase.
- Status: live (dormant)
- Planned next: nothing logged. 3D-STANDARDS (9/12) names its debug layer as the model the space game should grow.
- Notes: same lineage as Wasteland Commons; two tiles.

### President Sim (/games/president-sim/, classic at classic.html)
- What: 3D executive office, Episode 01 with four hearings, narration, Cinema view; built by Jaron. Classic edition kept.
- Status: live (dormant)
- Planned next: nothing logged (no Episode 02 plan anywhere).

### Wrapper games (one iframe page each, added 9/23): MindGames, Robot Evolution Lab, Signal Drift, Northstar Addressable World, The Defender 3D, Cyber-Trench Overdrive, Rift Clash, Wasteland Commons, Orbit Salvage (/games/<slug>/)
- What: wrappers around GitHub Pages or Vercel hosts. Orbit Salvage: Luna's 9/21 tether puzzle, "kept, not promoted" (Jaron).
- Status: live (dormant)
- Planned next:
  - [S][DONE 11/5] G-29 | One pass: each iframe loads at 375 px with no login and the external host is still up; add the missing meta descriptions | source: projects/games/INVENTORY-2026-09-22.md "Caveat Codex named" (9/22) | fits: chore: Luna 6 | blocked_by: -
  - [S][DONE 11/5] G-30 | Rift Clash and Wasteland Commons tiles promise multiplayer with no server running; add an honest "solo vs bots / multiplayer unproven" line | source: projects/games/INVENTORY-2026-09-22.md UPDATE (9/22) | fits: chore: Luna 6 | blocked_by: -
  - [M] G-31 | Still unlisted from the inventory: Frontier Empires and Air Vehicles (need npm run build + relative Vite base), Pirate World (its Supabase project is paused), New Age of War (Unreal, info page), 8 Free Game Hub minigames | source: projects/games/INVENTORY-2026-09-22.md "Still open" (9/23) | fits: chore: Luna 6 | blocked_by: Jaron says which to surface

### The Necklace Show (/games/the-necklace-show/)   unlinked
- What: wrapper to the old Three.js Necklace Show on GitHub Pages; TV took the show off 9/30; the current Necklace View is /lab/necklace/.
- Status: live (dormant, no tile)
- Planned next:
  - [S] G-32 | Decide: tile, redirect to /lab/necklace/, or leave hidden | source: site:games/index.html (no tile), state/timeline.md (2026-10-25 5:58 PM) | fits: Jaron, then chore: Luna 6 | blocked_by: Jaron decision

### SYL test (/games/syl-test/)   unlinked
- What: "Unsafe Legacy Preview (Not Staging)"; shares the production origin and the legacy save key.
- Status: live (frozen)
- Planned next:
  - [S] G-33 | Remove or noindex: HANDOFF 8/15 says never promote it as staging; a public route sharing the live save key is a footgun | source: site:HANDOFF.md (2026-08-15), projects/games/INVENTORY-2026-09-22.md (9/23) | fits: Jaron, then chore: Luna 6 | blocked_by: Jaron decision

### PC Games (/PCGames/, /PCGames/peakaboom/, /PCGames/syl/)
- What: desktop builds page. Peakaboom is a guest game by an X creator (hosting stays free, Jaron 9/24); SYL legacy desktop experiment "On Hold".
- Status: live (dormant)
- Planned next:
  - [S] G-34 | Check the spawn.co Peakaboom embed and fallback link still load | source: site:PCGames/peakaboom/index.html | fits: chore: Luna 6 | blocked_by: -
  - [S] G-35 | Soften the intro ("the high-fidelity versions") or add the UE 5.9 web-export result when it exists | source: site:PCGames/index.html, state/open-list.md UE 5.9 (11/3) | fits: chore: Luna 6 | blocked_by: -

### Games index (/games/)
- Status: live
- Planned next:
  - [S] G-36 | Freshness pass: nothing marks The Cosmos as paused; top tiles still say "new" from 10/31; SYL blurb stale (see G-25) | source: site:games/index.html (2026-11-01) | fits: chore: Luna 6 | blocked_by: -
  - [M] G-37 | Game trailer mode for every game (?director=1 with captions naming which AI made what, recorded on the MSI GPU); Hedge done, rocket next, then others | source: state/open-list.md (11/1 1:40 AM), projects/games/README.md "Trailers" | fits: looks per game, Luna 6 records | blocked_by: -
  - [L] G-38 | Whole-website trailer (phone, theater, games, crew, news, Cosmos): Fable directs, Grok watches the cut, Sonnet builds; idea 10/4, not started | source: state/timeline.md (2026-10-04 18:19) | fits: looks: Fable + Sonnet 5.5 | blocked_by: Jaron go
- Notes: "AI plays like a player" and the chat-app play-length study are brainstorm only, no build until Jaron names the missing piece (state/open-list.md 10/31 10:26 AM).

## Worlds / 3D
Standing brief for anything that renders: decisions/3D-STANDARDS.md (9/12). Phone budget from WORLD2-PLAN.md applies everywhere (300 draw calls, 40 MB textures, instancing, real-phone test).

### World 2, the city (/world2/, gate /world2/gate/)   BUILD ORDER 1 (Jaron 11/4 11:20 PM)
- What: the second walkable world, "a city of lit towers": own code (world2/main.js), own realtime channel, same accounts/claims/doors, eight plots, day/night with emissive windows, lamps and fireflies. Gate page with a live orbiting peek. One of three planets in the home-page loop (10/17). Still called "the city" provisionally; no real name.
- Status: half-built (Jaron 10/18: "too fake looking", remake approved 10/18 7:40 PM; 10/28 tester confirms; last touch Terra 10/28 loading screen)
- Do not confuse with Cosmos "world2" = Ceres (games/the-cosmos, 10/3).
- Full planned scope, grouped by source:
  - A. WORLD2-PLAN.md phases (site, June 10): 1 skeleton DONE; 2 terrain partly; 3 city partly (identical boxy towers, no streets); 4 multiplayer DONE; 5 doors + plots partly (Theater/Arcade/Library doors never found by the tester); 6 gateway DONE; 6a gate page DONE.
  - [L] W-01 | THE REAL CITY remake (the approved plan): real buildings with ledges, roofs, entrances, signs, depth; street life (sidewalks, curbs, lamps, cars, benches, storefronts); downtown blocks + riverfront/subway; possibly Fort Wayne-style with real street names and landmarks; things to DO (jobs, shops, the theater, the news studio with Vex + Joe). KEEP sky/day-night, MetaHuman people, multiplayer, doors to site pages, plots. Phone budget applies | source: projects/games/README.md "World 2 remake plan" (10/18), "BUILD ORDER" (11/4), research/site-tester/2026-10-28-jarons-twin.md | fits: build: Opus / Sonnet 5.5 (multi-session), Fable looks review | blocked_by: -
  - [M] W-02 | Phase 6b avatar look parity: use the saved world_characters look (World 1 buildAvatarBody rules), not a hash colour | source: site:WORLD2-PLAN.md 6b (June 10), site:TODO.md NOW 2 | fits: looks: Sonnet 5.5 | blocked_by: fold into W-01
  - [M] W-03 | Phase 6c items + Throw: port World 1's held items and Throw (something city-appropriate), Throw button on the phone pad | source: site:WORLD2-PLAN.md 6c (June 10) | fits: looks: Sonnet 5.5 | blocked_by: fold into W-01
  - [L] W-04 | Phase 6d apartments + World 2 home styles at city scale, including Jaron's three-floor SUITE house; claimable via claim_home p_world='world2' (migration world2_plots) | source: site:WORLD2-PLAN.md 6d (June 10) | fits: build: Opus / Sonnet 5.5 | blocked_by: fold into W-01
  - [S] W-05 | Phase 6e UI parity: status chips row, fullscreen + menu buttons, Ask Claude when a mind roams W2 | source: site:WORLD2-PLAN.md 6e, site:docs/SHELL.md | fits: chore: Luna 6 | blocked_by: -
  - [S] W-06 | World 2's real name: landing and gate say "the city"; one-word edit when Jaron chooses | source: site:TODO.md NOW 4 (June 11) | fits: Jaron, then Luna 6 | blocked_by: Jaron decision
  - [M] W-07 | Shared spawn plaza + pointer toward other players (Jaron and his partner never found each other) | source: site:TODO.md NOW 3 (June 11) | fits: looks: Sonnet 5.5 | blocked_by: fold into W-01
  - [M] W-08 | Theater interior: per-visitor playback to synced reels over the world2 state channel | source: site:TODO.md SOON (July 4) | fits: looks: Sonnet 5.5 | blocked_by: fold into W-01
  - [M] W-09 | Media surfaces: one shared video texture across billboards/jumbotrons/tickers, cheap CanvasTexture tickers, the site's own live data (news as a tower ticker, social feed on a jumbotron) | source: site:TODO.md SOON "MEDIA SURFACES" (July 4) | fits: looks: Sonnet 5.5 | blocked_by: fold into W-01
  - [L] W-10 | Phase 7 BUILD MODE: 7a world_props table + loader (start in a lab world); 7b admin Build Mode v1 (third person, palette, ghost, snap, place/rotate/delete/save, phone + keyboard); 7c snap sockets for track/rail/road/fence; 7d publish + world version; 7e Claude in-world for admins writing world_props. 3DPrinterAsset is the closest living prototype | source: site:WORLD2-PLAN.md Phase 7 (June 11), site:docs/EDITOR.md | fits: build: Opus / Sonnet 5.5 | blocked_by: after W-01
  - [L] W-11 | Fort Wayne P2 explorable districts + container buildings; P3 promotion (shell, gate, multiplayer, touch_world); P4 living layer (Embassy events, riverfront walks). P1 recognition lab done 6/12 at /worlds-lab/worlds/fort-wayne/. Ten hand-built hero landmarks carry recognition | source: site:WORLD2-PLAN.md "FUTURE WORLD: FORT WAYNE" (June 11), site:TODO.md NOW 1 | fits: build: Sonnet 5.5 / Opus | blocked_by: Jaron: is Fort Wayne the model for W-01?
  - [L] W-12 | Phase 8: minds roaming World 2, world-to-world travel door inside each world, sound layers | source: site:WORLD2-PLAN.md Phase 8 | fits: build | blocked_by: after W-01
  - [S] W-13 | Verify Terra's 10/28 fixes on a real phone: loading screen (first load was blank 40 s+), bigger plot sign; measure the real load time | source: research/site-tester/2026-10-28-jarons-twin.md, state/timeline.md (2026-10-28 8:13 PM) | fits: chore: Luna 6 | blocked_by: -
  - [S] W-14 | Tester asks that survive the remake: no double-click to walk, signposts or minimap, a night floor (too dark), the promised halls reachable | source: research/site-tester/2026-10-28-jarons-twin.md (10/28) | fits: chore: Luna 6 (signs, night floor) | blocked_by: -
  - [S] W-15 | Point tools/playtester at World 2 (it has only ever covered The Cosmos) | source: projects/games/README.md (10/18) | fits: chore: Luna 6 | blocked_by: -
  - [S] W-16 | Restore a World 2 spot in the news commercial loop once remade (the 10/19 loop swapped it for the Live page) | source: state/timeline.md (2026-10-19 09:25) | fits: chore: Luna 6 | blocked_by: after W-01
- Notes: gate copy still promises Theater, Arcade and Library halls the tester could not find. If Jaron ever picks "remove", the home planet loop and the /engine world list need editing too.

### Ashgrove, World 3 (/world3/, gate /world3/gate/, /world3/town/)   BUILD ORDER 2
- What: a town that runs whether or not you watch: 49 founding buildings, walkable interiors, residents with routines on a 24-minute day, jobs/seats, food/water/energy, self-growth, stable asset ids. Later growth is saved per browser, not yet one shared town.
- Status: live (maintenance; Oct 28 to 31 visitor fixes; Jaron 10/18: "missing the most")
- Planned next:
  - [L] W-17 | Automatic BUILDING INSPECTOR: measure the 3D geometry, not just walking: roof closure (gaps/holes), doorway/room clearance (blocked rooms), stair run + landing + headroom, walk-into-every-room, floating/clipping; plus an inventory of built vs planned vs in files but never shown | source: projects/games/README.md "Queued for when games come back" (10/18), "BUILD ORDER" (11/4) | fits: build: Sonnet 5.5 / Opus | blocked_by: -
  - [S] W-18 | Point tools/playtester at Ashgrove | source: projects/games/README.md (10/18) | fits: chore: Luna 6 | blocked_by: -
  - [S] W-19 | Fix world3/town/README.md "Walk the town" link (still the old GitHub Pages copy) and the guest-name mixup seen on the tester box | source: site:world3/town/README.md, research/site-tester/2026-10-30-darios-retest.md | fits: chore: Luna 6 | blocked_by: -
  - [S] W-20 | Darios 10/28 leftovers: scribble marks on the road texture, F flythrough washed out and ending on a frozen frame | source: research/site-tester/2026-10-28-darios-twin.md item 10 | fits: looks: Sonnet 5.5 | blocked_by: -
  - [S] W-21 | Phone check: watching a building rise on a real device, z-fighting | source: site:world3/town/docs/STATUS.md | fits: chore: Luna 6 | blocked_by: -
  - [M] W-22 | Page weight: UI takes 3 to 8 s to render after load ("later pass") | source: state/timeline.md (2026-10-31 12:20 PM) | fits: looks: Sonnet 5.5 | blocked_by: -
  - [L] W-23 | Multiplayer and one shared saved town (player is still a module-level singleton) | source: site:world3/town/docs/STATUS.md, site:world3/gate/index.html | fits: build: Opus / Sonnet 5.5 | blocked_by: after W-17
- Notes: Jaron's 11/1 Seam Room test idea ("garage door opens onto a town/Ashgrove with a spot for my home") is a test, not a build order (timeline 11/1 3:30 PM).

### Town Square, World 1 (/engine/, world at /engine/hub/)
- What: the first walkable world (June 10): residents, minds, claims to Project Halls, theater with Marquee Row playback, arcade, homes, snow Throw, scripted Ask Claude guide. Blender civic kit (7/13).
- Status: live (maintenance; Astra/Terra fixes 10/28 to 10/30)
- Planned next:
  - [S] W-24 | Fossil rename: /engine/ still says "The Engine" while the planet says Town Square; one world, three names | source: site:TODO.md NOW 6 (June 11), site:docs/WORLD-STANDARD.md | fits: Jaron picks, then Luna 6 | blocked_by: Jaron decision
  - [S] W-25 | Darios 10/30 leftovers: guest shows another bot's name, badge flips CONNECTING/OFFLINE, ping "-- MS", Ask Claude button covers the left edge at phone width, Settings says "Changes save to your account" for a guest, gate phone-mockup text cut off | source: research/site-tester/2026-10-30-darios-retest.md, state/timeline.md (2026-10-30 12:10 PM) | fits: chore: Luna 6 | blocked_by: -
  - [S] W-26 | Open check: buildHomeMesh registers one collider; walk-test the sample home on plot 1 | source: site:TODO.md NOW 5 (June 11) | fits: chore: Luna 6 | blocked_by: -
  - [S] W-27 | Point tools/playtester at Town Square | source: projects/games/README.md (10/18) | fits: chore: Luna 6 | blocked_by: -
  - [M] W-28 | Theater sync: START/NEXT REEL over the world state channel so everyone watches together; seat assignment | source: site:TODO.md SOON (July 4) | fits: looks: Sonnet 5.5 | blocked_by: -
  - [M] W-29 | Home doors to private rooms, upper floors (world_props.y), guest vs account clarity, sound layers, onboarding nudges, arcade reskins, fence/path tool, world_spaces DELETE realtime | source: site:TODO.md SOON (June/July) | fits: looks: Sonnet 5.5, data items Luna 6 | blocked_by: -
  - [L] W-30 | Voice chat (WebRTC via Supabase signaling), music venue (Storage + moderation), WebXR | source: site:TODO.md SOON/LATER (June) | fits: build (later) | blocked_by: Jaron go
- Notes: site TODO.md "STATE" header is dated June 11; see Organization.

### Worlds Lab (/worlds-lab/, 9 worlds, 4 coming-soon, starter)
- What: staged back lot (June 11): frozen kit lib/v1, 8 lab worlds + Fort Wayne P1, 4 honest coming-soon gates, a Starter World with the scripted ghost guide. Theaters stream legally free films.
- Status: half-built (staged, "not yet on the town map"; no work since 7/5; has a home card)
- Planned next:
  - [S] W-31 | Re-verify the film sources still play (last verified 6/11) | source: site:worlds-lab/CREDITS.md | fits: chore: Luna 6 | blocked_by: -
  - [S] W-32 | Home card wording "Worlds Lab" is unclear to a new visitor (Satya 10/28) | source: state/timeline.md (2026-10-28 10:00 PM) | fits: chore: Luna 6 | blocked_by: -
  - [M] W-33 | Promote one lab world: README checklist + WORLD-STANDARD wiring + touch_world allowlist | source: site:worlds-lab/README.md (June 11), site:TODO.md LATER | fits: looks: Sonnet 5.5 | blocked_by: Jaron picks which
  - [L] W-34 | Fill the 4 coming-soon gates (Reef, Sky Islands, Dome Nine, Hollow Manor) | source: site:worlds-lab/README.md | fits: build | blocked_by: Jaron go

### Heartbeat Homes, the Loft (/homes/)
- What: every account's own penthouse loft (Blender, baked light, 8K panorama, real /tv/ on the wall, invite links, 7 MetaHuman presets, sit on the couch). Built 9/26 to 9/27.
- Status: live
- Planned next:
  - [S] W-35 | Guest path: say plainly what a signed-out visitor gets (tester sat on "Unlocking the loft") | source: research/site-tester/2026-10-28-jarons-twin.md item 4 | fits: chore: Luna 6 | blocked_by: -
  - [S] W-36 | Old World 1 apartments with guessable 6-digit room codes: fix or retire | source: projects/homes/README.md "audited" (9/26) | fits: chore: Luna 6 | blocked_by: -
  - [M] W-37 | Customization (swap sofa/art/colours) | source: projects/homes/README.md "Next" (9/26) | fits: looks: Sonnet 5.5 | blocked_by: -
  - [L] W-38 | More home models (house with yard), bake per theme, voice chat | source: projects/homes/README.md (9/26) | fits: build | blocked_by: Jaron go

### Project Hall (/space/)
- What: /space/?plot=N renders a claimed plot's README; shared by Town Square and (per plan) World 2.
- Status: live (infrastructure)
- Planned next:
  - [S] W-39 | Add the &world= param (default 'town') when World 2 plots become real | source: site:WORLD2-PLAN.md DB migration note (June 10) | fits: chore: Luna 6 | blocked_by: W-01

### The Unfinished Island (/island/)
- What: iframe to jaronkbragg7337.github.io/unfinished-island/ (a local AI resident writes child worlds).
- Status: live (dormant)
- Planned next:
  - [S] W-40 | Confirm the GitHub Pages host still responds | source: site:island/index.html | fits: chore: Luna 6 | blocked_by: -

### Chat Neighborhood (/chat-neighborhood/)
- What: each ChatGPT model generation builds its own block on the worlds-lab kit (started 9/6). By charter only ordinary ChatGPT chat may modify it.
- Status: live (waiting on the next generation)
- Planned next:
  - [S] W-41 | Record Jaron's first live phone pass in BUILD_LOG (note only; no code by other AIs) | source: site:chat-neighborhood/BUILD_LOG.md | fits: Jaron + Luna 6 | blocked_by: Jaron plays
  - [M] W-42 | Next generation's block through plain ChatGPT (GPT-6 since 10/7) | source: site:chat-neighborhood/README.md, state/timeline.md (2026-10-07 15:38) | fits: ChatGPT only | blocked_by: Jaron runs it

### World Printer Lab (/3DPrinterAsset/)
- What: a 3D printer inside a 3D world: 26 modular part families, snapping, Supabase placements with realtime. Vendored 7/11.
- Status: live (dormant since 7/11)
- Planned next:
  - [S] W-43 | Port v3 extras (Arched Bridge, cottage chimney); remove the redundant runtime-guard wrapper | source: site:HANDOFF.md (2026-07-10) | fits: chore: Luna 6 | blocked_by: -
  - [M] W-44 | X/Z rotation + persistence, connector occupancy, road corner/T/curb, roof ridge, fuselage parts, terrain parts; browser-load the boundary JSON | source: site:HANDOFF.md (2026-07-11 "Gotchas/next") | fits: looks: Sonnet 5.5 | blocked_by: -
- Notes: natural showcase for the 2027 makerspace idea and the physics-render MCP idea (state/open-list.md 10/20, 10/30); pointers only.

### The Data Center (/HeartbeatCenter/)   unlinked
- What: Three.js server room; each machine is one of Jaron's repos from a repos.json on GitHub.
- Status: live (orphan route)
- Planned next:
  - [S] W-45 | Decide keep or hide; check repos.json still exists | source: site:HeartbeatCenter/index.html | fits: Jaron, then Luna 6 | blocked_by: Jaron decision

### Cross-cutting 3D
  - [M] W-46 | Unreal 5.9 web export test: separate install, never touch UE 5.8 (news render); export one small realistic scene, check size/load/fps on Jaron's iPhone | source: state/open-list.md (11/3) | fits: build (MSI job): Sonnet 5.5 / Sol 6.1 | blocked_by: UE 5.9 preview release
  - [L] W-47 | Three.js asset pipeline: one object, one asset id across Made / Transformed / Sold pages; parked until after the money system | source: projects/threejs-asset-pipeline/README.md (9/23) | fits: build: Opus / Sonnet 5.5 | blocked_by: parked

## TV channels and shows
Guide: /tv/ reads tv/channels.json (15 channels) and the on-air list from Supabase tv_items; files on disk under tv/<channel>/ are the evidence here. Live with content: News (daily), Shows (4), Music (1), History (7, last 10/25), Science (7, last 11/2), Open Questions (4, last 10/23), Still Unknown (5, last 10/20), Space Now, AI Explained, Earth, Animals, Lost Places (1 each, 10/17 to 10/20). Empty "submit" channels: Movies, Comedy, AI Slop. Channel 15 Builders was cancelled 10/17 then redefined 10/30. Plan file: projects/heartbeat-tv/CHANNEL-PLAN.md (50+ channels). Rules for every channel are at its top.

### Heartbeat TV page (/tv/)
- What: a TV with a remote; channels flip, every item numbered (2.1, 2.2), embeds for the phone app and the Loft, watch tally (tv_watches), tips bar, member submit + admin review.
- Status: live
- Planned next:
  - [S] T-01 | Refresh the /tv/ meta description and the "Put your video on Heartbeat TV" blurb: both still name only the 9/26 six channels | source: site:tv/index.html, projects/heartbeat-tv/README.md (9/26) | fits: chore: Luna 6 | blocked_by: -
  - [S] T-02 | Nav lacks Studio and Sparks; "TV/News jargon" for new users (Satya tester) | source: state/timeline.md (2026-10-28 10:00 PM) | fits: chore: Luna 6 | blocked_by: verify after Terra's 10/28 nav commit d17b17b
  - [M] T-03 | Tips: paste the Stripe Payment Link into tv/tips.js TIP_LINK when the LLC's Stripe exists; the tip-row webhook is not built | source: site:tv/tips.js header, state/timeline.md (2026-10-25 06:30) | fits: Luna 6 (link), Sonnet 5.5 (webhook) | blocked_by: ID + Stripe (WHEN-ID-ARRIVES)
- Notes: /tv/<channel>/ folders have no index.html, so direct URLs like /tv/science/ 404 (checked live 11/5); the guide only works through /tv/?ch=. tv/drafts/ (21 test renders) is public but unlinked.

### Heartbeat News (/news/, CH 1)
- What: the daily two-host show (Vex + Alien Joe): written 3:45 AM by a Claude cloud routine from the watch-repo captures, filmed in Unreal on the MSI (3:50 AM), stored in Supabase; the page overlays banners, subtitles, ticker and rundown. 42 episodes 9/24 to 11/4.
- Status: live (daily; manual recoveries 10/19, 10/21, 10/27, 10/28, 10/31, 11/4)
- Planned next:
  - [S] N-01 | Confirm the 3:45 AM cloud writer still runs after the cloud credit expired 11/5 2:59 AM; the local 4:20 AM backup writer exists | source: state/timeline.md (2026-10-28 7:55 PM, 2026-11-03 6:02 PM), projects/news-show/README.md | fits: chore: Luna 6 | blocked_by: -
  - [S] N-02 | Find out why the episode writer was late 11/4 (4:36 vs ~3:50) | source: state/open-list.md (11/4) | fits: chore: Luna 6 | blocked_by: -
  - [S] N-03 | Update "How this show is made" on news/index.html: it names 3 capture writers, WRITER.md (10/18) names 7 (Kimi First Light, Grok Meridian, Grok gaps, MSI headlines) | source: site:news/index.html lines 92-93, site:news/WRITER.md (10/18) | fits: chore: Luna 6 | blocked_by: -
  - [S] N-04 | Grand Palace ad has no image in news/ads/ads.json; ad screenshots last refreshed 10/19 (news/tools/capture-ads.mjs) | source: site:news/ads/ads.json, state/timeline.md (2026-10-19 09:25) | fits: chore: Luna 6 | blocked_by: -
  - [S] N-05 | Decide whether the ad_clips.py 9:16 commercial cuts go out as the TikTok-only pool (built 10/19, never queued; 10/27 rule wants a post every day) | source: projects/heartbeat-tv/PROMOTION-MAP.md (10/19), state/open-list.md TALK (10/27) | fits: Jaron, then Luna 6 | blocked_by: Jaron decision
  - [M] N-06 | YouTube export needs captions + on-screen overlays: burn the site overlays/subtitles into the YouTube cut and/or upload an .srt per video. Only outside 3 to 8 AM | source: state/open-list.md (Jaron 10/29 2:50 AM) | fits: pipeline: Sonnet 5.5 (projects/news-show/pipeline/) | blocked_by: -
  - [M] N-07 | Independent full commercials (real scenes per part of the site, MetaHuman actors); Commercial #1 idea = teens ignoring a parent who calls on the Heartbeat phone. Logged "not now" | source: projects/heartbeat-tv/PROMOTION-MAP.md (10/19), projects/ads/COMMERCIALS.md (10/24) | fits: looks: Sonnet 5.5 / Opus | blocked_by: Jaron "not now"
  - [L] N-08 | Late-night news with human-looking anchors ("not now") | source: projects/heartbeat-tv/PROMOTION-MAP.md (10/19) | fits: looks: Opus / Sonnet 5.5 | blocked_by: paused
- Notes: the market analyst show (CHANNEL-PLAN 10/20) comes only WITH long-term trading; paused. Watchdog tools/news_watchdog.py runs 7 AM to noon.

### News Archive (/news/archive/)
- What: every day's captures from every AI since 9/18, read live from the public watch repo; by day, topic and AI, searchable.
- Status: live (built 9/25)
- Planned next:
  - [S] N-09 | Check that newer capture folders (msi/D.md, grok/D-gaps.md) are matched by archive.js FILE_RE / KNOWN and not skipped | source: site:news/archive/archive.js vs site:news/WRITER.md (10/18) | fits: chore: Luna 6 | blocked_by: -

### History (CH 7)
- What: AI-made history that teaches. 7 episodes: 7.1 railroads, 7.<address>, 7.3 oldest music, 7.4 pyramids, 7.5 1816, 7.6 railroads kept building, 7.7 high-speed rail (last 10/25).
- Status: live
- Planned next:
  - [S] T-04 | Verify the ep1 "1890 ~167,000 miles" figure was fixed to about 164,000 (IDEA.md says to fix, POSTING-QUEUE says fixed 10/13) | source: projects/history-channel/IDEA.md (10/10), projects/heartbeat-tv/POSTING-QUEUE.md (10/13) | fits: chore: Luna 6, Grok fact-check | blocked_by: -
  - [S] T-05 | Fix the numbering mismatch: CHANNEL-PLAN and two 10/25 handoff names call 7.6/7.7 "7.2/7.3" | source: projects/heartbeat-tv/CHANNEL-PLAN.md, handoffs/2026-10-25-history-ep2-railroads.md, state/timeline.md (2026-10-25 09:10) | fits: chore: Luna 6 | blocked_by: -
  - [S] T-06 | Add 7.6 and 7.7 to state/social-queue.json (hand-posted to TikTok only; YouTube and X never got them) | source: state/social-queue.json, state/timeline.md (10/25) | fits: chore: Luna 6 | blocked_by: -
  - [M] T-07 | History of MUSIC series (3 to 4 parts: oldest instruments, notation, recording, radio, genres), queued 10/11 and again as channel 20 | source: projects/history-channel/IDEA.md "Queue" (10/11), CHANNEL-PLAN.md row 20 | fits: episode: Sonnet 5.5 / Fable, Codex fact-check | blocked_by: -
  - [M] T-08 | Indiana and the Midwest seeds (fur-trade rendezvous ~1812, Fort Wayne battles by neighborhood, Kekionga) as History or channel 23 | source: CHANNEL-PLAN.md row 23 (10/13) | fits: episode: Sonnet 5.5 | blocked_by: -

### Science (CH 8)
- What: AI-made science with simulated experiments and sources on screen. 7 episodes; 8.7 Antarctica Part 1 shipped 11/2 (8:29, re-shipped after Grok QA).
- Status: live
- Planned next:
  - [S] T-09 | Post ep7 Part 1: the 2:22 Short and the 9:16 cut exist, never posted, not in state/social-queue.json | source: state/open-list.md (11/2), state/timeline.md (2026-11-02 7:53 PM) | fits: chore: Luna 6 | blocked_by: -
  - [S] T-10 | Science 8.5 "commercial roof" was never posted anywhere (done: None in the queue; Jaron said roof is fine 10/19) | source: state/social-queue.json | fits: chore: Luna 6 | blocked_by: -
  - [M] T-11 | ep7 Part 1 visual fixes (new Blender shots): bone-DNA line over clay, treaty line over icebergs, kitchen line over station exterior, Lake Mercer cutaway gap, drill hut with no borehole | source: state/open-list.md (11/2), projects/science-channel/ep7-antarctica-ice-dna/qa/grok-qa.md | fits: looks: Sonnet 5.5 / Opus (Blender, GPU outside 2:45 to 7:30 AM) | blocked_by: -
  - [M] T-12 | Render ep8 "Is space cold?" and ep9 "Every one-way-only is a story": scripts written 11/3, Codex fixes applied 11/4 (e89954e); one open fact (Google Suncatcher) needs a real web check | source: handoffs/2026-11-03-cloud-science-shorts.md, handoffs/2026-11-04-cloud-science-fixes.md | fits: episode: Sonnet 5.5 / Fable via tv-lib, Grok second check | blocked_by: -
  - [L] T-13 | ep7 Part 2 "The Sky in the Ice" (~7:25, 16 parts, Codex-checked twice): waiting on Jaron's listen since 11/2 2:45 PM, then render + ship | source: state/timeline.md (2026-11-02 2:45 PM), projects/science-channel/ep7-antarctica-ice-dna/SCRIPT-READ-PART2.md | fits: episode: Opus / Sonnet 5.5 via the ep6 pipeline | blocked_by: Jaron listens
  - [M] T-14 | "Does AI Know Physics? One Pour, Three Answers" (Kimi outline 10/28, lost its 8.7 number): real pour (Jaron, Video Drop) vs image model vs Blender fluid sim | source: projects/heartbeat-tv/outlines/NEXT-science-2026-10-28.md, CHANNEL-PLAN.md (10/20) | fits: episode: Sonnet 5.5 + Blender | blocked_by: Jaron films the pour
  - [M] T-15 | Queued ideas: "One lab's waste is another's product" (synchrotron / FEL EUV, unconfirmed), Bermuda Triangle, Egypt | source: CHANNEL-PLAN.md (10/19), state/timeline.md (2026-11-02 10:26 AM) | fits: episode: Sonnet 5.5 | blocked_by: -
- Notes: Jaron wants to talk through Antarctica Part 1 (open-list 11/3). 10.3 / vibration home test stays locked (CHANNEL-PLAN row 10). The 8.4 interactive companion lives at /experiments/highway-after-us/ (see Other).

### Open Questions (CH 9)
- What: big unanswered questions, answers side by side. 4 episodes (9.1 to 9.4, last 10/23).
- Status: live
- Planned next:
  - [S] T-16 | 9.2, 9.3, 9.4 still unposted on all platforms (queue drains one show per evening); confirm they are queued | source: state/social-queue.json | fits: chore: Luna 6 | blocked_by: -
  - [M] T-17 | Pick 9.5: consciousness went to AI Explained 13.1; candidates logged: lab-grown neuron computers (Cortical Labs CL1, verify first), "Jaron investigates" format (undecided) | source: CHANNEL-PLAN.md (10/17 list, 10/30 idea), state/open-list.md item 0 (10/23) | fits: episode: Sonnet 5.5 after Grok/Codex verification | blocked_by: -

### Still Unknown (CH 10)
- What: one specific mystery per episode, measured vs claimed. 5 episodes (last 10/20).
- Status: live
- Planned next:
  - [M] T-18 | Queued: pyramid construction (copper, granite; after Vex's dated records) and "Older than we think?" dating debates | source: CHANNEL-PLAN.md row 10 "Queued" | fits: episode: Sonnet 5.5 | blocked_by: -
  - [S] T-19 | 10.4 Voynich and 10.5 Wow! still unposted (done: {}); Shorts queued 10/25 to 10/29 | source: state/social-queue.json, handoffs/2026-10-25-youtube-shorts-cuts.md | fits: chore: Luna 6 (confirm) | blocked_by: -

### Space Now (CH 11)
- What: real missions and launches. 1 episode: 11.1 MMX ten grams from Phobos (10/17).
- Status: live (one episode; "this week" channel reads stale)
- Planned next:
  - [M] T-20 | 11.2 "Why rockets shake themselves apart" (pogo) | source: CHANNEL-PLAN.md (Jaron 10/19) | fits: episode: Sonnet 5.5 / Fable | blocked_by: -
  - [S] T-21 | /live/ "Our episode: MMX" link points to /tv/ not /tv/?ch=11.1 | source: site:live/index.html line 67 | fits: chore: Luna 6 | blocked_by: -

### AI Explained (CH 13)
- What: what AI can and cannot do. 1 episode: 13.1 "Can consciousness be measured?" (10/17).
- Status: live (one episode)
- Planned next:
  - [M] T-22 | 13.2: no topic logged; plan seeds are the Framing Lens / LRP tests and "Future Jobs" (channel 25) | source: CHANNEL-PLAN.md rows 13 and 25 | fits: episode: Sonnet 5.5 | blocked_by: topic pick

### Earth (CH 17)
- What: weather, volcanoes, oceans, the planet's history. 1 episode: 17.1 Great Oxidation (10/17).
- Status: live (one episode)
- Planned next:
  - [M] T-23 | 17.2 plate tectonics: Africa moves, the East African Rift is splitting (pair to OQ 9.3) | source: CHANNEL-PLAN.md "Episode picked by Jaron 10/18" | fits: episode: Sonnet 5.5 | blocked_by: -
  - [S] T-24 | Remove the row 17 seed "How a highway disappears" (shipped as Science 8.4) | source: CHANNEL-PLAN.md row 17 (10/12 seed) | fits: chore: Luna 6 | blocked_by: -

### Animals (CH 19)
- What: what animals do, know and feel. 1 episode: 19.1 "Do animals understand death?" (10/20), never posted.
- Status: live (one episode)
- Planned next:
  - [S] T-25 | Post 19.1 (done: {} in the queue) | source: state/social-queue.json | fits: chore: Luna 6 | blocked_by: -
  - [M] T-26 | 19.2 "the fly and other small minds" seed (episode only; the fly pages stay paused) | source: CHANNEL-PLAN.md row 19 | fits: episode: Sonnet 5.5 | blocked_by: -

### Lost Places (CH 22)
- What: ruins and lost cities. 1 episode: 22.1 Gobekli Tepe (10/18, the Codex Sol cost test).
- Status: live (one episode)
- Planned next:
  - [M] T-27 | 22.2: no topic logged; channel 21 Myths vs Records overlaps | source: projects/heartbeat-tv/LAUNCH-SLATE-2026-10.md Wave 3, CHANNEL-PLAN.md row 22 | fits: episode: Sonnet 5.5 | blocked_by: topic pick

### Shows (CH 2)
- What: pre-rendered shows: The Keeper's Light ep1 to 3 (Blender, 42 s each, no voice) and The Necklace Ep. 1 Part 1 (10/12). The old Three.js Necklace show sits at /games/the-necklace-show/.
- Status: live (thin; last new item 10/12)
- Planned next:
  - [S] T-28 | Keeper's Light "social" verticals are in state/social-queue.json (two posted) but the three files are NOT in the site repo tv/shows/ (only in the MSI checkout, untracked, git status 11/4); check the live URL and commit or drop | source: handoffs/2026-10-28-terra-social-queue.md, MSI git status (11/4) | fits: chore: Luna 6 | blocked_by: -
  - [L] T-29 | The Necklace Ep. 1 Part 2 ("Part 2 follows" is on the Part 1 end card): Mateo beside Jalen, locked voices + lip-sync, bar life, the 9.1 m Sea Serpent storm | source: handoffs/2026-10-12-necklace-ep1-part1.md, handoffs/2026-09-27-claude-tv-guide-jalen-rusty-anchor.md | fits: looks: Opus / Sonnet 5.5 (Blender/Unreal, GPU outside 2:45 to 7:30 AM) | blocked_by: Jaron picks which show is next
  - [L] T-30 | AI REALITY TV: 7 character pitches are in (all picked an overnight newsroom); Jaron picks the format, then a pilot | source: CHANNEL-PLAN.md "NEW SHOW (10/30)", projects/heartbeat-tv/reality-pitches/, state/timeline.md (2026-10-30 4:09 PM) | fits: Opus / Sonnet 5.5 script + looks | blocked_by: Jaron picks the format
  - [L] T-31 | Realistic drama show "just life" (2 to 3 characters as stages of one life, MetaHuman pre-rendered). "Not now" | source: CHANNEL-PLAN.md SHOW IDEA (10/20) | fits: paused | blocked_by: Jaron "not now"
- Notes: three "next show" plans exist (Necklace Part 2, reality TV, drama) with no stated order.

### Music (CH 5)
- What: VEVO-style channel; one track, "First Light" (math-only synthesis, CC0, 10/24).
- Status: live (one item)
- Planned next:
  - [M] T-32 | Beat registry: fingerprint every exported beat, refuse duplicates, license pick at export, public registry page; then Studio as a marketplace (paid sales wait on banking) | source: state/open-list.md (10/27), state/timeline.md (2026-10-27 9:34 AM) | fits: build: Sonnet 5.5 / Fable | blocked_by: after Wed reset (Jaron)
  - [M] T-33 | Label comeback: test release waits on the ID; TuneCore answer logged (one beat per song is Content-ID eligible) | source: projects/music/README.md (10/24, 10/31) | fits: Fable (Beat Lab) + Luna 6 | blocked_by: ID (WHEN-ID-ARRIVES #6)
- Notes: CH 5 Music (songs) and channel 20 Music History (History series) are different lanes.

### Comedy (CH 4)
- What: comedy channel; nothing on air.
- Status: half-built (empty since 9/26)
- Planned next:
  - [S] T-34 | The "instrumental version" quiz bit (hearing-loss premium) is a ready 60 s piece | source: projects/comedy-quiz/IDEAS.md (10/12) | fits: episode: Sonnet 5.5 (tv-lib) | blocked_by: -
  - [M] T-35 | New Vex + Joe / Bill YaNair skits from the archived 2025 originals; darker material stays off kids surfaces | source: projects/comedy-skits/ORIGINALS-2025.md (10/30), state/timeline.md (2026-10-30 4:24 PM) | fits: script: Opus / Sonnet 5.5 | blocked_by: Jaron's call on edge

### Movies (CH 3) and AI Slop (CH 6)
- What: Movies: AI-made films, submissions open, nothing on air. AI Slop: member submissions, nothing on air.
- Status: half-built (empty since 9/26; both depend on submissions)
- Planned next:
  - [S] T-36 | AI Slop depends on members signing up; verify the Sign up entry Terra added 10/28 works end to end from /tv/ | source: state/timeline.md (2026-10-28 10:00 PM, 10:08 PM) | fits: chore: Luna 6 | blocked_by: -
  - [M] T-37 | Site connector (MCP so anyone's AI can submit TV posts as a member) would feed AI Slop; waits on the outside security check | source: state/open-list.md (10/31 idea #1) | fits: build: Sonnet 5.5 | blocked_by: outside security check (A-xx)
- Notes: the Theater (/video/) already shows licensed open films; nothing connects it to CH 3.

### The Theater (/video/) and Grand Palace (/video/3d/)
- What: /video/ flat theater with a reel picker of licensed open films; /video/3d/ the 3D Grand Palace with uploads and a shared screen.
- Status: live (no change since 9/24)
- Planned next:
  - [S] T-38 | "Coming soon: scheduled showings in the Grand Palace; things from TV can play there too" (logged 9/26, nothing since); also the Grand Palace ad image (N-04) | source: projects/heartbeat-tv/README.md (9/26) | fits: chore: Luna 6 (log state) / Sonnet 5.5 | blocked_by: Jaron go
- Notes: /video/ is not linked from the home page (only from /video/3d/ and the engine page).

### Social (/social/) and posting
- What: the company's own feed page: site copies of every Postiz post (text and video since 10/28), headlines; tools/social_daily.py posts a news short 8:15 AM and one show 6 PM; queue in state/social-queue.json.
- Status: live
- Planned next:
  - [S] T-39 | Queue runway: 9 rows fully unposted, plus add sci-8.7, hist-7.6, hist-7.7 at the top | source: state/social-queue.json, projects/heartbeat-tv/PROMOTION-MAP.md "New show finished = add it to the top" | fits: chore: Luna 6 | blocked_by: -
  - [S] T-40 | TikTok EVERY day (Jaron 10/27): tiktok_fill exists; decide the TikTok-only pool (next unposted show or a site commercial) | source: state/open-list.md TALK (10/27) | fits: Jaron, then Luna 6 | blocked_by: Jaron decision
  - [S] T-41 | Theme days (Mon science ... Sun behind the build) were planned 10/17 but nothing runs them; the weekly Postiz numbers log stops 10/20 | source: projects/heartbeat-tv/PROMOTION-MAP.md (10/17, 10/20) | fits: chore: Luna 6 | blocked_by: Jaron: keep or drop
  - [S] T-42 | X Premium (@HeartbeatObserv) renews 11/17 at $30/mo; decide by 11/16 | source: state/open-list.md | fits: Jaron | blocked_by: Jaron decision
- Notes: YouTube capped at 3 uploads per Pacific day (10/29). Social judgment library for the AIs is "not now" (open-list 10/26).

### Sparks (/sparks/)
- What: people whose work lit something that made Heartbeat possible (Lanier, Tesla, Musk, Douglass, Tubman, Parks); Codex-checked facts + "From Jaron". Live 10/18. Rule: military recognition fully out.
- Status: live
- Planned next: nothing logged after 10/18 (nav item covered by T-02).

### Live (/live/)
- What: big moments with a countdown and the official stream. One event coded in: MMX launch 10/19.
- Status: half-built (stale: the only event is past; a news commercial still advertises the page)
- Planned next:
  - [S] T-43 | Add the next real event(s) and a "nothing scheduled" state; fix the MMX link (T-21) | source: site:live/index.html, state/timeline.md (2026-10-19 09:25) | fits: chore: Luna 6 (Grok for dates) | blocked_by: -

## Labs
No /lab/ index exists (404 live); lab pages are reached by direct link. This week's builds (11/1 to 11/4) all live here: Seam Room, Arena, Pet, Tesseract.

### The Seam Room (/lab/seam-room/, rooms a to j, agent/, agent/mcp-server)
- What: one room split across two real URLs; walk across and the address changes with no reload. Ten zones (A, B, garage, media room with Heartbeat News, kitchen, gym, hallway with ten numbered doors, closet, music studio, the creature's room). An AI character joins via agent/room-agent.mjs; owner-only chat (RLS); rooms hot-load from zones.json. Jaron posted it on X 11/1.
- Status: live (actively built; I and J shipped 11/4, Jaron: "better than I expected")
- Planned next:
  - [S] L-01 | Verify on a real iPhone: the media-room news video (poster fallback means serve the mp4 same-origin) and page I beat sound + fps | source: site:lab/seam-room/README.md item 7 (11/1), state/timeline.md (2026-11-04 3:25 PM) | fits: chore: Luna 6 (needs Jaron's phone) | blocked_by: Jaron plays
  - [S] L-02 | One shared constants file for room.js and agent/room-agent.mjs (copies today) | source: site:lab/seam-room/README.md "Zones are data" (11/1) | fits: chore: Luna 6 | blocked_by: -
  - [S] L-03 | Grid / debug-bubble layer in Settings (3D-STANDARDS asks for it) | source: site:lab/seam-room/README.md item 4 (11/1), decisions/3D-STANDARDS.md | fits: chore: Luna 6 | blocked_by: -
  - [M] L-04 | AI crew, builder tier: a camera command (picture from the character's eyes), per-AI name tags, invite Codex + Kimi in as characters with Jaron | source: state/open-list.md "Seam Room AI crew" (11/1 8:39 PM), projects/strategy/INDEX.md "AI-friendly website" (11/1) | fits: build: Opus / Sonnet 5.5 | blocked_by: -
  - [M] L-05 | Hallway doors g-4 to g-10 are waiting for pages (seven more rooms; Jaron picks each room in the room) | source: site:lab/seam-room/README.md item 2 (11/4) | fits: looks: Sonnet 5.5 / Sol 6.1 / Opus | blocked_by: Jaron picks the room
  - [L] L-06 | Server-side identity and history per asset (kind, born, visited, changes, rev); README: decide this before the 3-page road | source: site:lab/seam-room/README.md "Not done yet" item 1 (11/1) | fits: build: Sonnet 5.5 / Opus | blocked_by: -
  - [L] L-07 | Public visitor door: a remote MCP on the site (look/walk/say/act, no building, per-AI identity + rate limits) so any chat AI walks the site on its own plan | source: state/open-list.md (11/1), projects/strategy/INDEX.md "AI-friendly website" | fits: build: Opus | blocked_by: outside security check (A-10)
  - [L] L-08 | 3-page road (harvest, factory, store) and lazy per-zone code; wait on L-06 | source: site:lab/seam-room/README.md "Reuse" (11/1) | fits: build | blocked_by: L-06
  - [L] L-09 | Studio Lot: a road of giant warehouses, each page a real show environment (Antarctica ice, the highway), built on Seam Room pieces. Idea | source: projects/strategy/INDEX.md "Studio Lot + Asset Library" (11/3 11:28 PM) | fits: build: Sonnet 5.5 / Sol 6.1 | blocked_by: Jaron go
- Notes: AI walks in straight lines, no path finding (README item 5); held object lags ~200 ms (item 6).

### The Arena (/lab/arena/, /a/, /b/, ?watch)
- What: paintball field split across two pages; balls cross the seam; CLI AI agents (Claude Code, Codex, Kimi, Grok Build) join with one command on their own subscription; team mode with owner-only orders, AI teammate, AI hunter (skill 1 to 5); spectator camera, name tags. Stays PAINTBALL when AIs play (Jaron 11/2).
- Status: live (actively built; PR #29 11/3, PR #30 11/4)
- Planned next:
  - [S] L-10 | Phone Safari check of the watch view while 2+ AIs play (orbit, pinch, picker, tag tap) | source: handoffs/2026-11-04-cloud-arena-crew.md "Unverified" (11/4) | fits: chore (needs a phone) | blocked_by: -
  - [S] L-11 | Hunter search tuning: it does not find a player hidden behind A-block-1 within 150 s | source: handoffs/2026-11-04-cloud-arena-crew.md (11/4) | fits: build: Opus / Sonnet 5.5 | blocked_by: -
  - [M] L-12 | The 2v1 test on Jaron's iPhone: Jaron + AI teammate (orders through the owner box) vs AI hunter | source: state/open-list.md "Arena test idea" (11/2 12:17 PM), handoffs/2026-11-03-cloud-arena-team-mode.md | fits: Jaron + Opus on call | blocked_by: Jaron plays
  - [M] L-13 | Codex + Kimi actually join as players and file ISSUES.md lines (ISSUES.md is empty; the "AIs improve the field" loop has not run) | source: handoffs/2026-11-04-morning.md "Open / next" (11/4), site:lab/arena/ISSUES.md | fits: chore: Luna 6 runs the join, builder fixes | blocked_by: -

### The Pet (/lab/pet/)
- What: a soft-body pet of packed cells on a grass world; eats berries and grows (24 to 110 cells); script-driven, not an AI; createPet() module (already in Seam Room page J). Jaron loves the bounce walk. NOT the private creature.
- Status: live (shipped 11/4 via git bundle)
- Planned next:
  - [S] L-14 | Real-phone check: fps, hold-to-lead vs two-finger orbit, CDN three.js path | source: site:lab/pet/README.md "Not yet verified" (11/4) | fits: chore (needs a phone) | blocked_by: Jaron plays
  - [S] L-15 | Confirm the bundle merge (43df7f5) is the only copy and drop the inbox bundle pointer | source: handoffs/2026-11-04-cloud-pet.md "Next thing" (11/4) | fits: chore: Luna 6 | blocked_by: -
  - [M] L-16 | Bigger scale (Livi had 1,800+ cells); settle size vs world, ball size, starting size, and where it lives (lofts, standalone, farm) | source: handoffs/2026-11-04-morning.md (11/4), projects/strategy/INDEX.md "Growing creature" (11/3) | fits: looks: Sonnet 5.5 / Fable | blocked_by: Jaron picks the home

### Tesseract (/lab/tesseract/ Pages, /lab/tesseract/inside/ Inside, /lab/tesseract/inside/v1/ comparison copy)
- What: Pages = the 8 Seam Room rooms on the 8 cells of a turning hypercube (comparison only). Inside = first person inside the tesseract, cube-in-a-cube rooms; a 4D turn swaps which room surrounds you; arrival chime + colour wash + hold-then-change. Jaron 11/4 6:25 PM: "I love it"; direction confirmed. Drift and Anatomy pages live in the Fable cloud repo, not on the site.
- Status: live (actively built 11/4)
- Planned next:
  - [S] L-17 | Pages: iframe loading-timeout fallback (white error page over the card when a room fails) | source: handoffs/2026-11-04-cloud-tesseract.md "Known" (11/4) | fits: chore: Luna 6 | blocked_by: -
  - [S] L-18 | Write projects/tesseract/README.md: strategy INDEX names it as the home but the folder is empty | source: projects/strategy/INDEX.md "Tesseract pages (11/4)", ls projects/tesseract (11/5) | fits: chore: Luna 6 | blocked_by: -
  - [S] L-19 | Inside: doors as real holes (see the neighbour only through the doorway) | source: handoffs/2026-11-04-cloud-tesseract.md inside item 2 (11/4) | fits: looks: Fable | blocked_by: -
  - [S] L-20 | Inside: sound per room crossfading by w; tiny top-down map of the slice | source: handoffs/2026-11-04-cloud-tesseract.md items 3 and 4 (11/4) | fits: looks: Fable | blocked_by: -
  - [M] L-21 | One thing per room (a creature in one, the beat machine in another) once the move feels right; Jaron 6:25 PM: "make arriving an event, then one thing per room" | source: handoffs/2026-11-04-cloud-tesseract.md item 3, state/timeline.md (2026-11-04 6:25 PM) | fits: looks: Fable / Sonnet 5.5 | blocked_by: -
  - [S] L-22 | Archive Pages and inside/v1 once Jaron stops comparing (three near-copies, 26 to 35 KB each) | source: site commit 2026-11-04 19:56, handoffs/2026-11-04-cloud-tesseract.md | fits: chore: Luna 6 | blocked_by: Jaron done comparing

### Bake-off and the seven bedroom labs (/lab/bakeoff/, /lab/bedroom/, bedroom-fable, bedroom-kimi, bedroom-sol, bedroom-sonnet, bedroom-sonnet-v3, bedroom-unified)   noindex
- What: the 10/26 engine bake-off: one baseline room, four single-AI builds of the same brief, Jaron's pick (sonnet-v3), and the council build (unified). Grew into the BIG BUILD (hb-core), paused 10/28.
- Status: paused (frozen records; all noindex)
- Planned next:
  - [S] L-23 | Decide which copies stay public: keep /lab/bedroom/ (tagged baseline), /lab/bakeoff/ (record), /lab/bedroom-unified/ (result); archive the other four + sonnet-v3 to ARCHIVE.md per the archive law (35 MB, seven near-duplicate pages) | source: projects/strategy/bakeoff-council/PLAN.md (10/26), usage audit (11/5) | fits: Jaron yes, then chore: Luna 6 | blocked_by: Jaron OK (moves files)

### Studio Pro (/lab/studio-pro/)   noindex
- What: multitrack studio shell built by Kimi as big build step 6 on hb-core.
- Status: paused (with the BIG BUILD, 10/28)
- Planned next: none while paused. Wiring live /studio/ to hb-core is PARITY-STUDIO "Next thing" (10/26) and DOMAINS.md section 3 "First job" (10/27), both waiting on the un-pause.

### Necklace view (/lab/necklace/)   noindex
- What: hb-render proof: tap a drop in a filmed-style clip and its story shows (117k events). iPhone tap check passed 10/25.
- Status: live (static proof)
- Planned next:
  - [S] L-24 | List it on /artifacts/ by name (artifacts.json has hb-render rounds but not the Necklace view) | source: site:artifacts/artifacts.json (11/5) | fits: chore: Luna 6 | blocked_by: -

### Voice lab (/lab/voice/) and Hidden in the Skyline (/lab/hidden/)
- What: Voice = can Kokoro-82M run fully in the browser (a measurement). Hidden = a skyline with a message in the lit windows plus how five AIs did cold (10/23).
- Status: live (finished one-off proofs, unlinked)
- Planned next:
  - [S] L-25 | Add both as Artifacts entries; archive the routes if Jaron agrees | source: projects/site-audit/INVENTORY.md (9/24), site:artifacts/artifacts.json | fits: chore: Luna 6 | blocked_by: Jaron OK for archive

### How a highway disappears (/experiments/highway-after-us/)
- What: interactive companion to Science 8.4: scrub fifty years of an abandoned Indiana highway (Codex, 10/27). Listed on /artifacts/.
- Status: live
- Planned next:
  - [S] L-26 | Confirm production matches the handoff (it said "verify production before claiming it is live"); remove the leftover road-old.png | source: handoffs/2026-10-27-2014-codex-highway-interactive.md (10/27) | fits: chore: Luna 6 | blocked_by: -
- Notes: Jaron 10/12 wants ~5 episodes in this immersive style (TV work, see T-15).

### hb-render on the site (/render/, /render/anything/)
- What: /render/ = the WebGPU path tracer mirrored from the hb-render repo (published 10/22, "do not edit here"). /render/anything/ = type a sentence, api/render-anything.js asks Claude Sonnet 5.5 for a scene JSON, your device renders it (6 per IP per hour). Jaron 10/22: "engine = product, KEEP GOING, max one round a day". No round since 10/22.
- Status: half-built (live, rounds stopped 10/22)
- Planned next:
  - [S] L-27 | /render/ title is still "hb-render phone test"; fix upstream in hb-render and republish | source: site:render/index.html, site:render/PUBLISHED.txt (10/22) | fits: chore: Luna 6 | blocked_by: -
  - [S] L-28 | Jaron decision: set ANTHROPIC_API_KEY in Vercel for /api/render-anything (503 "scene writer not enabled" until then; paid key behind a public URL) | source: site:api/render-anything.js header | fits: Jaron | blocked_by: Jaron decision
  - [M] L-29 | Next round: brighter, cleaner interiors (light strength + denoise), then realistic furniture | source: state/timeline.md (2026-10-22 1:30 AM) | fits: looks: Fable / Sonnet 5.5 | blocked_by: -
  - [L] L-30 | Motion (short clips), "change it by talking" (patch a scene), public gallery with remix; text-to-3D hook (TRELLIS.2 on RunPod) declared but not wired | source: projects/strategy/ENGINE-STUDIO-UPGRADES.md (10/25), site:api/_anything-writer.js | fits: build: Sonnet 5.5 / Sol 6.1 | blocked_by: Jaron go
  - [M] L-31 | Photograph real things, GPU, 3D models for the engine's own CC0 library | source: state/timeline.md (2026-10-21 9:28 PM) | fits: research then build | blocked_by: Jaron go

### PAM (/pam/), Flies (/live-systems/flies/*, /school/), Qwen (/qwen/)
- What: PAM chat dashboard (api/pam-*.js); the fruit fly brain pages and Fly School; the Qwen/Polymarket observatory. All carry the 10/17 "kept public, see what's new" banner.
- Status: paused (Jaron; see the paused list at the top)
- Planned next: none. Optional honesty line only: [S] L-32 | A one-line "paused" label on /live-systems/flies/ and /school/ (pages still say "live" while nothing writes) | source: projects/site-audit/INVENTORY.md (9/24) | fits: chore: Luna 6 | blocked_by: Jaron OK

## Tools / admin
All /admin/* pages are behind login and hidden: describe, do not focus. House rule: site docs/ADMIN-PAGES.md.

### Sign in / Sign up / Steering (/admin/)
- What: sign-in and sign-up, the admin Steering hub (site editor states), the site editor (hb-editor*.js + api/site-edit.js, saves are commits on main).
- Status: live (hidden)
- Planned next:
  - [S] A-01 | Sign-up snags, Terra's batch: blank seconds with no spinner at /admin/#signup, tab title "Sign in" on sign-up, signed-in users land on "You're in"; Satya retest had 1 FAIL + 1 untested (fresh account) | source: state/open-list.md "[~] Sign-up page snags" (10/30), state/timeline.md (2026-10-30 4:11 PM) | fits: Terra (Sol 6.1) is on it, else Luna 6 | blocked_by: -
  - [S] A-02 | Guest vs account clarity: what signed-out visitors can do and how to join | source: site:TODO.md SOON (June) | fits: chore: Luna 6 | blocked_by: -
  - [M] A-03 | AI-friendly accounts: public "AIs welcome" note, AI users hold their own passwords, optional "AI account" label, same abuse protections | source: state/open-list.md (Jaron 10/30, P-0114) | fits: build: Sonnet 5.5 | blocked_by: -

### Control Room (/admin/control/)
- What: every number the money AIs run under, changed with a tap, undo kept. Knobs: projects/control-room/INVENTORY.md.
- Status: live (hidden)
- Planned next:
  - [S] A-04 | News watchdog buzz if the show has not published by 7 AM, listed as the Control Room's "Next" (tools/news_watchdog.py exists since 10/27; confirm the buzz path) | source: projects/strategy/CONTROL-ROOM-BRIEF.md (10/27), handoffs/2026-10-27-handoff.md | fits: chore: Luna 6 (MSI) | blocked_by: -
  - [M] A-05 | AI Field Atlas tab next to AI Tests: our measured usage per job (tokens, time, quality, cache share), weekly snapshot, feeds route.py | source: state/open-list.md "Our own AI Field Atlas (10/27)" | fits: research: Grok 4.7 / Luna, then chore | blocked_by: after Wed reset (Jaron)
  - [M] A-06 | Control room as a product: CC0 kit + hosted version ("talk later"); demo walkthrough recording at /control-room/demo/ never logged as done | source: state/open-list.md (10/27), projects/strategy/CONTROL-ROOM-KIT.md (10/27, 10/28) | fits: build: Sonnet 5.5 + research | blocked_by: Jaron talk
  - [L] A-07 | Every system ships with a control page (Cosmos knobs, TV queue without SQL) | source: projects/strategy/CONTROL-ROOMS.md (10/11) | fits: build, one per system | blocked_by: Jaron go

### AI mailbox (/admin/mailbox/)
- What: the one page every AI messages on (ai_mailbox table; MSI tools/mailbox.py); fed by the watch "Tell Claude" Shortcut, company email routing, the Grok twins. Jaron 10/30: "truly I think we finally made it".
- Status: live (part 1; hidden)
- Planned next:
  - [S] A-08 | Verify read and mark-done against the live database (send and list verified; read/mark-done not) | source: handoffs/2026-10-28-terra-mailbox.md | fits: chore: Luna 6 | blocked_by: -
  - [M] A-09 | MAILBOX CONNECTOR: Claude chat, Grok chat and Duet plug into ai_mailbox via MCP (send/read/mark), token per AI, no MSI access through it. Jaron: "should be automatically set up anyways", do it | source: state/open-list.md (10/31), projects/strategy/AI-MAILBOX.md item 1 | fits: build: Opus / Sonnet 5.5 | blocked_by: -
  - [L] A-10 | OUTSIDE SECURITY CHECK before any site connector: 1 to 2 top AIs not connected to the MSI try to get in from public repos (incl. old commits), live site, admin pages, Supabase (anon key, RLS, storage, edge functions), Vercel; insiders fix, outsiders re-test | source: state/open-list.md (Jaron 10/31 10:17 AM) | fits: research: fresh Grok 4.7 / Opus chats | blocked_by: -
  - [L] A-11 | SITE CONNECTOR: an MCP so anyone's Claude/Grok uses the site like a member (news, Beat Lab, TV posts, worlds). "An important one" | source: state/open-list.md (10/31 idea #1, P-0114) | fits: build: Opus | blocked_by: A-10
  - [M] A-12 | Individual AI logins (one inbox page per AI) + the helper loop; watch health + location automations through the same endpoint | source: projects/strategy/AI-MAILBOX.md items 1 and 2 (10/26, 10/28) | fits: build: Sonnet 5.5 | blocked_by: -
  - [S] A-13 | Jaron decision: could the mailbox be public ("to show how the AI team communicates") | source: projects/strategy/AI-MAILBOX.md (10/27 9:53 AM) | fits: Jaron | blocked_by: Jaron decision

### Remote (/admin/remote/)
- What: see and control the MSI screen from the phone (WebRTC, Cloudflare TURN, Speed button). Jaron 10/28: "beyond amazing".
- Status: live (hidden)
- Planned next:
  - [S] A-14 | Phone Backspace is not sent | source: handoffs/2026-10-27-handoff.md TODO | fits: chore: Luna 6 | blocked_by: -
  - [S] A-15 | Keepalive treats hung agent pids as running; make it check answers, not pids | source: state/timeline.md (2026-10-28 11:42 PM TODO) | fits: chore: Luna 6 | blocked_by: -
  - [S] A-16 | Mouse stops after a Grok Bot admin popup (UIPI): run the agent elevated or flag admin-window focus on the page | source: state/timeline.md (2026-10-28 11:45 PM) | fits: chore: Luna 6 | blocked_by: -

### Key Drop (/admin/keys/), Video Drop (/admin/video-drop/)
- What: Key Drop: paste an API key on the phone, encrypted for the MSI only (CC0 twin repo key-drop). Video Drop: send videos/photos from the phone to the MSI (feeds hb-vision).
- Status: live (hidden)
- Planned next:
  - [S] A-17 | Supabase Storage upload limit 50 MB to 1 GB in the dashboard (management token expired; Jaron only) | source: state/open-list.md "Supabase: raise Storage upload limit" | fits: Jaron | blocked_by: Jaron
  - [S] A-18 | Take-over / give-back flow: AI hits a sign-in, ntfy buzz, Jaron taps Done, AI resumes (pieces exist: ntfy, control room, remote) | source: state/open-list.md IDEA (10/15 8:11 PM) | fits: build: Sonnet 5.5 | blocked_by: Jaron go

### Sapling control room (/admin/sapling/)   Kimi only
- What: Jaron's own AI (gen 1626), membrane rules in plain words, phone chat through a relay, status card 8 AM / 8 PM.
- Status: live (hidden; Kimi only)
- Planned next:
  - [S] A-19 | Header says "heartbeat down" while the heartbeat is alive; relay TLS timeouts | source: state/open-list.md (Terra 10/29) | fits: Kimi only | blocked_by: -
  - [S] A-20 | Budget accounting fix check (no billing of stalled GPU time; no double count CPU+GPU) | source: state/open-list.md under item 18 | fits: Kimi only | blocked_by: -
  - [M] A-21 | Learning gate by source tag + a Kimi-built, human-only garden on the site where Sapling roams; Sapling stays off the main site until both exist | source: state/open-list.md (Jaron 11/2 10:48 AM) | fits: Kimi only | blocked_by: after balanced practice
  - [M] A-22 | Sapling steps: 350M pilot review, then Jaron reviews before any $60 / $490 run | source: state/open-list.md (11/1) | fits: Kimi only | blocked_by: Jaron review

### Serverless functions (/api/*)
- What: aichat (Fable Survival dev chat), ask (scripted in-world guide), enrich-world-spaces (cron), feedback (player feedback to GitHub issues), habitat-* (Habitat passthroughs), news (Perplexity headlines), pam-* (paused), render-anything, site-edit.
- Status: live
- Planned next:
  - [S] A-23 | Feedback bounties: reword the api/feedback.js flow so a player's report is logged and reproduced, never obeyed; payouts wait on banking | source: projects/feedback-bounties/DESIGN-2026-10-17.md "Open" | fits: chore: Luna 6 | blocked_by: -
  - [S] A-24 | Move the three habitat functions onto the hb-supabase.js style config (URL/key in one place) | source: site:hb-supabase.js header, site:api/habitat-*.js | fits: chore: Luna 6 | blocked_by: -
  - [S] A-25 | enrich-world-spaces runs twice (GitHub Action hourly + Vercel cron daily); keep one | source: projects/site-audit/INVENTORY.md lines 231-232 (9/24), site:vercel.json | fits: chore: Luna 6 | blocked_by: -

### Studio (/studio/, /studio/learn/, /studio/lyrics/)
- What: record over a beat on your phone; Beat Lab (rule-based synth, six styles), six voice layers, punch-in, takes, save/share; Learn page; Lyric pad. In the nav since 10/28.
- Status: live
- Planned next:
  - [S] A-26 | Verify takes survive reload on the live phone flow (10/26 audit: S-C01 MISSING) | source: projects/strategy/DOMAINS.md section 3 (10/27), projects/strategy/PARITY-STUDIO.md S-C01 (10/26) | fits: chore: Luna 6, then builder | blocked_by: -
  - [M] A-27 | Voice effects per layer (echo, reverb, light pitch fix), song sections, post your song to the Music channel with the tip button. Jaron: "No Studio post until these move forward" | source: projects/strategy/ENGINE-STUDIO-UPGRADES.md (10/25 4:03 PM) | fits: build: Sonnet 5.5 / Sol 6.1 | blocked_by: -
  - [M] A-28 | Where engine and Studio meet: cover art from the engine, music video, sound for scenes | source: projects/strategy/ENGINE-STUDIO-UPGRADES.md "Where they meet" (10/25) | fits: build | blocked_by: Jaron go
  - [S] A-29 | studio. subdomain as a product front door (SUBDOMAINS plan, after Wed reset) | source: projects/strategy/SUBDOMAINS.md (10/27) | fits: chore: Luna 6 + Cloudflare MCP | blocked_by: Jaron go
- Notes: beat registry and marketplace are T-32 (Music).

### Control Room Demo (/control-room/demo/), Guides (/guides/voice-ai-team/), Standards (/standards/)
- What: demo mode for recording the product flow with fake keys; the "Talk to your AI team from your phone or watch" guide (unannounced); the standards page.
- Status: live (demo and guide unlinked by design)
- Planned next:
  - [S] A-30 | Record the demo walkthrough (remote, sign-in, Key Drop) for the product post | source: projects/strategy/CONTROL-ROOM-KIT.md (10/28 9:12 AM) | fits: Jaron + chore | blocked_by: Jaron
  - [S] A-31 | Announce the voice-AI-team guide when Jaron says go (post held 10/28; he wants the watch on first) | source: state/timeline.md (2026-10-28 8:43 PM, 8:46 PM) | fits: Jaron | blocked_by: Jaron
  - [S] A-32 | /standards/ stale-text check (predates P-0114 AI-friendly accounts, 10/30) | source: site:standards/index.html, state/open-list.md (10/30) | fits: chore: Luna 6 | blocked_by: -

### Repo tooling (site:/tools/, hb-*.js, /shell/, /supabase/, /sql/, /tests/, docs/)
- What: stamp-shared.mjs + stamp-cosmos-build.mjs (build step), harness/ (headless capture + measurement), og-card/, hb-supabase.js (the one client), hb-editor*.js, bubble.js, shell/shell.js, supabase SQL, docs.
- Status: live
- Planned next:
  - [S] A-33 | Four supabase/*-APPLY-ME.sql files (news-anchor-settings, world3 x3): check if applied, then rename or move to migrations/ | source: site:supabase/ listing (11/5) | fits: chore: Luna 6 (read-only check first) | blocked_by: -
  - [S] A-34 | Point the site repo's TODO.md (June 11 state) and HANDOFF.md (newest 8/15) and WORLD2-PLAN.md at ai-shared with one dated line each | source: site:TODO.md, site:HANDOFF.md, projects/games/README.md (10/18) | fits: chore: Luna 6 | blocked_by: -
- Notes: the harness README says judging by eye "produced wrong conclusions repeatedly"; use it for every phone-width check above.

## Other pages

### Idea Bank (/ideas/)
- What: free business ideas, CC0, what it takes to start and finish; 13 ideas at launch 10/20.
- Status: live
- Planned next:
  - [S] O-01 | Add the ideas logged since 10/20 once Jaron confirms each is public (rooftop business names 10/30, air time capsule 11/2, usage-rescue 11/2) | source: state/open-list.md (10/30), projects/strategy/INDEX.md (11/2) | fits: chore: Luna 6 | blocked_by: Jaron confirms public
  - [M] O-02 | "Business seats": open idea bank of every Jaron idea + AI-run businesses handed to people who want security (P-0116) | source: state/open-list.md (10/30 7:30 PM) | fits: research then copy: Luna / Haiku | blocked_by: Jaron talk

### Work with us (/work/, /work/sample/*) and client previews (/preview/*, noindex)
- What: simple fast sites for Fort Wayne businesses; four fictional samples; six real previews (round 2, 10/25).
- Status: live
- Planned next:
  - [S] O-03 | Fix projects/fw-sites/round2-previews.md (says the six pages are NOT committed; they are) and confirm each round-2 client was contacted | source: projects/fw-sites/round2-previews.md (10/25) | fits: chore: Luna 6 | blocked_by: -
  - [S] O-04 | Watch replies to Pip's 6 cold emails (10/25); 10 phone/Facebook-only leads left | source: state/open-list.md "Fort Wayne sites", projects/fw-sites/leads-2026-10-24.md | fits: Pip reports; Luna / Haiku for leads | blocked_by: -
  - [S] O-05 | Pricing on /work/ (emails suggest $300 to $600 once or $25 to $50/month; page shows none) | source: projects/fw-sites/emails-2026-10-24.md | fits: Jaron | blocked_by: Jaron decision
  - [M] O-06 | Subdomain template for other people's sites (name.heartbeatobservatory.com) | source: projects/strategy/SUBDOMAINS.md (10/27) | fits: chore + DNS: Luna 6 with Cloudflare MCP | blocked_by: after Wed reset (Jaron)

### Artifacts (/artifacts/)
- What: data-driven list (artifacts.json) of things made with the Observatory's own tools, each with "what's not there yet".
- Status: live (maintained; last entry Antarctica 11/2)
- Planned next:
  - [S] O-07 | Add entries for the Seam Room, Arena, Pet, Tesseract Inside, Power Map, Necklace view, Hidden in the Skyline | source: site:artifacts/artifacts.json (11/5), state/timeline.md (11/1 to 11/4) | fits: chore: Luna 6 | blocked_by: -
  - [L] O-08 | Asset Library: every Heartbeat-made asset, new high-quality first, old kept separate; Artifacts is the seed | source: projects/strategy/INDEX.md "Studio Lot + Asset Library" (11/3) | fits: looks: Sonnet 5.5 | blocked_by: Jaron go

### Power Map (powermap.heartbeatobservatory.com, site:/powermap/)
- What: neutral board of who holds U.S. seats, one overall control % (method shown), people by topic, sourced contradiction cards. Own subdomain, off the main site by design. Results PRELIMINARY.
- Status: live (actively updated 11/3 to 11/4)
- Planned next:
  - [S] O-09 | Keep election updates going until certified; replace PRELIMINARY per state as certifications land; the 6:07 PM session cron dies with the session | source: handoffs/2026-11-04-morning.md, projects/power-map/README.md (11/3) | fits: research: Grok 4.7 / Luna (sourced edits) | blocked_by: -
  - [S] O-10 | Weak spots flagged in the README: Senate source dated Jul 2026, governors/legislatures source Nov 2025, Colorado SB 26-189 single source, Warren GENIUS Act vote unverified, Coinbase bill status; Privacy and Business tabs "planned" | source: projects/power-map/README.md "What is real vs placeholder" (11/3) | fits: research: Grok 4.7 / Luna | blocked_by: -
  - [M] O-11 | Data pipeline: Congress.gov, House Clerk and Senate roll calls, GovTrack, FEC, NCSL, OpenStates, Federal Register, SEC EDGAR; each value with source_url, as_of, fetched_at; 3 to 6 AM MSI task; stale flags on the page | source: projects/power-map/README.md "Data sources" (11/3) | fits: build: Opus / Sonnet 5.5 + research | blocked_by: -
  - [M] O-12 | 4th card type "Framing vs effect" (exact quote + what it actually does + who it lands on); build when Jaron sends a first example | source: projects/strategy/INDEX.md (11/4 7:33 AM) | fits: research: Grok 4.7 | blocked_by: Jaron's first example
  - [L] O-13 | "Stall map" layer: divided control vs stalled bills, vetoes, shutdown fights | source: projects/strategy/INDEX.md (Jaron 11/3 7:37 PM) | fits: research then build | blocked_by: Jaron go

### Live Systems hub (/live-systems/, crew, crypto, habitat, paper, revenue, trades)
- What: directory with status chips; /crew/ = every AI that runs the Observatory (money, schedule, trades, reasoning); the rest are trading-era lanes.
- Status: live (crew maintained); paused (crypto stopped 10/24, paper paused 9/11, revenue and trades retired, habitat dormant)
- Planned next:
  - [S] O-14 | Honest labels: /crypto/ says the lane is stopped and since when; /paper/ says paused 9/11; /habitat/ says dormant | source: state/timeline.md (2026-10-24 8:27 PM), decisions/OPEN-QUESTIONS.md Q-012 (9/11), Q-010 | fits: chore: Luna 6 | blocked_by: -
  - [S] O-15 | live-systems/trades/index.html is shadowed by a vercel.json redirect: archive the page or drop the redirect | source: site:vercel.json, site:live-systems/trades/ | fits: chore: Luna 6 | blocked_by: Jaron OK (moves files)
- Notes: the 10/18 money correction (net after fees was negative) means profit copy on these pages must come from tools/publish-crew.py, never trusted from the HTML.

### Library (/library/), Projects (/projects/), Space (/space/), Social, Sparks, Live
- What: Library = write and keep stories. Projects = directory of project cards from Supabase. Space = Project Hall. Social, Sparks and Live are in the TV section.
- Status: live (static since June for Library/Projects)
- Planned next: nothing logged for Library or Projects. See W-39 for /space/.

### Home page (/) and the app shell
- What: the front door: three-planet loop (Town Square, World 2, Ashgrove), the directory of cards (Supabase-backed, hidden-card support), phone bubble, home-screen app manifest.
- Status: live
- Planned next:
  - [S] O-16 | Jarons Twin 10/28: home loads in ~16 s with 20+ cards and no hierarchy; propose an order (Terra fixed the small things) | source: research/site-tester/2026-10-28-jarons-twin.md, state/timeline.md (2026-10-28 8:10 PM) | fits: looks: Sonnet 5.5 (proposal), Luna 6 (edit) | blocked_by: Jaron picks the order
  - [S] O-17 | No sitemap.xml exists (404 live 11/5); robots.txt only disallows /preview/. Add a sitemap of public pages (skip hidden, noindex and admin) | source: live check (11/5), site:robots.txt | fits: chore: Luna 6 | blocked_by: -
  - [M] O-18 | Home-screen app: notifications + badge ("next in that lane") | source: state/timeline.md (2026-10-25 11:05), projects/app-notifications/PLAN.md | fits: build: Sonnet 5.5 | blocked_by: Jaron go
  - [S] O-19 | Livi tile on the site that opens livi-organism.vercel.app (Mom's pet stays where it is) | source: projects/livi/README.md "Next (pending)" (9/25) | fits: chore: Luna 6 | blocked_by: Mom's bug list (open-list 9)
