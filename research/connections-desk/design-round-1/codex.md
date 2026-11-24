# Connections Desk: operating design

## Purpose

The Connections Desk looks across the existing watch systems to find links worth checking: who has access or influence, who met whom, what happened around key events, and whether the pattern differs from ordinary background activity.

It produces **sourced links, competing explanations, and open questions**. It does not turn timing into causation, treat an unknown as proof or disproof, or set the safety level. Satya alone sets that level.

The desk should be able to conclude that a connection is **not established either way**. That is a useful result when the record is incomplete.

## How it fits the existing watches

| Existing system | What it contributes | What the Connections Desk adds |
|---|---|---|
| Atlas | Daily account of major powers and alignment | Checks its claims against other regions, event types, and alternative explanations |
| Prep Watch | Hourly preparedness moves and failures, with a baseline | Looks for links between those events and other developments; tests whether the rate is unusual |
| The wire | Fast keyword alerts | Groups related alerts, checks their sources and timing, and separates new reporting from recycled claims |
| News desk | Broad daily reporting and notes | Supplies leads and context; a headline alone does not establish a connection |
| The Worrier | Occasional intentionally worried read | Offers a challenge to complacent interpretations; its concerns are examined alongside other hypotheses |
| Satya | The only safety-level decision-maker | Receives a concise, uncertainty-labeled briefing and decides what, if anything, changes the level |

The desk should reuse existing records and link back to them. It should not create a second news feed or copy every headline into a new database.

## Team and roles

A small rotating team can cover the work without making every daily run a large multi-model exercise.

1. **Desk editor and evidence keeper — Codex Luna.** Builds the daily event list from Atlas, Prep Watch, wire, and news notes. Maintains source links, timestamps, event identifiers, and corrections. Does not infer intent from a source’s silence.
2. **Regional and language reader — Kimi.** Checks relevant non-English official statements and local reporting. Identifies whether an item is new, a translation, or a repeat of earlier coverage.
3. **Connection analyst — Grok Build.** Proposes links among people, meetings, events, capabilities, and scenarios. Each proposal must point to specific records and be labeled by evidence status.
4. **Red-team reader — DeepSeek or local Qwen.** Tries to break the strongest proposed link: finds alternative causes, missing time windows, weak sourcing, and examples that would count against it.
5. **Occasional worry seat — The Worrier.** Used on selected days or when a consequential pattern merits a deliberately worried read. It can raise a possibility; it cannot promote that possibility to a finding.
6. **Final desk editor — Codex Luna.** Resolves factual and labeling disputes by returning to the cited source. If the dispute cannot be resolved, the output preserves both views and the uncertainty.

Use the smallest number of seats needed for that day’s events. A quiet day can be one analyst pass and a short review. A day with a potentially consequential connection gets the full review.

## Daily rhythm

All times are Eastern. The desk uses no GPU and does not run during the protected **2:40–7:30 AM news-render window**. It never delays the daily show.

| Time | Work |
|---|---|
| 7:30–8:00 AM | Check that the daily news run is clear. Do not make the Connections Desk a dependency for publication. |
| 8:00–11:30 AM | Collect the latest available Atlas, Prep Watch, wire, and news items. Group duplicates; preserve original publication times and source identities. |
| 11:30 AM–12:00 PM | Draft or update event links, meeting records, and scenario indicators. Compare candidate co-occurrences with the stored baseline. |
| 12:00–12:30 PM | Red-team the strongest claims. Keep the challenge proportional: the top few links, not every ordinary event. |
| 12:30 PM | Write the daily page and send Satya a short mailbox note. If a new, important report arrives later, add a timestamped update rather than silently changing the earlier read. |

Atlas and Prep Watch have their own schedules. If a source has not produced its expected file by the cutoff, the desk marks that input **not available yet** and continues with what it has.

### Weekly work

Once a week, refresh the background rates and inspect the quality of the event records:

