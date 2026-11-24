# The Reading Room in 3D

Walk through four rooms where every thing wears its code in windows. Follow a wire across the floor to see what a flip changes, then walk through the door when it opens. On a card, squares say how much light a thing needs. Circles show where its wires come from and whether they carry light.

- On a phone, drag on the left to walk and on the right to look. Tap a lever or book to use it.
- With a keyboard, use W A S D or the arrows and drag with the mouse to look. E or Enter uses the switch or bookshelf you face.
- Walk up to a thing and look straight at it to read its card. Every card shows what was read from the thing's skin. The first two rooms add the rule in words. The last two count each use of “Read it to me.”
- The shelf has three books. They teach the marks, record your flips and show what the world read off its things. The code book can rebuild the room's machine and replay your changes.

## The lantern

By the start of every room a small lantern rests on a coded stand, asleep. It is the Path B learner from `../learner/`
(the same `learner/mind.js` that `learner/learn.mjs` measures). Face it and tap "Wake it", or tap the lantern itself.
It knows nothing about the marks. It glides to each thing and looks at its skin, flips levers, looks again, opens the door, plays a
few flips led by its own doubt, and goes through the door. Follow it and it carries on in the next room, keeping what it
learned. After the four hand-made rooms come rooms drawn at random, without end. The chip under the top bar opens what it
believes, worked out from its real numbers, and "Let it live 10 more rooms". While it is awake your own results for that
room are not kept. `node reading-room-3d/test-lantern.mjs` checks it (WebKit with full motion, Edge with reduce motion).

## Run it locally

From `computational-world`, run `python -m http.server 8000` and open `http://localhost:8000/reading-room-3d/` in a browser. The page uses the parent folder's `rooms.js`, `world.js`, `learner/mind.js` and `skin/skincode.js`. It loads Three.js r182 from jsDelivr.

For the automated walkthrough, run this from `computational-world` with the existing Playwright, WebKit and Edge installs:

```powershell
node reading-room-3d/test-walk.mjs --shots=all
```

The test serves files by intercepting browser requests, so it needs no running server. It uses the local Three.js r182 build if present. Use `CW_THREE_DIR` to point to another r182 `build` folder with `three.module.js` and `three.core.js`. Use `CW_PLAYWRIGHT_ROOT` for an alternate `node_modules` folder or `CW_WEBKIT` for an alternate WebKit executable. Add `--browser=iphone-webkit` or `--browser=edge` to run one browser. Screenshots are saved in `screenshots/`.

## Still to check

- The iPhone-sized WebKit run uses desktop hardware. Walking with both thumbs, rendering speed and battery use on a real iPhone still need a check.
- The automated run supplies Three.js locally. The public route, CDN load and direct clipboard write still need a live check after deployment.

## How the paint builds a room

The maker paints the rules, positions and room surfaces on canvases. The reader gets the canvases and decodes their
windows. Their text gives the machine its rules and tells the scene what to draw and where. Each wall has its own code.
Lamps and both door leaves use the same window pattern when lit and at rest. The floor and ceiling stay dim.

Run `node reading-room-3d/shots-looks.mjs --room=1` or `--room=4` to walk and save phone-size pictures.
`artifact-index.html` uses flat paths. Package it with `main.js`, `room-scene.js`, `room-skins.js`,
`hb-thumbstick.js`, `hb-device-tier.js`, `rooms.js`, `world.js`, `mind.js` and `skincode.js` in the same folder.

## The looks pass on the lit-window room (Fable, Monday 11/23/2026, after Sol's restyle)

Jaron: "I hope it still looks good. I haven't been a big fan of codex world builds." Sol restyled the room so every
thing wears its code. I read all of it, ran the tests myself, judged the phone pictures and changed three things:

- **One skin wraps a whole piece of furniture.** The restyle put the whole canvas on every face of every board, so a
  shelf edge 7 cm tall showed all its windows squeezed into blurred stripes. Now each board of the shelf, the bench and
  the lantern stand shows the part of the canvas that falls on it, at the canvas's own scale (`wrapped` in
  `room-scene.js`). A narrow post is slid sideways onto the towers, and a thin edge shows one whole row of windows.
  The skin reader now also reports where the towers stand (`span`), so the scene still takes nothing from the maker.
- **An iPhone gets the full-size paint.** The house tier file puts every iPhone in its lite tier (it reports four
  cores), and the restyle gave that tier canvases 0.58 times the size. This room is small (about 50 MB of painted
  surfaces at most), so a phone with WebGL 2 gets the full paint; only a phone that reports 2 GB of memory or less gets
  the small one. The walking test checks that path, and `shots-looks.mjs --cores=4` takes its pictures.
- **Paint is handed back between rooms.** A phone keeps a painted canvas's memory until the canvas is emptied, so the
  room being left empties its canvases before the next room is painted.

`window.rr.state().render` now also says which paint a visit got (`paint`) and how long the room took to paint, read
back and build (`madeMs`: 40 to 75 ms for room 1 on the MSI).

**Still not checked:** a walk on a real iPhone. And the lantern still learns from marks the page hands it; it does
not read the windows with its own eyes yet.
