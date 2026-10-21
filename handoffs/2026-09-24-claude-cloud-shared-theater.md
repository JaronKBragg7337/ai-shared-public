# 2026-09-24 — Claude (cloud): one shared screen in the Grand Palace (Q-022 answered)

Route: Claude Code cloud session; AI-Shared, live tests and the SQL file through the Heartbeat MAI connector. Pushed to main in both repos.

## What changed
| Repo / commit | What |
|---|---|
| Movie-Theater-Three.js-Asset- 84f6cd0, 732e9a2 | `src/shared.js`: the theater talks to a host page over postMessage only (allow-listed: heartbeatobservatory.com, localhost). Films, pasted links, uploads, play, pause, seek and stop go to the host; the host's room drives the screen. A video someone else started loads muted (autoplay rules) with a "Tap for sound" button. "Stop for everyone" shows for whoever started the video, or an admin. VideoScreen gained currentTime / seekTo / stop. Standalone (no host) nothing changes. |
| heartbeat-observatory 8e3981c, 362f092 | `/video/3d/shared-room.js`: the room. Supabase Realtime BROADCAST on `theater:grand-palace` (load / play / pause / seek / stop / hello / state / a 5-second position tick from whoever started it). No database row per event. A late arrival asks the room and joins at the right second. Admin stop goes over PRIVATE channel `theater-admin:grand-palace` (only is_admin() can send). Uploads (signed in) go to Storage bucket `theater-uploads` so everyone streams the same file; signed out, an upload plays for you only. |

Every world's theater door (Ashgrove building, Town Square, World 2) already leads to /video/3d/, so they all share this one screen. The simple /video page is still one-person (not asked for; could join the same room later).

## Database — waiting on Claude Code on the MSI
`projects/site-audit/2026-09-24-shared-theater-and-admins.sql` (also in INDEX.json open_blockers as theater-sql-2026-09-24):
1. `world_admins` follows `people.is_admin` forever (trigger + catch-up), and `is_world_admin()` also accepts `is_admin()`. Town Square, worlds-lab and the habitat tools read world_admins, so all three admins (and future ones) get every admin feature. Everything else already used is_admin().
2. Bucket `theater-uploads`: public read, video only, **100 MB per file** (my proposed cap: about 1-2 minutes of iPhone 1080p video or 10+ minutes of 720p; anything bigger should be a link). Signed-in upload into your own folder, one file per account (the page deletes your previous one), delete own / admins delete any. Check the project's global upload limit is at least 100 MB, or set the bucket to 50 MB.
3. Realtime policies: anyone may listen on `theater-admin:grand-palace`; only is_admin() may send.
Until it is applied: syncing works; admin Stop says it is not switched on yet; uploads play for the uploader only.

NOT changed: `desk_owners` (money) — logged as Q-024.

## Verification
- Local (cloud, Chromium, three browsers with a stand-in relay): room join, load, pause/play, admin sees "Stop for everyone", non-starter has no Stop. Timing checks could not run there (4 CPUs, software 3D).
- Live (MSI, www.heartbeatobservatory.com, real Supabase), final run: Android Chromium starts a pasted link; iPhone WebKit receives it; desktop Chromium arrives late and joins mid-video muted with Tap for sound; A and C within 2 s; pause, jump to 1:00 and play follow; a stop from a non-starter is ignored; the starter's Stop stops desktop and tells the iPhone. 13/14; the one fail is the Windows WebKit test browser, which cannot decode any video file (the message arrived).
- Found and fixed during live testing: a stop attempt by someone not allowed to stop made that screen lose track of the room (732e9a2 / 362f092).
- NOT verified: admin Stop live and shared uploads live (need the SQL and a signed-in admin); real iPhone Safari playback (needs a real phone); the built-in films in headless test browsers (codec / cross-origin limits of the test browsers, not the sync).
- Test scripts: %LOCALAPPDATA%\Temp\hb-live-check\live-sync.js (uses a local seekable test video served with byte ranges).
