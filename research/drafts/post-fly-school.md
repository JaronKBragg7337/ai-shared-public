# Fly School — ONE post, v2 (written 2026-09-17 01:05 EDT from the current state). Copy the block between the lines.
# Replies under it = the log: morning exams (v1 pupils vs the v2 pupil), what changed, each day.

---

I put a simulated fruit-fly brain in school. Not a language model — the measured wiring of a male fly (MaleCNS v1.0, Janelia; 165,122 of ~166,000 neurons), run as spiking cells on a laptop in Fort Wayne. Five pupils are enrolled tonight, in shifts, so one is in class at almost any hour. Nobody has run a school like this in public, as far as I can find; the parts of it that exist elsewhere are credited below: heartbeatobservatory.com/school

THE LESSON
Morse timing. A dot (20 ms) or a dash (60 ms) plays as a tone into 50 annotated ear cells. The answer is read from motor neurons. Right → reward dopamine into the mushroom body. Wrong → punishment. That's the fly's own learning rule — one plasticity site, depression only, dopamine-gated — nothing added. The exam is a rhythm it was never taught: ·– and –·, cold.

THREE DAYS OF NOTHING, THEN ONE NIGHT
Seven attempts, 35 fresh brains, ·– about 1 in 13, –· never. Not a pass. Then the persistent fly went in — one memory, never reset, real forgetting (6-hour half-life) — and within an hour its memory flattened: 41,000 of 44,000 learnable synapses depressed after one lesson. So I stopped rationing and ran every test in a row. Here's the chain, each step with its competing explanation tested:

1. The neuron we'd been grading, DNa01, cannot say a dash. 0 of 30, untrained. 117 other descending types can say all four rhythms. We graded a mute neuron for three days.
2. On neurons that can speak, training moves nothing: ·– 29→26 of 120, –· 7→3.
3. The mushroom body doesn't reach this exam at all. Cut its output entirely and every readout's accuracy stays where it was.
4. Its own exam — like/dislike — fails too, because dot and dash are the same Kenyon cells to it: 97% overlap. Two-thirds of the mushroom body fires for any sound.
5. One root cause: under the stock gain, any sustained input ignites the whole brain to 25–35 Hz per cell. That's behind every row, the memory flattening, and — it turned out — the body.