- Are incidents consistently timestamped and categorized?
- Are repeated reports being mistaken for independent confirmation?
- Are any indicators too vague to score?
- Did a previously unusual rate return to ordinary range?
- Have corrections changed any earlier connection labels?

Do not change an indicator or hypothesis after seeing a result without logging the change and its date. Keep the earlier version for comparison.

## Inputs and evidence handling

Each event record should contain:

- A stable event ID, date and time, location, actors, and event type.
- The original source link and the time the source published or updated the item.
- Whether the source is official, named reporting, anonymous reporting, or commentary.
- What the source directly establishes, what it attributes to someone else, and what it does not say.
- A pointer to related Atlas, Prep Watch, wire, or news entries.
- Corrections and later updates, kept as a history.

Use the brief’s four labels for every claimed link:

- **ESTABLISHED** — the cited source directly supports the specific link being stated.
- **REPORTED** — a named source or outlet reports the link, but the desk has not independently established it.
- **NOT ESTABLISHED EITHER WAY** — the available record does not settle the link.
- **RULED OUT** — a source directly rules out the specific link. State what was ruled out and by whom.

Apply a label to the *relationship*, not just to each event. For example, two events may each be established while the claim that one caused the other remains not established either way.

Never use “no evidence.” Say what was searched, in which sources and time window, and whether the result supports a conclusion. If the search was limited, say so.

### People and positions ledger

Track **publicly documented roles and access**, not a person’s presumed allegiance or private life. For each entry, record:

- Person or organization, public role, and dates in that role.
- Publicly documented access, authority, or capability relevant to the scenario.
- Source and label for each claim.
- Whether the position is current, former, proposed, or alleged.
- The specific action the person could plausibly enable, clearly separated from what they are known to have done.

For cyber claims, distinguish **access, foothold, capability, intent, and action**. A reported operator’s presence in a network does not by itself establish active control, an imminent operation, or a decision by a government to use that access. Apply the same care to alleged influence, recruitment, and personal relationships.

Use public sources only. Do not infer guilt or intent from association alone. Keep a correction path for mistaken identity, outdated roles, and retractions.

### Meetings and visits ledger

Record leaders, ministers, military chiefs, envoys, and other relevant public officials. Each entry should include:

- Date, location, participants, and meeting type: confirmed, reported, planned, canceled, or informal contact.
- Source for attendance and source for the stated agenda, if available.
- Whether a substantive outcome was announced.
- Events in pre-set windows before and after the meeting, as **co-occurrences** until a source or stronger analysis supports more.

A handshake, shared venue, or meeting on the same day does not establish coordination. “No meeting found” is not “no meeting occurred”; state the coverage searched.

## Baselines and co-occurrence

Before interpreting an event cluster, define the question and window. A default starting point is:

- **Event window:** 72 hours before through 72 hours after the focal event, with narrower windows for scheduled actions such as a vote or summit opening.
- **Comparison:** the same event categories, regions, and days of the week over the prior 12 months, where records are sufficiently complete.
- **Reporting lag:** retain both event time and publication time; compare like with like.
- **Minimum data:** show the number of recorded events and coverage gaps. If the sample is too small, describe the pattern without calling it unusual.

The desk should report counts and rates, not just a striking timeline. For instance: “Four outages occurred in the 72-hour window; the comparable baseline is usually two to five, based on 40 observed windows.” If the baseline is thin or the collection process changed, say so.

A simple event study can be useful, but it is not causal proof. Where enough comparable data exists, use matched windows or a permutation check: keep the same events and shuffle the focal dates within comparable periods to estimate how often a cluster of that size could appear by chance. Record the method and limitations. Never describe a correlation, timing match, or statistical anomaly as proof of coordination.

## Scenario indicators

Indicators are observable signals that would be expected **before** a scenario advances. Register them before scoring the next period. Define the source types, time window, and what counts as a hit. “More tension” is not a scorable indicator.

