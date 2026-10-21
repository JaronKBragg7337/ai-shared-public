# The Cosmos playtest report

Run: 2026-10-04 22:31 (local)  |  Build under test: `f0c52161e2d69006af95`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 15.8 minutes, 191 screenshots, 16 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)

## Short version

16 distinct problems found: 0 blockers, 3 serious, 13 smaller.

- **Nothing changed for 60+ seconds (same message, same place)** (Serious, seen 10 times)
- **Game said: "fetch failed"** (Serious, seen 2 times)
- **suitrack in airlock sits in the clear opening of door d_airlock_out (GANGWAY) inside the Wayfarer** (Serious)
- **wall screen scr_eng_wall in engineering sits in the clear opening of door d_eng_fore (ENGINEERING) inside the MSV Meridian** (Annoying)
- **wall screen scr_eng_wall in engine sits in the clear opening of door d_engine (ENGINE) inside the Shrike raider** (Annoying)

## Problems, worst first

### 1. Nothing changed for 60+ seconds (same message, same place)

- **How bad:** Serious (score 86), happened 10 times
- **Where:** spots, first at 04:53 into the run, on iPhone (WebKit)
- **What happened:** in "spots": position {"x":6622.2,"y":-3397245.8,"z":6622.2}, button "", caption "", toast "", ship outside
- **Later hits:** 06:34 in "spots": position {"x":6622.2,"y":-3397245.8,"z":6622.2}, button "", caption "", toast "", ship outside / 07:35 in "spots": position {"x":6622.2,"y":-3397245.8,"z":6622.2}, button "", caption "", toast "", ship outside
- **Screenshot:** [136-spots-PROBLEM-stuck-state.jpg](shots-iphone/136-spots-PROBLEM-stuck-state.jpg)

  ![Nothing changed for 60+ seconds (same me](shots-iphone/136-spots-PROBLEM-stuck-state.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. spots: server copy did not confirm the move to door Supply depot-1.5m-open (5s)
  1. spots: server copy did not confirm the move to door-floor Supply depot-looking-down-through-opening (5s)
  1. spots: server copy did not confirm the move to door Port control-15m-shut (13s)
  1. spots: server copy did not confirm the move to door Port control-15m-open (5s)
  1. spots: server copy did not confirm the move to door Port control-5m-shut (6s)
  1. spots: server copy did not confirm the move to door Port control-5m-open (5s)
  1. spots: server copy did not confirm the move to door Port control-1.5m-shut (5s)
  1. spots: server copy did not confirm the move to door Port control-1.5m-open (5s)

### 2. Game said: "fetch failed"

- **How bad:** Serious (score 80), happened 2 times
- **Where:** spots, first at 02:18 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 01:58 [spots] spots inside: Ares (liner): 73 shots, 18 doors, 17 rooms
- **Later hits:** 05:29 shown in opening-caption while the bot was: 05:25 [spots] spots: server copy did not confirm the move to door Crew hall-5m-open (5s)
- **Screenshot:** [098-spots-PROBLEM-refusal-message.jpg](shots-iphone/098-spots-PROBLEM-refusal-message.jpg)

  ![Game said: "fetch failed"](shots-iphone/098-spots-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts
  1. spots inside: Ares (liner): 73 shots, 18 doors, 17 rooms

### 3. suitrack in airlock sits in the clear opening of door d_airlock_out (GANGWAY) inside the Wayfarer

- **How bad:** Serious (score 78)
- **Where:** spots, first at 00:40 into the run, on iPhone (WebKit)
- **What happened:** Layout bounds check: door x=3.5, centre 1.4, width 1.3.

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts

### 4. wall screen scr_eng_wall in engineering sits in the clear opening of door d_eng_fore (ENGINEERING) inside the MSV Meridian

- **How bad:** Annoying (score 66)
- **Where:** spots, first at 00:40 into the run, on iPhone (WebKit)
- **What happened:** Layout bounds check: door z=-7.1, centre 0, width 1.

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts

### 5. wall screen scr_eng_wall in engine sits in the clear opening of door d_engine (ENGINE) inside the Shrike raider

- **How bad:** Annoying (score 66)
- **Where:** spots, first at 00:40 into the run, on iPhone (WebKit)
- **What happened:** Layout bounds check: door z=4.5, centre 0, width 1.

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts

### 6. wall screen scr_eng_wall in engine sits in the clear opening of door d_engine (ENGINE) inside the Drayman

- **How bad:** Annoying (score 66)
- **Where:** spots, first at 00:40 into the run, on iPhone (WebKit)
- **What happened:** Layout bounds check: door z=7.1, centre 0, width 1.

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts

### 7. Frame-time spike during "spots"

- **How bad:** Annoying (score 62), happened 7 times
- **Where:** spots, first at 00:42 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 8195 ms (typical 16 ms); 6 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 02:51 a single frame took 3421 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 03:05 a single frame took 4888 ms (typical 18 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [007-spots-PROBLEM-frame-spike.jpg](shots-iphone/007-spots-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "spots"](shots-iphone/007-spots-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts

### 8. Server connection (websocket) closed

- **How bad:** Minor (score 50), happened 4 times
- **Where:** loading the page, first at 00:14 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Later hits:** 02:43 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/ / 13:29 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Screenshot:** [005-start-PROBLEM-ws-closed.jpg](shots-iphone/005-start-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/005-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed

### 9. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:11 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/walter.glb (Load request cancelled)
- **Screenshot:** [001-start-PROBLEM-request-failed.jpg](shots-iphone/001-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/001-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 10. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:11 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/aoi.glb (Load request cancelled)
- **Screenshot:** [002-start-PROBLEM-request-failed.jpg](shots-iphone/002-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/002-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 11. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:11 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/ada.glb (Load request cancelled)
- **Screenshot:** [003-start-PROBLEM-request-failed.jpg](shots-iphone/003-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/003-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 12. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:11 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/sunita.glb (Load request cancelled)
- **Screenshot:** [004-start-PROBLEM-request-failed.jpg](shots-iphone/004-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/004-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 13. Door label "CARGO" used on 2 doors inside the MSV Meridian

- **How bad:** Minor (score 42)
- **Where:** spots, first at 00:40 into the run, on iPhone (WebKit)
- **What happened:** d_cargo, d_cargo_up

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts

### 14. Same sign text on 2 port signs: "marineris port"

- **How bad:** Small (score 22)
- **Where:** spots, first at 13:29 into the run, on iPhone (WebKit)
- **What happened:** beacon, arrivals-gantry

- **Steps to reproduce (what the bot did just before):**
  1. spots: server copy did not confirm the move to sign Supply-depot-sign (45s)
  1. spots: server copy did not confirm the move to sign Port-control-sign (11s)
  1. spots: server copy did not confirm the move to sign Crew-hall-sign (10s)
  1. spots: server copy did not confirm the move to sign beacon (20s)
  1. spots: server copy did not confirm the move to sign arrivals-gantry (12s)
  1. spots: server copy did not confirm the move to sign padboard-01 (13s)
  1. spots: server copy did not confirm the move to sign padboard-02 (13s)
  1. spots: server copy did not confirm the move to sign padboard-03 (11s)

### 15. Same sign text on 2 port signs: "pad status"

- **How bad:** Small (score 22)
- **Where:** spots, first at 13:29 into the run, on iPhone (WebKit)
- **What happened:** padboard-02, padboard-03

- **Steps to reproduce (what the bot did just before):**
  1. spots: server copy did not confirm the move to sign Supply-depot-sign (45s)
  1. spots: server copy did not confirm the move to sign Port-control-sign (11s)
  1. spots: server copy did not confirm the move to sign Crew-hall-sign (10s)
  1. spots: server copy did not confirm the move to sign beacon (20s)
  1. spots: server copy did not confirm the move to sign arrivals-gantry (12s)
  1. spots: server copy did not confirm the move to sign padboard-01 (13s)
  1. spots: server copy did not confirm the move to sign padboard-02 (13s)
  1. spots: server copy did not confirm the move to sign padboard-03 (11s)

### 16. Could not get the port to night for the night views

- **How bad:** Small (score 20)
- **Where:** spots, first at 13:52 into the run, on iPhone (WebKit)
- **What happened:** port.night = 0 after ?sky=night

- **Steps to reproduce (what the bot did just before):**
  1. spots: server copy did not confirm the move to sign padboard-01 (13s)
  1. spots: server copy did not confirm the move to sign padboard-02 (13s)
  1. spots: server copy did not confirm the move to sign padboard-03 (11s)
  1. spots note: interior door sign list not reachable (cosmos.ship.layout / signs.uvFor); interior doors need an aboard pass
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&build=2b7f021e4b775d0a8377&opening=off&sky=night
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. spots: night level 0 after sky=night

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| spots | done - 181 spot shots (inside 114, door 18, door-floor 3, ship 30, ramp 3, sign 8, night 5); 0 door overlaps; 5 ships. | 909 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / spots: typical 33 ms, slowest 8932 ms, 2 frames over 250 ms
- iphone / spots: typical 16 ms, slowest 8195 ms, 6 frames over 250 ms
- iphone / spots: typical 30 ms, slowest 6022 ms, 3 frames over 250 ms
- iphone / spots: typical 16 ms, slowest 5195 ms, 2 frames over 250 ms
- iphone / spots: typical 18 ms, slowest 4888 ms, 2 frames over 250 ms

## Trouble spot coverage

Spot shots by type: inside 114, door 18, door-floor 3, ship 30, ramp 3, sign 8, night 5. Live inventory: 3 port doors, 9 pads, 5 parked ships (courier, meridian, lifeboat, lifeboat, lifeboat), 8 port signs. Each shot carries a what-to-look-for line for the vision review; targets and prompts are in spots.json.
Math findings (no picture needed): door opening vs prop boxes, duplicate door names, lowered ramp without a visible mesh, repeated sign text, interior door signs falling back to MEDBAY. Inside the ships (aboard, doors at 5 m and 1.5 m, cockpit looking back, each room from its doorway): Hellas Dawn (Ares liner) 73 shots, Kestrel (Soft Landing) 41 shots; layouts checked by math only: meridian, raider, courier, hauler, lifeboat, bulker, escort. Not yet covered: boarding ships the player does not own (the Meridian), posters over doors, hull see-through is judged by the vision pass only.

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
