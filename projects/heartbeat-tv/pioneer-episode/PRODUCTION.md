# Pioneer episode (Science 8.11) - production contract (Claude Opus orchestrating, 11/15 2:45 PM)

Jaron approved the movement test 2:31 PM ("perfect and funny as fuck"), Vex floating on his base is fine. Now the full episode.

## Fixed inputs (do not change)
- `script.json` - 15 scenes (text = captions). `voices/NN_LL_<who>.wav` - every line, already voiced (Joe = Kokoro Onyx + studio chain, Vex = show eSpeak chain). NN = scene index 0-14, LL = line index.
- `timeline.json` - THE CLOCK. Every scene's start/end (seconds and frames f0..f1 at 24 fps) and every line's start/dur/f0/frames on the episode clock. Total 443.3 s (7:23), 10,639 frames. `voices/dialogue.wav` = all lines placed on that clock.
- Scene places: studio = s01 s02 s10 s15; truck = s03 s09 s14; space = s04 s05 s06 s12; board = s07 s08 s11 s13 (boards are Claude's, drawn in Pillow).

## Who does what
- **Studio scenes (s01, s02, s10, s15): Fable** (owns the Joe/Vex rig from the movement test: movement/plan.py, build_test.py, mux.py).
- **Truck + space scenes (s03, s04, s05, s06, s09, s12, s14): space builder agent.**
- **Boards, source cards, captions, music bed, end card, final mix, vertical cut, publish: Claude (orchestrator).**

## Output each builder delivers, per scene
- `renders/<id>.mp4`: 1920x1080, 24 fps, H.264 (crf <= 18), NO audio, exactly (f1 - f0) frames for that scene in timeline.json. Frame 0 of the file = frame f0 of the episode.
- Lip-sync / Vex mouth light must line up with the line timings in timeline.json (line f0 minus scene f0 = local frame).
- Keep the bottom ~22% of the frame free of anything important: Claude burns captions there and puts a source card bottom-left on scenes that have a board.
- Write `renders/<id>.txt`: one paragraph - what is shown, what's an illustration vs to scale, known weak spots.

## Unreal: ONE editor at a time (8 GB card)
- Lock file: `UNREAL.lock` in this folder. Before launching Unreal (editor OR commandlet), create it exclusively with your name + time; if it exists and is younger than 90 min, wait and retry; delete it as soon as your Unreal process exits. Never kill someone else's Unreal.
- Sapling (other GPU job) is already paused for this; leave it paused. Hard stop: all GPU work done by 2:20 AM (news render owns the GPU 2:40-7:30 AM).
- Don't edit the daily news pipeline files (news_studio.py, episode_render.py, run_rendered_news.ps1 in their own folders); build on top of them in your own scripts in this folder. If you save the Newsroom map, the next news run rebuilds it anyway (news_studio.py destroys all actors first) - that is fine.
- Unreal project: C:\Users\lilli\Projects\necklace-unreal\NecklaceFilm.uproject (UE 5.8). Put your own levels/assets under /Game/Pioneer/.
- No commits, no pushes, no posting. Claude publishes.

## Science look rules (from SOURCES.md / SCRIPT-READ.md)
- Pioneer 10/11: hexagonal equipment bus (~1.4 m across), 2.74 m white high-gain dish facing Earth, two RTG booms (two SNAP-19 RTGs on each, ~3 m out), one longer thin magnetometer boom (~6.6 m from centre), plaque on the antenna support struts. Spin-stabilised (it slowly rotates about the dish axis).
- Heat views are false color and must be labelled on screen "false-color heat view (illustration)".
- The live truck is ours (Heartbeat News live truck: white van, red/blue HBN livery, roof dish). Fun, not real hardware.
- Distances are not to scale in the space shots unless the shot says so; that's fine, they're illustrations.
