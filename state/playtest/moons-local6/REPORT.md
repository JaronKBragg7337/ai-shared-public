# The Cosmos playtest report

Run: 2026-10-03 07:14 (local)  |  Build under test: `390119337877cff96e1e`  |  Site: http://localhost:8461/?ws=ws://127.0.0.1:8463

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 19.4 minutes, 58 screenshots, 10 distinct problems

## Short version

10 distinct problems found: 0 blockers, 0 serious, 10 smaller.

- **Could not walk to core sample site S2** (Annoying)
- **Could not walk to core sample site S3** (Annoying)
- **Could not walk to core sample site S1** (Annoying)
- **Console error** (Annoying, seen 2 times)
- **Request returned HTTP 404** (Minor)

## Problems, worst first

### 1. Could not walk to core sample site S2

- **How bad:** Annoying (score 72)
- **Where:** boarding the ship, taking a seat and flying a course, first at 06:10 into the run, on iPhone (WebKit)
- **What happened:** gave up after 100s; last distance 225 m
- **Screenshot:** [024-fly-PROBLEM-cannot-reach.jpg](shots-iphone/024-fly-PROBLEM-cannot-reach.jpg)

  ![Could not walk to core sample site S2](shots-iphone/024-fly-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #chip-ramp (lower the ramp from the pilot seat)
  1. tap #space-sheet .close (close the Course sheet)
  1. tap button "Stand" (stand up)
  1. walk to off the ramp tip
  1. 3 sample sites known
  1. walk to core sample site S1
  1. tap #btn-action (action)
  1. walk to core sample site S2

### 2. Could not walk to core sample site S3

- **How bad:** Annoying (score 72)
- **Where:** boarding the ship, taking a seat and flying a course, first at 07:50 into the run, on iPhone (WebKit)
- **What happened:** gave up after 100s; last distance 1056 m
- **Screenshot:** [028-fly-PROBLEM-cannot-reach.jpg](shots-iphone/028-fly-PROBLEM-cannot-reach.jpg)

  ![Could not walk to core sample site S3](shots-iphone/028-fly-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #space-sheet .close (close the Course sheet)
  1. tap button "Stand" (stand up)
  1. walk to off the ramp tip
  1. 3 sample sites known
  1. walk to core sample site S1
  1. tap #btn-action (action)
  1. walk to core sample site S2
  1. walk to core sample site S3

### 3. Could not walk to core sample site S1

- **How bad:** Annoying (score 72)
- **Where:** boarding the ship, taking a seat and flying a course, first at 13:50 into the run, on iPhone (WebKit)
- **What happened:** gave up after 100s; last distance 3240 m
- **Screenshot:** [044-fly-PROBLEM-cannot-reach.jpg](shots-iphone/044-fly-PROBLEM-cannot-reach.jpg)

  ![Could not walk to core sample site S1](shots-iphone/044-fly-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. after trip: landed=true onMoon=true moon=Deimos flying=false
  1. on deimos: stand up and walk out
  1. tap #chip-ramp (lower the ramp from the pilot seat)
  1. tap #space-sheet .close (close the Course sheet)
  1. tap button "Stand" (stand up)
  1. walk to off the ramp tip
  1. 1 sample sites known
  1. walk to core sample site S1

### 4. Console error

- **How bad:** Annoying (score 55), happened 2 times
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** Failed to load resource: the server responded with a status of 404 (Not Found)
- **Later hits:** 00:01 Failed to load resource: the server responded with a status of 404 (Not Found)
- **Screenshot:** [002-start-PROBLEM-console-error.jpg](shots-iphone/002-start-PROBLEM-console-error.jpg)

  ![Console error](shots-iphone/002-start-PROBLEM-console-error.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 5. Request returned HTTP 404

- **How bad:** Minor (score 50)
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/_vercel/insights/script.js
- **Screenshot:** [001-start-PROBLEM-http.jpg](shots-iphone/001-start-PROBLEM-http.jpg)

  ![Request returned HTTP 404](shots-iphone/001-start-PROBLEM-http.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 6. Request returned HTTP 404

- **How bad:** Minor (score 50)
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/hb-editor.js
- **Screenshot:** [004-start-PROBLEM-http.jpg](shots-iphone/004-start-PROBLEM-http.jpg)

  ![Request returned HTTP 404](shots-iphone/004-start-PROBLEM-http.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 7. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/_vercel/insights/script.js (Load request cancelled)
- **Screenshot:** [003-start-PROBLEM-request-failed.jpg](shots-iphone/003-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/003-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 8. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:01 into the run, on iPhone (WebKit)
- **What happened:** http://localhost:8461/hb-editor.js (Load request cancelled)
- **Screenshot:** [005-start-PROBLEM-request-failed.jpg](shots-iphone/005-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/005-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off

### 9. Game said: "Cruise: raiders cannot follow a ship at this speed"

- **How bad:** Minor (score 42), happened 3 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 01:41 into the run, on iPhone (WebKit)
- **What happened:** shown in hud-readout while the bot was: 01:29 [fly] tap on empty 3D view at 263,604
- **Later hits:** 09:30 shown in hud-readout while the bot was: 09:27 [fly] tap button "×60" (speed up ×60) / 16:26 shown in hud-readout while the bot was: 16:26 [fly] tap button "×60" (speed up ×60)
- **Screenshot:** [012-fly-PROBLEM-refusal-message.jpg](shots-iphone/012-fly-PROBLEM-refusal-message.jpg)

  ![Game said: "Cruise: raiders cannot follo](shots-iphone/012-fly-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap on empty 3D view at 287,662
  1. tap button "×20" (speed up ×20)
  1. trip phase ascent, warp x20, eta 0s
  1. tap button "×20" (speed up ×20)
  1. tap button "×60" (speed up ×60)
  1. tap button "×5" (speed up ×5)
  1. tap on empty 3D view at 41,584
  1. tap on empty 3D view at 263,604

### 10. Frame-time spike during "fly"

- **How bad:** Minor (score 38), happened 3 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 00:10 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 2121 ms (typical 28 ms); 6 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 02:01 a single frame took 793 ms (typical 32 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 02:47 a single frame took 963 ms (typical 28 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [007-fly-PROBLEM-frame-spike.jpg](shots-iphone/007-fly-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "fly"](shots-iphone/007-fly-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open http://localhost:8461/?ws=ws://127.0.0.1:8463&qa=1&dev=1&opening=off
  1. websocket open ws://127.0.0.1:8463/
  1. === phase fly starts
  1. ship centre at port 0,0; ramp foot 0,30

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| boarding the ship, taking a seat and flying a course | done | 1158 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: started; Deimos: started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / fly: typical 28 ms, slowest 2121 ms, 6 frames over 250 ms
- iphone / fly: typical 28 ms, slowest 963 ms, 1 frames over 250 ms
- iphone / fly: typical 32 ms, slowest 793 ms, 1 frames over 250 ms
- iphone / fly: typical 25 ms, slowest 438 ms, 1 frames over 250 ms
- iphone / fly: typical 29 ms, slowest 437 ms, 1 frames over 250 ms

Button response time (tap to something changing on screen): median 315 ms, slowest 922 ms over 3 taps.

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
