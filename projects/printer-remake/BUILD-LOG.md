# World Printer remake - build log (newest last)

Brief: `BRIEF.md` (Jaron's words at the top). Worktree: `C:\Users\lilli\Projects\ho-printer` (branch fable52/printer-remake,
pushed to main). Live: heartbeatobservatory.com/3DPrinterAsset/ - old page kept at /3DPrinterAsset/classic/.

## Run 1 - Sat 11/21, 10:33 PM to 11:13 PM (Fable 5.2)

### Part 1 - the one flow, the printer, the shared yard (commit 55976e26)
- **`3DPrinterAsset/flow.js` is the whole idea.** A part is only a path the nozzle follows: layer after layer, each layer a few
  loops or lines of one bead (10 cm wide, 8 cm tall). There are no pre-made models. The mesh on screen is that bead swept along
  the path, and the printer on screen follows the very same points. Plain numbers, no three.js, so it runs in Node for tests.
- **15 parts, each shaped around what the flow repeats easily:** wall (a loop + a centre line), door arch and window wall (the
  opening closes in a pointed arch: each layer leans in, no beam, no support), curved wall, gable, pillar, slab, path strip,
  block, stairs, vault roof, dome, round wall, ribbon fence (one wavy line there and back), planter. 370 to 11,500 triangles each.
- **`app.js`:** a 24 m print yard with a gantry printer (rails, bridge, carriage, mast, nozzle). Pick a part, tap the yard
  (snaps to 30 cm; tap the top of a part to stack on it), Turn, Print here. The gantry travels there and lays the part in place;
  fresh bead is darker and dries. Orders queue up, so you can keep placing while it prints. Five materials. Slow / Normal / Fast.
  Remove mode: tap a part, Remove it (only the builder who printed it can - same rule as before).
- **Shared yard, no migration needed.** Same Supabase table `placements`, same world `printer-lab`, same anonymous sign-in and
  the same row rules. New rows are typed `flow:<part>:<material>`. The 12 old rows (July tests) are untouched and still show in
  the classic page; the classic page ignores the new rows and the new page ignores the old ones. Other builders' prints arrive
  live (realtime INSERT/DELETE) and are printed on your screen too.
- Old page moved to `3DPrinterAsset/classic/` (only its three.js paths changed to `../vendor/`). `vendor/` stayed where it is
  because /HeartbeatCenter/ loads three.js from it.
- **Starter build in the live yard** (10 rows added by SQL, placed_by empty so nobody can remove them by accident): a small
  sandstone house (door arch, window wall, two walls, clay vault roof), a path strip, a planter, and a lime tower (two round
  walls + clay dome). To clear them: `delete from placements where world='printer-lab' and type like 'flow:%' and placed_by is null`.
- A phone bug found and fixed before shipping: the action bar appears under the finger right after a tap, and the phone then
  "clicked" the new button by itself. The bar now ignores presses for 0.4 s after it appears.

### Part 2 - make your own part from the same flow (commit d75ac962) + small fixes (98e80744, 3b80eb2c)
- **"Your own" card:** six sliders (Sides, Width, Height, Lean, Twist, Waves) + "Closed top and bottom". It is the same
  loop-per-layer flow with the numbers left open, previewed live in the yard as you slide, printed and saved like any part
  (`flow:spin~sides~width~layers~lean~twist~waves~lid:<material>`; numbers are clamped when read back, so a bad row cannot break
  the page). A layer may only move 6 cm from the one below (about half a bead), like a real printer - the sliders cannot beat it.
- Beads now have a pressed-flat top and bottom with bulging sides (how a real bead sits), so leaning layers stay closed.
- Opening camera frames the starter house and tower (stands further back on tall phone screens). Remove button moved to the
  left so the site's phone tab does not cover it.

### Verified
- Local (Node): all 15 parts + 1,296 own-shape slider combinations mesh with no bad numbers.
- Local (Playwright WebKit, 390 px, touch): load, tap, print, stack on a slab, turn, queue of six, remove, own-shape sliders; no
  console errors; no sideways scroll. Desktop Chromium 1280 px: click, R to turn, Enter to print.
- **Live (WebKit 390 px, two separate visitors):** the 10 starter parts load; builder 1 prints a block and builder 2 sees it
  arrive; builder 2 is refused when trying to remove it; builder 1 removes it and it disappears for both. An own shape printed
  live is there for a fresh visitor after a reload. /classic/ loads with its canvas and no page errors.
  Last check 11:12 PM on the final build (`app.js?v=3d`): opens framed on the house and tower, own-shape panel clear of the phone tab.

