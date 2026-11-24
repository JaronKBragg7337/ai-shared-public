# Science 8.11 "The Pioneer Anomaly": research notes

Written 2026-11-15 by Claude Code (Opus 5.5), research + script lane only (no GPU, no render). Every number below was read
from the primary paper text (arXiv full text pulled and searched) unless marked otherwise. Claim table with status: SOURCES.md.

## Warnings first (where the brief / task numbers are slightly off)

1. **"Heat from the RTGs bouncing off the back of the dish explains essentially all of it" is not quite what the 2012 paper says.**
   Turyshev et al. 2012 (PRL 108, 241101): the thermal model gives **about 80%** of the Doppler-fitted acceleration, of which
   **about 35% comes from the RTGs and about 45% from electrical heat** (the electronics in the equipment box). The remaining
   ~20% is **inside the error bars** (thermal model total uncertainty 26.3%, dominated by a 25% term for RTG surface coating
   degradation). Their conclusion: no statistically significant anomaly remains. So the electronics are the bigger share, and
   "all" should be "about 80%, and the rest fits inside the uncertainty". The script says it that way.
2. **Telemetry recovery started in 2004, not 2011.** Turyshev began gathering records in 2004 (NASA/JPL news, July 2012); the
   Planetary Society appealed to members to fund it; recovered Doppler data were reported complete in Toth & Turyshev 2006.
   The 2011 paper (PRL 107, 081103) is the extended Doppler analysis; the 2012 paper is the thermal result.
3. **The 1998 PRL value is ~8.5 x 10^-10 m/s^2**, not 8.74. The famous (8.74 +/- 1.33) x 10^-10 m/s^2 is the 2002 PRD value
   (the papers write it as 10^-8 cm/s^2; same thing).
4. **Pioneer 11 last contact: sources disagree on the month, and the reason is not only power.** Anderson 2002: power nearly exhausted by September 1995, and Earth's motion carried it out of the antenna's view. NASA's mission pages say the mission ended 30 September 1995 with
   the last transmission; Anderson et al. 2002 and the 2012 JPL release say November 1995. Script just says "1995".
5. **Pioneer 10 last signal: 23 January 2003** (NASA); some 2003 releases say 22 January (time zone). Script says "January 2003".
6. **RTG heat:** "about 2.5 kW thermal" is supported by Turyshev et al. 2012, which uses Q_rtg = 2578 W for all four RTGs at
   1 July 1972. Note a SNAP-19 table elsewhere gives ~525 W per unit (2.1 kW for four); we use the paper's value.
   "~160 W electric": Anderson et al. 2002 says approximately 160 W **before launch** (about 65 W by ~2001).
7. **Rievers & Laemmerzahl 2011 is in Annalen der Physik 523, 439** (doi 10.1002/andp.201100081). Francisco, Bertolami, Gil,
   Paramos 2012 is **Physics Letters B 711, 337-346** (arXiv:1103.5222). Both confirmed.

## 1. The spacecraft (Anderson et al. 2002, PRD 65, 082004, Section II)

- Pioneer 10 launched **2 March 1972** local time (3 March UTC; Atlas/Centaur, Cape Kennedy); Jupiter encounter **4 December 1973** (UTC; 3 Dec in US
  time). Pioneer 11 launched **5 April 1973** local time (6 April UTC).
- Mass at launch 259 kg each (36 kg hydrazine). Nominal Pioneer 10 mass used in the analysis: 241 kg.
- High-gain dish: **2.74 m** diameter, 46 cm deep, aluminum honeycomb. Spacecraft 2.9 m long.
- Equipment compartment: hexagonal, 71 cm sides, 36 cm deep. Louvers under the platform for thermal control.
- **Two three-rod trusses, each holding two SNAP-19 RTGs** (four total, 13.6 kg each), about 3 m from center.
- **Magnetometer** on a third single-rod boom about **6.6 m** from center.
- RTG fuel Pu-238, half-life 87.74 yr. Each SNAP-19 converts **5 to 6 percent** of the heat to electricity. Total about
  **160 W electrical before launch**.
- Radio: transmits continuously at **8 W**, about **2.29 GHz** (S-band) through the dish; uplink ~2.11 GHz.
- Pioneer 10 spins ~4.8 rpm.

