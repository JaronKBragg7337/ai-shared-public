# How real game QA works, and what our playtester does about it

## World 2 target

Run `node tools/playtester/play.mjs --target world2 --url http://127.0.0.1:8000/world2/ --only phone --minutes 2` after serving the site repository locally. Omit `--only phone` to include desktop WASD. The World 2 report is saved under `state/playtest/` and records loading, entering, ground taps, the floating stick or keyboard, map opening, and a short walk. `--minutes` sets the exploration time budget, not a required duration: exploration stops after six gestures or when the budget runs out; fixed checks and loading can exceed the budget. It uses `dev=1` to read position, actual Playwright taps, and synthetic pointer events for held touches. It is not a real iPhone or a full world tour. World 2 needs its CDN dependencies; an explicit `--three-dir PATH` serves Three.js from a local package as an offline approximation, and the report identifies that substitution and version. `--out PATH` chooses a separate report directory. The Cosmos target remains the default.

Written 2026-10-08 for The Cosmos bot (`tools/playtester/play.mjs`). Plain words. The checklist at the bottom says which
items the bot does, and which only a person with a real iPhone can do.

## The short version of what professional testers do

1. **Smoke test every new build.** A few minutes: does it load, does the main screen work, can you do one full loop of the
   game without a crash. If that fails, nobody bothers with the deep tests. ([Ixie Gaming](https://www.ixiegaming.com/?p=15568), [game-qa-lead guidance](https://openskillindex.com/skills/alterlab-ieu-alterlab-gameforge-game-qa-lead))
2. **Regression pass.** After a fix, run the same paths again, because every fix can break something else. Short quick
   pass after every merge, longer full pass before a release. (same sources)
3. **Exploratory testing.** Stop following the script. Try odd inputs, odd order, push the limits, write down anything
   strange with a screenshot or video. This is where most real bugs are found. ([Ixie: exploratory testing in game QA](https://ixiegaming.com/?p=18443))
4. **Critical paths first.** The things 80 percent of players do in their first session get the most testing.
5. **Rank by risk.** A checklist only covers what you already thought of; spend time where the game has broken before.
6. **Write reports someone can reproduce:** build, device, exact steps, screenshot or video, what you expected.
   ([QA Madness case study](https://qamadness.com/case_studies/qa-process-setup-and-ongoing-testing-for-mobile-game-development-studio/))

## Mobile and phone testing (the part that matters most for Jaron)

- **Interruptions.** A call, a notification banner, a lock screen, switching apps. Banners are the nasty ones: the game
  keeps running under them while the player cannot see it. ([Datacalculus](https://datacalculus.com/en/blog/mobile-gaming-apps/game-tester/interrupt-testing-in-mobile-gaming-apps), [QASource](https://www.qasource.com/blog/mobile-interruption-testing), [Bugnet](https://bugnet.io/blog/qa-testing-for-interrupted-sessions-on-mobile))
- **Backgrounding.** Press home, come back: the game must be on the same screen, same spot, same money, with sound off while
  away. The phone may also kill the page while it is away, so a reload must put you back too. ([Bugnet: backgrounding](https://bugnet.io/blog/qa-testing-for-app-backgrounding-on-mobile))
- **iOS Safari specifics.** `pagehide` and `unload` often do not fire when Safari suspends a page, so save on
  `visibilitychange` and on a timer. A page can come back with its WebGL graphics context lost (seen on iOS 17), leaving a
  frozen black canvas. ([WebKit bug 199854](https://bugs.webkit.org/show_bug.cgi?id=199854), [Apple forums](https://developer.apple.com/forums/thread/737042), [three.js forum](https://discourse.threejs.org/t/context-lost-when-backgrounding-safari-on-ios-17-developer-beta-8/55772))
- **Network.** Drop the connection mid-action, go slow, come back. Games should show a clear message, retry, and recover
  without losing or doubling anything. Combine it with other things (lose the network while backgrounded, background during a
  save) because that is where race bugs live. ([Panto](https://www.getpanto.ai/blog/mobile-game-testing-guide), [QAwerk checklist](https://qawerk.com/blog/mobile-game-testing-detailed-qa-checklist/))
- **Rotation.** Turn the phone sideways during menus, during play and during a panel. The sources say little; testers
  simply do it everywhere and log the orientation in the report.
- **Device spread.** Different screens, memory, refresh rates and touch speed give device-only bugs. Test a cheap phone, not
  just a good one.

## "Break the game" behaviours

- **Walk into everything.** Walls, edges of the map, the sea, steep ground; jump against walls; look for falling out of the
  world and for walking off the map with nothing to stop you.
- **Out of order.** Soft locks mostly hide in unusual sequences: use the one item you needed on the wrong thing, press
  buttons before the game expects them, quit and reload in the middle of a cutscene or conversation.
  ([Bugnet: soft lock and dead-end detection](https://bugnet.io/blog/qa-testing-for-soft-lock-and-dead-end-detection))
- **The gate question.** For every step that blocks progress ask: is there any legal sequence of actions that destroys what
  the player needs to pass it, without satisfying it?
- **Spam.** Hammer one button 30 times; tap two buttons at once; double tap. Exposes double-actions and "busy" flags that
  never clear.
- **Idle.** Leave it alone for minutes. Looks for timeouts, drifting memory, kicked connections, things that quietly go wrong
  while nobody is touching it.
- **Monkey testing.** Random taps and keys everywhere for a while, watching only for crashes and errors. Cheap, finds
  surprising things.

## Economy and exploit checks

- Buy then sell the same thing: the player must never end up richer. Sell price should never beat buy price.
  ([Bugnet: trade and marketplace](https://bugnet.io/blog/qa-testing-for-trade-and-marketplace-systems))
- Money must never go below zero, and a purchase you cannot afford must be refused cleanly. Test zero, the cap, and
  "just short by one". ([Bugnet: currency and wallet](https://bugnet.io/blog/qa-testing-for-currency-and-wallet-systems))
- Double-spend: two purchases fired at the same instant both read the same balance. One request sent twice must charge once.
- Duplication usually comes from a race: confirm and cancel at the same moment, or use an item while it is being sold.
  Real example: New World switched its whole economy off after a dupe ([PCGamesN](https://www.pcgamesn.com/new-world/dupe-exploit)).
- Keep a ledger check: balance should equal the sum of what happened. Watch total money over time for sudden growth.
  ([Bugnet: economy edge cases](https://bugnet.io/blog/how-to-test-edge-cases-in-your-economy-and-currency))

## Progression and soft locks

A soft lock is when the game keeps running but the player can no longer finish, and nothing tells them. No crash, no error.
Testers hunt for it on purpose: map every gate and resource, then waste, sell or skip each one. Add a "nothing has changed
for a long time" detector so it shows up in testing. (Bugnet soft lock sources above.)

## Readability and new-player UX

Hand it to someone who has never seen it. Can they tell, without being told, what to do next? Is the next step on screen,
is the button label clear, does anything block the view? Playtesters note where a new player stops and looks confused.

## Accessibility basics (Game Accessibility Guidelines, "Basic" tier)

Easy and wide-reaching: readable default text size, high text contrast, do not use colour or sound alone to tell the
player something, big well-spaced touch targets on small screens, controls that can be remapped or are simple, volume
sliders per kind of sound, settings that are saved. ([Game Accessibility Guidelines](https://gameaccessibilityguidelines.com/), [Xbox Accessibility Guidelines](https://learn.microsoft.com/en-us/gaming/accessibility/guidelines)).
Apple's rule of thumb is a tap target of at least 44 points.

## Performance

- Judge by **frame time in milliseconds**, not average FPS: an average of 60 can hide a quarter-second stutter.
  Phone target is usually 30 fps = 33 ms per frame, and good practice leaves about a third as spare so the phone does not
  overheat. ([Unity profiling best practices](https://unity.com/how-to/best-practices-for-profiling-game-performance))
- Watch **memory over a long session** (leaks), **load time**, and test a low-end phone. Let a device cool between runs, a
  hot phone throttles. ([Room 8 Group](https://room8group.com/solutions/qa/game-performance-testing/), [Abratabia](https://www.abratabia.com/game-testing/performance-testing.php))

---

## The checklist: what the bot does, and what it cannot

Phase names are for `node tools/playtester/play.mjs --phases ...`. "qa" means all the new ones below.

| # | Real QA item | Bot? | How |
|---|---|---|---|
| 1 | Smoke test: loads, no errors, one full loop | YES | `smoke` numbers (load time, boot errors) plus the normal opening-to-port run |
| 2 | Regression pass on the main path | YES | opening, panels, tour, hire, dig, fly, rover on every run; same report layout each time so runs compare |
| 3 | Exploratory play | PARTLY | `freeplay` and `monkey` do random things; no judgement about what "looks fun" |
| 4 | Spam taps / double taps | YES | `spam` |
| 5 | Refresh in the middle of an action | YES | existing refresh checks (after tour, after dig, mid dig and mid ride in the opening) |
| 6 | Alt-tab / background and return | YES (simulated) | `lifecycle`: fires the same hidden/visible/blur events the browser fires |
| 7 | WebGL context lost on resume (iOS bug) | YES (simulated) | `lifecycle`: forces a context loss and restore, checks frames resume |
| 8 | Phone rotation | YES | `lifecycle`: switches to landscape and back, runs the layout check in both |
| 9 | Offline / network drop and recovery | YES | `network`: goes offline mid-play, taps, comes back, checks it reconnects and the purse is unchanged |
| 10 | Slow network | PARTLY | offline and recovery yes; throttled speed only on the desktop Chromium run |
| 11 | Real phone call, banner, lock screen, low battery | NO | needs a real iPhone |
| 12 | Walk into walls, edges, the sea | YES | `edges`: walks 8 directions, jumps at walls, checks for falling through and for leaving the map |
| 13 | Clipping / falling out of the world | YES | background watcher (every 2.5 s) plus `edges` |
| 14 | Do steps out of order | PARTLY | `monkey` taps buttons in random order; the soft-lock gate-by-gate map is still a human job |
| 15 | Idle for minutes | YES | `idle`: no input for 90 s, then checks memory, connection, frames |
| 16 | Buy then sell loop never profits | YES | `economy` (needs a trader on that world) |
| 17 | Money never below zero; cannot-afford refused | YES | `economy` |
| 18 | Double-spend / duplicate on double tap | YES | `economy` + `spam` count requests per tap and check the purse |
| 19 | Race-condition dupes between two players | NO | needs two clients at once |
| 20 | Soft-lock: stuck, no way forward | PARTLY | stuck-state watcher; `softlock` checks the player can still move and act at the end |
| 21 | Can a new player tell what to do next | PARTLY | `a11y` / `readability` checks that guidance is on screen; the vision pass looks at screenshots. A real first-time player is better |
| 22 | Text size, contrast, tap size, names on buttons | YES | `a11y` |
| 23 | Colour-only / sound-only information, subtitles | PARTLY | vision pass only |
| 24 | Frame time, spikes | YES, with a caveat | measured every run; headless software rendering is slower than a phone |
| 25 | Memory over time | YES | page memory (desktop) and graphics-object counts (both) sampled over the run, trend reported |
| 26 | Load time | YES | `smoke` |
| 27 | Battery, heat, throttling | NO | needs a real phone |
| 28 | Real touch feel, real iOS Safari audio | NO | Playwright WebKit on Windows is close, not the same |
| 29 | Many device models / OS versions | NO | one phone profile and one desktop profile |
| 30a | Walk the whole beginner chain (earn the first ship) on every start world | YES | `lifeboat`: buys the power cell and fuel coupler from the two givers (Okafor and Pruitt on Earth, the two traders on Mars), fits both at the boat, checks the NEXT line names them |
| 30 | Write a reproducible report | YES | `REPORT.md`: steps, screenshot, device, build id |

## How to run the new checks

```
node tools/playtester/play.mjs --phases qa --skip-opening --minutes 8     # just the QA checks, from the review start (Mars)
node tools/playtester/play.mjs --start earth --side skyward               # normal run; QA phases are in the default list, --no-qa leaves them out
node tools/playtester/play.mjs --phases tour,lifeboat --start earth       # the Earth chain only (the opening still has to be played to get to Earth)
```

The report has a "QA checks" table (pass / FAIL / skipped per check, per device) and a "Load, size and memory" section.

Live run on this Windows MSI: Playwright WebKit fails jsDelivr with "SSL connect error" (test browser only; Chromium and real iPhones load it). Download the three@0.182.0 tarball and pass --three-dir to its package folder. Passed all phone checks that way 11/6.
