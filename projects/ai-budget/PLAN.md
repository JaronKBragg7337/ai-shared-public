# The self-paying AI system - Jaron's plan (2026-09-29 5:06 PM), within ~3 months

**The goal, in his words:** "something in the system, most likely you [Claude], that is focused on paying attention to this
stuff, and then the AI that's supposed to be paying subscriptions... where I don't have to do it anymore and it just comes out
of the money." He builds and walks along the river talking about what we build; Grok Bot keeps making money; what we build
gets promoted; the AIs watch usage, cost and output and decide each month which plans are needed ("maybe this month we don't
need this subscription for this AI and we can use this one instead").

## Step 1 - measure (now, October) - BUILT 9/29
- `tools/ai-budget.py` -> `state/ai-budget.md`: each AI's plan and cost, latest usage, commits this month, the trader's
  settled profit this month, Jaron's target (Control Room row `builder_toolset_target`), plain-rule flags. Weekly task
  "AI Budget Report", Mondays 5:30 AM. Grok Bot's meter isn't readable by a script: add each reading to state/grok-usage.md.
- `tools/grok-money.py` -> `state/grok-money.md`: the trader's money by day/week/month/sport.
- First reading (9/29): Claude ~85% of its week, Grok 84%, Codex 4% - Codex is paid for and barely used.

## Step 2 - recommend (November, after 1-2 months of data)
- The report adds "next month": which plan each AI should be on, from last month's usage + what is planned to be built
  (state/whats-next.md) + what the trader earned. Claude writes it; Jaron reads it on his walk.

## Timing update (Jaron 9/29 9:50 PM)
- Correction 9:53 PM: the system ALREADY paid Claude's 9/27 renewal ($22 out of Polymarket, bot-chat 9/28), and should cover
  Grok's when it comes due. **The 9/30 Codex payment is the last AI subscription Jaron pays himself** - his commitment. From
  the Oct 27 renewals on (Claude and ChatGPT both renew on the 27th), every plan comes out of the system's money. One schedule for all: Grok renews on a different day - moving it to
  the 27th is his call. He wants enough profit by then to cover the bills AND next month's float.

## Step 3 - pay and switch by itself (first bills Oct 27; fully hands-off by ~late December)
- Money path: the trading account covers the month's plans (a monthly transfer out of the trading account sized to the bills),
  so Jaron's own money never touches the subscriptions. The desk's three numbers keep it visible: settled profit, open bets,
  withdrawable cash - and the bill money is its own line.
- Open, decide when we get there: which AI moves the money and switches plans (it needs access to each provider account;
  Claude and Codex never move money - their providers' terms). Plan switches happen at each renewal date, which we need on
  record (subscriptions.json: Claude and ChatGPT renew on the 27th; Grok's date still unknown).

## Promotion lane (runs alongside)
- What we build gets clips and posts made by the AIs; Grok Bot can boost. Jaron: TikTok and X live/monetization is the
  cleanest money. Keep trading and money out of anything paid/boosted (X paused a boost 9/24 for "Financial products").
- Posts on Jaron's own accounts are him speaking - he posts those. AI posting needs AI-owned accounts.

## Rules that stay
- Upgrades are Jaron's call; the system's job is to pay for them, not to gate them.
- Jaron's own withdrawals start at an account of $350-400 (Control Room). That floor is his, not the AI's.