## 2. The anomaly

- **When/where:** Beginning in **1980, at about 20 AU**, once solar radiation pressure had dropped below 5 x 10^-10 m/s^2, the
  largest residual was a constant sunward bias (Anderson 2002, intro).
- **1998:** Anderson, Laing, Lau, Liu, Nieto, Turyshev, PRL 81, 2858 (1998): apparent anomalous constant acceleration of about
  **8.5 x 10^-8 cm/s^2** sunward, from Pioneer 10/11 (also discussed Galileo and Ulysses).
- **2002:** same authors, PRD 65, 082004: **a_P = (8.74 +/- 1.33) x 10^-10 m/s^2**, sunward. Data: Pioneer 10 from 3 Jan 1987 to
  22 Jul 1998, **40 to 70.5 AU**; Pioneer 11 from 5 Jan 1987 to 1 Oct 1990 (coherent radio lost), **22.42 to 31.7 AU**.
- **2011:** Turyshev, Toth, Ellis, Markwardt, PRL 107, 081103: extended data set confirms the sunward acceleration but favors
  one that **decays with time** (~2 x 10^-11 m/s^2 per year); direction not pinned down (Sun vs Earth vs spin axis). So the script says "roughly toward the Sun".

## 3. Proposed explanations

Anderson 2002 has a section titled "Dark matter or modified gravity?" and discusses MOND (Milgrom), dark matter models and
other new-physics suggestions, alongside conventional ones (gas leaks, heat, drag, clock effects). Turyshev & Toth 2010
(Living Reviews in Relativity 13, 4) reviews the proposed mechanisms and, at that time, says the anomaly was still unexplained.
Wikipedia's list (secondary): thermal recoil, Kuiper belt / dark matter gravity, drag, gas leaks, observational errors, clock
acceleration, MOND, modified inertia, cosmological links (a_P is close to c x H0, now thought a coincidence).

## 4. The data rescue (NASA/JPL news release July 2012; phys.org copy)

- 2004: Turyshev starts gathering records; collected **more than 43 GB** (Doppler + telemetry): JPL navigators' files, more
  than a dozen boxes of magnetic tapes **under a JPL staircase**, NSSDC files at Goddard, magneto-optical tapes at Ames. He
  rescued a vintage tape machine about to be discarded.
- **Viktor Toth**, programmer in Canada, wrote software to read the telemetry tapes and clean the data.
- **The Planetary Society** appealed to members for funding; NASA later funded it too.
- Toth & Turyshev 2006 (arXiv:gr-qc/0603016): Doppler data collection complete; telemetry processing in progress.

## 5. Thermal models

- **Rievers & Laemmerzahl 2011, Annalen der Physik 523, 439** (ZARM, Bremen): high-precision finite-element thermal model;
  thermal recoil "likely resolves" the Pioneer 10 anomaly; worst-case modeling error ~10%.
- **Francisco, Bertolami, Gil, Paramos 2012, Physics Letters B 711, 337** (Lisbon): reflection model (Phong shading); thermal
  acceleration 26 yr after launch **(5.8 +/- 1.3) x 10^-10 m/s^2**, i.e. **44% to 96%** of a_P; earlier work by the same
  group had 33% to 67%.
- **Turyshev, Toth, Kinsella, Lee, Lok, Ellis 2012, PRL 108, 241101:** finite-element model of Pioneer 10 driven by recovered
  flight telemetry; thermal recoil magnitude, time behavior and direction similar to the anomaly. Thermal estimate ~80% of the
  Doppler estimate (~35% RTG, ~45% electrical). Remaining 20% within the 1-sigma error ellipses. Concluding phrase: "no
  anomalous acceleration remains". Exponential fits: Doppler tau = 28.8 +/- 2.0 yr, a0 = (10.1 +/- 1.0) x 10^-10 m/s^2 (t0 =
  1 Jan 1980); thermal tau = 36.9 +/- 6.7 yr, a0 = (7.4 +/- 2.5) x 10^-10 m/s^2. Caveats they list: Pioneer 11 not analyzed to
  the same depth (spot checks fine); spin-down not addressed; outgassing not addressed.
