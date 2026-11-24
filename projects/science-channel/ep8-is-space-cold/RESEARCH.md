# Ep 8 research: Is space cold?

Researched 2026-11-03 by a cloud Claude session for the Heartbeat Observatory Science channel. Science only. Every claim has a
source number; the list is at the bottom. **[GK]** = standard textbook physics, no single source needed. "Not established" = the
evidence is thin. **Note on method:** in this cloud session WebFetch was blocked for nasa.gov, wikipedia.org and spectrum.ieee.org,
so these facts come from WebSearch result summaries of the pages listed. Codex should open the primary pages before render.

**Watch-outs for the script (read first):**
- **"Space has a temperature" needs care.** The 2.7 K figure is the cosmic microwave background, the leftover glow of the Big
  Bang. A near vacuum has almost no particles, so "temperature" there mostly means that radiation. [1]
- **In sunlight, space hardware is often too hot, not too cold.** Sunlight heats anything it hits; the cold sink is only cold
  for a surface that faces away from the Sun and Earth. [1][2][GK]
- **The ISS 70 kW figure is the original design number.** NASA notes heat loads have grown since 2010. Say "built for about
  seventy kilowatts", not "rejects seventy kilowatts today". [2][3]
- **Space data centers: nothing at scale exists yet.** One satellite with one H100 chip (Starcloud-1) is the largest real
  demonstration found. Everything else is filings, plans and models. Whether it pays off: **not established.** [8][9][10][11]
- **Starcloud-2 slipped from October 2026 to 2027** (company statement reported 21 Aug 2026). Do not say it launched. [9]

---

## 1. The question, in one line
Space is extremely cold. So why is cooling things in space hard?

**Short answer:** Cold is not the same as cooling. In a vacuum there is no air or water to carry heat away, so heat can only
leave as infrared glow (radiation). That glow is slow at everyday temperatures, so spacecraft need big radiator surfaces.

---

## 2. How cold is space?
*Summary: the background glow of the universe is about 2.7 K, just above absolute zero, but a vacuum is a blanket, not a fridge.*
- The cosmic microwave background has a uniform temperature of about 2.725 K (about minus 270 C). [1]
- In empty space there are almost no atoms to bump into a thermometer, so "the temperature of space" really means the
  temperature of that background radiation. [1]
- Conduction and convection can't happen in empty space because there is no matter to carry them; heat moves only by
  radiation, slowly. [1]
- Space.com notes an exposed person would die from the lack of air and pressure long before they froze. [1] (Not used in script.)
- Objects near the Sun are heated by sunlight, so their temperature can be far above 2.7 K. [1][GK]

## 3. Three ways heat moves, and why only one works in space
- **Conduction:** heat passing through touch (a pan on a stove). [GK]
- **Convection:** a moving fluid, air or water, carrying heat away (a fan, a car radiator). [GK]
- **Radiation:** every warm object glows in infrared light and that light carries energy away, even through a vacuum. [GK]
- A vacuum flask (thermos) keeps drinks hot by surrounding them with a vacuum, which blocks conduction and convection. [1][GK]

## 4. The Stefan-Boltzmann law, plain words
- Heat radiated = area x emissivity (how good the surface is at glowing, 0 to 1) x a constant (5.67 x 10^-8 W per square meter
  per K^4) x absolute temperature to the fourth power. [4][5]
- In plain words: twice the area, twice the heat. Twice the absolute temperature (counted from absolute zero), sixteen times
  the heat (2 x 2 x 2 x 2). [4][GK]
- Worked number (our own arithmetic from the law): a perfect black surface at 300 K (27 C, room temperature) radiates about
  460 W per square meter of face. 5.67e-8 x 300^4 = 459 W/m^2. [4][GK]
- Real radiators have emissivity below 1 and must also deal with sunlight and Earth's glow falling on them, so real needs are
  larger. [4][5]
- Starcloud's own white paper (as reported) estimates a radiator at about 20 C emits about 633 W per square meter, counting both
  sides; it calls that far slower than water cooling of chips on Earth. [10] (Two-sided figure; not used in script.)

