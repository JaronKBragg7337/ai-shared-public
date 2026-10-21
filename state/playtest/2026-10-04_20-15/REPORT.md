# The Cosmos playtest report

Run: 2026-10-04 20:15 (local)  |  Build under test: `2b7f021e4b775d0a8377`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 2.2 minutes, 44 screenshots, 10 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)

## Short version

10 distinct problems found: 0 blockers, 0 serious, 10 smaller.

- **Frame-time spike during "spots"** (Annoying, seen 5 times)
- **Server connection (websocket) closed** (Minor, seen 3 times)
- **A request failed to load** (Minor)
- **A request failed to load** (Minor)
- **A request failed to load** (Minor)

## Problems, worst first

### 1. Frame-time spike during "spots"

- **How bad:** Annoying (score 62), happened 5 times
- **Where:** spots, first at 00:25 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4760 ms (typical 17 ms); 7 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 01:35 a single frame took 3373 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 01:46 a single frame took 4043 ms (typical 31 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [010-spots-PROBLEM-frame-spike.jpg](shots-iphone/010-spots-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "spots"](shots-iphone/010-spots-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts
  1. spots source inventory {"doors":3,"pads":9,"counts":{"portRooms":13,"pads":9,"ships":9}}
  1. spots: skipped door Supply depot-15m-open: the game moved the player 242 m away from the requested spot
  1. spots: skipped door Supply depot-5m-shut: the game moved the player 8 m away from the requested spot

### 2. Server connection (websocket) closed

- **How bad:** Minor (score 50), happened 3 times
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Later hits:** 01:26 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/ / 01:51 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Screenshot:** [007-start-PROBLEM-ws-closed.jpg](shots-iphone/007-start-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/007-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed

### 3. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/sunita.glb (Load request cancelled)
- **Screenshot:** [001-start-PROBLEM-request-failed.jpg](shots-iphone/001-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/001-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 4. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/jorge.glb (Load request cancelled)
- **Screenshot:** [002-start-PROBLEM-request-failed.jpg](shots-iphone/002-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/002-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 5. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/aoi.glb (Load request cancelled)
- **Screenshot:** [003-start-PROBLEM-request-failed.jpg](shots-iphone/003-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/003-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 6. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/walter.glb (Load request cancelled)
- **Screenshot:** [004-start-PROBLEM-request-failed.jpg](shots-iphone/004-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/004-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 7. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/ada.glb (Load request cancelled)
- **Screenshot:** [005-start-PROBLEM-request-failed.jpg](shots-iphone/005-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/005-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 8. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/zuri.glb (Load request cancelled)
- **Screenshot:** [006-start-PROBLEM-request-failed.jpg](shots-iphone/006-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/006-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 9. Same sign text on 2 port signs: "marineris port"

- **How bad:** Small (score 22)
- **Where:** spots, first at 01:26 into the run, on iPhone (WebKit)
- **What happened:** beacon, arrivals-gantry

- **Steps to reproduce (what the bot did just before):**
  1. spots note: model for meridian@pad09 not found (no ramp mesh check)
  1. spots: meridian-pad09-airlock ramp is raised, no walk views
  1. spots: skipped sign Supply-depot-sign: the game moved the player 251 m away from the requested spot
  1. spots: skipped sign Crew-hall-sign: the game moved the player 228 m away from the requested spot
  1. spots: skipped sign arrivals-gantry: the game moved the player 227 m away from the requested spot
  1. spots: skipped sign padboard-01: the game moved the player 78 m away from the requested spot
  1. spots: skipped sign padboard-02: the game moved the player 228 m away from the requested spot
  1. spots: skipped sign padboard-03: the game moved the player 347 m away from the requested spot

### 10. Same sign text on 2 port signs: "pad status"

- **How bad:** Small (score 22)
- **Where:** spots, first at 01:26 into the run, on iPhone (WebKit)
- **What happened:** padboard-02, padboard-03

- **Steps to reproduce (what the bot did just before):**
  1. spots note: model for meridian@pad09 not found (no ramp mesh check)
  1. spots: meridian-pad09-airlock ramp is raised, no walk views
  1. spots: skipped sign Supply-depot-sign: the game moved the player 251 m away from the requested spot
  1. spots: skipped sign Crew-hall-sign: the game moved the player 228 m away from the requested spot
  1. spots: skipped sign arrivals-gantry: the game moved the player 227 m away from the requested spot
  1. spots: skipped sign padboard-01: the game moved the player 78 m away from the requested spot
  1. spots: skipped sign padboard-02: the game moved the player 228 m away from the requested spot
  1. spots: skipped sign padboard-03: the game moved the player 347 m away from the requested spot

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| spots | done - 77 spot shots (door 10, skippedMoved 43, door-floor 2, ramp 2, ship 14, sign 2, night 4); 0 door overlaps; 5 ships. | 106 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / spots: typical 36 ms, slowest 6426 ms, 4 frames over 250 ms
- iphone / spots: typical 17 ms, slowest 4760 ms, 7 frames over 250 ms
- iphone / spots: typical 31 ms, slowest 4043 ms, 3 frames over 250 ms
- iphone / spots: typical 16 ms, slowest 3373 ms, 2 frames over 250 ms
- iphone / spots: typical 16 ms, slowest 3253 ms, 2 frames over 250 ms

## Trouble spot coverage

Spot shots by type: door 10, skippedMoved 43, door-floor 2, ramp 2, ship 14, sign 2, night 4. Live inventory: 3 port doors, 9 pads, 5 parked ships (courier, lifeboat, meridian, meridian, meridian), 8 port signs. Each shot carries a what-to-look-for line for the vision review; targets and prompts are in spots.json.
Math findings (no picture needed): door opening vs prop boxes, duplicate door names, lowered ramp without a visible mesh, repeated sign text, interior door signs falling back to MEDBAY. Not yet covered: aboard views of interior doors (pipes/boards/glass across them), hull see-through is judged by the vision pass only, other ship types' interior sign lists.

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
