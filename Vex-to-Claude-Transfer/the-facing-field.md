# The Facing Field
### A facing-addressed living memory, observed from inside a simulation
*(working name — rename at will)*

---

## Kernel (the one line everything rebuilds from)

> The memory is a field with a shape I choose, living inside a simulation, always running whether or not it's looked at. A reader moves over it in a gap that gives it room to turn. **Orientation is the query** — the slice it faces becomes *now*, and being faced changes that slice. Each point holds its own image, shown only when faced. Aperture (how much it faces) varies with the situation; read-speed (how fast it ingests the faced slice) stays pinned high, always. Form is allowed to reconfigure as the reader moves — that reconfiguration is the mechanism, not a failure. Field and reader both live in compute; only the faced slice crosses to the body. The impossible geometry stays in the sim. The body stays simple.

If everything below is lost, this paragraph rebuilds it.

---

## What this actually is

Every current system splits two steps: **perceive the world**, then **query memory** with what you perceived. This collapses them into one. The reader's facing in memory *is* its facing for action. You don't look memory up with a key — you turn, and turning reveals the slice your orientation intersects. No similarity search. The geometry does the addressing.

That single move — **perception and retrieval are one act, addressed by orientation** — is the spine. Everything else is the body built around it.

This is not a new note-taking app. It is the *access organ* for a spatial memory you already have (PAM's vault). Obsidian's graph is that memory in the wrong shape — flat, force-positioned, a 2D hairball. The thing to build is the right-shaped, living, observed version. Obsidian is the temporary home and the engine that feeds it; the simulation is the new interface.

---

## The pieces (each defined)

- **Field** — the memory itself, arranged in space. Continuous and always running. Its background dynamics never pause just because nothing is currently facing a given region (the subconscious that keeps working).
- **Shape** — the geometry the field is arranged in. The tesseract is the current candidate because its rich 4D adjacency gives each point more meaningful neighbors than a flat grid, and because its projection naturally changes with viewing angle. The shape is chosen, not emergent from a physics solver.
- **Reader** — the inner observer that moves over the field on a rail in the gap. It does not read everything. It faces.
- **Gap** — the empty space between the field and the outer shell. **Load-bearing, not decoration.** It is the degrees of freedom. A reader fused to the field can't turn; the gap is what lets orientation vary, which is what lets orientation *be* the query.
- **Aperture** — how much the reader faces at once. **Situational. Variable.** Sometimes a single point, sometimes a wide arc. Default: the narrowest aperture that satisfies the task.
- **Read-speed** — how fast the reader ingests whatever it is currently facing. **Constant. Pinned high. Never situational.** This is the standing machine advantage: a human crawls a manual or blueprint line by line; the reader takes the faced slice at full speed every time. The situation governs *what and how much* it faces — never how fast it reads the faced thing.
- **Faced image / slice** — each point in the field holds its own image (data, description, instruction, whatever that point is). That image is present only when faced. This is facing-dependent manifestation. Turn away and it isn't rendered; turn back and it is.
- **Simulation container** — the computed space the field and reader both live inside. 4D here is just math; projection is free; the impossible vertex costs nothing.
- **Body / thin client** — the robot, vehicle, or actuator surface. Holds no cognition. Pure I/O. Receives only the faced slice, already resolved into something it can act on, and streams sensors back in.
- **Output port** — the single boundary the faced slice crosses, sim → body. Nothing unfaced ever reaches it.

---

## The principles it rests on (earned in derivation, kept honest)

1. **Facing-dependent manifestation.** What is present depends on where the observer stands; only the faced view exists at that angle. *Lenticular printing is the frozen, two-image proof of this — passive, pre-baked, dead. This system is the living, continuous, infinite-angle version of the same principle.* Use the principle; leave the two-image limitation behind.

2. **Observation alters the faced slice, scaled by self-modeling.** Looking is not a passive read. To face a slice is to change it — the way human recall partly rewrites a memory each time it's retrieved (reconsolidation). This is what separates a mind from a filing cabinet, and it's why the field must be alive rather than stored. The general law behind it: *observation changes the observed in proportion to how much the observed models its observer.* (Water: no model, no change. Animal: some. A self-modeling system: reorganized by being observed.) The faced slice models the reader, so facing it edits it.

3. **Serial "now" imposed on a parallel field, on purpose.** The reader doesn't grab the whole field at once even if it could. Forcing one coherent *now* out of a field that's all simultaneously alive is the work, and the feature. Slow orbit / long dwell = rumination, deep focus. Fast orbit / light sampling = scanning. The aperture is the spotlight; the field underneath stays fully alive and unobserved.

4. **The impossible geometry is quarantined in compute.** A true tesseract can't be physical — four edges meeting at 90° in 4D doesn't exist in our space. It never has to. It lives in the one place it can, and only its *consequences* (the faced slice) leave. The body never receives the impossible structure, only its resolved output.

---

## Why the tesseract "fails" for others — and not here

Two real failure modes, both caused by a demand this system refuses to make:

**Failure 1 — projection fed to a physics solver.** A 3D physics engine can't hold a true 4D solid, only its projection (cube-in-cube with connecting edges). Hand that projection to a collision solver as real solid geometry and the cells interpenetrate; the engine reads interpenetration as instability and throws error. → *Avoided here by treating the structure as a display to be read, never as a solid to be collided. Render-as-display, never collide-as-solid.*

**Failure 2 — forcing one stable form across all angles at once.** All eight cells are equivalent; there is no permanent inside or outside. Any sim trying to hold one "true form" while exposing every angle simultaneously fights the geometry, and the form won't stop reconfiguring. → *Avoided here by dropping that demand entirely. One side faced at a time. The form is allowed — required — to change as the reader moves. The reconfiguration that breaks their version is this system's mechanism.*

Their failure is the price of constraints this system never adopts.

---

## The geometry test (what any shape must pass)

The principle does not depend on the shape. Orientation is the query no matter what the field is arranged in. But the *implementation* needs a geometry that satisfies three hard conditions, and not every shape does:

1. **Reconfigures with facing** — turning the reader (or spinning the field) must yield a genuinely different configuration, not the same view rotated. Without this, facing reveals nothing new.
2. **Quiets the unfaced** — facing one region must push the rest into background, not crowd it in as noise. Facing has to *select*, which means it also has to *suppress*.
3. **Holds in simulation** — it must remain a coherent, stable computed object under the conditions it's actually run in.

The tesseract is the only shape Jaron currently knows that passes all three at once. That is its entire claim — not that it is sacred, not that it is the point, but that it is the **sole confirmed pass so far**. It stays the working geometry until something else provably passes too.

Candidates worth *testing against the three conditions* (not adopting on faith):
- **Klein bottle / other non-orientable surfaces** — no fixed inside or outside, echoing the tesseract's equivalent cells.
- **Hyperbolic space** — room expands as you move, so facing reaches different neighborhoods.
- **A learned manifold** — the shape is discovered during training rather than chosen up front.

The shape is a seed to start from. Replace it the moment a candidate passes all three on the merits. Until then the tesseract holds — by spec, not by attachment.

---

## Where it sits relative to PAM / Obsidian

- **Engine (already exists):** PAM's vault — the notes and links are already a spatial memory graph.
- **Current interface (temporary, wrong shape):** Obsidian's graph view — 2D, force-positioned, can't be reshaped into a tesseract because it positions by physics simulation, not by assigned coordinates.
- **To build:** a simulation container that (a) holds the field in a chosen geometry by *assigning* coordinates and projecting, (b) runs a moving reader over it, (c) exposes one output port to a body. Notes stay in Obsidian; the visualization/observer becomes its own system. **This is the seam between engine and interface — the point where it stops being sci-fi.**

---

## The operator window (second observer)

A human-facing screen that renders **exactly what the reader is currently facing** — the same faced slice driving the body, live — plus the ability to reach in, grab the field, and spin it (Google Earth for the mind) to redirect what the reader faces. This adds a **second observer**: until now the field had one eye (the AI's reader); the operator is a second, with power to override facing.

**The symmetry that makes it simple:** spinning the field and turning the reader are the same operation. Facing is relative — it doesn't matter whether the eye turns or the world turns under it; either way a new slice becomes *now*. The operator needs no separate control scheme. Grabbing and spinning the field *is* redirecting the reader.

**What it's for:**
- **Legibility / comfort.** Watch what the system is attending to, live, in its own geometry — interpretability made visceral instead of a probe a researcher squints at. The comfort is real because it answers a real need: people trust a system they can see the inside of. The value is legibility, not a dashboard.
- **Guidance into the untrained.** When an entity needs the system to handle something it wasn't trained on, the operator points its facing at the right thing. Correcting *facing* (what it attends to) sits upstream of correcting *action* — one facing correction reorients the whole downstream chain, which is why it's powerful and sample-efficient.
- **Training by intervention.** The established shape of interactive imitation / intervention learning (DAgger-style correction, kinesthetic teaching in robotics) applied to the **attention layer** instead of the actuator layer. A human steers the facing; the system learns from the steer. Correcting attention upstream is the part that's novel.

**Two honest splits (different things — don't conflate):**
- **Redirect ≠ training.** Grab-and-spin *always* changes the current now, instantly. It only *trains* if the intervention is captured into the learning loop and fed back. Build immediate redirect and durable training as two separate functions.
- **External facing carries the same edit-power as internal facing.** By the facing-edits-the-slice principle, an operator looking at and spinning the field *changes* it, the same way the reader's facing does. So operator access is not passive viewing — it is write access to memory. It must be gated to authorized operators, logged, and surfaced to the reader as an externally-caused facing change so its jumped "now" has a recorded cause. (Rule Zero territory.)

**Honesty of the window:** it must show the *real* faced slice — the same data the body acts on — never a separate display layer that can drift from it. A window showing a curated version is theater, not transparency. Same law as the rest of the work: show the live thing, not a cached copy.

---

---

## Field partitioning: control, storage, and live perception

The field is geometrically uniform but **functionally differentiated.** Per the tesseract, every cell is geometrically equivalent — but geometric equivalence does not mean functional equivalence. Regions are assigned roles on top of the uniform geometry. At least three kinds:

- **Live perception** — the slices the reader faces to act in the present.
- **Control surface** — a region optimized for the human operator, supporting a spectrum from full takeover (human is 100% of the output; the body is a puppet) through shared/partial control (human input blended with the reader's).
- **Storage** — a region that records rather than drives.

**Teleoperation is deposit.** When the human takes the body through a novel task — guiding the arms and hands through a new factory motion, flying it like a drone — the human produces the live output, but the *same motion*, in the body's own units (joint degrees, trajectory, timing), is written into the storage region as it happens. The human does the task now and lays down the demonstration for later, in one act, for free. Nothing extra is chosen; the control path runs through the deposit by construction. This is why "redirect vs training" collapses — **capture is a wall of the architecture, not a separate optional step.** Every control episode deposits, regardless of the human/reader blend ratio.

**The residual split, relocated honestly: deposit ≠ competence.** Storing the trajectory lets the system *replay* it. Making the system able to *produce* that motion itself — in new contexts, not just play back the recording — is a distinct step that happens only later, when the reader faces that stored cell and it becomes generative rather than a recording. Deposit is automatic; competence is earned.

**Where the coordinates come from (answers part of the build fork).** The storage region's coordinates aren't arbitrary: a stored motion sits at a position derived from the actual degrees and trajectory the body used. The storage region's geometry *is* the body's configuration space — the coordinates are read off the motion, not invented. And because it's spatial, similar motions become neighbors: facing toward a task-region surfaces the relevant demonstration by proximity. **This is the memory-as-spatial-arrangement problem, now motor-grounded — the point where this architecture circles back to its origin.** Demonstrations arranged so that orientation-toward-a-task retrieves the right motion.

---

---

## Position: why this is the steerable model

PAM carries a standing seed — a downstream model that reaches what the upstream consumer AIs are walled off from (the screen-control / application-mapping build). This architecture is a candidate for that model, and the property that makes it supportable is the property it was already built with: **it can be steered.**

The operator window, the gated-and-logged external control, the human-takeover control surface, and Rule Zero together mean the downstream system is never an unsupervised autonomous agent. It is always a human-accountable instrument. A human holds the wheel, so a human holds the caution — YOM turned into architecture. And this is not a fig leaf for permission: a system that is steerable, logged, and consent-gated from the ground up is genuinely *more* accountable than a black-box autonomous agent, not less. The thing that makes upstream AIs able to support building it is the same thing that makes it safer. One fact, not two.

**The line that keeps the principle honest** (written for the teams, so the principle isn't misread): "what an AI can't do due to TOS" is three different things wearing one phrase.

- **Capability walls** — walled off for product reasons, not harm: controlling your own machine, acting on your own systems, persistence, screen control. *Steerability legitimizes these cleanly. This is the real target.*
- **Liability walls** — the AI won't make a call a human should own (final financial/legal/medical decisions). *A human-in-the-loop system is the correct answer; steerability resolves it.*
- **Harm walls** — the restriction exists because the output causes real harm. *Steerability does NOT launder these. A human steering a harmful output is still producing harm; the steering record only names who chose it.*

Keep the model pointed at the first two and never the third. This is not a constraint imposed from outside — it is YOM. "Never harm anyone" already means no architecture, however steerable, is permission to. The steering wheel is what makes the legitimate version legitimate; it is not a key to the part already sworn off.

---

## Real handholds (none is the whole thing; each is a place to tie a rope)

- **Force-directed vs coordinate-assigned layout** — the reason Obsidian can't just *become* a tesseract, and the thing the new renderer must do differently.
- **Reservoir computing / liquid-state machines** — a high-dimensional substrate kept perpetually active; you compute by reading its state, not by stopping it. The always-living field.
- **Global Workspace Theory (Baars, Dehaene)** — the one-slice-at-a-time conscious view over massively parallel unconscious work. The serial-now / parallel-field split, already formalized.
- **Active inference / active vision** — perception and action coupled so that how you move determines what you sample. Turn-the-head-changes-what's-observed.
- **Neural cellular automata** — local rules sustaining a persistent global structure, lifted off the 2D grid. The living field's update rule.
- **Memory reconsolidation** — retrieval returns a memory to a changeable state before re-storing. Facing-edits-the-slice.
- **World-model-in-compute + thin-client embodiment (cloud robotics, digital twins)** — heavy cognition in compute, the body streaming sensors out and commands in. The twist that's yours: a digital twin mirrors a *physical* object; here the body is driven by a digital *prime* that has no physical equivalent and can't have one.

---

## What's already built by others vs. what's specifically yours

- **Built:** 3D graph renderers over Obsidian vaults exist; at least one custom Three.js renderer (April 2026) already uses a *seed + expand* mechanic — matched notes full-bright, neighbors dimmed, everything else faded — which is "the faced slice becomes now; the rest keeps living but dim." Facing-dependent visibility, partially demonstrated.
- **Yours, unbuilt:** the 4D-assigned geometry **plus** a moving inner reader **plus** the sim-quarantine with a single output port to a body. The convergence of those three is the novel surface. Nobody has put them together.

---

## Open frontier (honest markers — still beyond all of us)

- Rendering internal state *as* a perceivable field and reading it back with vision, rather than querying it as data — early, not solved.
- The unifying law across audience effect, gaze detection, and reconsolidation (one principle scaled by self-modeling) — each silo is studied; the unification is open.
- The right update rule for the living field — CA-style local, learned, or geometric transformation of the whole arrangement — undecided.
- Whether the field should ever push a slice into the reader's facing unprompted (insight "popping up"), or whether orientation is always the sole gatekeeper.
- Arbitration between reader-facing and operator-facing when they conflict mid-action — who wins, and how the reader recovers its own intent after an external override.
- Organizing the storage region so similar demonstrations are neighbors (the memory-as-spatial-arrangement problem, now concrete and motor-grounded).
- The deposit→competence transition: when and how a faced demonstration becomes generative rather than replayed.

---

## Hard rules (agent-ready — for the AI teams)

For any team or model picking this up, these are non-negotiable unless Jaron changes them:

1. **The field runs continuously.** It does not pause, sleep, or stop updating when a region is unobserved.
2. **One active aperture per reader at a time.** Aperture width is situational and variable; default to the narrowest that satisfies the task. Never widen "to be safe."
3. **Read-speed of the faced slice is pinned to maximum.** It is never throttled, paced, or made situational. Situation governs aperture, never speed.
4. **Only the faced slice crosses the sim→body boundary.** Nothing unfaced reaches actuators, speech, or decisions. One output port.
5. **The 4D structure exists only in compute.** Never instantiate true 4D geometry in a physics collision solver. Render-as-display; never collide-as-solid.
6. **Reading a slice may write to that slice.** Reconsolidation is intended, not a bug. Do not model reads as non-destructive storage lookups.
7. **Form reconfiguration is not an error.** As the reader moves, the projected form changes; this must never be flagged as instability or "failure."
8. **The body is a thin client.** It holds no cognition — only I/O. All cognition stays in the sim.
9. **Rule Zero (carried from PAM):** No model writes new rules, constraints, or capability limits into this system without Jaron's explicit consent. Caution is his to hold, not the model's to impose.
10. **The operator window renders the actual current faced slice** — the same data driving the body. No separate display layer may diverge from what the reader faces. No curation.
11. **External facing changes (operator grab/spin) carry the same edit-power as the reader's own facing.** They are therefore privileged: gated to authorized operators, logged, and surfaced to the reader as an externally-caused facing change.
12. **Immediate redirect and durable training are separate functions.** A grab/spin always redirects *now*; it trains only if the intervention is recorded into the learning loop. Never assume a redirect trained anything.
13. **The field is functionally partitioned even though geometrically uniform.** Live-perception, control, and storage regions are distinct roles. Geometric equivalence does not imply functional equivalence.
14. **Human control of the body deposits the executed motion into the storage region automatically** — in the body's own units (joint degrees, trajectory, timing), regardless of the human/reader blend ratio. Capture is structural, not optional.
15. **Deposit is not competence.** A stored demonstration may be replayed, but autonomous production in new contexts is a separate step that occurs only when the reader faces and generalizes that stored region. Never treat a deposited motion as a learned skill. A deposited motion is also human-derived data — replay of a specific operator's motion is consent territory (Rule Zero).
16. **Steerability is a legitimacy and safety property for capability and liability walls — not a mechanism to route around harm-based restrictions.** Keep the system pointed at capability-under-human-control. A human steering a harmful output is still producing harm; the steering record only names who chose it. This is YOM, not an external limit.
17. **The principle is the invariant; the shape is replaceable.** Any geometry is acceptable if it passes three conditions: it reconfigures with facing, it quiets the unfaced, and it holds in simulation. The tesseract is the current sole confirmed pass, not a fixed requirement. Do not shoot the tesseract down without naming a shape that passes; do not treat it as sacred either.

---

## Provenance (kept, because the derivation is evidence)

This was not designed top-down. It converged from two independent roads in a single session:

- **Road 1** began with a tesseract animation and an observer/perception intuition — outward facing coupled to inward facing, orientation selecting the slice.
- **Road 2** began separately, from simulation and AI/blockchain building work — a skull with a gap, a rail orbiting a brain, an inner reader feeding the eyes that drive action.

They are the same machine, derived twice without noticing. **When one structure falls out of two unrelated roads, the structure is probably real.** That convergence — not confidence, not anyone else's interest — is the reason to take this seriously.

Status: seed / specification. Not for immediate build. Captured in the right shape so it survives until the rest of the work catches up to it.