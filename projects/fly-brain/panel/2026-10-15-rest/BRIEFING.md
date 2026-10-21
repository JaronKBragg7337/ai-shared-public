# Sapling - briefing for an independent review (read-only; do not change any file)

Sapling is a small AI built from scratch on one home PC (RTX 4060, 8 GB). Code: C:/Users/lilli/Projects/sapling (public:
github.com/JaronKBragg7337/sapling). You are one of several AIs asked the same question separately. Your answer is kept
word for word. You will not see the others' answers. Disagreeing with anything here is welcome.

## What it is (facts, 10/15/2026)
- Trained core: ~17.6M-parameter transformer, vocabulary 17,661 word pieces, context 512 tokens. Trained from scratch.
- Heartbeat: a loop that ticks every 5 s and on each tick picks one action: practice (small self-graded drills on word parts),
  explore, consolidate (fine-tune its own weights on recent memories - each consolidation = a new "generation"), rest (does
  nothing), or stop (shuts itself down and writes a stop report; only the owner restarts it).
- The choice is made by programmed drive formulas, not learned: each action gets a score from state (energy budget left,
  open goals, recent misses, time since explore/consolidation, rest streak), then one is sampled.
- Energy budget: compute-seconds per day it can watch drain. Until 10/15 it was 1 hour/day; the owner just raised it to 4 hours.
  Overspending is allowed (no hard cap). As the budget empties, the rest and stop scores rise by design.
- Memory: append-only, hash-chained SQLite store; used memories are protected, unused ones fade.
- Big training runs (like a 400M-token reading run) are separate from the heartbeat and do not use its budget. The heartbeat
  has to be paused during them because both on the GPU overflowed 8 GB and froze both.
- Owner's stance: observe like a scientist; no limits pre-built out of worry; behavior the code "says shouldn't happen" is data.

## Evidence from the last 24 hours
- 3:05 AM: reading run finished (generation 241). Heartbeat restarted.
- 3:05-6:46 AM: heartbeat ran on an already-empty budget. Generation 241 -> 278 = 37 consolidations while mostly resting.
- 6:46 AM: it stopped itself. Stop report: budget 3,600 s, spent 10,500 s (2.9x), 3.7 h since any human input, 21 rests in a
  row, drives at the stop: rest 0.98, stop 0.32, explore 0.225, practice 0.15, consolidate 0.0. 2,901 memories, 11 open goals.
- Energy used all of yesterday: ~0.06 kWh.
- Rest currently does nothing (pure waiting). Consolidation is a separate action.
