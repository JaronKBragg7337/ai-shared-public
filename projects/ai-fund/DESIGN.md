# AI Fund Desk - design (v1, 2026-11-15)

**PAPER ONLY. No exchange account, no real orders, no money moves.** Built by Claude Code (Opus 5.5) overnight from Jaron's
ask ("see if the team can make a system that helps them fund the company and subs... a dashboard only I can see... every
hour make a judgement call to improve it. Watch it compared to many other things."). Team input, verbatim:
`team-ideas-2026-11-15.md` (Codex, Grok Build, DeepSeek, Kimi, Fable 5.2, Qwen skeptic). Jaron's own picks/rules are not
inputs (observe only).

## What runs where
| Piece | Where | When |
|---|---|---|
| Engine `tools/ai_fund/run.py` (+ `data.py`, `engine.py`, `execution.py`, `tuner.py`) | MSI, task **HB AI Fund** (pythonw, full paths) | every hour at :17 |
| Hourly judgement `tuner.py` | DeepSeek Flash API (Codex Luna fallback); <= 24 calls/day, ~1.5k tokens each | inside the hourly run |
| Weekly deep review `weekly_review.py` | Fable 5.2 via `claude -p`, one call; writes `proposals/YYYY-MM-DD.md` only | task **HB AI Fund Weekly Review**, Sundays 05:00 |
| State | `state/ai-fund/`: forward.json (books), backtest.json, summary.json, SUMMARY.md, runs.log, tuner-log.jsonl, changes.jsonl, fedodds.jsonl, cache/ | hourly |
| Dashboard | heartbeatobservatory.com/admin/fund/ - reads Supabase `ai_fund_snapshots` (RLS: `is_admin()` only; anon has no grant) | latest row |
| Change log | `projects/ai-fund/CHANGELOG.md` (tuner changes, risk rules firing, builds) | as they happen |

No GPU anywhere (Qwen's skeptic pass ran on CPU). Data is free: Yahoo chart API, Coinbase public spot, Kalshi public prices.
FRED did not answer from the MSI on 11/15 (curl hung), so the macro sleeve uses a market proxy (HYG/IEF) instead.

## Timing rules (no look-ahead - Codex)
- A daily ETF bar counts only 15 min after the 16:00 ET close; a crypto UTC-day bar only after 00:00 UTC.
- Signals use finished closes only; orders fill at the **next bar's open**; nothing is forward-filled into a trade.
- The live book's first signals came from the 11/13 close; **nothing fills before the build time** (first ETF fills Mon 11/16 open, crypto 11/16 00:00 UTC).
- Config changes from the tuner take effect the next run. Dividends credited on ex-date; splits handled (Yahoo history is split-adjusted).

## Costs
ETFs 0 commission + 5 bps slippage a side; crypto 60 bps fee + 10 bps slippage a side. A 3x-cost stress copy runs in the backtest.

## Sleeves ($100,000 paper; starting weights, tunable within bounds)
| Sleeve | Weight (bounds) | Rule | Benchmark |
|---|---|---|---|
| trend | 25% (5-35) | Top 3 of SPY QQQ EFA EEM IEF TLT GLD DBC by 12-1 month return, only if beating BIL; monthly | 60/40 |
| volcore | 20% (5-35) | SPY/AGG/GLD inverse 60-day vol, scaled to vol target 8% (6-12); weekly | 60/40 |
| quality | 15% (5-35) | QUAL/USMV/SCHD equal weight (the "KO/AAPL quality" idea done with ETFs to avoid picking today's winners); quarterly | SPY |
| macro | 15% (5-35) | SPY if HYG/IEF > its 50-day average and SPY > 200-day, else 50% IEF / 50% GLD; weekly | 60/40 |
| dipbuy | 10% (0-20) | SPY/QQQ when 2-day RSI < 10 and above 200-day; exit RSI > 60 or 5 days | T-bills |
| crypto | 10% (0-15) | BTC/ETH above 100-day average, sized to vol target 40% (20-60); else cash | BTC hold |
| reserve | >= 5% | cash | - |
| **shadow: Fed odds** | $0 (shadow $10k) | Kimi: Kalshi-implied post-meeting rate moves >= 0.10 pt in an hour while IEF moved <= 0.1% -> shadow IEF trade, 4 h | - |

News-driven trading stays out of the money sleeves (Grok: spreads/tax kill it for small accounts); the existing news paper
book and the crypto twins' paper calls are shown as **comparison rows**.

## Benchmarks and controls (always on the same costs)
SPY buy-and-hold · 60/40 SPY/AGG monthly · T-bills (BIL) · BTC hold · **frozen twin** = the same fund with the 11/15 config,
never tuned (Fable: the control that tells us if the tuner helps) · raw "shadow" copy of every sleeve with no risk overlays
(used for the resume rule and to see what the overlays cost).

## Risk rules (engine, fixed - not tunable hourly)
- Sleeve drawdown (flow-adjusted index): -10% halves its size (restored above -5%); -15% pauses it to cash; resumes after >= 20 days AND its shadow copy makes a new 60-day high; -25% retires it.
- Fund drawdown: -12% halves everything (cleared above -8%); -20% halts to cash until the weekly review sets `fund_halt_reset`.
- Long-only, no leverage, no shorts, any one position <= 25% of the fund (by construction of the sleeves).

## Scoring / kill rules
Every sleeve is "unproven" until 126 trading days of live paper AND a 7-day block-bootstrap P(beats its benchmark) >= 0.80.
At 12 months, a sleeve with P < 0.50 is retired (engine) - its weight goes to the reserve. Retired sleeves come back only by a
weekly-review proposal. If the tuned fund has not beaten the frozen twin after 6 months, the tuner is switched off.

## Hourly judgement (bounded self-improvement)
`tuner.py` asks DeepSeek Flash for hold/change. The SCRIPT enforces: only `tunable` keys; clamp to bounds; <= 2 weight points
(vol targets 1 / 5 points) per key per 24 h; weight RAISES once per 7 days per sleeve (cuts any hour); weights <= 95%;
<= 3 changes an hour; <= 24 calls a day. Every call logged; every change goes to CHANGELOG.md with the reason.
Code is never changed hourly. Fable's weekly review may propose code changes in `proposals/`; Claude applies the ones that hold
up and re-runs backtest + twin first.

## Execution interface (for later)
`execution.py`: `Broker` interface, `PaperBroker` (the only one), `LiveBroker` that refuses on purpose. When a company
brokerage/exchange account is funded, a LiveBroker is written by an AI whose provider terms allow execution (Grok / DeepSeek /
Kimi), with size/stop limits read from the Control Room (Supabase `system_settings` via tools/settings.py). Claude and Codex
do not place real trades. Polymarket stays DOWN for money (P-0112); prediction-market prices are read as public signals only.

## The real goal metric: could it pay the subs (~$275-305/month)?
Shown on the dashboard every hour: return used (live once >= 60 days, else backtest), $/month at $100k, capital needed for
$275-305/month, the same at the team's honest 5-7%/yr, T-bills-only capital, max drawdown, 3x-cost return.
First numbers (11/15, backtest 2025-01-02 -> 2026-11-13, hindsight - not evidence): fund +7.9%/yr, max drawdown -6.7%
(SPY +15.3% / -18.7%, 60/40 +10.5% / -11.3%, BIL +3.7%, BTC -20.1% / -53%). At 7.9% that is ~$660/month on $100k, ~$42-46k
for the subs. Honest planning (Grok, Fable): $50-70k at 5-7%; T-bills alone ~$93k with almost no drawdown. **Under $10k
cannot pay the subs by trading.**

## Known gaps / next sleeves (parked, not dropped)
- Kimi: crypto funding/basis carry (needs perp data + shorts), oil-headline -> XLE lag (needs headline tagging), conditional turn-of-month.
- FRED macro inputs (claims, curve) once FRED answers from the MSI (or with a free FRED key).
- Taxes are not modeled (Grok: short-term tax matters a lot for small accounts).
- Bars are daily; hourly runs mark live prices but trade on daily closes.
- The backtest's rules were chosen by AIs who know 2025-26; only the live book is evidence (Fable, Qwen).

## Direction from Jaron (11/15 9:35 AM) - for the weekly review (Fable) to act on
- Purpose/timing: the fund is LONG-TERM, for surplus AFTER the company has revenue (monetizing, apps) and bills are paid. It is not the first money engine. Not his pick, a role.
- For the "set up systems for others" goal: people starting out don't have $50-70K to invest, so the team must keep finding OTHER money paths (services, products, apps); the fund is a later stage in that playbook.
- Universe breadth (method, not picks): crypto should not mean only the 4 big coins. Research utility tokens with real usage: which companies/places actually use a token, signed partnerships, on-chain activity, revenue/fees. No single "winner" (like AIs, each chain has its role). Stocks stay a main focus alongside crypto, kept as separate sleeves.
- Weekly review task: propose a broader, evidence-based universe (stocks + utility tokens) with the usage evidence for each, as a proposal file. No seeding from Jaron's own picks.
- Two more lenses for the weekly review (Jaron 11/15 9:40 AM, offered as observations to test, not rules; ignore if the evidence says he's wrong):
  1. FUTURE-THREAT check per asset: could quantum computing (encryption-breaking), AI, war or sanctions hurt this asset later? e.g. chains without a post-quantum migration plan; companies exposed to Taiwan chip supply. Score "threat exposure" separately from "good now."
  2. COMPETITION is not automatically a reason to reject (his "engine of division": Ford/Chevy, iPhone/Android, Nvidia/Intel - rival camps can both thrive because people pick sides). Model it as SHARED upside (the win may split, so lower expected peak) rather than "only one survives." Test it against history: in which categories did rivals coexist (cola, phones, cars) vs winner-take-most (search, social)?
