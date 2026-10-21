# The Cosmos playtest report

Run: 2026-10-03 06:33 (local)  |  Build under test: `390119337877cff96e1e`  |  Site: http://localhost:8461/?ws=ws://127.0.0.1:8462

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 1 minutes, 15 screenshots, 9 distinct problems

## Short version

9 distinct problems found: 0 blockers, 1 serious, 8 smaller.

- **Walking up the ramp does not get you aboard** (Serious)
- **Could not walk to up the ramp** (Annoying)
- **Frame-time spike during "fly"** (Annoying)
- **Console error** (Annoying, seen 2 times)
- **Request returned HTTP 404** (Minor)

## Problems, worst first

### 1. Walking up the ramp does not get you aboard

- **How bad:** Serious (score 88)
- **Where:** boarding the ship, taking a seat and flying a course, first at 00:56 into the run, on iPhone (WebKit)
- **What happened:** reached the ramp, walked in, still outside (position {"x":149.9,"y":0,"z":-99.2}, ramp {"progress":1,"target":1,"angle":0.4469997711314308})
- **Screenshot:** [014-fly-PROBLEM-cannot-board.jpg](shots-iphone/014-fly-PROBLEM-cannot-board.jpg)

  ![Walking up the ramp does not get you abo](shots-iphone/014-fly-PROBLEM-cannot-board.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. jump
  1. jump
  1. jump
  1. jump
  1. jump
  1. not getting closer (10 m away), trying to get unstuck #3
  1. jump

### 2. Could not walk to up the ramp

- **How bad:** Annoying (score 72)
- **Where:** boarding the ship, taking a seat and flying a course, first at 00:55 into the run, on iPhone (WebKit)
- **What happened:** gave up after 40s; last distance 9 m
- **Screenshot:** [012-fly-PROBLEM-cannot-reach.jpg](shots-iphone/012-fly-PROBLEM-cannot-reach.jpg)

  ![Could not walk to up the ramp](shots-iphone/012-fly-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. jump
  1. jump
  1. jump
  1. jump
  1. jump
  1. not getting closer (10 m away), trying to get unstuck #3
  1. jump

### 3. Frame-time spike during "fly"

- **How bad:** Annoying (score 62)
- **Where:** boarding the ship, taking a seat and flying a course, first at 00:15 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4707 ms (typical 27 ms); 7 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [008-fly-PROBLEM-frame-spike.jpg](shots-iphone/008-fly-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "fly"](shots-iphone/008-fly-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8462&qa=1&dev=1&opening=off
  1. websocket open ws://127.0.0.1:8462/
  1. === phase fly starts
  1. ship centre at port 150,-120; ramp foot 150,-90
  1. walk to the ship ramp
  1. route of 3 legs

### 4. Console error

- **How bad:** Annoying (score 55), happened 2 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** Failed to load resource: the server responded with a status of 404 (Not Found)
- **Later hits:** 00:01 Failed to load resource: the server responded with a status of 404 (Not Found)
- **Screenshot:** [002-start-PROBLEM-console-error.jpg](shots-iphone/002-start-PROBLEM-console-error.jpg)

  ![Console error](shots-iphone/002-start-PROBLEM-console-error.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8462&qa=1&dev=1&opening=off

### 5. Request returned HTTP 404

- **How bad:** Minor (score 50)
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/_vercel/insights/script.js
- **Screenshot:** [001-start-PROBLEM-http.jpg](shots-iphone/001-start-PROBLEM-http.jpg)

  ![Request returned HTTP 404](shots-iphone/001-start-PROBLEM-http.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8462&qa=1&dev=1&opening=off

### 6. Request returned HTTP 404

- **How bad:** Minor (score 50)
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/hb-editor.js
- **Screenshot:** [004-start-PROBLEM-http.jpg](shots-iphone/004-start-PROBLEM-http.jpg)

  ![Request returned HTTP 404](shots-iphone/004-start-PROBLEM-http.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8462&qa=1&dev=1&opening=off

### 7. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/_vercel/insights/script.js (Load request cancelled)
- **Screenshot:** [003-start-PROBLEM-request-failed.jpg](shots-iphone/003-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/003-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8462&qa=1&dev=1&opening=off

### 8. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/hb-editor.js (Load request cancelled)
- **Screenshot:** [005-start-PROBLEM-request-failed.jpg](shots-iphone/005-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/005-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8462&qa=1&dev=1&opening=off

### 9. Button too small for a thumb: #purse "10,000 marks · 2,500 cr" 138x11

- **How bad:** Small (score 30)
- **Where:** boarding the ship, taking a seat and flying a course, first at 00:15 into the run, on iPhone (WebKit)
- **What happened:** #purse "10,000 marks · 2,500 cr" 138x11 (fly, iphone)
- **Screenshot:** [009-fly-PROBLEM-tiny-button.jpg](shots-iphone/009-fly-PROBLEM-tiny-button.jpg)

  ![Button too small for a thumb: #purse "10](shots-iphone/009-fly-PROBLEM-tiny-button.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8462&qa=1&dev=1&opening=off
  1. websocket open ws://127.0.0.1:8462/
  1. === phase fly starts
  1. ship centre at port 150,-120; ramp foot 150,-90
  1. walk to the ship ramp
  1. route of 3 legs

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| boarding the ship, taking a seat and flying a course | done | 44 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / fly: typical 27 ms, slowest 4707 ms, 7 frames over 250 ms
- iphone / fly: typical 30 ms, slowest 171 ms, 0 frames over 250 ms
- iphone / fly: typical 30 ms, slowest 134 ms, 0 frames over 250 ms
- iphone / fly: typical 29 ms, slowest 93 ms, 0 frames over 250 ms
- iphone / fly: typical 29 ms, slowest 60 ms, 0 frames over 250 ms

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
