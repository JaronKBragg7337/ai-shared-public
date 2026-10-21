# 3D standards — Jaron's standing instructions for anything that renders

Written 2026-09-12 from his notes (originally for the space game; applies to every scene: Habitat,
the worlds, the fly scene, props). **Point every 3D brief at this file instead of re-pasting.**

## The fidelity block (verbatim — send this to the builder)
> ‼️‼️ Increase geometric fidelity. Improve silhouette readability. Add secondary and tertiary
> construction details. Ensure every component appears mechanically or architecturally assembled
> rather than booleaned together. Calibrate PBR materials with realistic roughness variation, edge
> wear, decals, and anti-tiling. Validate real-world proportions and maintain consistent texel
> density ‼️‼️

## Measurements, not vibes
- Every asset is built from a **real description or measurement** of the thing it is. If it is a box,
  there is a description somewhere of how that box is made; if it is a planet, NASA's numbers
  (gravity, poles, size). Transfer the measurements into the model. Same principle as the fly:
  anatomy, not a shape.
- **CC0 textures** only, wrapped in the colours the object actually has.
- Detail to the micro level. Props from Tripo/Meshy (rigged, game-ready) rather than hand-built
  primitives; primitives are placeholders and must be labelled as such.

## Every asset has an ID; every world has a grid
- Each asset carries an **asset ID**. Each planet/world has **longitude/latitude** (a grid).
- **Debug layer**: a button in Settings toggles a layer that shows the grid and a floating bubble
  over each asset with its ID and coordinates. Rustfall has a small version; it needs to be bigger
  for the space game. Purpose: Jaron can say "asset 4127 at (lat, long) is wrong" and the builder
  knows exactly what and where.
- The goal is to **not need to debug by hand**: scripts detect collisions / walk-through-walls /
  misplaced doors. (This is also the NPC-fly job — research/FLY-BRAIN.md.)

## Mobile first
- Runs on a phone and a laptop. Analog stick to walk, **invisible unless the left side of the screen
  is being pressed**.
- Load budget: interactive in < 3 s after assets are cached.

## Honesty on screen
Anything derived from real data says so; anything chosen or placeholder says so. Never invent a stat.

## Jaron's full template (verbatim, 2026-09-12) — swap the domain words per project
Originally for the space game ("NASA"); for a woodworking game swap in lumber companies / blueprints;
for the fly it is flybody. **The first line is the rule that saves the most usage.**

> Look for open source items, scripts, assets etc.
>
> Make it mobile friendly. Controls for analog stick to walk but have it invisible unless pressing
> screen on left side.
>
> ‼️‼️ Increase geometric fidelity. Improve silhouette readability. Add secondary and tertiary
> construction details. Ensure every component appears mechanically or architecturally assembled
> rather than booleaned together. Calibrate PBR materials with realistic roughness variation, edge
> wear, decals, and anti-tiling. Validate real-world proportions and maintain consistent texel
> density ‼️‼️
>
> Measurements. Every asset needs an asset ID and every planet needs longitude and latitude — a grid.
> A button in Settings toggles a debug layer: a floating bubble shows the grid and each asset's ID
> (Rustfall has a small version; the space game needs it bigger). If I see a collision or something
> not right, I give my coordinates and the asset ID and you know exactly what and where. The goal is
> to not need to debug, because scripts detect collisions — that is very important.
>
> Each asset should be detailed to the micro aspect. Use CC0 textures and wrap assets in the colours
> the object actually has. Use open-source information — NASA planet data (gravity, poles), real
> measurements of real assets. If it is a box, there is a description somewhere of how that box is
> made; if it is another object, there are measurements — transfer them into the 3D world. Hosted on
> heartbeatobservatory.com.

**Why (his words):** *"How something looks is really what makes people care to even look at it."*
*"If it's open source for something else, take what is open source, fill in the blanks, put it together."*
(Blueprints from a lumber company are measurements; measurements are all a 3D world needs.)

## Applied to the fly (2026-09-12 19:00)
**flybody** (TuragaLab/flybody, Apache 2.0) ships 85 measured OBJ meshes — head, thorax, 8 abdomen
segments, every leg segment, wing membranes, antennae, ocelli — plus `drosophila.blend` and a MuJoCo
XML with the joint tree. That IS the open-source asset. No Meshy/Tripo fly. Convert to one `fly.glb`
with the joint hierarchy preserved; wings/legs are then real joints, and the same file is what MuJoCo
drives later when a retired fly walks off the table.
