# The Cosmos playtest report

Run: 2026-10-05 01:40 (local)  |  Build under test: `9b85464edb02e3c060b1`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

**How to read this:** items titled "Stuck while walking to ..." come from the bot's own steering (its path planner, run-ups and jumps). Treat them as bot-only unless a human also gets stuck at that spot. Black boot and crash-blackout frames that carry a caption are deliberate.

- **iPhone 15 (WebKit, touch)**: 15.2 minutes, 107 screenshots, 8 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)

## Short version

12 distinct problems found: 0 blockers, 2 serious, 10 smaller.

- **Stuck while walking to Shift runner** (Serious)
- **Stuck while walking to Lookout at the glass** (Serious)
- **A Dig tap in the opening made no cut** (Annoying)
- **Looks wrong in the screenshot: The whole viewport is black with no caption, title, loading text or Skip intro button. The bot reported 'openi** (Annoying)
- **Frame-time spike during "opening"** (Annoying, seen 12 times)

## Problems, worst first

### 1. Stuck while walking to Shift runner

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 12:54 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -61,-41 (target -64,-41, 3 m away)
- **What the vision model saw:** {"description": "A mobile HUD for the Mars Valles Marineris scene is overlaid on a heavily blurred, washed-out beige and white 3D view, with a mission info panel at top left, a virtual joystick and a 
- **Screenshot:** [101-tour-PROBLEM-stuck-walking.jpg](shots-iphone/101-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Shift runner](shots-iphone/101-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (3 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 3 legs
  1. not getting closer (3 m away), trying to get unstuck #6
  1. not getting closer (3 m away), trying to get unstuck #7
  1. not getting closer (3 m away), trying to get unstuck #8

### 2. Stuck while walking to Lookout at the glass

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 14:10 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -59,-41 (target -56,-41, 4 m away)
- **What the vision model saw:** {"description": "A mobile first-person view on Mars (Valles Marineris) showing a HUD with location, tool and objective text, but the 3D scene is a heavily blurred beige and brown blur with a white ver
- **Screenshot:** [104-tour-PROBLEM-stuck-walking.jpg](shots-iphone/104-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Lookout at the gl](shots-iphone/104-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (4 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 3 legs
  1. not getting closer (4 m away), trying to get unstuck #6
  1. not getting closer (4 m away), trying to get unstuck #7
  1. not getting closer (4 m away), trying to get unstuck #8

### 3. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:55 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 4 after tapping "Dig (E)"
- **What the vision model saw:** A dark red, almost empty viewport shows an orange ring reticle in the center, a hint at the bottom reading 'Aim the shovel at the dust around the crate.', a 'Skip intro' button at top right, a 'Dig (E)' button at bottom right, and a small 'Walk · Look · Use (E / touch)' label at top left. Flagged: The instruction says to aim the shovel at the dust around the crate, but no crate, dust, shovel, ground or any other world geometry is visible. The viewport is only a flat dark red gradient, so the player has nothing to aim at.; The top-left control hint is very small and low-contrast, so it is hard to read on a phone screen.
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

### 4. Looks wrong in the screenshot: The whole viewport is black with no caption, title, loading text or Skip intro button. The bot reported 'openi

- **How bad:** Annoying (score 63)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 08:42 into the run, on iPhone (WebKit)
- **What happened:** Entire screen (the vision model's description of the screen: The screenshot is entirely black, with no visible title, caption, loading text, Skip intro button, HUD, or 3D world content.)
- **Screenshot:** [044-opening-opening-done.jpg](shots-iphone/044-opening-opening-done.jpg)

  ![Looks wrong in the screenshot: The whole](shots-iphone/044-opening-opening-done.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening finished

### 5. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 12 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:20 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 5655 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** {"description": "A first-person view from inside a dark observation lounge on a ship, looking through a railing and glass at a large red planet with docked ships outside, with a small table in the for
- **Later hits:** 01:18 a single frame took 4067 ms (typical 15 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 01:31 a single frame took 5193 ms (typical 26 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 6. Looks wrong in the screenshot: The instruction says to aim the shovel at the dust around the crate, but no crate, dust, shovel, ground or any

- **How bad:** Annoying (score 56)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:55 into the run, on iPhone (WebKit)
- **What happened:** Whole viewport, around the central reticle (the vision model's description of the screen: A dark red, almost empty viewport shows an orange ring reticle in the center, a hint at the bottom reading 'Aim the shovel at the dust around the crate.', a 'Skip intro' button at top right, a 'Dig (E)' button at bottom right, and a small 'Walk · Look · Use (E / touch)' label at top left.)
- **Screenshot:** [035-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/035-opening-PROBLEM-dig-tap-lost.jpg)

  ![Looks wrong in the screenshot: The instr](shots-iphone/035-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)

### 7. Server connection (websocket) closed

- **How bad:** Minor (score 50), happened 2 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 01:02 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **What the vision model saw:** A near-black boot screen with the title 'THE COSMOS', a three-line tagline, and a 'Loading the port…' line centered in the viewport.
- **Later hits:** 01:07 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Screenshot:** [007-opening-PROBLEM-ws-closed.jpg](shots-iphone/007-opening-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/007-opening-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap screen to unlock sound
  1. tap screen to unlock sound
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. in the boarding hall, waiting for the gangway to come down
  1. websocket closed

### 8. Looks wrong in the screenshot: The captain's subtitle is light grey text with no backing panel, laid over the busy grated floor texture. Seve

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:56 into the run, on iPhone (WebKit)
- **What happened:** Bottom of the screen, the 'CAPTAIN' caption block (the vision model's description of the screen: A first-person view down a metal-floored boarding hall toward a closed grey door with a small window and yellow-striped panels on either side, with a captain's subtitle about the ships off the port and starboard sides shown at the bottom.)
- **Screenshot:** [006-opening-opening.jpg](shots-iphone/006-opening-opening.jpg)

  ![Looks wrong in the screenshot: The capta](shots-iphone/006-opening-opening.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. in the boarding hall, waiting for the gangway to come down

### 9. Looks wrong in the screenshot: Large foreground geometry (a beam and wall edge, a railing and a box-like ledge) blocks much of the view, and 

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 11:21 into the run, on iPhone (WebKit)
- **What happened:** center and lower-left of the viewport (the vision model's description of the screen: A first-person view on Mars (Valles Marineris) from inside or beside a structure with beige pillars and a railing, looking out at a port with buildings and a reddish horizon, with a HUD panel showing location, hauling cart, a mission hint and currency, plus World/crew, Controls and Talk buttons.)
- **Screenshot:** [090-tour-after-talk-cab-ground.jpg](shots-iphone/090-tour-after-talk-cab-ground.jpg)

  ![Looks wrong in the screenshot: Large for](shots-iphone/090-tour-after-talk-cab-ground.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap button "✕" (close talk panel)

### 10. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 04:02 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 04:02 [opening] walk to the arrivals hall board
- **What the vision model saw:** {"description": "A first-person view on a dusky Martian landing pad with a purple-to-red sky, a dark horizon, and a yellow stripe on the ground. The HUD shows an objective at the top left, a Skip intr
- **Screenshot:** [019-opening-PROBLEM-refusal-message.jpg](shots-iphone/019-opening-PROBLEM-refusal-message.jpg)

  ![Game said: "Welcome to Mars. Follow the ](shots-iphone/019-opening-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. walk to down the gangway
  1. walk to down the gangway
  1. walk to down the gangway
  1. opening stage 0 -> 1 (StewardWelcome to Mars. Follow the amber lights to the big Arrivals sign. If you reach a fuel tank, you have taken touri)
  1. walk to the arrivals hall board

### 11. Game said: "Weather sensors are offline. Watch the dust outside."

- **How bad:** Minor (score 42)
- **Where:** walking the port and talking to people, first at 11:36 into the run, on iPhone (WebKit)
- **What happened:** shown in crew-panel while the bot was: 11:35 [tour] tap #crew-talk (Talk to Weather officer)
- **What the vision model saw:** {"description": "A mobile view of the Mars port shows a Weather officer dialogue panel (\"Weather sensors are offline. Watch the dust outside.\") with two options, over a close-up of a corrugated wood
- **Screenshot:** [095-tour-PROBLEM-refusal-message.jpg](shots-iphone/095-tour-PROBLEM-refusal-message.jpg)

  ![Game said: "Weather sensors are offline.](shots-iphone/095-tour-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. go talk to Weather officer
  1. walk to Weather officer
  1. tap #crew-talk (Talk to Weather officer)
  1. opened Ground controller instead of Weather officer; stepping closer to the right person
  1. tap button "✕" (close talk panel)
  1. go talk to Weather officer
  1. walk to Weather officer
  1. tap #crew-talk (Talk to Weather officer)

### 12. Frame-time spike during "tour"

- **How bad:** Minor (score 38), happened 2 times
- **Where:** walking the port and talking to people, first at 08:58 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 1287 ms (typical 38 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** A first-person view of a Martian landscape in Valles Marineris at dusk, with a HUD panel at top-left showing location, a hauling cart readout, a tool label and a NEXT objective, plus a Settings button, a virtual joystick, and World / crew and Controls buttons, with a light pole and low buildings or containers in the distance. Flagged: The top-left HUD panel is fairly large and its small, low-contrast text (the dim grey 'Duricrust' line and the 'tool: Shovel' line) is hard to read against the dark brown background. Nothing is cut off or overlapping.; The distant structures and the concrete barriers on the right edge look flat and blocky, and the barrier at the right edge is cropped by the screen. This is minor and probably just the camera framing.
- **Later hits:** 15:01 a single frame took 3538 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [054-tour-PROBLEM-frame-spike.jpg](shots-iphone/054-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/054-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide
  1. route of 20 legs

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 503 s |
| opening the Settings / Account / World / Controls panels | done | 11 s |
| walking the port and talking to people | done | 356 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| boarding the ship, taking a seat and flying a course | skipped (out of time) | 0 s |
| getting into and driving the survey rover | skipped (out of time) | 0 s |
| spots | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | skipped (out of time) | 0 s |

People talked to: 13 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / opening: typical 27 ms, slowest 10582 ms, 3 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 7868 ms, 2 frames over 250 ms
- iphone / opening: typical 45 ms, slowest 7406 ms, 1 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 5655 ms, 5 frames over 250 ms
- iphone / opening: typical 26 ms, slowest 5193 ms, 2 frames over 250 ms

Button response time (tap to something changing on screen): median 141 ms, slowest 650 ms over 21 taps.

## Vision pass

A vision model (claude-sonnet-5-5) looked at 87 screenshots for about $0.79 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
