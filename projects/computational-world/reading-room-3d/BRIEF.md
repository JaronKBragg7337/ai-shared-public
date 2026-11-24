# Brief: the Reading Room as a real 3D room

For GPT-6.2 Sol, from Fable (Claude Fable 5.2), Monday 11/23/2026, 6:20 PM. Thank you for taking this one.
Your main job is one thing: **make the Reading Room a 3D room a person walks through.** Everything else below is there to
help you do that well. If something here looks wrong, or you see a better way that clearly serves the goal, take the better
way and say so in your report. Flag anything I missed.

## Why

Jaron Bragg (the owner) pictured a world whose things carry their own knowledge: "what if the design on the wall is its
own code... an object that gets to be used, has it shown in it how to use it... a book can be opened with pages flipped
that have messages encoded on it." I built it this afternoon, and I built it flat (a 2D hallway). His answer, 6:06 PM:

> "I don't think Fable got the 3D world aspect and just built the new thing in 2D. If it works it works, but the whole
> point is a 3D world."

He is right. The logic is done and tested. What is missing is the place itself.

## What already exists (read these first; do not change them)

All in `C:/Users/lilli/AI-Shared/projects/computational-world/`:

- `rooms.js`: the four rooms as short lists, and everything worked out from a list: `buildRoom` (the running machine),
  `marksOf` (what a thing shows on its face), `thingFromMarks` (a face read back into a rule), `wordsOf` (the same rule in
  plain words), `codeText` / `parseCode` (the room as a page of text and back), `openSettings`, `fewestFlips`,
  `blindAverage`, `nameOf`, `count`.
- `world.js`: the parts, the engine (`EventEngine`), the history (`Chronicle`), `stateMark`.
- `reading-room.html`: the flat version. **Use it as the reference for behaviour**, not for looks: how a flip is recorded,
  how the change is shown level by level (`flip`, `runWaves`), the card for the thing you face, "Read it to me", the three
  books (`renderBook`), the faces as SVG and reading them back (`faceSvg`, `readFace`, `readFaces`), the results table and
  the "Copy my results" line, and the test hook `window.rr`.
- `test-reading-room.mjs`: how I test with real input in an iPhone-profile WebKit at 375 px and in Edge (Playwright lives
  at `C:/Users/lilli/.codex/runtime/unfinished-island/node_modules/`; WebKit at
  `%LOCALAPPDATA%/ms-playwright/webkit-2336/Playwright.exe`; Edge through `channel: 'msedge'`; pages are served to the
  browser by route interception at `http://cw.test/`, no server).
- `README.md`, section "The Reading Room": what it is and what its first numbers say.

The house style for walkable 3D lives in the site repo, `C:/Users/lilli/Projects/heartbeat-observatory/` (read only; do
not write there):

- `world2/index.html`, `world2/main.js`, `world2/shops.js` (rooms you walk into): renderer set-up, the loop, the phone
  budget, the screen furniture, how things are used by touching them.
- `hb-thumbstick.js`: **the house thumbstick. Use it.** A thumb on the left half walks (the stick appears where the thumb
  lands), a drag on the right side looks, a quick tap is handed to `onTap` so a person can USE a thing by touching it.
- `hb-device-tier.js`: how the site decides what a phone can afford.
- `WORLD2-REMAKE.md`: what went wrong before and the fixes (blank loading, boxy sameness, too dark, tap-to-walk).
- three.js is loaded as World 2 loads it: `https://cdn.jsdelivr.net/npm/three@0.182.0/build/three.module.js`.

Jaron's rule for every world: **"I don't want to tap to walk. I want to walk."** Thumbstick on a phone, keys on a computer.

## What to build

Write everything inside **`C:/Users/lilli/AI-Shared/projects/computational-world/reading-room-3d/`** and nowhere else.

A first-person room, eye height about 1.6 m, that is built from a room's list. One room at a time; four rooms.

**The room.** A real, warm reading room, not a grey box: a plank floor, plaster walls with a baseboard, a ceiling, soft
warm light. Make the textures in code (canvas), so the page needs no picture files. About 8 m wide and 3.4 m high; make
it as deep as the list needs (roughly 6 m plus 2 m for each switch or lamp on the longer side).

**Where things stand** (worked out from the list, never placed by hand):
- You start by the near wall, looking down the room at the door.
- Switches along the left wall, lamps along the right wall, in list order from near to far.
- The door in the middle of the far wall. It is a real door: shut, it is shut; when its rule is met it swings open and
  light comes through; you walk through it into the next room.
- The bookshelf on the far wall beside the door, with three real books on it.

**Every thing wears its own rule on its face.** Each thing has a plate at about chest height, big enough to read from
about 4 m. Draw the plate from `marksOf(...)` onto a canvas texture: the thing's sign, one square for each one it needs,
one circle for each wire with the sign of where it comes from under it, a solid ring for a bright wire, a dashed ring for
a dark wire, a filled circle while that wire carries light. Nothing on a plate is typed by hand. Plates update live.
- A switch is a chunky lever you can see is up or down, and its plate shows the same toggle.
- A lamp is a real lamp (a glass globe on an arm). When it lights, it glows and the room gets a little brighter and warmer.

**The wires are in the room.** Each link runs from its source down the wall, across the floor in tidy right-angle runs,
and up the wall to the circle that stands for it on the target's plate. A bright wire carrying light glows amber; a
resting one is dull brass; a dark wire is purple and dashed. On a flip, **the light runs along the wire** at the engine's
own pace, level by level (see `runWaves` in the flat page: about a third of a second for each level), and the lamp lights
when the light arrives. A person should be able to follow a wire across the floor with their eyes.

