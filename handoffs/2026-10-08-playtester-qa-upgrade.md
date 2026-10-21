# Handoff: AI playtester now tests like real QA (2026-10-08, night)

Who: Claude (Sonnet 5.5), alone. The game repo was not touched.

## Two new documents
- `tools/playtester/PRACTICES.md` - how professional game QA works (with sources), a 30-line checklist, which items the bot does and which it cannot.
- This handoff.

## What real QA does that the bot now does (all in `tools/playtester/lib/qa.mjs`)
Run them all with `--phases qa`, by name, or just run normally (they are in the default list; `--no-qa` leaves them out).
- **smoke**: load time, download size, warm reload.
- **a11y** (+ readability): text under 11 px, contrast, buttons with no name, 44 px tap size, pinch-zoom lock, volume control, "is a next step on screen".
- **spam**: hammer every panel button 10x, action button 20 taps in 2 s, 25 jumps and wild looks. Checks panels still close, requests answered, purse unchanged.
- **lifecycle**: app sent to background and back (hidden/blur/pagehide events), graphics context lost, phone rotated (also with a panel open).
- **network**: offline mid-play and back, refresh while offline, slow connection (desktop Chromium only).
- **economy**: buy then sell loop must never profit, purse never below zero, double-tap Buy charges 1x or 2x.
- **edges**: walk and jump into walls in 8 directions; falling through, leaving the map.
- **perf**: look all the way round, read draw calls and frame times. Memory/graphics-object samples every 20 s all run long, trend in the report.
- **monkey**: 30-40 s of random taps and gestures (skips buy/sell/hire/leave-type buttons), checks purse and frames.
- **idle**: 90 s with no input; drift, frame time, memory, connection.
- **softlock**: end-of-run refresh, can the player still walk, no panel stuck.
Results land in a new "QA checks" table (pass/FAIL/skipped per device) and a "Load, size and memory" section of REPORT.md. Real bugs also appear as normal findings.

## Earth fixes (the "Could not walk to ..." gap)
- Tour on a settlement world (Earth, Moon bases) now uses that world's own people (`cosmos.space.activeMoon.client.people`) and a new `outpost` walking frame with a box-avoiding route planner (`planRouteBoxes` in nav.mjs, heap A*, around the layout's solid boxes).
- New `lifeboat` phase (runs on every start world): buys the power cell and fuel coupler from the two givers (Okafor, Pruitt on Earth; the traders on Mars), walks back and taps Fit. Verified live on Earth: purse 10000 -> 9700 -> 9400, boat repaired, NEXT line updates. Checks the NEXT line names the givers.
- `hire`, `dig`, `spots`, `rover` skip with a note on non-Mars starts; `fly` on Earth boards, sits and reads the Course sheet (no trip).
- `state()` now also reports `outpost` coordinates.

## Other changes you should know
- A desktop run under 11 minutes now starts from the review start (`?opening=off`) instead of spending its whole budget on the 8-10 minute opening. `--desktop-opening` restores the old way. Its phase order puts the cheap QA checks first (walks are slow in headless Chromium).
- Vision still runs on Jaron's Claude plan (planToken untouched). Shots marked `skipVision` are left out (used for the deliberate safe-mode screen).
- Deliberate network cuts no longer create "request failed / websocket closed / console error" noise.
- Files changed: play.mjs, lib/core.mjs, lib/nav.mjs, lib/world.mjs, lib/report.mjs, lib/vision.mjs (one filter), new lib/qa.mjs, PRACTICES.md.

## Verified
Local/live (against the live site, build 714b42a01a8aa6cad4f1):
- Earth: `play.mjs --start earth --side skyward --minutes 15 --desktop-minutes 5` -> `state/playtest/2026-10-09_00-03/REPORT.md`. Phone: opening, panels, tour (Okafor and Pruitt reached), lifeboat chain repaired. No "Could not walk to" in the phone run. Desktop: 18 QA checks passed, 5 failed (all real a11y/layout items below), 1 skipped.
- Mars: default start, 12 + 5 min -> `state/playtest/2026-10-08_23-41/REPORT.md`. Economy checked separately on Mars (traders): sell pays half of buy (24 -> 12), no exploit, double tap charged 2x.
- Earth live session driven by hand also ran every QA phase once (all passed or reported sensibly).
Unverified: the QA phases on the iPhone (WebKit) profile in full (the 15-minute phone budget is used up by the opening + Earth tour + lifeboat; an earlier phone run did exercise smoke, a11y, lifecycle). Economy on Earth (no shop there).

## Real findings the new checks surfaced (for the game builder, not fixed here)
1. **Lost graphics context = the game restarts itself in "safe mode"** (`src/core/graphicsHealth.js`: handler reloads with `?tier=safe` after 800 ms and keeps it). iPhones lose the context when the app is backgrounded (iOS 17), so a player who only switched apps comes back to reduced graphics and a red banner for the rest of the session. By design, but worth a decision.
2. Pinch-zoom is switched off (`maximum-scale=1, user-scalable=no`).
3. Text 10 px in the HUD ("NEXT" line, tool, hauling, coordinates); hint text contrast 3.9:1.
4. One `input` with no label.
5. Touch-key buttons (`#touch-key-KeyD`) can end up on a desktop screen overlapping "World / crew" (seen after random tapping).
6. A game message "fetch failed" showed in the opening dig step on the phone run.
7. Game does not tell the player when the connection drops (hint only: the bot's offline switch may not close an already-open socket).
8. "Covered by #boot" for the Settings button at a landscape size once (first run, not repeated).

## What the bot still cannot do
Real phone call/banner/lock screen, battery and heat, low-end phone speed, many device models, real iOS Safari audio and real two-finger touch, race-condition duplication between two players, judging whether something is fun or confusing the way a first-time human does (only checks that guidance exists, plus the vision pass).

## Broken / caveats
- Headless software rendering makes frames slow (frame-time spike findings are noise at 4-10 s); desktop walking is slow, so the desktop tour can still time out ("Could not walk to Arrival guide", Mars review start) - bot speed, not a confirmed game bug.
- `--phases` with a desktop run still plays the opening unless `--skip-opening` is given (old behaviour).
- Each verification run appended a line to `state/timeline.md` automatically (a few extra lines from test runs).

## Still open
- Decision for Jaron/the builder: safe-mode restart on lost graphics context (item 1).
- Run the phone with a longer budget (e.g. `--minutes 30`) so all QA phases also run on WebKit.
