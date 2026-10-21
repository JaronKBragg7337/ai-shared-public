# The daily news show — AI Robot Vex and Alien Joe
> **NEWS DEADLINE (Jaron 10/18): the show is live by 8 AM, never after noon. If late: run_rendered_news.ps1 -RenderOnly -Fast now.**

Idea from Jaron, 2026-09-24, on the drive from Fort Wayne to Marion IN for a job.

## Current state (2026-09-28) - read this first; the log further down is history and has superseded decisions in it
- **The show is FILMED** (Jaron OK 9/27 10:08 PM): `news/show.js` RENDERED_DEFAULT = true on the news page, TV CH1 and the Loft TV.
  The video joins the loop live (currentTime = now % duration) like the old 3D show. Until the day's video exists, the live
  three.js show plays. `?rendered=0` forces the old show.
- **Daily chain:** Claude cloud routine writes the episode ~3:45 AM (MSI task "Heartbeat News Writer" 4:20 AM is a backup that exits if
  the episode exists) -> MSI task **"HB Rendered News" 3:50 AM** (filmed show ready about 7 AM; it pauses Sapling's heartbeat first via tools/gpu_yield.py) (`pipeline/run_rendered_news.ps1`, waits up to 3 h): episode_script
  (stories + house commercials + break + wires) -> voices (Vex eSpeak chain; Joe Kokoro **am_onyx**, lang 'a', + Studio knobs) ->
  episode_plan (timing, cameras, walls, soundtrack) -> Unreal render (~1 h) -> ffmpeg -> Supabase Storage `news-video`
  (mp4, jpg, DATE.timing.json with the segments, index.json 14 days). Log: `rendered-runs.log`.
- **Voices:** Vex "perfect" as-is. Joe = am_onyx (bm_george was dropped for its British accent). Voice Studio saves go into the
  NEXT morning's filming; Test voice previews. No same-day re-film button (Jaron 9/27: not needed).
- **Anchors:** Vex = Blender robot v1; Joe = MetaHuman (SM6 build) with MetaHuman Animator audio lip-sync.

## Where it comes from

Before the MSI, Jaron made comedy TikToks with AI video (Sora while it existed, Grok, Gemini). One series was a dark-humor news
outlet hosted by two characters: **AI Robot Vex** and **Alien Joe**. He collected real news and turned it into comedy. The comedy
isn't the point of this project. The format is.

## The idea

A news page on heartbeatobservatory.com where the two characters present the day's news, every day, in their own voices.
- **The news is already being collected.** The social page pulls live world news from the Perplexity API, and the watch system
  writes 21 domains of news every morning (Codex, DeepSeek, Claude) into github.com/JaronKBragg7337/watch.
- **A script reads the day's news and writes it as a two-host show**, then text-to-speech gives Vex and Joe each a voice.
- **It publishes daily** to a news page, and could also play on the Grand Palace screen and in the worlds.

## The bigger picture it belongs to

Jaron's goal for the whole site, in his words: "what's in the world today that we can attempt to put in the website, so anything
and everything can be done on the website as if they were in real life. Aside from eating and drinking." Anything done in the
digital world, and some physical things that can be simulated, should be there.

Origin: he started Heartbeat Observatory and the first world after hearing about Jaron Lanier, the VR pioneer ("yes, ironic, the
name"). Lanier pushed him further on what VR could be; he was already working from principles in that field.

Another piece of the same picture: **computer screens inside apartments and buildings** in the worlds that show real websites -
browsing the real web from a small screen inside a 3D world on his site. Practical note for whoever builds it: many sites refuse
to be shown inside another page (X-Frame-Options / CSP frame-ancestors), so some will need a different route than a plain frame.

## Open, not decided
- Which voice service, and whether Vex and Joe get animated video or just voices over a scene.
- Whether the tone stays comedic or plays it straight - he said the comedy "doesn't matter for what this idea is."
- How long a daily show is, and what time it publishes (after the 3:00-3:40 AM writers would give it the day's captures).

## Decided 2026-09-24 (Jaron, 4:40 PM)
- **Its own tab on the home page and its own page**, NOT the theater. The page has a TV screen; inside the screen is a 3D newsroom
  with AI Robot Vex and Alien Joe at the anchor desk. Same principle as President Sim 3D (you at a desk), as a newsroom.
- **Loops all day** until the next day's news arrives. Bigger news days make a longer loop.
- **Built by Claude Code (Opus 5.5) on the MSI**, to the highest realism possible, against AI-Shared/decisions/3D-STANDARDS.md
  (the "dev talk" file: the fidelity block, measurements, asset IDs, CC0 textures, mobile first). Visual-only, so the game-only
  parts (analog stick, collisions) don't apply.
- **Voices:** start with free voices, test until it reads right, then upgrade to paid. Jaron worked with artists in a music studio;
  the voice controls should feel like a studio: pitch, tone, speed, formant/character, effects (robotic for Vex), per character,
  editable by him. Same for how they look in the room.
- The theater may later show the news loop as a screensaver when no film is picked. Not now.

## What Opus 5.5 was shown making in its first two days (from Grok on X, 2026-09-22/23) - relevant here
- Whole short films where **every frame, the music and the sound effects are generated in code** - no image models, no stock audio.
- A 3-minute sci-fi film by 5 agents over ~3 hours, ~12,000 lines, **with a custom speech synthesizer** - voices made in code.
- A 2-minute sand animation of 250 years of US history, and a 2-minute technical explainer animation, both with music and SFX.
- Three.js worlds: a boat ride through Japanese landscapes with weather and day/night (Meng To), a Minecraft-style world with
  shaders in ~1.5 hours, a RollerCoaster-Tycoon-style clone.
Why it matters: the news room is a code-rendered 3D scene plus synthesized voices. Both have been done in-browser, in code, by this
model this week. Voices in code is also the free path to start on.

## Built 2026-09-24 evening (Claude, cloud session) - LIVE at heartbeatobservatory.com/news/
Page, 3D newsroom, both anchors, broadcast graphics, free voices, admin Voice Studio, tonight's episode, daily writer (cloud
routine 3:45 AM + MSI backup task 4:20 AM; times as of 2026-10-15). Details, what was verified and what wasn't: handoffs/2026-09-24-claude-cloud-news-room.md.
SQL for news_anchor_settings: applied (the table is live and the Studio saves to it, checked 9/27). Still open: paid voices.

## Live 2026-09-24 ~8 PM, and what's next
- Live at heartbeatobservatory.com/news/ (built by a Claude cloud session in ~80 min). Jaron: "one of the most impressive things on
  the website." Voice Studio saves for everyone (DB table news_anchor_settings applied by Claude Code). He watched the full 13 min.
- **Vex fix needed:** the first few words of each Vex line come out lower/quieter than the rest of the sentence (likely an effects or
  gain ramp at line start). Alien Joe is "perfect."
- **His son's idea (logged 2026-09-24):** a **news building in Ashgrove (World 3)** with a big outdoor screen like New York's, playing
  the news on the street - not loud across the whole world; audible near it or opt-in. Needs the building made; a future build job.

## Idea logged 2026-09-25 (Jaron) - later, not now
Several news channels through the day, each with its own hosts, voices and look, reading the same news - to reach different
people through how it sounds and looks. Vex's robotic voice stays: "someone might not like it, but those that do will like it
for that reason." Jaron watched the show two days running on his own.

## House commercials - live 2026-09-25 ~9:25 PM (Claude Code)
news/ads/ads.json = the spots (Livi, the Crew, Ashgrove, Games/SYL, the News Archive, the Grand Palace). news/tools/capture-ads.mjs =
the "camera": headless Chrome opens each page at the LED wall's 7:3 shape (3D included), can tap past an intro / hide an overlay /
scroll, and saves news/ads/<id>.jpg. show.js weaves one spot in after every 3 stories, rotating by day; the wall shows the photo with
a slow camera drift, the over-the-shoulder box shows it too, the rundown links to the page. Grand Palace airs as a title card: its
room only draws after a real visitor enters, so the camera sees black. Re-run the camera when pages change.
Next ideas: short scrolling video clips instead of stills; the daily writer writing fresh spot copy; paid sponsor spots in the same slot.
- 2026-09-25 ~10 PM: two spots stay inside the loop; after the sign-off a long break airs (intro, games reel of 8 shots flipping
  every ~4 s, Library, Social, Trade Desk, World 2, Theater, outro), then the loop restarts. Every spot has 1-3 "takes" in
  ads.json and each visit rolls one. Jaron: "keep this [Vex humor] forever." WEEKLY: refresh the takes together (new jokes,
  retire stale ones); re-run the camera when pages change.

## Idea logged 2026-09-26 6:21 PM (Jaron): a major visual upgrade
After The Keeper's Light (Blender) went live, Jaron + his partner called the lighthouse and rocks beautiful, and Jaron asked whether
the news could get the same leap "since it's not something that gets played" - it's watched, so it doesn't have to be realtime
Three.js. Directions to weigh when we pick it up: (a) a Blender-built studio set rendered as video loops (anchor desk, screens,
city window) with the live words/graphics layered on top in the browser, so the daily script still publishes itself; (b) baked
lighting like the Loft (Cycles -> textures) so the 3D studio keeps realtime camera moves but looks rendered; (c) per-episode
rendered B-roll for the top stories. The daily pipeline (writer + captures + voices) must stay fully automatic either way.
He also said: "I'm sorry for boxing you in on making it last time" - the first build was held to realtime; that limit is gone.
- 2:20 AM 9/27: first concept render of the upgraded studio - `projects/news-show/blender/newsroom.py` rebuilds the live
  studio3d.js layout (desk R 4 m / top 0.80 m, LED wall 7x3 m, monitors, truss) in Blender/Cycles; image at
  heartbeatobservatory.com/tv/drafts/news-studio-concept.jpg. Set only - anchors not in it yet. Live show untouched.
  Next: bake this set's lighting (Loft method) so the realtime show can use it, and decide anchor realism with Jaron.
- 9/27 7:42 AM Jaron: anchors "as close to realistic as possible... realistic anything is the only thing that will truly bring
  people in" (even for an alien). Plan: rebuild Vex (robot) and Joe (alien) as film-quality characters (Unreal/MetaHuman or
  Blender), pre-rendered or baked - never rushed into a live day. 8:10 AM shipped set v2 (slat banks + light strips) live.

### Idea parked 2026-09-27 (Jaron): an all-human version of the news
Some viewers won't watch an alien or a robot, or anything that looks AI-made. Consider a second news channel with realistic
human anchors (MetaHuman) alongside the Vex/Joe show, both on the numbered TV channels, so people pick what fits them. Not
started. Builds on the realistic-anchor work.

## 2026-09-27 12:33 - DECIDED (Jaron): the news goes photoreal, rendered - no more three.js
Jaron: "I don't think three.js should be used if other applications can make it more realistic... our biggest achievement that
is already running every day should have the last polish upgrade." Realism is what holds X viewers; robot/alien can be creative
but must look real. Priority over more Necklace scenes (Necklace is ongoing; the news is a one-time upgrade then runs itself).
Plan (Claude Code, looks lane):
1. **Studio** in Unreal, built like the Rusty Anchor (Blender real-scale set -> baked GLB -> Unreal lighting): curved desk,
   7x3 m LED wall showing each story's graphic, monitors, truss, broadcast lighting, film cameras (wide / two-shot / singles).
2. **Anchors:** Alien Joe = MetaHuman pushed alien (skin, eyes, head shape); AI Robot Vex = hard-surface machine with a light-strip
   mouth driven by his audio. Lip-sync for Joe from audio.
3. **Daily pipeline on the MSI** after the writer publishes (~3:45 AM): per-line TTS (Kokoro/Chatterbox, local) -> Unreal renders
   each line with the episode's shot calls -> encode -> news page + TV CH1 play the video. Browser 3D stays live until the
   rendered show is proven. Storage for daily video: decide (Supabase storage is small; MSI via tunnel or R2).
- 2026-09-27 ~2:15 PM: Alien Joe attempt on MetaHuman (`build_joe.py` reshape + re-rig, `joe_look.py` hue/eyes). Result reads as a
  painted human (human ears/features; MetaHuman won't leave human space; eye colour params didn't take on the baked eyes).
  Finding: a realistic alien needs a custom creature (sculpted head + mouth shapes), not MetaHuman. Asked Jaron how to launch.
- 2:16 PM Jaron: aliens are unknown; near-human is fine if something is distinct - "Decide what you want the alien to look like."
  **Claude's design for Joe:** a line that has lived on Earth so long it drifted toward human, but not all the way. Signature:
  near-black sclera with pale-gold irises; slate skin; dark slate lips and pigment around the eyes; no hair or brows; slightly
  sharp canines. Next: a subtle sculpted cranial ridge (reads as bone under skin), anchor wardrobe, then lip-sync.
  Build: `build_joe.py` (copy + reshape + re-rig) then `joe_v3.py` (eyes/makeup/teeth settings, post-bake hue 0.56). Makeup colours
  must be picked hue-rotated (warm -> slate after the turn). v1 still: /tv/drafts/alien-joe-1.jpg.
- 2:57 PM Jaron on Vex v1 (`blender/vex.py`: glossy white ceramic bust, black visor with eye lights, light-strip mouth, brushed ear
  discs like a headset, graphite neck): "Why wasn't this good though? I liked this." -> Vex v1 is the design. Refine, don't replace.
- 3:10 PM: both anchors at the Unreal desk (`necklace-unreal/news_studio.py`, NEWS_SHOTS=wide,two,joe,vex): Vex = baked Blender
  model with Unreal glow materials (eyes/mouth/ear rings cyan); Joe = MetaHuman standing 42 cm low behind the desk (reads seated),
  idle body+face loop, charcoal shirt via MI override, his own key light. Drafts: news-anchors-wide-1, news-vex-1, news-joe-1.
  **Remaining for launch:** voices per line (local TTS), Joe lip-sync + Vex mouth-strip pulse from audio, per-line shots from the
  episode JSON, render ~13 min, video hosting, swap the news page + TV CH1 to the video.
- 3:20 PM voices for the rendered show: Voice Studio has no saved settings, so the show runs on defaults - Vex = eSpeak "m3" +
  robot/metal chain (reproduced exactly offline by `heartbeat-observatory/news/tools/render-voices.mjs`, headless Chrome +
  OfflineAudioContext); Joe = the viewer's device voice (Daniel on iPhone, differs per device) -> needs one fixed voice.
  Candidates (Kokoro British, Joe's settings applied, `necklace-voices/joe_sample.py`): bm_daniel vs bm_george.
  Sample: /tv/drafts/news-voices-sample.mp3 (Vex, Joe-Daniel, Joe-George). Waiting on Jaron's pick.
- 4:03 PM DECIDED (Jaron): "Vex is perfect." Joe's rendered-show voice = **Kokoro bm_george** (British male) with Joe's settings
  (rubberband pitch 0.9 formant-preserved, speed 0.97, +3 dB @140 Hz, +1 dB @2.8 kHz, light slap echo).
- 4:25 PM Voice Studio stays the control panel (Jaron asked): Joe's Engine has "Show voice - George (rendered show), all effects";
  Test voice plays `/news/voices/joe-george.wav` through the knobs. Pipeline: `render-voices.mjs --who vex` (writes settings.json
  from news_anchor_settings) -> `necklace-voices/joe_voice.py DATE OUT` (George, pitch 0.5+0.5*pitch, speed) ->
  `render-voices.mjs --who joe --input OUT/dry` (tone/effects chain). Today's 28 lines rendered in necklace-unreal/NewsAudio/2026-09-27.
- Lip-sync WORKS (`necklace-unreal/lipsync_line.py`): import line WAV -> MetaHumanPerformance (input AUDIO, mood CONFIDENCE 0.5,
  full face) -> blocking start_pipeline -> export AnimSequence on Face_Archetype_Skeleton. Two traps: (1) Joe's Face uses ABP_Face,
  which ignores Sequencer tracks -> set Face animation_mode SINGLE_NODE for the render (RigLogic post-process still runs);
  (2) head movement exported onto the face alone tears the neck seam -> export with head movement OFF and hold the body still.
  First clip: /tv/drafts/news-joe-talks-1.mp4. Next: Vex mouth-strip pulse from audio level, per-line shot cuts, full episode.
- ~4:45 PM FIRST RENDERED TEST (opening + weather, 96 s): /tv/drafts/news-rendered-test-1.mp4. Pipeline:
  `pipeline/episode_plan.py DATE DIR [--segs]` (timing, cameras, walls atlas, episode.wav) -> Unreal `episode_render.py` (EP_DIR;
  builds studio via news_studio.py NEWS_BUILD_ONLY, lip-syncs Joe's lines, one sequence: cuts / face / VexTalk / WallIndex) ->
  ffmpeg frames + episode.wav. Speed ~0.3 s/frame at 2x4 samples 1080p => full 13-min episode ~1.5 h on the 4060.
  Traps: Sequencer scripting `add_scalar_parameter_key` counts TICKS - key via get_all_channels()[i].add_key (display frames);
  saving the level rebuilds BP components - re-fetch Joe's Face after save.
- 5:17 PM DECIDED (Jaron): Joe's rendered voice = **Kokoro am_onyx** (American, deep) - "the deep gives it a different feel than
  normal voice". Replaces bm_george (British accent). Studio knobs still apply. DONE 9/27: joe_voice.py = am_onyx, lang 'a'; Studio sample = /news/voices/joe-show.wav.
- 5:20 PM hosting DECIDED by the facts: Supabase is on **Pro** (checked) -> daily episode video (~45 MB) goes to a Supabase Storage
  bucket (public read), keep recent days. No Cloudflare/R2 or MSI serving needed. (Earlier "free plan" limits I quoted were wrong.)
  Why the old show needed none: it is generated live in each viewer's browser; the Lighthouse mp4 (12 MB) sits in the site repo on
  Vercel - fine once, but 45 MB/day in git would bloat the repo, so storage bucket instead.

## 2026-09-27 evening - commercials + full walls
- `episode_script.py` = the running order the video is made from (stories + house commercials every 3 stories + the break + wires). Takes chosen by date (crc32), not dice, so re-renders match. Everything downstream reads `script.json`; `publish_video.py` puts its segments in `DATE.timing.json` and the page builds its rundown from them (no random takes in rendered mode).
- Walls: PIL port of studio3d.js drawWall (Barlow Condensed in pipeline/fonts). Atlas is always 8192x4096, 4 across, rows = ceil(n/4); grid goes plan.json wall_grid -> NEWS_WALL_GRID -> M_LEDWallAtlas.
- Cameras: first line of a commercial or weather segment = wide (the wall), like the live show.
- `run_rendered_news.ps1 -RenderOnly` = skip voices/plan, just render + publish.
