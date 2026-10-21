# The activity ledger reconciles to $68.80; the chart overstates it by $53.2874

The supplied records account for the entire latest **$68.80 cash balance**, starting from zero. There is no unexplained $17 debit in this export. The publisher's resolution-based account calculation gives **$122.0874**, or **$53.2874 too high** before any additional rounding from splitting events among bots. Its basic mistake is treating selected position-resolution P&L snapshots as a complete account ledger, while claiming that those values include fees.

The earlier app readings cannot all be reproduced as contemporaneous portfolio totals from the supplied event dates. That is a separate historical-data conflict, described below. Matching today's balance does not establish that those earlier app chart points are current, correctly dated, or measuring the same thing.

Only REPORT.md was created. No publisher execution, network connection, account action, trade, contact, or source-file edit was performed.

## Where every dollar goes

| Account component | Exact USD |
|---|---:|
| Deposits, including the $75 advanced pending deposit | +318.6700 |
| Promotion/deposit bonus (API type REFERRAL_BONUS) | +25.0000 |
| Two TRANSFER credits | +5.0700 |
| Completed withdrawals | -44.5000 |
| **Net funding** | **+304.2400** |
| Fill cash movements, including net commissions and changes in short collateral | -1945.8668 |
| Position-resolution cash payouts | +1710.4268 |
| **Net trading cash** | **-235.4400** |
| **Final cash** | **68.8000** |

The $235.44 net trading cash loss consists of **$76.82 before commissions plus $158.62 net commissions**. Net commissions are $164.97 charges less $6.35 maker rebates. These are cash figures; the remaining 0.01 share still has a small asset value.

Here is the exact bridge from the existing publisher to the real cash balance. The fee adjustment is only for markets with resolution records; fees on the other markets are already in their separately added net result.

| Correction to current publisher | USD | Balance after correction |
|---|---:|---:|
| Existing accounting, reconstructed with one rounded AI event per market | | 122.0874 |
| Include omitted bonus and transfers | +30.0700 | 152.1574 |
| Subtract actual fill commissions on the 262 markets with resolution records | -88.5700 | 63.5874 |
| Replace resolution P&L snapshots with complete pre-fee cash results on those markets | -4.5146 | 59.0728 |
| Include net fill cash on 141 markets without resolution records | +9.7272 | **68.8000** |

Thus the publisher overstates trading cash performance by $83.3574 and understates funding by $30.07. The net overstatement is $53.2874. Subtracting every fee from its existing resolution-only total would also be wrong: it omits both gains and losses from markets closed through fills.

## Funding records and their dates

Dates in this report are UTC unless explicitly marked EDT (America/Indianapolis, UTC-4 on these dates). Balance changes use createTime; later updateTime often reflects processing completion, rather than when money first became available. Deposits with advances are counted once, not again through their nested transactions.

| Created UTC | Type | Transaction ID | Cash USD | Status / evidence |
| 2026-09-10T20:58:40 | ACCOUNT_DEPOSIT | `CDM4F1MG000Q` | +10.00 | COMPLETED |
| 2026-09-11T04:48:29 | ACCOUNT_DEPOSIT | `CDQZ3QTG000Q` | +35.00 | COMPLETED |
| 2026-09-11T06:28:55 | ACCOUNT_DEPOSIT | `CDR9GGHG000Q` | +100.00 | COMPLETED |
| 2026-09-11T14:04:46 | ACCOUNT_DEPOSIT | `CDRWXPFG000Q` | +13.00 | COMPLETED |
| 2026-09-12T00:59:38 | ACCOUNT_DEPOSIT | `CEAN5FEG000Q` | +38.98 | COMPLETED |
| 2026-09-12T01:00:23 | ACCOUNT_DEPOSIT | `CEAP2R4G000Q` | +20.00 | COMPLETED |
| 2026-09-18T01:16:31 | ACCOUNT_DEPOSIT | `CJ85YZDG000Q` | +26.69 | COMPLETED |
| 2026-09-18T01:16:42 | REFERRAL_BONUS | `CJ8605YG000Q` | +25.00 | COMPLETED; PROMOTION_DEPOSIT_BONUS |
| 2026-09-27T23:07:43 | ACCOUNT_WITHDRAWAL | `CRJCHX37000Y` | -22.00 | COMPLETED |
| 2026-09-28T20:28:25 | ACCOUNT_WITHDRAWAL | `CS66SJC9M00Y` | -10.00 | COMPLETED |
| 2026-09-29T06:04:46 | TRANSFER | `CSAC9NZJM00Y` | +2.60 | COMPLETED; transfer reason unspecified; credit interpretation |
| 2026-09-29T15:24:26 | ACCOUNT_WITHDRAWAL | `CSBKFJE6P00Y` | -10.00 | COMPLETED |
| 2026-10-06T15:34:51 | TRANSFER | `CXX9F1Z1G010` | +2.47 | COMPLETED; transfer reason unspecified; credit interpretation |
| 2026-10-09T17:22:28 | ACCOUNT_WITHDRAWAL | `CZVW5F0D6010` | -1.00 | COMPLETED |
| 2026-10-14T21:03:01 | ACCOUNT_WITHDRAWAL | `D35GX2Q30010` | -1.50 | COMPLETED |
| 2026-10-15T18:31:53 | ACCOUNT_DEPOSIT | `D43B43EWW010` | +75.00 | PENDING; nested advancedAmount = 75 USD |

