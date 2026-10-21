# The Cosmos playtest report

Run: 2026-10-09 00:03 (local)  |  Build under test: `7b8a58d96396c0a7036e`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

**How to read this:** items titled "Stuck while walking to ..." come from the bot's own steering (its path planner, run-ups and jumps). Treat them as bot-only unless a human also gets stuck at that spot. Black boot and crash-blackout frames that carry a caption are deliberate.

- **iPhone 15 (WebKit, touch)**: 15.5 minutes, 89 screenshots, 10 distinct problems
- **Desktop (Chromium, keyboard + mouse)**: 5.2 minutes, 49 screenshots, 19 distinct problems

## Videos

Playwright recordings (session length; include the spots phase):
- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)
- Desktop (Chromium, keyboard + mouse): [session video](videos-desktop/<email>)

## Short version

32 distinct problems found: 0 blockers, 1 serious, 31 smaller.

- **Game said: "fetch failed"** (Serious)
- **Buttons are covered by something on top of them (2 places)** (Annoying, seen 2 times)
- **A Dig tap in the opening made no cut** (Annoying, seen 4 times)
- **Buttons overlap each other (2 places)** (Annoying, seen 2 times)
- **Frame-time spike during "opening"** (Annoying, seen 8 times)

## Problems, worst first

### 1. Game said: "fetch failed"

- **How bad:** Serious (score 80)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:42 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 06:41 [opening] tap #opening-action (opening action)
- **What the vision model saw:** A crate sits on a hauling cart/trailer in a grassy field, with a 'fetch failed' message and a Carry button showing a spinning/loading icon. Flagged: 'fetch failed' error text displayed on screen; Carry button shows a spinning loading icon instead of resolving
- **Screenshot:** [036-opening-PROBLEM-refusal-message.jpg](shots-iphone/036-opening-PROBLEM-refusal-message.jpg)

  ![Game said: "fetch failed"](shots-iphone/036-opening-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)
  1. tap #opening-action (opening action)

### 2. Buttons are covered by something on top of them (2 places)

- **How bad:** Annoying (score 68), happened 2 times
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:38 into the run, on desktop (Chromium)
- **What happened:** #multiplayer-button "World / crew" is covered by #touch-key-KeyD ;  #voice-talk "Hold B to talkno one near" is covered by #touch-key-KeyW
- **What the vision model saw:** Mars pad scene with the Controls panel now closed, showing the lander, ramp, and PAD 08 marker with only the top HUD info panel and the Hold B to talk / World crew / Controls buttons visible. Flagged: Same unexplained cyan shape clipped at the left screen edge, present across all four desktop panel shots
- **Screenshot:** [012-panels-PROBLEM-covered.jpg](shots-desktop/012-panels-PROBLEM-covered.jpg)

  ![Buttons are covered by something on top ](shots-desktop/012-panels-PROBLEM-covered.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. mis-tap beside #purse
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)

### 3. A Dig tap in the opening made no cut

- **How bad:** Annoying (score 66), happened 4 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:31 into the run, on iPhone (WebKit)
- **What happened:** cuts stayed 4 after tapping "Dig (E)"
- **What the vision model saw:** Overhead view of dusty grass/dirt terrain with a glowing aim reticle and a prompt to dig around a crate, with a Dig button bottom right.
- **Later hits:** 06:33 cuts stayed 4 after tapping "Dig (E)" / 06:34 cuts stayed 4 after tapping "Dig (E)"
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

### 4. Buttons overlap each other (2 places)

- **How bad:** Annoying (score 66), happened 2 times
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:38 into the run, on desktop (Chromium)
- **What happened:** #touch-key-KeyW "Forward" overlaps #voice-talk "Hold B to talkno one near" by 97% ;  #touch-key-KeyD "Right" overlaps #multiplayer-button "World / crew" by 83%
- **What the vision model saw:** Same Mars pad scene with the Controls panel open, listing keybindings (Debug, View, Talk/hire, Fire, Forward/Back/Left/Right, Run, Close panels, etc.). Flagged: Same unexplained cyan shape clipped at the left screen edge as in image 3
- **Screenshot:** [010-panels-PROBLEM-overlap.jpg](shots-desktop/010-panels-PROBLEM-overlap.jpg)

  ![Buttons overlap each other (2 places)](shots-desktop/010-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #set-voice-mute (toggle back)
  1. tap #btn-close-settings (close Settings)
  1. mis-tap beside #purse
  1. tap #purse (open Account / purse)
  1. tap #account-panel .account-close (close Account / purse)
  1. tap #multiplayer-button (open World / crew)
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)

