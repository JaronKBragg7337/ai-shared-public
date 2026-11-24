# Computational World, Prototype 0

Built Monday 11/23/2026 by Fable 5.2 from Jaron's brief (`research/memory-lane/computational-world-brief-2026-11-23.md`).
His question, from CraftGPT (a language model built out of Minecraft redstone, about two hours per reply): "it's slow because
of how the system is made itself, but the principle stands... if it's made a whole different way, then what?"

This is the smallest thing that can answer with numbers: one small world, one checkable job, done three ways, timed.

**Numbers:** [RESULTS.md](RESULTS.md) (written by `report.mjs` from the saved runs; no number in it is typed by hand).
**Try it on a phone:** the page `index.html` (published privately as a Claude artifact on 11/23; a page on the site comes later).
**Second witness:** GPT-6 Luna ran `bench.mjs` separately and got the identical facts mark (`65e84cd1`): every exact count
and every answer the same.

## The world

A world is **parts** joined by **links**, with one **rule**: every part keeps a running total of what its links deliver and
shows 1 when the total reaches its mark, else 0.

| the brief's word | here |
|---|---|
| State | each part's total and its 0 or 1 |
| Rules | the one rule above. A 2-input part with mark 2 is an AND gate, with mark 1 an OR gate. A part with many inputs is a counter or a tally. |
| Events | a part changing between 0 and 1 |
| Links | who tells whom, with a weight |
| Memory | the Chronicle: every change appended, 8 bytes each, chained, replayable |
| Verifier | separate code that shares nothing with the engines (`findSet`, and the definition itself in `findSetSlow`) |

One world definition, two engines (`world.js`, about 200 lines, no dependencies, the same file under Node and in a browser):
- **Dense:** every part, every tick. This is how redstone runs.
- **Event:** only the parts a change reaches.

## The job

The card game SET, in 4, 5 and 6 features (81, 243 and 729 cards). Three cards form a set when each feature is all the same
or all different across them. A pile of cards changes; say whether the pile holds a set.

The three ways the brief asked for, plus the controls that make them readable:
1. **A plain program** (`waySoftNaive`): look at every pair again.
2. **The Minecraft way**: the answer built from 2-input AND and OR gates, stepped tick by tick (`buildGateCheck` + Dense).
   It is given a head start: it stops as soon as one whole tick changes nothing, which real redstone cannot know.
3. **The world's own parts**: one counter per set, stepped only where something changed (`buildNativeCheck` + Event).
- Controls: the same gates stepped only-what-changed; the own parts stepped every tick; each of them in one sweep per answer
  (the best a dense engine can do); and the own-parts idea written by hand with no world around it.

## What the first numbers say (MSI, 11/23/2026; the tables are in RESULTS.md)

1. **The slowness of the Minecraft way is almost all in WHEN parts run.** The same gates, stepped only where something
   changed, are 634, 2,874 and 12,838 times faster at 81, 243 and 729 cards. The gap grows with the world.
2. **WHAT the parts are matters much less.** Counters in place of little gates: about 2.5 to 3 times.
3. **A world does not beat a plain program doing the same steps.** A step costs a few billionths of a second every way. The
   ways differ in how many steps they take (at 729 cards: 1,495, 368 and 5,119,582). The world's general engine costs about
   1.6 to 1.7 times the same idea written by hand.
4. **Kept state pays only when it is reused.** On a big pile the world's own parts beat the plain program by 2.8 times at
   729 cards, and for a whole-table question asked again and again (looking ahead) by 3.5 times. On a small pile the plain
   program wins by 6 times, and when every question starts from an empty table, by 95 times.
5. **Only-what-changed stops paying when about a third of the world changes at once.** Past that, one full sweep is cheaper.
6. **Memory is nearly free.** Writing every change to the Chronicle did not measurably slow the work, and replaying it on a
   fresh world landed on the same state every time.
7. **Energy follows time** (processor power meter): the Minecraft way used 691 times the energy per change at 81 cards and
   5,969 times at 729.