The Oct 15 deposit `D43B43EWW010` explicitly contains `transactions[0].advancedAmount.value = "75"`. It is therefore supported as an advance despite its PENDING status. Without it the ending balance would be **-$6.20**. There is no separate deposit/card fee field or fee transaction in this export; the advanced amount equals the stated deposit. A charge outside this Polymarket account cannot be determined from this file.

Bonus `CJ8605YG000Q` was created Sep 18 01:16:42.376632056Z and updated Oct 14 22:02:47.009627701Z. The metadata calls it a promotion deposit bonus. The update is not evidence of a second $25 payment on Oct 14. Crediting it only at updateTime would lower earlier balances by $25 and still fail the known historical points. The exact second of original bonus availability is not separately recorded.

Transfers `CSAC9NZJM00Y` (+$2.60, Sep 29) and `CXX9F1Z1G010` (+$2.47, Oct 6) have no fee description, direction field, or meaningful transfer reason. Treating their positive amounts as credits gives the exact final reconciliation. Their underlying purpose cannot be established; calling them withdrawals or fees would be unsupported. Counting them as debits would lower the ending result by $10.14.

## Running cash versus the app's known points

**Cash and portfolio total are different while positions are open.** This file supplies fills and settlement snapshots, not historical market marks. The cash ledger below is reconstructible; an exact historical portfolio-total chart is not. No value was invented for open positions. Pending-order cash reservations are also not exported here.

| App point from TASK.txt | Ledger time used | Reconstructed cash USD | App USD | Assessment |
|---|---|---:|---:|---|
| Oct 8, time unspecified | Entire local Oct 8 | 49.23105 | 26.17 | Cash alone is $23.06105 above the reported portfolio total; cannot reconcile as the same dated measure. No events occurred that day. |
| Oct 9, time unspecified | Local day 00:00 to 23:59 EDT | 49.23105 at start; 0.20290 at end | 24.58 | Fills occur during the day; time and historical position marks are required. The cash range is $0.20290-$49.23105, not an exact match to a dated portfolio point. |
| Oct 16, about 02:00 EDT | 2026-10-16 06:00Z | 70.12330 | ~14.34 | Cash alone is ~$55.78330 above the reported total; only 0.01 share remains. Cannot reconcile. |
| Oct 18, 03:25 EDT, possibly stale 1D point | 2026-10-18 07:25Z | 68.80000 | 12.66 | $56.14 difference; no subsequent activity in the export changes cash. This point is inconsistent with the current total. |
| Oct 18, 21:42 EDT, current app balance | 2026-10-19 01:42Z; latest ledger event 2026-10-18 05:50:59Z | **68.80000** | **68.80** | **Exact cash match; 0.01 share of dust explains approximately zero open trades.** |

If the Oct 16 02:00 point was intended as UTC, reconstructed cash is $55.74955, with two football positions still open; that interpretation also fails $14.34. If Oct 18 03:25 was UTC, cash is $61.55, with football positions still open; it also fails $12.66. A timezone conversion alone does not solve these conflicts.

