# The Cosmos playtest report

Run: 2026-10-08 23:41 (local)  |  Build under test: `714b42a01a8aa6cad4f1`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

**How to read this:** items titled "Stuck while walking to ..." come from the bot's own steering (its path planner, run-ups and jumps). Treat them as bot-only unless a human also gets stuck at that spot. Black boot and crash-blackout frames that carry a caption are deliberate.

- **iPhone 15 (WebKit, touch)**: 13.2 minutes, 87 screenshots, 5 distinct problems
- **Desktop (Chromium, keyboard + mouse)**: 5.2 minutes, 49 screenshots, 18 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)
- Desktop (Chromium, keyboard + mouse): [session video](videos-desktop/<email>)

## Short version

35 distinct problems found: 0 blockers, 0 serious, 35 smaller.

- **Could not walk to Arrival guide** (Annoying)
- **A button is covered by something else: #multiplayer-button "World / crew" is covered by #touch-key-KeyD** (Annoying)
- **A Dig tap in the opening made no cut** (Annoying, seen 4 times)
- **Buttons overlap: #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83%** (Annoying)
- **Looks wrong in the screenshot: Developer/debug UI (square ID, coordinates, 'NEAREST ASSETS' list, per-object debug cards) is exposed on scree** (Annoying)

## Problems, worst first

### 1. Could not walk to Arrival guide

