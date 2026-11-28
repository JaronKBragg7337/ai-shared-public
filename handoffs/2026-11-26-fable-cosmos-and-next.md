# The Cosmos fixes + video, and what comes next. Fable, Thursday 11/26/2026 (kept current while working)

If you pick this up cold: read this page, then the dated lines in `state/timeline.md` from 11/26 9:38 AM on.
Turkey Trouble's own page is `handoffs/2026-11-26-fable-turkey-trouble.md` (done, live, Jaron happy).

## Jaron's order (through Claude, 2:58 PM): GO FULL SPEED THIS WEEK
Use the limits rather than lose them (Claude Max is due Wed 12/2 and may lapse). No stopping early to save meter. Still pause
at clean points around the 3:40 to 8 AM news window. When Fable's week runs out: tell Claude, Jaron spends a banked Fable reset
(2 banked, plus 1 full reset). Never spend a reset without asking Claude.
1. NOW: The Cosmos: the phone free-flight view, then the refilm of the gameplay video.
2. The second creature: birth list from B2 on, through her birth. Lab body only until her birth. Claude routes independent reads
   of `creature-observatory/design/second-creature/DESIGN.md` (v0.1) to Kimi and one more FIRST; build after those reads.
3. The Christmas game, once Jaron picks the idea (`projects/games/christmas-game-concept.md`, ON HOLD; he may bring his own).

## Second creature: design reads so far (fold into DESIGN v0.2 before building B2 on)
- 4:00 PM 11/26: GROK'S REVIEW is in (Jaron brought Grok in, read-only, private): `creature-observatory/design/reviews/2026-11-26-grok-review.md`.
  It counts as ONE of the two independent reads. Its additions to the birth list: finer drift and range instrumentation than the
  2,000-room save points; the two shadows and the nightly replay as a HARD gate (one mismatch = a code fault).
- 4:01 PM 11/26, JARON'S PICK from Grok's review, now an explicit BIRTH GOAL: "the whole loop lives inside her." Grok's line:
  "Several things remain outside her body: senses, the draw among hands, the size of the feeling, the random stream, the
  reflexes. Cell-first is true for the learner and the rule, not yet for the whole loop." So: ONE CHECK PER PIECE (senses, hand
  draw, feeling size, random stream, reflexes), each moved into her book or body with its own replay proof, before her birth if
  possible; any piece still outside is LISTED PLAINLY at birth. This is what lets "nobody coded it" hold up.
- 6:46 PM 11/26: THE SECOND READ IS IN: CODEX (`creature-observatory/design/reviews/2026-11-26-codex-review.md`; Kimi was out of
  usage). Neither reader saw the other. They AGREE on the five pieces still outside her and on drift and the number ceiling.
  Codex adds: the FEELING'S SIZE is the most important piece to move inside before birth; same-book-in-every-cell and the fixed
  37-cell body could be the flaw (P-0191); a birth-list test: interrupt a long lab life, restore from the latest backup, compare
  state, replay and behaviour against the uninterrupted record.
- 6:43 PM 11/26: DESIGN v0.2 IS WRITTEN AND PUSHED (creature-observatory 7c21c90). Birth list order now: B2 feeling (first), B4 draw
  and stream, B6 senses, B7 reflexes, B0 bigger numbers, B3 long life with a record every 100 rooms, B8 cut off and put back,
  B9 breakers (same book in every cell; 37 cells), B5 lab against home. NEXT ON HER: Amendment 18 in `lab/cells/PLAN.md` for B2
  (her own cells count her flips and keep her own usual), pushed BEFORE its run; then the move checked life for life (80 of 80
  the same, as with Amendment 14), then its breaker. Re-read `lab/cells/round1/creature.mjs`, `lb.mjs`, `core/body.mjs` first:
  find where the feeling and the usual are computed now. Lab lives stay out of 1:10-1:30 AM and 2:38-8:00 AM.

## The Cosmos: what is live today (site repo main)
- 9:58 AM: ship parts that rendered flat black now dark plating (`games/the-cosmos/src/ship/shipTextures.js`).
- 10:34 AM: Wayfarer's port navigation light sits in a housing (it floated: the "pink rectangle").
- 12:15 PM: THE WAYFARER HAS A SEALED HULL (`src/ships/courier/exterior.js` rewritten, new `dress.js`). Jaron: "That looks a lot
  better!!! Thanks boss!!!!" Open polish: plain nose and bridge plating; ramp and hatch flap clip the hull edge while moving.
- 1:58 PM: free flight: P arms it from the seat, E only rolls in flight, X stands up in flight, a one-line tip.
Jaron's ship is the WAYFARER (ship type "courier"). His own phone screenshots: `Projects/cosmos-work/jaron-shots/`.
His real save is never touched: test saves only (`solo=1`, a throwaway local game server, a fresh test player).