Scores: **0 absent in checked sources; 1 reported or partial; 2 established; U not adequately checked.** A zero means “not observed in the sources checked during this window,” not “did not happen.” Indicators are evidence inputs, not automatic forecasts.

### China–Taiwan: 14 indicators

| # | Observable indicator | What would count | Important alternative or limit |
|---|---|---|---|
| 1 | PLA activity changes from its recent baseline | Sustained rise in sorties, ships, or crossing patterns in Taiwan’s official daily reporting | Routine training, weather, or reporting-window differences |
| 2 | Large exercises shift toward blockade or strike tasks | Official notices or independently corroborated exercise activity around ports, air routes, or sea lanes | Announced training may be signaling, routine, or intended for another audience |
| 3 | Civilian roll-on/roll-off or transport assets are mobilized | Documented requisition, unusual port loading, or coordinated civilian fleet activity | Commercial movements and seasonal traffic need comparison |
| 4 | Rocket, logistics, medical, fuel, or ammunition preparations become visible | Multiple independently sourced, specific preparations tied to relevant units or locations | Ordinary exercises and routine replenishment |
| 5 | Air and maritime exclusion notices constrain access | Notices whose location, duration, and timing materially affect Taiwan approaches or shipping | Safety notices and exercises can have non-crisis purposes |
| 6 | Cyber access or disruptive activity targets Taiwanese critical services | Specific, technically supported incident reporting from operators or named authorities | Criminal activity, routine intrusion attempts, and uncertain attribution |
| 7 | Cable, satellite, or navigation disruptions rise around Taiwan | Verified outages, damage, jamming, or interference above the local baseline | Accidents, maintenance, weather, and faulty equipment |
| 8 | Information operations intensify around a defined trigger | Coordinated, documented narratives or impersonation targeting Taiwanese institutions or public response | Organic debate, ordinary propaganda, and algorithmic amplification |
| 9 | Cross-strait economic pressure changes materially | New or expanded restrictions affecting key sectors, shipping, or supplies | Domestic policy, trade disputes, or broad economic measures |
| 10 | Taiwan civil-defense or continuity actions change in scale | New official readiness instructions, mobilization, evacuation, or continuity measures | Natural-disaster preparedness or previously planned exercises |
| 11 | US, Japan, or partner military posture shifts in the region | Confirmed deployments, access agreements, logistics changes, or operational notices | Scheduled rotations and previously announced plans |
| 12 | Diplomatic channels narrow or an ultimatum is issued | Official suspension of talks, formal deadline, or directly quoted ultimatum | Public rhetoric may be bargaining and may coexist with active private channels |
| 13 | Foreign nationals, shipping, or aviation receive coordinated warnings | Official advisories that name a specific threat, area, or departure timetable | Routine travel advisories and seasonal notices |
| 14 | Multiple independent indicators converge in a pre-registered window | Distinct signals from separate domains, such as logistics plus access restrictions | Several reports may trace to one source or one routine exercise |

The desk should show each indicator’s history and source coverage. It should not convert the summed score into a probability unless a separately calibrated model has been tested against historical cases.

### US–Iran: 5 indicators

| # | Observable indicator | What would count | Important alternative or limit |
|---|---|---|---|
| 1 | A verified change in US force posture or operational authorization | Confirmed deployment, evacuation, or official change tied to a named theater | Routine rotation and contingency planning |
| 2 | Iran or aligned groups make a specific, attributable operational move | A named attack, mobilization, or threat with a source and target | Claims may be unverified, inflated, or falsely attributed |
| 3 | Gulf shipping or infrastructure disruption exceeds baseline | Independently confirmed incidents, route closures, or sustained traffic change | Accidents, weather, insurance effects, or unrelated commercial changes |
| 4 | Nuclear monitoring, access, or diplomacy changes materially | IAEA or government statements, confirmed access changes, or formal talks/withdrawals | Public statements may overstate what changed operationally |
| 5 | Cyber or proxy activity is technically or officially linked to the crisis | Specific incident with a named attribution and stated confidence | Similar tactics do not by themselves establish a common actor |

