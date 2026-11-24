# Map Briefing - build log

## 2026-11-22 (Sun) - first build, Fable 5.2

**What it is:** a vertical briefing where the map tells the story. A real 3D Earth, the camera flies to each place and lands,
the country outline glows, a marker / dashed ring / arc shows where, then a tag, a headline, one short line with one highlighted
phrase, a fact or quote card, and an end card with our H logo. Every line of text is from that day's Heartbeat News episode.

**One command, any date** (run from AI-Shared):

    node projects/map-briefing/render.mjs 2026-11-22            -> out/2026-11-22-vertical.mp4 (1080x1920) + stills
    node projects/map-briefing/render.mjs 2026-11-22 --wide     -> out/2026-11-22-wide.mp4 (1920x1080, same scenes)
    node projects/map-briefing/render.mjs 2026-11-22 --stills   -> stills only (about 20 s; check every story before the long render)
    node projects/map-briefing/render.mjs 2026-11-22 --draft    -> half size, 15 fps
    extras: --music <file|none>   --auto (ignore the hand-written board)   --fps 30
    python projects/map-briefing/sheet.py 2026-11-22            -> contact sheets of the stills

### Files
| File | Job |
|---|---|
| `render.mjs` | The command. Finds or builds the storyboard, starts a tiny local server, opens the scene in headless Chromium (playwright-core from tools/site-reel), steps time frame by frame, saves JPEG frames (each read back and compared), closes the browser and server, encodes with x264 veryfast / crf 21 / yuv420p / faststart (the news settings), then proves the mp4 against the frames. A damaged encode is thrown away and redone (second way = PIL decodes, raw RGB piped in, like the news fallback). |
| `verify_frames.py`, `raw_frames.py`, `sheet.py` | The proof step (decoded video vs rendered frames), the raw-pipe fallback reader, and contact sheets of the stills. |
| `scene.html` + `scene.js` | The look and the motion. Three.js globe + a 2D canvas for borders, glow, markers, rings, arcs, labels + HTML for type. `draw(t)` is a pure function of time, so the same date always gives the same video. |
| `board.mjs` | Safety net: builds a storyboard from the episode JSON with no AI (place list + every country name). Copies the episode's own words. |
| `boards/<date>.json` | The storyboard for a date (stops: camera, highlighted countries, markers, arcs, cards, sources). A hand/AI-written one wins over the automatic one. `boards/<date>.auto.json` is what the automatic builder produced. |
| `vendor/` | three.js 0.160 (MIT), `earth_16k.jpg` / `earth_8k.jpg` = NASA Blue Marble Next Generation, July, topography + bathymetry (public domain), `countries.json` = Natural Earth 50m countries (public domain), trimmed. |
| `music/bed.mp3` | Our own Studio beat (projects/music/beats/out/studio-rnb-68.mp3), played low-passed at 20% volume. |
| `data/` | Episode JSON cache + the raw Natural Earth file. `out/` = videos, stills, contact sheets. |

### Our look (not theirs)
Warm dark grade on the Earth (muted land, ink-blue sea), cream type, ONE amber accent, ember red only for strikes and fires.
Georgia serif headlines, Bahnschrift caps for tags and map labels, Segoe UI body. Story number chip + progress pips at the top.
A bright spark keeps travelling the highlighted border. No photos of people, no seals, no logos: people get a stripe flag
(only flags that are plain stripes are drawn) + name + role; things get simple line icons.

### Today's video (2026-11-22)
Nine stops from seven segments of today's episode: Hormuz tankers -> Bahrain strike claim -> Houthis fire at Riyadh ->
Kryvyi Rih (with the Zelensky quote) -> Sparta II in the Gulf of Finland -> missile parts in Poland (Rutte quote) ->
F.B.I. database probe -> El Chapo Isidro in Sinaloa -> Indonesia factory fire + Timor-Leste quake. About 90 seconds.
Storyboard written by hand from the episode's graphic stats: `boards/2026-11-22.json`.

### Honest "not there yet"
- **Sharpness on close landings.** Blue Marble is 500 m per pixel; we use a 16K copy. Tight shots (Bahrain, Hormuz) are soft.
  Fix: NASA's 86400-pixel tiles for a detail patch per stop, or a second map layer (Natural Earth relief) for close range.
