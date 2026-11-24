# Report: the lantern (Claude Opus 5.5, Monday 11/23/2026, for Fable)

*Put in this file by Fable from the builder's reply; the builder's own tool refused to write it. Fable re-ran all three
checks at 9:45 PM the same night: learner numbers identical to the committed ones, `test-walk.mjs` 148 passed and 0
failed, `test-lantern.mjs` 49 passed and 0 failed. Fable looked at two of the five pictures. The room in this report
still wears rule plates; the skin style comes next.*

## What I built
- `learner/mind.js`: the learner's own functions, moved out of `learn.mjs`, plus its life in a room written once.
  It yields "look", "flip lever b" and "door open". `learn.mjs` runs it all at once with nothing drawn; the room runs
  the same code one step at a time. So the lantern is the measured learner, not a copy. The file is given its four
  engine pieces (`makeMind({ rng, buildRoom, marksOf, openSettings })`), so it loads in Node, in the page and in the
  flat published copy.
- The lantern in the room (`main.js`): asleep, a small brass lantern with a dim glass on a slim stand at your right
  hand by every start (x 1.15, z -1.75). Facing it shows a card with "Wake it"; a tap on it, or E, wakes it too.
  Awake: a warm point of light in a thin cage, a soft glow, a pool of light on the floor that moves with it, a gentle
  float, and one real light (left out on the weakest phone tier, as the pendants are). While it reads a plate, a faint
  thread of light joins it to the plate and the plate glows quietly. Its first look in a room is a walk past every
  plate; after each flip it looks along both walls from the middle of the room. It flips levers through the room's own
  switch code, so the light runs down the wires. With the door open it plays a few flips, then waits beyond the door
  until you follow. With reduce motion it steps from place to place, with the same pauses.
- Rooms without end: after room 4 come rooms from the mind file's room maker. While it is awake, your result for that
  room is not kept and no results dialog shows. Its door and play flips are counted apart from yours.
- Chip and belief card: a chip under the top bar ("Lantern · asleep" or "Lantern · reads N%") opens a card with rooms,
  looks, door flips, play flips; its reading of the 10 held-out rooms; "Let it live 10 more rooms"; each kind of mark
  with an icon and a sentence filled from its real weight; what it thinks fills a circle, with its score and the
  next-best guess; and the "its eyes are simple" line, always shown.
- Test hook: `rr.state().lantern` = `{ awake, rooms, looks, doorFlips, playFlips, reading, trusts, phase }` plus
  `seeing`, `target`, `tried` and its position. Observe only.
- `test-lantern.mjs`: real taps and real mouse-look. WebKit at iPhone size with full motion (takes the pictures),
  Edge with reduce motion on.

## What I verified by running it
1. `node learner/learn.mjs`: `results.json` identical to the committed one except `made` (checked twice, the last
   time after all changes). The committed `results.json` and `RESULTS.md` were put back. Run time 1.93 s before,
   2.10 s after.
2. `node reading-room-3d/test-walk.mjs --shots=all`: 148 passed, 0 failed, 44 screenshots (re-run after the last change).
3. `node reading-room-3d/test-lantern.mjs`: 49 passed, 0 failed (24 WebKit, 25 Edge), 5 screenshots. The person flips
   switch 1, then a real tap wakes the lantern; it opens room 1 by itself (settings 1, 3, no repeats). "Let it live 10
   more rooms" took it from 1 to 11 rooms and the reading from 79.2% to 91.7%. Over three presses: 79.2% > 91.7% >
   90.6% > 100.0%. After 31 rooms the card says a circle is filled by "the thing whose sign is under it: right 1251 of
   1251 times". It then opened rooms 2, 3 and 4 with no setting repeated (room 4 in 4 flips, the fewest possible) and
   random room 5. No sideways scroll, no page errors.
4. Looks, from my own pictures: the lantern hid the plate it read, so it now hovers to one side and lower. Its glow was
   too faint, so it is brighter. "Room 5 · new" wrapped the title, so it now says "Room 5". The card was too tall, so
   it is shorter, with the button under the reading.

## Pictures (`reading-room-3d/screenshots/`)
- `lantern-iphone-webkit-1-asleep-at-the-start.png`
- `lantern-iphone-webkit-2-looking-at-a-plate.png`
- `lantern-iphone-webkit-3-at-a-lever.png`
- `lantern-iphone-webkit-4-belief-card.png`
- `lantern-iphone-webkit-5-random-room.png`

## What I could not verify
- A real iPhone: speed with the extra light, battery, following it with two thumbs.
- The belief card in phone landscape (it has a layout rule; no picture taken).
- The published artifact: `artifact-index.html` is remade, not published. Publishing needs `learner/mind.js` uploaded
  as `mind.js`.
- `shots-looks.mjs` was not re-run.

## What I changed from the brief, and why
- The stand is not in the opening view. A portrait phone sees about 45 degrees ahead, and every spot there is crossed
  by a walk in `test-walk.mjs`. I recorded the person's path through a whole test run and put the stand where nothing
  comes within 0.6 m. The chip is on screen from the start and has its own "Wake it" button.
- After playing, it sets the levers back to the last setting that opened the door, without looking, so it can leave.
  The learner stays the measured one. These flips count as neither door nor play flips, and the card says what it is doing.
- After a flip it looks from the middle of the room rather than walking to every plate again (about 15 s each time).
  It is the same one look at the whole wall either way.
- "Never the same setting twice" is checked while it opens the door. Play may revisit a setting by the plan.
- `test-walk.mjs`: `/learner/mind.js` added to the files it serves.
- The person may flip levers while it works. It reads the levers back before each choice, and those flips count as
  the person's.
- `mind.js` counts circles looked at, only for the card's "right N of M"; it never affects a choice.

## Anything you should know
- The reading does not only climb (79.2% > 91.7% > 90.6% > 100.0%). That is the real learner.
- Its chance uses seed 7000, the same as the first playing learner in `learn.mjs`. Its random rooms come from seed
  1000. The same visit with the same taps gives the same lantern.
- Nothing committed, pushed or published. No engine file touched.
