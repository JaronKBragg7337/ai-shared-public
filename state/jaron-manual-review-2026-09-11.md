# Jaron's own trades, 2026-09-10 22:00 → 2026-09-11 10:31 — reviewed by Claude Code 11:05

Source: venue activity via `polymarket_activities` (MANUAL-stamped orders only). 19 markets, 29 fills,
$4.80 in fees. Net **−$16.53** (resolved + sold + open marked). Deposits $158; account ~$131 + positions.

## By size
| bets | markets | won | net |
|---|---|---|---|
| ≥ $15 (Kuzmych $30, Derevianko $20, Horokh $45) | 3 | 1 | **−$19.87** |
| < $15 | 15 | 6 | **≈ +$1** |
The three big bets are the whole loss. The small ones are break-even and the sample is growing.

## By entry price
| bucket | markets | won | net | read |
|---|---|---|---|---|
| favourite ≥ 0.85 | 2 | 1 | −$19.57 | Derevianko: $20 to win $1.50, lost. Kuzmenko: won, paid 32¢. One loss erases 13 wins. Worst bet type on the board. |
| longshot ≤ 0.10 | 3 | 0 | −$5.95 | Lottery tickets. Cheap, but 0 for 3. |
| mid 0.10–0.85 | 13 | 6 | **+$6.86** | Komar @0.24 → +15. Horokh @0.57–0.65 → +29. Where the wins live. |

## What it says (data, not scolding — his rule: log it, move forward)
1. **Mid-priced live table tennis is where he made money**, both as underdog (Komar 0.24) and
   near-coin-flip (Horokh, Yelfimov, Deineha, Hanacek). 6 of 13.
2. **Heavy favourites are the trap**: tiny payoff, full downside. Never $20 at 0.93.
3. **Size did the damage, not selection.** Same picks at $5 each ≈ +$1 → the loss came from
   three oversized bets, one of which won big and still could not cover the other two.
4. **Cashing out early worked** (Smyk +0.46 instead of riding it). Selling when the read changes
   is a skill; Live Wire has `--exit` for exactly this.
5. **Open question for him:** 11:02 manual sell of 5.88 "Fed No Change" shares at 8¢ — this was the
   SYSTEM's position (#5, bought 17¢, resolves Sep 16). Intentional cash-out, or a mis-tap?

## Fed into Live Wire (agents/grok-bot/LIVE-WIRE.md → "What Jaron's own trades taught")
Prefer 0.20–0.70 entries in live matches. No favourites above 0.85. $5 default, $10 max. Exit when
the read changes rather than riding to zero.
