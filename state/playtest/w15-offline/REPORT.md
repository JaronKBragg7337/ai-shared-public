# World 2 playtest report

Run: 2026-11-06 20:30 Fort Wayne time
Site: http://127.0.0.1:18765/world2/
Build: 2026-11-05-route

**Offline substitution:** requests for Three.js 0.182.0 were served from local Three.js 0.185.1 at C:/Users/lilli/.codex/runtime/unfinished-island/node_modules/three. This is an approximation, not a test of the exact live dependency.

The page was opened with `dev=1` only to read player coordinates. The phone run uses 393 × 852 WebKit. A real Playwright tap tests the ground; the held thumb is a synthetic pointer gesture. Desktop movement uses keyboard input.

## Checks

### iPhone 15 (WebKit, touch)

| Check | Result | Evidence |
|---|---|---|
| World loads | pass | First frames in 2.5 seconds. |
| Enter the world | pass | The opening card closed. |
| Ground tap does not walk | pass | Game handler returned no object at 189,699; real tap moved from -35.50, 6.50 to -35.50, 6.50 (0.000 units). |
| Stick appears at thumb 1 | pass | Expected translate(71px, 613px); observed {"on":true,"transform":"translate(71px, 613px)"}. |
| Walking moves the player 1 | pass | Position -35.50, 6.50 to -23.22, 4.24; moved 12.49 world units. A nearby obstacle may block this direction. |
| Stick appears at thumb 2 | pass | Expected translate(134px, 613px); observed {"on":true,"transform":"translate(134px, 613px)"}. |
| Walking moves the player 2 | pass | Position -23.22, 4.24 to -13.81, 1.42; moved 9.83 world units. A nearby obstacle may block this direction. |
| Stick disappears on release | pass | Stick is hidden and inactive. |
| Map opens | pass | Map opened. |
| Map closes | pass | Map closed. |
| Opening map does not walk | pass | Player moved 0.000 world units while opening and closing map. |

- load and enter: done (4 s)
- ground tap: done (5 s)
- walking: done (4 s)
- map: done (1 s)
- exploration: done — 6 short walking gestures; position -13.81, 1.42 to 8.80, -20.73. This is a limited exploratory pass, not a full tour. (11 s)

### Desktop (Chromium, keyboard + mouse)

| Check | Result | Evidence |
|---|---|---|
| World loads | pass | First frames in 2.3 seconds. |
| Enter the world | pass | The opening card closed. |
| Ground tap does not walk | pass | Game handler returned no object at 614,656; real tap moved from -35.50, 6.50 to -35.50, 6.50 (0.000 units). |
| Walking moves the player 1 | pass | Position -35.50, 6.50 to -27.39, 5.12; moved 8.23 world units. A nearby obstacle may block this direction. |
| Map opens | pass | Map opened. |
| Map closes | pass | Map closed. |
| Opening map does not walk | pass | Player moved 0.000 world units while opening and closing map. |

- load and enter: done (5 s)
- ground tap: done (5 s)
- walking: done (2 s)
- map: done (1 s)
- exploration: done — 6 short walking gestures; position -27.39, 5.12 to -18.19, 2.30. This is a limited exploratory pass, not a full tour. (11 s)

## Findings and observations

A failed external request can reflect the local network rather than a game defect. Confirm each observation on the intended connection before treating it as a live bug.

### Console error

- Device: iphone; phase: load and enter; score: 55
- Failed to load resource: the server responded with a status of 404 (File not found)
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
- [Screenshot](shots-iphone/002-load-and-enter-PROBLEM-console-error.jpg)

### Console error

- Device: iphone; phase: load and enter; score: 55
- Failed to load resource: Could not connect to server
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
- [Screenshot](shots-iphone/007-load-and-enter-PROBLEM-console-error.jpg)

### Console error

- Device: desktop; phase: load and enter; score: 55
- Failed to load resource: the server responded with a status of 404 (File not found)
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
- [Screenshot](shots-desktop/002-load-and-enter-PROBLEM-console-error.jpg)

### Console error

- Device: desktop; phase: exploration; score: 55
- Failed to load resource: net::ERR_NETWORK_ACCESS_DENIED
- Steps:
  1. === map
  1. tap #minimap (open city map)
  1. QA pass: Map opens - Map opened.
  1. tap #hbpm .close-btn (close map)
  1. QA pass: Map closes - Map closed.
  1. QA pass: Opening map does not walk - Player moved 0.000 world units while opening and closing map.
  1. === exploration
  1. explore: hold KeyW
- [Screenshot](shots-desktop/012-exploration-PROBLEM-console-error.jpg)

### Request returned HTTP 404

- Device: iphone; phase: load and enter; score: 50
- http://127.0.0.1:18765/_vercel/insights/script.js
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
- [Screenshot](shots-iphone/001-load-and-enter-PROBLEM-http.jpg)

