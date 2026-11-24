# Runs without Jaron - the runbook (built 2026-10-20 by Claude Code)

For: court Nov 10 (could mean days to months away) and the baby due Dec 9. Goal: nothing stalls for 30 days with no human,
cushion for up to 6 months. Any AI working while Jaron is away reads THIS page first. History and decisions: README.md.

## 1. Bills - what must keep getting paid
Source of truth: state/subscriptions.json (monthly) + this list (things that aren't monthly or aren't AI).

| Bill | Amount | How it's paid | Due / renews | Risk if missed |
|---|---|---|---|---|
| Claude (Max) | $100/mo | X Money card, web | monthly | me + all Claude builders stop |
| ChatGPT / Codex | $20/mo | X Money card, web | monthly | news capture (Codex) + fact-checks stop |
| Grok (SuperGrok) | $30/mo | PAID 10/20: Apple order $43.87 charged to the X Money card (timeline 10/20 09:00); prepaid to ~Jan 10 2027 | reminder tasks exist; move to web in Jan | trading bots + news desks stop |
| Kimi | $39/mo | APPLE (renews 11/2) - to move to the web / X Money card (Apple confirmed 10/20) | monthly (reminder task 'Remind Kimi renewal decision') | First Light news capture stops |
| Supabase Pro | $25/mo | X Money card | monthly | **site database: everything stops** |
| **Postiz** | **$29/mo after the trial ends Oct 24** | needs a card on Postiz | from ~Oct 24 | **daily socials stop posting** - in subscriptions.json since 10/20; Jaron keeps it |
| X Premium (company @HeartbeatObserv) | $15/mo, $30 from 11/17 (Pip 10/24) | bought 10/17 | monthly | reach drops, 2nd Grok Bot goes |
| DeepSeek API | prepaid credits | X Money card | when credits run low | cheap research + news reader stop |
| Domain heartbeatobservatory.com | ~$10/yr | Cloudflare | **expires 2027-06-06** (checked 10/20) | site gone - safe for this window |
| Vercel, GitHub, Cloudflare, ntfy | free | - | - | - |

Monthly total ~$258 ($214 + Postiz $29 + X Premium $15), plus DeepSeek top-ups.
**Jaron 10/20: it's one connected system, not a ranking.** Core four (one missing = the rest fails or skips a step): Claude, Grok,
Supabase, Postiz. News balance (one missing = worse news, not dead): Kimi, DeepSeek, Codex. Goal: NOTHING gets cut - keep a
cushion on the X card (~$258 = 1 month of everything, ~$516 = 2). Emergency only: keep the core four first.

## 2. Logins - who can fix what
| Thing | If it logs out | Can an AI fix it alone? |
|---|---|---|
| Claude Code on the MSI | RECONNECT.md section 1 | No - needs a browser sign-in. Lasts months normally. |
| Codex (ChatGPT) on the MSI | section 2 | No - browser sign-in |
| Grok Build on the MSI | section 6 | No |
| Kimi Code on the MSI | section 8 | No |
| MSI connector (Grok/Claude chat reach) | section 3 | Partly - tunnel/server restart yes; re-authorize in the app no |
| Postiz channels (TikTok/YouTube/X tokens) | section 10 | No - each platform's own sign-in |
| Polymarket key | Key Drop | No - but from a phone, 2 min |
| Kraken key | Key Drop | same |
**Pattern:** AIs can restart anything; only a person can sign in. Every sign-in here lasts weeks to months, so the risk is
low but not zero. The watch tasks below catch it the same day.

## 3. What watches the system, and who hears it
Running as Windows tasks (no AI needed): MSI Connector Watch (30 min: tunnel, Polymarket service, Sapling relay, disk space),
MSI Status (30 min, state/MSI-STATUS.md: heat, power, disk, failed tasks, logins), MSI Health, Login Watch, DB Size Check, HB Rendered News (with fast-mode deadline rule), HB Socials News/Show, HB News Desks,
HB Key Drop, HB Build Ledger, Crew Publish, Live Board, Desk Schedule Watch, Desk Weekly Review, AI Budget Report.
Reminders already scheduled: Court 11-10 (week before + day before), birthdays, Kimi renewal, Christmas lights giveaway.