## 5. The International Space Station's radiators
*Summary: the ISS has a second set of "wings" just for throwing away heat.*
- The External Active Thermal Control System uses two loops of liquid anhydrous ammonia that carry heat to six radiators,
  three on the starboard side and three on the port side. Each radiator has eight panels. [2][3]
- The radiator assembly (Heat Rejection Subsystem) was designed to provide the station's 70 kW heat rejection need. [2]
  Since 2010 heat loads have increased (NASA ICES presentation), so 70 kW is the design figure. [3]
- Each radiator is about 75 feet (about 23 m) long when deployed; each of the eight panels is about 11 feet (about 3.4 m) wide.
  It folds to under 3 feet for launch. (Boeing 2002 release and NASA photo captions; Lockheed Martin 2002.) [6]
  - Comparison: a tennis court is 23.77 m long. [GK] So "about the length of a tennis court" is fair.
- Ammonia freezes at about minus 77.7 C (minus 108 F). Flight controllers steer the radiator wings in a closed loop, measuring
  the ammonia coming out, to reject enough heat without letting it freeze. [2]
- Radiators are kept out of direct sunlight where possible and pointed at the cold of deep space. [3]
- Recent real event: a radiator panel's face sheet peeled from its honeycomb core; the radiator was isolated, vented, and
  brought back into service in January 2025 to add heat rejection. [2] (Not used in script; good for a later episode.)

## 6. Spacesuits
*Summary: a suit is airtight, so your own body heat would cook you. Water tubes and a sublimator solve it.*
- A person on a spacewalk makes about 70 to 730 W of heat, depending on how hard they work (NASA paper). [7]
- The Liquid Cooling and Ventilation Garment (LCVG) is a close-fitting undergarment threaded with tubes; cool water flows
  through and absorbs body heat. [7]
- The warmed water goes to the backpack's sublimator: water freezes on a porous plate and the ice sublimates (turns straight to
  vapor) into vacuum, carrying heat away. This approach has flown since Apollo. [7]
- About 3.6 kg (8 lb) of water is lost to space per astronaut per typical spacewalk. [7]
- NASA notes that without control, the astronaut would swing between "heat stroke and frostbite"; a valve adjusts flow. [7]
- Newer designs: NASA's Spacesuit Water Membrane Evaporator (SWME) for next-generation suits; Axiom and Prada showed an LCVG for
  the AxEMU suit for Artemis (company announcement). [7] (Not used in script.)

## 7. The debate: data centers in space (as of November 2026)
*Summary: free, nearly constant sunlight is real; so is the radiator problem. No one has built one at scale.*

**The case for (who is proposing them)**
- **Starcloud** (US startup, Nvidia-backed): Starcloud-1 reached orbit on 2 Nov 2025 on a SpaceX rideshare with one Nvidia H100
  GPU. On 10 Dec 2025 it said it had trained Andrej Karpathy's NanoGPT on Shakespeare in orbit and run Google's Gemma (inference
  only). [8] Raised a $170M Series A (Mar 2026) and a $250M extension (Aug 2026). [9][10] Long-term vision: a solar array
  about 4 km by 4 km powering a 5 GW data center; CEO Philip Johnston predicts that "in 10 years, nearly all new data centers will
  be being built in outer space" (his prediction). [10] **Starcloud-2 (two 8 kW satellites) slipped to 2027.** [9]
- **Google, Project Suncatcher** (announced Nov 2025, a research "moonshot"): solar-powered satellites carrying TPU chips,
  linked by lasers, in a dawn-dusk sun-synchronous orbit (near-constant sunlight). Two prototype satellites with Planet targeted
  for early 2027. Google says panels in the right orbit can be up to 8 times more productive than on Earth. Its Trillium TPU
  was proton-beam tested for radiation. Sundar Pichai acknowledged thermal management and reliability are big challenges. [11]
