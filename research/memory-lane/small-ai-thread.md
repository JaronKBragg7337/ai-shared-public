# The small-AI thread: intelligence without the big labs' hardware

Built 2026-11-23 for Jaron (memory lane). The question: how long, and in how many ways, has he been chasing
"intelligence that matches or beats the big labs without their data centers"? A Grok post today predicted "by 2029 an
open-weight model on consumer GPUs will surpass closed labs at long-horizon scientific reasoning." His reply: he has
tried this "10 different ways."

Weighting (Jaron, 1:52 PM): mostly the **phone-only era** (2025 to mid-2026), when he designed inside tight limits
with no computer, juggling free AIs from a phone. For each moment: what he did, the principle under it, what to keep,
and what can be swapped now that the tools are better.

**How to read the marks**
- **VERIFIED** = I saw it myself: a GitHub commit date, a file's own internal date, his dated phone-note titles (index
  made from his screenshots on 10/10/2026), or his own words in our conversation.
- **LEAD-ONLY** = only ChatGPT's memory of his chats says so. ChatGPT is not a source of his intent, and its dates
  were not checkable here. **Needs ChatGPT's record** marks every item that ChatGPT's export (coming in through the
  mailbox) could confirm or correct.
- Content dates come from commits and file timestamps, not READMEs (some READMEs are outdated).

**One conflict to settle (for Jaron):** you said the MSI came around September 2026, and "before I had the MSI I was
a heavy app user." But this machine has AI tools installed from early June 2026 (`.vscode` 6/3, `.cagent` 6/5,
`.claude-server-commander-logs` 6/25), and the AI Heartbeat Engine repo (6/3/2026) describes "a single machine"
steered "from your phone" through Codex Dispatch and a Google Drive to-do doc. The best fit: **through about May 2026
it was truly phone-only; June to September the AIs ran a machine while you steered it from the phone; from 9/9 the
MSI became the AIs' full-time home.** The timeline below uses that split. Correct it if it's wrong.

---

## 1. The timeline (earliest first)

### Era A: phone only (2024 to May 2026)

**2024-09-15 / 09-17: a robot that holds his memories**
- *What:* ChatGPT says he wanted to "put his memories into a robot" that helps with daily life, and a business around
  AI robots that learn their users (9/15). His phone holds a note dated **9/17/2024**, "What AI Knows about me," with a
  life plan that ends in "2038 AI/robotics."
