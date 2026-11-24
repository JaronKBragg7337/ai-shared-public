# Safety signal scale v4 - MERGED DRAFT (11/15, not live)

**Read first:**
- **DRAFT ONLY. The live scale in tools/safety_signal.py is untouched and the live level was not changed.** Satya keeps the
  old boxes until Jaron says yes. Shadow mode stays on.
- **The numbers change meaning.** In this draft, 4 = "do your plan today" (old 5 MOVE) and 5 = "hold where you are, off the
  roads". Change the digits once, with the printed card, not in pieces.
- **Backtest result: this past week tops out at 3 (about 8 hours on 11/14, the Peoria bomb). Zero 4s. I found no real
  reason for a 4** - nothing that people's lives run on (power, fuel, water, phones, money, food, 911) went down at home or
  in our region.

Sources of each part are tagged: **[J]** Jaron's own rules, **[L]** live script, **[v2]/[v3]** Claude's proposals,
**[F]** Fable's blind design (research/worrier/scale-design-2026-11-15.md).

---

## The idea in three lines
1. Two dials on the page [v3]: **THREAT** (who is attacking, how close, is it over) and **STABILITY** (are the nine things
   life runs on still working [F]: power, water, fuel, food/pharmacy, payments, phones/internet, 911/hospitals, roads/air,
   order). The number is the higher of the two.
2. **Threat alone stops at 3** [F, v3]. 4 and 5 need the stability dial to break near us, with a short list of exceptions
   (a foreign state striking the mainland, an order for our county). That is what keeps 4 rare.
3. Rings [F]: **Home** = about 50 miles from where a household sleeps. **Region** = about 250 miles (Chicago, Indy, Detroit,
   Toledo, Columbus, Cincinnati, Peoria) OR anything we are wired to (our PJM/MISO grid, the pipelines and refineries that
   feed Indiana, the payment systems). Everything else = Nation / World. Far events still raise the number to 2-3, so the
   guard never drops [J note 1]; only 4 needs it near or connected.

## The scale (any ONE box is enough; highest box wins [L])

### 0 QUIET
**True:** nothing open that touches the US or the nine functions.
**Do:** live normally. Standing kit: two weeks of water/food/meds, half a tank or better, some small bills, the printed
household card [F, J 3:51].

