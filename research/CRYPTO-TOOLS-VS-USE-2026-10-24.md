# Crypto bots: tools they have vs what they used (2026-10-24, 8:40 PM)
Source: state/twin-crypto-paper.jsonl (334 bot calls, 242 scored at the real ask) + state/crypto-consensus.jsonl (61 live trades).
Rerun: `python tools/crypto_tool_usage.py`. Raw numbers: research/crypto-tool-usage-2026-10-24.txt. Small sample (~2 days).

| Tool on the board | Used in reasons | Result when used (paper) |
|---|---|---|
| Fair chance / options | 278 of 334 | 90 wins of 206, +$93 |
| Price vs open | 216 | 95 of 196, +$73 |
| FLOW (real money now) | 174 | 60 of 146, **+$95 (best)** |
| Order book / walls | 121 | 48 of 103, +$36 |
| Momentum 5/15 min | 93 | 44 of 71, +$30 |
| **POLY LAGS (the main tool in their how-to)** | 85 | **15 of 65, -$18 (worst)** |
| Funding | 52 | 17 of 41, -$7 |
| 1-min volatility | 19 | 2 of 16, -$20 |
| Open interest | 14 | 7 of 13, +$6 |
| Scheduled events | 10 | 1 of 7, -$7 |
| Headlines / ETF news | 1 | barely used |
| Fake-move warning | **0** | never used |

## What it says
1. Paper overall made money (+$90 on $720) but live lost (-$39.50 on 55 settled). Live traded the losing slice.
2. Live money went mostly to cheap long shots: 43 of 55 live trades bought a side under 35c; 9 won. Paper favorites (50c+) won 78% (+$36) but only 3 went live (all won).
3. POLY LAGS assumes Polymarket is behind. Most of the time Polymarket was right. Possible reason (not established): the market settles on the CF Benchmarks index; our board shows Kraken/a blend, so a "lag" can be our feed, not theirs.
4. Same calls on paper vs live: paper -$25, live -$40. Fees $3.10, the rest timing/exits.
5. Bots: Jarons Twin (contrarian) +$54 paper; Darios (momentum) +$5; Satya (fair price) -$34.

## Settlement price check (8:45 PM)
- Hourly US markets settle on CF Benchmarks BRTI (60 one-second prices averaged in the last minute) - read from the market's own rules via polymarket_market.
- Free BRTI data: not found. Public web page shows the value only; API needs a CF Benchmarks license or a Kalshi entitlement; terms bar use for financial products without a license.
- Our Kraken/blend stand-in matched the real settlement on 51 of 53 live trades (96%). The 2 misses were near-flat windows. So the feed is NOT the main cause of the losses.
- Main cause per the numbers: buying the cheap side because our "fair chance" said Polymarket was too low. Side bought at 15-35c won 23.8% (paid avg 25c) - Polymarket's price was closer to right than our model.
