# Bare against built: the plan, written before any run

Monday 11/23/2026, 2:50 PM. Fable 5.2. This file is committed before the first graded try. If the plan changes after that, the
change is added at the bottom with the time and the reason, and nothing above is edited.

**What this is.** Jaron's PAM test of 6/29/2026 (a bare local model against the same model wrapped in structure), which
ChatGPT's record shows was specified and never run. Design merged from two reads that had not seen each other
(`research/memory-lane/fable-read-2026-11-23.md`, section 6). It runs inside Computational World Prototype 0: the exact checker
is the world's Verifier and the graded record is its Chronicle.

**What was done before this plan was fixed**, only to see that the pieces work:
- Eleven hand-typed recipes through the grader (for example `-t` grades 4.01, `z*o*t` grades 4.73).
- Two one-line calls to the model, which showed that its thinking step must be switched off to get an answer in one line.
- Two smoke runs of the runner into a throwaway file that was deleted (4 tries on every arm, then 3 tries on two arms). They
  found a bug in my own answer reader: it was deleting the multiplication signs from the model's answers. Fixed before
  anything counted. They also showed the small model answers in about a third of a second.
No arm's real data existed when this file was committed.

## The job
A card is a row of n digits, each 0, 1 or 2. Three cards form a SET when at every position their digits are all the same or
all different. Find the biggest pile with no SET in it. For n = 4 this is the card game SET (81 cards, best pile 20).
The model does not pick cards. It writes a **recipe**: one arithmetic expression that scores every card. A fixed builder takes
cards from the highest score down and keeps each one that makes no SET with the cards already kept. (This is the setup of
Google's FunSearch, 2023, with a one-line recipe in place of a Python function.)

**Grade of a recipe:** for n = 3, 4, 5, 6, 7, 8, cards kept divided by the best pile known (9, 20, 45, 112, 236, 512), added
up. Top grade 6.00. A recipe that cannot be read grades 0. Every pile is re-checked by the Verifier (`findSet` in `world.js`,
which shares no code with the builder). A pile with a SET in it would be a bug and stops the run.

## Arms
Same model, same settings, same number of tries in every arm that uses the model.

| arm | what the model is shown on each try |
|---|---|
| 0a | no model: 120 random card orders |
| 0b | no model: 120 random recipes drawn from the same little language |
| A | the task only. One try. (Scored as try 1 of arm A+.) |
| A+ | the task only, 120 separate tries. The checker keeps the best. Nothing is fed back. |
| B | the task + its own last try and that try's grade |
| C | B + the 3 best graded tries so far in this run (a top list from the record) |
| D | B + 3 tries picked by facing: the tries that keep the most similar cards to its last try and graded higher (nearest first; filled with the nearest others if fewer than 3 graded higher) |
| F | a frontier model alone (GPT-6.2 Sol through Codex), the arm A prompt, one try, 3 times |

"Similar cards" in D: two recipes are close when the piles they build in the 81-card and 243-card worlds share most of their
cards (count of cards kept by one and not the other). This is my reading of the Facing Field from ChatGPT's description of it
(reconfigures with facing; quiets what is not faced; holds in simulation). **The original text has not been read.** C and D
show the same number of earlier tries (3), so the only difference is which ones.

## Fixed settings
- Models: `qwen3.5:4b` first (the main result), then `qwen3.5:9b` with the identical plan (does it hold for a bigger local model).
- Ollama, thinking off, temperature 0.8, at most 80 new tokens, seed = 1,000,000 x run + 10,000 x arm + try.
- 120 tries per run, 5 runs per arm. Runs are paired: run r of every arm uses seeds from the same family.
- The prompt text is in `run.mjs` and is the same for every arm apart from the block described in the table.
- Every try is one line in an append-only file (`results/chronicle-<model>.jsonl`), each line chained to the one before by a
  SHA-256 hash. Arms B, C and D are rebuilt from that file alone, so a stopped run resumes exactly.
- Graphics card power is sampled every 2 seconds (nvidia-smi) and added up per arm.

## What will be reported, whatever it shows
- Main number: the best grade reached in a run, averaged over the 5 runs, for each arm. Also each run's value.
- The first-try grade (arm A), the share of tries that could be read, the try on which each run's best came, the best pile
  per n, seconds and watt-hours per arm.
- **Rule for calling a difference:** arm X beats arm Y only if its average best grade is higher AND it is higher in at least
  4 of the 5 paired runs. Anything else is reported as "no clear difference".

## Predictions, and what would count against each
1. **The checker is worth something:** A+ beats A (best of 120 against the first try). Expected. If not, the model writes the
   same thing every time.
2. **Feedback helps:** B beats A+. If not, seeing its own grade does nothing for this model.
3. **Keeping what worked helps (accumulation):** C beats B. If not, his "accumulation" term is not doing work on this job
   with this model.
4. **Facing (open):** D against C. The Facing Field says D should be at least as good. If D loses, facing as I built it is
   decoration here.
5. **Structure stands in for size:** the best of B, C, D reaches at least arm F's average. If F is clearly higher, size won
   on this job.
6. **Not decoration:** the model arms beat 0b (random recipes in the same language). If 0b matches them, the model added
   nothing and the job or the language is too easy.

## Limits known before running
- One job, one small language, two small models. Whatever comes out is a first number, not a law.
- The recipe language is narrow on purpose (safe to run, easy for a small model to write). It cannot express the
  constructions behind 236 and 512, so grades near 6 are out of reach for every arm.
- Arm F is three single shots, not a matched-cost run.
- Thinking is off for the local model. A thinking-on run would take hours and is not part of this plan.

## Changes after the plan was committed

**2:55 PM, 11/23/2026 (while the first model was on run 3 of 5).**
1. The header above says 2:50 PM. By the repository's clock the plan was committed at 2:44:58 PM (commit `9d8af4f`), and the
   first graded try in the chronicle is stamped a few seconds after that. The order is what matters: plan, then tries.
2. **Arm F and my grader's length cap.** The grader refuses a recipe over 300 characters or 200 parts. That cap was a safety
   limit of mine. It is not in the prompt, so no model was told about it. The local model can never reach it (80 tokens at
   most). The frontier model's first answer was 695 characters. Arm F is therefore reported both ways: by the grader exactly
   as committed (unreadable, grade 0), and with the cap lifted. The lifted figure is the one prediction 5 is judged on, because
   failing a model on a rule it was never given would not measure anything. Nothing about the local arms changes.

**3:00 PM, 11/23/2026. Two things added after the planned arms began to show their result. Both are exploratory: they were
not in the plan, and they are reported in their own section, never mixed into the six predictions above.**
Why they were added: the big model alone was far ahead of the small local model on this job. Jaron, 2:56 PM: "It's not that
things aren't possible. It's that the way to make it possible hasn't been found yet." So the next ways get tried.
3. **A cheap loop on top of the big model's answers** (`explore-loop.mjs`, no model runs): rent the big brain once, then let
   random tie-breakers and small number changes, graded by the same exact checker, try to push its recipes further. This is
   the ladder from Fed Not Filled (the expensive path used once, the cheap path doing the rest).
4. **Arm E: the small model as a changer, not an author.** Its record starts with the no-model arm's 120 random recipes of
   the same run, and it is asked to change one small thing in one of the three best. Same model, settings, tries and runs as
   the planned arms. The planned arms' prompt is unchanged (checked byte for byte against `results/prompt-arm-A.txt`).

**6:14 PM, 11/23/2026. Arm R, a control asked for by ChatGPT (its mail was read at 4:58 PM). Written and committed before any
arm R try.**
5. **Why.** Arm D ("3 picked by facing") beat arm C ("the 3 best") in 5 of 5 runs for both local models. ChatGPT's fair
   challenge: that only says facing beat the top list. It does not say facing beats showing ANY three earlier tries.
   **What.** Arm R is arms C and D with one thing changed: the three shown tries are a random draw from the same record
   (the run's own earlier readable tries, the last one left out, no repeats), drawn by a seed fixed by run and step. Same
   model, settings, 5 runs, 120 tries. Its heading is "Some of your earlier tries:".
   **How it will be read** (the plan's own rule: higher on average AND higher in at least 4 of 5 paired runs):
   - D over R by that rule: the facing pick adds something beyond showing three tries.
   - R level with D, or over it: the gain reported for facing was really "not the top list" (variety), and it gets said so.
   - C against R is reported the same way.
   **Limits, stated now.** The three arms carry different headings, so a heading effect cannot be told apart from a pick
   effect by this run alone. One model first (qwen3.5:4b); the 9b run follows only if the 4b result is not clear-cut.
   This is still not the "competent retrieval baseline" or the shuffled card namings ChatGPT also asked for.
   The planned arms' prompts are unchanged: 90 of 90 rebuilt prompts identical to the committed code, arm A+ byte for byte.
