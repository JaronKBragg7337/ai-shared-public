# 2026-09-24 — Claude (cloud): trading page rebuilt around Live Wire (after Q-023)

Route: Claude Code cloud session; AI-Shared and live checks through the Heartbeat MAI connector. Pushed straight to main.

## Shipped (heartbeat-observatory, main)
| Commit | What |
|---|---|
| 04cefd5 | /live-systems/trades: Decide tab, Awaiting you / Verified / Approved / Placed counts, "Queue trades need your yes" line and the pending panel removed. Account, Ledger, History kept. Old #decide links open Account. No other wording changed. |
| dc09b50 | New page /live-systems/trades/decisions/ ("How the traders decide"), linked from the trade desk nav ("How it decides"). |
| 6ce42a1 | Decisions page: GitHub file reads retry 3x; a failed read says "could not load" + Try again, never "no capture". |

## The decisions page
- Trades: every trade_proposals row with proposed_by like grok-bot/% (42 today): market, side, price, size, the bot's reason (its "[grok-bot/..., live, no approval]" tag stripped), kill criterion, and result. Result = desk_trades resolution pnl by slug (won/lost, for the whole market) / "closed early" when a later EXIT row exists on the slug / "exit order" for EXIT rows / "not settled".
- News it had: each trade links to its day (America/Indiana/Indianapolis) in the News tab: organizer's brief (latest on or before the day, labelled if older), market-feed packets (and a highlight on the trade card when a packet names that market), Codex / DeepSeek / Claude captures with the 21 domains as collapsible sections. Read live from github.com/JaronKBragg7337/watch (branch master): one git-tree call for the listing (cached 10 min per tab; falls back to probing raw files if GitHub's 60/hour limit is hit), files from raw.githubusercontent.com. Today + last 10 capture days. No database change, no SQL.
- Second trader (Kraken): add one entry to TRADERS at the top of the page script (id, name, venue, proposedBy regex, actor, reads). Any grok-bot/* trader not listed still shows under its own name, with its own card and filter chip (tested with a fake second trader). If the Kraken lane writes rows under a different prefix than grok-bot/, widen the query in loadTrades (one line).

## Verification
- Local (cloud, Chromium, real repo files + real rows): iPhone 390, Android 412, desktop 1280 - trades, results, news days, captures, market feed on 09-18, forced-failure path; no sideways scroll, no errors.
- Live (MSI, www.heartbeatobservatory.com): iPhone WebKit, Android Chromium, desktop Chromium - trade desk tabs Account/Ledger/History, queue text gone, link present; decisions page 42 cards (8 won, 7 lost, 1 closed early, 11 exit orders, 15 not settled), brief + Codex + DeepSeek captures load, sw = viewport width, no page errors. First iPhone run showed file reads failing (fixed in 6ce42a1, re-verified).
- Not verified: a real second trader (none exists yet).

## For Jaron to look at (his words, not changed)
- Trade desk hero still says "Owner decision required", the lede still describes approving from the phone, and the footer says "Approval is the owner's alone ... only the owner can decide from it". Those describe the retired queue.
- Live Wire's reason on proposal #565 contains a piece of a laptop file path ("C:\Users\lilli") - the bot's own text, already public on the History tab.
- The organizer's brief and market feed have only 09-18 files; the page shows that honestly.