### Russia–NATO: 5 indicators

| # | Observable indicator | What would count | Important alternative or limit |
|---|---|---|---|
| 1 | Military posture changes near NATO borders | Confirmed, sustained movement beyond known exercise and rotation patterns | Routine exercises and incomplete public visibility |
| 2 | Air or maritime incidents change in frequency or severity | Officially documented incursions, close encounters, or route disruptions above baseline | Different national definitions and reporting practices |
| 3 | Critical infrastructure is disrupted with credible attribution | Confirmed damage or outage plus a source-supported attribution | Accident, equipment failure, or unattributed criminal activity |
| 4 | Mobilization, logistics, or civil-defense preparations expand | Specific orders, transport movements, or preparations beyond routine practice | Domestic readiness and disaster response |
| 5 | Diplomatic or military communication channels degrade | Confirmed suspension, new deadlines, or reduced crisis communication | Public rhetoric can worsen while private channels remain active |

The broader **Russia–China–Iran–North Korea** view is a separate lens over these scenarios. It asks whether there is evidence of coordination, reciprocal support, or synchronized pressure across actors. Shared interests, similar rhetoric, or activity in the same period do not establish a unified plan. Log each bilateral or multilateral link separately, then summarize the bloc view with the same evidence labels.

## A modern escalation map

Kahn’s 44-rung ladder is a useful reference for increasing crisis severity. The desk should not pretend that today’s cyber, economic, or space events fit neatly into one historical rung. Keep a **shared severity spine** and score modern activity on parallel tracks.

### Shared severity spine

| Band | Description |
|---|---|
| 0 — Routine | Normal activity or recurring rhetoric; no meaningful departure from baseline established |
| 1 — Signaling | Public threats, demonstrations, or diplomatic pressure without a new operational constraint |
| 2 — Coercive pressure | Material economic, cyber, information, or access pressure that imposes costs or changes behavior |
| 3 — Limited disruption | Confirmed disruption, restricted access, or deniable action with a specific target |
| 4 — Sustained confrontation | Repeated or coordinated actions across domains; force posture or critical services materially affected |
| 5 — Direct conflict | Confirmed direct use of force or sustained combat between the actors |
| 6 — Wider war risk | Expansion to additional theaters or parties, strategic infrastructure, or weapons with far greater destructive potential |

These bands describe the event’s observable severity, not the actor’s intent or the likelihood of war. They are not a direct conversion to Kahn’s numbered rungs.

### Parallel tracks

Score each track separately for each actor pair and for the broader bloc view:

- **Diplomatic and political:** statements, expulsions, meetings, channels, deadlines.
- **Conventional military:** force posture, exercises, mobilization, strikes, territorial access.
- **Cyber:** access, disruption, recovery, attribution. Keep pre-positioning separate from an executed disruption.
- **Information and deception:** coordinated narratives, impersonation, false claims, and evidence of deliberate deception.
- **Economic and industrial:** tariffs, export controls, sanctions, stockpiles, production capacity, and supply restrictions.
- **AI, chips, and technology:** controls, access, production, procurement, and documented operational use.
- **Space and navigation:** satellite posture, jamming, interference, service disruption.
- **Undersea and infrastructure:** cables, pipelines, ports, power, telecoms, and repair or protection activity.
- **Proxies and deniable action:** attacks or threats by aligned groups, keeping claimed affiliation and established direction distinct.
- **Civil readiness and continuity:** evacuations, emergency measures, protected infrastructure, public guidance.

### Placing a day

For each pair, and separately for the bloc lens:

1. List the day’s relevant events with evidence labels and source links.
2. Score the affected tracks; use “U” when coverage is insufficient.
3. Assign the shared severity band based on the **highest established or clearly reported event**, stating which label supports it.
4. Give a second reading if another plausible interpretation changes the placement.
5. Compare with the prior day and baseline. Note whether the change is in event severity, reporting volume, or source coverage.
6. Do not average away a serious event, and do not let several weakly sourced events add up to a confirmed escalation.
7. Keep intent and attribution as separate fields from severity. If a particular attack’s actor is unknown, score the attack’s observable severity while leaving attribution unknown.

