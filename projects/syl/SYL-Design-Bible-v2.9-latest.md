Space You Land (SYL Coming in 2027) top


Universe Codex & Design Bible v2.9

A Server-Authoritative 3D Persistent Universe

⸻

The Universe

Space You Land is a persistent 3D universe where leadership is temporary, stability is earned, and any player—regardless of wealth or status—can reshape history.

The galaxy operates on neutral, measurable dynamics: economy, activity, cooperation, and instability. No faction, player, or alliance can claim permanent victory. The universe itself ensures power remains fluid—not through admin intervention, but through system rules that survive misuse.

Governing idea: the universe does not belong to whoever shouts the loudest—it belongs to whoever can hold it together.

⸻

Core Principles

Server Authority

All economy, ownership, territorial expansion, and enforcement exist as authoritative server state. The client renders; the server decides truth.

AI as Advisor, Not Authority

The AI Director proposes actions based on server snapshots. The server validates, clamps, and logs every proposal. AI cannot bypass limits, execute raw code, or alter history.

Important distinction: Sovereignty / Custodian governance is not the AI Director. Custodians are server-driven NPC governance systems (deterministic simulation + rules), not an LLM with authority.

No Pay-to-Win

Monetization funds infrastructure and personalization—never power. Paid features provide cosmetic options, storage expansion, and enhanced narration. Combat stats, expansion shares, enforcement immunity, and intel access remain completely independent of payment.

Anyone Can Matter

Systems are designed so players without wealth, rank, or status can create meaningful change. Rebellion, espionage, solo operations, and underdog opportunities are built into the universe’s fabric.

Neutral Enforcement

Consequences are proof-based and measurable. All enforcement actions are recorded in an append-only audit ledger, creating tamper-evident accountability.

Continuity Over Control

The universe survives misuse and maintains fairness across extended timescales. Systems self-stabilize without administrative intervention.

⸻

The Seven Factions

Each faction offers a distinct advantage, operates under specific constraints, and has access to illegal edges that carry risk.
	1.	High-Tech Utopians
Home: Technos Prime
Edge: Advanced scanning, hacking, diplomatic channels, identity spoofing
Constraint: Fragile armor and lighter hull construction standards
Illegal Ops: Identity spoof networks, restricted AI cores
	2.	Militaristic Empire
Home: Fortis
Edge: Heavy armor, fleet coordination tools, superior defensive doctrine
Constraint: Low stealth capability, highly visible logistics trails
Illegal Ops: Weapons smuggling, forbidden ordnance trafficking
	3.	Space Nomads
Home: Wanderhome (mobile)
Edge: Extensive trade route knowledge, modular ship designs, barter bonuses
Constraint: Unstable governance structures, fragile political cohesion
Illegal Ops: Gray-market logistics, unlicensed route-running
	4.	Mystical Researchers
Home: Mystara
Edge: Anomaly detection, relic access, experimental “psychic-flavored” technologies
Constraint: Limited heavy industry, slow manufacturing capacity
Illegal Ops: Forbidden relic acquisition, sealed site trespass
	5.	Eco-Guardians
Home: Greenhaven
Edge: Bio-repair systems, enhanced morale mechanics, living hull technology
Constraint: Weak heavy industrial base, slower mass production
Illegal Ops: Gene contraband, bio-weapon research
	6.	Industrial Miners
Home: Ironclad
Edge: Superior mining, metallurgy, shipyard construction, resource extraction
Constraint: Vulnerable to labor strikes, supply shocks, and territorial disputes
Illegal Ops: Protected site excavation, industrial sabotage tools
	7.	Galactic Pirates
Home: Corsair’s Refuge
Edge: Cloaking tech, smuggling networks, hit-and-run tactics, stolen transponders
Constraint: Internal rivalry, unstable leadership structures
Illegal Ops: Everything—with escalating heat and enforcement risk

⸻

Gameplay Loops

Personal Loop

Fly → dock → trade/missions/combat → earn credits → upgrade ship and equipment → venture into riskier territory.

Faction Loop

Complete missions → participate in votes → diplomacy → embargoes → wars → shift momentum → expand territory.

Asset Loop

Own/manage stations or planets → set fees and taxes within caps → defend → navigate unrest, strikes, coups.

Shadow Loop

Black markets → trade intelligence → bribes/obligations → plant spies / get compromised → enforcement consequences.

Sanctuary Loop

Retreat to Private Sanctuary Instance (PSI) → store valuables/trophies → plan privately → return carrying only equipped items + ship cargo.

⸻

Ships

