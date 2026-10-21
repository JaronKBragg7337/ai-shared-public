# Cash-ledger fix verification — 2026-10-18

Implemented in `publish-crew-copy.py` and `crew-index-copy.html`. The publisher was **not run**. Tests extracted selected function definitions with Python's AST and called them directly against `polymarket-activity.json`; external dependencies were replaced with local stubs for integration checks. No account, database, network, or live-site action was performed.

## Totals on the supplied export

| Component | Exact USD |
|---|---:|
| Deposits, including the documented $75 pending advance | +318.67000000 |
| Promotion bonus | +25.00000000 |
| Transfer credits (purpose unspecified) | +5.07000000 |
| Withdrawals | -44.50000000 |
| **Net funding** | **+304.24000000** |
| **AI trades, net after fees** | **-110.42415000** |
| **Jaron by hand, net after fees** | **-125.01585000** |
| **Final cash** | **68.80000000** |

Exact reconciliation:

```text
318.67000000 + 25.00000000 + 5.07000000 - 44.50000000
             - 110.42415000 - 125.01585000 = 68.80000000

304.24000000 funding - 235.44000000 trading cash = 68.80000000
```

The displayed cents also add up without a remainder:

```text
$318.67 + $25.00 + $5.07 - $44.50 - $110.42 - $125.02 = $68.80
```

The funding card shows **$348.74**, explicitly comprising $318.67 deposits, +$25.00 bonus and +$5.07 credits. The account equation ends at snapshot cash; current cash and open-position value are identified separately instead of being used to invent a balancing event.

| Fees | USD |
|---|---:|
| Commissions charged | 164.97 |
| Maker rebates | -6.35 |
| **Fees paid, all time (net)** | **158.62** |
| AI net fees | 63.64 |
| Hand net fees | 94.98 |

Fees are already included in the owner results and must not be subtracted again. Closed-market counts are AI **108 won / 150 lost**, hand **108 won / 74 lost**. Counts use each owner's net cash result on markets whose account position is closed. Results include all cash, including open-market cash; the remaining position is **0.0100 share** in `tec-mls-eastconf-2026-12-12-w-mia`. A cash debit while a position remains open is not a final economic loss.

## Cincinnati–West Virginia

Market: `aec-cfb-cin-wvir-2026-10-17`. Both purchases ultimately pay zero.

| Fill | Owner | Actual cash, including execution fee |
|---|---|---:|
| `D5GA3MTG2ZRM` | AI / AUTOMATIC | -$10.16325 |
| `D5GT1JNGYZRP` | Jaron / MANUAL | -$0.99990 |
| Settlement payout | Both | $0.00000 |
| **Combined result** | | **-$11.16315** |

Thus the displayed results are **AI -$10.16, hand -$1.00**. The new code assigns each purchase debit and fee to its actual actor rather than weighting losses by gross share volume.

## Checks performed

- All **1,987 events** (1,709 fills, 262 payouts, 16 funding movements) were compared to the independent cash-ledger implementation already supplied in `REPORT.md`. **Every cash delta and every running balance matched exactly**, using Decimal values, not just the endpoint. Input records remained unchanged.
- Net funding plus exact AI and hand totals equals $68.80. Owner fees sum to $158.62; charged commissions minus maker rebates also equals $158.62. All events retain unrounded cash and running-balance strings alongside JSON numbers.
- Every settlement's reconstructed signed position matches `beforePosition.netPositionDecimal`; remaining owner shares match that position. Payouts use `beforePosition.cashValue`, including neutral settlements. Markets closed entirely by fills are included.
- Synthetic cases verified proportional pooling after a partial close, both directions of crossing through zero, short collateral, negative maker commissions, and a non-binary neutral payout split in a repeating 1:2 ratio. Pool shares are exact fractions. Only mixed-owner payout allocation is rounded to 1e-8 USD; its hand complement preserves each actual payout exactly.
- Synthetic pending deposits without documented advances are excluded. Partial advances count only their advanced amount, nested transaction IDs are counted once, and pending withdrawals are excluded. Duplicate events, incomplete settlement positions and unknown fill owners are rejected.
- `apply_polymarket` was called with local history and receipt stubs. It preserved all ledger events and exact headline totals, serialized the snapshot to JSON, removed transaction identifiers and retained the existing per-bot spend weights. The actual receipt matcher was separately exercised with a local stub: it relabeled a withdrawal as a bill without changing its amount or running balance.
- The full HTML module passed JavaScript syntax and execution checks with the actual computed ledger and DOM stubs. Assertions checked all new card labels and amounts, the displayed cents equation, all **1,987 plotted events**, first/last slider and click selection, receipt links, escaped titles, absence of NaN coordinates, and the guard against showing old resolution-based snapshots as cash. A deliberately different live cash/open-position reading did not change the snapshot equation or chart endpoint.

