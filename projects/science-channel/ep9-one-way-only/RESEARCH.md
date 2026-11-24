# Ep 9 research: Every one-way-only is a story

Researched 2026-11-03 by a cloud Claude session for the Heartbeat Observatory Science channel. Science and engineering
history only. Every claim has a source number; the list is at the bottom. **[GK]** = common knowledge, no single source needed.
"Not established" = the evidence is thin. **Disputed** = sources disagree; the script must say so. **Note on method:** WebFetch
was blocked in this cloud session for wikipedia.org and some other hosts, so these facts come from WebSearch result summaries of
the pages listed. Codex should open the primary pages (especially the CFR and Federal Register texts) before render.

**Watch-outs for the script (read first):**
- **Murphy's Law: the origin story is DISPUTED in almost every detail** (number of sensors, who wired them, who rode the sled,
  who named the law). Similar sayings existed before 1949. Tell it as "the story goes". [1][2][3][4]
- **Poka-yoke is often credited "at Toyota", but the best-known early case (the spring dish) was at Yamada Electric, 1961.**
  Shingo worked with Toyota and many other factories. Do not say he invented it at Toyota. [5][6]
- **The diesel nozzle rule is really about LEADED gas.** The US law (1970s) made the unleaded nozzle thinner and the filler
  neck narrower to keep leaded gas out of catalytic-converter cars. Diesel nozzles are wider (an industry standard, not the
  same EPA rule) and also don't fit. **It only protects one way:** a gas nozzle fits a diesel tank. [7][8][9][10]
- **Brake-to-shift is US law only since 1 Sep 2010**, for vehicles under 10,000 lb with an automatic and a Park position. [11]
- **SIM cut corner: no ETSI/ISO text found stating the reason.** The keying purpose is consistent across phone manuals and
  explainers, but that is secondary sourcing. [13]

---

## 1. The question, in one line
Why do so many everyday things only fit or work one way? Because many of them are fixes for mistakes people already made.

## 2. Murphy's Law (1949)
*Summary: real people, real project, real tests; the famous moment is retold many ways.*
- Project MX981 (1947 to 1954) at Muroc Army Air Field, later Edwards Air Force Base, California, tested human tolerance to
  sudden deceleration on a rocket sled on rails (the "Gee Whiz"), on a track first built for missile work. [1][3]
- Air Force flight surgeon John Paul Stapp led the human tests and rode the sled himself in many runs. [3]
- Captain Edward A. Murphy Jr., an engineer from Wright Field, Ohio, supplied sensors (usually described as strain gauges in
  the harness) to measure the forces. [1][4]
