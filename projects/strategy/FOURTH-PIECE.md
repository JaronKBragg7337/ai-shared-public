# The fourth piece (Jaron, 10/25 ~5 PM) - "every object can tell its own history"
**CORRECTION (Jaron 10/28 4:01 PM, read first):** the Necklace was only a reminder he mentioned, not the spec. History is for things that MOVE or will move (to tell which way something is going), not every asset. The MAIN purpose is video to 3D world: an old video of a loved one, or an AI-made video, turned into a world or game. The tools are mostly for AI, to build easily and fluently. Big Build step 8 is PAUSED until the creature needs analysis (CREATURE-NEEDS.md) decides what is actually needed. Take principles, not whole systems.

Found in a ChatGPT conversation Jaron shared by link (5:19 PM). His ideas below, in order; ChatGPT helped name and
research them. Jaron: "probably the most important conversation I shared in a bit." The other planned upgrades
(ENGINE-STUDIO-UPGRADES.md) stay - this is what they were missing.

## How he got there (the chain, all his)
1. **Orbeez water** -> he noticed his superpower: describing what's wrong by comparing it to something familiar.
   That's a design spec, not a vague complaint.
2. **Bring back the ‼️‼️‼️ Dev Talk bracket** (ChatGPT, Aug 2-18 2026, from his game work: "when I say something looks
   fake, investigate why, rank causes, explain plainly, fix highest-impact first"). Add **temporal fidelity**: not just
   "does this frame look real" but "does the motion stay believable over time" - momentum, continuity, timing, cause
   and effect, the feeling of movement.
3. **AI doesn't really watch video** - it samples frames (Gemini default 1 fps), so it misses the flow between frames.
   Our engine doesn't have to watch: it can record what actually happened.
4. **Grid IDs + asset numbers, but for time.** His old game system gave every object an ID and a grid spot (WHERE).
   Now: give movement an identity - each drop gets an ID, a path line, speed, where it hit, what it split into (WHAT
   HAPPENED, over TIME). CSI / Criminal Minds trajectory lines.
5. **That's The Necklace.** His childhood superpower and his book: touch anything and see everything it has seen.
   In a simulated world we can actually build that: select any object and replay its recorded history.
6. **Product: upload a video, step inside it.** The engines rebuild the place and how things moved, as a 3D world you
   can walk around in VR/AR - e.g. a moment with a loved one who's gone, from a video someone recorded. A real
   moment, not an AI avatar inventing new words.
7. **Assassin's Creed memory fade.** What the video clearly shows = solid. What we rebuild from evidence = marked as
   rebuilt. What was never seen = fades into pixels like a memory. "We don't try to fix everything if we can't, but we
   at least fix part of the moment." Honest by design. More videos of the same place = more of it turns solid.

## What it is, in one line
A shared **event history** under everything: IDs + time + position + what happened + what it caused. The render engine
records it, Sapling reads it and explains "why did this happen", Studio already works this way with sound (every hit
and vocal is an event on a timeline). The fourth piece isn't another engine beside the three - it's the memory they
all share.

## Honest walls (Claude, 10/25)
- **The render engine half is close.** The fluid sim already knows every particle's position and speed every frame;
  recording paths + collisions is a small build. Showing them as trail lines would have shown the orb bounce instantly.
- **Video -> walkable 3D of real people is research-grade** (Shape of Motion, World Labs Marble, NVIDIA World from
  Motion, 4D Gaussian splats). Rooms are doable now; moving people from one phone video is the hard part. The MSI's
  8 GB GPU won't run the big people models; that's a rented-GPU job (RunPod, terminate every pod).
- **People in someone else's video:** the uploader decides for their own memories; never generate new speech or
  actions for a real person, never use it on someone without the family's say.

## First test (proposed)
"Necklace view" in hb-render: give every water particle an ID, record its path through the bottle clip, draw trails +
collision marks over the video, click a drop to see its history. Then hand that event log to Sapling (when it's back)
and ask it why the water moved the way it did.

## Jaron's follow-up (5:24 PM)
- **"It doesn't need a big model or a big GPU - it needs the right scripts/tools to analyze movement and objects."**
  Mostly right; my "big GPU" wall was too strong. Our own engine needs no model at all (the sim already has every
  path). Real videos: classic, scripted computer vision runs on the MSI - camera + room from video (structure from
  motion, e.g. COLMAP), movement lines (optical flow / point tracking), people as body poses (MediaPipe-class), small
  object detectors. Only the newest "rebuild a full moving person" neural models want big GPUs, and the memory fade
  covers what the scripts can't get. Start with scripts; reach for big models only where a script truly can't.
- **Sapling's real role here = a reminder: make it AI-accessible.** Sapling is far behind (Kimi + RunPod credits over
  $10), so it isn't the piece to wait on. The point is any AI - Claude, Grok, ChatGPT through the MSI bridge, later
  Sapling - can ask the event history questions. hb-render already has an MCP server (render_scene / job_status /
  list_scenes); the event history gets tools there too, e.g. `trace_object` (one ID's full history) and
  `events_between` (what happened in a time window). Sapling plugs into the same door when it's ready.

## Jaron's test idea (5:29 PM) - he's the test subject
- Phone set down at a distance; record himself walking side to side (far, a good distance), walking toward the camera,
  and other ways of walking. He was in it and it's his memory, so he can say what's right and what's missing.
- Upload from his phone to the MSI the way Key Drop works ("Video Drop": a page on the site -> Supabase storage ->
  an MSI script pulls it down).
- **Skeleton:** take a clear frame (hands, elbows, knees visible), mark the body points by hand, and teach/check that the
  system finds those points no matter which way he's facing. Then build the rest on top.
  Note: ready-made pose finders (MediaPipe-class, 33 body points, any facing, runs on a phone CPU) already do the
  finding; his hand-marked frames become the answer key that grades them, and the place we add what they miss.

## Added from ChatGPT's read of the plan (Jaron shared 5:33 PM) - agreed
- **Two separate test tracks, one shared format.** (1) hb-render sim: trails are checked against the true simulated
  states (known answer). (2) Real uploaded video: movement is estimated, checked against Jaron's hand-marked frames and
  what he knows he did. Same IDs/timeline/format; never claim equal accuracy.
- **Memory fade for the skeleton too:** each joint is seen (solid), estimated from nearby frames + body limits
  (dashed), or too unsure (shown as unsure, never faked).
- **Human-assisted fixes:** if tracking loses his elbow, he taps the right spot on a few frames and the tracker uses
  those to fix the rest of the clip.
- **First real-video deliverable:** Jaron walking across the frame with his tracked skeleton + path line drawn over the
  original footage. Prove that before any 3D room.
- ChatGPT's animated "one droplet, multiple paths" diagram (W-0427 hits sand, splits into W-0428/W-0429, dashed =
  predicted) is the look target for the Necklace view overlay Sonnet is building.

## First real video (Jaron, 5:38 PM) - 45 s, phone on the ground, outdoors, low angle
Sideways walk (~7-10 s) -> leaves frame (~11-15 s) -> re-enters + turns side-to-front (~16-22 s) -> walks toward camera
(~23-29 s) -> backs up gesturing (~30-35 s) -> arms down/out/up (~36-41 s) -> comes to the phone, partly out of frame.
He picked 9 screenshots (his keyframes); ChatGPT (now takes video) added 6 "between" moments. Agreed rules:
- **Human keyframes + motion-event keyframes, both** (speed/direction change, foot contact, joint hidden, leaves/enters view).
- **Out of view = don't invent a path** (memory fade); on re-entry, recover the SAME ID.
- Size change walking toward camera = depth, not growth. Good test: the low camera makes this hard.
Video still needs to come through Video Drop for the MSI pipeline (as of 5:45 PM, not yet).

## Spark (Jaron, 8:52 PM): Grok-made videos as test footage + the product's other half
Ask Grok Imagine for a video (a person doing what we need, the place), then use that one video for everything: the
skeleton tracker, the place rebuild, and the simulation. Same pipeline later lets anyone turn their videos/photos into
games and simulated places - the memories product and the games product are one pipeline, two markets.
Claude's read: yes, with one catch - AI video isn't physically true (feet slide, hands melt, rooms shift between
frames), so it's test footage, not an answer key for physics. Bonus: the tracker + event history can MEASURE where an
AI video breaks physics (a temporal-fidelity score) - the Orbeez lesson pointed at someone else's video. Generated
people = no consent issues, endless angles. No xAI API key on the MSI (10/25), so Jaron makes clips in the Grok app
and sends them through Video Drop (note "Grok-made").
- **First Grok clip (9:51 PM, 15 s, 1280x720 night lot):** tracked in 32 s. Person in view 59% of frames, joints 0.88
  (89% solid), turn at 7.1 s found, 15 foot contacts, path line clean across. Misses: the first second it latched on a
  far light cluster while the man stood at the left edge; weakest joint L_ELBOW 0.49 (arm on the far side); 4 short
  faded "ghost" skeletons after he left - the phantom guard refused all of them. Next: foot-slide check (does a planted
  foot move?) = first AI-physics measurement.
- **Jaron (9:54 PM): "best angle first, then map through."** Real uploads won't all have good angles. Find the clearest
  stretch of the video, read the person there, then carry that read forward and backward through the bad angles.
  Build as anchor frames: score every frame for clarity, take the best one(s) as the anchor, measure bone lengths
  there (they can't change), then use those fixed lengths + nearby frames to fill hidden joints - drawn dashed
  (rebuilt), never solid. Same idea later for the place: the clearest view of a wall anchors the rest.
- **Jaron's Grok 360 bedroom test (9:55 PM):** a 360 spin around a guy at a keyboard - things in the room changed as it
  spun. Confirms: AI video people look real, AI video ROOMS drift. Use for a room check: when a 360 comes back to
  where it started, does the room match its first frame? (loop check). For building places, trust the first view as
  the anchor and mark everything the spin changed as "doesn't hold up".
- **Grok room batch (10:14 PM):** 5 stills = 5 DIFFERENT rooms (each picture is a new room; can't be stitched).
  3 videos from one overhead still (dark wood floor, white bed, 3 stepped doorways on the left wall, tall windows):
  two push-ins (15 s, 25 s) where the room mostly HOLDS while the camera moves, and a from-the-bed view whose 3 doors
  in a row match the 3 doorways seen from above = the same room from a second angle. Usable for a room rebuild
  (camera moves, room stays = what structure-from-motion needs). Files: media/video-drops/2026-10-25/grok-room-*.
  No COLMAP on the MSI yet (pycolmap CPU install = next step).
- **Jaron's method (10:10 PM) - why the room held:** he fed Grok the overhead still back and asked "the view from me
  laying on the bed looking at the three door ways." Geometry checks out: pillows by the windows (right), foot of the
  bed toward the left wall = the three doorways. Small drift: the doorways look stepped/angled from above, flat in the
  POV. This is the anchor idea used for MAKING places: one anchor picture + ask for new angles of THAT picture =
  consistent views to rebuild from. A director-engine pattern: anchor image -> requested angles -> rebuild -> check.
- **Room rebuild #1 (10:24 PM, pycolmap 4.2.1 on CPU, 3 min):** hb-vision `room.py`. Both Grok push-ins placed 100%
  (50/50 + 30/30 frames), 14,487 3D points, error 1.20 px = the AI room held together while the camera moved. The
  from-the-bed view (20 frames) did NOT join: it barely moves and faces a wall the overhead shots never show, so
  there's nothing shared to lock onto. Fix: ask Grok for an in-between angle (walking from the bed toward the doors).
  Output: hb-vision/out/rooms/grok-bedroom/ (points.ply, view.png).
- **Jaron's game idea (10:18 PM): the faded door.** He picked this room BECAUSE it has 3 doors = 3 possibilities.
  The memory fade becomes a mechanic: a door the footage never saw stays faded, a door someone must "unlock". Same
  rule as the honesty rule - unknown is shown as unknown - but in a game it's a locked area, opened by new footage,
  a quest, or a story beat. Links the memories product and the games product again.
- **Solid room (10:35 PM):** sparse SfM dots read as "random dots" (Jaron). Added torch 2.6 cu124 + Depth Anything V2
  Small on the MSI 4060: per-pixel depth for one frame, pinned to the SfM room's real scale (1,060 matched points,
  3% median fit error). Result swings around as a solid 3D room; holes appear exactly where the camera never saw
  (inside the doorways, behind the lamp) = the memory fade showing up on its own. hb-vision room_depth.py.
- **Jaron (10:28 PM): add tools to slow down and zoom in for detail; MSI GPU or RunPod OK for tests.** Plan:
  slow-motion = frame interpolation (RIFE-class: makes real in-between frames, marked as made, not seen);
  zoom = upscaling (Real-ESRGAN-class) + auto-crop that follows the person/joint; both run on the 4060.
  Honesty rule: in-between/upscaled pixels are "rebuilt", never counted as seen evidence.
- **Slow-mo + zoom built (10:50 PM):** hb-vision `detail.py` - follows one joint, crops + upscales, 4x slower via motion
  interpolation; every frame stamped SEEN or MADE. Plus a planted-foot slide table.
- **Foot-slide result: Grok PASSES.** Grok walker median 3.0 in (14 plants) vs Jaron's real walk 3.1 in (15 plants).
  The ankle naturally rolls forward a few inches over a planted foot, so this check can't tell them apart - matches
  Jaron's eye ("literally looks like a real person"). Sharper next test: heel + toe points separately, and the foot vs
  its own shadow. Jaron (10:34 PM): skip his new video for now; his first real walk (IMG_9272) is the baseline.
- **All together - LIVE (12:15 AM 10/26):** heartbeatobservatory.com/lab/bedroom/ (noindex, unlinked; WebKit 375 px
  checked, all assets 200, 4.5 MB). Room = 2 depth-filled frames fused into meshes (scale from 0.9 m doorways, an
  assumption). Person = Hunyuan3D-2mini from the anchor (local, 4.7 GB VRAM, 25 s; no RunPod), photo-colored, 17-joint
  rig. Walk = thigh/knee swing measured from Grok's walk clip + procedural arms. Three doors = faded, padlocked, tap
  says "Locked - not seen yet". Weak: soft face/hands, torn lamps/nightstand on the right, approximate rig + door
  alignment, view limited to what the footage saw. Next: a Grok clip through one door -> that door unlocks.
- **Bake-off verdict (Jaron, 1:50 AM 10/26):** Sonnet top (computer-desk study behind door 2 beats Sol's listening room);
  Fable close but its seen picture "too scattered", made room under-detailed; Kimi's first room shows the most of the
  original picture (what he wanted) but weak second room; Sol best at making everything up but barely used the real
  picture. Sonnet + Fable both nailed game / movie / music / show.
- **Next (Jaron): "Photoshop" patching** - take pieces of the seen walls/items and patch the unseen parts with the room's
  own pixels. New honesty label PATCHED = made from seen pieces, placed where the camera didn't look; every patch knows
  its source frame/region (pixel-level Necklace). Sonnet building v3 in lab/bedroom-sonnet-v3/.
- **Jaron's look-back (7:08-7:10 AM 10/26):** the unified room crowds the screen (too much shows at once); sound didn't
  play for him (likely iPhone silent switch muting Web Audio - check). Something says "slow down and look back" to the
  water drops: an in-between he hasn't named yet. Claude's offered read (not decided): the water itself was left half-done
  when we jumped from "trails found the cause" to the Necklace principle; and the event history went ON the screen
  instead of UNDER it (quiet until tapped, like the Necklace). He's clear: everything was made for a reason - this is
  about where each piece goes now, not undoing it. Bake-off trade-off he named: one-job-per-AI would have reduced the
  overload, but all-do-everything surfaced pieces he couldn't have thought of. He's thinking it over at work.
  Hold the "post on all platforms" until he's sorted it.
