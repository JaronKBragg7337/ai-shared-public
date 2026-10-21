# The Cosmos playtest report

Run: 2026-10-03 12:00 (local)  |  Build under test: `c2275c40d91c0db91fc4`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 22.1 minutes, 154 screenshots, 14 distinct problems
- **Desktop (Chromium, keyboard + mouse)**: 6.1 minutes, 49 screenshots, 9 distinct problems

## Short version

16 distinct problems found: 0 blockers, 5 serious, 11 smaller.

- **Game said: "Walk to that place."** (Serious, seen 2 times)
- **Stuck while walking to the ship ramp** (Serious, seen 2 times)
- **Stuck while walking to Shift runner** (Serious)
- **Stuck while walking to Lookout at the glass** (Serious)
- **The Dig button never appeared on open ground** (Serious)

## Problems, worst first

### 1. Game said: "Walk to that place."

- **How bad:** Serious (score 80), happened 2 times
- **Where:** digging regolith and delivering it to the weigh bay, first at 12:34 into the run, on iPhone (WebKit)
- **What happened:** shown in ship-toast while the bot was: 12:34 [dig] no Dig button (button: ""); turning to find ground
- **Later hits:** 13:14 shown in ship-toast while the bot was: 13:07 [dig] route of 9 legs
- **Screenshot:** [105-dig-PROBLEM-refusal-message.jpg](shots-iphone/105-dig-PROBLEM-refusal-message.jpg)

  ![Game said: "Walk to that place."](shots-iphone/105-dig-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)
  1. no Dig button (button: ""); turning to find ground

### 2. Stuck while walking to the ship ramp

