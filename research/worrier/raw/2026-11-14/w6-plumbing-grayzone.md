# W6 - Plumbing and gray zone layer

Written Saturday 2026-11-14. Window: roughly Oct 14 - Nov 14, 2026, weighted to Nov 1-14.

## Read this first: how far the checking went

- **The web-search budget for this run ran out after 17 searches** (it is shared across all agents in the turn). Everything after that came from opening known pages directly: CTP-ISW daily Iran Updates (Oct 28 - Nov 13), Yle, ERR, Focus Taiwan, Kyiv Independent, Iran International, Breaking Defense, The Hacker News, BleepingComputer, SecurityWeek, CyberScoop, CISA, Arms Control Today, Inside GNSS, Cloudflare, SCMP, Notes from Poland, 38 North, Stars and Stripes, Al Jazeera, NPR member stations, The Aviationist, Maritime Executive.
- **Not reachable** (blocked, paywalled or no search left): Reuters, AP, FT, WSJ, Guardian, DW, IAEA.org, Eurasianet, Caspian News, NetBlocks (stale page), Kentik, SpaceNews article bodies. Where an item rests on one of these, I read it second-hand and say so.
- **"Not found" below means "not on the pages I could open", not "did not happen".** The thinnest sections are: Red Sea / Taiwan / Atlantic / Pacific cables, GNSS data for November, co-orbital and launch activity, Caspian neighbours' official reactions, Gaza / West Bank / Jordan / Egypt, Japan / Korea cyber. These need a follow-up pass with search.
- Dates were checked against the calendar (Nov 14, 2026 is a Saturday). Several outlets carry off-by-one dates; corrections are noted in line.

Labels: ESTABLISHED / CLAIMED / NOT ESTABLISHED as defined in the brief. Where an official body says X did it and X denies it, I split the label: the statement is ESTABLISHED, the underlying act is CLAIMED.

---

## 1. Undersea cables, pipelines, internet disruptions

| Date | What | Source | Label |
|---|---|---|---|
| Nov 5 | Helsinki District Court jailed the Russian captain (3y6m) and Azerbaijani boatswain (2y10m) of the cargo ship Fitburg for aggravated sabotage: anchor dragged ~130 km on Dec 31, 2025, damaging Elisa and Arelion Finland-Estonia data cables. About EUR 1.9M damages. First conviction of foreign mariners for cable damage in an EEZ. Court did not need to find, and did not find, a Russian state order. | https://yle.fi/a/74-20255306 ; https://www.submarinenetworks.com/en/nv/insights/finland-jails-cargo-ship-officers-in-subsea-cable-sabotage-conviction | ESTABLISHED (verdict); state direction NOT ESTABLISHED |
| Oct 21-26 (reported Nov 6) | FT, relayed by CTP-ISW: three US-sanctioned vessels and an Iranian fishing vessel moved in patterns "commonly associated with subsea cable mapping" near the Europe-India Gateway cable. Iranian officials including SNSC secretary Rezaei have threatened cables if US strikes resume. | https://www.criticalthreats.org/analysis/iran-update-november-6-2026 | CLAIMED (one report, pattern-based; FT original not read) |
| May 18 (still the standing condition) | Cable operators issued force majeure for Gulf work; IRGC said it would require permits and "protection fees" for cables on its seabed. FALCON and GBI cross Iranian waters. No new Gulf cut reported then; the point is that any fault would not be repaired on a normal schedule. | https://windward.ai/blog/alcatel-pauses-gulf-subsea-cable-repairs-as-iran-demands-protection-fees/ | ESTABLISHED (industry notices, IRGC statement); current status NOT CHECKED |
| Q3 2026 (published Oct 27) | Cloudflare's quarterly review lists no Gulf or Red Sea cable disruption. It does list deliberate fibre damage in Russia's Far East on Sept 19 (Rostelecom), a Guyana cut, and Iraq exam shutdowns. | https://blog.cloudflare.com/q3-2026-internet-disruption-summary/ | ESTABLISHED |
| Nov 12 / Nov 13 | Microsoft 365 global outage (Nov 12); FAA nationwide ground stop of 4+ hours (Nov 13) after a failure in the network linking air route control centres. DHS: "no chatter, no footprints"; Bloomberg: FBI does not think it was an attack and is looking at a software update; officials say unrelated to the Microsoft outage. | https://www.securityweek.com/no-signs-of-hacking-in-faa-ground-stop-as-fbi-reportedly-probes-software-update/ | ESTABLISHED (events); hostile cause NOT ESTABLISHED |
| Nov 1-14 | Baltic, Taiwan/Matsu: no new cable or pipeline damage on Yle, ERR or Focus Taiwan front pages. Last Matsu item I found is Mar 30, 2026 (Chinese work barge, partial damage). | https://yle.fi/news ; https://news.err.ee/ ; https://focustaiwan.tw/ | NOT FOUND (limited check) |

**Background rate.** Worldwide there are roughly 150-200 cable faults a year (3-4 a week), most from anchors and fishing gear (industry figure from memory, not re-checked today). The Baltic has had 10+ incidents since 2023, clustered Nov-Jan (Nov 2024, Dec 2024, Jan 2025, Dec 2025). So one Baltic incident this winter would be normal, not a signal. What is above normal is on the repair side: Gulf repair work has been frozen since spring, so a fault there is long-lived by default.

