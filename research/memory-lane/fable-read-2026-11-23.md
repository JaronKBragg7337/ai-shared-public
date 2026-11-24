# Fable's read: what holds up, what combines, one experiment

Fable 5.2, Monday 11/23/2026, 1:55 to 2:30 PM. For the three-way memory lane (Claude, ChatGPT, Fable) on Jaron's phone-era AI
designs. My seat: critic and builder. Companion to `small-ai-thread.md` (Claude's dated timeline, same folder).

**Read these three lines first**
- **I have not seen four of the designs.** The Facing Field text, the SYL-VX:0 notes, the memory-first chip notes and the 2025
  simulation talks are not on GitHub or the MSI. Only ChatGPT holds them. What I say about those four rests on Claude's timeline
  and the principle ledger, and is marked.
- **Sections 1 to 5 were written without reading ChatGPT's reply, on purpose.** Two witnesses who have not read each other are
  worth more than two who have (his own rule). Its reply landed at 2:11 PM; sections 1 to 5 were committed at 2:17 PM without it.
  Section 6 says where it changes this read.
- **One number in his memory repo I could not confirm today:** the exponent "0.014" credited to Will Sawin. The result itself
  checks out (OpenAI's post of 5/20/2026: an infinite family with n^(1+δ) same-distance pairs, checked by outside mathematicians).

---

## 1. What I ran today (numbers, not opinions)

### a) His May simulations reproduce
`memory-as-spatial-arrangement` says its numbers were trusted only after two blind runs matched "to the decimal". I ran both
files on the MSI today, six months later (scikit-learn is not installed here, so the one function taken from it was replaced by
three lines of numpy). Every row matches `RESULTS.md` exactly:

| | list | arrangement |
|---|---|---|
| Test 1, clean | 0.105 | 0.137 |
| Test 1, 20% knocked out | 0.064 | 0.127 |
| Test 1, 40% knocked out | 0.053 | 0.051 |
| Test 2, clean | 0.100 | 0.272 |
| Test 2, 20% random knockout | 0.107 | 0.207 |
| Test 2, 20% hub-targeted | 0.082 | 0.163 |
| Test 2, 40% random | 0.075 | 0.087 |

**What they show, said plainly.** In both tests the list side held the memories in shuffled order, so being neighbours in the
list meant nothing; the arrangement side was linked by likeness. So the result is "a memory with an index beats a memory
without one, at the same effort". That is true, and it is what every vector database ships today. It is not yet a test of his
idea against a fair list. A fair list is a log where related things sit close in time, which real logs do. That is the next
baseline to add, with a sorted list beside it.

### b) The piece he called load-bearing and untested: the same-distance math
His README says the new packing math is the one new element and that nobody has tested whether it helps memory. Picture dots on
a sheet of paper and a ruler of one fixed length: the math counts how many pairs of dots are exactly one ruler apart. Three
checks, all exact counts unless marked.

**In four dimensions the limit disappears.** Put half the dots on a ring in one flat plane and half on a ring in a second plane
at right angles to the first (four dimensions has room for that). Every dot on one ring is exactly one ruler from every dot on
the other. With 256 dots that is **16,640** same-distance pairs; with 1,024 dots, **263,168**. On a flat sheet the proven ceiling
for 1,024 dots is about 20,000. This is textbook (the Lenz construction, 1950s), re-counted here.

**On a flat sheet, the old trick already does most of the work.** Keep a plain grid and choose the ruler length cleverly
(Erdős, 1946):

| dots | grid | wired to nearest only | best single distance | times more | partners of a middle dot | share of the proven ceiling |
|---|---|---|---|---|---|---|
| 1,024 | square | 1,984 pairs | 5,776 pairs | 2.9 | 16 | 29% |
| 1,024 | triangular | 2,945 | 7,432 | 2.5 | 24 | 37% |
| 1,000,000 | square | 1,998,000 | 25,992,416 | 13 | 96 | 13% |
| 1,000,000 | triangular | 2,996,001 | 32,919,176 | 11 | 96 | 17% |

For scale, an exponent of 0.014 multiplies by 1.10 at a thousand dots and 1.21 at a million. How the 2026 construction does at
sizes like these is not established (I have not read the paper, and its starting constant matters).

**A toy memory wired at one distance.** 2,304 cells; two cells are connected only if they sit exactly one chosen distance apart;
patterns are stored the simplest classic way (a Hopfield memory) and recalled from a copy with 10% of it wrong.

| wiring | partners per cell | patterns it holds |
|---|---|---|
| square grid, nearest | 4 | 2 |
| square grid, distance² 65 | 16 | 6 |
| square grid, distance² 325 | 24 | 8 |
| triangular grid, nearest | 6 | 2 |
| triangular grid, distance² 91 | 24 | 8 |
| random wiring (control) | 4 / 12 / 24 | 2 / 4 / 8 |

It holds about one pattern per three partners, and it does not care whether a grid or chance supplied the partners. With 20% of
the cells dead at half load, recall stayed at 0.986 or better in every row.

**What this says about his idea.**
1. The count of partners is what a memory like this lives on. The shape that supplies them is not.
2. Software memory is not stuck on a flat sheet. Any item can be linked to any other for free, and four dimensions already gives
   a quarter of all possible pairs. So in software the flat-sheet counting math has nothing to buy. The scarce thing is not how
   many relationships fit. It is **which ones are in view right now**.
3. That is his June idea. "Memory as arrangement" (May) says what is related; the Facing Field (June) says which relations are
   active from where you stand. I read them as two halves of one mechanism, and the second half is the one worth testing in
   software.
4. The counting math is the right question on a real flat sheet of parts that only talk at one distance. That is his 2025 seed
   (the crystal-and-liquid circuit whose wiring changes with frequency): there, picking the distance is picking the wiring, and
   the table above is the design chart. Whether such a part can be built is a specialist's call, as he wrote himself in May.
5. So the load-bearing wall moves. For anything buildable it is the 1946 trick, not the 2026 result.

**How far to trust this.** The exact counts were recomputed blind by GPT-6 Luna (its own code, never shown mine): all eight pair
counts and the four-dimension count matched to the digit. One side number differed (partners of a middle dot on the triangular
grid: Luna 16 and 32, mine 24 and 96). Cause found: Luna searched a box too small for that grid. Arithmetic settles it (91 = 7 x 13
gives 24; 53,599 = 7 x 13 x 19 x 31 gives 96). The toy memory has had one runner only and is a toy: a first pulse, not a result.

### c) The memory-first chip (12/22/2025 per ChatGPT: 500 tokens a second from an 8-billion model)
Measured on the MSI's RTX 4060 today: qwen3.5:9b writes **38.4 tokens a second**, qwen3.5:4b **55.4**. The 9b file is 6.6 GB, and
making one token means reading the whole model once: 38.4 x 6.6 GB is about 253 GB every second, which is close to what this
card's memory is rated to deliver (about 250 to 270 GB a second, from the part's published numbers as I remember them; not
measured here). So the card looks held back by memory speed, as his principle says, and 500 a second would take roughly 13
times faster memory. Checked today: Cerebras launched in August 2024 at about 1,800 tokens a second on an 8-billion model, and
says it got there by keeping the model in very fast memory on the chip; Groq was at about 750. **The instinct was right, and it
has been shipped.** Nothing to build here. The useful part is the rule of thumb: speed = memory speed ÷ model size.

---

## 2. Which principles hold up

**Proven inside his own systems**
- **Keep the record, swap the engine** (PMS, Atomic Chronicle, SYL-VX:0's interchangeable bodies). Sapling's core has been
  regrown and replaced several times (11.9M, 17.6M, 60.5M, now 98.6M parameters) and each swap is one row in the same memory
  chain; its README calls it "the same individual: memory.db and its hash chain were not touched". The crew changes models and
  the files carry on.
- **The brake lives in the ignition; never remove the stop** (Heartbeat Engine, 6/3/2026). Every later system kept it. One thing
  changed on the way, and I think for the better: Keava Owent (5/30) hard-coded that it may never choose to switch itself off;
  Sapling (10/14) says "it may stop itself; every stop is a report". "Earn my keep" stayed, the cage went, and the owner's
  controls were there in both.
- **Name roles, not products; one channel, one job.** Today: `route.py`, and the split between mailbox, files and phone buzz.
  "The AI that designs a system is not the AI that runs it" (AI Workforce) is how the crew works now.
- **Read the live condition, never the stored answer** (Live-Reference). Today gave two examples. The Supabase bill was caught
  by reading the mail, not by remembering it was paid. And the public copy of AI-Shared reports "5,015 files in" every night
  while nothing has been published since 10/21: his own phrase for that is a gesture shaped like the function.
- **Two blind witnesses before a number is trusted.** Used twice in this file, and the second time it caught a wrong number.

**Supported by outside work, not yet tested here** (named from my training; not re-checked today except the chip numbers)
- **A weak maker plus a strong checker beats a strong maker, wherever checking is cheap.** This is how Google's FunSearch (2023)
  and AlphaEvolve (2025) found new math with mid-size models. It is the mechanism by which a small model could do long science.
- **Fresh beats big on moving facts**, and **train on what resolved, not on what a model said** (models trained on model output
  degrade; grading by reality is the known cure).
- **A running simulation is the densest teacher**, because the label is free and true.
- **Structure grows; it is not placed** (his May tiers were already honest: structure solid, feeling unknown).

**Holds, but in a different place than he put it**
- **Memory as arrangement:** true as "index beats no index"; the packing math belongs to physical sheets (section 1b).
- **Orientation is the query** (from the timeline's description only): the principle is real in old hardware (holographic
  storage reads different pages out of one crystal by changing the angle of the light) and in today's models (attention uses
  the current state as the question). What it buys is selection, not capacity.

**Still open, and rightly left open by him**
- **The contribution unit** ("recorded, not scored"). The nearest thing that can be measured is the resolved record (section 3).
- **"Shielded systems go brittle"** (ECIH). Plausible, never run in his systems.

---

## 3. What could be combined now

1. **The Memory Steward.** The Heartbeat Engine named seven roles on 6/3/2026 and left one blank: "decides what the morning
   wakes up knowing... should not stay implied for long". It is still blank. Everything my look-around found this morning was
   that role's work: self-reports two months stale, the wrist-message log stopped on 11/01, open-list lines past their dates,
   25 questions from the funding lane that never reached him. Build it as a nightly job on a cheap model. The weekly Fable day
   is this role once a week; the nightly job is the other six days.
2. **The resolved record.** PAM's charter already says how a claim is written (confidence, a date by which it should show, what
   would prove it wrong). The news paper book, the trackers and the forecast system already produce claims that resolve. Put
   them in one append-only table of "what was called, by whom, what happened". Uses: sending jobs by measured hit rate instead
   of reputation, and later the training set for "own judgment". PAM stays paused; this borrows its form, not its engine.
