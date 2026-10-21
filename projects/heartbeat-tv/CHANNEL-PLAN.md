# Heartbeat TV - channel plan (50+), started 2026-10-11 by Claude Code

Jaron 10/11 12:27 PM: "you have full permission" to add channels; he plans 50+. Digital first - Heartbeat Observatory became the
company because it could be built without physical infrastructure, so channels come before physical builds.

Rules for every channel (same as History/Science):
- Accurate, sourced on screen, disputes labeled, today's laws shown as the best current understanding (people may dream).
- His old sparks are welcome as material; never branded "Jaron's idea/discovery".
- Each episode: TV (16:9) + vertical 9:16 cut for YouTube Shorts / TikTok / X. Renderer: projects/tv-lib/.
- A channel goes live with at least ONE episode - no empty channels on the guide (the AI Slop/Comedy/Music style "submit" empties
  were before this rule and can stay).
- Writer: Claude or Kimi or Grok; not ChatGPT as lead writer. A second AI checks facts before outside posting.

## Live
1 News · 2 Shows · 3 Movies · 4 Comedy · 5 Music · 6 AI Slop · 7 History · 8 Science

## Next (first episodes picked)
9  **Open Questions** - big unanswered questions, both sides fair. Ep 1: "Did we sing before we spoke?"
10 **Still Unknown** - real mysteries with evidence vs claims labeled. Ep 1: "The energy we can't explain yet" (dark energy).
   Made: 10.1 dark energy, 10.2 Coral Castle, 10.3 "Can vibration cut stone?" (10/16; ultrasonic machining + Stocks copper/sand; home test still NOT run).
   Queued: pyramid construction (copper, granite - after Vex's dated records), "Older than we think?" dating debates.

## Candidate channels (seed in brackets where one exists)
11 Space Now - real missions, launches, what's up there this week [Cosmos long vision]
12 How It's Made (Digital) - how apps, chips, the internet, AI actually work
13 AI Explained - what AI can and can't do, tested live [Framing Lens / LRP tests]
14 Money Basics - how money, banks, interest, crypto work; education only, no trade calls [money loop, two-sides]
15 Builders - how roofs, bridges, railroads, dams get built [his trade; railroads ep]
16 Inventions That Almost Were - ideas that were close but lacked tools at the time [his "needed infrastructure" sparks]
17 Earth - weather, volcanoes, oceans, materials [material rarity tests]
   Episode seed (10/12): "How a highway disappears" - season by season, what reclaims an empty road (edges, leaves, freeze-thaw, drains, seeds, trees). Simulated in 3D, sourced (succession studies, Pripyat, abandoned roads).
18 Body - how breathing, sleep, the brain work [Science 8.1 breath]
19 Animals - the fly and other small minds [fly seed]
20 Music History - the multi-part series already queued
21 Myths vs Records - legends checked against what's documented
22 Lost Places - ruins and cities, what we know and don't
23 Indiana & the Midwest - local history, Fort Wayne
   Seeds (10/13): fur-trade rendezvous reenactments (~1812 era: trade goods, muskets, axes, no modern gear); Fort Wayne battles/sites by neighborhood - "every place has a story".
24 Kids' Science (all ages) - simple experiments with household things
25 Future Jobs - what work looks like with AI, honestly [Q-025 jobs]
26 Law Made Plain - how laws, courts, LLCs work in plain words [LLC filing walk-through]
27 Words - where words and phrases come from ["words are powerful"]
28 Energy - power grids, batteries, open energy questions
29 Code Along - building a small app or game step by step [games]
30 Game Worlds - inside The Cosmos and the other worlds [Cosmos, games]
31 The Data - one chart, one story, sourced
32 Maps - how borders, roads, rivers shaped places
33 Food & Water Science - how food and water systems work [business policy: never sold]
   Recipes: AI finds recipes, writes its OWN steps + visuals (ingredient lists not copyrightable; others' written instructions/photos are), credits sources; texture = viewer's preference, never "crunchy is wrong".
   COOKING CHANNEL (AI-made, teaches cooking in general, like History/Science; Jaron never on camera - 10/14 4:53 PM). Material (never branded his): his own recipes, free; texture-first (ask how people want their VEGETABLES cooked, not just meat); grill steak + asparagus + shrimp + mashed potatoes; the food-truck menus he designed as a teen.
34 Disasters & Lessons - what went wrong, what changed after
35 Inventors - people behind things, credit where due
36 Mind & Habits - how attention, fear, motivation work [caution breeds fear]
37 Time - calendars, clocks, how we measure time
38 Materials - copper, granite, rare elements, why they behave as they do [rarity + pyramid sparks]
39 Sound - vibration, resonance, acoustics of old buildings [King's Chamber, Coral Castle]
40 Ocean & Ships - sailing, trade routes [Sobo sailboat]
41 Flight - from kites to rockets
42 Numbers - math stories without the fear
43 Weather Watch - why the forecast is what it is
44 Tools Through Time - stone tools to 3D printers
45 Light & Color - why things look the way they do [visual comfort]
46 Elections & Government Made Plain - how it works, no sides taken
47 Health Myths Checked - sourced, careful, not medical advice
48 Trade & Markets History - tulips to prediction markets, education only
49 Survival Skills (safe) - fire, shelter, water basics
50 Behind Heartbeat - how this company and its AIs work, in public [build in public]
   Story seed (Jaron 10/11): the LLC was founded (10/8) the same fall the US renamed AI to "super intelligence (SI)" (UN speech + executive order, Sept 2026) - a company born right at the name change; bio says "AI (SI)".

Order: 9 and 10 first, then pick by which seeds are strongest and which cut well to vertical. Add rows freely; keep this list current.

## Monetization guard (web check 10/11 - see projects/strategy/REVENUE-STREAMS.md)
YouTube demonetizes templated/repetitive AI channels (channel-level). Every episode needs its own visuals and format, not just
new text on the same cards. Vertical cuts run 61+ seconds (TikTok pays only over 1 minute). No AI anchor giving health/money/legal advice.

## Video QA reviewer (Jaron 10/14 9:14 PM)
Before shipping, an AI that WATCHES the finished video (sound + picture), like the game playtester: Gemini API (native video input) or Grok (already used to watch videos - memory grok-watches-video). Catches what verify_voice.py cannot: overlapping text, mismatched visuals, awkward pacing. Lesson logged: 8.4 highway posted to TikTok with cut-off narration (kokoro 25 s truncation) - nobody had listened; now verify_voice.py gate + this reviewer.

## Ship gate (coordinator 10/14)
Every episode passes verify_voice.py before shipping. (projects/tv-lib/verify_voice.py <final.mp4> <script.json>: local speech-to-text of the final narration vs script.json; any segment missing >5% of its words blocks the ship. Re-voicing longer than the cue window: projects/tv-lib/retime.py slows the video under it, no re-render. Needs: pip install faster-whisper.)

## Episode ideas from ChatGPT, shared by Jaron 10/17 8:43 PM (not yet fact-checked; no overlap with aired episodes)
- 9.2 Can something learn without a brain? (slime molds) - ChatGPT's pick for next; Open Questions has only 9.1 so far
- 9.3 Do animals understand death? (elephants, primates)
- 9.4 What if gravity isn't the full story? (dark matter vs modified gravity; neighbors 10.1 dark energy - keep distinct)
- 10.4 The book nobody can read (Voynich Manuscript)
- 10.5 72 seconds from somewhere (the 1977 Wow! signal) - ChatGPT listed it twice
- 7.5 The year summer never came (1816, Tambora)
- Science: the first great extinction was caused by life itself (Great Oxidation Event, ~2.4 billion years ago)
- History: did we build civilization backward? (Gobekli Tepe, 11,000+ years)
- Open Questions: can consciousness ever be measured? (animals, AI)
Channel framing to keep: Open Questions = real competing scientific explanations, debate not settled. Still Unknown = one
specific mystery: what's verified, test each explanation, separate open evidence from debunked claims.

## Episode picked by Jaron 10/18 12:31 PM (from his Dec 2025 Africa thread, via ChatGPT search)
- Open Questions (or History): "Did humanity's birthplace have something special that helped us survive, or is it just where
  the evidence was preserved?" Africa's rift valleys preserve fossils well (preservation bias) vs real survival advantages;
  Olduvai/Laetoli, the Toba debate. Never framed as Jaron's idea. Pair later: an Earth episode on plate tectonics (Africa moves;
  the East African Rift is splitting).
- Episode ideas (Jaron 10/19 late night): "One lab's waste is another's product" - synchrotron light is CERN's loss and Terafab's
  hinted goal (free-electron laser EUV, Musk "FEL FTW", not confirmed). "Why rockets shake themselves apart" (pogo) - Space Now.
- IDEA (Jaron 10/20, comes WITH long-term trading, not now): a daily MARKET ANALYST show on the site next to the news. The
  trading AIs (not Claude - Claude doesn't trade or give investment advice) put the market captures together and give their read.
  Born from Orchestra (his 2-hour manual multi-AI market sweeps). Needs: clear "AI analysis, not financial advice" label; keep
  the estimator isolation rules (ESTIMATION-ISOLATION.md) - the show must not feed the traders' own positions back to them.
- SHOW IDEA (Jaron 10/20, not now): a realistic drama in the vein of Shameless, "just life". Not "Jaron's life" - real problems
  people in similar spots relate to: child support + court, broke weeks, roofing crew days, two on a scooter with a baby coming,
  bills juggled at the last second. Some problems get solved, some avoided, some pushed to the last minute and somehow figured out.
  Built from his public Pieces of My Life + second-by-second detail he adds (voice notes) + other people's situations, changed and
  fictionalized. Realistic characters (MetaHuman/Unreal, pre-rendered). Real people never identifiable (kids, exes, family).
  - Device (Jaron 10/20): split the versions of himself over the years into 2-3 separate characters living side by side (he's 'been many types of a person'). Viewers see the stages of one life as different people.
- Episode idea (Jaron 10/20 via ChatGPT talk): 'Does AI know physics?' - bottle pouring water on desert sand, AI image (guesses the look) vs Blender fluid sim + render (calculates it); compare gravity, water volume, soaking into sand. Science channel. All software, MSI can render.
