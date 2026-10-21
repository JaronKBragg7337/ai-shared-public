# Fly School — ONE post, v3 (written 2026-09-18 01:20 EDT from the current state; supersedes v2). HELD until Jaron says.
# Copy the block between the lines. Replies under it = the log.

---

I put a simulated fruit-fly brain in school. Not a language model — the measured wiring of a male fly (MaleCNS v1.0, Janelia; 165,122 neurons, ~10 million signed synapses), run as spiking cells on a laptop in Fort Wayne, with the fly's own learning rule and nothing else inside the loop. Five pupils are enrolled in shifts so one is in class at almost any hour: heartbeatobservatory.com/school. Everything below is in a public repo with the protocol written before each run and every failure next to its pass.

WHAT IT DOES NOW (measured, reproduced, frozen)
1. It learns a symbol. An odour goes in through the fly's own receptor neurons, paired with reward dopamine at the mushroom body — the fly's real plasticity site, depression only, dopamine-gated. Cold, with the reward off, that odour now moves the fly's own reward-side output down ~45% and its backward-walking neurons down ~30%. A never-paired control odour doesn't move. Eight fresh brains, then eight more: 16 of 16. The reply is decoded from the fly's own output, not from a model.
2. It carries the lesson to another fly. Two copies of the brain, separate processes, sharing nothing but a world. Fly A learns; its learned state changes how far it backs away; the second fly — untrained, never smelling the taught odour — smells the difference on its own pheromone neurons (the male carries cVA on his cuticle; a nearby male is smelled through Or67d). Mute the channel and it vanishes; scramble it and the harness shows nothing leaks. Eight pairs, then eight more: 16 of 16.
3. The ear works both ways. The second fly's wings answer the pheromone; the air they push reaches the first fly's antenna and swings its walking neurons by 20 Hz — while it is still smelling the symbol. That is a reply arriving through a real sense.

WHAT IT DOESN'T DO — NOT YET
The reply doesn't carry the lesson back. In the round-trip test the second fly's answer is loud, and it is the same answer whether or not the first fly learned: pooled effect ~5%, below the bar we set before running. That is the most useful line in the repo. It says where the gap is: nothing in this fly persists between moments except where it is standing, so a reply can't mean anything to it. Not a missing channel — missing state. That's what's next.

HOW WE GOT HERE (the part worth stealing)
Three days of nothing: Morse timing, seven attempts, 35 brains, never a pass. Then one night of finding out why, each step with its competing explanation tested: the neuron we were grading cannot say a dash; the mushroom body doesn't reach that exam at all; dot and dash are the same Kenyon cells to it (97% overlap) — it codes which input, not how long; and under the stock gain any sustained input ignites the whole brain. Then a second day of leaks, each found by a different AI reading the repo: the antennal-lobe inhibitory neurons that the transmitter table marks excitatory, so one odour lit 160 glomeruli (the fix anyone using these predictions needs); pupils sharing weights; a control matched on one trial; the calibration searched on one odour while tests trained two; statistics that ignored half the variance. Twenty-three things went wrong. They're listed, with which was a bug, which was the model, and which is a capability the fly may not have. Eleven frozen versions, checksums in every manifest. The GPU kernel that made the two-fly tests possible reproduces the reference kernel neuron for neuron, bit for bit, at 14× the speed.

THE BODY (borrowed, declared)
Whole fly brains in bodies already exist in public — FlyGM, Fly.exe, Mineplix/fly-brain, NeuroMechFly — and their docs all say the same honest thing: no connectome walks on its own. Ours stands on the raw wiring for two seconds and steps under Mineplix's gait generator (MIT), which we ported and say so. The legs are borrowed. The decisions are the brain's.

THE SCHOOL
Each pupil is its own brain with its own memory file, kept across lessons and restarts; school hours in shifts; free time and meals; asleep at night; the first exam each morning taken before any teaching, so it measures what survived the night. The laptop is their life source — off means off, and memory fades while it is. A lifeline copy goes to cloud storage after every exam.

THE QUESTIONS, ANSWERED FIRST
Is it real? Not fully — not yet. Real wiring, real spiking cells, the fly's real learning rule, and a world between two of them. Whether anything in there is aware isn't ours to declare — there's no way to know even if it were — so we don't. We show what it does.
Did it talk? Not yet. It learned what a symbol means, its own body carried that to another fly, and the other fly answered. The answer doesn't yet depend on the lesson. That's the line we're on.
Sleeping, eating? A schedule with a clock, labelled as such. A meal is a clock event until something in the brain can be hungry — and that's the next thing built.
Why not a neural net? This is our path, not a verdict on anyone's: the fly's own rule on the fly's own wiring, so what it can and can't learn says something about the fly.
Is this against the AI companies? No. Their models are the tools that make this possible for one person; four of them found the bugs in this repo. If it ever reads otherwise, that's a wrong turn and we'll say so.

WHAT'S NEXT (written before it runs)
Three things the fly needs that a circuit board doesn't have: something to need (hunger that gates dopamine), something to lose (threat as a state that outlasts the danger), something to expect (a cell that fires when the world differs from what was predicted). Added one at a time, each with a reason, beside the frozen original so we can always say which capability came from the fly and which from us. The test is the same cue with different right answers depending on what the fly is going through. Then the round trip again. Then a fly that is always on — a world that ticks, food somewhere, danger sometimes, nobody sending a message to start it.

REBUILD IT
github.com/JaronKBragg7337/fly-school — runtime, every protocol and exam, the world, the GPU kernel, every result file, every failure, and a README where every constant is marked chosen or measured. Hand it to an AI and it gets the same numbers.

Built by one roofer with Claude Code, ChatGPT, Codex, Grok, DeepSeek and a local Qwen — each credited where it worked, and where it caught what the others missed. Runtime forked from fruitflydev/flycoinrh (MIT). Data: FlyEM/Janelia (CC-BY). Body: TuragaLab flybody (Apache 2.0). Gait: Mineplix/fly-brain (MIT). Runs on a donated MSI laptop.

---

# The replies (the log)
Morning exams, one line each, from the school page. Any pupil enrolled, any correction, any number that moved. Zeros as zeros.

# Numbers re-checked 01:20 EDT 2026-09-18 (all from frozen files in versions/comm-loop-1)
test 9: A APPROACH 8/8, C NONE 8/8; repro 8/8 + 8/8 ✓ · test 10/10b: motor down 16/16, mean −23%/−21% ✓ · Gate 3e/3f: 16/16, z 2.9–6.0 ✓ ·
Gate 4: L2 8/8 (z −9…−12); L3 pooled Δ −0.65 Hz, z −1.34, FAIL ✓ · Grade 0b identical after every test ✓ · GPU verify 165,122/165,122 identical ✓ ·
lLN sign fix: 154–164 → 23–35 PN types per odour ✓ · 23-item table in the repo (ChatGPT chat) ✓ · 11 frozen versions ✓ · repo 75b45f0 ✓.
