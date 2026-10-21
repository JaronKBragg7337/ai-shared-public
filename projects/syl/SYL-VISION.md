# SYL-VISION

A survey of Space You Land.  
Prepared for Jaron K. Bragg.  
September 30, 2026.

## What this document treats as truth

The main design is `bible/SYL-Design-Bible-v2.9-latest.md`.

The extra detail in v2.7 remains part of that design unless v2.9 changes it. This includes the sun-heat formula, storm corridor, storm direction, rebellion window, pirate cartel, companion personalities, and launch materials.

There is also important design inside `SYL-Full-Game`. It contains a locked v3.0.1 Universe Codex, four accepted amendments, an original-concept archive, and detailed world and server plans.

Those documents add ideas worth preserving. They also claim a different canon order from this survey brief. This document keeps them visible. It does not silently let them replace v2.9.

“Built” below means there is supporting code in this copy.

“Recorded” means a project log describes a result. That is useful evidence, but it is not a fresh test.

“Planned” means the idea exists in documents or unfinished code. It is not yet a working game system.

### What I could verify

I inspected the supplied designs, gameplay source, configuration, asset authoring scripts, tests, manifests, and development records across all eight versions.

I ran the two browser projects’ existing checks without creating their usual dependency files. An in-memory loader supplied the bundled Three.js module and corrected Windows file paths. The test assertions remained unchanged.

- The Cosmos: **136 checks passed.**
- SYL-Full-Game: **155 checks passed.**

These checks support the specific mechanics they test. They do not prove a persistent multiplayer universe.

I did not run Unreal, inspect Blueprint graphs inside binary assets, reproduce the old editor sessions, or test these copies on Jaron’s phone. Some large Unreal assets were omitted from the survey copy. Kurearthis also lacks its generated real-terrain data.

I did not verify the current public website or its outside scripts. The website findings describe the supplied folders.

Credentials and keys are not reproduced here.

## 1. The game in one page

Space You Land is a place you inhabit.

You walk through your ship. You sit at a station to use it. You land somewhere that has a history. People need fuel, food, repairs, protection, and routes that stay open.

You can make a living without becoming a ruler.

You can mine. Haul cargo. Repair a station. Escort a convoy. Sell information. Explore a strange site. Run a market. Steal a ship. Betray a faction. Help your enemies because everyone needs the same broken route reopened.

Seven factions offer different lives.

- **Utopians** favor technology, scanning, hacking, and diplomacy.
- **The Empire** favors armor, fleets, and defense.
- **Nomads** favor mobility, routes, barter, and adaptable ships.
- **Researchers** favor anomalies, relics, and unusual technology.
- **Eco-Guardians** favor living systems, repair, and morale.
- **Miners** favor extraction, industry, and shipbuilding.
- **Pirates** favor stolen identities, smuggling, stealth, and fast raids.

Each strength comes with a cost. Each faction has its own forbidden trades.

Ships and stations are more than possessions. They cost something to operate. They can change hands. Their owners can control access and charge fees within limits.

Political power is temporary.

A governor needs support. A commander needs a functioning station. Elections, appointments, rebellion, betrayal, and coups can change who rules. A faction’s behavior can change its character over time.

The universe keeps running when people leave.

If a region is abandoned, custodians keep it alive. If people break it badly enough, custodians restrict access, take stations, and impose emergency control.

Humans earn control back by rebuilding.

Repairing infrastructure, delivering scarce supplies, reopening routes, escorting convoys, and restoring elections earn local Rebuild Credit. You cannot become the hero of one damaged region by grinding somewhere safe.

A quiet hauler can become a legitimate leader.

Harm also leaves a record. Repeated killings, blockades, broken treaties, market abuse, and exploits create Heat. Hunters, patrols, undercover agents, and closed docks respond to that record.

The sun responds to wider instability.

When the galaxy becomes too divided, inactive, or unbalanced, COMMS FALL storms break long-range coordination. Markets become local. Large powers lose some reach. Small crews get room to act.

One storm corridor remains safe from damage. Private sanctuaries remain safe too.

You can play alone with limited NPC help. You can join a real crew. Your companion helps you understand events, but cannot decide outcomes.

Payment buys personalization and support for the game. It never buys better weapons, secret information, immunity, or a larger share of the universe.

The server keeps the real record. AI can advise. It cannot rewrite history.

The promise is simple:

**Leadership is temporary. Stability is earned. Anyone can matter.**

## 2. Every version, one by one

### A. The Cosmos with the ship

Folder: `versions/the-cosmos-with-ship/`

**What it actually built**

This is the strongest physical foundation in the collection.

Mars exists at planetary scale. Its body data distinguishes its mean, equatorial, and polar dimensions. Walking uses local up and gravity toward the planet.

Positions use precise world coordinates. Drawing happens near the camera, where graphics hardware can handle small details.

The project can turn latitude, longitude, and altitude into a position and back again. It also checks which way east points. That matters because a world can look plausible while its coordinate system is mirrored.

Its terrain is a three-dimensional material field. A point can be solid or empty below the outer surface.

The field includes:

- Regolith.
- Duricrust.
- Basalt.
- Ore.
- Latitude-dependent ice.
- Deep material that cannot be dug.
- Procedural cave space.

The terrain is procedural. Its relief is calibrated against Mars-like heights and depths. This is not a downloaded map of every real Martian mountain and canyon.

The digging code changes the field. It creates material lots with IDs, estimated volume, mass, and material type. Dropping material creates a deposit.

The current source also draws local excavation geometry. The README’s statement that dug holes are invisible is out of date.

The code has a fine surface around edits. It also adjusts ground contact so the walker can descend into a hole. Tests cover repeated excavation and digging deeper than three meters.

This is still a limited excavation system. Natural caves are represented in the field, but there is no complete system for drawing and navigating all nearby cave walls and ceilings.

The material bookkeeping balances what was removed, carried, and deposited. The physical amount comes from sampling. It is not an exact mixed-material measurement.

A lot currently receives its dominant material. A cut through several layers does not yet preserve a full mixture.

The carry limit also has a distinctive rule. It converts an Earth weight allowance into a larger mass allowance on Mars. That accounts for lower weight. It does not yet account for bulk or the effort of starting and stopping a heavy load.

The debug layer is unusually valuable.

It provides:

- Named ground cells.
- A depth layer in the address.
- A marked origin.
- Stable asset IDs.
- Measured asset boxes.
- Nearby asset distances.
- Copyable location reports.
- Latitude, longitude, and altitude.
- Material and ground information.

These tools make a report such as “the door over there is wrong” into a place the builder can find.

**The MSV Meridian**

The Meridian is a walkable, three-deck ship. It is roughly 49 meters long.

Its layout uses measured rooms, doors, stairs, ladders, ramps, furniture, windows, and standing clearance.

It contains a bridge, captain’s position, navigation and communications stations, engineering, cargo bay, airlock, medbay, crew quarters, galley, workshop, captain’s cabin, and upper and lower gun positions.

Small details matter here.

There are bunks, lockers, rugs, posters, photographs, extinguishers, first-aid fittings, crates, drums, and a rover in the cargo bay. These make the ship feel occupied.

The rover is a prop. The beds, food, medical equipment, and workshop are not yet working service systems.

There are seven station seats:

- Captain.
- Pilot.
- Navigation.
- Communications.
- Engineering.
- Dorsal gunner.
- Ventral gunner.

Station actions are checked against the occupied seat. Standing near a console does not grant its role.

The captain can fly and use the main guns. The pilot can fly. Gunners use their own weapons.

Navigation samples actual nearby terrain. Its display shows ground shape, position, heading, contacts, and landmarks.

Engineering distributes power among engines, guns, and shields. Those settings affect behavior.

Communications has a log and beacon control. It is not yet a working network of relays and distant messages.

Walking inside the ship uses the ship’s own coordinate frame. The player stays with the moving hull.

Flight has assisted lift, cruise, landing support, spring-like landing legs, and limits tied to engine power. The ramp must close before departure.

The airlock has a timed cycle. It does not yet simulate air pressure.

Weapons fire moving projectiles. Projectiles inherit the ship’s movement. Hits create effects. Practice targets and attacking drones provide a local combat exercise. Shields take damage before the hull.

Sound is synthesized. Engine noise follows thrust. Doors, guns, and impacts have their own sounds.

**What is worth keeping**

Keep the planet-first world model.

Keep the coordinate rules, measured IDs, material field, excavation work, ground contact, and validator.

Keep the whole Meridian as an experience reference. Jaron’s response to it is strong evidence about the game he wants to inhabit.

