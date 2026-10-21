# The Cosmos playtest report

Run: 2026-10-03 09:00 (local)  |  Build under test: `974d3b8c679b23402a45`  |  Site: http://localhost:8461/?ws=ws://127.0.0.1:8463

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 11 minutes, 57 screenshots, 24 distinct problems

## Short version

15 distinct problems found: 1 blockers, 3 serious, 11 smaller.

- **Floating off the ground on a moon (airborne for 8+ seconds)** (BLOCKER, seen 18 times)
- **Nothing changed for 60+ seconds (same message, same place)** (Serious)
- **Stuck while walking to back to the ship** (Serious)
- **Stuck on a walking route: pilot seat route** (Serious)
- **Could not walk to a wander on deimos** (Annoying)

## Problems, worst first

### 1. Floating off the ground on a moon (airborne for 8+ seconds)

- **How bad:** BLOCKER (score 90), happened 18 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 05:13 into the run, on iPhone (WebKit)
- **What happened:** walking on the moon, still airborne after 10 s, speed 4.03 m/s {"r":11972.79,"sampler":-0.061,"shipGround":-0.054,"vRad":0.613,"suitHold":0.8,"jump":0.6}
- **Later hits:** 05:16 walking on the moon, still airborne after 13 s, speed 3.61 m/s {"r":11975.76,"sampler":-0.037,"shipGround":-0.052,"vRad":0.665,"suitHold":0.8,"jump":0.6} / 05:19 walking on the moon, still airborne after 15 s, speed 3.79 m/s {"r":11978.75,"sampler":-0.036,"shipGround":-0.003,"vRad":0.701,"suitHold":0.8,"jump":0.6}
- **Screenshot:** [025-fly-PROBLEM-floating-on-moon.jpg](shots-iphone/025-fly-PROBLEM-floating-on-moon.jpg)

  ![Floating off the ground on a moon (airbo](shots-iphone/025-fly-PROBLEM-floating-on-moon.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to off the ramp tip
  1. 1 sample sites known
  1. walk to core sample site S1
  1. tap #btn-action (action)
  1. walk to a wander on phobos
  1. jump
  1. walk to back to the ship
  1. AIRTRACE [grounded-before, grounded-after, dist-to-drawn-ground, radial-vel, moving, pushOut]: [[0,0,0.034,0.725,1,0.12],[0,0,0.02,0.713,1,0.12],[0,0,0.006,0.7,1,0.12],[0,0,-0.008,0.688,1,0.12],[0,0,-0.02,0.671,1,0.12],[0,0,-0.039,0.661,1,0.12],[0,0,-0.051,0.639,1,0.12],[0,0,-0.077,1.474,1,0.06],[0,0,-0.026,0.75,1,0.06],[0,0,-0.036,0.737,1,0.06],[0,0,-0.047,0.724,1,0.06],[0,0,-0.057,0.712,1,0.06],[0,0,-0.065,1.315,1,0.06],[0,0,-0.008,0.75,1,0.06],[0,0,-0.015,0.738,1,0.06],[0,0,-0.022,0.725,1,0.06],[0,0,-0.031,0.709,1,0.06],[0,0,-0.042,0.7,1,0.06],[0,0,-0.048,0.688,1,0.06],[0,0,-0.058,0.674,1,0.06],[0,0,-0.069,0.651,1,0.06],[0,0,-0.093,1.154,1,0.12],[0,0,0.026,0.75,1,0.12],[0,0,0.006,0.737,1,0.12],[0,0,-0.005,0.725,1,0.12],[0,0,-0.013,0.712,1,0.12],[0,0,-0.023,0.688,1,0.12],[0,0,-0.044,0.675,1,0.12],[0,0,-0.058,0.663,1,0.12],[0,0,-0.072,1.401,1,0.06],[0,0,-0.019,0.75,1,0.06],[0,0,-0.031,0.74,1,0.06],[0,0,-0.039,0.728,1,0.06],[0,0,-0.05,1.237,1,0.06],[0,0,0.005,0.75,1,0.06],[0,0,-0.005,0.727,1,0.06],[0,0,-0.024,0.714,1,0.06],[0,0,-0.034,0.701,1,0.06],[0,0,-0.045,0.689,1,0.06],[0,0,-0.055,0.677,1,0.06]]

### 2. Nothing changed for 60+ seconds (same message, same place)

- **How bad:** Serious (score 86)
- **Where:** boarding the ship, taking a seat and flying a course, first at 10:47 into the run, on iPhone (WebKit)
- **What happened:** in "fly": position {"x":5.5,"y":0,"z":14.9}, button "", caption "", toast "", ship aboard
- **Screenshot:** [055-fly-PROBLEM-stuck-state.jpg](shots-iphone/055-fly-PROBLEM-stuck-state.jpg)

  ![Nothing changed for 60+ seconds (same me](shots-iphone/055-fly-PROBLEM-stuck-state.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #3
  1. jump
  1. not getting closer (14 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (14 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. not getting closer (14 m away), trying to get unstuck #6

### 3. Stuck while walking to back to the ship

- **How bad:** Serious (score 80)
- **Where:** boarding the ship, taking a seat and flying a course, first at 11:01 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at shipworld 6,15 (target 0,28, 14 m away)
- **Screenshot:** [056-fly-PROBLEM-stuck-walking.jpg](shots-iphone/056-fly-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to back to the ship](shots-iphone/056-fly-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (14 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (14 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. not getting closer (14 m away), trying to get unstuck #6
  1. not getting closer (14 m away), trying to get unstuck #7
  1. not getting closer (14 m away), trying to get unstuck #8

### 4. Stuck on a walking route: pilot seat route

- **How bad:** Serious (score 78)
- **Where:** boarding the ship, taking a seat and flying a course, first at 06:31 into the run, on iPhone (WebKit)
- **What happened:** at -0.4,10.1 (y 3), 26 m from the end
- **Screenshot:** [028-fly-PROBLEM-stuck-walking.jpg](shots-iphone/028-fly-PROBLEM-stuck-walking.jpg)

  ![Stuck on a walking route: pilot seat rou](shots-iphone/028-fly-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. walk to back to the ship
  1. AIRTRACE [grounded-before, grounded-after, dist-to-drawn-ground, radial-vel, moving, pushOut]: [[0,0,0.034,0.725,1,0.12],[0,0,0.02,0.713,1,0.12],[0,0,0.006,0.7,1,0.12],[0,0,-0.008,0.688,1,0.12],[0,0,-0.02,0.671,1,0.12],[0,0,-0.039,0.661,1,0.12],[0,0,-0.051,0.639,1,0.12],[0,0,-0.077,1.474,1,0.06],[0,0,-0.026,0.75,1,0.06],[0,0,-0.036,0.737,1,0.06],[0,0,-0.047,0.724,1,0.06],[0,0,-0.057,0.712,1,0.06],[0,0,-0.065,1.315,1,0.06],[0,0,-0.008,0.75,1,0.06],[0,0,-0.015,0.738,1,0.06],[0,0,-0.022,0.725,1,0.06],[0,0,-0.031,0.709,1,0.06],[0,0,-0.042,0.7,1,0.06],[0,0,-0.048,0.688,1,0.06],[0,0,-0.058,0.674,1,0.06],[0,0,-0.069,0.651,1,0.06],[0,0,-0.093,1.154,1,0.12],[0,0,0.026,0.75,1,0.12],[0,0,0.006,0.737,1,0.12],[0,0,-0.005,0.725,1,0.12],[0,0,-0.013,0.712,1,0.12],[0,0,-0.023,0.688,1,0.12],[0,0,-0.044,0.675,1,0.12],[0,0,-0.058,0.663,1,0.12],[0,0,-0.072,1.401,1,0.06],[0,0,-0.019,0.75,1,0.06],[0,0,-0.031,0.74,1,0.06],[0,0,-0.039,0.728,1,0.06],[0,0,-0.05,1.237,1,0.06],[0,0,0.005,0.75,1,0.06],[0,0,-0.005,0.727,1,0.06],[0,0,-0.024,0.714,1,0.06],[0,0,-0.034,0.701,1,0.06],[0,0,-0.045,0.689,1,0.06],[0,0,-0.055,0.677,1,0.06]]
  1. walk to up the ramp (moon)
  1. jump
  1. jump
  1. jump
  1. jump

### 5. Could not walk to a wander on deimos

- **How bad:** Annoying (score 72)
- **Where:** boarding the ship, taking a seat and flying a course, first at 09:45 into the run, on iPhone (WebKit)
- **What happened:** gave up after 60s; last distance 26 m
- **Screenshot:** [051-fly-PROBLEM-cannot-reach.jpg](shots-iphone/051-fly-PROBLEM-cannot-reach.jpg)

  ![Could not walk to a wander on deimos](shots-iphone/051-fly-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (26 m away), trying to get unstuck #3
  1. run-up jump #3
  1. jump
  1. not getting closer (26 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (26 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way

### 6. Buttons are covered by something on top of them (7 places)

- **How bad:** Annoying (score 68), happened 7 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 06:41 into the run, on iPhone (WebKit)
- **What happened:** #chip-range "Range" is covered by button.go ;  #chip-course "Course" is covered by button.go ;  #chip-jobs "Jobs" is covered by button.go ;  #chip-range "Range" is covered by button.wp ;  #chip-course "Course" is covered by div.row ;  #chip-jobs "Jobs" is covered by button.wp ;  #chip-jobs "Jobs" is covered by button.wp on
- **Screenshot:** [031-fly-PROBLEM-covered.jpg](shots-iphone/031-fly-PROBLEM-covered.jpg)

  ![Buttons are covered by something on top ](shots-iphone/031-fly-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. jump
  1. jump
  1. button near seat: "Sit  ·  Navigation"
  1. tap #btn-action (action)
  1. seated: nav
  1. mis-tap beside #chip-course
  1. tap #chip-course (open the Course sheet)

### 7. Buttons overlap each other (4 places)

- **How bad:** Annoying (score 66), happened 4 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 06:47 into the run, on iPhone (WebKit)
- **What happened:** #chip-range "Range" overlaps  "×1" by 48% ;  #chip-course "Course" overlaps  "×5" by 31% ;  #chip-course "Course" overlaps  "×20" by 34% ;  #chip-jobs "Jobs" overlaps  "×60" by 48%
- **Screenshot:** [035-fly-PROBLEM-overlap.jpg](shots-iphone/035-fly-PROBLEM-overlap.jpg)

  ![Buttons overlap each other (4 places)](shots-iphone/035-fly-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-action (action)
  1. seated: nav
  1. mis-tap beside #chip-course
  1. tap #chip-course (open the Course sheet)
  1. tap button "Deimos15000 km · about 111 h 10 minThe o" (choose Deimos)
  1. trip started: {"phase":"lift","dest":"Deimos (pad 03)","warp":1,"eta":0,"dist":0}
  1. trip phase lift, warp x1, eta 0s
  1. tap button "×5" (speed up ×5)

### 8. Console error

- **How bad:** Annoying (score 55), happened 4 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** Failed to load resource: the server responded with a status of 404 (Not Found)
- **Later hits:** 00:01 Failed to load resource: the server responded with a status of 404 (Not Found) / 00:04 Failed to load resource: the server responded with a status of 404 (Not Found)
- **Screenshot:** [002-start-PROBLEM-console-error.jpg](shots-iphone/002-start-PROBLEM-console-error.jpg)

  ![Console error](shots-iphone/002-start-PROBLEM-console-error.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 9. Request returned HTTP 404

- **How bad:** Minor (score 50), happened 2 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/_vercel/insights/script.js
- **Later hits:** 00:04 http://localhost:8461/_vercel/insights/script.js
- **Screenshot:** [001-start-PROBLEM-http.jpg](shots-iphone/001-start-PROBLEM-http.jpg)

  ![Request returned HTTP 404](shots-iphone/001-start-PROBLEM-http.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 10. Request returned HTTP 404

- **How bad:** Minor (score 50), happened 2 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/hb-editor.js
- **Later hits:** 00:04 http://localhost:8461/hb-editor.js
- **Screenshot:** [004-start-PROBLEM-http.jpg](shots-iphone/004-start-PROBLEM-http.jpg)

  ![Request returned HTTP 404](shots-iphone/004-start-PROBLEM-http.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 11. Server connection (websocket) closed

- **How bad:** Minor (score 50)
- **Where:** loading the page, first at 00:04 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: ws://127.0.0.1:8463/
- **Screenshot:** [006-start-PROBLEM-ws-closed.jpg](shots-iphone/006-start-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/006-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off
  1. websocket open ws://127.0.0.1:8463/
  1. websocket closed

### 12. A request failed to load

- **How bad:** Minor (score 45), happened 2 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/_vercel/insights/script.js (Load request cancelled)
- **Later hits:** 00:04 http://localhost:8461/_vercel/insights/script.js (Load request cancelled)
- **Screenshot:** [003-start-PROBLEM-request-failed.jpg](shots-iphone/003-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/003-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 13. A request failed to load

- **How bad:** Minor (score 45), happened 2 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/hb-editor.js (Load request cancelled)
- **Later hits:** 00:04 http://localhost:8461/hb-editor.js (Load request cancelled)
- **Screenshot:** [005-start-PROBLEM-request-failed.jpg](shots-iphone/005-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/005-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 14. Game said: "Cruise: raiders cannot follow a ship at this speed"

- **How bad:** Minor (score 42), happened 2 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 01:05 into the run, on iPhone (WebKit)
- **What happened:** shown in hud-readout while the bot was: 01:05 [fly] trip phase transit, warp x60, eta 1679s
- **Later hits:** 07:07 shown in hud-readout while the bot was: 07:06 [fly] tap button "×20" (speed up ×20)
- **Screenshot:** [014-fly-PROBLEM-refusal-message.jpg](shots-iphone/014-fly-PROBLEM-refusal-message.jpg)

  ![Game said: "Cruise: raiders cannot follo](shots-iphone/014-fly-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. trip phase lift, warp x1, eta 0s
  1. tap button "×20" (speed up ×20)
  1. tap button "×60" (speed up ×60)
  1. trip phase ascent, warp x60, eta 0s
  1. tap button "×5" (speed up ×5)
  1. tap button "×20" (speed up ×20)
  1. tap button "×60" (speed up ×60)
  1. trip phase transit, warp x60, eta 1679s

### 15. Frame-time spike during "fly"

- **How bad:** Minor (score 38), happened 4 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 00:13 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 1807 ms (typical 30 ms); 6 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 00:26 a single frame took 890 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 02:13 a single frame took 980 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [008-fly-PROBLEM-frame-spike.jpg](shots-iphone/008-fly-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "fly"](shots-iphone/008-fly-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off
  1. websocket open ws://127.0.0.1:8463/
  1. websocket closed
  1. websocket open ws://127.0.0.1:8463/
  1. === phase fly starts
  1. ship type meridian; ship centre at port 214,-120; ramp foot 214,-90

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| boarding the ship, taking a seat and flying a course | done | 650 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: started; Deimos: started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / fly: typical 30 ms, slowest 1807 ms, 6 frames over 250 ms
- iphone / fly: typical 29 ms, slowest 980 ms, 1 frames over 250 ms
- iphone / fly: typical 29 ms, slowest 890 ms, 1 frames over 250 ms
- iphone / fly: typical 26 ms, slowest 806 ms, 1 frames over 250 ms
- iphone / fly: typical 30 ms, slowest 386 ms, 1 frames over 250 ms

Button response time (tap to something changing on screen): median 693 ms, slowest 693 ms over 2 taps.

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