### Request returned HTTP 404

- Device: desktop; phase: load and enter; score: 50
- http://127.0.0.1:18765/_vercel/insights/script.js
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
- [Screenshot](shots-desktop/001-load-and-enter-PROBLEM-http.jpg)

### A request failed to load

- Device: iphone; phase: load and enter; score: 45
- http://127.0.0.1:18765/_vercel/insights/script.js (Load request cancelled)
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
- [Screenshot](shots-iphone/003-load-and-enter-PROBLEM-request-failed.jpg)

### A request failed to load

- Device: iphone; phase: load and enter; score: 45
- https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm (Could not connect to server)
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
- [Screenshot](shots-iphone/006-load-and-enter-PROBLEM-request-failed.jpg)

### A request failed to load

- Device: desktop; phase: exploration; score: 45
- https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm (net::ERR_NETWORK_ACCESS_DENIED)
- Steps:
  1. === map
  1. tap #minimap (open city map)
  1. QA pass: Map opens - Map opened.
  1. tap #hbpm .close-btn (close map)
  1. QA pass: Map closes - Map closed.
  1. QA pass: Opening map does not walk - Player moved 0.000 world units while opening and closing map.
  1. === exploration
  1. explore: hold KeyW
- [Screenshot](shots-desktop/011-exploration-PROBLEM-request-failed.jpg)

### Button too small for a thumb: #soundBtn "🔊 Sound" 72x25

- Device: iphone; phase: exploration; score: 30
- #soundBtn "🔊 Sound" 72x25 (World 2 exploration, iphone)
- Steps:
  1. QA pass: Opening map does not walk - Player moved 0.000 world units while opening and closing map.
  1. === exploration
  1. explore: stick direction forward
  1. explore: stick direction left
  1. explore: stick direction forward
  1. explore: stick direction left
  1. explore: stick direction forward
  1. explore: stick direction left
- [Screenshot](shots-iphone/014-exploration-PROBLEM-tiny-button.jpg)

### Console warning

- Device: iphone; phase: load and enter; score: 20
- THREE.Clock: This module has been deprecated. Please use THREE.Timer instead.
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
- [Screenshot](shots-iphone/004-load-and-enter-PROBLEM-console-warning.jpg)

### Console warning

- Device: iphone; phase: load and enter; score: 20
- THREE.WebGLShadowMap: PCFSoftShadowMap has been deprecated. Using PCFShadowMap instead.
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
- [Screenshot](shots-iphone/005-load-and-enter-PROBLEM-console-warning.jpg)

### Console warning

- Device: iphone; phase: load and enter; score: 20
- THREE.WebGLProgram: Program Info Log: (210,81-129): warning X4122: sum of 0.996094 and -2.98545e-017 cannot be represented accurately in double precision
(209,37-61): warning X4122: sum of 1 and -1.49272e-017 cannot be represented accurately in double precision
(210,82-106): warning X4122: sum of 1 
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
  1. QA pass: World loads - First frames in 2.5 seconds.
  1. tap #enterButton (enter World 2)
- [Screenshot](shots-iphone/008-load-and-enter-PROBLEM-console-warning.jpg)

### Console warning

- Device: desktop; phase: load and enter; score: 20
- THREE.Clock: This module has been deprecated. Please use THREE.Timer instead.
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
- [Screenshot](shots-desktop/003-load-and-enter-PROBLEM-console-warning.jpg)

### Console warning

- Device: desktop; phase: load and enter; score: 20
- THREE.WebGLShadowMap: PCFSoftShadowMap has been deprecated. Using PCFShadowMap instead.
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
- [Screenshot](shots-desktop/004-load-and-enter-PROBLEM-console-warning.jpg)

### Console warning

- Device: desktop; phase: load and enter; score: 20
- THREE.WebGLProgram: Program Info Log: (210,81-129): warning X4122: sum of 0.996094 and -2.98545e-017 cannot be represented accurately in double precision
(209,37-61): warning X4122: sum of 1 and -1.49272e-017 cannot be represented accurately in double precision
(210,82-106): warning X4122: sum of 1 
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
  1. QA pass: World loads - First frames in 2.3 seconds.
  1. tap #enterButton (enter World 2)
- [Screenshot](shots-desktop/005-load-and-enter-PROBLEM-console-warning.jpg)

## Limits

- This is a short scripted walk and map check, not a complete city, door, multiplayer, visual, or accessibility review.
- Synthetic pointer gestures and Windows WebKit do not reproduce real iPhone touch, Safari, GPU, heat or battery behavior.
- The ground candidate is checked with the game’s use handler before a real tap. A no-object result can also mean empty sky; an object hit is skipped.
- Network failures and local dependency substitutions are reported as observations; they do not establish what happens on the live site.

- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)
- Desktop (Chromium, keyboard + mouse): [session video](videos-desktop/<email>)