Keep the ship’s measured layout, seat permissions, power allocation, real terrain display, moving interior, boarding ramp, landing behavior, room detail, sound, and combat exercise.

Keep the phone fixes:

- Remove overlapping faces that flicker.
- Keep visible rooms connected through open doors.
- Keep stairs and doors visible across room boundaries.
- Place consoles below the pilot’s view.
- Give gunners a clear view.
- Use shared display drawing for world screens and readable phone panels.

Keep the separation between game facts and the pictures or sounds that report them.

**What is unfinished or went wrong**

There is one planet, one ship, and one player.

There is no persistent save of the world, no server authority, and no multiplayer.

The ship cannot yet leave the atmosphere and travel to another planet. Its normal speeds are suited to local flight.

The hull is not a complete terrain-contact shape. The nose or a wing can pass through a hill even though the legs and keel land.

The outer airlock hatch is not yet a real opening through the hull. Leaving an airborne ship is blocked. There is no EVA.

Damage does not yet give the full loss and repair loop. The ship retains enough thrust to remain usable at extremely low hull health. Landing with the ramp closed allows free hull recovery.

That is useful for practice. It conflicts with a persistent economy where repair has a cost.

Excavation currently gathers edits into a bounded local mesh. As the edited area grows, detail can become coarser. A persistent planet needs separately managed terrain regions.

Terrain rebuilding can hitch. The README records an older rebuild cost of about 230 milliseconds. I did not make a fresh timing measurement.

The README records an iPhone playtest and fixes afterward. It also states that the fixes were checked in desktop phone emulation. That is not proof of current performance on a real phone.

The project explicitly says a failed transition between bodies is one reason this foundation exists. Its answer was to earn the second planet after the first planet works.

That lesson should survive the merge.

**Main evidence**

`README.md`, `src/world/`, `src/player/walker.js`, `src/core/registry.js`, `src/dev/`, `src/ship/`, and `test/`.

### B. SYL-Full-Game

Folder: `versions/SYL-Full-Game/`

**What it actually built**

This version has the broadest playable game loop.

You start near a damaged ship. You gather supplies. You repair and install parts. You load fuel. You launch, travel, land, discover places, and save progress.

Its nine bodies are:

- Earth.
- Moon.
- Rustholm.
- Aethelgard.
- Cryos.
- Pyrrhus.
- Veldora.
- Ironcore.
- Dunewind.

There are 24 named landing zones and 44 pickup IDs.

These bodies use compressed dimensions. Earth has a radius of 3,000 meters. The code is not a real-scale solar system despite some real-world reference data.

The game preserves continuous world position during ascent and descent. The sky changes with altitude. Flight can move between bodies without swapping to an unrelated level.

The player and ship use radial orientation. The ship also has a free-attitude space mode. Later fixes stopped gravity and collision from disappearing in that mode.

The starter ship has real readiness rules.

It needs the right core parts, sufficient power, working landing gear, repairs, and fuel. Its damaged engine begins below the working threshold.

Installed parts affect recorded mass, thrust, fuel, cargo capacity, armor, and power.

The builder supports installation, removal, repair, and refueling. Repairs consume alloy or wiring.

Crafting is connected to the inventory screen. Recipes cover refining ore, processing ice, making circuits and composites, and building advanced modules.

Some module descriptions promise shields, scanning, thermal control, and weapons. Much of that is data and statistics. It does not mean each promised behavior is working.

Inventory records item counts and can calculate mass. It does not yet enforce a complete carrying and cargo-transfer system.

The ship’s visual shape is more than stacked boxes. It has a connected hull profile, swept wings, canopy, tail, engine shapes, and flames.

It has a door, ramp, cockpit, and an interior camera view. This is not the Meridian’s complete walk-around interior. Boarding still changes mode through proximity. Some interior movement paths are unfinished.

There is public transport.

Three carriers run a seven-stop route. They dwell, depart, move continuously, arrive, and allow boarding and disembarking.

This lets someone travel without repairing or piloting a ship.

The carriers use scripted travel. Each client runs its own copies. Their position, passengers, schedule, and cargo are not persistent server truth.

Saving while riding is blocked. The save does not preserve an in-transit passenger journey.

Progress saves to the browser. It includes the player, ship parts, inventory, discoveries, faction standings, mode, and collected pickups.

There are manual saves, loads, discovery checkpoints, and a one-minute autosave.

The save format has a version field. It has no implemented migration process yet.

Multiplayer shows other players and ships using presence and broadcasts. It can smooth remote movement and report connection state.

Players still report their own state. The service is not deciding movement, damage, cargo, or ownership.

The included Node server serves files. It is not the universe server.

**A major change in the current copy**

The generated surface settlements, roads, trees, rocks, masts, landing-pad decorations, and matching colliders were deliberately removed.

The latest client keeps terrain, water, atmosphere, sky, ships, transports, and pickups.

This was an attempt to stop disposable scenery from becoming the foundation of the real game.

The old prop builders still exist. They include buildings, trees, rocks, crystals, ice spires, storage tanks, dishes, masts, banners, canopies, containers, and solar equipment.

Some old space-prop code also survives but is not connected to the active scene.

A retained builder is not proof that its objects currently appear in the world.

**What is worth keeping**

Keep the gather, repair, fuel, launch, travel, land, discover, and save loop.

Keep modular part definitions, readiness checks, crafting data, useful body and zone identities, and discovery rewards.

Keep public transport. It opens the game to passengers, haulers, and people who do not want to pilot.

Keep the responsive controls, closeable phone panels, sensitivity settings, chase-camera lessons, free space attitude, and connection feedback.

Keep the builder tools:

- Test supply kits.
- Ready-ship placement.
- Developer flight.
- Body and zone travel.
- Collider display.
- Scene inspection.
- The live tuning panel.
- Copyable tuning values.

The tuning panel lets Jaron adjust feel without spending another AI conversation on every small change.

Keep the original procedural prop and texture builders as an asset library. Their placement rules must be rebuilt around measured sites.

Keep the canon archive, provenance records, server contract, physical-world contract, and ordinary read-only CI.

Those documents contain much of the bridge between the working prototypes and the intended game.

**What is unfinished or went wrong**

The current client has surface shells. A shell cannot represent a tunnel, overhang, or underground room.

The planets are compressed. Scale was explicitly reopened in the August roadmap.

The faction registry contains Fortis and six substitute faction names. That is not the seven-faction bible design.

Faction standings are stored values. There is no working government, market, rebellion, or territorial simulation behind them.

Damage is mostly module health and simplified crash damage. It is not impact-based component failure.

The remove-and-install path loses a part’s damage condition. Reinstalling its inventory item gives it fresh health. A persistent game cannot use that path unchanged.

Fuel loading can consume a whole item while discarding the amount beyond tank capacity. That needs an explicit conservation rule.

Save loading accepts browser-created state. It cannot become the server’s trusted import path.

The client’s developer tools can create supplies and move objects. They need a separate test world or server permission before multiplayer.

The history records repeated control problems, camera confusion, fake-looking scenery, duplicated collision layouts, and map overlap. The clean-world reset addressed some of these issues by removing both scenery and its colliders together.

The reason for the next foundation is well documented. This was a useful playable V1, but its world and authority model did not meet the later physical and persistent design.

**Main evidence**

`src/main.js`, `src/ship/`, `src/inventory/`, `src/crafting/`, `src/world/`, `src/save/`, `src/multiplayer/`, `HANDOFF.md`, `ROADMAP.md`, and `docs/`.

### C. SpaceYouLand, the Unreal version

Folder: `versions/SpaceYouLand/`

**What it actually built**

This archive contains substantial original asset work for Fortis.

The authoring scripts create:

- Fortis walls and gate sections.
- Watchtowers and searchlights.
- A heavy building.
- Crates and barriers.
- Fuel drums.
- Antennas.
- A gantry crane.
- A development apron.
- A gunship.
- A later walkable gunship.
- Physical interaction panels.
- Local planet surfaces.
- A remote landing site.
- Neighboring curved surface tiles.
- Earth and Moon reference geometry.

The walkable gunship is approximately 14 meters long.

Its source distinguishes the exterior, interior, trim, glass, fasteners, ramp, door, and identity details.

It has a hollow interior, measured deck, cockpit, cargo space, ribs, seams, bolts, landing feet, and compound collision shapes.

The ramp and door have their own movement pivots. They were built to move around physical hardware.

The physical interaction panel has a steel housing, separate light lens, cable fitting, fasteners, and raised lettering for ramp and pilot actions.

That is a useful discovery. An interaction can live on the object itself instead of only in a floating screen prompt.

Development records describe first-person boarding, sitting, standing, attached movement, ramp control, cockpit and chase views, and flight restricted to the pilot seat.

