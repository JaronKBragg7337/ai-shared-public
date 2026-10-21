# codex-gpt6-luna - Q-B
Time: 2026-10-15 07:52 | 25s

Right now, rest costs little measured compute. It waits for the next five second tick, and that waiting does not spend the compute budget. The heartbeat still runs, but yesterday’s total energy use was only about 0.06 kWh. The larger cost is opportunity: while resting, Sapling does no practice, exploration, or consolidation.

The budget and stop choice did not cap yesterday’s work. The budget was empty, yet Sapling overspent by 10,500 seconds against a 3,600 second allowance and consolidated 37 times. In the code, zero budget raises the rest score and lowers the work scores; it never blocks work. Stop only gets a score after the budget is empty and there have been at least 20 rests in a row. The owner must restart it after it stops.

What the system gives is a nudge toward idling when the allowance runs out, plus a logged way for Sapling to stop itself. Rest also briefly gets a boost after someone talks to it, helping keep it available to answer. These are preferences and observability, not safeguards.

It would start to matter if the scores changed behavior enough to reduce costly work, or if stopping created meaningful downtime or saved meaningful energy. That depends on the actual workload and power draw: a four hour budget can still be overspent, and rest only saves energy if waiting uses materially less power than working. The useful evidence is whether the new allowance changes work, energy use, or stop frequency over time.