The mixed-market convention is documented in the code: every fill's cash belongs to its actor; closing fills consume both owners' remaining shares proportionally; a crossing fill opens only its excess for its actor; settlement pays the remaining share pool. This is an attribution convention, not exchange-provided owner lot identification.

Per-bot allocation remains approximate, as requested: each market's AI result is split by absolute `desk_trades` fill spend. Existing independent cent rounding is preserved. In the synthetic 3:1 split, bot totals round to -$82.82 and -$27.61 (sum -$110.43), while the account headline remains -$110.42. **Those bot estimates never enter the account cash ledger.** Actual per-bot attribution cannot be verified without the unavailable live desk rows.

Browser layout and the live site were not exercised; the shared `crew.js` and styles are not supplied here. The HTML copy implements its own cash chart so its event types and endpoint do not depend on the shared settled-P&L chart. Nothing was published.

## Reproduce the exact ledger comparison locally

Run this PowerShell snippet in this folder. It extracts pure functions, so it does not import `executor`, refresh history, call `main`, or run the publisher:

```powershell
@'
import ast, json, re
from decimal import Decimal as D
from fractions import Fraction

path = 'publish-crew-copy.py'
tree = ast.parse(open(path, encoding='utf-8').read())
names = {'pm_cash_ledger', 'pm_account_story', 'pm_realized_ai'}
ns = {'Decimal': D, 'Fraction': Fraction}
pure = ast.Module(body=[n for n in tree.body
    if isinstance(n, ast.FunctionDef) and n.name in names], type_ignores=[])
exec(compile(pure, path, 'exec'), ns)
acts = json.load(open('polymarket-activity.json', encoding='utf-8'))
s = ns['pm_account_story'](acts)

report = open('REPORT.md', encoding='utf-8').read()
code = re.search(r'```python\n(def pm_cash_ledger.*?\n)```', report, re.S).group(1)
ref = {}
exec(code, ref)
expected = ref['pm_cash_ledger'](acts)
running = D(0)
for event, check in zip(s['events'], expected['events'], strict=True):
    running += D(event['usd_exact'])
    assert D(event['usd_exact']) == D(check['usd_exact'])
    assert running == D(event['cash_balance_exact']) == D(check['cash_balance_exact'])
assert len(s['events']) == 1987
assert running == D('68.80')
assert D(s['ai_result_exact']) + D(s['hand_result_exact']) + D(str(s['net_funding'])) == running
assert D(str(s['ai_fees_paid'])) + D(str(s['hand_fees_paid'])) == D('158.62')
assert D(str(s['fee_charges'])) - D(str(s['maker_rebates'])) == D('158.62')
assert s['market_results']['aec-cfb-cin-wvir-2026-10-17'] == {'ai': -10.16325, 'hand': -0.9999}
print('PASS: 1,987 deltas and running balances; $68.80 cash; owner totals; fees; Cincinnati.')
'@ | python -
```
