# The Cosmos playtest report

Run: 2026-10-04 23:50 (local)  |  Build under test: `3fdae244e5eb2890e1b4`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 20.5 minutes, 156 screenshots, 17 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)

## Short version

22 distinct problems found: 0 blockers, 5 serious, 17 smaller.

- **Stuck while walking to Shift runner** (Serious)
- **Stuck while walking to Lookout at the glass** (Serious)
- **Stuck while walking to the amber weigh bay** (Serious)
- **Stuck while walking to the ship ramp** (Serious)
- **The Dig button never appeared on open ground** (Serious)

## Problems, worst first

### 1. Stuck while walking to Shift runner

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 12:53 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -61,-41 (target -64,-41, 3 m away)
- **What the vision model saw:** {"description": "A mobile screenshot of the Mars Valles Marineris port in The Cosmos. The 3D view is a heavily blurred, close-up wall of beige and dark surfaces with a white vertical strip. A HUD show
- **Screenshot:** [102-tour-PROBLEM-stuck-walking.jpg](shots-iphone/102-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Shift runner](shots-iphone/102-tour-PROBLEM-stuck-walking.jpg)

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
- **What the vision model saw:** {"description": "A mobile portrait view of the Mars game (Valles Marineris) showing a HUD with location, regolith, hauling cart and tool info at top-left, Settings at top-right, and World/crew, Contro
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

### 3. Stuck while walking to the amber weigh bay

- **How bad:** Serious (score 80)
- **Where:** digging regolith and delivering it to the weigh bay, first at 18:46 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -92,36 (target -83,25, 12 m away)
- **What the vision model saw:** {"description": "A mobile first-person view on Mars (Valles Marineris, on dust-worn landing concrete) where a large brown cylindrical pillar or pole fills the center of the screen against a dark brown
- **Screenshot:** [144-dig-PROBLEM-stuck-walking.jpg](shots-iphone/144-dig-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to the amber weigh b](shots-iphone/144-dig-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (4 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 3 legs
  1. not getting closer (12 m away), trying to get unstuck #6
  1. not getting closer (12 m away), trying to get unstuck #7
  1. not getting closer (12 m away), trying to get unstuck #8

### 4. Stuck while walking to the ship ramp

- **How bad:** Serious (score 80)
- **Where:** boarding the ship, taking a seat and flying a course, first at 20:30 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -77,36 (target 150,-8, 7 m away)
- **What the vision model saw:** {"description": "A first-person view on a Mars landing pad in Valles Marineris, with a HUD showing coordinates, cart weight and credits, while a large dark wall-like object fills the right side of the
- **Screenshot:** [155-fly-PROBLEM-stuck-walking.jpg](shots-iphone/155-fly-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to the ship ramp](shots-iphone/155-fly-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (9 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 30 legs
  1. not getting closer (7 m away), trying to get unstuck #6
  1. not getting closer (7 m away), trying to get unstuck #7
  1. not getting closer (7 m away), trying to get unstuck #8

### 5. The Dig button never appeared on open ground

- **How bad:** Serious (score 78)
- **Where:** digging regolith and delivering it to the weigh bay, first at 17:28 into the run, on iPhone (WebKit)
- **What happened:** button text "Drop", standing at {"x":-74.5,"y":0.7,"z":39.8}, looking down
- **Screenshot:** [139-dig-PROBLEM-cannot-dig.jpg](shots-iphone/139-dig-PROBLEM-cannot-dig.jpg)

  ![The Dig button never appeared on open gr](shots-iphone/139-dig-PROBLEM-cannot-dig.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-action (action)
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)
  1. no Dig button (button: ""); turning to find ground
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)

### 6. Same message repeated 4+ times in a minute: "Nothing in reach"

- **How bad:** Annoying (score 70), happened 4 times
- **Where:** digging regolith and delivering it to the weigh bay, first at 16:48 into the run, on iPhone (WebKit)
- **What happened:** The game keeps saying the same thing instead of moving on.
- **What the vision model saw:** {"description": "A mobile view of the Mars game (Valles Marineris) showing a HUD with location, an empty hauling cart (0.0 / 1054 kg), a Shovel tool, 8,720 marks and 2,180 cr, a 'Structural concrete w
- **Later hits:** 16:58 The game keeps saying the same thing instead of moving on. / 17:10 The game keeps saying the same thing instead of moving on.
- **Screenshot:** [126-dig-PROBLEM-repeating-message.jpg](shots-iphone/126-dig-PROBLEM-repeating-message.jpg)

  ![Same message repeated 4+ times in a minu](shots-iphone/126-dig-PROBLEM-repeating-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)

### 7. Same message repeated 4+ times in a minute: "Structural concrete will not cut."

- **How bad:** Annoying (score 70)
- **Where:** digging regolith and delivering it to the weigh bay, first at 16:58 into the run, on iPhone (WebKit)
- **What happened:** The game keeps saying the same thing instead of moving on.
- **What the vision model saw:** {"description": "A mobile first-person view of the Mars Valles Marineris landing area shows a HUD with coordinates, a hauling cart bar at 0/1054 kg, the Shovel tool, and a 'Nothing in reach' tag. A vi
- **Screenshot:** [131-dig-PROBLEM-repeating-message.jpg](shots-iphone/131-dig-PROBLEM-repeating-message.jpg)

  ![Same message repeated 4+ times in a minu](shots-iphone/131-dig-PROBLEM-repeating-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. mis-tap beside #btn-action

### 8. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 7 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:24 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 3 after tapping "Dig (E)"
- **What the vision model saw:** {"description": "A first-person view of a flat, dark red Mars-like surface under a purple-pink dusk sky, with two rounded rocks at the lower-left edge, a 'Skip intro' button at top right, a 'Nothing i
- **Later hits:** 06:49 cuts stayed 3 after tapping "Dig (E)" / 06:51 cuts stayed 3 after tapping "Dig (E)"
- **Screenshot:** [033-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/033-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/033-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to the cabin exit
  1. tap #opening-action (opening action)
  1. opening stage 3 -> 4 (Something lies beneath the collapsed dust.)
  1. walk to the crate
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)

### 9. Buttons overlap: #btn-close-settings "✕" overlaps #set-tool "Hand spade Shovel Excavator " by 77%

- **How bad:** Annoying (score 66)
- **Where:** opening the Settings / Account / World / Controls panels, first at 08:42 into the run, on iPhone (WebKit)
- **What happened:** #btn-close-settings "✕" overlaps #set-tool "Hand spade Shovel Excavator " by 77% (Settings scrolled, iphone)
- **What the vision model saw:** {"description":"On an iPhone-sized Mars scene (Valles Marineris), the Settings panel is open over the game. It shows guest account sign-in fields, a Start fresh button, a Ship account button, and View
- **Screenshot:** [048-panels-PROBLEM-overlap.jpg](shots-iphone/048-panels-PROBLEM-overlap.jpg)

  ![Buttons overlap: #btn-close-settings "✕"](shots-iphone/048-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. opening stage 5 -> 6 (DevPort crew. We saw you come down. Everybody saw you come down. It was loud.)
  1. REFRESH (mid-ride)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening finished
  1. === phase panels starts
  1. tap #btn-settings (open Settings)

### 10. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 10 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:31 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4968 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** {"description": "A dark, dimly lit 3D station concourse viewed in first person on a phone, showing a ceiling with panels, a railing in front of a large window with a red Mars-like planet and a ship be
- **Later hits:** 06:06 a single frame took 7318 ms (typical 36 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 06:09 a single frame took 1375 ms (typical 31 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [004-opening-PROBLEM-frame-spike.jpg](shots-iphone/004-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/004-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 11. Frame-time spike during "dig"

- **How bad:** Annoying (score 62)
- **Where:** digging regolith and delivering it to the weigh bay, first at 19:00 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 3555 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** {"description": "A mobile screenshot of the Mars (Valles Marineris) scene with a HUD at top-left showing coordinates, a hauling cart load of 29.4/1054 kg, the Shovel tool and currency, while the 3D vi
- **Screenshot:** [148-dig-PROBLEM-frame-spike.jpg](shots-iphone/148-dig-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "dig"](shots-iphone/148-dig-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. route of 3 legs
  1. not getting closer (12 m away), trying to get unstuck #6
  1. not getting closer (12 m away), trying to get unstuck #7
  1. not getting closer (12 m away), trying to get unstuck #8
  1. tap #btn-drop-all (drop all)
  1. REFRESH (refresh right after digging)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 12. Frame-time spike during "fly"

- **How bad:** Annoying (score 62)
- **Where:** boarding the ship, taking a seat and flying a course, first at 19:13 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 6388 ms (typical 48 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** {"description": "A first-person view on a Martian landing pad in Valles Marineris, showing concrete ground with footprints, a tall dark box-like structure, a pole, a large teal-lit panel on the left a
- **Screenshot:** [151-fly-PROBLEM-frame-spike.jpg](shots-iphone/151-fly-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "fly"](shots-iphone/151-fly-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (refresh right after digging)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. refresh check: moved 0.0 m, marks 8720 -> 8720, aboard false -> false
  1. === phase fly starts
  1. ship type lifeboat; ship centre at port 150,-20; ramp foot 150,-8
  1. walk to the ship ramp
  1. route of 32 legs

### 13. Looks wrong in the screenshot: No start/play button or any interactive control is visible on the start screen, so the player has nothing to t

- **How bad:** Annoying (score 56)
- **Where:** loading the page, first at 00:15 into the run, on iPhone (WebKit)
- **What happened:** Whole screen, below the tagline (the vision model's description of the screen: A mostly black mobile screen shows a centered title 'THE COSMOS' with a small grey tagline beneath it ('Your ship. Your crew. Real worlds at their real size. Mars is only the first port.'), and no buttons, 3D scene, or other UI.)
- **Screenshot:** [001-start-PROBLEM-ws-closed.jpg](shots-iphone/001-start-PROBLEM-ws-closed.jpg)

  ![Looks wrong in the screenshot: No start/](shots-iphone/001-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket closed

### 14. Looks wrong in the screenshot: The whole viewport is black. No 3D world, ship interior, window, HUD, controls or narration/subtitle text is v

- **How bad:** Annoying (score 56)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 05:54 into the run, on iPhone (WebKit)
- **What happened:** Entire screen except the top-right button (the vision model's description of the screen: A fully black mobile screen with only a small dark 'Skip intro' button in the top-right corner and nothing else rendered.)
- **Screenshot:** [028-opening-opening.jpg](shots-iphone/028-opening-opening.jpg)

  ![Looks wrong in the screenshot: The whole](shots-iphone/028-opening-opening.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening stage 1 -> 2 (You are aboard the Kestrel. Walk to a window if you like.)

### 15. Server connection (websocket) closed

- **How bad:** Minor (score 50)
- **Where:** loading the page, first at 00:15 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **What the vision model saw:** A mostly black mobile screen shows a centered title 'THE COSMOS' with a small grey tagline beneath it ('Your ship. Your crew. Real worlds at their real size. Mars is only the first port.'), and no buttons, 3D scene, or other UI. Flagged: No start/play button or any interactive control is visible on the start screen, so the player has nothing to tap to begin. This coincides with the bot's 'websocket closed' log entry, so the connection may have dropped and the UI never finished loading.; The 3D world, ships, and crew are absent; the entire background is flat black with no starfield or scene. This may be intentional for a splash screen, but combined with the closed websocket it could mean the scene failed to load.; The tagline text is small, low-contrast grey on near-black, which makes it hard to read on a phone. 'size.' also wraps onto its own line, leaving an orphaned word.
- **Screenshot:** [001-start-PROBLEM-ws-closed.jpg](shots-iphone/001-start-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/001-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed

### 16. Looks wrong in the screenshot: The 3D world, ships, and crew are absent; the entire background is flat black with no starfield or scene. This

- **How bad:** Minor (score 49)
- **Where:** loading the page, first at 00:15 into the run, on iPhone (WebKit)
- **What happened:** Full screen background (the vision model's description of the screen: A mostly black mobile screen shows a centered title 'THE COSMOS' with a small grey tagline beneath it ('Your ship. Your crew. Real worlds at their real size. Mars is only the first port.'), and no buttons, 3D scene, or other UI.)
- **Screenshot:** [001-start-PROBLEM-ws-closed.jpg](shots-iphone/001-start-PROBLEM-ws-closed.jpg)

  ![Looks wrong in the screenshot: The 3D wo](shots-iphone/001-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket closed

### 17. Looks wrong in the screenshot: The stage 2 prompt ('You are aboard the Kestrel...') is not visible anywhere, so the player gets no guidance a

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 05:54 into the run, on iPhone (WebKit)
- **What happened:** Center and bottom of the screen (the vision model's description of the screen: A fully black mobile screen with only a small dark 'Skip intro' button in the top-right corner and nothing else rendered.)
- **Screenshot:** [028-opening-opening.jpg](shots-iphone/028-opening-opening.jpg)

  ![Looks wrong in the screenshot: The stage](shots-iphone/028-opening-opening.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening stage 1 -> 2 (You are aboard the Kestrel. Walk to a window if you like.)

### 18. Looks wrong in the screenshot: The dialog panel covers the HUD info card at the top left. Lines under the coordinates are hidden behind the d

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 09:37 into the run, on iPhone (WebKit)
- **What happened:** Top left, between the location/gravity HUD and the top of the dialog (around y=100-140) (the vision model's description of the screen: A mobile view of the Mars port at Valles Marineris, with an 'Arrival guide' dialog open over the top of the scene, giving directions and two reply buttons, above a rust-colored landscape with a market stall and a metal hangar building.)
- **Screenshot:** [058-tour-talk-answer-arrival-guide.jpg](shots-iphone/058-tour-talk-answer-arrival-guide.jpg)

  ![Looks wrong in the screenshot: The dialo](shots-iphone/058-tour-talk-answer-arrival-guide.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap button "What is your watch like?" (ask them something)

### 19. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:50 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 03:48 [opening] walk to down the gangway
- **What the vision model saw:** {"description": "A very dark mobile opening scene on Mars showing a faint distant port with an 'ARRIVALS' sign and buildings on the horizon, an instruction text and 'Skip intro' button at the top, and
- **Screenshot:** [017-opening-PROBLEM-refusal-message.jpg](shots-iphone/017-opening-PROBLEM-refusal-message.jpg)

  ![Game said: "Welcome to Mars. Follow the ](shots-iphone/017-opening-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. in the boarding hall, waiting for the gangway to come down
  1. walk to down the gangway
  1. walk to down the gangway
  1. walk to down the gangway

### 20. Game said: "Weather sensors are offline. Watch the dust outside."

- **How bad:** Minor (score 42)
- **Where:** walking the port and talking to people, first at 11:35 into the run, on iPhone (WebKit)
- **What happened:** shown in crew-panel while the bot was: 11:34 [tour] tap button "What is your watch like?" (ask them something)
- **What the vision model saw:** {"description": "A mobile view of a Mars port interior in which a 'Weather officer' dialogue panel is open with two reply buttons ('Understand. What can I do here?' and 'Goodbye'), over a corrugated-m
- **Screenshot:** [097-tour-PROBLEM-refusal-message.jpg](shots-iphone/097-tour-PROBLEM-refusal-message.jpg)

  ![Game said: "Weather sensors are offline.](shots-iphone/097-tour-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to Weather officer
  1. tap #crew-talk (Talk to Weather officer)
  1. opened Ground controller instead of Weather officer; stepping closer to the right person
  1. tap button "✕" (close talk panel)
  1. go talk to Weather officer
  1. walk to Weather officer
  1. tap #crew-talk (Talk to Weather officer)
  1. tap button "What is your watch like?" (ask them something)

### 21. Frame-time spike during "tour"

- **How bad:** Minor (score 38), happened 3 times
- **Where:** walking the port and talking to people, first at 08:58 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 1018 ms (typical 31 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** {"description": "A third-person view of a Martian landscape in Valles Marineris on a mobile screen, showing a HUD with location and cargo info at top left, a Settings button at top right, a virtual jo
- **Later hits:** 15:00 a single frame took 3680 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 15:10 a single frame took 9853 ms (typical 168 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.
- **Screenshot:** [055-tour-PROBLEM-frame-spike.jpg](shots-iphone/055-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/055-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide
  1. route of 20 legs

### 22. Frame-time spike during "hire"

- **How bad:** Minor (score 38), happened 2 times
- **Where:** hiring crew from the crew hall, first at 15:23 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 896 ms (typical 40 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** {"description": "A third-person view of the Mars surface in Valles Marineris showing a row of six crew members standing in front of a long corr
- **Later hits:** 15:35 a single frame took 1064 ms (typical 37 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [110-hire-PROBLEM-frame-spike.jpg](shots-iphone/110-hire-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "hire"](shots-iphone/110-hire-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (refresh after the port tour)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. refresh check: moved 0.0 m, marks 10000 -> 10000, aboard false -> false
  1. === phase hire starts
  1. candidates: Jorge(Navigator), Sunita(Gunner (dorsal)), Walter(Gunner (ventral)), Zuri Okafor 1(Captain), Ada Chen 1(Pilot), Aoi Patel 1(Communications officer)
  1. walk to candidate Ada Chen 1
  1. route of 6 legs

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 489 s |
| opening the Settings / Account / World / Controls panels | done | 12 s |
| walking the port and talking to people | done | 358 s |
| hiring crew from the crew hall | done | 21 s |
| digging regolith and delivering it to the weigh bay | done | 191 s |
| boarding the ship, taking a seat and flying a course | done | 81 s |
| getting into and driving the survey rover | skipped (out of time) | 0 s |
| spots | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | skipped (out of time) | 0 s |

People talked to: 13 of 16. Crew hired: 2. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / tour: typical 168 ms, slowest 9853 ms, 3 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 7459 ms, 2 frames over 250 ms
- iphone / opening: typical 36 ms, slowest 7318 ms, 1 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 6552 ms, 2 frames over 250 ms
- iphone / fly: typical 48 ms, slowest 6388 ms, 5 frames over 250 ms

Button response time (tap to something changing on screen): median 128 ms, slowest 629 ms over 23 taps.

## Vision pass

A vision model (claude-sonnet-5-5) looked at 90 screenshots for about $0.82 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
