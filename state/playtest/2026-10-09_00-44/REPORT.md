# The Cosmos playtest report

Run: 2026-10-09 00:44 (local)  |  Build under test: `3744d951f2a39a32653e`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

**How to read this:** items titled "Stuck while walking to ..." come from the bot's own steering (its path planner, run-ups and jumps). Treat them as bot-only unless a human also gets stuck at that spot. Black boot and crash-blackout frames that carry a caption are deliberate.

- **iPhone 15 (WebKit, touch)**: 30 minutes, 164 screenshots, 21 distinct problems
- **Desktop (Chromium, keyboard + mouse)**: 5.1 minutes, 45 screenshots, 14 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)
- Desktop (Chromium, keyboard + mouse): [session video](videos-desktop/<email>)

## Short version

35 distinct problems found: 0 blockers, 2 serious, 33 smaller.

- **Nothing changed for 60+ seconds (same message, same place)** (Serious, seen 4 times)
- **After the graphics context was lost and restored, the game never drew again** (Serious, seen 2 times)
- **A button is covered by something else: #multiplayer-button "World / crew" is covered by #touch-key-KeyD** (Annoying)
- **A Dig tap in the opening made no cut** (Annoying, seen 3 times)
- **Buttons overlap: #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83%** (Annoying)

## Problems, worst first

### 1. Nothing changed for 60+ seconds (same message, same place)

