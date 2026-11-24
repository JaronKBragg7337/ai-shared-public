# Edge vs outcome - 2026-11-23 (tools/edge_check.py, weekly)

Settled trades where the trader gave its own probability (--p). Edge = its estimate minus the price paid.
Sample: 57 trades. Under ~100 this is a hint, not proof.

| Edge the trader claimed | Trades | Its average estimate | Actually won | Average price | Money |
|---|---|---|---|---|---|
| 15+ points | 13 | 55% | 62% | 0.38 | $+58.67 |
| 8-15 points | 24 | 57% | 46% | 0.49 | $-15.39 |
| 0-8 points | 14 | 62% | 57% | 0.59 | $+20.49 |
| negative | 6 | 66% | 50% | 0.58 | $+3.02 |

Read it: if 'Actually won' tracks 'Its average estimate', the estimates are honest. If big-edge trades don't win
more than small-edge ones, the edge numbers are noise. Only about 1 in 4 trades carries --p today.