As a sensitivity check, delaying the $25 bonus until Oct 14 would make Oct 8 cash $24.23105, still $1.93895 below $26.17 before considering the open position. It does not establish an alternative reconciled history. Under the main ledger convention, all event-by-event cash balances are nonnegative; the minimum is $0.00375 on Sep 15 16:24:05.997984721Z (trade `CGTW192MYVAY`).

The correct conclusion is that the **latest dollars reconcile exactly, while these historical app points remain incompatible or insufficiently specified**. The supplied files cannot prove whether the problem is stale app sampling, a different chart measure, different historical credit timing, or another historical reporting issue. Do not add an artificial balancing transaction or shift the $75 to force those points to match.

## What changed from Oct 14 onward

Using 2026-10-14 00:00Z as the boundary:

```
Opening reconstructed cash          2.0117
Oct 15 deposit advance             75.0000
Oct 14 withdrawal                  -1.5000
Trading cash change                -6.7117
Ending cash                        68.8000
```

After the deposit itself, cash starts at $75.9809 and falls by $7.1809 to $68.80. The publisher's reconstructed per-market event series rises from $50.1321 to $122.0874 over the Oct 14 onward interval, a $71.9553 rise; the actual cash rise is $66.7883. **Its additional error over that interval is $5.1670**, not approximately $17.

That $5.1670 is explained by $1.59 of commissions on recently resolved markets plus $3.5770 of omitted net cash movements on markets without resolutions. Four-decimal event rounding cancels in this interval:

| Market / action | UTC date | Fill IDs (resolution absent) | Omitted net cash USD |
|---|---|---|---:|
| Aliens position closed; only the closing cash is inside this interval | Oct 14 | `D3JXSZK8MZ6Y` | +1.1900 |
| BTC 20:45 market closed through trades | Oct 14 | JSON records 97-103, inclusive, in the supplied array | +0.9828 |
| Miami-Orlando closed through trades | Oct 17 | `D501DHNG0ZRP`, `D50RHSYG8ZRM` | -3.2960 |
| Pittsburgh-Boston College closed through trades | Oct 17 | `D5EG9ZYGAZRQ`, `D5FJ40B0AZRM` | -2.6225 |
| Auburn-Georgia closed through trades | Oct 17 | `D5JWNCSH2ZRM`, `D5JWNE6GGZRQ`, `D5KN7FC02ZRP` | +0.1692 |
| Bought 0.01 share of Miami MLS dust | Oct 15 | `D3T8YR794Z6Y` | -0.0005 |
| **Sum** | | | **-3.5770** |

Record indices are zero-based; where a resolution lacks its own ID, its market slug plus updateTime identifies it. The BTC row's full slug is `cpc-btc-updown-15m-2026-10-14-2045z`.

Recent losing markets include East Carolina-UAB (-$10.09735), Cincinnati-West Virginia (-$11.16315), and Fresno State-San Diego State (-$5.11405); other markets produced gains. These are ordinary fill costs and payouts already included in the $6.7117 net interval loss, not an additional unexplained debit. No record supports charging another $17.

## Why resolutions, fees and fills cannot be summed the old way

The export contains 1,987 top-level records: 1,709 trades, 262 resolutions, 8 deposits, 5 withdrawals, 2 transfers and 1 bonus. Trade IDs are unique; resolution (marketSlug, side) pairs and resolution market slugs are unique. There is no duplicate-resolution explanation for the $53.2874 gap.

Of 403 traded markets, 262 have a resolution record. The remaining 141 consist of **140 flat markets and one 0.01-share position**. They are not 141 missing settlement payments: positions closed through trades need no resolution entry. Their aggregate net cash is +$9.7272, including the open dust position's lifetime cash movements. Examples include the omitted Miami-Orlando and Pittsburgh-Boston College losses above.

The 262 resolved markets generated -$245.1672 net cash, comprising -$156.5972 before fill commissions and -$88.57 commissions. Their afterPosition.realized fields sum to only -$152.0826. The latter are accounting snapshots, not a fee-inclusive cash total.

A clear example is Cincinnati-West Virginia: afterPosition.realized = -$10.8632, while the actual purchase debits are $10.16325 and $0.9999, totaling **-$11.16315**, with $0.30 commissions. Fresno State similarly reports realized -$4.9540, while fill `D5Q5VTFGEZRN` (JSON record 4) debits $5.11405 including its $0.16 execution commission. Resolution is record 0, slug `aec-cfb-frest-sdst-2026-10-17`, at Oct 18 05:50:59.120079147Z.

