# Polymarket money reconciliation — 2026-10-04

## What the records say

The local hand-trade report is reproducible: `my-trades.py` reads 532 fills and 52 settlements tagged `jaron-manual` and calculates **+$70.52** (+$221.60 realized on sales and -$151.07 on settlements). The system separately tags 49 fills and 10 settlements as `jaron-manual (demo)`, totaling **-$29.04**. Counting both tagged human lanes gives **+$41.48**. This is the recorded human result, not a complete proof of the account's result from Jaron's first deposit: the venue history interface is capped at its latest 100 activity items and does not accept a continuation cursor.

The local cash ledger contains **$243.67 deposits** and **$42.00 withdrawals**, for **$201.67 net cash in**. The deposits are $10.00, $35.00, $100.00, $13.00, $20.00, $38.98, and $26.69. The three withdrawals are $22.00, $10.00, and $10.00. The first recorded deposit is 2026-09-10; records therefore do not support a single $160 deposit as the full history. The extra $83.67 of recorded deposits versus the recalled $160 is not explained by the available venue activity page.

| Actor / lane in local ledger | Recorded P&L |
|---|---:|
| Human app trades (`jaron-manual`) | +$70.52 |
| Human demo trades (`jaron-manual (demo)`) | -$29.04 |
| **Human total, both lanes** | **+$41.48** |
| Grok bot / Live Wire lane | +$205.11 |
| Grok bot / Satya Twin | +$88.47 |
| Grok bot / Demis Twin | -$33.93 |
| DeepSeek direct | +$1.15 |
| DeepSeek split | $0.00 |
| **Named bot total** | **+$260.80** |
| `ai-outside-queue` (automatic orders with no bot trail) | +$43.87 |
| `system` (proposal/executor lane) | -$4.17 |
| `unknown` | $0.00 |
| `mixed` settlements that could not be assigned to one actor | -$3.10 |

P&L here is the local fill and settlement ledger's average-cost calculation, not a fresh recomputation from every venue fill. The reported AI figure of **+$223.60** is not reproduced by the current actor ledger. In particular, `grok-money.py` reports +$229.20 for its Grok actor grouping, while the same actor's current stored rows recalculate to +$205.11. The difference is **$24.09** and cannot be closed from the available feed. Adding every known bot row gives +$260.80; adding unattributed automatic activity and system/mixed rows changes the all-AI/system grouping further. The older +$223.60 number therefore cannot safely be treated as the full AI result.

## Fees and account check

Fill notes record **$112.11 net fees** across the actor lanes above (positive amounts are charges; negative amounts are rebates). Fees are already folded into local fill costs/proceeds used for P&L, so do not subtract them a second time.

The latest saved account snapshot (2026-10-04 17:52 UTC) is **$178.04 cash + $11.85 marked open positions = $189.89 account value**. Compared with local net deposits of $201.67, that implies **-$11.78** account-wide change in value. This snapshot is newer/different from the figures Jaron quoted (**$221.45 account value and +$186.10 P&L**) and does not verify them. The local actor P&L rows listed above sum to **+$338.88**, which is **$350.66 above** the snapshot-implied -$11.78. The activity window, mixed settlement attribution, cash/bonus treatment, and stale or inconsistent stored rows prevent that large difference from being reconciled. Current account balances also show a $25 bonus reservation, so displayed cash and spendable cash need not match.

## Gaps left open

- The Polymarket activity tool returns a maximum of 100 newest items; it exposes a `nextCursor` but its accepted inputs include only `limit`. Repeating the call returns the same page. I could not inspect transactions earlier than that window or independently verify the earliest fills, deposits, and settlements.
- The local ledger starts 2026-09-10, with the first deposit $10.00 and the first hand fill 2026-09-11. It predates the desk setup only by the records present locally; it does not prove no earlier fills are absent. The claimed early fall from roughly $160 to $60 cannot be measured from these records.
- Recorded deposits exceed the recalled $160 by $83.67; no corresponding complete activity history was available to determine whether these were additional deposits, credits, or other adjustments.
- The +$223.60 AI total cannot be matched to the present database rows. `grok-money.py` and its actor rows differ by $24.09, and no older venue page was accessible to locate the source.
- Four `mixed` settlements total -$3.10 and cannot be assigned to a single trader. One automatic fill is `unknown` (+$0.00 calculated P&L); `ai-outside-queue` totals +$43.87 but has no bot identity trail.
- Account app figures quoted (+$186.10 P&L on $221.45 value) differ from the latest stored snapshot ($189.89 value), so the quoted account P&L cannot be verified against a same-time balance and complete deposit history.

Only the requested report and timeline were written. No orders were placed, canceled, or changed.

## Full history (Claude, 10/4 5 PM) - tools/pm-history-all.py paged ALL 1,380 events (9/10 to now) -> state/polymarket-activities-all.json
Source = Polymarket's own manualOrderIndicator per order (MANUAL = Jaron in the app, AUTOMATIC = bots via API).
P&L = Polymarket's own "realized" per settled market (fees included); 6 markets both traded are split by shares.
- Human (app) trades: **-$179.06** over 68 settled markets
- AI (API) trades: **+$180.34** over 144 settled markets
- Money in: deposits $243.67 (7), referral bonus $25, transfer $2.60; out: withdrawals $42.00 (3)
- Check: in $271.27 - out $42 = $229.27; account now $221.45 -> whole-account result about -$8 (= human loss eaten by AI gain, plus open/unsettled)
- The Crew page's "AI profit settled $223.60" is higher than Polymarket's own +$180.34 - likely fees/realized method; to fix on the page.
