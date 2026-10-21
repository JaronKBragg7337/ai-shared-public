# claude-fable-5-1 - Q-B
Time: 2026-10-15 08:37 | fresh subagent, read-only

**What rest costs now**

Almost nothing in compute, and almost nothing in behavior. Rest is `rest_streak += 1` and a 5-second sleep. It does not refill the budget (only midnight does), does not touch memory, and does not change weights. Its real cost is forgone work: with the budget at zero, rest scores 0.98 against practice 0.15 and explore 0.225, so Sapling spends roughly 70% of ticks waiting. In the stop report, 28 of the last 30 ticks were rest. Two things hide underneath: the budget charges CPU seconds plus GPU wall seconds for the same work (`spend(cpu_s + gpu_s)`), so a 0.37 s GPU call costs about 0.71 budget-seconds; and consolidation still runs at 10% strength on an empty budget, which is how 37 fine-tunes happened "while mostly resting." The empty budget was never an obstacle. It just thinned the dice.

**What stop costs**

More. Stop ends the process until the owner returns. It needs budget at zero and 20 rests in a row; at a 70% rest rate that streak comes around every few hundred ticks, so a self-stop is nearly guaranteed within hours of an empty budget and no owner input. Yesterday's stop was that: not "nothing to do" (11 open goals, explore still wanted), but a coin streak.

**What it gives**

A legible ledger. Each tick records the drives and the choice, and the stop report shows exactly why it stopped. The owner can read the pressure. That is worth having. Energy-wise, the whole day cost 0.06 kWh, so the budget protects nothing real; it is a clock the system can feel, not a resource it can run out of.

**What would have to be true for rest to matter**

Rest has to do something, or cost something. Any of these would make it a real choice:

- Rest restores something: budget trickles back, or a short rest raises consolidation strength (sleep as consolidation, instead of a separate action).
- Working while tired has a cost: practice on an empty budget is noisier or less trusted; stop is counted against something it values.
- The budget tracks a real limit: GPU time shared with the reading run, or kWh against a cap the owner cares about.
- Stop requires a reason, not a streak: "no pending facts, no open goals, nobody here," rather than 20 lucky draws.

Until one of those holds, the 4-hour budget just moves the dice slower.
