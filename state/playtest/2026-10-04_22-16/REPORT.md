# The Cosmos playtest report

Run: 2026-10-04 22:16 (local)  |  Build under test: `2b7f021e4b775d0a8377`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 15.5 minutes, 66 screenshots, 18 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)

## Short version

38 distinct problems found: 2 blockers, 9 serious, 27 smaller.

- **The opening could not be finished, so the bot had to bypass it** (BLOCKER)
- **The opening is stuck at step 0** (BLOCKER, seen 3 times)
- **Nothing changed for 60+ seconds (same message, same place)** (Serious, seen 6 times)
- **Nothing changed for 60+ seconds (same message, same place)** (Serious, seen 3 times)
- **Game said: "fetch failed"** (Serious)

## Problems, worst first

### 1. The opening could not be finished, so the bot had to bypass it

- **How bad:** BLOCKER (score 99)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 07:37 into the run, on iPhone (WebKit)
- **What happened:** After a refresh and the Walk button, the opening still would not move on. The rest of the run used the review start (?opening=off).
- **What the vision model saw:** {"description": "A first-person view inside a ship's passenger lounge on Mars, showing blue armchairs, a coin-operated viewing telescope, a ceiling with light fixtures, and a window with a railing tha
- **Screenshot:** [038-opening-PROBLEM-opening-bypassed.jpg](shots-iphone/038-opening-PROBLEM-opening-bypassed.jpg)

  ![The opening could not be finished, so th](shots-iphone/038-opening-PROBLEM-opening-bypassed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. REFRESH (opening stuck, trying a refresh)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. REFRESH (opening stuck, trying a refresh)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening is blocked: bypassing with opening=off so the rest of the game can still be tested

### 2. The opening is stuck at step 0

- **How bad:** BLOCKER (score 97), happened 3 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 02:16 into the run, on iPhone (WebKit)
- **What happened:** no progress for 120 s. caption: "", hint: "", button: "", position {"x":6622.2,"y":-3397245.8,"z":6622.2}, the game's own view: {"busy":true,"active":true,"statePose":{"x":4.6,"z":4},"stage":0,"held":false,"label":""}
- **What the vision model saw:** {"description": "A third-person view inside a Mars port waiting room with a dark tiled ceiling, fluorescent light fixtures, blue benches, and a seated person with dark hair and a maroon top seen from 
- **Later hits:** 04:54 no progress for 120 s. caption: "", hint: "Welcome to Marineris. Leave by the starboard gangway: the boarding hall is behin", button: "", position {"x":6622.2,"y":-3397245.8,"z":6622.2}, the gam / 07:37 no progress for 120 s. caption: "", hint: "Welcome to Marineris. Leave by the starboard gangway: the boarding hall is behin", button: "", position {"x":6622.2,"y":-3397245.8,"z":6622.2}, the gam
- **Screenshot:** [014-opening-PROBLEM-stuck-stage.jpg](shots-iphone/014-opening-PROBLEM-stuck-stage.jpg)

  ![The opening is stuck at step 0](shots-iphone/014-opening-PROBLEM-stuck-stage.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)
  1. tap screen to unlock sound
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 3. Nothing changed for 60+ seconds (same message, same place)

- **How bad:** Serious (score 86), happened 6 times
- **Where:** walking the port and talking to people, first at 10:10 into the run, on iPhone (WebKit)
- **What happened:** in "tour": position {"x":6622.2,"y":-3397245.8,"z":6622.2}, button "", caption "", toast "", ship outside
- **What the vision model saw:** A mostly washed-out, blurry beige/white-grey screen with a faint orange circle at lower left and a small line of low-contrast tan text at the top left reading 'Welcome to Manneris. Leave by the starboard gangway: the boarding hall is behind the promenade.' Flagged: The 3D world is not visible. The whole viewport is a blurry, washed-out fog or white-out, with no recognizable ships, people, terrain or Mars port geometry. It looks like the camera is inside or against a blurred surface, or the scene has not rendered.; The welcome/instruction text is pale tan on a near-white background, so it is very low contrast and hard to read. It is also small.; A lone semi-transparent orange circle floats with no clear purpose. It may be a touch indicator or joystick, or a stray UI element, and it sits over the blurred scene.; Dark smudges and blotches are scattered over the blurry image, which looks like a broken or heavily stretched texture or an unfocused render.
- **Later hits:** 11:10 in "tour": position {"x":6622.2,"y":-3397245.8,"z":6622.2}, button "", caption "", toast "", ship outside / 12:11 in "tour": position {"x":6622.2,"y":-3397245.8,"z":6622.2}, button "", caption "", toast "", ship outside
- **Screenshot:** [052-tour-PROBLEM-stuck-state.jpg](shots-iphone/052-tour-PROBLEM-stuck-state.jpg)

  ![Nothing changed for 60+ seconds (same me](shots-iphone/052-tour-PROBLEM-stuck-state.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #3
  1. jump
  1. not getting closer (10 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (10 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 28 legs

### 4. Nothing changed for 60+ seconds (same message, same place)

- **How bad:** Serious (score 86), happened 3 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 05:06 into the run, on iPhone (WebKit)
- **What happened:** in "opening": position {"x":6622.2,"y":-3397245.8,"z":6622.2}, button "", caption "", toast "", ship outside
- **What the vision model saw:** A mostly black loading screen on a phone with a short welcome message at the top-left ('Welcome to Marineris. Leave by the starboard gangway: the boarding hall is behind the promenade.') and the text 'Preparing the opening…' near the bottom center. Flagged: The whole screen is black with no 3D world, scene, ship, people, or UI controls visible. This may be expected because the opening is still loading right after the websocket connected, but nothing besides text has rendered.; The welcome text is small, and its wrapped lines are cramped against the top-left corner. It is readable but sits close to the left edge, and the top may fall inside the notch/status-bar safe area.
- **Later hits:** 06:31 in "opening": position {"x":6622.2,"y":-3397245.8,"z":6622.2}, button "", caption "", toast "", ship outside / 07:31 in "opening": position {"x":6622.2,"y":-3397245.8,"z":6622.2}, button "", caption "", toast "", ship outside
- **Screenshot:** [026-opening-PROBLEM-stuck-state.jpg](shots-iphone/026-opening-PROBLEM-stuck-state.jpg)

  ![Nothing changed for 60+ seconds (same me](shots-iphone/026-opening-PROBLEM-stuck-state.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. REFRESH (opening stuck, trying a refresh)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. REFRESH (opening stuck, trying a refresh)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 5. Game said: "fetch failed"

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 09:04 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 08:58 [tour] not getting closer (11 m away), trying to get unstuck #6
- **What the vision model saw:** {"description": "A mostly blank, washed-out white/grey screen, as if the camera is pressed against a wall or surface, with faint welcome text at the top left, a small orange circular touch indicator a
- **Screenshot:** [048-tour-PROBLEM-refusal-message.jpg](shots-iphone/048-tour-PROBLEM-refusal-message.jpg)

  ![Game said: "fetch failed"](shots-iphone/048-tour-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. not getting closer (11 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (11 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 20 legs
  1. not getting closer (11 m away), trying to get unstuck #6

### 6. Stuck while walking to Arrival guide

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 09:12 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port 140,-82 (target -12,41, 11 m away)
- **What the vision model saw:** {"description": "A nearly all-white, blurry screen, apparently the camera pressed up against a pale wall or surface, with faint low-contrast overlay text at the top reading 'Welcome to Mariners. Leave
- **Screenshot:** [049-tour-PROBLEM-stuck-walking.jpg](shots-iphone/049-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Arrival guide](shots-iphone/049-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (11 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 20 legs
  1. not getting closer (11 m away), trying to get unstuck #6
  1. not getting closer (11 m away), trying to get unstuck #7
  1. not getting closer (11 m away), trying to get unstuck #8

### 7. Stuck while walking to Supply clerk

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 10:28 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port 140,-82 (target -65,19, 10 m away)
- **What the vision model saw:** A nearly blank, washed-out white/beige blurry view (apparently the camera pressed up against a wall or surface) with faint pale-orange instruction text at the top left reading 'Welcome to Mariner's. Leave by the starboard gangway: the boarding hall is behind the promenade.' and a faint orange circular touch indicator at lower left. Flagged: The 3D world is not visible. The whole frame is a featureless, blurry off-white surface with smudges, which suggests the camera is clipped into or pressed against a wall or object. This matches the bot's report of being stuck 10 m from its target.; The welcome/instruction text is pale orange on a near-white background, so contrast is very low and it is hard to read.; The orange touch/joystick indicator is faint and washed out against the background, so the on-screen control is barely visible.; Blurry dark smudges and blotches look like stretched or low-resolution textures, or a surface seen too close up.
- **Screenshot:** [053-tour-PROBLEM-stuck-walking.jpg](shots-iphone/053-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Supply clerk](shots-iphone/053-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (10 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 28 legs
  1. not getting closer (10 m away), trying to get unstuck #6
  1. not getting closer (10 m away), trying to get unstuck #7
  1. not getting closer (10 m away), trying to get unstuck #8

### 8. Stuck while walking to Food trader

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 11:43 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port 140,-82 (target -70,48, 11 m away)
- **What the vision model saw:** {"description": "A nearly blank, washed-out white/grey view of what looks like a wall or corner pressed up against the camera, with a faint low-contrast welcome message in the top-left (\"Welcome to M
- **Screenshot:** [056-tour-PROBLEM-stuck-walking.jpg](shots-iphone/056-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Food trader](shots-iphone/056-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (11 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 28 legs
  1. not getting closer (11 m away), trying to get unstuck #6
  1. not getting closer (11 m away), trying to get unstuck #7
  1. not getting closer (11 m away), trying to get unstuck #8

### 9. Stuck while walking to Salvage trader

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 12:59 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port 140,-82 (target -62,48, 11 m away)
- **What the vision model saw:** A mostly washed-out, blurry beige-gray screen with faint smudgy shapes and a low-contrast welcome message at top-left reading 'Welcome to Marineris. Leave by the starboard gangway: the boarding hall is behind the promenade.', plus a faint tan circular joystick-like control at lower left. Flagged: The 3D world is not visible. The whole viewport is a foamy, blurry, near-white haze with only vague smudges, so no recognizable ships, people, floor or architecture can be seen. It looks like the camera is inside or pressed against a surface or fog, which fits the bot reporting it is stuck.; The welcome text is tan on a pale beige background, so contrast is very low and it is hard to read.; The virtual joystick or touch control is a faint tan circle with an almost invisible outline, barely distinguishable from the background.; A row of tiny, faint dots or text fragments that look like an unreadable label or a broken HUD element.
- **Screenshot:** [059-tour-PROBLEM-stuck-walking.jpg](shots-iphone/059-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Salvage trader](shots-iphone/059-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (11 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 27 legs
  1. not getting closer (11 m away), trying to get unstuck #6
  1. not getting closer (11 m away), trying to get unstuck #7
  1. not getting closer (11 m away), trying to get unstuck #8

### 10. Stuck while walking to Water trader

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 14:14 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port 140,-82 (target -54,48, 11 m away)
- **What the vision model saw:** {"description": "A nearly all-white, washed-out, blurry view with faint grey smudges and a tilted bright panel edge, a faint pale-orange text line at the top reading 'Welcome to Marineris. Leave by th
- **Screenshot:** [062-tour-PROBLEM-stuck-walking.jpg](shots-iphone/062-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Water trader](shots-iphone/062-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (11 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 26 legs
  1. not getting closer (11 m away), trying to get unstuck #6
  1. not getting closer (11 m away), trying to get unstuck #7
  1. not getting closer (11 m away), trying to get unstuck #8

### 11. Stuck while walking to Field kit trader

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 15:29 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port 140,-82 (target -46,48, 11 m away)
- **What the vision model saw:** {"description": "A nearly all-white, heavily blurred or fogged screen with a faint beige gradient, showing only a tan caption in the top-left ('Welcome to Marineris. Leave by the starboard gangway: th
- **Screenshot:** [065-tour-PROBLEM-stuck-walking.jpg](shots-iphone/065-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Field kit trader](shots-iphone/065-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (11 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 25 legs
  1. not getting closer (11 m away), trying to get unstuck #6
  1. not getting closer (11 m away), trying to get unstuck #7
  1. not getting closer (11 m away), trying to get unstuck #8

### 12. Looks wrong in the screenshot: The 3D world is not visible. The whole viewport is a washed-out, blurry white/gray haze with no recognizable M

- **How bad:** Annoying (score 63), happened 3 times
- **Where:** walking the port and talking to people, first at 08:22 into the run, on iPhone (WebKit)
- **What happened:** entire screen (the vision model's description of the screen: A nearly all-white, washed-out blurry screen with faint gray smudges and a small translucent orange circle at lower left, with a faded welcome message at the top saying 'Welcome to Marineris. Leave by the starboard gangway: the boarding hall is behind the promenade.')
- **Screenshot:** [046-tour-walking.jpg](shots-iphone/046-tour-walking.jpg)

  ![Looks wrong in the screenshot: The 3D wo](shots-iphone/046-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump

### 13. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 8 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:16 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4230 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** {"description": "A dark first-person view inside a ship's observation lounge, with a railing and window showing a Mars-like orange planet and docked ships outside, a small table in the middle, and a s
- **Later hits:** 01:16 a single frame took 795 ms (typical 16 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 01:28 a single frame took 4050 ms (typical 18 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 14. Frame-time spike during "opening-bypass"

- **How bad:** Annoying (score 62)
- **Where:** starting from the review start (opening skipped), first at 07:57 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 5665 ms (typical 44 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** {"description": "A dark first-person view of a ship's passenger lounge with navy armchairs, a coin-operated telescope and a large window onto a Mars port with an orange-and-white tower, with a welcome
- **Screenshot:** [039-opening-bypass-PROBLEM-frame-spike.jpg](shots-iphone/039-opening-bypass-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening-bypass"](shots-iphone/039-opening-bypass-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. REFRESH (opening stuck, trying a refresh)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening is blocked: bypassing with opening=off so the rest of the game can still be tested
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 15. Looks wrong in the screenshot: The screen is an empty black void with only the title text. There is no 3D world, ship, planet, menu, or start

- **How bad:** Annoying (score 56)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 01:02 into the run, on iPhone (WebKit)
- **What happened:** Entire screen, especially the area around and below the centered text (the vision model's description of the screen: A mostly black mobile screen with a centered title 'THE COSMOS' and a small gray tagline reading 'Your ship. Your crew. Real worlds at their real size. Mars is only the first port.' and nothing else.)
- **Screenshot:** [008-opening-PROBLEM-ws-closed.jpg](shots-iphone/008-opening-PROBLEM-ws-closed.jpg)

  ![Looks wrong in the screenshot: The scree](shots-iphone/008-opening-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket closed

### 16. Looks wrong in the screenshot: The 3D world is not visible. The view is almost entirely a washed-out white or grey blur with no recognizable 

- **How bad:** Annoying (score 56)
- **Where:** walking the port and talking to people, first at 09:38 into the run, on iPhone (WebKit)
- **What happened:** Whole screen (the vision model's description of the screen: A nearly all-white, washed-out blurry view with a faint pale panel or wall filling most of the screen, a small caption in the top-left reading 'Welcome to Mariners. Leave by the starboard gangway: the boarding hall is behind the promenade.', and a faint orange circular touch control near the lower left.)
- **Screenshot:** [050-tour-walking.jpg](shots-iphone/050-tour-walking.jpg)

  ![Looks wrong in the screenshot: The 3D wo](shots-iphone/050-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump

### 17. Looks wrong in the screenshot: The 3D world is not visible. The whole frame is a featureless, blurry off-white surface with smudges, which su

- **How bad:** Annoying (score 56)
- **Where:** walking the port and talking to people, first at 10:28 into the run, on iPhone (WebKit)
- **What happened:** Entire screen (the vision model's description of the screen: A nearly blank, washed-out white/beige blurry view (apparently the camera pressed up against a wall or surface) with faint pale-orange instruction text at the top left reading 'Welcome to Mariner's. Leave by the starboard gangway: the boarding hall is behind the promenade.' and a faint orange circular touch indicator at lower left.)
- **Screenshot:** [053-tour-PROBLEM-stuck-walking.jpg](shots-iphone/053-tour-PROBLEM-stuck-walking.jpg)

  ![Looks wrong in the screenshot: The 3D wo](shots-iphone/053-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (10 m away), trying to get unstuck #8

### 18. Looks wrong in the screenshot: The camera appears to be pressed against or inside a wall or panel. The view is a blurry, featureless grey-whi

- **How bad:** Annoying (score 56)
- **Where:** walking the port and talking to people, first at 10:53 into the run, on iPhone (WebKit)
- **What happened:** entire screen (the vision model's description of the screen: A mostly blank, washed-out white-grey screen that looks like a close-up of a smooth wall or panel with a vertical seam, with faint pale-orange welcome text at the top left ('Welcome to Manneris. Leave by the starboard gangway: the boarding hall is behind the promenade.') and a faint orange circle on the left side.)
- **Screenshot:** [054-tour-walking.jpg](shots-iphone/054-tour-walking.jpg)

  ![Looks wrong in the screenshot: The camer](shots-iphone/054-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump

### 19. Looks wrong in the screenshot: The camera is jammed against or clipped into a wall or corner. The whole view is a featureless white/grey surf

- **How bad:** Annoying (score 56)
- **Where:** walking the port and talking to people, first at 11:22 into the run, on iPhone (WebKit)
- **What happened:** Entire screen (the vision model's description of the screen: A mostly blank, washed-out white/grey view that looks like the camera is pressed against or inside a wall corner, with faint smudgy marks, a low-contrast hint text at the top-left ('Welcome to Manneris. Leave by the starboard gangway; the boarding hall is behind the promenade.') and a faint tan circular touch-control dot at the lower lef
- **Screenshot:** [055-tour-walking.jpg](shots-iphone/055-tour-walking.jpg)

  ![Looks wrong in the screenshot: The camer](shots-iphone/055-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. sidestep around whatever is in the way

### 20. Looks wrong in the screenshot: The camera is clipped against or inside a white wall or corner surface. The view fills the whole screen with f

- **How bad:** Annoying (score 56)
- **Where:** walking the port and talking to people, first at 14:39 into the run, on iPhone (WebKit)
- **What happened:** entire screen (the vision model's description of the screen: A nearly blank, pale grey-white screen that looks like the camera is pressed up against a white wall or corner, with a faint vertical seam down the middle, a small tan circle at lower left, and low-contrast beige text in the top-left reading 'Welcome to Manneris. Leave by the starboard gangway: the boarding hall is behind the promenade.'
- **Screenshot:** [063-tour-walking.jpg](shots-iphone/063-tour-walking.jpg)

  ![Looks wrong in the screenshot: The camer](shots-iphone/063-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump

### 21. Looks wrong in the screenshot: The view is almost entirely a featureless pale surface with smudgy dark blotches. The camera seems to be clipp

- **How bad:** Annoying (score 56)
- **Where:** walking the port and talking to people, first at 15:07 into the run, on iPhone (WebKit)
- **What happened:** Whole screen (the vision model's description of the screen: A mostly blank, pale grey-white screen that looks like the camera is pressed up against a wall or corner, with a faint peach-colored welcome message at the top ('Welcome to Mariners. Leave by the starboard gangway; the boarding hall is behind the promenade.') and a translucent peach circular touch control at the lower left.)
- **Screenshot:** [064-tour-walking.jpg](shots-iphone/064-tour-walking.jpg)

  ![Looks wrong in the screenshot: The view ](shots-iphone/064-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. sidestep around whatever is in the way

### 22. Server connection (websocket) closed

- **How bad:** Minor (score 50), happened 3 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 01:02 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **What the vision model saw:** A mostly black mobile screen with a centered title 'THE COSMOS' and a small gray tagline reading 'Your ship. Your crew. Real worlds at their real size. Mars is only the first port.' and nothing else. Flagged: The screen is an empty black void with only the title text. There is no 3D world, ship, planet, menu, or start/play button, so the player has nothing to interact with. The last bot action was 'websocket closed', which suggests the game never connected or loaded past the intro text.; The tagline is small, low-contrast gray on near-black, which makes it hard to read on a phone. It also wraps awkwardly, leaving the single word 'size.' alone on its own line.
- **Later hits:** 01:06 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/ / 07:37 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Screenshot:** [008-opening-PROBLEM-ws-closed.jpg](shots-iphone/008-opening-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/008-opening-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)
  1. tap screen to unlock sound
  1. websocket closed

### 23. The Settings button is not on screen

- **How bad:** Minor (score 50)
- **Where:** opening the Settings / Account / World / Controls panels, first at 07:57 into the run, on iPhone (WebKit)
- **What happened:** #btn-settings
- **What the vision model saw:** {"description": "A dim first-person view inside a Marineris port lounge with blue armchairs, a coin telescope and a window onto the Mars landing field and a striped tower, with a welcome hint at top-l
- **Screenshot:** [041-panels-PROBLEM-panel-button-missing.jpg](shots-iphone/041-panels-PROBLEM-panel-button-missing.jpg)

  ![The Settings button is not on screen](shots-iphone/041-panels-PROBLEM-panel-button-missing.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (opening stuck, trying a refresh)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening is blocked: bypassing with opening=off so the rest of the game can still be tested
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase panels starts

### 24. The Account / purse button is not on screen

- **How bad:** Minor (score 50)
- **Where:** opening the Settings / Account / World / Controls panels, first at 07:57 into the run, on iPhone (WebKit)
- **What happened:** #purse
- **What the vision model saw:** {"description": "A dim first-person view inside a ship's passenger lounge on Marineris, with blue armchairs, a coin-operated viewer, and a window showing the Mars port and a striped control tower, wit
- **Screenshot:** [042-panels-PROBLEM-panel-button-missing.jpg](shots-iphone/042-panels-PROBLEM-panel-button-missing.jpg)

  ![The Account / purse button is not on scr](shots-iphone/042-panels-PROBLEM-panel-button-missing.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (opening stuck, trying a refresh)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening is blocked: bypassing with opening=off so the rest of the game can still be tested
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase panels starts

### 25. The World / crew button is not on screen

- **How bad:** Minor (score 50)
- **Where:** opening the Settings / Account / World / Controls panels, first at 07:57 into the run, on iPhone (WebKit)
- **What happened:** #multiplayer-button
- **What the vision model saw:** {"description": "A first-person view inside a dimly lit ship terminal lounge on Marineris, with blue armchairs in the foreground, a window wall looking out at a striped control tower and Martian lands
- **Screenshot:** [043-panels-PROBLEM-panel-button-missing.jpg](shots-iphone/043-panels-PROBLEM-panel-button-missing.jpg)

  ![The World / crew button is not on screen](shots-iphone/043-panels-PROBLEM-panel-button-missing.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (opening stuck, trying a refresh)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening is blocked: bypassing with opening=off so the rest of the game can still be tested
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase panels starts

### 26. The Controls button is not on screen

- **How bad:** Minor (score 50)
- **Where:** opening the Settings / Account / World / Controls panels, first at 07:57 into the run, on iPhone (WebKit)
- **What happened:** #btn-key-controls
- **What the vision model saw:** {"description": "A first-person view inside a dark ship lounge at the Mars port, with a blue armchair, a second chair cut off in the foreground, a coin telescope by a large window showing a dusk-lit p
- **Screenshot:** [044-panels-PROBLEM-panel-button-missing.jpg](shots-iphone/044-panels-PROBLEM-panel-button-missing.jpg)

  ![The Controls button is not on screen](shots-iphone/044-panels-PROBLEM-panel-button-missing.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (opening stuck, trying a refresh)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening is blocked: bypassing with opening=off so the rest of the game can still be tested
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase panels starts

### 27. Looks wrong in the screenshot: The welcome/instruction text is very low contrast (pale beige on near-white) and is hard to read.

- **How bad:** Minor (score 49), happened 2 times
- **Where:** walking the port and talking to people, first at 08:22 into the run, on iPhone (WebKit)
- **What happened:** top left, the text block (the vision model's description of the screen: A nearly all-white, washed-out blurry screen with faint gray smudges and a small translucent orange circle at lower left, with a faded welcome message at the top saying 'Welcome to Marineris. Leave by the starboard gangway: the boarding hall is behind the promenade.')
- **Screenshot:** [046-tour-walking.jpg](shots-iphone/046-tour-walking.jpg)

  ![Looks wrong in the screenshot: The welco](shots-iphone/046-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump

### 28. Looks wrong in the screenshot: The welcome text names 'Marineris', but nothing in the scene matches a starboard gangway, boarding hall or pro

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 08:22 into the run, on iPhone (WebKit)
- **What happened:** center of the screen (the vision model's description of the screen: A nearly all-white, washed-out blurry screen with faint gray smudges and a small translucent orange circle at lower left, with a faded welcome message at the top saying 'Welcome to Marineris. Leave by the starboard gangway: the boarding hall is behind the promenade.')
- **Screenshot:** [046-tour-walking.jpg](shots-iphone/046-tour-walking.jpg)

  ![Looks wrong in the screenshot: The welco](shots-iphone/046-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump

### 29. Looks wrong in the screenshot: The welcome caption is very low contrast, pale orange or beige text on a near-white background, so it is hard 

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 09:38 into the run, on iPhone (WebKit)
- **What happened:** Top-left, the 'Welcome to Mariners...' text (the vision model's description of the screen: A nearly all-white, washed-out blurry view with a faint pale panel or wall filling most of the screen, a small caption in the top-left reading 'Welcome to Mariners. Leave by the starboard gangway: the boarding hall is behind the promenade.', and a faint orange circular touch control near the lower left.)
- **Screenshot:** [050-tour-walking.jpg](shots-iphone/050-tour-walking.jpg)

  ![Looks wrong in the screenshot: The welco](shots-iphone/050-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump

### 30. Looks wrong in the screenshot: A hard vertical edge splits the screen, with a differently shaded surface on the right. This suggests geometry

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 09:38 into the run, on iPhone (WebKit)
- **What happened:** Right side, around x=310-340 (the vision model's description of the screen: A nearly all-white, washed-out blurry view with a faint pale panel or wall filling most of the screen, a small caption in the top-left reading 'Welcome to Mariners. Leave by the starboard gangway: the boarding hall is behind the promenade.', and a faint orange circular touch control near the lower left.)
- **Screenshot:** [050-tour-walking.jpg](shots-iphone/050-tour-walking.jpg)

  ![Looks wrong in the screenshot: A hard ve](shots-iphone/050-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump

### 31. Looks wrong in the screenshot: The welcome/instruction text is pale tan on a near-white background, so it is very low contrast and hard to re

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 10:10 into the run, on iPhone (WebKit)
- **What happened:** Top left, the first three lines of text (the vision model's description of the screen: A mostly washed-out, blurry beige/white-grey screen with a faint orange circle at lower left and a small line of low-contrast tan text at the top left reading 'Welcome to Manneris. Leave by the starboard gangway: the boarding hall is behind the promenade.')
- **Screenshot:** [052-tour-PROBLEM-stuck-state.jpg](shots-iphone/052-tour-PROBLEM-stuck-state.jpg)

  ![Looks wrong in the screenshot: The welco](shots-iphone/052-tour-PROBLEM-stuck-state.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. route of 28 legs

### 32. Looks wrong in the screenshot: The welcome/instruction text is pale orange on a near-white background, so contrast is very low and it is hard

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 10:28 into the run, on iPhone (WebKit)
- **What happened:** Top left, the 'Welcome to Mariner's...' text (the vision model's description of the screen: A nearly blank, washed-out white/beige blurry view (apparently the camera pressed up against a wall or surface) with faint pale-orange instruction text at the top left reading 'Welcome to Mariner's. Leave by the starboard gangway: the boarding hall is behind the promenade.' and a faint orange circular touch
- **Screenshot:** [053-tour-PROBLEM-stuck-walking.jpg](shots-iphone/053-tour-PROBLEM-stuck-walking.jpg)

  ![Looks wrong in the screenshot: The welco](shots-iphone/053-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (10 m away), trying to get unstuck #8

### 33. Looks wrong in the screenshot: The welcome text is pale orange on a near-white background, so contrast is very low and it is hard to read.

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 10:53 into the run, on iPhone (WebKit)
- **What happened:** top left, the welcome message (the vision model's description of the screen: A mostly blank, washed-out white-grey screen that looks like a close-up of a smooth wall or panel with a vertical seam, with faint pale-orange welcome text at the top left ('Welcome to Manneris. Leave by the starboard gangway: the boarding hall is behind the promenade.') and a faint orange circle on the left side.)
- **Screenshot:** [054-tour-walking.jpg](shots-iphone/054-tour-walking.jpg)

  ![Looks wrong in the screenshot: The welco](shots-iphone/054-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump

### 34. Looks wrong in the screenshot: The surface texture is smeared and low-resolution, with blurry smudges and a hard vertical seam. This suggests

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 10:53 into the run, on iPhone (WebKit)
- **What happened:** center and right, along the vertical edge near x=270 (the vision model's description of the screen: A mostly blank, washed-out white-grey screen that looks like a close-up of a smooth wall or panel with a vertical seam, with faint pale-orange welcome text at the top left ('Welcome to Manneris. Leave by the starboard gangway: the boarding hall is behind the promenade.') and a faint orange circle on
- **Screenshot:** [054-tour-walking.jpg](shots-iphone/054-tour-walking.jpg)

  ![Looks wrong in the screenshot: The surfa](shots-iphone/054-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump

### 35. Looks wrong in the screenshot: The welcome text is tan on a pale beige background, so contrast is very low and it is hard to read.

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 12:59 into the run, on iPhone (WebKit)
- **What happened:** top-left, welcome message (the vision model's description of the screen: A mostly washed-out, blurry beige-gray screen with faint smudgy shapes and a low-contrast welcome message at top-left reading 'Welcome to Marineris. Leave by the starboard gangway: the boarding hall is behind the promenade.', plus a faint tan circular joystick-like control at lower left.)
- **Screenshot:** [059-tour-PROBLEM-stuck-walking.jpg](shots-iphone/059-tour-PROBLEM-stuck-walking.jpg)

  ![Looks wrong in the screenshot: The welco](shots-iphone/059-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (11 m away), trying to get unstuck #8

### 36. Looks wrong in the screenshot: The virtual joystick or touch control is a faint tan circle with an almost invisible outline, barely distingui

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 12:59 into the run, on iPhone (WebKit)
- **What happened:** lower left, around (80, 640) (the vision model's description of the screen: A mostly washed-out, blurry beige-gray screen with faint smudgy shapes and a low-contrast welcome message at top-left reading 'Welcome to Marineris. Leave by the starboard gangway: the boarding hall is behind the promenade.', plus a faint tan circular joystick-like control at lower left.)
- **Screenshot:** [059-tour-PROBLEM-stuck-walking.jpg](shots-iphone/059-tour-PROBLEM-stuck-walking.jpg)

  ![Looks wrong in the screenshot: The virtu](shots-iphone/059-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (11 m away), trying to get unstuck #8

### 37. Looks wrong in the screenshot: The welcome text is beige on a near-white background, so contrast is very low and it is hard to read.

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 14:39 into the run, on iPhone (WebKit)
- **What happened:** top-left, the 'Welcome to Manneris...' text block (the vision model's description of the screen: A nearly blank, pale grey-white screen that looks like the camera is pressed up against a white wall or corner, with a faint vertical seam down the middle, a small tan circle at lower left, and low-contrast beige text in the top-left reading 'Welcome to Manneris. Leave by the starboard gangway: the boa
- **Screenshot:** [063-tour-walking.jpg](shots-iphone/063-tour-walking.jpg)

  ![Looks wrong in the screenshot: The welco](shots-iphone/063-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump

### 38. Looks wrong in the screenshot: The welcome/instruction text is peach on a near-white background, so it is very low contrast and hard to read.

- **How bad:** Minor (score 49)
- **Where:** walking the port and talking to people, first at 15:07 into the run, on iPhone (WebKit)
- **What happened:** Top left, the first three lines of text (the vision model's description of the screen: A mostly blank, pale grey-white screen that looks like the camera is pressed up against a wall or corner, with a faint peach-colored welcome message at the top ('Welcome to Mariners. Leave by the starboard gangway; the boarding hall is behind the promenade.') and a translucent peach circular touch control at the
- **Screenshot:** [064-tour-walking.jpg](shots-iphone/064-tour-walking.jpg)

  ![Looks wrong in the screenshot: The welco](shots-iphone/064-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. sidestep around whatever is in the way

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - bypass | 461 s |
| opening the Settings / Account / World / Controls panels | done | 0 s |
| walking the port and talking to people | done | 452 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| boarding the ship, taking a seat and flying a course | skipped (out of time) | 0 s |
| getting into and driving the survey rover | skipped (out of time) | 0 s |
| spots | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | skipped (out of time) | 0 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / opening-bypass: typical 44 ms, slowest 5665 ms, 3 frames over 250 ms
- iphone / opening: typical 45 ms, slowest 5521 ms, 3 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 5047 ms, 2 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 4670 ms, 2 frames over 250 ms
- iphone / opening: typical 33 ms, slowest 4310 ms, 3 frames over 250 ms

## Vision pass

A vision model (claude-sonnet-5-5) looked at 65 screenshots for about $0.59 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
