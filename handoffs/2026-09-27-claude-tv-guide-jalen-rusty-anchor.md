# Handoff - 2026-09-27 12:15 (Claude Code)
Goal Jaron set: TV numbered channels + remote; Jalen's full look; Rusty Anchor set + Ep 1 first shot. All three shipped.

1. **Heartbeat TV guide (live):** every item numbered (2.1 Keeper's Light, 2.2 Necklace...); tap to play, no forced order.
   `tv/guide.js` feeds `/tv/`, the phone app (Guide button inside the embed) and the Loft (Guide on the TV bar; the room follows).
   Keeper's Light removed from Movies (tv_items row set rejected with a restore note). New channel ids need the tv_items.channel CHECK widened.
2. **Jalen:** SM6 rebuild at /Game/MetaHumansSM6/Jalen; hair S_Messy, stubble, natural brows, faded tee (`build_look.py`,
   `clothes_color.py`). Skin tone decided: medium mixed (don't change). Pictures in /tv/drafts/jalen-*.jpg.
3. **Rusty Anchor + shot 001:** `projects/necklace-film/sets/rusty_anchor.py` (Blender, real scale, baked -> GLB) ->
   `necklace-unreal/shot_ep1_001.py` (import, lights, Jalen, camera, MRQ). Outputs /tv/drafts/necklace-ep1-shot001.jpg + .mp4.
Next: Mateo (salt-and-pepper beard, weathered) beside Jalen for the conversation; dialogue with the locked voices + lip-sync;
more bar life (patrons, bartender); a 9.1 m Sea Serpent for the storm. Traps: see WHEN-IT-BREAKS "Unreal".
