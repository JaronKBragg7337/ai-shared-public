# Movement test reviews (Pioneer episode)

## 1. Fable review

Reviewed `movement/v1.mp4` (Opus's first render, 504 frames) frame by frame and checked the motion math; fixed `plan.py` / `build_test.py`, re-rendered three times (one fast low-res check, two full). Final: `movement-test.mp4` (1920x1080, 22.5 s, 540 frames) and `movement-test-phone.mp4` (1280x720, 2.9 MB). Frames: `necklace-unreal/Saved/MovieRenders/MoveTest_v3`.

### What was wrong in v1 (frame / time references are v1's)
1. **Joe's feet skated the whole time he walked (1.5-7.5 s and 9.8-16 s).** Measured from the clip data: a planted foot moved 25-50 cm/s on average, peaks over 100 cm/s. Cause: `speeds.py` picked the "planted" foot by height alone, but in this clip the swinging foot's ball passes only ~3 cm above the floor, so the swing foot (moving 4 m/s the other way) was averaged in. The speed profile dipped to 55-100 cm/s every step when the true ground speed is a steady ~190 cm/s (times play rate). Joe travelled about 20% too slowly for his legs, so every step slid backward. The 25-sample smoothing hid the dips but kept the wrong average.
2. **Turns added more sliding.** The actor was rotated around its own centre, so during every arc the planted foot (20-50 cm from the centre) was swept sideways.
3. **Joe's mouth never moved on his line (frames 374-480).** The line was played through `DefaultSlot` on `ABP_Face`, but that AnimBP has no slot (it is only a CopyPoseFromMesh node), so the track did nothing. Confirmed by face crops: lips closed on every frame.
4. **Vex leaned the wrong way.** Unreal roll > 0 tips his top toward his forward (+Y); v1 keyed `-lean`, so by the rotation math he tipped backward as he sped up. Bank sign was right.
5. **Vex was hidden behind Joe in the walk-and-talk (frames 256-322)**: he rode on Joe's far side, level with him, on a pure side-on camera.
6. **Vex's hover cone glared** (frames 334-504): white shell material with a 900-unit point light 6 cm away.
7. **Lighting / framing:** the floor lights pointed straight down (Joe's face black at the end, frames 364+; Vex's top blown out) and mirrored in the glossy floor as hard white slabs (frames 130-196). Wide shot far and dark; the tracking camera lagged half a second behind, cut the feet off and left the pair at the frame edge.
8. **Frame 0 shows a ghost of Joe's default arms-out pose** (motion blur before the first animation tick).
9. Smaller: clip boundaries were rounded to frames only inside Unreal (up to half a frame of drift against the math); the stop clip's section ran one frame past the clip (risk of wrapping to its first, mid-stride pose).

### What I fixed
- **Foot lock by position, not by speed (plan.py).** Every 1/120 s the actor is moved, and pivoted, so the planted foot's ball stays where it is on the floor, through straight walking, turns and clip blends. "Planted" = ball on the floor AND not swinging forward. By the math: mean slip 1 cm/s, 95% under 10 cm/s (was 25-50). Checked in the render on the static low camera: the planted foot holds the same pixel column frame after frame (final frames 105-108; fast check frames 112-129).
- **Turns pivot on the planted foot**, and the turning is weighted toward late stance (heel up), like a real step turn. Turn rate eased (90 degrees in 1.7-1.8 s).
- **Pace:** the clip walks 1.9 m/s (brisk). Play rate 0.82 gives about 1.6 m/s: calm without looking slow-motion.
- **Clip boundaries snapped to whole frames in plan.py**, so the math and Sequencer agree exactly; per-clip blend lengths (6 frames between walk clips, 10 in and out of the idle); the stop clip ends on its last pose.
- **Lip-sync works:** Joe's face now plays Sequencer tracks directly (single-node, same as the daily show). The face mesh's post-process AnimBP still copies the neck and head from the walking body, so the head stays attached. Mouth opens on the line (final frames ~406-510); face idle (blinks) the rest of the time.
- **Vex:** tilt now follows his acceleration (forward when speeding up, back when braking, into turns), max 5 degrees; smoothed path; he looks at Joe while hovering and is turned part-way to him in the walk-and-talk; rides on Joe's far side half a step ahead so both stay in view, and drops level on the last turn instead of racing around the outside. Hover base is smaller, dark graphite, with a dim glow.
- **Lighting:** three soft lights from the camera side and behind (key / fill / rim) with low specular, instead of two top-down ones. Faces read; no new white slabs.
- **Cameras:** wide closer (35 mm); a low static side camera on the "across" stretch (the foot-sliding check); tracking camera with no lag, full bodies, set slightly to the side so the set (not the dark studio edge) is behind them at the end.
- **Choreography** re-timed for the real walking speed and moved so the path stays clear of the desk and inside the lit set.
- **mux.py** (new): builds the mp4 from the frames and the two lines; drops the first 2 frames (ghost pose). It feeds frames through PIL because this ffmpeg build's PNG reader threw inflate errors and dropped a frame on these renders.

### What still isn't right, and why
- **Feet swivel on the spot during turns.** The planted foot no longer slides, but the whole body turns as one piece, so the foot rotates on its ball by roughly 20-30 degrees per step in a turn. Real feet stay put and the hips turn over them. Fixing it needs leg IK (Control Rig foot IK) or real turn clips; the UEFN set has neither. Wider, slower arcs make it smaller: that is the lever for the long episode.
- **Small foot shuffle going into and out of standing** (about 4 cm per foot over 0.4 s at 8.9-9.3 s and 17.9-18.4 s, about 2 cm at each walk start). The idle clip stands with the feet 8 cm closer together than the stop and start clips. It is along the view axis in this test so it barely shows; from the side it would. Option for the episode: skip the idle clip for short pauses (the stop clip's last pose equals the start clip's first pose exactly).
- **The standing idle pose is wide and arms-out** (a game idle). A bit stiff for a host. Needs a different body idle.
- **No turn-in-place.** Joe can only change direction while walking; a host who must turn on the spot needs clips or a camera cut.
- **Vex's tilt direction is set from Unreal's rotation math and is small; I could not confirm it by eye at this size.** Worth one glance in the video: he should tip toward where he is going as he starts moving.
- **Not verified in motion:** I judged from frame sequences and the math, not by watching playback. Starts and stops looked clean in the frame sequences (final frames 36-70, 250-320, 388-457).
- **Outside movement:** Joe walks barefoot in shorts (his current outfit; not touched). The show's own Key light mirrors in the floor as a hard white rectangle bottom-left of the wide shot (pipeline light; left alone). Vex's white shell runs hot next to Joe's grey skin under any light bright enough for Joe. Joe looks straight ahead while Vex talks to him; a head turn toward Vex would sell the walk-and-talk.
- **Left in the Unreal project:** material `/Game/Sets/NewsMats/M_VexHoverBase`, sequence `/Game/Cinematics/MoveTest`, `/Game/NewsAudio/MoveTest/*`. No daily news pipeline file was edited.

## 2. Grok review (Grok Build CLI, grok-4.7, 11/15 ~1:40 PM) - VERDICT: NEEDS FIXES
Grok said plainly it could not play the file as moving video or hear it; it decoded all 540 frames and stepped through them. Raw output: `movement/grok-review.txt`.
- BIG 4.08 s: hard cut wide -> close side profile; distance, facing and stride all jump (the turn into the cross is skipped on screen).
- BIG 6.21 s: cut back to wide; Joe jumps from large foreground to small far left.
- MEDIUM 11.38 s: wide -> closer angle cut while walking pops.
- MEDIUM 4.08-6.21 s: Vex is in a different place when the wide returns (moved off-screen).
- SMALL 7.9-9.5 s: Joe stands dead still in a feet-together pose, no weight shift.
- SMALL 17.5-19.5 s: Joe's line comes after the walk has stopped; mouth too small in frame to time.
- Looked fine to Grok: no foot slide or swivel seen, step bounce visible (not floaty), walking turn not a pivot, starts ease in, final stop fine, arm swing, no neck seam, no clipping (Vex in front of the desk, not in it), mouth open on the line and closed in silence.

## 3. Jarons Twin review (Grok Bot, relayed by Grok Build for Claude; phone copy attached) - VERDICT: NEEDS FIXES
Raw relay log: `movement/twin-review.txt`. The twin's list, with Claude's check of each against motion.json and frames:
- BIG 0:07 "Joe snaps 90 deg, no turn animation" - NOT CONFIRMED: yaw eases 117 -> 180 deg over about 1 s while walking (frames 6.0-8.0 s look smooth; Grok also saw no pivot).
- BIG 0:11-0:12 "Vex passes through the desk corner" - NOT CONFIRMED: Vex stays at least 0.9 m in front of the desk front edge the whole time (camera parallax).
- BIG 0:17-0:20 "lip-sync missing" - PARTLY: the mouth does open on the words (face crops) but too little to read at phone size. Real problem.
- MEDIUM: first-step foot slide at 0:01; walk floaty (hips/shoulders barely rise); starts at full speed with no weight shift; dead stops for Joe and Vex; both go from walking to frozen at 0:20.
- SMALL: slight foot slide 0:04-0:07; Joe frozen when standing (no breathing / sway); Vex's arms stiff. "Vex has no mouth" - by design (mouth light).
- Looked fine: camera steady, clean cuts, no dropped frames, Vex's hover bob smooth.

**Decision (Claude):** real problems found (cut continuity, statue holds, late line, unreadable lip-sync, Vex motion too subtle, dead stops) -> back to Fable for fix pass 2, then to Jaron (per Jaron's review chain, 11:53 AM).

## 4. Fable fix pass 2

New `movement-test.mp4` / `movement-test-phone.mp4`: 27.1 s, 650 frames (take 21.5 s + two foot-check replays). Frames: `necklace-unreal/Saved/MovieRenders/MoveTest_p2` (+ `_c0`, `_c1`). Pass 1 scripts kept as `movement/*_pass1.bak.py`. Judged from frame sequences and the motion math again, not from playback.

### Fixed
1. **Cut continuity:** there are no cuts now. One camera does the whole take: locked wide for the first walk (Vex's glide across is on screen), then it travels in to follow the pair as the second walk starts (10.1-13.3 s), then moves closer for Joe's line. The low-camera views are appended after the take as two labelled replays: "FOOT CHECK - same take, low camera (walking + turns)" (4.2-6.3 s of the take) and "(the last stop)" (15.3-18.7 s). Same animation, rendered from copies of the sequence with only the camera swapped.
2. **Dead-still holds:** the idle now fades in as soon as the stop clip's feet are settled (1.0 s into the clip) instead of after its motionless tail; the idle plays at 1.3x and starts from its liveliest stretch for each hold (picked by head + hand travel in the clip data). The hold between the walks is shorter.
3. **Joe's line lands while walking:** Vex now speaks as he comes over and they set off (9.7-14.7 s); Joe answers at 14.3 s, about 2.1 s before the stop clip begins (16.4 s) and finishes as they arrive (18.8 s). The last turn became one long easy arc (3.2 s) to give the walk room.
4. **Lip-sync readable:** the camera ends in a knees-up two-shot for his line; mood intensity 0.5 -> 1.0. Face crops at frames 350-435 show the mouth opening and closing on the words (open at 355, 370, 375, 405).
5. **Vex:** bob raised to about 3 cm; tilt gains raised (up to ~7 degrees on starts and brakes); he follows his path on a soft spring, so he eases off and settles a little past his stopping point instead of stopping dead.

### Not fixed, and why
- **"Floaty walk / hips barely rise" (twin):** the clip data says the pelvis moves about 10 cm vertically over the walk loop and the head with it, so the rise is there; what reads as floaty is the slowed clip (0.82x of a brisk game walk with 1 m steps). Adding a fake vertical bob to the actor would lift the feet off the floor or push them through it, so I left it. Honest fix: a real slow-walk clip.
- **"Starts at full speed, no weight shift" (twin):** the start clip does shift weight for its first ~0.2 s, then is at pace within one step; that is the clip. No cheap honest fix.
- **Standing still is livelier but still modest.** The UEFN idle only sways about 2 cm. The MetaHuman body idle (`mhc_mh001_fmn_b_idle`) moves more (head ~5 cm) but stands with feet level and narrow, 18 cm away from where the stop clip leaves them, so blending to it would slide the feet. Needs an idle that matches the stop stance, or foot IK.
- **First-step shuffle (twin, 0:01):** real, about 2 cm per foot, from the idle and start clips standing differently; same for the ~4 cm settling into the idle after a stop. Unchanged from pass 1.
- **Foot swivel in turns, wide arms-out idle pose, no turn-in-place:** unchanged from pass 1 (need IK or clips).
- Joe's right arm touches the left frame edge for a moment in the close two-shot (around frame 398).
- New in the Unreal project: `/Game/Cinematics/MoveTest_C0`, `MoveTest_C1` (the foot-check copies).
