# The Cosmos playtest report

Run: 2026-10-08 23:05 (local)  |  Build under test: `714b42a01a8aa6cad4f1`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

**How to read this:** items titled "Stuck while walking to ..." come from the bot's own steering (its path planner, run-ups and jumps). Treat them as bot-only unless a human also gets stuck at that spot. Black boot and crash-blackout frames that carry a caption are deliberate.

- **iPhone 15 (WebKit, touch)**: 15.1 minutes, 104 screenshots, 20 distinct problems
- **Desktop (Chromium, keyboard + mouse)**: 5.6 minutes, 42 screenshots, 5 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)
- Desktop (Chromium, keyboard + mouse): [session video](videos-desktop/<email>)

## Short version

32 distinct problems found: 0 blockers, 0 serious, 32 smaller.

- **Could not walk to Arrival guide** (Annoying)
- **Buttons are covered by something on top of them (2 places)** (Annoying, seen 2 times)
- **A Dig tap in the opening made no cut** (Annoying, seen 3 times)
- **Buttons overlap each other (2 places)** (Annoying, seen 2 times)
- **Looks wrong in the screenshot: Red/dark banner reads 'Graphics problem: WebGL context lost - safe mode active' overlapping the status text** (Annoying)

## Problems, worst first

### 1. Could not walk to Arrival guide

