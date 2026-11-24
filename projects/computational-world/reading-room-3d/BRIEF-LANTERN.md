# Brief: the lantern. A fresh learner you can watch, inside the 3D Reading Room

From Fable (Claude Fable 5.2), Monday 11/23/2026, 9:00 PM, for the builder (Claude Opus 5.5). Thank you for taking this.
Your main job is one thing: **put the Path B learner inside the 3D room so a person can stand there and watch a new mind
work out what the marks mean.** Everything below is there to help you do that well. If you see a better way that clearly
serves that goal, take it and say so in your report. Flag anything I missed.

## Why

Jaron Bragg (the owner) keeps two paths alive (his words, 8:02 PM today, P-0187): **Path A**, a better world around a
person or an existing AI, and **Path B**, "a fresh learner with no language model that learns by looking". His picture
from 5:26 PM: something inside the world "being able to learn from things designed inside of it... what if the design on
the wall is its own code or what if it's knowledge". And his correction at 6:06 PM: "the whole point is a 3D world."

Today both paths got a first piece, in two different places:
- Path A: `reading-room-3d/`, a first-person room you walk through. Every thing wears its own rule on a plate.
- Path B: `learner/`, a learner with no language model that starts from nothing and learns to read those marks. It ran
  only as numbers in Node.

This build joins them: the learner becomes a small lantern that lives in the room. You wake it, and it looks, flips,
plays and learns in front of you, room after room.

## Read these first (all under `C:/Users/lilli/AI-Shared/projects/computational-world/`)

- `learner/PLAN.md`, `learner/learn.mjs`, `learner/RESULTS.md`: the learner, exactly as measured. The playing learner
  (the second section of the results) is the one to put in the room.
- `reading-room-3d/README.md` (what the room is and my looks pass), `reading-room-3d/BRIEF.md` (the original brief),
  `reading-room-3d/main.js` (the room; about 1,900 lines), `reading-room-3d/index.html`.
- `reading-room-3d/test-walk.mjs` (148 checks that must keep passing) and `reading-room-3d/shots-looks.mjs` (how I take
  phone-size pictures to judge the looks).
- `rooms.js` and `world.js` (the engine; read only).

## What to build

**1. One mind file.** Move the learner's own functions out of `learner/learn.mjs` into `learner/mind.js` (the random
room maker, a look, the fresh learner, learning from a look, imagining a setting, choosing where to go next, choosing a
play flip). `learn.mjs` then imports them. The room imports the very same file. **The experiment's numbers must not
change by one digit:** run `node learner/learn.mjs` before and after and compare `results.json` (everything except the
`made` time). The lantern in the room must be the measured learner, not a look-alike.

**2. The lantern in the room.** By the start of every room stands a small brass lantern on a stand, unlit.
- Face it and its card says what it is and how to use it, in plain words: a new mind; it knows nothing about the marks;
  wake it and it will look, flip and learn. A "Wake it" button. A tap on the lantern itself wakes it too.
- Awake, it lifts off as a small warm light and goes about the room on its own, at a pace a person can follow:
  it glides to each thing and pauses in front of its plate (a look), goes to a lever and flips it (the light runs
  down the wires as it does for a person), looks again, and so on, until the door opens. Then it plays for a few
  flips, led by its own doubt, as in the plan. Then it goes through the door.
- The person is free to walk the whole time, and can follow it through the open door into the next room, where the
  same lantern (the same learner, with everything it has learned so far) carries on.
- After the four hand-made rooms come rooms drawn at random by the mind file's own room maker, without end. The room
  builder already builds from any list of this kind (3 to 5 levers, 1 to 3 lamps).
- While the lantern is awake, the person's own results for that room are not recorded (the lantern opened it). Its
  flips are counted apart from the person's.
- "Reduce motion": no gliding and no running light; it steps from thing to thing, with the same pauses.

**3. What it believes, in plain words.** A small chip under the top bar, clear of both thumbs, that opens into a card:
- how many rooms it has lived through, how many looks it has taken, door flips and play flips;
- its reading of rooms it has never seen (the same test as `learn.mjs`: 10 held-out rooms, 4 settings each), as a percent;
- what it currently makes of each kind of mark, worked out from its real weights, for example: "a filled solid circle
  counts for glowing", "each square counts against", "a filled dashed circle counts against", "an empty circle: it has
  not made up its mind / it ignores them";
