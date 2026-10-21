> **Jaron's answers 10/3 9:06 AM (override anything below):** one system = our real Solar System at real scale, planets spin and
> moons orbit; Wanderhome and Corsair's Refuge = station networks; many ship types with a shipyard shop (the four built ships
> are the bar); old builds give ideas only - never their art or assets (they looked fake); the bible is a guide, not law.
> See DECISIONS.md.

# Space You Land - WORLD MAP

Written 2026-10-03 for Jaron. Question he asked (10/3 8:39 AM): before missions and story, what is the WHOLE environment the
game is supposed to have - every planet, ship, city, prop, small detail?

This is the full inventory, read from every design source, checked against what The Cosmos has today. Plain words. Where the
bible is silent, it says so. Where I am proposing something (not Jaron's words), it is marked PROPOSED so nobody mistakes it
for canon. The opening's set pieces are in the builders' file (not repeated here).

## How to read this

- **Status**: none / partial / done, for The Cosmos today (games/the-cosmos).
- **Size** (one Sonnet builder, one worktree, AI time not human time): S = under an hour. M = a few hours. L = most of a long
  session, or needs splitting.
- **Bible** = v2.9 (and v2.7 where v2.9 says "as previously written"). They are Jaron's draft vision. The Full Game "v3.0.1
  canon" and its amendments are NOT binding (DECISIONS 9/30); they are used here only as idea sources, and labelled.
- **Source tags**: [B] bible v2.9/v2.7, [D] Jaron's DECISIONS, [C] already in The Cosmos, [FG] SYL-Full-Game build, [UE] the
  Unreal SpaceYouLand build, [PC] the desktop PC experiment, [NB] SYL-Neighborhood, [V3] Full Game later canon (idea only).

## The big honest finding

**The bible names almost no places.** v2.9 and v2.7 give seven faction HOME WORLD NAMES and nothing else about geography:
no planet sizes, no cities, no station names, no map. Everything below those seven names comes from builds (Full Game's nine
bodies and 24 landing zones, the PC experiment's three more bodies, the Unreal Fortis art, The Cosmos' Mars). So "all the
planets that need to be there" is, strictly, **seven faction homes + one neutral hub per system + the private pocket moon
(PSI)**. Everything else is Jaron's call. This document lists the bible's required places first, then the ideas Jaron already
saw in builds, then proposals marked PROPOSED to fill the rest.

The bible is also nearly silent on **travel**: it says "Fly -> dock", "chokepoints", "trade lanes", "convoys", "sectors" (new
ones open every 6 to 24 hours), "systems" (plural, each with a neutral hub). It gives no jump drive, no speeds, no distances.
The jump drive exists only as a line in The Cosmos nav computer ("Fortis, Greenhaven, Ironclad... needs a jump drive"). Jaron's
decision 9/30: "I do want things to take a while."

---

## 1. Planets, moons, stations, fields and regions

### 1.1 What the bible REQUIRES to exist

| # | Place | What the bible says | In The Cosmos | Size |
|---|---|---|---|---|
| 1 | **Technos Prime** | Home of High-Tech Utopians. Edge: scanning, hacking, diplomacy, identity spoofing. Constraint: fragile armor, lighter hulls. | none | L |
| 2 | **Fortis** | Home of the Militaristic Empire. Heavy armor, fleet tools, defensive doctrine. Low stealth, "highly visible logistics trails". | none (listed in nav sheet, refused: needs jump drive) | L |
| 3 | **Wanderhome (mobile)** | Home of Space Nomads. "Mobile". Trade routes, modular ships, barter. Unstable governance. | none | L |
| 4 | **Mystara** | Home of Mystical Researchers. Anomalies, relics, "psychic-flavored" tech. Limited heavy industry. | none | L |
| 5 | **Greenhaven** | Home of Eco-Guardians. Bio-repair, morale, living hulls. Weak heavy industry. | none (listed, refused) | L |
| 6 | **Ironclad** | Home of Industrial Miners. Mining, metallurgy, shipyards. Vulnerable to strikes and supply shocks. | none (listed, refused) | L |
| 7 | **Corsair's Refuge** | Home of Galactic Pirates. Cloaking, smuggling, stolen transponders, hit and run. | none | L |
| 8 | **One neutral hub per system** | "Mandatory neutral hub: at least one per system" (hard cap rule). | partial: Marineris Port on Mars is the neutral hub of the Mars space (Jaron 9/30: start on a neutral place, "maybe Mars") | M to finish |
| 9 | **Stations (every kind)** | "Trade hubs, military outposts, research facilities, agricultural centers, repair yards, cultural landmarks, and smuggler dens." Owners set access, fees 0 to 20%, security, black-market pressure. | none (only a ground port) | L (kit) + M each |
| 10 | **Private Sanctuary Instance (PSI)** | "Private pocket-space moon/base." Owner only, storage, trophies, decor. No production. Leaving returns equipped items and ship cargo only. | none | M |
| 11 | **Sectors (expansion)** | New sectors open every 6 to 24 hours; shares by faction; "claimed territory". | none | L |
| 12 | **Storm Shadow Corridor** | Exactly one safe corridor during a solar storm; no damage of any kind; limited size. | none | M |
| 13 | **The Sun** | Has a SUN_HEAT meter (0 to 1), alerts 0.60 / 0.75 / 0.90, storm at 0.95. | partial: Sun disc and fixed direction only, no heat, no storm | M |
| 14 | **Chokepoints / trade lanes / convoy routes** | Custodians quarantine chokepoints; players reopen lanes; convoys travel. | none | M |
| 15 | **Regions with a Stability Index** | Region Stability Index, chaos signals, custodian stage visible to players. | none | L (server) + M (visible) |

Bible says nothing about: sizes or gravity of any home world, whether homes are planets or stations (Wanderhome is "mobile" and
Corsair's Refuge reads like a hideout), number of systems, how systems connect, a galaxy map.

### 1.2 Mars space (the one real place that exists) - [C] done to a high bar

Real scale, from `src/world/bodies.js` and `src/space/spaceSpec.js`.

| Body | Real-scale facts used | Status | Notes / gaps |
|---|---|---|---|
| **Mars** | Mean radius 3,389,500 m (equatorial 3,396,200, polar 3,376,200). Gravity 3.72076 m/s2. Escape 5,030 m/s. Day 24.62 h (SOL = 88,775 s used by the economy). Tilt 25.19 deg. Air 610 Pa, scale height 11.1 km, CO2 95%. Temperature -153 to +20 C, mean -65. Sky butterscotch (dust). 1.5 AU from the Sun. | **partial** | 3D density field with regolith / duricrust / basalt / ore / latitude ice / unmineable mantle, caves in the field (no cave geometry drawn). Real landmarks in the address book: Olympus Mons (18.65 N, 133.8 W, 21.9 km), Valles Marineris (14 S, 59.2 W), Airy-0, Hellas Planitia (8.2 km deep). Only the Marineris Port patch is built up. Mars does NOT rotate (no day or night), no weather. Polar caps and provinces painted only on the far view. |
| **Phobos** | Semi-axes 13.03 x 11.40 x 9.14 km, mass 1.066e16 kg, gravity 0.0056 m/s2, escape 11.2 m/s, orbit 9,376 km (period 7.65 h, tidally locked). Stickney crater 9 km across 1.7 km deep, Limtoc. | **done (first pass)** | Walkable, diggable volume. Stickney East survey pad (flat 62 m), 3 sample beacons (184 m, 680 m, 1.29 km), drifting cargo module 780 m SW, boulders, grooves, hydrated clay under Stickney ejecta (game fiction, marked). Moon parked (does not orbit). Grok job queue 6/7 (real models for beacon and cargo module, eye-level ground) still open. |
| **Deimos** | Semi-axes 7.8 x 6.0 x 5.1 km, gravity 0.0026, escape 5.6 m/s, orbit 23,459 km, 100 m of dust so it is smooth. Voltaire crater 2 km. | **partial** | Pad and field exist; much less dressed than Phobos. No jobs there except raiders and an abandoned hull. |
| **Mars orbit (400 km)** | Nav destination. Raiders live here. Orbit period 118 min. | **partial** | No station, no traffic, no debris, no ring of satellites. |
| **The Gate (120 km)** | Where lift pods hand over to the main drive. | done (a number) | No physical gate or marker. |
| **Space between** | Flip-and-burn courses, free flight with real gravity, time compression x5 to x500, fuel as delta-v (12 km/s). | done | Empty. Nothing to see between Mars and the moons: no debris, no traffic lanes, no beacons, no other ships except raiders. |

Mars sub-places that real Mars supplies for free and that the game should eventually reach (PROPOSED unless noted):

| Place | Real facts | Status | Size |
|---|---|---|---|
| Marineris Port (14 S, 59.2 W) | The current spawn. Apron 210 x 176 m, graded 160 m. See section 2.1. | partial/done | (in 2.1) |
| Valles Marineris canyon | 3,870 km long, 600 km wide, 9.3 km deep. Field is "procedural, not a surveyed canyon model". | partial: ridges only, no mapped walls | M |
| Olympus Mons | 21.9 km above the datum, 600 km wide, shield volcano, caldera. Real landmark in the address book. | none built | M |
| Hellas Planitia | Basin floor 8.2 km below datum; thickest air. | none built | M |
| Polar caps and ice | Latitude ice exists in the field; caps painted on far view only. | partial | M |
| Dust storm country | Global storms are a real Mars thing. | none | (see 6.1) |
| Lava tubes and caves | Field has caves (2.7% of rays hit a void, 13 to 352 m tall). "Caves have no geometry" (README). | partial | L |
| Airy-0 prime meridian marker | Landmark. | none | S |

### 1.3 Places that appeared in builds (Jaron already saw these ideas) - labelled by source

Full Game's nine bodies are COMPRESSED scale (Earth radius 3,000 m). Their `realRadiusKm` / `realGravity` fields record the
design intent. Several are wrong or inconsistent (Aethelgard and Veldora carry Jupiter and Saturn numbers while being described
as surface worlds). Treat as names and character, not numbers.

| Body | Source | Character | Landing zones / sites | Faction in build | In Cosmos |
|---|---|---|---|---|---|
| **Earth** | [FG][UE] | Home. Green and grey, sea level, 900 m air band. Unreal built true-scale Earth reference (radii, Moon at lunar distance). | Fortis Outpost North Pad (spawn), Abandoned Relay Station (pre-war, salvage alloy), Fortis Salvage Yard (fuel cache for stranded pilots), Fortis Civil Terminal Earth Line (transit) | Fortis | none |
| **Moon** | [FG][UE] | Grey, silent, contested, 1.62 m/s2, no air. | Tranquility Landing Field (survey beacon, regolith), Tranquility Civil Hub (shuttle dock) | Meridian Combine | none |
| **Rustholm** | [FG] | Captured asteroid rock, 0.45 m/s2 (game) / 0.11 real. Fuel runs. | Freeport Claim 7 (syndicate fuel cache), Freeport Transit Dock | Freeport Syndicate | none |
| **Aethelgard** | [FG] | Water world, deep oceans, storm-wracked archipelagos, blue palette. | Halcyon Enclave Diplomatic Harbor, Halcyon Civil Quay, **Submerged Ruins / The Drowned City** (crystal in flooded foundations) | Halcyon Accord | none |
| **Cryos** | [FG] | Ice moon of Aethelgard, shell over dark ocean. | Meridian Ice Station Gamma (ice harvest and fuel cracking), **The Great Crack Fissure Field** (ore veins) | Meridian Combine | none |
| **Pyrrhus** | [FG] | Volcanic hellscape, lava plains, ash storms, orange air. | Fortis Bastion (hardened, titanium mining), Bastion Transit Terminal (armored civilian berths), **Caldera 7 Abandoned Survey** (unstable exotic matter) | Fortis | none |
| **Veldora (Ringed)** | [FG] | Ringed garden world, methane seas, green air. Fleet anchored in the high atmosphere. | Kindred Mooring Fleet Anchorage, Kindred Public Mooring (passenger mast), **Ring Fragment Mine / The Shattered Arc** | Kindred of the Long Walk | none |
| **Ironcore** | [FG] | Nickel-iron asteroid, heavy for its size. | Registry Foundry Deep Core (titanium ingots), Surface Claim 12 Independent Strip | The Registry | none |
| **Dunewind** | [FG] | Mars-like desert, rust dunes, dust storms. | Freeport Dune Station "Smuggler's Rest" (fuel and contraband), Dune Transit Berth, **Wreck of the Typhon** (crashed survey vessel) | Freeport Syndicate | none |
| **Nimbara (Storm Giant)** | [PC] | Non-landing gas giant, banded atmosphere, rings. Fuel skimming target and navigation landmark. | none (not landable) | none | none |
| **Obsidian** | [PC] | Black volcanic world, active calderas, glass. | Fortis Forge Line (refinery cut into volcanic glass) | Fortis | none |
| **Mirrorglass** | [PC] | Blue-white ice body, long cracks, reflective crust. | Meridian Mirror Observatory (ice crust lenses weak signals) | Meridian Combine | none |

Full Game also has 44 pickup ids (salvage alloy, regolith ore, wiring loom, hydrazine, titanium ore, water ice, crystal matrix,
exotic matter, scrap electronics, nickel-iron, ingots, cracked hydrogen, sensor crystal, composite alloy, circuit boards,
reactor cores, and ship parts). Those are cargo items, not places, but each discovery site above hands out one ("discovery
reward"). Keep as a design pattern: **every site has one thing worth finding**.

### 1.4 How Full Game's invented factions map to the bible's seven (PROPOSED mapping, Jaron decides)

Full Game's registry had Fortis plus six placeholders (the file itself says "obsolete migration input, not canon"). To reuse
their places without silently renaming factions, this is the closest fit:

| Full Game placeholder | Closest bible faction | Why |
|---|---|---|
| Fortis | Militaristic Empire (Fortis) | same name; Full Game wrongly put it on Earth |
| Meridian Combine (Moon, Cryos, Mirrorglass) | Industrial Miners (Ironclad) | mining and ice cracking; amber colour |
| The Registry (Ironcore foundry) | Industrial Miners (shipyards, metallurgy) | "the world is built, not spawned" |
| Freeport Syndicate (Rustholm, Dunewind) | Galactic Pirates (Corsair's Refuge) | smuggling, fuel and contraband |
| Halcyon Accord (Aethelgard) | High-Tech Utopians (Technos Prime) | diplomacy |
| The Veil (spy network, no place) | Utopians (identity spoofing) or Pirates (stolen transponders) | espionage |
| Kindred of the Long Walk (Veldora fleet) | Space Nomads (Wanderhome) | walkable fleet, mobile |
| (nobody) | Mystical Researchers (Mystara) | closest: Mirrorglass observatory, Drowned City, crystal and exotic matter |
| (nobody) | Eco-Guardians (Greenhaven) | closest: Veldora's garden world |

### 1.5 PROPOSED real-scale and character for the seven homes

Bible gives only names. These are proposals so builders have something to build to. Pick real numbers so gravity, horizon and
travel time are honest (Jaron: real scale, "things to take a while"). All need Jaron's yes before anyone builds a world to them.

| Home | PROPOSED body | Gravity / air / sky | Look |
|---|---|---|---|
| Fortis | Rocky world near Earth size, cold and dry, one continent of armored cities and mountain bastions. (Keep Pyrrhus-style volcanic belt and Obsidian forge as its industrial north.) | about 9 m/s2, thin cold air, grey-brown sky, ash and dust storms | Walls, gates, searchlights, red warning lights, heavy panels (section 4) |
| Technos Prime | Smaller bright world with sealed domes and a high orbital ring of labs and relays. | about 7 m/s2, clean air, pale blue to white sky | Glass, white composites, soft blue light, lighter structures |
| Wanderhome | NOT a planet: a moving fleet of walkable ships and modular platforms that travels a trade loop (Full Game's Kindred anchored in Veldora's high air). Needs a route schedule so players can find it. | n/a (ships), or hangs in a gas giant's upper air | Patchwork, mismatched modules, lanterns, rope-and-cable look, lived-in |
| Mystara | Mist-covered, ruin-strewn world with anomaly fields; ringed or low-gravity. | about 5 m/s2, thick pale air, violet-gold sky | Standing stones, crystal, sealed doors, glyph light |
| Greenhaven | Temperate garden world, forests, rivers, living-hull yards. | about 9 m/s2, Earth-like air, green-blue sky | Wood-and-grown-material, domes of leaf and vine, soft greens |
| Ironclad | Heavy metal-rich world or a belt with a giant mining moon; deep pits, smelters, shipyards. | about 8 m/s2 world, or low-g belt | Rust, steel, chimneys, gantries, sparks, amber work lights |
| Corsair's Refuge | A hidden hollowed asteroid or wreck-built station in a dead zone (Full Game's Rustholm and Dunewind's Smuggler's Rest show the tone). | low gravity or none | Scavenged hull plates, stolen transponders on a wall, graffiti, mismatched lights |
| PSI | Pocket-space moon, private. | player-chosen look | Decor, trophy walls, vaults |

---

## 2. Cities, ports, outposts, bases, landmarks per world

The bible has **no named cities at all**. It has governance structures that imply places (below). The only built place is
Marineris Port. Everything else is PROPOSED from the faction identity, from Full Game's zone list, and from the Unreal Fortis
assets.

### 2.1 Marineris Port, Mars (the neutral hub) - [C] partial/done

Surveyed in the planet's frame. Coordinates are port-local metres (x right, z south). Registry ids `COS-MARS-STR-01xx`.

| Thing | Where / size | What is built | Gaps | Size to finish |
|---|---|---|---|---|
| Apron | 210 x 176 m, graded 160 m blend, 1.2 m engineered fill over duricrust | Concrete pavement with wear stamps, tyre tracks, oil stains, expansion joints, retaining kerbs with marker lights, 4 kerb openings, 4 floodlight masts, drainage and tie-downs | Wind, dust drift, no day/night lighting change | S |
| Pad 01 "Meridian" | 0,0; 38 x 64 | done | | done |
| Pad 02 "shuttle" | 62,-28; 30 x 38 | pad exists, **no shuttle ship stands on it** | shuttle ship | M |
| Pad 03 "courier" | 62,30; 26 x 32 | pad exists; Wayfarer courier def exists | not parked there, no price | S |
| Pad grid (player pads) | append-only grid east of the port | slabs, markings, lights, grading (new players each get a pad) | | done |
| Supply depot | -62,18; 24 x 18 x 7.44 | curved roof, ribs, rack bays, reception counter, pallet lift, rooftop plant, airlock hood, sliding doors | | done |
| Open market | -58,53; 32 x 8 | 4 coloured awnings (Ares Provisions, Second Orbit Salvage, Blue Well, Ridgeline), 6 rentable player stalls (row z 60) | | done |
| Port control tower | -60,-39; 12 x 12 x 28 | lobby, **elevator** (2.2 x 2.6 m car), glass cab at 22.5 m, 8 worker spots (controllers, weather officer, supervisor, runner, lookout), radar, beacon mast | weather instruments are "offline" | done |
| Fuel farm | 57,-70; 24 x 12 x 6 | built (tanks) | no fuel trucks, refuel is automatic | S |
| Cargo staging | 51,65; 26 x 6 x 2.9 | containers | | done |
| Beacon sign | -28,65; 16 x 1 x 5 | lit sign stand | | done |
| **Crew hall / cantina** | north of main pad | **a plain box with a label** (4 walls, door gap) | needs real building, interior, bar, notice board, seating, kitchen | M |
| Shipyard kiosk | -36,40 | kiosk with price board (sells Shrike 2,400 cr, Drayman) | needs a real yard: gantry, bay, ships on display | M |
| Hiring board | by Meridian ramp | board + 5 candidates (pilot Ada, captain Zuri, navigator Jorge, gunners Sunita and Walter) | | done |
| Weigh bay | -83,24 (amber) | amber weigh bay for regolith sale (quest) | no real depot yard, no conveyor, no scale building | S |
| Marineris Survey Office | named in jobs ("The Marineris Survey Office pays 300 credits per core sample") | **a name only** | building, desk, map wall, sample lockers | M |
| People | 15 port workers and traders (Loft MetaHuman bodies) | done | only 7 faces total (see section 5) | M |

### 2.2 Marineris City and Mars beyond the port - PROPOSED, none built

The bible says each system has a neutral hub. A hub that is only an airfield is thin. PROPOSED around the port:

| Place | Purpose | Notes | Size |
|---|---|---|---|
| Marineris Town (habitat blocks, domes, tunnels) | Where port workers live; residential variety (see Neighborhood's 10 house styles, adapted to Mars: pressurised, buried, regolith-bermed) | Residential Officer role in station governance implies housing | L |
| Clinic / medical | Healing, YOM-style relief if Jaron accepts that later canon | | M |
| Bank / exchange (marks to credits) | "Every world has its own currency; credits exchanged at ports" [D] | 4 marks = 1 credit exists in code | M |
| Admin / assembly / courthouse | Governance hierarchy exists on paper (Governor, Ministers, Assembly, Judicial) | even a neutral hub needs a place for votes | M |
| Regolith depot yard and compactor works | Digging decisions 10/1: dump zones, compactor, sell by the tonne | | M |
| Quarry (the dig field) | Marked dump zones near the port; machines (see VH1) | | M |
| Shuttle / rail platform | Public transport that is fixed (timed, scheduled) [D] | | M |
| Black market back-alley | Bible: black market 10 to 30% of trade; every faction market has a supplier boss | even the neutral hub has a quiet one | S |
| Outer outposts: relay, weather station, radiation shelter, survey camps | Real-world Mars infrastructure look | | M |
| Valles Marineris rim viewpoint, cable lift, canyon base camp | landmark | | M |
| Olympus Mons base camp | landmark | | M |

### 2.3 What each faction home needs (PROPOSED layout; bible only gives faction edge and constraint)

For every home world the minimum set: **landing port**, **capital city**, **governance hall** (planet: Governor, Ministers, Assembly,
Judicial Branch, advisory committees), **military or security post**, **market**, **shipyard**, **black market**, **resource
site tied to the faction edge**, **landmark**, **hazard site**, **residential district**, **orbital station** and **a wreck or ruin**.

| Faction home | Port | Capital / city | Key faction buildings (from the edge) | Landmark / ruin / hazard | Existing art to reuse |
|---|---|---|---|---|---|
| **Fortis** | Fortis Outpost North Pad [FG][UE]; Civil Terminal | walled capital: gate with twin towers, perimeter walls 6 m wide x 5 m tall with buttresses, corner watchtowers 9.6 m with searchlights, armored buildings 8 x 8 x 6.5 m | barracks, armory, fleet command, logistics yard (visible convoys: "highly visible logistics trails"), gantry crane, fuel depot, gunship apron, checkpoint | Pyrrhus Bastion (volcanic perimeter), Obsidian Forge Line, Caldera 7 survey, Abandoned Relay | [UE] walls, gate, tower, building, crates, barriers, fuel drums, antennas, gantry crane, dev apron, **walkable gunship** |
| **Technos Prime** | Diplomatic Harbor / Civil Quay (Halcyon) | glass and composite city, domes, tall light structures | research labs, scanning arrays, diplomatic embassy ring, hacking and spoof shops (illegal), restricted-AI-core vault | Drowned City analogue, signal observatory (Mirrorglass) | none |
| **Wanderhome** | Public Mooring / Fleet Anchorage | no ground city: a fleet of ships and platforms, a market deck, a council hull | barter exchange, route-map room, modular ship shed (fits "modular ship designs"), gray-market stalls | the Shattered Arc ring mine nearby | none |
| **Mystara** | a small pilgrim landing | ruin-city of sealed halls and obelisks | anomaly lab, relic vault, sealed sites (illegal to enter), slow workshop (limited heavy industry) | Drowned City, Caldera 7 exotic-matter vents, standing-stone fields | none |
| **Greenhaven** | Garden harbour | domed forest city, living-hull grow-yards | bio-repair clinic, gene bank, hull-grow bay, morale park, seed vault; weak industry (small yards) | great trees, river delta, "gene contraband" sites | Neighborhood house styles (cottage, farmhouse) for residential |
| **Ironclad** | Foundry Deep Core, Surface Claim strip | smelter city, gantries over pits, chimney skyline | shipyard (fits "shipyard construction"), smelters, ore sorting, union hall (strikes), dormitories | open pits, Great-Crack-style fissures, protected excavation sites (illegal) | Neighborhood civic blocks, Fortis crane |
| **Corsair's Refuge** | hidden dock behind a wreck | scavenged station inside a hollow rock | cloak workshop, transponder swap shop, smuggler market, cartel boss hall (one supplier boss per other faction's black market, plus an internal operations boss) | Typhon-style crash site, fuel cache | none |

### 2.4 Landmarks, ruins and hazard sites to scatter (from builds and bible)

Drowned City (flooded foundations, crystal), Shattered Arc ring mine, Great Crack fissure field, Caldera 7 (unstable exotic
matter), Abandoned Relay Station (pre-war), Wreck of the Typhon (crashed survey vessel), Mirror observatory, derelict cargo
modules, sealed relic sites, ancient-civilisation sites (older concept: "ancient civilizations, alien species"), crater
survey beacons, abandoned custodian relay depots, storm shadow corridor marker.

### 2.5 Station types the bible lists (none exist) - see section 3.3 for the structure kit

Trade hub, military outpost, research facility, agricultural centre, repair yard, cultural landmark, smuggler den. Each owner
controls: **access rules, fees (0 to 20%), security posture (patrol budget), black-market pressure (healthy 10 to 30%)**. Those
four dials must be visible on the walls: access signs, fee boards, patrol density, back-room traffic.

---

## 3. Ships, vehicles, stations and structures

### 3.1 The bible's ship classes, and what exists

Bible list (v2.9 and v2.7): "Ships are assets with ownership records, upkeep costs, and inherent risk." "All ships follow
faction-linked design philosophies but can be captured, stolen, or traded." Crew numbers in the bible are NOT a limit (Jaron
9/30: "No crew cap - the 3-5 in the bible is not a limit").

| Class (bible) | Bible crew | Bible description | In The Cosmos | Size |
|---|---|---|---|---|
| **Scout** | 1 | "Fast, minimal armament, ideal for reconnaissance" | **partial**: Wayfarer-class courier exists (24 m, 5 stations, def and exterior done), not for sale, no price, not parked on pad 03 | S to polish |
| **Fighter** | 1 to 2 | "Agile combat vessel" | none (only the drones: ducted quad-rotors with twin cannon) | M |
| **Merchant** | 1 to 3 | "Cargo hauler with modest defenses" | **done (large)**: Drayman hauler 52 m. No small merchant. | M for small and mid |
| **Research Vessel** | 2 to 4 | "Scanning arrays, anomaly detection" | none | M |
| **Mobile Base** | 3 to 5 | "Long-range operations platform" | **closest**: MSV Meridian (a 49 m gunship with bunks, galley, medbay); decide whether Meridian IS the mobile base or a gunship | decision |
| **Mining Rig** | 3 to 5 | "Industrial extraction vessel" | none (only the hand excavator bucket as a tool) | M |
| **Raider Corvette** | 2 to 5 | "Pirate-optimized hit-and-run ship" | **done**: Shrike-class raider 36 m, 4 crew | S to give its own palette |

### 3.2 Every ship that exists today ([C], all with walkable interiors)

| Ship | Type id / registry | Size | Crew | Rooms (fore to aft) | Weapons | Other | Status |
|---|---|---|---|---|---|---|---|
| **MSV Meridian** | `meridian` / COS-MARS-VEH-0001 | 49 m long, 24.5 m wing, 46 t, 3 decks (upper +6 m, main +3 m, lower 0) | up to 6 (stats), 7 stations | Bridge (raked canopy, captain's dais, pilot, nav, comms, holo table); dorsal turret nest; main corridor (rails, conduits, extinguishers, first aid); medbay (2 beds, scanner arch); crew quarters A (4 bunks); crew quarters B / observation lounge (4.4 m window, binoculars); galley and mess; captain's cabin + head; workshop; turret ladder niche; engineering (reactor, coolant, pumps, racks); cargo bay (crates, drums, six-wheel rover, boarding ramp, stair + gantry); airlock (cycling doors, gangway); EVA locker (suits); ventral gunner pod with glass floor | twin chin cannons (captain, gimbal +/-28 deg), dorsal turret, ventral turret, practice targets, personal drones | cargo 24,000 kg; price 18,000 cr; shields; power split 100 units | **done** |
| **Shrike raider** | `raider` / COS-MARS-VEH-0020 | 36 m long, 18 m wing | 4 | Cockpit, main corridor, crew quarters + mess, airlock + gangway, armoury, ladder niche, dorsal turret, engine room (reactor), cargo hold, stern ramp | nose guns, dorsal turret, 3 escort drones; shield 240, armor 0.22; cruise 52 m/s | cargo 7,000 kg; 2,400 cr; named hulls (Cinder Hawk, Dust Wolf, Red Lantern, Bad Penny, Salt Magpie, Long Odds, Quiet Knife, Gallow Jack); four crew faces from 7 Loft people with helmets | **done** (palette is Meridian-like; Grok job 8 open) |
| **Drayman hauler** | `hauler` / COS-MARS-VEH-0070 | 52 m x 11 m wide (envelope 17.4 x 8.5 x 53.7), 4.6 m under gantry | 5 | Flight deck, corridor, crew berth (4 bunks), mess, airlock, cargo control (load plan board), supplies, engine room, cargo hold (six rover berths, tie-down rails, gantry, wide stern vehicle ramp) | chin gun only; cruise 31 m/s | cargo capacity per `HAULER_CARGO_KG`; shipyard price per stats | **done** |
| **Wayfarer courier** | `courier` / COS-MARS-VEH-0060 | 24 m, 9.2 x 6.5 x 24 envelope, 18 t | 5 | Bridge, passage, berth (2 bunks), mess, airlock, machinery, hold | one main gun | cargo 3,500 kg; cruise 38 m/s | **partial**: def + exterior, no price, not for sale |
| **Hostile drone / escort drone** | in `guns.js`, `escorts.js` | ducted quad-rotor, twin cannon | 0 | none | 12 damage bolts | bounty 25 cr; escorts fly formation | done |
| **Survey rover** | vehicle `survey` | 940 kg, 6 wheels, 4 seats, 8 m/s | 4 | open cab | none | 2,400 marks; one in every Meridian hold; berths in Drayman | **done** |
| **Derelict cargo module (Phobos)** | prop | pod with dogged door, broken hazard stripe, scorch, blinking lamp | n/a | not enterable | | 1.8 t salvage, 150 cr | partial (plain model) |
| **Abandoned raider hull (Deimos)** | prop/ship | a Shrike, claimable | | | | | done |

Ship systems already in every hull: seats grant stations, power split across engines/guns/shields, ramp must close before
lift, landing gear springs, airlock cycle, ship-local walking frame, hired crew AI, raiders that can be disabled and claimed.

### 3.3 Every ship and vehicle still needed (PROPOSED unless a source is shown)

**Bible classes not yet built** (each also needs faction variants because "all ships follow faction-linked design philosophies"):

| Ship | Faction look (see section 4) | Interior rooms it needs | Weapons | Size |
|---|---|---|---|---|
| Scout (finish Wayfarer; add Utopian light scout) | Utopian: light hull, big sensor mast; Nomad: modular | cockpit, one-bunk cabin, tiny hold, airlock hatch | 1 light gun | S |
| Fighter / Interceptor | Empire: armored wedge; Pirate: stripped | cockpit (1 to 2 seats), avionics bay, no hold | 2 to 4 fixed guns | M |
| Merchant small (1 to 3) and mid | Nomad modular; Miner bulk; Eco grown | cockpit, cabin, galley, hold, ramp | 1 gun | M |
| Research Vessel (2 to 4) | Utopian white; Mystara glyph-lit | bridge, **lab**, **sensor deck**, sample vault, cabins | none or point-defense | M |
| Mobile Base (3 to 5) | Nomad ark; Meridian candidate | many cabins, workshop, medbay, hangar bay | medium | L |
| Mining Rig (3 to 5) | Miner: gantry, arms, ore bay | cockpit, ore processing, refinery nook, crew bunks, drill bay | drills as tools | M |
| Raider variants | Pirate: scavenged mixed plates, cloak emitter | as Shrike | | S to M |
| **Eco living-hull ships** (bible: "living hull technology") | Greenhaven | organic ribs, hull-grow bay | | M |
| **Capital ship / carrier / station-ship** (older concept: "fleet capital ships") | Empire first | multi-deck, hangar, bridge, brig, barracks | large | L |
| **Dropship / gunship** (Unreal walkable gunship, 14 m: hollow interior, measured deck, cockpit, cargo, ramp and door on real pivots, red trim, raised FORTIS 01 marking) | Fortis | as built in Unreal | | M (rebuild in three.js) |
| **Public transport**: shuttle (pad 02 waits for one), ferry, line carrier. Full Game: 3 carriers on a 7-stop route, seats, door, ramp. Jaron: "fix it (flies off at spawn, no timer/schedule)" [D] | civil | seat rows, door, ramp, stop display | none | M |
| **Convoy ships** (bible: "automated trade convoys", Rebuild Credit for escorts) | by owner | cargo only | escorts | M |
| **Patrol drones, hunter ships, bounty hunters** (bible: Heat triggers "bounty hunters tracking offenders") | Custodian grey / faction | | | M |
| **Custodian carriers and sovereign patrol** (bible: "custodian fleets") | neutral grey | | | M |
| Relief / YOM ships (Full Game later canon [V3], "YOM relief ships outside the perimeter"); NOT in the bibles | white and orange | clinic, supply hold | none | M, only if Jaron accepts |
| **Wrecks and derelicts** (bible: salvage; Rebuild Credit: repair) | any | burnt, torn interiors | | M (kit) |

**Ground and port vehicles** (decisions 10/1: digging machine and hauler truck, compactor, dump zones, matter beacon late):

| Vehicle | Source | Status | Size |
|---|---|---|---|
| Survey rover | [C] | done | done |
| **Digging machine** (excavator, 48 t hopper) | [D] "full warning; drive and dump" | **none** (the bucket is a tool, no machine) | L |
| **Hauler truck** | [D] | none | M |
| **Compactor** (dirt to blocks) | [D] | none | M |
| Matter beacon (late game, dirt to cargo hold) | [D] | none | S |
| Powered hauling cart | [C] rated 400 kgf, 1,054 kg on Mars, "no cart vehicle model yet" | none | S |
| Fuel bowser, forklift, tug, baggage cart, passenger bus, crane truck | PROPOSED (port realism) | none | M together |
| Convoy trucks and patrol rovers | bible "physical convoys", escorts | none | M |
| Tower elevator | [C] | done | done |
| Gantry crane | [UE] geometry only | none in Cosmos | S |

### 3.4 Stations and structures (none exist)

| Structure | Source | What it needs | Size |
|---|---|---|---|
| **Station kit** (docking ring, spokes, hab ring, market ring, corridors, airlocks, windows, hangars) | [B] "Stations: Power Nodes" | one modular kit so every station is built from it, with spin or deck gravity decision | L |
| **Neutral hub station over Mars** | [B] neutral hub per system | PROPOSED: orbital hub at 400 km | L |
| Faction stations (trade, military, research, agri, repair yard, cultural, smuggler den) | [B] | built from the kit with faction style | M each |
| Relay depots, beacons, comm masts | Custodian "relay depots" [V3]; bible COMMS FALL needs comm rigs | masts and dishes visible | S |
| Docking physics | bible "Fly -> dock" | Cosmos has pad landing only; no clamp docking | M |
| Drilling rigs, refineries, smelters, silos, domes, greenhouses, habitats | industrial and Eco edges | ground structures | M each |
| Checkpoints, barriers, closed docks, propaganda screens | [V3] only, but custodian stages make them necessary | see 6.4 | M |
| Public-transport platforms and masts (Veldora passenger mast, Dunewind berth) | [FG] | | S each |

---

## 4. Factions and how their places should LOOK

The bibles give faction mechanics only. **Visual identity below is PROPOSED**, built from three sources: the Unreal Fortis art
(real, Jaron saw it), Full Game's faction colours (placeholders, but he saw them), and the edge and constraint of each faction.
Builders use this so a place looks like who owns it.

| Faction (home) | Architecture | Colour (Full Game value where it exists) | Materials and light | Uniforms and people | Signage |
|---|---|---|---|---|---|
| **Militaristic Empire (Fortis)** [UE built] | Heavy, battered walls, buttresses, crenellated parapets, twin-tower gates, trussed watchtowers with searchlights, boxy armored buildings with recessed doors, vents, roof antennas. Straight lines, clear aprons and fields of fire. | Steel grey with **red** trim and hazard rails (0xd32f2f). Red warning lights. | dark steel, concrete, hazard stripe paint, raised stencil marks ("FORTIS 01") | uniform armor, helmets, rank bars, gunmetal and red | numbered, stencil, serious |
| **High-Tech Utopians (Technos Prime)** PROPOSED | Glass, white composite, thin spans, domes, light tubes; lighter structures (matches "fragile armor") | white and **blue** (Halcyon 0x42a5f5) | glass, gloss white, soft light, holo panels | clean tunics, visors, subtle tech jewelry | clean sans-serif, holo signs |
| **Space Nomads (Wanderhome)** PROPOSED | Patchwork module stacks, tents and awnings, rope and cable, mismatched docked ships | **teal** (Kindred 0x26a69a) plus bright fabric accents | canvas, patched hull, lanterns, string lights | layered scarves, tools on belts, mixed styles | hand-painted, route marks, trade chalk |
| **Mystical Researchers (Mystara)** PROPOSED | Obelisks, arches, crystal growths, sealed round doors, instruments in ruins | **violet and gold** (Veil 0x8e24aa was a placeholder) | stone, crystal, glyph light, mist | robes, lenses, field kits | glyphs, symbol rings |
| **Eco-Guardians (Greenhaven)** PROPOSED | Grown and wooden forms, domes of leaf and vine, living hull ribs, gardens | **green** | wood, bio-ceramic, moss, warm light | natural fabrics, green sashes, medic kit | leaf marks, soft painted |
| **Industrial Miners (Ironclad)** PROPOSED | Gantries, chimneys, pit heads, smelters, dormitory blocks, conveyor lines | **amber** (Meridian 0xffb300) and steel (Registry 0x90a4ae) | rust steel, sparks, work lights, soot | hard hats, coveralls, hi-vis | stencil numbers, bold arrows |
| **Galactic Pirates (Corsair's Refuge)** PROPOSED | Scavenged plates, welded wrecks, hollow rock, crooked antennas, graffiti | mismatched, with **toxic green** accents (Freeport 0x7cb342) and red | patched metal, dim bulbs, neon scraps | mixed salvage clothing, scarves, stolen badges | tags, stolen transponder plates on walls |
| **Neutral hub (Marineris, Mars)** [C built] | Practical civil-industrial: concrete apron, ribbed depot, awnings, tower, lit signs | concrete grey, dust red-orange, yellow safety paint (amber stripes), cyan pad lamps | PBR metal shared with ships | port workers in Loft people looks | "MARINERIS PORT", pad numbers |
| **Custodians** (bible: NPC governance, stages Observation to Quarantine) PROPOSED | Checkpoints, barriers, patrol drones, relay depots, enforcement yards; neutral and grey so no human faction owns the look | neutral grey with a single stage colour | robotic, calm | none (robots) | stage banner and Stability Index |
| **YOM** ([V3] only) | Relief stations, mobile clinics, rebuild depots | white and warm orange | soft light | robot relief crews | clear, friendly |

Faction relations that should show in places (bible diplomatic graph): Utopians with Researchers and against Pirates; Empire with
Miners and against Eco-Guardians; Eco-Guardians with Nomads; Researchers against Miners; Nomads and Pirates opportunistic.
Allied ports share a visual cue (a pennant or joint sign); rivals show closed access or patrol notices.

Ethos drift (bible axes: Order vs Chaos, Altruism vs Extraction) lets a faction's look change over time ("optional visuals").
Every faction style should therefore have an order-leaning and a chaos-leaning variant: tidy vs patched, bright vs dim.

---

## 5. Props and small details by place type

Check marks mean the prop exists in The Cosmos today. Plain = not built. Items from the Meridian and the port are real
construction (done). This list is the "all the little small details" Jaron asked for.

### 5.1 Port / landing field
Done: pad numbers and markings, taxi lanes, tyre tracks, oil stains, expansion joints, kerbs, floodlight masts, drain covers,
tie-down rings, fuel farm tanks, container stacks, lit sign, depot racks and cases, pallet lift, rooftop fans, market awnings,
price displays, trader goods (ration trays, tins, coffee, valves, copper, circuit boards, bottles, drums, fabric, field kit),
elevator, radar and beacon mast.
Needed: windsock, wind and dust instruments (work), fire truck, emergency tender, ground power carts, cable reels, chocks, cones,
barriers, fuel hoses, passenger stairs, baggage carts, waiting benches, shade shelters, vending machine, bulletin board, route
timetable board, lost-and-found, security gate and scanner, customs desk, lights that change at dusk, trash bins and bags, antenna
farm, solar farm, water tank, regolith stockpile, weigh scale, notice posters, stray crates, parked rover rows, hangar.

### 5.2 City / town (all worlds)
Needed: streets with kerbs, lamps, benches, trees or planters (Eco), plazas, fountains or water points (Mars scarcity), market
stalls, shops with real counters, doors with bells, windows with curtains, awnings, chimneys and vents, gutters, balconies,
porches (ten house styles from Neighborhood: ranch, cape, colonial, Victorian, modern, bungalow, townhouse, cottage, split-level,
farmhouse, adapted per world), laundry lines, vehicle parking, bus stops, noticeboards, wall posters, flags and pennants, public
terminals, clinic, school, bar, canteen, warehouse, workshop, repair shop, chandlery, temple or shrine (Mystara), garden plots,
street numbers, power poles and cable runs, water mains, drains, graffiti (Pirates), propaganda screens (Empire, Custodian), play
areas (Jaron has four kids), clocks, bells.

### 5.3 Ship interior (Meridian is the reference)
Done: bunks, lockers, rugs, posters, photos, extinguishers, first-aid, crates, drums, rover, consoles, screens, handrails,
conduits, door frames, signs, galley, medbay beds and scanner, reactor, coolant tanks, pumps, racks, suit lockers, binoculars,
holo table, chairs with swivel, glass floor pod.
Needed for new ships and richer Meridian: mugs and plates, food in the galley, bedding with real folds, personal items per crew
(photo, boots, jacket), tools on the workshop wall, parts bins, spare panels, welding gear, medical supplies that work, fire
suppression, emergency lights, oxygen cylinders, suit hooks, hatch wheels, log book, maintenance tags, scuffs and wear, name
plates by seat, intercom, speaker grilles, plants (Eco), prayer or charm (Nomad), trophy shelf (Pirate), flag (Empire), decals.

### 5.4 Outpost / relay / depot
Needed: relay mast and dishes, solar array, battery shed, habitat module, airlock hood, fuel drums, generator, cable trench,
antenna, lamp post, sample lockers, weather mast, communications log, survey stakes, flags, hand tools, hopper, spare parts rack,
beds, kitchenette, radiation shelter, storm door, windbreak berm, tire tracks.

### 5.5 Wreck and derelict
Needed: scorch marks, torn plating with exposed frames, debris trail, dirt scar, heaped berms, open hatches, loose cable, emergency
light blinking, rescue beacon, scattered cargo, partial interior still walkable, human traces (bag, boots), salvage tags,
hazard tape, fuel leak, flame (for fresh crashes), sand drift (old ones). Wreck kit exists only for the opening's site (builders'
file); the Phobos derelict is a plain plated pod.

### 5.6 Mine / quarry / industrial
Needed: excavator, haul truck, ore hopper, conveyor, crusher, sorting sheds, smelter stacks, slag heaps, pit rim barriers, ramp
roads, water bowser, shoring, ladders, cage lift, ventilation shaft, ore carts, drill rigs, explosive stores, dormitory, mess hall,
mine office, safety boards ("days without accident"), strike posters (Miner constraint).

### 5.7 Station (space)
Needed: docking collars, clamps, umbilicals, airlocks with pressure lights, observation windows, corridor signage, shop rings,
residential decks, hydroponics, bunk rows, security desks, detention cells (bible: detention ladder 5 to 45 min), market boards,
fee boards (0 to 20%), access-rules signs, black-market back rooms, cargo lifts, cranes, hangars, solar wings, radiators, antenna
farms, shield emitters, repair gantries.

### 5.8 Black market / pirate den
Needed: hidden doors, crates with no markings, stolen transponder plates on the wall, cloak workshop, fence counter, intel
broker booth (intel items: freshness 72 h, proof quality, chain of custody), debt ledger, cartel boss office.

### 5.9 People (props that walk)
Done: 7 Loft MetaHuman people (Ada, Zuri, Jorge, Sunita, Walter, Aoi, Isaiah) with Idle, Walk, Sit; 15 port workers; raider crews with looks.
Needed: faction uniforms and outfits, more faces and bodies, crowds, children (Jaron decision: real characters everywhere),
animations for work (typing, repairing, loading, carrying, sleeping, eating, talking), pets and creatures (Eco: "living" things),
guards, patrols, street sellers.

### 5.10 Landscape dressing (every world)
Done on Phobos only: boulders, rocks, grooves. Mars: none beyond the port apron.
Needed: rocks and boulders with identity, dust drifts, ripples, tracks, dried channels, ice patches, cairns, craters with rims,
rubble fans, vegetation per world (Eco, Veldora), water bodies with real shore (Aethelgard seas), lava and glow (Pyrrhus), ring
shadows (Veldora), aurora, fog banks (Mystara). Every piece with a stable id and seed (Full Game's retired props were random and
unstable, which is why they were removed).

---

## 6. Systems the environment needs

### 6.1 Weather and day/night, per world

| System | Bible | In The Cosmos | Needed | Size |
|---|---|---|---|---|
| Planet rotation, sunrise, sunset, long shadows | none | **none**: Mars does not rotate, Sun is fixed at 38 deg elevation (mid-morning forever). The economy has a sol clock but the sky ignores it. | rotate planets or move the Sun by body day length; moons then really orbit | M |
| Mars dust storms (local and global), dust devils, haze | none | none: tower says "dust + wind sensor offline" | the weather officer and instruments become real | M |
| Visibility, fog, dust in lights, wind sound | none | fog fixed; no wind | | M |
| Cold and temperature (-153 to +20 C) | none | none | suit heating, ice on surfaces | S |
| Other worlds: Aethelgard sea storms, Pyrrhus ash storms, Dunewind sand storms, Cryos ice fog, Mystara mist, Veldora methane haze, Nimbara bands | [FG][PC] names only | none | per-world weather profile | M each, cheap once the engine exists |
| Seasons and tilt | none | tilt 25.19 stored | optional | S |

### 6.2 Hazards

| Hazard | Source | Status |
|---|---|---|
| Vacuum, suit oxygen, EVA | goods exist (oxygen cylinder), airlock cycles, EVA locker with suits | **none**: "You cannot leave the ship while it is off the ground", no oxygen use, no health. Big gap. | L |
| Radiation (Mars, solar storms) | proposed | none | M |
| Low gravity falls and hops | done on moons | done |
| Cave-ins, deep shaft traps | digging "known weak points" | partial |
| Ship damage, fire, breach, pressure loss | Full Game contract only | partial (hull, shield; no fire or breach) | L |
| Heat (re-entry, Pyrrhus, Obsidian) | Cosmos: "No heat model" | none | M |
| Hostile drones, raiders | done outside neutral airspace (1,500 m line) | done |
| Mines, AoE, ramming (and the storm corridor forbids them) | bible | none | M |
| Dangerous matter (exotic matter, Caldera 7) | [FG] | none | S |

### 6.3 Sovereignty Law: what a player must SEE (bible: Observation, Containment, Martial Governance, Reclamation, Quarantine)

The bible says transparency: a Region Stability Index, chaos signals, and the control stage are visible. Full Game later canon says
every major system must be witnessable without a menu. Visible cues per stage (PROPOSED):

| Stage | Visible in the place |
|---|---|
| Observation | patrol drones overhead, scanners on poles, calm banners |
| Containment | checkpoints at chokepoints, barrier gates, patrol swarms, capped-tax boards |
| Martial Governance | armed patrols, curfew signs, closed services, propaganda screens |
| Reclamation | custodian crews taking stations, seized-station banners, interim commanders |
| Quarantine | sealed docks, quarantine grids across lanes, closed markets |
| De-escalation | barriers removed, crews of players rebuilding (Rebuild Credit: repair stations, reopen routes, escort convoys, deliver scarce supplies, rebuild chains) |

Heat (separate meter, per actor): bounty hunters, undercover agents "like normal residents", focused patrols, docking denial.
Needs: custodian drone ships, checkpoint kit, banner kit, a Stability Index display in every port and on every comms console,
station seats (Governor, Station Commander, Security Chief, Trade Director) as real offices. Size L overall, split in 7.

### 6.4 Solar storm: COMMS FALL (bible)

Sun heat 0 to 1; alerts at 0.60 / 0.75 / 0.90 shown to leaders; trigger 0.95 sustained 6 to 18 h; long-range comms fail, markets
go local, low-power rigs survive, open conflict law with starter protections, exactly one Storm Shadow Corridor (no damage of any
kind), PSI stays safe; approach vector biases toward the worst contributing region.
Needs: sky (corona flares, auroras, red-shifted light), static on screens, dead relays, corridor markers, storm approach cue,
quiet period after. Status none. Size M (visuals) on top of server work.

### 6.5 Travel systems

| Part | Bible | In The Cosmos | Needed | Size |
|---|---|---|---|---|
| Atmosphere climb to a gate | none | done (lift pods to 120 km) | | done |
| Flip-and-burn courses; free flight with real gravity, orbit read-outs, fuel delta-v, time compression x5 to x500 | none | done | | done |
| **Interstellar / inter-system jump** | bible says "systems" and "sectors" but not how | **none** (nav sheet refuses) | jump drive (cost, charge time, "I want things to take a while"), gates or drive, arrival sequence, jump point visuals | L |
| Public transport on a schedule | Jaron: keep it, fix it | none (Full Game's flew off at spawn) | timetable, fares, seats, boards, stops | M |
| Convoys and trade lanes | bible | none | physical convoys, lane markers | M |
| Docking (clamp, request, approach authorisation) | bible "dock" | pad landing only | | M |
| Sector generator (expansion epochs 6 to 24 h, deterministic seed from epoch + faction + index) | bible | none | procedural region content | L |
| Wanderhome's route | "mobile" | none | a moving home on a schedule | M |
| PSI entry and exit | bible | none | pocket space transition | M |

### 6.6 Space environment objects (needed for the space between to feel real)

Asteroid fields and belts with ids and seeds (Full Game's retired random asteroids prove the opposite is wanted), debris, wrecks,
buoys, derelict ships, comets or ice rocks, gas giant (Nimbara-like, with fuel-skimming and banded air), ring system (Veldora),
other planets visible in the sky at correct size and angle, moons that actually orbit, stars (procedural dome exists), the
Milky Way (exists), meteor trails, other ships' lights and engine glows, traffic (convoys, patrols, transports). Size M each,
L for a belt with a real mining loop.

### 6.7 Underground and terrain

Caves have no drawn geometry. Ice caves, lava tubes, mines, bases dug into rock (Full Game amendment: "constructed underground
spaces"). Tunnels rooms, shoring, support. Also: a real Valles Marineris canyon wall, Olympus slopes, craters at all scales,
dune fields (Dunewind), seas with shore (Aethelgard), lava (Pyrrhus), ice plains (Cryos). Size L for caves, M per terrain
profile.

### 6.8 Rules the environment must display (bible numbers)

Fees 0 to 20% shown on station boards. Planet tax 0 to 15%. Neutral hub per system. Black market 10 to 30% of volume (below 10%
scarcity visible, above 30% unrest). Heat. Intel decay 72 h. Detention 5 to 45 min with detention cells and a cell block. Solo
ghost range 50 km. These are server rules; the environment only needs the places and boards to show them.

---

## 7. Recommended BUILD ORDER: parallel work packages

Each package is sized for ONE Sonnet builder in its own git worktree. "Owns" lists the folders and files that package alone writes,
so packages in the same wave cannot collide. "One-line touches" means a single added line in a shared registry (merge conflict
is trivial; builders rebase before pushing). Every package ends with the standing rule: walked and looked at, screenshots from
several angles, phone width, validator green, no clipping, nothing floating or half-sunk.

### 7.0 Shared files that must NOT be edited freely (collision list)

`src/ships/registry.js` (one line per ship), `src/ships/visuals.js` (one entry per ship), `src/space/spaceSpec.js` (DESTINATIONS),
`src/world/bodies.js` (one body per world), `src/main.js` (wiring blocks), `server/simulation.mjs` and `server/fleet.mjs`,
`src/economy/*` (catalog and shops), `test/validate.mjs` (one section per package). Package F1 below turns the first three into
one-line-per-entry lists and adds a `register()` convention so later packages touch only their own folder plus one list line.

### Wave 0 - foundations (do first; small; two can run side by side)

| ID | Package | Size | Owns | Depends on | Delivers |
|---|---|---|---|---|---|
| **F0** | Faction style sheet and prop vocabulary | S | `src/style/` (new) | none | Palettes, material presets, sign vocabulary, uniform palette per faction (section 4), ethos variants. A data file, no meshes. Everyone reads it. |
| **F1** | World registry and generic world plumbing | L | `src/worlds/registry.js`, `src/worlds/_kit/` (terrain profiles: rocky, ice, volcanic, ocean, desert, asteroid, gas; per-body sky; site plan to port builder; per-body weather hook), one-line changes in `world/bodies.js`, `space/spaceSpec.js`, `ships/registry.js` | none | A second PLANET can exist (frames already handle moons). Add a world by dropping `src/worlds/<name>/`. A dev entry `?body=<name>` to stand on any world without travel. Mars becomes the first entry. |
| **F2** | Time and sky: rotation, day/night, moons orbit | M | `src/space/clock*`, sky and sun files | F1 interface (not the whole package) | Planet day length, sunrise and sunset, long shadows, moons that orbit, sun heat visual hook. |
| **F3** | Jump drive and inter-system travel | L | `src/space/jump*`, nav sheet entries, server frame handoff | F1 | Travel to other systems (slow on purpose), jump visuals, arrival, "needs a jump drive" becomes true. Can be built after F1's interface lands; world packages can be built and tested without it. |

F0 and F1 start together. F2 and F3 follow F1's registry file. Everything else waits only on F0 and F1.

### Wave 1 - ship packs (all run in parallel; each owns `src/ships/<name>/`; one-line registry and visuals touches)

| ID | Package | Size | Owns | Delivers |
|---|---|---|---|---|
| **SH1** | Scout line: finish Wayfarer (price, pad 03, shipyard, palette) + Utopian light scout | S | `src/ships/courier/`, `src/ships/scout/` | bible Scout class real and buyable |
| **SH2** | Merchant line (freighter line): small, mid, and a Nomad modular merchant | M | `src/ships/merchant/` | bible Merchant class beyond the Drayman |
| **SH3** | Fighter line: fighter, interceptor, fighter wing launch from carriers | M | `src/ships/fighter/` | bible Fighter class; combat variety |
| **SH4** | Research vessel | M | `src/ships/research/` | lab, sensor deck, sample vault interior |
| **SH5** | Mining rig, prospector skiff, ore barge | M | `src/ships/mining/` | Miner ships |
| **SH6** | Mobile base / Nomad ark (and decide: is the Meridian this class) | L | `src/ships/ark/` | many cabins, workshop, medbay, hangar |
| **SH7** | Fortis line: walkable gunship (from Unreal), patrol corvette, dropship | M | `src/ships/fortis/` | Empire ships in red-and-steel |
| **SH8** | Transit line: shuttle (pad 02), ferry, line carrier | M | `src/ships/transit/` | public transport vehicles |
| **SH9** | Raider variants and the Shrike's own palette (Grok job 8) + Corsair interceptor | S to M | `src/ships/raider/` | pirate look, cloaking emitter prop |
| **SH10** | Eco living-hull ships and Researcher ships | M | `src/ships/living/` | grown hull, glyph-lit hull |
| **SH11** | Custodian carrier and patrol/hunter drones (and YOM relief ship if Jaron accepts) | M | `src/ships/custodian/` | sovereignty-stage ships |
| **SH12** | Capital ship and carrier | L | `src/ships/capital/` | multi-deck capital (later, not first) |
| **SH13** | Wrecks and derelicts kit (hulls broken open, walkable) | M | `src/ships/wrecks/` | reusable wreck generator used by worlds and Phobos |

Most ships can also be done as one pack per faction later; the table above is by class so builders share interior kits.

### Wave 1 - vehicle packs (parallel with ships; separate files)

| ID | Package | Size | Owns | Delivers |
|---|---|---|---|---|
| **VH1** | Digging machine, hauler truck, compactor (decision 10/1) | L (split in two Ms if needed) | `src/vehicles/dig/`, `src/vehicles/haul/` | drive, dump, compact; full warning; mass books balance |
| **VH2** | Port service vehicles: fuel bowser, forklift, tug, baggage cart, bus, crane truck | M | `src/vehicles/port/` | living port, moving traffic |
| **VH3** | Patrol rover, convoy trucks, powered cart | M | `src/vehicles/patrol/` | convoys and escorts |

### Wave 2 - worlds and sites (parallel after F0 + F1; each owns `src/worlds/<name>/` only)

Each world is split into **world** (terrain, sky, weather profile, landing port) and **city** (capital, outposts, landmarks).
A world builder can start the city after the world's landing zone exists; both can be given to one builder in sequence or two builders.

| ID | Package | Size | Owns | Depends | Delivers |
|---|---|---|---|---|---|
| **MR1** | Mars: crew hall, shipyard, Survey Office, weigh depot made real (plus pad 02 and 03 dressing, fuel trucks use) | M | `src/worlds/mars/port-buildings/` | F0 | Marineris Port finished |
| **MR2** | Marineris Town: habitats, clinic, bank, assembly, shuttle platform, back-alley | L | `src/worlds/mars/town/` | MR1 | neutral hub as a place to live |
| **MR3** | Mars wilds: Valles rim, Olympus base camp, polar ice, Hellas, outposts, Airy-0, real canyon walls | L | `src/worlds/mars/wilds/` | F1 | reasons to leave the port |
| **MR4** | Phobos and Deimos finish: real beacon and cargo models (Grok jobs 6 and 7), Deimos jobs, survey base | M | `src/space/` moon files | none | moons at Meridian detail |
| **WD-FORTIS** | Fortis world: terrain, sky, ash weather, landing port (gate, apron, gunship pad, hangars, checkpoint) | L | `src/worlds/fortis/` | F0, F1 | the Empire's front door |
| **CT-FORTIS** | Fortis capital and Bastion: walls, towers, barracks, armory, fleet command, logistics yard, Obsidian-style forge | L | `src/worlds/fortis/city/` | WD-FORTIS | walled military city (assets exist in Unreal) |
| **WD-TECHNOS** | Technos Prime world and Civil Quay port | L | `src/worlds/technos/` | F0, F1 | |
| **CT-TECHNOS** | Technos capital, embassy ring, labs, spoof shops | L | `src/worlds/technos/city/` | WD-TECHNOS | |
| **WD-WANDER** | Wanderhome fleet: ship-city, market deck, moving route | L | `src/worlds/wanderhome/` | F0, F1, SH6 | the mobile home |
| **WD-MYSTARA** | Mystara world, ruin city, anomaly sites | L | `src/worlds/mystara/` | F0, F1 | |
| **WD-GREEN** | Greenhaven world, domed forest city, living-hull yards | L | `src/worlds/greenhaven/` | F0, F1 | |
| **WD-IRON** | Ironclad world, pits, smelters, shipyard | L | `src/worlds/ironclad/` | F0, F1 | |
| **WD-CORSAIR** | Corsair's Refuge: hollow rock or wreck-built hideout, black market | L | `src/worlds/corsair/` | F0, F1 | |
| **WD-PSI** | Private Sanctuary Instance: pocket moon, vault, trophies, decor | M | `src/worlds/psi/` | F1 | |
| **WD-FREE** | Extra worlds Jaron already saw: Earth and Moon, Pyrrhus, Aethelgard, Cryos, Dunewind, Rustholm, Ironcore, Obsidian, Mirrorglass, Nimbara (gas giant skimming) | M each | `src/worlds/<name>/` | F1 | only if kept; Jaron's call per world |

Cities for Mystara, Greenhaven, Ironclad and Corsair follow the same pattern (CT-MYSTARA, CT-GREEN, CT-IRON, CT-CORSAIR), L each (M for Corsair).

### Wave 2 - stations and kits (parallel with worlds)

| ID | Package | Size | Owns | Delivers |
|---|---|---|---|---|
| **ST1** | Station kit (docking ring, corridors, hab ring, market ring, hangar, airlock, windows) | L | `src/stations/kit/` | one kit all stations share |
| **ST2** | Neutral hub station over Mars (400 km orbit) | M | `src/stations/mars-hub/` | first real station; docking |
| **ST3** | Docking system (request, approach, clamp, pressure, airlock, cargo route) | M | `src/stations/docking/` | "Fly -> dock" |
| **KT1** | Town kit: streets, house styles (10 from Neighborhood, adapted), shops, lamps, benches, signs | L | `src/kit/town/` | residential variety for every city |
| **KT2** | Industry kit: pits, smelters, gantries, conveyors, silos, rigs | M | `src/kit/industry/` | Ironclad, Fortis forge, Mars quarry |
| **KT3** | Outpost kit: relay mast, hab module, solar, shelters, beacons | M | `src/kit/outpost/` | scatter everywhere |
| **KT4** | People pack: faction outfits, new faces and bodies, crowds, work animations | L | `src/people/` | looks per faction; children |
| **KT5** | Landscape dressing kit: rocks, dunes, plants, ice, water with shore, lava | M | `src/kit/terrain/` | per-world ground dressing |
| **KT6** | Black market and pirate-den kit; propaganda and checkpoint kit | M | `src/kit/sovereignty/` | custodian and shadow-economy places |

KT packages are best run BEFORE or alongside the city packages that use them; the city builders can start with their own local copies and swap to the kit
when it lands.

### Wave 3 - systems (parallel; each owns its own folder; mostly need F1 and F2)

| ID | Package | Size | Owns | Delivers |
|---|---|---|---|---|
| **SY1** | Weather engine and Mars dust storms; per-world profiles | M | `src/weather/` | tower weather officer works; haze, drifts, wind |
| **SY2** | EVA and vacuum: oxygen use, suit, hatch to space, drift | L | `src/eva/` | leave an airborne or orbiting ship |
| **SY3** | Hazards: radiation, heat, breach, fire, cave-in | M | `src/hazards/` | danger beyond raiders |
| **SY4** | Sovereignty visuals: stage kits, patrol drones, Stability Index boards | M | `src/sovereignty/` | custodian stages visible (needs SH11, KT6) |
| **SY5** | Solar storm COMMS FALL visuals and storm shadow corridor | M | `src/storm/` | sky, static, dead relays, corridor markers |
| **SY6** | Sector and region generator (expansion epochs) | L | `src/sectors/` | procedural regions with ids and seeds |
| **SY7** | Public transport schedule and boards | M | `src/transit/` | timed, fixed, visible timetable (needs SH8) |
| **SY8** | Space objects: asteroid fields, debris, buoys, gas giant, rings, traffic | M to L | `src/space/objects/` | the space between worlds has things in it |
| **SY9** | Cave geometry and underground rooms | L | `src/world/caves/` | caves, tunnels, bases dug into rock |
| **SY10** | Convoys and trade lanes | M | `src/convoys/` | physical convoys, lane markers |

### 7.1 What can run at the same time without colliding

- **Wave 0**: F0 and F1 together. F2 and F3 start once F1's registry file is committed.
- **Wave 1 ships and vehicles**: all 13 ship packs and 3 vehicle packs at once (separate folders, one-line registry touches). Practically limited by usage, not by collisions. Suggest 3 to 4 at a time.
- **Wave 2 worlds**: any worlds at once after F1 (separate `src/worlds/<name>/`). Suggest starting with Fortis (assets exist) and Technos or Ironclad.
- **Kits** run alongside worlds. Systems run alongside everything once F1 and F2 are in.
- **Do not run together**: two packages that both edit `src/main.js` wiring, or F1 with any package that edits `space/spaceSpec.js` / `world/bodies.js`.

### 7.2 Suggested first run (what I would start Monday if usage allows)

1. F0 + F1 (the two seams). 2. In parallel: SH1, SH2, SH7, VH1 (ships and the digging machine, no world needed). 3. Right after F1:
WD-FORTIS (assets exist, strongest reference), MR1 (finish the port), KT3 (outpost kit). 4. Then ST1, SY1, F2, F3. 5. Then the other
six world homes, then cities, then systems that need them.

### 7.3 Package count

Wave 0: 4. Ships: 13. Vehicles: 3. Worlds: 15 plus cities (about 7). Stations and kits: 9. Systems: 10. About **60 packages**.
The minimum set to make the game "feel like a universe with places" (for the trailer shoot): F0, F1, F2, SH1, SH2, SH7, SH8,
VH1, MR1, MR2, MR4, WD-FORTIS, CT-FORTIS (or a Fortis outpost), ST1, ST2, KT3, KT4, SY1, SY5, SY8: about **20 packages**.

---

## 8. Honest gaps and decisions only Jaron can make (the bible is vague or silent)

1. **Where do the seven homes live?** One system or seven? The Cosmos nav says Fortis, Greenhaven, Ironclad are "another system"
   needing a jump drive. Full Game put Fortis on Earth. Pick: Sol with all homes, or one system per home.
2. **Is Mars the neutral hub of its own system or the neutral hub of the whole game?** Bible: one neutral hub per system.
3. **Are Wanderhome and Corsair's Refuge places or ships/stations?** Bible says Wanderhome is mobile; Corsair's Refuge is unspecified.
4. **Real scale for each home.** The proposals in 1.5 are mine, not his.
5. **Faction visual identity** (section 4) is proposed except Fortis (Unreal art he has seen) and the Mars neutral port.
6. **Which build ideas stay?** Earth and Moon, the nine Full Game bodies, the three PC bodies: keep, rename or drop? Their factions
   were placeholders.
7. **The Meridian's class.** Bible has Mobile Base (3 to 5 crew). Meridian is 49 m, 3 decks, up to 6 or 7 crew. Mobile Base, a gunship, or its own class?
8. **Jump drive**: what is it, what does it cost, how long does it take? Bible silent. Time-compression rule for it.
9. **Do planets rotate and moons orbit?** Today Mars is frozen and the Sun is fixed.
10. **Custodians and YOM** (and "Sovereign" visuals): the bibles have custodians; YOM is only in Full Game's v3.0.1. Visual work for YOM waits on his yes.
11. **EVA and oxygen**: needed for any real space or vacuum place. Today you cannot leave an airborne ship.
12. **Player-made places**: bible lets players own stations and planets (asset loop) and set fees; where do player stations physically go and what do they look like?
13. **Residential life**: how much "ordinary life" (houses, schools, play areas) belongs? Neighborhood suggests yes; bible is silent.
14. **Detention**: a place to serve detention (5 to 45 min) with market and chat still available; where and what does a cell block look like?
15. **PSI look**: one fixed look with player decoration, or several moons?

## 9. Sources read

`syl-survey/bible/SYL-Design-Bible-v2.9-latest.md` and `v2.7.md` (full), `SYL-VISION.md` (full), `BRIEF.md`,
`versions/SYL-Full-Game/` (CANON.md, bodies.js and bodies_expanded.js, factions.js, civilTransport.js, spaceProps.js, worldDetails.js,
items, ship parts, ROADMAP.md, VISION.md, canon codex v3.0.1, amendments, original concept, physical world contract),
`versions/SpaceYouLand/` Unreal authoring scripts and first-playable plan, `versions/SYL-Neighborhood/README.md`,
`versions/site-PCGames-syl/src/desktop/desktopBodies.js`, `AI-Shared/projects/syl/DECISIONS.md`, and in The Cosmos: README, docs
(WORLD-STATE, MARS-PORT-REVIEW, PROVENANCE), `src/ships/` (registry, meridian, raider, hauler, courier defs and specs, shipyard,
visuals), `src/space/spaceSpec.js`, `src/world/bodies.js`, `src/port/portSpec.js`, `src/vehicles/`, `src/economy/` catalog and shops,
`src/world-state/multiplayerView.js` (crew hall, pad grid). I did not open the opening's builders' file, and nothing from it is here.
Not verified live: the current site build; everything marked "done" is from code and the project's own READMEs, not a fresh walk.

## Idea (Jaron 10/5 8:04 PM, a joke - jokes are his scouts; NOT approved): "the bots' bonus"
Every $1,000 the trading twins make, they earn a session in The Cosmos as raiders/pirates and terrorize players "till they
feel satisfied." Fits the API-AI-leaders idea (10/3) and Easter eggs: a named raider ship (Darios / Satya) that shows up
after a milestone, with a ticker line ("Darios Twin earned shore leave"). Needs the pluggable seat-holder work first.
Jaron 10/5 8:09 PM - he will make it happen. Add-on: Grok clips its raids and posts them as videos on a Heartbeat TV channel
**"Payback"**. Shows: "Caught in 4K by PI (Pirate Intelligence)", "Revenge of the Grok", "Humans Being Humans".
(Grok already watches video; recording = the playtester's Playwright video path. Real-player clips need players' OK.)