- **How bad:** Serious (score 86), happened 4 times
- **Where:** free play (random walking, tapping, refreshing), first at 17:53 into the run, on iPhone (WebKit)
- **What happened:** in "freeplay": position {"x":-0.9,"y":0,"z":-3.4}, button "Sit  ·  Pilot", caption "", toast "", ship aboard
- **What the vision model saw:** A 'World / crew' popup panel is open over the flight deck HUD, showing name field, buy-ship buttons, and faction join buttons. Flagged: Panel has no visible close/back affordance besides the small X top-right; bot tapped #multiplayer-button repeatedly and got stuck here per the filename/log, suggesting the panel doesn't dismiss or re-opens
- **Later hits:** 25:21 in "freeplay": position {"x":1.7,"y":0,"z":-3.9}, button "Sit  ·  Captain", caption "", toast "", ship aboard / 27:23 in "freeplay": position {"x":-2,"y":0,"z":-1}, button "", caption "", toast "", ship aboard
- **Screenshot:** [124-freeplay-PROBLEM-stuck-state.jpg](shots-iphone/124-freeplay-PROBLEM-stuck-state.jpg)

  ![Nothing changed for 60+ seconds (same me](shots-iphone/124-freeplay-PROBLEM-stuck-state.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: idle: the player does not drift or slide while standing still - 0.0 m
  1. QA pass: idle: frame time stays steady - median 38 ms -> 27 ms
  1. QA pass: idle: memory does not grow while nothing happens - heap ? -> ? MB, geometries 611 -> 611, textures 301 -> 301
  1. === phase softlock starts
  1. QA skipped: softlock: the player can still move at the end - aboard or mid-flight (stand-up and exit are covered by the fly phase)
  1. === phase freeplay starts
  1. tap on empty 3D view at 75,312
  1. tap #multiplayer-button (idle fiddling)

### 2. After the graphics context was lost and restored, the game never drew again

- **How bad:** Serious (score 80), happened 2 times
- **Where:** app to the background, graphics context lost, phone rotated, first at 14:59 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** (see screenshot)
- **What the vision model saw:** Indoor airlock/storage room scene shown right after a forced refresh meant to test recovery from a lost graphics context. Flagged: Scene appears fully rendered with no visible corruption, missing textures, or black regions, which is inconsistent with the 'context not restored' label — if something failed to restore it is not visible in this frame
- **Screenshot:** [095-lifecycle-PROBLEM-context-not-restored.jpg](shots-iphone/095-lifecycle-PROBLEM-context-not-restored.jpg)

  ![After the graphics context was lost and ](shots-iphone/095-lifecycle-PROBLEM-context-not-restored.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: a11y: tap targets at least 44 px (Apple guideline) - 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44
  1. QA FAIL: a11y: pinch-zoom is not locked off - width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
  1. QA pass: a11y: a volume or mute control exists
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"Raise ramp","hint":"","caption":"","hud":"Earth · Skyward Launch Complex 28.612° N 80.599° W Grass and soil · 9.82 m/s² Hauling cart: 0.0 / 399 kg to
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. QA FAIL: lifecycle: graphics context lost and restored, game draws again - events: ["lost"]

### 3. A button is covered by something else: #multiplayer-button "World / crew" is covered by #touch-key-KeyD

- **How bad:** Annoying (score 68)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:34 into the run, on desktop (Chromium)
- **What happened:** #multiplayer-button "World / crew" is covered by #touch-key-KeyD (Controls open, desktop)
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

### 4. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 3 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:34 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 4 after tapping "Dig (E)"
- **What the vision model saw:** Top-down view of a buried crate in dirt with a dig prompt and a 'Dig (E)' button in the bottom right corner.
- **Later hits:** 06:36 cuts stayed 4 after tapping "Dig (E)" / 06:40 cuts stayed 4 after tapping "Dig (E)"
- **Screenshot:** [035-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/035-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/035-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. no dig button shown while standing at the crate
  1. tap #opening-action (opening action)
  1. REFRESH (mid-dig)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. tap #opening-action (opening action)

### 5. Buttons overlap: #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83%

- **How bad:** Annoying (score 66)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:34 into the run, on desktop (Chromium)
- **What happened:** #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83% (Controls open, desktop)
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

### 6. Frame-time spike during "freeplay"

- **How bad:** Annoying (score 62), happened 14 times
- **Where:** free play (random walking, tapping, refreshing), first at 18:07 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** a single frame took 3663 ms (typical 15 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 18:12 a single frame took 5122 ms (typical 30 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 20:01 a single frame took 1396 ms (typical 28 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [126-freeplay-PROBLEM-frame-spike.jpg](shots-iphone/126-freeplay-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "freeplay"](shots-iphone/126-freeplay-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA skipped: softlock: the player can still move at the end - aboard or mid-flight (stand-up and exit are covered by the fly phase)
  1. === phase freeplay starts
  1. tap on empty 3D view at 75,312
  1. tap #multiplayer-button (idle fiddling)
  1. tap button "✕"
  1. REFRESH (random refresh while playing)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 7. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 8 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:15 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 3559 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Interior ship corridor/lounge scene with a dialogue line from a character named Walter about coffee, an orange dome visible through windows, and a bench/table in the foreground.
- **Later hits:** 05:45 a single frame took 4903 ms (typical 26 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 06:10 a single frame took 1515 ms (typical 16 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 8. Frame-time spike during "lifecycle"

- **How bad:** Annoying (score 62), happened 4 times
- **Where:** app to the background, graphics context lost, phone rotated, first at 15:11 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** a single frame took 3964 ms (typical 15 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Inside a hangar/cabin near a closed bulkhead door, with a location/status HUD panel and World/crew, Controls, and Raise ramp buttons.
- **Later hits:** 15:21 a single frame took 725 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [096-lifecycle-PROBLEM-frame-spike.jpg](shots-iphone/096-lifecycle-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "lifecycle"](shots-iphone/096-lifecycle-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"Raise ramp","hint":"","caption":"","hud":"Earth · Skyward Launch Complex 28.612° N 80.599° W Grass and soil · 9.82 m/s² Hauling cart: 0.0 / 399 kg to
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. QA FAIL: lifecycle: graphics context lost and restored, game draws again - events: ["lost"]
  1. REFRESH (recovering after a lost graphics context)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 9. Frame-time spike during "network"

- **How bad:** Annoying (score 62), happened 4 times
- **Where:** network cut, refresh offline, slow connection, first at 15:48 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** a single frame took 3429 ms (typical 15 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Inside the ship's main deck near a doorway looking out onto a grassy field, with two long diagonal cylindrical shapes (one blue, one red) crossing the screen. Flagged: Two long diagonal pipe/cylinder shapes cut across the view at an odd angle, not attached to any visible structure, as if camera is clipping through geometry
- **Later hits:** 15:53 a single frame took 4252 ms (typical 29 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [103-network-PROBLEM-frame-spike.jpg](shots-iphone/103-network-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "network"](shots-iphone/103-network-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: network: while offline the game keeps drawing and does not crash
  1. QA info: network: the game tells the player the connection is gone (within about 12 s) - connected flag true -> true; messages: 
  1. NETWORK BACK
  1. QA pass: network: after the network returns the game reconnects and answers again - 2 s
  1. QA pass: network: money and place unchanged by a network blip
  1. REFRESH (refresh after being offline)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 10. Frame-time spike during "smoke"

- **How bad:** Annoying (score 62), happened 3 times
- **Where:** smoke check (load time, download size, warm reload), first at 14:31 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** a single frame took 3468 ms (typical 15 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Outdoor launch-pad scene at a scaffold/gantry structure with a ladder, seen through a cockpit-style window, with a translucent HUD text panel top-left and World/crew and Controls buttons bottom-left. Flagged: A wide horizontal band of regular light/dark stripes runs across the bottom ~15% of the screen, looking like torn or corrupted texture/screen-tearing rather than ground or floor detail; Several small floating colored dots (pink, white, green) hang in mid-air over the launch pad with no visible object they belong to
- **Later hits:** 14:36 a single frame took 4221 ms (typical 31 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [085-smoke-PROBLEM-frame-spike.jpg](shots-iphone/085-smoke-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "smoke"](shots-iphone/085-smoke-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-action (action)
  1. QA pass: lifeboat: fit both parts, the boat is no longer drained - HUD: NEXT Work: Range dispatcher Marisol Quintero has a job: "A hand for the countdown". Walk up, tap Talk, then "Is there paid work for me?".
  1. === phase smoke starts
  1. QA info: smoke: page transfer on a cold load - 250 requests, 1.3 MB over the wire (slowest: tbeatobservatory.com/games/the-cosmos/src/worlds/registry.js 253 ms)
  1. QA pass: smoke: time from opening the link to the first drawn frames - 14.1 s (headless software rendering, a real phone is usually quicker to draw but slower to download)
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 11. Frame-time spike during "lifeboat"

- **How bad:** Annoying (score 62)
- **Where:** earning the first ship: buy the two lifeboat parts and fit them, first at 11:55 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4056 ms (typical 28 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Outdoor scene near a road/parking area with palm trees and a building, the same quest/info text panel in the top left, and joystick circles plus World/crew and Controls buttons in the bottom left.
- **Screenshot:** [073-lifeboat-PROBLEM-frame-spike.jpg](shots-iphone/073-lifeboat-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "lifeboat"](shots-iphone/073-lifeboat-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. refresh check: moved 0.0 m, marks 10000 -> 10000, aboard false -> false
  1. === phase lifeboat starts
  1. lifeboat on earth is drained, missing cell + coupler; HUD says: NEXT The lifeboat has no power. Buy a power cell from Okafor, the flight line crew chief (Skyward), the Skyward Launch Complex and a fuel coupler from Pruitt, t
  1. QA pass: lifeboat: the NEXT line on screen names who sells each part - NEXT The lifeboat has no power. Buy a power cell from Okafor, the flight line crew chief (Skyward), the Skyward Launch Complex and a fuel coupler from Pruitt, t
  1. go talk to Okafor
  1. walk to Okafor
  1. outpost route of 35 legs around 30 solid things

### 12. Frame-time spike during "dig"

- **How bad:** Annoying (score 62)
- **Where:** digging regolith and delivering it to the weigh bay, first at 16:03 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 3372 ms (typical 15 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Same main-deck doorway view as the previous shot, again with two diagonal blue and red cylinder shapes crossing the screen. Flagged: Same floating/clipping diagonal pipe shapes visible, unattached to surrounding structure
- **Screenshot:** [111-dig-PROBLEM-frame-spike.jpg](shots-iphone/111-dig-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "dig"](shots-iphone/111-dig-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA skipped: economy: buy then sell loop - no shop reachable on this world
  1. === phase edges starts
  1. QA skipped: edges: walking into walls and edges - aboard or mid-flight
  1. === phase hire starts
  1. === phase dig starts
  1. REFRESH (refresh right after digging)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 13. Frame-time spike during "fly"

- **How bad:** Annoying (score 62)
- **Where:** boarding the ship, taking a seat and flying a course, first at 16:17 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4370 ms (typical 28 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Same pilot seat view with Nav Computer/Course sheet open, engine-power refusal message, and the overlapping tooltip near the top stats bar. Flagged: Tooltip box "Use the seat request." overlaps and partially obscures the SPD/ALT stats bar text
- **Screenshot:** [115-fly-PROBLEM-frame-spike.jpg](shots-iphone/115-fly-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "fly"](shots-iphone/115-fly-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. refresh check: moved 0.0 m, marks 9400 -> 9400, aboard true -> true
  1. === phase fly starts
  1. ship type lifeboat; ship centre at port 3695185,-1935283; ramp foot 3695189,-1935271
  1. button near seat: "Sit  ·  Pilot"
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)
  1. seated: pilot
  1. tap #chip-course (open the Course sheet)

### 14. Frame-time spike during "panels"

- **How bad:** Annoying (score 62)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:20 into the run, on desktop (Chromium)
- **What happened:** a single frame took 7270 ms (typical 4 ms); 7 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-panels-PROBLEM-frame-spike.jpg](shots-desktop/003-panels-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "panels"](shots-desktop/003-panels-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. desktop budget is 5 min and the opening alone takes about 10: started from the review start (use --desktop-opening to play it)
  1. === phase panels starts
  1. tap #btn-settings (open Settings)

### 15. Looks wrong in the screenshot: Full black screen with zero text/caption despite log saying 'opening finished' — no Skip intro button, no load

- **How bad:** Annoying (score 56)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 08:24 into the run, on iPhone (WebKit)
- **What happened:** entire frame (the vision model's description of the screen: Entirely black frame with no caption, title, or loading text anywhere on screen.)
- **Screenshot:** [045-opening-opening-done.jpg](shots-iphone/045-opening-opening-done.jpg)

  ![Looks wrong in the screenshot: Full blac](shots-iphone/045-opening-opening-done.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening finished

### 16. Looks wrong in the screenshot: Entire 3D scene is black/empty even though the HUD says the player is landed on Earth with a valid location

- **How bad:** Annoying (score 56)
- **Where:** network cut, refresh offline, slow connection, first at 15:36 into the run, on iPhone (WebKit)
- **What happened:** full viewport below the HUD panel (the vision model's description of the screen: The HUD status panel and two buttons (World/crew, Controls) are shown, but the 3D world itself is a solid black viewport with no geometry rendered.)
- **Screenshot:** [102-network-PROBLEM-offline-silent.jpg](shots-iphone/102-network-PROBLEM-offline-silent.jpg)

  ![Looks wrong in the screenshot: Entire 3D](shots-iphone/102-network-PROBLEM-offline-silent.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. NETWORK BACK

### 17. Looks wrong in the screenshot: Full black frame with zero text, caption, or loading indicator (unlike the designed blackout frames which alwa

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 08:23 into the run, on iPhone (WebKit)
- **What happened:** entire screen (the vision model's description of the screen: Entirely black screen with no visible text, caption, or UI of any kind.)
- **Screenshot:** [044-opening-PROBLEM-console-warning.jpg](shots-iphone/044-opening-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: Full blac](shots-iphone/044-opening-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening finished

### 18. Looks wrong in the screenshot: A wide horizontal band of regular light/dark stripes runs across the bottom ~15% of the screen, looking like t

- **How bad:** Minor (score 49)
- **Where:** smoke check (load time, download size, warm reload), first at 14:33 into the run, on iPhone (WebKit)
- **What happened:** bottom of screen, full width, below the launch pad (the vision model's description of the screen: Outdoor launch-pad scene at a scaffold/gantry structure with a ladder, seen through a cockpit-style window, with a translucent HUD text panel top-left and World/crew and Controls buttons bottom-left.)
- **Screenshot:** [085-smoke-PROBLEM-frame-spike.jpg](shots-iphone/085-smoke-PROBLEM-frame-spike.jpg)

  ![Looks wrong in the screenshot: A wide ho](shots-iphone/085-smoke-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 19. Looks wrong in the screenshot: 'Earth frame.' tooltip text is small and sits directly over a bright ceiling light, making it hard to read

- **How bad:** Minor (score 49)
- **Where:** accessibility and readability scan, first at 14:37 into the run, on iPhone (WebKit)
- **What happened:** center of screen, over the ceiling light (the vision model's description of the screen: Indoor airlock/storage room with barrels, a striped door, a wall-mounted screen, HUD text panel top-left, and an 'Earth frame.' tooltip floating center screen.)
- **Screenshot:** [088-a11y-PROBLEM-a11y-small-text.jpg](shots-iphone/088-a11y-PROBLEM-a11y-small-text.jpg)

  ![Looks wrong in the screenshot: 'Earth fr](shots-iphone/088-a11y-PROBLEM-a11y-small-text.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"Raise ramp","hint":"","caption":"","hud":"Earth · Skyward Launch Complex 28.612° N 80.599° W Grass and soil · 9.82 m/s² Hauling cart: 0.0 / 399 kg to

### 20. Looks wrong in the screenshot: 'Raise ramp' button text blends into its tan/brown button background, very low contrast

- **How bad:** Minor (score 49)
- **Where:** accessibility and readability scan, first at 14:37 into the run, on iPhone (WebKit)
- **What happened:** bottom-right corner (the vision model's description of the screen: Same indoor airlock/storage room scene as the previous shot, with the 'Earth frame.' tooltip and HUD panel visible.)
- **Screenshot:** [089-a11y-PROBLEM-a11y-contrast.jpg](shots-iphone/089-a11y-PROBLEM-a11y-contrast.jpg)

  ![Looks wrong in the screenshot: 'Raise ra](shots-iphone/089-a11y-PROBLEM-a11y-contrast.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"Raise ramp","hint":"","caption":"","hud":"Earth · Skyward Launch Complex 28.612° N 80.599° W Grass and soil · 9.82 m/s² Hauling cart: 0.0 / 399 kg to

### 21. Looks wrong in the screenshot: White 'Earth frame.' tooltip text overlaps a bright white ceiling light fixture, washing out the text

- **How bad:** Minor (score 49)
- **Where:** accessibility and readability scan, first at 14:37 into the run, on iPhone (WebKit)
- **What happened:** center screen, over the ceiling light (the vision model's description of the screen: Same indoor airlock/storage room scene as the previous shot, with the 'Earth frame.' tooltip and HUD panel visible.)
- **Screenshot:** [089-a11y-PROBLEM-a11y-contrast.jpg](shots-iphone/089-a11y-PROBLEM-a11y-contrast.jpg)

  ![Looks wrong in the screenshot: White 'Ea](shots-iphone/089-a11y-PROBLEM-a11y-contrast.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"Raise ramp","hint":"","caption":"","hud":"Earth · Skyward Launch Complex 28.612° N 80.599° W Grass and soil · 9.82 m/s² Hauling cart: 0.0 / 399 kg to

### 22. Looks wrong in the screenshot: Two long diagonal pipe/cylinder shapes cut across the view at an odd angle, not attached to any visible struct

- **How bad:** Minor (score 49)
- **Where:** network cut, refresh offline, slow connection, first at 15:50 into the run, on iPhone (WebKit)
- **What happened:** upper-left to center of screen, crossing the doorway (the vision model's description of the screen: Inside the ship's main deck near a doorway looking out onto a grassy field, with two long diagonal cylindrical shapes (one blue, one red) crossing the screen.)
- **Screenshot:** [103-network-PROBLEM-frame-spike.jpg](shots-iphone/103-network-PROBLEM-frame-spike.jpg)

  ![Looks wrong in the screenshot: Two long ](shots-iphone/103-network-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 23. Looks wrong in the screenshot: Same floating/clipping diagonal pipe shapes visible, unattached to surrounding structure

- **How bad:** Minor (score 49)
- **Where:** digging regolith and delivering it to the weigh bay, first at 16:04 into the run, on iPhone (WebKit)
- **What happened:** upper-left to center of screen, crossing the doorway (the vision model's description of the screen: Same main-deck doorway view as the previous shot, again with two diagonal blue and red cylinder shapes crossing the screen.)
- **Screenshot:** [111-dig-PROBLEM-frame-spike.jpg](shots-iphone/111-dig-PROBLEM-frame-spike.jpg)

  ![Looks wrong in the screenshot: Same floa](shots-iphone/111-dig-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 24. Looks wrong in the screenshot: Panel has no visible close/back affordance besides the small X top-right; bot tapped #multiplayer-button repea

- **How bad:** Minor (score 49)
- **Where:** free play (random walking, tapping, refreshing), first at 17:53 into the run, on iPhone (WebKit)
- **What happened:** whole modal, especially around the X at top-right (the vision model's description of the screen: A 'World / crew' popup panel is open over the flight deck HUD, showing name field, buy-ship buttons, and faction join buttons.)
- **Screenshot:** [124-freeplay-PROBLEM-stuck-state.jpg](shots-iphone/124-freeplay-PROBLEM-stuck-state.jpg)

  ![Looks wrong in the screenshot: Panel has](shots-iphone/124-freeplay-PROBLEM-stuck-state.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-button (idle fiddling)

### 25. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:36 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 03:34 [opening] walk to down the gangway
- **What the vision model saw:** Dusk Mars port exterior with a road leading to a lit 'ARRIVALS' sign, a Skip intro button top right, and a steward's welcome dialogue at the bottom.
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

### 26. Game said: "Can't lift: the engines are too weak for this load. Route more power t"

- **How bad:** Minor (score 42)
- **Where:** boarding the ship, taking a seat and flying a course, first at 16:17 into the run, on iPhone (WebKit)
- **What happened:** shown in fl-warn while the bot was: 16:17 [fly] tap #chip-course (open the Course sheet)
- **What the vision model saw:** Pilot seat view with the Nav Computer sheet open showing Course options (Marineris Port, Mars orbit), an engine-power refusal message, and a tooltip near the top stats bar. Flagged: Tooltip box "Use the seat request." overlaps and partially obscures the SPD/ALT stats bar text
- **Screenshot:** [114-fly-PROBLEM-refusal-message.jpg](shots-iphone/114-fly-PROBLEM-refusal-message.jpg)

  ![Game said: "Can't lift: the engines are ](shots-iphone/114-fly-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. refresh check: moved 0.0 m, marks 9400 -> 9400, aboard true -> true
  1. === phase fly starts
  1. ship type lifeboat; ship centre at port 3695185,-1935283; ramp foot 3695189,-1935271
  1. button near seat: "Sit  ·  Pilot"
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)
  1. seated: pilot
  1. tap #chip-course (open the Course sheet)

### 27. Frame-time spike during "tour"

- **How bad:** Minor (score 38), happened 2 times
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 08:42 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 713 ms (typical 28 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Outdoor grassy field on Earth near a launch complex with palm trees and two dome structures in the distance, a large quest/info text panel in the top left, and movement joystick circles plus World/crew and Controls buttons in the bottom left.
- **Later hits:** 11:42 a single frame took 3803 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [055-tour-PROBLEM-frame-spike.jpg](shots-iphone/055-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/055-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. settlement world Earth: people Okafor, Pruitt, Marisol Quintero
  1. go talk to Okafor
  1. walk to Okafor
  1. outpost route of 117 legs around 30 solid things

### 28. Low text contrast in 1 places

- **How bad:** Minor (score 38), happened 2 times
- **Where:** accessibility and readability scan, first at 14:37 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** span.hint 3.9:1 (needs 4.5) "Third person to inspect "
- **What the vision model saw:** Same indoor airlock/storage room scene as the previous shot, with the 'Earth frame.' tooltip and HUD panel visible. Flagged: 'Raise ramp' button text blends into its tan/brown button background, very low contrast; White 'Earth frame.' tooltip text overlaps a bright white ceiling light fixture, washing out the text
- **Screenshot:** [089-a11y-PROBLEM-a11y-contrast.jpg](shots-iphone/089-a11y-PROBLEM-a11y-contrast.jpg)

  ![Low text contrast in 1 places](shots-iphone/089-a11y-PROBLEM-a11y-contrast.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 14.7 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 4 small: #hud-readout 10px "· Skyward Launch Complex" ; b. 10px "Earth" ; span.load 10px "Hauling cart: 0.0 / 399 " ; span.hint 10px "Third person to inspect "
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 1 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect "

### 29. Frame-time spike during "a11y"

- **How bad:** Minor (score 38)
- **Where:** accessibility and readability scan, first at 00:52 into the run, on desktop (Chromium)
- **What happened:** a single frame took 2542 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
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
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"","hint":"","caption":"","hud":"Mars · Valles Marineris 13°59'56.9\"S 59°11'47.9\"W +2213.1 m Martian regolith · 3.72 m/s² Hauling cart: 0.0 / 1054 k

### 30. Text smaller than 11 px in 4 places (hard to read on a phone)

- **How bad:** Minor (score 36), happened 2 times
- **Where:** accessibility and readability scan, first at 14:37 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** #hud-readout 10px "· Skyward Launch Complex" ; b. 10px "Earth" ; span.load 10px "Hauling cart: 0.0 / 399 " ; span.hint 10px "Third person to inspect "
- **What the vision model saw:** Indoor airlock/storage room with barrels, a striped door, a wall-mounted screen, HUD text panel top-left, and an 'Earth frame.' tooltip floating center screen. Flagged: 'Earth frame.' tooltip text is small and sits directly over a bright ceiling light, making it hard to read; 'Raise ramp' button label text is very faint/low-contrast against its button background
- **Screenshot:** [088-a11y-PROBLEM-a11y-small-text.jpg](shots-iphone/088-a11y-PROBLEM-a11y-small-text.jpg)

  ![Text smaller than 11 px in 4 places (har](shots-iphone/088-a11y-PROBLEM-a11y-small-text.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 14.7 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 4 small: #hud-readout 10px "· Skyward Launch Complex" ; b. 10px "Earth" ; span.load 10px "Hauling cart: 0.0 / 399 " ; span.hint 10px "Third person to inspect "

### 31. 1 buttons have no text or label (a screen reader says nothing)

- **How bad:** Small (score 34), happened 2 times
- **Where:** accessibility and readability scan, first at 14:37 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** input.
- **What the vision model saw:** Same indoor airlock/storage room scene, with the 'Earth frame.' tooltip, HUD panel, and bottom buttons visible. Flagged: 'Earth frame.' tooltip gives no clear indication of what it is (label, button, or status text) beyond two words; Door control panel screen (small blue-lit square) has no visible label identifying its function
- **Screenshot:** [090-a11y-PROBLEM-a11y-noname.jpg](shots-iphone/090-a11y-PROBLEM-a11y-noname.jpg)

  ![1 buttons have no text or label (a scree](shots-iphone/090-a11y-PROBLEM-a11y-noname.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 14.7 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 4 small: #hud-readout 10px "· Skyward Launch Complex" ; b. 10px "Earth" ; span.load 10px "Hauling cart: 0.0 / 399 " ; span.hint 10px "Third person to inspect "
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 1 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect "
  1. QA FAIL: a11y: every button has a name - input.

### 32. Zooming the page is switched off in the viewport tag

- **How bad:** Small (score 30), happened 2 times
- **Where:** accessibility and readability scan, first at 14:37 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
- **What the vision model saw:** Same indoor airlock/storage room scene again, identical layout with HUD panel, tooltip, and bottom buttons.
- **Screenshot:** [091-a11y-PROBLEM-a11y-zoom-locked.jpg](shots-iphone/091-a11y-PROBLEM-a11y-zoom-locked.jpg)

  ![Zooming the page is switched off in the ](shots-iphone/091-a11y-PROBLEM-a11y-zoom-locked.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 4 small: #hud-readout 10px "· Skyward Launch Complex" ; b. 10px "Earth" ; span.load 10px "Hauling cart: 0.0 / 399 " ; span.hint 10px "Third person to inspect "
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 1 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect "
  1. QA FAIL: a11y: every button has a name - input.
  1. QA pass: a11y: tap targets at least 44 px (Apple guideline) - 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44
  1. QA FAIL: a11y: pinch-zoom is not locked off - width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover

### 33. textures grew from 64 to 230 over the run (new areas loading, or a leak)

- **How bad:** Small (score 30)
- **Where:** free play (random walking, tapping, refreshing), first at 30:02 into the run, on iPhone (WebKit)
- **What happened:** samples 110; phases opening -> freeplay. Only a leak if it keeps climbing while standing still: the idle check measures that.

- **Steps to reproduce (what the bot did just before):**
  1. tap button "Close"
  1. jump
  1. jump
  1. jump
  1. jump
  1. REFRESH (random refresh while playing)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 34. Network cut for about 12 s and the game said nothing and still thinks it is connected

- **How bad:** Small (score 28), happened 2 times
- **Where:** network cut, refresh offline, slow connection, first at 15:35 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** connected=true. A hint only: the bot's offline switch may not cut a socket that is already open, so a real phone going into a tunnel could behave differently.
- **What the vision model saw:** The HUD status panel and two buttons (World/crew, Controls) are shown, but the 3D world itself is a solid black viewport with no geometry rendered. Flagged: Entire 3D scene is black/empty even though the HUD says the player is landed on Earth with a valid location
- **Screenshot:** [102-network-PROBLEM-offline-silent.jpg](shots-iphone/102-network-PROBLEM-offline-silent.jpg)

  ![Network cut for about 12 s and the game ](shots-iphone/102-network-PROBLEM-offline-silent.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: lifecycle: rotate to 852x393 with Settings open, the 3D view fills the screen - {"cw":852,"ch":393,"iw":852,"ih":393}
  1. tap #btn-close-settings (close settings)
  1. === phase network starts
  1. NETWORK CUT
  1. tap #purse (tap while offline)
  1. tap button "Close" (close account-panel)
  1. QA pass: network: while offline the game keeps drawing and does not crash
  1. QA info: network: the game tells the player the connection is gone (within about 12 s) - connected flag true -> true; messages: 

### Console warnings (1 kinds)

- THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed. (x12)

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 491 s |
| opening the Settings / Account / World / Controls panels | done | 10 s |
| walking the port (or the settlement of the start world) and talking to people | done - settlement Earth: 3 of 3 talked to | 175 s |
| earning the first ship: buy the two lifeboat parts and fit them | done - lifeboat repaired | 153 s |
| smoke check (load time, download size, warm reload) | done | 15 s |
| accessibility and readability scan | done | 2 s |
| app to the background, graphics context lost, phone rotated | done | 43 s |
| network cut, refresh offline, slow connection | done | 32 s |
| spamming buttons and jumps | done | 0 s |
| buy/sell loops and double taps on the shop | done | 0 s |
| walking and jumping into walls and edges in 8 directions | done | 0 s |
| hiring crew from the crew hall | done - skipped: the crew hall is at Marineris Port on Mars | 0 s |
| digging regolith and delivering it to the weigh bay | done - skipped: the regolith job and weigh bay are at Marineris Port on Mars | 0 s |
| boarding the ship, taking a seat and flying a course | done - boarded, sat, read the course sheet (no trip flown on a settlement world) | 10 s |
| turning on the spot, reading draw calls and frame times | done | 0 s |
| random tapping everywhere | done | 0 s |
| leaving the game alone for 90 s | done | 91 s |
| end-of-run soft-lock check | done | 0 s |
| free play (random walking, tapping, refreshing) | done | 731 s |

People talked to: 3 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

### Desktop (Chromium, keyboard + mouse)

| Step | Result | Time |
|---|---|---|
| opening the Settings / Account / World / Controls panels | done | 20 s |
| smoke check (load time, download size, warm reload) | done | 10 s |
| accessibility and readability scan | done | 6 s |
| spamming buttons and jumps | done | 25 s |
| app to the background, graphics context lost, phone rotated | done | 42 s |
| network cut, refresh offline, slow connection | done | 34 s |
| turning on the spot, reading draw calls and frame times | done | 9 s |
| random tapping everywhere | done | 33 s |
| walking and jumping into walls and edges in 8 directions | done | 96 s |
| walking the port (or the settlement of the start world) and talking to people | skipped (out of time) | 0 s |
| earning the first ship: buy the two lifeboat parts and fit them | skipped (out of time) | 0 s |
| buy/sell loops and double taps on the shop | skipped (out of time) | 0 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| leaving the game alone for 90 s | skipped (out of time) | 0 s |
| end-of-run soft-lock check | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | done | 15 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- desktop / panels: typical 4 ms, slowest 7270 ms, 7 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 6941 ms, 3 frames over 250 ms
- iphone / freeplay: typical 30 ms, slowest 5122 ms, 3 frames over 250 ms
- iphone / freeplay: typical 16 ms, slowest 5100 ms, 6 frames over 250 ms
- iphone / opening: typical 15 ms, slowest 4990 ms, 2 frames over 250 ms

Button response time (tap to something changing on screen): median 374 ms, slowest 1071 ms over 14 taps.

## QA checks (the things real testers do besides playing through)

See `tools/playtester/PRACTICES.md` for why each one exists. FAIL rows are also listed as problems above where they are real bugs.

### iPhone 15 (WebKit, touch): 21 passed, 5 failed, 7 skipped, 2 info

| Check | Result | Notes |
|---|---|---|
| lifeboat: the NEXT line on screen names who sells each part | pass | NEXT The lifeboat has no power. Buy a power cell from Okafor, the flight line crew chief (Skyward), the Skyward Launch Complex and a fuel coupler from Pruitt, the Homeguard organiser, the Skyward Laun |
| lifeboat: buy the cell from Okafor | pass | purse 10000 -> 9700 |
| lifeboat: buy the coupler from Pruitt | pass | purse 9700 -> 9400 |
| lifeboat: fit both parts, the boat is no longer drained | pass | HUD: NEXT Work: Range dispatcher Marisol Quintero has a job: "A hand for the countdown". Walk up, tap Talk, then "Is there paid work for me?". |
| smoke: page transfer on a cold load | info | 250 requests, 1.3 MB over the wire (slowest: tbeatobservatory.com/games/the-cosmos/src/worlds/registry.js 253 ms) |
| smoke: time from opening the link to the first drawn frames | pass | 14.1 s (headless software rendering, a real phone is usually quicker to draw but slower to download) |
| smoke: warm reload comes back | pass | 14.7 s |
| a11y: text is at least 11 px | FAIL | 4 small: #hud-readout 10px "· Skyward Launch Complex" ; b. 10px "Earth" ; span.load 10px "Hauling cart: 0.0 / 399 " ; span.hint 10px "Third person to inspect " |
| a11y: text contrast (4.5:1, or 3:1 for big text) | FAIL | 1 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " |
| a11y: every button has a name | FAIL | input. |
| a11y: tap targets at least 44 px (Apple guideline) | pass | 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44 |
| a11y: pinch-zoom is not locked off | FAIL | width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover |
| a11y: a volume or mute control exists | pass |  |
| readability: something on screen tells a player what to do next | pass | {"action":"Raise ramp","hint":"","caption":"","hud":"Earth · Skyward Launch Complex 28.612° N 80.599° W Grass and soil · 9.82 m/s² Hauling cart: 0.0 / 399 kg tool: Shovel NE","jobs":"","toast":"Earth frame."} |
| lifecycle: background 8 s and return keeps place, money and ship state | pass |  |
| lifecycle: graphics context lost and restored, game draws again | FAIL | events: ["lost"] |
| lifecycle: rotate to 852x393, the 3D view fills the screen | pass | {"cw":852,"ch":393,"iw":852,"ih":393} |
| lifecycle: rotate to 852x393 with Settings open, the 3D view fills the screen | pass | {"cw":852,"ch":393,"iw":852,"ih":393} |
| network: while offline the game keeps drawing and does not crash | pass |  |
| network: the game tells the player the connection is gone (within about 12 s) | info | connected flag true -> true; messages:  |
| network: after the network returns the game reconnects and answers again | pass | 2 s |
| network: money and place unchanged by a network blip | pass |  |
| network: refresh while offline, then online again, the game comes back | pass |  |
| network: slow connection | skipped | throttling only exists in Chromium; the phone profile does the offline test |
| spam: panel buttons hammered | skipped | aboard or mid-flight |
| economy: buy then sell loop | skipped | no shop reachable on this world |
| edges: walking into walls and edges | skipped | aboard or mid-flight |
| fly: the Course sheet lists somewhere to go | pass | × / Course / Jobs / Marineris Port · long-range driveengines too low t / Mars orbit (400 km) · long-range driveengines too  / Phobos · long-range driveengines too low to liftLa / Deimos · long-range driveengines too low  |
| perf: draw calls and triangles | skipped | aboard or mid-flight |
| monkey: random taps | skipped | aboard or mid-flight |
| idle: 90 s with no input, still drawing, still connected | pass |  |
| idle: the player does not drift or slide while standing still | pass | 0.0 m |
| idle: frame time stays steady | pass | median 38 ms -> 27 ms |
| idle: memory does not grow while nothing happens | pass | heap ? -> ? MB, geometries 611 -> 611, textures 301 -> 301 |
| softlock: the player can still move at the end | skipped | aboard or mid-flight (stand-up and exit are covered by the fly phase) |

### Desktop (Chromium, keyboard + mouse): 19 passed, 5 failed, 1 skipped, 2 info

| Check | Result | Notes |
|---|---|---|
| smoke: page transfer on a cold load | info | 250 requests, 1.3 MB over the wire (slowest: rtbeatobservatory.com/games/the-cosmos/src/ship/clearance.js 178 ms) |
| smoke: time from opening the link to the first drawn frames | pass | 14.9 s (headless software rendering, a real phone is usually quicker to draw but slower to download) |
| smoke: warm reload comes back | pass | 9.9 s |
| a11y: text is at least 11 px | FAIL | 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel" |
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
| lifecycle: graphics context lost and restored, game draws again | FAIL | events: ["lost"] |
| lifecycle: rotate to 900x560, the 3D view fills the screen | pass | {"cw":900,"ch":560,"iw":900,"ih":560} |
| lifecycle: rotate to 900x560 with Settings open, the 3D view fills the screen | pass | {"cw":900,"ch":560,"iw":900,"ih":560} |
| network: while offline the game keeps drawing and does not crash | pass |  |
| network: the game tells the player the connection is gone (within about 12 s) | info | connected flag true -> true; messages:  |
| network: after the network returns the game reconnects and answers again | pass | 2 s |
| network: money and place unchanged by a network blip | pass |  |
| network: refresh while offline, then online again, the game comes back | pass |  |
| network: slow connection (900 ms, 60 KB/s) for a panel tap | pass | 5 s |
| perf: turning on the spot, 95 percent of frames under 34 ms | pass | median 25 ms, 95th 33 ms, slowest 571 ms; peak 130 draw calls, 37k triangles (headless software rendering, judge relatively) |
| monkey: 26 random button taps and wild gestures, no crash | pass |  |
| edges: walked and jumped into walls in 8 directions, never fell through | pass | furthest 56 m from where it started |
| edges: still drawing afterwards | pass |  |

## Load, size and memory

- **iPhone 15 (WebKit, touch)**: load to first frames 14.1 s; cold-load download 1.3 MB in 250 requests; warm reload 14.7 s; busiest view not measured. Over the run (113 samples): graphics geometries 336 -> 130, textures 122 -> 230, page elements 236 -> 221 (JS heap is only readable in Chromium).
- **Desktop (Chromium, keyboard + mouse)**: load to first frames 14.9 s; cold-load download 1.3 MB in 250 requests; warm reload 9.9 s; busiest view 130 draw calls, 37k triangles. Over the run (36 samples): graphics geometries 363 -> 259, textures 206 -> 183, page elements 277 -> 219, JS heap 262 -> 225 MB.

## Vision pass

A vision model (claude CLI (sonnet)) looked at 36 screenshots for about $0.00 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
- Not possible from here (needs a real iPhone or two players): a real phone call or notification banner, lock screen, battery and heat, low-end phone speed, many device models, race-condition duplication between two players. The full list of what real QA does and which parts the bot covers is in tools/playtester/PRACTICES.md.
