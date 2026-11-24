# Crypto lane plan - DRAFT for Jaron to read (2026-10-22 6:30 PM). Nothing changed until he says go.
Builds on CRYPTO-LANE-ASSESSMENT-2026-10-22.md. Jaron's lean: borrow more risky than cautious.

## Why (the public reason)
Sports trading is seasonal and the twins sit idle Mon-Thu (last 3 weeks, bots only: Mon 2 trades, Tue 0, Wed 1, Thu 6;
Fri 45, Sat 142, Sun 41). Crypto up/down markets never close. This uses idle days; nothing is taken from sports.

## Who does what
- Mon-Thu: Darios, Satya, Jarons Twin all call BTC/ETH/SOL/XRP. Hourly + daily: every window, all four coins. 15 min: any coin they see.
- Fri-Sun: sports first for Darios + Satya (college football especially); crypto when they have room. The Twin stays on crypto every day.
- No fixed coin per bot - everyone calls everything, so traders are compared on the same windows.

## Three lenses (same model, different perspectives, so agreement means something)
- Darios = momentum: rides the move since the window opened.
- Satya = fair price: trades only where the market price is off the board's fair odds.
- Jarons Twin = contrarian check: looks for the reason the obvious side is wrong (crowd lean, order-book walls, futures funding).
Lenses shape how each one looks, not what it must conclude.

## Deciding (built to never deadlock, leaning toward action)
- Each bot writes its call (up / down / pass) + its own size within its own cap.
- 2 or 3 agree on a side -> one live trade on that side, size = average of the agreeing sizes.
- 1 vs 1 with one pass -> trade the side of whichever of the two has the better record on that window type, at half size.
- All three pass, or a clean 1-1-1 split -> no trade (logged as a pass).
- One live position per window, ever (no stacking).
- Every call is still scored on paper, so each lens builds its own record.

## Limits (Control Room settings, Jaron approved 2026-10-22 6:30 PM; $25 cap loosening per his addition below)
- Per trade: each bot's own cap, starting $3 (Twin) / $3 / $3; a cap rises $1 after each week the bot is net positive, falls $1 after a losing week.
- Per day across all four coins: max $25 at risk at once (the coins move together, so this is the real risk number).
- Old btc_max_size_usd ($1, from the 10/2 test) replaced by these rows.

## Review
- Weekly Monday: Edge Check + per-lens record. After 2 weeks: publish the numbers on the crew page and decide whether crypto
  gets more days, more size, or less.

## APPROVED by Jaron 2026-10-22 6:30 PM ("I'm OK with all of this"). Live start Mon 10/26.
Jaron's addition: the coins have moved together for years, but as digital rails mature some may split away (QNT already does).
So the $25-at-once rule is not a forever assumption: the board measures how closely the coins actually move (rolling correlation),
and when a coin decouples it counts as its own risk and the shared cap loosens for it. Measure it, don't assume it.

## PAUSED 2026-10-23 5:35 AM (Jaron). Night 1 post-mortem (Jarons Twin's own read, 5:51 AM, checked against the logs)
- Paper flattered: from 7 PM, 8/8 empty-book calls (+$16.74) were priced at the Twin's own fair number - nobody sold there;
  one ETH 15m long shot at 0.14 (+$18.43) was about half the paper profit and live couldn't get it (price jumped).
- Live lost on: forced hourly calls on every coin with no edge (the no-pass rule), and cheap 15m long shots (0.08-0.24) in
  the last 2-7 minutes (15m went 2 for 10). Hourly calls where price, momentum and books agreed went 7-4 live.
- Gaps: no fill logging (real per-trade P&L not on file); no news/X/scheduled-event input; the stop counted only settled
  trades, so trades already open ran past -$35.
Restart plan (Twin's, Claude agrees) - only when Jaron says go:
 1. Log real fills per trade. 2. Paper scored only at prices that existed. 3. Passing allowed again when there is no edge
 (drop must-call). 4. No 15m buys under ~0.25 in the last 5 minutes. 5. Add a news/events feed (Fed/CPI, ETF flows,
 headlines). 6. Restart small: $1-2, hourly only; add 15m once hourly is proven. 7. Stop counts open risk, not just settled.

## RESTARTED as v2 test, 2026-10-23 ~6:20 AM ET (Jaron: "Let's test it") - Claude Code
Built: real fills + exits + settlement + hold-vs-exit per trade in state/crypto-consensus.jsonl (crypto_decide.reconcile_fills); paper
scored only at the real ask (empty book = excluded); passing allowed (must_call removed; any up-vs-down disagreement = no trade, one bot
alone can trade); no 15m buy under 0.25 with under 5 min left; stop = settled P&L minus open cost (worst case); crypto_view signals
(POLY LAGS, FLOW, POSSIBLE FAKE MOVE, events, headlines, ETF) in tools/crypto_signals.py; exit command (crypto_paper.py exit).
Control Room: caps $2 each, crypto_lane_start = 2026-10-23T10:20:28Z, phase1 999 (no switch), phase2/stop 10, crypto_15m_enabled 0,
crypto_1d_enabled 0 (hourly only), account floor 30.
