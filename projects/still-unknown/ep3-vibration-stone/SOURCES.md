# Still Unknown 10.3 "Can vibration cut stone?" - sources and flags (Claude Sonnet 5.5, 2026-10-16)

Web-checked 2026-10-16 unless marked (knowledge). Pillow + numpy + ffmpeg for the boards; two looping Blender 5.1 Cycles macro shots (procedural, no assets; GPU yielded from Sapling for the render, restarted after). Kokoro af_heart narration on CPU. No photographs: every picture is drawn or rendered.

## Ultrasonic machining (documented engineering)
- Thoe, T. B., Aspinwall, D. K., Wise, M. L. H. (1998) "Review on ultrasonic machining", Int. J. Machine Tools & Manufacture 38(4):239-255, doi 10.1016/S0890-6955(97)00036-9. Only citation details and a secondary description of its scope were read (ScienceDirect returned 403). We cite it as "a review that surveys decades of work", not for specific numbers.
- Wikipedia "Ultrasonic machining" (fetched 2026-10-16), which cites Kalpakjian (2008): high-frequency, low-amplitude tool vibration with fine abrasive; usually 18-40 kHz; amplitude 0.05-0.125 mm (another course note gives ~0.01-0.1 mm; screen says "0.1 mm or less"); slurry of boron carbide, aluminium oxide or silicon carbide in water; tool usually low-carbon steel; materials: ceramics, carbides, glass, precious stones, hardened steel; transducers piezoelectric or magnetostrictive; deep holes difficult because slurry does not reach the bottom. (Wikipedia, so a secondary source.)
- History: course notes (UCI project page, Slovak STU lecture, IIT Guwahati ME688) credit Wood and Loomis, 1927, with first discussing it; Balamuth discovered it in 1945. Google Patents GB602801A: priority 1945-04-14, published 1948-06-03, assignee Industrial Research Corp. US 2,580,716 "Method and Means for Removing Material from a Solid Body", L. Balamuth, dated 1 Jan 1952, as cited by a later patent (we did not open the patent itself). First machines: 1951-52 report / 1954 depending on source; screen says sources differ.
- "Not a way to quarry large blocks" is our summary of the process's usual use (holes, cavities, small parts), not a quoted statement.

## Egypt: copper, sand, granite
- Stocks, D. A. (2001) "Testing ancient Egyptian granite-working methods in Aswan, Upper Egypt", Antiquity 75(287):89-94, doi 10.1017/S0003598X00052777 (Cambridge page: abstract extract only; full text paywalled). Experiments done 1999 per Science Frontiers #137. Details read via Hall of Ma'at "Ancient Egyptian Copper Slabbing Saws" (secondary summary of the article): copper blade ~14.5 kg, 1.8 m x 15 cm x 6 mm; quartz sand dry (flat edge) and wet (notched blade); two workers; ~12 cm3/hour in both; Stocks suggested experience could double it; blade pitted, more wear in the wet test; saw marks on granite sarcophagi per Petrie (1883), Reisner (1931), Lucas and Harris (1962). The slot-depth (3 cm x 95 cm in 14 h) and copper-loss (7.5 mm) numbers on popular sites are NOT used: the article text as summarised does not give them.
- NOVA "Secrets of Lost Empires: Obelisk" (PBS) describes the same kind of test; not used for numbers.
- Stocks, D. A., Experiments in Egyptian Archaeology: Stoneworking Technology in Ancient Egypt (Routledge; 2nd ed. 2023). Page figures not checked.
- Drilling: Stocks reports successful bow-driven copper-tube coring of granite with sand (details only in secondary summaries; narration gives no rate).

## The claims
- Dunn, C., "Advanced Machining in Ancient Egypt", Analog, Aug 1984 (text read at gizapower.com/Advanced/Advanced%20Machining.html): Petrie's spiral "sinks .100 inch in the circumference of 6 inches"; Donald Rahn (1983) told Dunn that diamond drills at 900 rpm penetrate 1 inch in 5 minutes = ~0.0002 in/rev; ratio ~500; Dunn proposes ultrasonic machining as "the only method that completely satisfies logic". The modern baseline is a single reported figure, which is why the screen says "figure given to Dunn". "Egyptologists dispute" is supported by search summaries (the Petrie vs Lucas drill debate, Penn Museum Expedition article) that we did not open in full.
- Sound/acoustic levitation: Wikipedia "Acoustic levitation" (fetched 2026-10-16): heaviest far-field levitated object listed as a 30 mm expanded-polystyrene sphere of 0.6 g; near-field levitation can lift "several kilograms" but only hundreds of micrometres above the surface. Andrade, Bernassau, Okina, Adamowski, ICSV24 (London, July 2017): 50 mm sphere held by three 25 kHz transducers (abstract only; not used in narration).
- "Drums and trumpets float stones" stories: retold widely (books, podcasts, videos). We could not find an original film, measurement or primary record. We did NOT verify any named origin (search results gave an unconfirmed Swedish 1939/1961 chain), so the video names none. Callback to ep 10.2 (Coral Castle): sound levitation was one popular theory there; the 1984 NRHP form does not contain it.