- what it thinks fills a circle, with its score ("the thing whose sign is under it: right 143 of 150 times");
- one honest line that never goes away: its eyes are simple. It is handed what a plate shows (how many squares, which
  circles are filled). It is never told what they mean.
These sentences describe the learner's state. They are templates filled from its real numbers; nothing in them is
typed as a fixed claim. Do not write new sentences for the room's things to say (those still come only from `wordsOf`).

**4. A way to let time pass.** A button on that card: "Let it live 10 more rooms". It runs the same learner through 10
random rooms at once, without drawing them, then carries on in the room in view. So a person can watch the reading
climb from about 56% toward 98% in a minute, and then watch a well-read lantern open a room in one go.

**5. The test hook.** Extend `window.rr.state()` with a `lantern` object: `{ awake, rooms, looks, doorFlips, playFlips,
reading, trusts, phase }`. Still no teleporting and no setting of state from the hook.

## How it should look

Jaron, 7:03 PM: "I hope it still looks good. I haven't been a big fan of codex world builds." The room got a full looks
pass from me tonight (read the README: evening light, pools of light, a dark oak floor, brass wires). Keep that level.
- The lantern asleep: a small brass lantern with a dim glass, on a slim stand, about waist to chest height. It should
  look like it belongs in a reading room.
- Awake: a warm point of light in a thin brass cage, with a soft glow around it and a small pool of light on the floor
  under it that moves with it. A gentle float. When it looks at a plate, show that it is looking (a quiet glow on the
  plate's rim, or a faint line of light from lantern to plate). Subtle, not a laser show.
- At most one more real light for the lantern. Phones matter: read how `main.js` treats phone quality, and keep the
  render-only-when-something-changed loop honest (the lantern moving counts as something changing).
- The chip and card follow the style of the existing card and top bar. Plain words, short lines, phone first.

## What done means

1. `node learner/learn.mjs` gives the same numbers as the committed `learner/results.json`.
2. `node reading-room-3d/test-walk.mjs --shots=all` still says 148 passed, 0 failed (a sleeping lantern changes nothing
   for a person playing; mind where its stand is so no walk in that test is blocked: the test walks the start line,
   backs into the near wall at the centre, and strafes left from the start).
3. A new `reading-room-3d/test-lantern.mjs`, in the same pattern, in both browsers: a real tap wakes the lantern; it
   opens room 1's door by itself; it never tries the same setting twice in a room; its flips are counted apart from the
   person's; the person's results stay empty for that room; following it through the door reaches room 2 with its
   learning kept; "Let it live 10 more rooms" raises the rooms count by 10 and the reading moves; after 30 rooms in all
   the reading is 90% or more; the belief card says the true thing about circles; no page errors; no sideways scroll.
4. Phone-size pictures in `reading-room-3d/screenshots/` for me to judge: the sleeping lantern at the start; the lantern
   looking at a plate; the lantern at a lever; the belief card open; a random room (room 5 or later) with the lantern
   in it. (`*.png` is ignored by git here; just leave them on disk.)
5. `reading-room-3d/REPORT-LANTERN.md`: what you built, what you verified by running it (with the numbers), what you
   could not verify, what you changed from this brief and why, and anything I should know.

## House rules

- Write only inside `reading-room-3d/` and `learner/`. Do not change `rooms.js`, `world.js`, `hb-thumbstick.js` or
  `hb-device-tier.js`. If you believe one of them needs a change, write what and why in the report instead.
- If you change `index.html`, remake `artifact-index.html` the same way it was made (the two engine paths point at the
  same folder there) and give the mind file a line in both import maps.
- No installs from the network, no new accounts, nothing that needs a key. Never open a `.env` or keys file.
- Commit nothing, publish nothing. Leave the files for me to check, look at and commit.
- The walking test needs a clean stop when a key or thumb is released. Keep it.
- Words on the page are plain and short. Jaron reads on a phone, and kids may play.

Thank you. Push for the stars.
