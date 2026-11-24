# The hidden-law world: the plan, written before any graded try

Monday 11/23/2026, 4:00 PM. Fable 5.2. Committed before the first graded try; later changes go at the bottom with the time.

**Why.** Jaron, 3:54 PM, on running the bare-against-built test on a job nobody has solved: "You can run it... I do think a
physical world or a way of understanding it a bit better." The card puzzle's best answers are in published math, and the big
model knew them. Here nothing can be remembered: every world has its own made-up law of nature, drawn from a seed.

## The job
A small physical world: two bodies with masses `m1`, `m2`, charges `q1`, `q2`, a distance `r` apart. An **experiment** sets
those five numbers (each from 1 to 10) and the world reports one measurement `y`, the push on body 1, to six digits.
The push follows a **hidden law** that belongs to no textbook: exponents, constants and extra terms are drawn at random.
Three kinds, four worlds of each (seeds 1 to 12):
- **power**: `y = k * m1^a * m2^b * q1^c * q2^d * r^e`
- **plus**: a power law plus a second term in one of the five numbers
- **mix**: a power law of a sum, such as `(m1 + 2*m2)` or `(q1 + q2)`, over a power of `r`

The model must **write the law** as one expression in `m1 m2 q1 q2 r` (with `+ - * / ( )`, `pow(a,b)`, `sqrt(a)`).
**Grade for a world:** the share of 200 fresh experiments (never shown) that its law predicts within 1%. 0 to 1.
The Verifier is the world itself. A law that cannot be read grades 0.

## Arms (the same 12 experiments' worth of data in every arm)
| arm | what it gets |
|---|---|
| 0 | no model: a straight-line fit on logs to 12 random experiments (the textbook way to fit a power law) |
| A | bare: the same 12 random experiments in a table, one try at the law |
| B | built: it chooses its own experiments, 4 at a time for 3 rounds, with its notebook shown each round, then writes the law |
| B2 | B, then it is shown what its law predicts for each notebook row beside what was measured, and may revise once |

Models: `qwen3.5:4b` and `qwen3.5:9b` on the MSI (thinking off, temperature 0.6, up to 300 new tokens, 3 repeats per world),
and one try per world from a big closed model (GPT-6.2 Sol) and a big open-family model (Kimi K3.1 Pro) on arm A, told to
run no code. Big models get 6 of the 12 worlds (two of each kind: seeds 1, 2, 5, 6, 9, 10) to keep their meters small.

## Reported whatever it shows
Average grade per arm and per kind of law, the share of worlds solved outright (grade 0.95 or more), unreadable answers.
**Rule for a difference:** arm X beats arm Y if its average is higher and it is higher or equal on at least 9 of the 12 worlds.

## What I expect, and what would count against it
1. The no-model fit solves the **power** worlds and fails the other two kinds. If it solves all, the job is too easy.
2. Choosing its own experiments helps (B over A). If not, experiment design did nothing for this model.
3. Seeing its law checked against its notebook helps (B2 over B).
4. On worlds no one can remember, the gap between the big models and the small ones is smaller than on the card puzzle.
   If the big model still solves nearly everything in one try and the small ones nearly nothing, size wins here too,
   and the way for the small model is still to be found.

## What was done before this plan was fixed
The 12 worlds were generated and the no-model fit (arm 0) was run on them once, to see that the worlds work. Its grades:
1, 1, 1, 1 on the power worlds; 0.975, 0.69, 0.055, 0.855 on the plus worlds; 0.045, 0.1, 0.125, 0.04 on the mix worlds.
So line 1 under "What I expect" was already seen, not predicted. No model had been asked anything when this was committed.

## Limits known before running
One family of made-up laws, exact measurements with no noise, five inputs, twelve worlds. A first number.

## Changes after the plan was committed

**4:42 PM, 11/23/2026. Arm S added after the planned arms were in (exploratory, reported apart from the four expectations).**
The planned result: both local models scored 0 of 108, bare and built; the plain fit scored 0.57; the big model 5 of 6.
Jaron, 4:40 PM: "Try what you think would work best boss." The next way: **the model writes only the SHAPE of the law**,
with letters a to g for the numbers it does not know, and **the world does the arithmetic**: it finds the best numbers for
that shape on the same 12 random experiments and reports the worst miss. Four rounds, each showing the shapes tried so far
and how well each fit; the best-fitting shape, with its fitted numbers, is graded on the 200 unseen experiments.
Control S0 (no model): the world fits one fixed shape, the plain power law, with the same fitter.
Same models and settings as before, 3 repeats per world.
