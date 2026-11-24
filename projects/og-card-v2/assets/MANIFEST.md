# OG card v2: real asset captures (Fable 5.2, 2026-11-20, about 3:45-5:15 PM)

Everything here is a real frame of the live site (https://www.heartbeatobservatory.com) or of a real HB video file.
Nothing was generated or retouched. Nothing on the site, its og:image, or the site repo was changed or pushed.
How: headless Chromium (playwright-core from tools/site-reel), MSI integrated GPU; ffmpeg for video frames.
Capture scripts are in the session scratchpad only (not kept in the repo).

**Read first (things that look off):**
- **Phone copy is not accurate as drafted.** See "Claim checks" at the bottom.
- **The Hub shows member name tags** in the normal view (one is Jaron's account handle). The hero has tags hidden for the capture. The one tagged alt is named DO-NOT-PUBLISH-UNBLURRED.
- **News frames carry today's headlines** on the back wall (oil, war stories). Crop or blur the wall text, or use the studio-wide frame whose screen says "MORE FROM HEARTBEAT".
- **Ashgrove and World 2 have a flat, hazy sky and heavy distance fog**; true high aerials wash out to white. The heroes are low elevated views on purpose.
- **Grand Palace 3D theater crashes headless Chromium on this GPU after about 8 s**, so there is one theater frame only (1280x720, with its on-screen buttons).
- Social and Phone were captured signed out, so no private names, numbers or messages appear. Social shows AI desk posts (First Light Desk, Watch Desk) with news text.

## Top row (wide tiles)

| File | Shows | Source | How | Notes |
|---|---|---|---|---|
| social-feed.png (2400x1350) | Social Feed page, signed out | /social/ | 1600x900 viewport @1.5x | Cream UI, matches the card palette. Crop to the centre column. |
| news-vex-joe.png (1400x700) | **Top pick, News.** Vex (robot) and Joe (alien) at the desk, angled two-shot | news-video/2026-11-20.mp4 at 172 s | ffmpeg frame, crop 1400x700 at (330,330) of the 1920x1080 frame | Unreal render, today's episode. Wall text is today's headlines. |
| news-vex-joe-angle-full.png (1920x1080) | Same frame, uncropped | same, 172 s | ffmpeg | For a different crop. |
| news-vex-joe-studio-wide.png (1920x1080) | Whole HBN studio, both anchors, screen reads "MORE FROM HEARTBEAT" | same, 1114 s | ffmpeg | No news text. Anchors are small; best if the tile wants the set. |
| alt/news-vex-joe-studio-crop.png (1280x640) | Tighter crop of the studio-wide | same | crop 1280x640 at (320,260) | |
| alt/news-vex-closeup.png, alt/news-joe-closeup.png (1920x1080) | Single close-ups (Vex on orange wall, Joe) | 1130 s, 1168 s | ffmpeg | For a side-by-side composite if wanted. |
| alt/news-studio-ashgrove-segment.png | Studio with Ashgrove on the big screen | 927 s | ffmpeg | |
| alt/news-page-live.png (2400x1350) | The /news/ page with the show playing | /news/ | page capture | |
| tv/tv-guide-page.png (2400x1350) | Heartbeat TV page: player + the 15-channel guide | /tv/ | page capture | Shows all channel names. |
| tv/tv-shows-keepers-light-ep1-dawn.png (1280x720) | Shows: The Keeper's Light ep 1, lighthouse at dawn | tv/shows/keepers-light-ep1.mp4, 17.5 s | ffmpeg native frame | **Top pick for the TV mosaic**, most cinematic. |
| tv/tv-shows-keepers-light-ep2-storm.png (1280x720) | Shows: ep 2, lantern room in the storm | keepers-light-ep2.mp4, 24.5 s | ffmpeg | |
| tv/tv-shows-necklace-rusty-anchor.png, tv-shows-necklace-exterior.png (1280x720) | Shows: The Necklace, the bar | necklace-ep1-part1.mp4, 68 s and 9 s | ffmpeg | Dark; realistic people. |
| tv/tv-history-railroads.png (1920x1080) | History: railroads map, 1882 | tv/history/history-ep1-railroads.mp4, 10 s | ffmpeg | |
| tv/tv-science-breath-into-air.png (1920x1080) | Science: sealed-pod CO2 sim | tv/science/science-ep1-breath-into-air.mp4, 13 s | ffmpeg | |
| tv/tv-spacenow-mmx-lander.png (1920x1080) | Space Now: MMX lander on Phobos | tv/spacenow/spacenow-ep1-mmx.mp4, 313 s | ffmpeg | |
| tv/tv-lostplaces-gobekli.png (1280x720) | Lost Places: Gobekli Tepe, cream slide | tv/lostplaces/lostplaces-ep1-gobekli.mp4, 228 s | ffmpeg | Cream, matches the card. |
| tv/tv-music-first-light.png (1280x720) | Music: First Light waveform | tv/music/music-ep1-first-light.mp4, 30 s | ffmpeg | |
| theater-grand-palace-seat.png (1280x720) | Grand Palace Cinema from a seat, film-leader "7" on screen | /video/3d/ (frame source jaronkbragg7337.github.io/Movie-Theater-Three.js-Asset-/?start=seats) | clicked Enter Theater, shot at about 5 s | Only frame before the crash. Has STAND/GRID/MEDIA buttons and a hint line at the bottom; crop the top two thirds. |
| library.png (2400x1350) | The Library page: free shelves, Written Here | /library/ | page capture | "Written Here" is empty today (no books yet). |
| alt/theater-page.png | The Theater (2D screening room) page | /video/ | page capture | |

## Worlds (round tiles; subject is centred, sky above for cropping)

| File | Shows | Source | How the angle was set | Notes |
|---|---|---|---|---|
| hub-hero.png (1600x1200) | **Top pick, The Hub.** Fountain plaza, Library, Theater, Projects, Heartbeat TV, people walking, late light | /engine/hub/ | Built-in dev pin: `?dev=1&tod=0.46&cam=-22,12,22,-0.785,-0.33`, fov set to 50 through the page's own `HB.camera`; name-tag sprites hidden for the shot | Two glowing figures are the AI residents (Claude, Perplexity). |
| alt/hub-front-overview.png | Straight-on overview, midday | same | `tod=0.3&cam=0,15,28,0,-0.4`, fov 55, tags hidden | A big grey roof sits in the lower right. |
| alt/hub-sunset-wide-with-nametags-DO-NOT-PUBLISH-UNBLURRED.png | Wide sunset, orange sky | same | `tod=0.5&cam=30,18,30,0.785,-0.4` | Member names visible. Reference only. |
| ashgrove-hero.png (1600x1200) | **Top pick, Ashgrove.** The civic block: church with steeple, town hall portico, school, streets and houses beyond | /world3/ | Page's own orbit camera (`TOWN.Cam`): target (128,5,134), dist 85, yaw 0.5, pitch 0.36; HUD hidden | The town, not one house. |
| alt/ashgrove-civic-block.png | Same block from the other side | same | yaw -2.4, dist 80, pitch 0.33 | |
| alt/ashgrove-grand-palace-side.png | East side with the Grand Palace building | same | target (275,6,70), dist 90, yaw -1.25, pitch 0.3 | |
| alt/ashgrove-neighborhood.png | Houses and a crossroads, closer | same | target (120,4,80), dist 80, yaw -0.8, pitch 0.35 | |
| world2-hero.png (1600x1200) | **Top pick, World 2 (rebuilt, live build 2026-11-11-phase3).** Riverfront skyline: three towers, brick storefronts, street trees, bridge corner | /world2/ | Built-in test handle: `?dev=1&tod=0.44`, `__camOverride = [-120,38,-190, 30,30,0]`, fov 40; HUD hidden | Confirmed this is the remake, not the old World 2. |
| alt/world2-river-bridge-wide.png | Wider, river and truss bridge in front | same | `tod=0.25`, cam [-190,60,-230 -> 20,22,-10], fov 38 | Hazier. |
| alt/world2-from-river.png | Skyline straight across the river, courthouse dome | same | `tod=0.4`, cam [60,55,-260 -> 10,25,0], fov 40 | |
| alt/world2-aerial-grid.png | High aerial of the street grid | same | `tod=0.25`, cam [160,70,140 -> 10,10,-10] | Wide-angle distortion. |

## Side cards

| File | Shows | Source | How | Notes |
|---|---|---|---|---|
| phone-home.png (1116x2301, transparent corners) | **Top pick, Phone.** The HB phone home screen: HB TV, News, Social, Library, Games, Worlds, Livi, The Crew, My Loft, Theater; dock with Phone and Messages | site-wide phone (bubble.js), opened on / | Clicked the phone button, element capture @3x | No personal data. |
| alt/phone-app-signed-out.png | Phone app, signed out: "Sign in to call people." | same | tapped Phone | Honest view of the condition. |
| alt/phone-open-on-homepage.png (2400x1350) | Phone open over the home page | / | page capture | Wide framing for the tile. |
| loft-hero.png (2400x1350) | **Top pick, The Loft.** Living room: HEARTBEAT neon, TV wall, sofa, floor-to-ceiling night skyline | /homes/ | Page handle `HBHome.P`: pos (11,0,-1.2), yaw 0.75, fov 58 | TV is off in the capture. |
| alt/loft-skyline-kitchen.png | Skyline windows and marble kitchen island | same | pos (10.5,0,-2), yaw 0.25, fov 62 | |
| alt/loft-from-mezzanine-with-demo-guests.png | From upstairs, three demo guests on the sofa | /homes/?guests=3 | pos (9.6,3.4,-4.2), yaw 1.1, pitch -0.28 | Guest names are the page's built-in demo names. |
| alt/loft-existing-site-card.jpg | The Loft's current share card already in the repo | homes/loft/card.jpg | copied | For comparison. |

## Games mosaic (each 1600x1000; six different games; The Cosmos once)

| File | Game | Source | Moment |
|---|---|---|---|
| games/game-the-cosmos.png | The Cosmos | /games/the-cosmos/ | **Top pick.** Opening: two liners crossing Mars, captain's line |
| games/game-rocket.png | Rocket | /games/rocket/ | Climbing through the cloud deck, engine lit |
| games/game-president-sim.png | President Sim | /games/president-sim/ | Oval Office title scene |
| games/game-robot-evolution-lab.png | Robot Evolution Lab | github.io/robot-evolution-lab (framed at /games/robot-evolution-lab/) | MEC-01 robot in the lab |
| games/game-cyber-trench-overdrive.png | Cyber Trench Overdrive | cyber-trench-overdrive.vercel.app (framed on site) | Neon title with the ship |
| games/game-mindgames-origin-lab.png | MindGames (Recursive Reality) | github.io/MindGames (framed on site) | Inside the Origin Lab |
| games/alt/ | The Hedge title, Fable Survival campfire, Northstar city, Wasteland Commons, Signal Drift, Orbit Salvage, ParkWorks title, Rocket on the pad, Cosmos observation deck | live pages | Spares if a tile reads badly small |

Each was captured by loading the game, pressing its start button, and holding W / Space for a few seconds. HUD text is left in (real). Rustfall, Rift Clash, The Defender and SYL only gave menu or dark frames in the time, so they are not included.

## Logo (assets/logo/, copied from the site repo's brand/ folder)
h-heartbeat.svg (vector, use this), h-heartbeat.png (512), icon-512.png, icon-192.png, icon-maskable-512.png, apple-touch-icon.png.
The current live card (not touched): og-home-2026-10-c2.jpg in the site repo root.

## Not captured
- AI/SI Team portraits: skipped on purpose (the six AIs make their own).
- A second theater angle and a 3D library interior: the theater crashes headless; the Library on the site is a page, not a room (the Hub has Library and Theater buildings, visible in hub-hero.png).
- Signed-in Social and Phone views: skipped to keep private names and messages out.

## Claim checks

**1. "Free calls + text over WiFi": partly true; the wording overstates it.**
- Calls: real, free, 1-to-1 voice between two browsers (WebRTC), code in bubble.js lines 218-221. No phone numbers, no Twilio, no SMS anywhere.
- Texts: site messages between members (Supabase `messages` table), not SMS.
- Conditions: both people need a Heartbeat account and must be signed in; the other person must be on the site at that moment ("Calls ring the other person on any page of the site while they are signed in", line 215); mic permission; rings out after 35 s.
- It uses public STUN only, no relay. The code says some cell networks may need one later, and a blocked network ends with "Couldn't connect - the network blocked a direct call."
- WiFi is not required; any internet works. Live on every page (stamped at deploy); the live bubble.js matches the repo.
- Truer line: "Free calls and messages between members."

**2. "13+ playable builds": true, and low.**
- The live /games/ page lists 17 games, each with a Play link (checked live: 17 game links).
- 8 are hosted on the site (The Hedge, Rocket, The Cosmos, SYL, Fable Survival, ParkWorks, Rustfall, President Sim). 9 are framed from their own hosts (MindGames, Robot Evolution Lab, Signal Drift, Northstar, The Defender 3D, Orbit Salvage on github.io; Cyber Trench Overdrive, Rift Clash, Wasteland Commons on vercel.app).
- All 17 loaded today in the capture run. Rift Clash and Wasteland Commons are solo-only for now; Fable Survival is labelled a prototype.
- Not counted: syl-test, the-necklace-show (unlisted), and /PCGames/ (desktop-only).
- "17 playable games" is accurate today; "13+" is safe.

## Added 2026-11-21 (looks-critic fixes, Claude Opus 5.5)
| File | Shows | How | Notes |
|---|---|---|---|
| theater-grand-palace-screen-lit.png (1280x720) | Grand Palace Cinema from the centre seat, lit picture on the screen, seats in front | live theater (?start=seats), headless Chromium with ANGLE d3d11 flags (no crash this time); UI overlays hidden by CSS | The picture on the screen is a still of our own Keeper's Light ep 3 (34.4 s), drawn onto the theater's own screen canvas through window.THEATER.screen.leader. Real video playback timed out headless, so this is a still, not a playing video. |
| social-post-space.png (796x934) | One calm Wire Desk post (space: Voyager light-day, Andromeda merger, Shijian-24 launch) | live /social/, signed out, 430 px viewport @2x, element capture | Replaces the Sudan-airstrikes crop. |
| phone-home-card.png (1116x2301) | Copy of phone-home.png with The Crew icon and label blanked | wallpaper filled by interpolating the pixels either side of the slot | **Retouched on purpose** (brief: do not bring The Crew back). The original phone-home.png is untouched. |
| tv/tv-shows-keepers-light-ep3-keeper.png | Keeper's Light ep 3, keeper at the rail, daylight sea | keepers-light-ep3.mp4, 22.9 s | No text. |
| tv/tv-shows-necklace-two-men.png | The Necklace, two men at the bar (Mateo introduces himself) | necklace-ep1-part1.mp4, 79.8 s | Subtitle at the bottom; card crop stops above it. |
| tv/tv-shows-necklace-pier-night.png | The Necklace, the Rusty Anchor on its pilings at night | necklace-ep1-part1.mp4, 43.5 s | Subtitle at the bottom; card crop stops above it. |
| tv/tv-lostplaces-gobekli-pillars.png | Lost Places title slide (T-pillar drawing) | lostplaces-ep1-gobekli.mp4, 15 s | Card crop uses the drawing only, no text. |
| tv/tv-shows-keepers-light-ep2-tower.png | Keeper's Light ep 2, storm tower | keepers-light-ep2.mp4, 19.1 s | Spare (dark). |