I could verify the authoring geometry and read the records. I could not inspect the Blueprint graphs or rerun the complete behavior.

The project also attempted true-scale Earth and Moon.

It records Earth’s equatorial and polar dimensions and a Moon at lunar distance. These were reference geometry and body data. They were not a completed system of orbital flight and planetary gravity.

The surface work went through several approaches.

It tried a curved planetary cap, a smaller collision proxy, a flat local ground patch, and revised visible surfaces.

The remote-site scripts also preserve a useful idea. Neighboring surface pieces share a curved world and a mathematically matching boundary.

**What is worth keeping**

Keep the original Fortis visual language.

It has heavy construction, armored panels, practical hardware, red warning lights, industrial infrastructure, and a ship that looks assembled.

Keep the asset source, measured dimensions, export pipeline, separate moving parts, compound collision, raised identity, and physical interaction panel.

Keep the apron and operational clearance idea. A ship needs a clear working area, not scenery pressed against every side.

Keep the remote landing destination and connected surface corridor.

Keep the rule that you remain the same person while boarding and sitting. A seat changes what you can control.

Keep the diagnostic lessons:

- A visible ground surface and its collision must agree.
- A hidden collider can make a base appear to float.
- Query-only collision can still block a trace or sweep.
- Distant structures can disappear because of draw distance.
- A camera value can be overridden by a placed instance.
- Cabin collision can disturb a rigid ship if attached incorrectly.
- A denser mesh can make a broken surface worse.

**What is unfinished or went wrong**

The records show repeated ground bounce, fall-through, walk-through, spikes, invisible layers, and disagreement between the visible planet and local collision.

The archive also records a missing inherited C++ parent in an early Unreal setup. Later work used another player path.

The scripts contain old project-specific output paths. They cannot be rerun safely without first making the destination explicit.

The heavy building is a sealed exterior. Its shape does not prove a walkable interior.

The crane and service equipment are geometry. There is no verified lifting, fuel-transfer, or manufacturing loop.

The first-playable plan includes survival, collection, enemies, health, weapons, and a win or loss condition. I could not verify all of that in readable implementation.

The latest log still records open ground and ship-contact issues.

A likely reason to restart was the mismatch between a compelling local scene and an unstable planetary foundation. That is supported by the recorded failures. It is not evidence that Unreal itself cannot support the game.

**Main evidence**

`_authoring/`, `BUILDLOG.md`, `BUILDLOG_ARCHIVE.md`, `SESSION_HANDOFF.md`, `MEMORY.md`, the first-playable plan, and Unreal configuration.

### D. SYL-Neighborhood

Folder: `versions/SYL-Neighborhood/`

**What it actually built**

This is a compact browser walking experiment.

It builds a town-like area with a street grid, sidewalks, a central plaza, streetlights, trees, a civic building, and 28 houses.

There are ten house styles:

- Ranch.
- Cape.
- Colonial.
- Victorian.
- Modern.
- Bungalow.
- Townhouse.
- Cottage.
- Split-level.
- Farmhouse.

The houses include roofs, chimneys, gutters, trim, porches, windows, vents, and other small details.

Assets receive names and IDs. Inspection can show a grid, labels, collision boxes, and nearby information.

Desktop controls support looking, walking, and sprinting. Phone controls provide movement, looking, entry, and inspection.

Four houses are marked enterable.

Entry hides the outside scene and moves the player into one shared interior. Exiting returns the player beside the selected house.

That is a reusable interior demonstration. It is not four interiors physically contained in four houses.

The room has furnishings and walls. Its collision is much simpler than those furnishings and partitions suggest.

Trees are placed randomly. The layout has no persistent save.

The README describes commercial variety and crosswalks. I did not find corresponding implemented systems that justify treating those as completed features.

**What is worth keeping**

Keep the ordinary-life side of SYL.

People need homes, porches, public spaces, familiar streets, different architecture, and somewhere that feels inhabited.

Keep the house builders, trim details, civilian scale, plaza, streetlights, phone inspection, and visible IDs.

Keep this as a reference for residential station areas and surface neighborhoods.

**What is unfinished or went wrong**

House entry uses distance from the house rather than a fully modeled doorway path.

Exterior collision is mostly bounding boxes. Interior collision does not match every visible obstacle.

Random placement has no saved seed. An ID alone does not preserve an object’s location across reloads.

The street grid is not a measured network of parcels, doors, crossings, utilities, and vehicle routes.

No restart cause is recorded. It is best understood as a focused experiment. Its useful contribution is settlement character and inspection.

**Main evidence**

`index.html` and `README.md`.

### E. SYL-Testing-pvp

Folder: `versions/SYL-Testing-pvp/`

**What it actually built**

This is the clearest small server-owned combat experiment.

Despite the description of a Node server, the source uses Bun APIs. It is not directly runnable as plain Node without changes.

Players connect through WebSocket.

The server maintains player IDs, health, scores, respawns, several moving NPCs, and combat results.

It sends world snapshots 20 times per second.

Shots have a server cooldown. The server chooses a hit target and applies damage. A kill changes the score and causes a respawn.

The client supplies an arena, player movement, local obstacle collision, aiming, firing, reloads, recoil, weapon movement, hit feedback, health displays, a roster, scores, and latency.

It also has crouch, jump, sprint, pause, disconnect, and touch combat controls.

A tunnel helper supports temporary remote testing.

**What is worth keeping**

Keep the small command-and-snapshot pattern.

Keep server-owned health, hit outcomes, score, and respawn.

Keep connection state, latency, remote players, readable hit feedback, and phone combat controls.

Keep pause and input clearing. Losing mouse control should not leave a character moving or firing.

Keep the principle of proving shared combat in a small place before spreading it across a galaxy.

**What is unfinished or went wrong**

Clients still report movement. The server clamps map bounds but does not fully enforce movement speed or obstacle collision.

The shot origin is not fully tied to the player’s accepted position.

Shots do not correctly test the arena’s cover.

Ammo and reloads are mainly client rules. A modified client can bypass them while still respecting the server’s shot cooldown.

There is no durable account, faction, evidence, inventory, or world history.

State is lost when the server restarts.

No restart cause is documented. This is a useful combat test bed, not a failed attempt at the whole game.

Its lesson is precise: putting health on the server is necessary, but it does not make every combat input trustworthy.

**Main evidence**

Server and client JavaScript, page and style files, package metadata, and the tunnel helper.

### F. Kurearthis

Folder: `versions/Kurearthis/`

**What it actually built**

The one-line README understates this project.

It contains a C++ planetary foundation, terrain authoring tools, real-data tools, test harnesses, and detailed proof records.

Its world-origin manager moves the local origin as the player travels.

Its custom gravity work computes radial movement using precise coordinates and local collision.

Its player stays upright relative to the planet, moves along the local tangent, and uses a camera that follows that orientation.

The terrain manager keeps a grid of fixed local tiles around the player. Tiles are added and removed as the player moves.

This replaced a rejected approach where one collision patch followed the player. A ground patch that moves with you can pass a motion test while failing the feeling of a real place.

The terrain code can sample a generated elevation file and water mask. Outside that region it falls back to procedural terrain.

The tools fetch and convert real elevation data. Other tools create a water mask from OpenStreetMap data.

The recorded first real region was Delhi. The Yamuna received a flat water level while nearby land used the elevation data.

The generated terrain and water files are absent from this copy. They must be regenerated before that scene can reproduce the recorded result.

The records also show atmosphere work and a second body at lunar distance.

That proves coexistence in the recorded scene. It does not prove landing on the Moon, switching gravity between bodies, or orbital travel.

**What is worth keeping**

Keep the fixed-tile streaming lesson.

Keep precise global coordinates, nearby collision, radial up, separate gravity proofs, and controlled tests.

Keep the real-terrain import path, water-mask treatment, data provenance, and distinction between measured geography and generated terrain.

Keep objective region selection. The project proposed starting with large population centers rather than treating the creator’s own place as the center of the world.

Keep temporary landmarks as a testing method. A featureless real-scale landscape can make movement feel like nothing is happening.

Keep the audit and capture tools. They check actual scene contents rather than trusting a handoff.

Keep the world-model proposal.

It says population, supply, medicine, economy, and government should keep progressing even when nobody is nearby. Detailed physical simulation happens near players. Distant places still retain their state and history.

That is directly useful to SYL’s continuity requirement.

**What is unfinished or went wrong**

The records report poor results from a single Earth-sized collision mesh.

Moving the world origin did not make that huge collision shape reliable.

The project then reported force-unit and timing problems in its Chaos experiments. A custom swept integrator produced better measured falls and rest.