- **Nobody has listened to the music bed** or watched the video at full speed with human eyes; frames were checked as stills.
- **Label placement is by hand** in the storyboard. The automatic builder puts one label under one marker and can collide.
- **The automatic builder is a safety net, not a writer.** It only knows ~90 places plus country names, shows one place per
  segment, and its headline is the strap clause. Tested on 11/22 only (7 stops, sensible), never on another date.
- **Arcs are schematic.** The Riyadh arc starts inside Yemen because the episode says Yemen's Houthis fired; no launch site
  is known. Same for the "Sinaloa" and "Bahrain" rings: the episode names no exact spot, and the marker says so.
- **F.B.I. marker** sits on Washington, D.C. (the bureau's headquarters); the episode names no place for the breach.
- No voice. No captions file. Not published anywhere.

### What it takes to run daily, after the news publishes
1. **Storyboard step (the only new thinking).** After the episode JSON is live, the news writer (Sonnet 5.5, named on
   purpose) writes `projects/map-briefing/boards/<date>.json`: pick 5-8 stories with a real place, copy the stat lines
   exactly, give each a camera spot, the country code(s) to light up, markers and one card. The shape is the 11/22 board;
   a short WRITER note with the schema + the rule "every line is the episode's own words, labels kept" is still to write.
   If that step fails or is late, `render.mjs` falls back to `board.mjs` by itself, so there is always a video.
2. **Check step.** `--stills` first (about 20 s), then a look at the contact sheet by a model that can see images
   (text overflow, labels colliding, marker in the wrong sea). Only then the full render (several minutes, Intel GPU, no RunPod).
3. **Scheduled task** on the MSI, after the news publish step in run_rendered_news.ps1 (never before 8 AM news is safe):
   `node projects/map-briefing/render.mjs <today>`; ntfy only on failure.
4. **A home on the site**, between News and TV as Jaron said: a page that plays the day's briefing + an archive, the mp4
   in Supabase storage like the news video. Then artifacts.json + a social post with the video (posts stay his call).
5. Nice next: per-story 10-15 s cuts for single posts (the timeline already knows each stop's start and end).

### Run notes (11/22)
- Frames: 2,712 at 30 fps, about 3 minutes on the MSI's Intel graphics (the NVIDIA card was busy; not touched). No RunPod, no Unreal.
- **MSI WARNING - files written during a render came out damaged, three times.** Run 1: one frame would not decode
  (8.27 s). Run 2: ffmpeg said "huffman table decode error" on the frames. Run 3: the mp4 decoded without any error but
  10 seconds of picture were blocky garbage. A side-by-side of a bad file and a good one made from the same frames
  showed the same size with **11 single bytes turned to zero** inside a 16 KB stretch. Eleven encodes of the same frames
  done by hand afterwards were all perfect. So the encoder is fine; something on the MSI zeroes stray bytes while the
  render is busy (same family as tonight's news "inflate returned error -3" on PNG frames). Cause NOT found (RAM, disk,
  Intel graphics driver, or something touching new files in AI-Shared are all open).
  What the script does about it: reads every frame file back after writing, closes the browser before encoding, encodes
  in the system temp folder, decodes the result and compares it with the rendered frames (`verify_frames.py`), copies it
  into out/ with a byte compare, and redoes a damaged encode up to four times. The final vertical file passed:
  "VERIFY ok 2712 frames, worst diff 1.26", zero frame rewrites, one encode.
  **Worth its own look: a memory test on the MSI, and the news pipeline has no such proof step.**
- Automatic builder (`--auto --stills`) tested on 11/22: 7 stops, right places, the episode's own lines (sheets in out/auto-test/). Stills only, no video, no other date.
- Wide 16:9 (`--wide`) rendered and proven too ("VERIFY ok 2712 frames"); a few map labels sit closer together than in vertical.
- Nothing published, nothing committed, no server left running. `data/bm_july.jpg` (27 MB NASA original) is git-ignored.

## HANDOFF (Fable 5.2, 11/22)
Done: scene, renderer, automatic storyboard builder, proof step, today's vertical + wide videos, stills, contact sheets.
Next, in order: (1) Jaron watches `out/2026-11-22-vertical.mp4` and says what he thinks of look, pace and the music bed.
(2) Write the short WRITER note for the storyboard step and wire it after the news publish. (3) Site page between News
and TV. (4) Sharper close-ups. (5) Find out why the MSI damages files under load.
