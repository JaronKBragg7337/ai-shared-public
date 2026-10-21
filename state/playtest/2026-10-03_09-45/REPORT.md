# The Cosmos playtest report

Run: 2026-10-03 09:45 (local)  |  Build under test: `6d58c42d7cd2e263d432`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 14.9 minutes, 51 screenshots, 7 distinct problems

## Short version

7 distinct problems found: 0 blockers, 2 serious, 5 smaller.

- **Nothing changed for 60+ seconds (same message, same place)** (Serious, seen 2 times)
- **Stuck while walking to back to the ship** (Serious)
- **Could not walk to a wander on deimos** (Annoying)
- **Tapping speed ×60 did not change the flight speed** (Annoying)
- **Tapping speed ×5 did not change the flight speed** (Annoying)

## Problems, worst first

### 1. Nothing changed for 60+ seconds (same message, same place)

- **How bad:** Serious (score 86), happened 2 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 10:13 into the run, on iPhone (WebKit)
- **What happened:** in "fly": position {"x":5.5,"y":0,"z":14.9}, button "", caption "", toast "", ship aboard
- **Later hits:** 11:21 in "fly": position {"x":5.5,"y":0,"z":14.9}, button "", caption "", toast "", ship aboard
- **Screenshot:** [039-fly-PROBLEM-stuck-state.jpg](shots-iphone/039-fly-PROBLEM-stuck-state.jpg)

  ![Nothing changed for 60+ seconds (same me](shots-iphone/039-fly-PROBLEM-stuck-state.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. not getting closer (26 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (26 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. jump
  1. walk to back to the ship

### 2. Stuck while walking to back to the ship

- **How bad:** Serious (score 80)
- **Where:** boarding the ship, taking a seat and flying a course, first at 11:24 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at shipworld 6,15 (target 0,28, 14 m away)
- **Screenshot:** [042-fly-PROBLEM-stuck-walking.jpg](shots-iphone/042-fly-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to back to the ship](shots-iphone/042-fly-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (14 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (14 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. not getting closer (14 m away), trying to get unstuck #6
  1. not getting closer (14 m away), trying to get unstuck #7
  1. not getting closer (14 m away), trying to get unstuck #8

### 3. Could not walk to a wander on deimos

- **How bad:** Annoying (score 72)
- **Where:** boarding the ship, taking a seat and flying a course, first at 10:08 into the run, on iPhone (WebKit)
- **What happened:** gave up after 60s; last distance 26 m
- **Screenshot:** [037-fly-PROBLEM-cannot-reach.jpg](shots-iphone/037-fly-PROBLEM-cannot-reach.jpg)

  ![Could not walk to a wander on deimos](shots-iphone/037-fly-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (26 m away), trying to get unstuck #3
  1. run-up jump #3
  1. jump
  1. not getting closer (26 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (26 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way

### 4. Tapping speed ×60 did not change the flight speed

- **How bad:** Annoying (score 60)
- **Where:** boarding the ship, taking a seat and flying a course, first at 06:02 into the run, on iPhone (WebKit)
- **What happened:** still ×5
- **Screenshot:** [027-fly-PROBLEM-warp-no-effect.jpg](shots-iphone/027-fly-PROBLEM-warp-no-effect.jpg)

  ![Tapping speed ×60 did not change the fli](shots-iphone/027-fly-PROBLEM-warp-no-effect.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #chip-course (open the Course sheet)
  1. tap button "Deimos15000 km · about 45 minThe outer m" (choose Deimos)
  1. trip started: {"phase":"lift","dest":"Deimos (pad 03)","warp":1,"eta":0,"dist":0}
  1. trip phase lift, warp x1, eta 0s
  1. tap button "×20" (speed up ×20)
  1. trip phase ascent, warp x20, eta 0s
  1. tap button "×5" (speed up ×5)
  1. tap button "×60" (speed up ×60)

### 5. Tapping speed ×5 did not change the flight speed

- **How bad:** Annoying (score 60)
- **Where:** boarding the ship, taking a seat and flying a course, first at 08:10 into the run, on iPhone (WebKit)
- **What happened:** still ×20
- **Screenshot:** [030-fly-PROBLEM-warp-no-effect.jpg](shots-iphone/030-fly-PROBLEM-warp-no-effect.jpg)

  ![Tapping speed ×5 did not change the flig](shots-iphone/030-fly-PROBLEM-warp-no-effect.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. trip phase transit, warp x20, eta 2327s
  1. tap button "×60" (speed up ×60)
  1. tap button "×20" (speed up ×20)
  1. tap on empty 3D view at 35,597
  1. tap on empty 3D view at 294,638
  1. tap on empty 3D view at 59,574
  1. trip phase settle, warp x20, eta 30s
  1. tap button "×5" (speed up ×5)

### 6. Game said: "Cruise: raiders cannot follow a ship at this speed"

- **How bad:** Minor (score 42), happened 3 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 01:36 into the run, on iPhone (WebKit)
- **What happened:** shown in hud-readout while the bot was: 01:36 [fly] tap button "×20" (speed up ×20)
- **Later hits:** 06:16 shown in hud-readout while the bot was: 06:13 [fly] trip phase transit, warp x20, eta 2327s / 12:06 shown in hud-readout while the bot was: 12:05 [fly] tap button "×60" (speed up ×60)
- **Screenshot:** [011-fly-PROBLEM-refusal-message.jpg](shots-iphone/011-fly-PROBLEM-refusal-message.jpg)

  ![Game said: "Cruise: raiders cannot follo](shots-iphone/011-fly-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap button "×60" (speed up ×60)
  1. tap button "×20" (speed up ×20)
  1. trip phase ascent, warp x20, eta 0s
  1. tap button "×60" (speed up ×60)
  1. tap button "×5" (speed up ×5)
  1. tap button "×20" (speed up ×20)
  1. trip phase transit, warp x20, eta 1682s
  1. tap button "×20" (speed up ×20)

### 7. Frame-time spike during "fly"

- **How bad:** Minor (score 38), happened 3 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 00:13 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 2731 ms (typical 17 ms); 6 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 00:38 a single frame took 915 ms (typical 26 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 02:07 a single frame took 756 ms (typical 28 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [004-fly-PROBLEM-frame-spike.jpg](shots-iphone/004-fly-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "fly"](shots-iphone/004-fly-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase fly starts
  1. ship type meridian; ship centre at port 214,-120; ramp foot 214,-90
  1. walk to the ship ramp
  1. route of 3 legs
  1. ramp lowered target=1 progress=1.00

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| boarding the ship, taking a seat and flying a course | done | 881 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: started; Deimos: started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / fly: typical 17 ms, slowest 2731 ms, 6 frames over 250 ms
- iphone / fly: typical 26 ms, slowest 915 ms, 1 frames over 250 ms
- iphone / fly: typical 28 ms, slowest 756 ms, 1 frames over 250 ms
- iphone / fly: typical 27 ms, slowest 558 ms, 1 frames over 250 ms
- iphone / fly: typical 28 ms, slowest 403 ms, 1 frames over 250 ms

Button response time (tap to something changing on screen): median 121 ms, slowest 304 ms over 3 taps.

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
