# Fly #1 — a real fruit-fly brain on live table tennis

**Status 2026-09-12 14:05:** Fly #1 running as task `Fly Brain` in **DRY RUN** (repaired after the Codex audit: per-mode cap/holding files, exit-code checks, sells teach, rewards polled every tick). **watcher-1** running as task `Fly Watcher`, writing `fly_ground`. No fly is alone. Jaron flips
it live by adding `--live` to the task's arguments (Codex or `Set-ScheduledTask`). Not before the
dry run has watched three matches — see `BUILD-BRIEF.md` "Definition of done".

| file | what |
|---|---|
| `watcher.py` | **watcher-1**: same brain, no hands. Sniffs every live table-tennis market every 15 s, writes senses + valence to Supabase `fly_ground` (the colony's shared ground), then fills in what the price did 60 s / 300 s later. Own mushroom store. Task `Fly Watcher`. |
| `fly.py` | the harness: senses → odour → brain → valence → press/let go; reward from the ledger; cap; ladder |
| `BUILD-BRIEF.md` | the spec (Jaron's decisions Q-013/Q-018, the ladder) |
| `runtime/` | `fruitflydev/flycoinrh` clone + MaleCNS data + `build/graph.npz` (165,122 neurons, 10,228,000 edges). Gitignored, ~1.2 GB. Rebuild: `.venv\Scripts\python runtime\build_graph.py` after fetching the three feathers from `storage.googleapis.com/flyem-male-cns/v1.0/connectome-data/flat-connectome/` (README path is missing that last folder). |
| `.venv/` | numpy/scipy/pandas/pyarrow/polymarket-us. No browser, no wallet deps. |
| `../../state/fly-brain/` | `log.md` (every sniff), `cap.json` (the money rule), `memory.json`, `mb_gains.v2.npz` (what it has learned), `milestones.md`, `graduates/` |

## How to read the log
`us 1-1 5-9 yes @ 0.36 d +0.00 sp 0.20 | KC 28 | val +67.7 (+74/+40/+89) streak +1x1 | -`
= our player leads 1-1 in sets, trails 5-9 in points; we would buy YES at 36¢; price unchanged since
the last set; spread 20¢; 28 Kenyon cells fired; approach-minus-avoid = +67.7 Hz averaged over 3
seeds (each shown); one tick into a positive streak; no action. PRESS/LET GO lines show what the
hands did and whether `desk-trade.py` accepted it (it refuses spreads over 5¢ on its own).

## What is measured vs chosen (say it every time)
Measured: the connectome, LIF model, KC→MBON plasticity site and direction, the sparse-KC
calibration (`pn05_apl10_kc03`). Chosen: which glomeruli carry which sense, the rates, the
valence thresholds (+20 / −15 Hz), 2-tick confirmation, 90 s cooldown, 3-second tick, and above all
the pairing P&L→dopamine. An untrained fly likes most smells; it will press on almost anything at
first and punishment carves that away. Expect the first trades to look random. That is the design.

## Known gaps (v1)
- Only one live table-tennis market existed at build time (a 20¢-spread WTT pro match); the screen
  correctly rejected it. Setka Cup (1–2¢ spreads) runs overnight US time — that is when the dry run
  gets its three matches.
- Serving is not a sense (the venue feed does not carry it).
- Reward in live mode arrives from the ledger at settlement (minutes later); the KC pattern from
  press time is replayed before dopamine so the lesson lands on the right smell. In dry run the
  harness settles a LET GO itself from the price move so learning can be exercised.
- The ledger label needs the reconciler to see `--by fly-brain` rows → `auto:fly-brain` → "Fly brain"
  on the trades page (done in `verifier.py` / `index.html`).

## Ops log
- **2026-09-13 09:50–10:05** — (1) Press/let-go bars now live in `cap.<mode>.json` and move with the fly's own
  realized P&L (win: press −1 Hz, loss: +1; let-go mirrors; bounds 5..40 / −30..−5). Only step and bounds are
  chosen. (2) Venue rate limits: 44% of the day's fly ticks were `RateLimitError`, each logging a full HTML page
  (logs hit 34 MB / 70 MB; moved to `*.bloated.md`). Fixes: one-line errors; back-off 10 s (fly) / 30 s
  (watcher); watcher sweep 15→30 s; fly tick 3→5 s (a point takes 10–20 s). Measured after: fly 44% → 27% → **12%**
  rate-limited, watcher ~22%. Remaining load is fly 24/min + watcher ~38/min + verifier + Live Wire against
  what looks like a ~60/min account limit. Next lever if it matters: watcher and fly share one events.list.
- **2026-09-16 20:45** — fly + watcher now share one venue scan (state/fly-brain/live-tables.json, 20 s). Fly rate-limited ticks 18–22% → 15%. The remaining load is per-table score/book calls, not the scan. Good enough; next lever if ever needed: batch the score reads.