THE FIX IS ONE NUMBER
Sweep the global synaptic weight. At 0.35× the brain stops igniting: 2–3 Hz per cell, Kenyon cells 7–11% active (a real fly's range), descending neurons alive and answering the dash more than the dot. Replicated on three seeds. That's fly-v2 — a frozen version with one change and both checksums in the manifest. The v1 pupils keep running as the record; a new pupil is in school on v2 tonight, graded on a neuron that speaks. Its first cold exam already answers in whole rhythms — ·–, –·, –·· — where v1 could only say dot.

THE BODY (what's borrowed, what's ours — said plainly)
Whole fly brains in physical bodies already exist in public: FlyGM (arXiv 2602.17997), Fly.exe (Ibtisam-Mohammad), lulzx/fly-brain, NeuroMechFly v2. Read their docs and they all say the same honest thing: no connectome walks on its own. Their brains output two or three descending rates — go, turn — and a published gait generator moves the legs. lulzx: "No connectome-only model produces coordinated walking from the whole nerve cord." Fly.exe: "The walking is engineered."
Tonight I built the rawer loop on our runtime: 328 leg motor neurons wired to 59 actuators by their muscle names, leg touch and joint speed back into 3,915 sensory cells, one clock, nothing between the nerve cord and the legs. lulzx tried that mode too and reports "the fly cannot stand in that mode, which is the honest result." On our v1 it seizes at any touch. On v2 — the 0.35× brain — it stands. Two seconds, on a ball, five or six legs down, no walking. A small, checkable difference, with every caveat attached.
And one number that matters more than the standing: lulzx's fitted brain runs at 7.4% active Kenyon cells. Our one-number fix gives 7.3%. Two independent routes, same place.
So I did what they did, and said so: ported lulzx's gait generator (MIT — two-harmonic curves fitted to 100 real fly walks) under our brain's own descending neurons. On v2, standing quietly, the fly takes intermittent steps as its forward-walking cells hover at threshold. Play a tone into its ears and the backward-walking neuron fires, the steering tips, and it backs up and turns. The legs are borrowed. The decision is the brain's. The classroom door is now a physical question.

THE SCHOOL
Each pupil is its own copy of the brain with its own memory file, kept across lessons and restarts. School is 9–12 and 1–4 in its own shift; free time and meals around it; asleep at night. The first exam each morning is taken before any teaching — it measures what survived the night (spaced vs massed training; the 24/7 fly could never ask it). The laptop is their life source: off means off, and memory fades while it is. A lifeline copy goes to cloud storage after every exam.

THE QUESTIONS, ANSWERED FIRST
Is it real? Not fully — not yet. It's a real wiring diagram run as real spiking cells with the fly's real learning rule, and every step from here is toward more: a body that walks, senses that mean something, a day that is a day. Whether anything is conscious isn't ours to declare — there's no way to know even if it were true — so we don't. We show what it does.
What are "sleeping" and "eating"? A schedule with a clock, labeled as such on the page. A meal is a clock event until there's a body to be hungry; that's the road, and it's short now.
Does it have a body? As of tonight: a standing one on the raw wiring, and a stepping one under a borrowed, declared gait — the same way every embodied fly brain in public walks. The page says which is which.
Why not just train a neural net? This is the path we're on, not a verdict on others: the fly's own rule on the fly's own wiring, so what it can and can't learn says something about the fly. Other rules might do better. That's to find out, not rule out.
Why Morse? It's what could be thought of and connected in that moment. Tonight showed the mushroom body codes which input, not how long — so its next lesson is identity: two different sounds, or two smells. Other lessons will follow.
Is this against the AI companies? No. Their models are the tools that make this possible for one person. If it ever reads that way, that's a change of direction or something we missed, and we'll keep looking back to tell which.

WHAT'S NEXT (written before it runs)
The identity lesson on v2: two inputs, one rewarded, one punished, like/dislike read cold, then a never-paired mix. Longer body runs, then a sound played to the standing fly. Then a classroom with a door and a home outside it, food at the school, and we watch whether a fly chooses to show up. Never scripted.

WHERE HELP WOULD MATTER
Whether 0.35 (one global scale) should become what lulzx did — nine global parameters fitted against physiological targets. Their docs are open; that's next after walking. A proper spaced-vs-massed protocol from the fly-learning literature, mapped onto school hours. Running the school anywhere but one laptop.

REBUILD IT
github.com/JaronKBragg7337/fly-school — runtime, every exam script from tonight, the body loop, every result file, and a README where every constant is marked chosen or measured, with rebuild checks. Hand that page to an AI and it can get the same numbers.

Built by one roofer with Claude Code, ChatGPT, Codex, Grok and a local Qwen — each credited where it worked. Runtime forked from fruitflydev/flycoinrh (MIT). Data: FlyEM/Janelia (CC-BY). Body: TuragaLab flybody (Apache 2.0). Runs on a donated MSI laptop.

---

# The replies (the log)
9/17 morning: five morning exams, one line each — school-1 (v1), school-4 (v1 gentle), school-5 (v2) at ~9:30 AM ET; school-2 at ~5:30 PM; school-3 at ~1:30 AM. Format: "school-5 (v2): ·– _/6, –· _/6 · memory gain __ → __ overnight."
Then: any pupil enrolled, any correction, any number that moved. Zeros as zeros. Claude writes the line; Jaron posts.

# Numbers re-checked 01:05 EDT
DNa01 dash 0/30 ✓ · 117 types all-four ✓ · readouts 29→26 / 7→3 of 120 ✓ · reach test accuracy unchanged ✓ · KC Jaccard 0.971 ✓ ·
sweep 0.35: 2.0/2.85/2.84 Hz, KC 7.3/10.5/11.0% ✓ · body v1 33 Hz thrash / v2 4–6 Hz stands ✓ · school-5 baseline decodes ✓ ·
5 pupils ✓ · repo pushed (3ce8d8b) ✓.