Ships are assets with ownership records, upkeep costs, and inherent risk. Examples:
	•	Scout (1 crew)
	•	Fighter (1–2 crew)
	•	Merchant (1–3 crew)
	•	Research Vessel (2–4 crew)
	•	Mobile Base (3–5 crew)
	•	Mining Rig (3–5 crew)
	•	Raider Corvette (2–5 crew)

All ships follow faction-linked design philosophies but can be captured, stolen, or traded.

⸻

Stations: Power Nodes of the Universe

Stations serve as trade hubs, military outposts, research facilities, agricultural centers, repair yards, cultural landmarks, and smuggler dens.

Station owners control:
	•	Access Rules (factions/reputation allowed)
	•	Fees: 0–20% transaction fees (hard-capped)
	•	Security Posture: patrol budgets/enforcement intensity
	•	Black Market Pressure: optimal 10–30% for stability

⸻

Economy

Resource Classes
	•	Basic: food, water, fuel
	•	Industrial: metals, composites, electronics
	•	Strategic: rare elements, experimental materials
	•	Illicit: contraband, stolen goods, forbidden tech

Stabilizers
	•	Faucets: missions, salvage, mining, bounties, trade margins
	•	Sinks: repairs, ammo, upkeep, docking fees, insurance, taxes
	•	Caps: storage limits, contraband heat, transaction throttles

Governance Caps
	•	Planet tax rate: 0–15%
	•	Station transaction fees: 0–20%
	•	Mandatory neutral hub: at least one per system

⸻

Governance and Leadership

Planet Governance

Governor (President) → Ministers → Assembly → Judicial Branch → Advisory Committees

Station Governance

Commander → Operations Chief → Security Chief → Trade Director → Residential Officer

Leadership is earned through elections, achievements, and appointments. Leaders face approval ratings, stability metrics, and possible no-confidence votes or coups.

⸻

Faction Relations

Alliances:
	•	Utopians ↔ Mystical Researchers
	•	Empire ↔ Industrial Miners
	•	Eco-Guardians ↔ Space Nomads

Rivalries:
	•	Empire ↔ Eco-Guardians
	•	Utopians ↔ Pirates
	•	Mystical Researchers ↔ Industrial Miners

Complex:
	•	Space Nomads ↔ Pirates (opportunistic, unstable)

⸻

Faction Momentum and Anti-Snowball Systems

Momentum (hourly) includes risk-weighted: trade throughput, PvE/PvP outcomes, territory control, infrastructure stability, governance approval.

Per-capita normalization:
EffectiveContribution = RawContribution / (ActivePlayers^0.4)

Leader pressure increases: upkeep strain, unrest probability, logistics exposure.
Trailers receive: lucrative contracts, discovery advantages, preferred lanes, lower friction.

⸻

Universe Expansion Engine

Expansion epochs: every 6–24 hours, new sectors open.

Deterministic seed:
hash(epoch + faction + index + ruleset_version)

Allocation:
	•	Minimum share per faction: 5%
	•	Leader share: 28–45% (scales with dominance)
	•	Primary rival share: 18–35% (conflict engagement over 72h)
	•	Remaining pool by relationship weights (Allied 0.6 / Neutral 1.0 / Enemy 1.2)
	•	Trade-assist parity clause: ally may match rival share only if normalization ≥ 0.22

Expansion costs increase defense obligations, unrest exposure, piracy pressure, and supply vulnerability.

⸻

AI Director (Proposal-Only System)

Closed loop: Unity snapshot → Server → AI proposal → Validation/clamping → Application → Unity renders

Whitelisted commands v1:
	•	adjust_tax
	•	adjust_station_fee
	•	change_station_access
	•	spawn_event
	•	start_faction_war / end_faction_war
	•	set_embargo / lift_embargo
	•	trigger_election
	•	trigger_coup
	•	tune_spawn_rates
	•	spawn_mission_templates

Validation checks: hard caps, cooldowns, neutral hub guarantees, append-only audit requirements.
AI cannot delete history, bypass limits, or execute unauthorized commands.

⸻

Ethos Drift: Factions Can Change

Axes: Order ↔ Chaos, Altruism ↔ Extraction
Drift influence: leadership 15–30%, player behavior 70–85%

Drift affects mission types, enforcement posture, black-market tolerance, reputation methods, diplomacy, and optional visuals. Factions can flip over time.

⸻

Solo Crew System

Solo mode (exactly 1 real player):
	•	NPC crew allowed up to ship capacity
	•	NPCs at 70–85% efficiency with delays
	•	Full ship system access

Multi-crew mode (2+ real players):
	•	NPC crew disabled (forces real teamwork)

First-hire captain bonus: Ghost Signature
	•	Hidden beyond 50 km
	•	Revealed 60–180s after firing/hacking
	•	Visual detection + close-range scans still work

