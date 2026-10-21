# The Cosmos playtest report

Run: 2026-10-03 09:52 (local)  |  Build under test: `6d58c42d7cd2e263d432`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 28 minutes, 238 screenshots, 48 distinct problems
- **Desktop (Chromium, keyboard + mouse)**: 7 minutes, 40 screenshots, 6 distinct problems

## Short version

30 distinct problems found: 2 blockers, 9 serious, 19 smaller.

- **The opening could not be finished, so the bot had to bypass it** (BLOCKER)
- **The opening is stuck at step 1** (BLOCKER, seen 3 times)
- **Nothing changed for 60+ seconds (same message, same place)** (Serious)
- **Nothing changed for 60+ seconds (same message, same place)** (Serious)
- **Nothing changed for 60+ seconds (same message, same place)** (Serious)

## Problems, worst first

### 1. The opening could not be finished, so the bot had to bypass it

- **How bad:** BLOCKER (score 99)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:39 into the run, on desktop (Chromium)
- **What happened:** After a refresh and the Walk button, the opening still would not move on. The rest of the run used the review start (?opening=off).
- **Screenshot:** [036-opening-PROBLEM-opening-bypassed.jpg](shots-desktop/036-opening-PROBLEM-opening-bypassed.jpg)

  ![The opening could not be finished, so th](shots-desktop/036-opening-PROBLEM-opening-bypassed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. mis-tap beside #opening-action
  1. tap #opening-action (mis-tap)
  1. press E
  1. REFRESH (opening stuck, trying a refresh)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening is blocked: bypassing with opening=off so the rest of the game can still be tested

### 2. The opening is stuck at step 1

- **How bad:** BLOCKER (score 97), happened 3 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 02:43 into the run, on desktop (Chromium)
- **What happened:** no progress for 93 s. caption: "", hint: "Move: WASD / left thumb · Look: mouse / right thumb", button: "Climb out (E)", position {"x":-2.7,"y":0,"z":13.7}
- **Later hits:** 04:41 no progress for 90 s. caption: "", hint: "Move: WASD / left thumb · Look: mouse / right thumb", button: "", position {"x":-2.7,"y":0,"z":-0.3} / 06:39 no progress for 90 s. caption: "", hint: "Move: WASD / left thumb · Look: mouse / right thumb", button: "", position {"x":-2.7,"y":0,"z":-11.7}
- **Screenshot:** [017-opening-PROBLEM-stuck-stage.jpg](shots-desktop/017-opening-PROBLEM-stuck-stage.jpg)

  ![The opening is stuck at step 1](shots-desktop/017-opening-PROBLEM-stuck-stage.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. mis-tap beside #opening-action
  1. tap #opening-action (mis-tap)
  1. tap #opening-action (opening action)
  1. mis-tap beside #opening-action
  1. tap #opening-action (mis-tap)
  1. tap #opening-action (opening action)
  1. mis-tap beside #opening-action
  1. tap #opening-action (opening action)

### 3. Nothing changed for 60+ seconds (same message, same place)

- **How bad:** Serious (score 86)
- **Where:** boarding the ship, taking a seat and flying a course, first at 21:12 into the run, on iPhone (WebKit)
- **What happened:** in "fly": position {"x":3.1,"y":0,"z":9}, button "", caption "", toast "", ship aboard
- **Screenshot:** [208-fly-PROBLEM-stuck-state.jpg](shots-iphone/208-fly-PROBLEM-stuck-state.jpg)

  ![Nothing changed for 60+ seconds (same me](shots-iphone/208-fly-PROBLEM-stuck-state.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. not getting closer (30 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (30 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. jump
  1. walk to back to the ship

### 4. Nothing changed for 60+ seconds (same message, same place)

- **How bad:** Serious (score 86)
- **Where:** free play (random walking, tapping, refreshing), first at 26:38 into the run, on iPhone (WebKit)
- **What happened:** in "freeplay": position {"x":3.1,"y":0,"z":9}, button "", caption "", toast "", ship aboard
- **Screenshot:** [234-freeplay-PROBLEM-stuck-state.jpg](shots-iphone/234-freeplay-PROBLEM-stuck-state.jpg)

  ![Nothing changed for 60+ seconds (same me](shots-iphone/234-freeplay-PROBLEM-stuck-state.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (9 m away), trying to get unstuck #8
  1. out of time, skipping home
  1. === phase rover starts
  1. my rover: null
  1. === phase freeplay starts
  1. tap #purse (idle fiddling)
  1. tap button "Close"
  1. jump

### 5. Nothing changed for 60+ seconds (same message, same place)

- **How bad:** Serious (score 86)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 02:18 into the run, on desktop (Chromium)
- **What happened:** in "opening": position {"x":-2.7,"y":0,"z":13.7}, button "Climb out (E)", caption "", toast "", ship outside
- **Screenshot:** [015-opening-PROBLEM-stuck-state.jpg](shots-desktop/015-opening-PROBLEM-stuck-state.jpg)

  ![Nothing changed for 60+ seconds (same me](shots-desktop/015-opening-PROBLEM-stuck-state.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. mis-tap beside #opening-action
  1. tap #opening-action (mis-tap)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. mis-tap beside #opening-action
  1. tap #opening-action (mis-tap)
  1. tap #opening-action (opening action)

### 6. Hiring Zuri Okafor 1 did not work

- **How bad:** Serious (score 84)
- **Where:** hiring crew from the crew hall, first at 11:49 into the run, on iPhone (WebKit)
- **What happened:** tapped Hire; they are still a candidate; marks 10000 -> 10000; screen said "Ada Chen 1Pilot · skill 82%✕Flies what you point her at. Keeps the ship off the rocks and out of trouble.Works at 82% of"
- **Screenshot:** [103-hire-PROBLEM-hire-failed.jpg](shots-iphone/103-hire-PROBLEM-hire-failed.jpg)

  ![Hiring Zuri Okafor 1 did not work](shots-iphone/103-hire-PROBLEM-hire-failed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #crew-talk (open hiring panel)
  1. hire result: status candidate, marks 10000 -> 10000
  1. walk to candidate Zuri Okafor 1
  1. route of 2 legs
  1. tap #crew-talk (open hiring panel)
  1. tap button "Meet Ada Chen 1 · 560 marks" (hire Zuri Okafor 1)
  1. the button said Meet first; waiting for the candidate to walk over, then Hire
  1. hire result: status candidate, marks 10000 -> 10000

### 7. Stuck while walking to back to the ship

- **How bad:** Serious (score 80), happened 2 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 22:21 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at shipworld -2,-8 (target 0,17, 25 m away)
- **Later hits:** 26:30 no progress for 56s at shipworld 3,9 (target 0,17, 9 m away)
- **Screenshot:** [211-fly-PROBLEM-stuck-walking.jpg](shots-iphone/211-fly-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to back to the ship](shots-iphone/211-fly-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (25 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (25 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. not getting closer (25 m away), trying to get unstuck #6
  1. not getting closer (25 m away), trying to get unstuck #7
  1. not getting closer (25 m away), trying to get unstuck #8

### 8. Stuck while walking to Shift runner

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 08:54 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -61,-41 (target -64,-41, 3 m away)
- **Screenshot:** [088-tour-PROBLEM-stuck-walking.jpg](shots-iphone/088-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Shift runner](shots-iphone/088-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (3 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 3 legs
  1. not getting closer (3 m away), trying to get unstuck #6
  1. not getting closer (3 m away), trying to get unstuck #7
  1. not getting closer (3 m away), trying to get unstuck #8

### 9. Stuck while walking to Lookout at the glass

- **How bad:** Serious (score 80)
- **Where:** walking the port and talking to people, first at 10:10 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at port -59,-41 (target -56,-41, 4 m away)
- **Screenshot:** [092-tour-PROBLEM-stuck-walking.jpg](shots-iphone/092-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Lookout at the gl](shots-iphone/092-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (4 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 3 legs
  1. not getting closer (4 m away), trying to get unstuck #6
  1. not getting closer (4 m away), trying to get unstuck #7
  1. not getting closer (4 m away), trying to get unstuck #8

### 10. The panel for candidate Ada Chen 1 has no Hire button

- **How bad:** Serious (score 78)
- **Where:** hiring crew from the crew hall, first at 11:22 into the run, on iPhone (WebKit)
- **What happened:** Ada Chen 1Pilot · skill 82%✕Flies what you point her at. Keeps the ship off the rocks and out of trouble.Works at 82% of a good hand: about 1.0 s to react, and a little off in the aim. Stays aboard un
- **Screenshot:** [099-hire-PROBLEM-no-hire-button.jpg](shots-iphone/099-hire-PROBLEM-no-hire-button.jpg)

  ![The panel for candidate Ada Chen 1 has n](shots-iphone/099-hire-PROBLEM-no-hire-button.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. refresh check: moved 0.0 m, marks 10000 -> 10000, aboard false -> false
  1. === phase hire starts
  1. candidates: Jorge(Navigator), Sunita(Gunner (dorsal)), Walter(Gunner (ventral)), Zuri Okafor 1(Captain), Ada Chen 1(Pilot), Aoi Patel 1(Communications officer), Ada Diaz 1(Pilot), Zuri Khan 1(Captain)
  1. walk to candidate Ada Chen 1
  1. route of 8 legs
  1. tap #crew-talk (open hiring panel)

### 11. Delivering to the weigh bay paid nothing

- **How bad:** Serious (score 78)
- **Where:** digging regolith and delivering it to the weigh bay, first at 16:00 into the run, on iPhone (WebKit)
- **What happened:** marks stayed 10000
- **Screenshot:** [162-dig-PROBLEM-deliver-no-pay.jpg](shots-iphone/162-dig-PROBLEM-deliver-no-pay.jpg)

  ![Delivering to the weigh bay paid nothing](shots-iphone/162-dig-PROBLEM-deliver-no-pay.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. tap #btn-action (action)
  1. dug 260 bites; cart 0.0/1054 -> 1042.2/1054
  1. walk to the amber weigh bay
  1. route of 15 legs
  1. tap #quest-deliver (deliver the tonne)
  1. delivery: marks 10000 -> 10000

### 12. Could not walk to Arrival guide

- **How bad:** Annoying (score 72)
- **Where:** walking the port and talking to people, first at 05:21 into the run, on iPhone (WebKit)
- **What happened:** gave up after 120s; last distance 12 m
- **Screenshot:** [044-tour-PROBLEM-cannot-reach.jpg](shots-iphone/044-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Arrival guide](shots-iphone/044-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #3
  1. jump
  1. not getting closer (9 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (9 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. route of 12 legs

### 13. Could not walk to a wander on phobos

- **How bad:** Annoying (score 72)
- **Where:** boarding the ship, taking a seat and flying a course, first at 21:06 into the run, on iPhone (WebKit)
- **What happened:** gave up after 60s; last distance 30 m
- **Screenshot:** [206-fly-PROBLEM-cannot-reach.jpg](shots-iphone/206-fly-PROBLEM-cannot-reach.jpg)

  ![Could not walk to a wander on phobos](shots-iphone/206-fly-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (30 m away), trying to get unstuck #3
  1. run-up jump #3
  1. jump
  1. not getting closer (30 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (30 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way

### 14. Could not walk to a wander on deimos

- **How bad:** Annoying (score 72)
- **Where:** boarding the ship, taking a seat and flying a course, first at 25:14 into the run, on iPhone (WebKit)
- **What happened:** gave up after 60s; last distance 30 m
- **Screenshot:** [226-fly-PROBLEM-cannot-reach.jpg](shots-iphone/226-fly-PROBLEM-cannot-reach.jpg)

  ![Could not walk to a wander on deimos](shots-iphone/226-fly-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (30 m away), trying to get unstuck #3
  1. run-up jump #3
  1. jump
  1. not getting closer (30 m away), trying to get unstuck #4
  1. run-up jump #4
  1. jump
  1. not getting closer (30 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way

### 15. Same message repeated 4+ times in a minute: "Down at Deimos (pad 04)."

- **How bad:** Annoying (score 70)
- **Where:** free play (random walking, tapping, refreshing), first at 27:42 into the run, on iPhone (WebKit)
- **What happened:** The game keeps saying the same thing instead of moving on.
- **Screenshot:** [236-freeplay-PROBLEM-repeating-message.jpg](shots-iphone/236-freeplay-PROBLEM-repeating-message.jpg)

  ![Same message repeated 4+ times in a minu](shots-iphone/236-freeplay-PROBLEM-repeating-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. REFRESH (random refresh while playing)
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. REFRESH (random refresh while playing)
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 16. Buttons are covered by something on top of them (13 places)

- **How bad:** Annoying (score 68), happened 13 times
- **Where:** opening the Settings / Account / World / Controls panels, first at 03:11 into the run, on iPhone (WebKit)
- **What happened:** #set-tool "Hand spade Shovel Excavator " is covered by div.settings-heading ;   "Hire Jorge" is covered by div.world-heading ;   "Decline" is covered by div.world-heading ;  #chip-range "Range" is covered by #space-sheet ;  #chip-course "Course" is covered by #space-sheet ;  #chip-jobs "Jobs" is covered by #space-sheet ;  #chip-range "Range" is covered by button.go ;  #chip-course "Course" is covered by button.go
- **Screenshot:** [030-panels-PROBLEM-covered.jpg](shots-iphone/030-panels-PROBLEM-covered.jpg)

  ![Buttons are covered by something on top ](shots-iphone/030-panels-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. opening stage 3 -> 4 (Zuri: Outer Accord. We saw you come down.)
  1. REFRESH (mid-ride)
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening finished
  1. === phase panels starts
  1. tap #btn-settings (open Settings)

### 17. Buttons overlap each other (11 places)

- **How bad:** Annoying (score 66), happened 11 times
- **Where:** opening the Settings / Account / World / Controls panels, first at 03:11 into the run, on iPhone (WebKit)
- **What happened:** #btn-close-settings "✕" overlaps #set-tool "Hand spade Shovel Excavator " by 77% ;  #chip-range "Range" overlaps  "Phobos7668 km · about 111 h " by 77% ;  #chip-course "Course" overlaps  "Phobos7668 km · about 111 h " by 78% ;  #chip-jobs "Jobs" overlaps  "Phobos7668 km · about 111 h " by 77% ;  #chip-range "Range" overlaps  "×1" by 48% ;  #chip-course "Course" overlaps  "×5" by 31% ;  #chip-course "Course" overlaps  "×20" by 34% ;  #chip-jobs "Jobs" overlaps  "×60" by 48%
- **Screenshot:** [029-panels-PROBLEM-overlap.jpg](shots-iphone/029-panels-PROBLEM-overlap.jpg)

  ![Buttons overlap each other (11 places)](shots-iphone/029-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. opening stage 3 -> 4 (Zuri: Outer Accord. We saw you come down.)
  1. REFRESH (mid-ride)
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening finished
  1. === phase panels starts
  1. tap #btn-settings (open Settings)

### 18. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 4 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 01:20 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 1 after tapping "Dig (E)"
- **Later hits:** 01:22 cuts stayed 1 after tapping "Dig (E)" / 01:24 cuts stayed 1 after tapping "Dig (E)"
- **Screenshot:** [012-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/012-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/012-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening stage 0 -> 1 (Move: WASD / left thumb · Look: mouse / right thumb)
  1. mis-tap beside #opening-action
  1. tap #opening-action (opening action)
  1. opening stage 1 -> 2 (Something lies beneath the collapsed dust.)
  1. walk to the crate
  1. tap #opening-action (opening action)
  1. mis-tap beside #opening-action
  1. tap #opening-action (opening action)

### 19. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 11 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:10 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** a single frame took 2910 ms (typical 16 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 01:34 a single frame took 2719 ms (typical 17 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 01:56 a single frame took 1155 ms (typical 16 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 ()

### 20. Frame-time spike during "freeplay"

- **How bad:** Annoying (score 62), happened 6 times
- **Where:** free play (random walking, tapping, refreshing), first at 26:54 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** a single frame took 2404 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 26:57 a single frame took 1839 ms (typical 32 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 27:17 a single frame took 2281 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [235-freeplay-PROBLEM-frame-spike.jpg](shots-iphone/235-freeplay-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "freeplay"](shots-iphone/235-freeplay-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. === phase freeplay starts
  1. tap #purse (idle fiddling)
  1. tap button "Close"
  1. jump
  1. jump
  1. REFRESH (random refresh while playing)
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 21. Frame-time spike during "opening-bypass"

- **How bad:** Annoying (score 62)
- **Where:** starting from the review start (opening skipped), first at 06:47 into the run, on desktop (Chromium)
- **What happened:** a single frame took 3725 ms (typical 4 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [037-opening-bypass-PROBLEM-frame-spike.jpg](shots-desktop/037-opening-bypass-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening-bypass"](shots-desktop/037-opening-bypass-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. mis-tap beside #opening-action
  1. tap #opening-action (mis-tap)
  1. press E
  1. REFRESH (opening stuck, trying a refresh)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening is blocked: bypassing with opening=off so the rest of the game can still be tested
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 22. No survey rover found for this player

- **How bad:** Annoying (score 60)
- **Where:** getting into and driving the survey rover, first at 26:30 into the run, on iPhone (WebKit)
- **What happened:** README says each Meridian carries one
- **Screenshot:** [231-rover-PROBLEM-no-rover.jpg](shots-iphone/231-rover-PROBLEM-no-rover.jpg)

  ![No survey rover found for this player](shots-iphone/231-rover-PROBLEM-no-rover.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (9 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. not getting closer (9 m away), trying to get unstuck #6
  1. not getting closer (9 m away), trying to get unstuck #7
  1. not getting closer (9 m away), trying to get unstuck #8
  1. out of time, skipping home
  1. === phase rover starts
  1. my rover: null

### 23. People standing exactly on top of each other (2 pairs)

- **How bad:** Minor (score 52), happened 93 times
- **Where:** hiring crew from the crew hall, first at 11:33 into the run, on iPhone (WebKit)
- **What happened:** Zuri Okafor 1 and Zuri Khan 1; Ada Chen 1 and Ada Diaz 1
- **Later hits:** 11:43 Zuri Okafor 1 and Zuri Khan 1; Ada Chen 1 and Ada Diaz 1 / 11:53 Zuri Okafor 1 and Zuri Khan 1; Ada Chen 1 and Ada Diaz 1
- **Screenshot:** [101-hire-PROBLEM-people-stacked.jpg](shots-iphone/101-hire-PROBLEM-people-stacked.jpg)

  ![People standing exactly on top of each o](shots-iphone/101-hire-PROBLEM-people-stacked.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. route of 8 legs
  1. tap #crew-talk (open hiring panel)
  1. hire result: status candidate, marks 10000 -> 10000
  1. walk to candidate Zuri Okafor 1
  1. route of 2 legs
  1. tap #crew-talk (open hiring panel)
  1. tap button "Meet Ada Chen 1 · 560 marks" (hire Zuri Okafor 1)
  1. the button said Meet first; waiting for the candidate to walk over, then Hire

### 24. Server connection (websocket) closed

- **How bad:** Minor (score 50), happened 8 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 01:24 into the run, on iPhone (WebKit)
- **What happened:** The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Later hits:** 02:06 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/ / 10:51 The live connection closed while playing: wss://cosmos.heartbeatobservatory.com/
- **Screenshot:** [014-opening-PROBLEM-ws-closed.jpg](shots-iphone/014-opening-PROBLEM-ws-closed.jpg)

  ![Server connection (websocket) closed](shots-iphone/014-opening-PROBLEM-ws-closed.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to the crate
  1. tap #opening-action (opening action)
  1. mis-tap beside #opening-action
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. REFRESH (mid-dig)
  1. websocket closed

### 25. Game said: "Cruise: raiders cannot follow a ship at this speed"

- **How bad:** Minor (score 42), happened 2 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 18:58 into the run, on iPhone (WebKit)
- **What happened:** shown in hud-readout while the bot was: 18:58 [fly] tap button "×60" (speed up ×60)
- **Later hits:** 22:53 shown in hud-readout while the bot was: 22:52 [fly] tap button "×60" (speed up ×60)
- **Screenshot:** [199-fly-PROBLEM-refusal-message.jpg](shots-iphone/199-fly-PROBLEM-refusal-message.jpg)

  ![Game said: "Cruise: raiders cannot follo](shots-iphone/199-fly-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap button "×20" (speed up ×20)
  1. trip phase ascent, warp x20, eta 0s
  1. tap button "×5" (speed up ×5)
  1. tap button "×20" (speed up ×20)
  1. tap on empty 3D view at 241,515
  1. tap button "×60" (speed up ×60)
  1. trip phase transit, warp x60, eta 1075s
  1. tap button "×60" (speed up ×60)

### 26. Game said: "Weather sensors are offline. Watch the dust outside."

- **How bad:** Minor (score 42)
- **Where:** walking the port and talking to people, first at 07:34 into the run, on iPhone (WebKit)
- **What happened:** shown in crew-panel while the bot was: 07:34 [tour] tap #crew-talk (Talk to Weather officer)
- **Screenshot:** [081-tour-PROBLEM-refusal-message.jpg](shots-iphone/081-tour-PROBLEM-refusal-message.jpg)

  ![Game said: "Weather sensors are offline.](shots-iphone/081-tour-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to Weather officer
  1. route of 5 legs
  1. tap #crew-talk (Talk to Weather officer)
  1. opened Ground controller instead of Weather officer; stepping closer to the right person
  1. tap button "✕" (close talk panel)
  1. go talk to Weather officer
  1. walk to Weather officer
  1. tap #crew-talk (Talk to Weather officer)

### 27. Frame-time spike during "fly"

- **How bad:** Minor (score 38), happened 4 times
- **Where:** boarding the ship, taking a seat and flying a course, first at 16:20 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 1263 ms (typical 28 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 18:13 a single frame took 730 ms (typical 29 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 19:16 a single frame took 755 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [169-fly-PROBLEM-frame-spike.jpg](shots-iphone/169-fly-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "fly"](shots-iphone/169-fly-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (refresh right after digging)
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. refresh check: moved 0.0 m, marks 10000 -> 10000, aboard false -> false
  1. === phase fly starts
  1. ship type courier; ship centre at port 278,-120; ramp foot 278,-101
  1. walk to the ship ramp
  1. route of 46 legs

### 28. Frame-time spike during "tour"

- **How bad:** Minor (score 38), happened 2 times
- **Where:** walking the port and talking to people, first at 03:32 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 848 ms (typical 27 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 10:58 a single frame took 2506 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [039-tour-PROBLEM-frame-spike.jpg](shots-iphone/039-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/039-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. mis-tap beside #btn-key-controls
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. go talk to Arrival guide
  1. walk to Arrival guide
  1. route of 36 legs

### 29. Frame-time spike during "hire"

- **How bad:** Minor (score 38)
- **Where:** hiring crew from the crew hall, first at 11:10 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 1131 ms (typical 29 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [096-hire-PROBLEM-frame-spike.jpg](shots-iphone/096-hire-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "hire"](shots-iphone/096-hire-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (refresh after the port tour)
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. refresh check: moved 0.0 m, marks 10000 -> 10000, aboard false -> false
  1. === phase hire starts
  1. candidates: Jorge(Navigator), Sunita(Gunner (dorsal)), Walter(Gunner (ventral)), Zuri Okafor 1(Captain), Ada Chen 1(Pilot), Aoi Patel 1(Communications officer), Ada Diaz 1(Pilot), Zuri Khan 1(Captain)
  1. walk to candidate Ada Chen 1
  1. route of 8 legs

### 30. Frame-time spike during "dig"

- **How bad:** Minor (score 38)
- **Where:** digging regolith and delivering it to the weigh bay, first at 16:07 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 2565 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [166-dig-PROBLEM-frame-spike.jpg](shots-iphone/166-dig-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "dig"](shots-iphone/166-dig-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to the amber weigh bay
  1. route of 15 legs
  1. tap #quest-deliver (deliver the tonne)
  1. delivery: marks 10000 -> 10000
  1. tap #btn-drop-all (drop all)
  1. REFRESH (refresh right after digging)
  1. websocket closed
  1. websocket open wss://cosmos.heartbeatobservatory.com/

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 180 s |
| opening the Settings / Account / World / Controls panels | done | 11 s |
| walking the port and talking to people | done | 450 s |
| hiring crew from the crew hall | done | 46 s |
| digging regolith and delivering it to the weigh bay | done | 251 s |
| boarding the ship, taking a seat and flying a course | done | 618 s |
| getting into and driving the survey rover | done | 0 s |
| free play (random walking, tapping, refreshing) | done | 90 s |

People talked to: 12 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: started; Deimos: started.

### Desktop (Chromium, keyboard + mouse)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - bypass | 397 s |
| opening the Settings / Account / World / Controls panels | skipped (out of time) | 0 s |
| walking the port and talking to people | skipped (out of time) | 0 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | done | 13 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- desktop / opening: typical 4 ms, slowest 5287 ms, 3 frames over 250 ms
- desktop / opening: typical 4 ms, slowest 3754 ms, 2 frames over 250 ms
- desktop / opening: typical 4 ms, slowest 3750 ms, 2 frames over 250 ms
- desktop / opening-bypass: typical 4 ms, slowest 3725 ms, 2 frames over 250 ms
- desktop / freeplay: typical 4 ms, slowest 3716 ms, 2 frames over 250 ms

Button response time (tap to something changing on screen): median 115 ms, slowest 880 ms over 25 taps.

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.

## Vision notes (screenshots looked at by Claude Sonnet 5.5 directly, because the API vision pass could not run)

The API key line `ANTHROPIC_API_KEY=` in `C:/Users/lilli/.secrets/keys.env` (line 63) is empty, and the Claude Code CLI fallback answers "OAuth token expired". So `play.mjs` skipped its automatic vision pass (it will use the key as soon as one is pasted in, or the CLI once it is logged in again). The agent who built the tester looked at the problem screenshots by hand instead:

- ![](shots-iphone/101-hire-PROBLEM-people-stacked.jpg) At the crew hall the name tags are huge grey translucent banners ("Aoi Patel", "Sunita") that run the full width of the phone screen and cover the horizon; the people themselves are small and turned away from the player. The tags look broken rather than designed.
- ![](shots-iphone/098-hire-no-hire-in-panel.jpg) After tapping Talk next to a candidate the player is standing facing a flat tan wall (a box or hull) at arm's length and no panel is on screen; the crew hall is blocked from view. The candidate pool shows people stacked on the same spot (Ada Chen 1 and Ada Diaz 1, Zuri Okafor 1 and Zuri Khan 1), so the Hire panel can name a different person than the one in front of you.
- The space Course/Jobs sheet on the phone sits on top of the navigation strip (Range / Course / Jobs) and the time-speed buttons, so those chips cannot be tapped while a sheet is open (see "Buttons are covered").
