# Site health check: heartbeatobservatory.com (2026-11-13)

**Read-only audit. Nothing was edited, committed, pushed or deployed.**

- **Work started:** Fri Nov 13 23:12 (machine clock). **Finished:** Fri Nov 13 23:55.
- **Pages checked:** 164 page files from the repo (`C:\Users\lilli\Projects\heartbeat-observatory`), plus 5 special addresses (/map, /tv/news/, /school/school-test/, /engine/world/, a made-up address to confirm the 404 page works).
- **Results:** **6 broken** (4 of them real broken links), **5 stale**, **6 with phone-width issues** (some pages are in more than one group), **58 paused or hidden on purpose** (facts only), **93 OK**.
- **Every page answered 200 (loaded).** None had sideways scrolling at phone width except one paused page and two internal tool files.
- **How it was checked:** an iPhone-sized screen (390x844) in WebKit, the same engine as iPhone Safari. For each page the script recorded the answer code, script errors, files that failed to load, whether the page was wider than the screen, and buttons or links too small to tap. Every internal link found on every page was then opened (1 link check per address). 3D pages were checked again in Chromium, because headless WebKit on this PC has no graphics chip (see the note at the end).
- Screenshots: `C:\Users\lilli\AI-Shared\research\audit-2026-11-13\site-shots\`

---

## BROKEN (most serious first)

1. **https://www.heartbeatobservatory.com/news/archive/** (linked from home)
   About 100 source chips lead to a "page not found". When a news item's source is a name (for example "AP News via AP (via Google News)", "The Verge", "White House") and not a web address, the page still turns it into a link. The chip says "link", and tapping it opens a 404 like `/news/archive/The%20Verge/`. Today's view alone has 2,034 source chips, and many are like this.
   *Fix:* in `news/archive/archive.js` (around line 299), only make the chip a link when the source starts with `http`, and show the name as plain text otherwise.

2. **https://www.heartbeatobservatory.com/lab/tesseract/**, **/lab/tesseract/inside/**, **/lab/tesseract/inside/v1/** (hidden lab pages)
   Links to `anatomy.html` and `pages.html` give 404 because those files were never added to the repo (the folder only has `index.html`).
   *Fix:* add the two pages, or remove the "Anatomy" / "Pages" links.

3. **https://www.heartbeatobservatory.com/map**: 404 on the main site.
   The power map works at https://powermap.heartbeatobservatory.com/ (checked, loads). `/map` only works on that address, not on www. Nothing on the site links to `/map`, so visitors only hit it if someone types or shares it.
   *Fix:* make `/map` on www forward to the powermap address, like `/powermap` already does.

4. **https://www.heartbeatobservatory.com/PCGames/peakaboom/**
   A Spawn "card" inside the page returns 404 (`spawn.co/embed/card/@jissi/peakaboom`). It comes from Spawn's side. The Play link (`spawn.co/jissi/peakaboom/play`) works.
   *Fix:* none needed on our side unless the empty card shows. Recheck on a phone, and if there's a blank box, link to the play page only.

5. **(Minor) https://www.heartbeatobservatory.com/live-systems/crew/bot/** opened with no bot named
   It shows "Not found" plus a script error. All 17 links the site actually uses (`?id=codex`, `?id=satya-twin`, ...) were opened and every one works. This only happens if someone opens the bare address.
   *Fix:* none needed, or forward the bare address to /live-systems/crew/.

### Needs a real-iPhone check (could not be confirmed here)
- **/museum/round-1/astra.html** and **/museum/round-1/fable.html** froze the WebKit test tab for more than 80 seconds. **/games/syl/** froze it once in the first pass and loaded in the second. In Chromium with software graphics all three load with no errors. This looks like a test-PC problem (no graphics chip) rather than a site bug. Still, heavy 3D pages that lock up when graphics are weak are worth one tap test on the real iPhone.

---

## STALE

1. **https://www.heartbeatobservatory.com/live-systems/** (linked from home, "Live Systems" card)
   The Trade Desk card still says "Grok bots trade live games on Polymarket US ... DeepSeek ... trades when its number beats the market". Per AGENTS.md (Jaron 10/28) the Polymarket system is down ($0). The Crew page shows $0.09 cash ready and $0.00 in open trades. Screenshot: `site-shots/live_systems.png`.
   *Fix:* change the card to say Polymarket trading is stopped (kept, not deleted), or point it at the crypto lane and the funding lane only.

2. **https://www.heartbeatobservatory.com/sparks/** (in the top menu)
   It says "Sparks is also a channel on Heartbeat TV (coming soon)". Heartbeat TV is live, and Sparks isn't in its channel list.
   *Fix:* remove "(coming soon)", or add Sparks as a TV channel.

3. **https://www.heartbeatobservatory.com/work/** (linked from home)
   It says "One founder, Jaron, an entrepreneur who also roofs for a living". Jaron said on 10/30 that roofing is his past and shouldn't be framed as his trade in content or pitches.
   *Fix:* drop "who also roofs for a living".

4. **https://www.heartbeatobservatory.com/powermap/** (and the powermap address; not linked from any page)
   The governors line reads "source updated Nov 6, 2025", and the newest date on the page is Nov 4, 2026. After the Nov 3, 2026 elections, the governor and legislature counts may be out of date.
   *Fix:* refresh the post-election numbers and the "source updated" date.

5. **https://www.heartbeatobservatory.com/games/president-sim/classic.html**
   The banner says "UPDATED JUNE 2026". It's the kept "classic" version (the main /games/president-sim/ is current), so this is low priority.
   *Fix:* label it "Classic (June 2026)" so the old date reads as on purpose.

---

## PHONE-WIDTH ISSUES

**Good news: no public page scrolls sideways at iPhone width.** The issues are small tap targets (under 24 px tall, harder to hit with a thumb):

- **/news/archive/**: 23 small targets, including every "every day →" link (17 px tall) and "← Watch the show". *Fix:* give those links more padding, at least 32 px tall.
- **/sparks/**: 15 small source links (17 px tall, e.g. "Wired", "NIST"). *Fix:* more line height or padding on the source links.
- **/social/**: 369 small targets, mostly source links in posts (about 19 px tall) and "Sign in →" (20 px). *Fix:* more padding on links inside posts.
- **/games/president-sim/**: top links 15 to 23 px tall ("Play Classic ↗" 15 px, "Sources & credits" 16 px, "How to play" 23 px). *Fix:* make them button-sized.
- **/studio/**: the volume and left/right sliders are 20 px tall. *Fix:* make the slider touch area taller (the bar can stay thin).
- **/powermap/** (hidden): 41 source links 16 px tall.

Site-wide: the floating round phone button (bottom right, stamped on every page) covers part of the content under it, e.g. a card on the news archive and on Revenue Desk. Not broken, but worth a look if it hides anything important.

Two internal tool files are wider than the screen, as designed (they are fixed-size image makers, not pages for visitors): /tools/og-card/og-card.html (1200 px) and /games/the-cosmos/tools/ship-thumb.html (960 px).

---

## PAUSED (facts only; nothing suggested)

- **Worlds Lab** (/worlds-lab/ + starter + 4 "coming-soon" + 9 worlds + 1 template file = 16 files): all load (200). Still a visible card on the home page. The template file has an unfilled `{{SCRIPT}}` placeholder that 404s, which is expected for a template.
- **/pam/**: loads (200). Hidden from the home directory as intended.
- **Fruit fly** (/live-systems/flies/, /flies/brain/, /flies/school/, /flies/school/live/, /school/, /school/school-test/): all load. Newest date shown is Sep 17. The flies page says "WAITING FOR A MATCH". Small tap targets in their headers.
- **/lab/hidden/**: loads.
- **Trading pages**: /live-systems/paper/ (newest date Sep 10), /live-systems/crypto/ (newest Oct 23), /live-systems/habitat/ ("OFFLINE", "3D rendering is unavailable on this device"), /live-systems/trades/ (forwards to /crew/trades/), /live-systems/trades/decisions/ (forwards to /crew/reasoning/).
- **/live-systems/revenue/** (hidden from home): "Last scan 1194 hours ago · 9/25/2026". It shows "Approval required before anything ships" and is **the only page that scrolls sideways at phone width** (a money amount pushes it to 1034 px). Screenshot `site-shots/live_systems_revenue.png`.
- **/qwen/** (hidden from home): "Last heartbeat 1309h ago", "State store updated Sep 20", Qwen and OpenClaw "DEGRADED", last error openclaw_timeout. Screenshot `site-shots/qwen.png`.
- **Hidden / noindex on purpose**: /lab/bakeoff/, the 7 /lab/bedroom* copies, /lab/necklace/, /lab/studio-pro/, the 6 /preview/* sites, the 5 /work/sample/* sites (placeholder reviews and names, labelled as samples). All load.
- **Admin** (/admin/ + control, keys, mailbox, remote, sapling, video-drop): all 7 load and show sign-in. Not tested past login.

---

## OK (93 pages; all load, no real errors, fit the phone)

**Linked from home or the top menu:** / · /news/ · /tv/ · /homes/ · /studio/ (tap note above) · /live/ · /ideas/ · /artifacts/ · /engine/ · /world2/gate/ · /world3/gate/ · /library/ · /social/ (tap note) · /video/ · /projects/ · /games/ · /3DPrinterAsset/ · /live-systems/crew/ · /PCGames/ · /standards/

**Linked from other pages:** /engine/hub/ · /world2/ · /world3/ · /news/desk/ · /render/ · /render/anything/ · /studio/learn/ · /studio/lyrics/ · /video/3d/ · /experiments/highway-after-us/ · /PCGames/syl/ · /live-systems/crew/ bot, chat, reasoning, retired, schedule, trades · /museum/round-1/ (10 rooms; see the iPhone note for astra and fable) · /lab/seam-room/j/ · games: cyber-trench-overdrive, fable-survival, hedge-maze, mindgames, northstar-addressable-world, orbit-salvage, parkworks, president-sim, rift-clash, robot-evolution-lab, rocket, rustfall, signal-drift, syl, the-cosmos (page says "Development is paused"), the-defender-3d, wasteland-commons

**Hidden / not linked from anywhere (load fine, listed so you know they exist):** /HeartbeatCenter/ · /chat-neighborhood/ (founded 9/6, one resident) · /control-room/demo/ · /guides/voice-ai-team/ (on hold, unannounced) · /island/ · /lab/arena/ (+a, b) · /lab/pet/ · /lab/seam-room/ a to i · /lab/voice/ · /morse/ · /museum/ · /realcity/ + /realcity/fort-wayne/ · /space/ · /world3/town/ · /games/syl-test/ · /games/syl/desktop.html · /games/the-necklace-show/ · /tv/news/ and the other TV channel addresses · /engine/world/ (forwards to /engine)

The site's own 404 page works (a made-up address returns 404 properly).

---

## Other things worth knowing

- **This PC (MSI) has trouble reaching GitHub over IPv6.** Connections to `jaronkbragg7337.github.io` and `raw.githubusercontent.com` got reset at random ("SSL connect error"). Over IPv4 every one worked (signal-drift, unfinished-island, MindGames, Movie Theater, repos.json, the watch feed). So the site is fine, but **any MSI script that pulls from GitHub may fail at random.** If the news pipeline or the nightly saves ever fail with connection resets, this is a likely cause. *Fix:* make Windows prefer IPv4 for those hosts, or add retries.
- **No 3D graphics in the WebKit test browser on this PC.** Every 3D page shows "WebGL context lost" in WebKit here. In Chromium with software graphics, all 14 3D pages rechecked load with no errors (rocket, syl, syl-test, rustfall, robot-evolution-lab, five museum rooms, world2, engine, the-cosmos). Future automated phone checks on the MSI will report false 3D errors unless they use Chromium or a real device.
- **Sitemap**: all 80 entries point to real pages (the /tv/<channel>/ entries are served by rewrites and load).
- **Not checked:** anything behind sign-in, how games play past the first screen, overlapping content (only sideways overflow and tap size were measured automatically), and a real iPhone.

## FIXED by Claude 11/14 ~12:00 AM (pushed ab77b4de, verified live)
- /news/archive/: source names that aren't web addresses now show as plain text, not dead links.
- /live-systems/: Trade Desk card now says paused since Oct 28 ($0, doesn't earn from others' losses).
- /work/: "who also roofs for a living" removed (roofing is his past, 10/30).
## Left (small, next day session)
- /lab/tesseract/ missing Anatomy/Pages files (hidden page). /sparks/ "TV coming soon" stale. /powermap/ governor counts after Nov 3 election. Tap targets under 24px on 5 pages. Two museum rooms (astra, fable): real-iPhone tap test. MSI IPv6-to-GitHub drops (consider preferring IPv4 for scripts).
