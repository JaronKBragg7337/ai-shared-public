# Grok Bot trader: money vs activity (made by tools/grok-money.py - rerun any time)

Profit = realized sell proceeds minus average cost of shares sold, plus P&L on shares held through settlement.
Log lines = routine passes + trades written that day; usage = Jaron's reading of the meter.
0 means Grok Bot did nothing that day (usage ran out, or it was switched off). Usage = Jaron's reading of the meter.

| day | log lines | fills | traded (buys+sells) | settled | profit | usage |
|---|---|---|---|---|---|---|
| Fri 09-11 | 17 | 4 | $10.66 | 0 | +$0.00 |  |
| Sat 09-12 | 277 | 2 | $10.05 | 1 | +$5.52 |  |
| Sun 09-13 | 206 | 1 | $4.96 | 1 | +$9.80 |  |
| Mon 09-14 | 209 | 0 | $0.00 | 0 | +$0.00 |  |
| Tue 09-15 | 12 | 0 | $0.00 | 0 | +$0.00 |  |
| Wed 09-16 | 0 | 0 | $0.00 | 0 | +$0.00 |  |
| Thu 09-17 | 62 | 13 | $65.60 | 1 | +$0.00 |  |
| Fri 09-18 | 166 | 1 | $4.95 | 1 | +$11.78 |  |
| Sat 09-19 | 201 | 7 | $29.55 | 5 | +$16.80 |  |
| Sun 09-20 | 251 | 2 | $1.48 | 1 | +$0.93 |  |
| Mon 09-21 | 178 | 5 | $16.88 | 2 | +$1.65 |  |
| Tue 09-22 | 143 | 9 | $28.35 | 2 | -$3.41 |  |
| Wed 09-23 | 70 | 0 | $0.00 | 0 | +$0.00 |  |
| Thu 09-24 | 119 | 0 | $0.00 | 0 | +$0.00 |  |
| Fri 09-25 | 148 | 9 | $34.83 | 5 | +$1.17 |  |
| Sat 09-26 | 51 | 63 | $286.61 | 22 | +$42.77 |  |
| Sun 09-27 | 47 | 78 | $561.50 | 18 | +$161.16 |  |
| Mon 09-28 | 53 | 23 | $154.34 | 9 | -$10.51 | 78% |
| Tue 09-29 | 49 | 43 | $213.95 | 21 | -$13.39 | 94% |
| Wed 09-30 | 9 | 7 | $24.82 | 3 | +$20.54 |  |
| Thu 10-01 | 11 | 5 | $19.88 | 1 | +$0.00 | 0% |
| Fri 10-02 | 49 | 37 | $188.30 | 11 | -$21.22 |  |
| Sat 10-03 | 1 | 134 | $770.19 | 17 | +$3.71 |  |
| Sun 10-04 | 0 | 66 | $330.04 | 4 | +$39.22 | 85% |
| Mon 10-05 | 0 | 0 | $0.00 | 0 | -$7.95 |  |
| Tue 10-06 | 0 | 0 | $0.00 | 0 | +$0.00 |  |
| Wed 10-07 | 0 | 0 | $0.00 | 0 | +$0.00 |  |
| Thu 10-08 | 0 | 0 | $0.00 | 0 | +$0.00 |  |
| Fri 10-09 | 0 | 20 | $68.99 | 4 | -$27.26 |  |
| Sat 10-10 | 0 | 50 | $141.05 | 8 | -$10.14 |  |
| Sun 10-11 | 0 | 11 | $33.21 | 3 | -$8.57 |  |
| Mon 10-12 | 0 | 0 | $0.00 | 0 | +$0.00 |  |
| Tue 10-13 | 0 | 0 | $0.00 | 0 | +$0.00 |  |
| Wed 10-14 | 0 | 0 | $0.00 | 0 | +$0.00 |  |
| Thu 10-15 | 3 | 3 | $25.31 | 3 | +$0.00 |  |
| Fri 10-16 | 9 | 4 | $20.91 | 1 | -$5.46 |  |
| Sat 10-17 | 8 | 16 | $68.10 | 8 | +$7.68 |  |
| Sun 10-18 | 13 | 0 | $0.00 | 1 | +$2.69 |  |
| Mon 10-19 | 0 | 0 | $0.00 | 0 | +$0.00 |  |

| week of (Mon) | settled profit | active days / days | profit per active day |
|---|---|---|---|
| 09-07 | +$15.32 | 3 / 3 | +$5.11 |
| 09-14 | +$29.51 | 6 / 7 | +$4.92 |
| 09-21 | +$203.34 | 7 / 7 | +$29.05 |
| 09-28 | +$18.35 | 7 / 7 | +$2.62 |
| 10-05 | -$53.92 | 3 / 7 | -$17.97 |
| 10-12 | +$4.91 | 4 / 7 | +$1.23 |
| 10-19 | +$0.00 | 0 / 1 | - |

| month | settled profit | active days / days | profit per active day |
|---|---|---|---|
| 2026-09 | +$244.82 | 19 / 20 | +$12.89 |
| 2026-10 | -$27.30 | 11 / 19 | -$2.48 |

| system | settled profit | fills | settled trades | days it traded | profit per trading day |
|---|---|---|---|---|---|
| Live Wire (v1, until 9/25 22:58Z) | +$44.25 | 45 | 15 | 10 | +$4.42 |
| Darios Twin (since 9/25 22:58Z) | +$173.27 | 568 | 138 | 16 | +$10.83 |

| Darios Twin by sport | settled trades | won | profit |
|---|---|---|---|
| cfb | 46 | 42 | +$117.20 |
| nfl | 13 | 12 | +$69.76 |
| odicr | 2 | 2 | +$23.51 |
| mlb | 8 | 5 | +$14.75 |
| intf | 1 | 1 | +$5.82 |
| itfwo | 1 | 1 | +$5.43 |
| kbo | 1 | 1 | +$3.70 |
| unl | 5 | 3 | +$3.55 |
| valorant | 2 | 1 | +$2.65 |
| epl | 1 | 1 | +$0.85 |
| nba | 2 | 2 | +$0.69 |
| lg1 | 1 | 1 | +$0.49 |
| lmx | 1 | 1 | +$0.25 |
| cnl | 1 | 1 | +$0.20 |
| afcq | 1 | 0 | -$0.38 |
| lal | 2 | 0 | -$1.96 |
| nhl | 5 | 3 | -$5.15 |
| cs2 | 1 | 1 | -$11.42 |
| wnba | 5 | 3 | -$12.50 |
| tennis | 39 | 17 | -$44.17 |

All time since 2026-09-11: realized + settlement P&L +$217.52 over 30 active days (+$7.25 per active day).
Money: profit +$217.52; open value $0.00; cash $68.80 (shared account snapshot 2026-10-19T11:12:02.724285+00:00).
Open value and cash are whole-account figures; profit above is actor-filtered to auto:grok-bot/live-wire.