⸻

Solo Integrity: Anti-Collusion System

Server monitors telemetry: damage, proximity, kill attribution, hostility windows.

If three “solo” ships fight and two coordinate suspiciously after one dies → flag collusion.

Penalty: Captain Walk-Off
	•	NPC captain leaves
	•	Cooldown: 2h → 12h → 48h (escalating)
	•	Ghost perks disabled temporarily
	•	Message: “This isn’t solo work.”

⸻

Rebellion, Espionage, and Enforcement

Rebellion path: formal initiation → defection window (logged) → neutral arbitration → measured consequences.

Espionage/treason classification based on proven sabotage, verified harmful intel leaks, coordinated actions aiding rivals. Terminology remains faction-flavored (no real-world baggage).

Enforcement ladder:
	•	Minor: warning + rep penalty
	•	Repeated sabotage/harassment: 15–30m detention
	•	State-level harm: 45m detention + deportation (forced faction repick)

Detention persists across logout; detainees retain markets, chat, PSI.

⸻

Pirate Cartel, Black Markets, and Intelligence Trading

Black market optimal 10–30% of trade volume. Below 10% stagnation; above 30% instability spikes.

Intel is tradeable with:
	•	Freshness: 72h decay
	•	Proof quality rating
	•	Chain of custody tracking
	•	Hop penalty: 20–30% per resale

Bribery/obligations tracked: debts, owed favors, future promises/contracts. Defaults damage reputation and restrict market access.

⸻

Companion System: Living Tutorial

Archetypes: Watcher / Crawler / Stride

Behaviors: explain-this UI, progressive learning, faction-flavored voice/personality, preference memory, bond development.

Zero authority over economy, enforcement, territory, combat outcomes, or political decisions. Guidance + narration only.

⸻

Monetization: Infrastructure Support Access (ISA) + BYOK

Allowed paid: personalization, extended storage vault sizes, enhanced narration quality, cosmetics, PSI upgrades/decor.

Prohibited: anything that increases combat stats, expansion shares, immunity, intel access, or stealth beyond defined solo rules.

BYOK companion: key stored client-side only; not transmitted to SYL servers. SYL provides entitlement verification + redacted context packets; output limited to narration/UI assistance.

⸻

Private Sanctuary Instances (PSI)

Private pocket-space moon/base.
Owner-only by default. Upgradeable storage, trophies, decor. No resource generation, no automation, no offline production. Leaving PSI returns only equipped items + ship cargo.

Modes: server-hosted (recommended) or client-local cosmetic (optional).

⸻

Sovereignty Law: Empty Space Gets Governed

Space You Land runs on human politics when players are present and responsible: elections, treaties, commerce, raids, alliances, betrayals, rebuilding.

But when a region collapses—through mass griefing, endless war, market manipulation, station lockdowns, or player absence—the solar system does not pause. It adapts.

What It Is

Sovereignty Law is the universe’s immune response: if humans abandon a sector, the server fills the vacuum with an NPC/sovereign stabilizer force—custodian fleets, interim station commanders, automated trade convoys, and security patrols—so the world remains alive.

If players remain present but destabilize the ecosystem, custodians escalate into emergency governance:
	•	taxes get capped
	•	access gets restricted
	•	chokepoints get quarantined
	•	key stations can be reclaimed by custodians

This is not punishment. It is continuity enforcement. The universe refuses to be permanently broken.

Transparency: Thresholds and Stages

Players can see:
	•	Region Stability Index
	•	Chaos signals
	•	Current AI Control Stage (custodian stage)

Escalation ladder (gradual):
Observation → Containment → Martial Governance → Reclamation → Quarantine
De-escalation mirrors this as stability returns.

Reclaiming Control Is a Campaign

Control returns in finite seats (Governor, Station Commander, Security Chief, Trade Director) only after humans prove they can run the region without collapsing it again.

The key metric is Rebuild Credit: verified actions that restore function after damage:
	•	repairing stations
	•	reopening trade routes
	•	escorting convoys
	•	delivering scarce supplies
	•	stabilizing elections
	•	rebuilding infrastructure chains

Rebuild Credit is region-scoped. You cannot grind somewhere safe and claim leadership somewhere broken. You must rebuild where the damage happened.

Legitimacy Beats Wealth

High Rebuild Credit increases eligibility for seats and becomes the legitimacy edge in contested governance:
	•	if multiple candidates qualify → election
	•	if close → reconstruction breaks the tie
	•	if still equal → coverage of rebuild categories → randomized roll → runoff

Message: if two people want power, the one who rebuilt more has the stronger claim.