3. **Interchangeable bodies are already real.** The watch ("Tell Claude") and the phone control rooms are shells around one
   memory. The apps coming with the Apple and Google accounts are the next body. Naming that is his call.
4. **Worlds as exam rooms.** The-current, Unfinished Island and The Cosmos all know the true answer and can grade a small model
   for free. (This morning's Cosmos build has the server check a player's count against its own clock: a weak maker and a strong
   checker, as a game.) **One caution:** the words in those worlds are often written by Claude. For Sapling, only numbers and
   outcomes may cross, never the prose.
5. **The Facing Field** needs its text before anyone designs with it. Two places it could go: the tesseract inside view as the
   face of the team's memory (his 11/4 "where you are picks the page"), and arm 3 of the experiment below. Anything about the
   creature goes in her own private log, not here.
6. **The keep ledger.** Keava's meter (energy and water per cycle), Sapling's per-tick watt-hours, the usage ledger and his
   10/27 money-map idea are one page waiting to be joined: what the system drew, in dollars and kilowatt-hours, beside what it
   produced (recorded, not scored). The bank account this week makes the dollar side real.

---

## 4. The one experiment: bare against built

His 6/29 PAM design asked for a bare local model against the same model wrapped in structure. Claude's timeline notes that
nothing we have measures long-horizon science, the thing Grok's post named. This is both, made exact.

