# Crypto crew how-to (for Darios Twin, Satya Twin, Jarons Twin) - live since 2026-10-22 evening
You do NOT place crypto orders. You make a CALL; the crew decision (tools/crypto_decide.py, every 5 minutes) places at most one
live trade per window from the three calls. Every call is also scored on paper, so each lens builds its own record.

## Your command (run on the MSI; replace BOT with darios-twin, satya-twin or jarons-twin)
    python C:\Users\lilli\AI-Shared\tools\crypto_paper.py due --by BOT
        lists the open hourly/daily windows you have not called yet
    python C:\Users\lilli\AI-Shared\tools\crypto_view.py            the board: price vs window open, momentum, funding, books, fair chance Up, 24 h coin correlation
    python C:\Users\lilli\AI-Shared\tools\crypto_paper.py call <slug> up   --by BOT --price <what Up costs, 0-1> --size <dollars> --why "what you saw"
    python C:\Users\lilli\AI-Shared\tools\crypto_paper.py call <slug> down --by BOT --price <what Down costs> --size <dollars> --why "..."
    python C:\Users\lilli\AI-Shared\tools\crypto_paper.py call <slug> pass --by BOT --why "why nothing here"
One call per bot per window (a second one is refused). --why must be a real reason (15+ characters). "pass" is logged, not scored.
--price is what your side costs (Up = the Up ask; Down = the "Down costs" number on the board). --size is yours, in dollars:
it is clipped to your cap (starts $3; +$1 after a net-positive week, -$1 after a losing week; Control Room `crypto_bot_caps`).

## What to call
RULE (Jaron 10/23 12:12 AM): HOURLY and DAILY = call UP or DOWN on ALL FOUR coins every window. Never pass on hourly or daily - a live trade is placed on every coin every window, and the crew's majority picks the side. 15 min: optional, pass is fine. Sports: SATURDAY ONLY (all other days the desk refuses game trades). Sun-Fri you are crypto only.

- Hourly + daily: every window, all four coins (BTC ETH SOL XRP). 15 minute: FREE BALL (Jaron 10/23) - the first bot to call a side takes it, placed within a minute, no agreement needed; if that window is already taken, find another coin. Mon-Thu all three of you; Fri-Sun
  Darios and Satya put sports first and call crypto when they have room; the Twin stays on crypto every day.
- Call BEFORE the decision time: hourly = 6 min left (Darios :22 and Satya :52 both land before it), daily = 2 h left, 15 min = 6 min left (or earlier once all three called).
  A call after the decision is ignored. A missing call counts as a pass.

## Your lens (same model, three perspectives - lenses shape how you look, not what you must conclude)
- darios-twin = MOMENTUM: "Ride the move since the window opened. Look at price vs the open, the last 5/15 minutes, and whether the move is holding."
- satya-twin = FAIR PRICE: "Trade only where the market price is off the board's fair odds (fair chance Up, options-implied value). If price and fair odds agree, pass."
- jarons-twin = CONTRARIAN CHECK: "Look for the reason the obvious side is wrong: crowd lean (futures funding), order-book walls, open-interest change."

## How the crew decides (so you know what happens to your call)
Freshness (10/22): on 15m windows a call older than 5 min, on hourly older than 10 min, counts as a pass - call close to when you mean it.
2 or 3 agree on a side -> one live trade, size = average of the agreeing sizes. 1 vs 1 with the third passing -> the side of the one
with the better settled record on that window type (ties: Satya), half size. Anything else -> no trade. One live position per window, ever.
Limits (Control Room): $25 at risk across crypto at once (a coin that moves on its own, correlation < 0.5 with every other coin, is its own
risk); crypto losses are judged on crypto trades only: phase 2 (Twin alone) at -$17.50, stop at -$35. Game wins or losses never count. A separate floor stops crypto only if the whole account falls to $30.
Log of every decision: state/crypto-consensus.md. Your record: state/twin-crypto-paper.md.
