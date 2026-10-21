# The Cosmos playtest report

Run: 2026-10-03 13:49 (local)  |  Build under test: `2cbecfe27c8269d7480d`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 15.1 minutes, 130 screenshots, 11 distinct problems

## Short version

11 distinct problems found: 1 blockers, 3 serious, 7 smaller.

- **A game action stays "pending" forever (the server never answers), so the buttons are dead** (BLOCKER)
- **Hiring Ada Chen 1 did not work** (Serious)
- **Stuck while walking to Shift runner** (Serious)
- **Stuck while walking to Lookout at the glass** (Serious)
- **A Dig tap in the opening made no cut** (Annoying, seen 9 times)

## Problems, worst first

### 1. A game action stays "pending" forever (the server never answers), so the buttons are dead

- **How bad:** BLOCKER (score 97)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 01:29 into the run, on iPhone (WebKit)
- **What happened:** in the opening step 0: the game's own busy flag has been on for 25 s; button text "", caption "Continue the opening first."
- **Screenshot:** [010-opening-PROBLEM-server-not-answering.jpg](shots-iphone/010-opening-PROBLEM-server-not-answering.jpg)

  ![A game action stays "pending" forever (t](shots-iphone/010-opening-PROBLEM-server-not-answering.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 ()
  1. tap screen to unlock sound
  1. tap screen to unlock sound

### 2. Hiring Ada Chen 1 did not work

- **How bad:** Serious (score 84)
- **Where:** hiring crew from the crew hall, first at 12:00 into the run, on iPhone (WebKit)
- **What happened:** tapped Hire; they are still a candidate; marks 10000 -> 10000; screen said "Ada Chen 1Pilot · skill 82%✕Walk over to them first.Flies what you point her at. Keeps the ship off the rocks and out of"
- **Screenshot:** [097-hire-PROBLEM-hire-failed.jpg](shots-iphone/097-hire-PROBLEM-hire-failed.jpg)

  ![Hiring Ada Chen 1 did not work](shots-iphone/097-hire-PROBLEM-hire-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. === phase hire starts
  1. candidates: Jorge(Navigator), Sunita(Gunner (dorsal)), Walter(Gunner (ventral)), Zuri Okafor 1(Captain), Ada Chen 1(Pilot), Aoi Patel 1(Communications officer)
  1. walk to candidate Ada Chen 1
  1. route of 8 legs
  1. tap #crew-talk (open hiring panel)
  1. tap button "Meet Ada Chen 1 · 560 marks" (hire Ada Chen 1)
  1. the button said Meet first; waiting for the candidate to walk over, then Hire
  1. hire result: status candidate, marks 10000 -> 10000

### 3. Stuck while walking to Shift runner

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 09:02 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -61,-41 (target -64,-41, 3 m away)
- **Screenshot:** [087-tour-PROBLEM-stuck-walking.jpg](shots-iphone/087-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Shift runner](shots-iphone/087-tour-PROBLEM-stuck-walking.jpg)

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
- **Where:** walking the port and talking to people, first at 10:18 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -59,-41 (target -56,-41, 4 m away)
- **Screenshot:** [090-tour-PROBLEM-stuck-walking.jpg](shots-iphone/090-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Lookout at the gl](shots-iphone/090-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (4 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 3 legs
  1. not getting closer (4 m away), trying to get unstuck #6
  1. not getting closer (4 m away), trying to get unstuck #7
  1. not getting closer (4 m away), trying to get unstuck #8

### 5. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 9 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 01:45 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 3 after tapping "Dig (E)"
- **Later hits:** 02:11 cuts stayed 3 after tapping "Dig (E)" / 02:14 cuts stayed 3 after tapping "Dig (E)"
- **Screenshot:** [014-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/014-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/014-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (mis-tap)
  1. tap #opening-action (opening action)
  1. opening stage 1 -> 2 (Something lies beneath the collapsed dust.)
  1. walk to the crate
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)

### 6. Buttons overlap: #btn-close-settings "✕" overlaps #set-tool "Hand spade Shovel Excavator " by 77%

- **How bad:** Annoying (score 66)
- **Where:** opening the Settings / Account / World / Controls panels, first at 04:28 into the run, on iPhone (WebKit)
- **What happened:** #btn-close-settings "✕" overlaps #set-tool "Hand spade Shovel Excavator " by 77% (Settings scrolled, iphone)
- **Screenshot:** [032-panels-PROBLEM-overlap.jpg](shots-iphone/032-panels-PROBLEM-overlap.jpg)

  ![Buttons overlap: #btn-close-settings "✕"](shots-iphone/032-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. opening stage 3 -> 4 (Zuri: Outer Accord. We saw you come down.)
  1. REFRESH (mid-ride)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening finished
  1. === phase panels starts
  1. tap #btn-settings (open Settings)

### 7. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 9 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:16 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 5451 ms (typical 16 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 01:34 a single frame took 992 ms (typical 17 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 02:05 a single frame took 7558 ms (typical 16 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 ()

### 8. Frame-time spike during "hire"

- **How bad:** Annoying (score 62)
- **Where:** hiring crew from the crew hall, first at 11:27 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4628 ms (typical 43 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [094-hire-PROBLEM-frame-spike.jpg](shots-iphone/094-hire-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "hire"](shots-iphone/094-hire-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (refresh after the port tour)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. refresh check: moved 0.0 m, marks 10000 -> 10000, aboard false -> false
  1. === phase hire starts
  1. candidates: Jorge(Navigator), Sunita(Gunner (dorsal)), Walter(Gunner (ventral)), Zuri Okafor 1(Captain), Ada Chen 1(Pilot), Aoi Patel 1(Communications officer)
  1. walk to candidate Ada Chen 1
  1. route of 8 legs

### 9. Frame-time spike during "dig"

- **How bad:** Annoying (score 62)
- **Where:** digging regolith and delivering it to the weigh bay, first at 14:57 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 7376 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [129-dig-PROBLEM-frame-spike.jpg](shots-iphone/129-dig-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "dig"](shots-iphone/129-dig-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #1
  1. jump
  1. tap #quest-deliver (deliver the tonne)
  1. delivery: marks 9280 -> 9280
  1. tap #btn-drop-all (drop all)
  1. REFRESH (refresh right after digging)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 10. Game said: "Weather sensors are offline. Watch the dust outside."

- **How bad:** Minor (score 42)
- **Where:** walking the port and talking to people, first at 07:43 into the run, on iPhone (WebKit)
- **What happened:** shown in crew-panel while the bot was: 07:43 [tour] tap button "Understood. What can I do here?" (answer back)
- **Screenshot:** [082-tour-PROBLEM-refusal-message.jpg](shots-iphone/082-tour-PROBLEM-refusal-message.jpg)

  ![Game said: "Weather sensors are offline.](shots-iphone/082-tour-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #crew-talk (Talk to Weather officer)
  1. opened Ground controller instead of Weather officer; stepping closer to the right person
  1. tap button "✕" (close talk panel)
  1. go talk to Weather officer
  1. walk to Weather officer
  1. tap #crew-talk (Talk to Weather officer)
  1. tap button "What is your watch like?" (ask them something)
  1. tap button "Understood. What can I do here?" (answer back)

### 11. Frame-time spike during "tour"

- **How bad:** Minor (score 38), happened 3 times
- **Where:** walking the port and talking to people, first at 04:40 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 1920 ms (typical 58 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 05:31 a single frame took 879 ms (typical 39 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 11:14 a single frame took 7329 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [039-tour-PROBLEM-frame-spike.jpg](shots-iphone/039-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/039-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide
  1. route of 28 legs

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 251 s |
| opening the Settings / Account / World / Controls panels | done | 12 s |
| walking the port and talking to people | done | 380 s |
| hiring crew from the crew hall | done | 44 s |
| digging regolith and delivering it to the weigh bay | done | 154 s |
| boarding the ship, taking a seat and flying a course | skipped (out of time) | 0 s |
| getting into and driving the survey rover | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | skipped (out of time) | 0 s |

People talked to: 13 of 16. Crew hired: 1. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / opening: typical 16 ms, slowest 7722 ms, 2 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 7558 ms, 3 frames over 250 ms
- iphone / dig: typical 16 ms, slowest 7376 ms, 2 frames over 250 ms
- iphone / tour: typical 16 ms, slowest 7329 ms, 2 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 5451 ms, 4 frames over 250 ms

Button response time (tap to something changing on screen): median 144 ms, slowest 567 ms over 24 taps.

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