The $4.5146 additional pre-fee discrepancy is concentrated in these snapshots. It is not an invented fee. It is the directly measured difference between a market's complete fill/payout cash result before fees and its final reported realized field:

| Resolution market slug | Resolution UTC / array index | Complete pre-fee result minus afterPosition.realized USD |
| `aec-nfl-dal-hou-2026-10-04` | 2026-10-04T20:19:29.060799020Z / 609 | -3.64077500 |
| `aec-nfl-ind-was-2026-10-04` | 2026-10-04T16:45:04.706037961Z / 639 | +2.45002500 |
| `aec-kbo-ndc-hea-2026-09-25` | 2026-09-25T12:14:42.607500051Z / 1393 | -1.99920000 |
| `aec-nfl-det-car-2026-10-04` | 2026-10-05T03:45:33.514362726Z / 542 | -1.09200000 |
| `rdc-usfed-fomc-2026-09-16-nochng` | 2026-09-16T18:18:44.433338946Z / 1561 | -0.99960000 |
| `aimc-gemini-3pt5pro-2026-09-30` | 2026-10-01T14:27:35.248896728Z / 1002 | +0.70650000 |
| `aec-cfb-ala-mspst-2026-10-03` | 2026-10-03T19:37:02.674186278Z / 756 | +0.54390000 |
| `aec-nfl-mia-min-2026-10-04` | 2026-10-04T23:06:29.314453372Z / 597 | -0.36680000 |
| `aec-ufc-marmcg-bensop-2026-10-03` | 2026-10-01T17:30:15.627036047Z / 1001 | -0.16400000 |
| `aec-nfl-den-sf-2026-10-04` | 2026-10-04T23:41:33.775253573Z / 596 | +0.04760000 |
| Other markets: rounding below $0.0001 each | | -0.00025000 |
| **Total** | | **-4.51460000** |

For example, neutral UFC resolution `aec-ufc-marmcg-bensop-2026-10-03` has realized zero but pays **$1.8368**, against **$2.0508** of actual fill debits (fills `CR97RDR9YYAJ`, `CR97RDRA4YAJ`, Sep 27 06:07:04Z). Its net cash result is **-$0.2140**. Treating every resolution as a binary $0/$1 payout would miss that $1.8368 and end at $66.9632. Its stored beforePosition.cost ($2.0555) also differs from the actual fill debit sum; it is not a substitute for the cash ledger. Other snapshot inconsistencies are measured above; this export does not document the venue's internal cost-basis/reset rules sufficiently to assign a stronger cause.

Use only the owned execution selected by isAggressor. Its commissionNotionalCollected is the fee for that fill. commissionNotionalTotalCollected is a cumulative order snapshot; summing it across partial fills repeats fees. The counterparty's execution and commissions are not this account's.

There are 1,431 distinct owned order IDs; 168 orders have multiple fill records. There are 282 EXECUTION_TYPE_PARTIAL_FILL records and 1,427 EXECUTION_TYPE_FILL records. A final FILL is the final incremental execution, not a second copy of all prior shares. For example, order `CVF2CQYSMYHK` has 11 distinct fills at Oct 2 05:07:31.366330860Z; their fees sum to $4.87, the final cumulative fee. Deduplicate by fill ID, never by order ID. Use lastShares / qtyDecimal rather than integer qty or a cumulative order quantity.

There are also 50 fills that cross from a positive to a negative signed position or vice versa. Order intent/action is insufficient to compute actual debits. Fill `CVH071GWWYHR` (Oct 2 07:01:00.902387923Z, `aec-wta-taypre-diapar-2026-10-01`) says SELL_SHORT for 83.33 shares while the account is short only 14.29; it leaves **+69.04 long shares**. Treating the displayed $4.2165 cost as sale proceeds would invent cash: the correct change is **-$64.8235**. Its later $69.04 resolution payout is already in the ledger.

For signed YES position n, fill direction dq (+shares for ORDER_SIDE_BUY, -shares for ORDER_SIDE_SELL), YES price p, and signed execution fee f, the cash change is:

