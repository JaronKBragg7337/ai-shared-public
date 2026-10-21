# Handoff — the state of everything, 2026-09-11 15:45 (Claude Code)

**For:** any agent, and Jaron. Written because he asked: "if you need to save this or anything else
important, not answered, planned to do — we should do now." This is the whole picture in one page.
Truth order if this drifts: `INDEX.json` → `TODO.md` → `decisions/OPEN-QUESTIONS.md` → newer handoffs.

## What exists and runs (all verified working today)

| piece | cadence | what it does |
|---|---|---|
| `Trade Proposer` (`tools/proposer.py`) | every 2h | screens Polymarket US (½ settle-within-48h, ½ long), researches price-blind via Codex, writes `trade_proposals` rows. Method `both`: split (facts → arithmetic, direction-locked) then direct at smallest size. Leaves `inbox/sentiment-requests.json` for Bridge. |
| `Trade Verifier` (`tools/verifier.py`) | every 5 min | re-checks numbers on pending rows; publishes `desk_account`; reconciles `desk_trades` (who did what) from the venue's activity feed; waits when the venue is dark. |
| `Trade Executor` (`tools/executor.py`) | every 5 min | places `verdict=approved` rows. Short limit price on the YES scale. |
| `Scout Scorer` (`tools/score-estimates.py`) | daily 06:30 | Brier per method vs the market price at the time → `state/scout-scores.md`. 35+ estimates waiting. |
| `AI-Shared Mirror` | daily 04:30 | robocopy to `G:\My Drive\AI-Shared-mirror`, secrets excluded. |
| `Desktop Commander Remote` | always | ChatGPT's door. |
| `Grok Machine MCP` | always | Grok/Claude-phone door (one server, two names: "Grok Machine" / "Heartbeat MAI"). |
| Bridge (Grok Bot) hourly routine | :51 | MSI health line → `state/bridge-health.md`. Steps 8–9 (sentiment, queue nudge) written in `agents/grok-bot/HEALTH.md`, **not yet pasted into the bot**. |
| `tools/desk.py` / `tools/desk-trade.py` | on demand | read / act from any shell. The two commands every door should know. |

Site: `/live-systems/trades/` = one page for everything: queue with editable size + payout, account,
positions, ledger labelled human/AI/agent, category path + link into the app. Front door trimmed;
paper trading unlisted (page stays); no ghost pages.

## Real money so far (venue-confirmed)
- System: 6 fills across 3 approved proposals (#1 Fed cut, #9 Dodgers NO, #11 Anthropic-#1 NO), all
  placed by the executor within 5 min of Jaron's tap. Zero errors.
- Jaron by hand: 19 table-tennis markets, net **−$16.53**; the three ≥$15 bets were the entire loss,
  the $5 bets broke even, mid-priced (0.20–0.70) entries won 6 of 13. Review:
  `state/jaron-manual-review-2026-09-11.md`. Lessons folded into Live Wire's brief.
- Account ≈ $129 available + 5 positions. Deposits $158 total.

## Needs Jaron at the MSI — ALL DONE 2026-09-11 19:00–19:45
1. Live Wire: Description + routine pasted (via chat), msi-heartbeat connector live. Wakes hourly at :20.
2. Bridge: steps 8–9 saved verbatim, :51 schedule unchanged.
3. DeepSeek key in; tested; `Trade Proposer` task now defaults to DeepSeek (midterms answered in 2s).
4. CoworkVMService recovery: Access denied even as admin (SYSTEM-only ACL). Won't-fix.
Also answered: Q-015 (fine, closed), Q-016 (`decisions/ASK-JARON.md`).

## 20:50 — verified live after the MSI session
Bridge's 19:58 wake wrote 6 `state/sentiment/*.json` (step 8 works). Live Wire logged its Valorant
exit + final P&L unprompted; routine now: eyes on its box, hands on MSI, $5→$10 ladder, +$10 take-profit,
table-tennis focus, claims via `state/agent-claims.jsonl` (reconciler relabels). Proposer on DeepSeek.
**System is in watch mode.** Next build conversations, when Jaron wants: Codex/ChatGPT Work standing
jobs; the fly brain (Q-013).

## Open decisions (ledger has the detail)
Q-013 fly brain (its own conversation) · Q-014 Qwen's role · Q-015 the 11:02 Fed sell · Q-016 the
"best at" file · Q-006 payment rail (parked) · Q-009 ChatGPT memory test (low) · Q-004 git (Sep 30).

## Traps learned this week (all also in INDEX.json / RUNBOOK)
- AtLogOn + repetition tasks do not repeat until the next logon → add a start-now trigger.
- BUY_SHORT / SELL_LONG limit prices are on the YES scale. SELL_SHORT inferred, first one small.
- polymarket.com ≠ Polymarket US. Ours is `.us`, key stays on the MSI behind the local MCP.
- Futures carry a stale `gameStartTime`; "in progress" = started within 8h.
- Codex declines election forecasts; the research split (facts, not forecasts) does not trigger it.
- The venue double-credited then corrected balances after its 2026-09-11 upgrade; our ledger has no
  duplicates because resolution rows are keyed by slug+time.
- Computer use on the MSI: Grok Bot's window is WebView2; without that grant the screen is masked.

## Ideas parked, not lost
Grok watching live video (Live Wire is the first form) · Claude phone → Heartbeat (done) · Orchestra
targeted via DeepSeek (after key) · Codex/Luna standing jobs (Q-009-adjacent, Jaron picks) ·
one-page site consolidation beyond Live Systems.
