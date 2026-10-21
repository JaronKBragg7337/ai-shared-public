# The Cosmos playtest report

Run: 2026-10-09 00:10 (local)  |  Build under test: `7b8a58d96396c0a7036e`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

**How to read this:** items titled "Stuck while walking to ..." come from the bot's own steering (its path planner, run-ups and jumps). Treat them as bot-only unless a human also gets stuck at that spot. Black boot and crash-blackout frames that carry a caption are deliberate.

- **iPhone 15 (WebKit, touch)**: 15 minutes, 88 screenshots, 9 distinct problems
- **Desktop (Chromium, keyboard + mouse)**: 5.1 minutes, 47 screenshots, 19 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)
- Desktop (Chromium, keyboard + mouse): [session video](videos-desktop/<email>)

## Short version

33 distinct problems found: 0 blockers, 0 serious, 33 smaller.

- **A button is covered by something else: #multiplayer-button "World / crew" is covered by #touch-key-KeyD** (Annoying)
- **A Dig tap in the opening made no cut** (Annoying, seen 3 times)
- **Buttons overlap: #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83%** (Annoying)
- **Frame-time spike during "opening"** (Annoying, seen 8 times)
- **Frame-time spike during "panels"** (Annoying, seen 2 times)

## Problems, worst first

### 1. A button is covered by something else: #multiplayer-button "World / crew" is covered by #touch-key-KeyD

- **How bad:** Annoying (score 68)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:33 into the run, on desktop (Chromium)
- **What happened:** #multiplayer-button "World / crew" is covered by #touch-key-KeyD (Controls open, desktop)
- **What the vision model saw:** Same Controls-panel view as the previous shot, on Mars at Valles Marineris, panel covering the lower-left of the screen over the landing pad and ship ramp. Flagged: Controls panel covers/hides the ship's boarding ramp and lower hull detail directly behind it, and the 'World / crew' button is not visible while it's open
- **Screenshot:** [011-panels-PROBLEM-covered.jpg](shots-desktop/011-panels-PROBLEM-covered.jpg)

  ![A button is covered by something else: #](shots-desktop/011-panels-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-voice-mute (toggle #set-voice-mute)
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)