The daily page should show, for example: “Cyber track: 2, reported; Attribution: not established either way; Shared band: 2, because the service disruption is confirmed.” It should not say “state cyberattack” unless the source supports that attribution.

## Four hypotheses to test fairly

Each hypothesis gets a short pre-registration card: version date, scope, time horizon, observable indicators, expected order of events, rival explanations, and what would count against it. Score every hypothesis against the same event set, including ordinary coincidence. Do not add a new indicator after seeing a surprising event without recording that change.

### 1. Small disruptions may distract or panic the US

**Test:** Define in advance what counts as a small disruption, what counts as a competing crisis or US attention demand, and what measurable outcome would show attention was diverted. Compare pre-set windows with similar periods that had no disruption. Check whether the disruption preceded the attention shift, whether the shift occurred, and whether any source documents the intended distraction.

**Alternatives:** Ordinary failures; unrelated criminal activity; natural or technical causes; media attention without any operational effect; multiple actors acting independently.

**Counts against:** Disruptions occur at their usual rate; they do not precede or predict measurable attention changes; or a supported technical cause explains them without a corresponding shift. Lack of a discovered intent statement alone does not rule it out.

### 2. An attack could be made to look Iranian when another actor conducted it

**Test:** Keep the scenario narrow: define the kind of attack, the period, the evidence that would indicate deliberate false attribution, and the public-response outcome being tested. Before the period, list expected signs such as falsified technical indicators, a demonstrable planted claim, inconsistent operational details, or a credible investigation distinguishing apparent from actual origin.

**Alternatives:** Genuine Iranian action; a third party; criminal actors; mistaken early reporting; genuine uncertainty in attribution; independent actors using similar methods.

**Counts against:** A well-supported attribution to Iran, no evidence of deliberate deception after a defined and documented investigation, or no observed change in public response attributable to uncertainty. “No public proof yet” remains **NOT ESTABLISHED EITHER WAY**, not ruled out.

### 3. Many moves may be positioning for a China–Taiwan crisis

**Test:** Use the pre-registered China–Taiwan indicators above. Track whether multiple independent domains change in the expected order and whether the changes exceed their baselines. Score the hypothesis over fixed windows, such as 30 and 90 days, then compare with windows without a crisis.

**Alternatives:** Routine military activity; domestic politics; disaster readiness; bargaining or deterrence; unrelated regional disputes; activity aimed at another audience.

**Counts against:** The supposed signals remain inside baseline, fail to converge across independent domains, reverse, or are better explained by documented routine purposes. A quiet period weakens a specific time-bounded forecast; it does not prove that future positioning will never occur.

### 4. Reshoring may partly aim to keep the US functioning in a major war

**Test:** Pre-register a sample of policies and firms, plus a coding rule for stated purpose. Separate explicit defense or continuity rationales from general resilience, jobs, competitiveness, and national-security language. Compare the timing of policies with crisis periods and record measurable dependencies: capacity, inputs, location, and time to replace supply.

**Alternatives:** Jobs and regional investment; routine industrial policy; commercial competitiveness; pandemic-era resilience; electoral incentives; ordinary diversification.

**Counts against:** The policy record consistently identifies other aims, the capacity would not support the proposed continuity need, or the policies do not reduce the relevant dependency. “Resilience” language alone does not establish preparation for war.

### Scoring and calibration

For each hypothesis, keep an evidence table with columns for the observation, which hypotheses it supports or weakens, source quality, and the reason for the score. Use a small ordinal scale—**−2 strongly against, −1 somewhat against, 0 non-diagnostic, +1 somewhat supports, +2 strongly supports**—with the rationale written in plain language. Do not sum these into a probability unless the method has been calibrated against a meaningful set of past cases.

