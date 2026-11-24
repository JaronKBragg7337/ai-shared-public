# HANDOFF — World 2 remake, Phase 3: shops and jobs (things to DO)

- **Date/time:** 2026-11-11, written about 6 PM Fort Wayne time
- **From:** Fable 5.2 (Claude Code, worktree agent)
- **Project:** Heartbeat Observatory, World 2 | **Repo/branch:** heartbeat-observatory @ `fable52/world2-phase3` (worktree `C:\Users\lilli\Projects\hb-world2-phase3`) | **Live URL:** none yet. Not merged, not pushed.

## The short version
Every shop with a sign can now be walked into, and there are four jobs that pay play money into a ledger.
It is committed on my branch only (commit `b79b609e`). Everything passes in Playwright at phone and desktop size. **Nobody has held it
on a real iPhone yet**, and that is the one check that matters before it goes live.

## What I built
- **A shop table: `world2/shops.json`.** 64 shops, 40 kinds, 4 jobs. Add a row and the city gives it a storefront, a
  sign and an interior. No code. `world2/SHOPS.md` is the how-to for Jaron and the AIs.
- **114 shops you can enter.** The city deals the 64 names onto its storefronts: shops that ask for a street first
  (Calhoun Coffee is on the corner of Calhoun and Berry), then one each, then second locations far apart. No name
  appears more than twice. 5 storefronts stay empty and read FOR LEASE.
- **Doors.** A red OPEN sign on the door and a green strip on the threshold. Walk up: the prompt names the shop. Tap
  the prompt, tap the door, or press E. These marks are drawn inside the city's existing meshes: 0 extra draw calls.
- **One interior kit (`world2/shops.js`).** Three layouts (cafe, retail, service). Each shop gets a floor, two-tone
  walls, a glass front, a counter with a till and a shopkeeper who greets you, a back shelf, lamps and a back room,
  then what its kind asks for: 24 kinds of goods and pieces like an espresso machine, booths, record bins, bikes,
  flower buckets, barber chairs, washers, a vault door. Built when you walk in, thrown away when you leave.
- **The window shows the real street.** In the 0.2 s of black as you step in, the street outside is drawn three
  times and kept as one picture. Day or night, it is the street you just left.
- **Four jobs (`world2/jobs.js`).** You walk with the stick or keys. Tapping only uses things.
  - Barista at Calhoun Coffee, 90 s: use the machines in the order on the ticket, hand the cup over at the counter.
  - Newsstand seller, 75 s: a new green kiosk on the courthouse green. Tap the stack each customer asks for.
  - Bike courier, 3 runs: take the bike outside Wells St Bikes; pickup door, then drop-off before the clock runs out.
  - Usher at the Grand Palace, 90 s: guests follow you to the seat on their ticket. Seats have number plates now.
- **The ledger.** A coin under the map shows your beats. Tap it (or L): balance, where the work is with "Show me the
  way", and what you earned and spent. Every shop sells one small thing at the till.
- **Policy, built in.** No real money anywhere. Food is "pretend" and priced in beats. "Heartbeat Observatory never
  sells food, water or land, and nothing in World 2 costs real money" is in the ledger. Every shop has a PLAY MONEY
  ONLY notice by the till. The currency name ("beats") and the policy line are data, one line each to change.
- **Version stamp:** `2026-11-11-phase3`, bumped the way Phase 2 did, now in seven places (listed in WORLD2-REMAKE.md).

## Where it lives (exact)
- Code: `C:\Users\lilli\Projects\hb-world2-phase3\world2\` — new `shops.json`, `shops.js`, `jobs.js`, `SHOPS.md`;
  changed `city.js`, `life.js`, `main.js`, `index.html`. Plan doc updated: `WORLD2-REMAKE.md` ("Phase 3 as built").
- Tests and screenshots: `C:\Users\lilli\AI-Shared\scratch\world2-remake\phase3\` (scripts in `scripts\`).
- To look at it: `node C:\Users\lilli\AI-Shared\scratch\world2-remake\phase3\scripts\serve.cjs` then
  `http://localhost:8133/world2/index.html`.

## Budgets measured (Playwright on the MSI, Intel UHD GPU; old and new build in the same session)
| | Limit | Measured |
|---|---|---|
| Inside a shop, draw calls | ≤ 30 | **14**, the same in all 114 shops |
| Inside a shop, triangles | ≤ 60k | **9k to 36k** (heaviest: yarn, florist, grocer). No shadow pass, the city is not drawn |
| City, phone, street | ≤ 250 calls, ≤ 400k tris | 114 calls, 343k before → 114 calls, 343k after |
| City, phone, aerial | ≤ 300 calls | 164 calls, 331k → 164 calls, 332k |
| City, desktop, street / aerial | | 133 / 227 calls → 133 / 227 calls (+1k triangles) |
| City textures | 40 MB with everything | 18.2 MB → 21.7 MB (the sign sheet holds 64 shop names now) |
| While inside a shop | | + about 6 MB kit textures + 3 to 5 MB for the street picture |
| Frame time | | 16.7 ms median, 18.1 ms p95, same as before (vsync-locked on the MSI; says nothing about a phone) |

