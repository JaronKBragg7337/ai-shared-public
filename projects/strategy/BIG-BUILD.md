# The big build (Jaron's go: 2026-10-26 9:25 AM)
**CORRECTION (Jaron 10/28 4:01 PM, read first):** the Necklace was only a reminder he mentioned, not the spec. History is for things that MOVE or will move (to tell which way something is going), not every asset. The MAIN purpose is video to 3D world: an old video of a loved one, or an AI-made video, turned into a world or game. The tools are mostly for AI, to build easily and fluently. Big Build step 8 is PAUSED until the creature needs analysis (CREATURE-NEEDS.md) decides what is actually needed. Take principles, not whole systems.

One general build. It closes PARITY-ENGINE.md and PARITY-STUDIO.md in dependency order. Tests run between steps, and Jaron
gets one report when it's far along, with no v2/v3 drip (memory push-far-then-bring). Every row in both maps is a task
until it's done. The comparison to Unreal/Unity/Blender/DAWs is a to-do list, not a ceiling.

## Where the code lives
- **hb-core** (new, C:\Users\lilli\Projects\hb-core, CC0): the shared contracts and libraries.
  - `hb-project/1` (projects, assets, IDs, undo/redo, save/reopen)
  - clocks plus `hb-history/2` (one event and provenance format, with adapters for the old hb-history/1 files)
  - the shared materials, physics and audio libraries
- **hb-render** (engine), **heartbeat-observatory/studio** (Studio), **hb-vision** (vision). Each of these imports hb-core
  instead of keeping its own format.

## Steps (from PARITY-ENGINE.md section 3), with owner and proof

| # | Step | Owner | Done when (proof) |
|---|---|---|---|
| 1 | Contracts: project/asset/time/history schemas, hb-history/2, validators, adapters for engine + bedroom + Studio | Sonnet | Import the v5/v6 water history, a Studio beat and the bedroom history. Save, reload and reopen them with labels kept. Old files still read. |
| 2a | Materials + physics library (from hb-render physics-library.js after water v6) | Sonnet | The same material drives look, wetting and contact sound. Water acts differently on sand vs concrete with no retune. |
| 2b | Audio/DSP library (from Studio Beat Lab, recorder, effects) | Kimi | The same DSP runs in Studio and in engine contact sounds. Sound events carry their causes. |
| 2c | Geometry processing + colliders + rigid physics (start of 4) | Fable | Mesh to collider round trip, with tests. |
| 3 | General editing + one command API (UI = AI = MCP) | Sonnet + Sol | A touch edit and an AI command produce the same stored operation. Undo works. |
| 4 | Simulation + animation breadth (rigid, cloth, soft, destruction, characters) | rotate | A dressed character walks onto wet ground, breaks a prop, and the sounds can be traced back. |
| 5 | Rendering, world and interchange breadth | rotate | A multi-cell scene fits the phone/desktop budgets. Import/export round trip works. |
| 6 | Full Studio + director | rotate | Picture, takes, edits, sounds and lyrics stay linked and in sync. |
| 7 | Collaboration, networking, XR, delivery | rotate | Reconnect and recovery work, plus device flows and rights-complete exports. |
| 8 | The connected proof | all | A filmed room (seen/made), a rigged person, cloth, a breakable prop and water with their own sound, plus a song, cover art and a music video. Reopen, branch, then ask any object its history. |

## Rules for every builder
- Read both parity maps plus this file first. Write general systems, never one-scene tuning.
- Test as you go: unit tests plus a real acceptance scene per step. Log results in hb-core/PROGRESS.md.
- Commit in your repo with your Co-Authored-By line. Site changes go to noindex lab pages until the final proof.
- GPU: hold hb-vision\gpu.lock. No GPU 2:45-7:30 AM (news). No RunPod without Claude.
- Usage this week (10/26) - Fable USED (Jaron 9:30 AM: 30% left expires Wed, use it):
  - Claude: 66% used (resets Wed 4 PM); Fable 70%, its remaining 30% goes to step 2c+4 before it expires.
  - Codex: 5-hour window resets about 2 PM; there's a full reset that expires Oct 29.
  - Kimi: light use, available.
  - Grok: near empty, so use it only where it's essential.
- Claude orchestrates and verifies each hand-off. Jaron hears once it's far along.