Those are project findings. They should not become a blanket claim about every Unreal setup.

The player’s horizontal movement is not fully swept against obstacles. Large step and snap allowances were used for planetary proofs. It is not yet a human-scale movement system for streets and ship interiors.

The tile layout has limits near the poles.

Recorded terrain performance improved from about 0.19 times real-time to about 0.7 times real-time. It still needed distance-based detail reduction.

There is no implemented store, ownership, economy, persistent server, or SYL faction system.

Some documents disagree about the immediate goal. An older start guide asks for a store, one item, an owned plot, and a placed object. The charter later requires planetary proofs first.

The build was explicitly paused. The record does not say it was discarded.

**Main evidence**

`Source/Kurearthis/`, `_authoring/`, `PLANETARY_PROOF.md`, `WORLD_MODEL.md`, `CHARTER.md`, build logs, and the asset manifest.

### G. site-games-syl

Folder: `versions/site-games-syl/`

**What it actually built**

This is a delivery copy of Full Game.

The supplied game source matches Full Game. The comparison found 44 identical non-vendor files.

The differences in the two HTML entry pages add website analytics and editor scripts.

Those outside scripts are not included here. Their behavior was not verified.

This folder inherits Full Game’s repair loop, travel, crafting, transports, local saves, presence multiplayer, and current bare-world state.

It does not contain a separate, more complete universe.

**What is worth keeping**

Keep the browser delivery path and working website integration reference.

Keep the distinction between source and deployed copy. A release should be traceable to a specific source revision.

Keep ordinary website navigation and device integration where they support the game.

**What is unfinished or went wrong**

Hand-copying files can make the website and source disagree.

The project history also warns that the test route and production route share the same browser save key. They are not safely isolated just because their URLs differ.

No separate restart cause is established. This is a shipping copy.

**Main evidence**

The file comparison, HTML entry pages, and matching `src/`.

### H. site-PCGames-syl

Folder: `versions/site-PCGames-syl/`

**What it actually built**

This is a separate legacy desktop experiment.

Its active entry loads `desktopMain.js`.

It changes planet sizes and distances. The desktop body scale is larger than the responsive version, but still compressed.

It adds three bodies:

- Nimbara, a storm giant.
- Obsidian, a dark volcanic world.
- Mirrorglass, an ice-like observatory world.

Together with the shared nine, that gives twelve body definitions.

It experiments with more varied terrain profiles, rings, stars, lighting, shadows, glow, and more detailed surface materials.

It includes three original GLB assets:

- Fortis gunship.
- Fortis habitat.
- Industrial prop.

Those files are present in this copy.

The loader supports reusable model loading and a visible fallback when loading fails.

This route uses its own browser save key.

Its gameplay is an older branch of the Full Game foundation. It does not contain all the responsive version’s later systems.

**What is worth keeping**

Keep its art studies.

Keep the storm giant, volcanic and mirror-world ideas as proposed destinations.

Keep its model-loading work, original asset source, material experiments, lighting, rings, and clear loading-failure signal.

Keep the separate save identity as a lesson in isolating experiments.

**What is unfinished or went wrong**

A fixed loaded ship model can look unchanged even when the underlying module state changes. That breaks the promise that ship assembly affects the physical ship.

A gas giant’s description does not make its underlying spherical collision behave like a gas giant.

The desktop route has different scale and presentation rules from the responsive game.

It is explicitly labeled on hold in the later documents. The accepted browser amendment rejects a separate PC product.

Its useful future role is an art and asset reference unless Jaron changes that direction.

**Main evidence**

`index.html`, `src/desktopMain.js`, `src/desktop/`, `assets/desktop/`, and the inherited game modules.

## 3. Discoveries outside the supplied v2 bibles

These are additions to preserve.

Some are working features. Some are experiments or lessons. Some appear in later design documents.

The bibles already call for ships, mining, stations, and rebuilding. The discoveries below often explain how those broad ideas become a place you can actually inhabit.

### Physical world and mining

1. **Start with the planet.** A local demo should not later require a different world underneath it. Cosmos and Kurearthis both learned this.

2. **Global precision and local detail can coexist.** Keep precise world positions. Draw and collide nearby.

3. **A real body needs a declared shape.** Mean radius, equatorial radius, polar radius, local up, longitude direction, and altitude cannot quietly mean different things.

4. **Geography needs provenance.** A generated Mars-like landscape and a measured Delhi landscape are different kinds of content. Both can be useful.

5. **The ground has an inside.** Caves, strata, deep boundaries, underground rooms, and deposits need a volume rather than one height per direction.

6. **Material moves through a chain.** Digging creates a lot. Carrying moves it. Dumping creates a pile. Later hauling and construction should continue that same history.

7. **Loose material occupies more space.** Cosmos already distinguishes dug solid volume from a looser deposit.

8. **Low gravity changes weight, but not every carrying cost.** Preserve the Mars carrying experiment. Add bulk and movement limits before treating it as complete.

9. **The tool must aim at the physical ground.** A shovel bite should follow the field even when the drawn surface is slightly behind.

10. **Show the actual cut and drop.** Cosmos uses measured bite and deposit markers.

11. **A dropped pile should clear the pit edge.** Otherwise the player can accidentally refill the place they are digging.

12. **Ground contact needs human-scale tolerance.** Small rest offsets and speed-aware checks prevent bouncing and skipping thin surfaces.

13. **Terrain work can be spread over time.** Coalescing nearby edits avoids rebuilding the same surface on every input.

14. **Fixed streamed land feels different from a following platform.** Kurearthis preserves both the rejected method and the better one.

15. **Water can need its own measured treatment.** A terrain sample alone did not correctly present the Yamuna.

16. **Real scale needs movement cues.** Landmarks, horizon, terrain variation, and displays help a player judge progress.

### Ship life

17. **The ship is a home with work areas.** The Meridian gives the bible’s crew idea bedrooms, food space, medical space, engineering, cargo, and private space.

18. **Seats grant station use.** This is already a working rule, not just a control label.

19. **The captain can fly and fight from one position.** The Meridian’s main guns preserve that particular imagined role.

20. **People walk in the moving ship’s frame.** This avoids leaving the player behind when the hull moves.

21. **The same measured plan can build rooms and walking rules.** Doors, stairs, ladders, furniture, and clearance should come from that plan.

22. **Stations can share real telemetry.** The world display and the enlarged phone display can report the same facts.

23. **A navigation display can survey real terrain.** It can support route planning and landing rather than act as a decorative radar.

24. **Power allocation creates crew work.** Engines, guns, and shields compete for a finite supply.

25. **Boarding equipment affects departure.** The ramp must be closed before lifting.

26. **Landing is a physical contact problem.** Legs, clearance, terrain slope, lift, and leveling need to agree.

27. **Projectile motion includes the firing ship’s motion.** Shots should not forget where their speed came from.

28. **Local targets and drones make ship systems immediately playable.** Preserve them as a training exercise.

29. **Small belongings matter.** Posters, photos, rugs, lockers, bunks, safety equipment, and cargo detail make the ship feel lived in.

30. **Sound can report machinery.** Thrust, doors, firing, impacts, and the deck hum already have a procedural sound foundation.

31. **A physical prompt can be part of the object.** Fortis panels use actual housings, lights, and raised lettering.

32. **Moving parts need real pivots.** A ramp or door should rotate around its hardware.

### Everyday life, travel, and progression

33. **You can earn the first launch.** Full Game’s damaged starter ship makes repair and fuel part of the opening.

34. **Travel can be a passenger activity.** Public transport allows participation without owning or flying a ship.

35. **A transport can be visible throughout its trip.** Keep this continuity while replacing client schedules with one shared schedule.

36. **Discovery can reward travel.** Full Game grants supplies and standing when a new zone is discovered.

37. **Refining connects raw materials to useful modules.** Preserve the ore, ice, circuit, composite, and advanced-part recipes.

38. **A residential place needs architectural variety.** Neighborhood’s ten house styles expand SYL beyond military pads.

39. **Public space matters.** Streets, sidewalks, a plaza, trees, and lamps belong beside factories and checkpoints.

40. **A shared interior is useful as a study.** Keep its furniture and room ideas. Replace the teleport arrangement when building real houses.

41. **New world names and sites are creative material.** Keep Full Game’s bodies, transit hubs, drowned-city idea, fissure field, and PC world studies in the content archive.

42. **A storm giant needs a different kind of destination.** Nimbara preserves the idea of a world that should not behave like ordinary solid ground.

### Tools, phones, and trust

43. **An address can include depth.** Cosmos’s named cells are more useful than a screenshot alone.