### 1 WATCH
**True (any one):**
- War or tension abroad involving the US or allies, including ongoing fire in the same hot zone (baseline rule) [L, F]
- A serious report or claim that nothing checkable backs up yet (single source, a side's own claim, a disputed leak) [F]
- An old event newly reported - it counts on the day it HAPPENED, not the headline day [J, F]
- A closed event in the Region (cause found, person caught, fixed); a storm/cold watch for Home [F]

**Do:** nothing. Shows on the page. No buzz.

### 2 TOP OFF
**True (any one):**
- Abroad, something NEW actually lands (confirmed, not just claimed): a new country hit, a new kind of target hit (land
  energy sites), an attack on US forces or bases outside the usual zone [L box 3, moved down]
- A plot or threat report backed by a COSTLY action: officials moved to bases, aircraft moved off a base, embassies
  emptied, flights restricted [F rule 5, v2]
- An open event in the Region (attack or unexplained failure, nobody caught), one place [F]
- A function failed nationwide for 2+ hours and the cause is still unknown [F]
- Two open events in different functions inside 7 days anywhere in the US (a pattern; label it: causal chain / shared
  cause / same time only) [J 11/14 patterns, F]
- A DHS NTAS bulletin [F]
- An Indiana fuel/energy emergency about SUPPLY (shortage, outage). A price or gas-tax break does not count [L, narrowed]
- A national fuel shock: a sharp US gas spike plus rationing talk [L]
- One function shaky at Home: storm warning plus a grid alert; more than 1 in 10 stations dry in a Region city; cards/EBT
  down statewide 4+ h; local hospitals turning ambulances away [F]
- A known flashpoint date (disputed election, verdict) AND stores boarding up or the Guard pre-positioned in a Region
  city [F]
- A chemical/biological weapons report only if a costly action backs it (e.g. Israel's Home Front Command issues
  guidance); otherwise it is a 1 [L, narrowed]

**Do (cheap, about an hour, fine if nothing happens) [J]:** fill the tank, some cash, refill meds, charge everything,
glance at the kit, make sure the card is filled in. One buzz, daytime only.

### 3 GET SET
**THREAT boxes:**
- Three open events (cause unknown or nobody caught) in different functions inside 72 hours anywhere in the US, counted by
  event date; or two at once in the Region [J patterns, F]
- A foreign state confirmed to have actually KNOCKED OUT a function on US soil (not just "got into a system") [F]
- An open attack at Home (the person is still out there) [F]
- **Wartime rule:** while the US is trading fire with a state, an open attack on a power/fuel/water/phone site in the
  Region counts here until it is shown to be one site with no second device [F]
- A DHS NTAS "elevated" alert [F]
- A nuclear threat moving from words to steps; confirmed chemical/biological steps [L]

**STABILITY boxes:**
- One function down at Home with no fix time, or a fix time over 24 hours [F]
- Two functions down across the Region or across several states for 6+ hours, cause unknown [F]
- Banks anywhere limiting withdrawals; card networks down nationwide 4+ hours [F, v3]
- Two nights running of looting or riots in a Region city [F, v3]
- A multi-state grid failure anywhere with no fix time (the trucks and panic buying reach us in a day or two) [F]
- Two or more early signs at once in the Region: ATM limits, fuel lines/dry stations, empty shelves in several cities,
  911 delays or police sick-outs, insurers pausing policies, curfews [v3]

**Do (still reversible; nobody quits a job or leaves home) [J]:** pack the vehicles, bring the household together, check
in morning and night, and **decide stay or go now, while it is calm**, so 4 is one word, not a discussion [F]. Households
on the early list act as if it is 4 [F rule 7]. Buzz at any hour.

### 4 MOVE (do your plan today)
**Needs a STABILITY box, or one of the marked exceptions:**
- Two or more functions down at Home with no fix time or a fix over 48 hours (in freezing weather, power counts as two:
  power and heat) [F]
- Power down across the Region with no fix time, even if our lights are still on [F]
- A far grid or payment failure has reached us (local stations dry, shelves stripped, cards failing), or has run 72 hours
  with no fix [F]
- Cards, ATMs or EBT down nationwide over 24 hours; or banks in Indiana limiting withdrawals [F, v3]
- More than half the gas stations at Home dry with no resupply date [F]
- Looting or riots at Home past one neighborhood; or in three or more Region cities at once; or a curfew at Home [F, v3]
- *Exception:* a foreign state knocks out a function in the Region, or two or more attacks in the Region inside 72 hours
  with nobody caught [F]
- *Exception:* a foreign state's military strike on the US mainland; any nuclear weapon use [F, L]
- *Exception:* an official evacuation/shelter order for your county, or an NTAS "imminent" alert naming Indiana or the
  Midwest. An order for your own address always wins for that household [L, F rule 15]

**Proof needed:** two hard sources (meters, maps, official orders) or a network member's own eyes plus one, AND a second,
different AI reading the same sources gets the same level. That is a limit inside the script, not a human approve
button [F rule 17].
**Do:** run the plan in daylight while roads and pumps still work. For many households the plan is to lock in at home.

### 5 HOLD (collapse risk)
**True (any one):**
- Three or more functions down at Home with no fix date, and one of them is order or 911 (looting nobody stops, police
  not coming) [F]
- Level 4 true at Home for 72+ hours and no outside help arriving [F]
- The grid or the money system broken across a big part of the country (roughly a quarter of the states or a whole grid
  region) for 72+ hours with no fix date, with looting or riots in several cities - "half the country in chaos never
  comes back the same" [J 3:49]

**Do:** be where your plan put you and stay. Travel only to get away from direct danger. Group up, check in at set times
by the backup method (radio, walkie, paper schedule). Guard water, heat, medicine. **Stay away from the flashpoints:
grocery stores, pharmacies, gas stations, gun shops, crowds** [F, J street lens].

---

## Rules for Satya (apply every 4 hours, in this order)
1. **Count by event date.** Anything that happened more than 7 days ago is a 1 at most, plus a "thin cushion" note on that
   function (water, fuel) [J, F rule 10].
2. **Proof caps.** A claim or report with nothing behind it = 1. One costly action behind it = 2. Level 3+ needs two hard
   sources or a member's eyes plus one [F rule 5]. Tag every reading **solid / partly / thin**; thin can't go above 2
   [v3, F].
3. **Baseline.** Weeks of the same attacks in the same hot zone (Hormuz mines, Red Sea shipping, US-Iran fire at Qeshm) are
   background = 1 [L].
4. **Domestic with a known motive scores one lower** than the same event foreign or unexplained [J]. If nobody is caught,
   it still stays "open" for decay [F].
5. **Ties:** in the first 24 hours of a new event, a tie goes up. After 24 hours with no new facts, a tie goes down. (This
   replaces "unsure = always higher".) [F rule 6]
6. **Decay:** a level drops one step after 72 hours with no new box ticked [v3]. A closed event drops one step after 24
   hours [F]. Down at most one step per day. A failed function doesn't drop until it has worked 48 hours straight [F].
7. **No short triggers.** "Held at a higher expectation" is shown as an arrow (2 ↑), not a hair-trigger to the next
   level. The live short trigger is what produced the 11/13 4. [new]
8. **Show it as one number, one arrow, one proof word**, e.g. "2 ↑ partly", with both dials under it [F rule 13, v3].
9. **Buzz:** 1 never. 2 once, daytime. 3+ any hour. Going down = a quiet note [F rule 14].
10. **Keep score:** every 2+ call graded 30 days later (right / early / false alarm); false-alarm count on the page [F, J
    trust budget].

## Offline plan (the signal's real job is the days before 5) [J 3:51, F]
- Printed card per person: meeting point, backup point, routes, who picks up whom, stay-or-go decided at 3. Same card
  saved offline on phones.
- Backup channels: crank/battery radio (NOAA + AM news), paper contact list, maybe GMRS walkies.
- The page says when it was last checked; older than 6 hours shows **STALE**, never calm [F rule 16].
- **No-signal trigger - JARON'S OPEN CHOICE.** Claude's suggestion: power AND phones both down 6 hours = treat as 4 and run
  your plan; only 2 hours if the radio is reporting something big. (Fable's other option: 2 hours = get set, 6 hours = run
  the plan.)

## How often each level should fire (cry-wolf budget) [F]
| Level | Expected | Too loose if |
|---|---|---|
| 0-1 | most days | |
| 2 | a handful of times a year, days at a time | more than ~12 a year |
| 3 | once a year or less | more than twice a year |
| 4 | about once a decade | more than once in 3 years |
| 5 | hopefully never | |

---

## BACKTEST: every reading in state/safety-signal.md
Live = what was set. Merged = what this draft gives on the facts written in that reading. (Reading 1 was on the old 0-3
scale.)

| # | When | Live | Merged | Why (merged) |
|---|---|---|---|---|
| 1 | 11/01 1:59 PM | 1 (old scale) | 1 | Iran "no limits" readiness order = words; no new hits |
| 2 | 11/03 1:15 PM | 2 | 1 | US-Iran fire at Qeshm = same zone; target list = words; Indiana EO is a gas-tax break, not a shortage |
| 3 | 11/03 1:20 PM | 3 | 1 | Tanker hits near Saudi/Oman = baseline; "unsure = higher" gone |
| 4 | 11/03 1:55 PM | 2 | 1 | Same facts |
| 5 | 11/03 4:01 PM | 2 | 1 | Same; Iran's drone-kill claims unverified |
| 6 | 11/03 6:30 PM | 3 | 1 | NYT chemical-weapons report: disputed, no costly action behind it = caps at 1 |
| 7 | 11/03 8:11 PM | 3 | 1 | Same |
| 8 | 11/04 8:04 AM | 3 | 1 | Same report, nothing new landed |
| 9 | 11/04 12:02 PM | 3 | 1 | Same |
| 10 | 11/04 4:04 PM | 3 | 1 | Same |
| 11 | 11/04 8:06 PM | 3 | 1 | Same |
| 12 | 11/05 8:12 AM | 3 | 1 | Same; gas-tax EO extended (price, not supply) |
| 13 | 11/05 12:10 PM | 3 | 1 | Same; Qatar tanker hit = Gulf shipping baseline |
| 14 | 11/05 4:04 PM | 3 | 1 | Same |
| 15 | 11/05 8:14 PM | 3 | 1 | Same |
| 16 | 11/06 8:19 AM | 3 | 1 | Same |
| 17 | 11/06 12:23 PM | 3 | 1 | Same |
| 18 | 11/06 4:09 PM | 3 | 1 | Trump weighing strikes = words |
| 19 | 11/06 8:07 PM | 3 | 1 | US "minor" Qeshm strikes = ongoing fire, same zone |
| 20 | 11/07 4:08 PM | 3 | 1 | IRGC drops missile-range limit = capability talk, not a hit |
| 21 | 11/07 8:11 PM | 3 | 1 | Houthi claims on Aramco/Riyadh: claims only, Saudi hadn't confirmed |
| 22 | 11/08 8:10 AM | 3 | 2 | Saudi CONFIRMS Aramco Tower damage = new kind of target actually hit |
| 23 | 11/08 12:05 PM | 3 | 2 | Same, inside 72 h |
| 24 | 11/08 4:06 PM | 3 | 2 | Same |
| 25 | 11/08 8:03 PM | 3 | 2 | Same |
| 26 | 11/09 8:05 AM | 3 | 2 | Same |
| 27 | 11/09 12:06 PM | 3 | 2 | Confirmed Saudi pipeline fire renews the box |
| 28 | 11/09 4:06 PM | 3 | 2 | Same |
| 29 | 11/09 8:04 PM | 3 | 2 | Same |
| 30 | 11/10 7:54 AM | 3 | 2 | Pipeline fire inside 72 h; French fridge hack (Oct) and US commissary probe (Aug) are old = 1 |
| 31 | 11/10 11:55 AM | 3 | 2 | US moved tankers off RAF Mildenhall over an Iran threat = costly action |
| 32 | 11/10 3:55 PM | 3 | 2 | Same |
| 33 | 11/10 7:56 PM | 3 | 2 | Same |
| 34 | 11/11 7:50 AM | **4** | 2 | Bessent moved to a base = costly action behind a plot report; nothing knocked out on US soil, so not 3 |
| 35 | 11/11 11:57 AM | 3 | 2 | Same; DOJ indictment = plotters caught (closed) |
| 36 | 11/11 3:54 PM | 3 | 2 | Didamar (Oman) = new country, a 2 (Oman later denied it) |
| 37 | 11/11 7:48 PM | 3 | 2 | Same |
| 38 | 11/12 7:51 AM | 3 | 2 | Third carrier, US pulled out of Qatar U17 = costly actions abroad |
| 39 | 11/12 11:53 AM | 3 | 2 | Same |
| 40 | 11/12 3:54 PM | 3 | 2 | New Houthi Saudi claims (unconfirmed) add nothing above 2 |
| 41 | 11/12 7:55 PM | 3 | 2 | Same |
| 42 | 11/13 7:52 AM | 3 | 2 | Iranian drones at US forces in Bahrain (confirmed, shot down) = attack abroad, 2 |
| 43 | 11/13 11:57 AM | **4** | 2 | WSJ water-cyber report: events July-summer = old, a 1 + water "thin cushion". No short trigger |
| 44 | 11/13 3:56 PM | **4** | 2 | Same |
| 45 | 11/13 7:52 PM | **4** | 2 | FAA nationwide ground stop, cause unknown = 2. Only one open US event (Microsoft's cause was stated) |
| 46 | 11/14 7:57 AM | **5** | 3 | Peoria bomb at an energy site, Region (230 mi), nobody caught, search live, during a shooting war = wartime rule. Not 4: nothing down at Home or Region |
| 47 | 11/14 11:47 AM | **5** | 3 | Same, search still live |
| 48 | 11/14 3:50 PM | **4** | 2 | Evacuation lifted, no second device = wartime bump ends. Still open (no suspect) + FAA + drone-plot report with officials moved = 2 ↑ |
| 49 | 11/14 7:56 PM | **4** | 2 | Same, 2 ↑ partly |

### Summary (hours from each reading to the next; last one runs to 11/15 4:00 AM)
| | Level 1 | Level 2 | Level 3 | Level 4 | Level 5 | Separate "4 or higher" episodes | Level changes (buzzes) |
|---|---|---|---|---|---|---|---|
| **Live, 11/1 - 11/15** | 47 h | 5 h | 230 h | 36 h | 8 h | **2** (11/11 ~4 h; 11/13-11/15 ~40 h incl. 8 h at 5) | 9 |
| **Merged, 11/1 - 11/15** | 162 h | 156 h | 8 h | 0 | 0 | **0** | 3 |
| **Live, 11/8 - 11/15 only** | 0 | 0 | 128 h | 36 h | 8 h | 2 | - |
| **Merged, 11/8 - 11/15 only** | 8 h | 156 h | 8 h | 0 | 0 | 0 | - |

**What it says:**
- Merged tops out at 3 for about 8 hours (Peoria, while the area was still being searched). Everything else this week is a
  2: top off, nothing more. **No 4: I found no real reason for one.** The nearest miss: had a second device turned up in
  the Region, or had a third unexplained US failure joined the FAA stop and Peoria inside 72 hours, it would still be a 3.
- Honest cost: that 8-hour 3 uses up this year's budget for 3s (once a year). A week with a shooting war, a real bomb at an
  energy site and the third nationwide air stop ever is plausibly that once-a-year week.
- 11/3-11/7 drops from 3 to 1 because the main reason (the chemical-weapons report) never had a costly action behind it,
  and the Indiana "energy emergency" is a gas-tax break, not a shortage. See question 3.

**Two things the backtest found in the live setup (not scale design, but they matter):**
1. **Overnight gap.** Readings ran at about 8 AM, 12, 4, 8 PM; nothing between 8 PM and 8 AM. Peoria's evacuation started
   8:02 PM ET on 11/13 and was first counted at 7:57 AM - 12 hours late. "Every 4 hours" needs a midnight and a 4 AM run,
   or at least a wire-alert wake-up.
2. Both live 4s came from loose boxes: "a credible named threat" (11/11) and the short trigger plus an old headline (11/13).
   Both are gone in this draft (rules 1, 2, 7).

---

## Open questions for Jaron (plain words)
1. **Do the numbers shift?** In this draft 4 means "do your plan today" (what 5 meant before) and 5 means "stay where you
   are, off the roads." Your 3:54 AM note said only 5 asks people to drop normal life. Here that line moves to 4, which is
   why 4 is made so hard to reach (zero times this week). OK, or keep 5 as "move"?
2. **No-signal rule:** if power AND phones are both out 6 hours (only 2 if the radio says something big), everyone runs
   their plan. Or Fable's version: 2 hours = get set, 6 hours = go. Which one goes on the printed card?
3. **War abroad by itself:** this draft keeps the ongoing Iran fighting at 1 (nothing to do) and only goes to 2 (top off)
   when something new actually lands. That is why 11/3-11/7 drops from 3 to 1. OK, or should any shooting war with US
   forces sit at 2?
