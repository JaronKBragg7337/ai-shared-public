# claude-haiku-5-5 - Q-B
Time: 2026-10-15 08:37 | fresh subagent, read-only

**What it costs now**

- Resting itself costs almost nothing. Rest does no work and uses no GPU, so the 21-rest stretch burned no meaningful energy. Yesterday's whole run used about 0.06 kWh.
- The real cost is idle time. Those rests meant no practice and no exploring, and the owner was away 3.7 hours.
- The budget is not a limit. `Meter` spends time whether or not budget is left, and nothing checks the budget before work starts. It reached 10,500 s against 3,600 s and kept going. The budget only changes scores, so it is a pressure signal, not a brake.
- The stop is the one costly outcome. At 6:46 it shut itself down with 11 open goals, and only the owner can restart it.

**What it gives**

- Rest works as a cheap fallback when the budget is empty, and it gets a bonus when someone is talking so it answers fast.
- Every choice is logged with its drive scores, and the stop report records state. That gives the owner something to observe, which fits the stated goal.
- In practice it gives little else. Rest is a pause with no effect, so it does not improve memory, skill, or anything measurable.

**What would have to be true for it to matter**

1. The budget has to block work. A real pre-work check would make depletion a real constraint instead of a soft score.
2. Rest has to do something. If it consolidates, replays, or lets memories fade on purpose, then choosing rest is a real trade-off.
3. The drive weights have to respond to outcomes. Right now the formulas are fixed, so the choice is a weighted dice roll. Tying scores to practice accuracy or goal progress would give it reasons.
4. The new 4-hour budget needs a restart to apply, because `Clock` reads settings at startup. Even then, 3,900 s remain today, so the stop rule (which needs budget at zero) stays dormant until today's budget is spent again.

Until those change, the rest-and-stop system is mostly a logged pause that can end the run, not a choice that changes what Sapling learns.
