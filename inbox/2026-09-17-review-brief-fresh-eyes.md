# Fresh-eyes review brief (2026-09-17 09:05 EDT) — for Grok chat and ChatGPT chat, READ-ONLY. Same brief to both.

You have a connector to the MSI. Do not run experiments, do not edit anything. Read, then give your best theories.

## What we are trying to do (one sentence)
Make a simulated fruit-fly brain (MaleCNS v1.0, 165,122 LIF neurons) answer a symbol: odour A paired with reward dopamine,
then, cold, the fly's own output for A changes in the direction the biology predicts, and a never-paired odour C does not.

## What is true, measured (do not re-argue these)
- Symbols enter only through ORN receptor neurons. No model in the loop.
- On fly-v5 (fly-v3 graph + calibration: PN x1.27, APL x6.0, KC x1.79, KC threshold +1.8 mV, MBON x0.86) the Kenyon-cell code is
  sparse (4.6%), reliable (same odour 0.69 Jaccard) and odour-specific (0.06 overlap).
- MBONs are KC-dominated by wiring: 82% of MBON input |w| is KC->MBON (92% of excitatory input on the PAM/reward side).
- The learning rule (runtime/mushroom.py, from fruitflydev/flycoinrh): dopamine-gated DEPRESSION of KC->MBON synapses whose KC
  was active (eligibility trace x0.55 per observe), lr 0.06 (variant 0.2), floor 0.25, PAM-side MBONs for reward, PPL1-side for
  punishment (side table verified against Aso 2014). No potentiation, no DAN feedback, no MBON->DAN loop.
- After 12-24 pairings (A + reward), A's eligible synapses are depressed to ~0.25-0.5 gain. Yet PAM-side MBON output on A drops
  only 10-15% on average across flies, and ~0% in one fly in three (results/mb_calib/ stage 2, 3 seeds x 6 reps).
- Four predeclared tests (per-trial and block-level decodes, 32 fresh seeds) all failed. Test 5 (1 s pulses, 24 pairings,
  12 reps) is running now.

## Where to look (read-only)
- C:\Users\lilli\AI-Shared\research\FLY-BRAIN.md — sections from "THE READOUT WAS WRONG" to the end (last night + this morning).
- C:\Users\lilli\Fly-Lab-2\comm_protocol.md — every predeclared test; comm_loop.py — the exact kernel, training, cold test, decode.
- C:\Users\lilli\AI-Shared\projects\fly-brain\runtime\mushroom.py — the rule; calibration.py — the CHOSEN gains; flysim.py — the cell.
- C:\Users\lilli\Fly-Lab\versions\fly-v3\MANIFEST.md, fly-v5\MANIFEST.md — what changed and why.
- C:\Users\lilli\Fly-Lab-2\results\comm_loop_test3_lr02.json, comm_loop_test4.json, mb_calib\r0_c007.json — raw numbers.

## The questions (answer each; number them; say "don't know" where you don't)
1. Why would 50-75% depression of A's KC->MBON synapses move PAM-side MBON output by only 10-15%? List every mechanism you can
   see IN THIS CODE (not in general) — e.g. which KCs are eligible vs which drive the cold response; the trace; the floor;
   the gain application (mb.apply writes base*gain into fb.wdata — check it reaches the kernel that comm_loop.py runs);
   MBON-MBON inhibition; APL; refractory; the 300 ms window; anything.
2. Is anything we built WRONG rather than weak? (side table use, reward/punish sign, readout population, decode, seeds, the
   equalisation of C's rate, the v3 min-6-synapse rule deleting KC->MBON edges (it kept 29k of 44k), the KC threshold shift.)
3. What does a real fly have here that this model lacks, that would plausibly turn a 10% change into a decision? (DAN feedback,
   potentiation, MBON->DAN, KC->APL adaptation, compartment-specific readout, longer odour, spaced training, anything.)
4. Which ONE experiment would you run next, exactly, that can pass or fail in under an hour on this laptop?
5. Grok only: compare with lulzx/fly-brain and Fly.exe — did either show a learned, odour-specific MBON or behavioural change?
   ChatGPT only: from the literature, what % MBON response change does one appetitive pairing session produce in vivo
   (Hige 2015, Cohn 2015, Owald 2015, Handler 2019), and over what odour duration / number of trials?

Give theories ranked by how likely you think they are, with the file:line or number that made you think it. No summaries.
