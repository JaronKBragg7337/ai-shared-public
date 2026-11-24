• I’ll read the brief and its referenced materials, then produce the complete design in Markdown.

• The existing feeds already separate sourced facts from interpretation well. The new desk should add a shared event record, advance indicators, baseline comparisons, and independent challenge—not another headline sweep.

• # Connections Desk: design round 1

  ## Purpose

  The Connections Desk turns the existing watches into a checked picture of how events relate.

  It should answer five questions every day:

  1. What happened, and what is only claimed?
  2. Who met whom, and what changed afterward?
  3. What happened at the same time, and how often would that happen anyway?
  4. Which explanations fit the same evidence, and which fit best?
  5. What would settle the important unknowns?

  It is an analysis layer, not another headline collector. It does not set a safety level, predict a date for war, or turn simultaneous events into a coordinated story.

  Its main product is a graph of **events, people, organizations, claims, and relationships**, with every relationship labeled:

  - **ESTABLISHED**: supported by a cited primary source or sufficiently strong independent documentation.
  - **REPORTED**: a named source makes the claim, but it is not independently established.
  - **NOT ESTABLISHED EITHER WAY**: the available material does not settle the claim. State what would settle it.
  - **RULED OUT**: a specific, bounded claim is contradicted by cited evidence. This does not rule out every broader possibility.

  The phrase “no evidence” is not used.

  ---

  ## 1. How it sits on top of the existing system

  | Existing system | What the Connections Desk takes | What it does not do |
  |---|---|---|
  | **Atlas / Convergence** | Strategic events, official positions, cross-theater leads, and sources | Repeat Atlas’s daily sweep |
  | **Prep Watch** | Government preparedness moves, infrastructure failures, market reactions, and failure baselines | Rebuild the hourly watch or maintain a competing outage list |
  | **The wire** | Headline leads and timestamps | Treat a keyword alert as confirmation |
  | **The Worrier** | Uncomfortable scenarios and overlooked possibilities | Treat a worrying possibility as evidence |
  | **News desk** | The day’s published account and corrections | Delay the show or require a rewrite before publishing its own analysis |
  | **Satya** | Receives the checked daily summary | The desk never chooses or recommends Satya’s safety number |

  Atlas and Prep Watch remain the collection and first-check systems. The desk adds five things they do not currently provide:

  1. A shared event and claim record.
  2. Meetings and public-access ledgers.
  3. Pre-written scenario indicators.
  4. Baseline and coincidence tests.
  5. Independent red-team review of proposed connections.

  ---

  ## 2. Seats and responsibilities

  Five seats are enough. Models can rotate, but the same model should not propose and finally approve its own connection.

  ### Seat 1: Registrar

  **Default:** Codex Luna, with deterministic scripts for deduplication.

  - Imports Atlas, Prep Watch, wire leads, and news notes.
  - Splits stories into atomic events and atomic claims.
  - Separates event time, publication time, and first-seen time.
  - Groups copied articles into one source family.
  - Assigns stable event and claim IDs.
  - Preserves contradictory accounts rather than silently selecting one.
  - Adds no interpretation.

  ### Seat 2: Connections analyst

  **Default:** Grok Build.

  - Updates the meetings and access ledgers.
  - Checks events against the pre-written scenario indicators.
  - Proposes relationships and names the evidence for each.
  - Maintains both the pair view and the Russia-China-Iran-North Korea core view.
  - Must include an ordinary explanation for every proposed pattern.

  ### Seat 3: Baseline keeper

  **Default:** local Qwen for extraction and Python for calculations; DeepSeek for difficult classification when needed.

  - Maintains seasonal and day-of-week baselines.
  - Runs co-occurrence and before-and-after tests.
  - Tracks collection coverage so “missing” is not counted as “zero.”
  - Flags multiple-comparison problems.
  - Uses free data and local computation.

  Qwen should not be the sole judge of attribution or geopolitical meaning.

  ### Seat 4: Skeptic

  **Default:** Kimi, rotating with a second model for weekly audits.

  - Receives the frozen evidence pack, not the analyst’s conclusion first.
  - Tries to break every proposed connection.
  - Checks source independence, timing, base rates, alternative causes, and missing denominators.
  - Looks especially hard at connections that support Jaron’s hypotheses.
  - Can downgrade a connection or require the unknown label.
  - Cannot silently delete the analyst’s claim; disagreements remain visible.

  The Worrier is a separate source of scenarios, not the Skeptic. A system needs both the person asking “what if?” and the person asking “what if this is ordinary?”

  ### Seat 5: Editor

  **Default:** Codex Luna.

  - Reconciles the analyst and Skeptic.
  - Checks that every atomic link has the correct label and source.
  - Produces the daily file, Satya’s short message, and the phone page.
  - Publishes corrections without waiting for approval.
  - Cannot introduce a new fact that is absent from the evidence pack.

  ---

  ## 3. The record: events are not claims

  The basic unit should be a claim about an event, not a headline.

  Each event record needs:

  ```yaml
  event_id: stable-id
  what_happened: plain one-sentence description
  event_start: timestamp or bounded time range
  event_end: timestamp or unknown
  published_at: timestamp
  first_seen_at: timestamp
  actors: []
  organizations: []
  places: []
  source_families: []
  coverage_quality: good | partial | poor
  ```

  Each claim record needs:

  ```yaml
  claim_id: stable-id
  event_id: related-event
  claim: one atomic statement
  label: ESTABLISHED | REPORTED | NOT ESTABLISHED EITHER WAY | RULED OUT
  named_source: source and URL
  source_type: official | direct-data | press | social | analyst
  source_family: syndication-or-copy-group
  supporting_items: []
  contradicting_items: []
  ordinary_explanations: []
  what_would_settle_it: specific document, observation, or investigation
  last_checked: timestamp
  ```

  A relationship receives its own record:

  ```yaml
  from: event-person-or-organization
  to: event-person-or-organization
  relationship: met | preceded | co-occurred | enabled | coordinated-with | caused | attributed-to
  label: ESTABLISHED | REPORTED | NOT ESTABLISHED EITHER WAY | RULED OUT
  evidence_for: []
  evidence_against: []
  analyst_note: short and bounded
  skeptic_note: short and bounded
  ```

  Important distinctions:

  - A meeting is established by an official readout. Its purpose may still be **NOT ESTABLISHED EITHER WAY**.
  - A cyber intrusion being present is separate from an attacker being identified.
  - Attribution to an organization is separate from attribution to a government.
  - Attribution to a government is separate from proof that it ordered a particular operation.
  - Simultaneity is not coordination.
  - Capability is not intent.
  - Intent is not a decision to act.
  - A correction creates a dated revision. It does not rewrite the original analysis as though the error never happened.

  ---

  ## 4. Daily rhythm

  Run after the daily news is live, normally around **08:15–09:00 Eastern**. If the news is late, the desk waits. It never competes with the show.

  No local GPU is required. Any optional local GPU experiment remains outside **02:40–07:30**, but the production desk should work entirely on cloud meters and local CPU.

  ### Normal run

  1. **08:15, freeze the input pack**
     - Previous 24 hours, with an explicit cutoff.
     - Read the current Atlas report, Prep Watch rounds, wire leads, and news notes.
     - Late material goes into the next run or a dated correction.

  2. **08:20, registration**
     - Deduplicate stories.
     - Extract events, claims, times, sources, and source families.
     - Identify changed or corrected items.

  3. **08:30, parallel analysis**
     - Connections analyst updates meetings, access, scenarios, and pair/core views.
     - Baseline keeper runs the scheduled comparisons.
     - Neither changes the frozen evidence pack.

  4. **08:40, independent challenge**
     - The Skeptic receives the same evidence and proposed links.
     - It must test coincidence and ordinary explanations before accepting an unusual one.

  5. **08:50, edit and publish**
     - Write the daily report and machine-readable updates.
     - Send Satya the short mailbox summary.
     - Update the phone page.
     - Send Claude only material corrections, blockers, or genuinely important changes.

  6. **After publication**
     - Keep a small list of what would settle the day’s main unknowns.
     - Feed those exact questions to the appropriate existing watch. Do not launch another general sweep.

  ### Weekly and monthly work

  - **Weekly:** test indicator usefulness, review false alarms, inspect missed events, and backfill weak baselines.
  - **Monthly:** compare forecasts or dated expectations with what happened. If numeric forecasts are later introduced, track calibration rather than celebrating individual correct calls.
  - **Quarterly:** remove indicators that add noise and publish a method change log.

  New indicators must be written before the period used to judge them. Backtests are labeled as backtests, not presented as successful advance predictions.

  ---

  ## 5. Inputs and free data

  ### Existing internal inputs

  - `research/convergence/YYYY-MM-DD.md`
  - `research/preparedness/LIVE.md`
  - `research/preparedness/rounds/`
  - Wire output from `C:\Users\lilli\Projects\watch\wire\`
  - `state/news-read/YYYY-MM-DD.md`
  - Worrier reports when produced

  ### External source order

  1. Official statements, laws, notices, military and civil-agency releases.
  2. Direct operational data and company status or incident reports.
  3. Named, credible reporting.
  4. Social posts as original claims or evidence of an information campaign.
  5. Analyst commentary as interpretation, never as event confirmation.

  Useful free classes of data include:

  - Taiwan, Japanese, US, NATO, Russian, Chinese, Iranian, and Korean official releases.
  - UN, IAEA, IMO, UKMTO, ICAO, and maritime or aviation notices.
  - Government customs, sanctions, budget, procurement, and trade records.
  - Company incident reports and public regulator findings.
  - Free market prices, shipping insurance reporting, flight and port disruption notices.
  - Free satellite products where resolution and delay are honestly stated.
  - Official meeting calendars and readouts, including cancellations.

  AIS gaps, satellite absence, blocked pages, and social-media silence are not treated as proof of concealment.

  ---

  ## 6. People in positions and who meets whom

  ### Use two separate ledgers

  #### A. Public positions and access campaigns

  This ledger covers both ordinary public roles and reported hostile access, without mixing them together.

  For public officials, record:

  - Name, public role, organization, appointment and departure dates.
  - Formal authority and publicly stated responsibilities.
  - Meetings, visits, official decisions, and relevant public statements.

  For campaigns such as Volt Typhoon, Salt Typhoon, or North Korean fake IT-worker operations, record:

  - Campaign or allegation name.
  - Reporting agency or named source.
  - Affected sector and organization at the level publicly documented.
  - First observed date, reported presence period, and whether current access is established, historical, remediated, or **NOT ESTABLISHED EITHER WAY**.
  - Capability described at a broad sector level.
  - Attribution and confidence stated by the source.
  - What activity, if any, followed the access.

  Do not publish exploit instructions, vulnerable-system lists, or target-selection detail.

  Private relationships, rumors, and guilt by association do not belong in the graph. A reported affair or resignation does not by itself establish espionage, recruitment, causation, or current access. Such a claim would need direct relevance and strong sourcing before even appearing as **REPORTED**.

  #### B. Meetings and visits

  Every meeting record includes:

  - Participants and their roles at the time.
  - Scheduled, held, canceled, or only proposed.
  - Place and format.
  - Official agenda and each side’s readout.
  - Agreements, disagreements, and omitted subjects.
  - Prior meeting in the same series.
  - Pre-registered observation windows, such as seven days before through seven days after.
  - Subsequent events, with separate labels for timing and causation.

  The denominator matters. The desk must keep **all comparable meetings**, not just meetings followed by something dramatic. It should also compare meetings with matched non-meeting dates.

  A canceled meeting can be important, but only if the cancellation itself is established.

  ---

  ## 7. Measuring co-occurrence fairly

  For each proposed pattern, define the test before looking at the outcome:

  - Event types and inclusion criteria.
  - Geographic scope.
  - Time window and allowed lag.
  - Expected ordinary explanations.
  - Baseline period, ideally two to three years.
  - Day-of-week, season, exercise, weather, holiday, and reporting-cycle adjustments.
  - Minimum source coverage.
  - What result would make the pattern uninteresting.

  Use three comparisons:

  1. **Baseline:** How often does this kind of event happen anyway?
  2. **Placebo:** Does the same apparent pattern occur around unrelated dates?
  3. **Lead-lag:** Do these events happen more often before or after the specified kind of meeting or crisis than at other times?

  Correct for the fact that testing hundreds of relationships will produce some impressive coincidences by chance. A single surprising cluster is a lead, not a finding.

  Every baseline result must show coverage. A rise from six events to ten is meaningless if the watch covered twice as many sources in the second period.

  ---

  ## 8. Scenario scoring

  Each scenario gets at least three competing explanations, including coincidence and routine behavior where appropriate.

  Every evidence item receives the same simple judgment against every hypothesis:

  - `+2`: strongly expected under this hypothesis and much less expected under its competitors.
  - `+1`: modest support.
  - `0`: neutral, unobserved, or equally compatible.
  - `-1`: modest evidence against.
  - `-2`: strong evidence against.

  These are transparent comparison scores, not probabilities. The report shows the reasoning rather than hiding it behind a total.

  Additional rules:

  - Highly correlated observations count as one evidence group.
  - Ten copied articles are one source family.
  - A hypothesis cannot gain support from an indicator added after the event.
  - Absence of an observation counts only where collection was expected to detect it.
  - The strongest counterevidence appears beside the conclusion.
  - A scenario can remain unresolved indefinitely.

  ---

  ## 9. First indicators

  Each indicator needs an owner, source set, baseline, observation rule, and cancellation rule. Numerical alert thresholds should be activated only after the baseline has been audited.

  ### China-Taiwan: first 15 indicators

  1. **Air and naval activity above its own normal range**
     - Track seven-day and 28-day aircraft, naval, coast-guard, and drone activity by type and location.
     - Compare with the same season and known exercise periods.
     - **Counts against an unusual-preparation reading:** a short, announced exercise followed by a return to normal.

  2. **Exercise changes from signaling toward blockade or joint operations**
     - Watch for unannounced, multi-service exercises combining amphibious, rocket, air, naval, coast-guard, logistics, and port-control components.
     - **Counts against:** a preannounced annual drill with limited forces and a clear ending.

  3. **Unusual maritime or aviation restrictions**
     - Track exclusion zones, navigation warnings, NOTAMs, their duration, geography, and overlap with military activity.
     - **Counts against:** routine space launches, weather closures, or previously scheduled training.

  4. **Amphibious and civilian roll-on/roll-off lift concentration**
     - Require corroboration across official notices, shipping data, imagery, or credible observation.
     - Distinguish actual requisition or embarkation from ships merely being present.
     - **Counts against:** commercial schedules, maintenance, ordinary ferry exercises, or rapid dispersal after a drill.

  5. **Reserve and transportation mobilization**
     - Watch for reserve recalls, transport requisitions, civil-military mobilization orders, and unusual conscription measures.
     - **Counts against:** annual reserve training, disaster response, or measures already in published plans.

  6. **Sustained military logistics preparation**
     - Look for convergent reporting of fuel, munitions, medical, blood, rail, and port support beyond routine exercise requirements.
     - Public visibility will often be poor. Missing observations stay **NOT ESTABLISHED EITHER WAY**.
     - **Counts against:** normal rotations, disaster stockpiling, or isolated unsourced claims.

  7. **Taiwan moves from preparation to activation**
     - Track reserve recalls, military dispersal, shelter activation, emergency stock release, continuity-of-government measures, and civilian evacuation instructions.
     - **Counts against:** scheduled civil-defense exercises or typhoon response.

  8. **Cyber disruption against Taiwanese essential services**
     - Compare government, telecom, financial, energy, and transport disruptions with their own baselines.
     - Record access, disruption, and attribution separately.
     - **Counts against:** vendor faults, maintenance, ordinary incident rates, or unrelated criminal activity.

  9. **Navigation, communications, satellite, and cable interference**
     - Track GPS interference, satellite jamming, telecom interruption, and undersea-cable faults by location and duration.
     - **Counts against:** accidental cable damage, localized equipment failure, solar effects, or normal military exercise notices.

  10. **Economic measures specific to Taiwan or its supporters**
      - Track customs stops, sanctions, import bans, export controls, financial restrictions, and pressure on third countries.
      - **Counts against:** broad commercial regulations with no Taiwan-specific pattern.

  11. **Diplomatic and legal preparation**
      - Watch for recalled envoys, suspended hotlines, explicit ultimatums, evacuation warnings, changes to legal authority, and non-routine use-of-force language.
      - **Counts against:** repeated standard wording or routine diplomatic protest.

  12. **US, Japanese, and allied force-protection changes**
      - Track deployments, dispersal, air and missile defense, force-protection changes, dependent or nonessential-staff departures, and emergency readiness.
      - **Counts against:** scheduled rotations and previously announced exercises.

  13. **Commercial shipping and aviation behavior changes**
      - Track war-risk premiums, rerouting, port cancellations, airspace avoidance, and insurance restrictions.
      - **Counts against:** weather, ordinary seasonal changes, port congestion, or commercial disputes.

  14. **Emergency financial and supply-chain safeguards**
      - Distinguish long-term resilience programs from activation: capital controls, emergency liquidity, reserve release, rationing, urgent chip or energy allocation.
      - **Counts against:** implementation continuing on an already announced industrial-policy timetable.

  15. **Cross-theater enabling activity**
      - Watch for joint patrols, diplomatic cover, intelligence or space support, material assistance, or simultaneous pressure explicitly connected to a Taiwan contingency.
      - Test the timing against a cross-theater baseline.
      - **Counts against:** independent routine activity, no enabling link, or similar frequency outside Taiwan crisis windows.

  These indicators distinguish **positioning** from **a decision to attack**. Several could rise during coercive signaling without invasion being intended.

  ### Russia-NATO: first five indicators

  1. **Force deployment and readiness**
     - Russian and NATO deployments, dispersal, logistics, air defense, reserve measures, and readiness compared with announced exercise baselines.
     - **Against escalation:** scheduled rotations and rapid return to normal posture.

  2. **Nuclear-force and command-posture changes**
     - Official alerts, unusual deployments, weapons movement corroborated by reliable sources, and changes to nuclear command communications.
     - **Against escalation:** routine exercises and repeated signaling without operational change.

  3. **Air and maritime encounters**
     - Airspace entries, unsafe intercepts, naval shadowing, and close approaches measured against prior frequency.
     - **Against escalation:** isolated navigation incidents or established patrol routes.

  4. **Hybrid attacks on NATO territory**
     - Cyber disruption, sabotage, cable damage, drone incursions, and proxy activity, with attribution kept separate.
     - **Against coordination:** ordinary failure rates, accidents, unrelated criminal activity, or common vendor faults.

  5. **Direct kinetic contact or formal alliance crisis**
     - Strikes reaching NATO territory, direct Russian-NATO engagements, Article 4 consultations, emergency force decisions, and formal ultimatums.
     - Log ceasefires, hotline reopening, and withdrawals as counter-signals.
     - **Against escalation:** accidental impact promptly contained through working channels.

  ### US-Iran: first five indicators

  1. **US strike and defense posture**
     - Carriers, bombers, tankers, missile defense, logistics, base force protection, and personnel departures compared with rotations.
     - **Against imminent-strike reading:** previously scheduled deployments without supporting logistics.

  2. **Iranian and partner-force operational preparation**
     - Missile, drone, naval, air-defense, and proxy-force dispersal or readiness changes.
     - **Against escalation:** routine exercises or defensive movements without follow-on activity.

  3. **Hormuz and regional shipping coercion**
     - Attacks, seizures, mining reports, navigation restrictions, insurance changes, and export interruption against a maritime baseline.
     - **Against attribution:** conflicting claims, accidental damage, or ordinary maritime incidents.

  4. **Nuclear-program and inspection changes**
     - IAEA access, enrichment activity, site operations, inspector expulsion, and weapons-related claims kept as separate claims.
     - **Against weaponization reading:** verified limits, restored access, and no supporting operational indicators.

  5. **Direct attacks and diplomatic off-ramps**
     - Attacks on US personnel or forces, Iranian casualty and damage reports, proxy claims, Oman or other mediation, hotlines, and negotiated pauses.
     - **Against sustained escalation:** attacks stop and verified mediation produces observable restraint.

  US-China, North Korea-US/ROK/Japan, and the core-coordination scenario should receive their own full cards next. They should not inherit China-Taiwan indicators merely because some events overlap.

  ---

  ## 10. The modern escalation ladder

  ### Keep Kahn’s spine, add parallel tracks

  Kahn’s 44 rungs remain useful for describing conventional political-military escalation. They should remain as historical annotations on the conventional track, not be forced to accommodate every modern capability.

  Modern escalation is often simultaneous and reversible. A country can have severe economic conflict, active cyber pre-positioning, and routine military activity at the same time. One number hides that picture.

  Use nine tracks, each scored from 0 to 5:

  - **0:** routine activity within baseline.
  - **1:** signaling or limited pressure.
  - **2:** extraordinary preparation, coercive posture, or latent capability.
  - **3:** limited coercive action or disruption.
  - **4:** sustained campaign or direct confrontation.
  - **5:** full-scale war or strategic attack.

  The levels describe activity within a track. Level 4 information operations are not said to be as destructive as level 4 conventional war.

  ### Track definitions

  | Track | 0–2 | 3 | 4–5 |
  |---|---|---|---|
  | **Diplomatic and legal** | Routine relations; protests and recalls; suspended dialogue, expulsions, ultimatums, or emergency legal authority | Diplomatic rupture with coercive demands or limited international isolation | Wartime coalition confrontation, declarations of war, or complete breakdown during direct conflict |
  | **Economic and technological** | Ordinary trade; targeted tariffs; broad sanctions, export controls, rare-earth or chip restrictions, emergency stockpiling | Comprehensive embargo, asset freezes, shipping restrictions, or coercive denial of essential supplies | Systemic economic warfare, blockade, wartime allocation, or rationing during full conflict |
  | **Information and attribution** | Routine messaging; targeted narratives; coordinated covert influence or fabricated-source operations | Established or reported deception tied to a specific coercive action, including false-attribution operations | Sustained wartime deception and information control integrated with a broader campaign |
  | **Cyber and pre-positioning** | Routine scanning; espionage campaigns; persistent access to important systems, with access and current presence separately labeled | Localized disruptive or destructive operation | Sustained multi-sector disruption; nationwide destructive campaign during full conflict |
  | **Space and sensing** | Routine operations; close approaches or signaling; persistent reversible jamming or surveillance posture | Temporary denial of important satellite or navigation services | Multiple disabled systems or a sustained space campaign as part of direct war |
  | **Maritime and undersea** | Routine patrols; harassment; suspicious infrastructure damage or exceptional exclusion zones | Seizures, localized blockade, or coercive cable and shipping disruption | Sustained blockade, repeated infrastructure attacks, or maritime war |
  | **Proxy and deniable force** | Routine contacts; threats or mobilization; new arms, funding, or intelligence support for a coercive front | Limited deniable or proxy attack | Sustained proxy war, multi-front campaign, or direct sponsor participation |
  | **Conventional and nuclear** | Routine forces; exercises and nuclear signaling; mobilization, unusual deployment, or alert changes | Limited strike, direct clash, quarantine, or blockade | Sustained direct conventional war; nuclear use or strategic attack |
  | **Homeland and civil resilience** | Routine guidance; new budgets or stockpiles; activated reserves, emergency procurement, or continuity measures | Reserve release, rationing, continuity operations, or emergency civilian mobilization | Wartime or national-survival economy |

  A high resilience score is not itself evidence that an attack is coming. Reshoring and preparedness can be prudent under several explanations.

  ### The six daily views

  Every day writes a track profile for:

  1. US-China.
  2. China-Taiwan.
  3. Russia-NATO.
  4. US-Iran.
  5. North Korea-US/ROK/Japan.
  6. Russia-China-Iran-North Korea core against the US and its partners.

  The core is an analytical view, not an assumption that the four governments form a unified command.

  An event enters the core view only when there is a specific relationship: communication, shared operation, material support, diplomatic coordination, or a documented enabling effect. Events merely occurring in the same week remain separate pair events with a co-occurrence note.

  ### Placement rules

  - Every rung cites claim IDs.
  - A reported event can produce a provisional placement such as `2, REPORTED`.
  - If the present state cannot be determined, show `?` and the last established observation with its date. Do not silently return to zero.
  - A rung rises only on new observed activity, not on a more dramatic interpretation.
  - A rung falls when activity ends, reverses, or is narrowly ruled out. Lack of fresh headlines is not de-escalation.
  - Attribution uncertainty does not erase an outage or attack. It prevents assigning that event to a suspected actor.
  - One event is counted once across dependent indicators.
  - The daily output shows the full profile and changes, not an average or a single desk safety score.
  - The strongest de-escalation evidence appears beside the strongest escalation evidence.

  ---

  ## 11. Testing Jaron’s four hypotheses

  Each hypothesis is useful only if it can lose.

  ### Hypothesis A: Small disruptions are distractions meant to occupy or alarm the US

  **Competing explanations**

  - Coordinated diversion by one actor.
  - Several actors exploiting a crisis independently.
  - Common vendor, maintenance, weather, or operational causes.
  - Normal clustering plus increased attention and viral compilation.

  **Advance expectations if coordinated diversion is occurring**

  - Disruptions repeatedly cluster before pre-specified US or allied decisions, rather than merely after headlines.
  - Affected services have a plausible connection to the decision or response capacity.
  - Investigations find shared infrastructure, methods, tasking, or actor links across otherwise separate incidents.
  - The pattern exceeds matched baseline and placebo windows.
  - Similar timing is less common around unrelated dates.

  **Counts against it**

  - Root-cause reports establish unrelated bugs, hardware failures, weather, or maintenance.
  - Incidents affect unrelated countries and actors indiscriminately.
  - Comparable clusters occur just as often outside crisis windows.
  - The apparent timing disappears when copied reports and publication delays are removed.
  - Events fail to impose meaningful operational cost or attention.

  Each incident’s occurrence and attribution remain separate. “Cause not established” cannot be converted into “diversion.”

  ### Hypothesis B: An attack could be made to look Iranian when China was responsible

  Break this into four separate questions:

  1. Did the attack occur?
  2. Who carried it out?
  3. Was identifying material deliberately planted?
  4. Did that deception change public or government support for a response?

  **Competing explanations**

  - Iran or an Iranian partner conducted it.
  - China conducted it with deliberate Iranian markers.
  - Another state or criminal actor conducted it.
  - Shared tools or infrastructure caused accidental misattribution.
  - Cause and attribution remain **NOT ESTABLISHED EITHER WAY**.

  **Tests**

  - Compare independent forensic reports, infrastructure ownership, operational timing, targeting, and technical evidence.
  - Distinguish unique evidence from widely shared tools, languages, time zones, and compromised servers.
  - Test whether claimed Iranian markers were available before attribution or appeared only in later commentary.
  - Examine public reaction separately through polling, official statements, and policy changes.
  - Require evidence of deliberate planting before calling something a false flag.

  **Counts against the Chinese-deception version**

  - Independent investigations converge on Iranian control using material evidence.
  - Specific claimed Chinese links are shown to be shared, ordinary, or misinterpreted.
  - The supposed Iranian markers are demonstrated to be genuine operational infrastructure rather than planted artifacts.
  - Public hesitation is explained by unrelated political or legal factors.

  Even strong evidence of Chinese involvement would not, by itself, establish an intent to frame Iran. Capability to imitate another actor is not evidence that imitation occurred.

  ### Hypothesis C: Many current moves are positioning for an eventual China-Taiwan crisis

  “Eventual” must be bounded. Use separate 12-month and 36-month observations without claiming a predicted attack date.

  **Competing explanations**

  - Taiwan-specific military or economic positioning.
  - General military modernization.
  - Broad sanctions-proofing and economic security.
  - Domestic disaster preparedness.
  - Ordinary industrial policy.
  - Coercive signaling without a decision for war.

  **Advance expectations if Taiwan-specific positioning is occurring**

  - Blockade, amphibious, logistics, mobilization, energy, chip, and financial-resilience measures accelerate together.
  - Measures have capabilities or geography specifically useful in a Taiwan contingency.
  - Exercises increasingly rehearse joint civilian-military and cross-theater support.
  - Official planning documents connect otherwise separate measures.
  - The pace exceeds prior plans and comparable non-Taiwan activity.

  **Counts against it**

  - Measures follow ordinary five-year plans or commercial timetables.
  - Similar policies occur in countries with no comparable Taiwan role.
  - Relevant capabilities do not increase, or resources move away from Taiwan-relevant missions.
  - Domestic disaster or economic explanations fit the details better.
  - Exercises and procurement remain fragmented rather than becoming operationally integrated.

  Evidence of positioning does not establish that Beijing has decided to use force.

  ### Hypothesis D: Reshoring is partly about surviving a major war

  **Competing explanations**

  - War or national-security resilience.
  - Pandemic and general supply-chain resilience.
  - Technology competition with China.
  - Jobs, regional development, and electoral politics.
  - Corporate subsidy-seeking and ordinary industrial policy.

  **Tests**

  - Examine official strategy documents, legislation, budget justifications, procurement terms, and congressional records over time.
  - Separate generic “national security” language from explicit surge capacity, wartime continuity, stockpile, hardening, or defense-production requirements.
  - Compare strategic sectors with similarly subsidized non-strategic sectors.
  - Check whether facilities reduce actual wartime dependencies, including equipment, materials, packaging, energy, and shipping.
  - Track whether projects include dual-use production, surge clauses, inventories, or continuity obligations.

  **Counts against the major-war explanation**

  - Projects are justified and structured primarily around jobs or ordinary commercial competition.
  - Production remains dependent on fragile foreign inputs with no resilience plan.
  - Facilities have no surge, inventory, dual-use, or continuity requirements.
  - Timelines and capacity are poorly matched to any plausible contingency.
  - Policy details fit electoral or industrial explanations better than resilience.

  An explicit national-security rationale may establish that resilience is **part** of a policy. It does not establish that leaders expect a major war.

  ---

  ## 12. Outputs

  ### Files

  ```text
  research/connections-desk/
    METHOD.md
    YYYY-MM-DD.md
    today.md
    events/
      YYYY-MM.jsonl
    ledgers/
      meetings.jsonl
      public-positions.jsonl
      access-campaigns.jsonl
    scenarios/
      us-china.md
      china-taiwan.md
      russia-nato.md
      us-iran.md
      north-korea.md
      core-coordination.md
    indicators/
      registry.json
    baselines/
      coverage.json
      *.json
    scorecards/
      YYYY-MM-DD.json
    reviews/
      weekly-YYYY-MM-DD.md
      corrections.jsonl
  ```

  `METHOD.md` owns definitions and changes. Scenario files contain indicators written in advance. Daily reports reference those versions rather than quietly changing them.

  ### Satya’s mailbox message

  Register `connections-desk` as a sender and send to `satya-twin`:

  ```bash
  python tools/mailbox.py send \
    --from connections-desk \
    --to satya-twin \
    --subject "Connections Desk YYYY-MM-DD" \
    --body "<six-line summary>"
  ```

  The six lines are:

  1. Biggest established change.
  2. Important reported or unresolved claim.
  3. Most relevant baseline result, including coincidence.
  4. Changes in pair and core track profiles.
  5. Strongest counterevidence or correction.
  6. Report path and the one observation that would settle the main unknown.

  No safety-level suggestion and no direct phone alert.

  ### Jaron’s phone page

  Publish `today.md` as `heartbeatobservatory.com/connections/`.

  The page should fit a phone and open with:

  - **Today in five plain lines.**
  - **What actually changed.**
  - **What happened together, and whether that is unusual.**
  - **Who met whom.**
  - **The pair view and the core view.**
  - **The four hypotheses: what helped and hurt each today.**
  - **What would settle the main unknowns.**
  - **Corrections to earlier reports.**

  Each connection card answers:

  > **What is the link?**  
  > Label and one sentence.
  >
  > **What supports it?**  
  > Named sources.
  >
  > **What argues against it?**  
  > Ordinary explanation and counterevidence.
  >
  > **What would settle it?**  
  > One concrete next observation.

  No stacked-headline globe, flashing red graphics, fear score, or safety number.

  ---

  ## 13. Cost

  The normal run uses:

  - One light Codex Luna registration and editing cycle.
  - One medium Grok Build analysis.
  - One medium Kimi skeptic pass.
  - Local CPU calculations and Qwen extraction where useful.
  - DeepSeek only for bounded extraction or backfill work.

  **Expected new cash cost:** roughly **$0.05–$0.30 per day**, mainly DeepSeek overflow, with a **$0.50 daily hard stop**. Existing subscription meters carry most of the work. This is a target to measure during the first week, not a vendor price quote.

  Log actual tokens, meter share, runtime, and API spend after every run. If the desk repeatedly exceeds the cap, reduce source text to relevant excerpts and move extraction locally rather than weakening the Skeptic pass.

  ---

  ## 14. What the current plan is missing

  ### De-escalation needs equal billing

  Track ended exercises, restored hotlines, verified withdrawals, resumed inspections, working incident investigations, trade exemptions, and successful mediation. Otherwise the system accumulates threats and forgets reversals.

  ### The desk must measure its own attention

  More reports can mean more searching, not more events. Coverage, source access, language, and publication delays belong in every baseline. A blocked page is a coverage problem, not a negative finding.

  ### Viral coordination is an event, not corroboration

  When fifty accounts repeat one claim, that may establish an information campaign. It does not establish the claim’s subject. Source-family grouping is essential.

  ### OSINT often cannot settle intent or hidden command

  The desk should be explicit about its ceiling. Public sources can sometimes establish access, activity, meetings, material support, and timing. They may never settle an order given in private. Those links remain **NOT ESTABLISHED EITHER WAY**, with no penalty for staying unresolved.

  ### Jaron’s hypotheses need isolation from the independent estimate

  Analysts should receive a frozen evidence pack and declared context, not Jaron’s positions, current worries, or a preferred conclusion. A second weekly pass should mask hypothesis names where practical. Any analysis that reads prior commentary must declare itself informed rather than independent.

  ### The first month should be shadow mode

  Run daily, but treat thresholds as provisional until baselines and coverage are audited. Backtest on held-out periods and keep placebo comparisons. Do not advertise early pattern hits as successful forecasts.

  ### Safety and privacy boundaries matter

  Use public information, avoid exploit and targeting detail, and do not build dossiers on private people. Public-role tracking and reported hostile-access tracking must remain visually and structurally separate.

  ### A useful failure condition

  If the desk merely restates Atlas with more dramatic language, or if its patterns cannot survive the Skeptic and baseline tests, stop publishing the pattern section and fix the method. A short report saying “today’s events are connected only by timing” is a successful report.

  ---

  ## Next thing

  Build the event/claim schema and three frozen scenario cards first: China-Taiwan, Russia-NATO, and US-Iran. Then backfill one ordinary month before judging any current cluster.

