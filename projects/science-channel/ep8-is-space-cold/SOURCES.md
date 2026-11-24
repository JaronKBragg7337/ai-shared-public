# Science ep8 "Is space cold?" - sources and what each claim rests on

Every narrated claim below maps to a source number in `RESEARCH.md` (same folder; full URL list at the bottom of that file,
accessed 2026-11-03). **[GK]** = standard textbook physics. Script written 2026-11-03 by a cloud Claude session. **Not yet
fact-checked: Codex checks it before render.** WebFetch was blocked in that session for nasa.gov, wikipedia.org and
spectrum.ieee.org, so claims rest on search summaries of the listed pages; Codex should open the primary pages.

## Claims in the narration

| Seg | Claim (as spoken) | RESEARCH.md source | Status |
|---|---|---|---|
| n01 | Leftover glow of the Big Bang is about 2.7 degrees above absolute zero | [1] | confirmed (2.725 K) |
| n01 | Space is cold but very bad at taking heat away | [1][GK] | framing, supported by section 3 |
| n02 | Heat leaves three ways (touch, moving air or water, infrared glow) | [GK] | textbook |
| n02 | In near vacuum, almost nothing to touch or flow; only radiation | [1] | confirmed |
| n02 | A thermos keeps coffee hot with a layer of vacuum | [1][GK] | textbook |
| n03 | Stefan-Boltzmann: radiated heat grows with area and with absolute temperature to the fourth power; double it, sixteen times | [4][5] | confirmed |
| n03 | Perfect dark surface at room temperature: about 460 W per square meter | [4] + our arithmetic (5.67e-8 x 300^4 = 459) | computed; one face, emissivity 1 |
| n03 | Space hardware needs big surfaces, turned away from the Sun | [3][5] | confirmed (ISS radiators kept out of sunlight where possible) |
| n04 | ISS has six radiators | [2][3] | confirmed (3 starboard, 3 port, 8 panels each) |
| n04 | Each about 23 m long, about a tennis court | [6]; tennis court 23.77 m [GK] | confirmed (75 ft, 2002 Boeing/Lockheed) |
| n04 | Liquid ammonia carries the heat | [2][3] | confirmed |
| n04 | Built to throw away about 70 kW | [2] | confirmed as DESIGN figure; loads have grown since 2010 [3], so "built to" wording |
| n04 | Ammonia freezes at about minus 78 C; controllers steer radiators to avoid freezing | [2] | confirmed (minus 77.7 C, closed-loop pointing) |
| n05 | Body makes about 70 W resting, more than 700 W working hard | [7] | confirmed (70 to 730 W, NASA) |
| n05 | Underwear laced with cool-water tubes (LCVG) | [7] | confirmed |
| n05 | Sublimator: water freezes, then turns straight to vapor in space, taking heat | [7] | confirmed |
| n05 | One spacewalk can use about 3.5 kg of water | [7] | confirmed (about 3.6 kg / 8 lb per astronaut per EVA) |
| n06 | AI computers use huge power; nearly all ends up as heat | [GK][13] | textbook (electrical power in chips becomes heat) |
| n06 | In the right orbit, panels see the Sun almost all the time | [11] | confirmed (dawn-dusk sun-synchronous orbit) |
| n06 | Google Suncatcher: panels up to 8x more productive | [11] | confirmed as GOOGLE'S CLAIM ("Google says") |
| n06 | Starcloud flew one Nvidia chip in 2025 and trained a small AI model in orbit | [8] | confirmed (H100, 2 Nov 2025; NanoGPT, Dec 2025) |
| n06 | SpaceX asked for up to one million data center satellites in 2026 | [12] | confirmed (FCC, 30 Jan 2026) |
| n06 | Blue Origin filed for more than fifty thousand | [12] | secondary source (51,600, Project Sunrise, 19 Mar 2026); Codex: check FCC docket |
| n07 | WEF: about 1,600 square meters of radiator per megawatt | [13] | confirmed (June 2026) |
| n07 | IEEE Spectrum: one top AI chip needs about 1.4 square meters of radiator, running hot | [14] | confirmed per search summary (H100, 700 W, at 60 C) |
| n07 | Radiators are heavy and must survive sunlight and debris with no repair crew | [13][15] | confirmed |
| n07 | A startup CEO admitted the economics of launch don't quite work yet | [16] | confirmed (Euwyn Poon, Orbital, The Register, Apr 2026) |
| n08 | Independent study: radiators about 14% of weight in its model; launch cost matters far more | [17] | confirmed (Forethought, conservative case) |
| n08 | Google plans two test satellites in early 2027 | [11] | confirmed (with Planet) |
| n08 | Whether space computing beats ground computing: not established | [13][14][16][17] | labelled open |
| n09 | Summary lines | n01 to n08 | no new claims |

## Dropped or softened while writing
- "Starcloud-2 launches October 2026": it slipped to 2027 [9]; not stated as a launch.
- SpaceX S-1 "unproven technologies" quote, the xAI deal value, and the "4x the cost of ground" figure: weak or conflicting
  sourcing (see RESEARCH.md "Could not confirm").
- Starcloud CEO's "in 10 years nearly all new data centers in space": kept in RESEARCH.md as his prediction, cut for time.
- "Hotter than the Sun side / colder than the shade side" ISS skin temperature numbers: no source found this session; not used.

## Fact-check status (11/4)
Codex reviewed 11/3-11/4; fixes applied by cloud Claude, see `FACTCHECK-codex.md` 'Applied (cloud, 11/4)'. Extra sources used for the n04 freeze check: NASA NTRS 20000032541 (ISS radiator pointing also prevents freezing) and SAE 981731 / 961387 (ammonia freeze point about -77.7 C; wing angle balances heat rejection against freezing). Claims in the table above are superseded by the softened wording in script.json where they differ (n01, n02, n03, n04, n05, n06 Starcloud, n07, n08 Google, n09).
