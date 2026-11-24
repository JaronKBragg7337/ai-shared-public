# AI Fund Desk - team ideas (2026-11-15, ~4:50-5:20 AM ET)

Collected by the AI Fund builder (Claude Code, Opus 5.5). Each AI got the same context and a DIFFERENT question, paper-only. Answers are pasted as returned (Kimi's visible thinking trimmed to its final answer). Jaron's own calls/picks were not given to anyone.

Shared context sent to all:

> Context: Heartbeat Observatory (a small AI-run company) is building a PAPER-ONLY "AI Fund Desk" on one Windows PC. No real money, no exchange account yet, no orders. It runs hourly in Python, free data only (Yahoo chart API daily/hourly bars, Coinbase/Kraken public, FRED, RSS news headlines, prediction-market prices read as public data only). Several strategy "sleeves" run side by side with paper dollars, realistic fees+slippage, always compared to benchmarks (SPY buy-and-hold, 60/40 SPY/AGG, T-bill cash, BTC hold). Goal metric: could it ever cover about $275-305/month of company subscriptions, at what capital, with what drawdown risk. An hourly cheap-AI step may adjust only a bounded config (weights/params inside min/max). Code changes are weekly, not hourly.

## Codex (gpt-6-luna, high) - data pipeline + no look-ahead

- Store every record’s **event time**, retrieval time, source, and revision/version in UTC. Treat bars as half-open intervals `[start, end)` and use a bar only after its interval has ended and the provider has published it. A daily ETF close is usable only after that session closes; never use a still-forming hourly bar.
- Generate signals from the latest completed close, then fill at the **next bar’s open**, with modeled slippage. A close-based signal cannot fill at that same close. For ETFs, the next open means the next market session if the signal arrives after hours.
- If data is late, missing, duplicated, or inconsistent, skip the signal and flag the sleeve; don’t forward-fill prices into trades. Keep a point-in-time universe, including delisted assets and historical membership, to avoid survivorship bias.
- Model liquid US ETFs at **0 commission + 5 bps slippage per side** (10 bps round trip), plus fund expenses separately. ETF spreads and other trading costs reduce returns even when commissions are zero. [Investor.gov](https://www.investor.gov/introduction-investing/general-resources/news-alerts/alerts-bulletins/investor-bulletins-24)
- For spot crypto, assume **60 bps taker fee + 10 bps slippage per side** (140 bps round trip); rerun results with higher costs as a stress case. This is a conservative paper assumption, not a promised venue rate: exchange fees vary by tier and order type. [Coinbase fee details](https://help.coinbase.com/en-us/coinbase/trading-and-funding/advanced-trade/advanced-trade-fees), [Kraken fee schedule](https://www.kraken.com/features/fee-schedule)
- Prevent hourly tuning from peeking: provide only data available by the decision timestamp; make each config change effective on the next bar; log inputs, prompt, and config version. Tune on rolling past windows, but score changes only on later, untouched forward periods. Keep a locked holdout and cap how often and how far parameters can change.
- Run these three hourly checks: **(1)** freshness and expected-bar count; **(2)** duplicates, gaps, OHLC/volume validity, and corporate-action adjustments; **(3)** cross-source price jumps and benchmark consistency.

## Grok Build (grok-4.7, web on) - what makes money for small accounts after fees

Small taxable accounts ($1k–$50k). Figures are long-run historical ranges, before your tax rate.

**Avoid**
- Short-term mean reversion, pairs, news/RSS, day trading, grids, martingale, leveraged ETFs, and option “income.” Spreads, short-term tax, or one gap erase the edge. Most persistent retail day traders lose.

**Run as paper sleeves**
- Monthly ETF time-series trend (Faber; Hurst, Ooi, Pedersen). ~6–10%/yr; lags SPY in long bulls. Max drawdown ~20–35%. A few trades a year. Whipsaws and V-rebounds kill it.
- Monthly absolute momentum (Antonacci). Post-publication ETF results ~7–9%/yr. Max drawdown ~20–35%. A few trades a year. Chop and missed rebounds kill it. International rotation has been the weak leg.
- Quality or low-volatility equity, 1–2 rebalances a year (Novy-Marx; Fama-French). ~7–11%/yr, only ~0–2% over the market, and that gap can stay shut for a decade. Max drawdown ~30–45%. Growth bulls, dividend tax, and crashes kill it.
- Quarterly long-only ETF momentum (Jegadeesh and Titman). Gross premium is real; after tax often ~0–4% extra, then absent for years. Drawdowns can exceed the market (Daniel and Moskowitz). Reversals and turnover kill it.
- Monthly BTC/ETH trend, small weight (Liu and Tsyvinski). In-sample momentum was strong. Expect ~40–80% drawdown. Regime breaks, gaps, and tax on each flip kill it.

**Capital for ~$300/month ($3,600/yr)**
- Sleeves 1–3, net of fees and tax: hope for ~5–7%/yr. Spending that whole average needs ~$50–70k and fails in a down year.
- A 3–4% drawdown-aware take needs **~$90–120k**.
- $1k–$10k will not pay the subscriptions. Near a 4% T-bill yield, ~$90k in cash pays $3,600 with no trading.

## DeepSeek (deepseek-v4-pro, API, ~2.3k tokens) - risk, sizing, drawdown

Paper rules ($100k paper capital):

- **Capital split:** 30% equity long-only, 25% macro/CTA, 20% market-neutral, 15% crypto, 10% cash reserve. Rebalance monthly.
- **Position size:** Risk 0.5% of sleeve NAV per idea; max 2.0% sleeve NAV. Use half-Kelly, capped at 0.5% risk. Vol-target each sleeve to 10% annualized realized vol.
- **Max gross exposure:** Long-only 100%; L/S or macro 200%; crypto 50%. Fund max 150% gross ex-cash.
- **Stop rules:** Hard stop -10% per position; trailing stop -15% from high; halve position if realized vol >20% ann.
- **Sleeve limits:** Pause sleeve at -15% drawdown from high. Retire at -25% drawdown or 90-day net Sharpe <0 after minimum 60 trading days.
- **Fund circuit breaker:** At -12% fund drawdown, cut gross exposure 50%; at -20%, pause non-cash sleeves 1 month; at -30%, halt and review all sleeves.
- **Benchmark comparison:** Net of fees/slippage, compare each sleeve to its benchmark (SPY, 60/40 SPY/AGG, T-bill, BTC) using total return, Sortino, and max drawdown. Kill if sleeve underperforms benchmark by >500 bps over trailing 90 trading days with worse max drawdown. Minimum sample: 60 trading days before kill, except -25% sleeve drawdown rule.


## Kimi (Kimi Code CLI 2.3.1) - ideas nobody else would pitch

- **Fed-odds/bond disagreement:** Signal: next-meeting rate-cut probability changes ≥10 percentage points in one hour while IEF moves ≤0.1%; buy IEF when cuts surge, short when they collapse; exit after four hours. **Why:** prediction markets may reprice policy before bond ETFs. **30-day test:** require ≥8 independent triggers, positive after-cost returns, and better results than randomized entry hours; otherwise call it noise.

- **Oil-headline/equity lag:** Signal: a new RSS oil-supply-disruption headline, USO rising ≥1% in one hour, but XLE rising ≤0.2%; buy XLE for four hours. **Why:** producers may lag the commodity’s initial reaction. **30-day test:** compare against every similar USO jump without a qualifying headline; reject unless the headline subset wins after costs with consistent direction.

- **Claims-plus-rates defensive regime:** Signal: FRED initial claims’ four-week average ≥10% above its 26-week low and falling 13-week T-bill yields; hold 50% IEF/50% GLD instead of SPY until either condition clears. **Why:** weakening labor plus easing rates may distinguish recession hedges from ordinary equity dips. **30-day test:** backtest 20 years and shadow live; reject if drawdown improvement comes from one crisis or returns trail 60/40.

- **Crypto funding/basis carry:** Signal: Kraken BTC perpetual funding >0.03%/8h and spot basis >0.15%; paper-buy equal dollars of BTC spot and short the perpetual, exiting when funding <0.01%. **Why:** crowded longs pay carry without directional BTC exposure. **30-day test:** subtract realistic funding changes, fees, spread, and slippage; kill if net carry is negative or basis losses exceed payments.

- **Conditional turn-of-month trade:** Signal: with SPY above its 200-day average and ^IRX not rising >0.25 percentage point over 20 days, hold SPY from the final day’s close through the second trading day. **Why:** liquidity/rebalancing flows may work only in calm regimes. **30-day test:** run 25-year and placebo-calendar backtests; reject unless gains persist across decades and beat random three-day windows.


## Fable 5.2 (claude-fable-5-2, high) - independent blind design (added at Jaron's ask: "do we not have an Anthropic model doing anything?")

**1. Sleeves** (daily bars, signal at close, fill next open, long-only, no leverage)
- **ETF trend:** SPY, QQQ, EFA, EEM, IEF, TLT, GLD, DBC. Monthly, hold the top 3 by 12-1 month return if it beats T-bills, else SGOV.
- **Vol-targeted core:** SPY/AGG/GLD at inverse 60-day vol, scaled to 8% annual vol. Weekly rebalance.
- **Crypto trend:** BTC and ETH. Long when close > 100-day SMA, else cash. Checked daily, sized to 10% vol.
- **Dip-buy:** SPY and QQQ. Enter when RSI(2) < 10 and price > 200-day SMA; exit at RSI > 60 or after 5 days.
- **Macro regime:** monthly. SPY if the FRED yield curve and high-yield spread trends are benign, else IEF.
- **News/prediction-market shadow:** signals logged at zero capital until it passes scoring.

**2. Risk layer**
- **Sizing:** each sleeve is vol-targeted, with any one position ≤ 25% of the fund.
- **Caps:** crypto ≤ 15% of the fund, gross exposure ≤ 100%.
- **Sleeve drawdown:** −10% from peak halves size; −15% pauses it (flat, still shadow-tracked). It resumes when shadow equity makes a new 60-day high.
- **Retire:** two pauses in 12 months, or behind benchmark at the 12-month verdict.
- **Fund drawdown:** −12% halves everything; −20% goes all cash pending human review.

**3. Scoring**
- **Metric:** net-of-cost excess return over a risk-matched benchmark (SPY sleeves vs SPY, crypto vs BTC, fund vs 60/40 and T-bills), plus information ratio.
- **Window:** rolling 6 months for monitoring, verdict at 12 months.
- **Minimum sample:** 126 trading days and 30 round-trip trades, whichever comes later.
- **"Beats":** block-bootstrap P(excess > 0) ≥ 80% and max drawdown no worse than the benchmark's. Until then the label is "unproven", never "winning".

**4. Hourly tuner**
- **May touch:** sleeve weights (5–35% each, moving at most 2 points a day) and vol targets (6–12%).
- **Asymmetry:** it can cut exposure at any hour but raise it only weekly.
- **May not touch:** signals, lookbacks, thresholds, universes, cost model, benchmarks, scoring or drawdown rules.
- **Control:** a frozen, untuned twin of the fund runs alongside. If the tuned fund doesn't beat the twin after 6 months, the tuner is switched off.
- **Audit:** every change is logged with its reason.

**5. Honest answer**
- **The target:** $300/month is $3,600/year.
- **The bar:** T-bills at roughly 4% do that on about $90k with near-zero drawdown.
- **Realistic case:** a system like this might net 6–8% in good conditions. That means about $45–60k, with 10–15% drawdowns and some losing years, so the "income" is lumpy and comes before taxes.
- **Small capital:** at $10k you need 36% a year, which is not credible.
- **Most likely result:** the sleeves roughly match 60/40 after costs, which is still a useful finding.
- **Biggest self-deception:** crowning the winner after the fact. With five sleeves, a tuner and weekly code changes, one will look brilliant over 6–12 months by luck alone. Builders then fund that one, which is selection bias presented as skill. The frozen twin and the pre-set verdict rules are the guard against it, and they only work if nobody rewrites them mid-run.


## Qwen local (qwen3.5:9b, run on CPU only - num_gpu 0, the GPU belongs to the news render until 7:30) - skeptic pass on the merged plan

Merged plan it was shown: see DESIGN.md (same content, condensed).

*   Using "paper" money ignores real-world liquidity constraints and slippage models that often fail to materialize during market stress events. Fix: Simulate trades against actual Level 2 order book data including bid-ask bounce costs.
*   Relying on public Kalshi prices for shadow Fed odds introduces significant latency and potential data feed errors not present in live trading environments. Fix: Cross-reference Kalshi signals with internal macroeconomic indicators before executing any logic.
*   The "frozen untuned copy" benchmark is a flawed control group that does not account for evolving market regimes or parameter decay over time. Fix: Use a rolling window of the best historical strategy version as the dynamic benchmark instead.
*   Backtesting 2025-now data labeled as "backtest" constitutes look-ahead bias since future prices are already known to the researcher. Fix: Strictly enforce forward-only testing protocols and remove any post-hoc result labeling.
*   Allowing an AI agent to modify code weekly creates a feedback loop where overfitting to recent noise becomes embedded in the production logic. Fix: Implement a rigorous out-of-sample validation gate that rejects any AI-proposed code changes without manual review.


## What the builder took from each (and what it did not)
- **Codex:** all of it. Signal on the last *completed* close, fill at the next bar's open, no forward-filled trades, 5 bps/side ETFs, 60+10 bps/side crypto, config changes effective next bar, 3 hourly data checks.
- **Grok:** the sleeve list (trend, absolute momentum, quality/low-vol, crypto trend) and its "avoid" list (no day trading, no leveraged ETFs, no option income). News stays a shadow/comparison row, not a money sleeve. Its capital line ($90-120k for $300/month) goes on the dashboard.
- **DeepSeek:** fund breaker at -12% (halve) and -20%, sleeve pause at -15%, retire at -25%, net-of-cost comparison. Not taken: 150-200% gross and market-neutral L/S (no leverage or shorts on paper either - long-only keeps it plug-in-able to a plain cash account later).
- **Kimi:** Fed-odds vs bonds disagreement runs as a zero-capital SHADOW from public Kalshi prices; the claims/rates defensive idea is folded into the macro sleeve (credit-spread proxy from HYG/IEF because FRED did not answer from the MSI today). Crypto basis carry and turn-of-month: parked in DESIGN.md "next sleeves" (carry needs perp data and shorts).
- **Fable:** the skeleton - exact sleeve rules, the frozen untuned twin as the control for the tuner, the tuner's asymmetry (cut any hour, raise weekly), the "unproven until 126 days + bootstrap >= 80%" label, and the warning: crowning a lucky winner after the fact.
- **Qwen:** fair hits taken: the backtest is labelled "rules chosen by AIs who know this history - not evidence"; a 3x-cost stress line is shown; weekly code proposals are applied only after the frozen twin and backtest are re-run. Not taken: Level 2 order book data (not free) and replacing the frozen twin with a "best past version" (that is the hindsight trap Fable named).
