# Fly versions — freeze + fork (Jaron, 2026-09-16: "treat upgrades like AI companies do with new models")

A **version** is a named, frozen copy of everything that decides how the fly learns and acts. It is copied once and never
edited. A **run** (new seeds, a constant, a gap) is not a version. A change to *how learning works* — a new trace, a new
learning rule, a new readout, a new sensory filter, a teacher — **is** a version, forked from a named one.

Rules:
1. Never upgrade a version in place. Fork it: `versions/fly-v1` → `versions/fly-v1-frame` (or `fly-v2`), with a one-line
   *what changed* and *why* in this file.
2. The school's exams do not change with the fly. Every version takes the same tests. That is what makes A vs B a
   measurement instead of "the latest fly seems better."
3. Every report-card row in `research/FLY-BRAIN.md` names the version that took it.
4. The baseline keeps running as a control for as long as its fork exists. "Don't delete it — build the opposite and
   watch both" (working-with-jaron.md) is the same rule.
5. A version's manifest lists the files and their SHA-256 so "what exactly was this fly" is answerable in six months.

| Version | Forked from | Frozen | What it is | What changed | Why |
|---|---|---|---|---|---|
| **fly-v3** | fly-v1 | 2026-09-17 03:20 | graph_v3_s0.35.npz: connections <6 synapses dropped, sensory cells shielded from central input, weights × 0.35; refractory 3.8 ms (flysim_v3.py). | lulzx's recipe at graph level | Grade 0b 8 pass / 2 fail (v2 7/3): sugar→MN9 36 Hz, bitter veto, JO-A→GF alive. Fly-Lab/versions/fly-v3/MANIFEST.md. |
| **fly-v2** | fly-v1 | 2026-09-17 02:20 | `graph_v2.npz` = graph.npz with every weight × 0.35; nothing else changed. | Global gain | Under v1 any sustained input ignites the whole brain (25–35 Hz/cell, 65–78% KCs) — root cause of rows 1–12, the memory saturation, and the body seizing. Sweep on 3 seeds: 0.35 gives 2–2.9 Hz/cell, KC 7–11%, DNs alive. Body stands on it. Pupil school-5 on it. Fly-Lab/versions/fly-v2/MANIFEST.md. |
| **fly-v1-axon** | fly-v1 | 2026-09-17 00:50 | v1 + `graph_axon.npz` (per-edge `axonal` flag: 21,266 DN-input edges whose synapses land in VNC ROIs, from MaleCNS syn-partners; DNa01 has 28+34 axonal input edges of ~315 each) + `flysim_axon.py` (axonal edges set an output GATE on the target instead of adding to voltage; gate = clip(1 + 0.05·mV, 0, 3), τ 5 ms — CHOSEN). Flags-off equivalence to v1: spike-identical (verified). | Two synapse classes | Ceballos et al. 2026: axo-axonic inputs veto/amplify DN spikes; v1 flattened them into the soma. Exam 01:45 was INVALID — the Morse script's inline kernel never used the gate (identical-to-v1 was the tell). Wired in 02:05; attempt 6 (v1 vs axon, both with 5 Hz leg drive) running. Files: Fly-Lab/versions/fly-v1-axon/, Fly-Lab/dn_axon_inputs.py, results/dn_axon_summary.json. |
| **fly-v1** | — | 2026-09-16 23:30 | MaleCNS v1.0 LIF runtime; mushroom.py (KC→MBON depression, per-call trace ×0.55, cutoff 0.05, 6 h forgetting); fly.py (Nose, press/let-go bars that move with P&L, replay-at-reward); watcher.py (set/end outcomes); morse_grade1.py (School Grade 1 protocol). Learned store `mb_gains.v2.npz`, cap `cap.dry.json`. | — | Baseline. Took Grade 1 attempts 1–4 (rows 1–4). Known: DNa01 output biased short-then-long; trace forgets before reward (harness replays). |

**The classroom is not a version.** `Fly-Lab-2/school/school.py` (2026-09-17) runs one fly, `school-1`, on **fly-v1** with the
Grade 1 protocol unchanged, 24/7, with a persistent store. It is the school (rule 2), and school-1 is the first fly that has
been to school more than once. When a fork is ready it takes the same lessons as a second pupil (`school-2` on `fly-v1-…`),
and the page shows both. The trader (fly-1) is paused, not cancelled, while this runs.

Planned forks (not yet made):
- ~~`fly-v2`~~ — made (row above). Was: **the gain regime.** Global synaptic scale (and/or inhibition) set so sustained input does not ignite the whole
  brain: KC 5–15% active, dot ≠ dash to the mushroom body, DNs still answering (Fly-Lab-2/gain_sweep.py, 2026-09-17).
  Every exam re-run on it as a new pupil. Root cause of rows 1–12 (FLY-BRAIN.md "The night's chain").
- `fly-v1-body` — **v0 exists** (Fly-Lab/body/body_loop.py, flybody + MuJoCo 3.13, 328 leg MNs → actuators by muscle,
  3,915 leg sensory ← touch/joint speed). Measured: stands still with no input; seizes with any. Needs fly-v2 first.
- `school-v1-lr` — same as fly-v1 but lr 0.06 → smaller / floor 0.25 → higher, or dopamine only on *change*. Answers: is the
  first-hour saturation (42.5k/44k synapses depressed after 5 lessons) the rule or the brain? Control: school-1 keeps running.
- `fly-v1-body` — flybody (MuJoCo, Apache 2.0) closed loop: joint angles/contacts → leg sensory neurons → brain → DN pool → motors. Gives DNa01 real input; makes the axon gate meaningful; the page shows the body the numbers drive. First fork needing GPU/MuJoCo. Codex, Saturday.
- `fly-v1-frame` — second slow eligibility trace opened/closed by taught prefix/suffix pulses (the abracadabra triangle). Answers: does the fly remember why it is rewarded without harness replay?
- `fly-v1-readout` — a DNa01 readout / output population that can physically produce long-then-short. Answers: is `-.` producible at all?
- `fly-v1-seq` — an added, explicitly chosen sequence-learning rule (cerebellum-inspired). Answers: what does an imported rule unlock that the measured fly lacks? (ChatGPT 9/16: keep v1 running as the control.)

## Manifest — fly-v1 (SHA-256, first 16 hex)
```
2abf791d36fa957c  calibration.py
7f42fdd6abea22a8  cap.dry.json
04714990ede10fd4  fly.py
f977e29b16135bd6  flysim.py
d1d466a9dee84310  mb_gains.v2.npz
5716c730fa0ef144  morse_grade1.py
d3147ae6188a77b4  mushroom.py
6a499bea798e8ba3  watcher.py
```
