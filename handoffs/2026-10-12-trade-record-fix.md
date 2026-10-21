# Trade record fix (10/11-10/12) - Claude Code (Sonnet 5.5)

## Short version
The resolution rows were never missing from the database. The scripts that READ desk_trades were only seeing 1,000 of 1,851 rows,
so fills showed up with no resolution. Fixed the readers. Nothing placed, cancelled or changed on the venue.

## 1. Cause (verified)
- Supabase returns at most 1,000 rows per request, whatever `limit=` says. desk_trades now has 1,851 rows.
- `tools/publish-crew.py` money() and `tools/my-trades.py` asked for `limit=5000/10000` with no order and no paging. They got an
  arbitrary 1,000 (the newest upserted rows fell off the end: latest row seen 10/11 18:52Z). Reproduced: that read returns 2-3 fills
  and ZERO resolution rows for clmb-mrst, hou-kanst, boise-frest, sa-pho; full read has all of them.
- Ruled out: slug matching (all 19 resolutions in the venue's newest 100 events are in desk_trades with the right slug); the
  100-event window (no gap); batch timing; actor inheritance. I compared desk_trades with the venue's FULL history file
  `state/polymarket-activities-all.json` (1,854 events, from tools/pm-history-all.py): 0 fills, 0 resolutions, 0 deposits, 0
  withdrawals missing, and no DB fill that the venue doesn't have.
- `tools/grok-money.py` was NOT truncated (its actor filter returns 730 rows, under the cap). Its numbers change only because
  the DEN-LAC resolution landed 10/11 23:21Z.

## 2. Fix (one change: paginated reader)
- `tools/executor.py`: new `sb_all(env, path)` - pages 1,000 at a time ordered by (at, id) until a short page.
- Switched to it: `publish-crew.py` money(), `grok-money.py`, `my-trades.py`. Backups: `tools/*.bak-2026-10-12`
  (executor, grok-money, publish-crew, my-trades).
- Any NEW script reading desk_trades broadly must use `X.sb_all`, not `limit=`.
- Not done: publish-crew.py was not re-run, so the live crew page still shows the old truncated numbers until its next scheduled run.

## 3. Backfill
Nothing to backfill: all venue resolutions are already in desk_trades. Not recorded anywhere (verifier ignores these event types):
2 TRANSFER events ($2.47 on 10/6, $2.60 on 9/29, direction unclear) and 1 REFERRAL_BONUS ($25, 9/18). Left as is, no invented rows.
Cannot be recovered from the venue (listed, not guessed):
- Sells with NO recorded buy, in markets that never resolved: $36.64 of proceeds, so profit there is unknown:
  tec-mlb-alchamp-2026-09-27-tb $16.76, paccc-usse-midterms-2026-11-03-dem $7.66, aec-nfl-ari-nyg-2026-10-04 $6.47,
  tac-oscars-03-14-2027-bestpic-odysse $4.79, tec-mlb-champ-lad $0.71, two tiny others. The buys are not in the venue history at all.
- tec-mlb-champ-2026-09-27-mil: DB shows 4 shares ($1.96) with no resolution, the venue shows no such position. Unresolved; basis unclear.
- aliens (usgcc-aliens-12-31-2026) is genuinely open (32 sh, cost $2.81, value $2.24).

## 4. Per-bot settled profit, weeks of 9/28 and 10/5 (all actors, shared slug P&L split by buy spend, like publish-crew)
Before = what the 1,000-row read saw. After = full 1,851 rows.
| actor | 9/28 before | 9/28 after | 10/5 before | 10/5 after |
|---|---|---|---|---|
| Darios Twin (live-wire) | +30.95 | -33.47 | -3.26 | -3.68 |
| Satya Twin | +53.47 | +152.54 | -12.57 | -41.60 |
| Demis Twin | +0.68 | -32.45 | 0.00 | -2.56 |
| DeepSeek (direct+split) | -1.22 | -6.57 | 0.00 | +0.29 |
| jaron-manual | +30.05 | +16.70 | +16.21 | -116.75 |
| all actors | +113.79 | +96.31 | +0.37 | -163.55 |
Note the 9/28 live-wire/satya swing is partly actor labelling on shared markets (one bot opens, another closes); trust the total.
grok-money.py (all grok-bot actors combined), unchanged by the fix: week 9/28 +18.35, week 10/5 -53.92 (was -50.30 before the last
resolution). 10/6-10/11 all actors: -43.96 (satya -41.60, live-wire -3.60, Jaron/outside-queue about +1.25). So the bots did lose ~$45
since 10/6, and the 10/5 week's big hit is Jaron's own BTC 15-minute hand trades (-116.75), not a bot.

## 5. Whole-account reconciliation
- Money in: deposits $243.67 + referral bonus $25.00 - withdrawals $43.00 = $225.67 net (two transfers, +/-$5.07, direction unknown).
- Money now: cash $2.01 + aliens $2.24 = $4.25. So the account is down about $221 on net funding ($196 if the $25 bonus does not count).
- Recorded P&L, all actors: -$96.52 (resolved markets -$150.54, matches the venue's own realized exactly; sold-out markets that never
  resolved +$54.02, of which $36.64 has no cost basis, see section 3).
- Gap still unexplained: about $125 ($100 without the bonus). The resolved side is exact, so the gap sits in sold-out/never-resolved
  markets and pre-record positions, or in venue fees/credits that are not in the activity feed. I tried a cash-flow identity and it did
  not close ($579 off), which means the payout side of my arithmetic is wrong, not that cash is missing; the P&L identity above is the
  one to trust. Not closed - needs a look at the venue's statement/CSV export for the account.

## 6. Other bugs seen, not changed (one problem, one fix)
- verifier.py reconcile_trades picks "ours" = the AGGRESSOR execution when the order id isn't in a proposal. When our order was the
  resting (passive) one (`trade.isAggressor` false) that records the COUNTERPARTY'S side. 2 of 1,598 fills so far:
  D155Q7P2RZ6Y (coast-marsh, recorded as jaron-manual buy; really a bot's passive sell, ~$2.3) and CVBKD3Y14YHR (pit-cle, actor
  unknown, no action). Fix would be `ours = aggressorExecution if trade.isAggressor else passiveExecution`. Also makes the 4
  'mixed' resolutions (tenn-ark, coast-marsh, usc-pennst, minnst-pur, total about +4.35) drop out of actor-filtered grok-money.
- verifier fetches only the newest 100 events per pass; fine today (no gap), but a >100-event burst between passes would lose rows.
