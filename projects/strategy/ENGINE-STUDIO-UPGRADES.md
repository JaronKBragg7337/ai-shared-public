# Engine + Studio upgrades (Jaron approved 10/25 4:03 PM: "both should get the ones you said for both")

No Studio post until these move forward (Jaron 3:54 PM). Builders: Sonnet 5.5 / Sol 6.1 (looks + big builds), engine
scene writing stays Sonnet/Opus/Fable only. Phone-first: every piece checked at iPhone width before it ships.

## Render engine (hb-render, C:\Users\lilli\Projects\hb-render)
1. **Motion** - short clips, not just stills: camera moves + the fluid already simulates over time (--time). Output MP4.
2. **Change it by talking** - edit an existing scene ("make it sunset", "move the bottle left"): writer gets the current
   scene JSON + the change, returns a patched JSON, same seed. Not a fresh scene.
3. **Public gallery** - every render shows the words that made it; "remix" opens it with those words + scene loaded.
(Already queued from 10/21: unknown-word squiggle, game-world size meter, chunk-growing worlds.)

## Studio (heartbeat-observatory/studio)
1. **Voice effects** - echo, reverb, light pitch fix, per layer, on the phone (Web Audio, no upload).
2. **Song sections** - mark verse/chorus; repeat or move a chorus without re-recording.
3. **Post your song to the site** - a song page on the Music channel with the tip button (no login wall to listen).

## Where they meet
1. **Cover art** - type what the song looks like; the engine paints the cover.
2. **Music video** - song + engine scene (moving, once Motion lands) saved as a video to Photos.
3. **Sound for scenes** - the engine knows what's in a scene (water, wind, sand); the sound side scores it.
Shared base: both already save a **recipe** (Beat Lab recipe in the WAV/MP3; scene JSON + seed). One combined recipe
file = song + scene together.

## The third engine (Jaron: "it's another engine... like the studio, like the engine")
His to find. Sparks offered 10/25 (not decisions): a motion/performance engine (people that move and act), a
time/director engine (puts picture + sound in order into a story), a world/rules engine (what things do when touched).

## Jaron's picks (10/25 4:07 PM)
- **Motion engine + director engine: both, "too much sense not to have."** World/rules engine comes after the rest is here.
- Studio, his additions: **edit your own voice recording**, not just beats (cut, move, fix a part, effects per take);
  **tap a spot on the track and drop in extra beats/sounds** (one-shots, drum hits, effects placed on the timeline).
- Started: Sonnet on engine Motion clips (4:08 PM). DONE ~5 PM (hb-render bc0c55f, tools/clip.mjs).
