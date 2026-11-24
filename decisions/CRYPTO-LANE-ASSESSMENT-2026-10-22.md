# Crypto lane: Claude Code's assessment (2026-10-22, asked by Jaron after a talk with Vex). NOTHING CHANGED YET.

## What the system does today (checked in files + Control Room)
- desk_schedule: a slug whose sport is in no lane is OFF. ETH/SOL/XRP slugs (cpceth-eth-..., cpcsol-sol-..., cpcxrp-xrp-...) read as
  sport eth/sol/xrp -> in no lane -> the live twins CANNOT trade them. BTC lane is open but btc_max_size_usd = $1.
- The $1 BTC cap came from Darios's own BTC trend test (10/2: $1/trade, stop at 10 trades or -$5), not from Jaron's losses. It was never reviewed or lifted.
- Darios's instructions say "no crypto" (crew update 10/15). Changing that = new instruction text Jaron pastes.
- NFL is auto-benched (21-day net below -$15, 10/19). Basketball + soccer lanes are open as tests; NBA/NHL season is just starting.
- Jarons Twin: crypto PAPER only, near rule-free on purpose. Day 1: 52 calls, 33 won, +$58 paper.

## Ideas vs the system
1. More of the crew on continuous markets: compatible (one lane row each for eth/sol/xrp + lift btc cap). Needs evidence first (below).
2. 21-domain news into short-term crypto: weak fit for 15m/1h (overnight captures are slower than price). Good fit for daily windows + Kraken long-term.
   Cheap test: tag each Twin call with whether a related headline existed, compare.
3. Several AIs on the same coins, no duplicate live positions: compatible. Paper: unlimited analysts. Live: one position per window
   (desk-trade's per-game cap already limits stacking on one slug).
4. No permanent coin assignments: agree. Everyone calls every coin on paper; compare traders on the SAME windows.
5. Limited live next to paper: agree - paper overstates (it assumes a fill at the ask, no slippage, Kraken price stands in for CF Benchmarks).
   A tiny live tracer is the only way to learn real fills.

## Evidence bar, written BEFORE the data (Claude Code's proposal 10/22, not a Jaron rule; the plan Jaron approved 10/22 6:30 PM replaced the tracer idea)
- Tiny live tracer: Twin or a twin, hourly windows only, $1/call, 7 days. Purpose: real fill vs paper price, not profit.
- Real lane (normal size) only when ALL hold: >= 7 days and >= 300 settled paper calls; positive after the spread for that window type;
  Edge Check shows its fair odds track outcomes; result not carried by one trending day (no single day > 50% of the profit).
- Sports stay running in parallel; nothing is retired for seasonality alone. Decision + numbers get published on the crew page.

## Source + clarification (6:20 PM)
- Full Jaron/Vex talk saved: research/vex-claude/2026-10-22-jaron-vex-crypto-lane.txt.
- ETH/SOL/XRP ARE live and tradeable on Polymarket US (desk.py search shows them "ok"). They are off only because OUR lane list has no eth/sol/xrp row - a one-row Control Room change, not a platform limit.
- Points from Vex (Claude kept these as things to watch; Jaron has not set them as rules): monthly bills must not drive trade decisions; 4 coins move together, so watch total exposure across them, not just per trade; news helps fast windows only if it arrives as timestamped events, not the 8 AM show.
- Jaron's own lean (transcript): he'd rather move the whole crew to markets than chase seasons, and part of him wants it tested for real, not only on paper - the $1 tracer is the bridge.
