# World 2 playtest report

Run: 2026-11-06 20:33 Fort Wayne time
Site: https://www.heartbeatobservatory.com/world2/
Build: 2026-11-05-route

The page was opened with `dev=1` only to read player coordinates and inspect the scene for ground. The phone run uses 393 × 852 WebKit. A real Playwright tap tests the ground; the held thumb is a synthetic pointer gesture. Desktop movement uses keyboard input. The requested minutes set the exploration budget, not a required duration: exploration stops at six gestures or when the budget runs out, while loading and fixed checks may exceed that budget.

## Checks

### iPhone 15 (WebKit, touch)

| Check | Result | Evidence |
|---|---|---|
| World loads | FAIL | World did not reach its first frames in 45 seconds. Loading text: Still fetching the engine - a slow connection can take a little longer…. External requests may be blocked in this environment. |
| Ground tap does not walk | skipped | World was not entered. |
| Walking moves the player | skipped | World was not entered. |
| Map opens | skipped | World was not entered. |
| Exploration | skipped | World was not entered. |

- load and enter: done — Boot did not complete; movement and map checks skipped. (46 s)

### Desktop (Chromium, keyboard + mouse)

| Check | Result | Evidence |
|---|---|---|
| World loads | pass | First frames in 2.4 seconds. |
| Enter the world | pass | The opening card closed. |
| Ground tap does not walk | pass | Raycast ground at -31.1,5.3; tap at 614,656 moved from -35.50, 6.50 to -35.50, 6.50 (0.000 units). |
| Walking direction 1 | pass | Position -35.50, 6.50 to -27.25, 5.09; moved 8.37 world units. A nearby obstacle may block this direction. |
| Walking direction 2 | pass | Position -27.25, 5.09 to -29.01, -3.13; moved 8.41 world units. A nearby obstacle may block this direction. |
| Walking moves the player | pass | At least one tested direction moved the player. |
| Map opens | pass | Map opened. |
| Map closes | pass | Map closed. |
| Opening map does not walk | pass | Player moved 0.000 world units while opening and closing map. |

- load and enter: done (6 s)
- ground tap: done (3 s)
- walking: done (4 s)
- map: done (1 s)
- exploration: done — 6 short walking gestures; position -29.01, -3.13 to -21.25, 0.52. This is a limited exploratory pass, not a full tour. (11 s)

## Game behavior observations

Confirm each observation with its reproduction steps before treating it as a live bug.

None recorded.

## Environment, requests and tool observations

Local hosting, blocked external dependencies, missing Vercel services, or the test harness can cause these. They do not by themselves establish a live game bug.

### World 2 did not finish loading

- Device: iphone; phase: load and enter; score: 90
- World did not reach its first frames in 45 seconds. Loading text: Still fetching the engine - a slow connection can take a little longer…. External requests may be blocked in this environment.
- Steps:
  1. Open the reported URL and wait 45 seconds.
- [Screenshot](shots-iphone/003-load-and-enter-PROBLEM-boot.jpg)

### Console error

- Device: iphone; phase: load and enter; score: 55
- Failed to load resource: SSL connect error
- Steps:
  1. === load and enter
  1. open https://www.heartbeatobservatory.com/world2/?dev=1
- [Screenshot](shots-iphone/002-load-and-enter-PROBLEM-console-error.jpg)

### A request failed to load

- Device: iphone; phase: load and enter; score: 45
- https://cdn.jsdelivr.net/npm/three@0.182.0/build/three.module.js (SSL connect error)
- Steps:
  1. === load and enter
  1. open https://www.heartbeatobservatory.com/world2/?dev=1
- [Screenshot](shots-iphone/001-load-and-enter-PROBLEM-request-failed.jpg)

### Console warning

- Device: desktop; phase: load and enter; score: 20
- THREE.WebGLProgram: Program Info Log: (221,81-129): warning X4122: sum of 0.996094 and -2.98545e-017 cannot be represented accurately in double precision
(220,37-61): warning X4122: sum of 1 and -1.49272e-017 cannot be represented accurately in double precision
(221,82-106): warning X4122: sum of 1 
- Steps:
  1. === load and enter
  1. open https://www.heartbeatobservatory.com/world2/?dev=1
  1. QA pass: World loads - First frames in 2.4 seconds.
- [Screenshot](shots-desktop/001-load-and-enter-PROBLEM-console-warning.jpg)

## Limits

- This is a short scripted walk and map check, not a complete city, door, multiplayer, visual, or accessibility review.
- Synthetic pointer gestures and Windows WebKit do not reproduce real iPhone touch, Safari, GPU, heat or battery behavior.
- A read-only scene raycast seeks a horizontal surface away from doors and lots; the ground check is skipped if no safe target is found.
- Network failures and local dependency substitutions are reported as observations; they do not establish what happens on the live site.

- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)
- Desktop (Chromium, keyboard + mouse): [session video](videos-desktop/<email>)