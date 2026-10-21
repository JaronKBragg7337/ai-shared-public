# claude-fable-5-1 - Q-A
Time: 2026-10-15 08:37 | fresh subagent, read-only

Keep it, for now.

Why:

1. It barely slows anything. The rest score is 0.08 + 0.9 × (1 − budget left)². With a full budget, rest scores 0.08 against roughly 0.75 for practice and 0.75 for explore, so rest wins maybe one tick in twenty. Now that the budget is 4 hours instead of 1, Sapling will spend most of each day with budget to spare, and rest will almost never be chosen. Turning it off would buy very little speed.

2. The one bad night was not the rest system's fault. The heartbeat restarted at 3:05 AM onto a budget that was already empty, because the budget is per day and the day's hour was gone. Even then, since the choice is sampled by weight and not by max, rest only took about 60% of ticks; it still did 37 consolidations in 3.7 hours. That is not a stalled system. It is a system working at reduced pace, as designed.

3. Real cost is almost nothing. 0.06 kWh for the whole day. Resting does not save energy in any way that matters, but it also does not waste it.

4. The self-stop is the actual thing that costs development time, because only the owner can restart it. But it needs budget at zero and 20 rests in a row, which at a 60% rest rate happens about once every few thousand ticks. With a 4-hour budget this should be rare. And the stop report from 6:46 AM is exactly the kind of data the owner said they want to observe. Removing the system removes the thing being studied.

What would change my mind:

- Logs showing rest taking a large share of ticks while budget is still above zero. That would mean the formula is wrong, not just the budget.
- Repeated self-stops overnight, each losing hours waiting for a restart. Then I would soften the stop rule (or let it restart itself after the day resets) rather than remove the budget.
- Evidence that GPU idle time is the bottleneck for whatever "faster development" means here. Right now, the big reading runs already pause the heartbeat, so the heartbeat is not where the time goes.

One small fix worth considering: reset or pro-rate the budget when the heartbeat restarts after a long pause, so it does not wake up already empty.
