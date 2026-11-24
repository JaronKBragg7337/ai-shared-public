# W4 - US infrastructure and homeland events, Nov 7-14, 2026 (with notes back to Nov 1)

Compiled Saturday Nov 14, 2026 (afternoon CT). Public reporting only.

## READ THIS FIRST - limits of this pass

- **Search coverage was cut short.** The shared web-search budget ran out after about 14 searches. Everything after that came from opening known pages directly (Wikipedia current-events pages, NPR member stations in Illinois/Michigan/Ohio/Indiana, CISA, DHS, The Record, CyberScoop, BleepingComputer, gCaptain, The War Zone, Utility Dive, Votebeat, JTA, CSB, Ethanol Producer).
- **So "nothing found" below means "nothing on the pages I could open", not "nothing happened".** The categories I could NOT search properly: US substation shootings, fiber cuts, cell/911 outages, pipeline and refinery fires, rail signaling, payment systems (Fedwire/ACH), GPS interference, satellite problems, domestic drone sightings, militia plots, state emergency declarations, and Indiana/Ohio/Kentucky local news (wane.com, AP, BBC, Reuters, WaPo, CNN all refused the fetch).
- A follow-up pass with fresh search budget should redo those categories.

## Corrections to the brief (things the team's log had slightly wrong or out of date)

1. **The WSJ story is dated Fri Nov 13, not Nov 12, and it does not describe a new November water attack.** It says attacks "since this summer" locked operators out of control panels at "small-town water stations across the Midwest" (plural, no towns named, no dates). The tanker breaches were in September. It is a roundup of the summer campaign, not a fresh incident. Source: https://www.yahoo.com/news/us/articles/iran-expands-cyberattacks-greater-real-132640639.html
2. **The FAA failure now has a stated cause** (Sat Nov 14 briefing): a contractor, **L3Harris**, was swapping copper wire for fiber at "at least one remote location"; routers/switches overloaded. Exact error still under investigation. Not "cause unknown" any more, but not closed either.
3. **Microsoft's outage ran Nov 12 to the morning of Nov 14**, not one day, and Microsoft said it was "not caused by a cyber attack or AI agents."
4. **Peoria: police have NOT called it a bomb.** The mayor did ("Bomb is my interpretation"). Police say "credible threat", "rendered safe", contents "still being determined". Police also said **DHS is not involved**; ATF and FBI lead.
5. **No federal shutdown now.** Funding runs to **Dec 11, 2026**. But DHS (which holds CISA and TSA) already went unfunded for 76 days this year (Feb 14 - Apr 30).

---

## Event list

Format: date/time | place | what happened | stated cause | investigating | claimed? | source | label

### A. The known items - latest status

**A1. FAA nationwide ground stop**
- Fri Nov 13. Instability first seen ~3:36 PM ET; ground stop issued 3:44 PM (NPR) or 3:54 PM (Wikipedia); lifted 8:15 PM ET | all 22 Air Route Traffic Control Centers | intermittent radar and radio; no domestic departures for 4+ hours; 3,000+ planes in the air landed safely; Friday >9,000 cancelled and ~25,000 delayed (FlightAware); Saturday 3,200-4,100 more cancelled; Europe and Mexico held US-bound flights. Third nationwide ground stop ever (9/11, Jan 2023, now).
- Stated cause: Duffy, Fri: "Our switches, our routers actually got overloaded with data... because of that we shut the system down." Duffy, Sat: contractor L3Harris was changing copper wire to fiber; checking "user error," "installator error," or a "faulty router"; "Our contractor didn't meet the moment." Mullin, Fri: no "footprints" of an attack, "appears this was mechanically driven," "This is not another 9/11." FAA Administrator Bedford, Sat: no sign of foul play or AI involvement. Bloomberg (one unnamed official): FBI does not believe a cyberattack or crime caused it. CBS (via Wikipedia): an update to the private network caused a reboot and crash.
- Still open: why one router at one remote site took down the whole country ("still under investigation"); why the work was done on a busy Friday afternoon. No formal written root-cause report yet. L3Harris: "We are supporting the FAA in its investigation."
- AI system angle: FAA expanded the SMART AI traffic tool to all centers Nov 10. FAA and vendor Air Space Intelligence deny a link; Mullin on Friday said "You just can't rule out anything at this point."
- Investigating: FAA/DOT; Congress expected to ask (Lieu, Duckworth). No inspector-general probe seen yet.
- Claimed by anyone: no claim found.
- Sources: https://www.wglt.org/2026-11-14/faa-blames-fridays-ground-stop-on-equipment-issue-during-telecoms-network-upgrade ; https://www.michiganpublic.org/2026-11-14/telecom-outage-triggers-rare-nationwide-faa-ground-stop-stranding-travelers ; https://www.cnbc.com/2026/11/13/faa-ground-stop.html ; https://www.aljazeera.com/news/2026/11/13/us-grounds-all-flights-after-communication-issue ; https://www.25newsnow.com/2026/11/14/thousands-flights-canceled-airlines-work-dig-out-nationwide-ground-stop/ ; https://en.wikipedia.org/wiki/2026_FAA_communication_outage
- Label: outage ESTABLISHED. Cause (contractor upgrade + router overload) ESTABLISHED as the officials' account, root cause not final. "No cyberattack" = ESTABLISHED as stated by Mullin and Bedford on the record; the FBI view is CLAIMED (one anonymous source).

