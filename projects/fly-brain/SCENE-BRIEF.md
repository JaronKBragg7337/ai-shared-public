# The Flies — 3D scene brief (for Codex on GPT-6 Astra, fresh window; three.js on the MSI so it can run + screenshot)

**What:** a live 3D page at `/live-systems/flies/brain/` in the heartbeat-observatory repo (GitHub
connector → commit to `main`; Vercel deploys). Vanilla three.js from a CDN, no build step, same
look as `/live-systems/trades/` (dark, `trades.css` tokens). Must run on a phone.

**Why:** Jaron watched "Sherwood" (a fly at a 3D desk, live spike scatter, vitals) and said *"what
others have plus what we have is what matters."* Ours is the same idea with real, measured data
behind every pixel, and a public test of whether the fly is actually learning.

## The data (already live — nothing to invent)

1. **Atlas — load once.** `https://www.heartbeatobservatory.com/live-systems/flies/atlas.json` and
   `atlas.bin`. `atlas.json` = `{n, index[], region[], regions[]}`; `atlas.bin` = `n` float16
   xyz triples (0..1) in the same order. These are the **measured soma positions** of 140,024
   neurons from the MaleCNS v1.0 connectome. `region` codes into `regions`:
   `ORN` (nose) · `PN` · `KC` (mushroom body, 4,064 — the learning cells) · `MBON` · `PAM` (reward
   dopamine) · `PPL1` (punishment dopamine) · `DN` (descending/motor) · `other`.
   Render as a point cloud. Colour by region. Decode float16 in JS (a 20-line helper) or ask me to
   also ship float32.
2. **Live state — poll every 3 s.** Supabase table `fly_live` (public read, publishable key in the
   trades page). One row per fly: `fly` (`fly-1` / `watcher-1`), `mode` (`dry`/`live`/`watch`),
   `state` (title, player, side, score, period, sets, pts, price, dprice, spread, **valence**,
   seeds, kc, holding, cap, realized, mb_events, gain_mean, spikes_per_sec, mean_mv, fired_total),
   `fired` = array of **atlas positions** (indices into the atlas order) that spiked this tick,
   sampled to ≤ 3000. Light those points (brighter, bigger, brief fade). That is the brain thinking.
3. **Actions — poll every 10 s.** Table `fly_actions` (press / letgo / refused / reward / milestone)
   for a ticker. Table `fly_ground` for the watcher's smells if you want a second strip.

## Standards — only the parts that apply to a fly nobody steers
From `decisions/3D-STANDARDS.md` take: the **fidelity block** (table, net, paddle, fly must read as
real objects, real proportions: table 2.74 × 1.525 m, 76 cm high, net 15.25 cm), **mobile-first**,
**honesty on screen**, and a small **debug toggle** showing asset IDs so Jaron can name a wrong part.
Do NOT add player controls, an analog stick, or a grid — the fly is the player; a human steering it
would mean it is no longer the fly deciding. (Human possession of a fly vessel is a retirement-world /
game feature, not this page — see research/FLY-BRAIN.md "Possession".)

## The fly asset — use the measured one, do not generate one (Jaron's rule: open source first)
`git clone --depth 1 https://github.com/TuragaLab/flybody` (Apache 2.0). `flybody/fruitfly/assets/`
has 85 OBJ meshes (head_*, thorax_*, abdomen_1..8_*, every leg segment, wing_*_membrane/brown,
antenna_*, ocelli) + `blender_model/drosophila.blend` + `fruitfly.xml` (MuJoCo: the joint tree and
each mesh's parent body). Build **one `fly.glb`** that keeps the body hierarchy from `fruitfly.xml`
as node parents (so wings and legs rotate about their real joints): Blender is on the MSI — a headless
`blender -b -P` script that imports the OBJs, parents them per the XML, and exports glTF is ~80 lines;
or `bpy` from the .blend. Scale `0.1` as the XML says. Put it at `live-systems/flies/brain/fly.glb`
(< 8 MB; decimate if needed, keep silhouettes). Animate by rotating wing/leg nodes: wings up when
valence > +20, grooming (forelegs) when < −15, a foreleg tap on PRESS. If the conversion fails, say so
and use a labelled placeholder — do not sculpt one.

## The scene

- **The brain**, centre, slowly auto-orbiting (drag to orbit), point cloud coloured by region, fired
  points flashing. A tiny legend. Label the mushroom body — it is the only part that learns.
- **The fly**: a low-poly fruit fly beside/under the brain, idle animation; wings up when valence
  > +20 ("wants in"), wings down / grooming when < −15, still otherwise. When a **press** lands,
  a short "press" animation (foreleg taps). No desk, no keyboard, no coffee — this fly is on a
  table-tennis table. A small paddle is fine. Keep it light on a phone.
- **Vitals strip** (top): `valence` as a bar from −80 to +80 with the +20 / −15 lines; `sugar` =
  realized P&L since start; `spikes/sec`; `KC firing` (the sparse count — 20–200 is healthy);
  `cap $x / $y`; `mode` (DRY / LIVE / WATCH) big and obvious.
- **The match** (side/bottom): title, "smelling from <player> (NO @ 31¢)", score with the current
  set highlighted, price and its move since the last set.
- **Ticker** (bottom): last 8 actions from `fly_actions`, colour by kind.
- **Two flies**: a toggle or split — `fly-1` (the trader) and `watcher-1` (no hands, smells every
  table). Default to fly-1.
- **Is it learning?** — link to the existing `/live-systems/flies/#learn` tab; do not recompute.

## Honesty rules (put them on the page, small, bottom)
"Every dot is a measured neuron position. Every flash is a neuron that actually spiked in the
simulation this tick. The valence is read from the fly's own mushroom body. What is *chosen*:
the pairing of profit with dopamine, the mapping of a match onto smells, and the thresholds."
Never invent a stat. If a field is missing, show "—".

## What Jaron said about the future (for the animation designer)
*"A fly that could get so smart it stops making money and goes wandering around the 3D worlds
would be cool."* — build the fly so it could walk off the table later. Same rig, same brain: the
DN (descending) neurons in the atlas are literally the walking output; a fly that stops pressing
and starts walking is a fly whose DNa/DNp cells are firing instead of its press readout. Leave
a hook for that: expose DN firing as a number in the vitals even if nothing uses it yet.

## Done when
Page loads on a phone in < 3 s after the atlas is cached, brain orbits, dots flash in time with
`fly_live.at` updates, vitals and match match the trades/flies pages, and the honesty note is
visible. Commit to `main` (Vercel deploys); then write `handoffs/YYYY-MM-DD-codex-fly-scene.md` in AI-Shared.
Run the page on the MSI and screenshot it at phone width before calling it done. If float16 decoding is a pain, say so and Claude Code ships float32.