```
new_n = n + dq
cash_change = -dq*p - max(-new_n, 0) + max(-n, 0) - f
```

This correctly accounts for cash locked in a new short position and released when a short closes. It works across zero, unlike trusting SELL_LONG/SELL_SHORT intent labels. Settlement adds beforePosition.cashValue and sets the signed position to zero; do not add realized again. All 262 reconstructed pre-resolution decimal positions match the corresponding beforePosition.netPositionDecimal exactly.

The final dust is **+0.0100 share** of `tec-mls-eastconf-2026-12-12-w-mia`. Its last purchase cost $0.0005, and its maximum binary payout is $0.01. It cannot explain dollars of discrepancy. Historical mark-to-market changes on other open positions are not available from this export.

## The hand-versus-AI split is an estimate and can reverse who lost money

Both pm_realized_ai (lines 471-492) and pm_account_story (lines 495-547) sum **all bought and sold lastShares**, then multiply a market's final realized value by AUTOMATIC shares / all shares. The human side is its complement. The ai_by_slug argument to pm_account_story is unused. Gross traded share count is neither invested dollars nor ownership of the shares remaining at settlement.

There are 220 markets with only AUTOMATIC fills, 144 with only MANUAL fills, and 39 with both. Summing the two attribution buckets preserves the chosen market total apart from tiny rounding/threshold effects, so the split itself is not the $53.2874 account gap. It does distort performance attribution.

Cincinnati-West Virginia demonstrates this without any choice of lot accounting: both purchases lose completely. Automatic fill `D5GA3MTG2ZRM` (Oct 17 19:01:38.018720986Z) buys 15.15 shares for $10.16325 including fees. Manual fill `D5GT1JNGYZRP` (19:36:26.710544755Z) buys 187.98 shares for $0.9999 including fees. Actual losses are therefore **AI -$10.16325; hand -$0.99990**. The script instead assigns roughly **AI -$0.81021; hand -$10.05299**, before its omitted commissions. The cheap manual shares overwhelm its share-count weighting.

The existing AI headline is +$205.83984064148635 and human headline rounds to -$357.92. Neither is audited economic P&L. Bot-level splitting in apply_polymarket adds another assumption: it distributes each market's AI result by absolute desk_trades cost_usd, including fills without distinguishing entry from exit. Those desk_trades rows are not supplied, so exact per-bot results cannot be verified here. The $122.0874 baseline and interval comparisons above evaluate the supplied accounting functions with one four-decimal AI event per market. Splitting those events among multiple bots can add small rounding differences; the actual published event sum cannot be reconstructed to its final fraction of a cent without those rows or the emitted snapshot. The full cash ledger is independent of that missing allocation data.

For exact attribution, carry each opening fill's quantity, price, fee and MANUAL/AUTOMATIC owner through a stated lot convention, split crossing fills into closing and opening pieces, and assign settlement to the remaining lots. For mixed ownership, choosing FIFO versus proportional pooling is an accounting policy; the export does not identify which owner's lots a later sell consumes. Preserve an explicit mixed/unattributed bucket where the policy is not established. The account cash chart must be independent of these P&L estimates.

## Exact publisher change

Replace the chart's accounting source with a chronological cash ledger. Do not patch it with a constant -$53.2874 adjustment, subtract a guessed $17, exclude all pending deposits, or sum fees on top of an already fee-inclusive fill cash movement.

Add this pure helper immediately before pm_realized_ai. It is included here as the proposed code change; publish-crew-copy.py itself was not edited. It rejects duplicate records or incomplete position histories instead of silently manufacturing a reconciliation. It assumes this export's two completed positive TRANSFER amounts are credits and uses createTime for balance availability; those historical timing/direction limits remain explicit.