- **How bad:** Annoying (score 72)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 10:23 into the run, on iPhone (WebKit)
- **What happened:** gave up after 120s; last distance 5 m
- **What the vision model saw:** Same desert HUD with a yellow-suited character standing near a shed, a pole with a flag/marker, and a small yellow hydrant-like object in the open terrain.
- **Screenshot:** [058-tour-PROBLEM-cannot-reach.jpg](shots-iphone/058-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Arrival guide](shots-iphone/058-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #3
  1. jump
  1. not getting closer (9 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (9 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 12 legs

### 2. A button is covered by something else: #multiplayer-button "World / crew" is covered by #touch-key-KeyD

- **How bad:** Annoying (score 68)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:41 into the run, on desktop (Chromium)
- **What happened:** #multiplayer-button "World / crew" is covered by #touch-key-KeyD (Controls open, desktop)
- **What the vision model saw:** Same Mars landing-pad scene with the Controls panel still fully open and showing the same key-binding list. Flagged: Bot's action was to toggle the Controls panel closed, but the panel is still open and pixel-identical to the previous screenshot — the close toggle had no visible effect
- **Screenshot:** [012-panels-PROBLEM-covered.jpg](shots-desktop/012-panels-PROBLEM-covered.jpg)

  ![A button is covered by something else: #](shots-desktop/012-panels-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. mis-tap beside #multiplayer-button
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)

### 3. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 4 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:28 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 4 after tapping "Dig (E)"
- **What the vision model saw:** Daytime dune/beach landscape with a small crashed crate/rover on the sand, a Dig (E) prompt bottom right and an instruction to aim the shovel.
- **Later hits:** 06:30 cuts stayed 4 after tapping "Dig (E)" / 06:32 cuts stayed 4 after tapping "Dig (E)"
- **Screenshot:** [034-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/034-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/034-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. REFRESH (mid-dig)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. tap #opening-action (opening action)

### 4. Buttons overlap: #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83%

- **How bad:** Annoying (score 66)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:41 into the run, on desktop (Chromium)
- **What happened:** #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83% (Controls open, desktop)
- **What the vision model saw:** Controls panel (key-binding list: Debug, View, Use/dig/lift, Drop, Climb, Talk/hire, Fire, tool keys, movement keys, Close panels) is open over the same Mars landing-pad scene. Flagged: Controls panel's bottom-right edge sits almost flush against the pad/horizon line with no margin, crowding the 3D scene below it
- **Screenshot:** [011-panels-PROBLEM-overlap.jpg](shots-desktop/011-panels-PROBLEM-overlap.jpg)

  ![Buttons overlap: #touch-key-KeyD "Right"](shots-desktop/011-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. mis-tap beside #multiplayer-button
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)

### 5. Looks wrong in the screenshot: Developer/debug UI (square ID, coordinates, 'NEAREST ASSETS' list, per-object debug cards) is exposed on scree

- **How bad:** Annoying (score 63)
- **Where:** app to the background, graphics context lost, phone rotated, first at 02:04 into the run, on desktop (Chromium)
- **What happened:** center and right side of screen (the vision model's description of the screen: After opening Settings and rotating, the screen shows a developer debug overlay (DEBUG · MARS coordinates panel, nearby-asset listing panels, a 'Raise ramp' button) over an almost entirely black background instead of the Mars scene.)
- **Screenshot:** [033-lifecycle-rotated-panel.jpg](shots-desktop/033-lifecycle-rotated-panel.jpg)

  ![Looks wrong in the screenshot: Developer](shots-desktop/033-lifecycle-rotated-panel.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-settings (open Settings, then rotate)

### 6. Looks wrong in the screenshot: Developer/debug UI (DEBUG · MARS panel, coordinate readouts, nearby-asset cards) still visible on screen, not 

- **How bad:** Annoying (score 63)
- **Where:** random tapping everywhere, first at 03:25 into the run, on desktop (Chromium)
- **What happened:** center and right side of screen (the vision model's description of the screen: End of the 30-tap monkey-test pass, screen still shows the same developer debug overlay (coordinates, asset list panels, 'Raise ramp' button) over a black background.)
- **Screenshot:** [042-monkey-end-of-monkey.jpg](shots-desktop/042-monkey-end-of-monkey.jpg)

  ![Looks wrong in the screenshot: Developer](shots-desktop/042-monkey-end-of-monkey.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: monkey: 30 random button taps and wild gestures, no crash

### 7. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 9 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:15 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4197 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Interior of the ship/station with a dialogue line from Walter about coffee, railing and a round orange structure visible through the windows, movement/look hints at the top. Flagged: flat, sharply-edged gray bar spanning the full width of the screen with no texture or shading, looks like a clipped/stretched geometry or UI element rather than part of the ceiling
- **Later hits:** 05:45 a single frame took 6958 ms (typical 30 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 05:58 a single frame took 1175 ms (typical 30 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 8. Frame-time spike during "lifecycle"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:54 into the run, on desktop (Chromium)
- **What happened:** a single frame took 4383 ms (typical 4 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 02:07 a single frame took 2542 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [031-lifecycle-PROBLEM-frame-spike.jpg](shots-desktop/031-lifecycle-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "lifecycle"](shots-desktop/031-lifecycle-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. spam: 0 requests sent, purse 10000 -> 10000
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA info: lifecycle: graphics context lost, game reloads itself into safe mode and still plays - the game restarted with ?tier=safe (reduced graphics). Banner: "Graphics problem: WebGL context lost - safe mode active"
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off&build=714b42a01a8aa6cad4f1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 9. Frame-time spike during "network"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** network cut, refresh offline, slow connection, first at 02:34 into the run, on desktop (Chromium)
- **What happened:** a single frame took 4566 ms (typical 4 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 02:42 a single frame took 2279 ms (typical 33 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [038-network-PROBLEM-frame-spike.jpg](shots-desktop/038-network-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "network"](shots-desktop/038-network-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap button "Close" (close account-panel)
  1. QA pass: network: while offline the game keeps drawing and does not crash
  1. QA info: network: the game tells the player the connection is gone (within about 12 s) - connected flag true -> true; messages: 
  1. NETWORK BACK
  1. QA pass: network: after the network returns the game reconnects and answers again - 2 s
  1. QA pass: network: money and place unchanged by a network blip
  1. REFRESH (refresh after being offline)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 10. Frame-time spike during "freeplay"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** free play (random walking, tapping, refreshing), first at 05:03 into the run, on desktop (Chromium)
- **What happened:** a single frame took 4583 ms (typical 4 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 05:09 a single frame took 2342 ms (typical 21 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [048-freeplay-PROBLEM-frame-spike.jpg](shots-desktop/048-freeplay-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "freeplay"](shots-desktop/048-freeplay-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. QA pass: edges: walked and jumped into walls in 8 directions, never fell through - furthest 39 m from where it started
  1. QA pass: edges: still drawing afterwards
  1. === phase freeplay starts
  1. tap #btn-key-controls (idle fiddling)
  1. jump
  1. REFRESH (random refresh while playing)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 11. Frame-time spike during "panels"

- **How bad:** Annoying (score 62)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:26 into the run, on desktop (Chromium)
- **What happened:** a single frame took 4487 ms (typical 4 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Settings panel is open on the right side of the Mars landing-pad scene, showing account/sign-in fields, a Start Fresh button, and View/Digging-tool dropdowns.
- **Screenshot:** [003-panels-PROBLEM-frame-spike.jpg](shots-desktop/003-panels-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "panels"](shots-desktop/003-panels-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. desktop budget is 5 min and the opening alone takes about 10: started from the review start (use --desktop-opening to play it)
  1. === phase panels starts
  1. mis-tap beside #btn-settings
  1. tap #btn-settings (open Settings)

### 12. Frame-time spike during "smoke"

- **How bad:** Annoying (score 62)
- **Where:** smoke check (load time, download size, warm reload), first at 00:53 into the run, on desktop (Chromium)
- **What happened:** a single frame took 4500 ms (typical 4 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Mars landing-pad scene (no panels open) with a status tooltip reading "Systems nominal. Ship down and stable." floating over the ship's engine/exhaust structure. Flagged: Status tooltip floats in open space overlapping the ship's exhaust nozzles with no visible pointer/anchor connecting it to anything
- **Screenshot:** [014-smoke-PROBLEM-frame-spike.jpg](shots-desktop/014-smoke-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "smoke"](shots-desktop/014-smoke-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase smoke starts
  1. QA info: smoke: page transfer on a cold load - 250 requests, 0.1 MB over the wire (slowest: eartbeatobservatory.com/games/the-cosmos/src/vehicles/api.js 100 ms)
  1. QA pass: smoke: time from opening the link to the first drawn frames - 21.2 s (headless software rendering, a real phone is usually quicker to draw but slower to download)
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 9.8 s

### 13. Looks wrong in the screenshot: Error banner 'Graphics problem: WebGL context lost - safe mode active' displayed, indicating a real rendering 

- **How bad:** Annoying (score 56), happened 3 times
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:43 into the run, on desktop (Chromium)
- **What happened:** top banner below the Mars/Valles Marineris header line (the vision model's description of the screen: Same Mars pad scene, now with a dark red error banner reading 'Graphics problem: WebGL context lost - safe mode active' across the top, the scene rendered flat/washed-out (sky and ground lost their gradient/detail, engine bells lost shading), and a tooltip reading 'Systems nominal. Ship down and s
- **Screenshot:** [026-lifecycle-PROBLEM-console-warning.jpg](shots-desktop/026-lifecycle-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: Error ban](shots-desktop/026-lifecycle-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 14. Looks wrong in the screenshot: Entire Mars terrain/sky has gone black/empty with no scene content

- **How bad:** Annoying (score 56)
- **Where:** app to the background, graphics context lost, phone rotated, first at 02:04 into the run, on desktop (Chromium)
- **What happened:** whole screen behind the panels (the vision model's description of the screen: After opening Settings and rotating, the screen shows a developer debug overlay (DEBUG · MARS coordinates panel, nearby-asset listing panels, a 'Raise ramp' button) over an almost entirely black background instead of the Mars scene.)
- **Screenshot:** [033-lifecycle-rotated-panel.jpg](shots-desktop/033-lifecycle-rotated-panel.jpg)

  ![Looks wrong in the screenshot: Entire Ma](shots-desktop/033-lifecycle-rotated-panel.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-settings (open Settings, then rotate)

### 15. Looks wrong in the screenshot: Scene background is black/empty instead of the Mars terrain

- **How bad:** Annoying (score 56)
- **Where:** random tapping everywhere, first at 03:25 into the run, on desktop (Chromium)
- **What happened:** whole screen behind the panels (the vision model's description of the screen: End of the 30-tap monkey-test pass, screen still shows the same developer debug overlay (coordinates, asset list panels, 'Raise ramp' button) over a black background.)
- **Screenshot:** [042-monkey-end-of-monkey.jpg](shots-desktop/042-monkey-end-of-monkey.jpg)

  ![Looks wrong in the screenshot: Scene bac](shots-desktop/042-monkey-end-of-monkey.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: monkey: 30 random button taps and wild gestures, no crash

### 16. When the graphics context is lost (iPhones do this after the app was in the background) the game restarts itself in reduced-graphics "safe mode"

- **How bad:** Minor (score 52)
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:46 into the run, on desktop (Chromium)
- **What happened:** by design (src/core/graphicsHealth.js). The page address gets ?tier=safe and it stays that way for the session, with a red graphics banner: "Graphics problem: WebGL context lost - safe mode active". A player who just switched apps and came back is left on worse graphics.
- **What the vision model saw:** The game's boot screen: near-black background with the title THE COSMOS, a tagline about the ship and Mars, and a 'Loading the port...' line.
- **Screenshot:** [030-lifecycle-PROBLEM-context-lost-safe-mode.jpg](shots-desktop/030-lifecycle-PROBLEM-context-lost-safe-mode.jpg)

  ![When the graphics context is lost (iPhon](shots-desktop/030-lifecycle-PROBLEM-context-lost-safe-mode.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. QA pass: spam: 25 jumps and wild looks, game keeps drawing
  1. spam: 0 requests sent, purse 10000 -> 10000
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA info: lifecycle: graphics context lost, game reloads itself into safe mode and still plays - the game restarted with ?tier=safe (reduced graphics). Banner: "Graphics problem: WebGL context lost - safe mode active"

### 17. Looks wrong in the screenshot: Scene remains flat/washed-out with no shading detail

- **How bad:** Minor (score 49), happened 2 times
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:43 into the run, on desktop (Chromium)
- **What happened:** entire 3D viewport (the vision model's description of the screen: Identical frame to image 4: WebGL context lost error banner still showing, flat degraded lighting, same 'Systems nominal' tooltip.)
- **Screenshot:** [027-lifecycle-PROBLEM-console-warning.jpg](shots-desktop/027-lifecycle-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: Scene rem](shots-desktop/027-lifecycle-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 18. Looks wrong in the screenshot: Camera appears clipped into or pressed right up against a wall surface, showing only a flat grainy texture wit

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:19 into the run, on iPhone (WebKit)
- **What happened:** entire frame (the vision model's description of the screen: A close-up, mostly featureless grey wall/panel texture fills almost the entire screen with no characters, objects, or UI text visible.)
- **Screenshot:** [015-opening-opening.jpg](shots-iphone/015-opening-opening.jpg)

  ![Looks wrong in the screenshot: Camera ap](shots-iphone/015-opening-opening.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. in the boarding hall, waiting for the gangway to come down

### 19. Looks wrong in the screenshot: Flat solid-color cyan/green/white rectangular blocks visible in the background behind the character, with no t

- **How bad:** Minor (score 49)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 11:53 into the run, on iPhone (WebKit)
- **What happened:** mid-screen, directly behind the player character's head/shoulders (the vision model's description of the screen: A tour NPC dialogue box ('Watch supervisor') is open over the HUD, with the player character's back and a waist-high crate/pedestal visible behind it.)
- **Screenshot:** [079-tour-talk-answer-cab-supervisor.jpg](shots-iphone/079-tour-talk-answer-cab-supervisor.jpg)

  ![Looks wrong in the screenshot: Flat soli](shots-iphone/079-tour-talk-answer-cab-supervisor.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap button "Is there paid work for a hauler?" (ask them something)

### 20. Looks wrong in the screenshot: Bot's action was to toggle the Controls panel closed, but the panel is still open and pixel-identical to the p

- **How bad:** Minor (score 49)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:42 into the run, on desktop (Chromium)
- **What happened:** entire Controls panel, bottom-left (the vision model's description of the screen: Same Mars landing-pad scene with the Controls panel still fully open and showing the same key-binding list.)
- **Screenshot:** [012-panels-PROBLEM-covered.jpg](shots-desktop/012-panels-PROBLEM-covered.jpg)

  ![Looks wrong in the screenshot: Bot's act](shots-desktop/012-panels-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (toggle closed Controls)

### 21. Looks wrong in the screenshot: Scene lighting/textures degraded to flat, washed-out colors (sky, ground, rocket) compared to normal shaded re

- **How bad:** Minor (score 49)
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:43 into the run, on desktop (Chromium)
- **What happened:** entire 3D viewport (the vision model's description of the screen: Same Mars pad scene, now with a dark red error banner reading 'Graphics problem: WebGL context lost - safe mode active' across the top, the scene rendered flat/washed-out (sky and ground lost their gradient/detail, engine bells lost shading), and a tooltip reading 'Systems nominal. Ship down and stable.' floating mid-screen.)
- **Screenshot:** [026-lifecycle-PROBLEM-console-warning.jpg](shots-desktop/026-lifecycle-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: Scene lig](shots-desktop/026-lifecycle-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 22. Looks wrong in the screenshot: 'Raise ramp' button overlaps/crowds the 'World / crew' and 'Controls' buttons in the bottom-left

- **How bad:** Minor (score 49)
- **Where:** app to the background, graphics context lost, phone rotated, first at 02:04 into the run, on desktop (Chromium)
- **What happened:** bottom-left corner (the vision model's description of the screen: After opening Settings and rotating, the screen shows a developer debug overlay (DEBUG · MARS coordinates panel, nearby-asset listing panels, a 'Raise ramp' button) over an almost entirely black background instead of the Mars scene.)
- **Screenshot:** [033-lifecycle-rotated-panel.jpg](shots-desktop/033-lifecycle-rotated-panel.jpg)

  ![Looks wrong in the screenshot: 'Raise ra](shots-desktop/033-lifecycle-rotated-panel.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-settings (open Settings, then rotate)

### 23. Looks wrong in the screenshot: 'Raise ramp' button directly overlaps the 'World / crew' button

- **How bad:** Minor (score 49)
- **Where:** random tapping everywhere, first at 03:25 into the run, on desktop (Chromium)
- **What happened:** bottom-left corner (the vision model's description of the screen: End of the 30-tap monkey-test pass, screen still shows the same developer debug overlay (coordinates, asset list panels, 'Raise ramp' button) over a black background.)
- **Screenshot:** [042-monkey-end-of-monkey.jpg](shots-desktop/042-monkey-end-of-monkey.jpg)

  ![Looks wrong in the screenshot: 'Raise ra](shots-desktop/042-monkey-end-of-monkey.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: monkey: 30 random button taps and wild gestures, no crash

### 24. Slow button: #btn-settings took 3.9 s to respond

- **How bad:** Minor (score 44)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:26 into the run, on desktop (Chromium)
- **What happened:** open Settings
- **What the vision model saw:** Desktop Settings panel open over the ship-pad scene, with account sign-in fields, a Start Fresh button, view and digging-tool dropdowns, and a 'Systems nominal' tooltip near the ship. Flagged: small solid teal/turquoise quadrilateral shape with no visible context, looks like a clipped or glitched object/icon
- **Screenshot:** [002-panels-PROBLEM-slow-button.jpg](shots-desktop/002-panels-PROBLEM-slow-button.jpg)

  ![Slow button: #btn-settings took 3.9 s to](shots-desktop/002-panels-PROBLEM-slow-button.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. desktop budget is 5 min and the opening alone takes about 10: started from the review start (use --desktop-opening to play it)
  1. === phase panels starts
  1. mis-tap beside #btn-settings
  1. tap #btn-settings (open Settings)

### 25. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:37 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 03:35 [opening] walk to down the gangway
- **What the vision model saw:** Dusk/night Mars spaceport scene with amber path lights leading to an Arrivals sign, a steward's dialogue line about following the lights, and a Skip intro button top right.
- **Screenshot:** [016-opening-PROBLEM-refusal-message.jpg](shots-iphone/016-opening-PROBLEM-refusal-message.jpg)

  ![Game said: "Welcome to Mars. Follow the ](shots-iphone/016-opening-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. in the boarding hall, waiting for the gangway to come down
  1. walk to down the gangway
  1. walk to down the gangway
  1. walk to down the gangway

### 26. Frame-time spike during "tour"

- **How bad:** Minor (score 38), happened 2 times
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 08:32 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 1111 ms (typical 25 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Desert overlook HUD screen showing location/status panel top left, a distant port complex, and movement joystick/World-crew/Controls buttons bottom left.
- **Later hits:** 13:03 a single frame took 2296 ms (typical 15 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [053-tour-PROBLEM-frame-spike.jpg](shots-iphone/053-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/053-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide
  1. route of 36 legs

### 27. Low text contrast in 2 places

- **How bad:** Minor (score 38)
- **Where:** accessibility and readability scan, first at 00:58 into the run, on desktop (Chromium)
- **What happened:** span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
- **What the vision model saw:** Same Mars landing-pad scene and HUD info box as the previous frame. Flagged: Grey secondary text ('Martian regolith · 3.72 m/s²') has low contrast against the dark brown HUD background, hard to read; Orange 'NEXT' label and surrounding body text blend closely in brightness against the dark brown panel, reducing contrast
- **Screenshot:** [018-a11y-PROBLEM-a11y-contrast.jpg](shots-desktop/018-a11y-PROBLEM-a11y-contrast.jpg)

  ![Low text contrast in 2 places](shots-desktop/018-a11y-PROBLEM-a11y-contrast.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 9.8 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 6 small: span.dim 10px "Martian regolith · 3.72 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; span.hint 10
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"

### 28. Frame-time spike during "a11y"

- **How bad:** Minor (score 38)
- **Where:** accessibility and readability scan, first at 00:59 into the run, on desktop (Chromium)
- **What happened:** a single frame took 2621 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Same Mars pad scene again, identical to images 1 and 2, no visible stutter or spike artifact captured in the still frame. Flagged: Filename flags a frame-rate spike but the still image shows no visible artifact (expected for a performance issue, which stills can't capture)
- **Screenshot:** [022-a11y-PROBLEM-frame-spike.jpg](shots-desktop/022-a11y-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "a11y"](shots-desktop/022-a11y-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 6 small: span.dim 10px "Martian regolith · 3.72 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; span.hint 10
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.
  1. QA pass: a11y: tap targets at least 44 px (Apple guideline) - 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44
  1. QA FAIL: a11y: pinch-zoom is not locked off - width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
  1. QA pass: a11y: a volume or mute control exists
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"","hint":"","caption":"","hud":"Mars · Valles Marineris 13°59'56.9\"S 59°11'47.9\"W +2213.1 m Martian regolith · 3.72 m/s² Hauling cart: 0.0 / 1054 k

### 29. Text smaller than 11 px in 6 places (hard to read on a phone)

- **How bad:** Minor (score 36)
- **Where:** accessibility and readability scan, first at 00:58 into the run, on desktop (Chromium)
- **What happened:** span.dim 10px "Martian regolith · 3.72 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
- **What the vision model saw:** Mars landing-pad scene with the top-left HUD info box (location, coordinates, cart weight, objective text) and no panels open. Flagged: HUD text (coordinates, regolith/gravity stats, objective paragraph) is rendered very small relative to the screen, hard to read at a glance
- **Screenshot:** [017-a11y-PROBLEM-a11y-small-text.jpg](shots-desktop/017-a11y-PROBLEM-a11y-small-text.jpg)

  ![Text smaller than 11 px in 6 places (har](shots-desktop/017-a11y-PROBLEM-a11y-small-text.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: smoke: time from opening the link to the first drawn frames - 21.2 s (headless software rendering, a real phone is usually quicker to draw but slower to download)
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 9.8 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 6 small: span.dim 10px "Martian regolith · 3.72 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; span.hint 10

### 30. 1 buttons have no text or label (a screen reader says nothing)

- **How bad:** Small (score 34)
- **Where:** accessibility and readability scan, first at 00:58 into the run, on desktop (Chromium)
- **What happened:** input.
- **What the vision model saw:** A landed ship/lander on a Mars landing pad with an info HUD panel top-left, a NEXT objective panel, and two menu buttons bottom-left.
- **Screenshot:** [019-a11y-PROBLEM-a11y-noname.jpg](shots-desktop/019-a11y-PROBLEM-a11y-noname.jpg)

  ![1 buttons have no text or label (a scree](shots-desktop/019-a11y-PROBLEM-a11y-noname.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 9.8 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 6 small: span.dim 10px "Martian regolith · 3.72 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; span.hint 10
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.

### 31. Zooming the page is switched off in the viewport tag

- **How bad:** Small (score 30)
- **Where:** accessibility and readability scan, first at 00:58 into the run, on desktop (Chromium)
- **What happened:** width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
- **What the vision model saw:** Same Mars pad scene as image 1, identical view, no visible zoom-lock indicator or UI difference from the prior frame. Flagged: Filename flags a 'zoom locked' problem but nothing on screen shows a zoom/camera lock indicator or any visual symptom of it
- **Screenshot:** [020-a11y-PROBLEM-a11y-zoom-locked.jpg](shots-desktop/020-a11y-PROBLEM-a11y-zoom-locked.jpg)

  ![Zooming the page is switched off in the ](shots-desktop/020-a11y-PROBLEM-a11y-zoom-locked.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 6 small: span.dim 10px "Martian regolith · 3.72 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; span.hint 10
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.
  1. QA pass: a11y: tap targets at least 44 px (Apple guideline) - 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44
  1. QA FAIL: a11y: pinch-zoom is not locked off - width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover

### 32. Network cut for about 12 s and the game said nothing and still thinks it is connected

- **How bad:** Small (score 28)
- **Where:** network cut, refresh offline, slow connection, first at 02:23 into the run, on desktop (Chromium)
- **What happened:** connected=true. A hint only: the bot's offline switch may not cut a socket that is already open, so a real phone going into a tunnel could behave differently.
- **Screenshot:** [037-network-PROBLEM-offline-silent.jpg](shots-desktop/037-network-PROBLEM-offline-silent.jpg)

  ![Network cut for about 12 s and the game ](shots-desktop/037-network-PROBLEM-offline-silent.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: lifecycle: rotate to 900x560 with Settings open, the 3D view fills the screen - {"cw":900,"ch":560,"iw":900,"ih":560}
  1. tap #btn-close-settings (close settings)
  1. === phase network starts
  1. NETWORK CUT
  1. tap #purse (tap while offline)
  1. tap button "Close" (close account-panel)
  1. QA pass: network: while offline the game keeps drawing and does not crash
  1. QA info: network: the game tells the player the connection is gone (within about 12 s) - connected flag true -> true; messages: 

### Console warnings (3 kinds)

- THREE.WebGLRenderer: Texture has been resized from (256x192) to (256x128). (x16)
- THREE.Material: parameter 'map' has value of undefined. (x6)
- THREE.WebGLRenderer: WebGL 1 support was deprecated in r153 and will be removed in r163. (x1)

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 478 s |
| opening the Settings / Account / World / Controls panels | done | 10 s |
| walking the port (or the settlement of the start world) and talking to people | done | 263 s |
| earning the first ship: buy the two lifeboat parts and fit them | skipped (out of time) | 0 s |
| smoke check (load time, download size, warm reload) | skipped (out of time) | 0 s |
| accessibility and readability scan | skipped (out of time) | 0 s |
| app to the background, graphics context lost, phone rotated | skipped (out of time) | 0 s |
| network cut, refresh offline, slow connection | skipped (out of time) | 0 s |
| spamming buttons and jumps | skipped (out of time) | 0 s |
| buy/sell loops and double taps on the shop | skipped (out of time) | 0 s |
| walking and jumping into walls and edges in 8 directions | skipped (out of time) | 0 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| boarding the ship, taking a seat and flying a course | skipped (out of time) | 0 s |
| getting into and driving the survey rover | skipped (out of time) | 0 s |
| spots | skipped (out of time) | 0 s |
| turning on the spot, reading draw calls and frame times | skipped (out of time) | 0 s |
| random tapping everywhere | skipped (out of time) | 0 s |
| leaving the game alone for 90 s | skipped (out of time) | 0 s |
| end-of-run soft-lock check | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | skipped (out of time) | 0 s |

People talked to: 8 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

### Desktop (Chromium, keyboard + mouse)

| Step | Result | Time |
|---|---|---|
| opening the Settings / Account / World / Controls panels | done | 21 s |
| smoke check (load time, download size, warm reload) | done | 10 s |
| accessibility and readability scan | done | 6 s |
| spamming buttons and jumps | done | 25 s |
| app to the background, graphics context lost, phone rotated | done | 43 s |
| network cut, refresh offline, slow connection | done | 35 s |
| turning on the spot, reading draw calls and frame times | done | 10 s |
| random tapping everywhere | done | 33 s |
| walking and jumping into walls and edges in 8 directions | done | 83 s |
| walking the port (or the settlement of the start world) and talking to people | skipped (out of time) | 0 s |
| earning the first ship: buy the two lifeboat parts and fit them | skipped (out of time) | 0 s |
| buy/sell loops and double taps on the shop | skipped (out of time) | 0 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| leaving the game alone for 90 s | skipped (out of time) | 0 s |
| end-of-run soft-lock check | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | done | 21 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / opening: typical 16 ms, slowest 7306 ms, 2 frames over 250 ms
- iphone / opening: typical 30 ms, slowest 6958 ms, 1 frames over 250 ms
- iphone / opening: typical 15 ms, slowest 5551 ms, 2 frames over 250 ms
- desktop / freeplay: typical 4 ms, slowest 4583 ms, 2 frames over 250 ms
- desktop / network: typical 4 ms, slowest 4566 ms, 3 frames over 250 ms

Button response time (tap to something changing on screen): median 135 ms, slowest 3939 ms over 16 taps.

## QA checks (the things real testers do besides playing through)

See `tools/playtester/PRACTICES.md` for why each one exists. FAIL rows are also listed as problems above where they are real bugs.

### Desktop (Chromium, keyboard + mouse): 19 passed, 4 failed, 1 skipped, 3 info

| Check | Result | Notes |
|---|---|---|
| smoke: page transfer on a cold load | info | 250 requests, 0.1 MB over the wire (slowest: eartbeatobservatory.com/games/the-cosmos/src/vehicles/api.js 100 ms) |
| smoke: time from opening the link to the first drawn frames | pass | 21.2 s (headless software rendering, a real phone is usually quicker to draw but slower to download) |
| smoke: warm reload comes back | pass | 9.8 s |
| a11y: text is at least 11 px | FAIL | 6 small: span.dim 10px "Martian regolith · 3.72 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for de |
| a11y: text contrast (4.5:1, or 3:1 for big text) | FAIL | 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel" |
| a11y: every button has a name | FAIL | input. |
| a11y: tap targets at least 44 px (Apple guideline) | pass | 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44 |
| a11y: pinch-zoom is not locked off | FAIL | width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover |
| a11y: a volume or mute control exists | pass |  |
| readability: something on screen tells a player what to do next | pass | {"action":"","hint":"","caption":"","hud":"Mars · Valles Marineris 13°59'56.9\"S 59°11'47.9\"W +2213.1 m Martian regolith · 3.72 m/s² Hauling cart: 0.0 / 1054 kg too","jobs":"","toast":"Systems nominal. Ship down and sta |
| spam: opener buttons hammered 10 times each, panels still open and close cleanly | pass |  |
| spam: action button | skipped | button says "" (not safe to hammer) |
| spam: 25 jumps and wild looks, game keeps drawing | pass |  |
| lifecycle: background 8 s and return keeps place, money and ship state | pass |  |
| lifecycle: graphics context lost, game reloads itself into safe mode and still plays | info | the game restarted with ?tier=safe (reduced graphics). Banner: "Graphics problem: WebGL context lost - safe mode active" |
| lifecycle: rotate to 900x560, the 3D view fills the screen | pass | {"cw":900,"ch":560,"iw":900,"ih":560} |
| lifecycle: rotate to 900x560 with Settings open, the 3D view fills the screen | pass | {"cw":900,"ch":560,"iw":900,"ih":560} |
| network: while offline the game keeps drawing and does not crash | pass |  |
| network: the game tells the player the connection is gone (within about 12 s) | info | connected flag true -> true; messages:  |
| network: after the network returns the game reconnects and answers again | pass | 2 s |
| network: money and place unchanged by a network blip | pass |  |
| network: refresh while offline, then online again, the game comes back | pass |  |
| network: slow connection (900 ms, 60 KB/s) for a panel tap | pass | 5 s |
| perf: turning on the spot, 95 percent of frames under 34 ms | pass | median 29 ms, 95th 33 ms, slowest 371 ms; peak 130 draw calls, 37k triangles (headless software rendering, judge relatively) |
| monkey: 30 random button taps and wild gestures, no crash | pass |  |
| edges: walked and jumped into walls in 8 directions, never fell through | pass | furthest 39 m from where it started |
| edges: still drawing afterwards | pass |  |

## Load, size and memory

- **iPhone 15 (WebKit, touch)**: load to first frames 14.5 s; cold-load download 1.3 MB in 250 requests; warm reload not measured; busiest view not measured. Over the run (41 samples): graphics geometries 331 -> 51, textures 122 -> 26, page elements 235 -> 220 (JS heap is only readable in Chromium).
- **Desktop (Chromium, keyboard + mouse)**: load to first frames 21.2 s; cold-load download 0.1 MB in 250 requests; warm reload 9.8 s; busiest view 130 draw calls, 37k triangles. Over the run (36 samples): graphics geometries 397 -> 291, textures 208 -> 165, page elements 276 -> 219, JS heap 258 -> 220 MB.

## Vision pass

A vision model (claude CLI (sonnet)) looked at 36 screenshots for about $0.00 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
- Not possible from here (needs a real iPhone or two players): a real phone call or notification banner, lock screen, battery and heat, low-end phone speed, many device models, race-condition duplication between two players. The full list of what real QA does and which parts the bot covers is in tools/playtester/PRACTICES.md.
