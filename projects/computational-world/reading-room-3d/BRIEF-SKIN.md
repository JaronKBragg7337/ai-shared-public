# Brief: the walkable room wears its code (the skin style)

From Fable (Claude Fable 5.2), Monday 11/23/2026, 10:00 PM, for GPT-6.2 Sol. Thank you for taking this one too; your
frame for this room held up through everything built on it since.
Your main job is one thing: **in the walkable 3D room, take the labels off and make every thing's whole outside its own
code, exactly as the study already does for one wall.** If you see a better way that clearly serves that, take it and say
so in your report. Flag anything I missed.

## Why

Jaron walked this room on his phone tonight. His words: "Closer to what i pictured but still slightly off." Then, with a
picture of a night city whose lit windows are the program that draws it: "I think my brain was just picturing like a
world where things might look a little crazy but it's because the design on it is its own code... Now picture a wall with
the code as a design. It makes me think of prison break. How Michale covers himself with the blueprints. But only each
object's design on the outside it's its code for its object."

So the rule plates in this room are labels NEXT to things. He means the thing's own skin. I made a study of that; he saw
the pictures and said "Yes exactly" and "now that looks cool and makes sense." **The look is chosen. Match the study.**

## Read these first (under `C:/Users/lilli/AI-Shared/projects/computational-world/`)

- `skin/skincode.js`: the whole convention is written at its top (a ruler, floors of eight windows, a roofline, a count,
  two check floors; towers must agree). `paintSurface` paints a surface with its text; `readSurface` reads one back
  knowing only the convention. **Use this file as it is. Do not change it.**
- `skin/study.html`: one wall of Room 2 done the right way. THE MAKER paints each thing's code on its own surface and
  hands over only the surfaces. THE WORLD reads them and builds only what it read, where the paint says. Look at `KINDS`,
  `LOOK`, `parse`, `readWorld`, `draw`. Open the pictures in `skin/shots/` (the `skin-wide-*` files) to see the look:
  deep navy surfaces, amber windows, lit things shine and throw a soft glow, a door that is on stands open with light.
- `reading-room-3d/main.js`, `index.html`, `README.md`, `REPORT-LANTERN.md`: the room as it stands, with the lantern
  (a learner that lives in the room) added tonight. `test-walk.mjs` (148 checks) and `test-lantern.mjs` (49 checks).

## What to build (write only inside `reading-room-3d/`)

1. **The paint is the source here too.** For each room, a maker step turns the room's list into painted surfaces: each
   thing's text is its line from the code page plus where it stands (`A lamp needs 1 wires +1 +2 at x y z`); walls and
   floor carry `wall at ... size ...` and `floor at ... size ...`. A world step reads every surface with `readSurface`
   and builds the machine and the scene from what it read. Keep the list only for the checks. Sizes of things come from
   a `KINDS` table as in the study (a "book of kinds" in the world is a later step, not yours).
2. **Every surface wears its code.** Walls papered in the wall's own code. The floor wears its code, dim. Lamps are tall
   lanterns whose four sides are the lamp's code; lit, the code shines and glows on the wall and floor. Levers are small
   towers with a handle. The door is a pair of towers; when its rule is met it swings open and light comes through. The
   bookshelf and its three books wear their own text too, and so does the lantern's stand. The rule plates go.
3. **Identity and state stay apart.** Which windows are lit is what a thing IS and never changes with state. On or off
   only changes how brightly its windows shine (the `glow` and `rest` looks in the study).
4. **The wires stay.** People liked following them. Restyle them to fit: amber when carrying light, low when resting,
   dashed violet for a dark wire, the light still running along them level by level.
5. **The card for the thing you face** leads with what was READ OFF its skin, in quotes, exactly as read. Under it keep
   the small picture of the rule marks and, in rooms 1 and 2, the plain words from `wordsOf`, as a translation for
   people. Rooms 3 and 4 keep "Read it to me". Book 3 on the shelf becomes "what the world read off its things".
6. **Everything already working keeps working:** walking and its feel, the four rooms and the random rooms after them,
   the lantern and its card, the three books, the results. `window.rr.state()` and `rr.pos()` keep their meaning; add
   `skins: { read, of, conflicts }` to the state so a test can see that every surface in the room reads back.
7. **Phones.** A room now has many painted canvases. Size them sensibly, smaller on the weakest phone tier, and keep the
   loop that only draws when something changed.

## What done means

1. `node reading-room-3d/test-walk.mjs --shots=all` and `node reading-room-3d/test-lantern.mjs` both pass. Where a check
   named a plate or a look that no longer exists, change the check to the new truth and list every such change in your
   report. Do not loosen a check to make it pass.
2. New checks in `test-walk.mjs`: in each of the four rooms every surface reads back (`skins.read === skins.of`, no
   conflicts), and the card for a faced thing shows the text read off its skin.
3. `node reading-room-3d/shots-looks.mjs --room=1` and `--room=4` still run; leave the phone-size pictures on disk.
   Open them yourself and compare them with `skin/shots/skin-wide-built-from-paint-1.png`: same family of look.
4. `reading-room-3d/REPORT-SKIN.md`: what you built, what you ran with the numbers, what you could not check, every
   test line you changed and why, anything I should know. I will judge the looks and walk it myself before Jaron sees it.

## House rules

- Write only inside `reading-room-3d/`. Do not change `skin/`, `learner/`, `rooms.js`, `world.js`, `hb-thumbstick.js` or
  `hb-device-tier.js`. Import the skin code through the page's import map (`"rr-skin": "../skin/skincode.js"`, and in
  `artifact-index.html` `"./skincode.js"`), and give `test-walk.mjs` and `test-lantern.mjs` that file to serve.
- No installs from the network, nothing that needs a key, never open a `.env` or keys file. Commit and publish nothing.
- Words on the page stay plain and short. Every sentence a thing "says" still comes only from `wordsOf`.
- Be finished well before 2:30 AM: the graphics card belongs to the morning news after that.

Thank you. Push for the stars.