Heat: Sharp Against Bad Actors Without Becoming Petty

Players and groups accrue Heat (risk signature) based on measurable harm patterns:
	•	repeated low-value kills
	•	blockade behavior
	•	treaty violations
	•	market manipulation
	•	exploit flags

Heat drives targeted NPC behavior:
	•	bounty hunters tracking offenders across systems
	•	undercover agents in stations
	•	patrol focus on specific groups
	•	docking denials forcing high-heat players to the edge

This makes the world feel alive: not every encounter is another player—sometimes it’s the universe responding.

The Outcome

A sandbox that can’t be permanently hijacked by griefers and can’t die when populations shift.

Players can start wars, crash markets, raid lanes, topple governments—but if they push too far, they risk losing the privilege of governing at all. When custodians take a region, enemies often become allies out of necessity. Pirates end up flying escort. Solo traders become diplomats by default.

The universe forces cooperation through environmental pressure, not moral lectures: stabilize the system together, or live under machine governance until it’s rebuilt.

Power is not owned. Power is leased—by the universe—to whoever proves they can maintain it.

⸻

Solar Storm System: Event-Driven “Sun Heating” (COMMS FALL)

(This section remains as previously written, and now sits alongside Sovereignty Law as a second neutrality-based stabilizer: one is “vacuum governance,” the other is “instability weather.”)

Purpose

A neutral, physics-themed mechanism triggering only when the universe shows sustained instability, imbalance, or unhealthy patterns. Stable societies can hold position longer, but systemic issues eventually force shake-ups that empower low-tier and solo players.

SUN_HEAT (0.0 → 1.0) rises on instability signals, cooperation collapse, and activity imbalance; falls when stability returns. Alerts at 0.60 / 0.75 / 0.90. Storm triggers at 0.95 sustained (6–18h lock). COMMS FALL localizes markets, disrupts long-range comms, keeps low-power rigs online, preserves starter protections, and includes exactly one storm safe corridor.

⸻

Canonical Values (Reference)

Core:
	•	α = 0.4 (per-capita normalization)
	•	Expansion epoch: 6–24h
	•	Conflict window: 72h
	•	Trade-assist threshold: 0.22
	•	Min faction share: 0.05
	•	Leader share: 0.28–0.45
	•	Rival share: 0.18–0.35

Solo:
	•	Ghost hide: 50 km
	•	Reveal: 60–180s
	•	Walk-off: 2h / 12h / 48h

Enforcement:
	•	Detention: 5–10m / 15–30m / 45m + deportation

Shadow economy:
	•	Intel freshness: 72h
	•	Hop penalty: 20–30%

Storm:
	•	Alerts: 0.60 / 0.75 / 0.90
	•	Trigger: 0.95 sustained
	•	Duration: 6–18h
	•	Cooldown: quiet period enforced

Sovereignty Law (new canonical anchors):
	•	Custodian stages: Observation → Containment → Martial → Reclamation → Quarantine
	•	Rebuild Credit: region-scoped legitimacy metric
	•	Heat: actor risk signature driving targeted NPC response
	•	Seats unlock: finite authority positions released as reclaim progress increases

⸻

The Philosophy

Leadership is temporary. Stability is earned. Anyone can matter.

The universe doesn’t judge. It measures. And it responds.
Not with admin hands—but with neutral laws: Sun Heating when societies destabilize, and Sovereignty Law when space is abandoned or broken.

⸻

Updated Marketing Copy (Now Includes Sovereignty Law)

ELEVATOR PITCH (1 SENTENCE)

Space You Land is a server-authoritative, persistent 3D galaxy where power can’t calcify—if players abandon or destabilize a region, custodians take over until humans rebuild it, and when imbalance spreads, solar storms fracture coordination so underdogs can reshape history.

TAGLINES (PICK 1)
	1.	Leadership is temporary. Stability is earned. Anyone can matter.
	2.	A galaxy that won’t let you win forever.
	3.	Build. Betray. Rebuild the right to rule.
	4.	The universe keeps the score—fairly.
	5.	No pay-to-win. No permanent empires. No dead end futures.

10–15 SECOND HOOK (AUDIO-READY)

Space You Land is a living galaxy where power is leased, not owned. Break a region and custodians take it back until you rebuild. Push the universe into imbalance and solar storms shatter coordination. Leadership is temporary. Anyone can matter.

30–60 SECOND TRAILER VO (AUDIO-READY)

