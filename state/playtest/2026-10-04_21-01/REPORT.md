# The Cosmos playtest report

Run: 2026-10-04 21:01 (local)  |  Build under test: `3fdae244e5eb2890e1b4`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 21.4 minutes, 144 screenshots, 19 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)

## Short version

29 distinct problems found: 0 blockers, 6 serious, 23 smaller.

- **Stuck while walking to Shift runner** (Serious)
- **Stuck while walking to Lookout at the glass** (Serious)
- **Stuck while walking to candidate Ada Chen 1** (Serious)
- **Stuck while walking to candidate Zuri Okafor 1** (Serious)
- **Stuck while walking to the ship ramp** (Serious)

## Problems, worst first

### 1. Stuck while walking to Shift runner

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 13:06 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -61,-41 (target -64,-41, 3 m away)
- **What the vision model saw:** {"description": "A mobile first-person view in the Mars Valles Marineris port shows a heavily blurred, close-up scene of pale walls, a yellow horizontal band, a dark window-like strip and a tall white
- **Screenshot:** [106-tour-PROBLEM-stuck-walking.jpg](shots-iphone/106-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Shift runner](shots-iphone/106-tour-PROBLEM-stuck-walking.jpg)

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
- **Where:** walking the port and talking to people, first at 14:22 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -59,-41 (target -56,-41, 4 m away)
- **What the vision model saw:** {"description": "A mobile first-person view in the Mars Valles Marineris port shows a HUD (location, regolith gravity, hauling cart, tool, currency) over a heavily blurred, close-up scene of white and
- **Screenshot:** [109-tour-PROBLEM-stuck-walking.jpg](shots-iphone/109-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Lookout at the gl](shots-iphone/109-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (4 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 3 legs
  1. not getting closer (4 m away), trying to get unstuck #6
  1. not getting closer (4 m away), trying to get unstuck #7
  1. not getting closer (4 m away), trying to get unstuck #8

### 3. Stuck while walking to candidate Ada Chen 1

- **How bad:** Serious (score 80)
- **Where:** hiring crew from the crew hall, first at 16:44 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -55,-34 (target -34,-66, 4 m away)
- **What the vision model saw:** {"description": "A mobile screenshot of the Mars Valles Marineris port area in The Cosmos showing a heavily blurred, beige and brown 3D view with a HUD panel at top left (coordinates, surface type, em
- **Screenshot:** [117-hire-PROBLEM-stuck-walking.jpg](shots-iphone/117-hire-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to candidate Ada Che](shots-iphone/117-hire-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (3 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 7 legs
  1. not getting closer (4 m away), trying to get unstuck #6
  1. not getting closer (4 m away), trying to get unstuck #7
  1. not getting closer (4 m away), trying to get unstuck #8

### 4. Stuck while walking to candidate Zuri Okafor 1

- **How bad:** Serious (score 80)
- **Where:** hiring crew from the crew hall, first at 18:07 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -55,-44 (target -32,-66, 11 m away)
- **What the vision model saw:** {"description": "A mobile Mars (Valles Marineris) view of the game with a HUD showing coordinates, a hauling cart bar, tool and currency text, Settings, World/crew and Controls buttons and a virtual j
- **Screenshot:** [121-hire-PROBLEM-stuck-walking.jpg](shots-iphone/121-hire-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to candidate Zuri Ok](shots-iphone/121-hire-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (7 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 4 legs
  1. not getting closer (11 m away), trying to get unstuck #6
  1. not getting closer (11 m away), trying to get unstuck #7
  1. not getting closer (11 m away), trying to get unstuck #8

### 5. Stuck while walking to the ship ramp

- **How bad:** Serious (score 80)
- **Where:** boarding the ship, taking a seat and flying a course, first at 21:25 into the run, on iPhone (WebKit)
- **What happened:** This is at the port perimeter kerb (a ~0.6 m high concrete wall ring at x = +/-103; walking steps up only 0.35 m, and a jump from a standstill against it goes straight up). no progress for 56s at port 102,-66 (target 214,-108, 8 m away)
- **What the vision model saw:** {"description": "A mobile screenshot of the Mars port in Valles Marineris shows a reddish regolith plain with a HUD panel at top-left (coordinates, airborne status, empty hauling cart, Shovel tool, 10
- **Screenshot:** [143-fly-PROBLEM-stuck-walking.jpg](shots-iphone/143-fly-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to the ship ramp](shots-iphone/143-fly-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (8 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 21 legs
  1. not getting closer (8 m away), trying to get unstuck #6
  1. not getting closer (8 m away), trying to get unstuck #7
  1. not getting closer (8 m away), trying to get unstuck #8

### 6. The Dig button never appeared on open ground

- **How bad:** Serious (score 78)
- **Where:** digging regolith and delivering it to the weigh bay, first at 18:52 into the run, on iPhone (WebKit)
- **What happened:** button text "", standing at {"x":-82.1,"y":0.1,"z":35}, looking down
- **What the vision model saw:** {"description": "A mobile screenshot of the Mars game (Valles Marineris) showing a HUD panel at top-left with location, coordinates, gravity, an empty hauling cart bar (0.0/1054 kg), tool Shovel and c
- **Screenshot:** [129-dig-PROBLEM-cannot-dig.jpg](shots-iphone/129-dig-PROBLEM-cannot-dig.jpg)

  ![The Dig button never appeared on open gr](shots-iphone/129-dig-PROBLEM-cannot-dig.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. no Dig button (button: ""); turning to find ground
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)
  1. tap #btn-action (action)

### 7. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 6 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:43 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 4 after tapping "Dig (E)"
- **What the vision model saw:** {"description": "A first-person view of a red Mars surface at the start of the opening, with a flat crate or lander platform carrying a dark device and a green-flagged pole, a
- **Later hits:** 06:45 cuts stayed 4 after tapping "Dig (E)" / 06:47 cuts stayed 4 after tapping "Dig (E)"
- **Screenshot:** [039-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/039-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/039-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. REFRESH (mid-dig)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. tap #opening-action (opening action)

### 8. Buttons overlap: #btn-close-settings "✕" overlaps #set-cinema "" by 33%

- **How bad:** Annoying (score 66)
- **Where:** opening the Settings / Account / World / Controls panels, first at 08:38 into the run, on iPhone (WebKit)
- **What happened:** #btn-close-settings "✕" overlaps #set-cinema "" by 33% (Settings scrolled, iphone)
- **What the vision model saw:** A mobile screenshot of The Cosmos on Mars (Valles Marineris) with the Settings panel open over the 3D scene, showing the guest sign-in form, a Start fresh button, a Ship account button, a View dropdown set to First, and a Digging tool selector. The HUD at top-left shows location, gravity, cart load and currency. Flagged: Faint text from an earlier notification or dialog ('Salvage crater and a rusty... hundred marks...') shows through the semi-transparent settings panel behind the header. It is hard to read and clutters the panel.; The Digging tool dropdown is cut off at the bottom of the screen. Its value is only partly visible (clipped 'Shovel'), and the panel needs scrolling to reach it.; The settings panel covers most of the screen, so the 3D world is mostly hidden. Only a thin strip of terrain and road is visible on the left edge, and the world looks mostly empty or dark on the right.
- **Screenshot:** [052-panels-PROBLEM-overlap.jpg](shots-iphone/052-panels-PROBLEM-overlap.jpg)

  ![Buttons overlap: #btn-close-settings "✕"](shots-iphone/052-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. opening stage 5 -> 6 (DevPort crew. We saw you come down. Everybody saw you come down. It was loud.)
  1. REFRESH (mid-ride)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening finished
  1. === phase panels starts
  1. tap #btn-settings (open Settings)

### 9. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 11 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:29 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 5062 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** {"description": "A very dark first-person view of a station observation deck with a ceiling grid, railing, a small table and a coin-operated telescope, with a Mars-like orange planet and a ship behind
- **Later hits:** 01:25 a single frame took 4228 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 01:37 a single frame took 6998 ms (typical 26 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [008-opening-PROBLEM-frame-spike.jpg](shots-iphone/008-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/008-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 10. Frame-time spike during "hire"

- **How bad:** Annoying (score 62), happened 3 times
- **Where:** hiring crew from the crew hall, first at 15:24 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 6475 ms (typical 38 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** {"description": "A first-person view on Mars (Valles Marineris) inside a metal hangar or cargo bay, facing a closed beige riveted double door with a small panel, with a HUD at top-left (coordinates, h
- **Later hits:** 15:36 a single frame took 860 ms (typical 35 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 16:53 a single frame took 908 ms (typical 34 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [113-hire-PROBLEM-frame-spike.jpg](shots-iphone/113-hire-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "hire"](shots-iphone/113-hire-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (refresh after the port tour)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. refresh check: moved 0.0 m, marks 10000 -> 10000, aboard false -> false
  1. === phase hire starts
  1. candidates: Jorge(Navigator), Sunita(Gunner (dorsal)), Walter(Gunner (ventral)), Zuri Okafor 1(Captain), Ada Chen 1(Pilot), Aoi Patel 1(Communications officer)
  1. walk to candidate Ada Chen 1
  1. route of 8 legs

### 11. Frame-time spike during "dig"

- **How bad:** Annoying (score 62)
- **Where:** digging regolith and delivering it to the weigh bay, first at 19:11 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 3597 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** {"description": "A first-person view on Mars (Valles Marineris) in the dig phase, showing a HUD with coordinates, an empty hauling cart and a shovel, a yellow-framed sign reading '1 TONNE RAW REGOLITH
- **Screenshot:** [135-dig-PROBLEM-frame-spike.jpg](shots-iphone/135-dig-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "dig"](shots-iphone/135-dig-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. dug 24 bites; cart 0.0/1054 -> 0.0/1054
  1. walk to the amber weigh bay
  1. route of 2 legs
  1. tap #quest-deliver (deliver the tonne)
  1. delivery: marks 10000 -> 10000
  1. REFRESH (refresh right after digging)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 12. Frame-time spike during "fly"

- **How bad:** Annoying (score 62)
- **Where:** boarding the ship, taking a seat and flying a course, first at 19:25 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 5530 ms (typical 40 ms); 6 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [138-fly-PROBLEM-frame-spike.jpg](shots-iphone/138-fly-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "fly"](shots-iphone/138-fly-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (refresh right after digging)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. refresh check: moved 0.0 m, marks 10000 -> 10000, aboard false -> false
  1. === phase fly starts
  1. ship type lifeboat; ship centre at port 214,-120; ramp foot 214,-108
  1. walk to the ship ramp
  1. route of 38 legs

### 13. Looks wrong in the screenshot: The 3D world is not rendered. The whole viewport is black or empty, with no Mars terrain, sky, ships, or peopl

- **How bad:** Annoying (score 56)
- **Where:** loading the page, first at 00:13 into the run, on iPhone (WebKit)
- **What happened:** Entire screen, from the top to just above the bottom buttons (the vision model's description of the screen: An almost entirely black phone-sized screen with only a small dark 'Walk (Q)' button and an empty dark rounded square button at the bottom, and no visible 3D world, HUD, or other content.)
- **Screenshot:** [002-start-PROBLEM-request-failed.jpg](shots-iphone/002-start-PROBLEM-request-failed.jpg)

  ![Looks wrong in the screenshot: The 3D wo](shots-iphone/002-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 14. Looks wrong in the screenshot: No start/play button or any interactive control is visible, so the player has no way to begin the game from th

- **How bad:** Annoying (score 56)
- **Where:** loading the page, first at 00:13 into the run, on iPhone (WebKit)
- **What happened:** Whole screen; the area below the tagline text is empty (the vision model's description of the screen: A nearly all-black mobile screen with a centered title 'THE COSMOS' and a small grey tagline reading 'Your ship. Your crew. Real worlds at their real size. Mars is only the first port.' There are no buttons, menus, or 3D scene visible.)
- **Screenshot:** [003-start-PROBLEM-request-failed.jpg](shots-iphone/003-start-PROBLEM-request-failed.jpg)

  ![Looks wrong in the screenshot: No start/](shots-iphone/003-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket closed

### 15. Looks wrong in the screenshot: The start screen has no start/play button or any other interactive control, so the player has no visible way t

- **How bad:** Annoying (score 56)
- **Where:** loading the page, first at 00:13 into the run, on iPhone (WebKit)
- **What happened:** Whole screen; the area below the tagline text is empty (the vision model's description of the screen: A nearly black mobile screen shows a centered title 'THE COSMOS' with a small grey tagline below it ('Your ship. Your crew. Real worlds at their real size. Mars is only the first port.'), and nothing else.)
- **Screenshot:** [004-start-PROBLEM-request-failed.jpg](shots-iphone/004-start-PROBLEM-request-failed.jpg)

  ![Looks wrong in the screenshot: The start](shots-iphone/004-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket closed

### 16. Looks wrong in the screenshot: The start screen has no visible start/play button or any other interactive control, so the player has no clear

- **How bad:** Annoying (score 56)
- **Where:** loading the page, first at 00:13 into the run, on iPhone (WebKit)
- **What happened:** Whole screen; the area below the tagline text is empty (the vision model's description of the screen: A nearly black mobile screen shows the centered title "THE COSMOS" with a tagline below it: "Your ship. Your crew. Real worlds at their real size. Mars is only the first port." There are no buttons, menus or 3D scene visible.)
- **Screenshot:** [005-start-PROBLEM-ws-closed.jpg](shots-iphone/005-start-PROBLEM-ws-closed.jpg)

  ![Looks wrong in the screenshot: The start](shots-iphone/005-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket closed

### 17. Server connection (websocket) closed

- **How bad:** Minor (score 50), happened 2 times
- **Where:** loading the page, first at 00:13 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **What the vision model saw:** A nearly black mobile screen shows the centered title "THE COSMOS" with a tagline below it: "Your ship. Your crew. Real worlds at their real size. Mars is only the first port." There are no buttons, menus or 3D scene visible. Flagged: The start screen has no visible start/play button or any other interactive control, so the player has no clear way to proceed. The test log also reports the websocket closed, which may mean the game failed to connect and the screen is stuck.; The screen is almost entirely black with no 3D world, starfield or background art, and no loading indicator or connection error message. It is unclear whether the game is loading, disconnected or hung.; The tagline text is small, low-contrast gray on near-black, which makes it hard to read on a phone. It also wraps awkwardly, leaving the orphan word "size." alone on its own line.
- **Later hits:** 01:13 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Screenshot:** [005-start-PROBLEM-ws-closed.jpg](shots-iphone/005-start-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/005-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed

### 18. Looks wrong in the screenshot: The button on the bottom right is an empty dark rounded square with no label or icon, so its purpose is unclea

- **How bad:** Minor (score 49)
- **Where:** loading the page, first at 00:13 into the run, on iPhone (WebKit)
- **What happened:** Bottom right corner, around x=354, y=804 (the vision model's description of the screen: An almost entirely black phone-sized screen with only a small dark 'Walk (Q)' button and an empty dark rounded square button at the bottom, and no visible 3D world, HUD, or other content.)
- **Screenshot:** [002-start-PROBLEM-request-failed.jpg](shots-iphone/002-start-PROBLEM-request-failed.jpg)

  ![Looks wrong in the screenshot: The butto](shots-iphone/002-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 19. Looks wrong in the screenshot: There is no loading indicator, title, or menu. The screen gives no sign of whether the game is still loading o

- **How bad:** Minor (score 49)
- **Where:** loading the page, first at 00:13 into the run, on iPhone (WebKit)
- **What happened:** Entire screen (the vision model's description of the screen: An almost entirely black phone-sized screen with only a small dark 'Walk (Q)' button and an empty dark rounded square button at the bottom, and no visible 3D world, HUD, or other content.)
- **Screenshot:** [002-start-PROBLEM-request-failed.jpg](shots-iphone/002-start-PROBLEM-request-failed.jpg)

  ![Looks wrong in the screenshot: There is ](shots-iphone/002-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 20. Looks wrong in the screenshot: The 3D world, stars, or Mars backdrop are absent; the screen is a flat black void behind the text, which could

- **How bad:** Minor (score 49)
- **Where:** loading the page, first at 00:13 into the run, on iPhone (WebKit)
- **What happened:** Entire background, above and below the centered text (the vision model's description of the screen: A nearly all-black mobile screen with a centered title 'THE COSMOS' and a small grey tagline reading 'Your ship. Your crew. Real worlds at their real size. Mars is only the first port.' There are no buttons, menus, or 3D scene visible.)
- **Screenshot:** [003-start-PROBLEM-request-failed.jpg](shots-iphone/003-start-PROBLEM-request-failed.jpg)

  ![Looks wrong in the screenshot: The 3D wo](shots-iphone/003-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket closed

### 21. Looks wrong in the screenshot: No 3D world, ship, or background is rendered behind the title. The screen is a flat black void, which may mean

- **How bad:** Minor (score 49)
- **Where:** loading the page, first at 00:13 into the run, on iPhone (WebKit)
- **What happened:** Entire viewport, above and below the centered text (the vision model's description of the screen: A nearly black mobile screen shows a centered title 'THE COSMOS' with a small grey tagline below it ('Your ship. Your crew. Real worlds at their real size. Mars is only the first port.'), and nothing else.)
- **Screenshot:** [004-start-PROBLEM-request-failed.jpg](shots-iphone/004-start-PROBLEM-request-failed.jpg)

  ![Looks wrong in the screenshot: No 3D wor](shots-iphone/004-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket closed

### 22. Looks wrong in the screenshot: The screen is almost entirely black with no 3D world, starfield or background art, and no loading indicator or

- **How bad:** Minor (score 49)
- **Where:** loading the page, first at 00:13 into the run, on iPhone (WebKit)
- **What happened:** Entire viewport outside the center text block (the vision model's description of the screen: A nearly black mobile screen shows the centered title "THE COSMOS" with a tagline below it: "Your ship. Your crew. Real worlds at their real size. Mars is only the first port." There are no buttons, menus or 3D scene visible.)
- **Screenshot:** [005-start-PROBLEM-ws-closed.jpg](shots-iphone/005-start-PROBLEM-ws-closed.jpg)

  ![Looks wrong in the screenshot: The scree](shots-iphone/005-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket closed

### 23. Looks wrong in the screenshot: The 3D world is not visible. The whole screen is black apart from the caption and button. This may be intentio

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 05:57 into the run, on iPhone (WebKit)
- **What happened:** Entire viewport, below the top caption row (the vision model's description of the screen: A nearly all-black mobile screen shows a small caption at the top left reading 'Impact. Hold on, the cabin is going dark.' and a 'Skip intro' button at the top right.)
- **Screenshot:** [032-opening-opening.jpg](shots-iphone/032-opening-opening.jpg)

  ![Looks wrong in the screenshot: The 3D wo](shots-iphone/032-opening-opening.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening stage 1 -> 2 (You are aboard the Kestrel. Walk to a window if you like.)

### 24. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:11 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/sunita.glb (Load request cancelled)
- **What the vision model saw:** {"description": "An almost entirely black phone-sized screen with only two dark rounded buttons at the bottom: one labelled \"Walk (Q)\" near the bottom center-left, and a second, empty, unlabelled bu
- **Screenshot:** [001-start-PROBLEM-request-failed.jpg](shots-iphone/001-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/001-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 25. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:11 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/walter.glb (Load request cancelled)
- **What the vision model saw:** An almost entirely black phone-sized screen with only a small dark 'Walk (Q)' button and an empty dark rounded square button at the bottom, and no visible 3D world, HUD, or other content. Flagged: The 3D world is not rendered. The whole viewport is black or empty, with no Mars terrain, sky, ships, or people.; The button on the bottom right is an empty dark rounded square with no label or icon, so its purpose is unclear. It may be a missing icon or an asset that has not loaded.; The 'Walk (Q)' label is small, low-contrast text on a dark button and is hard to read on a phone. It also shows a keyboard shortcut hint (Q), which does not apply to a touch device.; There is no loading indicator, title, or menu. The screen gives no sign of whether the game is still loading or has stalled after the websocket opened.
- **Screenshot:** [002-start-PROBLEM-request-failed.jpg](shots-iphone/002-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/002-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 26. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:11 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/aoi.glb (Load request cancelled)
- **What the vision model saw:** A nearly all-black mobile screen with a centered title 'THE COSMOS' and a small grey tagline reading 'Your ship. Your crew. Real worlds at their real size. Mars is only the first port.' There are no buttons, menus, or 3D scene visible. Flagged: No start/play button or any interactive control is visible, so the player has no way to begin the game from this screen. This is especially notable since the bot log shows the websocket closed.; The 3D world, stars, or Mars backdrop are absent; the screen is a flat black void behind the text, which could mean the scene failed to render or load.; The tagline is small, low-contrast grey on near-black, making it hard to read on a phone.; The tagline wraps awkwardly, leaving the single word 'size.' orphaned on its own line.
- **Screenshot:** [003-start-PROBLEM-request-failed.jpg](shots-iphone/003-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/003-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 27. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:11 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/ada.glb (Load request cancelled)
- **What the vision model saw:** A nearly black mobile screen shows a centered title 'THE COSMOS' with a small grey tagline below it ('Your ship. Your crew. Real worlds at their real size. Mars is only the first port.'), and nothing else. Flagged: The start screen has no start/play button or any other interactive control, so the player has no visible way to begin. The bot's last action was 'websocket closed', so the game may be stuck on this screen after a lost connection.; No 3D world, ship, or background is rendered behind the title. The screen is a flat black void, which may mean the scene did not load.; The tagline is small, low-contrast grey on near-black, which makes it hard to read on a phone. It also wraps awkwardly, leaving the single word 'size.' alone on its own line.
- **Screenshot:** [004-start-PROBLEM-request-failed.jpg](shots-iphone/004-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/004-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 28. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:53 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 03:53 [opening] opening stage 0 -> 1 (StewardWelcome to Mars. Follow the amber lights to the big Arrivals sign. If you reach a fuel tank, you have taken touri)
- **What the vision model saw:** A mobile opening scene of a Mars spaceport at dusk, showing a paved walkway leading toward a distant ARRIVALS sign and low buildings, with an instruction text and Skip intro button at the top and a Steward dialogue caption at the bottom. Flagged: The ground takes up a large part of the screen as a flat, nearly featureless gray surface with little detail, and only a faint seam line breaks it up. It looks sparse and low-resolution.; The 'amber lights' the steward mentions are barely visible. Only a faint lit post is seen at the right edge, and a tiny light near the sign. The player gets little visual guidance, so the dialogue does not match what is on screen.; The top-left instruction text is small and low-contrast against the dark sky, which makes it harder to read on a phone.; The dialogue text sits directly over the textured ground with no clear panel behind it. Contrast is acceptable but not strong.
- **Screenshot:** [022-opening-PROBLEM-refusal-message.jpg](shots-iphone/022-opening-PROBLEM-refusal-message.jpg)

  ![Game said: "Welcome to Mars. Follow the ](shots-iphone/022-opening-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to the boarding hall
  1. in the boarding hall, waiting for the gangway to come down
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. walk to down the gangway
  1. walk to down the gangway
  1. walk to down the gangway
  1. opening stage 0 -> 1 (StewardWelcome to Mars. Follow the amber lights to the big Arrivals sign. If you reach a fuel tank, you have taken touri)

### 29. Frame-time spike during "tour"

- **How bad:** Minor (score 38), happened 2 times
- **Where:** walking the port and talking to people, first at 08:58 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 1336 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** A mobile first-person view of a Martian landscape in Valles Marineris, showing a grey road with a yellow edge line, a distant port facility with buildings and a gantry, red dunes, and a hazy sky. The HUD shows location, coordinates, a hauling cart readout, the current tool, and the currency balance. A virtual joystick and the 'World / crew' and 'Controls' buttons are visible. Flagged: The road looks like a flat grey slab with a hard diagonal edge cutting across the red terrain. The yellow line runs at a steep diagonal, and the road surface has no texture detail. Because of this the road looks oddly tilted and disconnected from the ground.; Dark smudge-like shadow blobs sit on the terrain near the joystick and bottom-left. They have no visible source object and look like stray artifacts.; The virtual joystick overlaps the road and the terrain. Its thumb knob is off-center from the ring, which is probably just the current touch state. The faint ring has low contrast.
- **Later hits:** 15:12 a single frame took 3100 ms (typical 15 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [059-tour-PROBLEM-frame-spike.jpg](shots-iphone/059-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/059-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide
  1. route of 28 legs

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 487 s |
| opening the Settings / Account / World / Controls panels | done | 10 s |
| walking the port and talking to people | done | 376 s |
| hiring crew from the crew hall | done | 164 s |
| digging regolith and delivering it to the weigh bay | done | 50 s |
| boarding the ship, taking a seat and flying a course | done | 125 s |
| getting into and driving the survey rover | skipped (out of time) | 0 s |
| spots | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | skipped (out of time) | 0 s |

People talked to: 13 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / opening: typical 23 ms, slowest 10003 ms, 3 frames over 250 ms
- iphone / opening: typical 26 ms, slowest 6998 ms, 2 frames over 250 ms
- iphone / opening: typical 15 ms, slowest 6659 ms, 2 frames over 250 ms
- iphone / hire: typical 38 ms, slowest 6475 ms, 4 frames over 250 ms
- iphone / fly: typical 40 ms, slowest 5530 ms, 6 frames over 250 ms

Button response time (tap to something changing on screen): median 133 ms, slowest 931 ms over 23 taps.

## Vision pass

A vision model (claude-sonnet-5-5) looked at 90 screenshots for about $0.82 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