- **SpaceX:** FCC application filed 30 Jan 2026 for an "Orbital Data Center System" of up to 1 million solar-powered satellites,
  500 to 2,000 km up. No timeline and no hardware or mass details in the filing. SpaceX also acquired xAI (Feb 2026). [12]
- **Blue Origin:** filed 19 Mar 2026 for a 51,600-satellite orbital data center network, "Project Sunrise". [12]
- The general pitch: near-constant sunlight with no night or clouds in the right orbit, no land or water use, no permits. [10][11]

**The case against / what experts say**
- **World Economic Forum (June 2026):** cooling is "the real obstacle"; about 1,600 square meters of radiator per megawatt; at
  ISS-like hardware, roughly 100 tonnes of radiators per megawatt. Frames it as serious but early. [13]
- **IEEE Spectrum:** one Nvidia H100 draws 700 W and needs about 1.4 square meters of radiator at 60 C. Reporter Dina Genkina
  noted Starcloud-1's radiator was too small to let its chip run at full power. [14]
- **Durability:** radiators and coatings face UV, atomic oxygen, debris strikes and temperature swings with no repair crew. [15]
- **Launch cost:** Orbital (a startup) CEO Euwyn Poon said "the economics of launch don't quite work yet," citing about $7,000
  per kg on Falcon 9 (The Register, 15 Apr 2026). [16]

**The other side of the thermal argument**
- **Forethought** (independent research group) modelled radiators at only about 14% of system mass and about 5% of cost in its
  conservative case, and found launch cost is by far the most sensitive number; orbital data centers could compete if launch
  reaches about $100 per kg. [17]
- Analysts at Mach33 framed it as not "whether cooling is physically possible" (it is) but what the best operating point is. [15]

**Verdict for the episode:** physics allows it; the open questions are radiator mass and size, durability, and launch cost.
Whether space data centers will be cheaper than ground ones: **not established.**

---

## Sources (accessed 2026-11-03)
1. Space.com, "How cold is space?": https://www.space.com/how-cold-is-space
2. NASA NTRS, ICES 2026 paper on an ISS radiator face-sheet peel (EATCS description, ammonia freeze point, radiator pointing,
   Jan 2025 reintegration): https://ntrs.nasa.gov/citations/20260002946 ; SAE 951651, "Space Station Heat Rejection Subsystem
   Radiator Assembly Design and Development" (70 kW): https://saemobilus.sae.org/papers/space-station-heat-rejection-subsystem-radiator-assembly-design-development-951651
3. NASA NTRS, ICES 2026 presentation (two loops, 3 + 3 radiators, 8 panels each, loads up since 2010): https://ntrs.nasa.gov/citations/20260005213 ;
   NASA ISS ATCS overview: https://www.nasa.gov/wp-content/uploads/2021/02/473486main_iss_atcs_overview.pdf
4. HyperPhysics, Stefan-Boltzmann law: https://hyperphysics.gsu.edu/hbase/thermo/stefan.html ; Energy Education: https://www.energyeducation.ca/encyclopedia/Stefan-Boltzmann_law
5. NASA NTRS, spacecraft thermal course notes (Cottingham, 2023): https://ntrs.nasa.gov/api/citations/20230001953/downloads/ENAE%20691%20Spring23%20Thermal%20Cottingham.pdf
6. Boeing, 24 Sep 2002, S1 truss (radiators about 75 ft long, 11 ft wide): https://boeing.mediaroom.com/2002-09-24-First-of-Twin-Boeing-built-Trusses-Ready-for-International-Space-Station ;
   Lockheed Martin release, Oct 2002: https://www.globalsecurity.org/space/library/news/2002/space-021009-lockheed-martin01.htm ; Gunter's Space Page, ITS S1: https://space.skyrocket.de/doc_sdat/its-s1.htm
7. NASA NTRS, spacesuit heat rejection (70 to 730 W; about 3.6 kg water per EVA; sublimator): https://ntrs.nasa.gov/api/citations/20120003778/downloads/20120003778.pdf ;
   https://ntrs.nasa.gov/api/citations/20110023272/downloads/20110023272.pdf ; sublimator and SWME: https://ntrs.nasa.gov/api/citations/20140003403/downloads/20140003403.pdf