- **How bad:** Annoying (score 72)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 02:39 into the run, on desktop (Chromium)
- **What happened:** gave up after 120s; last distance 7 m
- **Screenshot:** [018-tour-PROBLEM-cannot-reach.jpg](shots-desktop/018-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Arrival guide](shots-desktop/018-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #3
  1. jump
  1. not getting closer (9 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (9 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 9 legs

### 2. Buttons are covered by something on top of them (2 places)

- **How bad:** Annoying (score 68), happened 2 times
- **Where:** app to the background, graphics context lost, phone rotated, first at 14:39 into the run, on iPhone (WebKit)
- **What happened:** #btn-settings "Settings" is covered by #boot ;  #multiplayer-button "World / crew" is covered by #touch-key-KeyD
- **What the vision model saw:** Near-black transition frame with the 'THE COSMOS' title barely visible at the bottom edge. Flagged: A hard vertical seam splits the screen into two slightly different shades of black, like two separate black layers not aligned, rather than one uniform blackout; The 'THE COSMOS' title text is cropped at the very bottom of the frame, with no tagline or loading line visible
- **Screenshot:** [096-lifecycle-PROBLEM-covered.jpg](shots-iphone/096-lifecycle-PROBLEM-covered.jpg)

  ![Buttons are covered by something on top ](shots-iphone/096-lifecycle-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: a11y: a volume or mute control exists
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"Raise ramp","hint":"","caption":"","hud":"Earth · Skyward Launch Complex 28.612° N 80.599° W Grass and soil · 9.82 m/s² Hauling cart: 0.0 / 399 kg to
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. websocket closed
  1. QA skipped: lifecycle: graphics context lost and restored - this browser does not allow forcing it
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 3. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 3 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:32 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 4 after tapping "Dig (E)"
- **What the vision model saw:** Close-up of a half-buried crate in a dug-out patch of dirt/grass with a Dig (E) button prompt and 'Aim the shovel at the dust around the crate' instruction.
- **Later hits:** 06:34 cuts stayed 4 after tapping "Dig (E)" / 06:37 cuts stayed 4 after tapping "Dig (E)"
- **Screenshot:** [036-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/036-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/036-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. mis-tap beside #opening-action
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. REFRESH (mid-dig)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. tap #opening-action (opening action)

### 4. Buttons overlap each other (2 places)

- **How bad:** Annoying (score 66), happened 2 times
- **Where:** opening the Settings / Account / World / Controls panels, first at 08:28 into the run, on iPhone (WebKit)
- **What happened:**  "✕" overlaps  "Hear the faction leader of h" by 46% ;  #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83%
- **What the vision model saw:** The World / crew panel is open over the Earth/Skyward Launch Complex scene, showing a name field, fleet/shipyard purchase options, and faction join buttons.
- **Screenshot:** [054-panels-PROBLEM-overlap.jpg](shots-iphone/054-panels-PROBLEM-overlap.jpg)

  ![Buttons overlap each other (2 places)](shots-iphone/054-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-view (settings switch #set-view)
  1. tap #set-tool (settings switch #set-tool)
  1. tap #set-voice-mute (toggle #set-voice-mute)
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)

### 5. Looks wrong in the screenshot: Red/dark banner reads 'Graphics problem: WebGL context lost - safe mode active' overlapping the status text

- **How bad:** Annoying (score 63)
- **Where:** app to the background, graphics context lost, phone rotated, first at 14:49 into the run, on iPhone (WebKit)
- **What happened:** top of screen, over the HUD readout (the vision model's description of the screen: Split-screen glitch: top half shows a 3D outdoor scene with HUD/dialogue text, bottom half of the screen is solid black with two floating menu buttons.)
- **Screenshot:** [101-lifecycle-PROBLEM-frame-spike.jpg](shots-iphone/101-lifecycle-PROBLEM-frame-spike.jpg)

  ![Looks wrong in the screenshot: Red/dark ](shots-iphone/101-lifecycle-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: lifecycle: rotate to 852x393 with Settings open, the 3D view fills the screen - {"cw":852,"ch":393,"iw":852,"ih":393}

### 6. Looks wrong in the screenshot: Entire bottom half of the screen is flat black with no scene content, just two buttons ('World / crew', 'Contr

- **How bad:** Annoying (score 63)
- **Where:** app to the background, graphics context lost, phone rotated, first at 14:49 into the run, on iPhone (WebKit)
- **What happened:** bottom half of screen (the vision model's description of the screen: Split-screen glitch: top half shows a 3D outdoor scene with HUD/dialogue text, bottom half of the screen is solid black with two floating menu buttons.)
- **Screenshot:** [101-lifecycle-PROBLEM-frame-spike.jpg](shots-iphone/101-lifecycle-PROBLEM-frame-spike.jpg)

  ![Looks wrong in the screenshot: Entire bo](shots-iphone/101-lifecycle-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: lifecycle: rotate to 852x393 with Settings open, the 3D view fills the screen - {"cw":852,"ch":393,"iw":852,"ih":393}

### 7. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 9 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:15 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4034 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** First-person view inside a ship looking out through a window at an orange dome structure, with Walter's dialogue line showing at the bottom and move/look instructions at top.
- **Later hits:** 05:44 a single frame took 5205 ms (typical 27 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 06:10 a single frame took 1627 ms (typical 17 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 8. Frame-time spike during "panels"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** opening the Settings / Account / World / Controls panels, first at 08:30 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** a single frame took 1488 ms (typical 28 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** View of the player's ship 'Skiff 7' on grass with a large 'NEXT' instructions box about buying a power cell/fuel coupler, and World/crew and Controls buttons in the bottom left.
- **Screenshot:** [056-panels-PROBLEM-frame-spike.jpg](shots-iphone/056-panels-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "panels"](shots-iphone/056-panels-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)

### 9. Frame-time spike during "smoke"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** smoke check (load time, download size, warm reload), first at 14:18 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4736 ms (typical 15 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** A gray wireframe/skeletal boat-like frame structure hovering disconnected above a grassy field, with the quest panel describing the lifeboat being ready. Flagged: Boat/lifeboat frame appears as an incomplete, untextured gray scaffold floating in mid-air, not resting on the ground, with small colored dots (pink, green, blue) floating separately beneath it; No crew, hull panels, or solid geometry visible on the structure — looks like an unfinished or broken model render
- **Later hits:** 14:23 a single frame took 4226 ms (typical 30 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [085-smoke-PROBLEM-frame-spike.jpg](shots-iphone/085-smoke-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "smoke"](shots-iphone/085-smoke-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-action (action)
  1. QA pass: lifeboat: fit both parts, the boat is no longer drained - HUD: NEXT Lifeboat ready. Crew are hired at the Crew Hall at Marineris Port on Mars: fly home (Course), land, and walk to the hall at the north e
  1. === phase smoke starts
  1. QA info: smoke: page transfer on a cold load - 250 requests, 1.3 MB over the wire (slowest: beatobservatory.com/games/the-cosmos/src/port/workerLines.js 131 ms)
  1. QA pass: smoke: time from opening the link to the first drawn frames - 14.2 s (headless software rendering, a real phone is usually quicker to draw but slower to download)
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 10. Frame-time spike during "lifecycle"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** app to the background, graphics context lost, phone rotated, first at 14:45 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 3137 ms (typical 15 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Split-screen glitch: top half shows a 3D outdoor scene with HUD/dialogue text, bottom half of the screen is solid black with two floating menu buttons. Flagged: Red/dark banner reads 'Graphics problem: WebGL context lost - safe mode active' overlapping the status text; A tooltip box 'Earth frame.' overlaps and obscures the NEXT objective text behind it; Entire bottom half of the screen is flat black with no scene content, just two buttons ('World / crew', 'Controls') floating on it
- **Later hits:** 14:51 a single frame took 4714 ms (typical 16 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [101-lifecycle-PROBLEM-frame-spike.jpg](shots-iphone/101-lifecycle-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "lifecycle"](shots-iphone/101-lifecycle-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. websocket closed
  1. QA skipped: lifecycle: graphics context lost and restored - this browser does not allow forcing it
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: lifecycle: rotate to 852x393, the 3D view fills the screen - {"cw":852,"ch":393,"iw":852,"ih":393}
  1. tap #btn-settings (open Settings, then rotate)

### 11. Frame-time spike during "lifeboat"

- **How bad:** Annoying (score 62)
- **Where:** earning the first ship: buy the two lifeboat parts and fit them, first at 11:32 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 5355 ms (typical 29 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Outdoor tour view near a hangar/runway building with a striped tarmac, the same info panel, and the same World/crew and Controls buttons. Flagged: Same unlabeled translucent circle overlay as image 1, floating over the ground with no icon or purpose shown
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
  1. outpost route of 34 legs around 30 solid things

### 12. Looks wrong in the screenshot: Full black screen with zero text/caption/UI of any kind

- **How bad:** Annoying (score 56)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 08:19 into the run, on iPhone (WebKit)
- **What happened:** entire screen (the vision model's description of the screen: Completely black frame with no caption, title, or loading text of any kind visible anywhere on screen.)
- **Screenshot:** [045-opening-PROBLEM-console-warning.jpg](shots-iphone/045-opening-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: Full blac](shots-iphone/045-opening-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening finished

### 13. Looks wrong in the screenshot: Boat/lifeboat frame appears as an incomplete, untextured gray scaffold floating in mid-air, not resting on the

- **How bad:** Annoying (score 56)
- **Where:** smoke check (load time, download size, warm reload), first at 14:19 into the run, on iPhone (WebKit)
- **What happened:** center of the screen, above the horizon (the vision model's description of the screen: A gray wireframe/skeletal boat-like frame structure hovering disconnected above a grassy field, with the quest panel describing the lifeboat being ready.)
- **Screenshot:** [085-smoke-PROBLEM-frame-spike.jpg](shots-iphone/085-smoke-PROBLEM-frame-spike.jpg)

  ![Looks wrong in the screenshot: Boat/life](shots-iphone/085-smoke-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 14. Looks wrong in the screenshot: Right roughly half of the screen is solid black with no 3D content rendered, while the left half shows the sce

- **How bad:** Annoying (score 56)
- **Where:** app to the background, graphics context lost, phone rotated, first at 14:49 into the run, on iPhone (WebKit)
- **What happened:** right half of the screen (the vision model's description of the screen: Zoomed-in landscape view with the same HUD/warning banner panel on the left and the 3D scene (structure, palm trees, crosswalk) visible only on the left portion of the screen.)
- **Screenshot:** [100-lifecycle-PROBLEM-console-error.jpg](shots-iphone/100-lifecycle-PROBLEM-console-error.jpg)

  ![Looks wrong in the screenshot: Right rou](shots-iphone/100-lifecycle-PROBLEM-console-error.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: lifecycle: rotate to 852x393 with Settings open, the 3D view fills the screen - {"cw":852,"ch":393,"iw":852,"ih":393}

### 15. Console error

- **How bad:** Annoying (score 55)
- **Where:** app to the background, graphics context lost, phone rotated, first at 14:45 into the run, on iPhone (WebKit)
- **What happened:** THREE.WebGLState: TypeError: undefined is not an object (evaluating 'gl.texImage3D.apply')
- **What the vision model saw:** Zoomed-in landscape view with the same HUD/warning banner panel on the left and the 3D scene (structure, palm trees, crosswalk) visible only on the left portion of the screen. Flagged: Right roughly half of the screen is solid black with no 3D content rendered, while the left half shows the scene normally, a hard vertical split; 'Graphics problem: WebGL context lost - safe mode active' banner still displayed even though part of the scene is rendering; A floating 'Earth frame.' tooltip label is cut off at the bottom edge of the screenshot
- **Screenshot:** [100-lifecycle-PROBLEM-console-error.jpg](shots-iphone/100-lifecycle-PROBLEM-console-error.jpg)

  ![Console error](shots-iphone/100-lifecycle-PROBLEM-console-error.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. websocket closed
  1. QA skipped: lifecycle: graphics context lost and restored - this browser does not allow forcing it
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: lifecycle: rotate to 852x393, the 3D view fills the screen - {"cw":852,"ch":393,"iw":852,"ih":393}
  1. tap #btn-settings (open Settings, then rotate)

### 16. Server connection (websocket) closed

- **How bad:** Minor (score 50)
- **Where:** app to the background, graphics context lost, phone rotated, first at 14:37 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **What the vision model saw:** The deliberate boot screen: near-black background with 'THE COSMOS' title, tagline, and a 'Loading the port…' line.
- **Screenshot:** [094-lifecycle-PROBLEM-ws-closed.jpg](shots-iphone/094-lifecycle-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/094-lifecycle-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: a11y: tap targets at least 44 px (Apple guideline) - 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44
  1. QA FAIL: a11y: pinch-zoom is not locked off - width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
  1. QA pass: a11y: a volume or mute control exists
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"Raise ramp","hint":"","caption":"","hud":"Earth · Skyward Launch Complex 28.612° N 80.599° W Grass and soil · 9.82 m/s² Hauling cart: 0.0 / 399 kg to
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. websocket closed

### 17. Looks wrong in the screenshot: 'Graphics problem: WebGL context lost - safe mode active' banner is still shown even though the 3D scene is cl

- **How bad:** Minor (score 49), happened 2 times
- **Where:** app to the background, graphics context lost, phone rotated, first at 14:48 into the run, on iPhone (WebKit)
- **What happened:** top of HUD panel (the vision model's description of the screen: Landscape view after rotating, showing the HUD panel with the WebGL-context-lost banner still displayed while the 3D scene (gantry structure, palm trees, sky, runway) has in fact loaded behind it.)
- **Screenshot:** [099-lifecycle-PROBLEM-console-warning.jpg](shots-iphone/099-lifecycle-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: 'Graphics](shots-iphone/099-lifecycle-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-settings (open Settings, then rotate)

### 18. Looks wrong in the screenshot: No crew, hull panels, or solid geometry visible on the structure — looks like an unfinished or broken model re

- **How bad:** Minor (score 49)
- **Where:** smoke check (load time, download size, warm reload), first at 14:19 into the run, on iPhone (WebKit)
- **What happened:** center of the screen (the vision model's description of the screen: A gray wireframe/skeletal boat-like frame structure hovering disconnected above a grassy field, with the quest panel describing the lifeboat being ready.)
- **Screenshot:** [085-smoke-PROBLEM-frame-spike.jpg](shots-iphone/085-smoke-PROBLEM-frame-spike.jpg)

  ![Looks wrong in the screenshot: No crew, ](shots-iphone/085-smoke-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 19. Looks wrong in the screenshot: Tooltip text "Earth frame." is very small relative to the screen and low in the frame, easy to miss

- **How bad:** Minor (score 49)
- **Where:** accessibility and readability scan, first at 14:25 into the run, on iPhone (WebKit)
- **What happened:** small dark pill/label centered above the doorway (the vision model's description of the screen: Interior metal corridor/room with a bright overhead light, a closed airlock-style door with a small dark screen, and a small floating tooltip reading "Earth frame." above the doorway.)
- **Screenshot:** [088-a11y-PROBLEM-a11y-small-text.jpg](shots-iphone/088-a11y-PROBLEM-a11y-small-text.jpg)

  ![Looks wrong in the screenshot: Tooltip t](shots-iphone/088-a11y-PROBLEM-a11y-small-text.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"Raise ramp","hint":"","caption":"","hud":"Earth · Skyward Launch Complex 28.612° N 80.599° W Grass and soil · 9.82 m/s² Hauling cart: 0.0 / 399 kg to

### 20. Looks wrong in the screenshot: "Raise ramp" button text and the "Earth frame." tooltip are dark/dim text on a dark semi-transparent backgroun

- **How bad:** Minor (score 49)
- **Where:** accessibility and readability scan, first at 14:25 into the run, on iPhone (WebKit)
- **What happened:** bottom-right button and the tooltip above the door (the vision model's description of the screen: Same interior corridor scene as image 4 (metal walls, lit door, "Earth frame." tooltip, Raise ramp button bottom-right).)
- **Screenshot:** [089-a11y-PROBLEM-a11y-contrast.jpg](shots-iphone/089-a11y-PROBLEM-a11y-contrast.jpg)

  ![Looks wrong in the screenshot: "Raise ra](shots-iphone/089-a11y-PROBLEM-a11y-contrast.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"Raise ramp","hint":"","caption":"","hud":"Earth · Skyward Launch Complex 28.612° N 80.599° W Grass and soil · 9.82 m/s² Hauling cart: 0.0 / 399 kg to

### 21. Looks wrong in the screenshot: Entire 3D viewport is solid black with no scene rendered

- **How bad:** Minor (score 49)
- **Where:** app to the background, graphics context lost, phone rotated, first at 14:45 into the run, on iPhone (WebKit)
- **What happened:** whole screen below/around the HUD (the vision model's description of the screen: Portrait HUD on a solid black viewport, with a 'Graphics problem: WebGL context lost - safe mode active' banner shown above the cart/tool/NEXT info and the World/crew and Controls buttons.)
- **Screenshot:** [097-lifecycle-PROBLEM-console-warning.jpg](shots-iphone/097-lifecycle-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: Entire 3D](shots-iphone/097-lifecycle-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-settings (open Settings, then rotate)

### 22. Looks wrong in the screenshot: A tooltip box 'Earth frame.' overlaps and obscures the NEXT objective text behind it

- **How bad:** Minor (score 49)
- **Where:** app to the background, graphics context lost, phone rotated, first at 14:49 into the run, on iPhone (WebKit)
- **What happened:** middle of top half, over the quest text block (the vision model's description of the screen: Split-screen glitch: top half shows a 3D outdoor scene with HUD/dialogue text, bottom half of the screen is solid black with two floating menu buttons.)
- **Screenshot:** [101-lifecycle-PROBLEM-frame-spike.jpg](shots-iphone/101-lifecycle-PROBLEM-frame-spike.jpg)

  ![Looks wrong in the screenshot: A tooltip](shots-iphone/101-lifecycle-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: lifecycle: rotate to 852x393 with Settings open, the 3D view fills the screen - {"cw":852,"ch":393,"iw":852,"ih":393}

### 23. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:36 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 03:36 [opening] opening stage 0 -> 1 (StewardWelcome to Mars. Follow the amber lights to the big Arrivals sign. If you reach a fuel tank, you have taken touri)
- **What the vision model saw:** Dusk view of a Mars spaceport walkway leading to an Arrivals building, with a Skip intro button top right and the Steward's welcome dialogue at the bottom.
- **Screenshot:** [017-opening-PROBLEM-refusal-message.jpg](shots-iphone/017-opening-PROBLEM-refusal-message.jpg)

  ![Game said: "Welcome to Mars. Follow the ](shots-iphone/017-opening-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. in the boarding hall, waiting for the gangway to come down
  1. walk to down the gangway
  1. walk to down the gangway
  1. walk to down the gangway
  1. opening stage 0 -> 1 (StewardWelcome to Mars. Follow the amber lights to the big Arrivals sign. If you reach a fuel tank, you have taken touri)

### 24. Frame-time spike during "tour"

- **How bad:** Minor (score 38), happened 5 times
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 08:31 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** a single frame took 739 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Outdoor tour view on Earth showing a grass field with palm trees, radio antenna towers, and two large dome structures, with an info panel (location/cargo/quest text) and World/crew and Controls buttons. Flagged: Two overlapping translucent tan/beige circles floating over the grass with no icon or label
- **Later hits:** 11:20 a single frame took 4081 ms (typical 15 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [058-tour-PROBLEM-frame-spike.jpg](shots-iphone/058-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/058-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. settlement world Earth: people Okafor, Pruitt
  1. go talk to Okafor
  1. walk to Okafor
  1. outpost route of 117 legs around 30 solid things

### 25. Low text contrast in 1 places

- **How bad:** Minor (score 38)
- **Where:** accessibility and readability scan, first at 14:25 into the run, on iPhone (WebKit)
- **What happened:** span.hint 3.9:1 (needs 4.5) "Third person to inspect "
- **What the vision model saw:** Same interior corridor scene as image 4 (metal walls, lit door, "Earth frame." tooltip, Raise ramp button bottom-right). Flagged: "Raise ramp" button text and the "Earth frame." tooltip are dark/dim text on a dark semi-transparent background, low contrast against the already-dim interior; Small screen/monitor on the door is pure black with no visible icon, label, or readable content
- **Screenshot:** [089-a11y-PROBLEM-a11y-contrast.jpg](shots-iphone/089-a11y-PROBLEM-a11y-contrast.jpg)

  ![Low text contrast in 1 places](shots-iphone/089-a11y-PROBLEM-a11y-contrast.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 16.2 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 8 small: #hud-readout 10px "· Skyward Launch Complex" ; b. 10px "Earth" ; span.dim 10px "Grass and soil · 9.82 m/" ; span.load 10px "Hauling cart: 0.0 / 399 " ;
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 1 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect "

### 26. Text smaller than 11 px in 8 places (hard to read on a phone)

- **How bad:** Minor (score 36)
- **Where:** accessibility and readability scan, first at 14:25 into the run, on iPhone (WebKit)
- **What happened:** #hud-readout 10px "· Skyward Launch Complex" ; b. 10px "Earth" ; span.dim 10px "Grass and soil · 9.82 m/" ; span.load 10px "Hauling cart: 0.0 / 399 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Crew are"
- **What the vision model saw:** Interior metal corridor/room with a bright overhead light, a closed airlock-style door with a small dark screen, and a small floating tooltip reading "Earth frame." above the doorway. Flagged: Tooltip text "Earth frame." is very small relative to the screen and low in the frame, easy to miss; Overhead light fixture is a blown-out solid white rectangle with no texture/detail
- **Screenshot:** [088-a11y-PROBLEM-a11y-small-text.jpg](shots-iphone/088-a11y-PROBLEM-a11y-small-text.jpg)

  ![Text smaller than 11 px in 8 places (har](shots-iphone/088-a11y-PROBLEM-a11y-small-text.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 16.2 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 8 small: #hud-readout 10px "· Skyward Launch Complex" ; b. 10px "Earth" ; span.dim 10px "Grass and soil · 9.82 m/" ; span.load 10px "Hauling cart: 0.0 / 399 " ;

### 27. 1 buttons have no text or label (a screen reader says nothing)

- **How bad:** Small (score 34)
- **Where:** accessibility and readability scan, first at 14:25 into the run, on iPhone (WebKit)
- **What happened:** input.
- **What the vision model saw:** Same interior corridor scene again (identical to images 4 and 5), metal walls, lit door, "Earth frame." tooltip, Raise ramp button. Flagged: The small black screen/panel embedded in the door has no visible name, label, or icon indicating what it is or does; Bottom-left Controls and World/crew buttons and bottom-right Raise ramp button have no icons, only text, in a scene already low on contrast
- **Screenshot:** [090-a11y-PROBLEM-a11y-noname.jpg](shots-iphone/090-a11y-PROBLEM-a11y-noname.jpg)

  ![1 buttons have no text or label (a scree](shots-iphone/090-a11y-PROBLEM-a11y-noname.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 16.2 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 8 small: #hud-readout 10px "· Skyward Launch Complex" ; b. 10px "Earth" ; span.dim 10px "Grass and soil · 9.82 m/" ; span.load 10px "Hauling cart: 0.0 / 399 " ;
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 1 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect "
  1. QA FAIL: a11y: every button has a name - input.

### 28. Zooming the page is switched off in the viewport tag

- **How bad:** Small (score 30)
- **Where:** accessibility and readability scan, first at 14:25 into the run, on iPhone (WebKit)
- **What happened:** width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
- **What the vision model saw:** Interior of the launch complex near a large door, with the location/stats HUD panel at top and a floating tooltip label plus World/crew, Controls, and Raise ramp buttons at the bottom. Flagged: A tooltip reading 'Earth frame.' floats in the middle of the scene with no visible crosshair, pointer, or highlighted object it's labeling
- **Screenshot:** [091-a11y-PROBLEM-a11y-zoom-locked.jpg](shots-iphone/091-a11y-PROBLEM-a11y-zoom-locked.jpg)

  ![Zooming the page is switched off in the ](shots-iphone/091-a11y-PROBLEM-a11y-zoom-locked.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 8 small: #hud-readout 10px "· Skyward Launch Complex" ; b. 10px "Earth" ; span.dim 10px "Grass and soil · 9.82 m/" ; span.load 10px "Hauling cart: 0.0 / 399 " ;
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 1 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect "
  1. QA FAIL: a11y: every button has a name - input.
  1. QA pass: a11y: tap targets at least 44 px (Apple guideline) - 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44
  1. QA FAIL: a11y: pinch-zoom is not locked off - width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover

### Console warnings (4 kinds)

- THREE.Material: parameter 'map' has value of undefined. (x11)
- THREE.WebGLRenderer: Texture has been resized from (125x83) to (64x64). (x6)
- THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed. (x4)
- THREE.WebGLRenderer: WebGL 1 support was deprecated in r153 and will be removed in r163. (x1)

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 485 s |
| opening the Settings / Account / World / Controls panels | done | 10 s |
| walking the port (or the settlement of the start world) and talking to people | done - settlement Earth: 2 of 2 talked to | 159 s |
| earning the first ship: buy the two lifeboat parts and fit them | done - lifeboat repaired | 159 s |
| smoke check (load time, download size, warm reload) | done | 16 s |
| accessibility and readability scan | done | 2 s |
| app to the background, graphics context lost, phone rotated | done | 26 s |
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
| free play (random walking, tapping, refreshing) | done | 11 s |

People talked to: 2 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

### Desktop (Chromium, keyboard + mouse)

| Step | Result | Time |
|---|---|---|
| opening the Settings / Account / World / Controls panels | done | 23 s |
| walking the port (or the settlement of the start world) and talking to people | done | 280 s |
| earning the first ship: buy the two lifeboat parts and fit them | skipped (out of time) | 0 s |
| smoke check (load time, download size, warm reload) | skipped (out of time) | 0 s |
| accessibility and readability scan | skipped (out of time) | 0 s |
| spamming buttons and jumps | skipped (out of time) | 0 s |
| buy/sell loops and double taps on the shop | skipped (out of time) | 0 s |
| walking and jumping into walls and edges in 8 directions | skipped (out of time) | 0 s |
| turning on the spot, reading draw calls and frame times | skipped (out of time) | 0 s |
| random tapping everywhere | skipped (out of time) | 0 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| leaving the game alone for 90 s | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | skipped (out of time) | 0 s |

People talked to: 6 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- desktop / panels: typical 4 ms, slowest 7708 ms, 8 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 5765 ms, 2 frames over 250 ms
- iphone / opening: typical 15 ms, slowest 5503 ms, 2 frames over 250 ms
- iphone / lifeboat: typical 29 ms, slowest 5355 ms, 3 frames over 250 ms
- desktop / tour: typical 4 ms, slowest 5233 ms, 2 frames over 250 ms

Button response time (tap to something changing on screen): median 425 ms, slowest 1345 ms over 18 taps.

## QA checks (the things real testers do besides playing through)

See `tools/playtester/PRACTICES.md` for why each one exists. FAIL rows are also listed as problems above where they are real bugs.

### iPhone 15 (WebKit, touch): 12 passed, 4 failed, 1 skipped, 1 info

| Check | Result | Notes |
|---|---|---|
| lifeboat: the NEXT line on screen names who sells each part | pass | NEXT The lifeboat has no power. Buy a power cell from Okafor, the flight line crew chief (Skyward), the Skyward Launch Complex and a fuel coupler from Pruitt, the Homeguard organiser, the Skyward Laun |
| lifeboat: buy the cell from Okafor | pass | purse 10000 -> 9700 |
| lifeboat: buy the coupler from Pruitt | pass | purse 9700 -> 9400 |
| lifeboat: fit both parts, the boat is no longer drained | pass | HUD: NEXT Lifeboat ready. Crew are hired at the Crew Hall at Marineris Port on Mars: fly home (Course), land, and walk to the hall at the north e |
| smoke: page transfer on a cold load | info | 250 requests, 1.3 MB over the wire (slowest: beatobservatory.com/games/the-cosmos/src/port/workerLines.js 131 ms) |
| smoke: time from opening the link to the first drawn frames | pass | 14.2 s (headless software rendering, a real phone is usually quicker to draw but slower to download) |
| smoke: warm reload comes back | pass | 16.2 s |
| a11y: text is at least 11 px | FAIL | 8 small: #hud-readout 10px "· Skyward Launch Complex" ; b. 10px "Earth" ; span.dim 10px "Grass and soil · 9.82 m/" ; span.load 10px "Hauling cart: 0.0 / 399 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat |
| a11y: text contrast (4.5:1, or 3:1 for big text) | FAIL | 1 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " |
| a11y: every button has a name | FAIL | input. |
| a11y: tap targets at least 44 px (Apple guideline) | pass | 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44 |
| a11y: pinch-zoom is not locked off | FAIL | width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover |
| a11y: a volume or mute control exists | pass |  |
| readability: something on screen tells a player what to do next | pass | {"action":"Raise ramp","hint":"","caption":"","hud":"Earth · Skyward Launch Complex 28.612° N 80.599° W Grass and soil · 9.82 m/s² Hauling cart: 0.0 / 399 kg tool: Shovel NE","jobs":"","toast":"Earth frame."} |
| lifecycle: background 8 s and return keeps place, money and ship state | pass |  |
| lifecycle: graphics context lost and restored | skipped | this browser does not allow forcing it |
| lifecycle: rotate to 852x393, the 3D view fills the screen | pass | {"cw":852,"ch":393,"iw":852,"ih":393} |
| lifecycle: rotate to 852x393 with Settings open, the 3D view fills the screen | pass | {"cw":852,"ch":393,"iw":852,"ih":393} |

## Load, size and memory

- **iPhone 15 (WebKit, touch)**: load to first frames 14.2 s; cold-load download 1.3 MB in 250 requests; warm reload 16.2 s; busiest view not measured. Over the run (51 samples): graphics geometries 326 -> 114, textures 122 -> 15, page elements 235 -> 221 (JS heap is only readable in Chromium).
- **Desktop (Chromium, keyboard + mouse)**: load to first frames 15.1 s; cold-load download 1.3 MB in 250 requests; warm reload not measured; busiest view not measured. Over the run (17 samples): graphics geometries 712 -> 116, textures 254 -> 27, page elements 275 -> 214, JS heap 241 -> 213 MB.

## Vision pass

A vision model (claude CLI (sonnet)) looked at 36 screenshots for about $0.00 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
- Not possible from here (needs a real iPhone or two players): a real phone call or notification banner, lock screen, battery and heat, low-end phone speed, many device models, race-condition duplication between two players. The full list of what real QA does and which parts the bot covers is in tools/playtester/PRACTICES.md.