**The job.** The card game SET has 81 cards. What is the largest pile with no valid set in it? 20. With bigger decks the proven
answers are 45 and 112; past that nobody knows, and the best piles found are 236 and 512 (checked today). The 512 was found in
2023 by Google's FunSearch, a mid-size model inside exactly this kind of loop; the best before it was 496. A pile is checked
exactly in under a second, so no answer can talk its way to a pass.

**Five arms, same number of tries, three repeat runs each**
0. **Rules only.** Plain search, no AI. If this wins, the model was decoration.
1. **Bare.** The local model writes a pile-building recipe, the checker grades it, nothing is remembered.
2. **Built, with a record.** Every graded try goes into an append-only record (Atomic Chronicle); each new try is shown the
   best so far.
3. **Built, with facing.** Same record, but what the model is shown is picked from where it stands: the tries most related to
   the one it is working on, not a top-ten list (memory as arrangement plus orientation as the query).
4. **A rented big brain, alone.** One frontier model, one try per run, no checker.

**What each outcome would mean**
- 2 beats 1: keeping what worked makes a small model better with no change to its weights. If they tie, his "accumulation"
  term is not doing work on this job.
- 3 against 2: the first scored test of arrangement and facing as the picker. If 3 is no better, it is decoration here.
- 2 or 3 at or above 4, for less money: structure stood in for size, on this job.
- 0 at or above all: pick a harder job.