44. **An asset needs an identity independent of its appearance.** Changing a mesh must not change who owns the thing.

45. **Inspection should not change the world.** Reporting tools can read facts without becoming game cheats.

46. **Visible collision tools catch invisible walls.** Keep the box overlays and scene validation.

47. **Jaron needs direct feel controls.** The live tuner and copied settings reduce repeated AI tuning sessions.

48. **Phone controls should use the same game rules.** Touch changes input, not the meaning of thrust, walking, or repair.

49. **Phone panels need deliberate exits and context.** Close buttons, sensitivity, clear station controls, and unobstructed vision are functional requirements.

50. **Interior visibility follows doors and sightlines.** Drawing only the current room and its immediate neighbors caused missing walls and views.

51. **Flicker can come from overlapping faces.** Keep the geometric fix and depth checks.

52. **Real-phone testing remains necessary.** A narrow desktop window does not measure iPhone heat, frame rate, battery use, or audio behavior.

53. **Pausing and focus changes must clear held input.** Preserve the combat test’s handling of lost control.

54. **Small server proofs expose trust gaps.** The PvP test owns health but still trusts too much movement and firing input.

55. **Save isolation is part of release design.** A test URL can overwrite production progress if both use the same browser key.

56. **A failed asset load should be visible.** The desktop fallback is a useful diagnostic.

57. **Original procedural art is reusable source.** Keep the builders and material recipes, not only the exported meshes.

58. **Restart evidence should survive.** Rejected collision, camera, terrain, and control approaches prevent the next builder from repeating them.

### Later design additions

These are present in Full Game’s later canon documents. They are not working systems yet.

59. **One permanent browser game.** Phone and desktop use one product. Meaningful state is not removed merely because the device is a phone.

60. **Exact physical assemblies.** Components have joints, material, support, clearance, and system connections.

61. **Damage has a place and a cause.** Energy, angle, thickness, and material can determine failure, detachment, debris, and craters.

62. **Detached parts retain their history.** A broken engine remains the same owned thing with mass, motion, and salvage value.

63. **Sites come before roads.** Declare destinations, doorways, docks, parcels, and utilities. Connect them with one measured network.

64. **Consequences need a physical witness.** Shortage, ownership, quarantine, damage, and recovery must change something the player can encounter.

65. **Unwatched places keep running.** Distant simulation can be cheaper without erasing route, stock, population, or political history.

66. **YOM is a relief faction.** It heals, supplies, teaches, escorts, and rebuilds. It cannot become an enforcement faction.

67. **Rebuild Blueprints are public recovery knowledge.** Basic help stays available. Advanced local work can depend on local Rebuild Credit.

68. **Custodians can have bounded learned patterns.** Successful routes and tactics can inform later behavior within their mandate.

69. **Custodian decay and corruption can create stories.** This needs reconciliation with the v2 promise of neutral enforcement.

70. **Cognitive Frameworks grow from play.** Research, hauling, repair, governance, trade, and conflict can shape how a player learns and discovers.

71. **That learning is visible and regional.** The later design calls for sustained, varied action and a transparent progress display. Chat alone does not earn it.

### Older proposals to preserve without presenting as finished design

72. **Player-created factions.**

73. **Fleet and capital-ship command.**

74. **Crew morale, living conditions, and mutiny.**

75. **Combat, diplomacy, engineering, and navigation skill trees.**

76. **A Galactic Council.**

77. **Aliens, ancient civilizations, and their technology.**

78. **Procedural missions and deeper station manufacturing.**

79. **Faction extinction.** This conflicts with the protected faction shares and recovery laws.

80. **A real-world society discovered before spaceflight.** The Unreal records discuss real countries, companies, government, medicine, industry, hidden rockets, and an eventual space arc.

The last proposal is a possible change in the game’s opening and setting. The records do not establish it as the accepted replacement for SYL.

## 4. The merged feature map

For the merged game, every consequential fact has one owner: the server.

The client handles controls, prediction, drawing, sound, and readable displays. It receives the accepted result.

The following map includes the supplied bible features and their important details.

### Persistent universe, authority, and history

**Existing contribution:** Cosmos has precise local physics and IDs. Full Game has local save composition and a detailed authority plan. PvP owns a few combat outcomes on a small server.

**How far along:** Separate proofs. No version has the required persistent universe.

**Merged home:** One server-owned world record. Local simulation, durable storage, and an append-only event history. Clients cannot upload a save and declare it true.

State must survive logout, absence, crashes, and restarts. Corrections add records rather than erase history.

### The five play loops

**Personal:** Full Game supplies gathering, repair, crafting, flight, and discovery. Cosmos supplies walking, excavation, ship stations, and local combat.

**Faction:** Full Game stores standing values. The actual faction loop is unbuilt.

**Asset:** Full Game installs and repairs modules. Cosmos supplies the inhabited ship. Ownership transfer, theft, capture, upkeep, and station ownership remain unbuilt.

**Shadow:** No working contraband market, intel trade, bribe, or obligation system.

**Sanctuary:** No working PSI.

**Merged home:** Personal activity in the physical client. Consequences, assets, reputation, contracts, and sanctuary permissions on the server.

### The seven factions

Full Game’s substitute factions are content proposals, not completed bible factions. They must not be silently relabeled.

**Utopians, Technos Prime**

Keep scanning, hacking, diplomacy, and spoofing. Keep fragile armor and the restricted-core trade.

Cosmos’s scanner and Full Game’s sensor-module data are partial building blocks. Hacking, spoofing, and faction rules are unbuilt.

**Empire, Fortis**

Keep armor, fleet strength, and defense. Keep visible logistics and the lack of stealth. Keep forbidden ordnance and weapons smuggling.

Unreal supplies the strongest Fortis art. Full Game supplies armor and ship-part data. Cosmos supplies a usable armed crewed ship.

A functioning Empire is still unbuilt.

**Nomads, Wanderhome**

Keep mobile living, routes, modular ships, barter, and fragile political ties. Keep gray logistics and unlicensed routes.

The Meridian’s living spaces, Full Game’s builder, and civil transports help. Barter, mobile faction authority, and route licensing are unbuilt.

**Researchers, Mystara**

Keep anomalies, relics, unusual technology, low industry, and slow manufacturing. Keep forbidden relics and sealed-site trespass.

Crystal and exotic-material data provide seeds. No anomaly research or relic-access system is working.

**Eco-Guardians, Greenhaven**

Keep biological repair, morale, living hulls, and weak heavy production. Keep gene contraband and bioweapons.

Plants, water, medbay art, and material recipes are supporting references. Living hulls and biological systems are unbuilt.

**Miners, Ironclad**

Keep mining, metallurgy, industry, and shipyards. Keep strikes and fragile supplies. Keep protected excavation and sabotage tools.

Cosmos excavation and Full Game refining are the strongest contributions. Industrial production, labor, shipyards, and territorial mining law are unbuilt.

**Pirates, Corsair’s Refuge**

Keep cloaking, smuggling, stolen identities, fast attacks, rivalry, and unstable leadership. Keep escalating Heat.

Cosmos weapons and PvP combat help. Cloaks, identity theft, smuggling, cartel roles, and pirate law are unbuilt.

**Merged home:** Server-owned faction membership, benefits, restrictions, relationships, standing, and behavior. Their places, equipment, missions, and signs appear physically.

### Ships and crew capacity

The bible specifies:

- Scout: 1.
- Fighter: 1–2.
- Merchant: 1–3.
- Research vessel: 2–4.
- Mobile base: 3–5.
- Mining rig: 3–5.
- Raider corvette: 2–5.

**Existing contribution:** Full Game’s modular starter ship. Unreal’s walkable Fortis gunship. Cosmos’s larger Meridian with seven stations.

**How far along:** A few strong ship prototypes. No complete class roster or shared crew capacity system.

**Merged home:** Measured ship plans, server-owned parts and occupants, local walking, seat permissions, power, fuel, cargo, damage, and ownership.

The Meridian needs an approved place in this roster. Seven stations do not necessarily mean seven simultaneous crew.

### Asset ownership, loss, capture, and upkeep

**Existing contribution:** IDs, local modules, repairs, fuel, and hull damage.

**How far along:** Partial mechanics. No legal ownership or persistent capture.

**Merged home:** Server ownership and custody records. Physical locks, access, boarding, salvage, repair, insurance, and upkeep.

A stolen object keeps its identity and history.

### Stations

Trade, military, research, agriculture, repair, culture, and smuggler stations all remain required.

**Existing contribution:** Named landing zones, Fortis art, ship rooms, civilian house studies, and transport stops.

**How far along:** Location and asset studies. No fully working station economy or government.

