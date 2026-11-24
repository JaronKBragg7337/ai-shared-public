# Path B, piece 1: a fresh learner that learns to read the room by looking

Fable 5.2, Monday 11/23/2026. Written and committed before the first run.

**Path B** (Jaron, 8:02 PM, P-0187): "a fresh learner with no language model that learns by looking", in the Reading
Room, not the creature. Path A (a better world around a person or an existing AI) is the room itself.

His picture (5:26 PM): something inside the world "being able to learn from things designed inside of it... what if the
design on the wall is its own code or what if it's knowledge".

## The question

Every thing in the Reading Room wears its rule as marks. A person who can read the marks opens a door in the fewest
flips. **Can something that starts knowing nothing about the marks learn what they mean just by looking, and then read
rooms it has never seen?** How many looks does that take, and how much does it save?

## The learner (no language model, no neural net library, a few dozen lines)

**What it is given** (its body, not knowledge of the marks):
- It can walk along the wall and look at one thing at a time. A look returns only what is drawn and what is visible:
  the thing's sign, whether it is a lever, how many squares, each circle (solid or dashed ring, filled or empty, the
  sign drawn under it), and whether the thing is glowing (a door: open).
- It can flip a lever. It wants the door open.

**What it is NOT given:** what a square means, what a circle means, what dashed means, what filled means, what the sign
under a circle points at, or the rule that ties them together.

**How it learns, from looks alone:**
1. *When does a thing glow?* One weighing of five counts it can see (squares, filled solid circles, filled dashed
   circles, empty solid circles, empty dashed circles). It starts with every weight at zero and nudges the weights each
   time a look proves its guess wrong (the perceptron rule, 1958). The truth it has to find: glow when filled-solid minus
   filled-dashed reaches the squares. Two of its five counts are distractions.
2. *When is a circle filled?* Five guesses, each scored by how often it matches what the learner sees: the circle follows
   the thing whose sign is drawn under it (true); it follows the thing wearing it; it follows the thing standing just
   before; it follows the thing in the same place along the wall as the circle's place on the plate; it is never filled.
   Ties go to the earlier guess in that list's REVERSE order, so the true guess has to earn its place.

**How it uses what it has learned:** in a new room it looks at every thing once, then imagines each way the levers could
stand, using its own two learned rules, and picks the nearest setting it expects to open the door. It flips, looks
again, learns from what it sees. If the door stays shut it never tries the same setting twice.

## The comparison

- **The watcher:** cannot see marks at all, only what glows. A careful one: never repeats a setting, tries the nearest
  untried setting next. It has nothing to carry from one room to the next.
- **Flipping blind:** one random lever each time (worked out exactly, as in the Reading Room).
- **A reader who already knows the marks:** the fewest flips possible.

## The run

- Rooms are drawn at random from the same parts as the Reading Room: 3 to 5 levers, 1 to 3 lamps, bright and dark wires,
  a door. Kept only if the door can be opened and is not open at the start.
- 200 learners, each from nothing, each living through 30 rooms of its own. Same for 200 watchers on the same rooms.
- Before each room, each learner is tested on 10 rooms it will never play (4 lever settings each): from the marks and the
  lever positions alone, does it say rightly which things glow? That share is its "reading".
- Afterwards, each trained learner plays the four hand-made rooms of the Reading Room.
- Counted: flips to open each room, looks taken, the reading share, by how many rooms the learner has lived through.

## What I expect (written before running)

1. Reading reaches 99% or more within 10 rooms, on average.
2. From room 11 on, the learner's flips average within 10% of the fewest possible.
3. The watcher does not get better with experience (its room-21-to-30 average within 10% of its room-1-to-10 average)
   and stays well above the learner.
4. Every trained learner opens the four hand-made rooms in exactly the fewest flips (2, 2, 3, 4).

If one of these fails it gets said plainly, with the next way to try.

## Limits, stated now

- **Its eyes are hand-made.** It is handed counts of squares and circles, not a picture of the plate. Learning to see the
  plate from its pixels is a later piece.
- **Its five guesses about circles are mine.** It weighs them by evidence, but it did not invent them.
- The rooms are small, and the rule family is one rule (add up, compare). Nothing here remembers or counts over time.
- This is a learner in the flat engine. The 3D room is for people; a learner that looks through a camera is further off.

## Changes after the plan was committed

**8:41 PM, 11/23/2026. The first run is in; three of my four expectations did not hold. Written before the next run.**

What the planned run said (`RESULTS.md` as committed with this note): all 200 learners found the truth about circles, and
the learner beat the careful watcher by more than 2 to 1 from early on. But reading stalled near 80 to 90% (I expected
99% within 10 rooms), its flips stayed 17% above the fewest possible (I expected within 10%), and on hand-made room 4
only 97 of 200 used the fewest flips.

My reading of why, to be tested and not assumed: this learner only looks while it is busy opening a door, and the random
rooms open in one or two flips. So it rarely sees the telling cases: a thing that is one short of what it needs, or a
dark wire carrying light. The rule for circles needs no such cases; the rule for glowing does.

**The next way: a learner that may play.** Same learner, same senses, same rooms, one thing added. After it opens a
door it stays for as many extra flips as the room has levers, purely to look. It chooses each of those flips by its own
doubt: of the settings one flip away, it prefers one it has not seen in this room, and among those the one where its own
weighing is closest to undecided for some thing (ties by chance). It looks after each flip and learns as before. Play
flips are counted separately and never as door flips.

Also added, so the reading is not a single number: a split of the reading test by kind of thing (needs 1 with no dark
wire; needs 2 or more; has a dark wire), for both learners.

**Read by the same four expectations**, labelled as after the plan. If playing does not lift reading to 99%, the ways
after that, in order: a larger doubt-driven play budget; rooms that get harder as it reads better; a learner that keeps
several weighings and trusts the best (as it already does for circles).