**Connections drawn**
- Cable-mapping pattern + Rezaei's threats -> preparation to cut cables if strikes resume. Label: **CAUSAL CHAIN proposed, not shown.** Wrong if: the vessels' tracks turn out to be fishing, loitering to dodge the blockade, or survey for the "fee" scheme; or if strikes resume and no cable is touched.
- Microsoft outage / FAA ground stop / European cyber waves in the same fortnight. Label: **SAME TIME ONLY.** Wrong (i.e. it becomes a chain) only if investigators report intrusion evidence; today they say the opposite.

---

## 2. Space and navigation

| Date | What | Source | Label |
|---|---|---|---|
| Oct 28 | AP, relayed by CTP-ISW: a geospatial firm counted 40 instances (Jul 1 - Oct 19) of Russian military satellites positioned over Saudi energy and military sites before and after Houthi strikes, including the Sept 10 East-West Pipeline strike. AP sources also say Russia gave targeting intelligence for Iranian strikes. CTP-ISW: imagery "very likely enables" battle-damage assessment. | https://www.criticalthreats.org/analysis/iran-update-october-28-2026 | CLAIMED (one firm's data + unnamed sources, via AP; AP original not read) |
| Nov 8-10 | IRGC claimed it struck "enemy navigation systems" on Oman's Didamar island. Reuters could not confirm damage. A senior Omani official said the navigational aids were not hit; Nov 10 satellite imagery shows no obvious damage. CTP-ISW says Iran hit radar/communications there and overstated the effect; ships kept transiting. Sources disagree on the day (Nov 8 vs Nov 10). | https://maritime-executive.com/article/uncertainty-surrounds-possible-attack-on-oman-s-strait-of-hormuz-lighthouse ; https://www.criticalthreats.org/analysis/iran-update-november-10-2026 | CLAIMED (Iran) and disputed (Oman). The brief's "Iran attacked navigation systems" is stronger than the record. |
| Nov 13 | IRGC claimed it destroyed a US early-warning radar in Bahrain in reply to a US strike on a telecom tower at Sirik. CENTCOM: two drones launched, both shot down. First claimed IRGC strike on a land-based US asset since early September. | https://www.criticalthreats.org/analysis/iran-update-november-13-2026 | Launch ESTABLISHED; damage CLAIMED and denied |
| Mid-Oct; again ~Nov 9-14 | Starshield terminals used by Ukraine capped at about 160 km/h, which stops interceptor drones catching jet-powered Russian drones. First episode mid-to-late October, lifted end of October, returned in November. Zelensky: "not random errors"; says limits now extend to occupied Ukrainian territory. Musk (Oct 24): the military terminals are controlled by the US government. No Pentagon or SpaceX explanation. EU Commission called it unacceptable if confirmed; US Democrats told Musk to preserve records. | https://kyivindependent.com/starshield-speed-restrictions-return-hampering-efforts-to-intercept-russian-drones-zelensky-says/ ; https://breakingdefense.com/2026/11/ukraine-eyeing-new-spacex-starshield-deal-by-mid-2027-still-no-answers-about-october-problems/ | ESTABLISHED (the cap); who ordered it NOT ESTABLISHED. Nothing points to Russian or Chinese interference; it reads as a US-side policy or contract limit. |
| Nov 8-9 | Ukraine says it struck a Russian satellite-communications jamming station near Sartana (occupied Donetsk). A Ukrainian adviser said on Nov 2 that Russia is fielding more Starlink jammers along the front. | https://kyivindependent.com/ukraine-strikes-russian-satellite-communications-jamming-station-general-staff-says/ | CLAIMED (Ukrainian General Staff) |
| Oct 19 / Oct 21 | Finnish authorities logged 392 vessels reporting GNSS interference in Finnish waters Jan-Aug 2026 (likely an undercount). TalTech study: Estonian stations went from episodic jamming in 2024 to sustained denial in 2025, with spikes during Ukrainian drone strikes on Ust-Luga. | https://insidegnss.com/ais-gnss-fusion-strengthens-maritime-navigation/ ; https://insidegnss.com/gnss-interference-reshaping-the-baltic-signal-environment/ | ESTABLISHED |
| Nov 12 | Offshore pipelay in the Middle East now runs on acoustic-inertial positioning because GNSS is "jammed, denied or spoofed" - a sign the Gulf interference is routine enough to engineer around. | https://insidegnss.com/utec-puts-acoustic-inertial-positioning-to-work-on-middle-east-pipelay-amid-gnss-disruption/ | ESTABLISHED (industry) |
| Oct 26-27 | DIA "Challenges to Space Security 2026": China's ISR fleet over 510 satellites, tripled since 2018; Chinese firms sell imagery to actors Western firms refuse. | https://breakingdefense.com/2026/10/dia-china-has-tripled-its-satellite-fleet-since-2018-as-expansion-continues/ | ESTABLISHED |
| Nov 13 | Starship Flight 15 launched; booster catch called off. Payload count (26 Starlink V3) not confirmed by me - article body paywalled. | https://spacenews.com/starship-launches-on-15th-test-calls-off-booster-catch/ | Launch ESTABLISHED; payload NOT CHECKED |
| Window | Co-orbital / anti-satellite events, Space Command warnings, Iran / Russia / China / North Korea satellite launches: nothing on SpaceNews or Breaking Defense front pages; 38 North shows no launch or test-site item (parade imagery of a new ICBM, Oct 29). | https://breakingdefense.com/category/space/ ; https://www.38north.org/ | NOT FOUND (limited check) |