### 5. Frame-time spike during "opening"

- **How bad:** Annoying (score 62), happened 8 times
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 00:14 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 3938 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Interior of a docked ship/boat near a large orange dome structure, with a character named Walter speaking a line of dialogue.
- **Later hits:** 05:44 a single frame took 4064 ms (typical 25 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 06:01 a single frame took 1577 ms (typical 26 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [003-opening-PROBLEM-frame-spike.jpg](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "opening"](shots-iphone/003-opening-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase opening starts
  1. opening stage -1 -> 0 (WalterForty-one trips on this line, son, and the coffee has never once improved.)

### 6. Frame-time spike during "panels"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** opening the Settings / Account / World / Controls panels, first at 08:40 into the run, on iPhone (WebKit) and desktop (Chromium)
- **What happened:** a single frame took 2051 ms (typical 28 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Gameplay HUD showing location/status info (Earth, Skyward Launch Complex, hauling cart weight, next objective) with a Settings panel open on top offering sign-in, account creation, and 'start fresh' options.
- **Screenshot:** [051-panels-PROBLEM-frame-spike.jpg](shots-iphone/051-panels-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "panels"](shots-iphone/051-panels-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (mid-ride)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. opening finished
  1. === phase panels starts
  1. tap #btn-settings (open Settings)
  1. tap #set-view (settings switch #set-view)
  1. tap #set-tool (settings switch #set-tool)

### 7. Frame-time spike during "lifeboat"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** earning the first ship: buy the two lifeboat parts and fit them, first at 12:34 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 5025 ms (typical 26 ms); 4 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** First-person view on a runway near the launch complex, with translucent orange and yellow circular markers on the ground and palm trees lining the runway in the background.
- **Later hits:** 14:04 a single frame took 1075 ms (typical 31 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [077-lifeboat-PROBLEM-frame-spike.jpg](shots-iphone/077-lifeboat-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "lifeboat"](shots-iphone/077-lifeboat-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. refresh check: moved 0.0 m, marks 10000 -> 10000, aboard false -> false
  1. === phase lifeboat starts
  1. lifeboat on earth is drained, missing cell + coupler; HUD says: NEXT The lifeboat has no power. Buy a power cell from Okafor, the flight line crew chief (Skyward), the Skyward Launch Complex and a fuel coupler from Pruitt, t
  1. QA pass: lifeboat: the NEXT line on screen names who sells each part - NEXT The lifeboat has no power. Buy a power cell from Okafor, the flight line crew chief (Skyward), the Skyward Launch Complex and a fuel coupler from Pruitt, t
  1. go talk to Okafor
  1. walk to Okafor
  1. outpost route of 35 legs around 30 solid things

### 8. Frame-time spike during "network"

- **How bad:** Annoying (score 62), happened 2 times
- **Where:** network cut, refresh offline, slow connection, first at 02:40 into the run, on desktop (Chromium)
- **What happened:** a single frame took 5483 ms (typical 4 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 02:48 a single frame took 3091 ms (typical 33 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [039-network-PROBLEM-frame-spike.jpg](shots-desktop/039-network-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "network"](shots-desktop/039-network-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap button "Close" (close account-panel)
  1. QA pass: network: while offline the game keeps drawing and does not crash
  1. QA info: network: the game tells the player the connection is gone (within about 12 s) - connected flag true -> true; messages: 
  1. NETWORK BACK
  1. QA pass: network: after the network returns the game reconnects and answers again - 2 s
  1. QA pass: network: money and place unchanged by a network blip
  1. REFRESH (refresh after being offline)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 9. Frame-time spike during "tour"

- **How bad:** Annoying (score 62)
- **Where:** walking the port (or the settlement of the start world) and talking to people, first at 12:20 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 4550 ms (typical 15 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** First-person view on Earth at the Skyward Launch Complex: a grassy field with palm trees leading to a large hangar building, with a HUD info panel top-left and World/crew and Controls buttons bottom-left.
- **Screenshot:** [075-tour-PROBLEM-frame-spike.jpg](shots-iphone/075-tour-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "tour"](shots-iphone/075-tour-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. outpost route of 20 legs around 30 solid things
  1. tap #crew-talk (Talk to Marisol Quintero)
  1. tap button "What does dispatch do?" (ask them something)
  1. tap button "Work and a crew. Understood." (answer back)
  1. tap button "✕" (close talk panel)
  1. REFRESH (refresh after the port tour)
  1. websocket closed (the bot refreshed the page)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 10. Frame-time spike during "smoke"

- **How bad:** Annoying (score 62)
- **Where:** smoke check (load time, download size, warm reload), first at 00:49 into the run, on desktop (Chromium)
- **What happened:** a single frame took 5316 ms (typical 4 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Same Mars landing-pad HUD scene as image 1, with an added toast reading 'Systems nominal. Ship down and stable.' floating over the ship's engine nozzles. Flagged: No visible frame-rate artifact, tearing, or stutter is evident in this single still frame despite the label 'frame-spike' — only the status toast is visibly different from image 1; Same low-contrast small gray text in the top info panel as image 1
- **Screenshot:** [015-smoke-PROBLEM-frame-spike.jpg](shots-desktop/015-smoke-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "smoke"](shots-desktop/015-smoke-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #multiplayer-panel button[aria-label*=lose] (close World / crew)
  1. tap #btn-key-controls (open Controls)
  1. tap #btn-key-controls (toggle closed Controls)
  1. === phase smoke starts
  1. QA info: smoke: page transfer on a cold load - 250 requests, 1.3 MB over the wire (slowest: w.heartbeatobservatory.com/games/the-cosmos/src/ship/guns.js 196 ms)
  1. QA pass: smoke: time from opening the link to the first drawn frames - 15.8 s (headless software rendering, a real phone is usually quicker to draw but slower to download)
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 11. Frame-time spike during "a11y"

- **How bad:** Annoying (score 62)
- **Where:** accessibility and readability scan, first at 00:58 into the run, on desktop (Chromium)
- **What happened:** a single frame took 3041 ms (typical 42 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **What the vision model saw:** Desktop: standing on a Mars landing pad near a parked rocket/ship with a ramp down, with a status HUD panel (location, cargo, objective text) top-left, a Settings button top-right, and three control buttons (Hold B to talk, World/crew, Controls) bottom-left.
- **Screenshot:** [023-a11y-PROBLEM-frame-spike.jpg](shots-desktop/023-a11y-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "a11y"](shots-desktop/023-a11y-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 7 small: span.dim 10px "Martian regolith · 3.72 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; #voice-talk-
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.
  1. QA pass: a11y: tap targets at least 44 px (Apple guideline) - 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44
  1. QA FAIL: a11y: pinch-zoom is not locked off - width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
  1. QA pass: a11y: a volume or mute control exists
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"","hint":"","caption":"","hud":"Mars · Valles Marineris 13°59'56.9\"S 59°11'47.9\"W +2213.1 m Martian regolith · 3.72 m/s² Hauling cart: 0.0 / 1054 k

### 12. Frame-time spike during "freeplay"

- **How bad:** Annoying (score 62)
- **Where:** free play (random walking, tapping, refreshing), first at 05:06 into the run, on desktop (Chromium)
- **What happened:** a single frame took 5716 ms (typical 4 ms); 2 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [048-freeplay-PROBLEM-frame-spike.jpg](shots-desktop/048-freeplay-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "freeplay"](shots-desktop/048-freeplay-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. jump
  1. jump
  1. QA pass: edges: walked and jumped into walls in 8 directions, never fell through - furthest 39 m from where it started
  1. QA pass: edges: still drawing afterwards
  1. === phase freeplay starts
  1. REFRESH (random refresh while playing)
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 13. When the graphics context is lost (iPhones do this after the app was in the background) the game restarts itself in reduced-graphics "safe mode"

- **How bad:** Minor (score 52)
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:47 into the run, on desktop (Chromium)
- **What happened:** by design (src/core/graphicsHealth.js). The page address gets ?tier=safe and it stays that way for the session, with a red graphics banner: "Graphics problem: WebGL context lost - safe mode active". A player who just switched apps and came back is left on worse graphics.
- **Screenshot:** [032-lifecycle-PROBLEM-context-lost-safe-mode.jpg](shots-desktop/032-lifecycle-PROBLEM-context-lost-safe-mode.jpg)

  ![When the graphics context is lost (iPhon](shots-desktop/032-lifecycle-PROBLEM-context-lost-safe-mode.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. QA pass: spam: 25 jumps and wild looks, game keeps drawing
  1. spam: 0 requests sent, purse 10000 -> 10000
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA info: lifecycle: graphics context lost, game reloads itself into safe mode and still plays - the game restarted with ?tier=safe (reduced graphics). Banner: "Graphics problem: WebGL context lost - safe mode active"

### 14. Looks wrong in the screenshot: 'fetch failed' error text displayed on screen

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:42 into the run, on iPhone (WebKit)
- **What happened:** center of screen, above the Carry button (the vision model's description of the screen: A crate sits on a hauling cart/trailer in a grassy field, with a 'fetch failed' message and a Carry button showing a spinning/loading icon.)
- **Screenshot:** [036-opening-PROBLEM-refusal-message.jpg](shots-iphone/036-opening-PROBLEM-refusal-message.jpg)

  ![Looks wrong in the screenshot: 'fetch fa](shots-iphone/036-opening-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)

### 15. Looks wrong in the screenshot: Visible error text "fetch failed" floating mid-screen with no context

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 06:45 into the run, on iPhone (WebKit)
- **What happened:** center of screen (the vision model's description of the screen: A blurred, dim view of grass/dirt terrain during the opening sequence, with a Walk/Look/Use hint top-left, a Skip intro button top-right, and a Carry (E) button bottom-right.)
- **Screenshot:** [037-opening-opening.jpg](shots-iphone/037-opening-opening.jpg)

  ![Looks wrong in the screenshot: Visible e](shots-iphone/037-opening-opening.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #opening-action (opening action)

### 16. Looks wrong in the screenshot: Fully black screen with zero text or loading indicator, unlike the game's other deliberate blackout frames whi

- **How bad:** Minor (score 49)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 08:35 into the run, on iPhone (WebKit)
- **What happened:** entire screen (the vision model's description of the screen: Completely black frame with no visible text, caption, or UI of any kind.)
- **Screenshot:** [046-opening-PROBLEM-console-warning.jpg](shots-iphone/046-opening-PROBLEM-console-warning.jpg)

  ![Looks wrong in the screenshot: Fully bla](shots-iphone/046-opening-PROBLEM-console-warning.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. opening finished

### 17. Looks wrong in the screenshot: Controls panel did not close after the 'toggle closed Controls' tap — this frame is pixel-identical to the pri

- **How bad:** Minor (score 49)
- **Where:** opening the Settings / Account / World / Controls panels, first at 00:38 into the run, on desktop (Chromium)
- **What happened:** Controls panel, left side of screen (the vision model's description of the screen: Identical Mars pad scene with the Controls panel still fully open, taken right after the bot tapped the Controls button to toggle it closed.)
- **Screenshot:** [011-panels-PROBLEM-overlap.jpg](shots-desktop/011-panels-PROBLEM-overlap.jpg)

  ![Looks wrong in the screenshot: Controls ](shots-desktop/011-panels-PROBLEM-overlap.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. tap #btn-key-controls (toggle closed Controls)

### 18. Looks wrong in the screenshot: Body text in the info panel (coordinates, regolith/hauling stats, tool name, and the multi-line NEXT objective

- **How bad:** Minor (score 49)
- **Where:** accessibility and readability scan, first at 00:57 into the run, on desktop (Chromium)
- **What happened:** top-left info panel (the vision model's description of the screen: Identical Mars landing-pad HUD scene, flagged for small text during an accessibility pass.)
- **Screenshot:** [018-a11y-PROBLEM-a11y-small-text.jpg](shots-desktop/018-a11y-PROBLEM-a11y-small-text.jpg)

  ![Looks wrong in the screenshot: Body text](shots-desktop/018-a11y-PROBLEM-a11y-small-text.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"","hint":"","caption":"","hud":"Mars · Valles Marineris 13°59'56.9\"S 59°11'47.9\"W +2213.1 m Martian regolith · 3.72 m/s² Hauling cart: 0.0 / 1054 k

### 19. Looks wrong in the screenshot: Gray secondary text ('Martian regolith · 3.72 m/s²', 'Hauling cart: 0.0 / 1054 kg', 'tool: Shovel') is low-con

- **How bad:** Minor (score 49)
- **Where:** accessibility and readability scan, first at 00:57 into the run, on desktop (Chromium)
- **What happened:** top-left info panel, lines below the orange location heading (the vision model's description of the screen: Identical Mars landing-pad HUD scene, flagged for contrast during an accessibility pass.)
- **Screenshot:** [019-a11y-PROBLEM-a11y-contrast.jpg](shots-desktop/019-a11y-PROBLEM-a11y-contrast.jpg)

  ![Looks wrong in the screenshot: Gray seco](shots-desktop/019-a11y-PROBLEM-a11y-contrast.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: readability: something on screen tells a player what to do next - {"action":"","hint":"","caption":"","hud":"Mars · Valles Marineris 13°59'56.9\"S 59°11'47.9\"W +2213.1 m Martian regolith · 3.72 m/s² Hauling cart: 0.0 / 1054 k

### 20. Game said: "Welcome to Mars. Follow the amber lights to the big Arrivals sign. If "

- **How bad:** Minor (score 42)
- **Where:** the opening (crash, climb out, dig the crate, ride to the port), first at 03:38 into the run, on iPhone (WebKit)
- **What happened:** shown in opening-caption while the bot was: 03:36 [opening] walk to down the gangway
- **What the vision model saw:** Night exterior view of a Mars landing port with an illuminated 'ARRIVALS' sign in the distance and a Steward's dialogue line at the bottom.
- **Screenshot:** [017-opening-PROBLEM-refusal-message.jpg](shots-iphone/017-opening-PROBLEM-refusal-message.jpg)

  ![Game said: "Welcome to Mars. Follow the ](shots-iphone/017-opening-PROBLEM-refusal-message.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. walk to the boarding hall
  1. in the boarding hall, waiting for the gangway to come down
  1. walk to down the gangway
  1. walk to down the gangway
  1. walk to down the gangway

### 21. Frame-time spike during "lifecycle"

- **How bad:** Minor (score 38), happened 3 times
- **Where:** app to the background, graphics context lost, phone rotated, first at 01:44 into the run, on desktop (Chromium)
- **What happened:** a single frame took 2379 ms (typical 4 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Later hits:** 01:56 a single frame took 5487 ms (typical 4 ms); 3 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.) / 02:08 a single frame took 3275 ms (typical 29 ms); 1 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [030-lifecycle-PROBLEM-frame-spike.jpg](shots-desktop/030-lifecycle-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "lifecycle"](shots-desktop/030-lifecycle-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. jump
  1. jump
  1. QA pass: spam: 25 jumps and wild looks, game keeps drawing
  1. spam: 0 requests sent, purse 10000 -> 10000
  1. === phase lifecycle starts
  1. app sent to the background (hidden, blur, pagehide)
  1. QA pass: lifecycle: background 8 s and return keeps place, money and ship state
  1. websocket open wss://cosmos.heartbeatobservatory.com/

### 22. Low text contrast in 2 places

- **How bad:** Minor (score 38)
- **Where:** accessibility and readability scan, first at 00:57 into the run, on desktop (Chromium)
- **What happened:** span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
- **What the vision model saw:** Identical Mars landing-pad HUD scene, flagged for contrast during an accessibility pass. Flagged: Gray secondary text ('Martian regolith · 3.72 m/s²', 'Hauling cart: 0.0 / 1054 kg', 'tool: Shovel') is low-contrast against the dark brown translucent panel background
- **Screenshot:** [019-a11y-PROBLEM-a11y-contrast.jpg](shots-desktop/019-a11y-PROBLEM-a11y-contrast.jpg)

  ![Low text contrast in 2 places](shots-desktop/019-a11y-PROBLEM-a11y-contrast.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 11.1 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 7 small: span.dim 10px "Martian regolith · 3.72 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; #voice-talk-
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"

### 23. Text smaller than 11 px in 7 places (hard to read on a phone)

- **How bad:** Minor (score 36)
- **Where:** accessibility and readability scan, first at 00:57 into the run, on desktop (Chromium)
- **What happened:** span.dim 10px "Martian regolith · 3.72 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; #voice-talk-sub 10px "no one near" ; span.hint 10px "Third person to inspect "
- **What the vision model saw:** Identical Mars landing-pad HUD scene, flagged for small text during an accessibility pass. Flagged: Body text in the info panel (coordinates, regolith/hauling stats, tool name, and the multi-line NEXT objective text) is rendered quite small relative to the panel and screen, hard to read at a glance
- **Screenshot:** [018-a11y-PROBLEM-a11y-small-text.jpg](shots-desktop/018-a11y-PROBLEM-a11y-small-text.jpg)

  ![Text smaller than 11 px in 7 places (har](shots-desktop/018-a11y-PROBLEM-a11y-small-text.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: smoke: time from opening the link to the first drawn frames - 15.8 s (headless software rendering, a real phone is usually quicker to draw but slower to download)
  1. REFRESH (smoke: warm reload (cache filled))
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 11.1 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 7 small: span.dim 10px "Martian regolith · 3.72 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; #voice-talk-

### 24. 1 buttons have no text or label (a screen reader says nothing)

- **How bad:** Small (score 34)
- **Where:** accessibility and readability scan, first at 00:57 into the run, on desktop (Chromium)
- **What happened:** input.
- **What the vision model saw:** Identical Mars landing-pad HUD scene, flagged for an unnamed/unlabeled element during an accessibility pass. Flagged: No visibly broken or unlabeled UI element can be confirmed from the image alone (an accessible-name gap is a DOM/aria issue, not something visible in a screenshot); all three bottom-left buttons and the Settings button show visible text labels
- **Screenshot:** [020-a11y-PROBLEM-a11y-noname.jpg](shots-desktop/020-a11y-PROBLEM-a11y-noname.jpg)

  ![1 buttons have no text or label (a scree](shots-desktop/020-a11y-PROBLEM-a11y-noname.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. QA pass: smoke: warm reload comes back - 11.1 s
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 7 small: span.dim 10px "Martian regolith · 3.72 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; #voice-talk-
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.

### 25. graphics shapes (geometries) grew from 349 to 650 over the run (new areas loading, or a leak)

- **How bad:** Small (score 30)
- **Where:** earning the first ship: buy the two lifeboat parts and fit them, first at 15:30 into the run, on iPhone (WebKit)
- **What happened:** samples 46; phases opening -> lifeboat. Only a leak if it keeps climbing while standing still: the idle check measures that.

- **Steps to reproduce (what the bot did just before):**
  1. tap button "Buy the fuel coupler · 300 marksFor your" (buy the coupler)
  1. QA pass: lifeboat: buy the coupler from Pruitt - purse 9700 -> 9400
  1. tap button "✕" (close talk panel)
  1. walk to the lifeboat (to fit the parts)
  1. outpost route of 94 legs around 30 solid things
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)
  1. QA pass: lifeboat: fit both parts, the boat is no longer drained - HUD: NEXT No more jobs here for now. Dig, haul and sell what the ground gives, or fly to another world (Course). The people here will have more w

### 26. textures grew from 122 to 342 over the run (new areas loading, or a leak)

- **How bad:** Small (score 30)
- **Where:** earning the first ship: buy the two lifeboat parts and fit them, first at 15:30 into the run, on iPhone (WebKit)
- **What happened:** samples 46; phases opening -> lifeboat. Only a leak if it keeps climbing while standing still: the idle check measures that.

- **Steps to reproduce (what the bot did just before):**
  1. tap button "Buy the fuel coupler · 300 marksFor your" (buy the coupler)
  1. QA pass: lifeboat: buy the coupler from Pruitt - purse 9700 -> 9400
  1. tap button "✕" (close talk panel)
  1. walk to the lifeboat (to fit the parts)
  1. outpost route of 94 legs around 30 solid things
  1. mis-tap beside #btn-action
  1. tap #btn-action (action)
  1. QA pass: lifeboat: fit both parts, the boat is no longer drained - HUD: NEXT No more jobs here for now. Dig, haul and sell what the ground gives, or fly to another world (Course). The people here will have more w

### 27. Zooming the page is switched off in the viewport tag

- **How bad:** Small (score 30)
- **Where:** accessibility and readability scan, first at 00:57 into the run, on desktop (Chromium)
- **What happened:** width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover
- **What the vision model saw:** Identical Mars landing-pad HUD scene, flagged for locked pinch-zoom during an accessibility pass. Flagged: No visual indicator of zoom state is present in the screenshot itself; this is a behavioral (input-handling) issue not confirmable from a static image
- **Screenshot:** [021-a11y-PROBLEM-a11y-zoom-locked.jpg](shots-desktop/021-a11y-PROBLEM-a11y-zoom-locked.jpg)

  ![Zooming the page is switched off in the ](shots-desktop/021-a11y-PROBLEM-a11y-zoom-locked.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. === phase a11y starts
  1. tap #btn-settings (open Settings for the accessibility scan)
  1. tap #btn-close-settings (close settings)
  1. QA FAIL: a11y: text is at least 11 px - 7 small: span.dim 10px "Martian regolith · 3.72 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; #voice-talk-
  1. QA FAIL: a11y: text contrast (4.5:1, or 3:1 for big text) - 2 low: span.hint 3.9:1 (needs 4.5) "Third person to inspect " ; span.hint 3.9:1 (needs 4.5) "Spade for detail, shovel"
  1. QA FAIL: a11y: every button has a name - input.
  1. QA pass: a11y: tap targets at least 44 px (Apple guideline) - 2 smaller: #btn-settings 76x40 ; #btn-close-settings 37x44
  1. QA FAIL: a11y: pinch-zoom is not locked off - width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover

### 28. Network cut for about 12 s and the game said nothing and still thinks it is connected

- **How bad:** Small (score 28)
- **Where:** network cut, refresh offline, slow connection, first at 02:27 into the run, on desktop (Chromium)
- **What happened:** connected=true. A hint only: the bot's offline switch may not cut a socket that is already open, so a real phone going into a tunnel could behave differently.
- **Screenshot:** [038-network-PROBLEM-offline-silent.jpg](shots-desktop/038-network-PROBLEM-offline-silent.jpg)

  ![Network cut for about 12 s and the game ](shots-desktop/038-network-PROBLEM-offline-silent.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. QA pass: lifecycle: rotate to 900x560 with Settings open, the 3D view fills the screen - {"cw":900,"ch":560,"iw":900,"ih":560}
  1. tap #btn-close-settings (close settings)
  1. === phase network starts
  1. NETWORK CUT
  1. tap #purse (tap while offline)
  1. tap button "Close" (close account-panel)
  1. QA pass: network: while offline the game keeps drawing and does not crash
  1. QA info: network: the game tells the player the connection is gone (within about 12 s) - connected flag true -> true; messages: 

### Console warnings (4 kinds)

- THREE.WebGLRenderer: Texture has been resized from (256x192) to (256x128). (x16)
- THREE.Material: parameter 'map' has value of undefined. (x6)
- THREE.BufferGeometry.toNonIndexed(): BufferGeometry is already non-indexed. (x2)
- THREE.WebGLRenderer: WebGL 1 support was deprecated in r153 and will be removed in r163. (x1)

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| the opening (crash, climb out, dig the crate, ride to the port) | done - done | 503 s |
| opening the Settings / Account / World / Controls panels | done | 10 s |
| walking the port (or the settlement of the start world) and talking to people | done - settlement Earth: 3 of 3 talked to | 200 s |
| earning the first ship: buy the two lifeboat parts and fit them | done - lifeboat repaired | 180 s |
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

People talked to: 3 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

### Desktop (Chromium, keyboard + mouse)

| Step | Result | Time |
|---|---|---|
| opening the Settings / Account / World / Controls panels | done | 19 s |
| smoke check (load time, download size, warm reload) | done | 12 s |
| accessibility and readability scan | done | 8 s |
| spamming buttons and jumps | done | 26 s |
| app to the background, graphics context lost, phone rotated | done | 46 s |
| network cut, refresh offline, slow connection | done | 38 s |
| turning on the spot, reading draw calls and frame times | done | 10 s |
| random tapping everywhere | done | 33 s |
| walking and jumping into walls and edges in 8 directions | done | 84 s |
| walking the port (or the settlement of the start world) and talking to people | skipped (out of time) | 0 s |
| earning the first ship: buy the two lifeboat parts and fit them | skipped (out of time) | 0 s |
| buy/sell loops and double taps on the shop | skipped (out of time) | 0 s |
| hiring crew from the crew hall | skipped (out of time) | 0 s |
| digging regolith and delivering it to the weigh bay | skipped (out of time) | 0 s |
| leaving the game alone for 90 s | skipped (out of time) | 0 s |
| end-of-run soft-lock check | skipped (out of time) | 0 s |
| free play (random walking, tapping, refreshing) | done | 13 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: Settings, Account, World / crew, Controls. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- desktop / panels: typical 4 ms, slowest 7991 ms, 8 frames over 250 ms
- iphone / opening: typical 16 ms, slowest 7584 ms, 3 frames over 250 ms
- desktop / freeplay: typical 4 ms, slowest 5716 ms, 2 frames over 250 ms
- desktop / lifecycle: typical 4 ms, slowest 5487 ms, 3 frames over 250 ms
- desktop / network: typical 4 ms, slowest 5483 ms, 3 frames over 250 ms

Button response time (tap to something changing on screen): median 143 ms, slowest 1386 ms over 13 taps.

## QA checks (the things real testers do besides playing through)

See `tools/playtester/PRACTICES.md` for why each one exists. FAIL rows are also listed as problems above where they are real bugs.

### iPhone 15 (WebKit, touch): 4 passed, 0 failed, 0 skipped, 0 info

| Check | Result | Notes |
|---|---|---|
| lifeboat: the NEXT line on screen names who sells each part | pass | NEXT The lifeboat has no power. Buy a power cell from Okafor, the flight line crew chief (Skyward), the Skyward Launch Complex and a fuel coupler from Pruitt, the Homeguard organiser, the Skyward Laun |
| lifeboat: buy the cell from Okafor | pass | purse 10000 -> 9700 |
| lifeboat: buy the coupler from Pruitt | pass | purse 9700 -> 9400 |
| lifeboat: fit both parts, the boat is no longer drained | pass | HUD: NEXT No more jobs here for now. Dig, haul and sell what the ground gives, or fly to another world (Course). The people here will have more w |

### Desktop (Chromium, keyboard + mouse): 18 passed, 5 failed, 1 skipped, 3 info

| Check | Result | Notes |
|---|---|---|
| smoke: page transfer on a cold load | info | 250 requests, 1.3 MB over the wire (slowest: w.heartbeatobservatory.com/games/the-cosmos/src/ship/guns.js 196 ms) |
| smoke: time from opening the link to the first drawn frames | pass | 15.8 s (headless software rendering, a real phone is usually quicker to draw but slower to download) |
| smoke: warm reload comes back | pass | 11.1 s |
| a11y: text is at least 11 px | FAIL | 7 small: span.dim 10px "Martian regolith · 3.72 " ; span.dim 10px "tool: Shovel" ; div.next-goal 10px "Lifeboat ready. Next: hi" ; b. 10px "NEXT" ; #voice-talk-sub 10px "no one near" ; span.hint 10px "Third person to ins |
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
| lifecycle: graphics context lost, game reloads itself into safe mode and still plays | info | the game restarted with ?tier=safe (reduced graphics). Banner: "Graphics problem: WebGL context lost - safe mode active" |
| lifecycle: rotate to 900x560, the 3D view fills the screen | pass | {"cw":900,"ch":560,"iw":900,"ih":560} |
| lifecycle: rotate to 900x560 with Settings open, the 3D view fills the screen | pass | {"cw":900,"ch":560,"iw":900,"ih":560} |
| network: while offline the game keeps drawing and does not crash | pass |  |
| network: the game tells the player the connection is gone (within about 12 s) | info | connected flag true -> true; messages:  |
| network: after the network returns the game reconnects and answers again | pass | 2 s |
| network: money and place unchanged by a network blip | pass |  |
| network: refresh while offline, then online again, the game comes back | pass |  |
| network: slow connection (900 ms, 60 KB/s) for a panel tap | pass | 6 s |
| perf: turning on the spot, 95 percent of frames under 34 ms | FAIL | median 29 ms, 95th 50 ms, slowest 646 ms; peak 130 draw calls, 37k triangles (headless software rendering, judge relatively) |
| monkey: 35 random button taps and wild gestures, no crash | pass |  |
| edges: walked and jumped into walls in 8 directions, never fell through | pass | furthest 39 m from where it started |
| edges: still drawing afterwards | pass |  |

## Load, size and memory

- **iPhone 15 (WebKit, touch)**: load to first frames 13.7 s; cold-load download 1.3 MB in 250 requests; warm reload not measured; busiest view not measured. Over the run (49 samples): graphics geometries 332 -> 650, textures 122 -> 342, page elements 236 -> 239 (JS heap is only readable in Chromium).
- **Desktop (Chromium, keyboard + mouse)**: load to first frames 15.8 s; cold-load download 1.3 MB in 250 requests; warm reload 11.1 s; busiest view 130 draw calls, 37k triangles. Over the run (35 samples): graphics geometries 363 -> 291, textures 206 -> 165, page elements 276 -> 219, JS heap 270 -> 238 MB.

## Vision pass

A vision model (claude CLI (sonnet)) looked at 36 screenshots for about $0.00 (cap $1).

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.
- Not possible from here (needs a real iPhone or two players): a real phone call or notification banner, lock screen, battery and heat, low-end phone speed, many device models, race-condition duplication between two players. The full list of what real QA does and which parts the bot covers is in tools/playtester/PRACTICES.md.