```python
def pm_cash_ledger(acts):
    """Cash only: one owned fill, resolution payout, or funding event per row.
    Amounts and quantities are USD/decimal shares; no network or publisher calls.
    """
    from collections import defaultdict
    from decimal import Decimal

    Z = Decimal("0")

    def usd(m):
        if not m or m.get("currency") != "USD":
            raise ValueError("Missing/non-USD cash value")
        return Decimal(m["value"])

    def payload(x):
        return (x.get("trade") or x.get("positionResolution")
                or x.get("accountBalanceChange"))

    def event_time(x):
        z = payload(x)
        if x.get("accountBalanceChange"):
            return z["createTime"]
        if x.get("trade"):
            e = (z["aggressorExecution"] if z["isAggressor"]
                 else z["passiveExecution"])
            return e["transactTime"]
        return z["updateTime"]

    positions = defaultdict(lambda: Z)
    market_cash = defaultdict(lambda: Z)
    owners = defaultdict(set)
    seen = set()
    events = []
    cash = funding = trading = fees = Z
    for x in sorted(acts, key=event_time):
        z = payload(x)
        at = event_time(x)
        slug = z.get("marketSlug", "")
        fee = Z
        owner = ""
        if x.get("trade"):
            rid = z["id"]
            e = (z["aggressorExecution"] if z["isAggressor"]
                 else z["passiveExecution"])
            o = e["order"]
            q = Decimal(e["lastShares"])
            side = o["side"]
            if side not in ("ORDER_SIDE_BUY", "ORDER_SIDE_SELL"):
                raise ValueError("Unknown execution side")
            dq = q if side == "ORDER_SIDE_BUY" else -q
            old = positions[slug]
            new = old + dq
            fee = usd(e["commissionNotionalCollected"])
            # YES-coordinate cash, including collateral for any SHORT position.
            delta = (-dq * usd(e["lastPx"])
                     - max(-new, Z) + max(-old, Z) - fee)
            positions[slug] = new
            flag = o.get("manualOrderIndicator", "")
            owner = ("ai" if flag == "MANUAL_ORDER_INDICATOR_AUTOMATIC"
                     else "hand" if flag == "MANUAL_ORDER_INDICATOR_MANUAL"
                     else "unknown")
            owners[slug].add(owner)
            kind = "trade"
            title = "Trade cash: " + slug
        elif x.get("positionResolution"):
            # Resolution has no independent ID in this export.
            rid = slug + "@" + at
            before = z["beforePosition"]
            if positions[slug] != Decimal(before["netPositionDecimal"]):
                raise ValueError("Incomplete position history: " + slug)
            # Includes NEUTRAL settlement. Do not substitute realized P&L.
            delta = usd(before["cashValue"])
            positions[slug] = Z
            kind = "payout"
            title = "Settlement cash: " + slug
        elif x.get("accountBalanceChange"):
            rid = z["transactionId"]
            status = z["status"]
            typ = x["type"]
            amount = usd(z["amount"])
            if status == "ACCOUNT_BALANCE_CHANGE_STATUS_PENDING":
                if typ != "ACTIVITY_TYPE_ACCOUNT_DEPOSIT":
                    continue
                # Evidence of an advance, not a blanket acceptance of PENDING.
                advanced = {}
                for t in z.get("transactions", []):
                    if t.get("advancedAmount"):
                        advanced[t["transactionId"]] = usd(t["advancedAmount"])
                amount = min(amount, sum(advanced.values(), Z))
                if amount <= Z:
                    continue
            elif status != "ACCOUNT_BALANCE_CHANGE_STATUS_COMPLETED":
                continue
            kinds = {
                "ACTIVITY_TYPE_ACCOUNT_DEPOSIT": "dep",
                "ACTIVITY_TYPE_ACCOUNT_WITHDRAWAL": "wd",
                "ACTIVITY_TYPE_REFERRAL_BONUS": "bonus",
                "ACTIVITY_TYPE_TRANSFER": "transfer",
            }
            if typ not in kinds:
                raise ValueError("Unknown balance change type: " + typ)
            kind = kinds[typ]
            # These two TRANSFER amounts are treated as credits; reason unspecified.
            delta = -amount if kind == "wd" else amount
            title = kind + (" (advanced; pending)" if "PENDING" in status else "")
        else:
            raise ValueError("Unknown activity type")

        key = (kind, rid)
        if key in seen:
            raise ValueError("Duplicate activity; reconcile its versions: " + rid)
        seen.add(key)
        cash += delta
        fees += fee
        if kind in ("trade", "payout"):
            trading += delta
            market_cash[slug] += delta
        else:
            funding += delta
        row = {"at": at, "k": kind, "usd": float(delta),
               "usd_exact": str(delta), "cash_balance": float(cash),
               "cash_balance_exact": str(cash), "title": title,
               "record_id": rid, "slug": slug, "owner": owner,
               "fee_usd": float(fee)}
        if kind in ("dep", "wd", "bonus", "transfer"):
            row["tx"] = rid
        events.append(row)

    return {
        "events": events,
        "balance_series": [{"at": r["at"], "usd": r["cash_balance"]}
                           for r in events],
        "cash_balance": float(cash), "cash_balance_exact": str(cash),
        "net_funding": float(funding), "net_trading_cash": float(trading),
        "trade_fees": float(fees),
        "open_positions": {s: str(q) for s, q in positions.items() if q},
        "market_net_cash": {s: float(a) for s, a in market_cash.items()},
        "market_owners": {s: sorted(a) for s, a in owners.items()},
        "balance_kind": "cash", "balance_source": "activity cash ledger",
    }

```

