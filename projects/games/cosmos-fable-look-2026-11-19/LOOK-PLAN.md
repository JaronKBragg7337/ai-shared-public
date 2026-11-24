# The Cosmos: look pass by Fable 5.2 (2026-11-19)

How I looked: served the game from my own worktree, drove it headless with Playwright on the MSI's real GPU.
iPhone WebKit 390x844 (phone tier) and desktop Chromium 1440x900 (high tier). 13 spots: Mars pad, port, open Mars
ground, Phobos from space, approach, final, landed ship, eye level on the pad, eye level among rocks, underfoot,
third-person walk, Mars in Phobos's sky, ship corridor. Shots are in `shots/before/`. File names end in
`-phone-webkit`, `-desktop-chromium`, or `-desktop-chromium-live` (the real clock, what a player gets).

"Missed before" = I searched games/the-cosmos/docs/qa and found no mention of it.

## Ranked problems

### 1. Phobos ground is lit by a helmet lamp that is stuck on (FIXED in this pass) - missed before
- Saw: `08-phobos-eye-pad`, `09-phobos-eye-rocks`, `10-phobos-underfoot`, `11-phobos-third-walk`. Everything within
  about 24 m of you is a warm tan haze; further out the ground is grey. Underfoot it looks like beige fog.
- Why it breaks realism: Phobos is charcoal grey rock in hard sunlight with no air. A warm glow that follows you
  around reads as fog or indoor lighting, and it fills in every shadow near you. This is the ground-level look.
- Cause (a real bug): the "you are in a hole" lamp measured your depth against MARS while you stand on Phobos.
  That reads as thousands of km underground, so the lamp ran at full power on every moon, in full sun.
- Fix: measure depth on the world you stand on; on moons the lamp comes on at night or in a dug hole only. Done.
- Effort: small (done, 11 lines in src/main.js).

### 2. The player walks Phobos (and Mars) in a T-shirt, jeans and bare head - missed before
- Saw: `11-phobos-third-walk` (phone and desktop). A man in a white tee and sneakers strolling in vacuum.
- Why: nothing kills "realistic space game" faster in a clip. This is the first thing a viewer of the Phobos
  walking clip will comment on. Same on Mars.
- Also the walk itself: a normal Earth stride at 5.6 mm/s2 gravity. Real motion there is slow floating hops.
- Fix: put the player (and outdoor NPCs) in a pressure suit + helmet when outside a ship or building; on tiny
  moons swap the walk cycle for a slow bound with long air time. The game already has a suit/helmet stand-in
  (looks-r1 flight deck crew) to start from.
- Effort: medium-large (a suit mesh that fits the Loft people rig, plus a low-gravity gait). One night build.

### 3. Phobos by day looks like an overcast sand dune, not an airless moon
- Saw: `06-phobos-final`, `08`, `09`, `11`. Pale, even grey; soft wavy ripples that read as wind-blown sand
  (there is no wind on Phobos); no hard shadows from rocks, the ship or the person (only a soft blob under the feet);
  rocks are a few low-poly pebbles; the 2-3 m boulders the notes describe do not read at all.
- Why: no air means ink-black shadows with knife edges, and Phobos reflects about 7% of light (darker than
  asphalt). Contrast is what sells "space".
- Fix: (a) cut the rusty fill light on moons by about half so shadows go near black; (b) let the sun shadow map
  cover rocks/ship/person on moon ground and make the far tier receive it; (c) replace the ripple bump with
  small craters and grit; (d) darken the ground about 30%; (e) proper boulders with shadows.
- Effort: medium. (a)+(d) are an hour; (b)(c)(e) are a build.

### 4. Every earlier look review saw a sun no player ever gets - missed before
- Saw: compare `09-...-desktop-chromium` (dev default) with `09-...-desktop-chromium-live`. A `?dev=1` session
  pins the sun about 75 degrees up. All QA shots were taken that way. With the real clock, Phobos today was in
  night: a nearly black screen with a dim brown pool (`11-phobos-third-walk-desktop-chromium-live`).
- Why: Phobos has ~3.8 hours of night in every 7.7. About half of real visits land in the dark, and a high noon
  sun is also the flattest, least dramatic light for the other half.
- Fix: review at `&sky=live` and at a low sun; give the night side a real plan (strong Mars-shine when Mars is
  lit, a proper white helmet beam, lit pad lights), and prefer low sun for clips.
- Effort: small to medium.

### 5. Phobos from space has a square patch pasted on it
- Saw: `04-phobos-space`. The detailed ground near the landing site shows as a sharp-edged rectangle with a
  different brightness and texture from the blurry body around it, plus a smaller square inside it. `05-phobos-approach`
  shows the same edge as a straight line with craters only on one side.
- Why: approach is the trailer moment; a visible tile edge says "game level", not "moon".
- Note: I used the review camera high above the pad; I did not fly a real approach, so how visible it is in normal
  flight is not confirmed.
- Fix: match colour/brightness between the whole-body shell and the tiers, fade the tier edge over a few hundred
  metres, and put craters on the shell at the same density.
- Effort: medium.

### 6. Mars in Phobos's sky is a dim, flat, dark-red disc
- Saw: `12-phobos-mars-sky`. Mars should be the showpiece: it fills a quarter of the sky from Phobos and its lit
  side is far brighter than the ground you stand on. Here it is darker than the regolith, with no visible terminator.
- Fix: light the far Mars by the real sun direction with a brightness that beats the ground; add a thin limb haze.
- Effort: small-medium.

### 7. Mars port: stars in a daytime butterscotch sky, and "brick" hulls
- Saw: `01-mars-spawn`, `03-mars-open-ground`. Stars show through a bright dusty daytime sky (they would not).
  The ship hull and tower texture reads as masonry bricks; engine bells are flat brown cones.
- Fix: fade stars with sun height; a metal panel texture with fewer, larger plates; darker, glossier bells.
- Effort: small (stars), medium (hull).

### 8. Small things
- HUD in the review camera says "Martian regolith" while on Phobos (`04`-`07`). Probably only in review cam; not checked in play.
- Corridor (`13-ship-interior`) is the best-looking place in the game; walls have a speckle that reads as dirt on a lens.
- Phobos pad marking text is mirrored/unreadable from the side shown in `07-phobos-landed-ship` (may just be the angle).