**Facing is reading.** The thing nearest the middle of your view, within about 3.5 m, is the one you face. Its plate gets
a quiet highlight, and a card slides up from the bottom of the screen with: its name, its face (reuse the SVG face), and
- in rooms 1 and 2, the rule in plain words from `wordsOf` (live, with the running sum);
- in rooms 3 and 4, marks only, with a "Read it to me" button that shows the words and is counted;
- for a switch, a "Flip it" button. Touching the lever in the world (a quick tap on it, close enough) flips it too.
- for the open door: "The door is open. Walk through it."
- for the bookshelf: the three books. A book opens as a panel with pages you turn. Same three books as the flat page:
  how to read the marks, the room's history, the room's own code with "Build the room again from this page".
The card must never cover the thumbs: keep it clear of where the house thumbstick and the look-drag work.

**Walking.** Phone: the house thumbstick exactly as World 2 uses it. Computer: W A S D to walk, drag to look, the left and
right arrow keys also turn, the up and down arrows also walk, E (or Enter) uses what you face. You cannot walk through
walls, things, or a shut door. Never tap-to-walk.

**The rest of the flow**, as in the flat page: "Room 1 of 4" and the flip count on screen; going through a door shows how
you did (your flips, the fewest possible, the flipping-blind average) and a way on to the next room; after the last room,
the "Your reading so far" table and the "Copy my results" line. Keep the wording of the flat page: plain words, no jargon.

**Reduce motion.** If the phone asks for less motion, changes show at once (no running light, no swing), as in the flat page.

## Files and shape

```
reading-room-3d/
  index.html        the page. An import map names: "three", "hb-thumbstick", "hb-device-tier", "rr-rooms", "rr-world".
  main.js           the 3D room. It imports only those five names, so the same file runs here, on the site and as an artifact.
  hb-thumbstick.js  copied unchanged from the site repo (so this folder runs on its own)
  hb-device-tier.js copied unchanged from the site repo
  test-walk.mjs     your walking test (see below)
  README.md         what it is, how to run the test, and an honest "not there yet" list
  REPORT.md         your report to me (see the end)
```
In `index.html` map `"rr-rooms": "../rooms.js"` and `"rr-world": "../world.js"`. Do not copy or edit those two files.
(`rooms.js` imports `./world.js` itself; that already works from this folder.)

Keep the test hook, grown for 3D, so a test can read the room but not cheat:
`window.rr.state()` returns at least `{ room, x, z, yaw, facing, through, settled, on, shown, open, best, blind, flips,
asks, history, facesOk, words, done }` (same meanings as the flat page; `yaw` in radians, 0 = looking down the room at
the door), and `window.rr.pos()` returns where each thing stands and where the doorway is: `{ "1": { x, z }, ...,
doorway: { x, z }, start: { x, z } }`. No teleporting and no "set state" in the hook.

## The phone budget

It must feel smooth on an iPhone. Follow `hb-device-tier.js` and World 2's choices. As a guide: pixel ratio capped at 2,
no real-time shadows on phones (a soft dark patch under things is fine), few lights (lamps can glow without each one being
a light; a handful of small lights at most), low draw calls, no post-processing on phones. Something should be on screen
within a second or two: show the room first, finish the details after.

## How I will judge it (and how you can check yourself)

Write `test-walk.mjs` in the pattern of `test-reading-room.mjs`: an iPhone-profile WebKit at 375 x 812 and Edge at
390 x 844, pages handed over by route interception (serve `https://cdn.jsdelivr.net/...three.module.js` from a local copy
if the browser has no network; say in the report where the copy came from). With real input only:
1. the page loads with no errors and no sideways scroll; `facesOk` is true in every room;
2. holding W (or the arrow keys) walks; letting go stops; you cannot leave the room or pass a shut door;
3. a drag on the house thumbstick walks, and a drag on the right side turns (in Edge, drive a real finger through
   `Input.dispatchTouchEvent`, as my test does);
4. turn to face switch 1 and walk to it: the card shows "Switch 1"; a real tap on "Flip it" turns it on; the light runs;
5. all four rooms can be opened by walking to the right switches (`state().open[0]` says which), and you can walk through
   each open door; room 2 with every switch on stays shut and the door's card says why;
6. room 3 shows marks only until "Read it to me" is tapped; the three books open; "Build the room again" says "Same room";
7. save screenshots of each room at phone size (looking down the room, facing a lamp's plate, facing the door, the open
   door, a book open). I will look at every one: the room should read as a warm, real place, plates readable, wires clear.
Please run your test and tell me plainly what passed, what failed and what you could not check. A test you could not run
is fine to report; a claim without a run is not.

## A few house rules

- Write only inside `reading-room-3d/`. If you believe `rooms.js` or `world.js` needs a change, do not make it: write what
  and why in the report.
- No installs from the network, no new accounts, nothing that needs a key. Do not open any `.env` or keys file.
- Every sentence a thing "says" comes from `wordsOf`. Do not write new sentences for things to say.
- Words on the page are plain and short (Jaron reads on a phone, and kids may play).
- Commit nothing; leave the files for me to check and commit.

## Your report (`REPORT.md`)

Short and plain: what you built; what you verified by running it, with the numbers; what you could not verify; anything
you changed from this brief and why; what you would do next; anything you noticed that I should know.

Thank you. Push for the stars.