Outdoors Phase 3 costs 0 to +1 draw calls. **Texture memory is the one to watch: about 37 of 40 MB while you stand in a shop.**

## Verified vs not
**Verified (tested, all PASS):** Chromium 390x844 with touch, Chromium 1280x800 with mouse and keys, WebKit 390x844.
- All 114 shops: the door prompt names the shop, in, budget, out, back on the sidewalk facing the street. Also at night.
- In all 114 shops every station and the back room can be walked to (a flood fill of the floor with your body width).
  This check found a real bug (2 shops put you inside a chair) and it is fixed.
- All four jobs worked for a whole shift at phone size with real touches: the stick to walk, taps on machines, stacks
  and seats or on the prompt. Wrong machine and wrong seat are refused. Pay lands in the ledger.
- Buy at the till, the ledger card, a poster that opens a site page, the map.
- 12 visits to one shop leave nothing behind (no leak).
- Two clients on the live channel: they see each other on the street and in the same shop, not in different shops.
- Phase 2's crowd audit is still clean, all Phase 1 doors still prompt, the gate preview still loads, zero console errors.

**Not verified:**
- **A real iPhone.** Most likely to differ: the street picture in the window (it copies the canvas into a texture;
  fine in Chromium and in WebKit on Windows), the job sounds, and how a shift feels with a thumb.
- Frame rate on a phone. The MSI is locked at 60.
- The courier with a human at the stick. My first test rider rode straight at each door and bumped along the row of
  parked cars until it found a gap (two of its six runs ran out of the test's time on a door with a car parked right in front). Once it crossed at
  the corner and used the sidewalk like a person, it did 6 legs with no hold-ups, all on time. Worth one real ride.
- I aimed the camera by setting the view directly in the job tests. Drag-to-look itself was covered in Phase 1.

## Things I found that the plan did not see
1. **You used to walk into the theater, arcade and library facing the exit door.** One number was wrong. Fixed.
2. **The theater's two house lights were on all the time,** so every pixel of the city shaded two extra point
   lights. Now they only burn inside the theater. This should help phones everywhere outdoors.
3. **Inside the three halls the city was still being drawn** when you faced west: 82 to 97 calls and 265k triangles.
   Now 6 to 13 calls. Measured.
4. **Shops only face the east-west streets.** The kit never builds on Calhoun, Harrison, Clinton and the other
   north-south streets: the leftover strip is half a metre too short for a lot. Those streets are side walls. So
   "Calhoun Coffee" has its door on Berry and its side on Calhoun. Worth fixing in the layout later.
5. **The ledger is on the device, not the account.** WORLDS-MODEL says one account across worlds. That needs a table
   and a server-side function so beats cannot be forged. I left the database alone on purpose.
6. **Texture memory is near its limit** (above). 50 more shop names would cost about 4 MB.
7. Office lobbies and the towers are still not enterable. They need their own kit.

## Anything I'd change
- Give the 114 storefronts 114 names (50 more rows; each is one line).
- Use the 5 FOR LEASE storefronts for "a building can be claimed as a business" from WORLDS-MODEL.
- Shopkeepers and customers are the sidewalk figure with a face added. Up close they are plain. MetaHumans later.
- The window picture is a still. A live street through the glass would cost the whole city's draw calls indoors.
- The Grand Palace is still the old box room. The usher job should move to the real auditorium in Phase 4.
- "Beats" is my name for the play money. Jaron may want another; it is one line in `shops.json`.
- The Phase 3 test scripts should move into `tools/playtester` with the Phase 1 and 2 ones (still owed from Phase 1).

## Screenshots (`AI-Shared\scratch\world2-remake\phase3\`)
- Phone, the job loop: `phone-coffee-1-street.png` … `phone-coffee-6-shift-over.png`, `phone-ledger.png`
- Phone, other jobs: `phone-news-1-the-stand.png`, `phone-news-2-selling.png`, `phone-courier-1-the-bike.png`,
  `phone-courier-2-riding.png`, `phone-usher-2-at-the-seat.png`
- The window: `phone-window-day.png`, `desk-window-day.png`. The map: `phone-map.png`
- One shop of every kind (40): `gallery-desk-in-day-1.png` to `-4.png`, `gallery-phone-in-day-1.png` to `-3.png`
- Desktop, the same coffee loop with mouse and keys: `desk-coffee-1-street.png` … `desk-coffee-6-shift-over.png`
- The city after: `city-desk-day-coffeeCorner.png`, `city-desk-night-coffeeCorner.png` and the street/aerial pairs
- Numbers: `results-*.json`, `measure-before-after.json`

## Blocked / needs a human
- Jaron on his iPhone: walk into Calhoun Coffee, look out the window, work one barista shift, ride one courier run.

## Exact next step for the next AI
- Review the branch, phone-check it, then merge and push (I did neither, as asked). If the window picture is black or
  wrong on the iPhone, `shops.open(slot, { street: false })` in `enterShop()` falls back to a plain sky colour.
