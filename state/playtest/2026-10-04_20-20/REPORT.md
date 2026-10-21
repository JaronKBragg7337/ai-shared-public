# The Cosmos playtest report

Run: 2026-10-04 20:20 (local)  |  Build under test: `2b7f021e4b775d0a8377`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 8.1 minutes, 77 screenshots, 9 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)

## Short version

9 distinct problems found: 0 blockers, 0 serious, 9 smaller.

- **Frame-time spike during "spots"** (Annoying, seen 5 times)
- **Server connection (websocket) closed** (Minor, seen 3 times)
- **A request failed to load** (Minor)
- **A request failed to load** (Minor)
- **A request failed to load** (Minor)

## Problems, worst first

### 1. Frame-time spike during "spots"

- **How bad:** Annoying (score 62), happened 5 times
- **Where:** spots, first at 00:27 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 6123 ms (typical 17 ms); 6 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 05:48 a single frame took 3214 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 05:58 a single frame took 3590 ms (typical 30 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [008-spots-PROBLEM-frame-spike.jpg](shots-iphone/008-spots-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "spots"](shots-iphone/008-spots-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts
  1. spots source inventory {"doors":3,"pads":9,"counts":{"portRooms":13,"pads":9,"ships":9}}

### 2. Server connection (websocket) closed

- **How bad:** Minor (score 50), happened 3 times
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Later hits:** 05:39 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/ / 07:50 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Screenshot:** [006-start-PROBLEM-ws-closed.jpg](shots-iphone/006-start-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/006-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed

### 3. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/zuri.glb (Load request cancelled)
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
- **What happened:** https://www.heartbeatobservatory.com/homes/people/sunita.glb (Load request cancelled)
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
- **What happened:** https://www.heartbeatobservatory.com/homes/people/aoi.glb (Load request cancelled)
- **Screenshot:** [005-start-PROBLEM-request-failed.jpg](shots-iphone/005-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/005-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 8. Same sign text on 2 port signs: "marineris port"

- **How bad:** Small (score 22)
- **Where:** spots, first at 05:39 into the run, on iPhone (WebKit)
- **What happened:** beacon, arrivals-gantry

- **Steps to reproduce (what the bot did just before):**
  1. spots: 4 parked ships: courier@pad01, lifeboat@pad06, meridian@pad05, meridian@pad08
  1. spots: courier-pad01-cargo hinge -0.2,1.8,18.3 foot -0.2,-0.1,21.8 (foot height above ground should be ~0)
  1. spots: courier-pad01-airlock hinge 3.3,1.8,9.1 foot 6.4,-0.1,9.1 (foot height above ground should be ~0)
  1. spots note: model for meridian@pad08 not found (no ramp mesh check)
  1. spots: meridian-pad08-airlock ramp is raised, no walk views
  1. spots note: model for meridian@pad05 not found (no ramp mesh check)
  1. spots note: model for lifeboat@pad06 not found (no ramp mesh check)
  1. spots: lifeboat-pad06-airlock ramp is raised, no walk views

### 9. Same sign text on 2 port signs: "pad status"

- **How bad:** Small (score 22)
- **Where:** spots, first at 05:39 into the run, on iPhone (WebKit)
- **What happened:** padboard-02, padboard-03

- **Steps to reproduce (what the bot did just before):**
  1. spots: 4 parked ships: courier@pad01, lifeboat@pad06, meridian@pad05, meridian@pad08
  1. spots: courier-pad01-cargo hinge -0.2,1.8,18.3 foot -0.2,-0.1,21.8 (foot height above ground should be ~0)
  1. spots: courier-pad01-airlock hinge 3.3,1.8,9.1 foot 6.4,-0.1,9.1 (foot height above ground should be ~0)
  1. spots note: model for meridian@pad08 not found (no ramp mesh check)
  1. spots: meridian-pad08-airlock ramp is raised, no walk views
  1. spots note: model for meridian@pad05 not found (no ramp mesh check)
  1. spots note: model for lifeboat@pad06 not found (no ramp mesh check)
  1. spots: lifeboat-pad06-airlock ramp is raised, no walk views

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| spots | done - 68 spot shots (door 18, door-floor 3, ship 24, ramp 6, sign 8, night 9); 0 door overlaps; 4 ships. | 462 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / spots: typical 17 ms, slowest 6123 ms, 6 frames over 250 ms
- iphone / spots: typical 34 ms, slowest 4364 ms, 3 frames over 250 ms
- iphone / spots: typical 30 ms, slowest 3590 ms, 4 frames over 250 ms
- iphone / spots: typical 16 ms, slowest 3250 ms, 2 frames over 250 ms
- iphone / spots: typical 16 ms, slowest 3214 ms, 2 frames over 250 ms

## Trouble spot coverage

Spot shots by type: door 18, door-floor 3, ship 24, ramp 6, sign 8, night 9. Live inventory: 3 port doors, 9 pads, 4 parked ships (courier, meridian, meridian, lifeboat), 8 port signs. Each shot carries a what-to-look-for line for the vision review; targets and prompts are in spots.json.
Math findings (no picture needed): door opening vs prop boxes, duplicate door names, lowered ramp without a visible mesh, repeated sign text, interior door signs falling back to MEDBAY. Not yet covered: aboard views of interior doors (pipes/boards/glass across them), hull see-through is judged by the vision pass only, other ship types' interior sign lists.

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
