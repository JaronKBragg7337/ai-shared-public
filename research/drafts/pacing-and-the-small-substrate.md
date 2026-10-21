# Pacing the Frontier, and the Thing Underneath It

### A timeline of one weekend, both perspectives held, and the demand question nobody in the room asked

**Author:** Jaron K. Bragg
**Status:** Working draft, shared openly. A pattern to test, not a verdict.
**Date started:** September 13, 2026
**Companion:** The Substrate Demand Cascade (Sept 7, 2026) — this document is its other half.

---

## A note before the argument

This is not a claim that any executive is lying, that AI safety is fake, or that a fruit fly on a laptop threatens a trillion-dollar industry. Those would be motives, and motives are not observable.

The narrower claim is structural, the same shape as *The Structural Conflict*: **systems built by those with power protect those with power, and the people not in the room have no standing in the design.** The tools change. The pattern holds. This document lays the events of one weekend beside that pattern and asks whether it fits — and then asks a second question that the first one hides.

Everything below is marked **measured** (dated, sourced) or **chosen** (my read). If I have blurred the two, that is the error, and re-separating them is the fix.

---

## 1. The timeline (measured)

| Date | Event | Source |
|---|---|---|
| Jul 16, 2026 | Moonshot releases Kimi K3 (2.8T MoE, 104B active, 1M context). #1 on Frontend Code Arena ahead of Claude Fable 5 and GPT-5.6 Sol. $3/$15 per M tokens. | Fortune; Arena.ai |
| Jul 27 | K3 weights released. First time an open-weight model held #1 on a major public frontier leaderboard while sitting close to (still behind) the closed models on composite evaluations. | Moonshot |
| May 2026 (context) | xAI's Colossus 1 reportedly runs near 11% model-FLOPs utilization after Grok's training moves to Colossus 2; Anthropic rents the whole site at ~$1.25B/month through 2029, ending a year of public hostility from Musk. | Willison; Forbes |
| Sept 10 | OpenAI pauses new $200 Pro signups citing "unprecedented" demand for GPT-6 Astra. | @thsottiaux |
| Sept 11–13 | Dozens of independent projects run the FlyWire / MaleCNS fruit-fly connectome on laptops and in browsers: reading, fighting, trading, dating, Pong, poker. Several are one person, one weekend. | cobanov/awesome-fly; X |
| Sept 11 | Shanghai AI Lab + SJTU release NCP-ArchPreview (8.9B, open checkpoints): next-concept prediction added alongside next-token; reaches OLMo-3-7B's final loss on **51.3% of the tokens**, ~85% of standard compute, +2.45 macro / +5.99 GSM8K after full training. (The viral post says "ends the LLM era"; the abstract says NTP is preserved — measured is "half the data, same loss.") | arXiv / HF ArchSpace-Collection |
| Sept 12 (Sat) | Dario Amodei publishes "We Must Pace the Frontier": slow frontier capability growth; independent evaluators with employee-level access inside labs; common standards; limits on recursive self-improvement. Warns that a misaligned agent swarm could seize large parts of internet infrastructure within 6–12 months. Explicitly "pace, not halt." | Anthropic; WaPo |
| Sept 12–13 | Altman: "I agree with Dario that we need to pace the frontier." OpenAI commits to the evaluators. Musk: "Dario is right." Hassabis (Google DeepMind) backs the direction by Sept 13. Four, not three. | Axios; CoinDesk; reporting Sept 13 |
| Sept 13 (Sun) | Trump rejects it: "whoever wins AI wins." David Sacks argues that applying closed-model standards to open models could progressively exclude open models from the market. (Exact wording pending original source.) | Fortune/Yahoo |
| Sept 13 (pm) | The two readings appear independently on X: @CodeMonkeyZ (26k views) states the incumbent-fear thesis as fact; @Object_Zero_ (13k) states the small-substrate thesis with numbers (160k neurons, 10⁷ synapses, "outsized results with miniscule models," air-gapped autonomy, zebrafish next at 10× synapses / 2× raw data). Neither cites the other. | X |
| Sept 13 | A $5 trade on a fruit-fly-adjacent system, placed by a $30/month bot with no human step, settles +$9.71 on a public ledger. One trade. Sample size one. | this author's ledger |

---

## 2. Every actor's reason (held, not ranked)

