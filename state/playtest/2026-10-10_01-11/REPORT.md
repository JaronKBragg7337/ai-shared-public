# The Cosmos playtest report

Run: 2026-10-10 01:11 (local)  |  Build under test: `ebf757b2335ac51bc73a`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

**How to read this:** items titled "Stuck while walking to ..." come from the bot's own steering (its path planner, run-ups and jumps). Treat them as bot-only unless a human also gets stuck at that spot. Black boot and crash-blackout frames that carry a caption are deliberate.

- **iPhone 15 (WebKit, touch)**: 15 minutes, 86 screenshots, 12 distinct problems
- **Desktop (Chromium, keyboard + mouse)**: 3 minutes, 38 screenshots, 14 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)
- Desktop (Chromium, keyboard + mouse): [session video](videos-desktop/<email>)

## Short version

36 distinct problems found: 0 blockers, 3 serious, 33 smaller.

- **Stuck while walking to Director Ila Sorn** (Serious)
- **Stuck while walking to Bram Okonkwo** (Serious)
- **After the graphics context was lost and restored, the game never drew again** (Serious)
- **Same message repeated 4+ times in a minute: "Aim the shovel at the dust around the crate."** (Annoying)
- **A button is covered by something else: #multiplayer-button "World / crew" is covered by #touch-key-KeyD** (Annoying)

## Problems, worst first

### 1. Stuck while walking to Director Ila Sorn

