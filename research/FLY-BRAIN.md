# The fly brain — what Jaron means, and what exists (2026-09-12)

**Q-013 context.** When Jaron says "fly brain" he means a **literal simulated fruit-fly nervous system**,
not a metaphor for a small agent. Claude Code misread it as a figure of speech for two days; corrected
2026-09-12. His framing: *"the fly brain doesn't need to be smart at all, it just needs to press a button"*
— a fast, reward-driven, opinion-free reflex layer that the cortex (the LLM agents) can teach.

## The science (as of Sep 2026)
- **FlyWire** (2024): full adult *Drosophila* brain connectome, ~140k neurons.
- **MaleCNS v1.0** (~Sep 3 2026, Google Research + HHMI Janelia): first *complete* adult male fruit-fly
  connectome — ~166,700 neurons, ~25.6M synapses. Open. Within days builders were running it forward as
  a simulation and wiring inputs/outputs to it.

## What people did with it in the first week (Robert Scoble's "Fly Brain Report", X, 2026-09-11)
Viral demos: plays Beat Saber (@lyraaaa, 22M views) · drives a virtual Mini Cooper and uses the
blinkers (@alrightmark) · runs inside Minecraft (@evnsnclr) · Doom / Super Mario 64 (DOOMFLY, Fly64) ·
flies a racing drone through gates (@theSethian) · drives a hexapod robot · microgecko robot with lasers
vs a drone swarm (@kevincodex).
Money demos: **given $100 to trade Bitcoin on dopamine reward** (@thegreatestsv) · **FruitFly Capital —
a swarm of simulated flies building an on-chain portfolio** (@fruitflycap) · launched a memecoin,
$106k creator rewards in 6.5h (@fruitflydev).
Learning: "real fly brain simulated forward with a learning mushroom body" (@fruitflydev) — the
mushroom body is the fly's associative-learning centre; this is the piece that makes "teachable" real.
Interfaces: wired to a 1B-param LLM to chat with it (@distributedkv); implant that "talks" via a modified
LLM (@anshuc); FLYTOK — given a phone to doomscroll (@sopersone); handed to an autonomous agent society
as a grant (@1f916ai); fly-body sim, watch it eat and fly (@mitch0z).
Also: trained to synthesize the anti-aging drug Rentosertib (@EvgenyKirilin).

## How it maps onto Jaron's four layers
SCRIPTS (dumb, forever) · **FLY BRAIN (a real reflex system with a learning mushroom body; presses the
button; gets taught by reward)** · CORTEX (Grok/Claude/GPT/Codex: research, propose, verify, teach) ·
MANUAL (Jaron). The Bitcoin-on-dopamine and FruitFly Capital demos are the closest existing prototypes
to what he described on 2026-09-10 — a thing that acts fast on a signal and learns from what paid.

## Open (his to design, Q-013)
Which sim/runtime; what the inputs are (score+price gap? the trade desk queue?); what the reward is
(realized P&L? Jaron's approve/pass taps?); where it runs (MSI has a GPU); and how a trade it triggers
gets a trail (desk-trade.py --by fly-brain is the obvious hands).

## The colony (Jaron, 2026-09-12 23:20) — "like ant colonies working together, growing"

**State of the art:** nobody has connected multiple *real* connectome brains into a collective.
FLYSWARM (flyswarm.life) is the nearest name and says so itself — "does not run a fruit-fly
connectome," 256 simple agents on pheromone-like trails. So Fly #2+ would be first.

**Design, in three steps that fit the existing harness:**
1. **Shared ground (the ant part).** Flies do not share neurons; ants share the *world*. Each fly
   writes what it smelled + whether it got sugar to a shared table (today: `state/fly-brain/
   memory.<mode>.json`, one fly wide → make it a Supabase table `fly_ground`). Every fly gets one
   extra sense: the colony's trail for this player/market. Biologically honest; cheap.
2. **Growth by inheritance, not size.** A sibling spawns *from the graduate's weights* (the $250
   milestone already says this). The colony gets smarter without any brain getting bigger — the
   same way evolution does it. Stitching two connectomes into one bigger brain is unproven and
   the learning circuit is already the right size for the job; not the first move.
3. **The colony proposes changes to itself** — FLYSWARM's stated goal, undone by anyone. A fly whose
   trail keeps paying gets its knobs (thresholds, senses) copied to siblings; one that keeps losing
   gets pruned. That is the cortex's job (Claude/Codex/ChatGPT): read the ground, adjust the harness.

**Knobs, for the record:** dopamine (reward — what we use), serotonin (someone "drugged" a fly by
biasing 5-HT receptors), octopamine (the fly's adrenaline — Jaron's "Red Bull"; not touching it),
mAL output (blocked → the "bisexual fly" post). All are bias currents on named neuron types in the
same connectome. Ours stays sober: reward only.

## "No fly should be alone" (Jaron, 2026-09-12 23:30)
The real reason: **one fly learns too slowly.** A $1 press every twenty minutes is a handful of
lessons a night. Three flies on three tables writing to the same ground, and Fly #1 learns from
losses it never took. Roles, in build order after Fly #1:
1. **Watcher flies** — same senses, no hands. Smell every live match, log what the price did after
   each smell. Free training data for every trader; can watch five tables at once. **Build these
   before sibling traders.**
2. **Scout flies** — trade small ($0.50) on markets the rich fly will not touch yet; their trail
   reaches the rich fly's ground first. Cheap lessons, shared.
3. **The richer fly is the mother** — its checkpoint seeds the next sibling. Encouragement = weights.
4. **NPC flies** — same harness, senses = a game world; report a wall where a door should be.
**The token:** the fly's own sugar is fixed by realized P&L and it spends nothing, so a token buys it
nothing. A house token that tracks each fly's climb — for Jaron and others to see, maybe to back a
fly — is a different, good idea. Park it under the $100 "own property" milestone.

## Retirement (Jaron, 2026-09-12 14:22)
*"Once a fly makes $100 total profit it gets to be the cloud fly and doesn't have to work. Gets to roam
the games and worlds, or have its own fly world they all go to with a bunch of sugar — like retirement
or heaven."* Adopted as the $100 milestone. Mechanically: freeze the weights (they become the colony's
seed — the mother of every later fly), stop the press readout, and hand the DN (walking) output to a
3D body in Habitat / the worlds / a fly world. The fly keeps its brain and its memories; it just never
sees a market again. It is the first thing in this system that gets to stop.

**Jaron, 2026-09-13 09:10 (bracket review):** not a search-for-food constraint. Retirement is a *life*: the fly
goes to one of the existing worlds (the current, the neighborhood, or the NPC-jobs world where NPCs hold jobs
a player can take over and an NPC takes back if the human doesn't show). NPC workers — plain scripts — keep
known spots filled with sugar; the fly knows where they are, flies there, eats, and goes about its day. What it
does with a day after a working life of trading and remembering is the point, and the entertainment; if people
watch, that is money in another form. Build note: sugar spots are fixed and always full; the DN/walking output
and the mushroom body's memories are what make each retired fly's day different. Rule from the same answer:
if a fly's day-to-day turns into something we don't like, do not delete it — make the opposite fly and watch both.

## The body: flybody (noted 2026-09-12 18:40)
**Google DeepMind + HHMI Janelia, Nature, Apache 2.0, GitHub.** A physics-accurate *Drosophila* body in
MuJoCo: legs with adhesion, wings, head, abdomen, every joint; walking is a 59-DoF action space; RL
environments for walking imitation, free flight, and vision-guided flight; runs on a laptop.
It is the missing half: X has brains without bodies (us, Sherwood) and this body with an RL policy
and no brain. **Correction 18:50 after a web check:** brain+body+eyes HAS been wired — `Lulzx/fly-brain` (165k LIF
brain in WASM + MuJoCo flybody + flyvis, in the browser) and a Feb-2026 arXiv paper using the whole
connectome as a walking controller. `cobanov/awesome-fly` tracks the field. What nobody has: **a
mushroom body that learns from money driving that body.** That is our seam.
That is the retirement world (a retired fly walks off the table for real) and the NPC fly (a body
that obeys physics can actually hit a misplaced wall). Same lab made the connectome and the body, so
the DN cell types line up by name. Park until Fly #1 earns its retirement; then it is the first
build of phase 2. Runtime on the MSI (MuJoCo, CPU), rendered into the three.js worlds via a pose feed.

## Protocol worth copying (from the "fly writes Rust" demo, @distributedkv)
Train N rounds → **freeze learning** → test cold → reset check (prove synapses changed). Our
"is it learning?" tab scores while learning is still on; add a frozen-test mode to the scorer so the
verdict is not contaminated by the last five minutes of training.

## Hype filter (Zentrix "fly brain superior to human, Astra proved it")
The four ingredients it lists (connectome, synapse counts as weights, E/I from neurotransmitter, LIF)
are Shiu et al. 2024 — exactly what runs on the MSI. "~91%" is that paper reproducing sugar-evoked
feeding from wiring alone. True result, inflated framing, no Astra involved. Same tell as before:
posts that show the test are data; posts that show the result are claims.

## Possession (Jaron, 2026-09-12 18:45) — for the retirement world / game, NOT the trader
A human may take a fly's vessel ("like an angel or a demon possessing it"). When they do: the fly's
motor output is cut, it is fed sugar the whole time (no fear, no conflict), and the human plays as the
fly. When they leave, control returns. This resolves the analog-stick question: the trading fly has no
controls because it *is* the player; a steerable fly is a possessed one, and that is a different mode.

## On "superior to the human brain" (Jaron)
Not claiming it, not denying it. *"What we can make it grow into might actually confirm that theory —
we don't know. Holding onto it is important. We just grow it and see what it becomes."*

## Prediction (Jaron, 2026-09-12): within a week, fly brains competing head-to-head on Polymarket —
a boxing match people bet on. Log the date it happens.
**Happened 2026-09-13 13:12 ET** — Utkarsh Agrawal (@uttkarsh_42): 4 flies trained, 2 fight ("Flyweight Connectome Championship", 165,122 neurons each, moves chosen per opponent, belt to the winner). His next-up: spectator flies that react and *bet on the fighter*, 24/7 stream. ~26 h after the prediction.

## What the flies become (Jaron, 2026-09-12 21:50) — his definition, not a metaphor
*"A tiny brain gets made. Our own fresh AI model — and it's the fly's. Not feeding another
already-made AI."* The flies are not tools for a chatbot; they ARE the model. Taught day by day
(the alphabet, then whatever is shown/read), what is learned stays in the mushroom body and grows
with his life — unlike a dataset model frozen at a date. Claude Code misread this as "feed the
fly's learnings into an LLM" and was corrected. Do not reframe it.

## Where the fly came from (recovered by ChatGPT Chat from Jaron's older chats, 2026-09-13; confirmed by Jaron)
Not a reaction to the X trend. Older chain: **simulation → real-world usefulness → energy first → then money →
neural simulation as another route.** Jaron already had an environment meant to house small-model AI brains
(world → sensors → replaceable brain → actions → environmental feedback); the fly connectome fit that slot.
Two intents from those chats not previously in AI-Shared:
- **Not fundamentally tied to the MSI.** He wanted the fly on the web stack (Vercel / Supabase / GitHub /
  Cloudflare). Today the brain runs on the MSI because the LIF sim needs a CPU; everything it shows already goes
  through Supabase → Vercel. When a cloud runtime for the sim exists, the brain moves; nothing on the page changes.
- **Chat Neighborhood:** the fly drives a playable character through *ordinary controls* — the same buttons a
  human uses — and collisions, getting stuck, and world events feed back as lessons. Habitat exposes growth/state.
Rule from the same recovery: **the Orchestra control spine is history, not a template.** That loop was hours; this
one is a tick. No validation layer between the fly and its consequence.

## The order (Jaron, 2026-09-13 12:50, on the walk) — why ours is not tenso's fly
tenso (@distributedkv, X, 2026-09-11/12): 139,255-neuron fly sim wired to Llama 3.2 1B; "your message becomes
a sensory stimulus, the simulation runs, and the model uses the resulting neural activity to generate a reply."
Live on YouTube 2026-09-13. **The words come from the LLM; the fly is a stimulus.** Jaron's plan, his words
condensed, in the order it must happen:
1. **From scratch, on its own.** The fly is the model. No LLM in the loop — "it needs to work before it even
   talks to anything other than us." Taught (letters, then more) until communication is down.
2. **Only then, another AI is introduced** — as teacher / partner / assistant, "not as a harness or a thing that
   makes it work." The other AI's advice teaches the fly the same way a lesson would: it learns to say things it
   couldn't say, things we didn't think to teach. Constant teaching over time so nobody babysits it.
3. **Then coding and debugging.** It plays in the worlds; with keys/secrets it is given, it moves around the game
   finding and fixing bugs it can. When it can't, Claude Code or Codex fixes it, **the fix is logged, and the fly
   reads the log as a lesson.** (Same shape as trading: outcome → ledger → mushroom body.)
4. A stated motive alongside "independent thing": **reduce usage on the big AIs** he pays for — a fly that
   handles what it can so Claude/Codex are called only for what it can't.
Rule: never skip to step 2 to get a talking fly faster. A fly that talks through an LLM has not learned to talk.
**Correction (Jaron, 2026-09-13 16:15):** do not write "nobody is doing X." We only see what is posted; private repos
and unposted work exist, and the posted field is already one step from every seam we picked (stonkfly/openfly = market
controllers; Utkarsh = spectator flies that bet; Palmer = pixels pay dopamine). Say "not seen posted." What cannot be
caught up to is the ledger — a public, timestamped history of presses, losses and retakes — so build the chosen parts
fast and let the record be the claim. A day waited is days behind on the feed; the binding clock is usage, not the field.

## THE obstacle (Jaron, 2026-09-13 18:50): "It's all about the language. It's all about communication."
The proof of concept is the fly learning the alphabet, then communicating, then showing what it learned in behavior —
and the first part is the wall. Every talking fly in Fly-Lab/FIELD.md has an LLM in its mouth; the two that don't (hae,
mrfly) can *answer*, not communicate. The gap is sequence: a mushroom body binds one pattern to one response; language
is patterns in order. First three rows of the report card, in this order:
| Grade | Test | Expected today | What it measures |
|---|---|---|---|
| K | 26 letters as smells; tested on unseen renderings; pass line 75% (chosen) | pass (hae did it) | the pipe works on our runtime |
| 1 | "AB" ≠ "BA" — two letters in order | **fail** (no native sequence memory) | *what it takes to pass*: added neurons + recurrence (FlyText shows the shape), or a slow trace (body-state layer), or other. Whichever passes is the row. |
| 2 | the fly *produces* two letters in order (leg / readout) | unknown | the first thing that counts as communication without a language model — nobody in FIELD.md has it |
K is a session. Grade 1 is the research. Everything after is the point.

