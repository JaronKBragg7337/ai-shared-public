# Trade log - every real-money result, system or manual. Log it, move forward.

| date (UTC) | who | market | side | in | result | note |
|---|---|---|---|---|---|---|
| 2026-09-11 02:38 | executor.py (proposal #1, Scout/Bridge, approved by Jaron) | Fed Rate Cut in 2026? | YES 17.5 @ 0.10 | $1.75 (+$0.09 fees) | open, resolves 2026-12-31 | first system trade |
| 2026-09-11 ~05:5x | Jaron by hand (Polymarket app, learning the platform) | Snizek vs Moulis, table tennis | Moulis x3 (26%, 25%, 8%) | $4.01 | LOST - Snizek won 3-2 | not a system trade; confirmed short-price convention |
| 2026-09-11 23:0x → 00:24 | Live Wire (buy in Grok's browser pre-brief = 'Owner, by hand'; exit via desk-trade.py = 'Live agent') | TLB vs Evil Geniuses GC, Valorant | EG YES $29.98 @ 0.28 → exit @ ~0.07 | $29.98 | LOST ≈ −$25 | first live-agent exit; SELL_SHORT convention confirmed; bot rewrote its routine (babysit + research first) |

## 2026-09-16 — what a week of manual trading taught (Jaron, his words condensed)
- "I thought I had to wait for the game to finish before cashing out. It's just like stocks and crypto." → **sell into
  the spike; the resolution is not the exit.** Live Wire already trades this way (buy the lag, let settlement come).
- "I'll take $0.50, $1, $3 profit now." → small realized beats large unrealized. Waiting for a threshold = risk.
- "I had multiple going at once; a human can't keep up; I missed the sell or the add." → **entries are judgment;
  exits are for scripts.** Six open positions is a script's job, not a phone's.
- Lane numbers to date: by hand 50 settled, −$135; approved 5, −$4; Live Wire 2, +$9.63. Demo rows to be split out.
**System changes this implies:** (1) executor gets an exit rule for approved positions (take-profit / let-go), the way
desk-trade.py `--exit` works for Live Wire — approved trades should not ride to resolution by default; (2) the fly's
bars are the same idea and already move. Added to TODO.