### 2. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 3 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:40 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 4 after tapping "Dig (E)"
- **What the vision model saw:** Top-down view of a white supply crate half-buried in green dust with a 'Dig (E)' button and instruction to aim the shovel at the dust. Flagged: A dark, undefined rounded blob/shadow sits in the top-left corner, not matching any scene element
- **Later hits:** 06:42 cuts stayed 4 after tapping "Dig (E)" / 06:44 cuts stayed 4 after tapping "Dig (E)"
- **Screenshot:** [035-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/035-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/035-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. mis-tap beside #opening-action
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. REFRESH (mid-dig)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. tap #opening-action (opening action)

### 3. Buttons overlap: #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83%

- **How bad:** Annoying (score 66)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:33 into the run, on desktop (Chromium)
- **What happened:** #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83% (Controls open, desktop)
- **What the vision model saw:** Desktop view on Mars at Valles Marineris with the Controls panel (grid of key-binding buttons) open, covering the lower-left portion of the screen including part of the ship ramp. Flagged: Controls panel covers the area where the 'World / crew' button normally sits, and it disappears from view entirely while the panel is open; Controls panel has no visible close (X) button or dimmed background separating it from the 3D scene, only a 'Close panels' text button within the grid
- **Screenshot:** [010-panels-PROBLEM-overlap.jpg](shots-desktop/010-panels-PROBLEM-overlap.jpg)

  ![Buttons overlap: #touch-key-KeyD "Right"](shots-desktop/010-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-voice-mute (toggle #set-voice-mute)
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)

### 4. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 8 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:19 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4286 ms (typical 16 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Interior of a ship/train car looking out tall windows at an orange dome structure outside, with Walter's dialogue line shown at the bottom and move/look instructions at the top. Flagged: Thin vertical white sliver objects visible through the windows (left and right) that don't match any recognizable scenery piece
- **Later hits:** 05:50 a single frame took 4740 ms (typical 30 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 06:17 a single frame took 1650 ms (typical 18 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 5. Frame-time spike during "panels"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** opening the Settings / Account / World / Controls panels, first at 08:38 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** a single frame took 1793 ms (typical 28 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Close-up of the lifeboat 'SKIFF 7' on grass, with a large semi-transparent info panel (Earth/Skyward Launch Complex, quest text) covering the top half, and World/crew and Controls buttons at bottom left. Flagged: Large info/quest panel covers most of the upper screen and overlaps the top of the skiff, obscuring the view
- **Screenshot:** [054-panels-PROBLEM-frame-spike.jpg](shots-iphone/054-panels-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "panels"](shots-iphone/054-panels-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)

### 6. Frame-time spike during "freeplay"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** free play (random walking, tapping, refreshing), first at 14:47 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 3785 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Phone view from just inside/at the doorway of the Skiff's main deck, with exterior grassy terrain visible on the left and dark wood-paneled interior filling most of the right side. Flagged: Camera appears to be clipped extremely close to the interior wall paneling, which fills most of the right half of the frame with no depth/detail visible; Thin bright cyan/white horizontal line cutting across the screen; Same reddish diagonal line artifact in the top-left corner as seen in other frame-spike shots; Large flat black rectangular area with no visible detail, inconsistent with surrounding lit interior
- **Later hits:** 14:51 a single frame took 4033 ms (typical 30 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [086-freeplay-PROBLEM-frame-spike.jpg](shots-iphone/086-freeplay-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "freeplay"](shots-iphone/086-freeplay-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. outpost route of 83 legs around 30 solid things
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)
  1. QA pass: lifeboat: fit both parts, the boat is no longer drained - HUD: NEXT No more jobs here for now. Dig, haul and sell what the ground gives, or fly to another world (Course). The people here will have more w
  1. === phase freeplay starts
  1. REFRESH (random refresh while playing)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 7. Frame-time spike during "network"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** network cut, refresh offline, slow connection, first at 02:44 into the run, on desktop (Chromium)
- **What happened:** a single frame took 4604 ms (typical 4 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 02:49 a single frame took 2525 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [037-network-PROBLEM-frame-spike.jpg](shots-desktop/037-network-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "network"](shots-desktop/037-network-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. NETWORK BACK
  1. QA pass: network: after the network returns the game reconnects and answers again - 2 s
  1. QA pass: network: money and place unchanged by a network blip
  1. REFRESH (refresh after being offline)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: network: refresh while offline, then online again, the game comes back
  1. SLOW NETWORK on (900 ms delay, 60 KB/s)
  1. tap #btn-settings (tap on a slow network)

### 8. Frame-time spike during "lifeboat"

- **How bad:** Annoying (score 62)
- **Where:** earning the first ship: buy the two lifeboat parts and fit them, first at 11:58 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 5411 ms (typical 37 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Phone view standing on a paved pad at the Skyward Launch Complex on Earth, with a brief/dialogue panel at top, a virtual joystick overlay bottom-left, and World/crew and Controls buttons bottom-left. Flagged: Thin red diagonal line/sliver crossing the very top-left corner of the screen, cutting through the lamp post and sky
- **Screenshot:** [074-lifeboat-PROBLEM-frame-spike.jpg](shots-iphone/074-lifeboat-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "lifeboat"](shots-iphone/074-lifeboat-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. refresh check: moved 0.0 m, marks 10000 -> 10000, aboard false -> false
  1. === phase lifeboat starts
  1. lifeboat on earth is drained, missing cell + coupler; HUD says: NEXT The lifeboat has no power. Buy a power cell from Okafor, the flight line crew chief (Skyward), the Skyward Launch Complex and a fuel coupler from Pruitt, t
  1. QA pass: lifeboat: the NEXT line on screen names who sells each part - NEXT The lifeboat has no power. Buy a power cell from Okafor, the flight line crew chief (Skyward), the Skyward Launch Complex and a fuel coupler from Pruitt, t
  1. go talk to Okafor
  1. walk to Okafor
  1. outpost route of 35 legs around 30 solid things

### 9. Frame-time spike during "smoke"

- **How bad:** Annoying (score 62)
- **Where:** smoke check (load time, download size, warm reload), first at 00:55 into the run, on desktop (Chromium)
- **What happened:** a single frame took 6195 ms (typical 4 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Desktop view on Mars at Valles Marineris with no panels open, showing the ship on its pad and a floating status tooltip reading 'Systems nominal. Ship down and stable.' Flagged: Status tooltip floats in open space over the ship's engine nozzles with no visible anchor point, line, or arrow connecting it to a specific object
- **Screenshot:** [013-smoke-PROBLEM-frame-spike.jpg](shots-desktop/013-smoke-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "smoke"](shots-desktop/013-smoke-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase smoke starts
  1. QA info: smoke: page transfer on a cold load - 250 requests, 1.3 MB over the wire (slowest: eartbeatobservatory.com/games/the-cosmos/lib/three.module.js 165 ms)
  1. QA pass: smoke: time from opening the link to the first drawn frames - 14.1 s (headless software rendering, a real phone is usually quicker to draw but slower to download)
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 10. Frame-time spike during "a11y"

- **How bad:** Annoying (score 62)
- **Where:** accessibility and readability scan, first at 01:04 into the run, on desktop (Chromium)
- **What happened:** a single frame took 3471 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Same Mars landing pad scene, static framing identical to the other a11y shots, with no visible stutter artifact captured in this still.
- **Screenshot:** [021-a11y-PROBLEM-frame-spike.jpg](shots-desktop/021-a11y-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "a11y"](shots-desktop/021-a11y-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 6 small: span.dim 10px "Duricrust · 3.72 m/s²" ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; span.hint 10px 
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.
  1. QA pass: a11y: tap targets at least 44 px (Apple guideline) - 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44
  1. QA FAIL: a11y: pinch-zoom is not locked off - width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
  1. QA pass: a11y: a volume or mute control exists
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"","hint":"","caption":"","hud":"Mars · Valles Marineris 13°59'56.9\"S 59°11'43.9\"W +2213.1 m Duricrust · 3.72 m/s² Hauling cart: 0.0 / 1054 kg tool:

### 11. Looks wrong in the screenshot: Error banner 'Graphics problem: WebGL context lost - safe mode active' overlaps and partially covers the locat

- **How bad:** Annoying (score 56), happened 2 times
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:47 into the run, on desktop (Chromium)
- **What happened:** top of screen, overlapping the 'Mars · Valles Marineris' header (the vision model's description of the screen: Same Mars landing pad scene but with a black error banner reading 'Graphics problem: WebGL context lost - safe mode active' and a status toast 'Systems nominal. Ship down and stable.', rendered with washed-out, flat-shaded (texture-less) models.)
- **Screenshot:** [025-lifecycle-PROBLEM-console-warning.jpg](shots-desktop/025-lifecycle-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: Error ban](shots-desktop/025-lifecycle-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 12. Looks wrong in the screenshot: Bottom half of the screen is a flat, detail-less reddish-brown block instead of rendered ground/terrain, with 

- **How bad:** Annoying (score 56)
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:47 into the run, on desktop (Chromium)
- **What happened:** lower half of screen, roughly x=0-1280, y=556-800 (the vision model's description of the screen: Desktop view on a Mars landing pad next to the ship, with a HUD (hauling cart weight, quest text, World/crew and Controls buttons) and a tooltip reading 'Systems nominal. Ship down and stable.')
- **Screenshot:** [026-lifecycle-PROBLEM-console-warning.jpg](shots-desktop/026-lifecycle-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: Bottom ha](shots-desktop/026-lifecycle-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 13. When the graphics context is lost (iPhones do this after the app was in the background) the game restarts itself in reduced-graphics "safe mode"

- **How bad:** Minor (score 52)
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:50 into the run, on desktop (Chromium)
- **What happened:** by design (src/core/graphicsHealth.js). The page address gets ?tier=safe and it stays that way for the session, with a red graphics banner: "Graphics problem: WebGL context lost - safe mode active". A player who just switched apps and came back is left on worse graphics.
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

### 14. Looks wrong in the screenshot: Full black screen with zero caption, title, or loading text (not just a loading/crash blackout, which should c

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 08:26 into the run, on iPhone (WebKit)
- **What happened:** entire screen (the vision model's description of the screen: Completely black frame with no visible UI, text, or caption of any kind.)
- **Screenshot:** [044-opening-PROBLEM-console-warning.jpg](shots-iphone/044-opening-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: Full blac](shots-iphone/044-opening-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening finished

### 15. Looks wrong in the screenshot: Large flat gray trapezoid shape with no texture or detail, inconsistent with the ground/sky/building around it

- **How bad:** Minor (score 49)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 09:29 into the run, on iPhone (WebKit)
- **What happened:** center-left of screen, mid-ground (the vision model's description of the screen: First-person tour view on grass near a large building, with an info panel at top, movement joystick, and World/crew and Controls buttons at the bottom.)
- **Screenshot:** [058-tour-walking.jpg](shots-iphone/058-tour-walking.jpg)

  ![Looks wrong in the screenshot: Large fla](shots-iphone/058-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. outpost route of 117 legs around 30 solid things

### 16. Looks wrong in the screenshot: Camera appears to be clipped extremely close to the interior wall paneling, which fills most of the right half

- **How bad:** Minor (score 49)
- **Where:** free play (random walking, tapping, refreshing), first at 14:48 into the run, on iPhone (WebKit)
- **What happened:** right two-thirds of screen (the vision model's description of the screen: Phone view from just inside/at the doorway of the Skiff's main deck, with exterior grassy terrain visible on the left and dark wood-paneled interior filling most of the right side.)
- **Screenshot:** [086-freeplay-PROBLEM-frame-spike.jpg](shots-iphone/086-freeplay-PROBLEM-frame-spike.jpg)

  ![Looks wrong in the screenshot: Camera ap](shots-iphone/086-freeplay-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 17. Looks wrong in the screenshot: Ship and rover models render flat/untextured and desaturated compared to the normal frames, consistent with lo

- **How bad:** Minor (score 49)
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:47 into the run, on desktop (Chromium)
- **What happened:** ship and rover on the pad (the vision model's description of the screen: Same Mars landing pad scene but with a black error banner reading 'Graphics problem: WebGL context lost - safe mode active' and a status toast 'Systems nominal. Ship down and stable.', rendered with washed-out, flat-shaded (texture-less) models.)
- **Screenshot:** [025-lifecycle-PROBLEM-console-warning.jpg](shots-desktop/025-lifecycle-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: Ship and ](shots-desktop/025-lifecycle-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 18. Looks wrong in the screenshot: A large translucent reddish rectangle with faint, unreadable ghost text is overlaid across the lower half of t

- **How bad:** Minor (score 49)
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:47 into the run, on desktop (Chromium)
- **What happened:** bottom half of the viewport, below the menu buttons (the vision model's description of the screen: Same Mars landing pad scene but with a black error banner reading 'Graphics problem: WebGL context lost - safe mode active' and a status toast 'Systems nominal. Ship down and stable.', rendered with washed-out, flat-shaded (texture-less) models.)
- **Screenshot:** [025-lifecycle-PROBLEM-console-warning.jpg](shots-desktop/025-lifecycle-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: A large t](shots-desktop/025-lifecycle-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 19. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:43 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 03:42 [opening] walk to down the gangway
- **What the vision model saw:** Dusk/night view of a Mars spaceport road leading to a lit 'ARRIVALS' sign, with a Steward dialogue line at the bottom and a Skip intro button top right.
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

### 20. Game said: "This deletes your current character (its ship, crew, marks and pad) an"

- **How bad:** Minor (score 42)
- **Where:** random tapping everywhere, first at 03:19 into the run, on desktop (Chromium)
- **What happened:** shown in account-section while the bot was: 03:19 [monkey] monkey tap touch-key-Space
- **Screenshot:** [040-monkey-PROBLEM-refusal-message.jpg](shots-desktop/040-monkey-PROBLEM-refusal-message.jpg)

  ![Game said: "This deletes your current ch](shots-desktop/040-monkey-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. monkey tap btn-settings
  1. monkey tap touch-key-Space
  1. monkey tap touch-key-KeyE
  1. monkey tap touch-key-Space
  1. tap on empty 3D view at 465,450
  1. monkey tap touch-key-KeyQ
  1. monkey tap Start fresh: new charact
  1. monkey tap touch-key-Space

### 21. Frame-time spike during "tour"

- **How bad:** Minor (score 38), happened 2 times
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 08:51 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 848 ms (typical 26 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Outdoor view of a grassy launch complex with palm trees, two dome buildings, and a tall antenna tower, with movement joystick and the same info panel plus World/crew and Controls buttons.
- **Later hits:** 11:46 a single frame took 4612 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [056-tour-PROBLEM-frame-spike.jpg](shots-iphone/056-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/056-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. settlement world Earth: people Okafor, Pruitt, Marisol Quintero
  1. go talk to Okafor
  1. walk to Okafor
  1. outpost route of 117 legs around 30 solid things

### 22. Frame-time spike during "lifecycle"

- **How bad:** Minor (score 38), happened 2 times
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:47 into the run, on desktop (Chromium)
- **What happened:** a single frame took 1975 ms (typical 4 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 02:05 a single frame took 5062 ms (typical 4 ms); 6 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [028-lifecycle-PROBLEM-frame-spike.jpg](shots-desktop/028-lifecycle-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "lifecycle"](shots-desktop/028-lifecycle-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. jump
  1. QA pass: spam: 25 jumps and wild looks, game keeps drawing
  1. spam: 0 requests sent, purse 10000 -> 10000
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 23. Low text contrast in 2 places

- **How bad:** Minor (score 38)
- **Where:** accessibility and readability scan, first at 01:03 into the run, on desktop (Chromium)
- **What happened:** span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
- **What the vision model saw:** Same Mars landing pad scene with the top-left HUD panel showing location, stats, and quest text. Flagged: Secondary stat lines ('Duricrust · 3.72 m/s²' and 'tool: Shovel') are rendered in dim gray text, noticeably lower contrast than the white/orange text above and below them on the same dark brown panel
- **Screenshot:** [017-a11y-PROBLEM-a11y-contrast.jpg](shots-desktop/017-a11y-PROBLEM-a11y-contrast.jpg)

  ![Low text contrast in 2 places](shots-desktop/017-a11y-PROBLEM-a11y-contrast.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 21.8 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 6 small: span.dim 10px "Duricrust · 3.72 m/s²" ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; span.hint 10px 
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"

### 24. Text smaller than 11 px in 6 places (hard to read on a phone)

- **How bad:** Minor (score 36)
- **Where:** accessibility and readability scan, first at 01:03 into the run, on desktop (Chromium)
- **What happened:** span.dim 10px "Duricrust · 3.72 m/s²" ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
- **What the vision model saw:** Landing pad on Mars (Valles Marineris) with a rover and ship on the tarmac, a large instructional HUD panel top-left, and two menu buttons (World/crew, Controls) bottom-left. Flagged: The quest/instruction paragraph in the top-left panel is rendered in a small font relative to the panel width, with several lines of dense text
- **Screenshot:** [016-a11y-PROBLEM-a11y-small-text.jpg](shots-desktop/016-a11y-PROBLEM-a11y-small-text.jpg)

  ![Text smaller than 11 px in 6 places (har](shots-desktop/016-a11y-PROBLEM-a11y-small-text.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: smoke: time from opening the link to the first drawn frames - 14.1 s (headless software rendering, a real phone is usually quicker to draw but slower to download)
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 21.8 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 6 small: span.dim 10px "Duricrust · 3.72 m/s²" ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; span.hint 10px 

### 25. 1 buttons have no text or label (a screen reader says nothing)

- **How bad:** Small (score 34)
- **Where:** accessibility and readability scan, first at 01:03 into the run, on desktop (Chromium)
- **What happened:** input.
- **What the vision model saw:** Same Mars landing pad scene; ship, rover, and crew-hall building are visible but none carry a visible name/label tag. Flagged: No object on screen (ship, rover, building) has any name or ID label, so nothing visually distinguishes them by name
- **Screenshot:** [018-a11y-PROBLEM-a11y-noname.jpg](shots-desktop/018-a11y-PROBLEM-a11y-noname.jpg)

  ![1 buttons have no text or label (a scree](shots-desktop/018-a11y-PROBLEM-a11y-noname.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 21.8 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 6 small: span.dim 10px "Duricrust · 3.72 m/s²" ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; span.hint 10px 
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.

### 26. textures grew from 122 to 252 over the run (new areas loading, or a leak)

- **How bad:** Small (score 30), happened 2 times
- **Where:** free play (random walking, tapping, refreshing), first at 15:02 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** samples 46; phases opening -> freeplay. Only a leak if it keeps climbing while standing still: the idle check measures that.

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: lifeboat: fit both parts, the boat is no longer drained - HUD: NEXT No more jobs here for now. Dig, haul and sell what the ground gives, or fly to another world (Course). The people here will have more w
  1. === phase freeplay starts
  1. REFRESH (random refresh while playing)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. jump
  1. tap on empty 3D view at 319,367
  1. tap #btn-key-controls (idle fiddling)

### 27. Zooming the page is switched off in the viewport tag

- **How bad:** Small (score 30)
- **Where:** accessibility and readability scan, first at 01:03 into the run, on desktop (Chromium)
- **What happened:** width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
- **What the vision model saw:** Same Mars landing pad scene, static framing identical to the other a11y shots.
- **Screenshot:** [019-a11y-PROBLEM-a11y-zoom-locked.jpg](shots-desktop/019-a11y-PROBLEM-a11y-zoom-locked.jpg)

  ![Zooming the page is switched off in the ](shots-desktop/019-a11y-PROBLEM-a11y-zoom-locked.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 6 small: span.dim 10px "Duricrust · 3.72 m/s²" ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; span.hint 10px 
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.
  1. QA pass: a11y: tap targets at least 44 px (Apple guideline) - 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44
  1. QA FAIL: a11y: pinch-zoom is not locked off - width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover

### 28. graphics shapes (geometries) grew from 265 to 703 over the run (new areas loading, or a leak)

- **How bad:** Small (score 30)
- **Where:** free play (random walking, tapping, refreshing), first at 05:05 into the run, on desktop (Chromium)
- **What happened:** samples 31; phases lifecycle -> freeplay. Only a leak if it keeps climbing while standing still: the idle check measures that.

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. jump
  1. jump
  1. jump
  1. jump
  1. QA pass: edges: walked and jumped into walls in 8 directions, never fell through - furthest 37 m from where it started
  1. QA pass: edges: still drawing afterwards
  1. === phase freeplay starts

### 29. Network cut for about 12 s and the game said nothing and still thinks it is connected

- **How bad:** Small (score 28)
- **Where:** network cut, refresh offline, slow connection, first at 02:30 into the run, on desktop (Chromium)
- **What happened:** connected=true. A hint only: the bot's offline switch may not cut a socket that is already open, so a real phone going into a tunnel could behave differently.
- **Screenshot:** [036-network-PROBLEM-offline-silent.jpg](shots-desktop/036-network-PROBLEM-offline-silent.jpg)

  ![Network cut for about 12 s and the game ](shots-desktop/036-network-PROBLEM-offline-silent.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: lifecycle: rotate to 900x560 with Settings open, the 3D view fills the screen - {"cw":900,"ch":560,"iw":900,"ih":560}
  1. tap #btn-close-settings (close settings)
  1. === phase network starts
  1. NETWORK CUT
  1. tap #purse (tap while offline)
  1. tap button "Close" (close account-panel)
  1. QA pass: network: while offline the game keeps drawing and does not crash
  1. QA info: network: the game tells the player the connection is gone (within about 12 s) - connected flag true -> true; messages: 

### Console warnings (4 kinds)

- THREE.WebGLRenderer: Texture has been resized from (256x192) to (256x128). (x15)
- THREE.Material: parameter 'map' has value of undefined. (x6)
- THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed. (x3)
- THREE.WebGLRenderer: WebGL 1 support was deprecated in r153 and will be removed in r163. (x1)

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 489 s |
| opening the Settings / Account / World / Controls panels | done | 11 s |
| walking the port (or the settlement of the start world) and talking to people | done - settlement Earth: 3 of 3 talked to | 176 s |
| earning the first ship: buy the two lifeboat parts and fit them | done - lifeboat repaired | 156 s |
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
| turning on the spot, reading draw calls and frame times | skipped (out of time) | 0 s |
| random tapping everywhere | skipped (out of time) | 0 s |
| leaving the game alone for 90 s | skipped (out of time) | 0 s |
| end-of-run soft-lock check | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | done | 29 s |

People talked to: 3 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

### Desktop (Chromium, keyboard + mouse)

| Step | Result | Time |
|---|---|---|
| opening the Settings / Account / World / Controls panels | done | 20 s |
| smoke check (load time, download size, warm reload) | done | 22 s |
| accessibility and readability scan | done | 7 s |
| spamming buttons and jumps | done | 25 s |
| app to the background, graphics context lost, phone rotated | done | 45 s |
| network cut, refresh offline, slow connection | done | 35 s |
| turning on the spot, reading draw calls and frame times | done | 9 s |
| random tapping everywhere | done | 33 s |
| walking and jumping into walls and edges in 8 directions | done | 83 s |
| walking the port (or the settlement of the start world) and talking to people | skipped (out of time) | 0 s |
| earning the first ship: buy the two lifeboat parts and fit them | skipped (out of time) | 0 s |
| buy/sell loops and double taps on the shop | skipped (out of time) | 0 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| leaving the game alone for 90 s | skipped (out of time) | 0 s |
| end-of-run soft-lock check | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | done | 9 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / opening: typical 16 ms, slowest 7728 ms, 3 frames over 250 ms
- iphone / opening: typical 22 ms, slowest 7175 ms, 3 frames over 250 ms
- desktop / panels: typical 4 ms, slowest 6995 ms, 6 frames over 250 ms
- desktop / smoke: typical 4 ms, slowest 6195 ms, 3 frames over 250 ms
- iphone / lifeboat: typical 37 ms, slowest 5411 ms, 4 frames over 250 ms

Button response time (tap to something changing on screen): median 139 ms, slowest 804 ms over 13 taps.

## QA checks (the things real testers do besides playing through)

See `tools/playtester/PRACTICES.md` for why each one exists. FAIL rows are also listed as problems above where they are real bugs.

### iPhone 15 (WebKit, touch): 4 passed, 0 failed, 0 skipped, 0 info

| Check | Result | Notes |
|---|---|---|
| lifeboat: the NEXT line on screen names who sells each part | pass | NEXT The lifeboat has no power. Buy a power cell from Okafor, the flight line crew chief (Skyward), the Skyward Launch Complex and a fuel coupler from Pruitt, the Homeguard organiser, the Skyward Laun |
| lifeboat: buy the cell from Okafor | pass | purse 10000 -> 9700 |
| lifeboat: buy the coupler from Pruitt | pass | purse 9700 -> 9400 |
| lifeboat: fit both parts, the boat is no longer drained | pass | HUD: NEXT No more jobs here for now. Dig, haul and sell what the ground gives, or fly to another world (Course). The people here will have more w |

### Desktop (Chromium, keyboard + mouse): 19 passed, 4 failed, 1 skipped, 3 info

| Check | Result | Notes |
|---|---|---|
| smoke: page transfer on a cold load | info | 250 requests, 1.3 MB over the wire (slowest: eartbeatobservatory.com/games/the-cosmos/lib/three.module.js 165 ms) |
| smoke: time from opening the link to the first drawn frames | pass | 14.1 s (headless software rendering, a real phone is usually quicker to draw but slower to download) |
| smoke: warm reload comes back | pass | 21.8 s |
| a11y: text is at least 11 px | FAIL | 6 small: span.dim 10px "Duricrust · 3.72 m/s²" ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detai |
| a11y: text contrast (4.5:1, or 3:1 for big text) | FAIL | 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel" |
| a11y: every button has a name | FAIL | input. |
| a11y: tap targets at least 44 px (Apple guideline) | pass | 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44 |
| a11y: pinch-zoom is not locked off | FAIL | width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover |
| a11y: a volume or mute control exists | pass |  |
| readability: something on screen tells a player what to do next | pass | {"action":"","hint":"","caption":"","hud":"Mars · Valles Marineris 13°59'56.9\"S 59°11'43.9\"W +2213.1 m Duricrust · 3.72 m/s² Hauling cart: 0.0 / 1054 kg tool: Shov","jobs":"","toast":"Systems nominal. Ship down and sta |
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
| perf: turning on the spot, 95 percent of frames under 34 ms | pass | median 25 ms, 95th 33 ms, slowest 525 ms; peak 130 draw calls, 37k triangles (headless software rendering, judge relatively) |
| monkey: 30 random button taps and wild gestures, no crash | pass |  |
| edges: walked and jumped into walls in 8 directions, never fell through | pass | furthest 37 m from where it started |
| edges: still drawing afterwards | pass |  |

## Load, size and memory

- **iPhone 15 (WebKit, touch)**: load to first frames 18.3 s; cold-load download 1.3 MB in 250 requests; warm reload not measured; busiest view not measured. Over the run (48 samples): graphics geometries 333 -> 160, textures 122 -> 252, page elements 235 -> 221 (JS heap is only readable in Chromium).
- **Desktop (Chromium, keyboard + mouse)**: load to first frames 14.1 s; cold-load download 1.3 MB in 250 requests; warm reload 21.8 s; busiest view 130 draw calls, 37k triangles. Over the run (35 samples): graphics geometries 334 -> 703, textures 208 -> 237, page elements 219 -> 353, JS heap 248 -> 239 MB.

## Vision pass

A vision model (claude CLI (sonnet)) looked at 36 screenshots for about $0.00 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
- Not possible from here (needs a real iPhone or two players): a real phone call or notification banner, lock screen, battery and heat, low-end phone speed, many device models, race-condition duplication between two players. The full list of what real QA does and which parts the bot covers is in tools/playtester/PRACTICES.md.
