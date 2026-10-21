# The Cosmos playtest report

Run: 2026-10-10 02:14 (local)  |  Build under test: `ac9cf3851c91bc8dbacb`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

**How to read this:** items titled "Stuck while walking to ..." come from the bot's own steering (its path planner, run-ups and jumps). Treat them as bot-only unless a human also gets stuck at that spot. Black boot and crash-blackout frames that carry a caption are deliberate.

- **iPhone 15 (WebKit, touch)**: 15.8 minutes, 84 screenshots, 7 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)

## Short version

10 distinct problems found: 0 blockers, 0 serious, 10 smaller.

- **Could not walk to Bram Okonkwo** (Annoying)
- **A Dig tap in the opening made no cut** (Annoying, seen 6 times)
- **Frame-time spike during "opening"** (Annoying, seen 8 times)
- **Frame-time spike during "tour"** (Annoying)
- **Console error** (Annoying, seen 8 times)

## Problems, worst first

### 1. Could not walk to Bram Okonkwo

- **How bad:** Annoying (score 72)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 15:29 into the run, on iPhone (WebKit)
- **What happened:** gave up after 240s; last distance 89 m
- **What the vision model saw:** Outdoor camp view on a cratered surface with an orange triangular marker floating in the sky and World/crew and Controls buttons at bottom left. Flagged: Orange triangle waypoint marker floats alone in open sky with nothing else indicating what it points to or an associated path/route
- **Screenshot:** [080-tour-PROBLEM-cannot-reach.jpg](shots-iphone/080-tour-PROBLEM-cannot-reach.jpg)

  ![Could not walk to Bram Okonkwo](shots-iphone/080-tour-PROBLEM-cannot-reach.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to Farah Adeyemi
  1. outpost route of 33 legs around 35 solid things
  1. tap #crew-talk (Talk to Farah Adeyemi)
  1. tap button "What jobs are there?" (ask them something)
  1. tap button "✕" (close talk panel)
  1. go talk to Bram Okonkwo
  1. walk to Bram Okonkwo
  1. outpost route of 81 legs around 35 solid things

### 2. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 6 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:26 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 4 after tapping "Dig (E)"
- **What the vision model saw:** Close-up dig interaction on dark regolith next to a crate, with a dig-target circle and a Dig (E) button.
- **Later hits:** 06:29 cuts stayed 4 after tapping "Dig (E)" / 06:31 cuts stayed 4 after tapping "Dig (E)"
- **Screenshot:** [034-opening-PROBLEM-dig-tap-lost.jpg](shots-iphone/034-opening-PROBLEM-dig-tap-lost.jpg)

  ![A Dig tap in the opening made no cut](shots-iphone/034-opening-PROBLEM-dig-tap-lost.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. REFRESH (mid-dig)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. tap #opening-action (opening action)

### 3. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 8 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:15 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4192 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** First-person view inside a ship interior near a round cargo/engine dome, with movement instructions at top and Walter's dialogue line at the bottom. Flagged: A solid gray horizontal bar/pill floats across the width of the screen just below the instruction text, not attached to any visible structure; Two thin vertical white line slivers with no clear geometry behind them, floating in the room
- **Later hits:** 05:46 a single frame took 4824 ms (typical 27 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 05:55 a single frame took 1345 ms (typical 26 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 4. Frame-time spike during "tour"

- **How bad:** Annoying (score 62)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 15:41 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4580 ms (typical 16 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Tour phase on Callisto's Valhalla Camp: a lunar/moon surface stretches into a black starless sky, with a status panel (location, cart load, current tool, NEXT objective) top-left, a Settings button top-right, and World/crew and Controls buttons bottom-left.
- **Screenshot:** [083-tour-PROBLEM-frame-spike.jpg](shots-iphone/083-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/083-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap button "What jobs are there?" (ask them something)
  1. tap button "✕" (close talk panel)
  1. go talk to Bram Okonkwo
  1. walk to Bram Okonkwo
  1. outpost route of 81 legs around 35 solid things
  1. REFRESH (refresh after the port tour)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 5. Console error

- **How bad:** Annoying (score 55), happened 8 times
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 10:05 into the run, on iPhone (WebKit)
- **What happened:** Failed to load resource: the server responded with a status of 404 ()
- **What the vision model saw:** Same Director Ila Sorn dialogue panel as the previous shot, with no visible change.
- **Later hits:** 10:06 Failed to load resource: the server responded with a status of 404 () / 10:40 Failed to load resource: the server responded with a status of 404 ()
- **Screenshot:** [057-tour-PROBLEM-console-error.jpg](shots-iphone/057-tour-PROBLEM-console-error.jpg)

  ![Console error](shots-iphone/057-tour-PROBLEM-console-error.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. settlement world Callisto: people Director Ila Sorn, Tomas Grey, Odette Marsh, Farah Adeyemi, Bram Okonkwo
  1. go talk to Director Ila Sorn
  1. walk to Director Ila Sorn
  1. outpost route of 80 legs around 35 solid things
  1. tap #crew-talk (Talk to Director Ila Sorn)

### 6. Request returned HTTP 404

- **How bad:** Minor (score 50), happened 8 times
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 10:05 into the run, on iPhone (WebKit)
- **What happened:** https://www.heartbeatobservatory.com/homes/people/undefined.jpg
- **What the vision model saw:** Dialogue panel open with Director Ila Sorn at Valhalla Camp, showing camp stats, a NEXT objective box, and dialogue choice buttons.
- **Later hits:** 10:06 https://www.heartbeatobservatory.com/homes/people/undefined.jpg / 10:40 https://www.heartbeatobservatory.com/homes/people/undefined.jpg
- **Screenshot:** [056-tour-PROBLEM-http.jpg](shots-iphone/056-tour-PROBLEM-http.jpg)

  ![Request returned HTTP 404](shots-iphone/056-tour-PROBLEM-http.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase tour starts
  1. settlement world Callisto: people Director Ila Sorn, Tomas Grey, Odette Marsh, Farah Adeyemi, Bram Okonkwo
  1. go talk to Director Ila Sorn
  1. walk to Director Ila Sorn
  1. outpost route of 80 legs around 35 solid things
  1. tap #crew-talk (Talk to Director Ila Sorn)

### 7. Looks wrong in the screenshot: NPC models look like unfinished placeholder mannequins — no face/texture detail, head appears to float just ab

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 02:38 into the run, on iPhone (WebKit)
- **What happened:** both figures in the stalls, left and right (the vision model's description of the screen: Two humanoid figures stand in locker-room-style stalls, each a plain white mannequin with a featureless round head, blocky torso/arms, and separate cylindrical legs.)
- **Screenshot:** [012-opening-opening.jpg](shots-iphone/012-opening-opening.jpg)

  ![Looks wrong in the screenshot: NPC model](shots-iphone/012-opening-opening.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. in the boarding hall, waiting for the gangway to come down

### 8. Looks wrong in the screenshot: UI text and panel content are rendered at extremely low contrast against a near-black background, making almos

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 08:18 into the run, on iPhone (WebKit)
- **What happened:** across the whole screen, especially the top text block and bottom buttons (the vision model's description of the screen: Near-black screen at the end of the opening sequence with a faint 'SKIFF 7' label and two barely-visible buttons at the bottom, plus illegible dark header text.)
- **Screenshot:** [043-opening-opening-done.jpg](shots-iphone/043-opening-opening-done.jpg)

  ![Looks wrong in the screenshot: UI text a](shots-iphone/043-opening-opening-done.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening finished

### 9. Looks wrong in the screenshot: Scene is washed out to near-solid pale beige/white with almost no visible terrain detail, far more extreme tha

- **How bad:** Minor (score 49)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 14:25 into the run, on iPhone (WebKit)
- **What happened:** entire viewport below the HUD panel (the vision model's description of the screen: Walking view where the screen has gone almost entirely flat beige/white with very low contrast, showing only the HUD, direction arrow, waypoint circle, and newly-appeared Shovel/Dig buttons.)
- **Screenshot:** [077-tour-walking.jpg](shots-iphone/077-tour-walking.jpg)

  ![Looks wrong in the screenshot: Scene is ](shots-iphone/077-tour-walking.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. outpost route of 81 legs around 35 solid things

### 10. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:37 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 03:37 [opening] walk to the arrivals hall board
- **What the vision model saw:** Dusk Mars landing pad exterior with a Steward's welcome dialogue at the bottom and a Skip intro button top right.
- **Screenshot:** [017-opening-PROBLEM-refusal-message.jpg](shots-iphone/017-opening-PROBLEM-refusal-message.jpg)

  ![Game said: "Welcome to Mars. Follow the ](shots-iphone/017-opening-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. in the boarding hall, waiting for the gangway to come down
  1. walk to down the gangway
  1. walk to down the gangway
  1. walk to down the gangway
  1. opening stage 0 -> 1 (StewardWelcome to Mars. Follow the amber lights to the big Arrivals sign. If you reach a fuel tank, you have taken touri)
  1. walk to the arrivals hall board

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 485 s |
| opening the Settings / Account / World / Controls panels | done | 10 s |
| walking the port (or the settlement of the start world) and talking to people | done - settlement Callisto: 4 of 5 talked to | 419 s |
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
| free play (random walking, tapping, refreshing) | skipped (out of time) | 0 s |

People talked to: 4 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / opening: typical 25 ms, slowest 7011 ms, 3 frames over 250 ms
- iphone / opening: typical 15 ms, slowest 5416 ms, 2 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 5170 ms, 4 frames over 250 ms
- iphone / opening: typical 27 ms, slowest 4824 ms, 1 frames over 250 ms
- iphone / tour: typical 16 ms, slowest 4580 ms, 2 frames over 250 ms

Button response time (tap to something changing on screen): median 115 ms, slowest 140 ms over 8 taps.

## Load, size and memory

- **iPhone 15 (WebKit, touch)**: load to first frames 14.8 s; cold-load download 1.3 MB in 250 requests; warm reload not measured; busiest view not measured. Over the run (49 samples): graphics geometries 329 -> 32, textures 122 -> 12, page elements 236 -> 219 (JS heap is only readable in Chromium).

## Vision pass

A vision model (claude CLI (sonnet)) looked at 36 screenshots for about $0.00 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
- Not possible from here (needs a real iPhone or two players): a real phone call or notification banner, lock screen, battery and heat, low-end phone speed, many device models, race-condition duplication between two players. The full list of what real QA does and which parts the bot covers is in tools/playtester/PRACTICES.md.
