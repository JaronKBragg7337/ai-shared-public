# The Cosmos playtest report

Run: 2026-10-09 23:59 (local)  |  Build under test: `84b5ad0a9da4dd931f6c`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

**How to read this:** items titled "Stuck while walking to ..." come from the bot's own steering (its path planner, run-ups and jumps). Treat them as bot-only unless a human also gets stuck at that spot. Black boot and crash-blackout frames that carry a caption are deliberate.

- **iPhone 15 (WebKit, touch)**: 18.1 minutes, 89 screenshots, 9 distinct problems
- **Desktop (Chromium, keyboard + mouse)**: 5 minutes, 44 screenshots, 15 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)
- Desktop (Chromium, keyboard + mouse): [session video](videos-desktop/<email>)

## Short version

33 distinct problems found: 1 blockers, 2 serious, 30 smaller.

- **Floating off the ground on a moon (airborne for 8+ seconds)** (BLOCKER, seen 13 times)
- **Stuck while walking to Tomas Grey** (Serious)
- **After the graphics context was lost and restored, the game never drew again** (Serious)
- **Could not walk to Bram Okonkwo** (Annoying)
- **A button is covered by something else: #multiplayer-button "World / crew" is covered by #touch-key-KeyD** (Annoying)

## Problems, worst first

### 1. Floating off the ground on a moon (airborne for 8+ seconds)