In apply_polymarket, replace existing lines 617-618 (the apply_receipts call and the combined P&L events assignment) with the following block (leave the neighboring bot P&L calculations out of the cash series):

```python
    # Preserve the old estimates separately for inspection, not account balance.
    story["pnl_events"] = sorted(
        [e for e in story["events"] + ai_events if e["at"]],
        key=lambda e: e["at"],
    )
    ledger = pm_cash_ledger(acts)
    story["events"] = ledger["events"]
    story["bills_paid"] = apply_receipts(story["events"])
    # Keep the publisher's existing removal of transaction identifiers.
    for event in story["events"] + story["pnl_events"]:
        event.pop("tx", None)
        event.pop("record_id", None)
    for key in (
        "balance_series", "cash_balance", "cash_balance_exact",
        "net_funding", "net_trading_cash", "trade_fees", "open_positions",
        "market_net_cash", "market_owners", "balance_kind", "balance_source",
    ):
        story[key] = ledger[key]
    story["pnl_attribution"] = "legacy gross-share estimate; not audited P&L"
```

The existing deposits = $318.67 and withdrawals = $44.50 fields should retain their meanings. The new net_funding field includes the $25 bonus and $5.07 transfers. Do not relabel these credits as money Jaron deposited. apply_receipts still labels the new withdrawal rows and removes their transaction IDs; it must not change amounts or balances. The block also removes diagnostic record IDs before publication. The analysis helper retains IDs in memory for auditing; the published snapshot need not expose them.

**Chart consumer contract:** plot `account_story.balance_series` using `at` for time and `usd` as the already-computed cash balance. Alternatively sum every new `events[].usd` exactly once, including `trade`, `payout`, `bonus`, and `transfer`; do not filter to the old four event types. Never append pnl_events to the cash series. Label it **Cash balance**, not total portfolio value or AI profit. The frontend chart is not included in this folder, so a literal Python-only edit cannot establish that an unseen consumer accepts the new categories; the balance_series field removes the need for it to perform any accounting. The remaining old AI/hand headline fields are explicitly estimated and must not be presented as verified results. A true total-portfolio history requires historical marks and funding-availability evidence not supplied here.

The helper has been executed locally in memory against all records, without importing or running the publisher. These checks pass:

```python
from decimal import Decimal
ledger = pm_cash_ledger(acts)
assert len(ledger["events"]) == 1987
assert Decimal(ledger["cash_balance_exact"]) == Decimal("68.80")
assert ledger["net_funding"] == 304.24
assert ledger["net_trading_cash"] == -235.44
assert ledger["trade_fees"] == 158.62
assert ledger["open_positions"] == {
    "tec-mls-eastconf-2026-12-12-w-mia": "0.0100"
}
assert pm_cash_ledger(list(reversed(acts)))["cash_balance_exact"] == ledger["cash_balance_exact"]
```

## Daily running ledger

Each row closes a UTC calendar day, after processing its records in timestamp order. Days without activity carry forward unchanged and are omitted. Funding includes bonuses/transfers and withdrawals; fill cash includes commissions. Values are retained beyond cents so totals remain reproducible.