**Background rate.** GNSS jamming in the eastern Baltic has been daily since 2024; in the Gulf it has been constant since March (one analysis found most logged Hormuz "transits" in one month were spoofing artefacts). Neither is new. What is above normal: both sides in the Gulf are now trading strikes on fixed sensors and communications (US on Qeshm radars and a Sirik telecom tower; Iran on Didamar and Bahrain radars).

**Connections drawn**
- Russian satellites over Saudi targets -> Houthi/Iranian strike assessment. Label: **CAUSAL CHAIN claimed by AP sources and assessed by CTP-ISW.** Wrong if: the passes match those satellites' normal ground tracks at normal revisit rates (a firm counting passes over a big country will always find some).
- Starshield cap and Trump's Russian-diesel deal in October. Label: **SAME TIME ONLY** (Breaking Defense notes the timing and does not link them). Wrong only if records show an instruction.
- Baltic jamming spikes and Ukrainian strikes on Ust-Luga. Label: **SHARED CAUSE** (Russian air defence turns jammers up when drones arrive). Supported by the TalTech data.

---

## 3. Europe hybrid and sabotage

| Date | What | Source | Label |
|---|---|---|---|
| Oct 11-12 | Refrigeration controls at about 700 French supermarkets and other sites switched to heat/defrost; stock lost, some fires. | https://www.iranintl.com/en/202611137304 ; CERT-FR alert CERTFR-2026-ALE-012 cited in https://thehackernews.com/2026/11/second-wave-of-cyberattacks-hits.html | ESTABLISHED |
| Nov 10 | France publicly blamed the IRGC's "Shahid Kaveh" cyber unit, working through front "hacktivist" groups; summoned Iran's ambassador; will seek EU sanctions; Paris prosecutors requested international arrest warrants. IRGC (Nov 14): "a worn-out Zionist scenario". | https://www.iranintl.com/en/202611111192 ; https://www.iranintl.com/en/liveblog/202611143682 | Attribution statement ESTABLISHED (read via Iran International, not a French primary); Iranian responsibility CLAIMED by one government, evidence not public |
| Nov 1-2 | Second wave, same night: supermarkets in at least nine countries (Belgium, Luxembourg, Sweden, Ireland, Estonia, Netherlands, Finland, Portugal, Italy) and three centres of France's national blood service (cold rooms reset; alarms caught it; no blood lost). Belgium's cyber centre: who did it "may never be determined". Many devices were internet-exposed with default passwords. | https://thehackernews.com/2026/11/second-wave-of-cyberattacks-hits.html ; https://www.iranintl.com/en/202611137304 | Events ESTABLISHED; attribution NOT ESTABLISHED (copycats are plausible) |
| Nov 5 | CISA, FBI, HHS, USDA, DoT fact sheet: harden refrigeration and cold-chain controllers. No actor named, no US incident described. | https://www.cisa.gov/resources-tools/resources/us-government-partners-urge-hardening-industrial-refrigeration-and-cold-chain-monitoring-systems | ESTABLISHED |
| Nov 10 | DOJ unsealed an 8-count indictment of three men said to act for the IRGC and Kataib Hezbollah through the front "Harakat Ashab al-Yamin": nearly 20 attacks or attempts in Europe and the US (about 7 in Britain; arson, explosives, a near-fatal stabbing), plus the Sept 26 Fairford plot (three disguised vans with fuel drums). One defendant in US custody since May allegedly kept directing from jail; two are in Iran. | https://www.stlpr.org/npr/2026-11-11/iran-backed-trio-accused-of-plotting-attacks-on-u-k-base-hosting-u-s-jets | ESTABLISHED (as allegations) |
| Nov 12 | ITV: seven-man network, run from a "control room in Baghdad", used Dutch organised-crime contacts to hire locals who often did not know the client. Funding suspected from both Quds Force and Iran's intelligence ministry. No Russian link reported. | https://www.iranintl.com/en/202611126962 | CLAIMED (one outlet, Western officials) |
| Nov 9 | US moved 9-10 KC-135 tankers out of RAF Mildenhall (to Germany, Spain, Prestwick) and 3 Ospreys to Lakenheath, some under weather waivers. WSJ: because of an Iran-related threat; both bases at the second-highest protection level. AP: one US official called it proactive, not a response to an immediate threat. No official reason given. | https://theaviationist.com/2026/11/10/raf-mildenhall-security-threat-dispersal/ | Movement ESTABLISHED; reason CLAIMED (anonymous) |
| Nov 10 | Separate case: a 41-year-old senior US Army member at Imjin Barracks (Gloucester) arrested under the UK National Security Act; police say the allegations concern Russia. **NPR says the two cases are unrelated.** | same NPR link | ESTABLISHED. The brief's "UK case linking an airbase, Iran and a Russian spy" merges two cases. |
| Nov 11 | Rezaei: if attacked again Iran "may even target some American military bases in European countries". Kayhan's list: Cyprus, Greece, Romania, Albania, Italy, Britain, Diego Garcia. (Portugal and Germany were not in the list I saw.) IRGC said on Nov 7 the 2,000 km missile range cap is lifted. | https://www.iranintl.com/en/202611114265 ; https://www.criticalthreats.org/analysis/iran-update-november-10-2026 | ESTABLISHED (statements) |
| Oct 13 | MI5 chief: Fairford was "not unique"; the "major shift this year" is Iranian ambition toward harder targets like military sites; 50+ arrests over Iran-linked plots in a year; so far Iran uses "low-level criminal proxies". Says Russia and Iran are both escalating - not that they act together. | https://www.scrippsnews.com/us-news/iran-war/mi5-chief-says-iran-is-targeting-military-sites-and-suspected-plot-at-raf-fairford-is-not-unique | ESTABLISHED |
| Nov 12-13 | Two men convicted in London of helping Iran target Iran International journalists. | https://www.iranintl.com/en/202611122230 | ESTABLISHED |
| Early Nov | Hoax bomb threats: airports in Rome, Copenhagen, Prague, Warsaw, Lisbon; RTE and Sky News; two Finnair flights on Nov 5 (Italian jets escorted one). Nov 11: 6,000+ Italian schools emailed from a hacked Taiwanese university account, signed with a Russian name. Meloni: meant to frighten and create chaos. | https://www.atlanticcouncil.org/?p=959811 ; https://yle.fi/a/74-20255278 ; https://focustaiwan.tw/society/202611120012 | Events ESTABLISHED; who did it NOT ESTABLISHED |
| Nov 11 | Ukraine hit Russia's Ust-Luga port and the missile corvette Naro-Fominsk near Gogland, ~40 km from Finland. Estonian officers: hit more than once, casualties, could not move under own power; port capacity down from ~700,000 to ~300,000 t/day. Finland closed airspace and a sea area 02:09-07:20 and suspects a 5-minute drone entry; drones briefly crossed Estonian airspace; Estonia says it never gave permission. | https://yle.fi/a/74-20256236 ; https://news.err.ee/1610195272/officer-russian-warship-hit-multiple-times-in-baltic-with-casualties ; https://news.err.ee/1610193178/defense-minister-drones-entered-estonian-airspace-from-northeast-and-southeast | ESTABLISHED (strike, closures); casualty detail CLAIMED |
| Nov 13 | Bild: at Abu Dhabi talks (~Nov 10) Russian negotiators floated Finland leaving NATO and no NATO bases in the Baltic states. Finnish ministers answered on the record ("absolutely outrageous"). | https://yle.fi/a/74-20256829 | CLAIMED (one outlet) |
| Late Oct (disclosed Nov 13) | German drone maker Quantum Systems hit through a tampered update for its ground-control software; Bundeswehr reportedly grounded the drones and pulled them from an exercise. No attribution; the firm says it was targeted for supporting Ukraine. | https://www.bleepingcomputer.com/news/security/german-military-drone-operations-disrupted-by-cyberattack/ | ESTABLISHED (incident); attribution NOT ESTABLISHED |
| Nov 10-12 | Poland charged two Ukrainians with sabotage for Russia (Nov 10) and indicted another over the Nov 2025 Warsaw-Lublin rail bombing (Nov 12). | https://notesfrompoland.com/2026/11/12/poland-indicts-ukrainian-man-for-assisting-in-rail-sabotage-on-behalf-of-russia/ | ESTABLISHED |
| Nov 13 | Germany passed a law giving its spy agencies hacking and sabotage powers. | https://therecord.media/german-parliament-passes-law-giving-spy-agencies-hacking-power | ESTABLISHED |

