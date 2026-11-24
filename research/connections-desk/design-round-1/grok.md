I'll read the design brief and follow the job it describes.The brief asks for a Connections Desk that sits on the existing watch systems. I'll read how Atlas, Prep Watch, the wire, and Satya actually work before writing the design.# Connections Desk

A daily analysis layer on top of the watches we already run. It keeps four ledgers (meetings, access, armed indicators, baselines), scores a short list of hypotheses against those ledgers, and publishes one phone page. It does not collect the world's news a second time.

Atlas already says whether China-Taiwan, Russia-Ukraine, and the Iran war moved together today (`research/convergence/`). Prep Watch already counts preparedness moves and infrastructure failures against a baseline (`research/preparedness/LIVE.md`, the weekly report, `rounds/`). The wire already says what is loud (`Projects/watch/wire/`, especially the day's `-top.md`). The Worrier already worries on purpose, once in a while (`research/worrier/`). Satya alone sets the level in `state/safety-signal.md`. The news desk already owns 2:40–7:30 AM.

The desk sits downstream of all of them. Its job is the part Jaron named: are these things connected, and how would we know? A quiet page is a successful run.

P-0166 is the editing rule. Words about the unknown are spent credibility. Every link is one of these, with a source wherever a source is required:

- **ESTABLISHED**, with the source.
- **REPORTED**, the claim and the named source.
- **NOT ESTABLISHED EITHER WAY**, plus the one thing that would settle it.
- **RULED OUT**, with the source that closed it.

The phrases "no evidence" and "nothing to see" are not used. Absence is written as one of: not established either way, baseline not ready, no armed indicator tripped, no costly act tagged today, no link changed label.

## 1. The design

### Seats

Four seats. One of them is allowed to write prose. The other three keep it honest. The Worrier is not a fifth seat. The desk reads the latest Worrier file as a list of candidate worries and then tests them. Folding the Worrier into the daily run would rebuild the globe-of-67-headlines, only with footnotes.

| Seat | Who | Does | Does not |
|---|---|---|---|
| Clerk | Codex Luna one day, Kimi the next | Updates the ledgers. Applies the weaker label. Ships the files and the mail. | Interpret. Search past a fixed budget. |
| Measurer | Local Qwen, evenings only | Turns counts into ABOVE / INSIDE / BELOW / BASELINE NOT READY. | Write sentences about why. |
| Analyst | Grok Build, one capped run | Scores the armed hypotheses. Drafts the full file and the phone page. | Ship. Override a baseline verdict. |
| Breaker | Whichever of DeepSeek or Kimi did not clerk | Tries to break every link stronger than "same time." Strikes one sentence from the phone page. | Add a new worry. Browse for a scarier story. |

If Qwen is down, DeepSeek measures, and the breaker is skipped that night. The analyst never grades their own arithmetic. A skipped breaker means the phone page publishes counts and labels only, with the hypothesis section set to "not scored tonight."

The clerk is the last writer and the only sender. The person who wrote the story does not mail it.

### The day (Fort Wayne time)

One main run, after the US day and after Taipei has published its daily defense count, and well clear of the news render.

- **8:00 PM. Clerk.** Reads the inputs below. Appends ledger rows. Leaves every "after" window blank if it is not due yet. Budget: 12 page opens, all of them sources for a row that is already on the page. Done by 8:50.
- **8:50 PM. Measurer.** Qwen, through `tools/qwen-bridge.py`. Receives a table of counts, returns a verdict table. Done by 9:20. If it is still running at 11:00 PM, kill it.
- **9:20 PM. Analyst.** Grok Build, cap 25 turns and 8 searches. Searches are only for a source the clerk marked unopened. Drafts the two files. Done by 10:10.
- **10:10 PM. Breaker.** May open a source the analyst already cited, to see whether it says what was claimed. May not go looking for a new event. Done by 10:40.
- **10:40 PM. Clerk ships.** Weaker label wins. Writes the files. Sends one mail.

Nothing on this desk starts after 11:00 PM. Nothing on this desk runs between 2:40 AM and 7:30 AM. That window belongs to the news capture, the script, and the render. Qwen is a GPU process, so the measurer is evening-only. The morning slip is forbidden from calling `qwen-bridge.py`.

- **8:15 AM. Morning slip. Luna. Ten minutes. No GPU.** Runs only after the show is already live. Reads the new wire top and a newer Atlas file if one exists. If an armed indicator tripped overnight, the clerk appends a dated block, updates the phone page, and mails again. If none tripped, it appends one line to the full file ("8:15 slip: no armed indicator tripped") and sends nothing.

Sunday, inside the same evening budget: a false-alarm note. Which indicators tripped this week and were later explained. Retire, raise, or keep. This is not a second convergence essay. Atlas already writes the Sunday week section.

Claude registers the clock task, the same way Prep Watch is scheduled. This design does not register it.

### Inputs

Read these. Do not rebuild them.

- `research/convergence/` for today and the two days before. Atlas's "links today" and the convergence word (QUIET / WATCH / RISING).
- `research/preparedness/LIVE.md`, the tail, plus the newest `research/preparedness/YYYY-MM-DD.md`. Failures and the baseline live here. The desk copies the counts. It does not re-sweep ministries.
- Today's `wire/*-top.md`. Use it as the list of stories people will assume are connected. Loudness is a control variable, not evidence. Drop an item whose event date is older than 72 hours unless an agency republished it. Date the event, not the post. Old clips re-posted as new are already a known trap.
- `state/news-read/` for today if the morning slip has it. The evening run reads yesterday.
- The newest file in `research/worrier/`, if it is less than 30 days old. Candidate hypotheses only. The Worrier's pattern section is not a finding.
- `state/safety-signal.md`, last entry only, so the mail can see the level Satya has already set. The desk does not discuss what the level should be.
- Its own ledgers, baselines, and open windows.

Web and X are for sourcing a row the inputs already named. They are not a second newsroom.

### Outputs

```
research/connections/PHONE.md                         today's page, overwritten
research/connections/phone/YYYY-MM-DD.md              the same page, kept
research/connections/YYYY-MM-DD.md                    the full file
research/connections/ledgers/meetings.jsonl           append-only
research/connections/ledgers/access.jsonl             append-only
research/connections/ledgers/indicators.md            the armed list
research/connections/ledgers/hypotheses.md            scores over time
research/connections/baselines/failures.md            points at Prep Watch, plus window math
research/connections/baselines/taiwan-adiz.md         the running distribution
research/connections/baselines/meetings.md            how often these people meet
research/connections/state/open-windows.md            rows waiting on their +7 days
```

The full file, every day, in this order: label legend, what changed, ledger diffs, measurer's verdict table untouched, hypothesis scores, ladder placements, breaker dissent, the sentence the breaker struck, open windows due tomorrow.

The phone page is what Jaron reads. Hard cap 400 words. Same shape every day, so a Tuesday can be compared with a Monday.

1. Date and one word: **QUIET**, **WATCH**, or **NOTE**. QUIET means no link changed label and no armed indicator tripped. WATCH means an armed indicator is one published fact short of tripping. NOTE means a label changed. Atlas keeps the word RISING. The desk does not use it.
2. Three sentences. What connected. What lined up and stayed unlabeled. What we still cannot say.
3. The ladder, one line per standing pair: the force group, and the gap if another track is ahead of force.
4. Indicator trips and near-trips, by id. Then one line of the form "12 of 15 China-Taiwan indicators did not trip." Silent indicators stay off the page.
5. Hypothesis changes, or the sentence "no hypothesis score changed."
6. One open question.
7. The path of the full file.

No level number. No advice about what to buy, pack, or fear. A fact that belongs on Satya's scale is described as a costly action or as talk, and left there.

### The mail

One mail each evening, to both `satya-twin` and `claude`. From `connections`. The morning slip mails only when a label changed.

```
python C:\Users\lilli\AI-Shared\tools\mailbox.py send --from connections --to satya-twin --subject "Connections YYYY-MM-DD: QUIET" --body "<six lines>"
python C:\Users\lilli\AI-Shared\tools\mailbox.py send --from connections --to claude --subject "Connections YYYY-MM-DD: QUIET" --body "<six lines>"
```

The six lines, under 120 words:

1. The status word, and the one link whose label changed, or "no link changed label."
2. Armed indicator trips by id, or "none."
3. Any pair where a non-force track is ahead of the force track, or "no track ahead of force."
4. Hypothesis score changes, or "none."
5. Costly actions today, named, or "no new costly action." Talk is not listed in the mail.
6. Paths of `PHONE.md` and the full file.

The mail never contains a recommended level. Satya sets the level. The desk's separation is deliberate: a track can move in the Pacific while every function Satya measures near home is still up. Those are different facts, and the fifth line is how the desk keeps them apart.

### How a claim is allowed to exist

Four habits, all mechanical.

**Indicators are written first.** They live in `ledgers/indicators.md` with a status of COOLING, ARMED, or RETIRED. A new indicator cools for 7 days. While cooling it can be logged as "would have tripped," and it cannot move a score or the phone page. An indicator is a public, checkable fact with a baseline and a stated non-trip. A sentence about what a government wants is not an indicator.

This first set was written on 18 November 2026 while Shenzhen, the Russian flight, the outage cluster, and the Nvidia resignation were already in the files. Every indicator below stays COOLING through 25 November. A trip whose event is already in the 12–18 November record is void. The Shenzhen week is the first ledger week. It is not the first confirmation of anything.

**Competing hypotheses share one evidence list.** The method is Heuer's: list the competitors before the day's reading, including coincidence and a local mundane cause, then mark each evidence item consistent, inconsistent, not diagnostic, or diagnostic. Rank by inconsistent marks, then by missing diagnostic marks. A hypothesis with no evidence is **untested**. It is not in the lead. The phone page says "untested" rather than giving it a quiet win.

**The baseline gets the first word.** Prep Watch's failure baseline stands: a normal month is about 8–15 significant failures worldwide, and Oct 15–Nov 16, 2026 was 14. The measurer uses that. For anything Prep Watch does not yet baseline (Taiwan aircraft and ships, meetings, cable faults, export licenses, war-risk insurance), the verdict is BASELINE NOT READY until 8 comparable weeks exist. On 18 November the Atlas ADIZ series on disk covers a few days. That is not a baseline. The first month of this desk is mostly construction, and the phone page will look empty. An empty page in week 1 is the design working.

A count above the line is a fact about the count. It becomes a connection only when a named source ties the events. Until then the label is NOT ESTABLISHED EITHER WAY, and the page reports both the count and the missing tie. That is the whole answer to "don't claim it, and don't wave it away."

**The breaker moves labels down.** For every link the analyst marked stronger than same-time, the breaker writes the best competing explanation and the label that explanation forces. The weaker label is the one that ships. An indicator the analyst called tripped, which was not armed before the event, is untripped automatically. The breaker also names one sentence the phone page must not say, and the clerk deletes it. If the breaker thinks of a new worry, it goes on a list for the next Worrier run. It does not go on today's page.

Same-time, shared-cause, and source-tied stay as three different relations. A meeting row can also be **sequenced**: B fell inside the 7 days after A, the window was written down when A was logged, and no source ties them. Sequenced is a calendar fact. It is not a cause.

### Meetings ledger

Who counts: a head of state or government, a foreign minister, a defense minister, a finance minister, a military chief, or a named envoy on war, sanctions, or chips. Anyone else only if Atlas or the wire already flagged them. Photo lines at a summit are one row for the meeting, not a row per handshake.

A departure counts too, as its own type. An ordered embassy drawdown, a flag carrier dropping a route, dependents leaving on a government instruction: someone spent money or took a risk. Those are the costly actions worth a row. A tracked plane on a routine training flight is not.

Fields: id, date, status (ANNOUNCED, HELD, CANCELLED, DENIED BY ONE SIDE), parties and roles, place, format, pairs, whether it is also a CRINK row, what each capital said the topic was, the before-notes, the after-notes, the date the after-notes are due, label, sources.

The before-notes are filled the day the row is opened, and only from classes decided here: a force-posture change, a sanction or export-control action, a failure the measurer can see, a ladder step that changed. The after-notes stay null until day +7. A row with a null after cannot support a hypothesis. `hypothesis_credit` stays false until the after-window is filled and the breaker has signed that row.

Both wordings are stored. They are never merged into one "the meeting was about." A denial by one side and a claim by the other is a completed row, not a defect. The 17 November file is full of these (the Trump / Ushakov / earlier US-staff disagreement on whether a bilateral exists). Keep the disagreement until the day passes and one version survives.

The Worrier's 14 November "who talks to whom" table is the seed. Re-enter those rows in this schema on night 1, with after-windows empty and credit false, and re-open any source the desk intends to keep. Do not import the Worrier's pattern judgments with the rows.

### Access ledger (who is sitting where)

Five types, and they stay in separate rows so a legal attaché is never filed next to an intrusion.

- **OFFICIAL-INTRUSION.** A government has named a campaign and a sector. Volt Typhoon and Salt Typhoon start here, pinned to the latest CISA, NSA, or FBI page the clerk actually opens. The 2024 advisories are the seed, not a conclusion that nothing newer exists.
- **INSIDER-CASE.** A case file, an indictment, or a company disclosure. The public North Korean IT-worker cases start here.
- **HUMAN-RECRUIT.** A named person, a role, and an allegation. The Nvidia resignation is this type.
- **LEGAL-PRESENCE.** Defense attachés, port calls, exercises, police cooperation. Lawful, and still worth knowing.
- **PROXY.** A militia, a contractor, a deniable force, public reporting only.

Fields that matter: actor as named by the source, where at sector-and-country grain, a one-sentence quote of what the agency said they could do, a separate quote of what a later source says they did, status (DISCLOSED, CONTESTED, ACCESS-ENDED, STALE), label, next review date.

The gap between "could, per the advisory" and "did, per a later attribution" is the point of the row. The desk does not fill that gap with its own scenario. No facility lists, no vulnerabilities, no sequences, no description of how anyone gets or keeps access. If a run produces those, that run is discarded and the mail says the run was discarded.

What a row is allowed to say about capability is the agency's own sentence and the date of that sentence. A presence advisory does not get upgraded into "disruption is coming."

Decay: 180 days without a new official or company statement, the status becomes STALE. Stale rows leave the phone page and stay in the ledger. STALE is not RULED OUT.

The Nvidia row is the test of restraint. Split it. The resignation, the board's later statement about the job, and any agreement to testify are employment facts, each with its own source and label. The recruitment allegation is REPORTED at the New York Times until a court, the company, or a named agency adopts it. "Access ended" is its own field, and a resignation does not by itself set that field to yes: whether anyone else still had access is NOT ESTABLISHED EITHER WAY, and a company or agency statement would settle it. Record the role and the allegation. Do not retell anyone's private life. Review the row when a filing or a hearing happens. Otherwise it ages on the ordinary clock. It does not become the desk's mascot.

North Korean IT-worker cases are not a China-Taiwan indicator. They become a review trigger only if the Justice Department or the FBI says a case reached a defense, telecom, or infrastructure employer. Stapling them to a Taiwan story, without a source that ties them, is the kind of connection this desk exists to leave unlabeled.

### Co-occurrence

The measurer sees counts.

- Failures by class, copied from Prep Watch: power, cloud, bank or payments, telecom, air traffic, water, cables. Acts of war and planted devices stay on their own lines there, and they stay on their own lines here.
- Flags from the meetings ledger: summit, exercise, deadline, departure.
- Taiwan aircraft and ships, once that series is long enough.
- Plumbing, not prices: a war-risk or hull insurer suspending cover, a flag state barring transit, an export license acted on, a payment rail or exchange halted. A price move counts only when a named market source ties it to the event and the move is outside that series' own 90-day daily range. Otherwise the cause is not established either way. This matches the rule Prep Watch was given on 17 November about markets.

For each flagged day, compare the 7-day window to the previous 8 windows that were not flagged. Publish the median, the 90th percentile, and one verdict. A line-up is reportable when the window is at or above that 90th percentile and contains at least two events, or when a source ties the events. "At or above" without a source is still not a connection. It is an above-baseline count with the cause not established either way.

Summit weeks are a biased sample, because summits are booked onto busy calendars. The pre-registered check is whether the unusual thing started before the meeting was announced. A failure that begins after the announcement is a weak sequence, and the page says so.

GDELT or any headline-volume tool may be used as a loudness control ("the press was louder that week"). It is never evidence that events in the world were connected.

### What one run costs

Expected new cash is a few cents on the nights DeepSeek takes the clerk or the breaker, and nothing on the others. Luna, Grok Build, Kimi, and Qwen are seats we already pay for. Kimi's plan is the same one that already runs First Light.

If those calls were billed at the list prices already written in `JARONS-MAP.md` (Luna $0.10 / $0.50 per million tokens, Grok 4.7 $2 / $6), a capped day of roughly 40–50 thousand tokens in and under 10 thousand out lands around 20 cents, almost all of it the one Grok Build call. That is a ceiling, not an invoice. The way this becomes expensive is an uncapped Grok run, or any run that touches the GPU during the render. The turn cap, the search cap, and the 11 PM kill are the cost control.

Qwen's electricity for half an hour is not worth a line on the ledger. Stamp a row in `state/task-costs.jsonl` anyway, the way other Luna jobs do, so a runaway week is visible.

### The first two weeks

Night 1 is files, the seed meeting rows, the access rows with their sources actually opened, and the indicator file set to COOLING. The phone page says the desk has started, the baselines are not ready, and no link is claimed. That page is the one to show Jaron first, so the empty shape is familiar before anyone is tempted to fill it.

Through 25 November, evenings maintain the ledgers and the measurer starts the failure-window series from Prep Watch's baseline. Hypothesis credit stays off. On 25 November the indicators arm. The first scores compare new events with the ledgers. They do not reach back into cooling week.

## 2. Indicators

An indicator trips only if it was ARMED before the event, the source named here published the fact, and the non-trip clause does not apply. A near-trip (one named fact short) can set the day's word to WATCH. It cannot move a hypothesis.

### China-Taiwan

The floor, already visible in Atlas's 17 November file, is a daily air and ship presence and a month that runs into the hundreds. A 5-sortie day is not a signal. These indicators sit above that floor.

| Id | Trips when | Source | Does not trip on | Bears on |
|---|---|---|---|---|
| CT-01 | Taiwan's defense ministry daily aircraft count is above the 90-day 95th percentile on 3 days inside 7 days. | The ministry's daily release. | One noisy day. A number inside the band. | Positioning, only once armed and only with a second track. |
| CT-02 | Median navy vessels in the daily count stay at or above 1.5 times the prior 90-day median for 5 published days. | Same. | A single surge that recedes inside the 5 days. | Positioning. |
| CT-03 | A named PLA exercise publishes a closure or live-fire box that includes Taiwan's territorial sea, or a box east of Taiwan in the Philippine Sea. | A PRC notice, or Taiwan or Japan reposting that notice with the coordinates. | The ordinary southwest ADIZ presence with no closure box. | Positioning. The earliest force tell. |
| CT-04 | Taiwan or Japan places a PLA carrier group east of Taiwan at the same time as a second group in the strait or the southwest. | A defense-ministry map or count that names both. | One carrier on a training cruise. | Positioning. |
| CT-05 | A NOTAM cluster reroutes international airways around Taiwan for a stated military reason, for more than 24 hours, outside a pre-announced exercise. | The aviation authority's NOTAM. | A weather reroute. A drill whose dates were public. | Positioning. The island getting harder to reach. |
| CT-06 | Taipei orders a reservist recall or a civil-defense activation that is not on the pre-published Han Kuang or Wan An calendar. | Presidential office, defense ministry, or interior ministry. | Those scheduled exercises. | Positioning. |
| CT-07 | A public evacuation, shelter opening, or fuel ration on the main island, which officials do not attribute to weather. | A Taiwan government page. | A typhoon. | Positioning. Late. If this trips, earlier ones should already have. |
| CT-08 | A cable owner reports a fault on a Taiwan-Matsu, Taiwan-Penghu, or Taiwan-Japan/US route and has not published a cause within 72 hours, and a second cable or landing-station fault falls inside 14 days. | The owner, or the Taiwan authority that regulates them. | A single cut. Those happen. | Positioning, space-and-undersea track. |
| CT-09 | Taiwan, Japan, or US Space Command reports GNSS interference or satellite-communications jamming covering Taiwan or the Bashi or Miyako channel. | That authority's statement. | A single ship's anecdote. | Positioning. |
| CT-10 | A PRC customs or coast-guard action halts a named Taiwan export category, or a named port (Kaohsiung, Keelung, Taichung, Mailiao), past routine inspection, with a date. | An agency document or a company filing. | A routine inspection with no halt. | Positioning, economic track. |
| CT-11 | A G7 or US statement names a specific PLA move as imminent, and the same week contains a costly action (an arms delivery moved up, liaison staff moved, an airline route dropped). | The statement plus the costly-action record. | The statement alone. | Positioning. Talk is not the trip. |
| CT-12 | A US Pacific carrier or amphibious group gets underway toward the first island chain when the public schedule had it in maintenance or in another theater, and no other reason (relief, a pre-planned exercise) is stated. | Navy or defense releases, both the old schedule and the new movement. | A deployment that was already on the calendar. | Positioning. |
| CT-13 | CISA, NSA, or the Taiwan government says in public that a named intrusion set has disrupted a US or Taiwan utility, port, or telecom, as opposed to maintaining access. | That statement. | Another advisory that repeats "pre-positioned." Presence is the access ledger. Disruption is this indicator. | Positioning, cyber track. |
| CT-14 | Taiwan's election commission, or a major platform's public report, documents a coordinated information operation in the 14 days before a scheduled recall, election, or named defense vote. | That report. | Ordinary partisan argument. | Positioning, information track. |
| CT-15 | Japan acts on the southwest islands: a munitions release, a deployment order, or an evacuation of Yonaguni or the Sakishima islands. | A Japanese government order. | A speech, including remarks already on the record about a survival-threatening situation. | Positioning. |

If a Taiwan crisis were actually being prepared, the order to expect is force disposition first (CT-03, CT-04, CT-02), then the island getting harder to reach and harder to see (CT-05, CT-08, CT-09), then societies acting (CT-06, CT-07, CT-15). CT-13 can move while the force group stays still. That is why cyber is a track of its own.

### US-Iran

This pair is already a war in the files Satya and Atlas maintain. These indicators are about widening, or about a new homeland function. They are not about whether shots are being fired.

| Id | Trips when | Does not trip on |
|---|---|---|
| IR-01 | CENTCOM or a Gulf government confirms a hit on a US base that causes casualties or knocks a function out. | A claim the other side denies, including a radar claim that is denied. |
| IR-02 | A US agency attributes a new disruption of a homeland function in a sector other than the water incidents already on the board. | Another retelling of the summer water reporting. |
| IR-03 | A war-risk or hull insurer suspends cover, or a flag state bans Hormuz transit, beyond the blockade already in effect. | A price move. |
| IR-04 | A Gulf state that had stayed out does both of these in one week: opens its territory to US strike aircraft, and expels Iranian diplomats. | Either one alone. Either one can be local politics. |
| IR-05 | The IAEA, or two governments, say a bombed site is being rebuilt toward enrichment. | One side's claim. |

### Russia-NATO

This pair is not the Russia-Ukraine war. The war stays on Atlas's ledger. These five are about NATO territory and NATO decisions.

| Id | Trips when | Does not trip on |
|---|---|---|
| RN-01 | A NATO member confirms a kinetic strike on its territory and names Russia. | An airspace brush. A drone pattern that is already the baseline. |
| RN-02 | NATO publishes an Article 4 request, or a North Atlantic Council communique that says Article 5 is under discussion. | Rumors and commentator threads. |
| RN-03 | Two or more NATO states announce forward deployments to the eastern flank in the same 14 days, outside a pre-scheduled exercise. | One country extending a rotation that was already planned. |
| RN-04 | Two governments attribute a Baltic or North Sea pipeline or cable cut to a state. | "Under investigation." |
| RN-05 | The hosting state, or a NATO agency, says on the record that a nuclear weapon has been moved in Belarus or Kaliningrad. | A Telegram channel. A recap of an older deployment. |

### Parking lot

Events that fit none of the standing pairs get logged under `pair: UNASSIGNED` so they are not forced onto the wrong ladder. The Russian aircraft Japan and Taiwan both recorded on 17 November are the example: they are not, by themselves, a Russia-NATO event, and they are not a PLA sortie. A standing pair is added only when its indicators are written and cooled. Korea is a named pair in the brief and has no armed indicators yet, so Korean events park here until a set is written. Israel stays inside the US-Iran pair for now, because that is how the current war is filed. Split it later if the war stops being one theater. India-China, India-Pakistan, and the Arctic are named here so their absence is a choice.

## 3. The ladder

### Tracks, beside Kahn, not inside his rungs

Kahn's 1965 ladder is one sequence with firebreaks, built for a bilateral nuclear crisis in which both sides know who did what and a central government is choosing the next rung. It is still the right tool for the force-and-nuclear question. It is the wrong tool for everything that was added later.

Cyber pre-positioning, a tariff schedule, a cable fault, and a proxy strike do not belong between "show of force" and "mobilization." They can sit still for years while the ships move, or move while the ships sit still. If Volt Typhoon were inserted as a rung, every quiet day in the strait would look like a crisis, because that disclosure is already years old. Inserted rungs would rebuild the fear machine out of a good book.

So Kahn stays whole, as the force track, and the newer domains are parallel tracks. A day is a row of placements, not a single number. A blended rung is not produced.

### Force track

Secondary copies of the book disagree on whether the first rung is numbered 0 or 1. The desk uses Kahn's names and his seven groups, and it does not publish a rung number. The six firebreaks between the groups, in his order, are: don't rock the boat, nuclear war is unthinkable, no nuclear use, central sanctuary, central war, city targeting.

The groups, with the rungs that sit in them:

- **Subcrisis.** Ostensible crisis. Political, economic, and diplomatic gestures. Solemn and formal declarations.
- **Traditional.** Hardening of positions. Show of force. Significant mobilization. "Legal" harassment and retortions. Harassing acts of violence. Dramatic military confrontations.
- **Intense.** Provocative break in relations. Super-ready status. Large conventional war or actions. Large compound escalation. A declaration of limited conventional war. Barely nuclear war. Nuclear ultimatums. Limited evacuation. A spectacular demonstration. A "justifiable" counterforce attack. A "peaceful" worldwide embargo or blockade.
- **Bizarre, and everything above it** (local nuclear use, then exemplary central attacks, military central war, civilian central war, up to spasm war). The desk does not place these from press reports. If a day appears to cross "no nuclear use," the placement is the firebreak, it requires a named official source, and it is line 1 of the mail.

A pair is placed in a group when today's costly action matches a named rung in that group. Words do not move the force track. The last costly action holds it.

### The other tracks

Each has a short ladder. The bottom step of several of them is already the steady state of this decade. The steady state is the floor, and a day is not news for sitting on the floor.

**Cyber.** No public campaign. Presence disclosed. An agency says the presence is for wartime disruption. One function is disrupted and attributed. Disruption repeats, or reaches a second function. Volt Typhoon, as the US agencies have described it, sits on "presence, described as pre-positioning," until a later sentence says a function was disrupted. That later sentence is CT-13 or IR-02, depending on the pair.

**Information and attribution.** Routine narratives. A government or a platform documents a coordinated operation. A named government disputes an attribution in public. A government reverses its own attribution.

**Economic.** Ordinary trade. Tariffs and export controls in force (the floor). A new control that bites a named chokepoint: chips, rare earths, a port, dollar clearing, insurance. A physical or legal cutoff of that chokepoint.

**Space and undersea.** Routine. Interference, or one fault under investigation. An attributed hostile act, or two faults in 14 days. Sustained loss of positioning, communications, or a cable function for a theater.

**Proxies and deniable violence.** None this period. A partner's forces active in a war that already exists. A new theater, or a new target class. The patron claims it, or is tied to it by an official finding.

### How a day is placed

For each standing pair, and for the CRINK core as its own row: one step per track, each with a label and a one-line reason. The force cell gets a Kahn group. The other cells get a step name.

A track moves up only on a new sourced fact that matches the next step. It moves down when that fact is RULED OUT, or when a disruption step goes 30 days without a new disruption. Presence disclosures do not decay on the 30-day clock. They decay on the access ledger's 180-day clock.

The sentence the desk is for is the gap: which track, if any, is ahead of force. "Cyber is a step ahead of the ships" is a finding. A single heat number is not.

Both views go in the cell. Taipei's wording and Beijing's wording are both stored. Placement follows the costly action when there is one. When the two capitals disagree and the only facts are words, the force group stays put and the disagreement is the information-track note.

### CRINK

Russia, China, Iran, and North Korea are scored as one row, built only from costly acts done by one of them for another: arms, energy, a veto, a payment rail, a port, a joint exercise that is more than a photo, a dual-use shipment a customs agency names. A communique is not a costly act.

The row has three words. **QUIET**: meetings and talk only. **COVER**: one costly act of support in the window. **ALIGNED**: two or more members each did a costly act for another inside 14 days. ALIGNED is not "alliance established." It is a count of costly acts, and the label on each act stays attached.

### Illustration, so the grain is visible

This is how the rule would treat 17 November using only what Atlas and Satya had already written. It is not a desk product, and it cannot trip anything.

- **US-Iran, force.** Large conventional war actions are already the recorded state: strikes, a blockade, a multi-carrier posture. That is the intense group. A reported dirty-bomb plan does not move it, because a report is not a use. The report stays on the information track as REPORTED, which is where Satya's log already has it.
- **China-Taiwan, force.** Show of force is the floor. Five aircraft and a handful of ships do not reach "dramatic military confrontation." An unannounced Pacific deployment is still a show of force until a closure box or a two-direction carrier pair is published.
- **US-China, force.** A summit week of diplomatic gestures, with hardening visible in the Japan-China freeze. Economic pressure is the track that may be ahead of force. The gap is the sentence. The summit itself is not.
- **The Russian flight.** Unassigned. Japan says its airspace was entered. Taiwan says its ADIZ was crossed. Neither fact is a Russia-NATO placement and neither is a PLA placement. It is a meetings-and-force note with two views stored, waiting on its +7 day window, which would close 24 November and still would not, by itself, credit a hypothesis.

## 4. The four hypotheses

Each one is scored only on evidence that post-dates the arming of the indicators it cites. All four start **untested**. Competitors are written here, before the next week of events, on purpose.

### (a) Small disruptions are distractions, to keep the US busy or panicked

Competitors:

- **H0.** Coincidence. The failure rate is the Prep Watch baseline.
- **H1.** Local brittleness. Bugs, hardware, and maintenance, piling up because the systems are fragile.
- **H2.** Harassment for its own sake. Impose a cost, with no second move timed behind it.
- **H3.** Distraction. Jaron's version. The disruptions cluster before a costly move somewhere else, and they hit attention rather than the logistics a war would need.
- **H4.** Shaping. Demonstrate access ahead of a crisis, without covering a move this week.

What would count for H3: the failure count in a pre-registered window at or above the 90th percentile of unflagged weeks, official causes still unpublished after 7 days for more than half of them, a costly move in another theater inside the following 3 days, the disrupted functions public-facing rather than war logistics, and the same shape in a second, separate window. One window is not a pattern.

What would count against H3: causes coming back as bugs or hardware, which Prep Watch already treats as the ordinary case. A rate inside the baseline. The disruptions hitting the same functions a real campaign would need, which fits H4 or an actual attack better than a distraction. The other-theater move having been on the calendar before the outages. A single window that fits and never repeats.

Scored when a window closes, not every evening.

### (b) An attack could be dressed up as Iran when it came from China

This one does not get the same test as the others. The Iran war is real in the files we already keep. A desk that treats "maybe China" as a standing explanation will train itself to set aside Iranian acts. That spends the credibility P-0166 is about.

Competitors:

- **H0.** The attributed actor did it.
- **H1.** A criminal or an insider, no state.
- **H2.** Iran did it, and China benefits without having done it.
- **H3.** China did it, and the Iran appearance is deliberate. Jaron's version.
- **H4.** China did it for its own reasons, and the Iran appearance is our prior.
- **H5.** Someone else.

The desk does not originate H3. H3 is opened only when a named government, a court, or two independent newsrooms citing named officials dispute the attribution. The diagnostic fact, if it ever exists, is an agency revising its attribution, or publishing that its indicators matched a different named set. The desk does not redo anyone's forensics and does not describe how a misattribution would be built.

What would count against H3: the actor claims the act, a second country concurs, the target fits Iran's stated campaign rather than a Taiwan-related one, or 30 days pass with no agency revision. Confirmed exchanged fire is the wrong object for this hypothesis. Where CENTCOM has confirmed an Iranian shot, H3 is not opened.

On the phone page, "attribution disputed" appears only with the names of the people disputing it.

### (c) Many moves are positioning for an eventual China-Taiwan crisis

"Eventual" cannot be tested. The version this desk will score has a horizon of 18 months and is about readiness, not about a date of attack. A timeless version is not kept on the list.

Competitors:

- **H0.** The coercion-and-training pattern that is already the floor.
- **H1.** Positioning for a crisis inside the horizon. Jaron's version.
- **H2.** The same visible moves, made so a crisis is not chosen. Deterrence.
- **H3.** Positioning for a different conflict, or for internal control.
- **H4.** Arms sales and exercises with no Taiwan timeline.

H1 and H2 predict the same ships. They come apart on the channel. H2 expects a crisis-management channel that gets used: a hotline tested, an exercise cancelled, a working military contact. H1 expects the moves plus that channel going quiet. Moves alone do not separate them.

What would count for H1: two tracks above their own 12-month floor at the same time, one of them force (CT-02, CT-03, or CT-04) and one of them cyber, economic, or space-and-undersea, inside the horizon, with the channel quiet.

What would count against H1: the Pacific deployment dispersing with no closure box. ADIZ counts under the 90-day median for 30 days. The channel being used. Chip and energy projects hitting their own published commercial dates with no logistics tell.

"Consistent with positioning" is allowed only under the two-track rule. One track is the floor of this decade.

### (d) Reshoring is partly so the US can survive a big war without collapsing

"Partly" will always look true if the desk scores tariff headlines. This one is quarterly. A daily tariff story does not move it.

Competitors:

- **H0.** Jobs and subsidies.
- **H1.** Insurance against a Taiwan shock, including a war. Jaron's version.
- **H2.** Insurance against a cutoff that is not a war: a quake, a blockade, an export ban.
- **H3.** Announcements timed to subsidies, which will slip.

The war-specific part is the part under test, not the existence of a factory.

What would count for H1: official documents naming wartime surge, defense stockpiles, or continuity of weapons and power. The capacity matching a war's bill of materials (munitions inputs, transformers, mature-node chips, pharmaceutical precursors, refined fuel) rather than only leading-edge AI chips. Timelines pulled forward after a Taiwan scare and not after an election. Allies moving the export-license and tooling constraints with the US, which a jobs program does not require.

What would count against H1: the capacity that actually lands is commercial leading-edge logic, while packaging, mature nodes, substrates, chemicals, and power stay offshore. Announced plants slipping their own dates. Exclusions quietly restoring the same import dependence. No published days-of-supply. A war-survival policy publishes a stock. An industrial policy publishes a job count.

The quarterly table has six columns: sector, stated reason quoted, days-of-supply if any number is published, on time or slipped, war-relevant or commercial, label. The first one is due at the end of February 2027, covering the quarter that starts once the indicators arm. Until then hypothesis (d) remains untested, on purpose.

## 5. What this design refuses, and what is still missing

The first month will find little, and that has to be written down as success. A desk that is graded on connections found will fit stories. Grade it on labels kept, windows closed on time, and indicators that survive the Sunday review.

I do not think hypothesis (b) should be tested the way the other three are. The bar above is the version I would actually run. A looser version is a machine for setting aside a war that is already underway.

I would not add rungs to Kahn. The tracks are the proposal. If the crew later wants a single number for a chart, that is the moment to stop and reread P-0166.

The series we do not have will matter more than any narrative seat. Prep Watch has a failure baseline. Nobody has a maintained series for Taiwan's daily counts, cable faults, export-license actions, or war-risk insurance. Building those, by hand, in jsonl, is the real first job. A graph database, an embeddings index of headlines, or an LLM "connection score" would make the desk worse. If this ever needs a dashboard, it has already failed.

The wire's volume is a temptation. On 18 November it turned 719 lines into 42 must-airs. The desk reads that list as "what will look connected on a phone," and then checks it against the ledgers.

Satya's scale measures functions down, close to home. This desk will keep finding Gulf and Pacific facts that should not move a household in Fort Wayne. The mail's fifth line exists so the desk does not tug the level without setting it.

Three things the brief did not ask for, which I would still keep:

- **Departures** as ledger rows. Embassy drawdowns and dropped airline routes are people moving, and they are costly. They belong next to meetings.
- **An unassigned bin** for events that fit no pair, so the Russian flight over Japan is kept without being promoted into the wrong war.
- **A quarterly reshoring table** instead of a daily score on hypothesis (d).

Three things I would leave out of version 1 on purpose: a separate Israel ladder, an India set, and an Arctic set. They are named in the parking lot so nobody thinks they were forgotten.

The access ledger is the piece most likely to go rotten. The rot looks like facility names and "what they could do" written in our own words. The discard rule is there because that rot will feel like thoroughness.

Claude should route the mail and not rewrite the phone page. Labels drift when a second editor polishes the prose. The breaker is the last editor.

Day 1's page, the one I would want Jaron to see before any of this earns a stronger sentence:

> Connections Desk, 18 November. QUIET. The ledgers are open. The failure baseline is Prep Watch's. The Taiwan aircraft baseline is not ready. No indicator is armed. No link is claimed. Shenzhen's after-window, if the meetings happen, closes seven days after they do, and nothing about that week can confirm a hypothesis until then.
