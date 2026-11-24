# The Cosmos: Fable build log

Lead builder: Fable 5.2. Started 2026-11-19 12:50 PM. Jaron: "Let Fable just build what Fable wants... Goal is a full game that makes sense."
Worktree: `C:\Users\lilli\Projects\ho-fable-cosmos` (branch `fable/cosmos-look-2026-11-19`), pushed to main after each milestone.
The plan page: `games/the-cosmos/docs/GAME-PLAN.md`. Screenshot tool: `cshot.mjs` here (scenarios `sc-*.mjs`), shots in `shots/`.

## Notes that hold for the whole run

- **F0 faction styles: nothing to recover.** Checked 11/19 1:00 PM: every file of commit 0c0228c7 in `ho-f0f3` (src/factions/**, test/pkg-factions.mjs,
  docs/FACTION-STYLES.md) is already on main, identical except line endings. The uncommitted files there are build stamps only.
- **The live game server (the authority) runs from the main checkout on the MSI** and is older than main (its build id differs from the live site's).
  Client-only changes (looks, UI) go live through the site alone. A change to shared rule code (anything `server/*.mjs` imports from `src/`)
  does NOT reach live players until someone updates and restarts that checkout, which this run may not touch. So this run stays client-side,
  and flags any rule change it would have needed.
- The site's deploy stamps its own build id; a local `tools/stamp-cosmos-build.mjs` run is not needed before pushing.

## Baseline checks (before any change of this run, 12:59 to 1:45 PM)

- `node test/phone-check.mjs`: 33 pass, 0 fail.
- `node test/validate.mjs` (takes about 45 minutes): 2010 pass, 2 fail. Both failures are not from this run and not about looks:
  "Deimos is farther and takes longer (47 min)" (trip maths on today's real orbit positions) and "holding Talk puts real audio packets
  into the other" (the fake microphone in a headless browser). So this run gates each milestone on phone-check plus its own browser
  shots, and runs the full validator now and then.

## Milestone 0: the plan page (1:00 PM)

- `games/the-cosmos/docs/GAME-PLAN.md`: what the game is, the journey, what exists, what is weak, the ordered next list, the full-game
  checklist, open questions, where the plan versions disagree, ideas kept from older plans. Reconciled against every plan version
  the orchestrator listed (a subagent read all nine documents; newest wins).
- Went live inside milestone 1's commit.

## Milestone 1: pressure suits, helmets, low-gravity bound (1:05 to 2:05 PM)

- What changed: `src/crew/personRig.js` (`Person.setSuit`, `buildSuit`: rigid suit pieces bound to the person's own bones, one draw call
  plus the visor; the face stays visible behind the visor), new `src/crew/suitPolicy.js` (suit when outside and the air is under 50 kPa;
  bound when gravity is under 2 m/s2), wired for the player, Mars port workers (tower crew indoors excepted), Moon, Ceres and Callisto
  people, the opening's guide, gate officer, driver and recruiter, and other players. Review cameras can show the player
  (`cosmos.freeCam.showPlayer = true`).
- Live commit: `17774701`. Live build id `1d810aa802ce617046c7`.
- Before: `../cosmos-fable-look-2026-11-19/shots/after/11-phobos-third-walk-phone-webkit.png` (T-shirt and jeans on Phobos).
- After: `shots/m1-wip/s6-phobos-walk-b-phone-webkit.png`, `s2-phobos-front-close-desktop-chromium.png`, `n1-mars-traders-desktop-chromium.png`,
  `n3-moon-desktop-chromium.png`, `n3-ceres-phone-webkit.png`. Live: `shots/m1-live-plain.png` (a visitor's page), `shots/m1-live-solo.png`.
- Verified locally: iPhone WebKit 390x844 and desktop Chromium 1440x900, no page errors, no sideways scroll, phone-check 33/33.
- Verified live: the page loads for a visitor at phone width with no errors and no sideways scroll; in a solo review session on the live
  build the suit is on and the gait is the bound on Phobos.
- Not verified: a real iPhone. Two real players seeing each other's suits (code path only). Suits inside domes and halls: there is no
  "indoors" record for buildings yet, so people under the Daedalus dome and in the arrivals hall wear suits too. Hired crew walking
  from the hall to a ship still wear plain clothes. Hair may poke through a helmet on big hairstyles (seven bodies, three looked at).

## Milestone 2: airless worlds look airless (2:05 to 2:55 PM)

- What changed: `src/space/spaceSky.js` (fill light on airless worlds is now Marsshine from above plus ground bounce from below; the Sun's
  light respects Mars's shadow and the local horizon), `src/world/regolith.js` (small craters in the surface normal, Phobos's 70 cm streaks
  removed, the bump fades with distance), `src/world/planetMesh.js` + `src/space/moonField.js` (baked terrain shadows smoothed and nearly
  black on airless worlds), `src/main.js` (a finer, tighter sun shadow map on airless worlds).
- A real bug found on the way: a moon inside Mars's shadow stayed in full sunlight while the helmet lamp came on. Phobos is eclipsed for
  up to 54 minutes of each 7.65 hour orbit, so players met this often.
- Live commit: `2e8519fd`.
- Before: `shots/m2-before/` (same cameras, real clock, Sun at 20 and 55 degrees). After: `shots/m2-wip/` (same names; `-moon`, `-ceres` suffixes
  for those worlds; `*-phone-webkit.png` for the phone). Best pair: `p5-third-high-*`, `p2-eye-rocks-high-*`, `p7-final-low-*`.
- Verified locally: iPhone WebKit and desktop Chromium on Phobos, desktop on the Moon and Ceres; no page errors; phone-check 33/33.
- Not verified: live check for this commit is in the next entry. Deimos and Callisto were not looked at after the change (same code path).
  Ship interiors parked on a moon were not re-checked for brightness. The full validator was not re-run after this change.
- Review tip: every earlier look review used the pinned dev Sun. Use `&sky=live` and `cosmos.setSkyShift(seconds)`; `sc-phobos.mjs` finds
  a low and a high Sun by itself and skips times when Mars eclipses the moon.

## Milestone 3: a night you can walk in (2:55 to 3:10 PM by the log, 2:05 PM by the MSI clock: earlier times in this log are estimates)

- What changed: `src/main.js` (Mars's whole-planet shell keeps the Sun's light when the camera's key light is off; a white helmet beam
  along the view on airless worlds at night or in a hole), `src/space/spaceSky.js` (Marsshine counts for more once the Sun is gone).
- Found on the way: after milestone 2 made the Sun's light respect shadow, Mars itself went black in Phobos's night sky. Fixed here; Mars
  is now the bright showpiece it should be (`shots/m3-wip/g4-sky-0-night-*.png`).
- Live commit: `fbf32d13`.
- Before: `shots/m3-before/` (black screen at night: `g2-third-night`, `g5-pad-night`). After: `shots/m3-wip/` same names, plus
  `sheet-mars.png` (Mars port at night, dusk and noon: no change intended there) and phone shots `*-phone-webkit.png`.
- Verified locally: desktop Chromium and iPhone WebKit; phone-check: iPhone 17/17; Galaxy failed 4 steps on the first run
  ("execution context destroyed" in the opening's ride step) and passed 16/16 when run again alone. Treated as a flake; watch for it.
- Not verified: Deimos, the Moon, Ceres and Callisto at night (Ceres and Callisto use their own light settings and did not get the
  night boost). The beam in a dug hole. A real phone.
- Seen, not fixed: at Mars dusk the open ground takes the sky's blue (`sheet-mars.png`, middle row). The pad paint on Phobos glows
  bright orange at night.

## Scope change (Jaron, 1:59 to 2:04 PM)

Production-ready full game, built in whole parts; every platform (phone iOS + Android first, PC with mouse/keyboard and gamepad, the
home-screen app, consoles later). GAME-PLAN.md now has ten parts in the order a new player meets them and one production bar.
Milestones 1 to 3 are "part 0, looks groundwork". Next: part 1, the first hour.

- Milestone 3 live check (2:20 PM): live build `66d385efc348f8571f87`; a visitor's page loads at phone width with no errors and no
  sideways scroll; solo review session on live shows the suit and the bound.

## Milestone 4: a controller plays the game (2:10 to 2:35 PM, MSI clock)

First piece of part 4 (the game shell: every platform).

- What changed: new `src/ui/gamepad.js` (standard Gamepad API to the keys and look the game already uses; a D-pad focus ring over
  on-screen buttons; `inputKind()` / `hintFor()` so hints name the device in hand), wired in `src/main.js` (polled first each frame,
  a help toast on first use, `cosmos.gamepad` in dev), opening hints in `src/opening/opening.js`, a controller line in Settings
  (`index.html`), new test `test/gamepad-browser.mjs`.
- Live commit: `44c24bb8`.
- Verified locally: `node test/gamepad-browser.mjs` 20/20 (a fake standard pad on desktop Chromium and the iPhone WebKit profile: walk,
  look, no stuck key, view switch, settings, focus ring, A to press, no errors, no sideways scroll). phone-check 33/33.
- Not verified: a real controller in a real hand (feel, dead zone, look speed). Flying a ship with the pad (it sends the same keys the
  keyboard does, so it should fly, but nobody flew it). Every panel with the focus ring (only Settings was tested). No button remapping.
  The left stick is on/off, not analog. Live check of this commit: see the handoff.

## HANDOFF (written 2:35 PM MSI clock, 11/19, by Fable 5.2; context getting long)

**State.** Five commits live on main from this run, in order: `10f47520` (lamp), `17774701` (suits + plan page), `2e8519fd` (airless
light), `fbf32d13` (night + plan in parts), `44c24bb8` (controller). Worktree `C:\Users\lilli\Projects\ho-fable-cosmos`, branch
`fable/cosmos-look-2026-11-19`, clean except `docs/qa/phone-check/2026-11-19/` (untracked test output; leave it out of commits).
A static server may still be running on port 4380 from the worktree (shots use it); start one with `PORT=4380 node server.js`.

**The plan.** `games/the-cosmos/docs/GAME-PLAN.md` is the current plan: ten parts in the order a new player meets them, one production
bar every part must pass, the platform line (phone iOS + Android first, PC keys + gamepad, home-screen app, console-ready later).
Part 0 (looks groundwork) is shipped as a first version. Keep its checklist and "Shipped" table current after every part.

**Next three, in order.**
1. **Part 1, the first hour, as a production pass.** Play the opening as a brand-new player on the iPhone WebKit profile from first
   launch to first take-off and fix every unclear moment. Start from `test/opening-browser.mjs` (it drives the whole flow) and the old
   shots in `docs/qa/2026-10-03/opening2/` (sheet: `shots/opening-phone-sheet.png`). Already seen: the Kestrel's cruise to another world
   is a white screen with pale text on it (`phone-kestrel-space.png`); buttons on a phone still show key letters ("Carry (E)",
   "Open the crew locker (E)": use `hintFor` from `src/ui/gamepad.js`); check sound on the key beats, refresh at every stage, and the
   server-down path. The opening's people on the apron now wear suits: look at the guide, the gate officer and the driver in the
   real flow (only wired, not looked at).
2. **Part 4, the game shell.** Home-screen app mode (test with a standalone display: no browser bars, safe areas, rotation, return
   from background), a quality setting and frame-rate check on the phone tier, long-session memory, the server-down message, then the
   focus ring on every panel and analog sticks.
3. **Part 2, Mars and its moons as a finished region.** Real boulders with shadows on Phobos and Deimos, the square detail patch seen
   from space (look-pass problem 5), hull plates instead of "bricks", suits off indoors (needs an "indoors" record for buildings),
   Mars dusk ground turning sky-blue, the Phobos pad paint glowing at night, a reason to visit each place.

**Gotchas.**
- `node --check file.js` does NOT catch errors in these ES modules here. Copy the file to `something.mjs` and check that.
- Bash heredocs in this harness break on some files with apostrophes or backticks. Write patch scripts with the Write tool, then run them.
- The live game server (authority) runs from the main checkout, which this run must not touch. Everything shipped so far is
  client-only. A change to rules shared with `server/*.mjs` needs the orchestrator to update and restart the server: flag it.
- The deploy stamps the build itself (vercel.json). New modules need no local stamp.
- Full `node test/validate.mjs` takes about 45 minutes and rewrites tracked files under `docs/qa/`: run `git checkout -- games/the-cosmos/docs/qa`
  in the worktree afterwards. Its two known failures are in "Baseline checks" above. phone-check takes about 3 minutes; its Galaxy half
  flaked once ("execution context destroyed" in the ride step) and passed on a rerun.
- Review looks with the real clock: `Q='&sky=live'` and `cosmos.setSkyShift(seconds)`. A `?dev=1` session without it pins a high Sun and
  hides night, eclipses and low light. `sc-phobos.mjs` and `sc-night.mjs` find the Sun angles themselves.
- `window.cosmos` exists only in dev sessions; a visitor's page has none (the live check waits for the canvas instead).
- Shots: `node cshot.mjs <webkit|chromium> <phone|desktop> <outDir> <scenario.mjs> [names]`; live: `node live-check.mjs <prefix> [scenario]`.
- 2:40 to 7:30 AM the MSI GPU belongs to the news render: no browser testing then.

- Milestone 4 live check (2:18 PM): live build `777699b806d24f7102ef` serves `src/ui/gamepad.js`; a visitor's page loads at phone width with no errors and no sideways scroll (`shots/m4-live-plain.png`). The controller itself was not driven on the live site.

---

# Second Fable session (started 2:18 PM MSI clock, 11/19)

## Part 1: the first hour, production pass (2:18 to 2:54 PM, MSI clock)

A whole part, not a fix: the opening played on an iPhone-size screen from first launch to the home pad, every beat photographed and its
words written down, then fixed and played again. New test `test/first-hour-browser.mjs` does that play-through on an iPhone profile
(WebKit, 375 px) and an Android profile (Chromium, 360 px) and checks every beat for things a stranger trips on.

- Found on the first play (before: `shots/p1-before-sheet-a.png`, `-b.png`, `-c.png`; 14 of 49 checks failed; after: iPhone and Android profiles pass every beat):
  1. Every action button on a phone showed a keyboard letter: "Read the board (E)", "Dig (E)", "Carry (E)", "Walk (Q)", "Ride (E)".
  2. The whole flight to another world was a close-up of a wall. Boarding stood you in a windowless vestibule facing a door.
  3. Spoken lines were pale text straight on the picture: unreadable over a white wall, a bright floor, the truck.
  4. The three-and-a-half-minute liner ride gave no word on how long it lasts or that you can walk. The "how to move" hint was
     replaced by "tap to turn on sound" for its whole life on a phone.
  5. The arrow to the arrivals hall only appeared after a full minute of being lost, with no name or distance.
  6. Arriving home: the first goal was a long paragraph in tiny type naming two people and two places at once, and a toast said "Ceres frame."
  7. No sound answered anything the player did: not a press, not the shovel, not the crash.
  8. Settings could not be opened at all during the opening (about the first ten minutes of the game).
- What changed (after: `shots/p1-after-sheet-a.png`, `-b.png`, `-c.png`, desktop `shots/p1-desktop-sheet.png`):
  - `src/ui/gamepad.js` `labelFor()`: one label, three devices. A thumb sees "Dig", a keyboard "Dig (E)", a controller "Dig (X)".
    Used by the opening's buttons, the main action button, Climb, Drop all and the "Stand up" hint.
  - `src/opening/opening.js`: lines and hints sit on a dark plate sized to the words; the liner says how to move for 40 seconds, then
    "Landing on Mars in about 2 minutes. The ship is yours to walk until then."; the Kestrel says where its windows are when you
    stand in a room without one; Settings stays reachable for the whole opening (rows that need the open game are put away).
  - `src/ui/goalHint.js`: a goal can ask for its arrow early and carry a name and a distance ("Arrivals hall · 68 m",
    "Marta Voss · 298 m", "Your lifeboat · 40 m"). The old one-minute rule stays the default everywhere else.
  - `src/opening/repair.js`: the lifeboat's first goal is one step at a time ("Step 1 of 3: buy a power cell (300 marks) from Marta
    Voss, the foundry foreman. Follow the arrow, then use the button when you reach them."), in plain letters.
  - New `src/ui/sfx.js`: small made-on-the-spot sounds (no downloads): a press for every button in the game, a shovel bite, a lift,
    a latch, a yes, a no, the crash, arriving home. Settings has "Action sounds" (on by default, remembered).
  - `src/space/spaceSystem.js`: "Ceres frame." now reads "Now in Ceres space."
  - `src/opening/state.js`: boarding puts you in the forward cabin's aisle facing a starboard window (`shots/p1-kprobe-a.png` shows the
    whole flight from there: Mars falling away, the cruise, the other world filling the glass).
- Live commit: `a238af70` (parts 1 and 4 together).
- **NEEDS THE GAME SERVER RESTARTED (orchestrator):** the boarding spot (`KESTREL_BOARD` in `src/opening/state.js`) is set by the
  server. Until it is restarted from a checkout that has this commit, live players still board in the vestibule; they now get the
  hint that says where the windows are. Nothing breaks either way.
- Verified locally: `node test/first-hour-browser.mjs` (iPhone and Android profiles: every beat, a refresh in every stage, sounds
  counted on the Android half because Playwright's WebKit on Windows has no Web Audio at all); `node test/opening-browser.mjs` passed
  (desktop flow, refresh, five crash causes, two players); `node test/gamepad-browser.mjs` 20/20; phone-check iPhone 17/17, Galaxy 16/16 when run alone (in the full run its ride step
  flaked again with "execution context destroyed" and six later steps fell with it: the same flake the first session logged); `node test/opening-checks.mjs` exit 0.
- Not verified: a real phone. The walk between the beats (the test places the player at each spot; nobody thumbed the whole
  route). The first take-off after fitting (the old desktop test fits the parts; the lift-off itself was not flown here).
  How the sounds actually sound (they were counted, not heard). The controller through the whole opening (hints only).
  Sound on iOS Safari itself. The Earth, Moon and Callisto starts.
- Seen, not fixed: on a phone the lounge view is half ceiling (tall screen, fixed field of view). The home pad's first view is the
  lifeboat's hull, close. Ceres's horizon shows noisy stripes on a desktop (`shots/p1-desktop-sheet.png`, top left). The status card
  still leads with coordinates and gravity before the next step. A first-time player has no Skip (by design) and the liner is 3.5 minutes.

## Part 4, the game shell: server down, picture quality, home-screen app (2:37 to 2:54 PM, MSI clock)

Second set of pieces of part 4 (the controller was the first). Shipped in the same commit as part 1.

- What changed:
  - `src/world-state/remoteWorld.js`: when the shared world does not answer on first launch the page used to wait for ever under one
    small line. Now it says "The shared world is not answering. Trying again…", keeps trying by itself, and shows a button, "Play on
    your own for now", with one line under it: a solo game saves on this device and the shared-world journey is safe and waiting.
    (`shots/p4-shell/iphone-server-down.png`, `android-server-down.png`.) A drop in the middle of a game was already handled.
  - New `src/ui/quality.js` and a "Picture quality" row in Settings: Auto, Fast, Full detail. It is remembered on the device and
    reloads the game into the choice. Auto is the old guess (touch screen = Fast, else Full). On Full detail the game now watches its
    real frame rate; under about 22 frames a second for 15 seconds it offers Fast once ("Switch to Fast" / "Keep Full detail").
  - New `games/the-cosmos/manifest.webmanifest` and its link in `index.html`: "Add to Home Screen" from the game's page installs The
    Cosmos itself (opens the game, full screen, any rotation). Before, the site-wide manifest made that icon open the site's front page.
    It uses the site's icons: the game has no icon of its own yet.
  - Settings is reachable during the opening (logged under part 1).
- **A choice to check (Jaron or the orchestrator):** the game page now has its own home-screen app instead of the site-wide one. To go
  back, remove the one `<link rel="manifest">` line in `games/the-cosmos/index.html`; the deploy then stamps the site manifest again.
- Verified locally: `node test/shell-browser.mjs` on an iPhone profile (WebKit) and an Android profile (Chromium) against a static
  server with no game server behind it: the message, the button's size, a solo game really starting, Settings opening inside the
  opening, the quality row, the reload into Full detail and the saved choice, the manifest served. Pictures in `shots/p4-shell/`.
- Not verified: the installed app itself on a real iPhone or Android phone (no browser bars, the notch, rotation, coming back from the
  background): only the tags and the manifest were checked. The slow-device offer on a really slow device (its arithmetic is tested,
  the pop-up was not seen). Memory over a long session. A server that dies and comes back while the "not answering" screen is up.
- Still open in part 4: the installed app on real phones; analog sticks; the focus ring on every panel; long-session memory; a
  loading screen that says what it is loading; a "back online, return to the shared world" offer inside a solo game; a game icon.

- Live check of `a238af70` (2:58 PM): live build `38662f83f423fb1c62bc` serves `src/ui/sfx.js`, `src/ui/quality.js` and the game's
  `manifest.webmanifest`. A visitor's page at 375 px starts the opening with no errors and no sideways scroll; the plate and the
  Settings button show; Settings opens inside the opening with Picture quality ("Now: Fast.") and Action sounds; the page carries
  only the game's manifest. Pictures: `shots/p1-live-sheet.png`.

## Parts 1 and 4, follow-up: the lifeboat comes alive; the way back from solo; a phone on its side (2:58 to 3:12 PM, MSI clock)

- What changed:
  - `src/opening/repair.js`: the moment both parts are fitted the game now says "Power on. Your lifeboat flies. Climb aboard and take
    the pilot seat." with the arrival sound (it used to pass with no word). The buy button reads "Buy the power cell · 300 marks"
    (it was a five-line sentence on a phone).
  - `src/world-state/remoteWorld.js` `watchForReturn()`: a solo game that started because the server was down looks in on the server
    every 20 seconds; when it answers, one offer: "Return to the shared world" / "Stay solo" (`shots/p4-shell/iphone-world-back.png`).
  - `src/opening/opening.js`: on a phone held sideways the spoken line sits lower, off the middle of the picture.
  - `test/first-hour-browser.mjs` now plays on through the home pad with real taps: buy the cell, buy the coupler, fit both, and reads
    the status card after each (Step 1, 2, 3 of 3) and the "Power on" line. 78 of 78 checks.
- Rotation looked at (`rotate-probe.mjs`, `shots/p4-rotate-cr-sheet.png`): in Chromium at 812 x 375 the opening and Settings lay out
  with nothing off screen and no overlapping buttons. **In Playwright's WebKit the 3D picture went black after the turn**
  (`shots/p4-rotate-sheet.png`) while the words stayed. Chromium does not do it, so it may be the test browser and not the game, but
  nobody has turned a real iPhone sideways in this game today: check that first on a real phone.
- Seen, not fixed: the test stands the player exactly on a person's spot, which puts the camera inside their head (a red eye and a
  mouth fill the screen: `shots/p1-home-sheet.png`). A real player walks up and stops short, but nothing stops you walking into a
  person. `?opening=off` did not switch the opening off on a second visit in a solo dev session (the probe's last three pictures).
- Live commit: `664e1661`. Live check (3:19 PM): build `9cf6b4d578c285c15542`, a visitor's page at 375 px, no errors, no sideways scroll.
- Verified locally for `664e1661`: first-hour 78/78, shell 41/41 (both phone profiles).

## Part 1, last piece: the next step leads the status card (3:16 to 3:27 PM, MSI clock)

- What changed: `src/main.js`, `index.html`: a new pilot's card opens with the one plain next step; the readings (place, coordinates,
  ground, cart, tool) come after it (`shots/p1-home-sheet2.png`: Step 1, Step 2, Step 3, then "Power on" and the first job offer).
- Live commit: `23f08510`; then `9b26edf3` (plan page only). Live check (3:27 PM): build `351664e502395b58c3b6`, a visitor's page at
  375 px, no errors, no sideways scroll, Settings opens in the opening.
- Verified locally: first-hour 78/78; phone-check iPhone 17/17 on the second run (the first run failed one step, "this browser could
  not decode a voice mp3 (0)", while a live check was running beside it: treated as load, watch for it).
- Also checked: what a live player sees in the Kestrel until the server restarts (`shots/p1-kprobe-vestibule.png`): the wall, with the
  line "The windows are in the forward cabin: through the door ahead, then right." on a plate for the whole flight.
- Not verified: the card on a real phone; the Galaxy half of phone-check was not re-run after this last change.

## HANDOFF 2 (written 3:30 PM MSI clock, 11/19, by Fable 5.2, second session; stopped for the 4:10 PM session reset)

This replaces the first handoff above as the place to start. Its gotchas still hold; new ones are added below.

**State.** Live on main from this session, in order: `a238af70` (part 1, the first hour, production pass + the game shell's
server-down path, picture quality, home-screen app), `664e1661` (the lifeboat comes alive, the way back from solo, a phone on its
side), `23f08510` (the next step leads the status card), `9b26edf3` (plan page). All four checked live at phone width.
Worktree `C:\Users\lilli\Projects\ho-fable-cosmos`, branch `fable/cosmos-look-2026-11-19`, clean except untracked test pictures
(`docs/qa/2026-11-19/`, `docs/qa/phone-check/2026-11-19/`: leave them out of commits, 20 MB). A static server may still run on 4380.

**For the orchestrator, two things only you can do.**
1. **Restart the game server** from a checkout with `a238af70` or later. `KESTREL_BOARD` in `src/opening/state.js` now boards a
   player at a window in the forward cabin; the server sets that spot. Until the restart, live players board in the windowless
   vestibule (they get a hint that says where the windows are). Nothing breaks either way.
2. **A real phone, five minutes.** Nobody has held this build. Most wanted: (a) turn an iPhone sideways in the game: the picture went
   black in the WebKit test browser and not in Chromium; (b) hear the sounds (press, dig, crash, arrival): they were counted, not heard;
   (c) "Add to Home Screen" from the game's page, open the icon: it should open The Cosmos full screen, not the site's front page.

**Where the production bar stands** (`games/the-cosmos/docs/GAME-PLAN.md` has the table, one row per part):
- Part 1, the first hour: stranger understands, refresh, no errors, sound: yes on the iPhone and Android test profiles. Open: a real
  phone; the walk between the beats by a real thumb; the first take-off; a controller through the opening; the Earth, Moon and
  Callisto starts; frame rate and memory measured.
- Part 4, the game shell: server down (first launch, and the way back), picture quality with a slow-device offer, Settings in the
  opening, action sounds, the game's own home-screen manifest, a controller (first version). Open: the installed app on real phones,
  analog sticks, the focus ring on every panel, long-session memory, a game icon, a loading screen that says what it loads.

**Next three, in order.**
1. **Finish part 1's open items that need no phone:** fly the first take-off in `test/first-hour-browser.mjs` (after "Power on" the
   player is told to take the pilot seat: check the seat, the lift-off button and the first job offer on a phone), and play the
   opening with the pad (`test/gamepad-browser.mjs` has the fake pad). Stop people being walked into (the camera ends up inside a
   head: `shots/p1-home-sheet.png`).
2. **Part 2, Mars and its moons as a finished region** (unchanged from the first handoff: boulders with shadows, the square patch
   from space, hull plates not bricks, suits off indoors, Mars dusk ground turning blue, the Phobos pad paint glowing at night,
   a reason to visit each place). Build `test/mars-region-browser.mjs` the way `first-hour-browser.mjs` is built: play it, write
   down every beat's words, picture it, then fix.
3. **Part 4's rest:** analog sticks, the focus ring on every panel, a memory check over a 30-minute session, a game icon.

**New gotchas.**
- Playwright's WebKit on Windows has no Web Audio at all (`typeof AudioContext === 'undefined'`). Anything about sound must be
  checked in Chromium; `first-hour-browser.mjs` counts sounds on its Android (Chromium) half.
- Many source files here have CRLF line endings and some are mixed. A multi-line search-and-replace from a script silently fails
  to match. Anchor on one line, or use the Edit tool.
- Bash heredocs that write Python with backslashes mangle it. Write the script with the Write tool, then run it.
- The test authority (`server/index.mjs`) does not serve `manifest.webmanifest`; `server.js` and the live site do.
- A test that places the player and reads the status card at once reads the old card: the server's answer comes in real time and
  the card redraws about once a second. Poll for it (`until()` in `first-hour-browser.mjs`).
- `test/shell-browser.mjs` starts its own static server on 4391 and stops it; if a run is killed, stop that server by hand
  (`netstat -ano | grep 4391`).
- phone-check's Galaxy half still flakes in the ride step when run after the iPhone half; alone (`PHONE_ONLY=Galaxy`) it passes 16/16.
- Tools added in this folder: `live-p1.mjs` (live check of the opening's first screen and Settings), `rotate-probe.mjs`
  (`ENG=chromium` for Chromium), `sheet.py <dir> <out.png> [name parts]` (contact sheets; `COLS=`, `W=`).

---

# Third Fable session (started 4:05 PM MSI clock, 11/19)

Rebased on main (nothing new). Orchestrator's news taken in: server restarted 3:35 PM on `ac9cf385`; the own-manifest question is Jaron's, left alone.
Jaron's 4:15 PM direction ("all factions working, jobs, missions, more things in environments") folded into the plan's order: after the first hour come
a lived-in Mars region (part 2), jobs and missions as a ladder (part 3), factions that visibly do things (part 4); the shell keeps growing beside them.

## Part 1, last stretch: the first take-off (4:05 to 5:20 PM); shipped `e964e9e0`

Played from "power on" to the first landing on an iPhone-size screen with real taps and a held thumb: new test `test/first-flight-browser.mjs`
(iPhone WebKit 375 px + Android Chromium 360 px; `SKY=day|night` turns the real Sun to the hour asked for; `WORLD=ceres|mars`). 79 of 79 checks pass.
Before: `shots/ff-before-sheet.png`, `shots/ff-before-sheet-b.png`. After: `shots/ff-day-night.png` (day), `shots/ff-night-after.png` (night).

Found on the first play, all fixed:
- **Nobody was told how to fly.** After "Power on" the card went straight to a job on foot. Now four plain steps lead the card (and an arrow with a name
  points at the ramp): get in by the ramp at her back; the pilot seat and the door marked FLIGHT; hold LIFT; fly, then LAND. Then "Down and safe. That was
  your first flight", a sound, and the card moves on to work. Kept per player on the device, so a refresh does not start the lesson again; a pilot with a
  crew or a bigger ship never sees it. The words change for keys, thumbs or a pad. `src/opening/repair.js`.
- **Holding LIFT could leave the ship sitting on its pad.** With the ramp down the client asked the server for the ramp every frame until the answer came,
  and each ask is a toggle: up, down, up. Now one ask at a time. `src/world-state/multiplayerView.js`.
- **At night the ground of an airless world could not be lit by anything.** The baked shadow painted the ground black whenever the Sun was down, so the
  helmet lamp, the beam and Mars in the sky had nothing to light (the 11/19 night work lit people and hulls, not the ground). Now nothing is baked once the
  Sun is well under the horizon. `src/world/planetMesh.js`. Lamps also come on as the Sun reaches the horizon on airless worlds, not 2 degrees under it.
- **A refresh on a night side could throw the game into safe mode** ("First frames contain only the clear color"): 25 sample points of a night picture are
  all black. The check now reads three whole rows first and is skipped when it is known to be night. `src/core/graphicsHealth.js`.
- **The ship lights her own pad at night** (one wide lamp under the hull, on only in the dark and near the ground). From the chase view there was a lit toy
  on a black screen and no ground to leave or come back to.
- Two server answers no player should see ("Use the seat request.", "Board or leave through the boarding action.") no longer pop up when sitting or boarding.
- "Mars neutral airspace" was shown over Ceres: off Mars it says "Port airspace".
- Ramp and Course buttons at the pilot seat were 30 px tall: now 40.
- The arrow's name tag no longer lies across the status card.

**Server-shared rule changed (orchestrator: restart when convenient, nothing breaks until then):** `server/authority.mjs`, the `ramp` action. An owner standing
outside could work the ramp only on Mars (the check used the port's own "near", which is Mars only; everywhere else it answered "Walk over to them first.").
Now it checks the distance to the ramp foot on whatever world the ship stands on. Until the restart, the outside "Raise ramp / Lower ramp" button does nothing
off Mars; boarding and flying are not affected.

Not fixed, seen: LIFT held 8 s on Ceres puts her at 600 m and 150 m/s (thrust is tuned for Mars; Ceres pulls 13 times less). The 6 s wait while the ramp folds
before she moves. Toasts land on top of the flight bar. Walking straight in from the ramp meets the cabin table (a player steers round it).

Also in `e964e9e0`: **a controller plays the opening.** New test `test/gamepad-opening-browser.mjs` (a fake pad, no key, mouse or touch): sticks walk and look on
the liner, X reads the board, the D-pad and A choose a world and a side, X boards, opens the locker, climbs out, digs, lifts the crate and takes the ride. 23 of 23.
Found and fixed: the board's sides are radios, not buttons, and the pad's focus ring could not reach them (a controller player could not leave the port).

Checks before the push: first-flight 79/79 (iPhone + Android, night), first-hour 78/78, gamepad 20/20, gamepad-opening 23/23, shell 41/41, phone-check all pass.
Live (5:25 PM): build `7ba7768474c958a1acd9` serves the new steps; a visitor's page loads at phone width, no errors, no sideways scroll (`shots/p1b-live*`).
The take-off itself was not flown on the live site (it needs a fitted lifeboat on the live server).

## Part 2, first half: Mars and its moons, a lived-in region (5:00 to 5:45 PM)

Jaron, 4:15 PM: "all factions working, jobs, missions, more things in environments". A survey first (what moves today: nothing; every person stood still, no
ship ever landed by itself, Phobos had a painted disc, Deimos had rocks). Then four pieces built side by side (two by helper agents under my brief, two by me):

- **Stickney East on Phobos is a station now** (`src/worlds/phobos/client.js`, `outpostKit.js`): three habitat cylinders under a regolith-bag berm with an airlock
  facing the pad, a guyed comms mast and dish, three propellant tanks with a pipe run to the pad edge, a regolith oven and its spoil, eight solar wings, a cargo
  yard of lashed containers and netted crates, a hopper, 24 pad edge lights, lit signs, tether lines and anchor piles everywhere (Phobos pulls 0.006 m/s2), and
  three suited people, one walking the tether line. About 10 draw calls. Pictures: `shots/p2-outposts-sheet.png`, `shots/p2-phobos-*`.
- **A survey camp on Deimos** (`src/worlds/deimos/client.js`): a marked landing circle with edge lights, an inflatable shelter under a bag berm, a tripod core
  drill on anchored outriggers with its control stand and core rack, a beacon mast, solar wings, crates, three people. Pictures: `shots/p2-deimos-*`.
- **Ships come and go at Marineris Port by themselves, and a cargo tug drives the apron** (`src/port/traffic.js`): a hauler or a courier flies an approach,
  comes down on its lift engines, drops its ramp, sits a couple of minutes, lifts and leaves. The timetable is a pure function of the shared world clock, so two
  players see the same ship land at the same moment; at most two alive (one on a phone); they use spots no player's ship is given, and wave off if one is taken.
  Pictures: `shots/p2-traffic-sheet.png`, `shots/p2-traffic/`.
- **People at work at the port** (`src/port/portPeople.js`): five suited workers walk a beat between two places of work, stop, and walk back (three on a phone):
  a porter along the market and the arrivals hall, a pad hand round Pad 01, a fuel hand, a loader, a runner between the tower and the crew hall. On the real
  ground, not a flat plane. Pictures: `shots/p2-walkers-sheet.png`.
- **The Moon Round: three paid jobs that lead on from one another and take a pilot to each place** (`src/missions/catalog.js`, thread `mars-moons`, from the
  supply clerk, open from the first day): "Stores for Stickney" (a case of scrubber cartridges to the Phobos airlock, 220 cr), then "Cores from Deimos" (a rack
  of drill cores back to the weather desk, 320 cr), then "The moon round" (both moons in one run, 400 cr). New test `test/moon-round-checks.mjs` plays all three
  on the real authority with real flights: 13 of 13.

**Server-shared files changed (orchestrator: the three new jobs do not exist for live players until the game server is restarted on this commit):**
`src/missions/catalog.js` (three missions, one thread) and `src/port/portPeople.js` (walkers only; `PORT_WORKERS` is unchanged). Everything else in this half
is client-only and live at once.

Shipped `3ee80594` (5:40 PM). Checks before the push: first-hour 78/78, phone-check all pass, port / moons / worlds checks exit 0, pkg-missions 80/80,
moon-round 13/13. Live (6:18 PM): build `126aa1f5671d6ee3fec2` serves `src/port/traffic.js` and the three new jobs in the catalog. **The live page was not
opened in a browser after this push** (paused before it): run `node live-check.mjs shots/p2-live` first thing.

## HANDOFF 3 (written 6:20 PM MSI clock, 11/19, by Fable 5.2, third session; paused by the orchestrator at 83% of the shared session)

This replaces HANDOFF 2 as the place to start. Its gotchas still hold.

**State.** Live on main from this session: `e964e9e0` (the first take-off, a controller plays the opening, night ground, the ship's landing lamp) and
`3ee80594` (Mars and its moons lived-in, first half). Worktree `C:\Users\lilli\Projects\ho-fable-cosmos`, branch `fable/cosmos-look-2026-11-19`.
**One local commit is NOT pushed: `00babd1b`.** It holds two helper agents' finished work that I have not looked at or tested myself:
- `src/worlds/ceres/activity.js` (+ hook in `ceres/client.js`): Ironclad and Greenhaven visibly at work at Occator Works (their own people, an ore hauler
  and a water tender on a shared timetable, a stockpile and tank gauges that move, a balance board). Agent's pictures: `shots/p4-ceres-*` (42).
- `src/port/desert.js` (+ hook in `portSystem.js`): the desert north of Marineris Port (haul road, borrow area, solar field, ice well with a pipeline, a mast,
  the first landing site, workers). Pictures: `shots/p2-desert-*`, start with `p2-desert-sheet-day.png` and `-night.png`.
- `src/port/trafficFx.js` (+ hooks in `traffic.js`): engine rumble, touchdown thump and dust for the traffic ships, a whine for the tug.
All client-only. The agents report no page errors, first-hour 78/78 and port-checks passing with their work in. **Before pushing it:** look at the picture
sheets, run `test/first-hour-browser.mjs`, `test/first-flight-browser.mjs`, `test/phone-check.mjs`, `test/port-checks.mjs`, then push and check live.
Known gaps the agents named: Ceres activity ships are not hidden during the Ceres opening; nobody has heard the sound; no collision on the new solids;
far desert clusters can sit a little high or low until approached; the balance board's leader line was not seen with real data.
Untracked test pictures under `games/the-cosmos/docs/qa/` stay out of commits. No test server is running (4383 stopped; the agents stopped theirs).

**For the orchestrator.**
1. **Restart the game server on `3ee80594` or later.** Two server-shared changes are waiting: (a) `src/missions/catalog.js`: the three Moon Round jobs do not
   exist for live players until then (the supply clerk offers them; taking one answers "The paperwork for that one is not through yet"); (b)
   `server/authority.mjs`, the `ramp` action: off Mars an owner outside cannot work the ramp until then. Nothing breaks in the meantime.
2. A real phone, still: the first take-off by a real thumb, the sounds, a phone on its side, the home-screen icon.

**Where the production bar stands** (`docs/GAME-PLAN.md`, order changed for Jaron's 4:15 PM direction: lived-in Mars region, then jobs and missions as a
ladder, then factions that do things; the shell beside them).
- Part 1, the first hour: complete to the first landing on iPhone and Android profiles, with a controller through the opening. Open: a real phone, frame rate
  and memory measured, the Earth, Moon and Callisto starts, a big screen.
- Part 2, Mars and its moons: first half live. Open: a play-through in a browser as a stranger (`test/mars-region-browser.mjs` is still to be written: take
  "Stores for Stickney" from the clerk by taps, fly, walk to the airlock, read every beat), people on the moons who can talk and give jobs (needs a cast in
  `src/missions/where.js` `peopleIndex`, a shared file), a shop on Phobos, the desert (in the unpushed commit), sound (same), boulders, the square patch from orbit,
  suits off indoors, the Pad Status board saying "03 CLEAR" under a parked courier.
- Parts 3 and 4: nothing repeats yet (a freight board), no roles; factions act visibly only on Ceres, and only in the unpushed commit.

**Next three, in order.**
1. Review, test and push `00babd1b` (above). Then `node live-check.mjs` for both pushes.
2. Finish part 2: `test/mars-region-browser.mjs` (the Moon Round by taps on a phone profile, every beat pictured and read), then fix what it finds; give the
   people of Stickney East and the Deimos camp names, talk and one job each that starts there.
3. Part 3's first whole piece: a repeating freight board at every port (the catalog refuses a job once done: `server/missions.mjs` `accept`), with pay by
   distance, so there is always work.

**New gotchas.**
- The test authority (`tick:false`) does not move ships or send state by itself. `first-flight-browser.mjs` advances it inside `step()` and asks for a
  checkpoint so the page gets the new state; copy that for any test that flies in a shared world.
- Changing server state from a test while a pose is in flight gets rolled back by the next refused action. Do it as one action (see the `test-grant` trick).
- A `?dev=1` session without `sky=live` lights the ground of other worlds with a different Sun than the lamps and the night logic use. Review looks on moons
  with `&sky=live` (first-flight does; `SKY=day|night`).
- The start-up "empty picture" check counts drawn frames, so a manually stepped test stretches it over the whole run.
- Helper agents work well on client-only pieces in new files with a tight brief (they made the outposts, the traffic, the desert, Ceres); they run for 20 to
  40 minutes and block the lead while they do. Keep shared-file changes with the lead.
- Job pay must stay between 60 and 400 credits (`test/pkg-missions.mjs` checks it).

## Fourth session (9:12 PM to about 10:40 PM MSI clock, 11/19, Fable 5.2)

### Reviewed and pushed: Ceres's two sides at work, the Mars desert, traffic sound and dust (`f271d624`, was the unpushed `00babd1b`)

The helper agents' commit from the third session, now looked at and tested by the lead. Nothing had to be dropped.
- Read: the hooks in `portSystem.js`, `traffic.js` and `ceres/client.js`, all of `trafficFx.js`, the timetable and update path of `ceres/activity.js`.
  The Ceres ships fly during the Ceres opening too; left as it is on purpose (they land at their own stands, away from the pad and the wreck, and a
  works that is busy when you crawl out of the wreck reads right).
- Looked at: the desert day sheet, the Ceres yard, hauler, board and top-down pictures.
- Tests with the work in: `first-hour-browser` 78/78, `first-flight-browser` iPhone 35/35 and Android 42/42, `phone-check` all pass, `_port-only` 46/46.
- Live: build `895a983cd3baf9a3f5a3`, phone width, no errors, no sideways scroll; the desert is built on the live site (12 draw calls) and the sound
  object is there. Picture: `shots/live-p2b-live-desert-well.png`.
- Still true: nobody has HEARD the sound (headless tests only read the nodes); nothing in the desert is solid; the first-landing site is 1.3 km out.

### Part 3, first whole piece: the freight board (work that never runs out) + the moons answer back + every side has a run of its own

**What a player gets.** Ask anyone who hands out jobs "Is there paid work for me?" and under their story job there is now **The freight board**: runs that
are always there and pay every time, with your **freight ticket** on top (runs flown, your rank, the bonus). 25 runs on five worlds:
- Mars: Well samples (the supply clerk; a walk up the haul road to the ice well and back, 80), Read the mast (the weather desk, after her story job; out
  past the well to the far mast, 100), Keep the first landing (the Crew Hall clerk; the whole haul road, 1.3 km, to brush the plaque and sign the book, 120), Freight for Stickney (180, after the first story run),
  Freight for the Deimos camp (240), Long haul: Occator Works (a crossing to Ceres, 400).
- Phobos and Deimos (new): four of the suited figures now have names, a line, a question and freight. Nadia Ferro (yard hand) sends empties down to the
  port (180); Tomas Reyes (propellant tech) sends a flask to Deimos (200); Aoi Tanabe (geologist) sends survey plates back to Phobos (200); Zuri Achebe
  (driller) sends a rack of cores to the tower (240). Nobody flies home empty.
- The Moon: crates from Tranquility to Shackleton (150) and Daedalus (170), and a load back from each.
- Ceres: Long haul: Marineris Port (400). Earth: Fill for the sea wall (dig 300 kg, 90). Callisto: Long haul: Marineris Port (600, the longest run).
- Every side of every two-sided world has a run of its own, open after that side's oath job, that feeds its home every time (half the oath job's weight):
  Ironclad ore, Greenhaven salt, Fortis rations, Technos Prime chip trays, Skyward's line check, the Homeguard wall, Mystara ice, the Unbound's drill charges.
- The ticket: New hand, Hauler at 3 runs (+10% on freight), Senior hauler at 10 (+20%), Freight master at 25 (+30%). The story says so when the rank changes,
  the World / crew sheet shows the ticket, and other players see the rank on your name tag (`Name · Hauler`).
- The status card now prefers work from the people on the ground you stand on (on Phobos it names Nadia Ferro, not the supply clerk on Mars), and when
  every story on a world is told it points at the freight board instead of going quiet.

**How it is built.** `src/missions/freight.js` (new, pure data: the 25 jobs with `repeat: true`, the rank table, `freightPay`). `catalog.js` adds them to
`MISSIONS`; `open()` and `offeredBy()` know a repeating job stays open. `server/missions.mjs`: accept lets a repeating job be taken again; finish counts runs
in `missions[player].freight` and pays by the ticket. `talk.js`: the work view lists the story job then the board. `where.js`: a place in the desert round
the port (`{ port: [x, z] }`, on the ground there) and the four moon people. `src/worlds/phobos/cast.js` (new): who they are; `outpostKit.js` gives each
outpost a `people` object, so the Talk button finds them. `tracker.js`: the card and the sheet.

**Tests.** `test/freight-checks.mjs` 30/30 on the real authority with real flights (repeats, pay, the ticket, the story run unlocking freight, both crossings,
Ironclad's run moving Ceres's home, the Moon out and back, all four moon people). `test/freight-browser.mjs` 13/13 on an iPhone profile at 375 px with real
taps (the board, button sizes, taking the well run, the arrow, the pay, the run offered again, a second player seeing the rank appear on the name tag, then Phobos: talk to Nadia Ferro, her board, take her run).
`pkg-missions` 80/80, `moon-round-checks` 13/13, `pkg-roles` 97/97, `pkg-ceres` 171/171.
Pictures: `shots/fr-01-board-iphone.png`, `fr-03-at-the-well-iphone.png`, `fr-08-phobos-board-iphone.png`.

**Needs the game server restarted.** `server/missions.mjs` and the catalog changed. Until then the live site shows the board, and taking a run answers
"The paperwork for that one is not through yet" (the message already in place for a job newer than the server). Nothing breaks.

**Commits.** `f56d4f00` (the board, the moon people, the sides' runs), `57ba30ae` (the rank on the name tag), `41751ebf` (the mast and the first landing).
**Live.** After `f56d4f00`: build `38e3a1d8c0138e4e367d`, phone width, no errors, no sideways scroll; the live modules hold 23 freight jobs (8 of them the
sides' own), the board draws for the supply clerk, and the four moon people resolve by name (`live-freight.mjs`). After
`41751ebf`: build `6351aba088e64d25eef6`, the same checks clean, 25 freight jobs live. Pictures: `shots/live-p3b-live-plain.png`, `-live-freight.png`.
**Not done in a browser:** the board on a big screen (see HANDOFF 4), the moon people on Deimos (Phobos was played by taps), any run flown by taps from
take-off to delivery (the flights were flown on the real authority in `freight-checks.mjs`), a gamepad on the board.

## HANDOFF 4 (written about 10:40 PM MSI clock, 11/19, by Fable 5.2, fourth session; stopped early to leave the shared session room for the 3 AM news jobs)

This replaces HANDOFF 3 as the place to start. Its gotchas still hold.

**State.** Live on main from this session, all checked on the live site at phone width (no errors, no sideways scroll):
- `f271d624` Ceres's two sides at work, the Mars desert, traffic sound and dust (the helper agents' commit, reviewed and tested; nothing dropped).
- `f56d4f00` the freight board, the people of Phobos and Deimos who talk and send freight, a repeating run for every side.
- `57ba30ae` a freight rank shows on your name tag for other players.
- `41751ebf` the weather mast and the first landing site each get a paid run.
Worktree `C:\Users\lilli\Projects\ho-fable-cosmos`, branch `fable/cosmos-look-2026-11-19`, nothing unpushed. Untracked test pictures under
`games/the-cosmos/docs/qa/` stay out of commits. No test server is running.

**For the orchestrator.**
1. **Restart the game server on the newest main.** `server/missions.mjs` and the job catalog changed: the 25 freight runs, the freight ticket, the moon
   people as job givers and the rank on the name tag all wait for it. Until then the live site SHOWS the freight board, and taking a run answers "The
   paperwork for that one is not through yet". Nothing breaks, but it will read as broken to a player who tries twice.
2. A real phone, still: the first take-off by a real thumb, the sounds (nobody has heard the traffic rumble, thump or tug whine), a phone on its side,
   the home-screen icon.
3. Voices for the four moon people (Nadia Ferro, Tomas Reyes, Zuri Achebe, Aoi Tanabe): they talk in text only. Every other talking person has rendered
   voice clips (`tools/gen-voices.mjs`); that tool was not run this session.

**Where the production bar stands** (`docs/GAME-PLAN.md` is current).
- Part 2, Mars and its moons: most of it live. Open: voices on the moons, a shop on Phobos, solid things in the desert, boulders, the square patch from
  orbit, suits off indoors, a full stranger's play-through, a real phone.
- Part 3, jobs and missions: the first whole piece is live in the client (the freight board and the freight ticket). Open: the other roles (surveyor,
  digger, escort, trader), trade between worlds, fuel and repairs that cost (Jaron's open question), a bigger ship to save for.
- Part 4, factions: visible on Ceres only; every side of every two-sided world now has its own repeating run that feeds its home. Open: yards, people
  and ships for the sides of the Moon, Earth and Callisto (copy the shape of `src/worlds/ceres/activity.js`), patrols, a home that visibly grows.

**Next three, in order.**
1. Part 4 on the Moon: Fortis at Shackleton and Technos Prime at Daedalus visibly at work, built like `ceres/activity.js` (a helper agent did Ceres in
   about 35 minutes from a tight brief; client-only, new files). Then Earth and Callisto the same way.
2. Part 3's second piece: money that means something. A price for fuel and repairs is Jaron's open question (GAME-PLAN, bottom); what can be built
   without it is a bigger ship to save for with the price on a board at each port, and a second ticket (digger) counted from the digging runs.
3. Part 2's leftovers: solid props in the desert (the walker passes through the well and the lander), a shop on Phobos (Tomas Reyes sells propellant
   once fuel has a price), and `test/mars-region-browser.mjs` (the Moon Round by taps; `test/freight-browser.mjs` has the pieces to copy).

**New gotchas.**
- A test that teleports a player in a shared world must set the browser AND the server and wait until both hold (`put` and `off` in
  `test/freight-browser.mjs`). The older way (one set, one sleep) is why `test/missions-browser.mjs` is flaky on this machine: on untouched main
  (`3ee80594`) it failed at its Earth leg, on this branch it failed at its first Talk on two runs and went through Mars on a third.
- `test/missions-browser.mjs` writes into TRACKED pictures (`docs/qa/missions/*.png`). Run it with `MISSION_SHOTS=<scratch folder>` or restore them
  afterwards (`git checkout -- games/the-cosmos/docs/qa/missions`), or the next rebase stops.
- The desktop pass of `test/freight-browser.mjs` is opt-in (`ONLY=all`) and does not pass: in the software-drawn headless Chromium the walker ends 4 to
  5 m from where the test puts it and the Talk prompt never shows. So the freight board has NOT been looked at on a big screen. The panel is the same
  Talk panel every job uses.
- A person who talks during the opening (the arrival guide) should not be given a day-one freight job: the Talk panel would offer paid work in the
  middle of the opening. The first-landing run was moved to the Crew Hall clerk for that reason.
- `pkg-missions` holds the story gates: the weather officer must have nothing for a new pilot until the shift notes are done. A freight job for a
  story giver needs that giver's story job in `needs`.
- Freight pay is checked at 60 to 400 credits, 600 for a crossing between worlds (`pkg-missions`). The ticket bonus is on top.
- Do not edit source files while a browser test is running: the test server serves the files as they are on disk, and a page that loads between two
  edits gets half of each.
- Quoting: a Python heredoc inside Git Bash eats backslashes before quotes. Put edit scripts in a file in the scratchpad and run the file.

## Fifth session (about 6:50 AM to 8:15 AM MSI clock, 11/20, Fable 5.2)

### Part 4, second piece: the Moon's two sides at work, and one kit for every side's yard

**What a player gets.**
- **Shackleton (Fortis): Supply Stand 6**, inside the wall south of the apron, between the ice dock's weigh bay and the motor pool. A ration lighter in
  Fortis gunmetal ("Ration Six", FT-0006) flies in over the south wall, hovers, lands on a numbered slab with a red edge, and drops her ramp. While she
  is down the stack of ration and ammunition crates on the three pallets grows from 3 to 12; the base eats it down again before the next one. Round it:
  sintered-block barriers, red lamps, a three-walled store with shelves ("RATION STORE 6"), an ammunition stack, drums, cold white work lamps, signs in
  Fortis lettering ("SUPPLY STAND 6 · RATIONS IN", "COUNT IT IN. COUNT IT AGAIN."), a hand pushing a pallet truck between the ramp and the store, a
  guard walking the stand's edge, a tally hand at the stack (a fourth on a desktop).
- **Daedalus (Technos Prime): the tray dock**, on a low white deck in front of Fab Floor 2. Sealed cases of chips pile up on a plinth (ten of them) as
  the fab prints them; a white courier ("Quiet Carrier", TP-0002) lands on the dock and her stay empties the plinth. Blue light-lines round the dock and
  the deck, a smooth white arch from the fab door, a seal reader, signs in Technos lower case ("bay-2 / tray dock · outbound", "fab floor 2 · sealed
  trays only", "signal over noise."), a hand with a trolley, a dock hand, a seal checker (a fourth on a desktop).
- **At both: a lit board**, "THE MOON · THE TWO SIDES", with each side's emblem, what it is for, its leader and which way it leans, and the two meters
  of the Moon's home (between the two; the home's strength). "No report" in a solo world.
- **A home that shows its strength (first sign).** In a shared world the yard's stack is as tall as the home is strong: at strength 100 the stack fills
  to the top, at 0 it only ever reaches half. The side's own freight run (Rations for the gate, Trays for the dishes) raises that number.
- A ship a visit every 12 minutes, on the world clock, so every player there sees the same landing; she is waved off if a player's ship is on her stand.
  Real Moon gravity: she brakes nose-up at atan(0.8 / 1.62) = 26 degrees and lifts off at a third of a metre per second squared.

**How it is built.** `src/worlds/_kit/sideYard.js` (new): the machinery of Ceres's hand-made `activity.js`, made reusable. `makeTimetable(cfg)` is pure
(visits, poses, stock level); `SideYard` builds the place once when the camera is within 6 km, borrows the settlement's own materials, draws signs
through the Moon's `SignAtlas`, flies one ship per side with the port's `poseShip`, walks hands on `beatPose` / `pushPose`, and draws the board. A world
hands it a config: gravity, slot length, per side a stand, flight numbers, a stock (`take` or `bring`, how many pieces, how to draw piece j), the hands,
a `build(h)` that draws the props, a board, and an optional `origin` (x, z to move the whole yard; y to lift it onto a deck).
`src/worlds/moon/yards.js` (new) holds the two configs; `moon/clientCommon.js` builds and ticks the yard. Ceres keeps its own file untouched.
Client only. **No game server restart needed.**

**Two things found on the way.**
- The first place picked for Fortis's stand was already taken by the ice dock's weigh bay and its ice heaps (they are drawn, but they are not in
  `layout.js` BOXES, so reading the layout did not show them). The yard moved 20 m east with `origin`. Look at a picture before trusting the layout.
- At Daedalus the drawn ground stands a little above the pad's plane away from the pad (the station's own plazas are half buried by it: an older fault,
  not fixed here), while `surfaceRadius` says it is level. The dock therefore stands on a 0.3 m deck. The station's buried plazas are still open.

**Tests.** `test/yards-browser.mjs` (new) 19/19 on an iPhone profile at 375 px, solo: at each site the yard builds, the ground is level, the ship is
seen braking, then down with the ramp open, the hands are out, the board is drawn, the stock moves the right way over her stay (Fortis 4 to 12, Technos
9 to 0), the stand is empty between visits, no sideways scroll, no page errors. Built in 30 to 60 ms; the ship in 3 to 5 ms (the exterior was cached).
Pictures (not committed): the scratch folder of the session; retake with `YARD_SHOTS=<folder> node test/yards-browser.mjs`.
`phone-check` passes with the work in. `pkg-moon` printed nothing inside 100 seconds on this machine and was not waited for (the change is client-only).

**Commit.** `425f57c6`. **Live:** build `f7b51cbd6f6697afc636`, 390 px wide, no errors, no sideways scroll, plain page and solo session; on the live
site the Shackleton yard builds, FT-0006 stands landed with her ramp down, 8 crates on the pallets, the board drawn (`live-yards.mjs`; picture
`shots/live-p4-live-yard-shackleton.png`). Daedalus was not looked at on the live site (same code, tested locally).

## HANDOFF 5 (written about 8:15 AM MSI clock, 11/20, by Fable 5.2, fifth session; stopped at the 80 minute mark)

This replaces HANDOFF 4 as the place to start. Its gotchas still hold.

**State.** Live on main from this session: `425f57c6` (the Moon's two sides at work + the shared yard kit). Worktree
`C:\Users\lilli\Projects\ho-fable-cosmos`, branch `fable/cosmos-look-2026-11-19`, nothing unpushed. Untracked test pictures under
`games/the-cosmos/docs/qa/` stay out of commits. No test server is running.

**For the orchestrator.**
1. **No game server restart is needed for this session's work** (client only). The freight board went live with the 10:35 PM restart on `41751ebf`;
   nobody has yet taken a freight run on the live server by taps (see "next three", 2).
2. A real phone, still: the first take-off by a real thumb, the sounds, a phone on its side, the home-screen icon. New for the list: stand at
   Shackleton or Daedalus (Course, then walk south from the pad) and watch a ship come in; say if it stutters.
3. Voices for the four moon people: still text only (`tools/gen-voices.mjs` not run).

**Where the production bar stands** (`docs/GAME-PLAN.md` is current; part 4 now has its own row in the bar table).
- Part 4, factions: four of eight sides are seen at work (Ironclad, Greenhaven, Fortis, Technos Prime), each with a yard, people, a ship and a board;
  a strong home stacks its yard higher. Open: Earth (Skyward, Homeguard) and Callisto (Mystara, the Unbound), sound for the yard ships, patrols, a home
  that changes more than its stack, switching, licenses, seats and votes, the season.
- Parts 2 and 3: as HANDOFF 4 left them.

**Next three, in order.**
1. Part 4 on Earth and Callisto with the kit: write `src/worlds/earth/yards.js` and `src/worlds/callisto/yards.js` like `moon/yards.js` (two sides in one
   config each, so the ships take turns; Earth g 9.81 wants a steeper, faster approach and a short hover; Callisto g 1.236), hook them in
   `earth/client.js` (parent `complex.root`) and `callisto/client.js` (parent `camp.root`, check the name in `camp.js`), add both to SITES in
   `test/yards-browser.mjs`. LOOK AT A PICTURE of the chosen ground first (see the gotchas). Then wire `port/trafficFx.js` to the yard ships for sound.
2. Take a freight run on the live server by taps (the server is on `41751ebf`): `test/freight-browser.mjs` has the pieces; point one at the live site
   with a throwaway player, or play it by hand in the browser pane, and log what the pay line and the ticket say.
3. Part 3's second piece (money that means something) or part 2's leftovers, as HANDOFF 4 lists them.

**New gotchas.**
- `layout.js` BOXES do not list everything that is drawn (Shackleton's weigh bay, ice heaps, vehicles' signs). Take a top-down picture of the ground
  you mean to build on before placing anything (`__cam(x, 60, z, x2, 0, z2)` in `test/yards-browser.mjs`).
- `body.surfaceRadius` can say "level" where the drawn ground is not (Daedalus, 40 m and more from the pad). If a slab comes out half buried, lift the
  yard with `origin.y` and stand it on a deck (`h.slab(x0, z0, x1, z1, col, 0)`).
- A ship's bearing in the kit: `bear` is where she comes FROM (0 = from the south, 90 = from the east), `out` is the heading she leaves ON
  (0 = she leaves northward). She lands nose north unless the stand has `yaw`; the courier's ramp is at her stern, so cargo comes out on the south side.
- A dev session without `sky=` has a fixed mid-morning Sun (good for pictures); `SKY=live` in `yards-browser.mjs` gives the real one (Daedalus was in
  night on 11/20: the lamp pools and light-lines show then).
- Yard material keys: stay with the ones `SideYard.materials()` lists (concrete, steelDark, steel, metal, paint, white, hazard, rubber, plasticDark,
  glow, glowWhite, glowAmber, glowRed, glowBlue, glowGreen, glowCool); a key the settlement never used is not there to borrow.

## Sixth session (8:49 AM onward, MSI clock, 11/21, Fable 5.2)

Rebased on main first (2 commits behind: news and Seam Room, nothing of ours). Order kept as HANDOFF 5 set it: part 4 on Earth and Callisto with
sound, then the live freight run. One thing jumped the queue inside part 4 because it was in the way: the Prospectors' Camp stood in the wrong place.

### Part 4, third piece: Earth's and Callisto's sides at work, yard ships you can hear, the Prospectors' Camp on its own ground (`32dd6b55`)

**What a player sees.** All eight home sides now work where you can watch.
- **Earth, Skyward: Payload Stand 2**, on the grass south-west of the landing pad. A white courier (SW-0002 "Upbound Two") comes in from the
  south-west on a hard, short braking burn (Earth's pull), lands on a slab edged in range orange, and the rack of payload canisters fills (3 to 8);
  the mount uses them up before the next. A lattice gantry with an orange arm, a prep shelter, a windsock (Earth has wind), hands in orange.
- **Earth, Homeguard: Sea Wall Depot 1**, south-east. Blocks for the sea wall are cast and stacked (12), a harbour-navy courier ("Tide Table")
  carries them out toward the coast. A brick site hut with a brass lamp, a sandbag line, one finished panel of wall with THE WALL HOLDS on it.
  The sign says SEA WALL DEPOT 1 · ON LOAN FROM SKYWARD, so Pruitt's "we have nothing built yet, I am standing in someone else's yard" stays true.
- **Callisto, Mystara: the Relay Stand**, on the ice east of the camp behind the quartermaster's shed. A violet courier (MY-0009 "Ninth Band")
  brings spares for the relays the storms took; the row of coil drums grows (2 to 9). Violet basalt, old-gold inlay, lit glyph lines (the camp's own
  violet glyph material), standing stones at the corners, a measuring house, a relay mast half put together on trestles.
- **Callisto, the Unbound: the freight pad at the Prospectors' Camp**, 1.2 km north. Salvaged deck plates that do not match, an orange cross brushed
  on by hand, core boxes stacked on skids (9 to 0 over the ship's stay), a tarp awning on four poles that are not the same height, a courier in red
  primer (UB-0004 "Number Four"). Signs: CLAIM FREIGHT · WEIGH IT YOURSELF, and SELF-SERVICE. ALL OF IT.
- A lit board at each place names the world's two sides and how they stand ("no report" in a solo world).
- **Sound, true to the place** (HANDOFF 5's "then yard-ship sound through port/trafficFx.js"). `trafficFx.js` now takes a medium:
  `mars` (the port's thin air, numbers unchanged), `earth` (a full atmosphere: louder, brighter, heard to 4.5 km), `ground` (no air: nothing crosses
  the vacuum, so you get only what the exhaust drums into the ground under 45 m and the ground carries to your boots: a 34 to 84 Hz shake within
  320 m, and the touchdown thump). Every yard ship uses it: Earth through the air; the Moon, Callisto and Ceres through the ground. One set of voices
  for all yards on the page (a phone has few to spare); the yard whose ship is flying owns it. No dust on the yards (they are swept slabs).

**The Prospectors' Camp was in the wrong place (found by looking at the picture).** The Unbound's ship came out half sunk in rough ground and the
camp's own slab could not be seen at all. Cause: `camp.js` asked for the port's frame with `body.playerPad(portOff.x, portOff.z)`; `playerPad` takes
(east, NORTH) and outpost z runs SOUTH, so the whole camp (huts, rig, claim board, buggy) was drawn 1.2 km SOUTH of the Valhalla pad, 2,436 m from
its own levelled port, on ungraded ground, half buried. Bram the prospector was placed by a different path and stood alone at the right spot, so a
player who followed the mission arrow north found one man on an empty flat. One sign fixed; the camp now stands round him on its level ground
(measured: 1 m from the port's point on the live build). Its slab was also exactly level with the ground and flickered once visible: it stands 4 cm
proud now. Nobody had seen this because the camp test only checked that two roots existed.

**How it is built.** `src/worlds/earth/yards.js` and `src/worlds/callisto/yards.js` (new, configs only). Kit additions in `_kit/sideYard.js`:
`o.pi` (a yard at one of the world's other ports, in that port's own frame), `turns` / `turn0` (two yards that stand apart share one rota, so one ship
is alive at a time across both), `o.clock` (they share one dev clock too), `cfg.medium`, `h.has(key)` (may I borrow this material), and
`yardVoice` / `yardHush` / `yardSoundStatus` (exported; `ceres/activity.js` calls them for its two ships). `test/look.mjs` (new): the picture-first
tool (top-down shots, ground heights at points, any page expression). Client only. **No game server restart needed.**

**Tests.** `test/yards-browser.mjs` 76/76 on an iPhone profile at 375 px, solo, six yards: built, level ground (worst 0 m), ship in, **high up she is
silent on airless worlds and heard on Earth**, low over the stand she is felt (0.07 to 0.09 through the ground at 65 to 85 m; 0.22 through Earth's
air), down with the ramp open, hands out, board drawn, stock moves the right way, stand empty and **yard quiet** after she leaves, no sideways scroll;
plus Ceres's ore hauler silent high, felt low (0.03 at 147 m), quiet when gone. Yards build in 30 to 56 ms. Earth under the real Sun (`SKY=live`):
daylight, no lamp pools. `phone-check` passes (iPhone and Galaxy profiles). `pkg-callisto` 30/30, `worlds-checks` clean.
Three stale checks repaired (all older than this session, none about this work): `pkg-callisto` counted the freight board's repeating runs as story
jobs; `leftovers-checks` wanted exactly 15 port people (a phone now also gets 3 walkers); `economy-checks` took the key named inside a
`hintFor({ keys, touch, pad })` hint for a bare key prompt. The full validator was started and stopped after 948 passes with only those two failures
(it takes 45 minutes and rewrites tracked pictures; they were restored).
Pictures: `shots/p4b-earth-ground-before.png` (the ground before), `p4b-earth-skyward.png`, `p4b-earth-skyward-on-foot.png`, `p4b-earth-homeguard.png`,
`p4b-callisto-unbound.png`, `p4b-prospectors-camp-fixed.png`.

**Live.** Build `401acefe8c37bbe78b32`, 390 px, plain page and solo session: no errors, no sideways scroll. On the live build: the Unbound's ship
lands at the Prospectors' Camp (camp 1 m from its port), Mystara's at the Relay Stand, Skyward's at Payload Stand 2 with sound 0.21 through the air
(`live-yards2.mjs`; pictures `shots/live-p4b-live-yard-*.png`).

**Seen and not fixed (for a later session).**
- **Jupiter bobs in Callisto's sky.** `callisto-browser` fails one check today: Jupiter stands 7 degrees up at Valhalla where a locked moon would hold
  it near 32. Cause (frames.js `yawOf`): a world's frame only turns about the FIXED axes' +Y (Mars's pole), so Callisto's spin axis is Mars's, not
  its own orbit's, and Jupiter rides up and down over each 16.7-day orbit. Same rule for the Moon (Earth in its sky). Deep in the frame code; not a
  quick fix. Until then that check passes or fails with the date.
- **Earth's blue sky stays up on a world you JUMP to** (the dev `debugStand`, not a flight): the yard test now visits Earth last. Not checked whether
  a real crossing away from Earth clears it by itself (it should, the globe fades with height); worth one look.
- Earth carries both sides on one ground: about twice a single yard's draw calls (120 visible meshes with four people). Not measured on a phone.

### A real freight run on the LIVE server (HANDOFF 5's second item; plan line pushed as `86777d4e`)

A throwaway visitor on the live shared world (heartbeatobservatory.com/games/the-cosmos, game server on `41751ebf`, client build
`401acefe8c37bbe78b32`), iPhone-profile WebKit at 390 px. Tools: `live-run.mjs` (the driver) and `live-run-freight.mjs` (the steps), both in this
folder. What the live screens said, word for word:

1. **Talk · Supply clerk** (a tap): "Supply desk. Raw regolith: 12 marks a tonne. We weigh it here." with "Is there paid work for me?" on the list.
2. **The board** (a tap on that line): the story job first ("Stores for Stickney · 220 credits · a port job"), then
   "The freight board · work that is always here, paid every run / Your freight ticket: New hand · 0 runs · Hauler at 3 /
   Well samples · 80 credits / Walk the haul road north to the ice well, collect the day's water samples, and bring them back to the supply desk."
3. **Taking it** (a tap on "Well samples"): "Well samples. Walk the haul road north from the port to the ice well (the tall tower) and take the sample
   rack." The card on top says "NEXT Well samples: ..." and the line under the purse says "North-east gate, then the road. The samples are in the grey
   rack at the foot of the tower." The server had the job as active, step 0.
4. **At the well** (inside 14 m of it): the step moved to 1 by itself, carrying "a rack of water samples". The line: "Six tubes, cold enough to fog.
   The top one has a date and "still clean" written on it." The card: "NEXT Well samples: Carry the samples back to the supply desk (west of the pads).
   You are carrying a rack of water samples."
5. **Back at the desk: THE PAY LINE: "Well samples: 80 credits paid."** The purse went from "10,000 marks · 2,500 cr" to "10,320 marks · 2,580 cr"
   (80 credits = 320 marks). The server: no active job, `freight: { runs: 1, credits: 80 }`.
6. **The board again** (two taps): **THE TICKET: "Your freight ticket: New hand · 1 run · Hauler at 3"**, and "Well samples · 80 credits" is offered
   again. No page errors in the whole run. Pictures: `shots/live-run-fr4-01-well.png`, `-02-paid.png`, `-03-board-again.png` (and `live-run-fr-02-board.png`).

**So the freight board works on the live server end to end: asked, taken, stepped, paid, counted, offered again.**

**What was a player and what was not.** Every choice was a real tap on the real buttons. The ground was NOT walked by a thumb: the test first held the
walk key for real (205 m from its pad to the clerk in 170 s, the live server following every step), but a walker with no eyes could not find its way
from the supply desk round the port's buildings to the north-east gate (15 minutes, 33 tries, ended 86 m from where it started). So the road was
covered by `H.hopTo`: 4 m straight hops every half second (8 m/s, inside the 12 m/s the server allows a person, so it never pulled the pose back).
That goes through walls. The server-side run is real; "a stranger finds the gate from the desk" is NOT shown by this.

**Found on the way.**
- **Two throwaway visitors are left on the live world**, both named "Visitor 840": `baa47f7a-0352-48c9-968f-04298a094e9a` (holds an unfinished
  "Well samples" job, 10,000 marks) and `15ca6770-48d2-4cf5-bc5e-2db66ebd3116` (1 freight run, 10,320 marks). Harmless; the orchestrator may remove them.
- Two different visitors got the same name, "Visitor 840". Not looked into (it may be made from something both sessions share).
- On a phone the NEXT card is tall when the next step is a long sentence: after the pay it covered the top 38% of the screen ("Lifeboat ready. Next:
  hire a crew. Walk to the Crew Hall ..."). Worth a three-line clamp with a tap for the rest.
- After a freight run is paid, the NEXT card falls back to the opening's last advice (hire a crew). It could say that the freight board has more.
- With the run key held, the walker covered about 1.2 m/s in the headless test browser (the game says 4.4 m/s running). A slow test machine, most
  likely (movement is per frame), but nobody has timed a walk on a real phone: the 600 m to the well would be a long thumb-hold if it is that slow.

## HANDOFF 6 (written about 10:05 AM MSI clock, 11/21, by Fable 5.2, sixth session; stopped early because the session's context had grown long)

This replaces HANDOFF 5 as the place to start. Its gotchas still hold.

**State.** Live on main from this session: `32dd6b55` (Earth's and Callisto's sides at work, yard-ship sound, the Prospectors' Camp moved to its
port) and `86777d4e` (game plan only). Worktree `C:\Users\lilli\Projects\ho-fable-cosmos`, branch `fable/cosmos-look-2026-11-19`, nothing unpushed.
The untracked picture folders under `games/the-cosmos/docs/qa/` (11/19, 11/20) are still there and still out of commits. No test server or browser
of mine is running.

**For the orchestrator.**
1. **No game server restart is needed** (everything this session is client only). The server is still on `41751ebf`, health ok at 10:00 AM.
2. Two throwaway "Visitor 840" players are on the live world from the freight test (ids above). Remove them if you like.
3. A real phone, still: the first take-off by a thumb, the sounds (new: stand at a yard on the Moon or Callisto and FEEL a ship land: a low shake,
   no roar; on Earth a roar), a phone on its side, the home-screen icon, and how long the walk to the ice well really takes.
4. Voices for the four moon people: still text only (`tools/gen-voices.mjs` not run).

**Where the production bar stands** (`docs/GAME-PLAN.md` is current).
- Part 4, factions: **all eight home sides are seen at work** and their ships are heard. Sound moved from "no" to "part" (tested gains; no real phone).
  Open: nobody is told to go and look (a job or a line that sends you to a yard), patrols, a home that changes more than its stack, switching,
  licenses, seats and votes, the season, the two station sides (part 7).
- Part 3, jobs: the freight board is proven on the live server. Open: the other roles, trade between worlds, fuel and repairs that cost (waits on
  Jaron's prices: open question in the plan), a goal to save for.
- Parts 1, 2, 5: as HANDOFF 4 and 5 left them.

**Next three, in order.**
1. **Give the yards a reason** (part 4, "stranger understands"): one line from each home's dispatcher that names the two yards, and a small paid
   errand on each freight board that ends AT a yard (count the stack and report, or carry one crate to the stand while the ship is down:
   `yard.status().stocks` and the timetable are pure functions of the clock, so the server can know the same numbers through `makeTimetable`).
   That makes the yards part of the work, not scenery.
2. **Phone comfort on the way to work** (parts 1 and 3): clamp the NEXT card to three lines with a tap for the rest; after a paid freight run let it
   point at the board again; time the walk to the well on a real-speed browser (or shorten the first run) so the first paid job is not a
   five-minute thumb-hold.
3. **Jupiter and Earth held still in a locked moon's sky** (`space/frames.js` `yawOf`: a frame turns only about Mars's pole, so Jupiter bobs about
   25 degrees over each Callisto orbit; today it sits 7 degrees up at Valhalla instead of about 32). It needs a tilt in the frame, not only a yaw:
   read `worldKin` and everything that uses `yaw` before touching it. Then `callisto-browser` passes on every date.
   After these: part 3's money piece once Jaron has answered the price question, or part 2's leftovers as HANDOFF 4 lists them.

**New gotchas.**
- `body.playerPad(east, NORTH)`: outpost z runs SOUTH. Pass `-z`. (This one sign had the whole Prospectors' Camp 2.4 km from its port for weeks.)
- A place at a world's second port gets its own frame: `new SideYard({ pi: camp.portPi, parent: camp.portRoot, ... })`; its people come out only when
  the player is within 320 m of THAT frame's origin; two yards of one world share a rota with `turns` / `turn0` and one `clock` object.
- A ship's hold (`sides[i].hold`) is drawn with the SHIP's materials, not the yard's: `paint`, `white`, `plasticDark`, `glowWhite` exist; `concrete` does not.
- Keep a stock piece to one material (one draw call each; a yard has 8 to 12 of them).
- The dev sky lies about night: without `sky=live` the picture is lit as day while the yard's own clock may say night, so lamp pools show at "noon".
  Judge lamps with `SKY=live`.
- `test/yards-browser.mjs` jumps between worlds without flying; Earth's sky stays up on the next world, so Earth is visited last. Pictures of other
  worlds taken after an Earth jump are wrong, not the game.
- Python heredocs eat `\b` (it became a backspace byte in a regular expression): write regex edits from a file, and check with `grep -c $'\x08'`.
- `node test/validate.mjs` rewrites tracked pictures under `docs/qa/` even when stopped early: `git checkout -- games/the-cosmos/docs/qa` after.
- A blind walker cannot cross Marineris Port (walls, halls, parked ships): for live tests use `live-run.mjs` `H.hopTo`, and say that you did.
- The live player's identity is kept in the browser's storage; `live-run.mjs` saves it to a state file only when a run ENDS (a killed run starts a
  new visitor).

## Seventh session (8:34 AM onward, MSI clock, 11/23, Fable 5.2; Jaron: "Lets push for the stars")

Rebased on main first (10 commits behind: news, the printer, the share card; nothing of ours). Order kept as HANDOFF 6 set it: give the yards a reason,
then phone comfort on the way to work.

### Part 4, fourth piece: the yards are part of the work (tally runs), and the server knows what stands on every stand

**What a player gets.** Every freight board that stands beside a side's yard has a new cheapest run, a **tally**: walk to the yard, count what is
really standing there, set the number on a small card and sign it. Eight of them, one for each home side:
- The Moon: **Count the stand** (Quartermaster Ostrander at Shackleton: the crates on the three pallets of Fortis's Supply Stand 6, 60) and **Count the
  trays** (Supply Clerk Stroud at Daedalus: the sealed cases on Technos Prime's plinth, 60).
- Earth: **Count the canisters** (Skyward's rack at Payload Stand 2, 70) and **Count the wall blocks** (the Homeguard's Sea Wall Depot 1, 70), both from
  Quintero at Range dispatch, who says she trusts neither side's own count.
- Callisto: **Count the coils** (Farah Adeyemi at the camp desk: the drums at Mystara's Relay Stand, 60) and **Count the core boxes** (Bram Okonkwo at the
  Prospectors' Camp: the Unbound's stack by the awning, 60).
- Ceres: **Read the tanks** (the lit gauge on Greenhaven's four tanks: a quarter, half, three quarters, full; 60) and **Count the bunker** (how many of
  Ironclad's three bays have ore in them, 70), both from the flight office.
- The keeper's first line names both of the world's yards (the tally is the cheapest run, so its pitch is the one the board opens with).
- At the yard a **count card** comes up: what the tally hand asks ("How many crates stand on the three pallets?"), a minus, the number in words
  ("7 crates", "half full"), a plus, "Sign the tally", and a line about the side's ship ("Ration Six is due in about 4 minutes" / "is down on the stand
  with her ramp open"). Three buttons, 52 px tall. On a phone it sits under the status card and the NEXT text steps aside, so the stack is in view.
- The number has to be what is really there. One out is near enough (the stack moves while a ship is down; the hand says what he made it). A wrong
  count is not paid: "7 wall blocks? Not by my count. Look again.", and the hand keeps the sheet for 15 seconds, so trying every number does not work.
- Signed right: paid at once (it counts on the freight ticket like any freight), and the hand's line says the count and where the ship is.

**How it is built.**
- `src/worlds/_kit/yardClock.js` (new): `makeTimetable`, moved out of `sideYard.js` unchanged. Pure, no three.js: the server can load it.
- `src/worlds/ceres/timetable.js` (new): Occator Works' hand-made timetable (visits, poses, `oreLevelAt`, `waterLevelAt`), moved out of `activity.js`
  unchanged. `activity.js` imports it back and still exports every name it did.
- `src/worlds/yardBook.js` (new, pure): `YARD_TT` (the timetable and stock numbers of the six kit yards; `moon/yards.js`, `earth/yards.js` and
  `callisto/yards.js` now take their numbers from here, so the picture and the count cannot drift), `TALLIES` (per side: where the stock stands, what
  is asked, the largest answer, the landing stand), `tallyTruth`, `tallyCheck`, `tallyWords`, `yardShipAt`, `yardShipWords`.
- `server/missions.mjs`: step kind `count` (a seventh kind; it waits like `choose`), action `mission-count { n }` (routed in `authority.mjs`), `count()`
  (on the job, on foot, within reach of the stock; the truth from `worldTimeAt(auth.now())` and the home's strength; right moves the job on; wrong
  returns `{ ok: true, wrong: true, hand }` and notes the time, because a thrown error would roll the wait back too), `standBlocked()`.
- A weak home stacks lower (`stackShare`: strength 0 = half, 100 = full), exactly as the yard draws it; a new shared world starts at strength 20.
- A ship parked on a side's stand waves that side's ship off, and then the stock does not move. The browser always knew; the server now looks
  (`standBlocked`: a landed ship within the stand's clear circle) and only then also takes the "nothing was carried" count. So "full" is never a free answer.
- `src/missions/freight.js`: the eight runs (`COUNT(key, text, beat)` builds the step from the book; `{n}` and `{ship}` in a beat are filled by the server).
- `src/missions/tallyUI.js` (new): the card. `tracker.js`: the arrow points at the stock for a `count` step. `main.js`: wiring, `cosmos.tallyUI`.

**Tests.**
- `test/tally-checks.mjs` (new) 72/72 on the real authority: the book against each yard's own timetable at 3,900 moments; all eight runs played
  (on the board with its pay, not countable from the desk, standing there is not enough, a wrong count, the wait, the true count paid, offered again);
  one out; the ticket; refusals; "full" refused with the stand clear and taken with a ship parked on it; the server seeing a parked ship.
- `test/tally-browser.mjs` (new) on an iPhone profile at 375 px in a shared world on Earth, by real taps: the board, taking the run, the card and its
  button sizes, the count read off the yard THE PAGE DREW and signed (the server, which never saw the page, pays), a wrong count, the right one after the
  wait, and the page's count against the book's at 24 moments of the timetable with this world's own home strength.
- Kept passing: `pkg-missions` 80/80 (it now knows seven step kinds), `freight-checks` 30/30, `moon-round-checks` 13/13, `pkg-roles` 97/97,
  `yards-browser` 76/76 (the six kit yards after the move of the timetable; the page logs "useProgram: program not valid" in headless WebKit, not looked into).

### Phone comfort on the way to work (HANDOFF 6's second item)

**What a player gets.**
- **The NEXT step folds to three lines.** The status card's first block could run to six or seven lines and cover the top third of a phone. It now
  shows three with "Tap to read all of it" under it; a tap unfolds it ("Tap to fold it"), a second tap folds it. A step that fits is left alone.
  It no longer flickers: it used to be rebuilt five times a second with the readings under it (which also made it impossible to tap); it is now its
  own element (`#hud-next`) that changes only when its words do.
- **While the count card is up, the NEXT step steps aside.** The card says what to do; the screen is for looking at the stack.
- **Paid, and back to the board.** For three minutes after a freight run pays, the card says "Paid 70 credits: Count the canisters. Marisol Quintero
  has that run again, and more on the freight board..." instead of jumping to whatever was next on the list (on Mars that was "hire a crew").
- **Keep walking.** The well run is 800 m each way from the supply desk (measured: `where.js`, straight line): 14 minutes there and back at a walk,
  6 at a full run, all of it with a thumb held hard over. Once the stick has been in its run zone for two seconds a button appears on top of the left
  dock: "Keep walking". Tap it with the other thumb and the walker runs on the way the view faces; steer by dragging the view; the left thumb can let
  go. It reads "Stop" while it is on. It stops on a second tap, when a thumb comes back to the stick, when the job's arrow changes (you have arrived),
  when the walker has not moved for a second and a half ("Stopped: something is in the way."), when a panel opens and when you board. Touch only.
  The walks themselves were not shortened: they are the desert, and now they cost a tap.

**How it is built.** `src/ui/keepWalking.js` (new; `update()` once a frame, `apply(input)` on the stick's numbers before the ship and the walker see
them), docked by `phoneLayout.js` (`#btn-keepwalk`, last in the left column). `tracker.js`: `goalId` (what the arrow points at) and `afterPay()`;
`opening/repair.js` asks it before the crew line. `main.js`: `refreshHud()` and `#hud-next`; `index.html`: the fold.

**Tests.** `test/tally-browser.mjs` grew to cover all of it by real taps on the iPhone profile: the fold, the unfold, the fold again, the card
stepping aside, the paid line, the Keep walking button (appears after two seconds of running, thumb-sized, on the left; tapped, the walker covers
more than 6 m in 3 s with no thumb on the stick; tapped again, it stops; a thumb back on the stick takes over). `first-flight-browser` on both
phone profiles: no errors in the whole run (it reads the NEXT text all the way through). `pkg-ceres` 25/25 after the move of the Works' timetable.

### Shipped and checked live

- **Commits.** `6a863cfa` (the tally runs, the yard book, the count card, the NEXT fold, Keep walking, the paid line; pushed 9:24 AM) and `ecb13c53`
  (27 voice clips: `tools/gen-voices.mjs` now reports 795 lines, 795 voiced, 0 to generate; every clip decodes, 2 to 40 seconds; pushed 9:31 AM).
- **The live site** (build `5c00b16277b9541f2f28`, WebKit iPhone profile, 390 px, `live-check.mjs` with `live-tally.mjs`): the plain page loads with
  no errors and no sideways scroll; the live modules hold 33 freight runs (8 tallies) and the yard book; the yard the live page draws on Earth agrees
  with the book at 12 moments of the timetable (7/9, 8/10, 7/12 ... canisters/blocks); the Keep walking button comes up (107 by 48 px). One new clip
  fetched from the live site: 200, 51,597 bytes. Pictures: `shots/live-p7-live-plain.png`, `-live-keep-walking.png`.
- **The live game server.** The orchestrator (Opus, in the main chat) restarted it on the new commit within minutes of being asked (health build
  `5c00b16277b9541f2f28` at 9:28 AM, the same id as the site). `live-run.mjs` with `live-tally-probe.mjs`, a new throwaway "Visitor 621" at Marineris
  Port: a count with no job on is refused with "You are on no job." (the new action is wired), a Moon tally asked for on Mars with "That job is on the
  Moon." (the server knows the new jobs), a job that does not exist with "There is no such job." The world's revision did not move (2056558).
- **NOT done on the live server:** a tally taken, counted and paid. Every yard stands on a world other than Mars and a live visitor starts at Marineris
  Port, so it needs a real flight first (a crossing to Ceres by the long-range drive, or the Moon). The same run was played by real taps against a real
  server on this machine (`tally-browser.mjs`); what the live server has not shown is the pay itself.
- **Not run this session:** `first-hour-browser` (it reads the NEXT text; `first-flight-browser` does too and passed), `missions-browser`, the 45-minute
  `validate.mjs`, a big screen, a gamepad on the count card, a real phone.

### Found on the way (not this run's doing)

- **`test/phone-check.mjs` fails on this machine today, on a clean copy of main as well** (`Projects/ho-printer`, none of this run's changes: 18 pass,
  15 fail; this worktree: 18/15 and 19/13, the failing profile changing from run to run). Every failure is one thing: "Graphics problem: WebGL invalid
  operation - switching to safe mode" in the headless browser during the opening, on the heavy profiles (Galaxy at 1440 by 2960, iPhone 15 at 3x); the
  reload into safe mode then leaves the test without `window.cosmos`. It passed 33/33 on 11/19, 11/20 and 11/21. Since then: the Windows 26H2 update
  (11/22); and at the time the graphics card was 67% full (5,487 of 8,188 MiB, one python.exe, 0% busy). The 375 px, 2x tests all pass. The same
  boot, alone, passed four times in a probe. Mailed to the orchestrator; not chased.
- **`yards-browser` logs "WebGL: INVALID_OPERATION: useProgram: program not valid"** in headless WebKit while passing 76/76. Probably the same thing.
- **The arrow to a place at the Prospectors' Camp points under the ground.** `where.js` `toWorldPos` puts an outpost place on the pad's plane, and the
  camp's port stands 443 m above the Valhalla pad's plane. The bearing is right, the height is not (Bram's story steps have had this all along; the
  Unbound tally has it too). A place should be put on the real ground there (`surfaceRadius`).
- **The main site checkout was stuck in a half-applied autostash since 11/22 4:20 AM** (the folder the game server runs from). Found at the start,
  read-only; the orchestrator verified it and reset it at 8:40 AM (timeline).

## HANDOFF 7 (written about 9:35 AM MSI clock, 11/23, by Fable 5.2, seventh session; stopped at one hour because Fable's week stood at 82%)

This replaces HANDOFF 6 as the place to start. Its gotchas still hold.

**State.** Live on main from this session: `6a863cfa` and `ecb13c53`. Worktree `C:\Users\lilli\Projects\ho-fable-cosmos`, branch
`fable/cosmos-look-2026-11-19`, nothing unpushed (the branch itself is not on GitHub: main is where it goes). Untracked picture folders under
`games/the-cosmos/docs/qa/` (now also `phone-check/2026-11-23`) stay out of commits. No test server or browser of mine is running. The game server is
on the new commit. One more throwaway visitor is on the live world ("Visitor 621"; its storage state was in this session's scratch folder only).

**For the orchestrator.**
1. Nothing is waiting on you: the restart is done. If "Visitor 621" and the two "Visitor 840" are still on the live world, remove them if you like.
2. `phone-check` and the graphics card (above): worth one look next to open-list 0a.
3. A real phone, still: the first take-off by a thumb, the sounds, a phone on its side, the home-screen icon. New for the list: a tally run (fly to
   the Moon or Ceres, ask the freight keeper, "Count the stand"), whether the stack can really be counted by eye on a small screen, and Keep walking
   on the haul road (does the button come up when it should; is steering by the view comfortable).
4. Voices: the freight keepers speak now. The four moon people still have no voice in the cast (they need one picked, then `tools/gen-voices.mjs`).

**Where the production bar stands** (`docs/GAME-PLAN.md` is current).
- Part 4, factions: all eight home sides are seen at work, heard, and now worked at: a paid tally at every yard, and the server knows each yard's stock
  and when each side's ship is down. Open: pay that follows what a yard is short of, patrols, a home that changes more than its stack, switching,
  licenses, seats and votes, the season, the two station sides (part 7).
- Part 3, jobs: 33 repeating runs. Open: the other roles, trade between worlds, fuel and repairs that cost (waits on Jaron's prices), a goal to save for.
- Part 5, the shell: the NEXT step folds; Keep walking. Open: as before (memory on a real phone, the big screen, the gamepad through every panel).
- Parts 1, 2: as HANDOFF 4 and 5 left them.

**Next three, in order.**
1. **A tally taken and paid on the live server** (the one thing this session could not show): extend `live-run.mjs` with a flight by taps (Course,
   Ceres or the Moon, the time compression buttons in the pilot's panel), then "Read the tanks" at Occator Works (35 m from the flight office) read off
   `activity.status()` on the page. Use it as the first real stranger's play-through of a crossing too, and write down every place it was not obvious.
2. **Pay that follows need** (parts 3 and 4, the first price that moves): each side's own run (Rations for the gate, Trays for the dishes, the line
   check, the wall, ice, charges, ore, salt) pays more when that side's yard is short: `tallyTruth(side, now, share)` is already on the server.
   Show it on the board ("the stand is down to 3: pays 200") and in the tally hand's line. Keep it inside the pay limits `pkg-missions` checks.
3. **Jupiter and Earth held still in a locked moon's sky** (unchanged from HANDOFF 6, item 3: `space/frames.js` `yawOf`, a tilt in the frame; read
   `worldKin` and everything that uses `yaw` first). Then `callisto-browser` passes on every date.
   After these: put places on the real ground in `where.js` (the camp arrow), the money piece once Jaron has answered the price question, part 2's leftovers.

**New gotchas.**
- **A refused action rolls the whole world record back.** Anything a refusal should remember (the wait after a wrong count) cannot be done by throwing:
  return `{ ok: true, wrong: true, ... }` and change the record. And `multiplayerView.request` shows `r.msg` as a ship's message when `ok`: send an
  empty `msg` and put your words in another field if the screen already says them.
- **A stock's "full" depends on the home's strength** (`stackShare`: a new shared world starts at strength 20, so a full stack is 60%). A test that
  expects "between 2 and 8" is wrong in a weak world. And a waved-off ship changes a stock: the server only allows for it when a ship is really parked
  on the stand (`standBlocked`), or "full" becomes an answer that always passes.
- **The status card is rewritten five times a second.** Anything a thumb must tap cannot live in `#hud-readout`: give it its own element beside it
  (as `#hud-next`), rebuilt only when its content changes. Playwright's `tap()` waits for a stable element and will time out on the other kind.
- **This worktree has both kinds of line ending** (`sideYard.js` and `activity.js` are CRLF on disk, most files LF; git stores LF either way). A script
  that edits by exact text must use the file's own line ending, or it finds nothing.
- **Shell heredocs still eat backslashes and quotes.** Every edit script that worked went through the Write tool into the scratch folder and was run
  from there; the ones typed into the shell were the ones that failed (this handoff's first try among them).
- `git push origin HEAD:<this branch>` makes a new branch on GitHub. Push `HEAD:main` only.
- `pkg-ceres` and the other `pkg-*.mjs` print nothing when run directly: they export `run({ check, section })` for `validate.mjs`. A three-line runner
  that imports the file and calls `run` is enough.
- Graphics memory: check `nvidia-smi` before blaming the game for a WebGL error in a headless test on this machine.