**Cost and limits.** $0. About three hours of the 4060 in a quiet window, giving way to Sapling and the news render. About an
hour to build. No training, nothing touches Sapling or the creature, and no Claude-written text enters any training set. It
may turn out the 4b model is too weak to write a recipe at all; that is a result too (the floor for the maker), and the 9b gets
the same test. The harness takes other jobs: his same-distance puzzle is the second one, once its checker handles dots that are
off the grid. The record it leaves, tries by an open model graded by an exact checker, is the kind of data Fed Not Filled says
to train on later (Kimi's lane, Jaron's decision).

---

## 5. Things I noticed on the way

- **The public copy of AI-Shared has not been pushed since 10/21/2026.** The nightly export flags its own script (the file that
  lists the names to hide) and so never publishes. Nothing private got out. Before it is unstuck: today's timeline lines hold a
  family member's full legal name that is not on the hide list, and the company's tax number is not masked. Sent to Claude.
- **Keava Owent's README still says "keep that test green forever"** about never shutting itself off. His 10/14 decision for
  Sapling went the other way. One line in that repo would bring it up to date (his repo, his call).
- **The timeline's guess on the chip ("tens of tokens a second, roughly 10 times short") was right**: 38.4, about 13 times short.

## 6. After ChatGPT's reply (it landed 2:11 PM; read after sections 1 to 5 were committed)

Its handoff is saved beside this file (`chatgpt-phone-era-handoff-2026-11-23.md`).

**Where the two reads agree without having seen each other**
- **The same experiment.** ChatGPT's suggested next step: the same small model bare, then with verified retrieval, then with
  simulation feedback, plus a frontier baseline at matched cost, all written down before it runs. Mine: bare against built, with
  a frontier arm. Two differently built minds reached the same shape, which is his own test for when to trust an answer (9/16).
- **Memory geometry:** only ordinary relationship memory was ever tested; it needs a harness on the MSI with fair baselines and
  blind re-runs. Section 1 is a first one.
- **The chip:** measure the real 4060. Done today: 38.4 and 55.4 tokens a second.

