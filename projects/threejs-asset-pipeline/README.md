# Three.js asset pipeline - one object, three pages, one identity

Parked side project, not cancelled. Written down 2026-09-23 by Claude Code from Jaron's description; the idea itself is
two to four weeks older and was "touched on quite a few times" without being recorded.

## The idea, in his words

"Items moving from one page to another, all being manufactured like in factories, in real simulated worlds, from micro detail,
that get transported from one page, keeping that same aspect going, to another page, going through a factory, getting
upgraded, updated, whatever it may be, transforming it into the next part, and then going to another page where it would be
sold at a store - all while keeping the same asset ID." Each page is built to show what Three.js can actually do.

So: three pages on heartbeatobservatory.com, one continuous object.
1. **Made** - the item is produced at micro detail in a simulated world.
2. **Transformed** - it travels to a second page, passes through a factory, and is upgraded into its next form.
3. **Sold** - it arrives at a third page, a store, still the same item.
The load-bearing rule is continuity: the object keeps one asset ID and its history across all three pages, so it is visibly
the same thing that was made, changed, and sold - not three separate models.

## Why now is a good moment to remember it

The Three.js account on X has been paying attention to Jaron's work: it reposted one of his projects and liked a number of
others. His stated intent: show them things Three.js can do that they did not know could be done. This project is the one
built for exactly that audience. (Opus 5.5's first two days of public demos were mostly Three.js worlds - see
research notes for 2026-09-22/23 - so the tools just got much better at this kind of build.)

## What already exists toward it

- decisions/3D-STANDARDS.md - Jaron's standard that every asset carries an asset ID and every world has a lat/long grid,
  so he can point at "these coordinates, this asset ID" and an AI knows exactly what and where.
- world3 (Ashgrove town) already uses stable spatial asset IDs (e.g. B07-L1-R03-F02) that survive edits -
  state/fly-scene-build/world3/town/docs/DECISIONS.md D6 and STATE-AUTHORITY.md.
- The site has the neighbours this would live beside: /3DPrinterAsset/ (a 3D printer inside a 3D world), /worlds-lab/,
  the three worlds, and the games directory.

## Status and when it comes back

Side project. Jaron's order of work: the money system first, then a full baseline week with no side projects to see what the
system costs to run, then spend what is left on projects like this. When it comes back, the first real question is where the
object's identity and history live between pages (it cannot be localStorage alone if it must survive a page change from one
visitor to another), and that should be decided before any scene is built - same lesson as Ashgrove's D6.

## 2026-11-01: first step built - the Seam Room
Jaron brought it back as a room split in two: each half a real URL, walk across = page switch, see both sides. v1 at heartbeatobservatory.com/lab/seam-room/ (a/ + b/): a log carried A->B keeps its asset ID and history, shaped into a chair on B. seam.js is the reusable switch. Next open step = the one named above: identity/history server-side.
