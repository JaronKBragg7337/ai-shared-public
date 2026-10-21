# The Cosmos playtest report

Run: 2026-10-08 16:47 (local)  |  Build under test: `714b42a01a8aa6cad4f1`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

**How to read this:** items titled "Stuck while walking to ..." come from the bot's own steering (its path planner, run-ups and jumps). Treat them as bot-only unless a human also gets stuck at that spot. Black boot and crash-blackout frames that carry a caption are deliberate.

- **iPhone 15 (WebKit, touch)**: 16.8 minutes, 63 screenshots, 10 distinct problems
- **Desktop (Chromium, keyboard + mouse)**: 9.5 minutes, 48 screenshots, 5 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)
- Desktop (Chromium, keyboard + mouse): [session video](videos-desktop/<email>)

## Short version

16 distinct problems found: 0 blockers, 0 serious, 16 smaller.

- **Could not walk to Arrival guide** (Annoying)
- **Could not walk to Supply clerk** (Annoying)
- **Could not walk to Food trader** (Annoying)
- **Could not walk to Salvage trader** (Annoying)
- **A Dig tap in the opening made no cut** (Annoying, seen 8 times)

## Problems, worst first

### 1. Could not walk to Arrival guide

- **How bad:** Annoying (score 72)
- **Where:** walking the port and talking to people, first at 10:28 into the run, on iPhone (WebKit)
- **What happened:** gave up after 120s; last distance 1000000000 m
- **What the vision model saw:** {"description": "A first-person view of a flat, empty sandy plain at the Skyward Launch Complex on Earth, with a HUD panel at top-left showing location, a hauling cart readout and a quest hint, plus a
- **Screenshot:** [056-tour-PROBLEM-cannot-reach.jpg](shots-iphone/056-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Arrival guide](shots-iphone/056-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide

### 2. Could not walk to Supply clerk

- **How bad:** Annoying (score 72)
- **Where:** walking the port and talking to people, first at 12:28 into the run, on iPhone (WebKit)
- **What happened:** gave up after 120s; last distance 1000000000 m
- **What the vision model saw:** {"description": "A first-person view on a flat, empty sand plain under a blue sky at the Skyward Launch Complex on Earth, with a top-left HUD showing location, coordinates, cart load and a NEXT object
- **Screenshot:** [057-tour-PROBLEM-cannot-reach.jpg](shots-iphone/057-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Supply clerk](shots-iphone/057-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide
  1. go talk to Supply clerk
  1. walk to Supply clerk

### 3. Could not walk to Food trader

- **How bad:** Annoying (score 72)
- **Where:** walking the port and talking to people, first at 14:28 into the run, on iPhone (WebKit)
- **What happened:** gave up after 120s; last distance 1000000000 m
- **What the vision model saw:** A first-person view on a flat, empty sand plain at the Skyward Launch Complex under a blue sky with clouds, with a HUD panel at top-left showing location, objective text and currency, a Settings button, a virtual joystick, World/crew and Controls buttons, and an orange arrow marker at the right edge. Flagged: The bot's last action was 'walk to Food trader', but no trader, buildings, people, ships or any other objects are visible. The terrain is a featureless flat plain out to the horizon, so the world looks empty or not yet loaded.; The objective text is a long, dense block of small monospace text. The NEXT line is hard to read and repeats 'the Skyward Launch Complex' awkwardly. The HUD panel covers a large part of the upper-left sky.; The ground texture is blurry and low-detail, with no visible tiling or detail, so it reads as a flat gray-beige fill. A faint hard line is visible at the horizon.
- **Screenshot:** [058-tour-PROBLEM-cannot-reach.jpg](shots-iphone/058-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Food trader](shots-iphone/058-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide
  1. go talk to Supply clerk
  1. walk to Supply clerk
  1. go talk to Food trader
  1. walk to Food trader

### 4. Could not walk to Salvage trader

- **How bad:** Annoying (score 72)
- **Where:** walking the port and talking to people, first at 16:29 into the run, on iPhone (WebKit)
- **What happened:** gave up after 120s; last distance 1000000000 m
- **What the vision model saw:** {"description": "A mobile first-person view of a flat, empty sand plain under a blue sky at the Skyward Launch Complex on Earth, with a quest/info panel at top left, a Settings button at top right, a 
- **Screenshot:** [059-tour-PROBLEM-cannot-reach.jpg](shots-iphone/059-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Salvage trader](shots-iphone/059-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. go talk to Arrival guide
  1. walk to Arrival guide
  1. go talk to Supply clerk
  1. walk to Supply clerk
  1. go talk to Food trader
  1. walk to Food trader
  1. go talk to Salvage trader
  1. walk to Salvage trader

### 5. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 8 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:33 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** cuts stayed 4 after tapping "Dig (E)"
- **What the vision model saw:** {"description": "A first-person view on a dark grassy ground in the opening scene, with two pinkish rocks, a large dark building or crate on the left, a red angled panel in the center, and a fenced ed
- **Later hits:** 06:34 cuts stayed 4 after tapping "Dig (E)" / 06:37 cuts stayed 4 after tapping "Dig (E)"
- **Screenshot:** [035-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/035-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/035-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. REFRESH (mid-dig)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. tap #opening-action (opening action)

### 6. Buttons overlap:  "✕" overlaps  "Hear the faction leader of h" by 46%

- **How bad:** Annoying (score 66)
- **Where:** opening the Settings / Account / World / Controls panels, first at 08:26 into the run, on iPhone (WebKit)
- **What happened:**  "✕" overlaps  "Hear the faction leader of h" by 46% (World / crew scrolled, iphone)
- **What the vision model saw:** On an iPhone, the World / crew panel is open over the Skyward Launch Complex scene. It shows a name field, boarding options, the player's fleet, ship purchase buttons and faction join buttons. Flagged: The faction list is cut off at the bottom of the screen. The 'Join corsairs' button is partly clipped by the panel edge, so the panel needs scrolling and nothing indicates that.; The panel covers almost the whole viewport, leaving the 3D world mostly hidden and dimmed. This is probably expected for a modal.
- **Screenshot:** [053-panels-PROBLEM-overlap.jpg](shots-iphone/053-panels-PROBLEM-overlap.jpg)

  ![Buttons overlap:  "✕" overlaps  "Hear th](shots-iphone/053-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-view (settings switch #set-view)
  1. tap #set-tool (settings switch #set-tool)
  1. tap #set-voice-mute (toggle #set-voice-mute)
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)

### 7. Looks wrong in the screenshot: Entire viewport is solid black with no caption, loading text, title, or Skip intro button. The bot's last acti

- **How bad:** Annoying (score 63)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 08:16 into the run, on iPhone (WebKit)
- **What happened:** Whole screen (the vision model's description of the screen: The screenshot is a completely black frame with no visible text, caption, title, buttons, or any 3D world content.)
- **Screenshot:** [044-opening-PROBLEM-console-warning.jpg](shots-iphone/044-opening-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: Entire vi](shots-iphone/044-opening-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening finished

### 8. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 18 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:15 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** a single frame took 3672 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** {"description": "A dark first-person view of a ship's observation deck with a ceiling grid, railing and windows showing an orange Mars and docked ships, with a control hint at the top and a subtitle f
- **Later hits:** 05:44 a single frame took 4307 ms (typical 27 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 06:02 a single frame took 1548 ms (typical 26 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 9. Frame-time spike during "tour"

- **How bad:** Annoying (score 62)
- **Where:** walking the port and talking to people, first at 16:38 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 3781 ms (typical 15 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** {"description": "A mobile first-person view of an empty flat tan desert plain under a blue sky with wispy clouds, with a HUD panel at top-left showing location (Earth, Skyward Launch Complex), hauling
- **Screenshot:** [062-tour-PROBLEM-frame-spike.jpg](shots-iphone/062-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/062-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to Supply clerk
  1. go talk to Food trader
  1. walk to Food trader
  1. go talk to Salvage trader
  1. walk to Salvage trader
  1. REFRESH (refresh after the port tour)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 10. Looks wrong in the screenshot: The Settings panel is cut off at the bottom. The 'View' label and a button next to it are clipped by the scree

- **How bad:** Minor (score 49)
- **Where:** opening the Settings / Account / World / Controls panels, first at 08:20 into the run, on iPhone (WebKit)
- **What happened:** bottom of the Settings panel, around y=810 (the vision model's description of the screen: On an iPhone in portrait, the game shows a Skyward Launch Complex scene with a metal ship hull and grass. A top-left HUD panel lists location, cart weight and a quest hint, and the Settings panel is open over the lower half with account sign-in fields and a Start fresh button.)
- **Screenshot:** [047-panels-panel-Settings.jpg](shots-iphone/047-panels-panel-Settings.jpg)

  ![Looks wrong in the screenshot: The Setti](shots-iphone/047-panels-panel-Settings.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-settings (open Settings)

### 11. Looks wrong in the screenshot: The bot's last action was 'walk to Food trader', but no trader, buildings, people, ships or any other objects 

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 14:28 into the run, on iPhone (WebKit)
- **What happened:** Center and lower viewport, the whole ground area (the vision model's description of the screen: A first-person view on a flat, empty sand plain at the Skyward Launch Complex under a blue sky with clouds, with a HUD panel at top-left showing location, objective text and currency, a Settings button, a virtual joystick, World/crew and Controls buttons, and an orange arrow marker at the right edge.)
- **Screenshot:** [058-tour-PROBLEM-cannot-reach.jpg](shots-iphone/058-tour-PROBLEM-cannot-reach.jpg)

  ![Looks wrong in the screenshot: The bot's](shots-iphone/058-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to Food trader

### 12. Looks wrong in the screenshot: The bot was walking to the Salvage trader, but no trader, buildings, people, ships or any other objects are vi

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 16:29 into the run, on iPhone (WebKit)
- **What happened:** Center and lower viewport, the whole ground area (the vision model's description of the screen: A first-person view on a flat sandy plain at the Skyward Launch Complex on Earth, with a sky above, a HUD panel at top-left showing location, a hauling cart bar and a quest hint, plus Settings, World / crew and Controls buttons and an orange arrow marker on the right.)
- **Screenshot:** [061-tour-before-refresh.jpg](shots-iphone/061-tour-before-refresh.jpg)

  ![Looks wrong in the screenshot: The bot w](shots-iphone/061-tour-before-refresh.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to Salvage trader

### 13. Looks wrong in the screenshot: The world looks empty. The Skyward Launch Complex location shows only a flat featureless sand plain with no bu

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 16:46 into the run, on iPhone (WebKit)
- **What happened:** Main 3D viewport, the lower two-thirds of the screen (the vision model's description of the screen: A first-person view on a flat, empty sand plain under a blue sky with thin clouds, with a translucent HUD panel at top-left showing location, hauling cart, tool and a NEXT objective, plus Settings, World / crew and Controls buttons.)
- **Screenshot:** [063-tour-after-refresh.jpg](shots-iphone/063-tour-after-refresh.jpg)

  ![Looks wrong in the screenshot: The world](shots-iphone/063-tour-after-refresh.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. refresh check: moved 0.0 m, marks 10000 -> 10000, aboard false -> false

### 14. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42), happened 2 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:37 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** shown in opening-caption while the bot was: 03:35 [opening] walk to down the gangway
- **What the vision model saw:** A very dark first-person view of the Mars port at night, with a lit 'ARRIVALS' sign and low buildings in the distance, a hint at the top, a 'Skip intro' button at top right, and a Steward caption at the bottom. Flagged: The scene is extremely dark and low contrast. The ground, sky and buildings are barely visible, and the amber lights the hint says to follow are hard to see, so the path is difficult to follow.; The hint text at top left is very small and thin on a dark background, which makes it hard to read on a phone.
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

### 15. Game said: "Shared world disconnected. Reconnecting…"

- **How bad:** Minor (score 42)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 07:25 into the run, on desktop (Chromium)
- **What happened:** shown in opening-caption while the bot was: 07:25 [opening] websocket closed (the bot refreshed the page)
- **What the vision model saw:** {"description": "A third-person view of a green, grassy Mars-port landscape in the opening phase: a small grey capsule or hatch sits in a dug-out crater in the foreground, with rocks and a crashed red
- **Screenshot:** [034-opening-PROBLEM-refusal-message.jpg](shots-desktop/034-opening-PROBLEM-refusal-message.jpg)

  ![Game said: "Shared world disconnected. R](shots-desktop/034-opening-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to the crate
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. REFRESH (mid-dig)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed (the bot refreshed the page)

### Console warnings (1 kinds)

- THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed. (x3)

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 484 s |
| opening the Settings / Account / World / Controls panels | done | 9 s |
| walking the port and talking to people | done | 480 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| boarding the ship, taking a seat and flying a course | skipped (out of time) | 0 s |
| getting into and driving the survey rover | skipped (out of time) | 0 s |
| spots | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | skipped (out of time) | 0 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

### Desktop (Chromium, keyboard + mouse)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 553 s |
| opening the Settings / Account / World / Controls panels | skipped (out of time) | 0 s |
| walking the port and talking to people | skipped (out of time) | 0 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | skipped (out of time) | 0 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- desktop / opening: typical 17 ms, slowest 8858 ms, 3 frames over 250 ms
- desktop / opening: typical 4 ms, slowest 8325 ms, 4 frames over 250 ms
- desktop / opening: typical 4 ms, slowest 7912 ms, 3 frames over 250 ms
- desktop / opening: typical 4 ms, slowest 7808 ms, 3 frames over 250 ms
- iphone / opening: typical 27 ms, slowest 6896 ms, 3 frames over 250 ms

Button response time (tap to something changing on screen): median 107 ms, slowest 113 ms over 4 taps.

## Vision pass

A vision model (claude-sonnet-5-5) looked at 88 screenshots for about $0.90 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