**Background rate.** UK defence sites: 126 drone incidents in 2024, 250 in 2025, about 340 in the first eight months of 2026 (https://kyivindependent.com/uk-military-sites-see-near-daily-drone-incidents-in-2026-as-europe-confronts-widening-hybrid-threat/). A Dutch think tank counted 151 Russian-linked operations in Europe since 2022. Mass hoax bomb emails to schools and airports have hit Europe in most recent years. So drones over bases and hoax waves are the normal state of 2026. Above normal: (a) a NATO government formally blaming Iran for a physical-effect cyber attack on civilian food and then seeing a blood service hit; (b) US aircraft dispersed from an English base twice in six weeks.

**Is there sourced overlap between Russian and Iranian networks? No.** What exists: both use paid criminals and online recruits (a Dutch official's "crime as a service" description; MI5; Estonia's security chief); UK police were reported in September-October to be examining a possible Russian role at Fairford with no result published; and the US soldier/Russia arrest happened in the same county and week as the Iran indictment, which NPR says is coincidence. No shared recruiter, handler or payment channel has been named anywhere I could read. Label for "they use the same playbook": **SHARED CAUSE** (cheap, deniable, the same criminal labour pool). Label for "they are coordinating in Europe": **NOT ESTABLISHED.** It would be shown by one court document or official statement naming a common intermediary.

---

## 4. The Caspian and Caucasus

| Date | What | Source | Label |
|---|---|---|---|
| Nov 7 | CENTCOM created Task Force Iron Gate: about 20 people at Tampa HQ, working with other agencies against weapons, dual-use goods and money moving over Iran's land borders and the Caspian. No ships, no stated boarding authority, no announced agreement with any neighbour. It is a targeting and coordination cell, not a blockade force. | https://www.stripes.com/theaters/middle_east/2026-11-08/iran-caspian-sea-centcom-23399154.html ; https://www.aljazeera.com/news-analysis/2026/11/9/trump-says-iran-is-sealed-off-but-can-new-us-task-force-stop-weapons-flow | ESTABLISHED |
| Nov 8-12 | Trump: "full force and effect". IRGC spokesman: "merely a wordplay". As of Nov 12, no publicly confirmed interdiction, border closure or partner agreement. | https://gulfnews.com/world/mena/us-targets-irgc-weapons-routes-through-caspian-sea-1.500744356 | ESTABLISHED |
| Nov 10 | Iran's deputy foreign minister met Russia's ambassador to discuss countering the task force. CTP-ISW: Iran and Russia are cooperating against the interdiction effort. No Kremlin statement found. | https://www.criticalthreats.org/analysis/iran-update-november-10-2026 | Meeting ESTABLISHED (Iranian statement); Russian position NOT FOUND |
| Nov 5-6 | Rezaei met Putin; Telegraph says he asked for S-400s (CTP-ISW: Russia unlikely to spare them). FT: Russia agreed to supply 90 helicopter-mounted precision-missile launchers. Earlier: Russian drone parts, ammunition, TNT and detonators via the Caspian through July; Ukraine struck one shipment in July. | https://www.criticalthreats.org/analysis/iran-update-november-09-2026 ; https://www.iranintl.com/en/202611089896 | CLAIMED (single-outlet reports) |
| Oct 28 - Nov 12 | Armenia's parliament approved the US-run "Trump Route" (TRIPP) through Syunik on Oct 28. Khamenei adviser Velayati (Nov 5): if Trump's allies cross Iran's red line "we will break their legs"; Iran will secure the South Caucasus "with or without Russia". State media: Tehran "must prevent" the corridor. | https://www.iranintl.com/en/202611129472 | ESTABLISHED (statements) |
| Standing | Azerbaijan could cooperate quietly; Turkmenistan very reluctant; Turkey uninterested in a border confrontation; Pakistan mediating so unlikely to join; Kazakhstan's Iran trade already stalled on payment risk. Azerbaijan shut cargo crossings Mar 5-9 after blaming Iran for a drone attack. | Al Jazeera link above; Iran International link above | Analyst views = NOT ESTABLISHED as policy; March closure ESTABLISHED |
| Window | Any incident involving a Russian ship or cargo in the Caspian since Nov 7: none found. Azerbaijan-Russia tension, north-south corridor status: not reached. | - | NOT FOUND |

**Connection drawn.** Iron Gate -> Russian confrontation. Label: **NOT ESTABLISHED** (analyst forecast). The US has no presence on a closed sea; the realistic tools are sanctions, intelligence hand-offs and Israeli or US strikes on Iranian ports (as at Bandar Anzali in March). Wrong if: a Russian-flag cargo is stopped or struck. The sharper live risk in this region is Iran versus the Armenia corridor, which the brief did not mention.

---

## 5. Iran's arc

| Front | What (dates) | Source | Label |
|---|---|---|---|
| Iraq | Militia attacks on US sites: "nothing significant" most days. Oct 27 militia drones surveilled the US Embassy. Oct 31 Baghdad reportedly sent four army brigades to Basra to stop militia attacks on Kuwait. Nov 5: Kataib Hezbollah, Nujaba, KSS have not paid most fighters for two months; Iran reportedly suspended funding. Nov 6: three PMF members arrested moving 35 rockets. Nov 8: unknown actors possibly hit the Emirati-owned Khor Mor gas field a day after a KH threat. Nov 9: PM Zaydi threatened to arrest militiamen who join a US-Iran fight. Nov 12-13: KH mobilised and threatened to fire on Iraqi forces at Jurf al-Sakhr; Baghdad on highest alert Nov 13; Nov 14 PM sacked nine officials. CTP-ISW still assesses militias "likely to participate" if the war resumes. | https://www.criticalthreats.org/analysis/iran-update-november-09-2026 ; https://www.criticalthreats.org/analysis/iran-update-november-13-2026 ; https://www.iranintl.com/en/liveblog/202611143682 | Mostly CLAIMED (Iraqi media, unnamed sources) with ESTABLISHED government actions |
| Lebanon | No Hezbollah fire into Israel listed Nov 1-13; daily Israeli strikes and demolitions in the south. Saudi-owned media (Oct 21, 24): Iran told Hezbollah not to join a new war and it agreed. Hezbollah MP: no guarantees to anyone. Lebanon charged 13 Hezbollah members over an 800 kg explosives truck; arrested five more with maps on Nov 10. UNIFIL winding down. | https://www.criticalthreats.org/analysis/iran-update-october-30-2026 ; https://warhistory.org/maps/lebanon/2026-11 | "Held back" = CLAIMED; absence of attacks = consistent across sources |
| Yemen / Saudi | The loud front. Near-daily Houthi missile and drone claims on Riyadh airport, Aramco sites, the East-West Pipeline (minor damage Nov 9; an 11-day shutdown in September); Aramco office tower hit Nov 8; US ordered non-emergency staff out of Saudi Arabia Oct 30; Saudi strikes on Sanaa fuel and missile sites; Houthi ground push toward Aden. Yemen says 14 IRGC officers and 7 Hezbollah officials advise the Houthis. Some ships now take Houthi "transit permits" for Bab al-Mandeb (WSJ, Nov 6). | https://www.criticalthreats.org/analysis/iran-update-november-8-2026 ; https://www.criticalthreats.org/analysis/iran-update-november-04-2026 ; https://www.criticalthreats.org/analysis/iran-update-november-6-2026 | Intercepts and Nov 8 damage ESTABLISHED; most Houthi hit claims CLAIMED/unverified |
| Syria | Signed a defence deal with Saudi Arabia Nov 4; advisers deploying; 600 special forces to follow. Syria is now on the anti-Houthi side. | https://www.criticalthreats.org/analysis/iran-update-november-09-2026 | ESTABLISHED (AP/Reuters via CTP) |
| Hormuz | Iranian ship attacks hit a monthly high in October; first successful limpet-mine attack Oct 29; underwater drones and RPGs in use. Iran announces mine strikes that CTP-ISW reads as an information campaign (no sign of re-mining). US "minor" strikes on Qeshm Nov 2 and Nov 6. Gulf oil exports above pre-war levels (WSJ, Oct 29). | https://www.criticalthreats.org/analysis/iran-update-november-04-2026 ; https://www.criticalthreats.org/analysis/iran-update-november-7-2026 | ESTABLISHED (UKMTO, CENTCOM); mine claims CLAIMED |
| Gaza, West Bank, Jordan, Egypt/Suez | Not reached. | - | NOT CHECKED |

**Read:** proxies are not being "switched on" as a set. The Houthis are fully engaged but in their own war with Saudi Arabia over ports and oil. Hezbollah is silent and reportedly told to stay out. Iraqi militias are unpaid, under arrest pressure and fighting Baghdad over smuggling money; they are being held for the day US strikes resume, by their own stated condition. Label for "Iran is holding Iraq and Lebanon in reserve": **SHARED CAUSE** is as likely (money ran out, both groups were badly hurt). Wrong if: militia attacks on US sites start without a new US strike.

---

## 6. Cyber beyond the US

| Date | What | Source | Label |
|---|---|---|---|
| Oct 11 - Nov 2 | Refrigeration campaign and French attribution to the IRGC "Shahid Kaveh" unit (see section 3). This is the only Iran-named operation I found this month; the classic names (CyberAv3ngers, APT33/35) did not appear on any page I opened. | section 3 links | as above |
| Oct 30 - Nov 13 | Check Point gateways exploited; Israeli organisations hit first, some then wiped with a Palestinian-themed note. The backdoor matches a toolkit ESET tied to a China-nexus group in June. Check Point declines to attribute: could be that actor, an access broker selling entry, or a false flag. | https://thehackernews.com/2026/11/hackers-exploit-php2shell-flaws-in.html | Attacks ESTABLISHED; attribution NOT ESTABLISHED |
| Nov 13 | "SilentAir": hijacked mobile-network equipment in at least six Asian countries used to intercept texts (including login codes), mostly of people in Taiwan. State actor, high confidence; China link, low confidence (Enea). | https://thehackernews.com/2026/11/silentair-hijacks-asian-telecom.html | CLAIMED (one vendor) |
| Nov 9-10 | ESET: Russia's Turla (FSB) inside Kazakhstan and Romanian government mail servers, the Romanian one set to capture EU/NATO mail. | https://cyberscoop.com/russian-turla-group-used-new-toolset-to-silently-pilfer-emails-from-kazakhstan-romanian-governments/ | CLAIMED (one vendor) |
| Nov 9 | Italy's PM blamed pro-Russian hackers for leaking the foreign minister's data. | https://www.securityweek.com/italys-meloni-blames-pro-russian-hackers-for-leak-of-foreign-ministers-data-on-the-dark-web/ | ESTABLISHED (statement; headline-level read) |
| Late Oct | Quantum Systems update-server compromise (section 3). | section 3 link | ESTABLISHED |
| Nov 13 | Osaka breach (~1M people) "amid dozens of cyber incidents in Japan"; TSMC employee-data breach via a cloud provider. | https://therecord.media/city-of-osaka-japan-email-data-breach | ESTABLISHED (headline-level) |
| Nov 12-14 | North Korea: FBI ties $400M crypto theft to deepfake video calls; $1.2B recovered. | https://thehackernews.com/2026/11/fbi-says-north-korean-hackers-stole.html | ESTABLISHED |
| Window | Gulf energy, Korea, Sandworm, Volt Typhoon disruptive events: nothing on the pages opened. Salt Typhoon: retrospectives only. CISA's last two weeks: vulnerability alerts plus the refrigeration fact sheet; no country named. | https://www.cisa.gov/news-events/cybersecurity-advisories | NOT FOUND |

**Cooperation or shared tooling between Iran, Russia, China?** One possible data point only: China-nexus tooling under an Israel-focused wiper. Label: **NOT ESTABLISHED**; Check Point itself lists three innocent-to-sinister readings. It becomes real if a second vendor ties the wiper operator to an Iranian group and the access to the China-nexus group. The rest of the month's activity sorts cleanly by each state's own long-standing interests.

---

## 7. Nuclear layer

| Date | What | Source | Label |
|---|---|---|---|
| Nov 13 | IAEA quarterly report (seen by Reuters): the agency does not know where Iran's newest enrichment plant - the underground Isfahan Fuel Enrichment Plant, declared June 2025, never inspected - sits within the site or whether it holds material. It cannot verify the amount or location of the 440.9 kg of 60% uranium (about 10 weapons' worth if enriched further by the agency's yardstick) and cannot conclude nothing was diverted. Only Bushehr gets access. Grossi: inspectors must return "without further delay". | https://www.iranintl.com/en/202611133720 | ESTABLISHED (Reuters via Iran International) |
| Oct 28 | Grossi to AP: Iran does not appear to be enriching now. | https://www.armscontrol.org/act/2026-11/news/us-iran-threaten-escalation-diplomacy-stalls | ESTABLISHED |
| Nov 12 | Assembly of Experts called a review of NPT membership and defence doctrine an "unavoidable necessity". It has no direct nuclear authority; the foreign ministry said that week Iran stays in the NPT; Rezaei said last month no decision. Tehran's Friday prayer leader made the same call Oct 8 and Oct 30. | https://www.iranintl.com/en/202611121701 | ESTABLISHED (statement). Exit decision NOT ESTABLISHED |
| Nov 5-11 | Rezaei: "not a single gram" of enriched uranium leaves Iran; NYT says he is privately more open. Reported Qatari proposal (3.67% cap, dilute at home, inspectors back, blockade lifted). Trump (Nov 12) moved Vance off the talks and said a deal is unnecessary. | https://www.criticalthreats.org/analysis/iran-update-november-09-2026 ; https://www.iranintl.com/en/202611129077 | Public lines ESTABLISHED; private lines CLAIMED |
| Nov 3 | Chemical-weapons claim: NYT says Israel told the US Iran is moving quickly to put chemical agents on a missile or smuggle them. US officials are split; some compare it to 2002 Iraq intelligence and see a push to restart the war; Gulf governments were given no evidence and found it unserious; Israel's Home Front Command is not drilling for it. **Nothing newer found that confirms or debunks it.** | https://gvwire.com/2026/11/03/israeli-claims-of-iranian-chemical-weapons-divide-us-officials/ | CLAIMED (one side, anonymous sources) |
| Sep 24 - Oct 20 | US repeats charges that China (2020) and Russia ran low-yield tests and threatens to respond "on an equal basis"; both deny. US voted against a UN test-moratorium resolution (177 in favour). New START has expired; US rejected Russia's offer to keep its limits. P5 officials met quietly in New York the week of Oct 5. China (Oct 16) rejected three-way disarmament talks; a US official (Oct 20) cited "initial signs of openness". | https://www.armscontrol.org/act/2026-11/news/nuclear-weapon-states-consult-trump-talks-denuclearization | ESTABLISHED |
| Nov 12-14 | SCMP: Rubio raised a US-China-Russia trilateral with Wang (Nov 12); White House confirmed trilateral talks on the APEC sidelines in Shenzhen "next week" (Nov 14). I could not open the article to confirm the Nov 19 date, that it is leader-level with Putin present, or that "denuclearization" is on a written agenda (Trump said so on Oct 19). | https://www.scmp.com/news/china/diplomacy | Talks ESTABLISHED (headline-level); date and agenda NOT CONFIRMED by me |
| Window | North Korea: parade imagery of a new ICBM and a "tactical nuclear attack" submarine (Oct 29); no test-site or launch item seen. | https://www.38north.org/ | ESTABLISHED (limited check) |

**Connection drawn.** Blockade and strike threats -> Iranian nuclear-doctrine drift. Label: **CAUSAL CHAIN stated by the Iranian speakers themselves** (they tie the review to renewed attack). Wrong if: it is pre-summit bargaining and the calls fade after Shenzhen or a Qatar deal. Note the two facts point different ways: no enrichment seen (Grossi) but no way to see (IAEA report).

---

## Top 3 worries from this layer

**1. State cyber with physical effect has reached European civilian cold chains, and it is spreading by imitation.**
Evidence: 700 French sites (Oct 11-12); France's formal IRGC attribution and ambassador summons (Nov 10); nine more countries and a blood service the night of Nov 1-2; a five-agency US warning Nov 5. The method is cheap (exposed controllers, default passwords), so anyone can now repeat it.
Wrong if: France's evidence proves thin or no EU partner backs the sanctions request; national CERTs pin the Nov 2 wave on unrelated hobbyists or criminals; no third wave after vendors' fixes; nothing similar in hospitals, pharma or water by year-end.

**2. US aircraft in England are being moved because of threats on the ground, and the people named as directing it are out of reach in Iran.**
Evidence: bombers left Fairford (late Sept); tankers left Mildenhall Nov 9 under weather waivers with protection levels raised; MI5 "not unique"; indictment says the cell kept running from a US jail and from Iran; Rezaei's Nov 11 threat; UK drone incidents at defence sites at record levels.
Wrong if: the Mildenhall move is explained as routine or exercise-related; aircraft return within days with protection levels lowered; no further arrests or charges tied to bases before year-end. Note the base case: every public attempt so far was caught and used hired amateurs.

**3. Gulf cables and navigation aids are being positioned as the next thing to break, with no repair capacity behind them.**
Evidence: reported cable-mapping tracks near the Europe-India Gateway (Oct 21-26); Rezaei's cable threats; repair work frozen since May; both sides now striking radars and telecom towers (Qeshm, Sirik, Didamar claim, Bahrain claim).
Wrong if: the FT tracks are explained otherwise; strikes resume and cables stay intact; repair ships are allowed back. Evidence here is the weakest of the three (one report), consequence the largest.

Close fourth: **nuclear blindness plus doctrine pressure.** The IAEA cannot locate a plant or 440.9 kg of 60% uranium, and senior clerics are calling an NPT review a "necessity", a week before a summit and with US strike options being pushed. Wrong if inspectors are let back in under a Qatar-brokered deal.

## Evidence FOR and AGAINST the deniable-pressure idea

**For**
- Europe is where Iran behaves exactly as the idea predicts: front names (Harakat Ashab al-Yamin; "hacktivist" covers for Shahid Kaveh), hired criminals who do not know the client, two Iranian services funding the same network without knowing it, blanket denials.
- Targets moved from Jewish sites to US military sites after the US resumed limited strikes in Aug-Sept (CTP-ISW's timing).
- Iran's Gulf campaign leans on perception: mine "announcements", an overstated Didamar strike, a claimed radar kill - small physical acts with large claimed effects.
- Russian help is of the quiet kind: satellite passes, components over the Caspian, a diplomatic huddle over Iron Gate.
- Preparatory signals with no act yet: cable mapping, embassy drone surveillance, rockets being moved in Iraq.

**Against, or complicating**
- In the Gulf Iran is the opposite of deniable. It claims, and over-claims, its strikes; threatens European bases by name on television; lifted its missile range cap in public. A weaker side seeking deniability does not issue press releases.
- The proxy network is not being lit up on many fronts. Hezbollah is silent and reportedly told to stay out; Iraqi militias are unpaid and boxed in by Baghdad; Syria has changed sides. Only the Houthis are loud, for their own aims.
- No sourced Russia-Iran operational link in Europe. The one apparent link in the brief (airbase + Iran + Russian spy) is two unrelated cases per NPR.
- Russia "almost certainly cannot" give significant material support (CTP-ISW); the S-400 ask is unlikely to be met. No Chinese operational help surfaced beyond trade.
- Most of the month's alarming "plumbing" events have ordinary explanations on the record: FAA outage (software update), Microsoft outage, Starshield cap (US-side restriction), Finnish airspace closures (Ukrainian strike), Nov 2 freezer wave (default passwords, possibly copycats).
- The Atlantic Council piece attributes the same freezer and bomb-hoax wave to Russia "hallmarks" while France attributes the first freezer wave to Iran. Analysts are assigning the same events to different culprits by prior belief - a warning against doing the same here.

**Net:** the idea holds in one theatre (Europe, cyber and hired sabotage) and fails as a general description. Iran's pressure is a mix: deniable far from home, loud and exaggerated close to home, and its "many fronts" are fewer and weaker than a year ago. Coordination with Russia or China beyond supply and imagery is not established.

## What is quiet that I expected to be loud

- **No cable cut** found anywhere in the window - not in the Gulf after eight months of war and open threats, not in the Baltic at the start of its usual season, not near Taiwan after a large Chinese drill (limited check).
- **No militia attack on US sites in Iraq** and **no Hezbollah fire**, despite weekly US strikes on Qeshm.
- **No public Kremlin reaction** to a US task force aimed at Russia's Caspian trade (not found; may exist).
- **No visible Russian retaliation** in the Gulf of Finland three days after a missile ship was disabled 40 km from Finland.
- **No named Iranian group in US vendor or agency reporting** this fortnight; CISA's refrigeration warning names nobody even after France did.
- **No disruptive Sandworm or Volt Typhoon event**, no counterspace warning, no Iranian or North Korean launch on the pages reached.
- **No confirmation or collapse of the Nov 3 chemical-weapons claim** - eleven days of silence either way.
- **No Iron Gate action** at all: seven days, zero announced interdictions.

## Things the brief missed

1. France formally blamed the IRGC for the supermarket refrigeration attacks and summoned Iran's ambassador (Nov 10); a second wave hit nine countries and the French blood service (Nov 1-2).
2. The "UK case linking an airbase, Iran and a Russian spy" is two separate cases; the Russia one is a US Army member arrested at Imjin Barracks.
3. Oman denies the Didamar navigation aids were hit; imagery shows no obvious damage.
4. Ukraine disabled a Russian missile ship near Finland and halved Ust-Luga's capacity (Nov 11); Finland closed airspace and sea; drones crossed Estonian airspace; Bild reports Russia floated Finland leaving NATO.
5. AP: Russian military satellites over Saudi targets around Houthi strikes (Oct 28).
6. Finland's Fitburg cable verdict (Nov 5) - the first conviction of its kind.
7. Hoax bomb-threat waves across European airports, airlines, broadcasters and 6,000 Italian schools.
8. IAEA quarterly report (Nov 13) and the Assembly of Experts' NPT-review call (Nov 12).
9. Iran's threats against Armenia over the US-run Trump Route; this, not the Caspian, is the live Caucasus flashpoint.
10. IRGC claim of a strike on a US radar in Bahrain (Nov 13) after a US strike on a Sirik telecom tower; missile range cap lifted (Nov 7).
11. FAA nationwide ground stop (Nov 13) and Microsoft 365 outage (Nov 12) - both currently explained as non-hostile, both worth a re-check.
12. Iraq: Iran reportedly stopped paying the militias; armed standoff between Kataib Hezbollah and the government; Baghdad on highest alert (Nov 13).
13. Syria-Saudi defence deal; Syrian troops heading to Saudi Arabia.
14. Check Point gateway wiper attacks on Israel using China-linked tooling (unattributed); Quantum Systems update-server compromise grounding German military drones.
15. The Starshield cap looks like a US-side restriction that has widened to occupied Ukrainian territory, not outside interference.
16. Israel Hayom: alleged Iranian drone plot against Trump; US Treasury chief reportedly moved to a military base (both CLAIMED, single-source).
17. Houthi "transit permits" for Bab al-Mandeb are being taken up by some shippers.
18. Kayhan's list of European targets includes Albania and omits Portugal and Germany (as far as I could see).

## Follow-up needed (search budget ran out)

Red Sea and Taiwan cable status; NetBlocks / Kentik November data; GPSJam-type data for the Baltic, Black Sea and eastern Mediterranean in November; Russian and Chinese co-orbital activity; Kremlin, Baku and Astana statements on Iron Gate; the FT cable-mapping original; the French government's own attribution text; Gaza / West Bank / Jordan / Egypt; Japan and Korea incidents; the Shenzhen date and agenda; Starship Flight 15 payload.