**Merged home:** Reachable station plans tied to stock, services, access, ownership, staffing, and transport.

Keep docking fees within **0–20%**. Keep security and patrol spending. Keep black-market pressure within its intended band.

### Resources, manufacture, and cargo

**Existing contribution:** Cosmos material lots and deposits. Full Game items, mass, fuel, refining, crafting, and module recipes.

**How far along:** Two useful local systems. No shared chain from rock to cargo to production.

**Merged home:** One material and item model.

It must cover:

- Food, water, and fuel.
- Metals, composites, and electronics.
- Rare and experimental resources.
- Stolen goods, contraband, and forbidden materials.

Mining, loading, transfer, refining, repair, construction, and salvage must conserve amounts.

### Credits, markets, and economic limits

**Existing contribution:** Repairs and fuel consume local items. Crafting consumes inputs.

**How far along:** No real credit ledger, market, tax system, or production economy.

**Merged home:** Server-owned balances, stock, orders, and transfers.

Keep credit sources from missions, salvage, mining, bounties, and trade.

Keep sinks from repair, ammo, upkeep, docking, insurance, and taxes.

Keep storage limits, transaction limits, and Heat-related restrictions.

Planet taxes remain within **0–15%**. Each system needs at least one neutral hub.

### Planet and station government

**Existing contribution:** Design documents and visual places. Stored faction standing is not government.

**How far along:** Unbuilt.

**Merged home:** Server-owned offices, eligibility, votes, appointments, support, policy, terms, and removal.

Keep the planet hierarchy:

Governor, ministers, assembly, judges, and advisory committees.

Keep the station hierarchy:

Commander, operations, security, trade, and residential roles.

Keep achievements, approval, no-confidence actions, elections, and coups.

Policies must change access and services in the actual place.

### Diplomacy

**Existing contribution:** Faction relationship storage and written design.

**How far along:** No active treaties, wars, alliances, or embargoes.

**Merged home:** A server-owned relationship network with dated agreements and consequences.

Keep the initial relationships:

- Utopians with Researchers.
- Empire with Miners.
- Eco-Guardians with Nomads.
- Empire against Eco-Guardians.
- Utopians against Pirates.
- Researchers against Miners.
- Opportunistic Nomad and Pirate cooperation.

### Momentum and limits on dominant factions

**Existing contribution:** Design only.

**How far along:** Unbuilt.

**Merged home:** An hourly server calculation from accepted trade, combat, territory, infrastructure, approval, and risk.

Keep:

`effective contribution = raw contribution / active players^0.4`

Large factions should not win by headcount alone.

Leaders face upkeep, unrest, and stretched logistics. Smaller factions receive opportunities, discoveries, contracts, and easier access where the rules allow.

The definition of an active player and the zero-player case must be explicit.

### Expansion

**Existing contribution:** Multiple body and zone definitions. No actual expansion allocator.

**How far along:** Unbuilt.

**Merged home:** A reproducible server event every **6–24 hours**.

Keep the v2.7 population-based sector count and seed ingredients. Keep the **72-hour** conflict window and **0.22** trade-assist threshold.

Keep the stated shares:

- Every faction: at least **5%**.
- Leader: **28–45%**.
- Rival: **18–35%**.

Keep allied, neutral, and enemy weights of **0.6**, **1**, and **1.2**.

Keep costs in defense, unrest, piracy, and supply.

The allocation must reserve the floors before applying the remaining shares. The stated upper bounds cannot all apply at once.

### AI Director

**Existing contribution:** Detailed Full Game authority documents. No working Director.

**How far along:** A strong specification.

**Merged home:** An isolated proposal service.

It receives a redacted snapshot. It proposes a bounded action. The server checks permission, limits, timing, and state before accepting it.

Keep the permitted areas: taxes, fees, access, events, wars, embargoes, elections, coups, spawn rates, and missions.

AI cannot run raw code, change history, bypass limits, or write directly to the world.

Accepted actions are recorded. Replaying history uses the recorded action rather than asking AI to invent it again.

### Ethos Drift

**Existing contribution:** Design only.

**How far along:** Unbuilt.

**Merged home:** Server measurements along order versus chaos and altruism versus extraction.

Keep the leader influence of **15–30%** and broader behavior influence of **70–85%**.

Ethos can affect missions, enforcement, markets, reputation, diplomacy, and approved visual changes.

### Solo crew

**Existing contribution:** Meridian stations and power controls. No hired crew.

**How far along:** The ship has jobs, but no crew employment system.

**Merged home:** Server-owned crew roster and station orders.

With exactly one real player, NPC crew may work at **70–85%** effectiveness with delays.

With two or more real players, that NPC assistance is disabled under the supplied bible rule.

### Ghost Signature

**Existing contribution:** Scanner and combat building blocks.

**How far along:** Unbuilt.

**Merged home:** Server visibility rules.

The first hired captain’s bonus hides the ship beyond **50 kilometers**. Firing or hacking reveals it for **60–180 seconds**.

Close scans and direct sight still matter. This is not invisibility against a nearby observer.

### Solo integrity

**Existing contribution:** PvP has damage and kill events. Presence supplies limited movement information.

**How far along:** No complete evidence record or collusion detector.

**Merged home:** Server telemetry for damage, proximity, hostility, and kill attribution.

Keep captain walk-off penalties of **2**, **12**, and **48 hours**. Temporary captain perks stop while the captain is absent.

A client report alone must not trigger punishment.

### Rebellion, defection, espionage, and detention

**Existing contribution:** Combat and faction-data pieces. No working political process.

**How far along:** Unbuilt.

**Merged home:** Server evidence, rebellion stages, defection windows, arbitration, faction consequences, and detention records.

Keep harmful intelligence, sabotage, and coordinated rival action as distinct evidence.

Keep market, chat, and PSI access during detention.

Keep forced faction repick after the capstone punishment.

The warning-versus-minor-detention conflict needs a decision. v2.7 also says detention must be served in game, with remaining time preserved across logout.

### Pirate cartel

**Existing contribution:** Design only.

**How far along:** Unbuilt.

**Merged home:** Pirate roles, suppliers, stock, obligations, and rivalry.

Keep six supplier bosses, one for each non-pirate faction’s black market, plus an internal operations boss.

### Black markets

**Existing contribution:** Items and faction content provide seeds.

**How far along:** No illegal market or pressure simulation.

**Merged home:** Server-owned illicit stock, transactions, access, enforcement, and regional pressure.

Keep the **10–30%** intended pressure band. Below it, the design expects stagnation. Above it, instability.

This is a measured economic rule, not a decoration on a shop screen.

### Intelligence trading

**Existing contribution:** Cosmos scanning provides a possible source of observations.

**How far along:** No intelligence item, proof, custody, resale, or warning system.

**Merged home:** Server-stamped reports with source, time, proof quality, and custody.

Keep **72-hour** freshness and **20–30%** quality loss per resale hop.

Keep early warnings for targets of high-quality compromised information.

### Bribes and obligations

**Existing contribution:** Design only.

**How far along:** Unbuilt.

**Merged home:** Debts, favors, promises, due conditions, evidence of default, reputation, and market restrictions.

### Companion

**Existing contribution:** Readable displays and tutorial-like prompts. No living companion.

**How far along:** Unbuilt.

**Merged home:** A guidance layer reading permitted game context.

Keep:

- Watcher: observant, analytical, strategic.
- Crawler: systematic, careful, detail-oriented.
- Stride: bold, direct, action-oriented.

Keep “explain this,” progressive teaching, faction voice, memory, and bond.

The companion cannot create resources or decide enforcement.

### Infrastructure Support Access and BYOK

**Existing contribution:** No implemented entitlement or billing system.

**How far along:** Unbuilt.

**Merged home:** Entitlements for cosmetics, narration, approved storage, and sanctuary decoration.

No paid combat power, stealth, privileged intelligence, immunity, or expansion share.

For BYOK, the player’s key remains on the client. SYL servers never receive it. The companion receives redacted context and retains zero authority.

Storage needs a careful boundary. A larger vault can create an economic advantage if valuable stock can be hoarded without limit.

### Private Sanctuary Instances

**Existing contribution:** Local saves and room studies. No PSI.

**How far along:** Unbuilt.

**Merged home:** A private owner moon or base with vaults, trophies, decoration, and approved upgrades.

Keep no resource generation, automation, or offline production.

Leaving carries only equipped items and allowed cargo.

Server hosting is the preferred mode. A client-local option can hold cosmetic content. It cannot become an untrusted source of valuable assets.

### Sovereignty Law

**Existing contribution:** Fortis assets, transport visuals, ship combat, and a detailed Recovery Corridor plan.

