# Space Now 11.1 "MMX: ten grams from Phobos" - sources and what each claim rests on (2026-10-17, Claude Fable 5.1)

Status date on screen: Oct 17, 2026. All primary pages read the same night (WebFetch / downloaded PDF). Secondary pages only
where marked.

| Claim (segment) | Source | Status |
|---|---|---|
| Launch 04:41:03 JST Oct 20, 2026 = 3:41 PM ET Oct 19; H3 flight 10; Tanegashima (Yoshinobu); backup Oct 21-Nov 7 with a time per day (s1, s2, s13) | JAXA press release 2026-08-20 (jaxa.jp/press/2026/08/20260820-1_j.html); ESA "Mars moon lander set to launch on 19 October" (20:41 BST / 21:41 CEST) | confirmed, scheduled |
| H3-24L = 2 LE-9 engines, 4 SRB-3 boosters, long fairing (s2) | JAXA launch plan PDF jaxa20260820-1_01.pdf, section 1.4 | confirmed |
| Flight sequence: SRB pairs 1:56 / 1:58, fairing 3:17, stage-1 cutoff 4:52, separation 4:59, stage-2 burn 5:12-10:40, burn 2 1:03:57-1:10:21, MMX separation 1:11:12 at 592 km, 11.2 km/s (s3) | JAXA launch plan PDF, section on flight sequence (Oct 20 JST case; times shift on backup days, said on screen) | confirmed, published plan |
| JAXA streams the launch live in Japanese and English (s2) | ESA launch article | confirmed |
| Launch mass 4,480 kg; 3 modules (outbound / exploration / return); mission 5 years; instrument list incl. P-SMP provided by NASA, MIRS by CNES, MEGANE by NASA, IDEFIX by CNES/DLR (s4, s10, s11) | JAXA launch plan PDF, table 4. (ESA factsheet says "about 4,200 kg incl. fuel" - JAXA's newer figure used; "most of it fuel" dropped after Codex) | confirmed |
| Module roles: propulsion = travel to Mars, cast off; exploration = legs, samplers, instruments; return = engine, solar wings, antenna, capsule (s4) | ESA MMX factsheet; DLR facts and figures; JAXA mission flow (propulsion module absent after Mars orbit insertion) | confirmed |
| Partners JAXA + NASA, CNES, DLR, ESA (s4) | ESA launch article; JAXA launch plan | confirmed |
| Phobos ~27 x 22 x 18 km, dark (albedo ~0.07), ~6,000 km above Mars, period 7 h 39 min (s5) | NASA Science Phobos page; verified for Science 8.6 (projects/science-channel/ep6-phobos/SOURCES.md) | confirmed |
| Capture vs giant impact, both under study; impact fits the circular equatorial orbit, capture fits the dark asteroid-like surface (s5) | JAXA mission site (both hypotheses under study); ESA launch article; Science 8.6 sources (Paetzold 2025) | confirmed; reasoning worded as "fits", both called hypotheses |
| Labs read minerals, water, organic matter, isotopes, age (s6) | JAXA science page (water, organics, origin, "when it migrated"); JAXA MMX science goals (isotopes, radiometric dating; from 8.6 sources) | confirmed |
| Hyodo's test: impact debris ~50% Martian material with volatiles baked out; capture = outer-solar-system body with water/organics (s6) | JAXA MMX News "Why explore the moons of Mars?" (mmx-news.isas.jaxa.jp/?p=1446), explanations by Ryuki Hyodo (ISAS/JAXA) | confirmed, attributed to Hyodo |
| Mars ejecta on Phobos: ~340 ppm statistical, ~760 ppm with rare large impacts; >= ~34 grains in 10 g at 0.3 mm grains (s7) | Hyodo et al. 2019, arXiv 1912.12056; JAXA ISAS summary (10-100x earlier estimates). On screen and in narration: MODEL ESTIMATE | confirmed as a model |
| Timeline: Mars orbit Aug 2027, Phobos QSO from Sept 2027, Idefix early 2029, landing + sampling 2030, return 2031 (ESA) vs rover 2029, sampling 2029, return flight 2030, Earth 2031 (DLR) (s8, s12) | ESA launch article; DLR facts and figures; JAXA mission flow (1 year out, ~5 years total). Disagreement stated on screen and in narration | confirmed, published plans differ |
| First spacecraft to orbit Phobos (quasi-satellite orbit); dozens of candidate landing sites (s8) | ESA launch article; JAXA mission flow | confirmed |
| Idefix 25 kg (~15 g weight on Phobos), CNES + DLR, release ~40 m, rights itself, ~100 days / three months, Raman (RAX) + radiometer (miniRAD) + cameras, ~1 mm/s (s9) | DLR facts and figures; DLR news 2026 "Off to the moons of Mars" (~40 m, rights itself, ~3 months); ESA (15 g). "Four wheels": DLR 2023 news (older) | confirmed; 40-100 m (2023) replaced by ~40 m (2026) after Codex |
| Radio delay up to 44 min round trip (s10) | JAXA MMX mission site | confirmed |
| C-SMP corer > 2 cm with shape-memory alloy; P-SMP nitrogen gas near a footpad; P-SMP provided by NASA (s10) | JAXA MMX News (corer interview; P-SMP flight model); JAXA launch plan table 4 | confirmed |
| Two soft landings, ~2-3 hours on the surface each (s10, s12) | JAXA MMX science page (mmx.jaxa.jp/en/science/) | confirmed (replaced "one or two" after Codex) |
| Instruments TENGOO, OROCHI, LIDAR, MIRS, MEGANE, MSA, CMDM, IREM, SHV 8K + 4K with NHK; Deimos in the second half (s11) | JAXA launch plan table 4; JAXA science page; ESA factsheet; JHU APL MEGANE page | confirmed |
| MEGANE reads gamma rays and neutrons from cosmic-ray hits to get elements (s11) | JHU APL MEGANE page | confirmed |

## What changed after the Codex fact check (gpt-6-luna, high effort, read-only; FACTCHECK-codex.md) - 7 WRONG, all fixed
1. s6 binary "wet vs dry" test + "JAXA's science team says" -> Hyodo's own framing (~50% Martian material, volatiles baked out; capture = outer-solar-system body), attributed to him (JAXA MMX News).
2. s7 "first pieces of Mars brought back on purpose" -> "a spacecraft would be carrying material from Mars home for the first time, mixed into the Phobos dirt" (conditional, model).
3. s9 release "40-100 m" (DLR 2023) -> "about 40 metres" (DLR 2026); "100 days" -> "about three months".
4. s10 "one landing, or two" -> "two soft landings, about two to three hours on the ground each time" (JAXA science page).
5. s11 Deimos "on the way out" -> "later in the mission" (JAXA: second half); cameras "8K and 4K".
6. s12 OPEN list: removed "one landing or two" and "time on the surface"; landing year kept as open (ESA 2030 vs DLR 2029).
7. s13 (and s3) "a year of silence / quiet" -> "roughly a year of cruise".
UNSURE items also softened: "most of it fuel" dropped (s4); "dropped there" -> "cast off once its job is done"; "ten grams is a lot" -> what labs can read; grain count now states the 0.3 mm assumption; "scheduled" added to the launch time in the ledger.

## Not verified / honest limits
- Not heard by a human; Kokoro am_michael pronunciations of Tanegashima, Idefix, MEGANE respelled in "say" fields.
- JAXA leaflet PDF (2024) not readable; its 4,200 kg figure is older than the Aug 2026 launch plan.
- Whether the launch actually goes Oct 20 JST: checked the night of Oct 17, no slip reported (ESA, JAXA pages).