| UTC day | Net funding USD | Fill cash USD | Resolution payouts USD | Ending cash USD |
| 2026-09-10 | 10.00000 | 0.00000 | 0.00000 | 10.00000 |
| 2026-09-11 | 148.00000 | -222.26180 | 149.37000 | 85.10820 |
| 2026-09-12 | 58.98000 | -126.46180 | 55.92000 | 73.54640 |
| 2026-09-13 | 0.00000 | -71.49395 | 46.72000 | 48.77245 |
| 2026-09-14 | 0.00000 | -79.51300 | 49.10000 | 18.35945 |
| 2026-09-15 | 0.00000 | -18.35070 | 0.00000 | 0.00875 |
| 2026-09-16 | 0.00000 | 9.17465 | 0.00000 | 9.18340 |
| 2026-09-17 | 0.00000 | 0.63200 | 0.00000 | 9.81540 |
| 2026-09-18 | 51.69000 | -44.45020 | 5.78000 | 22.83520 |
| 2026-09-19 | 0.00000 | -19.46160 | 31.32000 | 34.69360 |
| 2026-09-20 | 0.00000 | -10.55870 | 16.23000 | 40.36490 |
| 2026-09-21 | 0.00000 | -6.04510 | 0.00000 | 34.31980 |
| 2026-09-22 | 0.00000 | -9.95840 | 12.11000 | 36.47140 |
| 2026-09-24 | 0.00000 | -14.15300 | 0.00000 | 22.31840 |
| 2026-09-25 | 0.00000 | -23.62530 | 6.17000 | 4.86310 |
| 2026-09-26 | 0.00000 | -134.99250 | 179.35000 | 49.22060 |
| 2026-09-27 | -22.00000 | -244.80915 | 328.85000 | 111.26145 |
| 2026-09-28 | -10.00000 | -97.98465 | 85.18000 | 88.45680 |
| 2026-09-29 | -7.40000 | -121.66290 | 90.38000 | 49.77390 |
| 2026-09-30 | 0.00000 | -49.51970 | 73.11000 | 73.36420 |
| 2026-10-01 | 0.00000 | 18.34150 | 6.54680 | 98.25250 |
| 2026-10-02 | 0.00000 | -94.99525 | 97.96000 | 101.21725 |
| 2026-10-03 | 0.00000 | -176.09980 | 194.92000 | 120.03745 |
| 2026-10-04 | 0.00000 | -54.54155 | 131.94000 | 197.43590 |
| 2026-10-05 | 0.00000 | -164.48485 | 13.81000 | 46.76105 |
| 2026-10-06 | 2.47000 | 0.00000 | 0.00000 | 49.23105 |
| 2026-10-09 | -1.00000 | -37.02660 | 1.49000 | 12.69445 |
| 2026-10-10 | 0.00000 | -42.23830 | 29.71000 | 0.16615 |
| 2026-10-11 | 0.00000 | -9.75445 | 11.60000 | 2.01170 |
| 2026-10-14 | -1.50000 | -1.96030 | 2.43000 | 0.98140 |
| 2026-10-15 | 75.00000 | -0.00050 | 0.00000 | 75.98090 |
| 2026-10-16 | 0.00000 | -25.30760 | 19.45000 | 70.12330 |
| 2026-10-17 | 0.00000 | -52.05400 | 48.39000 | 66.45930 |
| 2026-10-18 | 0.00000 | -20.24930 | 22.59000 | 68.80000 |

## Evidence and verification boundaries

Sources: TASK.txt's app readings; the full local polymarket-activity.json; and publish-crew-copy.py, particularly lines 471-547 and 582-627. Source data is USD. Trade times, resolution updateTime and funding createTime were ordered globally; nested execution/order/transaction copies were not counted as additional events. Arithmetic uses Python Decimal; presentation rounds only after aggregation. The proposed ledger helper and original pure accounting functions were run in isolation; the publisher's network-capable main code was never run. The source IDs and exact resolution timestamps above permit inspection without contacting any service.

Original source SHA-256 hashes:

- TASK.txt: `e63e438da20ad614d632f012c92ac4059a1fe340dc01323ba34e4dec8ca50ed7`
- polymarket-activity.json: `90e40019cfa14f0c3c7c0d5e32d5264621e7aa3e976cbc194ebf5e82c0b148ec`
- publish-crew-copy.py: `50adf51a0a2af1e1635b94cdcc537c028d3379d5c81b76c621c926f76d013222`

Prepared by Codex. Only REPORT.md was written.