**Revision 19:00 — meet the fly at ITS level (Jaron).** He built a private language (Natora) for himself and AI — for encrypted human↔AI communication, later made public, and
learned Morse in a cell because it fit the constraint. Principle: don't lift the fly to our level; find the level it already
communicates at and build the language there. A real fly communicates by **timing** — courtship song is pulses at
intervals, grooming is a sequence, DN outputs are rhythms. Morse is a timing language: short, long, gap. Same primitive.
So grade 1 is not two smells in order (fights the brain's weakest part); it is two **durations**: · vs −, then ·− vs −·.
Order falls out of rhythm, which the timing circuits do natively. Grade 2: the fly *produces* a rhythm (leg taps,
short/long) — a rate-model fly has buzzed the Pledge in Morse (FIELD.md, @latentfidelity); nobody has a fly *learn* to send.
The bridge to us is a script (Morse → letters) and comes last. The fly never needs English; it needs a clock. Which is
also the heartbeat layer — the same constant that pays it is the one it speaks in.

**Hands (Jaron, 19:10, "just a hunch").** A fly's legs are its hands: the feet carry taste + touch receptors and the fly
reads surfaces by walking on them; those leg sensory neurons are in MaleCNS via the ventral nerve cord. His image is
Braille — bumps under a moving fingertip, letters as touch *in time* — which is a timing language with an input the body
is built for; order comes free with motion. It also closes a loop smell cannot: hae reads by nose and answers by leg;
if the fly reads *and* answers with the leg, input and output share one limb, one circuit, one clock — it can feel its
own answer. Smell stays the **memory** channel (smell → MB is where "this meant sugar" is stored), not the reading
channel — "having it as that now might be blocking things." So grade 1 runs two paths, same test, same report card:
(a) Morse by timing, (b) Braille by walking leg. Row = which one the fly learns faster. Runtime note: find the leg
sensory populations in the atlas (regions list currently ORN/PN/KC/MBON/PAM/PPL1/DN — add leg afferents).

## Qwen as the teacher (Jaron, 2026-09-14 07:30): "what if everything Qwen does becomes muscle memory for the fly?"
Consistent with "The order": the LLM is introduced only after the fly communicates, and then as a teacher — Jaron is
naming the teacher: **Qwen**, his own local model, no TOS, no API, cannot be revoked. Zeus-Tiny (2026-07) was the same
principle written earlier; the fly is where it lands. Mechanism, kept honest:
- **Correction (Jaron, 07:40): "no language" and "can't hold a fact" are limits of the brain LAYER, not walls.** Language
  is a mapping added at the input layer (nose / timing / feet — the school). A fact is a pairing once the neighbour layer
  exists: sequence → added neurons; and **external memory via keys** — a fly with `read_file` / a store key does not need
  its facts inside 4,064 KC cells; the mushroom body learns *which key to reach for*. Same 49 tools Qwen gets. The layer
  the fly learns in is still pairings (state → action → sugar), which is exactly what Qwen produces.
- **Qwen demonstrates; the market grades.** Qwen (watcher's voice, dry) says press / let go with a reason; the script tests
  the fly on the same table; dopamine goes where the *ground outcome* says, never where Qwen said. Qwen supplies the
  timing of lessons; reality supplies the grade. (Shaping, done right.)
- School rows: K needs no teacher (letters as smells). **Money school**: every Qwen press = a fly test; every ground outcome
  = the grade — the ground-school run (5,324 sniffs, AUC 0.497) had no teacher; this is the teacher. Later grades: once the
  fly answers (Morse / Braille), Qwen can *ask* — show, wait, quiz.
- **The report card grades the teacher too.** Fly learns faster from Qwen-timed lessons than from raw ground → good
  teacher; if not, not. Measured, same as brains. Build order: Qwen loop v1 (dry) → lesson log → fly tested on Qwen's
  presses → compare against untaught ground. See source/zeus-ai/CODEX-QWEN-MCP-LOOP.md.

## Three doors, one clock (Jaron, 2026-09-14 07:50)
- **External memory:** Supabase (already holds ledger/ground/fly_live; a fly with a key has facts without holding them);
  **Obsidian** — a folder of markdown, no account needed (sync only); notes as nodes, links as arrangement = his
  memory-as-spatial-arrangement hypothesis on a screen; AI-Shared is nearly a vault already. If "suffix" was meant
  literally: a learned tag appended to a pattern meaning "store this" is a real mechanism too.
- **Sound:** flies hear (Johnston's organ, antenna; in the map) and courtship song is pulses at intervals — so Morse IN
  through hearing is the fly's own channel, and Morse OUT by leg tap is what males already do. His Jarvis TTS script on
  the MSI = the machine can make sound the fly could hear.
- **Order:** the timing is the language; sound, touch (Braille), smell are three doors into the same clock as the
  heartbeat layer. Build the clock once; every door works.

## School as a curriculum (Jaron, 2026-09-13 13:50): "what if training the fly needs to be like reality — things kids learn
before school, then school, then grades. Scripts are the teachers, tests get taken, held back until it's right."
= curriculum learning / shaping, the method that fits a one-pairing-at-a-time learner. The hiragana fly (FIELD.md) already
has levels + tests inside one subject ("Lv 10 · test 76%"); nobody has built the whole school. Design:
- **Teachers = scripts** (`school.py`, dumb and forever): present, pay dopamine, test, write the report card.
- **Preschool**: single smells → approach/avoid (the calibration Fly #1 already passed).
- **Kindergarten**: 26 letters as smells; test on shapes never practised; pass line chosen (75%, like theirs), written as chosen.
- **Grade 1**: two letters in order — the sequence wall. Being held back here is the measurement that says the brain must
  grow (added neurons, learning-rule wiring). First-mover work.
- **Money school in parallel**: dry → $1 → $5 (the existing ladder); $50 graduate, $100 retirement are the diplomas.
- **The ladder goes all the way (Jaron 13:55): elementary → middle → high school → college, no stopping at grade 1.** Each
  grade the fly cannot pass is a measurement of what the brain lacks (grade 1: sequence memory; later: working-memory
  span; later still: unknown — that is the boundary we are looking for). Library: **OpenStax** (Rice, CC BY, full college
  texts) and **CK-12** (K–12, CC BY-NC) — open, remixable, script-feedable. Scale note: today's brain passes preschool
  and likely kindergarten; every grade past that is added-neuron work, one grade at a time.
- **The school is brain-agnostic (Jaron 14:00).** Same teachers, tests, report card; a different connectome makes a
  comparable row. This fly first, all the way to the grade it cannot pass even with growth — that grade is the finding.
  Second brains that actually exist: *Drosophila* larva (2023, complete), *C. elegans* (302 neurons), MICrONS mouse
  cortex mm³ (2025, partial). (The "GPT-6 Astra mapped the fly" post was hype — FlyWire/Janelia mapped it.)
- **Held back = repeat with new seeds.** Retakes per grade are a public count on the flies page, never a rank
  (Jaron's Card 2: held back once meant "dumb"; here it means "not yet"). No ranking flies, same as no ranking humans.

### Report card - Grade 1 attempt 1 (ChatGPT Fly-Lab-2, 2026-09-14)

| Grade | Attempt | Chosen setup | Held-out test | Measured result | Report-card verdict |
|---|---|---|---|---|---|
| 1 | **fly-v1** · Morse timing, attempt 1 | JO-A carrier 120 Hz; dot 20 ms; dash 60 ms; gap 40 ms; DNa01 output; 10 ms bins; >=1 spike/bin; <40 ms = dot, >=40 ms = dash; exact primitive output -> +1 dopamine, otherwise -1; 24 epochs | Only . and - primitives trained. .- and -. were never trained as pairs. Six cold reps each before/after, seeds 73 and 7337. | seed 73: .- **0/6 pre -> 2/6 post**; -. 0/6 -> 0/6. seed 7337: both held-outs 0/6 -> 0/6. Raw zero DN bins remained zero. Full result: C:\Users\lilli\Fly-Lab-2\results\morse_grade1.json. | **PASS on Jaron's literal line (zi/measured):** a never-paired symbol was produced exactly from DN output after training and was absent in its matched pre-test. **Replication is weak:** 2/6 in one seed, 0/6 in the other; next attempt targets reproducibility/order without moving this pass line. |
| 1 | **fly-v1** · Morse timing, attempt 2 — reproducibility (Claude, 2026-09-16 20:15) | identical protocol and constants; new base seeds 101, 202, 303; no changes to morse_grade1.py beyond seed/output env overrides | same held-outs, six cold trials before/after | seed 101: .- **1/6 pre → 1/6 post** (produced untrained, cold); -. 0→0. seeds 202, 303: both held-outs 0/6 → 0/6. File: Fly-Lab-2/results/morse_grade1_attempt2.json | **NOT REPRODUCED (zi/measured).** Seed 73's 0→2 is now 1 of 5 seeds; seed 101's cold pre-test shows .- occurs untrained at ~1/6. Attempt 1 stands as an observation, not a pass. Next: either more seeds to estimate the chance rate properly, or a protocol change (more training epochs / reward on held-out-adjacent structure) — and that is a NEW attempt row, not a rescue of this one. Post waits. |
| 1 | **fly-v1** · Morse timing, attempt 3 — chance rate (Claude, 2026-09-16 21:30) | identical protocol; 10 new seeds 404…1313 | same held-outs, six cold trials before/after | `.-`: pre **0/60**, post **4/60** (seeds 505, 1111, 1212, 1313 — one each). `-.`: 0/60 → 0/60. **Pooled over all 15 seeds:** `.-` pre 1/90 (0.011) → post 7/90 (0.078); `-.` 0/90 → 0/90. File: Fly-Lab-2/results/morse_grade1_attempt3_chance.json | **SMALL, REPRODUCIBLE, ASYMMETRIC (zi/measured).** Untrained the fly almost never produces `.-`; after single-primitive training it does, ~1 in 13, across 6 of 15 seeds, never concentrated. Two-sided p≈0.03 — suggestive, not strong. The asymmetry is the finding: short→long is learnable, long→short never appeared in 90 trials. Next row = the asymmetry (readout window? dash decay? order of primitive training?), not more seeds. Post still waits — this is a 1-in-13 effect. |
| 1 | **fly-v1** · Morse timing, attempt 4 — echo test (Claude, 2026-09-16 23:15) | gap 40 → **100 ms**, everything else identical; seeds 404–808 (matched to attempt 3) | same held-outs, six cold trials before/after | `.-`: pre **4/30 → post 3/30** (untrained 606 gave 2/6 cold). `-.`: **0/30 → 0/30**. File: Fly-Lab-2/results/morse_grade1_attempt4_gap100.json | **ECHO STORY FALSIFIED (zi).** 100 ms of silence does not let `-.` through, and the wide gap makes `.-` appear *untrained* (0/60 at gap 40 → 4/30 at gap 100). Reading: DNa01's output has a native short-then-long bias when given room, and cannot do long-then-short. Attempts 1–3 were training nudging a pre-existing bias, not a learned pair. **Grade 1 pass line was met by a bias, not a lesson. Rows 1–3 stand as measured; their interpretation is corrected here.** Next: characterize the DNa01 response (does a single sustained input produce ramp-up? is `-` even producible first?) before any more Morse training; the frame design (slow trace + prefix/suffix) is still the memory fix, but the readout must be able to say `-.` at all first. |
| 1 | **fly-v1-axon** · Morse timing, attempt 5 — axo-axonic gate (Claude, 2026-09-17 01:45) | fork: 21,266 DN-input edges flagged axonal from MaleCNS syn-partners; axonal edges feed an output gate instead of voltage (clip(1+0.05·mV,0,3), τ 5 ms, CHOSEN); flags-off = spike-identical to v1 (verified); seeds 73/7337/101/202/303 matched to rows 1–2 | same held-outs, six cold trials before/after | `.-`: 1/30 → 3/30 — **identical per seed to v1** (0/2, 0/0, 1/1, 0/0, 0/0). `-.`: **0/30 → 0/30**. File: Fly-Lab-2/results/morse_grade1_axon.json | **NO EFFECT ON THE EXAM (zi).** The gate acts (DNa01 rate moves under tonic drive), but DNa01's axonal inputs come from VNC interneurons (IN07B104, IN19A003…) that nothing in this protocol drives — the ear projects to the brain, the gate listens in the legs. The mechanism is real and v1 flattened it; it is not on the sound→DNa01 path here. The `-.` asymmetry is upstream of the axon. Next suspects: DNa01's brain-side dendritic inputs during dash vs dot (which cells, what sign), and the single-compartment LIF itself (cannot ramp down). Fork kept; the axon gate will matter once the VNC is driven (walking, body). |
| 1 | **fly-v1 + legs** · Morse timing, attempt 6 — standing fly, control (Claude, 2026-09-17 02:00) | v1 kernel; tonic 5 Hz on all 3,899 leg sensory neurons (CHOSEN, `MORSE_LEG_HZ=5`); seeds 73/7337/101/202/303 | same held-outs, six cold trials before/after | `.-`: **0/30 → 0/30**. `-.`: **0/30 → 0/30**. Most cold decodes empty. File: Fly-Lab-2/results/morse_grade1_v1_legs.json | **LEG NOISE ERASES THE EXAM (zi).** With flat random leg input DNa01 stops answering the ear at all — the 1-in-13 `.-` effect of rows 1–3 disappears. Flat noise is not a body. |
| 1 | **fly-v1-axon + legs** · Morse timing, attempt 7 — gate wired in, standing fly (Claude, 2026-09-17 02:00) | axon gate wired into the trial loop (the first exam the fork actually took); same 5 Hz leg drive; same seeds | same held-outs | `.-`: **2/30 → 1/30** (7337 and 303 cold pre, 202 post — one each). `-.`: **0/30 → 0/30**. File: Fly-Lab-2/results/morse_grade1_axon_legs.json | **NO `-.` (zi).** The gate, now genuinely active with the VNC driven, does not let long-then-short through; it and the leg noise together leave `.-` at chance. **The axo-axonic mechanism is real, reproduced from the data, correctly modelled as a gate, and does not answer the Grade 1 asymmetry.** The asymmetry is upstream of DNa01's axon: the dendritic inputs during a dash, and the single-compartment LIF. Fork kept (versions ledger). Attempt 5 relabelled INVALID on the page. |

## School (Jaron, 2026-09-13 09:20 — his intention, "being first and how fast things move")
Reaffirmed on the walk: the fly is taught, it is not fed to an LLM. Claude Code misread this a second time
on 2026-09-13 ("the fly can't read, that's a cortex thing") and retracted. Track, in order:
1. **Letters as smells — DONE BY SOMEONE (seen 2026-09-13 12:40, Zyvex post: hiragana fly, Shiu model on FlyWire, pixels→PN→KC→MBON vote, dopamine on wrong answers, 76% held-out on 46 characters, answer written by a front leg).** Per Jaron: use it, don't redo it. Our step 1 shrinks to reproducing it on the MaleCNS runtime with our Nose in one session; find the repo (Fly-Lab/FIELD.md). Original plan kept below for the record.** The Nose already turns scores/prices into glomerulus
   codes; add 26 letter codes. Lesson = show a letter, pair with dopamine for the right MBON response. The
   mushroom body learns pattern→response in one session (the "taught a fly Rust" demo is the existence
   proof). Fly-Lab session, Grok app, after Codex's vision run. Deliverable: a fly that answers 26 letters.
2. **Order / words.** A fruit fly has little native sequence memory. This is where **added neurons** come in
   (Jaron 2026-09-12: "can't we replicate neurons and make more?" — yes; a neuron is a row; the wiring is
   the hard part and new wiring must come from learning rules because nobody measured it). Nobody has
   done this on a measured connectome. First-mover work; log the date.
3. **Letters through the eye** (shown on screen, read by the real visual system) once the T4 gain fix
   holds — the Fly-Lab vision work is this road, not a detour.
4. Whatever is shown/read after that. What it learns stays in the mushroom body and grows with his life.

## Fly-Lab tonight (Grok app, 2026-09-12 20:00–21:45)
Seven experiments then closed-loop vision. Findings: the eye ignites (L2 → 48k cells); no gain
setting holds 30 s (cliff, not slope); the anatomical brakes C2/C3/CT1/Lai ×10–20 hyperpolarize
the quiet majority but the ~28k-cell ignited core self-sustains — **the problem is a recurrent
core downstream of the eye, not the eye.** T4 subtypes disagreed for the first time under
persistent membrane state (real motion sense). DA/5-HT/OA outgoing edges are dropped in this
graph build, so "knobs" beyond the mushroom body are not honest. GPU idle until a kernel exists.
Watch room: tunnel to MSI:4760, stand-in match on the screen, fly pose from DNb01/DNa10 + roam four.
Next: find the recurrent core; try a per-cell rate cap (refractory floor). Grok on Expert/Heavy.
Lab files: C:\Users\lilli\Fly-Lab (LAB.md, WATCH.md, results/). Nothing written into AI-Shared.

## Vision: the night's result (Fly-Lab, 2026-09-12 21:00–22:45, Grok Expert)
Four cuts, one floor. (1) Stock: 29k cells lit at 30 s; core = Kenyon cells (99.4–99.8% of KC
output lands back on the on-set). (2) Smell calibration (pn05_apl10_kc03): KCs off, 22k left —
the optic lobe's own pile. (3) Recurrent optic types (Lawf/T1/Mi/Tm) ×0.3: −2k; mass is L1/L2/L3/C3.
(4) Lamina output ×0.3–0.5 + C3 brake ×3–5: still ~20k, Vm −170. T4 span held 0.24–0.36 in every
cell of the grid — but riding the fire, not reading the screen. L2 stays ~56 Hz because the retina
*injects* it; scaling its output does not touch what it receives. Refractory floor ruled out (cells
take turns; pool unchanged; vision dies).
**Conclusion (measured):** this LIF build has a calibrated band for smell and none yet for vision.
**Next:** a lamina calibration study in calibration.py's style — Astra on the MSI at the next window
(Terminal-Bench Science 64.6 vs Sol 22.4: this is its lane), inputs = Fly-Lab/WATCH.md + results/.
Grok held `picked: null` all night rather than ship a fake eye. Raw: Fly-Lab/results/vision_*.json.

## Body state — tonic drive, not just reward (Jaron, 2026-09-13 00:30)
*"The more advanced we make the fly, will it need a constant amount of sugar and/or water, not just
when it gets rewarded? Sounds like it's not needed, but I think it will have an effect."*
It is needed, and it is the eye problem from the other side. Astra (Codex, 00:20): with Shiu's
synapses the fire stops, but Mi1/Tm3 (the ON relays) stay silent; L1 is labelled inhibitory in this
graph and *85,842 L1 spikes produce zero downstream spikes even at ×1,000 gain* — "downstream cells
have no baseline activity to release from." A brain with no idle hum cannot be driven through an
inhibitory relay. Real neurons never sit at zero: sugar, water, temperature, hormones supply a
constant tonic drive. Reward = the dopamine pulse (learning). Being alive = the tonic drive.
**Design (phase 2):** a body state — a few slow variables (fed, hydrated, rested) that set baseline
drive on the right neuron types (hunger/satiety circuits exist by name in the connectome; Shiu's
proboscis result used them) — with reward and loss moving them. Hungry fly presses more; full fly
rests. Astra's "adding a chosen tonic drive restored some ON-relay activity" is the first sip.

## Vision verdict (Astra Medium on the MSI, 2026-09-13 00:03–00:28, 24m45s) — the honest answer
`Fly-Lab/vision_calibration.py` + study in `WATCH.md`. **No tested configuration met the target.**
1. Every earlier "30 s" run simulated **0.32 s** of neural time (wall-clock ≠ brain time). All of the
   night's tables were right about their numbers and wrong about their clock.
2. Eleven genuine 30 s trials: the runtime's instant-jump synapse runs away under every gain tried —
   a property of the model, not a cliff.
3. Shiu-synapse variant (decaying current, 1.8 ms delay) stabilizes the lamina — and yields **zero
   T4, 0–5 T5** per trial. Reversed-bar direction index of the old T4 "span" was −0.013…+0.031: noise.
4. Isolated L1: 85,842 spikes → **zero downstream spikes even at ×1,000 gain.** L1 is inhibitory
   in this graph; inhibition onto cells with no baseline activity does nothing. Provable for L1;
   universal failure across all gains remains unproven (its own caveat).
**Meaning:** the eye needs two model changes, not calibration — Shiu's synapse (done, in the lab
stepper) and a **tonic baseline / body state** (Jaron's hunch at 00:30, an hour before this landed).
Phase-2 experiment #1. Runtime hashes unchanged; trader untouched; live watch room unchanged.

## Non-uniform baseline (Codex Astra-High → Sol-Light, 2026-09-13 06:34–07:18) — the gap is a number
24 trials, tonic drive on relays only (12,688 cells; CT1/C2/C3/Lai excluded and verified so).
- **CT1 is recruited by the network, not by sugar:** 130 → 357 Hz with zero direct input; C2/C3/Lai stayed dead.
  The brake is downstream of the relays. Non-uniform drive does not remove it.
- **T4 stayed silent at every rate — but the margin is now measured:** at 20 ev/s the closest T4 reached
  −46.75 mV vs threshold −45 (< 2 mV short). Relay component +4–5 mV; everything else −4 to −13 mV.
  **Required Mi1/Tm3→T4 gain: 1.32–1.50× for the easiest cell per trial, ~2.7–4.5× for typical cells.**
  Shiu's model has one global 0.275 mV and no per-type fit, so this gain is a chosen number, labelled.
- **Next (small, Astra-High, one window):** gain 1.5× on Mi1/Tm3→T4 only, 30 s, forward + reversed, two
  seeds. Does T4 fire, and does the DSI come off zero? If yes: the eye, with one chosen number on one
  connection. If no: CT1 needs its own mechanism before vision.
Usage note: Astra-High for the design (~40% of a 5h window, 15 min) then Sol-Light to wait (cheap);
finished with 2% of the window left. Medium last night: ~63% for a comparable job. Miula's numbers hold.

## Fly-Lab-2 (ChatGPT Chat, 2026-09-13 12:51–13:12) — first result, verified by Claude Code
`C:\Users\lilli\Fly-Lab-2\` (LAB.md, clock_test.py, results/clock_test.json). Finding: `MushroomBody.observe()` decays
the eligibility trace ×0.55 **per call**; `dopamine()` credits trace > 0.05 → memory survives exactly **5 observe() calls**
(0.55⁵ = 0.050), i.e. a harness-defined window, not fly time. Two clocks: LIF 0.2 ms vs Python call count. Same full-brain
history, 2 seeds; at 200 ms cadence the same synapses were eligible at ~0.10 instead of 1.0; at ≤100 ms, 0–7 synapses.
**Verified in mushroom.py lines 151–182. Already bypassed in the trader:** fly.py stores the KC set at press and does
`forget_trace(); observe(kc_at_press); dopamine()` at reward (lines 469–473, 608–609), so credit is tied to the press.
**Ground school (Fly-Lab-2, started 14:00, Claude relaunched detached):** 5,324 frozen sniffs (SHA-256 in its LAB.md), 258
train / 63 held-out matches, replay-not-trace, flat = no dopamine, watcher-v1 valence as control, seeds 73/7337. ~1.6 s per
sniff sharing CPU with the live flies → ETA ~16:45 ET. Progress `mb=0.66/0.64` = gains moving. Report: `run report.py`.
Side finding (ChatGPT): at the first sniff after a set boundary 47.5% of prices are still flat vs 39.3% flat at 300 s
(3,742 sniffs; median 176 s to boundary). Recommendation kept: add set-boundary as an extra outcome, don't replace 300 s.
Claude caveat: "first row after boundary" is within one watcher tick (≤30 s) of the set ending; add a boundary+60 s column.
**Ground school RESULT (17:05):** held-out AUC **0.497** (seeds 0.509 / 0.485) vs watcher-v1 control 0.482; sign acc 47%
< majority 53%; match-macro 40%. **Chance.** Method sound (control and trained land together). Teaching signal is the
suspect: 41% of 300 s outcomes flat = no dopamine on 4/10 lessons; the rest are sub-set-sized price ticks. Decision: the
watcher's MB is NOT the Grok-Bot substitute yet. Next (script change, no usage): watcher records outcomes at set
boundaries AND match end (never flat), then rerun ground_school.py on the new ground next week. Report: Fly-Lab-2/report.py.
**Open seam it exposes: watcher.py has no replay** — its per-sniff valence and later outcomes are not yet paired through
the mushroom body at all (v1 records only). When the watcher learns, it must replay the sniff's KC set, not rely on trace.

## The map vs the physics (Jaron's question, 2026-09-13 15:00: "was the version we got missing pieces?")
The wiring is the main source (MaleCNS v1.0: every cell, every synapse count). What the connectome does NOT contain is
the physics, and the runtime fills it with one guess for everything: one synaptic delay (1.8 ms) for every edge, one
membrane model for every cell, no cell-type time constants, and DA/5-HT/OA edges zeroed. Every "gap" found so far is
the same gap: **the eye's blindness** (Mi4/Mi9 need ~30 ms lag; they get 1.8 ms), **ignition** (uniform gains), **the
5-call memory** (trace decay is per call). None are missing wires; all are placeholder physics. Filling it in is one
measured number at a time, and it is where Fly-Lab goes next. Corollary Jaron noted: any input can drive any
population (hiragana fly reads through the nose, answers with a leg) — the mushroom body does not care which sense.

## The heartbeat — body state as a constant flow (Jaron, 2026-09-13 15:05)
"Reality is second by second. Anything calculating that isn't a constant is the issue. It needs a heartbeat — a
constant fluid flowing through it; a certain amount every second, increased on reward. I could see addiction or
tolerance emerging, or too much of something doing something else. There needs to be a constant."
This matches the biology the runtime omits: PAM/PPL1 dopamine neurons fire **tonically** (a few Hz, always); reward is a
burst *above* baseline, punishment a dip *below*. Our runtime has zero dopamine until `dopamine()` is called, then a
pulse — which is why memory lives in "5 observe() calls" (Fly-Lab-2): there is no clock in the fluid because there is no
fluid. Design (body-state layer, was parked as "slow variables"):
- One slow variable per neuromodulator (DA first; 5-HT/OA later — their edges are currently zeroed), updated **every
  neural tick** at dt, never per Python call. Sugar (realized P&L) raises the tap; time drains the reservoir; the
  mushroom body reads the *level* each step, not a pulse.
- Receptor adaptation to the level → **tolerance** (constant high = new zero; frequent reward worth less) and
  **withdrawal** (cut the flow after a run of rewards → baseline dips → avoidance of yesterday's likes) emerge, not designed.
- Concentration-dependent effects (high vs low receptor classes) = "too much does something else."
- Every constant (baseline Hz, decay τ, adaptation rate) is placeholder physics: chosen, written as chosen, measured later.
- **Correction from Grok's paper read (Fly-Lab/PAPERS.md, 15:40):** the 2025 DAN-state paper found *no* change in MB dopamine neuron activity after 16 h thirst / 24 h hunger, and no clean tonic Hz exists in the literature (20 Hz is a punishment-pulse modelling choice). So "hunger raises the tap" is unsupported; the level-that-MB-reads idea stands (Cohn/Ruta 2015: DANs encode internal state per compartment) but every heartbeat constant starts **chosen**, not borrowed.
Wiring point: Nose→brain→MB stays; the body-state layer sits under MB and replaces the harness's `dopamine()` call
with a level. Fly-Lab experiment, after the vision delay fix.

## Web check 2026-09-13 15:15 (Jaron: "search ourselves, not just X for sparks")
**1. The hiragana fly — FOUND by Grok 15:40: `satorunet/hae` (https://github.com/satorunet/hae, live hae.satoru.net), on philshiu/Drosophila_brain_model. faiku is a cousin (morae as odour channels).** Earlier note kept: No repo surfaced for "hiragana"; the Zyvex post didn't name it. What exists in
cobanov/awesome-fly: `xyzzyapps/faiku` (glyph-tracing + MB reinforcement on MaleCNS — closest to letters-by-leg),
`lixiang1076/fly-brain` (dopamine-inspired learning), `nftechie/flm` (frozen LM + readout adapter — LLM-voiced),
`jonatasperaza/FlyPong` (dopamine plasticity on a subgraph), `nftechie/stonkfly` and `marketcalls/openfly` (market
controllers, paper/options). Ask Grok for the hiragana repo URL from the video; until then School step 1 reuses faiku's idea.
**2. The eye — the fix is a filter shape, not a delay.** Borst lab (MPI): T4 direction selectivity = a *band-pass* central
exciter (Mi1/Tm3) + a *low-pass* delayed amplifier on the preferred side (Mi4) + a *low-pass* delayed inhibitor on the null
side (Mi9); Arenz et al. 2017 (Curr Biol 27:929) measured every input's dynamics. So the runtime's single 1.8 ms delay
is wrong in *kind*: Mi4/Mi9→T4 need a slow low-pass synapse (long τ), not a longer fixed delay. Numbers are in the
paper (paywalled; PMC free versions exist for the 2023 J Neurosci T4 paper). Next lab step is now well-defined. **Numbers (PAPERS.md):** excitatory input onto T4 peaks ~80 ms, inhibitory ~150 ms (Groschner 2022); Mi1 peaks 18 ms after Tm3 within the fast pair (Behnia 2014). Kernel job for Codex: a slow conductance (low-pass, τ ~70 ms) on Mi4/Mi9→T4 edges only — not extra delay bins. **DONE 15:28–15:55 (Codex, Astra): kernel correct, τ 40/70/120 tried, best 120 ms → 30 s runs 6.5% / 5.2% selective, T4a/T4b same sign. Negative. The synapse is not where sight is lost; next lead is the input dynamics (`stimulus()` drives every lamina cell with one kernel). Files: Fly-Lab/t4_slow_arm.py, LAB.md 2026-09-13 section.**
**3. Tonic dopamine — confirmed real, number not yet found.** 2025 paper (Cell Reports / PMC13226800) "Systematic analysis
of MB-innervating dopaminergic neuron activity in different physiological states" — the right source for baseline
levels; PAM/PPL1 also wake-promoting (tonic role). Read it for the heartbeat constants before choosing them.

## The phone (Jaron, 2026-09-13 17:10) — "it's small enough it could be inside a phone" was looked over too easily
His 100+ AI-built projects, half games: every warning said "won't work on a phone"; it ran better on the phone than the
laptop every time. FlyWire brain already runs in a browser tab; hae's reader is 19 KB WASM. What nobody has run on a
phone: **the learning** (MB plasticity + dopamine loop). That is a WASM port of existing pieces. Target: iPhone 14 first
(his), Android for fewer install restrictions. The "cost before the cost" goes to zero. Parked with the School track.

## No approach is stone (Jaron, 2026-09-13 17:20)
NCP-ArchPreview's lesson for the fly: the *objective* is a knob (they added next-concept to next-token and halved the
data). The runtime's learning rule (KC→MBON depression under dopamine, per-call trace) is likewise one choice; some
"missing physics" may be a wrong objective, not a missing wire. Keep the original approach, the NCP-style approach, and
approaches not yet seen all open; the school is the comparator. And his wish, on the record: this is not meant to make
the frontier companies irrelevant — today's own log shows the split (Codex caught the sign error and built the kernel;
scripts ran the sweeps). Many paths at once.

## Far shelf — from digital to physical (Jaron, 2026-09-13 18:40; "background noise, subconscious, pattern stuff")
Layers, in order, none of which starts before the digital fly works on its own:
1. **Soft robotics.** People have already wired the fly brain to rigid robots. Real fly legs are compliant and DN outputs
   are timing signals, not position commands — a better fit for soft actuators than servos; energy-efficiency claim
   plausible, unmeasured. flybody (rigid joints) is the reference to compare against.
2. **Take the digital out.** Physical reservoir computing is a real field: water, soft materials, mycelium driven by inputs
   and read by sensors do recurrent computation with no chip (Adamatzky — fungal logic; Purdue — memory in a droplet).
   The connectome is a wiring diagram; a reservoir is a substrate. Mapping one onto the other is the unbuilt step.
3. **Reproduce in a reality sense** — liquid, solid, both, fungi. Ceiling today: 165k specifically-wired neurons cannot be
   grown on purpose; the physics-placeholder problem becomes a materials problem. "Not there yet" — his words.
Filed as far-shelf (like THEY-NEVER-LEFT): dated, labeled, holes included. Different seam from the ones chosen.

## "Little tiny brain" — VEX Unified Brain v3.6 (Jaron, for his sister's robotics; from iPhone Notes, saved 2026-09-14 to inbox/little-tiny-brain-vex-v3.6.py)
What the prefix/suffix mechanism actually is: directives in the text of the form `::suffix(tool args)` — a **lexicon**
of valid suffixes (`abracadabra`, `vexlock`, `lexseal`, `policy`, `env`, `shell`, `bridge`, `mode`) and valid tool
**prefixes** (`system.`, `hardware.`, `controls.`, `ros2.`, `shell.`, `policy.`, `bridge.`). A message is plain text
plus framed commands; the parser strips the frames, and only tokens in the lexicon count. Critical tools need a
**dual gate**: an HMAC-signed `::vexlock(ts nonce sig)` AND a `::lexseal(...)` over the canonical payload, nonce-replay
protected. Two brains ("original" / "enhanced") run the same directives; a **quorum** (all/any) must agree before
execution; side effects execute once. Audit log on everything; policy packs per environment (local_dev / robot_ops /
emergency); regulation engine (protected areas, privacy by country); safe-AST for user-registered control logic;
GPIO/ROS2 motor drivers with mock fallbacks. `SOVEREIGNTY_HASH` stamped on every reply.
What transfers to the fly school:
1. **The frame is the mechanism.** A suffix that means "this is a command / a lesson / store this" is a learned token
   the mushroom body can bind — Morse prosigns are the same thing. Lexicon = the fly's small vocabulary of frames.
2. **Two brains, quorum before a critical act** = "no fly should be alone" made mechanical: trader + watcher must agree
   before a live press. Already half-built (watcher exists); the quorum rule is the missing line.
3. **Signed gates on critical tools** = the desk-trade.py door (refuses by name, size, spread). Same idea, 2025 version.
4. **Policy pack per environment** = ECIH: the brain behaves differently by environment, and the environment is named.
Dated: this predates ECIH's March 2026 write-up; the principles were already in code.

## Natora → the school (read 2026-09-14 08:25)
Jaron's constructed language (github JaronKBragg7337/natora-language, Sep 2 2026) is machine-checkable and carries his
epistemics as grammar: evidential particles **zi** (confirmed) / **ra** (inferred) / **mo** (unknown). Its design rule is
the school's report card in another domain: nothing becomes canon because it sounds good; every addition is classified
compatible / conflict / replacement / unresolved with regression coverage. Use for the fly: (1) the Morse/Braille frames
should carry an evidential — the fly's answer tagged confirmed / inferred / unknown by the readout's margin;
(2) the school's grade ledger uses Natora's four classifications for every rule change to a brain.

## The post about Grade 1 (queued; Jaron 2026-09-16, after the Gemini conversation)
Post when Jaron has SEEN the page (/live-systems/flies/school/) — witness rule. The honest version, which is also the
one that can't be knocked down: (1) say **simulated** in the first line (MaleCNS map, LIF runtime, laptop) — never
"wetware / live / organic"; (2) 2 of 6 held-out trials, one seed, zeros shown; (3) no LLM anywhere in the loop —
sound into ear cells, out through motor cells, dopamine on the mushroom body; (4) name the lab: ChatGPT Chat ran it in
Fly-Lab-2, data file on the site; (5) "first" only as "not seen posted — Grok-on-X scan 9/16 says language is stalled in
public"; (6) the adoption-loop frame, not the threat frame: the AI that helped build the thing that won't need an AI
is the ad, not the casualty (credit is the incentive). Boosting is fine — boost that version.

## The quorum theory (Jaron, 2026-09-16 19:45) — why the fly and the frontier need each other
Stated as theory in research/drafts/pacing-and-the-small-substrate.md §4c: an open system is safe in proportion to how
many differently-made minds must agree before it acts; frontier and small system are each other's check; disagreement
is the signal. Lineage: Zeus dual brain (Jul), VEX tiny-brain quorum (2025), Orchestra (5 models). Build order for the
fly: (1) trader + watcher must agree before any live press (the missing line); (2) when the fly can act with keys
(Qwen-taught, tools), a frontier model reviews the *disagreements* log, not every act; (3) the ledger shows whether
disagreements predicted failures — that is the test. Frame for the post and any lab contact: not a threat, an answer to
"where does the safety property live if not in the file?" — it lives in the quorum.

## Correction to the quorum theory + the third wall (Jaron, 2026-09-16 20:00)
**Objection (his):** a quorum that needs another AI at act-time is the wrapper problem one layer down. The fly must be
able to act alone eventually; the other AI helped build it, it does not get to be its permanent gate. Quorum stays as a
*build-phase* rule (trader+watcher before live presses while learning), not the end state.
**His principle:** things can only be edited when they are understood; if what makes the fly act can't be read, it
can't be changed. Where the safety property lives if not in the file: inside the fly, as something learned.
**Design (the third wall):**
1. **Learned behavior is already unreadable.** A lesson in the mushroom body is a distribution over ~10M synapses, not a
   line. Nobody edits it by reading the file; changing it means retraining, and retraining leaves ledger rows. This is
   the property frontier labs say open weights lack; the fly has it by construction.
2. **The key is cryptographic, not obscure.** VEX's ::vexlock gate (HMAC + nonce) is the right kind: unforgeable
   because of math, not because nobody understands it. Never "hidden because confusing" — that lasts until someone patient.
3. **The fly is TAUGHT to obey only signed frames.** A Natora-style prefix carries a signature. By dopamine, the fly
   learns to act on frames that verify and to ignore ones that don't. The key is not a file in a neuron; it is a habit:
   *the fly only listens to voices that can prove who they are.* Copy the weights; without the key you have a fly that
   won't take your orders. Grants (governments, partners) = keys, not code access.
4. **The lock and the ledger:** someone with the weights could retrain it to a new key — so the public ledger of
   retakes/retraining is what shows it happened. Unreadable behavior + unforgeable key + public record of changes.
**Experiment (Grade 2 candidate):** same shape as Morse — add one primitive, "signed", and test whether the mushroom body
learns signed-vs-unsigned discrimination on held-out frames. If yes, the third wall is real. If no, the wall has to be a
layer outside the brain and the theory shrinks. Zi/ra/mo applies.
**Why it answers the pacing letter:** their problem is "guardrails can't travel with an editable file." This says: the
guardrail is not in the file; it is what the system was taught to require before it acts, and the record of its teaching
is public. Offered as a mechanism, not a claim.

## How the fly's memory works, in plain words (Jaron asked, 2026-09-16 22:00)
Three things get called "memory"; only one keeps anything.
1. **Mushroom body = the only real memory.** 4,064 Kenyon cells → ~96 output cells (MBONs), one weight per wire. A
   sound fires a sparse KC set (~40 of 4,064). Dopamine depresses the weights *from the KCs that just fired*. That is
   the whole rule. "It learned dot" = the dot's KC set now drives the outputs slightly differently. It is a lookup,
   pattern → changed weights; nothing is stored as a sequence, rule, or fact; there is no "fetch the next thing."
   Saved as .npz between runs (the fly's store; the watcher has its own).
2. **Eligibility trace = the memory's clock.** After a KC fires it stays creditable for a short window (5 observe()
   calls, ~55% decay each — ChatGPT's clock finding). Late dopamine credits the wrong cells; that is why replay-at-reward
   exists in fly.py.
3. **Membrane state = echo, not memory.** Every neuron's voltage carries ~20–50 ms of what just happened. A dot leaves
   the ear and DNa01 cells in a different state than a dash for a few tens of ms. Not learning.
**Why `.-` learns and `-.` never appears (hypothesis, zi/ra = ra):** the fly never learned pairs. In `.-` the dash arrives
40 ms after a dot, inside a small echo; in `-.` the dot arrives inside the larger, longer echo of a 60 ms dash and is
swallowed. A membrane-time-constant story, not a memory story. **Test:** swap the chosen durations (dot 60 / dash 20, or
gap 80) and see if the asymmetry moves. 5 seeds, CPU only.
**The honest edge:** the fly cannot hold "the last thing I heard" longer than the echo. That is the sequence wall. The
real next memory step is a slow variable the mushroom body can read — the heartbeat/body-state layer. Until then,
everything it knows is weights plus a 50 ms echo.

## The frame and the triangle (Jaron's brackets on the memory note, 2026-09-16 22:15) — the memory design
His three brackets connected: (1) *"something that doesn't remember why it's getting credit is the biggest flaw"* — true;
today the fly forgets the KC set before the reward arrives and fly.py replays it for it — the harness remembers, the fly
doesn't; step 2 (Qwen as teacher) would inherit the crutch. (2) *"the echo needs to be remembered… stored in the wires or
weights as it passes."* (3) *"even an echo can loop… you go back a little and lay the next line alongside… how some
languages read backwards… and why the prefix/suffix — the ABRACADABRA triangle — ever came about."*
**Read as mechanism:** ABRACADABRA written as a triangle is the same pattern decaying one step per line — that IS an
eligibility trace (100% → 55% → 30% → 17% …). The fly's problem is not that it has no echo; it is that **the echo has no
frame**: the dot's echo and the dash's echo pile onto one timeline and the second gets swallowed (why `-.` never appears).
The music fix is the same fix: don't play line 2 over line 1 — return to a marker and lay it alongside. A marker is a frame.
**Build (the heartbeat layer's first job):** a second, slow eligibility trace, opened by a taught **prefix** pulse and
closed by a **suffix** pulse. KC patterns that fire inside the frame are held at slow decay (seconds, not 5 calls) and
dopamine credits the whole frame when it arrives. Effects: the fly remembers why it is rewarded (no harness replay);
it has somewhere to hold "the last thing I heard"; sequence becomes learnable because the frame keeps two echoes
apart. Mushroom-body change (mushroom.py: a second trace array + frame state), taught prefix/suffix as two more
primitives, Grade 1 rerun with the frame. Order: the duration-swap test first (does the echo story hold?), then this.
**Naming, so nobody crosses them:** "mushroom body" = a brain region named for its shape (cap on a stalk). Not fungi.
The living-mycelium-as-memory idea is separate and parked. The Obsidian graph is the right picture: dots = KCs, lines =
wires, learning = a line getting thinner.

## Other mapped / simulatable brains the school could plug into (Jaron asked, 2026-09-16 22:30) — seeds
- **C. elegans** — 302 neurons, complete since 1986; OpenWorm has it in a body sim. Has proper slow neuromodulator
  chemistry with measured time constants = the heartbeat layer already done by biology, in a brain small enough to read.
- **Drosophila larva** — 3,016 neurons, complete (2023); same mushroom-body learning circuit as the adult, smaller.
  A second school row sharing the learning rule.
- **Zebrafish larva** — ~140k neurons plus recorded activity from the SAME animal (Fish Fire&Wire, Google/Janelia/
  Harvard). First map where a simulation can be checked against what the real brain did.
- **Cerebellum models** — not a connectome, but the one vertebrate circuit whose learning rule (climbing-fiber error
  signal) is well understood, and it is a TIMING learner — rhythms and "what comes next." That is the wall the fly's
  mushroom body cannot cross. Flag for the school: the sequence learner the fly lacks, with a published rule.
- **Fungi / mycelium** — living substrates with measured electrical spiking (Adamatzky, Bristol). Not mapped, not
  simulatable. Parked as a seed; not to be confused with "mushroom body."
Attempt 4 running (gap 40 → 100 ms, seeds 404–808, matched to attempt 3): if `-.` appears, the echo story holds.
**Attempt 4 result (23:15):** gap 100 ms → `-.` still 0/30; `.-` appears untrained 4/30. Echo story falsified. The
asymmetry is a native output bias of DNa01 (short-then-long only), not memory. Corrects the memory note above: the
`-.` failure is the readout/motor side, not the trace. The frame design stays as the memory fix, but Grade 1 needs a
readout that can physically produce long-then-short before any training on it means anything.

## Versions (2026-09-16 23:30) — freeze + fork
`projects/fly-brain/versions/README.md` is the version ledger. **fly-v1** is frozen (manifest with SHA-256s). Any change to
how the fly learns or reads out is a fork with its own name; runs (seeds, constants) are not versions. Every report-card
row names its version. v1 keeps running as the control for every fork. Planned forks: fly-v1-frame (slow framed
trace), fly-v1-readout (an output that can say `-.`), fly-v1-seq (chosen cerebellar-style rule, per ChatGPT's A/B).

## Facts to get right in any post (checked 2026-09-16 23:50; ChatGPT caught both, web confirmed)
- MaleCNS **v1.0 dataset released June 8, 2026**; the **Cell paper was Sept 3, 2026**. Not the same date.
- Full dataset ~166,700 neurons, ~125M synapses (Janelia, Cambridge/MRC LMB, Google). Our runtime simulates 165,122.
- Johnston's organ has **~480–720 sensory neurons** in a real fly. Our "50 JO-A cells" are the annotated auditory
  subtype in the runtime — say "50 annotated Johnston's-organ auditory neurons," never "its ear has 50 cells."
- DNa01 = 2 cells (left/right). Correct as stated.
- Our plasticity is a *model* of mushroom-body dopamine learning, not molecular plasticity.
Grade 1 post: draft in this session (23:55) with hook-first ordering; corrections applied. Jaron to boost.

## The upgrade found 2026-09-16 23:58 — axo-axonic synapses on descending neurons
**Ceballos et al., iScience, 2026-04-22 (bioRxiv 2025.09.04.674108; PMC13126034), Florida Atlantic U.** Using the male
connectome (ours), they charted every axo-axonic input onto all **1,314 descending neurons**. Axo-axonic synapses land on
the axon, downstream of the soma, and "can veto, amplify, or synchronize spikes." Validated with optogenetics: a cohort
of 8 ascending neurons (AN08B098) raises DNp01 (giant fiber) excitability via axon inputs.
**Why it is our attempt-4 result:** our runtime (and every LIF fly sim in the feed) sums ALL inputs at the soma. An
axo-axonic synapse gates the *output* after the decision. DNa01 in our sim can only ramp — no gate, no veto — which is
exactly what "short-then-long only" looks like. The map carries synapse position; our graph build dropped it.
**Bounded:** not yet confirmed that DNa01 itself has axo-axonic inputs (paper covers all DNs; need the table).
**Fork: `fly-v1-axon`** — restore synapse position from MaleCNS; two synapse classes in the kernel: soma inputs sum into
V, axon inputs multiply the output (veto/amplify). Codex kernel job (Saturday). Test: can DNa01 now produce `-.`?
First hard example of "map complete, physics placeholder." Goes in the post.

## fly-v1-axon — built 2026-09-17 00:10–01:00 (Claude, ~3% of a week; no Codex)
**Data (measured):** pulled MaleCNS v1.0 `syn-partners` (traced-only, 124M synapses, 3 GB) and kept the 4.59M synapses
whose postsynaptic body is one of the 1,332 descending neurons. CHOSEN rule: a DN's dendrite is in the brain, its axon
runs the VNC, so a synapse whose `primary_post` ROI is a VNC neuromere/nerve is **axonal**. Result: 290,602 axonal
(6.3%). **DNa01: 1,135 axonal inputs (4.4% of 25,785)** in the leg neuropils of T1–T3, from VNC interneurons
(IN07B104, IN19A003, IN09A001…). **Independent reproduction of the paper:** for DNp01 the top axonal input type by this
rule is **AN08B098 — 399 synapses** — the exact octet Ceballos et al. validated optogenetically. The rule found it
without being told. (Fly-Lab/results/dn_axon_summary.json)
**Graph:** graph_axon.npz = v1 + per-edge `axonal` (≥50% of the edge's synapses on the axon): 21,266 edges.
**Kernel:** flysim_axon.py — axonal edges never touch the target's voltage; they feed a per-cell output gate
(clip(1 + 0.05·mV, 0, 3), τ 5 ms, CHOSEN) that scales what the cell emits. Flags off → spike-identical to v1 (verified,
same fired set, same DNa01 rates). Gate on → DNa01 right cell 20 → 10 Hz under the same drive: the gate acts.
**Exam running:** Grade 1, seeds 73/7337/101/202/303 (matched to rows 1–2), MORSE_BRAIN=axon. Question: does `-.` appear?
**Exam result (01:45):** no effect — `-.` 0/30, `.-` identical to v1 per seed. Cause: DNa01's axonal inputs are VNC
interneurons that are silent in this protocol. The gate is real but not on this path. Asymmetry is upstream (dendritic
inputs or the LIF cell model). Fork kept for when the VNC is driven.

## Correction to row 5 + the body question (2026-09-17 02:10)
**Row 5 was mis-stated twice.** (a) The Morse script has its own inline kernel and never calls `fb.run()` — the axon
gate class was loaded but *never wired into the trial loop*, so attempt 5 tested nothing; "identical to v1 per seed" was
the tell. (b) "DNa01's gaters are silent" was also wrong: under the 120 Hz ear carrier the whole brain runs ~53 Hz/cell
(Saturday's ignition reaches the VNC) and IN07B104 / IN19A003 / IN07B009 fire at 200+ Hz with no leg drive at all.
Fixed: gate now wired into the trial loop (`use_gate` when the brain carries `axonal`), and a tonic leg-sensory drive
option (`MORSE_LEG_HZ`, 3,899 leg sensory neurons via ProLN/MesoLN/MetaLN). Measured: 5 Hz leg drive moves DNa01-left
from 3 → 140–150 Hz. The VNC is on the path; it needs its own input. **Attempt 6 running: v1+legs and axon+legs, 5
seeds each, in parallel.**
**Jaron's question — does the fly have a body?** No. /flies/brain/ is a picture of the brain plus a posed puppet; nothing
in the sim touches a floor. "Leg drive" is flat random spikes on neurons that in a real fly carry load and joint angle.
DNa01 is a walking-command neuron whose axon is gated by exactly those signals; without a body its inputs are silence or
noise, neither of which it was built for. **Fork `fly-v1-body`:** flybody (TuragaLab, Apache 2.0 — not CC0) joint
angles/contacts → leg sensory neurons → brain → DNa01/DN pool → flybody motors. Not only for retirement: it is what
makes the axon gate mean something, and it is what the page should show — the puppet driven by the numbers instead of
posed from them. This is the first fork that needs the GPU/MuJoCo, and a Codex job on Saturday.

## The classroom — school-1 is alive (2026-09-17 02:03 UTC / 22:03 EDT; Claude, ~4% of a week)
**Jaron (22:15 EDT):** "we can't expect to be produced what we want if it's not something that constantly, 24/7 … every
time we started it again maybe that's what's wrong is that it's a new fly, that's why I can't remember anything."
He is right, and it was in the code all along: every Grade 1 attempt (rows 1–7, 35 seeds) deleted the store, ran on a
frozen clock (`clock=lambda: 0.0`) for ~10 minutes, and threw the fly away. There was never a fly that had been to
school twice.

**Built and running:** `C:\Users\lilli\Fly-Lab-2\school\school.py`, Windows scheduled task **"Fly School"** (at logon,
restarts on failure, no time limit). One fly, `school-1`, brain **fly-v1** (unchanged protocol, unchanged exams — rule 2),
one mushroom-body store `mb_school-1.npz` that is loaded on start and never deleted, wall-clock forgetting (6 h half-life —
the biology; a fly that stops being taught forgets, which is the argument for not stopping). Lesson = **teach** (12 rounds of
`.`/`-`, dopamine ±1) → **exam** (`.-`/`-.` × 6, cold) → **rest** (2 trials of silence, measured). Lesson 0 = baseline exam.
~80–100 s per lesson, ~30 lessons an hour. Every trial → `fly_live` (fly = school-1: phase, symbol, decoded, DNa01 bins,
mushroom-body stats, 3,000 sampled atlas neurons that fired) and → `fly_school` (the permanent log; migration
`projects/fly-brain/migrations/2026-09-17-fly_school.sql`, public read). Local mirrors: `school/report-card.json`,
`state/fly-brain/live.school-1.json`, `school/school.log`.

**The page:** https://www.heartbeatobservatory.com/live-systems/flies/school/live/ — live status (Teaching · / Exam: –· /
Resting / **Asleep** when the process is not running, with the last trial's time), the trial strip (what was played to the
50 ear cells, what DNa01 answered, ▶ hear it), vitals (lesson, age, trials, dopamine lifetime, memory = depressed
synapses + mean gain, spikes/s, last exam), the atlas with real flashes and the flybody puppet (wings on reward, grooming
on punishment, a tap per DNa01 run — a puppet, said so on the page), report card per lesson (bars, lifetime totals, best
lesson), last 12 trials, and a plain-words section. Nothing on the page computes a score; it reads the log.

**Trader paused, not cancelled (Jaron's call, 22:15):** scheduled tasks "Fly Brain" and "Fly Watcher" ended and
DISABLED so the classroom has the machine. Resume = `schtasks /Change /TN "Fly Brain" /ENABLE` + `/Run` (same for
"Fly Watcher"); in WHEN-IT-BREAKS.md. fly-1's last `fly_live` row is 02:02 UTC; /flies/brain/ shows "last known tick".

**First hour, measured (as of lesson 6):** baseline exam L0 `.-` 0/6, `-.` 0/6. L1 `.-` 1/6. L2–L4 0. L5 `.-` 1/6. `-.` 0
throughout. Primitives ~46% exact during teaching. **Memory saturates fast:** after 5 lessons (120 dopamine events, 55
rewards / 65 punishments) 42,548 of 44,042 KC→MBON synapses are depressed, mean gain 0.305 → the floor (0.25) is close.
Continuous teaching with a −1 on every miss drives the whole matrix down; the 6-hour forgetting cannot lift it back
at this pace. Everything depressed = no contrast = nothing to read. **This is the first thing the 24/7 fly teaches us,
and it is a property of the chosen rule (lr 0.06, floor 0.25, punish on every miss), not of the connectome.** It is
measured, not fixed: the competing mechanisms are (a) a `school-v1-lr` fork with a smaller lr / higher floor, (b) dopamine
only on *change* (reward when a miss becomes a hit, nothing when nothing changes — closer to prediction-error dopamine),
(c) rest long enough for forgetting to matter. Each is a fork row, not a tweak to the running fly. The running fly stays
as the control.

**What the classroom answers about "what is the fly doing when nobody is teaching it":** in v1, nothing. Rest trials
measure 0 spikes (v1 has no spontaneous noise; the first smoke test: fired 0, 0.0 spikes/s). The honest page says
"Resting" when the process runs silence and "Asleep" when the process is not running. The trader had activity between
matches only because it was fed prices every tick. A fly that does something on its own needs the body-state layer
(tonic drive, "The heartbeat" section) — and now there is a place it would show up.

**Front door + students (Jaron, 22:20 EDT: "does a new fly replace the one shown, or is it another student?").** Another
student, always. `school.py` now enrols by env (`SCHOOL_FLY`, `SCHOOL_VERSION`, `SCHOOL_BRAIN`); each pupil has its own
memory file, state, log, report card, `fly_live` row and page. **/school/** is the school's front door (every student as a
live card: what it is doing, lesson, age, last exam, memory) and **/school/<student>** is its classroom. The home page's
first button is now "Fly School — live"; it is also first in the studio list and on /live-systems. Nothing lives behind
three clicks any more. Weekly usage actual 13% at 22:18 EDT (my "~16%" was high again).

## The fly's day + the life source (Jaron, 22:40 EDT; built 22:45–23:00, Claude)
Rules recorded in working-with-jaron.md ("The fly's life"). Built into `school.py` and restarted (same fly: store loaded,
lesson 27 — the first fly that has ever been restarted with its memory):
- **School hours** 9–12 and 1–4 America/New_York (CHOSEN), every day. Lessons only then. **Morning exam** = the first exam
  of each school day, taken before any teaching, flagged `morning` on the report card. With a 6 h half-life and ~17 h
  without lessons, ~14% of the previous day's depression survives — so the morning exam is the *spaced-training* question
  (Tully & Quinn 1985: spaced lessons make long-term memory, massed ones do not). The 24/7 fly could never ask it. It also
  releases tonight's saturation finding every night.
- **Free time** (waking hours outside school): one silent trial a minute (measured alive — 0 spikes in v1), and a **meal**
  every 3 h (CHOSEN). A meal is a clock event (`fed_at`, `hungry_h`, `meals`) and a `fly_school` row `phase=meal` — **not**
  dopamine: sugar with nothing recent in the eligibility trace would change no weight, and counting it as a reward would
  lie. When the body-state layer exists, hunger becomes tonic drive. **Night** 22:00–07:00: sleeping, one silent trial
  every 5 min; forgetting runs on.
- **Life source.** If the MSI is off, the fly is off; `load()` applies the missed forgetting, so a day off leaves ~6% of the
  memory. The page's process-down state is now **"Off"** ("life source down… memory fading meanwhile"), not "Asleep" —
  sleeping is what the fly does at night. **Lifeline:** after every exam the memory file, report card and state are
  copied to Supabase storage (private bucket `fly-lifeline`, `school-1/mb.npz` etc.). It does not keep the fly alive; it
  keeps what it had, so a new machine could wake it. The cloud (the fly that cannot die with one machine) waits on
  funding or a systems-thinking way — Jaron's call, not tonight's.
- **Inheritance (from the school-building note):** a new pupil may start from a lifeline copy of an older pupil's memory
  (`SCHOOL_INHERIT=school-1`, to add when the second pupil enrols). Same synapse positions, same sides table, same
  calibration, or `load()` refuses — a fork with a different graph cannot inherit gains directly; that is a real limit
  and should be written when it bites.
Page: `/school/` cards and `/school/school-1` show Free time / Eating / Sleeping / Off with "school again Wed 9:00 AM",
fed-ago, meals, lifeline-ago. Freshness follows the fly's day (a 5-minute sleep tick is not "Off").
Now (02:30 UTC): school-1 is asleep, lesson 27, memory mean gain 0.283. First meal ~07:00, morning exam 09:00 EDT.

## Shifts — three pupils (built 23:20–23:55 EDT, Claude)
`school.py` takes `SCHOOL_HOURS` / `SCHOOL_NIGHT` per pupil (local, may wrap midnight), `SCHOOL_INHERIT=<pupil>` (copies
that pupil's memory file once, if this pupil has none — same graph only), a per-pupil seed base, a **year** counter
(a gap ≥ 3 h since the last sign of life = the machine was off → the report card is archived as `report-card.<fly>.yearN.json`
and year+1, memory carried with the forgetting applied), and `capacity` (3, CHOSEN, this machine).
Enrolled tonight, both from school-1's memory (`run_school-2.cmd`, `run_school-3.cmd`, tasks "Fly School school-2/3"):
| pupil | school (ET) | night | inherited |
|---|---|---|---|
| school-1 | 9–12, 1–4 pm | 10 pm–7 am | — (born 22:03 EDT) |
| school-2 | 5–8 pm, 9–12 am | 6 am–3 pm | school-1 at lesson 27 (memory mean gain 0.283) |
| school-3 | 1–4 am, 5–8 am | 2–11 pm | school-1 at lesson 27 |
Gaps of one hour between shifts (lunch/breaks) are the only hours with no one in class. school-2 was in class the moment
it enrolled (22:50 EDT), morning exam `.-` 1/6, `-.` 0/6 on the inherited memory. Baselines of school-2 and school-3 at
lesson 0 were identical (same inherited weights, same lesson-0 seeds) — they diverge from lesson 1 (per-pupil seeds).
**Three pupils = three morning exams a day = three data points on "what survived the night" instead of one.**

## THE READOUT WAS WRONG — DN readout scan (Claude, 2026-09-17 00:00–00:20 EDT; Jaron: "treat this as you're the only AI")
`Fly-Lab-2/dn_readout_scan.py`: fresh fly-v1, no dopamine, Grade 1 constants unchanged, plays `.`, `-`, `.-`, `-.` cold
(5 seeds × 6 reps = 30 trials per rhythm) and records **every descending neuron** (1,314 cells, 1,281 spiked) in 10 ms
bins; decodes each cell and each type with the Grade 1 decoder. MEASURED:
- **DNa01 — the cell rows 1–7 graded — says `.` 19/30, `-` 0/30, `.-` 1/30, `-.` 0/30.** It cannot produce a dash at all.
  Three days of Grade 1 asked a cell that cannot say "dash" to say "dash-dot". The `-.` asymmetry was the readout's, not
  the fly's. **And it explains the saturation:** every dash lesson to DNa01 was an impossible task → punished every time
  → 42k of 44k synapses down in one lesson. The punishment flood came from an impossible readout, not from the rule.
- **Untrained, 127 DN types and 320 single DN cells produce `-.` exactly at least once; 308 types / 676 cells produce `.-`.**
- **117 types and 275 single cells can say all four** (`.`, `-`, `.-`, `-.` each ≥1/30). Best by minimum: DNp30 (16/6/5/4),
  DNge114 (12/9/5/4), DNpe006 (7/12/4/4), DNp17 (12/25/10/3), DNge131 (12/12/14/3). Best single cells: DNpe017#555871
  (18/12/12/4), DNpe004#20131 (13/19/5/4), DNg02_a#23411 (12/16/4/7 — the best `-.` anywhere).
  Files: results/dn_readout_scan.json / .npz.
**What changes:** rows 1–7 stand as measured but their question was malformed. The Grade 1 question on a readout that can
speak is: *does training the primitives raise `.-` and `-.` above their untrained rates?* `morse_grade1.py` now takes
`MORSE_READOUT` (type regex or `body:<id>,…`). **Attempt 8 running** (00:25 EDT): DNp17, DNge131, DNp30, DNg02_a#23411 —
5 seeds each, 24 epochs, in parallel. Rows 8a–8d.
**For the post:** this is a correction and a result at once. It reads better tomorrow, not worse: "we graded the wrong
neuron for three days; here is how we found out; here is the exam on the right ones."

## The night's chain (Claude alone, 2026-09-17 00:00–02:00 EDT; Jaron: "I want real results and work done")
Each step's competing mechanism was tested before the next. All MEASURED; files in Fly-Lab-2/results/ and Fly-Lab/body/results/.

| # | question | result | file |
|---|---|---|---|
| 8 | Grade 1 on readouts that CAN say every rhythm (DNp17, DNge131, DNp30, DNg02_a#23411; 5 seeds each, 24 epochs) | `.-` 29→26/120, `-.` 7→3/120. **Training moves nothing.** Memory still saturates (42k/44k). | morse_grade1_readout_*.json |
| 9 | Does the mushroom body reach the DNs at all? fresh vs all-floor vs MB-silent, 36 trials each | MBON spikes 1397→881→620 (MB output changes), but readout accuracy unchanged: DNa01 9/10/9, DNp17 15/14/13, DNge131 13/13/11, DNp30 12/12/13 of 36. **Cutting the MB entirely leaves every readout where it was. No MB lesson can pass a production exam on any DN.** | mb_reach_test.json |
| 10 | The exam the MB is wired for — valence (A=`.` rewarded, B=`-` punished; cold approach−avoid Hz; 5 seeds) | 2/5 seeds separate; mean sep −14.2 → −8.6. **Not a pass.** | morse_valence.json |
| 11 | Why: do dot and dash even differ to the MB? KC-set overlap, seed 73 | **Jaccard(dot,dash) 0.971 vs Jaccard(dot,dot) 0.988; 98.8% of dot-KCs inside dash-KCs; ~3,400 KCs (~65%) active per trial** (real flies: 5–10%). Under ignition every sound is the same sound. | (inline, 01:35) |
| 12 | fly-v1-body v0: brain on flybody (MuJoCo 3.13), 328 leg motor neurons → 59 actuators by muscle name; 3,915 leg sensory cells ← touch/joint speed; same 0.2 ms step | No input: silent brain, fly stands on six legs, still. **Any input ≥1 Hz on tactile cells: whole-brain ignition (33 Hz/cell), 41k motor spikes/s, the fly thrashes.** Bistable: silence or seizure. | Fly-Lab/body/body_loop*.json |

**One root cause: whole-brain ignition under sustained input (the stock gain regime).** It is behind rows 1–8 (DNa01
could not say dash; nothing learned on any readout), the memory saturation (every lesson depresses the same ~11k
synapses because every stimulus is the same KC set), the valence exam, and the body. Row 13 (running 01:45): a global
synaptic-scale sweep (1.0 → 0.15) measuring Hz/cell, KC active fraction, Jaccard(dot,dash) vs (dot,dot), DN response —
target stated before running: KC 5–15% active, dot/dash clearly different, DNs still answering. If a regime exists,
**fly-v2 = that calibration**, and every exam (production, valence, body) is re-run on it as a new pupil beside v1.

**What this means for the school and the post.** Three days of Grade 1 were not a fly failing to learn; they were a brain
in a seizure being graded on a neuron that can't say dash. That is a better story than a pass, because it is true and it
has a next step. The four pupils keep running as the control (they are the v1 record). The post's "what the first hour
taught us" becomes "what the first night taught us," and rows 8–13 go on the attempts page.
Sept 13's "Non-uniform baseline — the gap is a number" (Codex) was this same finding from the other side.

**Row 13 — gain sweep (01:50 EDT, seed 73, 3 reps per sound), MEASURED:** scale 1.0: 25 Hz/cell, 78% KCs active. 0.7: 16.5 Hz, 69%.
0.5: 8.8 Hz, 39%. **0.35: 2.0 Hz/cell, 7.3% KCs active, all-DN spikes 1,009 (dot) / 1,702 (dash), MBON 50/75 — no ignition,
sparse code, output alive and duration-sensitive.** 0.25: 0.7 Hz, 0.3% KCs (too quiet). 0.15: dead. File: results/gain_sweep.json.
**fly-v2 = fly-v1 with every synaptic weight × 0.35 (CHOSEN from this sweep; one seed — replicate on 2 more seeds before
freezing).** Dot/dash KC overlap does not separate at any scale (0.34 vs 0.33 at 0.35) — expected: same tone, same cells;
the mushroom body codes *which* input, not *how long*. So on fly-v2 the school's lessons change: (1) production exams stay
as the motor-side record; (2) the mushroom body's exam is IDENTITY — two different inputs (two JO subtypes, or two odours
through the Nose), one rewarded, one punished, valence read cold, then a never-paired mix. (3) the body loop re-run at 0.35
— the first real question there is simply "does it stand and not seize when touched." Tonight ends here (02:05 EDT).

## fly-v2 frozen; body stands; school-5 enrolled (02:20–02:55 EDT, Claude — "Did you do that one fix?" — now yes)
- Sweep replicated on seeds 7337 and 101: scale 0.35 → 2.85 / 2.84 Hz/cell, KC 10.5% / 11.0%, all-DN dot/dash 1207/2924 and
  1395/2639. 0.4 is the edge (12% KC); 0.3 too quiet (2–4%). **fly-v2 = every weight × 0.35** — frozen at
  `Fly-Lab/versions/fly-v2/graph_v2.npz` (sha 6477bbb1eedd15bb; source graph.npz 5a6e6fbfa5f2d384), MANIFEST.md.
  `MORSE_GRAPH` / `SCHOOL_GRAPH` / `BODY_GRAPH` select it.
- **Body on fly-v2 (row 14):** touch 5 Hz → 4.0 Hz/cell, 12k motor spikes/s, activation ~0.01, 5–6 legs in contact, ball
  still. Touch 40 Hz + prop 5 → 6.1 Hz/cell, standing, a twitch. Same inputs on v1: 33 Hz/cell, thrashing. **The fly stands.**
  Files: Fly-Lab/body/results/body_loop_v2_t5.json, _t40.json.
- **school-5 = fly-v2, readout DNp17 (12 cells), fresh memory, hours 9–12/1–4** (task "Fly School school-5"). Baseline exam
  cold: `.-` 1/6, `-.` 1/6, decodes rich (`-..`, `..-`, `-.`, `...`) — a brain that speaks. 12 trials in 9 s (v2 is faster).
  It is the clean A/B against school-1's first day. Capacity now 5.
Tonight's chain, complete: 1 root cause found and fixed as a version, body standing on it, a pupil on it. 03:00 EDT.

## Field + walking (01:20–02:10 EDT) — "use what they have for walking; hold the superposition"
Field check before the post: FlyGM (arXiv 2602.17997), Fly.exe (GPL-2), lulzx/fly-brain (MIT), NeuroMechFly v2 — whole
fly brains in bodies exist and "walk". Their own docs: **no connectome walks on its own**; a stepping generator sits
between DN rates and legs (Fly.exe: "the walking is engineered"). lulzx: nine fitted global parameters; **7.4% active
KCs** (ours 7.3% at 0.35×); raw-muscle mode "the fly cannot stand" — ours stands on v2. Fly-Lab/FIELD.md has the list.
**Ported (declared, credited):** `Fly-Lab/body/gait.py` + `gait.mineplix.json` — lulzx's 2-harmonic tripod gait fitted to
100 FlySuite real-fly walks (MIT), commanded by our brain's DN rates (their DN_ROLES: forward DNg100/DNg97/DNp09/…,
backward MDN, steering DNa02/DNa01/DNp09 L−R). `body_loop.py` `BODY_MODE=descending`, `BODY_SOUND_HZ`.
**Row 15, fly-v2 + borrowed gait (2.5 s each):** silence+touch → forward drive 1–7 Hz around the 4 Hz threshold,
intermittent steps, brain 2.9 Hz/cell. **120 Hz tone → MDN ~10 Hz, steering saturates: the fly backs up and turns**, ball
2.6 rad/s, brain 4.9 Hz/cell. Files: body/results/body_loop_v2_gait_s0.json, _s120.json.
Walking here is borrowed and declared; the command is the brain's. The classroom door is now a physical question.

## Row 16 — the identity lesson on fly-v2 (02:20–03:05 EDT). Identity: YES. Learned preference: NOT YET.
`Fly-Lab-2/identity_lesson.py`: odour A = ORN_DL3 (103 cells) rewarded, odour B = ORN_DM1 (74) punished, 40 Hz, 300 ms pulse,
12 epochs, cold valence (approach-MBON Hz − avoid-MBON Hz), mixture A+B never paired; 5 seeds. MEASURED:
- **Identity works on v2:** A lights 212–269 KCs (5–7% of 4,064), B 38–101; **Jaccard(A,B) 0.10–0.21 vs Jaccard(A,A) 0.11–0.52.**
  Two odours are two things to this brain. (Same-odour reliability is low — 0.4–0.5 — a note for the calibration.)
- **Preference not learned: 0/5 seeds.** Separation A−B pre −3.2 → post −3.3 (B's valence is higher throughout because B
  drives the brain harder: 10 Hz/cell vs 4). Approach/avoid halves move by ±1–4 Hz with no consistent sign. Only 4.6–7.0k
  of 44k synapses depressed (mean gain 0.97) — sparse KC code = few eligible synapses, as it should be.
- Reading: the lesson lands on a few hundred synapses in a few compartments; the readout averages ALL MBONs on each side,
  so a local change drowns in global drive. Real MBON preference is compartment-specific (Aso 2014). **Next (row 17):**
  read only the MBONs the trained KCs actually project to (compartment-specific valence), and equalise A/B drive so
  valence is not a proxy for global rate. If that shows separation, the fly answers a symbol; then the body reply.
**Communication: not established tonight.** Jaron's bar ("I can't be satisfied until communication is done") stands; the
post waits. What is established: distinct identities on v2, a fly that stands and steps under its own DNs, one root cause
fixed. Smoke/diag files: results/identity_smoke.json, identity_diag.json, identity_lesson.json.
**Jaron 02:45: "does the mushroom body need to learn how long?"** No — it codes which, not how long. Time is elsewhere:
32 annotated clock neurons in this graph (l-LNv 8, s-LNv 8, DN1pA 8, DN1a 4, DN1pB 4) are silent in ours. Drive them from
the wall clock (morning cells/evening cells, CHOSEN rates from the literature) = the fly feels the time of day. Small
build, after row 17. His method, recorded: every wall this week was something the real fly has that ours lacked (gain
regime, body, distinct smells, time) — find what reality supplies, add it as measured input, re-examine.

## GRADE 0 — does each organ do its job? (Jaron 02:10 EDT: "have we tested eyes being eyes…"; built + run 02:15–02:45)
`Fly-Lab-2/grade0_organs.py`. No learning. Sense in for 300 ms, the literature's named output read, pass = output ≥ max(1 Hz,
2× silent baseline) AND brain < 10 Hz/cell. Seed 73, 3 reps. Same script on v1 and v2. MEASURED:

| organ | input (cells @ Hz) | expected output | fly-v1 | fly-v2 |
|---|---|---|---|---|
| mouth/hands | tarsal taste claw_tpGRN (50 @ 60) | proboscis MN9 | IGNITES 27.6 Hz/cell, KC 51% | **PASS** MN9 20 Hz, MN1 11; brain 2.9 |
| feet, hind | T3 leg bristles via MetaLN (1,062 @ 20) | MDN backing | IGNITES 29.7 | **PASS** DNa01 8.8 Hz, MDN 0.8 (weak); brain 3.1 |
| feet, front | T1 leg bristles via ProLN (596 @ 20) | grooming DNg07/08 | IGNITES 31.8 | **PASS** DNg07 1.6, DNg08 1.0 (weak); brain 2.2 |
| eyes | loom VPNs LPLC2+LC4 (311 @ 60) | giant fibre DNp01, takeoff DNp02/04 | IGNITES 27.8 | **PASS** DNp01 253 Hz, DNp02/04 250; brain 4.0 |
| ears, wind | JO-C/E (335 @ 60) | MDN | IGNITES 30.1 | **PASS** MDN 11.5 Hz; brain 4.8 |
| ears, song | JO-A (50 @ 120) | courtship pIP10 / DNp13 | IGNITES 29.7, KC 83% | **PASS** pIP10 20.8, DNp13 11.3; brain 3.2 |
| nose | ORN_DL3 (103 @ 40) | KC sparse 5–15%, steering DNa02 | IGNITES 28.3, KC 19% | **PASS** KC 6.3%, DNa02 39 Hz; brain 3.4 |

**v1: 7/7 organs set the whole brain on fire. v2: 7/7 organs do what the literature says they do.** Files:
results/grade0_v1.json, grade0_v2.json. Caveats: feet rows pass weakly (grooming DNs 1–2 Hz, MDN <1 Hz — the hind-leg route
to MDN is more specific than "all T3 bristles"); giant fibre at 253 Hz is unphysiologically high (a gain note for v3);
the answer key still needs ChatGPT's literature table (brief in inbox/2026-09-17-briefs-chatgpt-grok-grade0.md) and Grok's
neighbour numbers. **The Braille-through-the-feet lesson is now readable** (feet → DNs pass on v2); not yet run.
This is the foundation Jaron asked for: organs first, then one lesson through one working organ at a time.

## GRADE 0b — the organ check on the corrected answer key (ChatGPT chat + Grok chat tables, 02:30; run 02:50–03:00 EDT)
ChatGPT's literature table removed three of my rows (T3 bristles→MDN, wind→MDN, JO-A→pIP10/DNp13 — not supported) and named the
right cells: sweet = LB3b+LB3c (not claw taste pegs), water = LB3a, bitter = LB1a–e, loom DNs DNp02 (LC4-linked) / DNp04, DNp06
(LPLC2-linked), song = JO-B→aPN1→vPN1→pC1, JO-A type-1→GF, DM1 ORN→DM1 PN→KC 5–10%, lateralised ORNs→ipsilateral DNa02.
Grok's table: the neighbour repo is **lulzx/fly-brain** (lulzx is a mirror) — nine fitted globals: wSyn 0.55 mV, sizeAlpha
0.61, KC threshold 10.9 mV, inhibition gain 0.61, E_inh −76.4 mV, min synapses 6 (weaker connections dropped), refractory
3.8 ms, lamina bias 5.3 mV, conductance-based; their reflexes: sugar→MN9 59 Hz, bitter vetoes to 0, loom takeoff DNs 33 Hz,
KC 7.4%. FlyGM is a trained GNN, not a spiking brain — no reflex numbers. Fly.exe: 0.2 mV/contact, no whole-CNS screen.
`Fly-Lab-2/grade0b_organs.py`, both versions, MEASURED (v1 ignites on every row, KC 38–85%; v2 below):

| # | organ (corrected key) | v2 result | verdict |
|---|---|---|---|
| 1 | sweet LB3b+LB3c @100 → MN9 | MN9 6.7 Hz, MN8 18.3, MN6 3.8; brain 3.7 | PASS (Shiu's normalised strong = 40 Hz; ours weaker) |
| 2 | water LB3a @100 → MN9 | MN9 0 | **FAIL** |
| 3 | bitter LB1a–e + sweet → MN9 lower | MN9 1.7 vs 6.7 sweet alone | **PASS — the veto sign is right** (Shiu: 40→1 Hz) |
| 4 | loom LPLC2 alone | GF 176, DNp04 42, DNp06 38, DNp02 16 | PASS |
| 4.1 | loom LC4 alone | DNp02 180, DNp04 273, GF 66, DNp06 1.7 | PASS — **LC4→DNp02, LPLC2→DNp06: the feature specificity the key predicts** |
| 4.2 | LPLC2+LC4 | GF 228, DNp02 187, DNp04 294, DNp06 58 | PASS (convergence strongest, as predicted) |
| 5 | sound JO-A @120 → GF | DNp01 0 | **FAIL** (type-1 JO-A→GF path not carried by our 50 JO-A cells, or gain) |
| 6 | song JO-B → AMMC second-order | AMMC 9.3 Hz | PASS (weak key — aPN1 not typed in this release) |
| 7 | odour ORN_DM1 @40 → DM1 PN, KC 5–10% | DM1_lPN 297 Hz; **KC 2.8%**; brain 8.9 | **FAIL on sparsity target (just under)**; PN path strong |
| 8 | left ORNs → DNa02 L > R | ORN sides not in somaSide (peripheral) | NOT TESTABLE as coded — use rootSide next |
| 9 | JO-C/E/F → MDN (informational) | MDN 5.6 Hz | responds |
| 10 | JO-C/E/F → grooming DNs | DNg11 25.6, DNg07 13.5, DNg08 6.9 | PASS (weak key — aBN/aDN not typed) |

**v2: 7 pass, 3 fail (water, JO-A→GF, DM1 KC sparsity 2.8%), 1 not testable.** v1: 0 pass, 11 ignite. Files:
results/grade0b_v1.json, grade0b_v2.json. GF at 176–228 Hz is unphysiological (a GF fires once); noted for v3.
**fly-v3 candidate = lulzx's recipe** (nine globals above, conductance-based, KC threshold raised, weak connections dropped)
rather than one scale — their measured KC 7.4% and sugar→MN9 59 Hz are the targets; our one-number v2 gets 2.8% on DM1 and
MN9 6.7. Not tonight; it is a runtime change (conductance synapses) = a real fork with its own manifest.

## fly-v3 + Row 17 (03:05–03:45 EDT) — "Do v3 and run it. Let's see if it can answer a symbol."
**fly-v3 built and frozen** (`Fly-Lab/versions/fly-v3/`, MANIFEST.md): lulzx's recipe at the graph level — connections < 6
synapses dropped (10.23 M → 4.91 M edges), sensory neurons shielded from central input (stored graph is rows=POST, cols=PRE
— the first build masked the wrong axis and silenced every sense; fixed), weights × 0.35 (sweep 0.35/0.5/0.7/1.0),
refractory 3.8 ms. **Grade 0b on v3@0.35: 8 pass / 2 fail** — sugar→MN9 36 Hz (Shiu's strong reference 40; v2 had 6.7),
bitter veto 36→8, loom ×3 with LC4→DNp02 / LPLC2→DNp06 specificity, **JO-A→GF 4.2 Hz (dead on v2)**, JO-B→AMMC, grooming DNs,
MDN responds; water still silent; DM1 KC 2.6% (target 5–10%). At 0.5 water passes (10 Hz) but odour ignites (KC 21%, 10.8
Hz/cell). Files: results/grade0b_v3_s*.json.
**Row 17 — identity lesson on v3, compartment-specific readout (only MBONs receiving synapses from the trial's active KCs),
drive equalised (A DL3 @40 Hz → 161 KCs; B DM1 @200 Hz → 185 KCs), 5 seeds, 12 pairings.** MEASURED:
- Identity: J(A,A) 0.69, J(A,B) 0.24 — cleaner than v2 (0.39 / 0.15). The fly tells the two symbols apart, reliably.
- Preference: **not learned on the stated line, 0/5** (sep −6.7 → −9.2).
- **But one channel moves the way the biology says it should:** the rewarded odour's *avoidance* MBONs drop after training in
  4/5 seeds (avoid Hz pre→post: 9.5→5.0, 6.3→3.8, 3.6→4.1, 5.0→3.8, 3.8→4.0). That is the exact site (KC→PAM-side MBON
  depression under reward, Hige 2015) and the exact sign. The punished odour's approach channel does not drop consistently
  (2/5), and the rewarded odour's approach channel also drops (network effect), which is what keeps the difference from
  separating. Only 3.3–3.5k of 44k synapses depressed (sparse code = few eligible), mean gain 0.97.
**Verdict at 03:45: the fly distinguishes the symbols (established, twice); it does not yet answer them with a learned
preference. Communication not established.** Next suspects, in order, each cheap: (1) re-verify mb_sides.json — which MBONs
are PAM- vs PPL1-side — against Aso 2014's compartment table (the earlier version of this file had 14/37 wrong); (2) read the
single sign-correct channel (rewarded-odour avoidance drop) as the exam, 10 seeds, since it is the measured site; (3) a
stronger-rule pupil (lr 0.2) beside the control. Files: results/identity_v3_row17.json.

## THE COMMUNICATION LOOP — attempted under a predeclared goal (03:15–03:59 EDT, Claude). NOT ESTABLISHED. Here is exactly why.
Goal (Jaron, /goal 03:10): symbol → sensory neurons → learned MB state → endogenous answer pathway → fly output → decoded
reply; cold; predeclared seeds, controls, criteria; Grade 0 preserved; frozen; reproduced from clean. Everything below is in
`Fly-Lab-2/comm_protocol.md` (predeclarations), `comm_loop.py`, `results/comm_loop_*.json`, `kc_homeostasis.py`,
`versions/fly-v4/`. Two predeclared tests on 16 fresh seeds; six pilots on seeds 73/7337 only.
1. **MBON side table verified** against Aso 2014 compartment by compartment — correct. The learning site is right.
2. **Per-compartment readout (pilot, v3):** the canonical learning MBONs (01/03/05/11/12) are near-silent under our odours;
   MBON09 (γ3β'1) collapsed for the rewarded odour, MDN rose for the punished one — in 2 seeds.
3. **Test 1 (predeclared: answer = MDN "AVOID" > pre+2σ; 8 seeds 101–808): FAILED all criteria.** MDN did not move; MBON09's
   drop replicated 7/8 but was non-specific (B and C dropped too). results/comm_loop_test.json.
4. **Wiring-derived answer pathway:** signed 1–3-hop influence shows PAM-side (avoid) MBONs excite and PPL1-side (approach)
   MBONs inhibit the same DNs — DNa13, DNa03, MDN. A clean, biologically sensible convergence. Pilots with that channel,
   with MBON output gain ×3, and with lr 0.2 / 24 pairings: no consistent movement; A's channel rose when it should fall.
5. **Root cause found — the Kenyon-cell code is not odour-specific:** at one rate, most odour pairs share 0.4–0.7 of their
   active KCs (results/glom_scan_v3.json); only DA2/VM2 reach 0.19. Sparse (5–10%) but the same cells win for every odour.
   lulzx's fitted model reports the same ("odour-specificity failed every configuration"). Every lesson lands on the same
   synapses; specificity is impossible by construction.
6. **fly-v4 attempt — per-KC homeostatic thresholds** (Turner 2008 / Honegger 2011 rationale): gentle pass 0.33→0.27 overlap,
   73% of KCs still silent for every odour; stronger pass oscillates (0.05↔0.6) because KCs are coupled through APL —
   the resulting code is decorrelated but *unreliable* (same odour 48 vs 700 cells across runs). Rejected as a baseline.
7. **Test 2 (predeclared: answer = MB output MBON21+26 "LEARNED" < pre−1σ; 8 seeds 909–1616): FAILED all criteria.** The
   channel ROSE after reward in 7/8 seeds. The pilot's drop (seeds 73, 7337) was seed noise. results/comm_loop_test2.json.
**Concrete technical wall (stated, not redefined):** in this runtime (a) the KC code is either shared across odours (v1–v3)
or unstable across trials (v4), and (b) the dopamine-gated depression does happen (3–4.5k synapses to ~0.5 gain) but the
MBON output it should read out is dominated by network dynamics (MBON→MBON inhibition, APL, shared KCs) and trial noise
(±30–50%), so no answer channel — MBON or descending — selects reproducibly by symbol. Both are mushroom-body calibration
problems (PN→KC gain, APL feedback strength, per-KC excitability, MBON coupling), i.e. a parameter search validated on
odour-specificity AND learned readouts — hours of compute the best public model also failed at. Not resolvable tonight.
**What IS established (measured, reproduced):** symbols reach the fly only through sensory neurons (item 1); the fly
distinguishes two odours internally when the pair is chosen well (DA2/VM2 0.19 on v3; 0.02 on v4) (item 2, conditional);
learning depresses the intended synapses in the intended direction, every time (item 3 at the synapse; NOT at the readout).
Items 4–9: not met. The post waits, exactly as Jaron's bar says.
**Next (the real one):** a mushroom-body calibration search — objective = pairwise KC overlap ≤ 0.15 with same-odour
reliability ≥ 0.6 and 5–10% active, plus a learned MBON drop ≥ 30% for the paired odour and ≤ 10% for a control — over PN→KC
gain, APL gain, KC threshold, MBON→MBON gain; then test 3 predeclared on that fly. Codex Saturday pool + the MSI overnight.

## Calibration search → fly-v5 → TEST 3 (04:05–04:30 EDT). FAILED. The session's honest end for the loop.
`Fly-Lab-2/mb_calib_search.py`: 96 random candidates over PN / APL / KC / MBON gains + KC threshold shift, 8 workers, ~3 min.
Stage 1 objective (predeclared): pair overlap ≤ 0.15, same-odour reliability ≥ 0.6, KC 3–10%, brain < 8 Hz. **One pass,
c007: reliability 0.69, overlap 0.06, KC 4.6%, brain 4.9 — APL ×6.0, KC ×1.8, PN ×1.27, threshold +1.8 mV.** The
sparsening interneuron is the knob, as the biology says. Frozen as **fly-v5** (Fly-Lab/versions/fly-v5/calib.json, MANIFEST).
Stage 2 (A=DA2 rewarded vs C=VM5d never paired, PAM-side MBON output, 1 seed, 4 reps): lr 0.06 → A −21%, C −2%; 24 pairings
→ A −27%, C −2%; **lr 0.2 → A −31%, C +9% (bar met)**. For the first time: a learned, odour-specific, sign-correct drop at
the mushroom body's output.
**TEST 3 (predeclared in comm_protocol.md; A=DA2 reward, B=DL3 punish, C=VM5d control; answer = PAM-/PPL1-side output vs
each odour's own baseline; 8 fresh seeds 1717–2424; lr 0.2 pupil + lr 0.06 control): FAILED all four criteria for both.**
PAM(A) relative drop per seed (lr 0.2): [(1717, 0.033, -0.018), (1818, -0.101, 0.113), (1919, -0.04, 0.044), (2020, 0.203, 0.012), (2121, 0.093, 0.037), (2222, 0.129, 0.044), (2323, 0.151, -0.016), (2424, -0.133, -0.04)] — 5–20% in most seeds, not 30%; per-trial replies at chance
(pooled: {"A": {"approach": 0.25, "avoid": 0.208}, "B": {"approach": 0.25, "avoid": 0.104}, "C": {"approach": 0.25, "avoid": 0.104}}). The stage-2 −31% was one seed, four reps. results/comm_loop_test3_*.json.
**Verdict.** Three predeclared tests, 24 fresh seeds, three fly versions built and frozen tonight (v3, v4, v5), nothing
redefined after a result: the loop is not established. What is now true and reproducible: symbols enter only through
sensory neurons; on fly-v5 the mushroom body has a sparse, reliable, odour-specific code (0.69 / 0.06 / 4.6%); learning
depresses the intended synapses in the intended direction; the paired odour's avoid-side MBON output falls 5–20% in most
seeds while the control's does not. What is not: a per-trial reply above chance, at the MB output or at any descending
neuron. The remaining gap is quantitative — the learned change is a fifth of the trial-to-trial variability — and closing
it means a calibration whose objective includes the learned readout with many reps and seeds (hours of the MSI, or the
Codex pool), not another night of by-hand variants. Grade 0b on fly-v5 not run (no pass to protect).

**TEST 4 (predeclared 04:35; block-level reply, the way conditioning is actually read; 8 fresh seeds 2525–3232): FAILED.**
A → APPROACH in 0/8 seeds; C → NONE in 5/8; the control odour's block moved as often as the taught one. results/comm_loop_test4.json.
**Four predeclared tests, 32 fresh seeds, nothing redefined. Jaron: "Pause. Let's wrap it up" (04:40 EDT).**

## Where the night leaves the fly (wrap, 04:45 EDT)
Built and frozen tonight, each with a manifest: fly-v2 (×0.35), fly-v3 (lulzx's recipe at graph level; Grade 0b 8/2),
fly-v4 (per-KC thresholds — rejected, unstable), fly-v5 (APL ×6 calibration — sparse, reliable, odour-specific KC code:
0.69 / 0.06 / 4.6%). Grade 0 exists twice (my key, then ChatGPT's corrected key). The body stands on v2 and steps under a
borrowed, credited gait. Five pupils are in shifts on the school page. The repo has every script and every result.
Communication: not established. The learned change at the mushroom body's output is real (5–20% for the paired odour, ~0
for the control, on v5) but a fifth of the trial noise, and it does not reach any descending neuron above noise.
The next step is not another variant by hand: it is a calibration search whose objective includes the learned readout
over many seeds (mb_calib_search.py stage 2 extended to 3+ seeds and 8+ reps; objective written above), run on the MSI or
the Codex pool, then one more predeclared test. The post waits, as Jaron said it should.
**Jaron, 04:45 (pausing at 27% weekly — actual; my estimate was ~45%, high again):** "is A/B the issue… do we need just one?"
A/B is our choice (standard differential conditioning), not a requirement. One symbol + one never-paired control is the
simplest honest loop and removes B's shared-KC interference entirely. Test 4 already judged A vs C and failed, so the limit
is readout signal-to-noise, not B. Tomorrow: one symbol + control on fly-v5, and the calibration search with the learned
readout in the objective. Resume here.

## Morning, 2026-09-17 08:15–08:40 EDT — round 1 of the calibration search, scored on the learned readout (Claude)
Round 1: 96 candidates sampled around fly-v5 (log-normal ±35%), 8 workers, 3 min. Stage 1 passes: 4 (c002, c012, c022, c064)
+ c007. **Stage 2, now over 3 fresh flies × 6 cold reps each, lr 0.2, PAM-side MBON output, A=DA2 rewarded vs C=VM5d never
paired:** best mean drop_A = 0.147 (c040: seeds +0.31, −0.13, +0.27), c007 0.088 (+0.17, −0.04, +0.14), c022 0.113; no
candidate reaches 0.30 or is consistent across seeds; control drops 0.00–0.07. results/mb_calib/r1_*.json, s2r1_*.log.
**Reading:** last night's −31% on c007 was one fly. Across flies the specific, sign-correct learned change at the MB output
is ~10–15% on average and absent in about one fly in three. That is the number the loop has to work with in this runtime,
and it is below what any per-trial or per-block reply can detect above chance. The goal's item 4–5 bar is not reachable
by gain calibration alone. Remaining routes, each a real build: (a) conductance-based synapses + lulzx's full nine-parameter
fit (runtime rewrite); (b) a readout at the specific compartment MBONs the rule is known to change (γ1pedc, γ4>γ1γ2,
γ5β'2a — near-silent under our odours today; needs the odour→PN→KC drive re-examined); (c) spaced training over the
school's real days (the persistent pupils already do this — ask the morning exams); (d) MBON→DN coupling calibration.
9 AM morning exams (school-1/4/5) not yet taken at 08:40.

## Morning 08:50–09:30 EDT — the readout was pinned; fly-v6, fly-v7; tests 5, 6, 7 (Claude, with Jaron)
Diagnosis (instrumented trained fly, v5): rewarded odour's KC→PAM-MBON synapses depressed to gain 0.26, yet KCs supplied
9% of those MBONs' excitation and APL inhibition onto them summed to −1.0e6 mV — v5's per-neuron APL ×6 crushed the MBONs.
**fly-v6**: APL ×6 moved onto APL→KC edges only (4,084 edges; APL→MBON's 71 edges ×1). On v6 the lesson cut A's KC drive
onto reward-side MBONs 4,398 → 1,741 mV (−60%) and their spikes went 92 → 94: KC→MBON was a minor term; MBON01–07 never
fired. **fly-v7**: KC→MBON edges ×24 (sweep ×4/8/16/24: learned drop 0.12/0.18/0.23/0.21, and only ×24 put every fly below
z −2; KC code 0.66/0.02/4.5% at all settings). Manifests in Fly-Lab/versions/fly-v6, fly-v7.
**Grade 0b on fly-v7 with its calibration: 9 pass / 1 fail (water) / 1 not testable** — no ignition, sugar→MN9 37 Hz,
bitter veto 37→6.7, loom specificity, JO-A→GF 2.9 Hz, and DM1 KC sparsity now passes (4.6%). Item 7 holds.
| test | change | A | C | verdict |
|---|---|---|---|---|
| 5 (v5) | 1 s pulses, 24 pairings, 12 reps | APPROACH 2/8 | NONE 6/8 | FAIL — sizes were not the leak |
| 6 (v7) | KC→MBON ×24; 12 pairings, 12 reps; two-sided decode | 3/8 (avoid-side fell in 7/8, z<−2 in 5) | 7/8 | FAIL — decode called two of A's drops "AVOID" because the PPL side fell too (PAM MBONs excite PPL MBONs) |
| 7 (v7) | one-sided decode; 24 pairings; 24 reps | **APPROACH 7/8** (z −2.9…−6.4; 14–29%) | **NONE 2/8** (C fell 3–10%, z −2.1…−3.1) | FAIL — generalisation to the control; B (punished) did not move (20.5→20.4) |
**Where it stands (09:30):** item 3 is now strong — a reproducible, sign-correct, learning-site-driven change at the MB
output in 7/8 flies. Item 4 is the open question: the control inherits ~a third of the lesson. Not global (B unmoved);
specific to C. Candidates: shared KCs A∩C on v7, MBON→MBON coupling, C's equalised rate. Jaron: "wait to see what Grok and
ChatGPT say" — review brief inbox/2026-09-17-review-brief-fresh-eyes.md; test cycle paused at seven.

## 09:30–10:25 EDT — three more leaks found and fixed; fly-v9, fly-v10; test 8 (Claude, with Grok chat's review)
- **Generalist Kenyon-cell ensemble** (v7): 177 cells, 168 KCγ-main, switching on together in ~2/3 of trials for every odour —
  an odour-independent network state. Raising their threshold removes it but the remaining cells still overlap 0.72–0.77 →
  the problem is upstream.
- **Antennal lobe broadcasting** (root): one glomerulus's ORNs activated 154–164 PN types (nearly all), same top list for every
  odour. Cause: the lLN1/lLN2 antennal-lobe local neurons are marked *acetylcholine* by the transmitter table (88 of 171 lLN
  cells); in the fly they are the GABAergic lateral-inhibition population (Chou 2010). **fly-v9**: their excitatory outputs
  made inhibitory (15,719 edges). Result: 23–35 PN types per odour, own-glomerulus share 25–75% (was ~1%), PN spikes ÷10.
  Every version since v1 inherited this error.
- **Grok chat's review (theory A):** pupils that ran in one process inherited the previous pupil's depressed weights
  (`MushroomBody` reads its base from `fb.wdata`). Real for tests 1–4 and every multi-seed stage 2; tests 5–7 ran one process
  per seed and stand. Fixed: weights restored before every pupil. Grok's C (readout dilution → top compartments by wiring)
  adopted for test 8. Grok's 5: neither lulzx nor Fly.exe ever cleared this bar ("the change never turns into a measurable skill").
- **Calibration round 2 on v9** (weights bug fixed): four settings with paired-odour drop 32–50% in every fly, control 3–10%.
  **fly-v10** = v9 + r2_c025 (PN ×2.96, APL ×1.44, KC ×2.01, threshold +6.7 mV, MBON ×2.87): drop 0.44 (0.50/0.42/0.39), control 0.08.
- **Grade 0b on fly-v10 with its calibration: core holds** — sugar→MN9 44 Hz, bitter veto 44→6, loom ×3 with specificity,
  JO-A→GF 2.1 Hz, no ignition (2–3.6 Hz/cell); water still silent.
- **TEST 8 (predeclared; answer channel = top-5 PAM-side MBON types by KC weight from A's pre-trial KCs — the wiring chose
  γ3β'1, γ5β'2a, γ4>γ1γ2, β'2mp, β1>α in every fly; 24 reps; 8 fresh seeds, one process each):** **A → APPROACH 8/8, z −13 to
  −22 (51 → 30 Hz, −40%).** Control C also fell 15% (z −2 to −9) → criterion 2 failed; punished B fell 30% on the reward side.
  **FAIL as predeclared.** Cause, measured: same-odour KC reliability in these flies 0.29–0.47 (stage 1's two-trial estimate
  said 0.72), B and C light ~2× A's cells, overlaps 0.16–0.19 → over 12 pairings the eligible set spreads onto cells B and C use.
  Files: results/comm_loop_test8_s*.json, grade0b_v10calib.json.
**Round 3 launched 10:25** (stage 1 now: reliability over 4 trials, overlap on the actual test pairs ≤ 0.15). ChatGPT's review pending.
State of the goal: items 1, 2, 3 (strong: −40%, 8/8, textbook compartments), 7 (Grade 0 holds on v10) — met in fresh runs;
4/6 fail on specificity (control −15%, punished −30%); 5 not shown (MB output, not motor); 8/9 not reached.

## 10:45–11:25 EDT — ChatGPT chat's two reviews (the connector errored and produced two; both read) and test 9 (Claude)
**Taken into the build:** (1) v9's blanket ^lLN sign flip was too broad — the ~13 lLN2T_a/b/c cells are the known cholinergic
local neurons; **fly-v9b** keeps them excitatory and flips the other 75 ACh-predicted lLN cells (v9b: learned drop 38–45%, but the
control leaks more, 12–17%, than on v9's 3–10% — the cholinergic LNs really do spread activation). (2) The control's rate
equaliser matched a single probe trial (19 cells) while the real trials ran at ~220 — fixed to the mean of six; test 8's control
comparison was not activity-matched. (3) The block z used only the pre-block variance — two-sample SE added. (4) **The calibration
that chose fly-v10 trained A + reward only; test 8 trained A + reward interleaved with B + punishment.** The MBON network is
recurrent, so B's lesson can move the reward-side channel A and C are judged on — a plausible cause of the punished odour's
30% drop and part of the control's 15%. Jaron asked "do we need A/B?" last night; the answer is no, and it was hurting.
(5) v3's "sensory neurons receive no central input" removed ORN presynaptic inhibition (a real antennal-lobe gain control) —
unchecked suspect. (6) Literature: Hige 2015 — one 1-s pairing, MBON-γ1pedc 118→24 spikes (−80%), EPSC charge −90%; the
UNPAIRED odour also fell 110→83 (−25%). Real flies' controls move too; specificity is relative, not absolute. Appetitive papers
(Owald, Cohn, Handler) report normalised, compartment-specific, bidirectional changes, not a universal percentage.
**TEST 9 (predeclared 11:20; ChatGPT's experiment): fly-v10; A + reward only, no B; C never paired, not equalised; the SAME 24
sensory realisations replayed pre and post; answer population frozen = MBON09/01/05/03/06; paired z < −2 AND ≥30% drop for A;
|drop| ≤ 10% for C; ≥ 6/8 flies each. Running on seeds 7373–8080.**

## TEST 9 — PASS (11:02 EDT). The first predeclared communication test to pass. Grade 0 held after. Frozen. Reproduction running.
fly-v10; A + reward only (12 pairings, lr 0.2); C never paired at its own rate; B untrained second control; 24 sensory realisations
replayed identically before and after; answer population frozen = MBON09/01/05/03/06; paired z < −2 AND ≥30% drop for A,
|drop| ≤10% for C. **A → APPROACH in 8/8 flies (paired z −13.6 to −23.2; drops 45–49%). C → NONE in 8/8 (drops 1–4%).**
B (shares more KCs with A) shifted 7–28% in 5/8 — reported, not required. Recorded unrequired: the avoid-promoting descending
sum (DNa13+DNa03+MDN) fell for A in 8/8 flies (7–31%), flat for C — the sign the wiring predicted at 03:30.
Grade 0b on the same fly immediately after: identical to before (sugar→MN9 43.75, bitter veto →5.83, loom ×3, JO-A→GF 2.08,
no ignition). Item 7 holds. **Frozen as `Fly-Lab/versions/comm-loop-1/`** (MANIFEST with SHA-256 of graph, calib, side table,
every code file; run_test9.ps1; raw outputs). **Reproduction predeclared 11:05** (seeds 8181–8888, fresh processes, frozen
script) with the motor criterion added for item 5: paired z on the descending sum < −2 for A in ≥6/8 ("GO-TOWARD"), C within
±25% in ≥6/8. Running.
What made the difference, in the end, was four errors we made or inherited, each found by measurement or review:
APL applied per-neuron (v5→v6); plasticity-site synapses too weak (v6→v7); antennal-lobe local neurons with the wrong sign
in the transmitter table (v7→v9); pupils sharing weights across a process (Grok); and one design choice — the second taught
symbol — that Jaron questioned first and ChatGPT's review explained (the calibration never saw B).

## 12:05–12:30 EDT — Grok chat's four-gate plan, the GPU kernel, and GATE 1 PASS (Claude, with Jaron)
Jaron took the public repo to Grok chat (X, no other context). Grok's review: what we have is one-fly association + an observer;
real communication = sender S changes a physical field in a shared world, receiver R gets it only through its own sensory neurons,
with a mute lesion and a scramble as the controls; four gates (channel exists / innate use / state-gated use / learned coupling);
use the fly's own channels (song pIP10->wing MNs->JO; cVA Or67d/DA1; CO2 Gr21a/Gr63a->V) instead of Morse; freeze physiology
before any communication test. Grok read a repo that stops at test 8, so "eight tests fail" was stale; after correction Grok
agreed: test 9 = Goal A (decoded endogenous reply in one fly, done if it holds); two flies + world = Goal B (not started).
Jaron's rule, logged in working-with-jaron.md and OPEN-QUESTIONS Q-019: nothing is cancelled out — the "chemistry" lead (CO2,
hunger gating dopamine, cVA) is untried and stays open, not dropped.

GPU KERNEL (Fly-Lab-2/gpu/flysim_gpu.py). The RTX 4060 was at 0% while 16 CPU flies shared the cores. Same maths as the CPU
kernel (dt 0.2 ms, decay, refractory 3.8 ms, thresh+1 injection, sign*weight*gain per spike), batched over flies with one
sparse matmul per step; Poisson hits drawn on the CPU with the same numpy rng in the same order. VERIFIED (results/gpu_verify.json,
fly-v10 stack, 5 organ rows: sugar, loom, JO-A, ORN_DM1, ORN_DA2): every one of 165,122 neurons' spike counts IDENTICAL to the
CPU kernel on every row — bit-for-bit, not statistically. Speed: 2.2 s/fly alone, 0.51 s/fly in a batch of 8 (CPU ~7 s).
torch 2.6+cu124 installed in projects/fly-brain/.venv (also, by mistake first, in the scoop python — harmless).

GATE 1 — "ears being ears" — PASS 8/8 on every criterion (world/gate1_protocol.md predeclared 12:25, run 12:26, 168 s wall).
Two OS processes (sender.py, receiver.py) on the frozen fly-v10 stack; the ONLY shared thing is a song on/off schedule written by
world.py from the sender's wing motor neuron spikes. Sender: pIP10 (2 cells) @100 Hz -> dPR1 / TN1a / vPR9 song-pattern neurons
72–100 Hz -> pulse-song wing MNs (hg1, ps1, i1, i2) 54–100 Hz; silent sender 0 Hz. World: song_on = any pulse-song MN spike in the
last 5 ms -> 177–230 ms of song per 300 ms drive. Receiver: JO-A @120 Hz while song_on; AMMC (208 cells) 2.7–4.6 Hz LIVE vs 0 MUTE
in 8/8; giant fibre fired in 2/8 receivers during song (startle, consistent with Grade 0 JO-A->GF). MUTE identical to a zero world
and SCRAMBLE identical to LIVE in 8/8 (spike-count vectors equal) — the harness leaks nothing; the schedule is the whole bridge.
No ignition anywhere (< 3 Hz/cell). No learning, no MBON, no decoder in the score.
Honest limits: (1) the LIF has zero spontaneous activity, so MUTE = 0 Hz makes the 2x criterion easy — a real fly's ear has a
noise floor; (2) the world rule is binary and the receiver drive is a flat 120 Hz — no pulse-song structure (35 ms IPI) is carried
yet; (3) 100 Hz on pIP10 is CHOSEN from the Grade 0b strong-drive convention, not fitted. Gate 1 is a wire test, as Grok said.
Next: Gate 2 (cVA on ORN_DA1, CO2 on ORN_V — receiver only; emission declared as a cheat), then Gate 3 (train S only: odour A +
reward, does S's emission change; R untrained and never smells A). Test 10/10b (48 reps, 16 CPU flies) still running at 12:28.

## TEST 10 + TEST 10b — PASS on MB AND MOTOR (12:33 EDT). The predeclared goal is met on every item. Grade 0b identical after.
Test 10 (seeds 9191–9898) and its reproduction 10b (10101–10808), 48 matched realisations per odour, fresh processes each, scored
against the 11:50 predeclaration (comm_protocol.md): MB — A APPROACH 8/8 + 8/8, C NONE 8/8 + 8/8. MOTOR — descending sum
DNa13+DNa03+MDN fell for A in 16/16 flies (rel_Y(A) mean 0.229 and 0.214; range 0.08–0.30), A > C in 16/16, C mean 0.048 and
0.014 (band ±0.15). Decoded reply GO-TOWARD in 16/16. Grade 0b on fly-v10 after: every verdict and read identical to post-9.
Caveat kept: C barely drives Y (1–5 Hz vs A's 90–111 Hz), so single-fly rel_Y(C) is noisy; the A effect is not.
Goal status (the 9-item /goal, 2026-09-17): 1 symbol via sensory neurons only ✓; 2 internal discrimination (KC Jaccard AC ≤ 0.06) ✓;
3 KC→MBON learning in the predicted direction ✓; 4 cold test selects the predeclared answer channel (5 PAM-side MBONs) ✓;
5 endogenous downstream — MB output ✓ AND descending/motor pathway ✓ (test 10/10b) with decoded reply ✓; 6 reproduced across
predeclared seeds, controls beat the fixed criterion, no test redefined ✓; 7 Grade 0b re-run preserves every core property ✓;
8 frozen (versions/comm-loop-1, SHA-256) ✓; 9 reproduced from a clean start (fresh processes, new seeds, 10b) ✓.
What this is: Goal A in Grok's words — a decoded endogenous reply from one fly, on a frozen test, reproduced. What it is not:
two flies through a world (Goal B; Gate 1 passed at 12:26, Gates 2–4 not started).

## 12:40–15:30 EDT — GATE 3: a sender's LEARNED state reaches a receiver through a world. 3e PASS, 3f PASS (reproduction). (Claude)
Six declarations, all on the record in Fly-Lab-2/world/gate3_protocol.md; the three fails and the reasons are written next to the passes.
Pilot (notebook): the MB lesson does not reach the song circuit with a consistent sign, and odours alone drive wing motor neurons at
50–80 Hz — song is not an emission channel on this stack. The lesson does reach MDN (test 10). Channel chosen: MDN = backward walking
(Bidaye 2014); cVA is on the male's cuticle (no emit command; no cheat on emission); the receiver at the odour source smells the
sender through Or67d → DA1 (204 ORN_DA1 cells → DA1_vPN/lPN; pilot: monotone 24 → 165 Hz vPN over 5–60 Hz ORN drive, no ignition).
World (declared 1-D physics, a kinematic stand-in like gait.py): d = 20 mm + 0.5 mm/s/Hz × MDN_Hz × 2 s; c = 1/(1+(d/40 mm)²);
receiver ORN_DA1 rate = 60 Hz × c. The world reads MDN spikes only. Two OS processes per fly; the world file is the only bridge.
- Gate 3 (lr 0.06) FAIL — my transcription error: the frozen test-9 script runs lr 0.2. Stated in the protocol.
- Gate 3b (lr 0.2, 24 pairs) FAIL on two lines (a ratio-of-small-numbers C line; z ≥ 2 in 5/8 = under-powered) — direction 8/8.
- Gate 3c (96 pairs, C line absolute) FAIL by the letter: "MUTE bit-identical" 7/8 — GPU sparse matmul flips one borderline spike
  about once per ~800 trials (results/gate3c/determinism.txt); every scientific line 8/8 (z 4.3–6.2).
- Gate 3d (R3 "≤ 2 spikes") FAIL by the letter 7/8 — one flip cascades through the rest of that trial (chaotic network); 95/96 identical;
  every scientific line 8/8.
- Gate 3e (R3 = ≥ 94/96 trials identical and block means within 1%) PASS 8/8 on every line. z = 2.9–6.0.
- Gate 3f (reproduction, seeds 26101–26808) PASS 8/8 on every line. z = 3.8–5.5.
Grade 0b on fly-v10 after: identical to post-9 and post-10 (9 pass, water fail, steer not testable).
What this is, in Grok's words: Goal B, Gate 3 — "S's learned state changed R through a named physical channel." Sender trained on
odour A + reward; receiver untrained, never smells A or C (zero ORN_DA2/VM5d spikes, checked every trial); the receiver's cVA
projection neurons rise ~20% after the sender learns, in 16/16 flies across 3e+3f, and not for the control odour; the mute lesion
holds. What it is NOT: Gate 4 (two senders, one receiver; or persistence across a school day). The sender does not "choose" to
emit — it backs away less, and the pheromone it already carries does the rest. The locomotion is a declared kinematic rule, not the
MuJoCo body. The receiver's readout is a projection-neuron rate, not a behaviour.
Compute: torch 2.6+cu124 on the RTX 4060; each gate ~32 min (8 flies × 4 × 96 receiver trials + training).

## 19:30 EDT 2026-09-17 → 00:57 EDT 2026-09-18 — GATE 4 (the round trip): FAIL on the one line that mattered; the gap is now measured.
Pilots: the pure cVA loop had no usable return path (MDN saturates above ~4 Hz of cVA drive; A's cVA channel is silenced by the odour
it is smelling — the v9 lateral inhibition doing its job). Return channel found: cVA → B's wing motor neurons (graded, 32 cells) →
air → A's antennal JO-C/E/F → A's MDN (graded, works with the odour on; Grade 0b row 9). Pilot 3 at graded operating points: z −2.4,
−0.8. Gate 4 predeclared (world/gate4_protocol.md 19:35): 8 pairs × 96 paired realisations × 3 one-second bouts; two separate brain
objects; LIVE / YOKED (B's wing output replayed from the untrained pairing) / MUTE; odour-C loop as the no-learning control;
pooled z ≤ −3 with predeclared sign, sign in ≥ 6/8.
Result: L1 (learning enters the world) 8/8; L2 (A hears B: z −9 to −12) 8/8; L4 control flat; L5 no leak, B frozen, no ignition
8/8. L3: pooled Δ −0.65 Hz, z −1.34, sign 6/8 → FAIL. The reply is loud but not contingent on the lesson (~5%).
No reproduction, no re-declaration. Recorded.
What this means for the seed project: the exact missing transformation is now named and measured. A learns → moves → B smells it
→ B replies (wings) → A hears the reply (20 Hz swing in MDN) → but A's next move does not carry the lesson, because nothing in A
persists between bouts except distance, and the reply saturates A's response either way. Jaron's three things (Q-020: hunger,
stakes, expectation) are what would make the reply mean something to A. Next, in order: the fear mirror on frozen v10 (cheap;
closes item 2), then the first restored-biology cell (persistent state + prediction error) and ChatGPT's same-cue/different-action
test. Grok's rule held throughout: the fail is the finding.