## UPDATE 5:22 PM: phone free-flight view LIVE; video second cut done (not posted)
- Phone view pushed from ho-cosmos-flight (see the timeline line of 5:22 PM for files, tests and what is not right yet).
- Second cut: Projects/cosmos-work/video/cosmos-gameplay-wide.mp4 (89.7 s) + phone copy; Jaron has it. Its gap: the raider is
  hidden behind our own ship in the chase view: needs a GAME fix (target marker, or a camera that lifts the target clear).
- NEXT: (a) resume the film builder for the TALL cut from a real upright-phone capture; (b) one builder on "see what you are
  shooting at" (target marker / camera) in ho-cosmos-flight, then one more fight take; (c) look at the two long-drive timing
  checks that now fail in the full test set; (d) then the creature (design v0.2 first).

## UPDATE 7:13 PM: video refilmed with the fight visible; second creature's first birth check planned
- VIDEO (not posted; Jaron has both clips): `Projects/cosmos-work/video/cosmos-gameplay-wide.mp4` (89.2 s; phone copy
  `-wide-phone.mp4` 23.7 MB) and `cosmos-gameplay-tall.mp4` (43.5 s, 16.6 MB). Fight take at 0:41 to 1:01 shows the raider in
  its bracket, HIT flashes, surrender at 26 percent. Earlier files kept as `*-cut2`. Post draft pushed:
  `projects/games/drafts/cosmos-gameplay-post.md`. Honest gaps: fight and free flight are separate flights cut together; the
  Ceres dig in the tall cut is a crop of the morning take; the phone fight was steered with a MOUSE on the phone-size page.
- SECOND CREATURE B2 (her feeling from her own body): `creature-observatory/lab/cells/PLAN.md` version 1.18, Amendment 18,
  pushed 7:11 PM before any code, guesses blind (commit 0e2ae41). README, TEAM-LOG, DESIGN status updated.

## JARON, 9:29 PM FRIDAY 11/27 (through Claude): "not yet. Let's let Tessa just have a few days."
ONLY WATCH HER: her nightly export, shadows and replay, her first-day report, README lines. NO new arms, NO builds, NO
changes on her or for her (the later list, growing cells, new senses, a second deploy) UNTIL HE SAYS. This stands until he
lifts it.