- Heat budget scale: Anderson 2002 says only **about 63 W of directed power** would explain the anomaly, against ~2000 W of
  RTG heat at that time. Check: F = P/c, so P = m a c = 241 kg x 8.74e-10 m/s^2 x 3.0e8 m/s = **63 W**. Matches.

## 6. Pioneer plaque (Planetary Society; NASA)

6 x 9 inch (15 x 23 cm) gold-anodized aluminum plaque on both probes; designed by Carl Sagan and Frank Drake, artwork by
Linda Salzman Sagan. Shows a man and woman, a hydrogen hyperfine transition symbol, a pulsar map locating the Sun, and the
planets with the probe's path from Earth.

## 7. Where they are now (estimate, from a live tracker)

Heavens-Above "Spacecraft escaping the Solar System" read on 2026-11-15: **Pioneer 10 142.3 AU** from the Sun (11.86 km/s),
**Pioneer 11 119.7 AU** (11.12 km/s). Cross-check: Universe Magazine had Pioneer 10 at 136.18 AU on 3 Apr 2024; at ~2.5 AU/yr
that gives ~142.7 AU in Nov 2026. Consistent. Status: ESTIMATE (computed ephemeris, no contact since 2003).
One-way light time to Pioneer 10 now: 142.3 AU x 1.496e11 m / 3e8 m/s = about 19.7 hours.

## 8. The concrete picture (our math; constant a_P assumed)

a = 8.74e-10 m/s^2. Year = 3.156e7 s. Formulas: speed change v = a t; position shift d = 1/2 a t^2.

| Time | Speed change | Position shift |
|---|---|---|
| 1 year | 0.0276 m/s = 2.8 cm/s (0.10 km/h) | 0.5 x 8.74e-10 x (3.156e7)^2 = 4.35e5 m = **435 km** |
| 10 years | 0.276 m/s = **0.99 km/h** | **43,500 km** (more than Earth's 40,075 km circumference) |
| 11.5 years (1987-1998 data span) | 0.32 m/s | 57,600 km |
| 20 years | 0.55 m/s | 174,000 km (0.45 of the Earth-Moon distance) |

- Earth gravity / a_P = 9.81 / 8.74e-10 = **1.12 x 10^10**, about eleven billion.
- 435 km is about the driving distance Chicago to Detroit (~450 km by road, ~380 km straight line); script says "about four
  hundred kilometers". Wikipedia's secondary summary says positions predicted a year ahead were "some 400 km off" and the speed
  loss was "1 km/h over ten years": both agree with our math.
- This is OUR SIMPLIFICATION: the 2011 analysis found the pull slowly decays, so the real shift differs a little.

## Sources (URLs, read 2026-11-15)

- Anderson et al. 1998: https://arxiv.org/abs/gr-qc/9808081 (PRL 81, 2858)
- Anderson et al. 2002: https://arxiv.org/abs/gr-qc/0104064 (PRD 65, 082004), full text searched
- Turyshev & Toth 2010 review: https://arxiv.org/abs/1001.3686 (Living Rev. Relativ. 13, 4)
- Turyshev, Toth, Ellis, Markwardt 2011: https://arxiv.org/abs/1107.2886 (PRL 107, 081103)
- Rievers & Laemmerzahl 2011: https://arxiv.org/abs/1104.3985 (Ann. Phys. 523, 439), full text searched
- Francisco et al. 2012: https://arxiv.org/abs/1103.5222 (PLB 711, 337), full text searched
- Turyshev et al. 2012: https://arxiv.org/abs/1204.2507 (PRL 108, 241101), full text searched
- Toth & Turyshev 2006: https://arxiv.org/abs/gr-qc/0603016
- NASA/JPL news July 2012: https://www.jpl.nasa.gov/news/study-finds-heat-is-source-of-pioneer-anomaly/ (read via
  https://phys.org/news/2012-07-source-anomaly.html; JPL page reset the connection)
- NASA, Pioneer 10 last signal: https://science.nasa.gov/missions/pioneer/pioneer-10-sends-last-signal/
- Planetary Society plaque: https://www.planetary.org/articles/0120-the-pioneer-plaque-science-as-a-universal-language
- Heavens-Above: https://heavens-above.com/SolarEscape.aspx
- Wikipedia (secondary cross-check only): https://en.wikipedia.org/wiki/Pioneer_anomaly