### Not verified
- Small known flaw: the "Your own" preview first appears at the middle of the view, which can be on top of an existing part
  until you tap another spot.
- **A real iPhone.** WebKit on Windows is the closest check we have; frame rate, heat and Safari's bottom bar are unknown.
- Big yards. Each part is its own draw call with 370 to 11,500 triangles and there is no far-distance simplification yet. Fine at
  tens of parts; not measured at hundreds.
- Two-finger pinch/pan on a phone (OrbitControls default) was not driven by the test.
- The classic page was only loaded, not played, after the move.

### One test part left in the live yard
The live own-shape test (a clay twisted vase by the starter planter, row bc0a41de-e080-40d0-8604-eec48ffc8ce9) was left there on
purpose as an example. It belongs to a throwaway test visitor, so only SQL can remove it.

## HANDOFF (end of run 1)
Where it stands: the remake is live and is already the page at /3DPrinterAsset/. The old lab is one tap away ("Old lab").
Everything is in three small files: `flow.js` (recipes + mesher), `app.js` (yard, printer, controls, sync), `style.css`.
Test locally with `python -m http.server` from the worktree root and open `/3DPrinterAsset/?solo` (solo = nothing is saved).

Next, in the order I would do them:
1. Ask Jaron to try it on his iPhone - his feel for
   "smooth" is the real test. Ask Grok to watch a screen recording of a print for anything that looks fake.
2. **More shapes from the same flow** - the flow can already do them, they only need recipes in `PARTS`: a bench and a table
   (ribbon profiles), a tree (a trunk loop that splits into two, then four), road curve and crossing, a bridge arch, a chimney,
   steps that turn. Then vehicles: a hull and wheels are loops too. That is the road from "building parts" to "any asset".
3. **Draw your own loop** - let a finger draw the outline on the ground, and the flow stacks it. That is the fully open version
   of "Your own".
4. **Snapping to neighbours** (ends of walls, tops of walls for roofs) - today it is a 30 cm grid + stack-on-top only. This is
   the piece Build Mode (backlog Phase 7c snap sockets) can reuse.
5. **Realism passes:** a visible strand of wet bead under the nozzle, hose and cable chain on the gantry, sound (motor hum +
   extrusion), slight sag/wobble per layer, contact shadow under parts, trees/sky beyond the gravel.
6. **Big yards:** merge finished parts into chunks or simplify far ones; measure on a phone first.
7. Old rows: if Jaron wants the 12 July rows in the new yard, map their types to flow parts (wall, pillar, floor->slab,
   road-*->path, cottage->skip) in `fromRow`.
8. Housekeeping not done this run: artifacts page entry + social post with a clip (AGENTS.md "finish something made with our
   own tools"); backlog item L-PRINTER-REMAKE status; the old RUNTIME_SAFETY.md now lives in classic/.

## Run 1b - Sun 11/22, 12:15 to 12:30 AM (Fable 5.2) - Jaron's first iPhone try
Jaron (12:13 AM): "super freaking amazing". One bug, his words: "I couldn't pull the thing down after it's pulled up on the
printer lab" - the control sheet with the own-shape sliders covered the lower half with no way back. His screenshot also showed
the site's phone tab covering the Width value.

Fixed (site commit ceb41222, live as `app.js?v=3e`):
- The sheet has a handle at its top, 44 px tall, full width: **tap it** to put the sheet away or bring it back, or **drag it
  down / up**. It is its own strip above the sliders, so it cannot fight with dragging a slider, and the sheet still keeps clear
  of Safari's bottom bar. Put away, only the handle ("Show controls") is left: the yard still takes taps, shows Turn / Print
  here, and prints.
- The site's phone tab now sits at the top right under "Old lab" on this page (CSS in the page's own style.css; bubble.js
  itself is unchanged), so it is never on top of the sheet.

Verified (WebKit 390x844, touch, local and then LIVE): tap handle hides (sheet 404 px -> 55 px), tap again shows, drag down
hides, drag up shows, the Width slider still drags (1.0 m -> 2.3 m) with the sheet staying up, a tap on the yard with the sheet
away shows Print here, phone tab at 62-120 px from the top with the sheet starting at 440 px. No page errors.
Not verified: a real iPhone (the drags were driven as pointer drags, not real fingers); landscape.

HANDOFF stays as written above (next steps list unchanged). Jaron has started building in the live yard.