Welcome to Space You Land—an always-changing, persistent galaxy where the server decides the truth and no faction can lock the universe down forever.
Choose one of seven factions: utopians, empires, nomads, researchers, eco-guardians, industrial miners, or pirates. Fly, dock, trade, mine, fight, steal, and build influence—alone or with others.
Own ships. Control stations. Tax planets within hard caps. Run black markets. Trade intelligence that decays with time. Start wars—or end them.
But this universe has an immune system. If a region collapses or gets abandoned, custodians step in—capping taxes, restricting access, reclaiming stations—until humans earn control back through real reconstruction. And when instability spreads far enough, the sun heats up… leaders get warnings… and COMMS FALL hits—long-range coordination breaks, markets turn local, and small crews suddenly matter again.
You don’t win forever here. You survive, adapt, rebuild legitimacy, and write history—again and again.
Space You Land. Coming 2027.

STORE PAGE SHORT DESCRIPTION (1–2 LINES)

A server-authoritative, persistent 3D universe where power can’t calcify. Break or abandon a region and custodians take over until you rebuild; push the galaxy into imbalance and solar storms fracture coordination so underdogs can rise.

STORE PAGE MAIN DESCRIPTION 

Space You Land (SYL) is a server-authoritative 3D persistent universe built around one core truth: no one holds power forever.

In SYL, the galaxy runs on measurable dynamics—economy, activity, cooperation, instability. You can become a governor, a station commander, a cartel broker, a pirate legend, or a quiet solo operator who changes everything. The server enforces hard caps, logs decisions in an append-only audit ledger, and keeps the universe fair over long timelines.

Choose from seven factions, each with real strengths, real constraints, and illegal edges that carry escalating heat: High-Tech Utopians, Militaristic Empire, Space Nomads, Mystical Researchers, Eco-Guardians, Industrial Miners, and Galactic Pirates.

PLAY YOUR WAY
• Fly → dock → trade/missions/combat → earn credits → upgrade → push into riskier space
• Run stations and planets: set access rules, fees, security posture, and manage unrest
• Work the shadow economy: intelligence trading with decay, chain-of-custody, bribery obligations, spies, sabotage, and enforcement risk
• Retreat to your Private Sanctuary Instance (PSI): plan in total privacy and return carrying only equipped items and cargo

A GALAXY THAT PUSHES BACK
SYL won’t let regions die—or be permanently hijacked.

SOVEREIGNTY LAW (EMPTY SPACE GETS GOVERNED)
If players abandon a sector, the universe fills the vacuum with custodian fleets, interim station commanders, automated convoys, and patrols so the world stays alive. If players destabilize the ecosystem—endless war, griefing, market manipulation—custodians escalate into emergency governance: taxes get capped, access gets restricted, chokepoints get quarantined, and key stations can be reclaimed.
Players can see a region’s Stability Index and the current control stage. Control returns through a campaign, unlocking authority seats only when humans prove legitimacy through region-scoped Rebuild Credit: repairing stations, reopening trade routes, escorting convoys, delivering scarce supplies, and rebuilding infrastructure chains.

SOLAR STORMS (COMMS FALL)
SYL also includes an event-driven Solar Storm system powered by a neutral “Sun Heating” meter. When instability, cooperation collapse, or faction activity imbalance persists, leaders receive warnings—then storms can trigger:
• Long-range communications degrade
• Faction-wide coordination tools become limited
• Markets fragment into local economies
• Low-power, low-tier comm rigs stay online—so smaller ships and solo play can thrive

FAIRNESS BY DESIGN
• No pay-to-win: monetization supports infrastructure and personalization only
• AI is advisor-only: proposals are validated, clamped, and logged—no raw code, no bypassing limits
• Anti-snowball mechanics: per-capita normalization, leader strain, and trailer support opportunities
• Proof-based enforcement: consequences are measurable and auditable

Leadership is temporary. Stability is earned. Anyone can matter.

FEATURE BULLETS (STORE PAGE “KEY FEATURES”)

• Persistent server-authoritative galaxy: the server decides truth, the client renders it
• Seven factions with unique edges, constraints, and high-risk illegal operations
• Player-driven economy with hard caps on taxes and station fees
• Stations as power nodes: control access, security, fees, and black market pressure
• Shadow economy: trade intelligence with decay, chain-of-custody, and resale penalties
• Sovereignty Law: abandoned or broken regions fall under custodian governance until rebuilt
• Rebuild Credit legitimacy: earn authority seats by restoring the region you damaged—or the one you saved
• Solar storms (COMMS FALL) that disrupt coordination and re-balance opportunity
• Private Sanctuary Instances (PSI): safe planning space with upgrades, trophies, and storage
• Solo integrity system that detects collusion and enforces consequences
• No pay-to-win monetization: cosmetics, storage, narration, PSI decor—never power

⸻