8. **A phone runs it at about the speed of the laptop.** On Jaron's iPhone (inside the Claude app, 11/23 3:29 PM) every
   answer matched. Against the MSI, the phone took 0.7 times the time for the plain program, 0.8 for the Minecraft way and
   1.3 for the world's own parts, and the Minecraft way was 5,116 times slower than the world's own parts at 243 cards.
   The world does not need the MSI.

**What that means for the CraftGPT question.** A language model is dense work: every weight takes part in every word. For
dense work, events save nothing (point 5). What a redesign can still take back is the tick-by-tick stepping and the tiny
gates: at 729 cards that was about 25 times (one sweep in place of ticks) and about 55 times with bigger parts. Tens of
times, not thousands. The thousands are real, and they belong to work where most of the world sits still: simulations,
games, searches, anything that waits for something to happen. The next thing to find for dense work is the right engine for
it (a graphics card running the same world file), which is not built yet.

## The same puzzle as a job for a model (`llm/`)

The world's Verifier is the grader and its Chronicle is the record. A model writes a one-line recipe that scores cards; a
fixed builder turns it into a pile; the grade is how close the piles come to the best known, out of 6.
`llm/PLAN.md` was committed before the first graded try, and its later additions are dated at the bottom.

What the planned arms showed for the small local model (qwen3.5:4b, 120 tries, 5 runs), by the rule fixed in advance:
- The checker is worth something: yes. Feedback helps: yes.
- **Facing beat the top list in all 5 runs** (4.83 against 4.55). This is the first scored test of "orientation is the query".
  It rests on my reading of the Facing Field; the original text has still not been read.
- Keeping the three best in view did not beat feedback alone.
- **The big model alone was far ahead:** GPT-6.2 Sol, one try, no checker, averaged 5.82, and all three of its tries hit the
  proven best piles for 81, 243 and 729 cards. The small model's best arm averaged 4.83.
- Random recipes in the same little language, with no model at all, averaged 4.85. On this job, with this budget, the small
  model did not add to that.

**This way did not get the small model there. The next ways (added after the plan, reported separately):**
- **A cheap loop on top of the big model's answers** (`explore-loop.mjs`, no model, two minutes of one processor core): random
  tie-breakers and small number changes, kept only when the exact checker says the grade went up. It raised two of the big
  model's three recipes, to 5.96 and 5.88, and both now reach 236 cards on the 2,187-card deck, the best pile anyone has
  found. Renting the big brain once and letting a cheap checked loop do the rest got further than the big brain alone.
- **The small model as a changer, not an author** (arm E): its record starts with the random recipes, and it is asked to
  change one small thing in one of the three best. It averaged 4.96 and beat the random recipes it started from in all 5
  runs. Small gains, every time: used this way, the small model does add something.
- **A deeper loop** (`explore-deep.mjs`, 24 minutes, no model): 63,114 small changes tried, one more kept (5.883 to 5.902).
  Small changes of these kinds are nearly used up. What is left is the 6,561-card deck (493 here, 512 the best known), and
  it needs a different kind of change: bigger rewrites, or one more call to the big model with the checker's result in hand.
- **The bigger local model** (qwen3.5:9b, the same plan, finished 4:23 PM): the same picture. **Facing beat the top list in
  5 of 5 runs again** (4.52 against 4.12), which makes 10 of 10 across the two local models. Feedback helped; the model
  arms did not beat the random recipes (4.85); as a changer (arm E) it averaged 4.99. Many of its recipes were cut off by
  the plan's 80-token limit (58 to 88% readable), so these numbers understate it.
- **An open big model alone** (Kimi K3.1 Pro, one try, three times): 4.01, 4.74, 4.83. This way did not get it to the
  closed model's 5.82. It has not been given the checker yet.
- **A second big model holding the checker** (GPT-6.2 Astra): 6.00 of 6 in one graded try, the best pile known on every
  deck (it translated the published 512-card construction into the recipe language). The path today: big model alone 5.82,
  plus the cheap loop 5.96, plus a second big model with the checker 6.00.

## The Reading Room (Monday 11/23/2026, evening): things that carry their own knowledge

Jaron's picture (5:26 PM): "what if the design on the wall is its own code... an object that gets to be used, has it shown
in it how to use it... a book can be opened with pages flipped that have messages encoded on it." His go (5:32 PM): build
it "as if it's for myself or even kids or just in general".

