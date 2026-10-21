# The Cosmos playtest report

Run: 2026-10-04 20:06 (local)  |  Build under test: `2b7f021e4b775d0a8377`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 1.6 minutes, 67 screenshots, 15 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)

## Short version

15 distinct problems found: 0 blockers, 4 serious, 11 smaller.

- **Walkable cargo ramp on the courier has no visible mesh** (Serious)
- **Walkable airlock ramp on the courier has no visible mesh** (Serious)
- **Prop box overlaps the clear opening at Supply depot** (Serious, seen 2 times)
- **Prop box overlaps the clear opening at Port control** (Serious)
- **Frame-time spike during "spots"** (Annoying, seen 4 times)

## Problems, worst first

### 1. Walkable cargo ramp on the courier has no visible mesh

- **How bad:** Serious (score 85)
- **Where:** spots, first at 00:40 into the run, on iPhone (WebKit)
- **What happened:** courier-pad01-cargo: ramp is lowered (walkable) but no ramp object found under the ship model. You would float down it.

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts
  1. spots source inventory {"doors":3,"pads":9,"counts":{"portRooms":13,"pads":9,"ships":7}}
  1. spots: 3 parked ships: courier@pad01(remote), lifeboat@pad06(model not found), meridian@pad04(model not found)

### 2. Walkable airlock ramp on the courier has no visible mesh

- **How bad:** Serious (score 85)
- **Where:** spots, first at 00:40 into the run, on iPhone (WebKit)
- **What happened:** courier-pad01-airlock: ramp is lowered (walkable) but no ramp object found under the ship model. You would float down it.

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts
  1. spots source inventory {"doors":3,"pads":9,"counts":{"portRooms":13,"pads":9,"ships":7}}
  1. spots: 3 parked ships: courier@pad01(remote), lifeboat@pad06(model not found), meridian@pad04(model not found)

### 3. Prop box overlaps the clear opening at Supply depot

- **How bad:** Serious (score 78), happened 2 times
- **Where:** spots, first at 00:21 into the run, on iPhone (WebKit)
- **What happened:** Port collision box COS-MARS-STR-0110 intersects the door opening (cheap bounds check).
- **Later hits:** 00:21 Port collision box COS-MARS-STR-0110 intersects the door opening (cheap bounds check).

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts
  1. spots source inventory {"doors":3,"pads":9,"counts":{"portRooms":13,"pads":9,"ships":7}}

### 4. Prop box overlaps the clear opening at Port control

- **How bad:** Serious (score 78)
- **Where:** spots, first at 00:21 into the run, on iPhone (WebKit)
- **What happened:** Port collision box COS-MARS-STR-0112 intersects the door opening (cheap bounds check).

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts
  1. spots source inventory {"doors":3,"pads":9,"counts":{"portRooms":13,"pads":9,"ships":7}}

### 5. Frame-time spike during "spots"

