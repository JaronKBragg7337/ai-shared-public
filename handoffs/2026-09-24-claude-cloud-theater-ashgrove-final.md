# 2026-09-24 — Claude (cloud): theater, Ashgrove Grand Palace, social, Keava — final round

Route: Claude Code cloud session, reaching this folder through the Heartbeat MAI connector.
Rules followed: pushed straight to main, no PRs, no secrets printed, nothing outward. Read the new "stop means stop" rule in AGENTS.md (2026-09-24); working in short turns from here.

## Live on heartbeatobservatory.com (all READY on Vercel)
| Commit | What |
|---|---|
| bab3e45 | Phone zoom trap fixed on every page. hb-editor.js (loaded on all pages) makes every text box, text area and dropdown 16px or bigger on touch screens, so iPhone Safari never zooms in. On pages that block pinch-zoom, leaving a box resets any zoom. Four pages that scrolled sideways on phones fixed (engine, space, habitat, revenue). |
| (Grand Palace repo, main) | /video/3d/ itself: link box 16px, every input 16px, Now Showing panel fits the screen and scrolls on its own, `?start=seats` sits you in seat J14 facing the screen. |
| 996e61a | /video: "Bring your own" — paste a link or play a file from your device. Town Square theater door and World 2 "take your seat" sign go to /video/3d/. |
| 4ab51aa | /social: For You ranked the way X's open-source For You ranks (xai-org/x-algorithm, commit 44d37eb). |
| d45b078 | Ashgrove: Grand Palace building on the east avenue. Its doors seat you. World doors pass `start=seats` and the back link names the world you came from. |

Rollback: before today = dpl_J7JX6dQkWKRT8WMxB3VmAztw89XM (056459e). Before Ashgrove only = dpl_5rPuHWV3iB1RYpxfrrqdC6BrvRTT (4ab51aa).

## Ashgrove placement (world3/cinema.js — nothing in town/ edited)
- No free block fits 38 x 63 m. The park is load-bearing (NPC lunch/errands, tools/ambient.js), so the map grows east.
- Glass front x 294, facing west onto the east avenue (x 280). Centre z 62, width z 43-81. Back wall x 356.8. New lawn x 324-372.
- 12 trees cleared (street trees on the east side + east outskirts). They are still "planted" into a thrown-away builder so the town's random stream is unchanged: every building, lamp and car identical (tested: buildings identical, only those 12 trees and their colliders removed).
- Door zone in front of the glass doors shows "Enter the Grand Palace — take your seat" (green Enter button on phones). It goes to /video/3d/?start=seats&from=ashgrove.
- The outside is redrawn in Ashgrove's own WebGL engine at the real building's size and look; the inside you walk into is the real three.js Grand Palace.

## Verification (the three-part rule)
- Verified locally (cloud container, Chromium): Ashgrove cinema at desktop 1280, iPhone 390x844, Android 412x915 - door prompt shows, green Enter button on phones, navigates to /video/3d/?start=seats&from=ashgrove; town identical apart from 12 trees. /video 28/28 checks; all 71 pages scanned at 390 and 320 px for small inputs and sideways scroll.
- Verified remotely (MSI, live heartbeatobservatory.com): /video/3d/ tap test in iPhone WebKit, run twice (last night and today): link box 16px, page zoom stays 1, Now Showing panel fits, Play visible, typing works. Desktop WebKit same, with one console error logged (not yet read). Vercel shows all five commits READY; live world3/cinema.js matches the tested file.
- NOT yet verified: live Android/desktop Chromium tap runs (no result file written today - rerun `node theater-tap.js android-chromium` / `desktop-chromium` in %LOCALAPPDATA%\Temp\hb-live-check); live phone-width look at /world3/ door, /video, /social from the MSI. See an addendum below if a later session filled these in.

## Keava
Pushed to github.com/JaronKBragg7337/keava-owent (6c1a5d4) after a secret scan: only environment-variable NAMES found, no values. Ran once on the MSI with email off (no SendGrid key set → messages go to a local outbox file). It is a loop, not a chatbot: each round it checks itself, finds gaps in what it knows, picks one, and drafts - never sends. It meters its own energy and water. Its limits live in config/membrane.yaml, which it cannot write; outbound to others is off. Keep-or-not is Jaron's call.

## Not built (Q-022)
Shared uploads and watch-together.

## Social ideas for Jaron (none built)
1. "Not interested" / mute / block on posts (X's biggest signals). Needs a small table for mute/block; SQL would go to AI-Shared\projects\site-audit\.
2. "Why am I seeing this?" line on For You posts.
3. Hide posts you've already seen from For You.
4. Muted words.
5. Count shares and copy-link (X weighs copy-link 20x a like).
6. Reply notifications.
Suggested order: 1, then 2.

## Addendum 10:40 (same session, after the laptop move)
Live checks from the MSI against www.heartbeatobservatory.com (scripts and screenshots in %LOCALAPPDATA%\Temp\hb-live-check):
- /video/3d/ tap test: iPhone WebKit PASS, Android Chromium PASS (GPU flags added to theater-tap.js; watchdog raised to 300 s), desktop WebKit PASS. Desktop WebKit's one error is the test browser having no window focus for pointer lock, not a site fault.
- Desktop Chromium: NOT fully verified. After Enter the page takes pointer lock; the test's Escape brings back the start overlay, so the MEDIA menu never opened and the tap step didn't run. This is the theater's existing desktop control flow, not today's change, and the zoom bug is phone-only. A desktop test needs to open MEDIA another way.
- live-look.js, iPhone 390 and Android 412: /video no sideways scroll, no small inputs, link box 16px, file button present. /social no sideways scroll, no small inputs, For You ranking live, 9 posts. /world3/ Grand Palace present, door prompt "Enter the Grand Palace - take your seat" shown on screen, the door goes to /video/3d/?start=seats&from=ashgrove. No page errors anywhere.
- Nothing rolled back; nothing needed it.
