# First unattended live win — 2026-09-13 (forensic reconstruction)

Reconstructed by Claude Code 2026-09-13 10:05 ET from: `trade_proposals` #65, `desk_trades` rows (fill
CFBV8X6BMTNR, resolution), Polymarket US `polymarket_activities` (both sides of the fill), and
`state/live-wire.md` lines 355–364. Nothing below is from memory.

## The claim, stated precisely
**The first trade in this system that went entry → hold → settlement with no human touching any step,
and won.** Not the first AI-placed trade (Live Wire placed #13, #14, #39, #40 on Sep 12). Not the first
AI-entered winner (#14 Missouri vs Kansas, bought 47¢ by Live Wire on Sep 12 01:30Z — but it was
*sold manually* in the app at 99¢ at 03:36Z, so a human closed it). #39/#40 Memphis was an AI entry and
AI exit that lost 8¢. #65 is the first with zero human steps end to end.

## Timeline (ET = UTC−4)
| ET | UTC | what | who / evidence |
|---|---|---|---|
| 5:00 | 09:00 | BLG vs Anyone's Legend, LPL Split 3 Finals, starts | venue title |
| 5:34 | 09:34 | Live Wire's sweep: logs `WATCH NO TRADE` on BLG-AL — series 0-0, ~30 min into game 1, "Elo ~72% pre; early/draft no score-lag". Dispatches the "box" (computer-use eyes) to polymarket.us/live and score pages. | live-wire.md 357, 363 |
| ~5:35 | ~09:35 | Eyes see the stream HUD: game 1 at 26:03, AL up 11–6 in kills; desk book still BLG YES 0.66/0.67 (unmoved). | live-wire.md 364 (logged 09:37 after the fact) |
| 5:36:10 | 09:36:10 | Live Wire runs `desk-trade.py --by grok-bot/live-wire --side no --size 5` on the BLG market. desk-trade reads the book the same second (0.66/0.67, spread 1¢), writes proposal #65 with verdict `auto`, submits `BUY_SHORT limit 0.66` (YES scale) for 14.71 shares. Order id CFBP559NCTMP. Rationale logged: "box eyes AL 11-6 kills ~26:03 G1 vs sticky BLG series YES 0.66/0.67; fav lag on G1 stomp". Kill rule: "BLG wins G1 or equalizes kills/objectives before nexuses". | trade_proposals #65 |
| 5:36:56 | 09:36:56 | Order fills **passively**: a counterparty's manual limit order buying BLG at 0.76 (296.96 shares, only 37.51 filled) crosses ours. We pay 34¢/share, $4.96 + $0.04 fee = $5.0014. | venue trade CFBV8X6BMTNR (aggressor = counterparty, passive = us) |
| 5:37:04 | 09:37:04 | Verifier's 5-minute reconcile sees the fill, matches order id to proposal #65's fill_note, writes ledger row `actor = auto:grok-bot/live-wire`. | desk_trades fill row |
| — | — | Kill rule never triggered. AL won game 1; series went 3–1 AL. | venue score |
| 8:36:26 | 12:36:26 | Venue settles the position: 14.71 shares × $1 = $14.71 payout. | positionResolution |
| 8:37:04 | 12:37:04 | Verifier writes the resolution row: realized **+$9.7086**. | desk_trades resolution row |
| 8:40 | 12:40 | Jaron opens the app on his walk and sees "+$14.71". | screenshot |

## Money
$5.00 in → 14.71 shares at 34¢ → $14.71 out → **+$9.71 (+194%)**. Account went ~$87 → $96.87.

## What played a part
1. **Grok (xAI) as "Live Wire"** — a scheduled task on the MSI running the Grok bot with a browser/computer-use
   "box" for eyes. It decided. No probability model, no edge number: a *lag read* — the live game state
   (AL stomping game 1) vs a market that hadn't moved off the pre-match favourite.
2. **`tools/desk-trade.py`** — the only door to money. Holds the Polymarket US key on the MSI (no agent has it),
   re-read the book the same second, refused nothing (spread 1¢ ≤ 5¢, size $5 ≤ max, `--why` present, `--by`
   not an OpenAI/Anthropic name), wrote the proposal row, placed the order.
3. **Polymarket US** — rested the limit order; a human on the other side filled it 46 s later.
4. **`tools/verifier.py`** — reconciled fill and settlement to the public ledger with the right actor tag.
5. **The public page** (heartbeatobservatory.com/live-systems/trades) — showed the row with `AUTO (NO APPROVAL)`.

## What did NOT play a part
Jaron (asleep, then walking). Claude, Codex, ChatGPT (research/build only, never trade — by rule). The
proposer script and the approval queue (desk-trade bypasses both by design for live trades). The fly
brain (dry mode, table tennis only). Qwen, DeepSeek. The kill rule (never fired).

## Open honesty notes for any post
- One trade. Sample size one. Live Wire's record before this: 1 AI-entered win closed by a human,
  1 tiny AI loss (−8¢), 1 exit. This is a milestone of *the loop working unattended*, not of edge.
- "Autonomous" means: a scheduled bot, a browser for eyes, a CLI with the key, a reconciler, a page.
  Every piece is named above; nothing is a black box.
- The counterparty was a person placing a manual order at 76¢ while AL was up 11–6. That is the
  whole trade.

## Posted
2026-09-13 10:51 ET, X (@JaronBragg), single post ~2,800 chars + two screenshots (site + receipt). Credits: @grok, @Polymarket, @AnthropicAI, @OpenAI. Hardware donor unnamed (no permission yet). Every number in the post matches this file.