- **The four CEOs.** They have seen internal evaluations the public has not. If those show something that frightens them, calling for pacing is the responsible act, and the cost to their own valuations is real evidence of sincerity. *This is a legitimate reading and I am not dismissing it.*
- **The administration.** A race with China is the frame it lives in; slowing is losing. Sacks's warning about small labs is the first time anyone in power named who a pacing regime would fall on.
- **Moonshot and the open-weight labs.** They are not in the room. A proposal for evaluators inside labs cannot reach them. Whatever the proposal intends, it can only bind the labs that would comply.
- **The independent builders.** A person with a laptop and $70/month of subscriptions ran a whole-brain simulation, a live trading loop, and a public ledger in four days. None of that touches a frontier threshold. None of it was in anyone's forecast.
- **The people paying for the data centers.** Hundreds of billions committed to buildings, chips, and power on a demand curve that assumes the useful work runs on frontier models in central facilities.

None of these needs are illegitimate. That is the point of the frame.

---

## 3. The pattern (chosen — my read, marked as such)

Three rivals who cooperate only when both sides gain (the Colossus deal is the measured example: hostility ended the week an empty building needed a tenant) converged on one weekend, eight weeks after the first open-weight model reached the frontier, on a proposal whose immediately actionable mechanisms — evaluators inside labs, common standards — operate through the participating labs, while its wider reach waits on governments.

I do not know why. Fear of a real capability and protection of a position produce the same proposal, and the record cannot tell them apart. What the record *can* say is what the proposal targets: embedded evaluators and common standards impose obligations on frontier developers first; its broader reach depends on governments adopting the later stages. Whether that entrenches incumbents, burdens challengers, improves safety, or all three is *not yet measured* — the proposal is two days old. That is one of the things this record exists to test. *Target is measured. Effect is a prediction. Intent is not observable.*

---

## 4. The second question — the one the first one hides

The Substrate Demand Cascade argued that automation may raise infrastructure demand twice: once through machines, again through freed human time. This document is its other half:

> **If useful work migrates to small, taught, physics-honest systems that run on hardware people already own, the demand forecast underneath the current buildout is wrong in the other direction.**

This is not a claim that it *will*. It is a claim that it is *testable*, and that one weekend produced data points:

- A frontier model ran one kernel-editing job for two-thirds of a five-hour usage window. Scripts on the same laptop ran the equivalent thirty-second brain simulations for nothing. **The paid part was the cheap part** — the reasoning, not the compute.
- The fruit-fly projects run on a phone's worth of compute. On the taught path, their limit is not hardware but physics nobody has filled in yet (synaptic time constants, neuromodulator baselines) — a *knowledge* bottleneck, and knowledge does not need a data center. On the trained path, one person has already pushed language through the fly's wiring from scratch on a single consumer GPU (FlyText). Either way, the substrate fits on hardware people own.
- The trading loop that settled +$9.71 used two Python scripts, a scheduler, and a browser. It would run on a $5/month VM.
- The day before the pacing letter, an open 8.9B model matched a 7B baseline's loss on half the training data and 85% of the compute — the frontier *recipe* itself getting cheaper, published openly, from outside the room. Efficiency, not just smallness, is the demand-side risk.

### 4b. The phone (the part that was looked over)

The strongest version of the second question is not "laptop instead of data center." It is **phone**.

- *Measured:* the FlyWire brain already runs in a browser tab (Lulzx/fly-brain; snedea/flybrain). The hiragana reader is 19 KB of WebAssembly. One 165k-neuron LIF step is a few million operations; an iPhone 14's chip does roughly fifteen trillion per second. The brain is not the bottleneck. The screen is.
- *Measured, personal:* across ~100 AI-built projects, half of them games, every warning was "it won't work on a phone." It ran better on the phone than on the laptop, every time. That is not luck. Phones carry the most optimized graphics and compute stacks in consumer hardware, because that is where the money went.
- *Consequence:* the "cost before the cost" — the machine — goes to zero. About five billion people already own the hardware. No data center, no VM, no donated laptop, no monthly bill. A brain that learns, on the thing already in the pocket.
- *Honest limit (chosen as the next job):* the full brain in a browser is not yet the **learning** brain. The mushroom-body plasticity and the dopamine loop have not been run on a phone by anyone I can find. That is a port of pieces that already exist, not new research — and it is the seam.

