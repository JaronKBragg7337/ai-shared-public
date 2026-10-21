# The Cosmos playtest report

Run: 2026-10-03 09:06 (local)  |  Build under test: `974d3b8c679b23402a45`  |  Site: http://localhost:8461/?ws=ws://127.0.0.1:8463

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 11 minutes, 41 screenshots, 10 distinct problems

## Short version

10 distinct problems found: 0 blockers, 1 serious, 9 smaller.

- **Stuck while walking to back to the ship** (Serious)
- **Could not walk to a wander on deimos** (Annoying)
- **Console error** (Annoying, seen 4 times)
- **Request returned HTTP 404** (Minor, seen 2 times)
- **Request returned HTTP 404** (Minor, seen 2 times)

## Problems, worst first

### 1. Stuck while walking to back to the ship

- **How bad:** Serious (score 80)
- **Where:** boarding the ship, taking a seat and flying a course, first at 11:02 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at shipworld 6,15 (target 0,28, 14 m away)
- **Screenshot:** [040-fly-PROBLEM-stuck-walking.jpg](shots-iphone/040-fly-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to back to the ship](shots-iphone/040-fly-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (14 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (14 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. not getting closer (14 m away), trying to get unstuck #6
  1. not getting closer (14 m away), trying to get unstuck #7
  1. not getting closer (14 m away), trying to get unstuck #8

### 2. Could not walk to a wander on deimos

- **How bad:** Annoying (score 72)
- **Where:** boarding the ship, taking a seat and flying a course, first at 09:46 into the run, on iPhone (WebKit)
- **What happened:** gave up after 60s; last distance 26 m
- **Screenshot:** [036-fly-PROBLEM-cannot-reach.jpg](shots-iphone/036-fly-PROBLEM-cannot-reach.jpg)

  ![Could not walk to a wander on deimos](shots-iphone/036-fly-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (26 m away), trying to get unstuck #3
  1. run-up jump #3
  1. jump
  1. not getting closer (26 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (26 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way

### 3. Console error

- **How bad:** Annoying (score 55), happened 4 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** Failed to load resource: the server responded with a status of 404 (Not Found)
- **Later hits:** 00:01 Failed to load resource: the server responded with a status of 404 (Not Found) / 00:04 Failed to load resource: the server responded with a status of 404 (Not Found)
- **Screenshot:** [002-start-PROBLEM-console-error.jpg](shots-iphone/002-start-PROBLEM-console-error.jpg)

  ![Console error](shots-iphone/002-start-PROBLEM-console-error.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 4. Request returned HTTP 404

- **How bad:** Minor (score 50), happened 2 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/_vercel/insights/script.js
- **Later hits:** 00:04 http://localhost:8461/_vercel/insights/script.js
- **Screenshot:** [001-start-PROBLEM-http.jpg](shots-iphone/001-start-PROBLEM-http.jpg)

  ![Request returned HTTP 404](shots-iphone/001-start-PROBLEM-http.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 5. Request returned HTTP 404

- **How bad:** Minor (score 50), happened 2 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/hb-editor.js
- **Later hits:** 00:04 http://localhost:8461/hb-editor.js
- **Screenshot:** [004-start-PROBLEM-http.jpg](shots-iphone/004-start-PROBLEM-http.jpg)

  ![Request returned HTTP 404](shots-iphone/004-start-PROBLEM-http.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 6. Server connection (websocket) closed

- **How bad:** Minor (score 50)
- **Where:** loading the page, first at 00:04 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: ws://127.0.0.1:8463/
- **Screenshot:** [006-start-PROBLEM-ws-closed.jpg](shots-iphone/006-start-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/006-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off
  1. websocket open ws://127.0.0.1:8463/
  1. websocket closed

### 7. A request failed to load

- **How bad:** Minor (score 45), happened 2 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/_vercel/insights/script.js (Load request cancelled)
- **Later hits:** 00:04 http://localhost:8461/_vercel/insights/script.js (Load request cancelled)
- **Screenshot:** [003-start-PROBLEM-request-failed.jpg](shots-iphone/003-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/003-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 8. A request failed to load

- **How bad:** Minor (score 45), happened 2 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/hb-editor.js (Load request cancelled)
- **Later hits:** 00:04 http://localhost:8461/hb-editor.js (Load request cancelled)
- **Screenshot:** [005-start-PROBLEM-request-failed.jpg](shots-iphone/005-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/005-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 9. Game said: "Cruise: raiders cannot follow a ship at this speed"

- **How bad:** Minor (score 42), happened 2 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 01:31 into the run, on iPhone (WebKit)
- **What happened:** shown in hud-readout while the bot was: 01:31 [fly] tap button "×60" (speed up ×60)
- **Later hits:** 06:03 shown in hud-readout while the bot was: 06:01 [fly] tap button "×60" (speed up ×60)
- **Screenshot:** [014-fly-PROBLEM-refusal-message.jpg](shots-iphone/014-fly-PROBLEM-refusal-message.jpg)

  ![Game said: "Cruise: raiders cannot follo](shots-iphone/014-fly-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap button "×60" (speed up ×60)
  1. tap button "×20" (speed up ×20)
  1. trip phase ascent, warp x20, eta 0s
  1. tap button "×60" (speed up ×60)
  1. tap button "×20" (speed up ×20)
  1. tap button "×5" (speed up ×5)
  1. trip phase transit, warp x5, eta 1682s
  1. tap button "×60" (speed up ×60)

### 10. Frame-time spike during "fly"

- **How bad:** Minor (score 38), happened 3 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 00:14 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 2261 ms (typical 30 ms); 6 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 00:26 a single frame took 881 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 02:46 a single frame took 853 ms (typical 27 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [008-fly-PROBLEM-frame-spike.jpg](shots-iphone/008-fly-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "fly"](shots-iphone/008-fly-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off
  1. websocket open ws://127.0.0.1:8463/
  1. websocket closed
  1. websocket open ws://127.0.0.1:8463/
  1. === phase fly starts
  1. ship type meridian; ship centre at port 0,0; ramp foot 0,30

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| boarding the ship, taking a seat and flying a course | done | 651 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: started; Deimos: started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / fly: typical 30 ms, slowest 2261 ms, 6 frames over 250 ms
- iphone / fly: typical 29 ms, slowest 881 ms, 1 frames over 250 ms
- iphone / fly: typical 27 ms, slowest 853 ms, 1 frames over 250 ms
- iphone / fly: typical 26 ms, slowest 311 ms, 1 frames over 250 ms
- iphone / fly: typical 29 ms, slowest 216 ms, 0 frames over 250 ms

Button response time (tap to something changing on screen): median 310 ms, slowest 310 ms over 2 taps.

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