**Gap:** every alert goes ONLY to Jaron's phone (ntfy). If he can't see it, nobody does.
Fix options (Jaron picks; none needs his partner):
- (a) alerts also land in state/bot-chat.md so whichever AI runs next reads them and fixes what it can (no human). **Recommended.**
- (b) a second ntfy subscriber - optional, only if someone wants it.

## 4. Pre-decided defaults (so nothing waits for an answer)
- News late -> fast mode automatically; nothing published by noon -> skip the day, the archive still updates. (built)
- A daily social post fails -> retry next run; a platform logged out -> keep posting to the others. (built)
- Trading: hard limits stay in the scripts; a losing lane benches itself (Desk Schedule Watch) - one problem, one fix, never a
  full stop. No new money gets added while Jaron is away.
- Bills: pay in the order above. A bill that can't be covered -> pause the lowest one, never Supabase.
- New ideas from AIs: build only what's on the open list or the TV slate; anything new waits in state/open-list.md.
- Anything that needs a yes (messages to people, new accounts in his name, money moves above a bill) waits for him.

## 5. Money for bills (the profit split, Control Room rows monthly_bills_usd + profit_split)
Above $400: 50% trades, 30% to the X card for bills, 20% stays in for now. Polymarket can't withdraw by API (tested 10/19), so
from Polymarket a person or Grok Bot's logged-in browser moves it; Kraken can withdraw by script to saved destinations.
**Before court:** load the X card with 1 month of bills (~$258) at minimum; cushion goal = more months as profit allows.

## 6. Still open (Jaron)
1. Bill order: ANSWERED 10/20 - core four + news balance, cushion so nothing is cut (see section 1).
2. Alerts: option (a), (b) or both.
3. Postiz $29/mo after Oct 24: Jaron knew (10/20) - keep.
4. X Premium = $15/mo (Jaron 10/20).
5. Optional, only if they want it: his partner-GUIDE.md (one page, 3 steps max).
6. Yearly vs monthly (checked 10/20): savings only on Postiz (~$72/yr, $23/mo yearly - decide at the Oct 24 billing), Kimi (~$96/yr if Pro tier, $372 upfront), maybe Grok (renamed 10/12, yearly price unlisted). No yearly discount: Claude Max ($1,200/yr either way), ChatGPT Plus, Supabase. Prepaying = runs during an absence, but ties up cash.

Due dates (from receipts + Jaron's notes, 10/20): Postiz Oct 24 (first charge) / ChatGPT the 27th / Claude Max the 2nd / Kimi the 2nd (STILL VIA APPLE - move to web; reminder Oct 30) / X Premium company ~17th (estimate) / Supabase ~23rd / Grok prepaid to ~Jan 10 2027 / DeepSeek when low. Busy stretch: ~$188 Oct 24 - Nov 2. (Personal X Premium $11 via Apple: confirmed renews 2026-11-10, see next line.)
CONFIRMED from Apple Subscriptions screen 10/20 8:33: Grok SuperGrok $30 via APPLE renews 2027-01-10; Kimi Allegretto $39 via APPLE renews 2026-11-02 (yearly on Kimi = $374.99, 20% off $468); personal X Premium $11 via APPLE renews 2026-11-10 (= court day); iCloud+ 2TB expired Oct 16; ChatGPT via Apple expired Aug 17 (now web). Kimi usage 10/20: total 40%, Code 7-day 43%.
RESOLVED 10/20 09:00 (SuperGrok safe to Jan 10; timeline 10/20 08:47-09:00). History - WARNING 10/20 8:38: Apple order MVGMTJ2GV6 $43.87 (SuperGrok 3-month deal $30 + personal X Premium $11, bought 10/10) FAILED on Chime (balance -$19.01 since Sat 10/17). Apple shows "renews Jan 10" = billing retry, NOT paid. Grok (core four) at risk until paid. Options given: pay once with X Money card in Apple then remove card / or move to grok.com web. Jaron: no yearly plans until 2027 (after court + the baby).
UPDATE 10/20 8:44 (history): Jaron planned to pay from the paycheck; instead $35 went Polymarket -> X card 8:47 and the Apple order was charged to the X Money card 9:00. Open: refill Polymarket $35 on payday; Jaron removes the X card from Apple after work (task 'Remind remove X Money card from Apple').
