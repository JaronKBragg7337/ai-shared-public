# The Cosmos playtest report

Run: 2026-10-09 01:24 (local)  |  Build under test: `3744d951f2a39a32653e`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

**How to read this:** items titled "Stuck while walking to ..." come from the bot's own steering (its path planner, run-ups and jumps). Treat them as bot-only unless a human also gets stuck at that spot. Black boot and crash-blackout frames that carry a caption are deliberate.

- **iPhone 15 (WebKit, touch)**: 15.8 minutes, 109 screenshots, 7 distinct problems
- **Desktop (Chromium, keyboard + mouse)**: 5.1 minutes, 46 screenshots, 16 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)
- Desktop (Chromium, keyboard + mouse): [session video](videos-desktop/<email>)

## Short version

31 distinct problems found: 1 blockers, 3 serious, 27 smaller.

- **Page error (uncaught exception)** (BLOCKER)
- **Stuck while walking to Shift runner** (Serious)
- **Stuck while walking to Lookout at the glass** (Serious)
- **After the graphics context was lost and restored, the game never drew again** (Serious)
- **A button is covered by something else: #multiplayer-button "World / crew" is covered by #touch-key-KeyD** (Annoying)

## Problems, worst first

### 1. Page error (uncaught exception)

- **How bad:** BLOCKER (score 95)
- **Where:** random tapping everywhere, first at 02:52 into the run, on desktop (Chromium)
- **What happened:** NotAllowedError: Failed to execute 'requestPointerLock' on 'Element': Too many pointer lock requests in a short window of time. |     at HTMLCanvasElement.<anonymous> (https://www.heartbeatobservatory.com/games/the-cosmos/src/ui/touch.js?v=3744d951f2a39a32653e:205:91)
- **Screenshot:** [038-monkey-PROBLEM-page-error.jpg](shots-desktop/038-monkey-PROBLEM-page-error.jpg)

  ![Page error (uncaught exception)](shots-desktop/038-monkey-PROBLEM-page-error.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap on empty 3D view at 710,625
  1. monkey tap btn-key-controls
  1. tap on empty 3D view at 1214,328
  1. tap on empty 3D view at 184,350
  1. tap on empty 3D view at 305,305
  1. tap on empty 3D view at 777,437
  1. monkey tap touch-key-KeyW
  1. tap on empty 3D view at 878,590

### 2. Stuck while walking to Shift runner

- **How bad:** Serious (score 80)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 13:36 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -61,-41 (target -64,-41, 3 m away)
- **What the vision model saw:** Overworld HUD view where a bright, overexposed diagonal stripe (blown-out/clipped geometry or lighting) cuts across the entire screen, obscuring the scene behind it. Flagged: Large bright white/tan diagonal band dominates the view, looks like a broken or overexposed texture/geometry rendering through everything behind it; Button label is truncated, reads 'Left to lo...' instead of full text; Small triangular arrow icon floating alone with no visible attached UI element
- **Screenshot:** [103-tour-PROBLEM-stuck-walking.jpg](shots-iphone/103-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Shift runner](shots-iphone/103-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (3 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 3 legs
  1. not getting closer (3 m away), trying to get unstuck #6
  1. not getting closer (3 m away), trying to get unstuck #7
  1. not getting closer (3 m away), trying to get unstuck #8

### 3. Stuck while walking to Lookout at the glass

- **How bad:** Serious (score 80)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 14:52 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -59,-41 (target -56,-41, 4 m away)
- **What the vision model saw:** First-person phone view from inside a dim cabin/boat interior, with a HUD showing Mars coordinates and a NEXT objective about buying a power cell, plus bottom buttons for World/crew, Controls, Talk/Watch supervisor, and a grayed-out Lift-to-lobby button. Flagged: A huge, overly bright vertical white bar/beam fills most of the center of the screen, looking like a broken texture or the player wedged inside wall/ladder geometry rather than a lit hallway; A semi-transparent dotted circle floats in the middle of the view with no label, unclear what it represents (possibly a stuck interaction prompt or joystick remnant); A tan arrow icon floats in open air mid-screen pointing right, not attached to any visible path or object; "Lift to lobby (E)" button is grayed out/unusable while the player appears stuck, consistent with the reported stuck-walking bug
- **Screenshot:** [106-tour-PROBLEM-stuck-walking.jpg](shots-iphone/106-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Lookout at the gl](shots-iphone/106-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (4 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 3 legs
  1. not getting closer (4 m away), trying to get unstuck #6
  1. not getting closer (4 m away), trying to get unstuck #7
  1. not getting closer (4 m away), trying to get unstuck #8

### 4. After the graphics context was lost and restored, the game never drew again

- **How bad:** Serious (score 80)
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:36 into the run, on desktop (Chromium)
- **What happened:** (see screenshot)
- **What the vision model saw:** Boot/loading screen: near-black background with the title THE COSMOS, a tagline, and a 'Loading the port...' caption.
- **Screenshot:** [026-lifecycle-PROBLEM-context-not-restored.jpg](shots-desktop/026-lifecycle-PROBLEM-context-not-restored.jpg)

  ![After the graphics context was lost and ](shots-desktop/026-lifecycle-PROBLEM-context-not-restored.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. jump
  1. QA pass: spam: 25 jumps and wild looks, game keeps drawing
  1. spam: 0 requests sent, purse 10000 -> 10000
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. QA FAIL: lifecycle: graphics context lost and restored, game draws again - events: ["lost"]

### 5. A button is covered by something else: #multiplayer-button "World / crew" is covered by #touch-key-KeyD

- **How bad:** Annoying (score 68)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:33 into the run, on desktop (Chromium)
- **What happened:** #multiplayer-button "World / crew" is covered by #touch-key-KeyD (Controls open, desktop)
- **What the vision model saw:** Desktop exterior Mars landing pad scene, after the bot tapped Controls again to close the panel, but the Controls panel is still fully open and identical to the previous screenshot. Flagged: The Controls panel did not close after the toggle-closed tap — it remains open and visually unchanged from before the action; World/crew button is still hidden/covered by the stuck-open Controls panel
- **Screenshot:** [011-panels-PROBLEM-covered.jpg](shots-desktop/011-panels-PROBLEM-covered.jpg)

  ![A button is covered by something else: #](shots-desktop/011-panels-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. mis-tap beside #btn-key-controls
  1. tap #btn-key-controls (open Controls)

### 6. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 4 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:29 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 4 after tapping "Dig (E)"
- **What the vision model saw:** First-person view on the Mars surface aiming a shovel at a half-buried crate, with a 'Dig (E)' button and an instruction caption.
- **Later hits:** 06:31 cuts stayed 4 after tapping "Dig (E)" / 06:32 cuts stayed 4 after tapping "Dig (E)"
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

### 7. Buttons overlap: #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83%

- **How bad:** Annoying (score 66)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:33 into the run, on desktop (Chromium)
- **What happened:** #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83% (Controls open, desktop)
- **What the vision model saw:** Desktop exterior Mars landing pad scene with the Controls keybindings panel open at bottom left, listing action buttons like Debug, View, Fire, movement keys, etc. Flagged: The World/crew button, visible in other shots at this same bottom-left spot, is missing/hidden — the Controls panel appears to be covering or replacing it
- **Screenshot:** [010-panels-PROBLEM-overlap.jpg](shots-desktop/010-panels-PROBLEM-overlap.jpg)

  ![Buttons overlap: #touch-key-KeyD "Right"](shots-desktop/010-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. mis-tap beside #btn-key-controls
  1. tap #btn-key-controls (open Controls)

### 8. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 8 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:14 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 3970 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Interior ship lounge/common area with a round orange object visible through the windows, an NPC named Walter speaking a line of dialogue at the bottom.
- **Later hits:** 05:49 a single frame took 4259 ms (typical 27 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 06:02 a single frame took 1089 ms (typical 21 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 9. Frame-time spike during "lifecycle"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:44 into the run, on desktop (Chromium)
- **What happened:** a single frame took 4171 ms (typical 4 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Same Mars spaceport scene as earlier images, with an added status tooltip reading 'Systems nominal. Ship down and stable.' near the ship. Flagged: Status tooltip box sits very close to/overlapping the bottom edge of the HUD panel above it; Cyan/teal patch on the ground, out of place color/texture
- **Later hits:** 01:56 a single frame took 2550 ms (typical 25 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [027-lifecycle-PROBLEM-frame-spike.jpg](shots-desktop/027-lifecycle-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "lifecycle"](shots-desktop/027-lifecycle-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: spam: 25 jumps and wild looks, game keeps drawing
  1. spam: 0 requests sent, purse 10000 -> 10000
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. QA FAIL: lifecycle: graphics context lost and restored, game draws again - events: ["lost"]
  1. REFRESH (recovering after a lost graphics context)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 10. Frame-time spike during "network"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** network cut, refresh offline, slow connection, first at 02:26 into the run, on desktop (Chromium)
- **What happened:** a single frame took 4529 ms (typical 4 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 02:31 a single frame took 2667 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [034-network-PROBLEM-frame-spike.jpg](shots-desktop/034-network-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "network"](shots-desktop/034-network-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. NETWORK BACK
  1. QA pass: network: after the network returns the game reconnects and answers again - 2 s
  1. QA pass: network: money and place unchanged by a network blip
  1. REFRESH (refresh after being offline)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: network: refresh while offline, then online again, the game comes back
  1. SLOW NETWORK on (900 ms delay, 60 KB/s)
  1. tap #btn-settings (tap on a slow network)

### 11. Frame-time spike during "panels"

- **How bad:** Annoying (score 62)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:19 into the run, on desktop (Chromium)
- **What happened:** a single frame took 6412 ms (typical 4 ms); 6 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Desktop exterior Mars landing pad scene with the Settings panel open on the right, showing sign-in fields and start-fresh/ship options.
- **Screenshot:** [003-panels-PROBLEM-frame-spike.jpg](shots-desktop/003-panels-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "panels"](shots-desktop/003-panels-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. desktop budget is 5 min and the opening alone takes about 10: started from the review start (use --desktop-opening to play it)
  1. === phase panels starts
  1. tap #btn-settings (open Settings)

### 12. Frame-time spike during "smoke"

- **How bad:** Annoying (score 62)
- **Where:** smoke check (load time, download size, warm reload), first at 00:44 into the run, on desktop (Chromium)
- **What happened:** a single frame took 4300 ms (typical 4 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Desktop exterior Mars landing pad scene in its normal state, HUD panel top-left, World/crew and Controls buttons bottom-left, no panels open.
- **Screenshot:** [013-smoke-PROBLEM-frame-spike.jpg](shots-desktop/013-smoke-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "smoke"](shots-desktop/013-smoke-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase smoke starts
  1. QA info: smoke: page transfer on a cold load - 250 requests, 1.3 MB over the wire (slowest: tbeatobservatory.com/games/the-cosmos/src/voice/proximity.js 127 ms)
  1. QA pass: smoke: time from opening the link to the first drawn frames - 13.7 s (headless software rendering, a real phone is usually quicker to draw but slower to download)
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 9.3 s

### 13. Frame-time spike during "freeplay"

- **How bad:** Annoying (score 62)
- **Where:** free play (random walking, tapping, refreshing), first at 05:03 into the run, on desktop (Chromium)
- **What happened:** a single frame took 4246 ms (typical 4 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [045-freeplay-PROBLEM-frame-spike.jpg](shots-desktop/045-freeplay-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "freeplay"](shots-desktop/045-freeplay-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. jump
  1. QA pass: edges: walked and jumped into walls in 8 directions, never fell through - furthest 56 m from where it started
  1. QA pass: edges: still drawing afterwards
  1. === phase freeplay starts
  1. tap on empty 3D view at 476,604
  1. REFRESH (random refresh while playing)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 14. Looks wrong in the screenshot: Large bright white/tan diagonal band dominates the view, looks like a broken or overexposed texture/geometry r

- **How bad:** Annoying (score 56)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 13:36 into the run, on iPhone (WebKit)
- **What happened:** center of screen, running diagonally top-right to bottom-left (the vision model's description of the screen: Overworld HUD view where a bright, overexposed diagonal stripe (blown-out/clipped geometry or lighting) cuts across the entire screen, obscuring the scene behind it.)
- **Screenshot:** [103-tour-PROBLEM-stuck-walking.jpg](shots-iphone/103-tour-PROBLEM-stuck-walking.jpg)

  ![Looks wrong in the screenshot: Large bri](shots-iphone/103-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to Lookout at the glass

### 15. Looks wrong in the screenshot: A huge, overly bright vertical white bar/beam fills most of the center of the screen, looking like a broken te

- **How bad:** Annoying (score 56)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 14:53 into the run, on iPhone (WebKit)
- **What happened:** center of screen, full height (the vision model's description of the screen: First-person phone view from inside a dim cabin/boat interior, with a HUD showing Mars coordinates and a NEXT objective about buying a power cell, plus bottom buttons for World/crew, Controls, Talk/Watch supervisor, and a grayed-out Lift-to-lobby button.)
- **Screenshot:** [106-tour-PROBLEM-stuck-walking.jpg](shots-iphone/106-tour-PROBLEM-stuck-walking.jpg)

  ![Looks wrong in the screenshot: A huge, o](shots-iphone/106-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to cab landing

### 16. Looks wrong in the screenshot: The Controls panel did not close after the toggle-closed tap — it remains open and visually unchanged from bef

- **How bad:** Annoying (score 56)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:33 into the run, on desktop (Chromium)
- **What happened:** bottom left panel (the vision model's description of the screen: Desktop exterior Mars landing pad scene, after the bot tapped Controls again to close the panel, but the Controls panel is still fully open and identical to the previous screenshot.)
- **Screenshot:** [011-panels-PROBLEM-covered.jpg](shots-desktop/011-panels-PROBLEM-covered.jpg)

  ![Looks wrong in the screenshot: The Contr](shots-desktop/011-panels-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (toggle closed Controls)

### 17. Looks wrong in the screenshot: The interior room (yellow-panelled walls, hanging lights, furniture) appears to float directly above the dirt 

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:27 into the run, on iPhone (WebKit)
- **What happened:** upper third of the screen, where interior meets the dust field (the vision model's description of the screen: Split view of a lit ship/hangar interior sitting above a red Martian dust field with rocks, a small crate/rover with a flag, and a 'Dig (E)' prompt.)
- **Screenshot:** [033-opening-opening.jpg](shots-iphone/033-opening-opening.jpg)

  ![Looks wrong in the screenshot: The inter](shots-iphone/033-opening-opening.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 18. Looks wrong in the screenshot: Three large flat, untextured color panels (blue, green, white) with no icons or content are visible, looking l

- **How bad:** Minor (score 49)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 11:37 into the run, on iPhone (WebKit)
- **What happened:** Bottom edge of the screen, below the dialogue panel, cut off by the screen bottom (the vision model's description of the screen: Dialogue panel with the 'Watch supervisor' NPC open, showing a job offer and an 'Accept · A tonne for the foundation' button which was just tapped.)
- **Screenshot:** [082-tour-quest-accepted.jpg](shots-iphone/082-tour-quest-accepted.jpg)

  ![Looks wrong in the screenshot: Three lar](shots-iphone/082-tour-quest-accepted.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap button "Accept · A tonne for the foundation" (accept the job)

### 19. Looks wrong in the screenshot: "Lift to lobby (E)" button is grayed out/unusable while the player appears stuck, consistent with the reported

- **How bad:** Minor (score 49)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 14:53 into the run, on iPhone (WebKit)
- **What happened:** bottom right button (the vision model's description of the screen: First-person phone view from inside a dim cabin/boat interior, with a HUD showing Mars coordinates and a NEXT objective about buying a power cell, plus bottom buttons for World/crew, Controls, Talk/Watch supervisor, and a grayed-out Lift-to-lobby button.)
- **Screenshot:** [106-tour-PROBLEM-stuck-walking.jpg](shots-iphone/106-tour-PROBLEM-stuck-walking.jpg)

  ![Looks wrong in the screenshot: "Lift to ](shots-iphone/106-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to cab landing

### 20. Looks wrong in the screenshot: The World/crew button, visible in other shots at this same bottom-left spot, is missing/hidden — the Controls 

- **How bad:** Minor (score 49)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:33 into the run, on desktop (Chromium)
- **What happened:** bottom left, where World/crew normally sits (the vision model's description of the screen: Desktop exterior Mars landing pad scene with the Controls keybindings panel open at bottom left, listing action buttons like Debug, View, Fire, movement keys, etc.)
- **Screenshot:** [010-panels-PROBLEM-overlap.jpg](shots-desktop/010-panels-PROBLEM-overlap.jpg)

  ![Looks wrong in the screenshot: The World](shots-desktop/010-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (open Controls)

### 21. Looks wrong in the screenshot: World/crew button is still hidden/covered by the stuck-open Controls panel

- **How bad:** Minor (score 49)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:33 into the run, on desktop (Chromium)
- **What happened:** bottom left, where World/crew normally sits (the vision model's description of the screen: Desktop exterior Mars landing pad scene, after the bot tapped Controls again to close the panel, but the Controls panel is still fully open and identical to the previous screenshot.)
- **Screenshot:** [011-panels-PROBLEM-covered.jpg](shots-desktop/011-panels-PROBLEM-covered.jpg)

  ![Looks wrong in the screenshot: World/cre](shots-desktop/011-panels-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (toggle closed Controls)

### 22. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:36 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 03:34 [opening] walk to down the gangway
- **What the vision model saw:** Dusk intro scene looking down a road toward a lit 'ARRIVALS' sign at a Mars port, with a Steward's welcome dialogue at the bottom and a Skip intro button top-right.
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

### 23. Game said: "Weather sensors are offline. Watch the dust outside."

- **How bad:** Minor (score 42)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 12:19 into the run, on iPhone (WebKit)
- **What happened:** shown in crew-panel while the bot was: 12:18 [tour] tap button "Understood. What can I do here?" (answer back)
- **What the vision model saw:** Dialogue panel open with a 'Weather officer' NPC saying weather sensors are offline, with two reply options and a close (✕) button, over the same status HUD and a corridor background.
- **Screenshot:** [098-tour-PROBLEM-refusal-message.jpg](shots-iphone/098-tour-PROBLEM-refusal-message.jpg)

  ![Game said: "Weather sensors are offline.](shots-iphone/098-tour-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #crew-talk (Talk to Weather officer)
  1. opened Ground controller instead of Weather officer; stepping closer to the right person
  1. tap button "✕" (close talk panel)
  1. go talk to Weather officer
  1. walk to Weather officer
  1. tap #crew-talk (Talk to Weather officer)
  1. tap button "What is your watch like?" (ask them something)
  1. tap button "Understood. What can I do here?" (answer back)

### 24. Frame-time spike during "tour"

- **How bad:** Minor (score 38), happened 2 times
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 08:35 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 1010 ms (typical 26 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Overworld HUD during the tour phase showing location/status readout, a desert road leading to distant buildings, a movement joystick, and 'World / crew' and 'Controls' buttons.
- **Later hits:** 15:44 a single frame took 3667 ms (typical 16 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
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
  1. route of 28 legs

### 25. Low text contrast in 2 places

- **How bad:** Minor (score 38)
- **Where:** accessibility and readability scan, first at 00:48 into the run, on desktop (Chromium)
- **What happened:** span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
- **What the vision model saw:** Landed ship on a Mars spaceport pad (PAD 06) with a HUD info panel top-left (location, terrain, hauling cart, current tool, and a 'NEXT' objective telling the player to find the Crew Hall) and World/crew and Controls buttons bottom-left. Flagged: Small flat cyan/teal patch on the ground, color and shape don't match the surrounding Martian terrain — looks like a misplaced or clipped object/texture; No player name, callsign, or ship ID shown anywhere in the HUD
- **Screenshot:** [017-a11y-PROBLEM-a11y-contrast.jpg](shots-desktop/017-a11y-PROBLEM-a11y-contrast.jpg)

  ![Low text contrast in 2 places](shots-desktop/017-a11y-PROBLEM-a11y-contrast.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 9.3 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"

### 26. Frame-time spike during "a11y"

- **How bad:** Minor (score 38)
- **Where:** accessibility and readability scan, first at 00:49 into the run, on desktop (Chromium)
- **What happened:** a single frame took 2587 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Same Mars spaceport scene again, identical HUD panel and buttons. Flagged: Cyan/teal patch on the ground, out of place color/texture
- **Screenshot:** [021-a11y-PROBLEM-frame-spike.jpg](shots-desktop/021-a11y-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "a11y"](shots-desktop/021-a11y-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.
  1. QA pass: a11y: tap targets at least 44 px (Apple guideline) - 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44
  1. QA FAIL: a11y: pinch-zoom is not locked off - width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
  1. QA pass: a11y: a volume or mute control exists
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"","hint":"","caption":"","hud":"Mars · Valles Marineris 13°59'50.7\"S 59°11'39.9\"W +2213.1 m Martian regolith · 3.72 m/s² Hauling cart: 0.0 / 1054 k

### 27. Frame-time spike during "perf"

- **How bad:** Minor (score 38)
- **Where:** turning on the spot, reading draw calls and frame times, first at 02:40 into the run, on desktop (Chromium)
- **What happened:** a single frame took 829 ms (typical 25 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [036-perf-PROBLEM-frame-spike.jpg](shots-desktop/036-perf-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "perf"](shots-desktop/036-perf-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (refresh after being offline)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: network: refresh while offline, then online again, the game comes back
  1. SLOW NETWORK on (900 ms delay, 60 KB/s)
  1. tap #btn-settings (tap on a slow network)
  1. tap #btn-close-settings (close settings)
  1. QA pass: network: slow connection (900 ms, 60 KB/s) for a panel tap - 6 s
  1. === phase perf starts

### 28. Text smaller than 11 px in 2 places (hard to read on a phone)

- **How bad:** Minor (score 36)
- **Where:** accessibility and readability scan, first at 00:48 into the run, on desktop (Chromium)
- **What happened:** span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
- **What the vision model saw:** Desktop exterior Mars landing pad scene identical in layout to the normal view, with the top-left HUD panel showing status text and the NEXT objective. Flagged: HUD text (coordinates, regolith stats, NEXT objective paragraph) is rendered quite small relative to the 1280x800 screen, making it hard to read at a glance, consistent with the readability/a11y check being run
- **Screenshot:** [016-a11y-PROBLEM-a11y-small-text.jpg](shots-desktop/016-a11y-PROBLEM-a11y-small-text.jpg)

  ![Text smaller than 11 px in 2 places (har](shots-desktop/016-a11y-PROBLEM-a11y-small-text.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: smoke: time from opening the link to the first drawn frames - 13.7 s (headless software rendering, a real phone is usually quicker to draw but slower to download)
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 9.3 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"

### 29. 1 buttons have no text or label (a screen reader says nothing)

- **How bad:** Small (score 34)
- **Where:** accessibility and readability scan, first at 00:48 into the run, on desktop (Chromium)
- **What happened:** input.
- **What the vision model saw:** Same Mars spaceport scene as image 1, identical HUD panel and buttons. Flagged: No player name, callsign, or ship/character identifier visible anywhere on screen; Same cyan/teal patch on the ground, inconsistent with surrounding terrain color
- **Screenshot:** [018-a11y-PROBLEM-a11y-noname.jpg](shots-desktop/018-a11y-PROBLEM-a11y-noname.jpg)

  ![1 buttons have no text or label (a scree](shots-desktop/018-a11y-PROBLEM-a11y-noname.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 9.3 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.

### 30. Zooming the page is switched off in the viewport tag

- **How bad:** Small (score 30)
- **Where:** accessibility and readability scan, first at 00:48 into the run, on desktop (Chromium)
- **What happened:** width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
- **What the vision model saw:** Same Mars spaceport scene again, identical HUD panel and buttons as images 1-2. Flagged: Cyan/teal patch on the ground, out of place color/texture
- **Screenshot:** [019-a11y-PROBLEM-a11y-zoom-locked.jpg](shots-desktop/019-a11y-PROBLEM-a11y-zoom-locked.jpg)

  ![Zooming the page is switched off in the ](shots-desktop/019-a11y-PROBLEM-a11y-zoom-locked.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.
  1. QA pass: a11y: tap targets at least 44 px (Apple guideline) - 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44
  1. QA FAIL: a11y: pinch-zoom is not locked off - width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover

### 31. Network cut for about 12 s and the game said nothing and still thinks it is connected

- **How bad:** Small (score 28)
- **Where:** network cut, refresh offline, slow connection, first at 02:12 into the run, on desktop (Chromium)
- **What happened:** connected=true. A hint only: the bot's offline switch may not cut a socket that is already open, so a real phone going into a tunnel could behave differently.
- **What the vision model saw:** Daytime Mars port scene (Valles Marineris) with a cargo ship's open cargo bay and ramp, an info/quest panel top-left, and UI buttons (Settings, World/crew, Controls, Raise ramp). Flagged: No network status indicator, error banner, or reconnect message visible anywhere, even though this screenshot is tagged as the network-recovery moment ('NETWORK BACK') — the UI gives the player no feedback that connectivity was lost and restored
- **Screenshot:** [033-network-PROBLEM-offline-silent.jpg](shots-desktop/033-network-PROBLEM-offline-silent.jpg)

  ![Network cut for about 12 s and the game ](shots-desktop/033-network-PROBLEM-offline-silent.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: lifecycle: rotate to 900x560 with Settings open, the 3D view fills the screen - {"cw":900,"ch":560,"iw":900,"ih":560}
  1. tap #btn-close-settings (close settings)
  1. === phase network starts
  1. NETWORK CUT
  1. tap #purse (tap while offline)
  1. tap button "Close" (close account-panel)
  1. QA pass: network: while offline the game keeps drawing and does not crash
  1. QA info: network: the game tells the player the connection is gone (within about 12 s) - connected flag true -> true; messages: 

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 477 s |
| opening the Settings / Account / World / Controls panels | done | 10 s |
| walking the port (or the settlement of the start world) and talking to people | done | 432 s |
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

People talked to: 13 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

### Desktop (Chromium, keyboard + mouse)

| Step | Result | Time |
|---|---|---|
| opening the Settings / Account / World / Controls panels | done | 20 s |
| smoke check (load time, download size, warm reload) | done | 10 s |
| accessibility and readability scan | done | 6 s |
| spamming buttons and jumps | done | 25 s |
| app to the background, graphics context lost, phone rotated | done | 42 s |
| network cut, refresh offline, slow connection | done | 35 s |
| turning on the spot, reading draw calls and frame times | done | 10 s |
| random tapping everywhere | done | 32 s |
| walking and jumping into walls and edges in 8 directions | done | 95 s |
| walking the port (or the settlement of the start world) and talking to people | skipped (out of time) | 0 s |
| earning the first ship: buy the two lifeboat parts and fit them | skipped (out of time) | 0 s |
| buy/sell loops and double taps on the shop | skipped (out of time) | 0 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| leaving the game alone for 90 s | skipped (out of time) | 0 s |
| end-of-run soft-lock check | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | done | 16 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / opening: typical 16 ms, slowest 6720 ms, 2 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 6671 ms, 4 frames over 250 ms
- desktop / panels: typical 4 ms, slowest 6412 ms, 6 frames over 250 ms
- desktop / network: typical 4 ms, slowest 4529 ms, 3 frames over 250 ms
- desktop / smoke: typical 4 ms, slowest 4300 ms, 2 frames over 250 ms

Button response time (tap to something changing on screen): median 128 ms, slowest 1351 ms over 24 taps.

## QA checks (the things real testers do besides playing through)

See `tools/playtester/PRACTICES.md` for why each one exists. FAIL rows are also listed as problems above where they are real bugs.

### Desktop (Chromium, keyboard + mouse): 19 passed, 5 failed, 1 skipped, 2 info

| Check | Result | Notes |
|---|---|---|
| smoke: page transfer on a cold load | info | 250 requests, 1.3 MB over the wire (slowest: tbeatobservatory.com/games/the-cosmos/src/voice/proximity.js 127 ms) |
| smoke: time from opening the link to the first drawn frames | pass | 13.7 s (headless software rendering, a real phone is usually quicker to draw but slower to download) |
| smoke: warm reload comes back | pass | 9.3 s |
| a11y: text is at least 11 px | FAIL | 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel" |
| a11y: text contrast (4.5:1, or 3:1 for big text) | FAIL | 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel" |
| a11y: every button has a name | FAIL | input. |
| a11y: tap targets at least 44 px (Apple guideline) | pass | 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44 |
| a11y: pinch-zoom is not locked off | FAIL | width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover |
| a11y: a volume or mute control exists | pass |  |
| readability: something on screen tells a player what to do next | pass | {"action":"","hint":"","caption":"","hud":"Mars · Valles Marineris 13°59'50.7\"S 59°11'39.9\"W +2213.1 m Martian regolith · 3.72 m/s² Hauling cart: 0.0 / 1054 kg too","jobs":"","toast":"Systems nominal. Ship down and sta |
| spam: opener buttons hammered 10 times each, panels still open and close cleanly | pass |  |
| spam: action button | skipped | button says "" (not safe to hammer) |
| spam: 25 jumps and wild looks, game keeps drawing | pass |  |
| lifecycle: background 8 s and return keeps place, money and ship state | pass |  |
| lifecycle: graphics context lost and restored, game draws again | FAIL | events: ["lost"] |
| lifecycle: rotate to 900x560, the 3D view fills the screen | pass | {"cw":900,"ch":560,"iw":900,"ih":560} |
| lifecycle: rotate to 900x560 with Settings open, the 3D view fills the screen | pass | {"cw":900,"ch":560,"iw":900,"ih":560} |
| network: while offline the game keeps drawing and does not crash | pass |  |
| network: the game tells the player the connection is gone (within about 12 s) | info | connected flag true -> true; messages:  |
| network: after the network returns the game reconnects and answers again | pass | 2 s |
| network: money and place unchanged by a network blip | pass |  |
| network: refresh while offline, then online again, the game comes back | pass |  |
| network: slow connection (900 ms, 60 KB/s) for a panel tap | pass | 6 s |
| perf: turning on the spot, 95 percent of frames under 34 ms | pass | median 25 ms, 95th 33 ms, slowest 829 ms; peak 130 draw calls, 37k triangles (headless software rendering, judge relatively) |
| monkey: 28 random button taps and wild gestures, no crash | pass |  |
| edges: walked and jumped into walls in 8 directions, never fell through | pass | furthest 56 m from where it started |
| edges: still drawing afterwards | pass |  |

## Load, size and memory

- **iPhone 15 (WebKit, touch)**: load to first frames 13.9 s; cold-load download 1.3 MB in 250 requests; warm reload not measured; busiest view not measured. Over the run (49 samples): graphics geometries 334 -> 53, textures 122 -> 26, page elements 236 -> 220 (JS heap is only readable in Chromium).
- **Desktop (Chromium, keyboard + mouse)**: load to first frames 13.7 s; cold-load download 1.3 MB in 250 requests; warm reload 9.3 s; busiest view 130 draw calls, 37k triangles. Over the run (36 samples): graphics geometries 257 -> 157, textures 198 -> 156, page elements 277 -> 219, JS heap 247 -> 211 MB.

## Vision pass

A vision model (claude CLI (sonnet)) looked at 36 screenshots for about $0.00 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
- Not possible from here (needs a real iPhone or two players): a real phone call or notification banner, lock screen, battery and heat, low-end phone speed, many device models, race-condition duplication between two players. The full list of what real QA does and which parts the bot covers is in tools/playtester/PRACTICES.md.
