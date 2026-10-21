# The Cosmos playtest report

Run: 2026-10-04 23:40 (local)  |  Build under test: `f0c52161e2d69006af95`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 9.3 minutes, 52 screenshots, 8 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)

## Short version

8 distinct problems found: 0 blockers, 0 serious, 8 smaller.

- **A Dig tap in the opening made no cut** (Annoying, seen 10 times)
- **Frame-time spike during "opening"** (Annoying, seen 10 times)
- **Server connection (websocket) closed** (Minor, seen 2 times)
- **A request failed to load** (Minor)
- **A request failed to load** (Minor)

## Problems, worst first

### 1. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 10 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:32 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 0 after tapping "Dig (E)"
- **Later hits:** 06:34 cuts stayed 0 after tapping "Dig (E)" / 06:36 cuts stayed 0 after tapping "Dig (E)"
- **Screenshot:** [038-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/038-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/038-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-note button (close the locker note)
  1. walk to the cabin exit
  1. walk to the cabin exit
  1. mis-tap beside #opening-action
  1. tap #opening-action (opening action)
  1. opening stage 3 -> 4 (Something lies beneath the collapsed dust.)
  1. walk to the crate
  1. tap #opening-action (opening action)

### 2. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 10 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:25 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4937 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 05:31 a single frame took 3534 ms (typical 19 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 06:11 a single frame took 6159 ms (typical 34 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [008-opening-PROBLEM-frame-spike.jpg](shots-iphone/008-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/008-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 3. Server connection (websocket) closed

- **How bad:** Minor (score 50), happened 2 times
- **Where:** loading the page, first at 00:09 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Later hits:** 05:09 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Screenshot:** [005-start-PROBLEM-ws-closed.jpg](shots-iphone/005-start-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/005-start-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. websocket closed

### 4. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:09 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/walter.glb (Load request cancelled)
- **Screenshot:** [001-start-PROBLEM-request-failed.jpg](shots-iphone/001-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/001-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 5. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:09 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/aoi.glb (Load request cancelled)
- **Screenshot:** [002-start-PROBLEM-request-failed.jpg](shots-iphone/002-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/002-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 6. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:09 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/ada.glb (Load request cancelled)
- **Screenshot:** [003-start-PROBLEM-request-failed.jpg](shots-iphone/003-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/003-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 7. A request failed to load

- **How bad:** Minor (score 45)
- **Where:** loading the page, first at 00:09 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/sunita.glb (Load request cancelled)
- **Screenshot:** [004-start-PROBLEM-request-failed.jpg](shots-iphone/004-start-PROBLEM-request-failed.jpg)

  ![A request failed to load](shots-iphone/004-start-PROBLEM-request-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 8. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:47 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 03:45 [opening] walk to down the gangway
- **Screenshot:** [021-opening-PROBLEM-refusal-message.jpg](shots-iphone/021-opening-PROBLEM-refusal-message.jpg)

  ![Game said: "Welcome to Mars. Follow the ](shots-iphone/021-opening-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. in the boarding hall, waiting for the gangway to come down
  1. walk to down the gangway
  1. walk to down the gangway
  1. walk to down the gangway

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 529 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / opening: typical 22 ms, slowest 7087 ms, 2 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 6317 ms, 2 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 6218 ms, 2 frames over 250 ms
- iphone / opening: typical 34 ms, slowest 6159 ms, 1 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 4937 ms, 5 frames over 250 ms

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