Record forecasts with a time horizon and review date. When the horizon ends, score whether the specified indicators occurred. Track calibration separately from whether a story felt persuasive.

## Outputs

### Daily files

Store the desk’s work under `research/connections-desk/`:

- `daily/YYYY-MM-DD.md` — plain-language daily brief with the day’s strongest links, competing explanations, confidence labels, baseline context, and open questions.
- `events/YYYY-MM.jsonl` — one structured event per line, with IDs, timestamps, sources, categories, and correction history.
- `ledgers/people.md` and `ledgers/meetings.md` — sourced, dated records with links to underlying events.
- `scenarios/indicators.md` — versioned definitions and daily indicator scores.
- `scenarios/hypotheses.md` — dated hypothesis cards, alternatives, forecasts, and review results.
- `baselines/` — category definitions, coverage notes, rolling counts, and any comparison method used.
- `corrections.md` — changes to labels or claims, with the earlier wording and reason for correction.

The daily page begins with **what changed**, then **what might connect**, **what could explain it otherwise**, **what remains unknown**, and **what to watch next**. On quiet days, say that no unusual connection was established in the available coverage; don’t manufacture a pattern to fill the page.

### Satya via `ai_mailbox`

Send a short daily note to Satya Twin. Include:

- New established or reported links, with source links and labels.
- What changed against baseline.
- The strongest competing explanation and the red-team objection.
- Any attribution or coverage gap.
- The exact question the desk thinks Satya should consider.
- A plain statement that the desk does not set or recommend a safety level.

Urgent, newly confirmed events can be sent promptly. Do not send every headline or speculative hypothesis as an alert. Satya decides whether the information affects the level.

### Phone page for Jaron

Make one short page that opens with a plain-language paragraph and fits a phone screen without requiring a table to understand it. Suggested sections:

1. **What changed today**
2. **What may connect**
3. **How sure are we?**
4. **What else could explain it?**
5. **What would change our read?**

Link each claim to its source and to the fuller daily record. Display **NOT ESTABLISHED EITHER WAY** in full; do not compress it into “unknown” where that would hide which link is uncertain. The page should remain useful on quiet days and say plainly when the day’s connections were not unusual.

## Cost and operating limits

Use free public sources and existing model or tool allowances. Do not buy data, scrape around access controls, or add a GPU requirement.

A basic daily run should cost **$0 in direct data or API spending** if it stays within existing free or included allowances. Model quota and tool usage still have a cost in availability. A practical starting cap is:

- One synthesis pass on ordinary days.
- One additional language or regional pass when the sources require it.
- One red-team pass on the strongest few links.
- No full-team pass on every event.

The exact token or credit cost cannot be estimated reliably from the files reviewed; it depends on current provider allowances and the volume of that day’s source material. Log which seats ran and whether any were unavailable. If a seat is unavailable, mark the review gap and continue; do not delay the news show or imply that an unrun review happened.

## What else matters

- **Collection bias:** Official sources and English-language outlets leave gaps. Keep a coverage note for each region and event type; absence from the desk’s sources is not absence from the world.
- **Source dependence:** Ten articles can all derive from one anonymous briefing. Record the originating source when known; repeated syndication is not independent confirmation.
- **Correction handling:** Preserve corrections and prior labels so the desk can fix forward without erasing what it previously said.
- **Indicator drift:** Version every indicator definition. If it changes, show the old and new definitions and do not compare scores as though nothing changed.
- **Capability versus intent:** Describe what an actor could do separately from evidence that it plans or has done it.
- **Quiet findings count:** The desk’s success measure is not the number of links it publishes. Track whether its claims were well sourced, whether baselines were useful, how often red-team review caught overreach, and whether time-bounded indicators were calibrated.
- **No single story owns the data:** Each observation can support, weaken, or be irrelevant to multiple hypotheses. This helps prevent one dramatic narrative from absorbing every new event.