**A2. Peoria, Illinois - device at BioUrja Renewables ethanol plant** (about 215 miles from Fort Wayne)
- Fri Nov 13: 1:08 PM CT BioUrja reports a bomb threat; ~2 PM suspicious package found; 6:45 PM judged a credible threat, 1-mile zone set (5,000+ people, parts of downtown, Caterpillar buildings, East Peoria); 9:12 PM "rendered safe". Sat Nov 14: search 6 AM to just before 1 PM, nothing else found; evacuation and Illinois River closure (mile 160-164) lifted 1 PM CT.
- Stated cause/motive: none stated. Police say the threat was received "electronically"; they have not said what it said, by what channel, or what the device was. Chief Dixon: "We found a credible package that we believe to be a threat. We're not considering this a hoax." He declined to say whether it is treated as terrorism. Mayor Ali: "We know it's a bomb," later "Bomb is my interpretation."
- Investigating: ATF (Chicago Field Division) and FBI Springfield (SAC Ryan Presley: "We will work tirelessly to identify the individual responsible") lead a criminal investigation; Peoria PD, Illinois State Police, Coast Guard. Dixon said DHS was not involved. No BioUrja representative at the press conference.
- Claimed by anyone: no. No arrest, no suspect, no motive.
- Other sites threatened the same week? None found on Illinois public radio, Peoria TV, or the ethanol trade press. Not searched widely (see limits).
- Sources: https://www.wcbu.org/local-news/2026-11-14/peoria-evacuation-order-lifted-after-bomb-search-finishes-at-biourja-plant ; https://www.wcbu.org/local-news/2026-11-13/peoria-police-urge-evacuation-after-bomb-threat-at-biourja-renewables ; https://abcnews.com/US/peoria-police-urge-evacuations-after-reported-bomb-threat/story?id=138137440 ; https://chicago.suntimes.com/public-safety/2026/11/14/bomb-found-ethanol-plant-peoria-forces-evacuations-biourja-renewables ; https://www.25newsnow.com/2026/11/14/much-downtown-peoria-shut-down-due-bomb-threat-biourja/
- Label: threat + device treated as real = ESTABLISHED. "It was a bomb" = CLAIMED (mayor; police will not confirm). Any link to Iran or to anything else = NOT ESTABLISHED (no official or outlet has drawn one).

