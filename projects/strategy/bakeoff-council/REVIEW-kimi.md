# Round 1 review — Kimi K3.1 Pro

## Fable
- Keep `cleanSeen()` (`index.html:308-319`): removing stretched and out-of-room triangles is a focused repair that preserves photographic evidence.
- Keep the event-driven presentation in `startDemo()` / `stepDemo()` (`index.html:480-549`): replay cuts, step-derived tempo, and generated documentary captions all read the same history rather than playing canned media.
- Keep tappable footprints linked directly to event IDs (`footprint()`, `index.html:364-369`); that is The Necklace at its clearest.
- **Drop:** the scattered opening composition and mostly empty, glowing box beyond D2. Also fold the separate `beatFromSteps()` control into one music mode instead of maintaining two tempo systems.

## Kimi (mine)
- Keep the opening camera (`HOME_POS` / `HOME_TARGET`, `index.html:144-147`): Jaron confirmed that it shows the most of the original picture. That evidence-first framing should survive every redesign.
- Keep `EventHistory.for()/story()` and the footstep → sound parent/child records (`history.js:37-50`; `index.html:242-247`): a compact, inspectable causal chain.
- Keep the readable object-memory panel and live JSON download (`index.html:255-260`, `279`).
- **Drop:** the oversized bottom sheet when it steals the room view, the bare blue annex, and the manual note pads. My replay also jumps back to live afterward; Sonnet’s continuous seek/play model is better.

## Sol
- Keep the listening alcove (`index.html:47`): specific furniture, acoustic-looking wall strips, seating, and a clear MADE label give the unlock a real payoff.
- Keep `advance()`’s deformed-sole grounding (`index.html:83-85`) and explicit simulated-contact wording; feet and honesty receive equal attention.
- Keep Sound guide: `spatialPan()`, navigation cues, footstep notes, and lamp pulses (`index.html:51`, `69-70`, `81`) turn history into another sensory channel.
- **Drop:** the aggressive source-mesh clipping and extensive replacement furnishings that leave barely any original picture. The dollhouse plinth is presentation, not evidence.

## Sonnet
- Use Sonnet as the base. `buildMadeRoom()` (`app.js:189-217`) is the best second room: desk, chair, books, rug, lamp, and window form a study rather than an effect.
- Keep `analyzeGait()` plus distance-driven gait (`app.js:291-309`, `361-370`), the reactive door visit (`317-324`, `400-402`), and full-history `applyView()` (`423-456`).
- Keep all four modes, especially Witness’s event-checked claims and Show’s five continuity checks (`modes.js:25-63`, `130-172`). `audio.js` already unifies live, replay, and offline sound.
- **Drop/change:** the high dollhouse-first framing and any generic box detailing that competes with the photograph—not the study or modes.

## What I would do differently
I optimized interface polish before the unlock’s emotional payoff. Next time: original image first, detailed destination second, then UI. I would also adopt Sonnet’s reactive actor and substantive history-driven demos instead of four smaller demonstrations.

## Unified build, in order
1. Start with Sonnet and its history/mode architecture; retain v3’s pixel patching with visible **PATCHED** labels and per-patch source history.
2. Restore Kimi’s evidence-rich opening composition; use Fable’s triangle cleanup only where patching cannot repair tears.
3. Keep Sonnet’s study as the canonical D2 room; add Sol’s listening corner and Fable’s fog-to-room reveal, all marked made.
4. Add Sol’s grounding check, Kimi’s causal-chain presentation/export, then retain Sonnet’s four demos with Fable’s optional narration.

## New uses worth demoing next
Fable’s **temporal-fidelity score** and **roofing/job-site repair history**; Sol’s **maintenance care log** and **spatial audio wayfinding**. The first two serve Jaron directly; the latter two already have credible tiny-demo foundations.