- **How bad:** BLOCKER (score 90), happened 13 times
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 12:04 into the run, on iPhone (WebKit)
- **What happened:** walking on the moon, still airborne after 10 s, speed 0.07 m/s {"r":2407415.58,"sampler":0.564,"shipGround":0.564,"vRad":-0.009,"suitHold":0.8,"jump":1.7926866684520575}
- **What the vision model saw:** First-person view at Callisto's Valhalla Camp, standing on the moon's surface near rows of supply crates on shelving under a starry sky, with HUD location/quest text top-left, World/crew and Controls buttons bottom-left, and a quest prompt box bottom-right. Flagged: A sharp diagonal line/crease crosses the ground in front of the player, as if the terrain is a flat tilted plate rather than continuous ground — consistent with the player floating above/at the edge of the moon's collision mesh
- **Later hits:** 12:06 walking on the moon, still airborne after 13 s, speed 0.06 m/s {"r":2407415.47,"sampler":0.45,"shipGround":0.45,"vRad":-0.008,"suitHold":0.8,"jump":1.7926866684520575} / 12:09 walking on the moon, still airborne after 15 s, speed 0.05 m/s {"r":2407415.36,"sampler":0.347,"shipGround":0.347,"vRad":-0.007,"suitHold":0.8,"jump":1.7926866684520575}
- **Screenshot:** [067-tour-PROBLEM-floating-on-moon.jpg](shots-iphone/067-tour-PROBLEM-floating-on-moon.jpg)

  ![Floating off the ground on a moon (airbo](shots-iphone/067-tour-PROBLEM-floating-on-moon.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to Tomas Grey
  1. outpost route of 45 legs around 0 solid things
  1. not getting closer (3 m away), trying to get unstuck #1
  1. run-up jump #1
  1. jump
  1. not getting closer (3 m away), trying to get unstuck #2
  1. run-up jump #2
  1. jump

### 2. Stuck while walking to Tomas Grey

- **How bad:** Serious (score 80)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 12:58 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at outpost 27,58 (target 30,58, 3 m away)
- **What the vision model saw:** Same Valhalla Camp supply-depot view as the previous shot, with the player apparently stuck in place after repeated attempts to walk closer to a target. Flagged: A partial arrow/cursor-like shape is clipped at the very top-left corner of the screen, as if a UI icon is rendering off-screen or stuck; Same diagonal terrain seam/edge as the prior shot is still visible, reinforcing that the player is not standing on normal ground
- **Screenshot:** [070-tour-PROBLEM-stuck-walking.jpg](shots-iphone/070-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Tomas Grey](shots-iphone/070-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (3 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (3 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. not getting closer (3 m away), trying to get unstuck #6
  1. not getting closer (3 m away), trying to get unstuck #7
  1. not getting closer (3 m away), trying to get unstuck #8

### 3. After the graphics context was lost and restored, the game never drew again

- **How bad:** Serious (score 80)
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:40 into the run, on desktop (Chromium)
- **What happened:** (see screenshot)
- **What the vision model saw:** The screen shows the game's boot/title screen (THE COSMOS, tagline, and a 'Loading the port…' line) after the bot refreshed to recover from a lost graphics context. Flagged: After the refresh meant to recover the lost graphics context, the game dropped all the way back to the initial boot/loading screen instead of restoring the player into the port/ship where they were — it's stuck on 'Loading the port…' rather than resuming session state
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

### 4. Could not walk to Bram Okonkwo

- **How bad:** Annoying (score 72)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 17:46 into the run, on iPhone (WebKit)
- **What happened:** gave up after 240s; last distance 323 m
- **What the vision model saw:** Player standing on a vast, almost featureless tan/beige expanse of regolith with only a floating arrow marker and a ground-level circle marker visible, HUD showing Shovel equipped and a Dig button bottom-right. Flagged: The entire visible terrain is empty with no structures, landmarks, or the outpost itself in view despite the quest context referencing an outpost route, suggesting the player is stranded far from any reachable target; The Dig button at bottom-right is rendered very faint/washed out compared to the Shovel button beside it, could read as disabled or broken
- **Screenshot:** [086-tour-PROBLEM-cannot-reach.jpg](shots-iphone/086-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Bram Okonkwo](shots-iphone/086-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #3
  1. jump
  1. not getting closer (3 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (3 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. outpost route of 75 legs around 0 solid things

### 5. A button is covered by something else: #multiplayer-button "World / crew" is covered by #touch-key-KeyD

- **How bad:** Annoying (score 68)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:35 into the run, on desktop (Chromium)
- **What happened:** #multiplayer-button "World / crew" is covered by #touch-key-KeyD (Controls open, desktop)
- **What the vision model saw:** Desktop view identical to the previous shot, taken right after tapping the Controls button again to close the panel, but the Controls panel is still fully displayed. Flagged: Tapping Controls to toggle it closed did not close the panel — it remains open and still covers the 'World / crew' button underneath; Same partially clipped cyan/teal shape at the far-left screen edge persists
- **Screenshot:** [011-panels-PROBLEM-covered.jpg](shots-desktop/011-panels-PROBLEM-covered.jpg)

  ![A button is covered by something else: #](shots-desktop/011-panels-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-close-settings (close Settings)
  1. mis-tap beside #purse
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. mis-tap beside #btn-key-controls
  1. tap #btn-key-controls (open Controls)

### 6. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 3 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:23 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 3 after tapping "Dig (E)"
- **What the vision model saw:** Top-down digging minigame view of a sandy/dusty area with a buried crate and antenna poking out, an orange target ring in the dirt, and a Dig (E) button bottom right.
- **Later hits:** 06:40 cuts stayed 3 after tapping "Dig (E)" / 06:42 cuts stayed 3 after tapping "Dig (E)"
- **Screenshot:** [033-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/033-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/033-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. opening stage 3 -> 4 (Something lies beneath the collapsed dust.)
  1. walk to the crate
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. mis-tap beside #opening-action
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)

### 7. Buttons overlap: #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83%

- **How bad:** Annoying (score 66)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:35 into the run, on desktop (Chromium)
- **What happened:** #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83% (Controls open, desktop)
- **What the vision model saw:** Desktop view of the Controls (keybindings) panel opened on the left side, listing action buttons like Debug, View, Fire, Shovel, etc., over the same Mars landing pad scene. Flagged: The open Controls panel covers the area where the 'World / crew' button normally sits, hiding it from view/use; Same partially clipped cyan/teal shape at the far-left screen edge as before
- **Screenshot:** [010-panels-PROBLEM-overlap.jpg](shots-desktop/010-panels-PROBLEM-overlap.jpg)

  ![Buttons overlap: #touch-key-KeyD "Right"](shots-desktop/010-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-close-settings (close Settings)
  1. mis-tap beside #purse
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. mis-tap beside #btn-key-controls
  1. tap #btn-key-controls (open Controls)

### 8. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 9 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:15 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 3773 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Interior of a ship/station walkway looking out through windows at a large orange dome structure and a docked ship, with Walter speaking a dialogue line at the bottom. Flagged: A flat solid-gray horizontal bar cuts straight across the screen above the window line, with a dark triangular wedge at its left edge — looks like a misplaced/misrendered geometry strip rather than part of the ceiling or window frame; A thin white vertical line/pole floats above the railing with no visible base or object it belongs to
- **Later hits:** 05:46 a single frame took 4323 ms (typical 27 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 05:57 a single frame took 1379 ms (typical 26 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 9. Frame-time spike during "lifecycle"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:51 into the run, on desktop (Chromium)
- **What happened:** a single frame took 4742 ms (typical 4 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 02:01 a single frame took 2721 ms (typical 25 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
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
- **Where:** network cut, refresh offline, slow connection, first at 02:31 into the run, on desktop (Chromium)
- **What happened:** a single frame took 4966 ms (typical 4 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 02:36 a single frame took 2879 ms (typical 33 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
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
- **What happened:** a single frame took 7566 ms (typical 4 ms); 8 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Desktop view of the Settings panel open on the right side over a Mars Valles Marineris landing pad scene with the ship's engine nozzles and a 'Systems nominal' tooltip. Flagged: A small cyan/teal shape is clipped at the far-left edge of the screen, only a sliver visible, suggesting a UI element is partially off-screen
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
- **Where:** smoke check (load time, download size, warm reload), first at 00:45 into the run, on desktop (Chromium)
- **What happened:** a single frame took 4796 ms (typical 4 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Landing pad on Mars (Valles Marineris) with a tilted spacecraft/lander, its two large engine nozzles, a ramp, and a HUD overlay showing location, cart status, and a quest prompt. Flagged: Hauling cart progress bar is rendered nearly full even though the label reads '0.0 / 1054 kg'; Small cyan/light-blue triangular shape sitting on the ground with no label or context
- **Screenshot:** [013-smoke-PROBLEM-frame-spike.jpg](shots-desktop/013-smoke-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "smoke"](shots-desktop/013-smoke-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. mis-tap beside #btn-key-controls
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase smoke starts
  1. QA info: smoke: page transfer on a cold load - 250 requests, 1.3 MB over the wire (slowest: ps://www.heartbeatobservatory.com/_vercel/insights/script.js 240 ms)
  1. QA pass: smoke: time from opening the link to the first drawn frames - 14.6 s (headless software rendering, a real phone is usually quicker to draw but slower to download)
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 13. Looks wrong in the screenshot: Two overlapping panel borders/Close buttons render on top of each other (one small Close top-right, another la

- **How bad:** Annoying (score 56)
- **Where:** opening the Settings / Account / World / Controls panels, first at 08:31 into the run, on iPhone (WebKit)
- **What happened:** whole panel area (the vision model's description of the screen: Account/purse panel open showing 'Ship account · Mars marks' with currency, supplies, and crew-wage info, plus a Close button.)
- **Screenshot:** [048-panels-panel-Account-purse.jpg](shots-iphone/048-panels-panel-Account-purse.jpg)

  ![Looks wrong in the screenshot: Two overl](shots-iphone/048-panels-panel-Account-purse.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #purse (open Account / purse)

### 14. Looks wrong in the screenshot: The entire visible terrain is empty with no structures, landmarks, or the outpost itself in view despite the q

- **How bad:** Annoying (score 56)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 17:46 into the run, on iPhone (WebKit)
- **What happened:** whole screen/background (the vision model's description of the screen: Player standing on a vast, almost featureless tan/beige expanse of regolith with only a floating arrow marker and a ground-level circle marker visible, HUD showing Shovel equipped and a Dig button bottom-right.)
- **Screenshot:** [086-tour-PROBLEM-cannot-reach.jpg](shots-iphone/086-tour-PROBLEM-cannot-reach.jpg)

  ![Looks wrong in the screenshot: The entir](shots-iphone/086-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. outpost route of 75 legs around 0 solid things

### 15. Looks wrong in the screenshot: After the refresh meant to recover the lost graphics context, the game dropped all the way back to the initial

- **How bad:** Annoying (score 56)
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:40 into the run, on desktop (Chromium)
- **What happened:** whole screen, centered loading text (the vision model's description of the screen: The screen shows the game's boot/title screen (THE COSMOS, tagline, and a 'Loading the port…' line) after the bot refreshed to recover from a lost graphics context.)
- **Screenshot:** [026-lifecycle-PROBLEM-context-not-restored.jpg](shots-desktop/026-lifecycle-PROBLEM-context-not-restored.jpg)

  ![Looks wrong in the screenshot: After the](shots-desktop/026-lifecycle-PROBLEM-context-not-restored.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (recovering after a lost graphics context)

### 16. Console error

- **How bad:** Annoying (score 55), happened 6 times
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 11:04 into the run, on iPhone (WebKit)
- **What happened:** Failed to load resource: the server responded with a status of 404 ()
- **What the vision model saw:** Identical dialogue popup for Director Ila Sorn with the same three conversation choices, background slightly repositioned.
- **Later hits:** 11:05 Failed to load resource: the server responded with a status of 404 () / 13:18 Failed to load resource: the server responded with a status of 404 ()
- **Screenshot:** [061-tour-PROBLEM-console-error.jpg](shots-iphone/061-tour-PROBLEM-console-error.jpg)

  ![Console error](shots-iphone/061-tour-PROBLEM-console-error.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. AIRTRACE [grounded-before, grounded-after, dist-to-drawn-ground, radial-vel, moving, pushOut]: [[0,0,0.696,-0.044,1,0],[0,0,0.695,-0.048,1,0],[0,0,0.693,-0.045,1,0],[0,0,0.692,-0.036,1,0],[0,0,0.691,-0.038,1,0],[0,0,0.69,-0.046,1,0],[0,0,0.689,-0.047,1,0],[0,0,0.687,-0.033,1,0],[0,0,0.687,-0.042,1,0],[0,0,0.685,-0.046,1,0],[0,0,0.684,-0.047,1,0],[0,0,0.683,-0.047,1,0],[0,0,0.681,-0.04,1,0],[0,0,0.68,-0.035,1,0],[0,0,0.679,-0.028,1,0],[0,0,0.679,-0.043,1,0],[0,0,0.678,-0.048,1,0],[0,0,0.676,-0.036,1,0],[0,0,0.675,-0.039,1,0],[0,0,0.674,-0.045,1,0],[0,0,0.673,-0.036,1,0],[0,0,0.672,-0.038,1,0],[0,0,0.671,-0.045,1,0],[0,0,0.67,-0.03,1,0],[0,0,0.669,-0.042,1,0],[0,0,0.668,-0.034,1,0],[0,0,0.667,-0.06,1,0],[0,0,0.665,-0.039,1,0],[0,0,0.664,-0.039,1,0],[0,0,0.663,-0.034,1,0],[0,0,0.662,-0.038,1,0],[0,0,0.661,-0.045,1,0],[0,0,0.66,-0.034,1,0],[0,0,0.659,-0.039,1,0],[0,0,0.658,-0.032,1,0],[0,0,0.658,-0.04,1,0],[0,0,0.657,-0.045,1,0],[0,0,0.655,-0.047,1,0],[0,0,0.654,-0.035,1,0],[0,0,0.653,-0.039,1,0]]
  1. not getting closer (4 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (4 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. outpost route of 7 legs around 0 solid things
  1. tap #crew-talk (Talk to Director Ila Sorn)

### 17. Request returned HTTP 404

- **How bad:** Minor (score 50), happened 6 times
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 11:04 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/undefined.jpg
- **What the vision model saw:** Same HUD as above, now with a dialogue popup for Director Ila Sorn offering three conversation choices against a shelving/corridor background.
- **Later hits:** 11:05 https://www.heartbeatobservatory.com/homes/people/undefined.jpg / 13:18 https://www.heartbeatobservatory.com/homes/people/undefined.jpg
- **Screenshot:** [060-tour-PROBLEM-http.jpg](shots-iphone/060-tour-PROBLEM-http.jpg)

  ![Request returned HTTP 404](shots-iphone/060-tour-PROBLEM-http.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. AIRTRACE [grounded-before, grounded-after, dist-to-drawn-ground, radial-vel, moving, pushOut]: [[0,0,0.696,-0.044,1,0],[0,0,0.695,-0.048,1,0],[0,0,0.693,-0.045,1,0],[0,0,0.692,-0.036,1,0],[0,0,0.691,-0.038,1,0],[0,0,0.69,-0.046,1,0],[0,0,0.689,-0.047,1,0],[0,0,0.687,-0.033,1,0],[0,0,0.687,-0.042,1,0],[0,0,0.685,-0.046,1,0],[0,0,0.684,-0.047,1,0],[0,0,0.683,-0.047,1,0],[0,0,0.681,-0.04,1,0],[0,0,0.68,-0.035,1,0],[0,0,0.679,-0.028,1,0],[0,0,0.679,-0.043,1,0],[0,0,0.678,-0.048,1,0],[0,0,0.676,-0.036,1,0],[0,0,0.675,-0.039,1,0],[0,0,0.674,-0.045,1,0],[0,0,0.673,-0.036,1,0],[0,0,0.672,-0.038,1,0],[0,0,0.671,-0.045,1,0],[0,0,0.67,-0.03,1,0],[0,0,0.669,-0.042,1,0],[0,0,0.668,-0.034,1,0],[0,0,0.667,-0.06,1,0],[0,0,0.665,-0.039,1,0],[0,0,0.664,-0.039,1,0],[0,0,0.663,-0.034,1,0],[0,0,0.662,-0.038,1,0],[0,0,0.661,-0.045,1,0],[0,0,0.66,-0.034,1,0],[0,0,0.659,-0.039,1,0],[0,0,0.658,-0.032,1,0],[0,0,0.658,-0.04,1,0],[0,0,0.657,-0.045,1,0],[0,0,0.655,-0.047,1,0],[0,0,0.654,-0.035,1,0],[0,0,0.653,-0.039,1,0]]
  1. not getting closer (4 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (4 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. outpost route of 7 legs around 0 solid things
  1. tap #crew-talk (Talk to Director Ila Sorn)

### 18. Looks wrong in the screenshot: A solid flat light-gray horizontal bar cuts across the full width of the screen over the window/railing area, 

- **How bad:** Minor (score 49)
- **Where:** loading the page, first at 00:15 into the run, on iPhone (WebKit)
- **What happened:** horizontal band about 1/4 down from the top, spanning the full screen width (the vision model's description of the screen: First-person view in a ship corridor overlooking an orange dome structure outside, with move/look control hints at top and Walter's dialogue line at the bottom.)
- **Screenshot:** [001-start-loaded.jpg](shots-iphone/001-start-loaded.jpg)

  ![Looks wrong in the screenshot: A solid f](shots-iphone/001-start-loaded.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 19. Looks wrong in the screenshot: A sharp diagonal line/crease crosses the ground in front of the player, as if the terrain is a flat tilted pla

- **How bad:** Minor (score 49)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 12:04 into the run, on iPhone (WebKit)
- **What happened:** center-left of screen, cutting diagonally across the regolith (the vision model's description of the screen: First-person view at Callisto's Valhalla Camp, standing on the moon's surface near rows of supply crates on shelving under a starry sky, with HUD location/quest text top-left, World/crew and Controls buttons bottom-left, and a quest prompt box bottom-right.)
- **Screenshot:** [067-tour-PROBLEM-floating-on-moon.jpg](shots-iphone/067-tour-PROBLEM-floating-on-moon.jpg)

  ![Looks wrong in the screenshot: A sharp d](shots-iphone/067-tour-PROBLEM-floating-on-moon.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump

### 20. Looks wrong in the screenshot: Same diagonal terrain seam/edge as the prior shot is still visible, reinforcing that the player is not standin

- **How bad:** Minor (score 49)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 12:58 into the run, on iPhone (WebKit)
- **What happened:** center-left of screen (the vision model's description of the screen: Same Valhalla Camp supply-depot view as the previous shot, with the player apparently stuck in place after repeated attempts to walk closer to a target.)
- **Screenshot:** [070-tour-PROBLEM-stuck-walking.jpg](shots-iphone/070-tour-PROBLEM-stuck-walking.jpg)

  ![Looks wrong in the screenshot: Same diag](shots-iphone/070-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (3 m away), trying to get unstuck #8

### 21. Looks wrong in the screenshot: The open Controls panel covers the area where the 'World / crew' button normally sits, hiding it from view/use

- **How bad:** Minor (score 49)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:36 into the run, on desktop (Chromium)
- **What happened:** lower-left, under the Controls panel (the vision model's description of the screen: Desktop view of the Controls (keybindings) panel opened on the left side, listing action buttons like Debug, View, Fire, Shovel, etc., over the same Mars landing pad scene.)
- **Screenshot:** [010-panels-PROBLEM-overlap.jpg](shots-desktop/010-panels-PROBLEM-overlap.jpg)

  ![Looks wrong in the screenshot: The open ](shots-desktop/010-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (open Controls)

### 22. Looks wrong in the screenshot: Tapping Controls to toggle it closed did not close the panel — it remains open and still covers the 'World / c

- **How bad:** Minor (score 49)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:36 into the run, on desktop (Chromium)
- **What happened:** lower-left, under the Controls panel (the vision model's description of the screen: Desktop view identical to the previous shot, taken right after tapping the Controls button again to close the panel, but the Controls panel is still fully displayed.)
- **Screenshot:** [011-panels-PROBLEM-covered.jpg](shots-desktop/011-panels-PROBLEM-covered.jpg)

  ![Looks wrong in the screenshot: Tapping C](shots-desktop/011-panels-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (toggle closed Controls)

### 23. Looks wrong in the screenshot: Frame is pixel-identical to the previous capture, consistent with view being locked/unresponsive to the zoom a

- **How bad:** Minor (score 49)
- **Where:** accessibility and readability scan, first at 00:53 into the run, on desktop (Chromium)
- **What happened:** whole viewport (the vision model's description of the screen: Same Mars landing-pad scene framed identically to the others, suggesting the camera/zoom did not change between captures.)
- **Screenshot:** [019-a11y-PROBLEM-a11y-zoom-locked.jpg](shots-desktop/019-a11y-PROBLEM-a11y-zoom-locked.jpg)

  ![Looks wrong in the screenshot: Frame is ](shots-desktop/019-a11y-PROBLEM-a11y-zoom-locked.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"","hint":"","caption":"","hud":"Mars · Valles Marineris 13°59'56.9\"S 59°11'47.9\"W +2213.1 m Martian regolith · 3.72 m/s² Hauling cart: 0.0 / 1054 k

### 24. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:39 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 03:36 [opening] walk to down the gangway
- **What the vision model saw:** Night-time arrival scene on a dim landing strip with a lit ARRIVALS sign in the distance, a Skip intro button top right, and Steward dialogue at the bottom welcoming the player to Mars.
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

### 25. Game said: "This deletes your current character (its ship, crew, marks and pad) an"

- **How bad:** Minor (score 42)
- **Where:** random tapping everywhere, first at 02:51 into the run, on desktop (Chromium)
- **What happened:** shown in account-section while the bot was: 02:50 [monkey] monkey tap btn-close-settings
- **Screenshot:** [037-monkey-PROBLEM-refusal-message.jpg](shots-desktop/037-monkey-PROBLEM-refusal-message.jpg)

  ![Game said: "This deletes your current ch](shots-desktop/037-monkey-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. monkey tap purse
  1. jump
  1. monkey tap btn-key-controls
  1. monkey tap btn-action
  1. monkey tap touch-key-Digit1
  1. monkey tap Start fresh: new charact
  1. monkey tap btn-close-settings

### 26. Frame-time spike during "tour"

- **How bad:** Minor (score 38), happened 2 times
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 10:15 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 900 ms (typical 27 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Tour-phase HUD showing the Callisto/Valhalla Camp status panel with coordinates, hauling cart, tool, and the NEXT objective text about buying a power cell and fuel coupler, over a blurred corridor background, with World/crew and Controls buttons at bottom.
- **Later hits:** 17:57 a single frame took 4884 ms (typical 15 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [057-tour-PROBLEM-frame-spike.jpg](shots-iphone/057-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/057-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. settlement world Callisto: people Director Ila Sorn, Tomas Grey, Odette Marsh, Farah Adeyemi, Bram Okonkwo
  1. go talk to Director Ila Sorn
  1. walk to Director Ila Sorn
  1. outpost route of 80 legs around 0 solid things
  1. not getting closer (4 m away), trying to get unstuck #1
  1. run-up jump #1

### 27. Low text contrast in 2 places

- **How bad:** Minor (score 38)
- **Where:** accessibility and readability scan, first at 00:52 into the run, on desktop (Chromium)
- **What happened:** span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
- **What the vision model saw:** Same Mars landing-pad scene with the HUD panel and toast message 'Systems nominal. Ship down and stable.' Flagged: Dim grey subtext ('Martian regolith · 3.72 m/s²', 'tool: Shovel') has low contrast against the dark brown translucent panel, harder to read than the orange headline text; Hauling cart bar shows full despite '0.0/1054 kg' value
- **Screenshot:** [017-a11y-PROBLEM-a11y-contrast.jpg](shots-desktop/017-a11y-PROBLEM-a11y-contrast.jpg)

  ![Low text contrast in 2 places](shots-desktop/017-a11y-PROBLEM-a11y-contrast.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 9.8 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"

### 28. Frame-time spike during "a11y"

- **How bad:** Minor (score 38)
- **Where:** accessibility and readability scan, first at 00:53 into the run, on desktop (Chromium)
- **What happened:** a single frame took 2775 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Same Mars landing-pad scene with HUD and toast message still visible. Flagged: No visible stutter/tear artifacts in this single frame; a frame-rate spike can't be confirmed from a static screenshot; Hauling cart bar shows full despite '0.0/1054 kg' value
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

### 29. Text smaller than 11 px in 2 places (hard to read on a phone)

- **How bad:** Minor (score 36)
- **Where:** accessibility and readability scan, first at 00:52 into the run, on desktop (Chromium)
- **What happened:** span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
- **What the vision model saw:** Same Mars landing-pad scene with the HUD panel showing location, cart status, and a long quest-instruction paragraph. Flagged: Body text in the HUD (coordinates, 'Martian regolith' line, quest paragraph) is rendered quite small relative to the 1280x720 frame, hard to read at a glance; Hauling cart bar shows full despite '0.0/1054 kg' value
- **Screenshot:** [016-a11y-PROBLEM-a11y-small-text.jpg](shots-desktop/016-a11y-PROBLEM-a11y-small-text.jpg)

  ![Text smaller than 11 px in 2 places (har](shots-desktop/016-a11y-PROBLEM-a11y-small-text.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: smoke: time from opening the link to the first drawn frames - 14.6 s (headless software rendering, a real phone is usually quicker to draw but slower to download)
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 9.8 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"

### 30. 1 buttons have no text or label (a screen reader says nothing)

- **How bad:** Small (score 34)
- **Where:** accessibility and readability scan, first at 00:52 into the run, on desktop (Chromium)
- **What happened:** input.
- **What the vision model saw:** Same Mars landing-pad scene; no distinguishing name/label is visible on the ship, the pad building, or the small cyan object. Flagged: The small cyan triangular object on the ground has no name/label/tooltip despite looking like an interactive marker; Hauling cart bar shows full despite '0.0/1054 kg' value
- **Screenshot:** [018-a11y-PROBLEM-a11y-noname.jpg](shots-desktop/018-a11y-PROBLEM-a11y-noname.jpg)

  ![1 buttons have no text or label (a scree](shots-desktop/018-a11y-PROBLEM-a11y-noname.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 9.8 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.

### 31. Zooming the page is switched off in the viewport tag

- **How bad:** Small (score 30)
- **Where:** accessibility and readability scan, first at 00:52 into the run, on desktop (Chromium)
- **What happened:** width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
- **What the vision model saw:** Same Mars landing-pad scene framed identically to the others, suggesting the camera/zoom did not change between captures. Flagged: Frame is pixel-identical to the previous capture, consistent with view being locked/unresponsive to the zoom action being tested
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

### 32. graphics shapes (geometries) grew from 364 to 757 over the run (new areas loading, or a leak)

- **How bad:** Small (score 30)
- **Where:** free play (random walking, tapping, refreshing), first at 05:01 into the run, on desktop (Chromium)
- **What happened:** samples 30; phases lifecycle -> freeplay. Only a leak if it keeps climbing while standing still: the idle check measures that.

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. jump
  1. jump
  1. jump
  1. QA pass: edges: walked and jumped into walls in 8 directions, never fell through - furthest 41 m from where it started
  1. QA pass: edges: still drawing afterwards
  1. === phase freeplay starts
  1. jump

### 33. Network cut for about 12 s and the game said nothing and still thinks it is connected

- **How bad:** Small (score 28)
- **Where:** network cut, refresh offline, slow connection, first at 02:17 into the run, on desktop (Chromium)
- **What happened:** connected=true. A hint only: the bot's offline switch may not cut a socket that is already open, so a real phone going into a tunnel could behave differently.
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
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 492 s |
| opening the Settings / Account / World / Controls panels | done | 9 s |
| walking the port (or the settlement of the start world) and talking to people | done - settlement Callisto: 3 of 5 talked to | 551 s |
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
| turning on the spot, reading draw calls and frame times | skipped (out of time) | 0 s |
| random tapping everywhere | skipped (out of time) | 0 s |
| leaving the game alone for 90 s | skipped (out of time) | 0 s |
| end-of-run soft-lock check | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | skipped (out of time) | 0 s |

People talked to: 3 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

### Desktop (Chromium, keyboard + mouse)

| Step | Result | Time |
|---|---|---|
| opening the Settings / Account / World / Controls panels | done | 21 s |
| smoke check (load time, download size, warm reload) | done | 10 s |
| accessibility and readability scan | done | 7 s |
| spamming buttons and jumps | done | 25 s |
| app to the background, graphics context lost, phone rotated | done | 42 s |
| network cut, refresh offline, slow connection | done | 35 s |
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
| free play (random walking, tapping, refreshing) | done | 6 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / opening: typical 16 ms, slowest 7584 ms, 4 frames over 250 ms
- desktop / panels: typical 4 ms, slowest 7566 ms, 8 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 5757 ms, 2 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 4982 ms, 1 frames over 250 ms
- desktop / network: typical 4 ms, slowest 4966 ms, 3 frames over 250 ms

Button response time (tap to something changing on screen): median 411 ms, slowest 1166 ms over 11 taps.

## QA checks (the things real testers do besides playing through)

See `tools/playtester/PRACTICES.md` for why each one exists. FAIL rows are also listed as problems above where they are real bugs.

### Desktop (Chromium, keyboard + mouse): 19 passed, 5 failed, 1 skipped, 2 info

| Check | Result | Notes |
|---|---|---|
| smoke: page transfer on a cold load | info | 250 requests, 1.3 MB over the wire (slowest: ps://www.heartbeatobservatory.com/_vercel/insights/script.js 240 ms) |
| smoke: time from opening the link to the first drawn frames | pass | 14.6 s (headless software rendering, a real phone is usually quicker to draw but slower to download) |
| smoke: warm reload comes back | pass | 9.8 s |
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
| network: slow connection (900 ms, 60 KB/s) for a panel tap | pass | 6 s |
| perf: turning on the spot, 95 percent of frames under 34 ms | pass | median 25 ms, 95th 30 ms, slowest 50 ms; peak 130 draw calls, 37k triangles (headless software rendering, judge relatively) |
| monkey: 29 random button taps and wild gestures, no crash | pass |  |
| edges: walked and jumped into walls in 8 directions, never fell through | pass | furthest 41 m from where it started |
| edges: still drawing afterwards | pass |  |

## Load, size and memory

- **iPhone 15 (WebKit, touch)**: load to first frames 14.0 s; cold-load download 1.3 MB in 250 requests; warm reload not measured; busiest view not measured. Over the run (56 samples): graphics geometries 330 -> 32, textures 123 -> 12, page elements 235 -> 219 (JS heap is only readable in Chromium).
- **Desktop (Chromium, keyboard + mouse)**: load to first frames 14.6 s; cold-load download 1.3 MB in 250 requests; warm reload 9.8 s; busiest view 130 draw calls, 37k triangles. Over the run (35 samples): graphics geometries 363 -> 757, textures 206 -> 256, page elements 277 -> 310, JS heap 272 -> 225 MB.

## Vision pass

A vision model (claude CLI (sonnet)) looked at 36 screenshots for about $0.00 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
- Not possible from here (needs a real iPhone or two players): a real phone call or notification banner, lock screen, battery and heat, low-end phone speed, many device models, race-condition duplication between two players. The full list of what real QA does and which parts the bot covers is in tools/playtester/PRACTICES.md.
