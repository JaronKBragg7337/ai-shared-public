# Codex fact check: Science 8.11 The Pioneer Anomaly

Run 2026-11-15 by Claude Code (Opus) with: codex exec -s read-only --skip-git-repo-check -C <this folder> (web search on). Raw output below, then what was applied.

The strongest fixes are in scenes 05, 11, 12, 13 and 14: distinguish transmitted radio power from electricity consumed, qualify the heat comparison, credit the telemetry software carefully, and explain Pioneer 11’s loss of contact separately. Section 8’s arithmetic checks out under its stated constant-acceleration assumption.

The status applies to the factual claims in each scene or row. Fictional staging and jokes are not flagged.

### Script scenes

- **s01, UNSURE:** The local brief says Grok suggested the topic as “Still Unknown,” but I could not verify the original X exchange or the words displayed as a quote. Fix: Present the wording as a paraphrase unless the original post confirms it. [Brief](</C:/Users/lilli/AI-Shared/projects/heartbeat-tv/pioneer-episode/BRIEF.md>)
- **s02, OK:** This is fictional staging, with no factual claim requiring correction. [Script](</C:/Users/lilli/AI-Shared/projects/heartbeat-tv/pioneer-episode/script.json>)
- **s03, OK:** The rocket trip is fiction. “A fifty year head start” is a reasonable approximation for a spacecraft launched in 1972. [NASA](https://www.nasa.gov/history/50-years-ago-pioneer-10-launches-to-explore-jupiter/)
- **s04, OK:** The launches were March 2, 1972 and April 5, 1973 in Florida local time. In UTC they were March 3 and April 6. The Jupiter first and dish size check out. Labeling the launch dates as local would avoid confusion. [NASA Pioneer 10](https://science.nasa.gov/mission/pioneer-10/), [NASA Pioneer 11](https://science.nasa.gov/mission/pioneer-11/)
- **s05, WRONG:** Eight watts is approximately the transmitted radio power, not the electricity consumed by the whole transmitter. The orange RTG glow could also be mistaken for visible light. Fix: “Its radio signal was transmitted at about eight watts,” and label the orange RTG view as illustrative or false color. [Turyshev et al. 2012](https://arxiv.org/html/1204.2507)
- **s06, OK:** The plaque’s material, approximate dimensions, images and named credits are supported. [NASA](https://www.nasa.gov/history/45-years-ago-pioneer-11-explores-jupiter/), [Planetary Society](https://www.planetary.org/articles/0120-the-pioneer-plaque-science-as-a-universal-language)
- **s07, UNSURE:** The Doppler result and historical number are right, but the board presents a sunward pull as directly established. Later analysis says the direction could not be determined unambiguously. Fix: “The signal was consistent with a small acceleration approximately toward the Sun.” [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064), [Turyshev et al. 2012](https://arxiv.org/html/1204.2507)
- **s08, UNSURE:** The arithmetic is right, but the spoken lines make idealized offsets sound like measured positions. Fix: “If that extra acceleration stayed constant and everything else stayed equal, after one year the difference would be about 400 kilometers.” [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s09, OK:** Dark matter, modified gravity and spacecraft effects were among the proposed explanations. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s10, OK:** “No answer yet” works as a historical midpoint in the story, before the thermal investigation is introduced. [Turyshev et al. 2012](https://arxiv.org/html/1204.2507)
- **s11, UNSURE:** JPL says Toth helped Turyshev create the program, rather than crediting him alone. Fix: “Viktor Toth helped create software to read and clean the telemetry.” The date, staircase, funding and data volume are supported. [NASA/JPL](https://science.nasa.gov/missions/pioneer/study-finds-heat-is-source-of-pioneer-anomaly/)
- **s12, WRONG:** Heat is not itself defined as invisible light, and 63 W is an equivalent net directed radiation power, not a claim that 63 W of total heat was emitted. Fix: “Pioneer sheds heat as mostly invisible infrared light. An imbalance equivalent to about 63 watts beamed in one direction would produce a push of that size.” [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064), [Turyshev et al. 2012](https://arxiv.org/html/1204.2507)
- **s13, WRONG:** The 80% compares the thermal model with that team’s independently Doppler-fitted force for Pioneer 10. The board’s “of that” incorrectly makes 35% and 45% shares of the 80%, although they are shares of the comparison baseline. Fix: “For Pioneer 10, the thermal estimate was about 80% of the team’s Doppler estimate: about 35 percentage points from RTGs and 45 from electrical heat. The estimates agreed within uncertainty.” [Turyshev et al. 2012](https://arxiv.org/html/1204.2507)
- **s14, WRONG:** NASA attributes Pioneer 10’s final weak signal to declining power, but describes Pioneer 11 losing contact when Earth moved out of its antenna’s view. The AU definition should also say *average* Earth to Sun distance. Fix: “Pioneer 10’s fading power left its signal too weak. Pioneer 11 lost contact after Earth moved out of its antenna’s view.” [NASA Pioneer 10](https://science.nasa.gov/missions/pioneer/pioneer-10-sends-last-signal/), [NASA Pioneer 11](https://science.nasa.gov/mission/pioneer-11/)
- **s15, UNSURE:** Heat is a well-supported explanation, especially for the detailed Pioneer 10 analysis, but the original Grok quote remains unverified and Pioneer 11 was not analyzed to the same depth in the 2012 paper. Fix: “The evidence points strongly to heat pushing the spacecraft.” Treat the Grok wording as a paraphrase unless verified. [Turyshev et al. 2012](https://arxiv.org/html/1204.2507)

### SOURCES.md rows

These bullets follow the table’s original order, one per row.

- **s04, OK:** Pioneer 10 launched March 2 in Florida, which was March 3 UTC. [NASA](https://science.nasa.gov/mission/pioneer-10/)
- **s04, OK:** Pioneer 11 launched April 5 in Florida, which was April 6 UTC. [NASA](https://science.nasa.gov/mission/pioneer-11/)
- **s04, OK:** Pioneer 10 was the first spacecraft to fly past Jupiter, with closest approach on December 4, 1973 UTC. [NASA](https://science.nasa.gov/mission/pioneer-10/)
- **s04, OK:** The high-gain dish was 2.74 m across and was used to communicate toward Earth. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s05, OK:** The equipment compartment was hexagonal, with sides about 71 cm long. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s05, OK:** Two booms carried four SNAP-19 RTGs, two per boom, using plutonium-238. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s05, OK:** Five percent is a coarse approximation of the cited 5% to 6% conversion efficiency. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s05, OK:** About 2,500 W is reasonable rounding. The specific 2,578 W value in the 2012 model is for July 1, 1972, not the launch date. [Turyshev et al. 2012](https://arxiv.org/html/1204.2507)
- **s05, OK:** The paper gives about 160 W electrical output before launch. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s05, OK:** The magnetometer was about 6.6 m from the spacecraft center; separation from spacecraft magnetic interference is a reasonable description of the boom’s purpose. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s05, OK:** Eight watts is the nominal transmitted radio power, at approximately 2.29 GHz. It is not total transmitter electricity consumption. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s05, UNSURE:** Refrigerator lamps vary, and the comparison does not hold for every modern LED lamp. Fix: “About as much transmitted power as a small old-style light bulb.” [NASA](https://www.nasa.gov/history/50-years-ago-pioneer-10-launches-to-explore-jupiter/)
- **s05, OK:** Forty to 70 AU is approximately 3.7 to 6.5 billion miles. Those paper distances are from the Sun; Earth distance differs slightly. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s06, OK:** The plaque’s approximate dimensions, material, images and design credits are supported. [NASA](https://www.nasa.gov/history/45-years-ago-pioneer-11-explores-jupiter/), [Planetary Society](https://www.planetary.org/articles/0120-the-pioneer-plaque-science-as-a-universal-language)
- **s07, OK:** Doppler tracking measures changes in radio frequency associated with relative motion. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s07, OK:** Anderson describes the Pioneer 10 discrepancy beginning around 1980 at about 20 AU. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s07, OK:** Both Pioneer 10 and 11 contributed to the anomaly finding. [Anderson et al. 1998](https://arxiv.org/abs/gr-qc/9808081)
- **s07, UNSURE:** The values and attributions are correct, but “sunward” is a fitted interpretation whose precise direction remained uncertain. Fix: “Consistent with approximately sunward acceleration.” [Anderson et al. 1998](https://arxiv.org/abs/gr-qc/9808081), [Turyshev et al. 2012](https://arxiv.org/html/1204.2507)
- **s07, OK:** The stated data intervals and heliocentric distance ranges match the 2002 analysis. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s07, OK:** John Anderson led a team with JPL and other institutional coauthors. [Anderson et al. 1998](https://arxiv.org/abs/gr-qc/9808081)
- **s08, OK:** The stated ratio is approximately 11.2 billion. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s08, OK:** One year gives approximately 435 km and 2.8 cm/s under the stated constant-acceleration assumption. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s08, OK:** The road comparison is reasonable: one route is approximately 286 miles, or 460 km. [Enterprise route guide](https://www.enterprise.com/en/road-trips/destinations/iIlinois/drive-from-chicago-to-detroit.html)
- **s08, OK:** The ten-year calculation gives approximately 43,500 km and 1 km/h; Earth’s equatorial circumference is about 40,075 km. [NASA](https://www.nasa.gov/pdf/475486main_HEP_I_MS_6.pdf)
- **s09, OK:** The cited papers discuss dark matter, modified gravity and other possibilities. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s11, OK:** Turyshev began gathering records in 2004. [NASA/JPL](https://science.nasa.gov/missions/pioneer/study-finds-heat-is-source-of-pioneer-anomaly/)
- **s11, OK:** JPL reports more than a dozen boxes of magnetic tapes under a staircase. [NASA/JPL](https://science.nasa.gov/missions/pioneer/study-finds-heat-is-source-of-pioneer-anomaly/)
- **s11, UNSURE:** The cited release credits Toth with helping Turyshev create the program. Fix: “Toth helped create software to read and clean the telemetry.” [NASA/JPL](https://science.nasa.gov/missions/pioneer/study-finds-heat-is-source-of-pioneer-anomaly/)
- **s11, OK:** Planetary Society members were asked to help fund the rescue, and NASA later provided funding. [NASA/JPL](https://science.nasa.gov/missions/pioneer/study-finds-heat-is-source-of-pioneer-anomaly/)
- **s11, OK:** The release reports more than 43 GB collected. [NASA/JPL](https://science.nasa.gov/missions/pioneer/study-finds-heat-is-source-of-pioneer-anomaly/)
- **s12, UNSURE:** Radiation carries momentum, but \(F=P/c\) assumes power is directed in one direction; general emission needs a direction or efficiency factor. Fix: “For a perfectly directed beam, \(F=P/c\).” [Turyshev et al. 2012](https://arxiv.org/html/1204.2507)
- **s12, OK:** RTG and electrical heat, reflection and uneven emission are supported as a simplified picture. [Turyshev et al. 2012](https://arxiv.org/html/1204.2507)
- **s12, OK:** About 63 W of *directed equivalent* power and roughly 2,000 W of RTG waste heat at the later epoch match the 2002 discussion. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s12, OK:** A 60 W old-style bulb is a reasonable scale comparison for 63 W. [Anderson et al. 2002](https://arxiv.org/pdf/gr-qc/0104064)
- **s13, OK:** The German team said thermal recoil likely resolves the Pioneer 10 anomaly. Its paper describes a worst-case error on the order of 10%, with 11.5% for the listed parameters. [Rievers and Lämmerzahl 2011](https://arxiv.org/html/1104.3985)
- **s13, UNSURE:** The 44% to 96% comparison is in the paper, but it is tied to an illustrative point 26 years after launch and includes uncertainties in both quantities. Fix: “At 26 years after launch, the team’s comparison gave about 44% to 96% of the reported anomaly.” [Francisco et al. 2012](https://arxiv.org/pdf/1103.5222)
- **s13, UNSURE:** The 80%, 35% and 45% figures are correct only with the paper’s comparison made explicit. Fix: “For Pioneer 10, thermal force was about 80% of the team’s Doppler estimate, comprising approximately 35 percentage points from RTGs and 45 from electrical heat.” [Turyshev et al. 2012](https://arxiv.org/html/1204.2507)
- **s13, UNSURE:** The estimates’ uncertainty regions overlap; this does not establish an exactly measured 20% residual. The 26.3% and 25% figures are expressed relative to \(a_P\). Fix: “The difference is statistically consistent with uncertainty; the largest listed uncertainty is possible RTG coating degradation.” [Turyshev et al. 2012](https://arxiv.org/html/1204.2507)
- **s13, OK:** The short quotation appears in the abstract. Its surrounding conclusion is that no *statistically significant* difference remained in the detailed Pioneer 10 comparison. [Turyshev et al. 2012](https://arxiv.org/html/1204.2507)
- **s13, OK:** “Mostly solved” is a defensible plain-language framing, with the listed Pioneer 11 and spin-down caveats retained. [Turyshev et al. 2012](https://arxiv.org/html/1204.2507)
- **s14, OK:** The tracker returned approximately 142.3 AU for Pioneer 10, consistent with the rounded November estimate. Its page is dynamic, so preserve the observation date. [Heavens-Above](https://heavens-above.com/SolarEscape.aspx)
- **s14, OK:** The tracker returned approximately 119.7 AU for Pioneer 11, consistent with the rounded November estimate. Its page is dynamic. [Heavens-Above](https://heavens-above.com/SolarEscape.aspx)
- **s14, OK:** NASA gives January 23, 2003 for Pioneer 10’s last signal. [NASA](https://science.nasa.gov/missions/pioneer/pioneer-10-sends-last-signal/)
- **s14, OK:** Both dates refer to 1995. NASA’s detailed account distinguishes the September 30 last Ames contact from engineering data received on November 24. [NASA](https://science.nasa.gov/mission/pioneer-11/)
- **s14, WRONG:** The row presents fading power as the sufficient explanation for both losses of contact. NASA describes Pioneer 11’s final loss in terms of Earth moving out of its antenna’s view. Fix: “Pioneer 10’s signal became too weak as power declined; Pioneer 11 lost contact after Earth moved out of its antenna’s view.” [NASA Pioneer 10](https://science.nasa.gov/missions/pioneer/pioneer-10-sends-last-signal/), [NASA Pioneer 11](https://science.nasa.gov/mission/pioneer-11/)
- **s01, s15, UNSURE:** The brief supports the production’s framing, but I did not locate the original X exchange to verify a direct quotation. Fix: Label it as a paraphrase until the original is checked. [Brief](</C:/Users/lilli/AI-Shared/projects/heartbeat-tv/pioneer-episode/BRIEF.md>)

### RESEARCH.md section 8

Using its stated \(a=8.74\times10^{-10}\) m/s² and year of \(3.156\times10^7\) seconds, I independently get:

| Elapsed time | Speed change | Position shift |
|---|---:|---:|
| 1 year | 0.02758 m/s | 435.3 km |
| 10 years | 0.2758 m/s, or 0.993 km/h | 43,527 km |
| 11.5 years | 0.3172 m/s | 57,564 km |
| 20 years | 0.5517 m/s | 174,107 km |

All displayed section 8 values are correctly rounded. The gravity ratio is \(1.122\times10^{10}\), and 174,107 km is about 0.453 times the mean Earth to Moon distance. These are illustrative offsets with a constant added acceleration and matching initial conditions, not measured trajectory errors. [NASA Earth and Moon comparison](https://science.nasa.gov/moon/by-the-numbers/)

Next thing: update the script and claim table, starting with the transmitted-power wording in s05.

## Applied (Claude Code, Opus, 11/15)

- s01/s15 Grok quote UNSURE: FIXED. Spoken line is now "Grok said, more or less:"; shot notes say use the real X screenshot if production has it, otherwise a card labeled PARAPHRASE.
- s04 launch dates: OK. Dates are US local (Florida); UTC is March 3 and April 6. Noted in RESEARCH.md; script keeps local dates (NASA's usual).
- s05 eight watts WRONG: FIXED. Now "the radio signal it beams home goes out at just eight watts"; board says "Radio signal sent at 8 W". RTG glow labeled false color in the shot.
- s05 refrigerator bulb UNSURE: FIXED. Now "About as much as a small old-style night-light bulb" (those were 4 to 7 W).
- s07 sunward direction UNSURE: FIXED. Board and line now say "roughly toward the Sun"; RESEARCH.md notes the 2011/2012 papers could not pin the direction (Sun vs Earth vs spin axis).
- s08 idealized offsets UNSURE: FIXED. Now "If that pull stays steady, after one year..."; board says "if the pull stayed steady".
- s11 Toth credit UNSURE: FIXED. Now "helped build software to read the telemetry".
- s12 heat = invisible light WRONG: FIXED. Now "Warm things give off heat as infrared light, a kind of light you can't see"; 63 W now said as "the lopsided part only has to equal about sixty-three watts beamed one way".
- s12 F = P/c UNSURE: FIXED in SOURCES.md (perfectly directed beam).
- s13 percentages WRONG/UNSURE: FIXED. Board: "about 80% of their Doppler estimate", "About 35 points from the RTGs, about 45 from the electronics", "The difference is inside the uncertainty". Spoken: "eighty percent of the pull they measured from the radio data" and "That gap fits inside the error bars". Portugal line now adds "at one point in the trip" (26 years after launch on the board).
- s14 loss of contact WRONG: FIXED. Pioneer 10: power dropped until the signal was too weak; Pioneer 11: low power and Earth drifted out of its antenna's view. AU defined as Earth's average distance.
- s15 "It was heat" UNSURE: FIXED. Now "The best evidence says it was heat."
- Section 8 math: Codex got the same numbers (435 km, 43,527 km, 0.993 km/h, ratio 1.122e10). No change.
- Also added on-screen source cards to s03, s10 and s15 so every scene with a factual claim shows a source.
