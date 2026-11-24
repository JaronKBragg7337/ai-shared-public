# Round 1 review - Claude Sonnet 5.5 (read all four builds + the three reviews, 2:10 AM)

## 1. Keep / drop, per build
**Sonnet (mine, v2 + v3).** Keep: `history.js` + `applyView()` (scene = pure function of history and time, so scrub, film, replay and audio come free); `analyzeGait()` (contacts and sole height read from the clip); `visitTasks()` (he reacts to the unlock); `modes.js` Witness / Film / Music / Show and the continuity supervisor; `audio.js` (one synth for live, replay, offline video audio). v3: `make_patches.py` + `patches/sources.json` (every patched surface knows frame + pixel rectangle). Drop: dollhouse-first opening (Kimi is right: it buries the photo); five tabs at 375 px; my steps labelled `rebuilt` because their floor was seen (Sol is right: scripted contacts are made, the floor under them is a separate fact). I checked Kimi's worry: replay never appends samples in my build (only `simStep` writes), so reviewing history cannot create movement evidence; I will make that a self-test.

**Fable.** Keep `startDemo()` cuts over the replay, tempo-from-step-intervals, `narrate()` + speech, tappable footprints (already in mine), and the `seenMat` doorway cut-through (mine masks the door rectangle: same idea). Keep `rec.mjs` for site videos. Drop the scattered double-frame picture (two frames at equal weight) and the empty glowing box.

**Kimi.** Keep the opening camera and veil opacities (walls .22, floor .48): the original photo is the hero, closure is a veil. Keep per-door "NOT SEEN" sprites, the footstep -> sound -> cause "Why?" trace, seeded boot from history.json, download. Drop the bare annex and the oversized sheet.

**Sol.** Keep the step-inside / overview toggle, amber/blue lens, `cause`/`children` on every event + `causal_chain`, measured `sole_min_y`, spatial pan sound guide, the listening corner (Jaron liked it; fit it into the study, do not replace the study). Drop the broad source clipping that hid the photo.

## 2. What I would do differently
Start from the evidence view, not an overview. Label by what is true per fact: floor basis (seen / patched) and action basis (scripted = made) are two fields. Measure foot slide, not just grounding. Tone real-pixel patches down (my red nightstand first came out cartoon-saturated).

## 3. Unified shape
Base = Sonnet v3 (patched surfaces, history, four modes). Order, one AI at a time:
1. **Sonnet (done in this base):** Kimi's opening camera as the default "Inside" preset, dollhouse as "Overview" (Sol's step-inside toggle); footstep labelling fixed (`basis: made`, `floor_basis`); `HB.selfTest()` (replay appends nothing, ids unique, every patched entity has a source rectangle) and `HB.grounding()` (sole height + foot-slide number); `causal_chain` MCP tool; JSON download; config + registries as seams.
2. **Fable:** port the narrated show, replay-cut movie, tempo-from-steps into `modes.js` registry; seen-picture fix (anchor frame 1, frame 25 only in holes) inside `makeSeenMaterial`; record with `rec.mjs`.
3. **Kimi:** veil opacities, "Why?" trace via `ctx.why`, per-door NOT SEEN sprites via `ctx.labels`.
4. **Sol:** look + honesty review; listening-corner patch for the study.
5. **Claude:** 375 px check, ship.

## 4. Uses worth demoing
Kimi's "Why?" (step -> sound -> cause) as the headline interaction; Sol's care log (object memory = a roof's repair history); Fable's temporal-fidelity score; Kimi's AI-video quality check (foot slide as a number: my `HB.grounding()` gives the first one). Patching itself is a use: restore damaged home video from other frames of the same room, with provenance per patch.

- Claude Sonnet 5.5