**A3. Microsoft 365 outage**
- Thu Nov 12 ~11:17 AM-noon ET through the morning of Sat Nov 14 | worldwide, 70+ countries | Outlook/Exchange Online, Teams, SharePoint, Copilot, Defender XDR. US House staff lost a legislative day; some law enforcement could not process bail payments; UK NHS cancelled some operations; a Canadian hospital network declared an infrastructure "code grey".
- Stated cause: settings applied to servers after an update; a process that sets up secure connections was overwhelmed; Microsoft rolled back a recent network configuration change. Microsoft: "not caused by a cyber attack or AI agents." (No formal post-incident report yet. The team's "health-check problem" wording was not what I found; closest is the overwhelmed secure-connection process.)
- Investigating: Microsoft. Claimed: no.
- Sources: https://en.wikipedia.org/wiki/2026_Microsoft_outage ; https://www.bleepingcomputer.com/news/microsoft/massive-microsoft-365-outage-disrupts-outlook-teams-copilot-worldwide/ ; https://www.aljazeera.com/news/2026/11/13/microsoft-hit-by-global-outages-what-happened-and-why
- Label: ESTABLISHED (outage and company's stated cause).

**A4. Iranian cyber campaign with physical effects (WSJ roundup)**
- Published Fri Nov 13 | Midwest water stations (since summer), two Texas-bound energy tankers (September), hundreds of European grocery refrigerators pushed to 120 F | operators locked out of control panels; ship networks breached; food spoiled, some fires.
- Stated cause/attribution: Check Point's Sergey Shykevich ties it mainly to CyberAv3ngers (Shahid Kaveh), under Iran's cyber command. US officials were "investigating" Iranian involvement in the tankers. Acting CISA head Nicholas Andersen: controllers are threatened by Iranian actors. Iran denies.
- Background that is firm: July 26-27 attack on 30+ Minnesota water systems (passwords and IP addresses changed on internet-exposed Rockwell controllers; some boil-water notices, flooding, low pressure; no contamination); FBI/EPA July 30 alert citing seven states; other reports say 12 states / 100 municipalities (one report, unverified). The July joint advisory "did not name a culprit" but said it resembled CyberAv3ngers.
- Sources: https://www.yahoo.com/news/us/articles/iran-expands-cyberattacks-greater-real-132640639.html ; https://www.cybersecuritydive.com/news/us-authorities-escalation-attacks-water-system-devices/826715/ ; https://www.kharon.com/brief/iran-war-cyberattacks-water-systems-cyberav3ngers
- Label: the attacks ESTABLISHED; Iran attribution = ATTRIBUTED-SUSPECTED (firms and officials point at Iran; no formal US attribution found); "12 states" CLAIMED.

**A5. DOJ indictment of three Iran-backed operatives**
- Unsealed Tue Nov 10, New York | Mohammad Baqer Saad Dawood al-Saadi, Mohsen Mohajeri, Mohammad Ali al-Hassani | eight counts; nearly 20 plots in Europe and the US tied to an IRGC-backed network; a New York synagogue named as a target; RAF Fairford plot (three vans, some with fuel barrels, stopped by UK police).
- FBI Director Patel: "This eight-count indictment shows the determination of Iran to commit terrorist attacks in Europe and the U.S."
- Source: https://cbn.com/news/world/irans-shadow-war-intensifies-terror-cells-go-live-while-cyber-and-military-threats-grow (secondary; DOJ release not opened)
- Label: ESTABLISHED (indictment exists; allegations unproven in court).

**A6. Bessent moved to a military base**
- Reported Nov 10-11 (NYT origin, picked up by CNBC, Reuters, Fox) | unnamed sources | Treasury: he "will not be deterred by the Iranian regime's threats." Reuters: severity "not immediately clear". No public link to the indictment.
- Source: https://www.cnbc.com/2026/11/11/us-iran-war-trump-hormuz-bessent-threats.html
- Label: ESTABLISHED that he moved (multiple outlets + Treasury comment); nature of the threat CLAIMED.

**A7. Alleged Iranian drone plot against Trump and senior officials**
- Sat Nov 14 | Israel Hayom, anonymous Israeli and US sources | Mossad passed details to the CIA after US agencies asked for help checking the threat; several officials said to be moved to secure sites; Trump said to have cancelled Saturday golf (Gulf News relaying the same report).
- Not confirmed by the CIA, White House or Iran. Context: Reuters reported in August that US agencies could not corroborate several earlier Israeli-supplied Iranian threat warnings. Also: on Nov 3 Trump announced the US will end military aid to Israel by year-end, and Israel is pressing Washington on Iran policy - a reason to read single-source Israeli warnings carefully.
- Source: https://www.israelhayom.com/2026/11/14/israeli-intelligence-warns-of-iranian-plot-to-target-trump-top-us-officials-with-drones/ ; https://gulfnews.com/world/mena/middle-east-war-trump-weighs-restraint-as-israel-warns-of-alleged-iranian-plot-1.500746947
- Label: CLAIMED (one outlet, anonymous).

**A8. NTAS**
- Checked Nov 14: "There are no current advisories." Last bulletin was June 22, 2025 (expired Sept 22, 2025). So through a year-long war, an indictment naming US plots, and a cabinet officer living on a base, DHS has issued no public bulletin.
- Source: https://www.dhs.gov/national-terrorism-advisory-system
- Label: ESTABLISHED.

### B. New items found this pass (Nov 7-14)

**B1. Tanker hits docked riverboat, New Orleans**
- Fri Nov 13 ~12:30 PM CT | Mississippi River, New Orleans | Marshall Islands-flagged asphalt tanker *Atlantic Asphalt* struck the docked American Cruise Lines paddlewheeler *American Heritage*, which capsized/sank; all survived, ~32 hurt; river closed mile 93-96.
- Stated cause: none stated. "The cause of the collision remains under investigation."
- Investigating: Coast Guard; NTSB go-team. Claimed: no.
- Source: https://gcaptain.com/tanker-strikes-docked-paddlewheeler-on-mississippi-river-causing-it-to-capsize/
- Label: ESTABLISHED; UNEXPLAINED.

**B2. Bulk carrier hits Tacony-Palmyra Bridge**
- Thu Nov 12 ~1:15 PM ET | Delaware River, Philadelphia-Palmyra NJ | Singapore-flagged *Strategic Alliance* struck the open draw span; span stuck up, major traffic disruption, no injuries.
- Stated cause: none stated. "The cause of the incident remains under investigation."
- Investigating: Coast Guard; Burlington County Bridge Commission. Claimed: no.
- Source: https://gcaptain.com/singapore-flagged-bulk-carrier-strikes-delaware-river-bridge-coast-guard-investigating/
- Label: ESTABLISHED; UNEXPLAINED.

**B3. Brooklyn building collapse**
- Wed Nov 11 | Brooklyn, NY | three-story apartment building next to a construction site collapsed; 8 dead, 17-19 hurt.
- Stated cause: not obtained (source pages refused); the construction-site detail is the only lead. Label: ESTABLISHED event; cause not checked.
- Source: https://en.wikipedia.org/wiki/Portal:Current_events/November_2026

**B4. Vanderbilt University ransomware**
- Found Mon Nov 9 | Nashville, TN (about 400 miles from Fort Wayne) | campus told to shut down devices and leave Wi-Fi; services back Tuesday.
- Claimed by: BYOD ransomware gang (new since September; claims 1M+ Social Security numbers). Investigating: university "with government agencies".
- Source: https://cyberscoop.com/vanderbilt-university-ransomware-attack-byod/
- Label: ESTABLISHED; criminal gang claim, no state link suggested.

**B5. FBI flash alert on "Artex" AI attack tool**
- Reported Nov 13 (alert released within the prior week) | FBI says the open-source AI platform lets criminals and nation-states "automate multiple phases of cyber intrusions at machine speed"; mostly Chinese-nexus users named; energy, telecom, healthcare, government among targets. No Iran mention.
- Source: https://therecord.media/artex-ai-tool-fbi-flash-alert
- Label: ESTABLISHED.

**B6. CISA fact sheet on refrigeration / cold-chain controllers**
- Nov 5 | CISA, FBI, HHS, USDA, DOT | "malicious cyber activity targeting industrial refrigeration and cold chain monitoring systems globally"; warns of fire hazard and spoiled inventory. Names no actor and no US incident. This is the US response to the European grocery attacks.
- Source: https://www.cisa.gov/resources-tools/resources/us-government-partners-urge-hardening-industrial-refrigeration-and-cold-chain-monitoring-systems
- Label: ESTABLISHED. No new Iran joint advisory this week: the latest is the July 22 update of the April controller advisory. CISA's public list for Nov 3-13 shows only routine "known exploited vulnerability" additions (15 flaws in six postings).

**B7. Heavy patch/zero-day week (background noise that matters)**
- Nov 10 Patch Tuesday fixed 1,000+ Microsoft flaws; Nov 12-13: new Windows privilege zero-day, Check Point gateway zero-day used to deploy a server wiper, Apache HTTP/2 critical flaw, ScreenConnect worm hitting IT service providers, 4,800 GitHub accounts hijacked. None tied to a US infrastructure outage.
- Source: https://www.bleepingcomputer.com/
- Label: ESTABLISHED.

**B8. US bases in England under threat (abroad, but it is the same adversary)**
- Nov 9: security levels at US bases in England "raised without explanation"; Nov 9-10: at least 12 KC-135s and three CV-22s left RAF Mildenhall "amid reports of Iranian threats" (WSJ/Reuters); Nov 13: suspected drones over RAF Lakenheath triggered a security response; Nov 12: UK court convicted two Iranian men of spying on Iran International journalists. Also Nov 9: USAF looking at netting to shield F-35s at Tyndall AFB, Florida from drone attack (a posture sign, not an incident).
- Source: https://www.twz.com/ ; https://www.reuters.com/world/europe/us-aircraft-evacuated-second-uk-base-due-iran-threat-wsj-reports-2026-11-10/
- Label: ESTABLISHED (movements); Iran link ATTRIBUTED-SUSPECTED. No domestic drone-over-base report found (not searched widely).

**B9. Violence and protest**
- Nov 8, Philadelphia: three arrested as pro-Palestinian and pro-Israel protesters clashed in Rittenhouse Square amid a boycott of six Jewish-owned restaurants. ESTABLISHED.
- Nov 12, Washington DC (Logan Circle): shooting spree, 1 dead, 4 hurt; gunman died by suicide. Motive not stated in what I could open. ESTABLISHED; ordinary-crime framing so far.
- Source: https://en.wikipedia.org/wiki/Portal:Current_events/November_2026

### C. Notable back to Nov 1 (and a little earlier)

- **Nov 5 - man detained near the White House** on suspicion of plotting to assassinate Trump; described as Venezuelan. Only seen on Wikipedia's year page; primary source not opened. Label: CLAIMED until a primary source is read. https://en.wikipedia.org/wiki/2026_in_the_United_States
- **Nov 4 - Tampa, Citibank building shooting**, 2 dead including the shooter. Motive not checked. ESTABLISHED.
- **Nov 3 (reported) - Oklahoma man charged** (Robin Patrick Martin) with mailing white-powder threat letters headed "DECLARATION OF WAR" to "well over 100" election offices since Sept 2024. An arrest, i.e. a threat closed. ESTABLISHED. https://cyberscoop.com/oklahoma-man-charged-white-powder-letters-election-officials/
- **Nov 2 (reported) - Michigan State University** listed by the BYOD gang (claims data on 1.3M people); MSU says no evidence its core systems were breached. CLAIMED (gang) vs denied. https://therecord.media/michigan-state-university-byod-gang-cyber-incident
- **Oct 26 - University of New Mexico Health**: ambulances diverted about two hours; BYOD claimed it, apologized, offered keys. ESTABLISHED. One secondary source also says Cleveland's University Hospitals ran for days without key systems about a week earlier - NOT ESTABLISHED by me (could not open an Ohio source).
- **Nov 2 - second wave of supermarket fridge/freezer hacks across Europe; Nov 3 - bomb hoaxes on seven European flights and on an Israeli cruise ship in Greece; week of Nov 9 - more flight and media-outlet bomb hoaxes in Europe, Nov 11 - bomb threats at Italian schools.** Officials called the flight threats "malicious hoaxes". ESTABLISHED as events; no actor named.
- **September - FAA communications outage (Newark/Philadelphia)** traced to a construction crew cutting a Verizon fiber line. ESTABLISHED; shows the FAA telecom layer fails for dull reasons too.
- **Nov 3 midterms**: Democrats won both chambers. Votebeat: "Despite fears, voting ran smoothly across the country"; "Trump's election threats fizzled." No attack on an election office, certification standoff, or militia plot found on the pages I could open. Mississippi Senate was called Nov 11 after a week of counting, without reported violence. Label: quiet so far, ESTABLISHED as far as checked.

### D. Capacity to respond

- **Shutdown:** none now. Current funding ends **Dec 11**; talks stalled as of Nov 11 (Republicans want war funding in the lame duck, Democrats want a clean short extension; a stopgap into Feb/March is the expected outcome). ESTABLISHED. https://en.wikipedia.org/wiki/2026_United_States_federal_government_shutdowns
- **DHS already ran dry for 76 days (Feb 14 - Apr 30, 2026)** - the longest shutdown in US history. 1,110+ TSA officers quit; FEMA paused non-disaster work. ESTABLISHED.
- **CISA:** lost roughly a third of its staff in the first year of this administration; election-security work cut; state/local sharing centers defunded; the Cyber Safety Review Board dismissed (so there is no standing body to do a public post-mortem on something like the FAA failure). Still no confirmed director: acting head (Nicholas Andersen, per WSJ); Trump named Palantir's Michael LoSapio around Nov 4 and Hill Democrats are already objecting. ESTABLISHED (CyberScoop, Feb 25 and Nov 2026). https://cyberscoop.com/cisa-personnel-cuts-trump-second-term-analysis/
- **Leadership churn the same fortnight:** White House chief of staff replaced Nov 6 (Wiles out, Miller in); DOJ civil-rights chief resigned Nov 5; Hegseth impeachment on the lame-duck agenda; DHS Secretary Mullin is recent in the job. ESTABLISHED (Wikipedia year page, CNN/CNBC headlines).
- **FAA:** officials themselves say the system "is going to continue to fail" (Duffy) and "you will have more of these". $12.5B approved, $30-50B more requested. Controller-staffing numbers not obtained.
- **FBI staffing:** not obtained.

### E. Midwest / within ~300 miles of Fort Wayne

- Peoria device (A2) - the one serious physical event, ~215 miles west.
- Summer water-controller attacks hit Minnesota hardest and "small-town water stations across the Midwest"; I found no named Indiana, Ohio, Michigan or Kentucky utility. Not established either way.
- Michigan State University cyber claim (C).
- Chicago O'Hare and Midway were the first airports ground-stopped Friday before it went national (Wikipedia). Fort Wayne-area flights were affected like everyone's.
- Indiana public radio (WFYI) showed nothing local in the categories asked. Fort Wayne TV (WANE) refused the fetch. **Indiana-specific local news is a gap in this pass.**

---

## Three bins

**EXPLAINED (cause stated and plausible)**
- Microsoft 365 outage - bad server/network configuration change; company says no attack.
- FAA ground stop - *mostly* here: contractor upgrade, router overload, three officials on record seeing no attack. Kept one foot in UNEXPLAINED because the root cause is "still under investigation" and nobody has explained how one router took down 22 centers.
- Vanderbilt, UNM Health, Michigan State - criminal ransomware gang (BYOD) claimed them.
- Oklahoma election-threat letters - suspect charged.
- September FAA telecom outage - construction crew cut fiber.

**UNEXPLAINED (no cause or actor stated yet)**
- Peoria device - no suspect, motive, content of the threat, or description of the device.
- New Orleans tanker strike - cause under investigation (NTSB).
- Delaware River bridge strike - cause under investigation (Coast Guard).
- Brooklyn collapse - cause not obtained by me (may be explained elsewhere).
- Nov 5 White House detention - details not obtained.
- DC and Tampa shootings - motive not obtained.

**ATTRIBUTED-SUSPECTED (officials or major outlets point at an actor)**
- Midwest water-controller lockouts, tanker network breaches, European refrigerator attacks - Iran (CyberAv3ngers), per security firms and unnamed officials; no formal US attribution found.
- The ~20 plots in the Nov 10 indictment, incl. a New York synagogue - Iran-backed network (DOJ allegation).
- Threats against Bessent; RAF Mildenhall/Fairford/Lakenheath - Iran (officials, unnamed).
- Drone plot against Trump - Iran, but single-source (CLAIMED).

---

## Shapes

**1. Friday Nov 13, a two-hour window: New Orleans tanker strike (12:30 PM CT), Peoria threat (1:08 PM CT), FAA instability (2:36 PM CT).** Plus Microsoft still recovering and the Delaware bridge strike the day before.
- Label: **SAME TIME ONLY.** Different sectors, different layers (a ship's handling, an emailed-or-similar threat plus a physical package, a router during a wiring job), different regions, and two of the five have on-the-record dull causes.
- What would show this is wrong: a claim of responsibility covering more than one; the FAA root-cause report finding tampering in the router or L3Harris's network; the NTSB finding the tanker's controls or navigation were interfered with; the Peoria threat text naming the war or other targets.

**2. Microsoft (Thu) then FAA (Fri) - both "an update overloaded the system".**
- Label: **SAME TIME ONLY**, with a weak **SHARED CAUSE** candidate that is boring: mid-November is the pre-holiday change window, and Tuesday was a 1,000-flaw patch day, so a lot of people were pushing changes at once. Mullin dismissed a link. No evidence the FAA network depended on the Microsoft services that failed.
- Wrong if: the FAA or L3Harris work is shown to have relied on Microsoft 365/Azure sign-in during the outage, or if both trace to the same faulty vendor update.

**3. Electronic threats: Peoria ("received electronically") and the European flight/media/school bomb hoaxes the same fortnight.**
- Label: **SAME TIME ONLY.** The key difference: Europe's were hoaxes; Peoria had a real object placed on site, which means a person was physically there. That points local, not remote.
- Wrong if: FBI ties the Peoria message to the same sender infrastructure as the European hoaxes, or other US plants turn out to have received the same message.

**4. Iran-linked pressure rising in one week: Mildenhall evacuation (Nov 9), indictment + Bessent (Nov 10), UK convictions (Nov 12), WSJ cyber roundup + Lakenheath drones (Nov 13), drone-plot report (Nov 14).**
- Label: **SHARED CAUSE** (one adversary, one war) - this is the real cluster, and it is mostly ESTABLISHED. But note part of it is a *reporting* cluster: the indictment and the WSJ piece describe months of earlier activity, not seven new attacks in seven days.
- Wrong if: the threat warnings are walked back, or it emerges they all trace to one uncorroborated intelligence stream (the August Reuters report on uncorroborated Israeli warnings is the caution here).

**5. Energy/fuel as a target class: ethanol plant (Peoria), energy tankers (September), fuel-laden vans at Fairford, water and refrigeration controllers.**
- Label: **SAME TIME ONLY** for Peoria versus the rest. The Iranian items share an actor; Peoria has no actor. It is tempting to put Peoria in the Iran pile because the sector fits. Nothing public supports that. Ethanol plants are also classic targets for disgruntled insiders, local grievances and extortion.
- Wrong if: FBI brings terrorism charges or names a foreign link; right now police say DHS is not even involved.

**6. Transport layer: two ship strikes in 24 hours plus aviation.**
- Label: **SAME TIME ONLY.** Ship strikes on bridges and docks are routine (see base rates). Worth one look only because Iranian actors breached two tankers' networks in September - so the NTSB/Coast Guard findings on *Atlantic Asphalt* (propulsion, steering, pilot error) are worth reading when they come.

**7. The thin-explainer shape.** Not an event cluster but it changes how to read all of them: CISA down a third with no confirmed head, the review board gone, DHS fresh off a 76-day lapse, NTAS silent all year, a Dec 11 funding cliff. Label: **SHARED CAUSE** for *slow or missing explanations*, not for the events. It means "no official statement" is weaker evidence of "nothing there" than it used to be - and also that officials saying "no attack" within hours (FAA) is fast, and should be re-checked against the written report.

### Base rates (from memory, approximate - I could not re-verify these this session)

- **FAA ground stops:** single-airport ground stops for weather or volume happen many times every day. **Nationwide** stops: three in history (Sept 11 2001; Jan 11 2023, a database file error; Nov 13 2026). So Friday is rare - but its one precedent in the last 25 years was also a contractor/maintenance error.
- **Bomb threats:** federal bomb-data reports count a few thousand a year in the US, i.e. dozens a week, mostly schools and businesses, almost all empty. Actual explosive devices found or detonated run in the low hundreds a year. A threat *plus a real object* at an industrial plant is uncommon - a handful a year at most. Peoria is above background.
- **Substation / grid physical incidents:** utilities report roughly 150-200 attacks, vandalism and suspicious-activity events a year to DOE, about 3-4 a week, nearly all copper theft or gunfire with no outage. Finding none this week on the pages I opened does not mean none occurred.
- **Big cloud outages:** a global multi-hour failure at a top provider happens every one to three months (AWS and Azure both in Oct 2025, Cloudflare Nov 2025, the CrowdStrike/Windows failure July 2024). Almost all are configuration changes. Microsoft's is ordinary in kind, long in duration.
- **Ship strikes:** the Coast Guard logs thousands of marine casualties a year; ships hit bridges and docks somewhere in the US most months. Two in two days is unremarkable; a capsized cruise boat is not, but severity is not cause.
- **Hospital/university ransomware:** several US healthcare or education victims every week. BYOD's run is normal criminal background.

---

## Top 3 worries

1. **Peoria.** The only event this week that is physical, on US soil, real (not a hoax), against a fuel site, and has no suspect, no motive and no description - 215 miles from Fort Wayne. It is most likely local or personal, but it is the item where the next fact matters most. Watch for: what the electronic message said, charges, and whether any other plant got the same message.
2. **The Iran-linked threat picture is established and climbing while the public warning system says nothing.** Indictment naming US plots and a New York synagogue; a cabinet secretary on a base; US aircraft pulled from UK bases; controllers at US water plants already tampered with this summer - and NTAS reads "no current advisories", CISA is a third smaller with no confirmed head, and funding lapses again Dec 11. The worry is less a single event than that a real one would be explained slowly.
3. **The FAA's one-router answer.** The official account is plausible and matches the Jan 2023 precedent. But "one remote site, one router, 22 centers down" is not yet explained, the no-attack call was made within hours, the FBI view is one anonymous source, and the body that would write an independent review was disbanded. Officials also say it will happen again. Treat as explained-pending-report, and read the written root cause when it lands.

## What looks scary but is probably ordinary

- **Microsoft outage** - a bad configuration change, like nearly every big cloud outage. Long, costly, not sinister.
- **FAA + Microsoft back to back** - coincidence in a heavy change week; no shared dependency shown.
- **Two ship strikes in two days** - routine maritime accidents until an investigator says otherwise.
- **The WSJ "Iran expands cyberattacks" headline** - a summary of summer and September events, not new November attacks. One sober read (Kharon/CSIS) is that the water hacks are cheap signaling meant to make the war feel close, with minimal damage so far.
- **The Trump drone-plot story** - one outlet, anonymous sources, from a government with a current interest in US Iran policy; US agencies could not corroborate similar warnings in August.
- **University ransomware (Vanderbilt, Michigan State)** - a criminal gang chasing data, not infrastructure sabotage.
- **Post-election unrest** - so far it has not happened; voting and counting ran smoothly, and the main election-threat story of the fortnight is an arrest.

## Things the brief missed

- The **L3Harris** name and the copper-to-fiber job as the FAA's stated cause; the **SMART AI tool** rollout to all centers three days earlier (denied as a cause, but Mullin would not rule it out on day one).
- The **New Orleans tanker strike** and the **Delaware River bridge strike** - two unexplained transport events inside the same 24 hours as Peoria and the FAA.
- **Peoria details:** police refuse the word "bomb"; DHS not involved; the Illinois River itself was closed to barge traffic for a day; the evacuation zone was sized to the plant's chemicals, not the device.
- The **Nov 5 CISA/FBI/HHS/USDA/DOT cold-chain warning** - the US government quietly telling grocers and cold-storage operators the European refrigerator attacks could come here.
- The **FBI flash alert on the Artex AI attack tool** - machine-speed intrusions, energy and telecom among targets.
- **US aircraft evacuated from RAF Mildenhall, security raised at US bases in England, suspected drones over RAF Lakenheath on Nov 13** - the same week's overseas half of the picture.
- **The 76-day DHS shutdown earlier this year** and CISA's one-third staff loss - capacity was already damaged before any Dec 11 lapse.
- **A man detained near the White House Nov 5** on suspicion of plotting to kill Trump (needs a primary source).
- **White House chief of staff changed Nov 6**; Hegseth impeachment in play - the people at the top of the response chain are in flux.
- **Trump's Nov 3 announcement ending military aid to Israel** - context for weighing Israeli-sourced threat reports.
- **The BYOD ransomware run** (UNM Health Oct 26, Michigan State, Vanderbilt Nov 9) - a hospital diversion and a Midwest university in three weeks.
- **Not checked at all and still owed:** substations, fiber cuts, 911/cell outages, refinery and pipeline incidents, rail, payments, GPS, domestic drones, militia plots, state emergency declarations, and Indiana/Ohio/Kentucky local reporting.
