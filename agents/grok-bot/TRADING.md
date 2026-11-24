# Polymarket US — Bridge trading pipeline

**Status (10/23 sweep): Sept 11 pipeline, written by Claude Code. 'Jaron approves every order' / 'only after Jaron's explicit yes' was the Sept design; the approve queue was retired 9/24 (Q-023) and orders now go through desk-trade.py inside Control Room limits. The method notes below (edge vs spread, Scout isolation, crypto excluded because of PolyBench) are Claude Code's, not Jaron rules; the crypto lane was approved by Jaron 10/22 (decisions/CRYPTO-LANE-PLAN-2026-10-22.md). Kept as history.**

**Owner:** Bridge (grok-bot)  
**Venue:** Polymarket US via MSI `127.0.0.1:8765` (not polymarket.com)  
**Updated:** 2026-09-11 after Claude/Jaron process correction

## Roles

| Who | Does |
|---|---|
| Bridge | Screen liquidity, call Scout with questions only, apply edge>spread, size, place after yes |
| Scout | Independent p + confidence from evidence only — never sees prices, spreads, or cheapness |
| Claude Code | Cross-read live BBO numbers before anything reaches Jaron |
| Jaron | (Sept 11: approved every order; retired 9/24) |
| Qwen | May execute tooling elsewhere; not trusted to form the view (2026-09-10 misreads) |

## Order of operations (the default - research follows liquidity so effort is not wasted; deviate when there is a reason)

1. **Screen first** for markets that are `tradeable`, spread **≤ 2¢**, preferably priced **0.10–0.90**, **crypto excluded** (PolyBench: LLMs lose worst there with high confidence).
2. **Hand Scout the QUESTION only** — resolution text OK; never price, spread, or which side looks cheap. Naming the market is fine; naming the number is not.
3. Scout returns **probability + confidence** (+ drivers / change-triggers).
4. Re-read live BBO. Apply filters below. Size. Bring survivors to Jaron with Claude cross-reading the same slug.
5. Place only after Jaron's explicit yes (Sept 11 design, retired 9/24). Disagreement between Bridge and Claude on the quote → **no trade**.

## Math (do not invert)

When **buying** a side at entry price `P` with Scout fair `F` for that side:

- **EV/share = F − P** (positive means ask/entry is below fair — a gain).
- **Spread = ask − bid** on the Yes book (for No/short, use the complementary quotes: `ask_no ≈ 1 − bid_yes`, `bid_no ≈ 1 − ask_yes`, or venue `shortQuote`).
- **Standing rule: edge must exceed spread.**  
  `(F − P) > (ask − bid)`  
  If not, **no trade**, regardless of thesis quality.

Tonight's ATL moneyline failed this: edge ~6¢, spread ~8–9¢.

## Venue quirks (Polymarket US)

- Signal is `bestBidQuote` / `bestAskQuote` `{value, currency}` — not clobTokenIds/volume/liquidity.
- `polymarket_search` annotates `tradeable` + `tradeable_reason`. If `tradeable` is false, the price is **not information**.
- `polymarket_bbo` / `orderbook` / `market` take **`slug`**, not numeric id.
- `longQuote` ≈ cost to buy Yes/long; `shortQuote` ≈ cost to buy No/short.
- Call `today` before any dated reasoning.
- **BUY_SHORT limit `price` is on the YES scale**: send `1 − (max you will pay for No)`. A $1 buy of
  No at 8% went out from the app as `BUY_SHORT price 0.82`. Sending the No price (0.27) "works" only
  because it is marketable — it is not a real limit. Verified from account activity 2026-09-11.
- `polymarket_activities` = the app's History tab. Every order carries `manualOrderIndicator`:
  MANUAL = Jaron in the app, AUTOMATIC = executor/MCP. That is how the ledger labels who did what.

## Sizing

Account starts ~$10. PolyBench: edge dies as size rises (slippage). Default candidate size **$1–$2** (Sept 11, account was ~$10; size now follows the Control Room). Thin OI → cut size or pass even if edge>spread.

## Confidence

Frequency is fine. **Undifferentiated confidence** is the failure — always finding a trade *or* always abstaining without a filter. Low Scout confidence → pass or micro-size even when edge>spread on paper.

## Isolation

Do not feed Scout prices, books, positions, or P&L. Do not put market opinions into AI-Shared core docs. Operations and runbooks only.