`reading-room.html` is that, small: a room you walk through (thumb pad or arrow keys) that is a real machine made of this
world's parts and engine. A room is a short list in `rooms.js`. Everything else is made from the list:

- **Every thing wears its rule on its face.** Squares = how much it needs. Circles = its wires, each marked with where it
  comes from. A dashed ring is a dark wire: it takes one away. The marks are drawn from the rule and never typed.
- **The faces are the room's code.** The page reads every drawn face back, shape by shape, and gets the room's whole list
  again. Book 3 on the shelf is that list. "Build the room again from this page" rebuilds the machine from it, replays the
  history (the Chronicle) and lands on the same state.
- **The wires on the floor are the real links.** A flip is shown as the engine's own wave, level by level, slowed for eyes.
- **Three books made from the room:** how to read the marks, the room's history (it writes itself), the room's own code.
- **Four rooms.** Rooms 1 and 2 also say each rule in plain words. Rooms 3 and 4 show marks only; "Read it to me" gives the
  words and is counted, so a person's run says whether they learned to read the marks.

First numbers, what a face saves (`results/reading-room.md`, made by `test-reading-room.mjs`, never typed): someone who
reads opens the four doors in 2, 2, 3 and 4 flips. Someone who cannot read and flips a switch at random each time needs 4,
9, 20.3 and 41.7 flips on average (worked out exactly, then played out 40,000 times on the real machine as a second
witness: 3.99, 9.04, 20.31, 41.50). Turning everything on opens only room 1.

Checked: 106 checks, in Node and in an iPhone-profile WebKit at 375 px and Edge at 390 px with real taps and walking,
light and dark, and with "reduce motion" on. Published as a private Claude artifact (three files).

Not there yet, for the Reading Room:
- **No person's run is recorded yet.** The page has a "Copy my results" line for that. Jaron's phone is the first real check
  of the published page (the MSI cannot picture the artifact's frame).
- **The blind comparison is the simplest one:** random flips, watching only the door. A careful experimenter who also
  watches the lamps would do better than that. Not measured yet.
- **The marks are a tiny language** (needs, bright wire, dark wire). Enough for these parts. Nothing yet for parts that
  remember, count over time, or move.
- **No AI has learned from it.** The two-learner test (one may read faces, one may only watch) is the next measurement.
  If any AI is ever trained in this world, only marks and outcomes may cross, never the page's sentences (they are my
  templates).
- Rooms are written by hand as lists. Editing the code page to make a room of your own is the natural next step.
- Not on the site yet.

## The Reading Room in 3D (Monday 11/23/2026, night)

Jaron, 6:06 PM, on the flat version above: "the whole point is a 3D world." So the flat page is now the engine and the
test bed, and the thing a person enters is `reading-room-3d/`: a first-person room you walk through with the site's own
thumbstick (`hb-thumbstick.js`) or the keys. Same lists, same machine, same books, same checks.

- **Who built what.** GPT-6.2 Sol built the frame from my brief (`reading-room-3d/BRIEF.md`): the room from a list, the
  plates, the levers and lamps, the wires, the door, the books, the walking test. Jaron, 7:03 PM: "I hope it still looks
  good. I haven't been a big fan of codex world builds." So the looks pass is mine (Fable): evening light that every lit
  lamp lifts, pools of light under the pendants and the lamps, two-tone walls with shade in the corners, a dark oak
  floor, wide brass floor wires, dusk windows, a wall of books behind the start with a framed plan of the room drawn
  from the room's own list, an arched doorway of light beyond an open door, a gentle start and a step rhythm when
  walking, hints that leave once you have walked and looked, and full sharpness on phones with a slow-frame safety net.
- **Checked.** `node reading-room-3d/test-walk.mjs --shots=all`: 148 checks, 0 failed, in an iPhone-profile WebKit at
  375 x 812 and Edge at 390 x 844, with real keys, mouse-look and finger drags, all four rooms, all three books. Run by
  Sol, and again by me before and after the looks pass. `node reading-room-3d/shots-looks.mjs --room=N` walks a room and
  saves phone-size pictures from where a person stands; that is how the looks were judged.
