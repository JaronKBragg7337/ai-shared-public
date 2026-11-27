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
