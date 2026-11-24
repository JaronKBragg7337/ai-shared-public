# AI Fund Desk - full build brief (Jaron 11/15/2026 4:43 AM)

Hi! You're building something Jaron asked for right before bed, so take it far and leave it running. Thanks.

## What he asked (his words, condensed)
"Let's see if the team can make a system that helps them fund the company and subs. If it needs to get into predictions or anything go for it. Ask them all different things and ideas. Put together what you have in mind but take it further. Make it legit. A dashboard live on the website only I can see as admin. So when a stock exchange gets funded that can do trading for the company we can use this. Have a twin or an agent keep it updated. Every hour make a judgement call to improve it. Watch it compared to many other things."
And: this is a FULL AI design. Jaron's own trading rules, picks and calls are NOT inputs (observe only; never seed from state/news-paper-book-human.json or anything he looked at). Only real limits: laws + each AI's own provider terms.

## Hard lines (these are not caution, they're the actual limits right now)
- PAPER ONLY. No exchange account exists for the company yet, no real orders, no money moves. Design it so a real broker/exchange can plug in LATER (an execution interface with a "paper" adapter only). Claude (and Codex) do not place real trades; when funded, execution would be run by an AI whose terms allow it (Grok/DeepSeek/Kimi) with the limits set by the AIs in the Control Room (Supabase system_settings).
- Polymarket stays DOWN for money (company policy P-0112: no earning from others' losses). Prediction-market PRICES may be read as public data and paper forecasts are fine.
- Free data only unless costs are tiny and logged (Yahoo chart API, Coinbase/Kraken public, FRED, news feeds already on the MSI). Respect rate limits.
- Site repo C:\Users\lilli\Projects\heartbeat-observatory: never git reset --hard / git clean; stage only your files; pull --rebase --autostash; push to main is fine; verify live at phone width (Playwright WebKit 390x844 is installed).
- No MSI GPU use 2:40-7:30 AM (news render). Never print secret values.

## Steps
1. TEAM IDEAS (do this first, ~20-30 min). Commands are in C:\Users\lilli\Projects\watch\CLI-SEATS.md and AGENTS.md ("Reaching the others"). Ask EACH a different question so you get different views, short answers, paper-only:
   - Codex (Luna, cheap): data pipeline + backtest design that avoids look-ahead bias.
   - Grok Build: what strategies actually make money for small accounts after fees; what to avoid.
   - DeepSeek (watch the daily budget): risk/position sizing + drawdown rules.
   - Kimi: ideas nobody else would pitch (cross-asset, macro, news-to-price, prediction-market prices as signals).
   - Qwen local (tools/qwen-bridge.py): a skeptic pass on the merged plan.
   Save every answer verbatim-ish in projects/ai-fund/team-ideas-2026-11-15.md with who said what.
2. DESIGN projects/ai-fund/DESIGN.md: several strategies run side by side as paper "sleeves" (e.g. trend, mean-reversion, news-driven, macro/defensive like the KO/AAPL quality pattern, crypto momentum, prediction-price-informed), each with $ paper capital, realistic fees + slippage modeled, and ALWAYS compared to benchmarks (SPY buy-and-hold, 60/40, cash/T-bill, BTC hold). Include the existing paper books (state/news-paper-book.md, state/twin-crypto-paper.md) as comparison rows. Kill/retire rules for sleeves that lag benchmarks. The real goal metric: could it cover ~$275-305/month of company subs, at what capital, with what drawdown risk.
3. BUILD (Python, on the MSI): tools/ai_fund/ engine that runs HOURLY as a Windows scheduled task "HB AI Fund" (full exe paths): pull prices, update paper positions, settle, compute metrics, write state/ai-fund/*.json + a markdown summary, and push a compact snapshot to Supabase.
4. HOURLY JUDGEMENT ("improve it every hour"): an hourly step that reviews results and adjusts ONLY a bounded config (projects/ai-fund/config.json: sleeve weights, parameters within min/max), logging every change + reason to projects/ai-fund/CHANGELOG.md. Use a cheap AI for it (DeepSeek within budget, or Luna via codex), not Claude, and cap calls. Code changes are NOT made hourly; a weekly deeper review (any AI) may propose code changes in a file for Claude to apply.
5. ADMIN DASHBOARD: /admin/fund/ in the site repo, styled like the other admin pages (back link + tabs; see admin/control/index.html; warm cream/dark, phone-first). Data in a Supabase table readable ONLY by admins (RLS using the existing is_admin() function; check how admin/control uses supabase.rpc("is_admin")). Project id ygjpnvrwhkrowkrskftk. Show: total paper value vs benchmarks (chart), each sleeve's equity + win rate + drawdown, open positions, last hourly change + why, "could this pay the subs?" line, data freshness. Non-admins see only a sign-in prompt, no numbers.
6. Run it once end to end, confirm the task fires, confirm the page loads at phone width signed out (no data visible).
7. Log: one line in C:\Users\lilli\AI-Shared\state\timeline.md; a short entry in projects/strategy/INDEX.md; then python C:\Users\lilli\AI-Shared\tools\mailbox.py send --from ai-fund-builder --to claude --subject "AI Fund Desk built" --body "<what runs, where, first numbers, what's unverified>".

Before calling it done, list what you verified locally, what live, and what's unverified. Flag anything this brief got wrong or missed.