- **How bad:** Serious (score 80), happened 2 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 15:39 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port 54,-30 (target 214,-101, 8 m away)
- **Later hits:** 17:07 This is at the port perimeter kerb (a ~0.6 m high concrete wall ring at x = +/-103; walking steps up only 0.35 m, and a jump from a standstill against it goes straight up). no progress for 56s a
- **Screenshot:** [128-fly-PROBLEM-stuck-walking.jpg](shots-iphone/128-fly-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to the ship ramp](shots-iphone/128-fly-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (8 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 21 legs
  1. not getting closer (8 m away), trying to get unstuck #6
  1. not getting closer (8 m away), trying to get unstuck #7
  1. not getting closer (8 m away), trying to get unstuck #8

### 3. Stuck while walking to Shift runner

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 09:03 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -61,-41 (target -64,-41, 3 m away)
- **Screenshot:** [084-tour-PROBLEM-stuck-walking.jpg](shots-iphone/084-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Shift runner](shots-iphone/084-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (3 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 3 legs
  1. not getting closer (3 m away), trying to get unstuck #6
  1. not getting closer (3 m away), trying to get unstuck #7
  1. not getting closer (3 m away), trying to get unstuck #8

### 4. Stuck while walking to Lookout at the glass

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 10:19 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -59,-41 (target -56,-41, 4 m away)
- **Screenshot:** [087-tour-PROBLEM-stuck-walking.jpg](shots-iphone/087-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Lookout at the gl](shots-iphone/087-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (4 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 3 legs
  1. not getting closer (4 m away), trying to get unstuck #6
  1. not getting closer (4 m away), trying to get unstuck #7
  1. not getting closer (4 m away), trying to get unstuck #8

### 5. The Dig button never appeared on open ground

- **How bad:** Serious (score 78)
- **Where:** digging regolith and delivering it to the weigh bay, first at 13:06 into the run, on iPhone (WebKit)
- **What happened:** button text "Drop", standing at {"x":-90.2,"y":0.3,"z":83.7}, looking down
- **Screenshot:** [115-dig-PROBLEM-cannot-dig.jpg](shots-iphone/115-dig-PROBLEM-cannot-dig.jpg)

  ![The Dig button never appeared on open gr](shots-iphone/115-dig-PROBLEM-cannot-dig.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)

### 6. Could not walk to Arrival guide

- **How bad:** Annoying (score 72)
- **Where:** walking the port and talking to people, first at 05:52 into the run, on desktop (Chromium)
- **What happened:** gave up after 120s; last distance 9 m
- **Screenshot:** [046-tour-PROBLEM-cannot-reach.jpg](shots-desktop/046-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Arrival guide](shots-desktop/046-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide
  1. route of 36 legs

### 7. Talk panel did not open for Watch supervisor

- **How bad:** Annoying (score 70)
- **Where:** walking the port and talking to people, first at 06:07 into the run, on iPhone (WebKit)
- **What happened:** tapped Talk, no panel
- **Screenshot:** [062-tour-PROBLEM-panel-not-open.jpg](shots-iphone/062-tour-PROBLEM-panel-not-open.jpg)

  ![Talk panel did not open for Watch superv](shots-iphone/062-tour-PROBLEM-panel-not-open.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)
  1. lift going up
  1. arrived in the control cab
  1. go talk to Watch supervisor
  1. walk to Watch supervisor
  1. route of 3 legs
  1. tap #crew-talk (Talk to Watch supervisor)

### 8. Buttons are covered by something on top of them (2 places)

- **How bad:** Annoying (score 68), happened 2 times
- **Where:** opening the Settings / Account / World / Controls panels, first at 03:50 into the run, on desktop (Chromium)
- **What happened:** #multiplayer-button "World / crew" is covered by #touch-key-KeyD ;  #voice-talk "Hold B to talkno one near" is covered by #touch-key-KeyW
- **Screenshot:** [038-panels-PROBLEM-covered.jpg](shots-desktop/038-panels-PROBLEM-covered.jpg)

  ![Buttons are covered by something on top ](shots-desktop/038-panels-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. mis-tap beside #purse
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)

### 9. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 8 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 01:18 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** cuts stayed 0 after tapping "Dig (E)"
- **Later hits:** 01:40 cuts stayed 3 after tapping "Dig (E)" / 01:47 cuts stayed 7 after tapping "Dig (E)"
- **Screenshot:** [012-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/012-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/012-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. === phase opening starts
  1. opening stage -1 -> 0 ()
  1. tap screen to unlock sound
  1. tap screen to unlock sound
  1. opening stage 0 -> 1 (Move: WASD / left thumb · Look: mouse / right thumb)
  1. tap #opening-action (opening action)
  1. opening stage 1 -> 2 (Something lies beneath the collapsed dust.)
  1. tap #opening-action (opening action)

### 10. Buttons overlap each other (3 places)

- **How bad:** Annoying (score 66), happened 4 times
- **Where:** opening the Settings / Account / World / Controls panels, first at 03:32 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** #btn-close-settings "✕" overlaps #set-tool "Hand spade Shovel Excavator " by 77% ;  #touch-key-KeyW "Forward" overlaps #voice-talk "Hold B to talkno one near" by 97% ;  #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83%
- **Screenshot:** [030-panels-PROBLEM-overlap.jpg](shots-iphone/030-panels-PROBLEM-overlap.jpg)

  ![Buttons overlap each other (3 places)](shots-iphone/030-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. opening stage 3 -> 4 (Jorge: Free Settlements. We saw you come down.)
  1. REFRESH (mid-ride)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening finished
  1. === phase panels starts
  1. tap #btn-settings (open Settings)

### 11. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 17 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:10 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** a single frame took 2627 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 01:38 a single frame took 2585 ms (typical 16 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 02:06 a single frame took 805 ms (typical 26 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 ()

### 12. Game said: "Weather sensors are offline. Watch the dust outside."

- **How bad:** Minor (score 42)
- **Where:** walking the port and talking to people, first at 07:46 into the run, on iPhone (WebKit)
- **What happened:** shown in crew-panel while the bot was: 07:45 [tour] tap button "Understood. What can I do here?" (answer back)
- **Screenshot:** [079-tour-PROBLEM-refusal-message.jpg](shots-iphone/079-tour-PROBLEM-refusal-message.jpg)

  ![Game said: "Weather sensors are offline.](shots-iphone/079-tour-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opened Ground controller instead of Weather officer; stepping closer to the right person
  1. tap button "✕" (close talk panel)
  1. go talk to Weather officer
  1. walk to Weather officer
  1. mis-tap beside #crew-talk
  1. tap #crew-talk (Talk to Weather officer)
  1. tap button "What is your watch like?" (ask them something)
  1. tap button "Understood. What can I do here?" (answer back)

### 13. Frame-time spike during "tour"

- **How bad:** Minor (score 38), happened 4 times
- **Where:** walking the port and talking to people, first at 03:53 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** a single frame took 1195 ms (typical 26 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 11:06 a single frame took 745 ms (typical 16 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [037-tour-PROBLEM-frame-spike.jpg](shots-iphone/037-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/037-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide
  1. route of 28 legs

### 14. Frame-time spike during "freeplay"

- **How bad:** Minor (score 38), happened 2 times
- **Where:** free play (random walking, tapping, refreshing), first at 17:40 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 2742 ms (typical 29 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 19:51 a single frame took 2911 ms (typical 30 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [139-freeplay-PROBLEM-frame-spike.jpg](shots-iphone/139-freeplay-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "freeplay"](shots-iphone/139-freeplay-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. mis-tap beside #btn-key-controls
  1. tap #btn-key-controls (idle fiddling)
  1. mis-tap beside #purse
  1. tap #purse (idle fiddling)
  1. tap button "Close"
  1. REFRESH (random refresh while playing)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 15. Frame-time spike during "hire"

- **How bad:** Minor (score 38)
- **Where:** hiring crew from the crew hall, first at 11:18 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 2926 ms (typical 29 ms); 6 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [091-hire-PROBLEM-frame-spike.jpg](shots-iphone/091-hire-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "hire"](shots-iphone/091-hire-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (refresh after the port tour)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. refresh check: moved 0.0 m, marks 10000 -> 10000, aboard false -> false
  1. === phase hire starts
  1. candidates: Jorge(Navigator), Sunita(Gunner (dorsal)), Walter(Gunner (ventral)), Zuri Okafor 1(Captain), Ada Chen 1(Pilot), Aoi Patel 1(Communications officer)
  1. walk to candidate Ada Chen 1
  1. route of 6 legs

### 16. Frame-time spike during "dig"

- **How bad:** Minor (score 38)
- **Where:** digging regolith and delivering it to the weigh bay, first at 13:37 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 2903 ms (typical 17 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [121-dig-PROBLEM-frame-spike.jpg](shots-iphone/121-dig-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "dig"](shots-iphone/121-dig-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. dug 86 bites; cart 0.0/1054 -> 90.2/1054
  1. walk to the amber weigh bay
  1. route of 9 legs
  1. quest was not accepted, so no Deliver button is expected
  1. tap #btn-drop-all (drop all)
  1. REFRESH (refresh right after digging)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 201 s |
| opening the Settings / Account / World / Controls panels | done | 10 s |
| walking the port and talking to people | done | 438 s |
| hiring crew from the crew hall | done | 20 s |
| digging regolith and delivering it to the weigh bay | done | 113 s |
| boarding the ship, taking a seat and flying a course | done | 122 s |
| getting into and driving the survey rover | done | 88 s |
| free play (random walking, tapping, refreshing) | done | 294 s |

People talked to: 12 of 16. Crew hired: 2. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

### Desktop (Chromium, keyboard + mouse)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 203 s |
| opening the Settings / Account / World / Controls panels | done | 15 s |
| walking the port and talking to people | done | 121 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | skipped (out of time) | 0 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- desktop / tour: typical 4 ms, slowest 6675 ms, 2 frames over 250 ms
- desktop / opening: typical 4 ms, slowest 6470 ms, 4 frames over 250 ms
- desktop / opening: typical 17 ms, slowest 5229 ms, 3 frames over 250 ms
- desktop / opening: typical 4 ms, slowest 4996 ms, 3 frames over 250 ms
- desktop / opening: typical 4 ms, slowest 4667 ms, 3 frames over 250 ms

Button response time (tap to something changing on screen): median 126 ms, slowest 1178 ms over 28 taps.

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
