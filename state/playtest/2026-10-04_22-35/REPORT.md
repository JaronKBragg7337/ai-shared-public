# The Cosmos playtest report

Run: 2026-10-04 22:35 (local)  |  Build under test: `f0c52161e2d69006af95`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 3.4 minutes, 144 screenshots, 12 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)

## Short version

12 distinct problems found: 0 blockers, 2 serious, 10 smaller.

- **Nothing changed for 60+ seconds (same message, same place)** (Serious)
- **suitrack in airlock sits in the clear opening of door d_airlock_out (GANGWAY) inside the Wayfarer** (Serious)
- **wall screen scr_eng_wall in engineering sits in the clear opening of door d_eng_fore (ENGINEERING) inside the MSV Meridian** (Annoying)
- **wall screen scr_eng_wall in engine sits in the clear opening of door d_engine (ENGINE) inside the Shrike raider** (Annoying)
- **wall screen scr_eng_wall in engine sits in the clear opening of door d_engine (ENGINE) inside the Drayman** (Annoying)

## Problems, worst first

### 1. Nothing changed for 60+ seconds (same message, same place)

- **How bad:** Serious (score 86)
- **Where:** spots, first at 02:53 into the run, on iPhone (WebKit)
- **What happened:** in "spots": position {"x":6622.2,"y":-3397245.8,"z":6622.2}, button "", caption "", toast "", ship outside
- **Screenshot:** [136-spots-PROBLEM-stuck-state.jpg](shots-iphone/136-spots-PROBLEM-stuck-state.jpg)

  ![Nothing changed for 60+ seconds (same me](shots-iphone/136-spots-PROBLEM-stuck-state.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts
  1. spots inside: Ares (liner): 73 shots, 18 doors, 17 rooms
  1. spots inside: Kestrel (kestrel): 41 shots, 10 doors, 9 rooms
  1. spots inside: no standing room in front of door d_lock_out

### 2. suitrack in airlock sits in the clear opening of door d_airlock_out (GANGWAY) inside the Wayfarer

- **How bad:** Serious (score 78)
- **Where:** spots, first at 00:31 into the run, on iPhone (WebKit)
- **What happened:** Layout bounds check: door x=3.5, centre 1.4, width 1.3.

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts

### 3. wall screen scr_eng_wall in engineering sits in the clear opening of door d_eng_fore (ENGINEERING) inside the MSV Meridian

- **How bad:** Annoying (score 66)
- **Where:** spots, first at 00:31 into the run, on iPhone (WebKit)
- **What happened:** Layout bounds check: door z=-7.1, centre 0, width 1.

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts

### 4. wall screen scr_eng_wall in engine sits in the clear opening of door d_engine (ENGINE) inside the Shrike raider

- **How bad:** Annoying (score 66)
- **Where:** spots, first at 00:31 into the run, on iPhone (WebKit)
- **What happened:** Layout bounds check: door z=4.5, centre 0, width 1.

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts

### 5. wall screen scr_eng_wall in engine sits in the clear opening of door d_engine (ENGINE) inside the Drayman

- **How bad:** Annoying (score 66)
- **Where:** spots, first at 00:31 into the run, on iPhone (WebKit)
- **What happened:** Layout bounds check: door z=7.1, centre 0, width 1.

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts

### 6. Frame-time spike during "spots"

- **How bad:** Annoying (score 62), happened 3 times
- **Where:** spots, first at 00:34 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 5866 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 03:11 a single frame took 4227 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 03:19 a single frame took 4212 ms (typical 29 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [007-spots-PROBLEM-frame-spike.jpg](shots-iphone/007-spots-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "spots"](shots-iphone/007-spots-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts

### 7. Server connection (websocket) closed

- **How bad:** Minor (score 50), happened 2 times
- **Where:** loading the page, first at 00:12 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Later hits:** 03:00 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Screenshot:** [005-start-PROBLEM-ws-closed.jpg](shots-iphone/005-start-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/005-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed

### 8. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:10 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/walter.glb (Load request cancelled)
- **Screenshot:** [001-start-PROBLEM-request-failed.jpg](shots-iphone/001-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/001-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 9. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:10 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/sunita.glb (Load request cancelled)
- **Screenshot:** [002-start-PROBLEM-request-failed.jpg](shots-iphone/002-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/002-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 10. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:10 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/ada.glb (Load request cancelled)
- **Screenshot:** [003-start-PROBLEM-request-failed.jpg](shots-iphone/003-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/003-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 11. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:10 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/aoi.glb (Load request cancelled)
- **Screenshot:** [004-start-PROBLEM-request-failed.jpg](shots-iphone/004-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/004-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 12. Door label "CARGO" used on 2 doors inside the MSV Meridian

- **How bad:** Minor (score 42)
- **Where:** spots, first at 00:31 into the run, on iPhone (WebKit)
- **What happened:** d_cargo, d_cargo_up

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| spots | done - inside-the-ships only: 135 shots | 168 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / spots: typical 16 ms, slowest 5866 ms, 5 frames over 250 ms
- iphone / spots: typical 16 ms, slowest 4227 ms, 2 frames over 250 ms
- iphone / spots: typical 29 ms, slowest 4212 ms, 2 frames over 250 ms
- iphone / spots: typical 26 ms, slowest 357 ms, 1 frames over 250 ms
- iphone / spots: typical 24 ms, slowest 169 ms, 0 frames over 250 ms

## Trouble spot coverage

Spot shots by type: inside 135. Live inventory: 0 port doors, 0 pads, 0 parked ships (), 0 port signs. Each shot carries a what-to-look-for line for the vision review; targets and prompts are in spots.json.
Math findings (no picture needed): door opening vs prop boxes, duplicate door names, lowered ramp without a visible mesh, repeated sign text, interior door signs falling back to MEDBAY. Inside the ships (aboard, doors at 5 m and 1.5 m, cockpit looking back, each room from its doorway): Hellas Dawn (Ares liner) 73 shots, Kestrel (Soft Landing) 41 shots, Skiff (lifeboat) 21 shots; layouts checked by math only: meridian, raider, courier, hauler, bulker, escort. Not yet covered: boarding ships the player does not own (the Meridian), posters over doors, hull see-through is judged by the vision pass only.

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