- **The story:** in 1949 a run gave zero readings because the sensors had been installed wrong, wired backwards. [1][2]
- **Disputed details:**
  - How many sensors (four, six, sixteen are all told). [1]
  - Who rode: Stapp in most tellings; some say a chimpanzee. [1]
  - Who made the wiring error: a technician (most tellings) or Murphy himself (Time's version, per one source). [1]
  - Who named it: project manager George Nichols said the team named it, partly mocking what he saw as Murphy's arrogance;
    Murphy's son Robert says it came from his father; Murphy himself gave different accounts of who named it. Researcher and
    filmmaker Nick T. Spark investigated (Annals of Improbable Research, 2003; book "A History of Murphy's Law", 2006) and found
    the evidence on each side weak or inconsistent. [2][4]
  - Earlier sayings: similar ideas were in print before 1949 (a 1945 "mythical fourth law of thermodynamics", "anything can
    happen and usually does"); a magicians' version has been traced to 1908 (one researcher, not checked here); the American
    Dialect Society list reports a use of the name "Murphy's Law" in early 1949 from an interview with physicist Howard P.
    Robertson. [2][4]
- Stapp made the law public, telling reporters the team's good safety record came from believing in Murphy's Law and working to
  get around it: assume what can go wrong will, and plan for it. [1][3]
- Plain version usually quoted: "If anything can go wrong, it will." Exact original wording: **not established.** [1][2]

## 3. Poka-yoke (Shigeo Shingo)
- Shigeo Shingo (1909 to 1990), Japanese industrial engineer, consultant and trainer for many factories including Toyota; a key
  figure in the Toyota Production System. [5][6]
- Poka-yoke = mistake-proofing: a device or method that makes a mistake impossible or makes it obvious right away. Shingo split
  them into "control" (stops the process) and "warning" (signals) types. [5][6]
- Name: the idea was first called baka-yoke ("fool-proofing"); changed to poka-yoke ("avoiding inadvertent mistakes"). Why it
  changed is told different ways; Shingo said he chose the new name himself. [5]
- **Early case, 1961, Yamada Electric:** a switch needed two small springs and workers sometimes forgot one. Fix: first count
  two springs into a small dish; a spring left in the dish shows a step was missed. Shingo described it in "Zero Quality Control:
  Source Inspection and the Poka-Yoke System". Widely cited as an early case; "the first" is **not established**. [6]
- Core idea: don't blame the worker; design the process so an error can't pass. [5][6]

## 4. The fuel nozzles (United States)
- In the 1970s EPA required unleaded gas nozzles with a spout tip no wider than 0.840 in (2.134 cm), and required cars whose
  emission controls (catalytic converters) leaded gas would damage to have a filler-inlet restrictor that blocks a nozzle
  0.930 in or wider. Rules first published 1973 (38 FR 26450), for the catalytic-converter cars of the mid-1970s. [7][8][9]
- Purpose stated by EPA: admit the unleaded nozzle but not the larger leaded one. [9]
- Leaded gasoline for cars ended in the US; in 1996 EPA removed the leaded-nozzle provisions but retained the filler-inlet size requirement (Codex fix 11/4), and
  kept the 0.840 in unleaded nozzle limit (40 CFR 80.22, later 1090.1550). [8][9]
- Industry standard SAE J285: unleaded spouts nominal 13/16 in (20.6 mm); spouts for all other fuels 15/16 in (23.8 mm) or more.
  Diesel nozzles sold today are typically 15/16 in. [10]
- Effect: a standard diesel nozzle won't fit most gasoline cars. A gasoline nozzle does fit a diesel filler, so the protection
  works one way. Some stations use smaller nozzles on diesel pumps, and some vehicles have wider necks. [10][12]
- (Not used: Europe's nozzle sizes; many newer diesel cars add misfuel inhibitors. Not researched this session.)

## 5. Brake to shift out of Park
- FMVSS 114 (Theft Protection and Rollaway Prevention), S5.3: vehicles under 10,000 lb GVWR with an automatic transmission that
  has a Park position, made on or after 1 Sep 2010, must have a brake transmission shift interlock: the shifter can't leave Park
  unless the service brake is pressed, whatever the key position. [11]
- Required by the Cameron Gulbransen Kids Transportation Safety Act of 2007, signed Feb 2008 (named for a child; aimed at
  child safety around vehicles). [11]
- Automakers had a voluntary agreement to fit it by 1 Sep 2010 anyway. [11]

## 6. The microwave door
- 21 CFR 1030.10 (FDA performance standard for microwave ovens): at least two operative safety interlocks; at least one can't be
  operated by any part of the body or an inserted object of set size; failure of one part must not make all interlocks
  inoperative; and a means of monitoring the interlocks. [14]
- FDA has documented ovens running with the door open due to miswiring, and gives a service test for the monitor circuit. [14]
- (The rule's effective date, ovens made after October 1971, was not re-checked this session; not in script.)

## 7. The SIM card's cut corner
- SIM cards (mini, micro, nano / 2FF, 3FF, 4FF) all keep a notched, cut corner; the 2012 ETSI nano-SIM kept it. [13]
- Purpose: orientation keying, so the card fits the slot or tray only one way, contacts line up, and pins aren't damaged.
  Consistent across manuals and explainers; **no standards text found stating it.** [13]

## 8. USB-C: the other fix
- USB Type-C Specification 1.0 completed and announced Aug 2014 (11 or 12 Aug, sources differ by a day), by the USB 3.0
  Promoter Group, then managed by USB-IF. [15]
- The connector is rotationally symmetric: the plug goes into the receptacle either way up. Reversible plug orientation was
  listed as a headline feature. [15]

## 9. The closing idea
- "The world looks well designed partly because it is covered in patches from mistakes people already made" is the episode's
  framing, illustrated by sections 2 to 8. It is an interpretation, not a measured fact; the script says "many", not "all".

---

## Sources (accessed 2026-11-03)
1. Military.com, "The Real-Life Murphy and How 'Murphy's Law' Came to Be": https://www.military.com/history/real-life-murphy-and-how-murphys-law-came-be.html ;
   Wikipedia, Murphy's law (origin section): https://en.wikipedia.org/wiki/Murphy%27s_law
2. Improbable Research, "The 100th birthday of Murphy" (2018) and "A look back at a look back for Murphy's Law" (2019):
   https://www.improbable.com/2018/01/10/the-100th-birthday-of-murphy-the-murphy-of-murphys-law/ ; https://www.improbable.com/2019/12/10/a-look-back-at-a-look-back-for-murphys-law/ ;
   Word Origins: https://wordorigins.org/big-list-entries/murphys-law ; ADS-L "A Budget of Murphy's Law" (2019): https://listserv.linguistlist.org/pipermail/ads-l/2019-November/156065.html
3. Air and Space Forces Magazine, "Valor: The Track to Survival": https://www.airandspaceforces.com/article/valor-the-track-to-survival/ ; Wikipedia, John Stapp: https://en.wikipedia.org/wiki/John_Stapp
4. Dayton Innovation Legacy, "Edward A. Murphy, Jr.": https://www.daytoninnovationlegacy.org/murphy.html ; Wikipedia, Nick T. Spark: https://en.wikipedia.org/wiki/Nick_T._Spark ;
   Improbable Research, "The Fastest Man on Earth" (AIR 9:5, 2003): https://improbable.com/the-fastest-man-on-earth/
5. Lean Blog, "Poka-Yoke and Shigeo Shingo: Why 'Foolproofing' Became Mistake-Proofing" (2024): https://www.leanblog.org/2024/02/shigeo-shingo-mistake-proofing-poka-yoke/ ;
   GoLeanSixSigma on Shingo: https://goleansixsigma.com/shigeo-shingo-grand-daddy-quality/
6. Mistakeproofing.com tutorial: https://mistakeproofing.com/?p=17 ; Michel Baudin on Shingo's spring example: https://michelbaudin.com/tag/mistake-proofing/ ; Wikiwand, Poka-yoke: https://www.wikiwand.com/en/Poka-yoke
7. 40 CFR 80.22 (2010 text): https://www.gpo.gov/fdsys/pkg/CFR-2010-title40-vol16/pdf/CFR-2010-title40-vol16-sec80-22.pdf ; FindLaw: https://codes.findlaw.com/cfr/title-40-protection-of-environment/cfr-sect-40-80-22/
8. 40 CFR 80.24 (restrictor, 0.930 in): https://codes.findlaw.com/cfr/title-40-protection-of-environment/cfr-sect-40-80-24/ ; Federal Register, 6 Jun 1996: https://www.govinfo.gov/content/pkg/FR-1996-06-06/html/96-14307.htm
9. Federal Register, 24 May 2002 (purpose of the restrictor): https://www.govinfo.gov/content/pkg/FR-2002-05-24/pdf/02-12846.pdf ; 40 CFR 1090.1550: https://www.customsmobile.com/regulations/40/1090.1550
10. SAE J285 "Gasoline Dispenser Nozzle Spouts": https://saemobilus.sae.org/content/j285_199901 ; Fill-Rite nozzle data sheet (13/16 gas, 15/16 diesel): https://www.jmesales.com/content/docs/Fill-Rite/FIL-BR-967-Nozzle-Data-Sheet.pdf
11. Federal Register, 30 Mar 2010, FMVSS 114 final rule: https://www.govinfo.gov/content/pkg/FR-2010-03-30/pdf/2010-7078.pdf ; Federal Register, 25 Aug 2009 NPRM: https://www.govinfo.gov/content/pkg/FR-2009-08-25/pdf/E9-20384.pdf ;
    Justia copy: https://regulations.justia.com/regulations/fedreg/2010/03/30/2010-7078.html
12. Mental Floss, "Here's Why Confusing Diesel With Gas at the Pump Is a Problem": https://mentalfloss.com/article/92463/heres-why-confusing-diesel-gas-pump-problem ; Broken Secrets: https://brokensecrets.com/2010/06/09/diesel-fuel-nozzles-dont-fit-in-standard-fuel-cars
13. TechCrunch, ETSI nano-SIM (4FF) standard, 2012: https://techcrunch.com/?p=564578 ; ZTE manual (cut corner orientation): https://www.manualslib.com/manual/1176862/Zte-T81.html?page=7 ;
    India Herald explainer (secondary): https://www.indiaherald.com/Technology/Read/994883818/-Why-Is-a-SIM-Card-Cut-at-the-Corner-The-Hidden-Purpose-Explained
14. 21 CFR 1030.10, Cornell LII: https://www.law.cornell.edu/cfr/text/21/1030.10 ; eCFR Part 1030: https://www.ecfr.gov/current/title-21/chapter-I/subchapter-J/part-1030 ;
    FDA/HHS, "Open Door Operation of Microwave Ovens as a Result of Oven Miswiring": https://www.hhs.gov/guidance/sites/default/files/hhs-guidance-documents/FDA/Open-Door-Operation-of-Microwave-Ovens-as-a-Result-of-Oven-Miswiring-%28PDF-Only%29.pdf
15. AnandTech, "USB Type-C Connector Specifications Finalized" (Aug 2014): https://www.anandtech.com/show/8377 ; The Register, 12 Aug 2014: https://www.theregister.com/2014/08/12/reversible_usb_connector_ready_for_largescale_production/ ;
    USB 3.0 Promoter Group announcement (PDF copy): https://docs.ampnuts.ru/eevblog.docs/Standards/USB%203.1/USB_Type-C_Specification_Announcement_Final.pdf

## Could not confirm (do not state as fact in the episode)
- The exact words Murphy or Stapp said in 1949 (several versions).
- The 1877 Alfred Holt and 1908 magicians' versions of the saying (not found / not checked).
- That the Yamada Electric dish was Shingo's FIRST poka-yoke.
- A standards document (ETSI/ISO 7816) stating why the SIM corner is cut.
- Whether the 1970s filler restrictor applied to the 1975 model year exactly (the 1973 rule and catalytic-converter era are confirmed).
- Whether the brake shift interlock law followed specific child deaths (the act's child-safety aim is confirmed; the incidents behind it were not checked).