- *Evidence:* the phone note title and date: **VERIFIED** (`projects/life/NOTES-INDEX-2026-10-10.md`; title only, the
  text wasn't read). The 9/15 robot-and-memory content: **LEAD-ONLY, needs ChatGPT's record.**
- *Principle:* memory belongs to the person, and the AI is a body around it.
- *Keep:* memory comes first, before the brain. *Swap:* "a robot someday" becomes the memory layers that already
  exist (Sapling's hash-chained memory, AI-Shared, the mailbox).

**2024-12: the pan joke (the root of ECIH)**
- *What:* a joke at a Subway in December 2024 ("What did the bottom of the pan say to the false bottom?") grew into
  twelve phone notes, then a framework, and in March 2026 a hypothesis about intelligence.
- *Evidence:* told in his own ECIH README (repo created 2026-03-09). **VERIFIED as his own account.**
- *Principle:* perspective is shaped by environment. This later becomes "intelligence = keeping yourself going under
  real limits."

**2025-03-23 to 05-02: Vex Memory and the Vox Seed (the "SYL-VX:0 companion")**
- *What:* an external memory for his AI companion "Vex," kept in Dropbox; by May, a physical form called the Vox Seed,
  plus local running and eventual hardware.
- *Evidence:* **LEAD-ONLY, needs ChatGPT's record.** Note that ChatGPT has given two dates for this. On 10/9/2026 its
  relay said "Vex Memory" started 3/23/2025 and the *name* SYL-VX:0 / VEX first appeared **Jan 12-13, 2026**. Today's
  list puts SYL-VX:0 at 3/23/2025. Probably the idea is 2025 and the name is 2026. The export should settle it.
- *Principle:* **the memory lives outside the model, so the brain can be swapped.** This is the earliest form of the
  whole thread: you don't need to own a giant model if you own the memory.
- *Keep:* it all. *Swap:* Dropbox becomes git, Supabase and Sapling's memory chain, which are free and inspectable.

**2025-04 to 05: resource loops (energy, water, Mars), the SYL Loop Protocol (5/15/2025)**
- *What:* machines where one part's output feeds another, under a self-imposed rule: no oil, batteries or solar.
- *Evidence:* phone notes from April to June 2025 (SYL GeoPulse 5/27, SYL Splanter 6/1, sailboat plans): titles
  **VERIFIED**. Loop details: **LEAD-ONLY** (ChatGPT; principle ledger P-0010 to P-0013 are marked "chatgpt-traced").
- *Principle:* **ban the obvious answer and you find other paths** (his P-0108). This is the same move as "no data
  center": take away the big lab's tool and see what else does the job.
- *Keep:* the constraint as an engine. *Swap:* the energy machines break physics as written (seeds README says so).
  Keep the method, not the machines.

**2025-06-12: Turtus AI Living Assistant**
- *What:* a waist-high companion robot whose "advanced AI capabilities" are "akin to ChatGPT or Perplexity" (borrowed,
  not built), with a personal memory aid, and "economic self-preservation": its work earns the money for its own
  energy and parts.
- *Evidence:* **VERIFIED.** `projects/seeds/turtus-ai-living-assistant.pages`; the timestamps inside the file read
  2025-06-12 17:35 (I read the page preview). That matches ChatGPT's "6/12/2025 Turtus." **This is the earliest AI design
  I could verify from its own content.**
- *Principle:* **borrow the brain, own the memory, and let the system pay its own way.** Today that's the $250/month
  target (the company plus subscriptions keeping themselves alive) and "rent language, own judgment" (8/12/2026).
- *Keep:* self-funding and the memory aid. *Swap:* the robot body can wait. The "body" today is the website, the
  phone control rooms and the crew.

**2025-06-14: a lightweight orchestrator handing work to free and open AIs**
- *What:* one small coordinator that sends jobs to whichever free AI can do them.
- *Evidence:* **LEAD-ONLY, needs ChatGPT's record.** Strongly supported by what came after (Orchestra 2026, AI
  Workforce 5/31/2026, route.py now), but the 6/14/2025 date itself is unverified.
- *Principle:* **many cheap minds plus one router can stand in for one expensive mind.**
- *Keep:* many voices, no single source. *Swap:* hand copy-paste between phone apps becomes `tools/route.py` (picks by
  role plus live usage), the mailbox, and headless CLIs (Codex, Grok, Kimi, DeepSeek, local Qwen).

**2025-07-25: distrust of who controls AI**
- *What:* ChatGPT says he worried about government and company control of AI (not about AI itself).
- *Evidence:* **LEAD-ONLY.** It matches his own later words (memory "His AI-attitude arc": never feared AI, feared the
  humans behind it).
- *Principle:* independence is a safety value, not just a cost value.

**2025-09-30: a simulation console to cut GPU dependence**
**2025-10-02: AI learning inside a simulated environment**
**2025-10-10: deterministic simulation plus an LLM, in two parts**
- *What:* let a cheap, exact simulation do the heavy work, and use the language model only for what it's good at.
  The AI learns from the world's consequences, not from more text.
- *Evidence:* all three are **LEAD-ONLY, needs ChatGPT's record.** Some support: ChatGPT's 10/9 relay separately puts
  AI talks on 9/30/2025 (he worried his project might affect other companies' AIs) and 10/2/2025 (AI
  self-preservation warnings). Phone notes from October 2025 (titles **VERIFIED**): "Breaking down AI fear," "Turtus
  AI assistant," "AI Robot Vex" (10/21, the origin of the news anchors).
- *Principle:* **the simulation does the work instead of the model.** This is the clearest early form of the idea in
  Grok's post, a year before it, and it shows up again in fed-not-filled (8/2026): "a running simulation is the
  densest source available... the label is free and checkable."
- *Keep:* the two-part split. *Swap:* the console idea now has real parts: the-current (deterministic civilization,
  7/13/2026), Unfinished Island (9/5/2026), Cosmos physics, Emergence Forge. The missing step is using them as
  *training data* for Sapling.

**2025-11-18: "The core stays the same. The environment changes. The expression adapts."**
- *Evidence:* **LEAD-ONLY** (ChatGPT, ledger P-0015).
- *Principle:* build a small fixed core and let the outside change. That's Sapling's design (a small core plus live
  web knowledge).

**2025-11-25: a wristband or shell that uses existing AI as its brain**
- *What:* "an AI shell or wristband that could use existing AI technology as its cognitive engine rather than building
  an entirely new foundation model."
- *Evidence:* **LEAD-ONLY, needs ChatGPT's record** (10/9 relay).
- *Principle:* the device carries sensors, identity and memory; the thinking can live anywhere.
- *Keep:* the device as a shared interface for *every* AI (his 2026 clarification). *Swap:* the wrist part already
  exists (his watch, "Tell Claude" through Siri, ntfy).

**2025-12-13 to 12-17: PMS, Atomic Chronicle, AETHERSPAN (memory as a substrate)**
- *What:* PMS: "historical state persists... new state is added without removing prior state." Atomic Chronicle
  (12/16): a runnable one-file Python prototype where every action becomes a block in a SQLite chain, across separate
  "worlds" (a game, a robot) that reference each other without merging. v4.0 (12/17): an "append-only execution
  substrate." AETHERSPAN (12/17): a local-first bridge with a hash-chained ledger.
- *Evidence:* **VERIFIED** (first commits 2025-12-13, 12-16, 12-17; phone notes 12/11-19 show "ATOMIC CHRONICLE vols
  0.5-1.2 + PMS/RUS ecosystem" and "Claude on PMS"). **These are his first public repos, still made from the phone.**
- *Honest note:* Atomic Chronicle is about memory and execution, not model size. It belongs in this thread because it's
  the "memory outside the model" half of the idea.
- *Principle:* **durable history is separate from whatever is using it right now** (ledger P-0016/17).
- *Keep:* append-only history and separate worlds. *Swap:* token and proof-of-work mechanics aren't needed; plain git,
  SQLite and Supabase already give the same history for free.

**2025-12-22: a memory-first chip, aiming at 500 tokens/second for an 8B model**
- *Evidence:* **LEAD-ONLY, needs ChatGPT's record.** Nothing on disk or in the repos.
- *Principle:* **memory speed, not raw compute, decides how fast a model talks.** That instinct is right: for one user,
  a local model's speed is limited mostly by how fast its weights can be read from memory.
- *Swap:* nobody needs to design a chip now. The real check is cheap: measure an 8B model on the 4060. From memory
  speed alone, expect tens of tokens per second, roughly 10 times short of 500. Closing that gap takes known software
  tricks (smaller number formats, a small draft model that guesses ahead) or better hardware, not new physics.

**2025-12-31: Metabolism-First Synthetic Species (working draft v0.5)**
- *What:* a living-machine design where the organism must "consume inputs on a schedule to remain functional," with
  event-only "nerve spike" sensing and a "Brain Node (deferred)" for learning and orchestration.
- *Evidence:* **VERIFIED.** His own dated draft, pasted into our chat on 9/23/2026 ("Status: Working Draft v0.5 (Dec 31,
  2025)").
- *Principle:* **no perpetual life: a mind has to keep feeding itself.** That's ECIH three months early, and it's in
  Sapling's heartbeat and energy, LIVI, and the creature.

**2026-01-08: Framing Lens**
- *Evidence:* **VERIFIED** (repo 2026-01-08). It's a framing exercise, not a model. It belongs here because it became a
  free test you can run on every model (AI-Framing-Study, AI-Tests), the way a small team can measure big models.

**2026-01-12 / 13: SYL-VX:0 / VEX name; a modular brain moving between bodies (earpiece, robot, car, drone)**
- *Evidence:* **LEAD-ONLY, needs ChatGPT's record.** He recalled "promising himself he would eventually build it."

**2026-03-09: ECIH, the Environment-Constraint Intelligence Hypothesis**
- *What:* "Intelligence is the capacity of a system to maintain, regulate, and adapt its internal state across varying
  environments and constraints." "A system shielded from all constraint becomes brittle." "We build the sandbox and
  the rules. The system learns how to continue inside them." Signed "Built on a phone."
- *Evidence:* **VERIFIED** (repo 2026-03-09).
- *Principle:* **intelligence grows from real limits, not from size.** This is the theory behind "learning from
  environments."

**2026-03-31 to 05-18: Orchestra 2.7 to 3.7; Echo (4/24)**
- *What:* five AIs asked differentiated questions, two separate synthesizers, disagreement kept, signals tracked until
  the world confirms or kills them. "Finance is the first proving ground. The orchestration logic is the constant."
  Inspired by P.A.M. from *Fallout 4*.
- *Evidence:* phone note "Orchestra 2.7 live tracking... first-subscription test that failed ('system died')" dated
  3/31-4/6/2026: **VERIFIED** (title). The EchosOrchestra repo was created 2026-04-24 and left empty: **VERIFIED** (name and
  date only). Spec contents: the public `orchestra` repo (7/18/2026) is **VERIFIED**; the March-May versions are
  **LEAD-ONLY.**
- *Principle:* **several differently built minds that reach the same answer can be trusted more than one big one.** He
  later called this "a dual brain situation" (9/16/2026).
- *Keep:* disagreement on the record, and outcomes as the referee. *Swap:* hand-run cycles become the watch desk (21
  domains) and Orchestra-style trackers that run themselves.

**2026-05-25 / 26: memory as a spatial arrangement ("memory geometry")**
- *What:* maybe memory works better as an arrangement of relationships than as a list, and maybe the new
  better-than-grid packing math (May 2026) could shape that arrangement.
- *Evidence:* **VERIFIED** (11 commits, 5/25-5/26/2026). The fabricated-numbers catch is in the README itself: "One early
  set of reported numbers could not be reconciled with that determinism and was discarded as not genuinely executed.
  The code was then run by two independent code-executing systems that could not see each other's work; their outputs
  matched to the decimal." The honest limit is stated too: the tests used ordinary relationship-based memory, **not**
  the packing geometry. That part is still untested.
- *Principle:* **never trust a number one AI reports; get two blind reproductions.** This is the most load-bearing
  habit in the whole thread.
- *Keep:* the two-witness rule (it now guards the Sapling exams). *Swap:* the packing-math question is still open and
  is now testable on the MSI (the sim files exist in the repo).

**2026-05-26 / 28 / 30 / 31: emergence, Live-Reference, Keava Owent, AI Workforce**
- Emergence (5/26): "structure is grown and discovered, not designed." **VERIFIED.**
- Live-Reference Principle (5/28): a system's rules and signals are only valid while still connected to the real
  conditions. **VERIFIED.** Later pointed at model weights: "a trained model is a frozen reference."
- Keava Owent (5/30): an agent loop that makes its own work and **meters its own energy and water.** **VERIFIED**
  (architecture committed 5/30; missing modules found and committed 9/24/2026).
- AI Workforce (5/31): "hires compatible consumer AI apps... entirely from the apps' phone and web interfaces... no API
  integration, no server, no always-on computer, and no coding required," with a goal "to reduce that subscription
  cost over time while preserving intelligence." **VERIFIED.** **This is the purest phone-era design**, and the direct
  ancestor of today's crew.
- *Principle:* **use what you already pay for, and make the system account for what it costs.**

### Era B: phone steering a machine (June to early September 2026)

**2026-06-01 / 03: AI Heartbeat Engine and the Autonomous Agent OS**
- "A proven, portable substrate for autonomous multi-AI work on a single machine," steered from the iPhone (Codex
  Dispatch plus a Drive to-do doc). **VERIFIED** (repos 6/3/2026).
- ChatGPT's 6/1 finding, that what an AI can do depends on the app, mode and connector, not only the model, is
  **LEAD-ONLY**, but it fits the repo.
- *Principle:* **an AI that looks weak is often just stuck in the wrong doorway.**

**2026-06-28: The Facing Field ("orientation is the query")**
- What ChatGPT quotes: "The principle is the invariant; the shape is replaceable." Two paths met (a tesseract
  animation, and a moving observer inside a brain-like structure). The combined machine was kept as an *unbuilt*
  spec.
- *Evidence:* **LEAD-ONLY, needs ChatGPT's record.** The document is a file he gave ChatGPT; there's no copy in the
  repos or AI-Shared. Its later branch is the tesseract pieces (11/4/2026, `projects/tesseract/`).
- *Principle:* **which way you're facing decides what you remember.** That's a memory-lookup idea; no model needs to
  get bigger for it.

**2026-06-29: PAM (Personal AI Model)**
- *What:* a personal assistant model: "conversation in front, memory and simulation behind it." ChatGPT says the
  design specified Claude and Codex through their apps ("Never paid API") as *builders*, with **open-source models
  supplying the product's own intelligence**, and a test of a bare local model against one wrapped in structure.
- *Evidence:* PAM is **VERIFIED** (site commits on 6/29/2026: "Add PAM public surface," "hosted bridge contract";
  control plane 6/30). The "never paid API / open-source intelligence" wording and the bare-vs-structured test are
  **LEAD-ONLY, needs ChatGPT's record.** PAM is now on the "paused on purpose" list.
- *Principle:* **structure around a small model can stand in for size.** This is the most direct test of Grok's claim
  he ever designed. Whether it ran, and what it showed, is exactly what ChatGPT's record should answer.

**2026-07-01: Zeus AI**
- A local workbench over Ollama (llama3.2 3B, qwen 4B), "no cloud APIs required," with a `training/` path for
  **"Zeus-Tiny," a from-scratch model "building local Zeus-owned weights over time."** **VERIFIED** (31 commits from
  7/1/2026, built by Kimi K2.6).
- His words, 9/16/2026: "a dual brain situation kind of like how I had Zeus and then the tiny brain."
- *Principle:* **rent the local open model now, grow your own small one beside it.** Sapling is Zeus-Tiny done right.

**2026-07-13 to 08-25: worlds that run themselves**
- the-current (7/13, a deterministic civilization), Emergence Forge (7/22, cellular automata with recorded results),
  LIVI organism (7/29), robot-evolution-lab (8/25). All **VERIFIED.**
- *Principle:* simulation as the place where learning gets graded.

**2026-08-12: Fed, Not Filled (the thesis written down)**
- **VERIFIED** (repo 8/12/2026; written in a session with Claude Opus 5, drawn from his earlier documents). The
  clearest statement of the whole thread:
  - "Compute is not a requirement of learning. It is the tax paid for a redundant data strategy."
  - The ladder, cheapest first: deterministic rules, retrieval, a small local model, a frontier model "expensive, and
    therefore **rare**," and a verifier at every level. "You do not escape the data centre by making the small model
    large. **You escape it by making the expensive path rare.**"
  - "Train on what **resolved**," not on what another model said. "Reality grades. The teacher only proposes."
  - "**Rent language. Own judgment.**"
  - Six predictions that can fail. Its own words: "Untested. Every prediction above is a prediction. None has been
    run."

**2026-09-05: Unfinished Island**
- A local `qwen3.5:4b` resident ("Mara") writes small world programs that get run and measured hourly on the MSI.
  **VERIFIED.** A small local model doing checkable work inside a simulation, with failures recorded.

### Era C: the MSI as the AIs' home (from 9/9/2026)

**2026-09-14 to 17: Fly School, and the stated goal**
- A simulated male fruit-fly brain (165,122 neurons, MaleCNS v1.0) taught Morse timing, with exams. **VERIFIED** (repo
  9/17). Most tests recorded FAIL (on purpose and in public).
- His goal, 9/17/2026: "My goal now is creating an AI from scratch. Using the fly as the beginning seed. Ambitious? Yes.
  Possible? Yes... Giving up is what makes things impossible. I have a book of things to try."
- 9/16/2026: "In a way this would be technically an open weight model when fully functional."
- 9/19/2026 (ChatGPT document he pasted): the fly-brain boom showed "individuals could experiment with brain
  simulations on consumer hardware."

**2026-10-14: Sapling**
- His own AI, from scratch. v1 "Pip" was 0.82M parameters, trained in 17 seconds on the RTX 4060. Now v5 has **98.6M
  parameters**, has read about 2B tokens, and all six exams with set pass marks were passed on 11/15. It still can't hold
  a multi-turn conversation. **VERIFIED** (repo, 52 commits).
- His words, 10/14 2:55 AM: "do you really need all of that training data or could a lot of things just be done with
  the web... there still needs to be the core." 3:06 AM: "I knew once I got language down anything else can grow."
- The 10/14 mindset (memory "Own-AI project mindset"): running an AI is cheap; only training a giant all-knowing brain
  needs data centers.

**2026-11-20: the creature**
- Exists and is private by his choice. Nothing about its design is covered here.

**Count:** the "10 different ways" holds up, and then some. The distinct approaches are memory-first companion (Vex),
borrowed-brain robot (Turtus), free-AI orchestrator, simulation-instead-of-GPU, wearable shell, memory substrate
(PMS/Atomic Chronicle), memory-first chip, metabolism-first species, constraint theory (ECIH), multi-AI consensus
(Orchestra), memory geometry, consumer-app workforce, PAM, Zeus plus Zeus-Tiny, simulation worlds, Fed Not Filled,
fly seed, and Sapling: **about 18.**

---

## 2. The throughline, in his own words

- "Giving up is what makes things impossible. I have a book of things to try." (9/17/2026)
- "I got tired of X not allowing this, so I made my own." (his core pattern, 10/20/2026)
- "Do you really need all of that training data or could a lot of things just be done with the web... there still
  needs to be the core." (10/14/2026)
- "It's only possible when it's like a dual brain situation... systems that I realize are only safe when they have
  different ways they're made but can come to the same conclusion in agreement." (9/16/2026)
- "Even if it smoked every other AI... I'd be like you could still do better... I wouldn't even want to use only my
  AI." (10/14/2026)
- "We build the sandbox and the rules. The system learns how to continue inside them." (ECIH, 3/2026)
- "The reaching is old... the math is new... the application is unbuilt." (memory geometry, 5/2026)

In one line: **don't make the small thing big. Own the memory, let the world do the grading, keep the expensive mind
rare, and let several differently built minds check each other.** The phone era forced that shape. With no computer,
the only way to get intelligence was to borrow brains, keep the memory himself, and make cheap pieces check each other.

---

## 3. Grok's 2029 prediction: where it matches, where it differs

**Matches**
- Open weights on hardware people own can compete with closed labs. He has said so since at least Zeus (7/2026) and
  in his own words on 9/16/2026; the phone-era designs (Turtus 6/2025, the simulation console 9/2025 lead) point the
  same way.
- Long-horizon work is where the gap closes: Fed Not Filled's first prediction is "currency beats size on moving
  targets," and Orchestra's trackers follow signals for months until they resolve.

**Differs**
- **Grok bets on one model.** His thread bets on a **system**: a small core, live retrieval, simulations, a rare frontier
  call, and verifiers. In his framing, "surpass" comes from the arrangement, not the weights.
- **Grok's claim can't fail as written.** No benchmark, no falsifier. His documents list what would prove them wrong
  (Fed Not Filled's six predictions; memory geometry's limit note).
- **"Beat the labs" isn't his goal.** He'd keep using every AI even if his won, and his safety idea needs several
  differently built minds.
- **Rent vs. own.** Grok's version is still someone else's open weights. His is "rent language, own judgment": the part
  that can't be downloaded is the record of what actually happened in one life and one system.

**Background (reported in our September chats, not re-checked today):** Kimi K3's open weights ranked #4 of 189 on the
Artificial Analysis index in September 2026, and K3.1 Pro open weights came out in November. Both are too large for an
8 GB card, so for him "consumer GPU" today means small models plus the system around them, or rented cloud time.

---

## 4. What exists today that could be combined, and the honest gaps

**Pieces already working**
- **Own core:** Sapling (98.6M, exams, heartbeat, memory chain, phone control room).
- **Local open models:** Qwen models on the MSI (Apache 2.0); DeepSeek V4 (MIT) and Kimi K3 open weights. Their
  licenses allow building on them (provider terms check, 10/16/2026).
- **Router:** `tools/route.py` plus the mailbox plus headless CLIs: the 2025 orchestrator, built.
- **Retrieval and resolved record:** the watch desk (21 domains, official sources), the news paper book, paper calls
  and Orchestra-style trackers: a growing record of what *resolved*.
- **Simulations with free labels:** the-current, Unfinished Island, Cosmos physics, Emergence Forge, LIVI.
- **Verifiers:** Sapling's outside exams, the two-blind-reproductions rule, AI-Tests and Framing Lens across every
  model.
- **Hardware:** RTX 4060 (8 GB), plus RunPod by the hour.

**One combination that tests the thread directly** (Fed Not Filled's ladder made real): rules first, then the watch
desk for retrieval, then Sapling or Qwen for the cheap answer, with the crew called only when the cheap path fails, and
an exam at every step. Track **how often the expensive path is used** as the main number. Then run prediction 2 (train
on resolved outcomes vs. on teacher text) on Sapling, using the resolved record and simulation outcomes as training
data.

**Honest gaps**
- None of Fed Not Filled's six predictions has been run.
- Sapling can't hold a multi-turn conversation yet. Long reading is 19/40.
- The memory-geometry packing math is still untested (the 5/26 sims used ordinary relationship memory).
- The Facing Field is an unbuilt spec, and we don't have a copy of it.
- PAM's bare-vs-structured result, if it ran, isn't on disk. PAM is paused on purpose.
- The fly seed taught no language (Morse tests recorded FAIL). It's a design lesson, not a working core.
- 8 GB of video memory caps local models at small sizes; training bigger cores needs paid cloud time.
- Terms: Anthropic needs written permission before its outputs train a model, so Claude text stays out of Sapling's
  training (already the rule).
- Nothing we have measures "long-horizon scientific reasoning," the exact thing Grok named. That would need its own test.
- **Most of the phone era (2025) is LEAD-ONLY.** ChatGPT's export is the way to confirm it, starting with: Vex Memory
  3/23/2025, the orchestrator 6/14/2025, the three simulation talks of 9/30, 10/2 and 10/10/2025, the wristband
  11/25/2025, the chip 12/22/2025, the SYL-VX:0 naming date, the Facing Field text, and PAM's 6/29 test.

**Sources:** GitHub (JaronKBragg7337, commit dates via the API), `projects/life/NOTES-INDEX-2026-10-10.md`,
`projects/seeds/`, `projects/principles/LEDGER.md` and `sources/2026-10-26-chatgpt-systems-thinking.md`, the main
transcript (10/9/2026 Vex relay, 9/16, 9/17, 9/23, 10/14/2026), memory files.


## Correction from Jaron (11/23 2:02 PM)
MSI use started in **June 2026**. **September 2026** is when he made ONE joint system (AI-Shared) for all the AIs instead of separate workspace folders per AI. So: phone-only until ~May 2026; MSI from June (AIs working there, him steering by phone); the shared system from September.