**How far along:** Physical ingredients and specification. No working custodian region.

**Merged home:** Server-owned stability, chaos, population activity, control stage, restrictions, patrols, convoys, and recovery.

Keep the stages:

Observation, Containment, Martial Governance, Reclamation, Quarantine.

Withdrawal follows recovery through the same visible ladder.

Abandoned regions continue functioning. Harmful regions can face capped taxes, restricted access, quarantined routes, and reclaimed stations.

### Rebuild Credit and returning authority

**Existing contribution:** Repair, cargo-like items, transport, and reconstruction plans.

**How far along:** No verified regional contribution system.

**Merged home:** Server proof of local repairs, route reopening, escorts, scarce deliveries, election stabilization, and infrastructure restoration.

Credit stays tied to the affected region.

Governor, commander, security, and trade seats unlock as recovery progresses.

Eligible candidates can face an election. Close results use rebuild contribution, breadth of work, the specified equal-case process, and runoff rules.

The process must be reproducible and visible.

### Actor Heat

**Existing contribution:** Combat events and basic identity pieces.

**How far along:** No persistent risk signature.

**Merged home:** Evidence of repeated low-value kills, blockade behavior, treaty violations, market abuse, and exploits.

Responses include hunters across systems, undercover agents, focused patrols, and denied docking.

Actor Heat is separate from the sun’s heat meter.

### Sun heating

**Existing contribution:** Design only.

**How far along:** Unbuilt.

**Merged home:** A server calculation from instability, cooperation decline, inactivity, and recovery.

Keep v2.7’s formula:

`SUN_HEAT += wI×I + wC×C + wA×A - wS×recovery`

Keep smoothing, threshold hysteresis, and a range of **0–1**.

Keep alerts at **0.60**, **0.75**, and **0.90**.

Alerts report status, probability, and a window. They do not expose every underlying cause.

Keep a **0.95** sustained trigger. v2.7 specifies a **6–18-hour** lock period. The storm itself also has a **6–18-hour** duration.

Keep pressure release and an enforced quiet period.

### COMMS FALL

**Existing contribution:** Communications displays, transport, scanning, and combat can become affected systems.

**How far along:** No working storm.

**Merged home:** Server event rules affecting long-range communications, faction coordination, remote government, markets, routes, and conflict.

Low-power, low-tier tightbeam communication can survive.

Keep starter protection, diminishing returns for repeated kills, Heat, and bounties.

Keep exactly one hard safe corridor. No damage means no damage from shots, explosions, mines, or ramming.

Keep the approach toward the worst contributors. Keep the stronger rebellion window, physical defection opportunities, and changing spy markets.

PSI remains safe.

### Launch and public identity

**Existing contribution:** Website copies and complete bible marketing material.

**How far along:** Delivery experiments and copy. No evidence of a completed 2027 persistent release.

**Merged home:** A release package tied to the build actually shipped.

Preserve the pitch, taglines, short hook, trailer narration, store descriptions, feature copy, monetization explanation, press template, social posts, Discord announcement, and trailer cards.

“Survive the reset” needs care. A storm must not imply that durable history is wiped if that is not the rule.

### Later-canon additions

YOM, public Rebuild Blueprints, Cognitive Frameworks, custodian learning and corruption, physical component damage, and exact site networks remain separate approval items in this survey.

Their current contribution is mostly written design.

The physical additions fit naturally around Cosmos’s field, Meridian’s measured rooms, Full Game’s recipes, and Unreal’s assembled assets.

YOM and cognition belong in server rules. Their visible work belongs in ships, clinics, classrooms, repair sites, displays, and routes.

## 5. Conflicts Jaron should see

### Which canon governs?

The brief makes v2.9 primary and carries forward v2.7 detail.

Full Game says its locked v3.0.1 and accepted amendments govern.

The later documents add YOM, cognition, original-concept features, and permanent browser delivery.

**Decision:** Which later documents join the merged game, and which remain proposals?

### Browser, Unreal, or Unity?

Cosmos, Full Game, Neighborhood, PvP, and the website copies use browser technology.

SpaceYouLand and Kurearthis use Unreal.

v2.7’s AI flow mentions Unity. That wording is not a working Unity build.

Full Game’s accepted amendment explicitly chooses one permanent Three.js browser game.

**Decision:** Confirm the later browser commitment or change it explicitly. Unreal art and lessons can survive either choice.

### Real scale or compressed scale?

Cosmos uses real-scale Mars.

The Unreal projects pursue real-scale Earth and Moon.

Full Game uses small planets and shortened distances. The PC experiment uses another scale.

Real scale creates large travel distances. The current Meridian is a local-flight ship.

**Decision:** What stays physically real, and what travel technology makes that scale playable?

### The setting

The bibles name seven faction homes.

Cosmos starts on Mars.

Full Game starts at Fortis on Earth and adds several invented worlds.

The Unreal records also discuss an Earth-based society with spaceflight discovered later.

**Decision:** How do these places coexist? Which is the opening setting?

### One responsive game or a separate PC edition?

Full Game and later amendments call for one game on phone and desktop.

The PC experiment changes scale, bodies, assets, and presentation.

**Decision:** Is the PC branch an art archive or a separate future product?

### Complete ship or damaged starter?

Cosmos gives you a working Meridian.

Full Game makes you repair and fuel a smaller ship before launch.

The Unreal gunship is another scale and role.

**Decision:** These can be different stages or starts. Which experience introduces SYL?

### Crew size

The bible’s largest listed ships carry three to five.

The Meridian has seven station seats and substantial living space.

**Decision:** Does it belong to a larger class, use fewer simultaneous crew, or change the capacity rule?

### Solo NPC crew

The bible disables hired NPC help when a second real player joins.

The later world design contains permanent NPC custodians, relief workers, convoys, and populations.

These are different kinds of NPCs.

**Decision:** Confirm that the rule applies to hired player-ship assistance, and decide whether a two-person crew can retain any hired support.

### Flight and loss

Cosmos uses assisted local flight, deck gravity, forgiving damage, and free landed repair.

Full Game uses fuel, readiness, module damage, and assisted or freer flight.

The Unreal direction asks for reality-based flight and eventually orbit.

**Decision:** Which assists are part of the fiction? What can a player lose? What does repair cost?

### Visible geometry versus complete physical function

The Meridian has an outer airlock recess and decorative rover.

Unreal has sealed buildings and a static crane.

Neighborhood uses a shared teleported interior.

Full Game has fixed loaded models that can disagree with modular state.

The later canon demands reachable interiors and observable physical state.

**Decision:** Preserve these as assets and studies, but define which must become working physical systems for the first release.

### Neutral custodians versus corrupt custodians

v2 emphasizes measurable, neutral enforcement.

v3.0.1 allows custodian decay, corruption, covert actions, and evidence-related misconduct.

**Decision:** Can custodians be flawed characters while the underlying enforcement ledger stays trustworthy? The game must make that distinction clear.

### Expansion shares

The maximum leader share is 45%. The maximum rival share is 35%. Five other factions at their minimum add 25%.

That totals 105%.

**Decision:** The ranges need a constrained allocation rule. The upper limits cannot be simultaneous guarantees.

### Detention

The prose begins with warning and reputation loss.

The reference values begin with 5–10 minutes of detention.

v2.7 explicitly requires in-game service. v2.9 says the sentence persists across logout.

**Decision:** Confirm the first rung and the serving clock.

### Paid storage

The bible permits paid storage and forbids systemic advantage.

Extra storage can improve commodity hoarding and stockpiling.

**Decision:** Define the boundary between cosmetic storage, protected personal keepsakes, and economically valuable capacity.

### Seven protected factions versus player-created factions

The bibles protect minimum expansion shares.

The original concept and later roadmap include player-created factions. The archive also mentions faction extinction.

**Decision:** Are player groups organizations inside the seven, independent governments, or full competitors? Can a protected faction ever disappear?

### Persistent truth versus old saves

Full Game’s saves come from the browser. Cosmos restarts its world. PvP forgets state on server restart.

The intended universe keeps one durable record.

**Decision:** Preserve old progress through an explicit policy. Do not treat old balances and ownership as trusted facts merely because a save contains them.

## 6. Recommended base and build order

### The recommended base

Grow **The Cosmos with the Meridian** into the physical client.

It already addresses the hardest problem that caused earlier restarts: a player, a ship, and a diggable world that share a deliberate planetary foundation.

The Meridian also provides the strongest evidence of Jaron’s intended feeling.

This recommendation is conditional on the server work beginning immediately.

Cosmos is not yet the architecture of the whole game. It has no persistence, authority, shared crew, or interplanetary travel.