- **How bad:** Serious (score 80)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 11:42 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at outpost 8,-95 (target -8,-74, 4 m away)
- **What the vision model saw:** A status/map overlay screen for Callisto Valhalla Camp with quest text, a location marker, and 'World/crew' and 'Controls' buttons, over a backdrop of the game world. Flagged: Background behind the UI panel is almost entirely blown-out white/blurred with no recognizable scenery, inconsistent with a normal environment render
- **Screenshot:** [064-tour-PROBLEM-stuck-walking.jpg](shots-iphone/064-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Director Ila Sorn](shots-iphone/064-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (4 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. outpost route of 10 legs around 0 solid things
  1. not getting closer (4 m away), trying to get unstuck #6
  1. not getting closer (4 m away), trying to get unstuck #7
  1. not getting closer (4 m away), trying to get unstuck #8

### 2. Stuck while walking to Bram Okonkwo

- **How bad:** Serious (score 80)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 14:36 into the run, on iPhone (WebKit)
- **What happened:** no progress for 56s at outpost -19,-80 (target 6,-1198, 3 m away)
- **What the vision model saw:** iPhone tour view with the move joystick and HUD text visible, but the whole environment behind it is a washed-out, blurry white/grey haze with faint vertical streaks. Flagged: world geometry is not visibly rendering – screen is filled with a blurred white/grey haze instead of the camp environment, consistent with the camera being clipped inside an object while stuck
- **Screenshot:** [080-tour-PROBLEM-stuck-walking.jpg](shots-iphone/080-tour-PROBLEM-stuck-walking.jpg)

  ![Stuck while walking to Bram Okonkwo](shots-iphone/080-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. run-up jump #4
  1. jump
  1. not getting closer (3 m away), trying to get unstuck #5
  1. sidestep around whatever is in the way
  1. outpost route of 75 legs around 0 solid things
  1. not getting closer (3 m away), trying to get unstuck #6
  1. not getting closer (3 m away), trying to get unstuck #7
  1. not getting closer (3 m away), trying to get unstuck #8

### 3. After the graphics context was lost and restored, the game never drew again

- **How bad:** Serious (score 80)
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:42 into the run, on desktop (Chromium)
- **What happened:** (see screenshot)
- **Screenshot:** [027-lifecycle-PROBLEM-context-not-restored.jpg](shots-desktop/027-lifecycle-PROBLEM-context-not-restored.jpg)

  ![After the graphics context was lost and ](shots-desktop/027-lifecycle-PROBLEM-context-not-restored.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. jump
  1. QA pass: spam: 25 jumps and wild looks, game keeps drawing
  1. spam: 0 requests sent, purse 10000 -> 10000
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. QA FAIL: lifecycle: graphics context lost and restored, game draws again - events: ["lost"]

### 4. Same message repeated 4+ times in a minute: "Aim the shovel at the dust around the crate."

- **How bad:** Annoying (score 70)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:57 into the run, on iPhone (WebKit)
- **What happened:** The game keeps saying the same thing instead of moving on.
- **What the vision model saw:** Top-down dig minigame showing a crate, a highlighted dig circle in the dust, and a 'Dig (E)' button with instruction text.
- **Screenshot:** [038-opening-PROBLEM-repeating-message.jpg](shots-iphone/038-opening-PROBLEM-repeating-message.jpg)

  ![Same message repeated 4+ times in a minu](shots-iphone/038-opening-PROBLEM-repeating-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to the crate
  1. tap #opening-action (opening action)
  1. no dig button shown while standing at the crate
  1. no dig button shown while standing at the crate
  1. tap #opening-action (opening action)
  1. mis-tap beside #opening-action
  1. tap #opening-action (opening action)
  1. walk to the crate

### 5. A button is covered by something else: #multiplayer-button "World / crew" is covered by #touch-key-KeyD

- **How bad:** Annoying (score 68)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:35 into the run, on desktop (Chromium)
- **What happened:** #multiplayer-button "World / crew" is covered by #touch-key-KeyD (Controls open, desktop)
- **What the vision model saw:** Identical Mars pad view to the previous shot, with the Controls panel still open at bottom-left despite the action being to toggle it closed. Flagged: Action log says Controls was toggled closed, but the Controls panel is still fully visible on screen, covering the same bottom-left area (World/crew button still hidden underneath it)
- **Screenshot:** [012-panels-PROBLEM-covered.jpg](shots-desktop/012-panels-PROBLEM-covered.jpg)

  ![A button is covered by something else: #](shots-desktop/012-panels-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. mis-tap beside #btn-key-controls
  1. tap #btn-key-controls (open Controls)

### 6. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 11 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:27 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 4 after tapping "Dig (E)"
- **What the vision model saw:** Top-down dig-site view showing only a small sliver of yellow caution-striped flooring and a crate edge in the top-left corner. Flagged: Most of the screen is a flat, featureless dark reddish-brown void with no geometry or texture visible
- **Later hits:** 06:30 cuts stayed 4 after tapping "Dig (E)" / 06:33 cuts stayed 4 after tapping "Dig (E)"
- **Screenshot:** [035-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/035-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/035-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. REFRESH (mid-dig)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. tap #opening-action (opening action)

### 7. Buttons overlap: #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83%

- **How bad:** Annoying (score 66)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:35 into the run, on desktop (Chromium)
- **What happened:** #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83% (Controls open, desktop)
- **What the vision model saw:** Same Mars pad view with the status HUD still open at top and a Controls keybinding panel now open at bottom-left, replacing the World/crew button. Flagged: The Controls panel sits directly under the status/quest text box with only a few pixels of gap, and the World/crew button is gone/replaced without clear indication it moved
- **Screenshot:** [011-panels-PROBLEM-overlap.jpg](shots-desktop/011-panels-PROBLEM-overlap.jpg)

  ![Buttons overlap: #touch-key-KeyD "Right"](shots-desktop/011-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. mis-tap beside #btn-key-controls
  1. tap #btn-key-controls (open Controls)

### 8. Looks wrong in the screenshot: screen is washed out into bright white/pink blurry vertical bands, scene underneath is unreadable

- **How bad:** Annoying (score 63)
- **Where:** free play (random walking, tapping, refreshing), first at 15:01 into the run, on iPhone (WebKit)
- **What happened:** entire screen below the status panel (the vision model's description of the screen: End-of-freeplay screen is almost entirely blown-out white/pink with blurry vertical streaks, status panel barely readable at top.)
- **Screenshot:** [086-freeplay-end-of-freeplay.jpg](shots-iphone/086-freeplay-end-of-freeplay.jpg)

  ![Looks wrong in the screenshot: screen is](shots-iphone/086-freeplay-end-of-freeplay.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap on empty 3D view at 79,384

### 9. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 7 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:15 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 3983 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Interior view of a ship bay/corridor with railings and an orange dome structure outside the windows, while Walter speaks a line of dialogue about coffee.
- **Later hits:** 05:46 a single frame took 4110 ms (typical 27 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 05:57 a single frame took 1322 ms (typical 27 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 10. Frame-time spike during "lifecycle"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:50 into the run, on desktop (Chromium)
- **What happened:** a single frame took 4716 ms (typical 4 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 02:02 a single frame took 2841 ms (typical 25 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [028-lifecycle-PROBLEM-frame-spike.jpg](shots-desktop/028-lifecycle-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "lifecycle"](shots-desktop/028-lifecycle-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: spam: 25 jumps and wild looks, game keeps drawing
  1. spam: 0 requests sent, purse 10000 -> 10000
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. QA FAIL: lifecycle: graphics context lost and restored, game draws again - events: ["lost"]
  1. REFRESH (recovering after a lost graphics context)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 11. Frame-time spike during "network"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** network cut, refresh offline, slow connection, first at 02:31 into the run, on desktop (Chromium)
- **What happened:** a single frame took 5762 ms (typical 4 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 02:39 a single frame took 2596 ms (typical 33 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [035-network-PROBLEM-frame-spike.jpg](shots-desktop/035-network-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "network"](shots-desktop/035-network-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap button "Close" (close account-panel)
  1. QA pass: network: while offline the game keeps drawing and does not crash
  1. QA info: network: the game tells the player the connection is gone (within about 12 s) - connected flag true -> true; messages: 
  1. NETWORK BACK
  1. QA pass: network: after the network returns the game reconnects and answers again - 2 s
  1. QA pass: network: money and place unchanged by a network blip
  1. REFRESH (refresh after being offline)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 12. Frame-time spike during "tour"

- **How bad:** Annoying (score 62)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 14:47 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4533 ms (typical 15 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** iPhone tour view, same washed-out white/grey blurry background with vertical light streaks, HUD panel showing status text. Flagged: world geometry not rendering, screen is a blurred white/grey haze with faint vertical streaks instead of the scene; terrain label shows a bare dash instead of a terrain name
- **Screenshot:** [083-tour-PROBLEM-frame-spike.jpg](shots-iphone/083-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/083-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. sidestep around whatever is in the way
  1. outpost route of 75 legs around 0 solid things
  1. not getting closer (3 m away), trying to get unstuck #6
  1. not getting closer (3 m away), trying to get unstuck #7
  1. not getting closer (3 m away), trying to get unstuck #8
  1. REFRESH (refresh after the port tour)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 13. Frame-time spike during "freeplay"

- **How bad:** Annoying (score 62)
- **Where:** free play (random walking, tapping, refreshing), first at 14:55 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4417 ms (typical 30 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** iPhone freeplay start, same washed-out white/grey blurry background with vertical light streaks as the previous tour frame. Flagged: world geometry not rendering, screen is a blurred white/grey haze with faint vertical streaks instead of the scene; terrain label shows a bare dash instead of a terrain name
- **Screenshot:** [085-freeplay-PROBLEM-frame-spike.jpg](shots-iphone/085-freeplay-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "freeplay"](shots-iphone/085-freeplay-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (3 m away), trying to get unstuck #6
  1. not getting closer (3 m away), trying to get unstuck #7
  1. not getting closer (3 m away), trying to get unstuck #8
  1. REFRESH (refresh after the port tour)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. refresh check: moved 0.0 m, marks 10000 -> 10000, aboard false -> false
  1. === phase freeplay starts

### 14. Frame-time spike during "panels"

- **How bad:** Annoying (score 62)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:19 into the run, on desktop (Chromium)
- **What happened:** a single frame took 8033 ms (typical 4 ms); 7 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Desktop panels view: a Settings panel is open on the right over a Mars spaceport scene with a ship and buildings, guest account sign-in fields visible. Flagged: a thin sliver of an unidentified element peeks out from behind the right edge of the Settings panel
- **Screenshot:** [002-panels-PROBLEM-frame-spike.jpg](shots-desktop/002-panels-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "panels"](shots-desktop/002-panels-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. desktop budget is 3 min and the opening alone takes about 10: started from the review start (use --desktop-opening to play it)
  1. === phase panels starts

### 15. Frame-time spike during "smoke"

- **How bad:** Annoying (score 62)
- **Where:** smoke check (load time, download size, warm reload), first at 00:46 into the run, on desktop (Chromium)
- **What happened:** a single frame took 5154 ms (typical 4 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Same Mars landing pad scene as the prior shots, with the status HUD open and World/crew and Controls buttons showing at bottom-left (panel now closed).
- **Screenshot:** [014-smoke-PROBLEM-frame-spike.jpg](shots-desktop/014-smoke-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "smoke"](shots-desktop/014-smoke-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. mis-tap beside #btn-key-controls
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase smoke starts
  1. QA info: smoke: page transfer on a cold load - 250 requests, 1.3 MB over the wire (slowest: heartbeatobservatory.com/games/the-cosmos/src/world/edits.js 259 ms)
  1. QA pass: smoke: time from opening the link to the first drawn frames - 14.9 s (headless software rendering, a real phone is usually quicker to draw but slower to download)
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 16. Frame-time spike during "a11y"

- **How bad:** Annoying (score 62)
- **Where:** accessibility and readability scan, first at 00:55 into the run, on desktop (Chromium)
- **What happened:** a single frame took 3233 ms (typical 33 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [022-a11y-PROBLEM-frame-spike.jpg](shots-desktop/022-a11y-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "a11y"](shots-desktop/022-a11y-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.
  1. QA pass: a11y: tap targets at least 44 px (Apple guideline) - 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44
  1. QA FAIL: a11y: pinch-zoom is not locked off - width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
  1. QA pass: a11y: a volume or mute control exists
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"","hint":"","caption":"","hud":"Mars · Valles Marineris 13°59'56.9\"S 59°11'47.9\"W +2213.1 m Martian regolith · 3.72 m/s² Hauling cart: 0.0 / 1054 k

### 17. Looks wrong in the screenshot: world geometry not rendering, screen is a blurred white/grey haze with faint vertical streaks instead of the s

- **How bad:** Annoying (score 56), happened 2 times
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 14:48 into the run, on iPhone (WebKit)
- **What happened:** entire background below the HUD panel (the vision model's description of the screen: iPhone tour view, same washed-out white/grey blurry background with vertical light streaks, HUD panel showing status text.)
- **Screenshot:** [083-tour-PROBLEM-frame-spike.jpg](shots-iphone/083-tour-PROBLEM-frame-spike.jpg)

  ![Looks wrong in the screenshot: world geo](shots-iphone/083-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 18. Looks wrong in the screenshot: world geometry is not visibly rendering – screen is filled with a blurred white/grey haze instead of the camp 

- **How bad:** Annoying (score 56)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 14:36 into the run, on iPhone (WebKit)
- **What happened:** entire background behind the HUD and joystick (the vision model's description of the screen: iPhone tour view with the move joystick and HUD text visible, but the whole environment behind it is a washed-out, blurry white/grey haze with faint vertical streaks.)
- **Screenshot:** [080-tour-PROBLEM-stuck-walking.jpg](shots-iphone/080-tour-PROBLEM-stuck-walking.jpg)

  ![Looks wrong in the screenshot: world geo](shots-iphone/080-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (3 m away), trying to get unstuck #8

### 19. Console error

- **How bad:** Annoying (score 55), happened 6 times
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 12:27 into the run, on iPhone (WebKit)
- **What happened:** Failed to load resource: the server responded with a status of 404 ()
- **What the vision model saw:** Same Tomas Grey dialogue box open, but the background behind it has changed to a flat, almost featureless tan/brown ground with no visible detail. Flagged: ground behind the dialogue is a flat, blurry gradient with no texture, craters, or detail
- **Later hits:** 12:27 Failed to load resource: the server responded with a status of 404 () / 12:49 Failed to load resource: the server responded with a status of 404 ()
- **Screenshot:** [067-tour-PROBLEM-console-error.jpg](shots-iphone/067-tour-PROBLEM-console-error.jpg)

  ![Console error](shots-iphone/067-tour-PROBLEM-console-error.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (4 m away), trying to get unstuck #6
  1. not getting closer (4 m away), trying to get unstuck #7
  1. not getting closer (4 m away), trying to get unstuck #8
  1. go talk to Tomas Grey
  1. walk to Tomas Grey
  1. outpost route of 52 legs around 0 solid things
  1. mis-tap beside #crew-talk
  1. tap #crew-talk (Talk to Tomas Grey)

### 20. Request returned HTTP 404

- **How bad:** Minor (score 50), happened 6 times
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 12:27 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/undefined.jpg
- **What the vision model saw:** iPhone tour view: a dialogue box for Tomas Grey (quartermaster) is open with conversation options, over a dimly lit camp scene with a metal railing and starry sky.
- **Later hits:** 12:27 https://www.heartbeatobservatory.com/homes/people/undefined.jpg / 12:49 https://www.heartbeatobservatory.com/homes/people/undefined.jpg
- **Screenshot:** [066-tour-PROBLEM-http.jpg](shots-iphone/066-tour-PROBLEM-http.jpg)

  ![Request returned HTTP 404](shots-iphone/066-tour-PROBLEM-http.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (4 m away), trying to get unstuck #6
  1. not getting closer (4 m away), trying to get unstuck #7
  1. not getting closer (4 m away), trying to get unstuck #8
  1. go talk to Tomas Grey
  1. walk to Tomas Grey
  1. outpost route of 52 legs around 0 solid things
  1. mis-tap beside #crew-talk
  1. tap #crew-talk (Talk to Tomas Grey)

### 21. Looks wrong in the screenshot: Most of the screen is a flat, featureless dark reddish-brown void with no geometry or texture visible

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:27 into the run, on iPhone (WebKit)
- **What happened:** center and bottom ~85% of the frame (the vision model's description of the screen: Top-down dig-site view showing only a small sliver of yellow caution-striped flooring and a crate edge in the top-left corner.)
- **Screenshot:** [035-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/035-opening-PROBLEM-dig-tap-lost.jpg)

  ![Looks wrong in the screenshot: Most of t](shots-iphone/035-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to the crate

### 22. Looks wrong in the screenshot: The 'approaching vehicle' is a flat, untextured grey rectangular slab with no wheels, cab, or detail — looks l

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 07:05 into the run, on iPhone (WebKit)
- **What happened:** mid-ground, center of screen (the vision model's description of the screen: Exterior view of a cratered surface with a plain grey slab labeled as an approaching vehicle, seen from behind a fence/railing.)
- **Screenshot:** [039-opening-stage-5.jpg](shots-iphone/039-opening-stage-5.jpg)

  ![Looks wrong in the screenshot: The 'appr](shots-iphone/039-opening-stage-5.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening stage 4 -> 5 (A vehicle is approaching.)

### 23. Looks wrong in the screenshot: The entire game world is heavily blurred/out of focus, making the environment unrecognizable

- **How bad:** Minor (score 49)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 11:23 into the run, on iPhone (WebKit)
- **What happened:** whole screen except HUD text (the vision model's description of the screen: A tour/walking view that is almost entirely out of focus, with a small yellow triangle icon and translucent circle floating over the blurred scene, plus a dimmed HUD panel and 'World/crew'/'Controls' buttons.)
- **Screenshot:** [063-tour-walking.jpg](shots-iphone/063-tour-walking.jpg)

  ![Looks wrong in the screenshot: The entir](shots-iphone/063-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. outpost route of 10 legs around 0 solid things

### 24. Looks wrong in the screenshot: Background behind the UI panel is almost entirely blown-out white/blurred with no recognizable scenery, incons

- **How bad:** Minor (score 49)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 11:42 into the run, on iPhone (WebKit)
- **What happened:** full background behind the HUD panel and buttons (the vision model's description of the screen: A status/map overlay screen for Callisto Valhalla Camp with quest text, a location marker, and 'World/crew' and 'Controls' buttons, over a backdrop of the game world.)
- **Screenshot:** [064-tour-PROBLEM-stuck-walking.jpg](shots-iphone/064-tour-PROBLEM-stuck-walking.jpg)

  ![Looks wrong in the screenshot: Backgroun](shots-iphone/064-tour-PROBLEM-stuck-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (4 m away), trying to get unstuck #8

### 25. Looks wrong in the screenshot: diagonal blue/white striped moiré pattern, looks like a texture glitch rather than part of the scene

- **How bad:** Minor (score 49)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 14:07 into the run, on iPhone (WebKit)
- **What happened:** just under the top status panel, spanning the width of the screen (the vision model's description of the screen: Player is on a wooden plank/railing structure on Callisto with the status panel at top, a movement joystick at bottom left, and World/crew and Controls buttons at bottom.)
- **Screenshot:** [078-tour-walking.jpg](shots-iphone/078-tour-walking.jpg)

  ![Looks wrong in the screenshot: diagonal ](shots-iphone/078-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump

### 26. Looks wrong in the screenshot: the top instruction/status text is clipped and missing words where the World/crew panel overlaps it (e.g. jump

- **How bad:** Minor (score 49)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:31 into the run, on desktop (Chromium)
- **What happened:** top status bar, behind/right of the World/crew panel (the vision model's description of the screen: Desktop World/crew panel is open over a Mars landing pad scene with a ship and crew hall in the background.)
- **Screenshot:** [008-panels-panel-World-crew.jpg](shots-desktop/008-panels-panel-World-crew.jpg)

  ![Looks wrong in the screenshot: the top i](shots-desktop/008-panels-panel-World-crew.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-button (open World / crew)

### 27. Looks wrong in the screenshot: Action log says Controls was toggled closed, but the Controls panel is still fully visible on screen, covering

- **How bad:** Minor (score 49)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:35 into the run, on desktop (Chromium)
- **What happened:** bottom-left Controls panel (the vision model's description of the screen: Identical Mars pad view to the previous shot, with the Controls panel still open at bottom-left despite the action being to toggle it closed.)
- **Screenshot:** [012-panels-PROBLEM-covered.jpg](shots-desktop/012-panels-PROBLEM-covered.jpg)

  ![Looks wrong in the screenshot: Action lo](shots-desktop/012-panels-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (toggle closed Controls)

### 28. Slow button: #btn-settings took 3.6 s to respond

- **How bad:** Minor (score 44)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:20 into the run, on desktop (Chromium)
- **What happened:** open Settings
- **What the vision model saw:** First-person view on a Mars landing pad with the HUD status panel at top-left and the Settings panel open on the right side. Flagged: The 'Settings' button at the top-right stays visible and active even though the Settings panel is already open beneath/beside it, instead of changing state or being hidden
- **Screenshot:** [003-panels-PROBLEM-slow-button.jpg](shots-desktop/003-panels-PROBLEM-slow-button.jpg)

  ![Slow button: #btn-settings took 3.6 s to](shots-desktop/003-panels-PROBLEM-slow-button.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1&opening=off
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. desktop budget is 3 min and the opening alone takes about 10: started from the review start (use --desktop-opening to play it)
  1. === phase panels starts
  1. tap #btn-settings (open Settings)

### 29. Game said: "Mystara studies what Jupiter is singing about. We have the only safe r"

- **How bad:** Minor (score 42), happened 2 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 07:25 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 07:15 [opening] opening stage 5 -> 6 (GreyTomas Grey, Mystara, keeper of the camp's cupboards and, today, its rescue rover. We saw your beacon. We always see )
- **What the vision model saw:** Night beach/shoreline scene with a pale moon and stars overhead while Grey delivers a line of dialogue.
- **Later hits:** 07:46 shown in opening-caption while the bot was: 07:33 [opening] websocket open wss://cosmos.heartbeatobservatory.com/
- **Screenshot:** [042-opening-PROBLEM-refusal-message.jpg](shots-iphone/042-opening-PROBLEM-refusal-message.jpg)

  ![Game said: "Mystara studies what Jupiter](shots-iphone/042-opening-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. mis-tap beside #opening-action
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. opening stage 4 -> 5 (A vehicle is approaching.)
  1. walk to the rescue vehicle
  1. tap #opening-action (opening action)
  1. opening stage 5 -> 6 (GreyTomas Grey, Mystara, keeper of the camp's cupboards and, today, its rescue rover. We saw your beacon. We always see )

### 30. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:39 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 03:39 [opening] opening stage 0 -> 1 (StewardWelcome to Mars. Follow the amber lights to the big Arrivals sign. If you reach a fuel tank, you have taken touri)
- **What the vision model saw:** Dusk/night view of a Mars landing port with the Arrivals building and amber path lights, Steward giving a dialogue instruction with a Skip intro button top right.
- **Screenshot:** [017-opening-PROBLEM-refusal-message.jpg](shots-iphone/017-opening-PROBLEM-refusal-message.jpg)

  ![Game said: "Welcome to Mars. Follow the ](shots-iphone/017-opening-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. in the boarding hall, waiting for the gangway to come down
  1. walk to down the gangway
  1. walk to down the gangway
  1. walk to down the gangway
  1. opening stage 0 -> 1 (StewardWelcome to Mars. Follow the amber lights to the big Arrivals sign. If you reach a fuel tank, you have taken touri)

### 31. Low text contrast in 2 places

- **How bad:** Minor (score 38)
- **Where:** accessibility and readability scan, first at 00:54 into the run, on desktop (Chromium)
- **What happened:** span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
- **What the vision model saw:** Same Mars landing pad scene, HUD open at top, World/crew and Controls buttons at bottom-left, during an accessibility contrast check. Flagged: Dim grey-brown text ('Martian regolith...', 'Hauling cart...', 'tool: Shovel') has low contrast against the dark brown panel background, falling below comfortable readability
- **Screenshot:** [018-a11y-PROBLEM-a11y-contrast.jpg](shots-desktop/018-a11y-PROBLEM-a11y-contrast.jpg)

  ![Low text contrast in 2 places](shots-desktop/018-a11y-PROBLEM-a11y-contrast.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 11.0 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"

### 32. Text smaller than 11 px in 2 places (hard to read on a phone)

- **How bad:** Minor (score 36)
- **Where:** accessibility and readability scan, first at 00:54 into the run, on desktop (Chromium)
- **What happened:** span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
- **What the vision model saw:** Same Mars landing pad scene, HUD open at top, World/crew and Controls buttons at bottom-left, during an accessibility small-text check. Flagged: Secondary HUD lines ('Martian regolith · 3.72 m/s²', 'Hauling cart: 0.0 / 1054 kg', 'tool: Shovel') are small and low-contrast grey text on a dark brown background, hard to read
- **Screenshot:** [017-a11y-PROBLEM-a11y-small-text.jpg](shots-desktop/017-a11y-PROBLEM-a11y-small-text.jpg)

  ![Text smaller than 11 px in 2 places (har](shots-desktop/017-a11y-PROBLEM-a11y-small-text.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: smoke: time from opening the link to the first drawn frames - 14.9 s (headless software rendering, a real phone is usually quicker to draw but slower to download)
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 11.0 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"

### 33. 1 buttons have no text or label (a screen reader says nothing)

- **How bad:** Small (score 34)
- **Where:** accessibility and readability scan, first at 00:54 into the run, on desktop (Chromium)
- **What happened:** input.
- **What the vision model saw:** Mars spaceport scene (Valles Marineris / Marineris Port) with a large HUD info panel top-left showing location, cargo and a 'NEXT' objective, and two menu buttons ('World/crew', 'Controls') bottom-left. Flagged: Solid cyan/teal quadrilateral shape floating at the very left edge of the screen, partly clipped off-screen, sitting on the ground near the ramp
- **Screenshot:** [019-a11y-PROBLEM-a11y-noname.jpg](shots-desktop/019-a11y-PROBLEM-a11y-noname.jpg)

  ![1 buttons have no text or label (a scree](shots-desktop/019-a11y-PROBLEM-a11y-noname.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 11.0 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.

### 34. textures grew from 122 to 246 over the run (new areas loading, or a leak)

- **How bad:** Small (score 30)
- **Where:** free play (random walking, tapping, refreshing), first at 15:02 into the run, on iPhone (WebKit)
- **What happened:** samples 45; phases opening -> freeplay. Only a leak if it keeps climbing while standing still: the idle check measures that.

- **Steps to reproduce (what the bot did just before):**
  1. not getting closer (3 m away), trying to get unstuck #7
  1. not getting closer (3 m away), trying to get unstuck #8
  1. REFRESH (refresh after the port tour)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. refresh check: moved 0.0 m, marks 10000 -> 10000, aboard false -> false
  1. === phase freeplay starts
  1. tap on empty 3D view at 79,384

### 35. Zooming the page is switched off in the viewport tag

- **How bad:** Small (score 30)
- **Where:** accessibility and readability scan, first at 00:54 into the run, on desktop (Chromium)
- **What happened:** width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
- **Screenshot:** [020-a11y-PROBLEM-a11y-zoom-locked.jpg](shots-desktop/020-a11y-PROBLEM-a11y-zoom-locked.jpg)

  ![Zooming the page is switched off in the ](shots-desktop/020-a11y-PROBLEM-a11y-zoom-locked.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel"
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.
  1. QA pass: a11y: tap targets at least 44 px (Apple guideline) - 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44
  1. QA FAIL: a11y: pinch-zoom is not locked off - width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover

### 36. Network cut for about 12 s and the game said nothing and still thinks it is connected

- **How bad:** Small (score 28)
- **Where:** network cut, refresh offline, slow connection, first at 02:19 into the run, on desktop (Chromium)
- **What happened:** connected=true. A hint only: the bot's offline switch may not cut a socket that is already open, so a real phone going into a tunnel could behave differently.
- **Screenshot:** [034-network-PROBLEM-offline-silent.jpg](shots-desktop/034-network-PROBLEM-offline-silent.jpg)

  ![Network cut for about 12 s and the game ](shots-desktop/034-network-PROBLEM-offline-silent.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: lifecycle: rotate to 900x560 with Settings open, the 3D view fills the screen - {"cw":900,"ch":560,"iw":900,"ih":560}
  1. tap #btn-close-settings (close settings)
  1. === phase network starts
  1. NETWORK CUT
  1. tap #purse (tap while offline)
  1. tap button "Close" (close account-panel)
  1. QA pass: network: while offline the game keeps drawing and does not crash
  1. QA info: network: the game tells the player the connection is gone (within about 12 s) - connected flag true -> true; messages: 

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 506 s |
| opening the Settings / Account / World / Controls panels | done | 11 s |
| walking the port (or the settlement of the start world) and talking to people | done - settlement Callisto: 3 of 5 talked to | 344 s |
| earning the first ship: buy the two lifeboat parts and fit them | skipped (out of time) | 0 s |
| smoke check (load time, download size, warm reload) | skipped (out of time) | 0 s |
| accessibility and readability scan | skipped (out of time) | 0 s |
| app to the background, graphics context lost, phone rotated | skipped (out of time) | 0 s |
| network cut, refresh offline, slow connection | skipped (out of time) | 0 s |
| spamming buttons and jumps | skipped (out of time) | 0 s |
| buy/sell loops and double taps on the shop | skipped (out of time) | 0 s |
| walking and jumping into walls and edges in 8 directions | skipped (out of time) | 0 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| boarding the ship, taking a seat and flying a course | skipped (out of time) | 0 s |
| turning on the spot, reading draw calls and frame times | skipped (out of time) | 0 s |
| random tapping everywhere | skipped (out of time) | 0 s |
| leaving the game alone for 90 s | skipped (out of time) | 0 s |
| end-of-run soft-lock check | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | done | 6 s |

People talked to: 3 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

### Desktop (Chromium, keyboard + mouse)

| Step | Result | Time |
|---|---|---|
| opening the Settings / Account / World / Controls panels | done | 21 s |
| smoke check (load time, download size, warm reload) | done | 11 s |
| accessibility and readability scan | done | 7 s |
| spamming buttons and jumps | done | 25 s |
| app to the background, graphics context lost, phone rotated | done | 43 s |
| network cut, refresh offline, slow connection | done | 36 s |
| turning on the spot, reading draw calls and frame times | skipped (out of time) | 0 s |
| random tapping everywhere | skipped (out of time) | 0 s |
| walking and jumping into walls and edges in 8 directions | skipped (out of time) | 0 s |
| walking the port (or the settlement of the start world) and talking to people | skipped (out of time) | 0 s |
| earning the first ship: buy the two lifeboat parts and fit them | skipped (out of time) | 0 s |
| buy/sell loops and double taps on the shop | skipped (out of time) | 0 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| leaving the game alone for 90 s | skipped (out of time) | 0 s |
| end-of-run soft-lock check | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | done | 22 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- desktop / panels: typical 4 ms, slowest 8033 ms, 7 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 7227 ms, 3 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 6770 ms, 3 frames over 250 ms
- desktop / network: typical 4 ms, slowest 5762 ms, 3 frames over 250 ms
- desktop / smoke: typical 4 ms, slowest 5154 ms, 3 frames over 250 ms

Button response time (tap to something changing on screen): median 603 ms, slowest 3582 ms over 11 taps.

## QA checks (the things real testers do besides playing through)

See `tools/playtester/PRACTICES.md` for why each one exists. FAIL rows are also listed as problems above where they are real bugs.

### Desktop (Chromium, keyboard + mouse): 15 passed, 5 failed, 1 skipped, 2 info

| Check | Result | Notes |
|---|---|---|
| smoke: page transfer on a cold load | info | 250 requests, 1.3 MB over the wire (slowest: heartbeatobservatory.com/games/the-cosmos/src/world/edits.js 259 ms) |
| smoke: time from opening the link to the first drawn frames | pass | 14.9 s (headless software rendering, a real phone is usually quicker to draw but slower to download) |
| smoke: warm reload comes back | pass | 11.0 s |
| a11y: text is at least 11 px | FAIL | 2 small: span.hint 10px "Third person to inspect " ; span.hint 10px "Spade for detail, shovel" |
| a11y: text contrast (4.5:1, or 3:1 for big text) | FAIL | 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel" |
| a11y: every button has a name | FAIL | input. |
| a11y: tap targets at least 44 px (Apple guideline) | pass | 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44 |
| a11y: pinch-zoom is not locked off | FAIL | width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover |
| a11y: a volume or mute control exists | pass |  |
| readability: something on screen tells a player what to do next | pass | {"action":"","hint":"","caption":"","hud":"Mars · Valles Marineris 13°59'56.9\"S 59°11'47.9\"W +2213.1 m Martian regolith · 3.72 m/s² Hauling cart: 0.0 / 1054 kg too","jobs":"","toast":"Systems nominal. Ship down and sta |
| spam: opener buttons hammered 10 times each, panels still open and close cleanly | pass |  |
| spam: action button | skipped | button says "" (not safe to hammer) |
| spam: 25 jumps and wild looks, game keeps drawing | pass |  |
| lifecycle: background 8 s and return keeps place, money and ship state | pass |  |
| lifecycle: graphics context lost and restored, game draws again | FAIL | events: ["lost"] |
| lifecycle: rotate to 900x560, the 3D view fills the screen | pass | {"cw":900,"ch":560,"iw":900,"ih":560} |
| lifecycle: rotate to 900x560 with Settings open, the 3D view fills the screen | pass | {"cw":900,"ch":560,"iw":900,"ih":560} |
| network: while offline the game keeps drawing and does not crash | pass |  |
| network: the game tells the player the connection is gone (within about 12 s) | info | connected flag true -> true; messages:  |
| network: after the network returns the game reconnects and answers again | pass | 2 s |
| network: money and place unchanged by a network blip | pass |  |
| network: refresh while offline, then online again, the game comes back | pass |  |
| network: slow connection (900 ms, 60 KB/s) for a panel tap | pass | 5 s |

## Load, size and memory

- **iPhone 15 (WebKit, touch)**: load to first frames 14.6 s; cold-load download 1.3 MB in 250 requests; warm reload not measured; busiest view not measured. Over the run (48 samples): graphics geometries 338 -> 159, textures 122 -> 246, page elements 236 -> 223 (JS heap is only readable in Chromium).
- **Desktop (Chromium, keyboard + mouse)**: load to first frames 14.9 s; cold-load download 1.3 MB in 250 requests; warm reload 11.0 s; busiest view not measured. Over the run (15 samples): graphics geometries 363 -> 401, textures 206 -> 208, page elements 277 -> 235, JS heap 245 -> 240 MB.

## Vision pass

A vision model (claude CLI (sonnet)) looked at 36 screenshots for about $0.00 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
- Not possible from here (needs a real iPhone or two players): a real phone call or notification banner, lock screen, battery and heat, low-end phone speed, many device models, race-condition duplication between two players. The full list of what real QA does and which parts the bot covers is in tools/playtester/PRACTICES.md.