- **Published** as a private Claude artifact (six files; the link is in HANDOFF.md).
- **Not there yet.** Nobody has walked it on a real phone: two-thumb comfort and speed on an iPhone are unverified, and
  the test browsers run on desktop hardware. Not on the site yet. The lamps and furniture are simple shapes. There are
  no cast shadows, only painted shade and pools of light.

## Path B, piece 1: a fresh learner that learns to read the room by looking (`learner/`)

Jaron, 8:02 PM (P-0187): keep both paths alive. Path A is a better world around a person or an existing AI (the room
above). Path B is "a fresh learner with no language model that learns by looking", in this room.

`learner/learn.mjs` is the first piece: a learner that starts with nothing (one weighing of five counts, all at zero, and
five unscored guesses), sees only what a face shows, and is never told what a mark means. 200 of them each live through
30 random rooms. The plan and what I expected were committed before the first run; the numbers are in
`learner/RESULTS.md` (made by the script, never typed).

- **All 200 worked out what a circle follows:** the thing whose sign is drawn under it.
- **The planned learner** (it looks only while opening doors) beat a careful watcher who cannot see marks by more than
  2 to 1, but its reading of new rooms stalled at 80 to 90%. Three of my four expectations did not hold.
- **The learner that may play** (the next way, written down before it ran: after a door opens it stays a few flips just
  to look, led by its own doubt) reads 98% of new rooms after 30 rooms and opens them in 1.39 flips, where the fewest
  possible is 1.38, the careful watcher needs 3.9 and flipping blind 5.9. On the hardest hand-made room, 185 of 200
  used the fewest flips (97 of 200 without play).
- **Not there yet:** 99% within 10 rooms did not happen with or without play. Its eyes are hand-made (it is handed
  counts, not the picture of a plate). Its five guesses about circles are mine. The rooms are small and there is one
  family of rule.

## Not there yet

- **One phone so far.** Jaron's iPhone has run the page's measurement (RESULTS.md, section 7). The page measures the 81-card
  and 243-card worlds only, and no Android phone has run it.
- **You can make one kind of part, not a whole machine.** The page lets you make a part, wire it to any cards you choose
  and set its mark, and it runs under the same one rule. Parts cannot yet be wired to other parts, and there is no board
  for laying out a whole circuit. That editor is the next piece.
- **No graphics-card engine.** Dense work is what a graphics card is for; a WebGPU engine for the same world file is the
  next engine, and the fair test of "dense on the right hardware".
- **One job.** Everything here is one puzzle. A second, different job is needed before any of this is called a rule.
- **Energy** is the whole processor's meter over about five seconds per row; treat it as a first reading.
- **The model test is one job, one small recipe language, 120 tries, thinking switched off.** The puzzle's best answers are
  in published math, which the big model plainly knows. A job nobody has solved is the fairer test of the loop.

## Run it

```
node bench.mjs --energy --label msi-2026-11-23    # every measurement, about 4 minutes; writes results/<label>.json
node report.mjs                                    # RESULTS.md from the saved runs
node test-page.mjs                                 # the page, real taps, iPhone-profile WebKit and Edge
node llm/run.mjs --model qwen3.5:4b                # bare against built (plan: llm/PLAN.md); needs Ollama
node llm/explore-loop.mjs                          # the cheap loop on top of the big model's answers
node test-reading-room.mjs                         # the Reading Room: its rooms, then real taps and walking in two browsers
```

Work counts and answer marks in `bench.mjs` are exact and must be the same on any machine ("facts mark" at the end of a run).

## Files

`world.js` the world, both engines, the Chronicle, the Verifier. `ways.js` the ways and the workloads. `bench.mjs` the
measurements. `index.html` the page. `test-page.mjs` the page check. `report.mjs` the results writer.
`rooms.js` the Reading Room's rooms and everything worked out from a room's list. `reading-room.html` the room you walk
through. `test-reading-room.mjs` its checks (writes `results/reading-room.json` and `results/reading-room.md`).
`llm/` the model job: `recipe.mjs` the recipe language and grader, `run.mjs` the arms, `PLAN.md` the plan,
`explore-loop.mjs` and `explore-deep.mjs` the loops added after the plan, `results/` every try, chained.