## Our arithmetic (shown on screen, labelled)
- Average Great Pyramid block ~2.3 metric tonnes (some encyclopedic sources say 2.5 short tons = 2.27 t; estimates). Weight 2,300 kg x 9.81 = 22.6 kN.
- Idealised plane standing wave, perfect reflection, uniform over a flat 1 m2 underside: radiation pressure = 2I/c, so I = P c / 2 = 22.6 kPa x 343 / 2 = 3.9 MW/m2; p_rms = sqrt(I rho c) with rho c ~ 415 Pa s/m = ~40 kPa; SPL = 20 log10(40,000 / 20e-6) = ~186 dB re 20 uPa. Air ceiling: 194 dB = pressure amplitude equal to 1 atm (101 kPa). Real acoustic radiation forces are nonlinear at these levels; this is order-of-magnitude, labelled "rough".
- Mass ratio: 2,300,000 g / 0.6 g = 3.83 million.
- 12 cm3 = cube of 2.29 cm on a side. Hand strokes ~1-2 per second is our estimate (not from Stocks); 20,000 / ~2 = ~10,000.

## The home test (plan, NOT run)
projects/science-channel/home-test-vibration-cutting/BUILD-SHEET.md (Vex + Claude, 2026-10-11): ultrasonic cleaner ~40 kHz, copper strip, grit, soft stone; same minutes with vibration on vs off. The video says plainly that it has not been run and there is no result.

## Flags (open items)
- Thoe et al. full text, Stocks 2001 full text, and the Penn Museum article were not read; their numbers come from secondary summaries (named above).
- First-machine date and the 1927 Wood and Loomis attribution rest on course notes; the video hedges both ("credited", "sources disagree").
- The 0.1 mm amplitude: the video says "about a tenth of a millimetre or less".
- No physical-evidence claim is made about what the Egyptians did; the video says the experiment shows what can work.

## r2 corrections after Codex fact-check (FACTCHECK-codex.md, read-only, web search)
- s2: "too fast to hear" was WRONG for 18-20 kHz (hearing reaches ~20 kHz). Now "typically twenty to forty thousand times a second, at or above the edge of human hearing". Amplitude now "a tiny fraction of a millimetre" (screen: micrometres up to about 0.1 mm; sources range from a few micrometres to ~0.125 mm).
- s3: "Not the tool. The grit." softened to "the loose grit does most of the cutting; the tool supplies and shapes the impacts" (cavitation and direct effects also contribute).
- s4: GB602801 is an application by Industrial Research Corporation (J. O. Farrer named in the abstract); histories link it to Balamuth, so the video says so. US 2,580,716 to Balamuth, 1952 (confirmed by Codex). "Sources disagree which machine was first" dropped; now "early to mid nineteen fifties".
- s5: "springy metals mostly absorb the hits" was misleading; now ductile metals deform instead of chipping, so it is usually less efficient on them. "Not a way to quarry blocks" now "used for holes and cavities; not documented as a way to quarry large blocks".
- s8: "ten thousand times as many hits" was an invalid comparison; now "ten thousand times the vibration rate. Not a comparison of cutting speed", and the shared principle (loose abrasive, softer tool) replaces "cousin".
- s9: "Egyptologists dispute that" was unsupported as a sweeping claim; now "experimental archaeologists have tested copper tubes with sand, and cut granite" and "in the literature we read" for the no-device statement. Dunn's modern figure was a private communication about one diamond-drilling setup (screen: "figure given to Dunn, 1983").
- s10: the drums-and-trumpets story is a modern story usually set in Tibet, not Egyptian evidence (said now). 0.6 g is "one published far-field demonstration", not a "record". Near-field: several kg (Codex: a published system supported ~10 kg) at tens to hundreds of micrometres.
- s11: air limit now "roughly 191 to 194 dB depending on convention (low-pressure half reaches vacuum)". 186 dB stays labelled ideal/rough.
- s12: Codex: an ultrasonic cleaner is NOT a valid ultrasonic-machining rig (cavitation bath, no driven tool). The video no longer calls it a test anyone can do; it says the rough plan uses a cleaner, would only be a first look, and has not been run. Heading is now "what a strong test looks like".
- s13/s14: ledger says "some Egyptian granite objects carry saw cuts" and "Dunn's feed-rate comparison" is the disputed part. "Not ruled out, either: new evidence could settle it" kept (channel rule); Codex flags it as unfalsifiable-sounding opinion.
- Kept: block mass ~2.3 t (NOVA/PBS estimate), 12 cm3/h and the experience-doubling suggestion (Hall of Ma'at summary of Stocks), Petrie 1883 saw cuts on Khufu's sarcophagus, Dunn 0.100 vs 0.0002 in/turn = 500 x and his ultrasonic proposal (Analog 104(8), Aug 1984).
