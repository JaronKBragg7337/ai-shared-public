# The Cosmos playtest report

Run: 2026-10-04 17:55 (local)  |  Build under test: `cbdce28e67f51a90891b`  |  Site: https://www.heartbeatobservatory.com/games/the-cosmos/

A bot played the live game like a person: real taps, a held thumb on the stick, random waits, mis-taps and refreshes mid-action. It was marked as a test client (`?qa=1`) so the server sweeps it away. `dev=1` was added only so the bot can read the game's state (where people stand, button labels); every button was pressed with a real tap.

- **iPhone 15 (WebKit, touch)**: 0.4 minutes, 24 screenshots, 3 distinct problems

## Short version

3 distinct problems found: 0 blockers, 2 serious, 1 smaller.

- **Prop box overlaps the clear opening at Supply depot** (Serious, seen 2 times)
- **Prop box overlaps the clear opening at Port control** (Serious)
- **Frame-time spike during "spots"** (Annoying)

## Problems, worst first

### 1. Prop box overlaps the clear opening at Supply depot

- **How bad:** Serious (score 78), happened 2 times
- **Where:** spots, first at 00:16 into the run, on iPhone (WebKit)
- **What happened:** Port collision box COS-MARS-STR-0110 intersects the door opening (cheap bounds check).
- **Later hits:** 00:16 Port collision box COS-MARS-STR-0110 intersects the door opening (cheap bounds check).

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts
  1. spots source inventory {"doors":[{"i":0,"name":"Supply depot","x":-62,"z":26.84,"width":3.2,"progress":0},{"i":1,"name":"Port control","x":-60,"z":-33.16,"width":2.4,"progress":0},{"i":2,"name":"Crew hall","x":-28,"z":-61.16,"width":4,"progress":0}],"duplicate":[],"overlaps":[{"door":"Supply depot","prop":"COS-MARS-STR-0110"},{"door":"Supply depot","prop":"COS-MARS-STR-0110"},{"door":"Port control","prop":"COS-MARS-STR-0112"}],"counts":{"portRooms":13,"pads":5,"ships":7}}

### 2. Prop box overlaps the clear opening at Port control

- **How bad:** Serious (score 78)
- **Where:** spots, first at 00:16 into the run, on iPhone (WebKit)
- **What happened:** Port collision box COS-MARS-STR-0112 intersects the door opening (cheap bounds check).

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts
  1. spots source inventory {"doors":[{"i":0,"name":"Supply depot","x":-62,"z":26.84,"width":3.2,"progress":0},{"i":1,"name":"Port control","x":-60,"z":-33.16,"width":2.4,"progress":0},{"i":2,"name":"Crew hall","x":-28,"z":-61.16,"width":4,"progress":0}],"duplicate":[],"overlaps":[{"door":"Supply depot","prop":"COS-MARS-STR-0110"},{"door":"Supply depot","prop":"COS-MARS-STR-0110"},{"door":"Port control","prop":"COS-MARS-STR-0112"}],"counts":{"portRooms":13,"pads":5,"ships":7}}

### 3. Frame-time spike during "spots"

- **How bad:** Annoying (score 62)
- **Where:** spots, first at 00:18 into the run, on iPhone (WebKit)
- **What happened:** a single frame took 3794 ms (typical 16 ms); 5 frames over 250 ms in that window. (Headless software rendering makes everything slower than a real phone, so judge by how far a spike sticks out.)
- **Screenshot:** [007-spots-PROBLEM-frame-spike.jpg](shots-iphone/007-spots-PROBLEM-frame-spike.jpg)

  ![Frame-time spike during "spots"](shots-iphone/007-spots-PROBLEM-frame-spike.jpg)

- **Steps to reproduce (what the bot did just before):**
  1. open https://www.heartbeatobservatory.com/games/the-cosmos/?qa=1&dev=1
  1. websocket open wss://cosmos.heartbeatobservatory.com/
  1. === phase spots starts
  1. spots source inventory {"doors":[{"i":0,"name":"Supply depot","x":-62,"z":26.84,"width":3.2,"progress":0},{"i":1,"name":"Port control","x":-60,"z":-33.16,"width":2.4,"progress":0},{"i":2,"name":"Crew hall","x":-28,"z":-61.16,"width":4,"progress":0}],"duplicate":[],"overlaps":[{"door":"Supply depot","prop":"COS-MARS-STR-0110"},{"door":"Supply depot","prop":"COS-MARS-STR-0110"},{"door":"Port control","prop":"COS-MARS-STR-0112"}],"counts":{"portRooms":13,"pads":5,"ships":7}}

## What the bot got through

### iPhone 15 (WebKit, touch)

| Step | Result | Time |
|---|---|---|
| spots | done - 3 doors enumerated; 3 opening overlaps; capture prompts stored with screenshots. | 8 s |

People talked to: 0 of 16. Crew hired: 0. Panels opened: none. Course to Phobos: not started; Deimos: not started.

## Frame times (headless software rendering, so a real phone is usually smoother)

- iphone / spots: typical 16 ms, slowest 3794 ms, 5 frames over 250 ms
- iphone / spots: typical 20 ms, slowest 41 ms, 0 frames over 250 ms

## Not covered / limits

- Real iOS Safari audio, GPU speed and real thumbs are not tested; the phone run uses Playwright's Windows WebKit with a synthetic held thumb (a real second finger is not possible there), but every button is a real touch tap.
- Voice chat, other human players and signing in are not exercised.
- The bot never sees the world except through the page, so a visual problem is only caught by the pixel check or the vision pass.

## Trouble spot run details

- Port door inventory: 3 doors (Supply depot, Port control, Crew hall). The run saved 22 screenshots including six per door (15 m, 5 m and 1.5 m, shut/open) and a down-through-opening view. No vision review was run, as requested.
- Cheap bounds scan reported 3 prop-box intersections across 2 door openings. This is a coarse AABB warning and needs visual/manual confirmation.
- Playwright session recording: [<email>](videos-iphone/<email>). This records the entire session, including the door inspection sequence.
- Scope still incomplete: ramp/gangway routes and mesh visibility, parked-ship ring views, sign readability/repeated text, night pad views, and door-down camera placement are not yet exercised. The current data file lists these target types, but the phase only executes door shots plus the door AABB/name checks.
