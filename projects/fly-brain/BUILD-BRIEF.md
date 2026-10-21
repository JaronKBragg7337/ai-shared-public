# Fly #1 — build brief (for Codex on GPT-6 Astra, fresh 5h window)

**Owner:** Jaron. **Decision record:** `decisions/OPEN-QUESTIONS.md` Q-013, Q-018.
**Research:** `research/FLY-BRAIN.md`, `research/FLY-BRAIN-RUNTIMES.md`.
**Written by:** Claude Code, 2026-09-12 12:25. Claude/Codex build the harness; neither ever presses.

## What you are building
A harness around a simulated fruit-fly brain that watches ONE live table-tennis market on Polymarket
US and decides press / don't press. Runs on the MSI. Everything the fly does leaves a trail.

## Runtime
Start from `fruitflydev/flycoinrh` (`flysim.py` + `mushroom.py`): CPU, NumPy/SciPy LIF over the
MaleCNS graph, input `{neuron_indices: rate_hz}`, readout = chosen motor populations, dopamine-gated
KC→MBON learning with eligibility trace. Clone into `projects/fly-brain/runtime/` (gitignored). If it
will not run on this machine, fall back to `nftechie/stonkfly` (native C++ kernel) and say so.
Do NOT install a GPU stack; the RTX 4060 is for Qwen.

## Senses (v1) — for the single market the harness has selected
Map each to a small population of sensory neurons (pick populations by name/role from the
connectome; document which). Update every 2 s from `tools/desk.py book <slug> --json` and the live
score (scrape polymarket.us's event page, or the Setka/ensigame score feed — whichever is reachable
without login; document the source):
1. sets won, our side vs other side
2. points in the current set, our side vs other side
3. serving: us / them
4. YES price now (the side we would buy)
5. price change since the last set ended (signed)
6. spread

Memory the fly keeps for itself (a JSON the harness feeds back as a sense): player names it has
seen, and whether it won or lost when it pressed on them.

## Action
One readout population = PRESS. Above threshold for ≥ 2 consecutive ticks → the harness runs
`tools/desk-trade.py --by fly-brain --slug <slug> --side yes|no --size <cap> --why "<sensory snapshot>"`.
Exit: a second readout population = LET GO → `--exit`. Nothing else. The fly never sees a size.

## Reward (Stonkfly's recipe, verified in `research/FLY-BRAIN-RUNTIMES.md`)
Realized P&L from the ledger (`desk_trades` where actor = 'auto:fly-brain'), polled every 30 s.
Profit → stimulate the PAM dopamine population (reward). Loss → stimulate PPL1 (aversive). Magnitude
scaled by P&L / trade size. That is the whole teaching signal. No rules, no prompts, no approve taps.

## Money limit — in the HARNESS, hard-coded, invisible to the fly (Jaron's spec)
Start: **$1 per trade, $5 total exposure.** Every **$10 realized profit** unlocks **+$1/trade and
+$5 exposure**; losses reduce it the same way. Floor $1/$5. Read the cap from `state/fly-brain/cap.json`
which only the harness writes. Never more than one open position per market. Skip same-name matchups.

## The ladder — two tiers of reward (Jaron, 2026-09-12 12:30)
*"Money is the small ones. Upgrades are the big ones for the fly's drive."* The fly feels only
dopamine; we see a career. Small PAM burst per winning trade. A LARGE burst (3–5× the per-trade
magnitude) when cumulative realized P&L first crosses each milestone; the harness also changes the
fly's world:
| realized P&L reaches | large burst + | what changes |
|---|---|---|
| $10 (and each +$10) | medium | cap +$1/trade, +$5 exposure (the money rule above) |
| $50 | large | **graduate v1**: weights checkpoint copied to `state/fly-brain/graduates/v1-<date>.npz`, never overwritten |
| $100 | large | **retirement** (Jaron, 2026-09-12 14:22): the fly stops working. Its weights are frozen and cloned to the cloud as the colony's seed; the fly itself moves to the fly world — the 3D worlds, or a fly world of its own with unlimited sugar. It never trades again. "Retirement or heaven." The DN (walking) output the scene brief exposes is how it walks there. |
| $250 | large | **a sibling**: second fly spawned from the checkpoint on a second market — the swarm begins |
Milestones are one-way: losses fire PPL1 in small doses and lower the cap, but a graduate stays a
graduate and property is never taken back. Record every milestone in `state/fly-brain/milestones.md`.
v1 needs the threshold checks and the large-burst stimulus wired; the cloud clone is a later task.

## Trail (non-negotiable)
- Every press/exit = a `trade_proposals` row (`proposed_by='fly-brain'`, `verdict='auto'`) via
  desk-trade.py — already handled by that script.
- `state/fly-brain/log.md`: one line per tick where anything changed (senses, readout levels, action, reward).
- `state/fly-brain/cap.json`, `state/fly-brain/memory.json`, and a checkpoint of synaptic weights every
  10 min so a restart does not forget what it learned.
- Ledger label "Fly brain" — add `auto:fly-brain` to the ACTOR map in `live-systems/trades/index.html`.

## Market selection (harness, dumb)
From `tools/desk.py live --json`: table tennis only, in progress, spread ≤ 2¢, YES price 0.20–0.80,
not same-name. One at a time; move to the next when the match settles.

## Run it
Windows task `Fly Brain` (AtLogOn + start-now trigger, restart on failure, no time limit), venv under
`projects/fly-brain/.venv`. `--dry-run` first: it must run through three full matches logging senses,
readouts and would-be presses with NO orders before anyone flips it live. Jaron flips it live.

## Definition of done for v1
Dry run across 3 matches with sensible logs → Jaron says go → first real $1 press → ledger shows
"Fly brain" → reward fires → weights checkpoint changes. Report exactly what happened, including
if the fly never presses (that is data too). Handoff to `handoffs/YYYY-MM-DD-codex-fly-brain-v1.md`.
