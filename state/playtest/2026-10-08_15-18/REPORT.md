# The Cosmos playtest report

Run: 2026-10-08 15:18 (local)  |  Build under test: `b1aaba9baac2a41dfaf6`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

**How to read this:** items titled "Stuck while walking to ..." come from the bot's own steering (its path planner, run-ups and jumps). Treat them as bot-only unless a human also gets stuck at that spot. Black boot and crash-blackout frames that carry a caption are deliberate.

- **iPhone 15 (WebKit, touch)**: 27.3 minutes, 71 screenshots, 17 distinct problems
- **Desktop (Chromium, keyboard + mouse)**: 9 minutes, 47 screenshots, 5 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)
- Desktop (Chromium, keyboard + mouse): [session video](videos-desktop/<email>)

## Short version

25 distinct problems found: 3 blockers, 1 serious, 21 smaller.

- **Page error (uncaught exception)** (BLOCKER, seen 70 times)
- **Page error (uncaught exception)** (BLOCKER, seen 5 times)
- **Page error (uncaught exception)** (BLOCKER)
- **Nothing changed for 60+ seconds (same message, same place)** (Serious, seen 16 times)
- **Could not walk to Arrival guide** (Annoying)

## Problems, worst first

### 1. Page error (uncaught exception)

- **How bad:** BLOCKER (score 95), happened 70 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 08:53 into the run, on desktop (Chromium)
- **What happened:** TypeError: Cannot read properties of undefined (reading 'id') |     at MultiplayerView.shipPose (https://www.heartbeatobservatory.com/games/the-cosmos/src/world-state/multiplayerView.js?v=b1aaba9baac2a41dfaf6:168:95) |     at MultiplayerView.updateBodies (https://www.heartbeatobservatory.com/games/the-cosmos/src/world-state/multiplayerView.js?v=b1aaba9baac2a41dfaf6:255:59) |     at MultiplayerView
- **What the vision model saw:** {"description": "A very dark first-person cockpit view on Mars (Valles Marineris) at sunset or sunrise, with a faint sun glow on the horizon, a diagonal strut on the right, and a dim HUD with coordina
- **Later hits:** 08:53 TypeError: Cannot read properties of undefined (reading 'id') |     at MultiplayerView.shipPose (https://www.heartbeatobservatory.com/games/the-cosmos/src/world-state/multiplayerView.js?v=b1aaba / 08:53 TypeError: Cannot read properties of undefined (reading 'id') |     at MultiplayerView.shipPose (https://www.heartbeatobservatory.com/games/the-cosmos/src/world-state/multiplayerView.js?v=b1aaba
- **Screenshot:** [045-opening-PROBLEM-page-error.jpg](shots-desktop/045-opening-PROBLEM-page-error.jpg)

  ![Page error (uncaught exception)](shots-desktop/045-opening-PROBLEM-page-error.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. opening stage 4 -> 5 (A vehicle is approaching.)
  1. walk to the rescue vehicle
  1. tap #opening-action (opening action)
  1. opening stage 5 -> 6 (PruittPruitt, Homeguard. We saw you come down. I would say welcome home, but there is not much home built yet.)
  1. REFRESH (mid-ride)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 2. Page error (uncaught exception)

- **How bad:** BLOCKER (score 95), happened 5 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 08:30 into the run, on iPhone (WebKit)
- **What happened:** TypeError: undefined is not an object (evaluating 's.id') |     at shipPose (https://www.heartbeatobservatory.com/games/the-cosmos/src/world-state/multiplayerView.js?v=b1aaba9baac2a41dfaf6:168:94) |     at updateBodies (https://www.heartbeatobservatory.com/games/the-cosmos/src/world-state/multiplayerView.js?v=b1aaba9baac2a41dfaf6:255:67) |     at tick (https://www.heartbeatobservatory.com/games/th
- **What the vision model saw:** The screenshot is a completely black frame with no visible text, caption, title, buttons, or 3D scene content. Flagged: The whole viewport is black. There is no caption, title, loading text, Skip intro button, HUD, or world rendering. The bot reported 'opening finished', so the game world should be showing, and this is not one of the deliberate blackout frames, which carry a caption.
- **Later hits:** 08:30 TypeError: undefined is not an object (evaluating 's.id') |     at shipPose (https://www.heartbeatobservatory.com/games/the-cosmos/src/world-state/multiplayerView.js?v=b1aaba9baac2a41dfaf6:168:9 / 25:21 TypeError: undefined is not an object (evaluating 's.id') |     at unknown (https://www.heartbeatobservatory.com/games/the-cosmos/src/world-state/multiplayerView.js:168:94)
- **Screenshot:** [047-opening-PROBLEM-page-error.jpg](shots-iphone/047-opening-PROBLEM-page-error.jpg)

  ![Page error (uncaught exception)](shots-iphone/047-opening-PROBLEM-page-error.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening stage 4 -> 5 (A vehicle is approaching.)
  1. walk to the rescue vehicle
  1. tap #opening-action (opening action)
  1. opening stage 5 -> 6 (PruittPruitt, Homeguard. We saw you come down. I would say welcome home, but there is not much home built yet.)
  1. REFRESH (mid-ride)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening finished

### 3. Page error (uncaught exception)

- **How bad:** BLOCKER (score 95)
- **Where:** walking the port and talking to people, first at 25:21 into the run, on iPhone (WebKit)
- **What happened:** Unhandled Promise Rejection: TypeError: null is not an object (evaluating 'view.ship') |     at RemoteCrew (https://www.heartbeatobservatory.com/games/the-cosmos/src/world-state/remoteCrew.js?v=b1aaba9baac2a41dfaf6:9:31) |     at unknown (https://www.heartbeatobservatory.com/games/the-cosmos/src/main.js?v=b1aaba9baac2a41dfaf6:481:24)
- **What the vision model saw:** A near-black boot screen shows the title "THE COSMOS", a three-line tagline, and a dim "Loading the port…" line, all centered.
- **Screenshot:** [070-tour-PROBLEM-page-error.jpg](shots-iphone/070-tour-PROBLEM-page-error.jpg)

  ![Page error (uncaught exception)](shots-iphone/070-tour-PROBLEM-page-error.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to Field kit trader
  1. go talk to Reception clerk
  1. walk to Reception clerk
  1. to the tower lift
  1. walk to tower door
  1. REFRESH (refresh after the port tour)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 4. Nothing changed for 60+ seconds (same message, same place)

- **How bad:** Serious (score 86), happened 16 times
- **Where:** walking the port and talking to people, first at 09:32 into the run, on iPhone (WebKit)
- **What happened:** in "tour": position {"x":1024105,"y":3050879,"z":-5498457}, button "", caption "", toast "Back in Mars space.", ship outside
- **What the vision model saw:** {"description": "A mobile first-person view on Mars (Valles Marineris) looking at a large, blown-out bright sun glow over a flat, dark terrain horizon. The HUD shows coordinates, a hauling cart readou
- **Later hits:** 10:33 in "tour": position {"x":1024105,"y":3050879,"z":-5498457}, button "", caption "", toast "Back in Mars space.", ship outside / 11:33 in "tour": position {"x":1024105,"y":3050879,"z":-5498457}, button "", caption "", toast "Back in Mars space.", ship outside
- **Screenshot:** [059-tour-PROBLEM-stuck-state.jpg](shots-iphone/059-tour-PROBLEM-stuck-state.jpg)

  ![Nothing changed for 60+ seconds (same me](shots-iphone/059-tour-PROBLEM-stuck-state.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. mis-tap beside #btn-key-controls
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide

### 5. Could not walk to Arrival guide

- **How bad:** Annoying (score 72)
- **Where:** walking the port and talking to people, first at 10:43 into the run, on iPhone (WebKit)
- **What happened:** gave up after 120s; last distance 1000000000 m
- **What the vision model saw:** {"description": "A first-person view on Mars in Valles Marineris showing a HUD with coordinates, a hauling cart readout, and a Shovel tool. A very bright, blown-out sun glare fills the middle of the v
- **Screenshot:** [060-tour-PROBLEM-cannot-reach.jpg](shots-iphone/060-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Arrival guide](shots-iphone/060-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. mis-tap beside #btn-key-controls
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide

### 6. Could not walk to Supply clerk

- **How bad:** Annoying (score 72)
- **Where:** walking the port and talking to people, first at 12:44 into the run, on iPhone (WebKit)
- **What happened:** gave up after 120s; last distance 1000000000 m
- **What the vision model saw:** {"description": "A first-person view on Mars (Valles Marineris) at a low sun glare over a flat, dim ground, with a HUD showing location, hauling cart, tool, currency, a 'Back in Mars space.' toast, a 
- **Screenshot:** [061-tour-PROBLEM-cannot-reach.jpg](shots-iphone/061-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Supply clerk](shots-iphone/061-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. mis-tap beside #btn-key-controls
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide
  1. go talk to Supply clerk
  1. walk to Supply clerk

### 7. Could not walk to Food trader

- **How bad:** Annoying (score 72)
- **Where:** walking the port and talking to people, first at 14:44 into the run, on iPhone (WebKit)
- **What happened:** gave up after 120s; last distance 1000000000 m
- **What the vision model saw:** {"description": "A mobile first-person view on Mars (Valles Marineris) shows a very bright, blown-out sun glare over a flat dark terrain horizon, with a HUD at top-left (coordinates, hauling cart 0.0/
- **Screenshot:** [062-tour-PROBLEM-cannot-reach.jpg](shots-iphone/062-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Food trader](shots-iphone/062-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide
  1. go talk to Supply clerk
  1. walk to Supply clerk
  1. go talk to Food trader
  1. walk to Food trader

### 8. Could not walk to Salvage trader

- **How bad:** Annoying (score 72)
- **Where:** walking the port and talking to people, first at 16:44 into the run, on iPhone (WebKit)
- **What happened:** gave up after 120s; last distance 1000000000 m
- **What the vision model saw:** {"description": "A mobile first-person view on Mars in Valles Marineris shows a very bright, blown-out sun glowing over a dark, flat horizon, with a HUD at top-left (location, hauling cart, tool, curr
- **Screenshot:** [063-tour-PROBLEM-cannot-reach.jpg](shots-iphone/063-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Salvage trader](shots-iphone/063-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. go talk to Arrival guide
  1. walk to Arrival guide
  1. go talk to Supply clerk
  1. walk to Supply clerk
  1. go talk to Food trader
  1. walk to Food trader
  1. go talk to Salvage trader
  1. walk to Salvage trader

### 9. Could not walk to Water trader

- **How bad:** Annoying (score 72)
- **Where:** walking the port and talking to people, first at 18:44 into the run, on iPhone (WebKit)
- **What happened:** gave up after 120s; last distance 1000000000 m
- **What the vision model saw:** {"description": "A mobile first-person view on Mars (Valles Marineris) looking toward a very bright, blown-out sun glare over a flat dark terrain, with a HUD at top-left showing coordinates, a hauling
- **Screenshot:** [064-tour-PROBLEM-cannot-reach.jpg](shots-iphone/064-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Water trader](shots-iphone/064-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. go talk to Supply clerk
  1. walk to Supply clerk
  1. go talk to Food trader
  1. walk to Food trader
  1. go talk to Salvage trader
  1. walk to Salvage trader
  1. go talk to Water trader
  1. walk to Water trader

### 10. Could not walk to Field kit trader

- **How bad:** Annoying (score 72)
- **Where:** walking the port and talking to people, first at 20:44 into the run, on iPhone (WebKit)
- **What happened:** gave up after 120s; last distance 1000000000 m
- **What the vision model saw:** {"description": "A mobile first-person view on Mars (Valles Marineris) shows a very bright sun glare low on the horizon above flat, dim terrain, with a HUD at top left, a Settings button at top right,
- **Screenshot:** [065-tour-PROBLEM-cannot-reach.jpg](shots-iphone/065-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Field kit trader](shots-iphone/065-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. go talk to Food trader
  1. walk to Food trader
  1. go talk to Salvage trader
  1. walk to Salvage trader
  1. go talk to Water trader
  1. walk to Water trader
  1. go talk to Field kit trader
  1. walk to Field kit trader

### 11. Could not walk to Reception clerk

- **How bad:** Annoying (score 72)
- **Where:** walking the port and talking to people, first at 22:44 into the run, on iPhone (WebKit)
- **What happened:** gave up after 120s; last distance 1000000000 m
- **What the vision model saw:** {"description": "A mobile first-person view on Mars (Valles Marineris) showing a very large, blown-out sun glare over a flat, dark terrain horizon, with a HUD at top-left (coordinates, hauling cart, s
- **Screenshot:** [066-tour-PROBLEM-cannot-reach.jpg](shots-iphone/066-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Reception clerk](shots-iphone/066-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. go talk to Salvage trader
  1. walk to Salvage trader
  1. go talk to Water trader
  1. walk to Water trader
  1. go talk to Field kit trader
  1. walk to Field kit trader
  1. go talk to Reception clerk
  1. walk to Reception clerk

### 12. Could not walk to tower door

- **How bad:** Annoying (score 72)
- **Where:** walking the port and talking to people, first at 25:14 into the run, on iPhone (WebKit)
- **What happened:** gave up after 150s; last distance 1000000000 m
- **What the vision model saw:** {"description": "A mobile first-person view on Mars (Valles Marineris) shows a large, blown-out sun glare over a flat dark terrain horizon, with a HUD at top left, a Settings button, a 'Back in Mars s
- **Screenshot:** [067-tour-PROBLEM-cannot-reach.jpg](shots-iphone/067-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to tower door](shots-iphone/067-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. go talk to Water trader
  1. walk to Water trader
  1. go talk to Field kit trader
  1. walk to Field kit trader
  1. go talk to Reception clerk
  1. walk to Reception clerk
  1. to the tower lift
  1. walk to tower door

### 13. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 5 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:34 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** cuts stayed 4 after tapping "Dig (E)"
- **What the vision model saw:** {"description": "A dark, blurry green ground fills the screen with a single low-poly tan rock or boulder near the top right, an instruction at the top left reading 'Closer to the crate, then Dig.', a 
- **Later hits:** 06:38 cuts stayed 4 after tapping "Dig (E)" / 06:48 cuts stayed 8 after tapping "Dig (E)"
- **Screenshot:** [036-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/036-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/036-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. REFRESH (mid-dig)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. tap #opening-action (opening action)

### 14. Buttons overlap:  "✕" overlaps  "Hear the faction leader of h" by 46%

- **How bad:** Annoying (score 66)
- **Where:** opening the Settings / Account / World / Controls panels, first at 08:41 into the run, on iPhone (WebKit)
- **What happened:**  "✕" overlaps  "Hear the faction leader of h" by 46% (World / crew scrolled, iphone)
- **What the vision model saw:** A mobile screenshot of the Mars game with the 'World / crew' panel open over the 3D view, showing a name field, boarding controls, the fleet list, shipyard purchase buttons and faction join buttons. Flagged: The faction button list runs off the bottom of the viewport. The 'Join corsairs' button is partly cut off at the panel's bottom edge. This is probably just a scrollable panel, but there is no visible scroll cue.; The top HUD readout is partly covered by the panel. A line of text below the coordinates is hidden behind the panel's top edge and is unreadable, and the gravity line shows '— · 3.72 m/s²' with a dash placeholder.; The panel covers almost the whole screen, so the world view and game controls are hidden. Only a thin strip of terrain shows at the bottom edge.
- **Screenshot:** [056-panels-PROBLEM-overlap.jpg](shots-iphone/056-panels-PROBLEM-overlap.jpg)

  ![Buttons overlap:  "✕" overlaps  "Hear th](shots-iphone/056-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-tool (settings switch #set-tool)
  1. tap #set-voice-mute (toggle #set-voice-mute)
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. mis-tap beside #purse
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)

### 15. Looks wrong in the screenshot: The whole viewport is black. There is no caption, title, loading text, Skip intro button, HUD, or scene. The b

- **How bad:** Annoying (score 63), happened 2 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 08:30 into the run, on iPhone (WebKit)
- **What happened:** Entire screen (the vision model's description of the screen: The screenshot is a completely black frame with no visible text, caption, title, buttons, or any 3D world content.)
- **Screenshot:** [046-opening-PROBLEM-console-warning.jpg](shots-iphone/046-opening-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: The whole](shots-iphone/046-opening-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening finished

### 16. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 17 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:15 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** a single frame took 3706 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** {"description": "A dark first-person view inside a ship's observation deck looking through a railing and window at a large orange-red planet-like curve and docked ships, with a small table in the fore
- **Later hits:** 05:44 a single frame took 4993 ms (typical 26 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 06:13 a single frame took 1631 ms (typical 16 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 17. Looks wrong in the screenshot: The whole frame is extremely dark, almost black. The world, horizon and cabin interior are barely visible, and

- **How bad:** Annoying (score 56)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 08:53 into the run, on desktop (Chromium)
- **What happened:** entire viewport (the vision model's description of the screen: A very dark, nearly black view from inside a cabin or cockpit shows a faint sunset glow on the horizon, a dim landscape, a diagonal strut on the right, and barely visible HUD panels, a Settings button, and 'World / crew' and 'Controls' buttons.)
- **Screenshot:** [044-opening-PROBLEM-console-warning.jpg](shots-desktop/044-opening-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: The whole](shots-desktop/044-opening-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening finished

### 18. Looks wrong in the screenshot: Walter, who is speaking, is not visible in the frame. The subtitle plays but only an empty floor and a table a

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:15 into the run, on iPhone (WebKit)
- **What happened:** center and lower half of the viewport, with the subtitle at the bottom (the vision model's description of the screen: A first-person view inside a dark ship observation lounge, looking through a railing and glass at a reddish planet-like curve and a docked ship, with a small table in the foreground, a tutorial hint at the top and a subtitle from Walter at the bottom.)
- **Screenshot:** [004-opening-opening.jpg](shots-iphone/004-opening-opening.jpg)

  ![Looks wrong in the screenshot: Walter, w](shots-iphone/004-opening-opening.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 19. Looks wrong in the screenshot: A pale lavender blocky object is cut off by the right screen edge and sits in the foreground. It could be a cl

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 02:13 into the run, on iPhone (WebKit)
- **What happened:** bottom right corner (the vision model's description of the screen: A first-person view inside a sci-fi boarding hall with a tiled ceiling, a diagonal ceiling beam, grey metal wall panels with yellow-black striped trim, a diamond-plate floor, and an orange lit doorway on the left.)
- **Screenshot:** [011-opening-opening.jpg](shots-iphone/011-opening-opening.jpg)

  ![Looks wrong in the screenshot: A pale la](shots-iphone/011-opening-opening.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. in the boarding hall, waiting for the gangway to come down

### 20. Looks wrong in the screenshot: The camera is pressed right up against a wall or door panel, so the view is almost entirely one surface. Only 

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 04:53 into the run, on iPhone (WebKit)
- **What happened:** Whole frame, the door panel fills nearly all of it (the vision model's description of the screen: A close-up, angled view of a gray sci-fi bulkhead door with a dark blue-trimmed monitor, a small vent plate, and a yellow-black hazard stripe edge, with the pilot's caption at the bottom and a Skip intro button at the top right.)
- **Screenshot:** [025-opening-opening.jpg](shots-iphone/025-opening-opening.jpg)

  ![Looks wrong in the screenshot: The camer](shots-iphone/025-opening-opening.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening stage 1 -> 2 (You are aboard the Kestrel. Walk to a window if you like.)

### 21. Looks wrong in the screenshot: The game is still on the boot/loading screen even though the bot's reload wait timed out after 120 seconds. Th

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 27:15 into the run, on iPhone (WebKit)
- **What happened:** Whole screen, 'Loading the port…' line (the vision model's description of the screen: A near-black boot screen shows the title "THE COSMOS", a tagline about your ship, crew and real-size worlds, and a dim "Loading the port…" line, all centered on the phone screen.)
- **Screenshot:** [071-tour-PROBLEM-harness.jpg](shots-iphone/071-tour-PROBLEM-harness.jpg)

  ![Looks wrong in the screenshot: The game ](shots-iphone/071-tour-PROBLEM-harness.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. SESSION ERROR page.waitForFunction: Timeout 120000ms exceeded.
    at Session.reload (C:\Users\lilli\AI-Shared\tools\playtester\lib\core.mjs:106:21)
    at async refreshCheck (C:\Users\lilli\AI-Shared\tools\playtester\play.mjs:81:54)
    at async runSession (C:\Users\lilli\AI-Shared\tools\playtester\play.mjs:115:57)
    at async file:///C:/Users/lilli/AI-Shared/tools/playtester/play.mjs:133:44

### 22. Looks wrong in the screenshot: The top-left info panel text is too dim to read (position/coordinates and a distance line), and the top-center

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 08:53 into the run, on desktop (Chromium)
- **What happened:** top-left panel and top-center (the vision model's description of the screen: A very dark, nearly black view from inside a cabin or cockpit shows a faint sunset glow on the horizon, a dim landscape, a diagonal strut on the right, and barely visible HUD panels, a Settings button, and 'World / crew' and 'Controls' buttons.)
- **Screenshot:** [044-opening-PROBLEM-console-warning.jpg](shots-desktop/044-opening-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: The top-l](shots-desktop/044-opening-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening finished

### 23. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42), happened 2 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:38 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** shown in opening-caption while the bot was: 03:38 [opening] opening stage 0 -> 1 (StewardWelcome to Mars. Follow the amber lights to the big Arrivals sign. If you reach a fuel tank, you have taken touri)
- **What the vision model saw:** A dusk-lit Mars spaceport scene on a phone: a concrete walkway leads toward low hangar buildings and a lit ARRIVALS sign, with an intro hint at the top, a Skip intro button at top right, and a Steward dialogue caption at the bottom. Flagged: The world is empty. No people, ships or other characters are visible anywhere on the walkway or near the Arrivals hall, which feels sparse for a port scene. It could be intentional at this early stage.; The amber lit posts that the steward and hint text tell the player to follow are barely visible. Only one faint post shows at the right edge and one dim light near the horizon, so the guidance is hard to see.
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

### 24. Bot harness error: page.waitForFunction: Timeout 120000ms exceeded.

- **How bad:** Small (score 10)
- **Where:** walking the port and talking to people, first at 27:15 into the run, on iPhone (WebKit)
- **What happened:** page.waitForFunction: Timeout 120000ms exceeded.
    at Session.reload (C:\Users\lilli\AI-Shared\tools\playtester\lib\core.mjs:106:21)
    at async refreshCheck (C:\Users\lilli\AI-Shared\tools\playtester\play.mjs:81:54)
    at async runSession (C:\Users\lilli\AI-Shared\tools\playtester\play.mjs:115:
- **What the vision model saw:** A near-black boot screen shows the title "THE COSMOS", a tagline about your ship, crew and real-size worlds, and a dim "Loading the port…" line, all centered on the phone screen. Flagged: The game is still on the boot/loading screen even though the bot's reload wait timed out after 120 seconds. The port never seems to have finished loading, so the game may be hung on load after reload. The screen itself looks like the normal boot frame, so this is inferred from the error log and not from any visible defect.
- **Screenshot:** [071-tour-PROBLEM-harness.jpg](shots-iphone/071-tour-PROBLEM-harness.jpg)

  ![Bot harness error: page.waitForFunction:](shots-iphone/071-tour-PROBLEM-harness.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. go talk to Reception clerk
  1. walk to Reception clerk
  1. to the tower lift
  1. walk to tower door
  1. REFRESH (refresh after the port tour)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. SESSION ERROR page.waitForFunction: Timeout 120000ms exceeded.
    at Session.reload (C:\Users\lilli\AI-Shared\tools\playtester\lib\core.mjs:106:21)
    at async refreshCheck (C:\Users\lilli\AI-Shared\tools\playtester\play.mjs:81:54)
    at async runSession (C:\Users\lilli\AI-Shared\tools\playtester\play.mjs:115:57)
    at async file:///C:/Users/lilli/AI-Shared/tools/playtester/play.mjs:133:44

### Console warnings (1 kinds)

- THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed. (x3)

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 497 s |
| opening the Settings / Account / World / Controls panels | done | 11 s |
| walking the port and talking to people | done | 991 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

### Desktop (Chromium, keyboard + mouse)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 521 s |
| opening the Settings / Account / World / Controls panels | skipped (out of time) | 0 s |
| walking the port and talking to people | skipped (out of time) | 0 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | skipped (out of time) | 0 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- desktop / opening: typical 4 ms, slowest 8016 ms, 3 frames over 250 ms
- desktop / opening: typical 4 ms, slowest 7433 ms, 2 frames over 250 ms
- desktop / opening: typical 4 ms, slowest 7333 ms, 2 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 7183 ms, 3 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 6746 ms, 3 frames over 250 ms

Button response time (tap to something changing on screen): median 740 ms, slowest 753 ms over 4 taps.

## Vision pass

A vision model (claude-sonnet-5-5) looked at 90 screenshots for about $0.91 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