8. Starcloud-1 and in-orbit training: GeekWire, Dec 2025: https://www.geekwire.com/2025/starcloud-power-training-ai-space/ ; OODA Loop: https://oodaloop.com/briefs/technology/greetings-earthlings-nvidia-backed-starcloud-trains-first-ai-model-in-space-as-orbital-data-center-race-heats-up/
9. TechCrunch, 21 Aug 2026, Starcloud raises $250M, 2027 rideshares for two 8 kW satellites: https://techcrunch.com/2026/08/21/starcloud-raises-200-million-for-orbital-data-centers-as-launch-options-dry-up/
10. NVIDIA blog on Starcloud (4 km x 4 km, 5 GW, Johnston quotes): https://blogs.nvidia.com/blog/starcloud/ ; Starcloud site: https://starcloud.com/ ; SiliconANGLE, 30 Mar 2026: https://siliconangle.com/?p=736852
11. Google Project Suncatcher: Satellite Today, 6 Nov 2025: https://www.satellitetoday.com/technology/2025/11/06/google-targets-in-space-computing-with-project-suncatcher-moonshot/ ; InfoQ: https://www.infoq.com/news/2025/11/google-suncatcher-space ; Tom's Hardware: https://www.tomshardware.com/tech-industry/artificial-intelligence/google-exploring-putting-ai-data-centers-in-space-project-suncatcher-wants-to-harness-in-orbit-solar-power-to-scale-ai-compute
12. SpaceX FCC filing: Bloomberg, 31 Jan 2026: https://www.bloomberg.com/news/articles/2026-01-31/spacex-seeks-fcc-nod-to-build-data-center-constellation-in-space ; Satellite Today, 2 Feb 2026 (xAI): https://www.satellitetoday.com/connectivity/2026/02/02/spacex-acquires-xai-<redacted>/ ;
    Blue Origin Project Sunrise (51,600): https://www.softwareseni.com/spacex-and-the-million-satellite-fcc-filing-orbital-data-centre-plans-at-scale/ (secondary; confirm against the FCC docket)
13. World Economic Forum, June 2026, "Why cooling is the real obstacle to space-based data centres": https://www.weforum.org/stories/2026/06/space-data-centres-cooling/
14. IEEE Spectrum, "Why Thermodynamics Rules Future Orbital Data Centers": https://spectrum.ieee.org/orbital-data-centers-heat ; "Orbital Data Centers: Why the Hype Outpaces Reality": https://spectrum.ieee.org/orbital-data-center-hype
15. SatNews, 17 Mar 2026, "The Physics Wall": https://satnews.com/2026/03/17/the-physics-wall-orbiting-data-centers-face-a-massive-cooling-challenge/ ; SpaceComputer landscape analysis: https://blog.spacecomputer.io/cooling-for-orbital-compute/
16. The Register, 15 Apr 2026, "Orbital datacenter startup admits launch economics don't fly": https://www.theregister.com/2026/04/15/orbital_space_datacenter_startup_economics/
17. Forethought, "Will we really put data centers in space?": https://www.forethought.org/research/will-we-really-put-data-centers-in-space

## Could not confirm (do not state as fact in the episode)
- Total ISS radiator area in square meters (no primary figure found; 6 x 23 m x 3.4 m is our own estimate, about 470 m^2 one side).
- Today's actual ISS heat rejection (only the 70 kW design figure and "loads have grown since 2010").
- A NASA figure for the EMU's cooling capacity in watts (only the 70 to 730 W body-heat range).
- SpaceX's reported S-1 risk wording ("significant technical complexity and unproven technologies"): one secondary source only. Dropped.
- The SpaceX/xAI deal value ($250B vs $1.25T combined, sources conflict). Dropped.
- Independent "orbital compute costs about 4x ground" figure (unclear sourcing). Dropped.
- Whether Starcloud-1's chip ever ran at full power for long (IEEE says the radiator limited it).
