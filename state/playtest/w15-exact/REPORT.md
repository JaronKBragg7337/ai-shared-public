# World 2 playtest report

Run: 2026-11-06 20:30 Fort Wayne time
Site: http://127.0.0.1:18765/world2/
Build: unknown

The page was opened with `dev=1` only to read player coordinates. The phone run uses 393 × 852 WebKit. A real Playwright tap tests the ground; the held thumb is a synthetic pointer gesture. Desktop movement uses keyboard input.

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

## Findings and observations

A failed external request can reflect the local network rather than a game defect. Confirm each observation on the intended connection before treating it as a live bug.

### World 2 did not finish loading

- Device: iphone; phase: load and enter; score: 90
- World did not reach its first frames in 45 seconds. Loading text: Still fetching the engine - a slow connection can take a little longer…. External requests may be blocked in this environment.
- Steps:
  1. Open the reported URL and wait 45 seconds.
- [Screenshot](shots-iphone/006-load-and-enter-PROBLEM-boot.jpg)

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
- [Screenshot](shots-iphone/005-load-and-enter-PROBLEM-console-error.jpg)

### Request returned HTTP 404

- Device: iphone; phase: load and enter; score: 50
- http://127.0.0.1:18765/_vercel/insights/script.js
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
- [Screenshot](shots-iphone/001-load-and-enter-PROBLEM-http.jpg)

### A request failed to load

- Device: iphone; phase: load and enter; score: 45
- http://127.0.0.1:18765/_vercel/insights/script.js (Load request cancelled)
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
- [Screenshot](shots-iphone/003-load-and-enter-PROBLEM-request-failed.jpg)

### A request failed to load

- Device: iphone; phase: load and enter; score: 45
- https://cdn.jsdelivr.net/npm/three@0.182.0/build/three.module.js (Could not connect to server)
- Steps:
  1. === load and enter
  1. open http://127.0.0.1:18765/world2/?dev=1
- [Screenshot](shots-iphone/004-load-and-enter-PROBLEM-request-failed.jpg)

## Limits

- This is a short scripted walk and map check, not a complete city, door, multiplayer, visual, or accessibility review.
- Synthetic pointer gestures and Windows WebKit do not reproduce real iPhone touch, Safari, GPU, heat or battery behavior.
- The ground candidate is checked with the game’s use handler before a real tap. A no-object result can also mean empty sky; an object hit is skipped.
- Network failures and local dependency substitutions are reported as observations; they do not establish what happens on the live site.

- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)