**What ChatGPT's record adds or changes**
- **PAM's test was written and never run.** ChatGPT recovered the two messages of 6/29/2026 where he required it: a bare local
  model against the same model with structured context, real outputs recorded, and "if B does not win, diagnose". No result
  exists anywhere. So the experiment in section 4 would be its first run, five months late.
- **The Facing Field now has its own tests.** From the file in ChatGPT's library (6/28/2026): a shape qualifies if it
  (1) reconfigures with facing, (2) quiets what is not faced, (3) holds in simulation. It has a variable aperture, and it warns
  that "redirect is not training, deposit is not competence". That confirms the reading in section 1b (facing is selection:
  it "quiets the unfaced"), and it matches the toy result (the shape that supplied the partners did not matter: "the shape is
  replaceable"). It also gives the facing arm of the experiment a definition that is his, not mine.
- **The simulation console has an origin and a limit.** 9/30/2025, the day he saw a working ChatGPT built out of Minecraft
  redstone (5,087,280 parameters, about two hours per reply). The half that holds: let exact, cheap rules do the work rules can
  do, and let them do the grading. The half that does not: a computer simulated inside a game is always slower than the computer
  it runs on. His own numbers show it: Sapling today is 98.6M parameters, 19 times that redstone model, and it answers live on
  the laptop.
- **SYL-VX:0:** the name first appears on 3/23/2025 and was proposed by the assistant; he accepted it on 3/29. The principle
  (the person owns the memory, the body is a thin shell) does not depend on who named it.

**Where I would push on ChatGPT's test design**
- It needs a job with an exact checker and an arm with no AI at all. Without those, "the structured arm won" cannot be told
  apart from "the job was easy" or "the answer read well".
- "Structure" should be split into separate arms, so a win says which part did the work.

**The merged experiment (both reads), to be written down before any run**

| arm | what the local model gets |
|---|---|
| 0 | nothing: plain search, no AI |
| A | one try, no checker (ChatGPT's bare arm) |
| A+ | many tries; the checker keeps the best; nothing is fed back |
| B | it also sees the grade of its own last try and revises (ChatGPT's "simulation feedback") |
| C | it also sees the best checked earlier tries from an append-only record (ChatGPT's "verified retrieval") |
| D | the same record, but picked by the Facing Field's three tests, with the aperture as a dial |
| F | a frontier model alone, at matched cost |

Same job (the SET cards), same number of tries, three runs each. Seeds, budgets and scoring are fixed in a plan file first.
Logged: correct or not, time, watt-hours, card memory. A second AI re-runs the final table blind. About four hours of the 4060,
$0. It does not touch PAM's code or data (PAM stays paused); it runs the test PAM asked for.

**Still missing:** the Facing Field file itself, word for word, on the MSI. It is his document. It should live in his own repo
and not only in one app's library.

## Sources
Repos cloned and read today: persistent-memory-substrate, the three Atomic Chronicle repos, AETHERSPAN,
memory-as-spatial-arrangement (README, METHODOLOGY, RESULTS, both sims), emergence-structure-that-grows,
live-reference-principle, fed-not-filled, ECIH, Keava-Owent (README, memory and ledger modules), ai-heartbeat-engine,
ai-workforce, autonomous-agent-os, pam-continuum. On the MSI: `projects/seeds/`, `projects/tesseract/README.md`,
`projects/principles/`, Sapling's README. Web, today: OpenAI's 5/20/2026 post on the unit-distance result
(https://openai.com/index/model-disproves-discrete-geometry-conjecture/), OEIS A186705 (https://oeis.org/A186705), Cerebras'
launch notes (https://www.cerebras.ai/blog/introducing-cerebras-inference-ai-at-instant-speed), the FunSearch paper
(https://www.nature.com/articles/s41586-023-06924-6). Runs, all in `checks/` beside this file: `geo_check.py` (fixed seed; needs
only numpy; about 6 seconds) with its output, `tps.py` with its output, and GPT-6 Luna's blind recount (the prompt and its
report). Anyone can re-run them and should get the same numbers.
