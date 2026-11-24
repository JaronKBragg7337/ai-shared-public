# World 2 playtest report

Run: 2026-11-06 20:35 Fort Wayne time
Site: https://www.heartbeatobservatory.com/world2/
Build: 2026-11-05-route

**Offline substitution:** requests for Three.js 0.182.0 were served from local Three.js 0.182.0 at C:/Users/lilli/AppData/Local/Temp/claude/80c4e6a25ace175e/6cacb0b9-dd02-46b4-88e9-fcea9022ace0/scratchpad/t182/package. This is an approximation, not a test of the exact live dependency.

The page was opened with `dev=1` only to read player coordinates and inspect the scene for ground. The phone run uses 393 × 852 WebKit. A real Playwright tap tests the ground; the held thumb is a synthetic pointer gesture. Desktop movement uses keyboard input. The requested minutes set the exploration budget, not a required duration: exploration stops at six gestures or when the budget runs out, while loading and fixed checks may exceed that budget.

## Checks

### iPhone 15 (WebKit, touch)

| Check | Result | Evidence |
|---|---|---|
| World loads | pass | First frames in 2.0 seconds. |
| Enter the world | pass | The opening card closed. |
| Ground tap does not walk | pass | Raycast ground at -31.5,5.6; tap at 189,699 moved from -35.50, 6.50 to -35.50, 6.50 (0.000 units). |
| Stick appears at thumb 1 | pass | Expected translate(71px, 613px); observed {"on":true,"transform":"translate(71px, 613px)"}. |
| Walking direction 1 | pass | Position -35.50, 6.50 to -23.21, 4.22; moved 12.50 world units. A nearby obstacle may block this direction. |
| Stopped after release 1 | pass | After release and a 0.35 s settle, position changed 0.000 units over one second. |
| Stick appears at thumb 2 | pass | Expected translate(134px, 613px); observed {"on":true,"transform":"translate(134px, 613px)"}. |
| Walking direction 2 | pass | Position -23.21, 4.22 to -20.99, -3.05; moved 7.60 world units. A nearby obstacle may block this direction. |
| Stopped after release 2 | pass | After release and a 0.35 s settle, position changed 0.000 units over one second. |
| Walking moves the player | pass | At least one tested direction moved the player. |
| Stick disappears on release | pass | Stick is hidden and inactive. |
| Map opens | pass | Map opened. |
| Map closes | pass | Map closed. |
| Opening map does not walk | pass | Player moved 0.000 world units while opening and closing map. |

- load and enter: done (4 s)
- ground tap: done (3 s)
- walking: done (6 s)
- map: done (1 s)
- exploration: done — 6 short walking gestures; position -20.99, -3.05 to 2.79, -23.36. This is a limited exploratory pass, not a full tour. (11 s)

## Game behavior observations

Confirm each observation with its reproduction steps before treating it as a live bug.

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
- [Screenshot](shots-iphone/009-exploration-PROBLEM-tiny-button.jpg)

## Environment, requests and tool observations

Local hosting, blocked external dependencies, missing Vercel services, or the test harness can cause these. They do not by themselves establish a live game bug.

### Console error

- Device: iphone; phase: load and enter; score: 55
- Failed to load resource: SSL connect error
- Steps:
  1. === load and enter
  1. open https://www.heartbeatobservatory.com/world2/?dev=1
  1. QA pass: World loads - First frames in 2.0 seconds.
  1. tap #enterButton (enter World 2)
- [Screenshot](shots-iphone/002-load-and-enter-PROBLEM-console-error.jpg)

### A request failed to load

- Device: iphone; phase: load and enter; score: 45
- https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm (SSL connect error)
- Steps:
  1. === load and enter
  1. open https://www.heartbeatobservatory.com/world2/?dev=1
  1. QA pass: World loads - First frames in 2.0 seconds.
  1. tap #enterButton (enter World 2)
- [Screenshot](shots-iphone/001-load-and-enter-PROBLEM-request-failed.jpg)

### Console warning

- Device: iphone; phase: load and enter; score: 20
- THREE.WebGLProgram: Program Info Log: (221,81-129): warning X4122: sum of 0.996094 and -2.98545e-017 cannot be represented accurately in double precision
(220,37-61): warning X4122: sum of 1 and -1.49272e-017 cannot be represented accurately in double precision
(221,82-106): warning X4122: sum of 1 
- Steps:
  1. === load and enter
  1. open https://www.heartbeatobservatory.com/world2/?dev=1
  1. QA pass: World loads - First frames in 2.0 seconds.
  1. tap #enterButton (enter World 2)
- [Screenshot](shots-iphone/003-load-and-enter-PROBLEM-console-warning.jpg)

## Limits

- This is a short scripted walk and map check, not a complete city, door, multiplayer, visual, or accessibility review.
- Synthetic pointer gestures and Windows WebKit do not reproduce real iPhone touch, Safari, GPU, heat or battery behavior.
- A read-only scene raycast seeks a horizontal surface away from doors and lots; the ground check is skipped if no safe target is found.
- Network failures and local dependency substitutions are reported as observations; they do not establish what happens on the live site.

- iPhone 15 (WebKit, touch): [session video](videos-iphone/<email>)