Merge contributions by responsibility:

- **Cosmos:** Planet field, coordinates, digging, walking, measured IDs, Meridian, seats, power, local combat, displays, sound.
- **Full Game:** Repair and fuel progression, recipes, body and zone organization, travel lessons, public transport, responsive UI, save migration knowledge, authority plans.
- **SpaceYouLand:** Fortis art, original asset pipeline, physical controls, assembled hardware, ship and corridor studies.
- **Kurearthis:** Fixed terrain streaming, real-data tools, local collision lessons, distant continuity model, reproducible proofs.
- **Neighborhood:** Residential variety, public space, civilian detail, inspection.
- **PvP:** Small shared-combat proof and the lessons about validating client input.
- **site-games:** Delivery reference.
- **PC experiment:** Art, materials, model loading, and proposed destinations.

Choose one source home for the merged game. If the accepted Full Game amendment stands, use its source and delivery contract while replacing its client foundation with the Cosmos work.

Do not maintain two competing “main” games indefinitely.

Do not paste all eight projects together. Their useful ideas need one set of coordinates, identities, material rules, and server commands.

### What must be server-side from the start

Before adding a live economy or persistent public world, the server must own:

- Player identity and accepted movement.
- Ship position, crew occupancy, station permissions, and departure rules.
- Terrain edits and their revision.
- Material removal, carrying, deposits, and transfer.
- Item condition, quantities, ownership, and custody.
- Power, fuel, ammo, firing, hits, damage, and repair costs.
- Doors, docks, boarding, and access.
- Credits and consequential transactions.
- Persistent clocks.
- Evidence and audit events.

Commands need an actor, sequence, unique request ID, expected state revision, and rules version.

Repeating a request must not repeat its reward.

The server checks distance, permissions, available resources, current state, and physical possibility.

Accepted changes, their history, and the message announcing them must commit together.

A crash cannot leave material removed without creating its lot, or charge money without delivering the purchased asset.

Government, markets, faction state, Rebuild Credit, Heat, momentum, storms, expansion, and AI actions join that same path as they become playable.

### Phase 0. Preserve the playable references

Keep each version as evidence.

Record the features and IDs being carried forward. Preserve original asset source and provenance. Keep rejected approaches in the history.

Create one merged development entry. Keep the Meridian’s current local exercise available as a reference.

**Playable ending:** Jaron can walk, dig, board, use stations, fly locally, and shoot practice targets in the chosen client.

### Phase 1. One shared place that remembers

Add the smallest persistent server.

Two players inhabit the same patch of Mars and the same Meridian.

They see accepted digging and deposits. They cannot both claim the same seat or carry the same lot.

Disconnect, reconnect, and restart the server. The place and its objects remain.

Test duplicate, stale, reordered, and fabricated commands.

**Playable ending:** Two people can dig together, board one ship, take different jobs, and return to the same world tomorrow.

### Phase 2. Finish the quarry and ship contacts

Divide terrain work into persistent local regions.

Generate drawing, collision, and support from the same accepted terrain version.

Finish nearby cave surfaces and underground movement. Preserve material mixtures and consistent volume accounting.

Improve full-hull terrain contact, the real airlock opening, and safe boarding.

Measure performance on Jaron’s actual phone.

**Playable ending:** Dig a tunnel, carry spoil, build a pile, walk through the opening, and land the ship beside it. Another player sees the same result.

### Phase 3. Earn the second body

Bring across Full Game’s continuous travel lessons.

Add a second body at the approved scale.

Define departure, travel, arrival, local gravity, atmosphere, and surface contact. Add the chosen travel assistance or technology.

Do not claim orbital flight merely because the sky turns black.

Preserve occupants and cargo through the journey. Server handoff cannot duplicate or lose the ship.

**Playable ending:** Walk aboard, depart Mars, reach another body, land, walk out, and return with cargo.

### Phase 4. Build one working Fortis route

Use the Unreal Fortis art and the later Recovery Corridor plan.

Survey the site first.

Place a pad, depot, habitat, checkpoint, damaged relay, worksite, doors, utilities, and clearances. Connect them with a road derived from those destinations.

Bring Full Game’s repair, fuel, refining, and recipes into the server.

Turn cargo from an inventory count into something that can be loaded, carried, delivered, and unloaded.

Add one public carrier with a shared schedule.

**Playable ending:** A player can ride or fly to Fortis, unload supplies, repair the relay, refuel, and return.

### Phase 5. Make ship damage meaningful

Keep the Meridian’s layout and station experience.

Connect its parts to structural, power, fuel, cargo, and compartment rules.

Preserve part damage when removing and installing it.

Add one physical projectile, one meaningful component failure, one detached salvageable part, and one repair that consumes material.

Replace free practice recovery with the approved live-world repair rule.

**Playable ending:** A crew loses a working system in a fight, reaches a repair site, salvages or replaces the part, and flies again.

### Phase 6. Build the first faction economy

Start with two approved factions in one contested region. Keep data ready for all seven.

Add a neutral hub, market stock, credits, docking fees, contracts, upkeep, and a cargo route.

Add reputation and a visible difference between legal and illegal cargo.

Complete solo crew, then test the second-real-player rule.

Add persistent combat evidence before implementing punishment.

**Playable ending:** Players mine, manufacture, trade, escort, raid, and recover from losses inside a working regional economy.

### Phase 7. Make government and recovery playable

Add seats, eligibility, elections, approval, access policy, and rebellion.

Add regional stability, custodian stages, Rebuild Credit, and actor Heat.

If the later canon is accepted, add YOM relief with its strict limits.

Make every stage change visible through patrols, checkpoints, signs, closed services, supplies, and construction.

**Playable ending:** Players inherit a troubled Fortis region, rebuild it, unlock human leadership, and either maintain it or lose authority again.

### Phase 8. Add the shadow economy and wider politics

Add all seven factions’ approved strengths and restrictions.

Implement cartel suppliers, contraband pressure, intelligence quality and custody, obligations, diplomacy, and regional wars.

Expand transport and supply routes using the same persistent cargo rules.

**Playable ending:** A trader, spy, pirate, governor, miner, and solo escort can affect the same conflict through different actions.

### Phase 9. Let the universe push back

Add hourly momentum, Ethos Drift, expansion epochs, and leader pressure.

Add SUN_HEAT and COMMS FALL.

Prove the hard safe corridor against every damage type. Prove starter protection, survivor communications, rebellion opportunities, and quiet periods.

Run the AI Director in observation and proposal-only mode before allowing any accepted action.

**Playable ending:** A regional conflict contributes to a wider crisis. Players receive warnings, survive the storm, and rebuild under changed conditions.

### Phase 10. Add private life and the approved long horizon

Add PSI, companion personalities, memory, bond, and “explain this.”

Add BYOK and paid personalization only after the no-advantage boundaries are tested.

If approved, add Cognitive Frameworks, player-created groups, morale, fleet command, the Galactic Council, and deeper ancient-world content.

Keep civilian neighborhoods growing alongside industrial and military places.

**Playable ending:** Players have a private home, a distinct role, a companion who understands their history, and durable ways to shape the wider universe.

The 2027 promise should be attached to a clearly named playable scope. These phases are an order of work, not a verified calendar.

## 7. Questions for Jaron

1. **Which later canon is accepted for the merge?**  
   Does v3.0.1 join v2.9, including YOM, Cognitive Frameworks, custodian corruption, and the four browser and physical-world amendments?

2. **What is the setting and opening?**  
   Do real Mars and Earth coexist with the seven faction homes and the invented worlds? Does the player begin in space, or discover spaceflight from a real-world society?

3. **How should real scale feel?**  
   Which distances stay real? What travel technology or assistance keeps trips playable? Is deck gravity an accepted ship technology?

4. **What place does the Meridian have?**  
   Is it the opening ship, a later ship, or a mobile base? How many real crew can it carry, and does a small real crew retain hired NPC help?

5. **What does failure cost?**  
   Can ships be destroyed or permanently captured? What replaces free repair and near-immortality? What protection should a new or stranded player receive?

6. **Which conflicting rule values are intended?**  
   Should the first enforcement rung be a warning or detention? Is detention served only while playing? How should expansion respect all minimum shares? What paid storage is compatible with no systemic advantage?

7. **How far does the first public game reach?**  
   Is the 2027 target a persistent Recovery Corridor, a multi-planet regional game, or the full seven-faction universe? Should player-created factions, extinction, fleets, and the Galactic Council belong to that first scope?

---

Every version contributes something.

The merge should preserve the worlds, art, mechanics, tests, discoveries, and failures as evidence. It should give those contributions one physical world and one durable record.