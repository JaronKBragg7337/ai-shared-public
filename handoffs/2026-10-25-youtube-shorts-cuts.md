# Handoff 2026-10-25 - YouTube Shorts cuts of the long vertical shows (Claude Sonnet 5.5)

## What shipped
17 cuts of 2:03-2:28 (limit 3:00; target 2:30), saved next to each original as `*-short.mp4`, queued on the YouTube channel
(Postiz integration cmvcfuzny1h5ulu0yl77gu5vj) as public, "#Shorts" in title and description, "Made with AI by Heartbeat Observatory"
in the description (the YouTube settings offer no AI-disclosure field: only title, type, made-for-kids, thumbnail, tags).
Spacing: 6 hours apart, first at 14:08Z (10/25), last 10/29 14:08Z - at least 1 h as asked; 6 h because Postiz failed the 10/20 render-engine
upload on YouTube's daily upload cap and the news already uses 2 uploads a day. If the cap is not a problem, shorten the gaps with `posts:*`.

## How
`projects/heartbeat-tv/shorts/`: `make_short.py` (cuts whole narration scenes at each show's own scene boundaries, 0.12 s dip between
non-adjacent scenes, drops the sources end card, adds a closing card "Full episode free at heartbeatobservatory.com" voiced with the
show's own Kokoro voice), `plans.py` (which scenes each Short keeps), `post_shorts.py` (upload + schedule), `posted.json`.
Facts untouched: scenes are kept or dropped whole, no wording changed. Still Unknown scene counters ("06/18") are painted out. No GPU, no RunPod, CPU ffmpeg only.

| Short | Length | File | Postiz post id | Scheduled |
|---|---|---|---|---|
| Coral Castle: one man, 1,100 tons #Shorts | 2:23 | `projects/still-unknown/ep2-coral-castle/stillunknown-ep2-coral-castle-short.mp4` | cmvnw7cxm16x1pi1c7bw1cozg | 2026-10-25T14:08:00Z |
| The energy we can't explain yet #Shorts | 2:22 | `projects/still-unknown/ep1-dark-energy/stillunknown-ep1-dark-energy-short.mp4` | cmvnw7mqj4yaop71cufltaldq | 2026-10-25T20:08:00Z |
| Did we build civilization backward? #Shorts | 2:16 | `projects/lost-places/ep1-gobekli/lostplaces-ep1-gobekli-short.mp4` | cmvnw7q1p16x4pi1cr589web0 | 2026-10-26T02:08:00Z |
| Can consciousness be measured? #Shorts | 2:14 | `projects/ai-explained/ep1-consciousness/aiexplained-ep1-consciousness-short.mp4` | cmvnw7tiz4ybkp71c9v9c5fls | 2026-10-26T08:08:00Z |
| The first great extinction was caused by life itself #Shorts | 2:27 | `projects/earth/ep1-oxygen/earth-ep1-oxygen-short.mp4` | cmvnw7whl16x7pi1c2honhls1 | 2026-10-26T14:08:00Z |
| MMX: ten grams from Phobos #Shorts | 2:14 | `projects/space-now/ep1-mmx/spacenow-ep1-mmx-short.mp4` | cmvnw7ytf16x8pi1c437m1lqg | 2026-10-26T20:08:00Z |
| Can vibration cut stone? #Shorts | 2:06 | `projects/still-unknown/ep3-vibration-stone/stillunknown-ep3-vibration-stone-short.mp4` | cmvnw82bq4yckp71cpuklyc48 | 2026-10-27T02:08:00Z |
| How a highway disappears #Shorts | 2:22 | `projects/science-channel/ep4-highway-disappears/science-ep4-highway-disappears-short.mp4` | cmvnw87lt16xbpi1cpu9ybce9 | 2026-10-27T08:08:00Z |
| How a commercial roof dies #Shorts | 2:25 | `projects/science-channel/ep5-commercial-roof/science-ep5-commercial-roof-short.mp4` | cmvnw8b5k16xdpi1c46va5sqh | 2026-10-27T14:08:00Z |
| Phobos: the moon that's falling #Shorts | 2:21 | `projects/science-channel/ep6-phobos/science-ep6-phobos-short.mp4` | cmvnw8eco4ydkp71cvej4z8h3 | 2026-10-27T20:08:00Z |
| Can something learn without a brain? #Shorts | 2:25 | `projects/open-questions/ep2-no-brain/openquestions-ep2-no-brain-short.mp4` | cmvnw8jgx4ye1p71c5wbe7z21 | 2026-10-28T02:08:00Z |
| Did humanity's birthplace have something special? #Shorts | 2:03 | `projects/open-questions/ep3-birthplace/openquestions-ep3-birthplace-short.mp4` | cmvnw8o3u16xhpi1cm7q9u26f | 2026-10-28T08:08:00Z |
| What if gravity isn't the full story? #Shorts | 2:22 | `projects/open-questions/ep4-gravity/openquestions-ep4-gravity-short.mp4` | cmvnw8tl316xipi1cqt173sin | 2026-10-28T14:08:00Z |
| The year summer never came #Shorts | 2:15 | `projects/history-channel/ep5-1816/history-ep5-1816-short.mp4` | cmvnw8z5k16xkpi1cp7ihma7m | 2026-10-28T20:08:00Z |
| Do animals understand death? #Shorts | 2:12 | `projects/animals/ep1-death/animals-ep1-death-short.mp4` | cmvnw91wg16xlpi1cmdu49w67 | 2026-10-29T02:08:00Z |
| The book nobody can read #Shorts | 2:07 | `projects/still-unknown/ep4-voynich/stillunknown-ep4-voynich-short.mp4` | cmvnw94r116xmpi1c0p51n6s1 | 2026-10-29T08:08:00Z |
| 72 seconds from somewhere #Shorts | 2:16 | `projects/still-unknown/ep5-wow/stillunknown-ep5-wow-short.mp4` | cmvnw97r316xnpi1cflmk12rs | 2026-10-29T14:08:00Z |

## Not made, on purpose
- Render engine: not a long vertical show. It is the ad post already queued by Pip (post cmvncdy040d20n31cmzbdt3p6, 10/25 16:00Z).
- Under 3:00 already (no cut needed): history ep1-4 + ep6, science ep1-3, necklace, first light. Open Questions ep1 already has its 94 s short (posted 10/23).

## Check before relying on it
- Space Now (MMX) video still says the launch is upcoming (written before 10/19). The Short keeps that scene as recorded; the post text is rewritten without the date. Same for Science 8.6 caption.
- Still Unknown 10.3 Short opens "This episode keeps the two apart" (the show's own line, kept verbatim).
- Per-scene progress bars on some shows (Animals, AI Explained) jump after cuts.
- Spot-checked on screen: coral, contact sheets of hwy, sci6, h5, su5. Not watched end to end.
