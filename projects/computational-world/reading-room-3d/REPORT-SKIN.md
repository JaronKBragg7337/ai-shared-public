# Reading Room skin report

## What changed

- A maker paints the room’s rules, positions, and building surfaces with the unchanged `skin/skincode.js`. The reader gets the canvases. It decodes them with `readSurface`, builds the machine from the rules it read, and uses the decoded positions and sizes to build the scene. The maker’s written text is kept for comparison. A small `KINDS` table supplies the sizes of things.
- The rule plates are gone. The room has navy walls with amber windows, a dim blue floor, four-sided lamp towers, lever towers with handles, and two coded door leaves that swing into a lit passage. The shelf, three books, bench, learner, and its stand each wear their own text. I carried the code into the passage and kept the ceiling’s windows especially dim.
- The original canvases are the textures. As a thing turns on, the renderer brightens the same windows and adds soft light on nearby surfaces. The wires still carry their pulses level by level. Bright wires glow amber and dark wires stay dashed violet. The door’s passage light appears as the leaves open.
- Cards lead with the exact decoded line in quotes. Under it are the small rule marks and the same `wordsOf` translation. Rooms 3 and 4 offer **Read it to me**. Book 3, **What the world read off its things**, lists the decoded lines with their positions. It can still rebuild the machine and replay the room’s history. The lantern’s learner still gets its marks from the same mind code.
- `rr.state()` now includes `skins: { read, of, conflicts }`. Each thing shares one canvas across its coded faces. Phones on the weakest tier get smaller canvases. I found that a three-pixel cell can put the decoder’s sample outside a one-pixel window, so every canvas leaves room for cells of at least four pixels. The scene still renders only when dirty.

## What I ran

| Command | Result |
| --- | --- |
| `node reading-room-3d/test-walk.mjs --shots=all` | 166 passed, 0 failed, 44 screenshots. |
| `node reading-room-3d/test-lantern.mjs` | 49 passed, 0 failed, 5 screenshots. |
| `node reading-room-3d/shots-looks.mjs --room=1` | 9 phone-size screenshots, no page errors. |
| `node reading-room-3d/shots-looks.mjs --room=4` | 9 phone-size screenshots, no page errors. |

WebKit and Edge each read **23/23**, **25/25**, **26/26**, and **28/28** surfaces in Rooms 1–4, with zero conflicts. The reduced-motion checks also passed on the forced low-memory tier. In a separate Edge run I round-tripped all four rooms and 12 generated rooms with the smallest textures, and confirmed that a surface with disagreeing towers was refused. I repainted a Room 1 door to use Switch 1 and move 0.2 m to the right. The running machine and doorway both followed the repaint. I also loaded Room 1 from the flat artifact entry point with its assets served locally.

I opened both sets of phone screenshots and compared them with [the wide study](../skin/shots/skin-wide-built-from-paint-1.png). I checked the same lamp at rest and glowing, both door leaves closed and open, the books, and the lantern looking at a skin. The walk screenshots sampled up to 119 draw calls and 1,454 triangles in both browsers. Those samples are from desktop hardware.

All 67 new PNGs opened at their expected phone dimensions and are in `screenshots/`. The older files with `plate` in their names predate this build.

- [Room 1 lamp at rest](screenshots/looks-iphone-webkit-room1-4-lamp-wall.png) and [lit](screenshots/looks-iphone-webkit-room1-8-a-lit-lamp.png)
- [Room 4 door shut](screenshots/iphone-webkit-room-4-door-shut.png) and [open](screenshots/looks-iphone-webkit-room4-7-the-way-on.png)
- [Room 4 shelf and books](screenshots/looks-iphone-webkit-room4-9-the-books.png)
- [The lantern looking at a lamp’s skin](screenshots/lantern-iphone-webkit-2-looking-at-a-skin.png)

## Test changes

| File and lines | Change and reason |
| --- | --- |
| `test-walk.mjs` 39 and `test-lantern.mjs` 32 | Serve the two new room modules and the existing `skincode.js`. |
| `test-walk.mjs` 306–311 | Name the translated card marks in the existing clean-start check. Add a separate count and zero-conflict check for every room. The count requires all rule surfaces and all 19 room and furniture surfaces. |
| `test-walk.mjs` 345–346 | Require the skin quote as well as the rule marks in Room 3 before the words are requested. Keep the hidden words and visible button checks. |
| `test-walk.mjs` 382–383 | Compare the lamp card’s leading quote against the expected rule and coordinates in each room. |
| `test-walk.mjs` 391, 394, and 401–402 | Name the lit lamp’s marks as a card. Rename the pictures for the skin, including the across-aisle view. Keep the two-squares, two-filled-wires, standing distance, and out-of-range card assertions. |
| `test-walk.mjs` 425 | Expect the new Book 3 title when tapping the third physical book. |
| `test-walk.mjs` 446–453 | Still compare all machine rule lines. Also require the lamp’s exact position, one distinct line per surface, and wall, floor, book, and stand lines. The following history replay assertion remains. |
| `test-walk.mjs` 500–507 | Force the smallest texture tier in the reduced-motion pass and check all 23 Room 1 surfaces. Keep the real lever taps and the no-wave, no-swing assertions. |
| `test-lantern.mjs` 186 | Rename the picture to `looking-at-a-skin`. The lantern assertions are the same. |

`shots-looks.mjs` now takes the resting and lit lamp pictures from the same viewing spot, adds a view of the three books, and exits with an error if the page reports an error.

## What remains to check

A physical phone still needs a walk to judge two-thumb feel, frame rate, and battery use. This was a local build, so live hosting and CDN loading were outside the run. The flat entry was checked locally and its required files are listed in `README.md`. All work and screenshots are inside `reading-room-3d/`.