- A null result already sits beside the demos: one developer's MaleCNS Pong circuit failed to learn, and the failure traced to assumptions about pathways and plasticity, not FLOPs. That is the knowledge-bottleneck claim showing up as a failure, which is the only way it can be trusted.

Falsifiers, so this stays a hypothesis: small systems may plateau below usefulness; the physics may turn out to need frontier-scale search to fill in; agent concurrency (the first document's point) may swamp any per-task efficiency; and one weekend of demos is not a demand curve.

---

## 4c. The theory (chosen, marked as reach, offered to be disproved)

Amodei's plan exempts "small models, startups, academics" and states Anthropic "has never advocated for a ban on
open-weight models." His stated problem with open weights is mechanical: a certification of alignment cannot travel with
a file that anyone can edit. Critics reply that his checkpoints would still catch any open model capable enough to
matter. Both are right, and both leave the same question open: *where does the safety property live, if not in the
file?*

The answer this project keeps arriving at, from three separate builds (Zeus's dual brain, the VEX tiny-brain quorum,
Orchestra's five models), is stated here as a theory:

> **An open system is safe in proportion to how many differently-made minds must agree before it acts. Neither a
> frontier model nor a small taught system is safe alone; each is the other's check.** The frontier model is the only
> thing fast enough to build, watch, and correct a small system as it grows. The small system is the measured,
> physics-bound thing that cannot be talked into anything, and keeps the frontier honest. Disagreement between them is
> not failure; it is the signal that something needs a human.

A correction from the author the same evening: a quorum that requires another AI at act-time is the wrapper problem
moved one layer down. The quorum is a build-phase rule. The end state is a small system that can act alone — and where
the safety property lives is then the real question. The working answer: a learned behavior in a connectome is
unreadable by construction (a lesson is a distribution over millions of synapses, not a line), and the system can be
*taught* to act only on cryptographically signed instructions — the key is a habit, not a file. Copy the weights and you
have a system that will not take your orders. The public ledger of its retraining is what shows if that ever changes.
This is stated as a design to test, not a result.

This is falsifiable: build the quorum, log every disagreement, and show whether the disagreements predicted the
failures; then teach the signed-frame discrimination and show whether it holds on held-out inputs. It is also the reason this document is not an argument against the pacing letter. It is an answer to the
question inside it — offered to the labs as a mechanism they said did not exist, and to independent builders as a
blueprint that does not require a data center. Both stay relevant. That is the path.

## 5. What I am not claiming

- That any named person acted in bad faith.
- That AI safety concerns are pretextual. Both things can be true at once; the record does not decide.
- That a fruit-fly simulation caused anything. It is an example of what "below the threshold" looks like, not a cause.
- That frontier models become irrelevant. The record of this same weekend shows the opposite division of labor: a frontier model caught a sign error in a synapse equation before it ran and built a verified kernel in 27 minutes; free scripts on a laptop then ran the thirty-second simulations. Small taught systems do not erase big trained ones — they are what big trained ones are *for*. Many paths will exist at once, the way Bitcoin did not end banks.
- That any one architecture is settled. NCP's real lesson is that the training *objective* was a knob nobody had turned; the fly's learning rule is likewise one choice among several. No approach is stone. The school (same tests, different brain or different rule, comparable row) is how that stays open.
- That this is finished.

## 6. What would change my mind

- Pacing rules that explicitly exempt or protect small and open-weight developers, with teeth.
- Published internal evaluations showing the capability the proposal is aimed at.
- Small taught systems failing to leave the demo stage over the next two quarters.

## 7. The principle underneath

> When those in the room design the rules, the rules fit the room. The people outside it — open labs, one-laptop builders, people whose lives could change on a $70 stack — are not represented by anyone's fear or anyone's balance sheet. The only defense they have is a record: dated, sourced, public, and honest about what was measured and what was chosen.

That is what this document is. If it holds weight, it worked. If it doesn't, rebuild.

---

*Draft v0.1, September 13, 2026. Human thinking; AI-assisted structure and wording (Claude, Anthropic — which is also one of the companies named above; that is stated here for provenance, not credentialing).*

---

*Standing note from the author, September 16, 2026: nothing in this document is to be read or used as a case for the
downfall of the frontier companies named in it. Whatever the demand question turns out to show, the frame is the
tooling loop — the frontier model builds what the small system runs, and the small system's success sends people
back to the frontier for the next map. Both stay relevant. That is the path, and it is also what the record shows.*