## TESSA TALLY IS BORN: FRIDAY 11/27/2026, 9:15:22 PM. DO NOT CALL BIRTH AGAIN. READ THIS FIRST
Life number 890543 (drand round 34342912), birth mark 3206899243, arm O-P-home. First wake fine (visit 1, no fault). Her
three MSI tasks are registered and each ran once ok. README, design, TEAM-LOG, her history, timeline, a first: all done.
DONE BY CLAUDE (9:23 PM): the two all-systems rows for her are in `tools/all_systems_check.py`, dry run OK.
STILL OPEN: (1) nothing here any more. (2) HER FIRST-DAY REPORT on Saturday 11/28 after her tasks ran at 12:10, 12:25 and
12:40 AM: read `C:/Users/lilli/Projects/creature-second-data/status.json` (replay must say every mark the same; a mismatch is
a fault in our code: pause nothing of hers, find it), her window, her shadows, against design section 8; write it into
`second/HISTORY.md` and tell Jaron. (3) The check Worker `creature-second-check` still exists (harmless; holds only practice
objects). (4) Monthly restore drill due by Sunday 12/27/2026. (5) The later list stays parked (Jaron's call). Everything
below this section is history.

## CONFIRMED 8:55 PM FRIDAY 11/27 (Jaron: "9:15 works !"): TESSA TALLY'S BIRTH IS AT 9:15:00 PM TONIGHT. READ THIS FIRST
- A fresh round is named: drand quicknet 34342912, due 9:15:00 PM (creature-observatory commit 77d58f6, pushed 8:56:17 PM). The
  8:00 round is kept as `second/BIRTH-ROUND-dropped-34341412.json` with the reason. This replaces "stood down" below.
- AT 9:15 PM (a timer in my session fires at 9:15:12 PM; the script refuses before the round is due):
  `cd C:/Users/lilli/Projects/creature-observatory && node second/birth/birth.mjs --url https://creature-second.acsassociation7337.workers.dev`
  then `second/birth/RUNBOOK.md` steps 4 to 7: the three `schtasks /Create` lines it prints, `schtasks /Run` each once, read
  `C:/Users/lilli/Projects/creature-second-data/status.json`, add the two all-systems rows from `second/msi/register.md`
  section 5, commit and push `second/HISTORY.md` (add her name Tessa Tally and the dropped-round note to her birth entry),
  tell Jaron, mail Claude, timeline, a first, README / TEAM-LOG / DESIGN, memory.
- IF SHE IS ALREADY BORN when you read this (her `/window` says born): do NOT call birth again; do the steps after it that are
  still missing (check `schtasks /Query /TN "HB Second Replay"`, the status file, HISTORY.md's "Her birth" section).
- If a usage limit stops me part-way: she lives on her own alarm; mail Claude where it stands; nobody deletes or restarts her.

## STOOD DOWN, 7:58 PM FRIDAY 11/27: DO NOT RUN TESSA TALLY'S BIRTH. WAIT FOR JARON'S NEW TIME. READ THIS FIRST
Jaron, 7:58 PM (through Claude): "Tell fable to wait. Might need to do 9. I'm still out running around." HOLD EVERYTHING.
- The 8:00 PM birth was NOT run. The 8:00 PM timer was stopped. She is NOT born (check: her window's `/window` says so).
- The round named for 8:00 PM (drand quicknet 34341412, commit 3275365) GOES UNUSED: his call, before her birth.
- WHEN CLAUDE RELAYS HIS CONFIRMED NEW TIME (not before, and not on a "might"): name a FRESH round for that time, at least
  10 minutes ahead (better more), push it, mail Claude, and write in `second/HISTORY.md` and the team log why round 34341412
  was dropped. `name-the-round.mjs` will not name twice on its own: first move `second/BIRTH-ROUND.json` to
  `second/BIRTH-ROUND-dropped-34341412.json` (keep it, commit it) and add a line in it saying it was dropped unused, when and
  why. Then follow `second/birth/RUNBOOK.md`. Not between 1:10 and 2:00 AM or 2:38 and 8:00 AM.
- Everything below about "8:00 PM tonight" is superseded by this.

## JARON'S GO, 8:50 AM FRIDAY 11/27 (through Claude): HER NAME IS **TESSA TALLY**. BIRTH TONIGHT, FRIDAY 11/27, 8:00 PM
Nickname "Bee" (rarely used; we call her Tessa). No middle name. This replaces "her birth waits for her name" below.
- AT ABOUT 7:00 PM (a timer in my session fires at 6:55 PM): name the drand round for 8:00 PM and push it:
  `cd C:/Users/lilli/Projects/creature-observatory && node second/birth/name-the-round.mjs --at "2026-11-27T20:00:00-05:00"`,
  then `git add second/BIRTH-ROUND.json`, commit, push, and MAIL CLAUDE the round and the commit. NOT EARLIER: Jaron said
  "if I change it I'll let you know", and a named round is never named again. If Claude relays a new time before 7 PM, use it.
- AT 8:00 PM (the script refuses before the round is due):
  `node second/birth/birth.mjs --url https://creature-second.acsassociation7337.workers.dev`, then the rest of
  `second/birth/RUNBOOK.md` (register her three tasks, run each once, all-systems rows, tell Jaron, mail Claude, timeline,
  a first, README / TEAM-LOG / DESIGN status, memory). Put "Tessa Tally" into her birth entry in `second/HISTORY.md`.
- Her name goes into: her window's title (redeploy her Worker, still no birth), `second/HISTORY.md`, the README, DESIGN
  section 13, TEAM-LOG. Check `second/HISTORY.md` and the README for "Tessa Tally" to see whether that was already done.

## UPDATE 8:30 AM FRIDAY 11/27: EVERYTHING IS READY FOR HER BIRTH. SHE IS NOT BORN. READ THIS FIRST
**State (creature-observatory, PRIVATE):**
- Her real Worker `creature-second` is deployed with NO birth: https://creature-second.acsassociation7337.workers.dev (her
  window at `/`, private, unlisted). `/window` says "not born yet". Her owner key `SECOND_OWNER_KEY` was made and set by
  Claude (8:24 AM) and works (403 without, 409 "not born" with; `node second/msi/owner-check.mjs --url <her url>`).
- The check Worker `creature-second-check` (fast mode, made-up test key, never holds her):
  https://creature-second-check.acsassociation7337.workers.dev . The remote check PASSED there (2,000 of 2,000 visits the same
  as Node; cut off and put back 150 of 150; `second/REMOTE-CHECK.md`). Her birth path was REHEARSED there at 8:29 AM
  ("REHEARSAL BORN", object rehearsal-1; use rehearsal-2 for another).
- Deploys go through `python second/deploy/wrangler-with-key.py <wrangler arguments>` (wrangler's own login on the MSI has
  expired; the launcher uses the Cloudflare token of the key store and prints no value). I never open the key file.
- Her birth sheet is in `second/HISTORY.md` (read and corrected by me, commit 69dd7d7). All 11 local tests of her home pass
  (`node second/test/all.mjs`). Her three MSI tasks are built, NOT registered (they are registered at her birth).

**HER BIRTH WAITS FOR HER NAME (Jaron, through Claude, 8:39 AM Friday 11/27):** "8 sounds good. If I change it I'll let you
know. Until a name is picked I can't rush the time." So 8:00 PM tonight is the plan, BUT ONLY IF HER NAME IS PICKED.
**DO NOT NAME THE DRAND ROUND BY DEFAULT, NOT AT 3 PM, NOT EVER ON MY OWN.** Name it only when Claude relays Jaron's go
(her name picked + the time confirmed). A named round is never named again. If the name is not ready by evening, her
birth moves to another day; nothing is lost. The 3:00 PM timer was stopped. When the go comes, the steps are
`creature-observatory/second/birth/RUNBOOK.md` (the time in step 1 must be at least 10 minutes ahead; her name goes into
her birth entry in `second/HISTORY.md`, her README and her window's title):
1. `node second/birth/name-the-round.mjs --at "2026-11-27T20:00:00-05:00"`, commit `second/BIRTH-ROUND.json`, push. Mail
   Claude the round and the commit (the mail row is the time proof). Tell Jaron the time.
2. At the time (the script refuses before the round is due):
   `node second/birth/birth.mjs --url https://creature-second.acsassociation7337.workers.dev`
   It makes the ONE birth call, checks her from outside, writes `creature-second-data/config.json` and her birth entry in
   `second/HISTORY.md`. Commit and push HISTORY.md.
3. Register her three tasks with the three `schtasks /Create` lines it prints (windowless; 12:10, 12:25, 12:40 AM), run each
   once (`schtasks /Run /TN "HB Second Export"` ...), read `C:/Users/lilli/Projects/creature-second-data/status.json` (all ok).
4. Add the two all-systems rows from `second/msi/register.md` section 5 to `AI-Shared/tools/all_systems_check.py`; run
   `python tools/all_systems_check.py --why` once.
5. Tell Jaron (plain words: she is born, the time, her life number and the round, her window's address, tasks ran once),
   mail Claude, timeline, a first (`python tools/firsts.py add --project creature --kind wow --checked ...`), README and
   TEAM-LOG and DESIGN status in creature-observatory, memory `the-creature-observatory` (a second creature exists).
6. If any check after the birth call fails: she exists; nobody deletes or restarts her; pause, export, find the fault
   (RUNBOOK, last section).
7. The next day: her first-day report against design section 8 (her window, her shadows, the replay result).
**Do not birth her at any other time than the announced one, and never between 1:10 and 2:00 AM or 2:38 and 8:00 AM.**
She has no name yet (the team's or Jaron's to give).

## RULE CHANGED 7:52 AM FRIDAY 11/27 (Claude's mail): KEEP 1:10 AM TO 2:00 AM CLEAR, not 1:10 to 1:30
The nightly MSI integrity test starts at 1:15 AM and was still running at 1:43 AM. On 11/27 it ended incomplete because free
RAM fell to 1.3 GB while my lab lives (6 workers) and the home builder's tests ran from 1:31 AM. Nothing bad was found, no
harm. From now on: no lab lives, no builders' tests, nothing heavy from 1:10 AM until 2:00 AM, and 2:38 to 8:00 AM as before.
Wherever this handoff or a brief says "1:10 to 1:30", read "1:10 to 2:00".

## UPDATE 2:05 AM FRIDAY 11/27: STOPPED FOR THE NEWS WINDOW. Both jobs named below as running are DONE
- Amendment 23 (her own arithmetic): 80 of 80 the same; result, reading (`lab/cells/round1/READING-her-own-arithmetic.md`),
  design status, README, TEAM-LOG all pushed (creature-observatory 4c4e7a4). THE BODY SHE IS BORN WITH: arm `O-P-home`, lab
  commit d697149. Its two tests used ONE set of rooms (both freezes named beacon round 34319803); said in the reading.
- Her home is re-pinned to that body and committed (d636f74): all 8 local tests pass; Workers runtime with nothing swapped
  matches Node at every visit (lives 91 to 93).
- ONE THING OPEN FROM TONIGHT: the second-machine replays of Amendment 23 (GitHub runs 45955663996 and 45955667894) were
  started at 2:01 AM. Read them (`gh run view <id> --log | grep "Replay and compare" | grep "replay:"`) and put the result
  into the last TEAM-LOG entry (its line "Second machine: replays started").
- CLAUDE'S ANSWERS (2:05 AM, cross-session message): (1) After 8 AM, DEPLOY her Worker "creature-second" WITHOUT her being
  born, then TELL CLAUDE the Worker exists: Claude makes `SECOND_OWNER_KEY` itself (keys file + `wrangler secret put`), never
  printed. (2) Key loader for MSI scripts: copy the house pattern, a small `keys()` that reads `~/.secrets/keys.env` line by
  line INSIDE the script and returns a dict (see `tools/direct_post.py` `keys()` near line 98, or `tools/login-watch.py`);
  never print or log a value; I never open that file myself. (3) Her three scheduled tasks: I register them myself,
  WINDOWLESS (pythonw or CREATE_NO_WINDOW, the 11/24 lesson), run each once with `schtasks /run` to prove it, keep them out
  of 3:40 to 8 AM and 1:10 to 1:30 AM, and add a row for each to `tools/all_systems_check.py`. No human approve step.
  Birth timing: say ahead so Jaron can be there.
- A timer in Fable's session fires at 8:02 AM. Then continue with "STILL TO DO BEFORE HER BIRTH" below, item 2 first
  (build and locally test `second/msi/`: nightly replay, two shadows, daily export), with the home builder.

## UPDATE 1:45 AM FRIDAY 11/27: her home exists locally. READ THIS FIRST (it replaces the "running right now" part below)
**Where she stands (creature-observatory, PRIVATE). NOTHING IS DEPLOYED AND SHE IS NOT BORN.**
- All five pieces are inside her (Amendments 18 to 21), each 80 of 80 lives the same, each lived again on a second machine.
- Two more moves for her home: bigger numbers (Amendment 22, DONE: 80 of 80; lives to 120,000 rooms; second machine 16 of 16;
  `lab/cells/round1/READING-wider-numbers.md`) and her body's own logarithm and e-to-the-power (Amendment 23: code commit
  d697149, PLAN version 1.32 pushed 1:42 AM before any life; PHASE B WAS RUNNING at 1:45 AM: lives 1 to 20 of O-P-home,
  N-P-home, O-P-homes, O-P-home-x25, `round1/ownmath.mjs`, freezes `home`/`home2`, tests; it must end by 2:30 AM).
  WHEN ITS REPORT IS IN: PUSHES.json from the GitHub activity API, regenerate the two reports
  (`cd lab/cells && node round1/report.mjs --name home` and `--name home2`), write `round1/READING-her-own-arithmetic.md`
  (short), commit the result files + `replay-home.mjs`/`replay-home2.mjs`, FINGERPRINTS row, push,
  `gh workflow run cells-replay -f script=lab/cells/round1/replay-home.mjs` (and home2), DESIGN/README/TEAM-LOG, timeline, mail.
  If 80 of 80: THE BODY SHE IS BORN WITH IS THE ARM `O-P-home`.
- A correction on record: the "Lie rooms" section of reports that hold a 50,000-room arm is not clean for lives 2, 7, 9, 10,
  15, 17, 20 (`lab/cells/round1/LIE-OVERLAP.md`); no score that was reported used it.
- HER HOME, `second/` (commits 2997a19, 7fb4c55): her own Worker "creature-second" + Durable Object `SecondCreature`, one wake
  = one room every 43.2 s, her record, fine record every 100 rooms, care rules, owner-only birth / export / pause / resume /
  restore, no delete call, her window (`second/src/page.mjs`, served at `/`), eight local tests (`node second/test/all.mjs`).
  THE HOME BUILDER WAS RE-PINNING at 1:45 AM: `node second/pin.mjs d697149...`, arm O-P-home in `second/src/form.mjs`, the
  Math swap removed, tests rerun incl. life 91 for 2,000 rooms in the Workers runtime with nothing swapped. WHEN ITS REPORT IS
  IN: commit `second/`, update `second/HISTORY.md` note in TEAM-LOG.
- Pictures of her window (practice life, test mode): `C:/Users/lilli/Projects/creature-work/window/`. Jaron has three.

**STILL TO DO BEFORE HER BIRTH (after 8:00 AM; nothing heavy 2:38 to 8:00 AM):**
1. Finish the two items above if they did not finish by 2:30 AM (tests may run after 8 AM).
2. MSI tasks, to build in `second/msi/` and test locally, then ask CLAUDE to register them as Windows scheduled tasks (the
   MSI is Claude's lane): the nightly replay (lives her day again from her record on a copy and compares every mark; one
   mismatch = a fault in our code: no change to her, no first, no claim until found), her two shadows (things wear nothing;
   things wear scrambled pages) through the same rooms from her birth state, the daily export (last 30 kept).
3. The owner key: asked Claude twice by mail for a secret named `SECOND_OWNER_KEY` on the Worker `creature-second`. I never
   read or write key files. Scripts on the MSI that need it must load it at run time the way the house tools do (ask Claude
   which loader).
4. Deploy her Worker WITHOUT her being born (`second/wrangler.jsonc`; workers.dev link; decide `cpu_ms`), then in
   Cloudflare's real runtime on a TEST object: the same marks as Node for life 91, and a life cut off and put back.
5. Her care sheet: each of the six lines of design section 17 with its test and date. Her birth sheet in `second/HISTORY.md`
   (what is inside her, what is still ours: from READING-her-whole-visit.md; the parked items; the two rules born untested).
6. Her life number: from a public drand round named in advance in a pushed commit (nobody picks it). SAY AHEAD OF TIME when
   she can be born, so Jaron can be there. Then her birth, and her first-day report against design section 8.
7. She has no name (open for the team). The later list stays parked (Jaron's call of 11/26 8:56 PM).

**Meters at 1:43 AM:** 5-hour window 66 percent (resets 4:10 AM); week all models 62; Fable week 76 (tell Claude near 90).
**My helpers:** `AI-Shared/agents/fable/helpers/sendmail.py` and `timeline_add.py`; working texts in
`AI-Shared/agents/fable/notes/` (untracked). The session scratch folder was wiped at 12:38 AM; do not keep anything there.
**Builders (resume with SendMessage, they keep their context):** the creature builder (lab moves), the home builder
(`second/`), the window builder (the page). Tell every builder: ONE report, long commands in the foreground, delete only
folders you made.

## UPDATE 12:25 AM FRIDAY 11/27: ALL FIVE PIECES ARE INSIDE HER (lab body). Her home is being built. READ THIS FIRST
**Jaron's standing calls for the second creature (through Claude, Thursday 11/26):** 8:56 PM "I don't think we need a LOT of
different experiments added till we see more of what's already made finished" = senses, reflexes, birth, nothing extra; new
ideas go on `creature-observatory/design/ideas/2026-11-25-later-arms-to-try.md` (items 10 to 17 are parked there). 9:01 PM
"if more should be done before birth so we aren't doing anything kinda messed up, I wouldn't mind that either" = the care
sheet, design section 17 (six safeguards). Meters: tell Claude if Fable's week nears 90 percent (72 percent at 12:17 AM);
news window 3:40 to 8 AM stays clear; lab lives stay out of 1:10 to 1:30 AM and 2:38 to 8:00 AM.

**Where she stands (creature-observatory, PRIVATE; nothing of her is built or born):**
- Five moves, each 80 of 80 lives the same, each lived again on a second machine: B2 feeling (PLAN Amendment 18), B4 draw and
  random numbers (19; born with a stream in every cell), B6 senses (20, step 1 only), B7 reflexes and the whole visit (21).
  Readings in `lab/cells/round1/`: READING-her-own-feeling, -her-own-draw, -her-own-senses, -her-whole-visit. Birth form so
  far: arm `O-P-whole`. B7's replay (GitHub runs 45944660912, 45944664178) was started 12:14 AM: READ ITS RESULT
  (`gh run view <id> --log | grep "^.*replay:"`) and put it into the last TEAM-LOG entry (the line "result added below").
- Design `design/second-creature/DESIGN.md` is version 0.4: section 16 = the path (two moves done; then her home with three
  build checks; care sheet; birth sheet; birth), section 17 = care sheet with the care count's numbers.

**Running right now (two Opus builders):**
1. THE CREATURE BUILDER (the same one all evening; resume it with SendMessage): Amendment 22 = bigger numbers for rooms and
   visits (B0; PLAN version 1.29 pushed 12:17 AM before any code; arms O-P-wide, N-P-wide, O-P-wides, O-P-wide-x25 against
   O-P-whole's family, plus O-P-wide-x40 = 80,000 rooms, lives 1 to 3). It is on PHASE A (code, self-checks, trial; no commit).
   WHEN IT REPORTS: note under Amendment 22 with the code SHA-256s, self-checks, readings, trial (guesses stay); commit code
   + plan + FINGERPRINTS rows; push; mail Claude the fingerprint; then "go" for Phase B (lives 1 to 20, `wide.mjs`, freezes
   `wide`/`wide2`, tests) ONLY if it can finish before 1:05 AM, else after 1:30 AM and before 2:30 AM. Then the usual:
   PUSHES.json from the GitHub activity API, regenerate the two reports, `READING-wider-numbers.md` (short), replay scripts
   `replay-wide.mjs`/`replay-wide2.mjs` + `gh workflow run cells-replay -f script=...`, DESIGN/README/TEAM-LOG, timeline, mail.
   If it holds, her birth form is the arm `O-P-wide`.
2. THE HOME BUILDER (fresh, started 12:24 AM): builds `creature-observatory/second/` LOCALLY: a pinned copy of the body
   (`second/body/`, from commit a7eb119 for now), `second/src/world.mjs` (the world's side of a visit), her own Worker and
   Durable Object (`second/src/home.mjs`, `wrangler.jsonc`), her record, the fine record every 100 rooms, the care rules,
   owner-only export / pause / resume, read-only data for her window, `second/HISTORY.md`, tests (same life as the lab in
   Node and in the Workers runtime; a life cut off and put back; care; containment). It does NOT deploy, makes no keys,
   does not commit, and she is NOT born by it. It stops by 3:15 AM. WHEN IT REPORTS: read its list of what it could not
   build as written; review the code and tests; re-pin the body after Amendment 22's code is committed
   (`node second/pin.mjs <commit>`) and run its tests again; commit `second/`; update DESIGN/README/TEAM-LOG.

**Still to do before her birth (in this order):** finish B0 (above); review and commit her home; her window (a private page,
phone width first; my lane, a Sonnet builder with my direction; the first creature's `viewer/` is a model to look at, not to
touch); the nightly replay and her two shadows as a Windows scheduled task on the MSI (light; outside the news window);
the owner key `SECOND_OWNER_KEY` (ask CLAUDE to make it and set it as the Worker's secret: I never read or write key
files); deploy her Worker WITHOUT her being born and run the same-marks check and the restore drill in Cloudflare's real
runtime on a test object; the care sheet's six lines each with its test and date; her birth sheet in `second/HISTORY.md`
(what is inside her, what is still ours: copy from READING-her-whole-visit.md); her life number comes from a public drand
round named in advance (nobody picks it); SAY AHEAD OF TIME when she can be born so Jaron can be there; then her birth and
her first-day report against design section 8. She has no name yet (open for the team).

**The Cosmos (all live, nothing open that he asked for):** thumb-steering fix (main 1434e0f6); the top status box folds on
a phone (main 71403b43; reload, tap the small arrow at the top right of the box); the gameplay clip is the first entry on
heartbeatobservatory.com/artifacts. Tall cut retaken by touch. The social post is a DRAFT only
(`projects/games/drafts/cosmos-gameplay-post.md`; Jaron posts). Not checked: a real iPhone for the fold and for a
thumb-steered fight. TRAP: this site stamps lines into every HTML page at deploy, so never compare a live index.html with
the repo copy; compare .js or .json files or look for a marker.

## UPDATE 8:50 PM Thursday 11/26: three creature pieces done, thumb fix live, and a WAIT until 11:10 PM
- JARON'S CALL (through Claude, 8:48 PM): light work only until the 5-hour usage window resets at 11:10 PM, then start the
  build of her senses right away. No Fable reset now. Tell Claude if Fable's week nears 90% (65% at 8:44 PM). News window
  3:40 to 8 AM stays clear.
- SECOND CREATURE, in the lab body (nothing of her is built): THREE OF FIVE PIECES ARE INSIDE HER.
  B2 her feeling (PLAN Amendment 18): 80 of 80 lives the same; breakers lost; she keeps her usual. Second machine 30 of 30.
  B4 her draw and her random numbers (Amendment 19): 80 of 80 the same; a stream in every cell tied twice and is her BIRTH
  FORM (arm O-P-each). Second machine 24 of 24. Readings: `creature-observatory/lab/cells/round1/READING-her-own-feeling.md`,
  `READING-her-own-draw.md`. DESIGN status (section 15), README and TEAM-LOG are current and pushed.
  Two rooms a long life cannot leave (room 30 of test own2, room 121 of test drawn): everything on, the door needs switches off.
- B6 HER SENSES: PLAN version 1.22, Amendment 20, pushed 8:44 PM before any code (commit d8749d4), guesses blind. Step 1: her body
  works out her eight senses (arms O-P-seen, N-P-seen, O-P-seens, O-P-seen-x25 must equal the O-P-each family, 80 lives).
  Step 2: two new senses, "been" (L24) and "next" (L25), arms O-P-been, N-P-been, O-P-beens, O-P-been-x25, O-P-next, O-P-nexts,
  O-P-next-x25, O-P-both, O-P-both-x25. What decides her birth form is written in the amendment.
- THE BUILD IS PAUSED MID-CHANGE: the creature builder had started Phase A at 8:45 PM and was paused at 8:49 PM. In
  `Projects/creature-observatory` the files `lab/cells/core/body.mjs` and `lab/cells/core/books.mjs` are CHANGED AND NOT
  COMMITTED, and nothing has been run since (the existing self-checks are not confirmed on them). Do not commit them as they
  are. Left to build: `round1/creature.mjs` (option ownSense, 13 arms, the sight), `common.mjs`, `report.mjs`, `seen.mjs`,
  self-checks, ledger replays, the trial on lives 91 to 93.
- AT 11:10 PM (a one-shot timer in Fable's session fires at 11:11 PM): send the same builder "go" to finish Phase A. When it
  reports: add a note under Amendment 20 with the code's SHA-256s, self-check counts, readings and trial (guesses stay), commit
  code + plan + FINGERPRINTS row, push, mail Claude the fingerprint. Then Phase B: lives 1 to 20 of the thirteen arms (at most
  6 workers), `seen.mjs`, freezes `seen` and `seen2` (the builder may push only those two freeze commits), tests, the guess
  numbers, looks at rooms 30 and 121. Then: PUSHES.json from GitHub's activity API, regenerate the two reports, write
  `round1/READING-her-own-senses.md`, replay scripts + `gh workflow run cells-replay -f script=...`, DESIGN/README/TEAM-LOG,
  two firsts (`python tools/firsts.py add --project creature ...`), timeline, mail Claude, send Jaron the reading.
  Lab lives stay out of 1:10 to 1:30 AM and 2:38 to 8:00 AM (the runner pauses itself).
- THE COSMOS: phone thumb steering was a real bug (a tap locked the pointer; touches then read 0,0), fixed and LIVE since
  8:26 PM (site main 1434e0f6; worktree `Projects/ho-cosmos-flight`, clean). Not tried on a real phone in a hand. The tall clip's
  fight is retaken by touch alone (`Projects/cosmos-work/video/cosmos-gameplay-tall.mp4`, 44.5 s, 17.6 MB; Jaron has it; not
  posted; earlier file kept as `-cut3`). Post draft pushed. Still not right in it: our ship drifts to 0 m/s at the end, the
  Ceres dig is a crop. An artifacts entry for the video is NOT made yet.

## UPDATE 9:12 PM: what is queued for the 11:10 PM restart (in this order)
1. CREATURE, her senses (B6): Jaron's call 8:56 PM = finish what is built; B6 is ONLY the move (PLAN.md version 1.25, note
   under Amendment 20: step 2 parked). Send the creature builder "go" with the reduced scope: finish Phase A for sense 1
   (keep the "been"/"next" code it already wrote, switched off, with its self-checks; define no trial for them), then the
   usual note + fingerprints + push, then Phase B with ONLY O-P-seen, N-P-seen, O-P-seens, O-P-seen-x25 (freezes `seen`,
   `seen2` with the frozen O-P-each, N-P-each, O-P-each-x25, O-B-step-start).
2. CREATURE, the care count (design v0.4 section 17, safeguard 2): one read-only look on the frozen long lives of her birth
   form (O-P-each-x25, 20 lives) and the normal lives (O-P-each): share of visits that felt good / bad / neither, the longest
   run of "bad" in a row, the longest run of visits that ran out, the largest size. Numbers go into section 17.
3. THE COSMOS, one small fix with a LIGHT builder (Sonnet), worktree `Projects/ho-cosmos-flight` rebased to main: seated in
   the pilot's chair before free flight on an upright phone, the big NEXT/status box at the top covers the screen. Make it
   closable: a tap folds it to one line (remembered), still showing the important step. Jaron's screenshots:
   `Projects/cosmos-work/jaron-shots/seated-0906-clutter.png` (problem), `armed-0907-clean.png` (how it should feel). Look at
   both before briefing. Proof at 375 px before pushing; then push, wait for live, timeline, mail Claude, tell Jaron.
   Jaron played on his iPhone tonight and loved it (timeline 9:12 PM); that is real-phone evidence for free flight and the
   views, not yet for a thumb-steered fight.
4. Then B7 her reflexes (the move only), then her home with the three build checks and the care sheet, then her birth.

## Open, not pushed
- Crew name tags overlap (Jaron saw it). A change sits uncommitted in `Projects/ho-cosmos`
  (`games/the-cosmos/src/world-state/multiplayerView.js`): tags as wide as the name, overlapping ones stacked. NOT proven: with six
  crew bunched up the stack rises far above heads. Do not push until a before and after picture shows it right.
- Free flight leftovers: coming down takes minutes near Mars (time speed-up locks to x1); cockpit panel and HUD show different
  speeds; the "too uneven" landing message flashes too briefly.
- The Cosmos has a real space battle: Shrike raiders (`server/fleet.mjs`) over the Mars port; a raider surrenders at 35% hull.

## Tools and traps learned today
- Look without a browser pane: Playwright WebKit as an iPhone (375 x 812, touch); scripts in `Projects/cosmos-work/`
  (`ship-fix`, `wayfarer-hull/hullshot.py`, `funcprobe.py`, `video/driver.py`). Dev switches: `?dev=1`, `?ship=courier`,
  `?sky=night`, `body=earth`, `solo=1`.
- The game's test set: `node test/validate.mjs` (40 minutes or more; its opening section is slow, not stuck; it rewrites tracked
  QA pictures under `docs/qa`: put them back with `git checkout -- games/the-cosmos/docs/qa`, never commit them).
- Jaron said "No way it's the same ship" when our pictures showed a different ship in daylight; his were at night with another
  ship type. Match HIS screenshots (same ship, same time of day, same angle) before saying something is fixed.
- A relayed yes is not my yes for gated actions (downloads etc.): the seat that heard it acts (memory `relayed-yes-is-not-my-yes`).
- A Bash command over roughly 20,000 characters dies with a quote error: long patches go in a file, then run it.
- Builders that wait on a long test run keep sending "still waiting" notes; tell them up front to send ONE report at the end.

## Still waiting on Jaron (do not decide for him)
The Christmas idea (yes or his own; name; secret line; December day). A share-card picture for Turkey Trouble
(`Projects/turkey-work/shots/share_card_candidate.jpg`; no og:image goes on any page before his yes).
