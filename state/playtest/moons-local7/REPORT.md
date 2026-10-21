# The Cosmos playtest report

Run: 2026-10-03 08:48 (local)  |  Build under test: `974d3b8c679b23402a45`  |  Site: http://localhost:8461/?ws=ws://127.0.0.1:8463

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 10.8 minutes, 45 screenshots, 13 distinct problems

## Short version

13 distinct problems found: 1 blockers, 3 serious, 9 smaller.

- **Floating off the ground on a moon (airborne for 8+ seconds)** (BLOCKER, seen 7 times)
- **Nothing changed for 60+ seconds (same message, same place)** (Serious, seen 2 times)
- **Stuck while walking to back to the ship** (Serious)
- **Tapped Sit at the pilot seat, still standing** (Serious)
- **Could not walk to a wander on deimos** (Annoying)

## Problems, worst first

### 1. Floating off the ground on a moon (airborne for 8+ seconds)

- **How bad:** BLOCKER (score 90), happened 7 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 04:29 into the run, on iPhone (WebKit)
- **What happened:** walking on the moon, still airborne after 10 s, speed 3.24 m/s {"r":11921.53,"sampler":0.038,"shipGround":0.024,"vRad":1.45,"suitHold":0.8,"jump":0.6}
- **Later hits:** 04:32 walking on the moon, still airborne after 13 s, speed 2.06 m/s {"r":11925,"sampler":-0.024,"shipGround":-0.045,"vRad":0.735,"suitHold":0.8,"jump":0.6} / 04:34 walking on the moon, still airborne after 15 s, speed 4.22 m/s {"r":11927.27,"sampler":0.308,"shipGround":0.318,"vRad":-0.094,"suitHold":0.8,"jump":0.6}
- **Screenshot:** [024-fly-PROBLEM-floating-on-moon.jpg](shots-iphone/024-fly-PROBLEM-floating-on-moon.jpg)

  ![Floating off the ground on a moon (airbo](shots-iphone/024-fly-PROBLEM-floating-on-moon.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap button "Stand" (stand up)
  1. walk to off the ramp tip
  1. 1 sample sites known
  1. walk to core sample site S1
  1. tap #btn-action (action)
  1. walk to a wander on phobos
  1. jump
  1. walk to back to the ship

### 2. Nothing changed for 60+ seconds (same message, same place)

- **How bad:** Serious (score 86), happened 2 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 09:40 into the run, on iPhone (WebKit)
- **What happened:** in "fly": position {"x":5.5,"y":0,"z":14.9}, button "", caption "", toast "", ship aboard
- **Later hits:** 10:40 in "fly": position {"x":5.5,"y":0,"z":14.9}, button "", caption "", toast "", ship aboard
- **Screenshot:** [041-fly-PROBLEM-stuck-state.jpg](shots-iphone/041-fly-PROBLEM-stuck-state.jpg)

  ![Nothing changed for 60+ seconds (same me](shots-iphone/041-fly-PROBLEM-stuck-state.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. not getting closer (26 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (26 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. jump
  1. walk to back to the ship

### 3. Stuck while walking to back to the ship

- **How bad:** Serious (score 80)
- **Where:** boarding the ship, taking a seat and flying a course, first at 10:48 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at shipworld 6,15 (target 0,28, 14 m away)
- **Screenshot:** [044-fly-PROBLEM-stuck-walking.jpg](shots-iphone/044-fly-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to back to the ship](shots-iphone/044-fly-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (14 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (14 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. not getting closer (14 m away), trying to get unstuck #6
  1. not getting closer (14 m away), trying to get unstuck #7
  1. not getting closer (14 m away), trying to get unstuck #8

### 4. Tapped Sit at the pilot seat, still standing

- **How bad:** Serious (score 76)
- **Where:** boarding the ship, taking a seat and flying a course, first at 00:30 into the run, on iPhone (WebKit)
- **What happened:** button "Sit  ·  Pilot seat"
- **Screenshot:** [009-fly-PROBLEM-sit-failed.jpg](shots-iphone/009-fly-PROBLEM-sit-failed.jpg)

  ![Tapped Sit at the pilot seat, still stan](shots-iphone/009-fly-PROBLEM-sit-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open ws://127.0.0.1:8463/
  1. websocket closed
  1. websocket open ws://127.0.0.1:8463/
  1. === phase fly starts
  1. ship type meridian; ship centre at port 0,0; ramp foot 0,30
  1. button near seat: "Sit  ·  Pilot seat"
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)

### 5. Could not walk to a wander on deimos

- **How bad:** Annoying (score 72)
- **Where:** boarding the ship, taking a seat and flying a course, first at 09:33 into the run, on iPhone (WebKit)
- **What happened:** gave up after 60s; last distance 26 m
- **Screenshot:** [039-fly-PROBLEM-cannot-reach.jpg](shots-iphone/039-fly-PROBLEM-cannot-reach.jpg)

  ![Could not walk to a wander on deimos](shots-iphone/039-fly-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (26 m away), trying to get unstuck #3
  1. run-up jump #3
  1. jump
  1. not getting closer (26 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (26 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way

### 6. Frame-time spike during "fly"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 00:17 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 3564 ms (typical 28 ms); 6 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 02:27 a single frame took 831 ms (typical 33 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [008-fly-PROBLEM-frame-spike.jpg](shots-iphone/008-fly-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "fly"](shots-iphone/008-fly-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off
  1. websocket open ws://127.0.0.1:8463/
  1. websocket closed
  1. websocket open ws://127.0.0.1:8463/
  1. === phase fly starts
  1. ship type meridian; ship centre at port 0,0; ramp foot 0,30

### 7. Console error

- **How bad:** Annoying (score 55), happened 4 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** Failed to load resource: the server responded with a status of 404 (Not Found)
- **Later hits:** 00:01 Failed to load resource: the server responded with a status of 404 (Not Found) / 00:05 Failed to load resource: the server responded with a status of 404 (Not Found)
- **Screenshot:** [002-start-PROBLEM-console-error.jpg](shots-iphone/002-start-PROBLEM-console-error.jpg)

  ![Console error](shots-iphone/002-start-PROBLEM-console-error.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 8. Request returned HTTP 404

- **How bad:** Minor (score 50), happened 2 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/_vercel/insights/script.js
- **Later hits:** 00:05 http://localhost:8461/_vercel/insights/script.js
- **Screenshot:** [001-start-PROBLEM-http.jpg](shots-iphone/001-start-PROBLEM-http.jpg)

  ![Request returned HTTP 404](shots-iphone/001-start-PROBLEM-http.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 9. Request returned HTTP 404

- **How bad:** Minor (score 50), happened 2 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/hb-editor.js
- **Later hits:** 00:05 http://localhost:8461/hb-editor.js
- **Screenshot:** [004-start-PROBLEM-http.jpg](shots-iphone/004-start-PROBLEM-http.jpg)

  ![Request returned HTTP 404](shots-iphone/004-start-PROBLEM-http.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 10. Server connection (websocket) closed

- **How bad:** Minor (score 50)
- **Where:** loading the page, first at 00:05 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: ws://127.0.0.1:8463/
- **Screenshot:** [006-start-PROBLEM-ws-closed.jpg](shots-iphone/006-start-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/006-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off
  1. websocket open ws://127.0.0.1:8463/
  1. websocket closed

### 11. A request failed to load

- **How bad:** Minor (score 45), happened 2 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/_vercel/insights/script.js (Load request cancelled)
- **Later hits:** 00:05 http://localhost:8461/_vercel/insights/script.js (Load request cancelled)
- **Screenshot:** [003-start-PROBLEM-request-failed.jpg](shots-iphone/003-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/003-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 12. A request failed to load

- **How bad:** Minor (score 45), happened 2 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/hb-editor.js (Load request cancelled)
- **Later hits:** 00:05 http://localhost:8461/hb-editor.js (Load request cancelled)
- **Screenshot:** [005-start-PROBLEM-request-failed.jpg](shots-iphone/005-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/005-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 13. Game said: "Cruise: raiders cannot follow a ship at this speed"

- **How bad:** Minor (score 42), happened 2 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 01:17 into the run, on iPhone (WebKit)
- **What happened:** shown in hud-readout while the bot was: 01:16 [fly] tap button "×60" (speed up ×60)
- **Later hits:** 06:02 shown in hud-readout while the bot was: 06:01 [fly] tap button "×60" (speed up ×60)
- **Screenshot:** [015-fly-PROBLEM-refusal-message.jpg](shots-iphone/015-fly-PROBLEM-refusal-message.jpg)

  ![Game said: "Cruise: raiders cannot follo](shots-iphone/015-fly-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap button "×60" (speed up ×60)
  1. tap button "×5" (speed up ×5)
  1. trip phase ascent, warp x5, eta 0s
  1. tap button "×60" (speed up ×60)
  1. tap button "×5" (speed up ×5)
  1. tap button "×20" (speed up ×20)
  1. trip phase transit, warp x20, eta 1682s
  1. tap button "×60" (speed up ×60)

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| boarding the ship, taking a seat and flying a course | done | 634 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: started; Deimos: started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / fly: typical 28 ms, slowest 3564 ms, 6 frames over 250 ms
- iphone / fly: typical 33 ms, slowest 831 ms, 1 frames over 250 ms
- iphone / fly: typical 28 ms, slowest 681 ms, 1 frames over 250 ms
- iphone / fly: typical 27 ms, slowest 389 ms, 1 frames over 250 ms
- iphone / fly: typical 30 ms, slowest 359 ms, 1 frames over 250 ms

Button response time (tap to something changing on screen): median 330 ms, slowest 330 ms over 2 taps.

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