- **How bad:** Annoying (score 62), happened 4 times
- **Where:** spots, first at 00:24 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 3318 ms (typical 17 ms); 6 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 01:04 a single frame took 3626 ms (typical 16 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 01:17 a single frame took 1237 ms (typical 33 ms); 7 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [013-spots-PROBLEM-frame-spike.jpg](shots-iphone/013-spots-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "spots"](shots-iphone/013-spots-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts
  1. spots source inventory {"doors":3,"pads":9,"counts":{"portRooms":13,"pads":9,"ships":7}}

### 6. Server connection (websocket) closed

- **How bad:** Minor (score 50), happened 3 times
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Later hits:** 00:53 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/ / 01:17 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Screenshot:** [008-start-PROBLEM-ws-closed.jpg](shots-iphone/008-start-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/008-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed

### 7. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/walter.glb (Load request cancelled)
- **Screenshot:** [001-start-PROBLEM-request-failed.jpg](shots-iphone/001-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/001-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 8. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/ada.glb (Load request cancelled)
- **Screenshot:** [002-start-PROBLEM-request-failed.jpg](shots-iphone/002-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/002-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 9. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/zuri.glb (Load request cancelled)
- **Screenshot:** [003-start-PROBLEM-request-failed.jpg](shots-iphone/003-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/003-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 10. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/sunita.glb (Load request cancelled)
- **Screenshot:** [004-start-PROBLEM-request-failed.jpg](shots-iphone/004-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/004-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 11. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/aoi.glb (Load request cancelled)
- **Screenshot:** [005-start-PROBLEM-request-failed.jpg](shots-iphone/005-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/005-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 12. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:08 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/jorge.glb (Load request cancelled)
- **Screenshot:** [006-start-PROBLEM-request-failed.jpg](shots-iphone/006-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/006-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 13. Same sign text on 2 port signs: "marineris port"

- **How bad:** Small (score 22)
- **Where:** spots, first at 00:53 into the run, on iPhone (WebKit)
- **What happened:** beacon, arrivals-gantry

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts
  1. spots source inventory {"doors":3,"pads":9,"counts":{"portRooms":13,"pads":9,"ships":7}}
  1. spots: 3 parked ships: courier@pad01(remote), lifeboat@pad06(model not found), meridian@pad04(model not found)
  1. spots note: lifeboat-pad06-cargo lowered but the ship model could not be found, mesh check skipped
  1. spots: lifeboat-pad06-airlock ramp is raised, no walk views
  1. spots note: meridian-pad04-cargo lowered but the ship model could not be found, mesh check skipped
  1. spots: meridian-pad04-airlock ramp is raised, no walk views

### 14. Same sign text on 2 port signs: "pad status"

- **How bad:** Small (score 22)
- **Where:** spots, first at 00:53 into the run, on iPhone (WebKit)
- **What happened:** padboard-02, padboard-03

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts
  1. spots source inventory {"doors":3,"pads":9,"counts":{"portRooms":13,"pads":9,"ships":7}}
  1. spots: 3 parked ships: courier@pad01(remote), lifeboat@pad06(model not found), meridian@pad04(model not found)
  1. spots note: lifeboat-pad06-cargo lowered but the ship model could not be found, mesh check skipped
  1. spots: lifeboat-pad06-airlock ramp is raised, no walk views
  1. spots note: meridian-pad04-cargo lowered but the ship model could not be found, mesh check skipped
  1. spots: meridian-pad04-airlock ramp is raised, no walk views

### Console warnings (1 kinds)

- person failed to load isaiah Error: THREE.GLTFLoader: WebP required by asset but unsupported. (x3)

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| spots | done - 56 spot shots (door 18, door-floor 3, ship 18, sign 8, night 9); 3 door overlaps; 3 ships. | 71 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / spots: typical 16 ms, slowest 4308 ms, 5 frames over 250 ms
- iphone / spots: typical 16 ms, slowest 3626 ms, 3 frames over 250 ms
- iphone / spots: typical 17 ms, slowest 3318 ms, 6 frames over 250 ms
- iphone / spots: typical 33 ms, slowest 1237 ms, 7 frames over 250 ms
- iphone / spots: typical 34 ms, slowest 476 ms, 3 frames over 250 ms

## Trouble spot coverage

Spot shots by type: door 18, door-floor 3, ship 18, sign 8, night 9. Live inventory: 3 port doors, 9 pads, 3 parked ships (courier, lifeboat, meridian), 8 port signs. Each shot carries a what-to-look-for line for the vision review; targets and prompts are in spots.json.
Math findings (no picture needed): door opening vs prop boxes, duplicate door names, lowered ramp without a visible mesh, repeated sign text, interior door signs falling back to MEDBAY. Not yet covered: aboard views of interior doors (pipes/boards/glass across them), hull see-through is judged by the vision pass only, other ship types' interior sign lists.

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
