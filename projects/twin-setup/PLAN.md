# Twin setup for other people - draft plan (Jaron, 10/4 8:55 AM, talking it through; nothing built)

Idea: set up a money twin (one Grok Bot trader like Darios/Satya) for someone else, paid.

## Package (his numbers)
- $160 total for the system: $100 into their own Polymarket US account + $60 subscriptions (= 2 months of Grok at $30)
- + $75 setup fee (his)
- Client owns every account, key and dollar. Jaron never holds their money.

## What is truly needed
- Grok with Grok Bot ($30/mo) - the trader
- Polymarket US account, their own (KYC is theirs)
- The trade script with seatbelts (size per buy, no oversell, one bot per game) on Grok Bot's own computer
- Optional: stats page (free GitHub/Vercel/Supabase) - part of the deal if they want it
- NOT needed: the MSI, the other AIs, Claude, the connector (unless they want the page)

## Defaults for a client (start safe, loosen later - never the other way)
- Football first (college + NFL = the money so far); tennis OFF; warn hard if they want it
- Per-buy size scaled to their bankroll (our $10 cap was on ~$200)
- Routines off before ~11 AM on game days if usage is tight

## Path
1. Prove it on people close first, funded from the desk's own profit (his partner = possible first)
2. Build the kit (later - his call: not an old repo, not from scratch; maybe repo/USB + an AI setup assistant)
3. 90-day watch + on-call; refund = subscriptions paid only, never Polymarket money
4. Only then sell, through the LLC

## Check before charging anyone
- CFTC: paid setup of trading for others may count as a commodity trading advisor; small-client exemption exists - confirm
- Polymarket US terms: own account/keys per person, automated trading allowed, which states
- xAI terms for Grok Bot trading
- Refund/guarantee + no-profit-promise wording; watching their system = their data, needs their OK in writing

## Refund + human moves (Jaron 10/4 9:01, talking it through)
- The system already tags every trade bot vs human; withdrawals show in the account feed. Their page shows WHAT (human trade,
  withdrawal, AI trade) - never asks WHY. Read-only view, no access to their money.
- Guarantee = the system works as described (trades, script runs, page updates). Fails that in 90 days -> refund setup fee +
  subscriptions. Market losses, their own trades and withdrawals are theirs and don't count - the records show which is which,
  so nobody has to judge anyone's story.
- Someone fakes a problem to copy the system: allowed to happen. Exposure = what they paid; the system is open anyway; the fee
  is for doing it, not for a secret.
- Working floor (e.g. the starting $100): below it the page just says the bot has less to work with. No lock, no lecture.

## Open steps, two doors (Jaron 10/4 9:04)
- The exact steps go public (CC0) so anyone can do it themselves for free, or with their own AI.
- Tell every client up front: do it yourself and skip the $75, or pay him to do it.
- Honest note in the steps: some AIs add their own caution on top of the plain steps (refuse to trade, shrink everything);
  the steps say what the system needs so they can tell their AI's caution from what the setup actually requires.

## Public commitment (Jaron on X, 10/5 8:53 AM, reply to @DevinSoto)
"I'm about to set up my system for 10 people on me free to prove it. Then after that open source it but charge $75 fee for
those that want it set up and don't want the troubles. In time grok will be big."
-> Phase 1 = 10 free setups funded by the desk (was "a few close people"). Free = no paid-advisor question yet; the legal
check is needed before the first $75.

## The real test (Jaron 10/5 7:52 PM)
The point of the money growing is to USE it - gas, bills, subscriptions, cigarettes - so a client's account will always see
money made, money taken out, money made. Never a rule that says "you can't touch it." Two different things on the ledger:
- a WITHDRAWAL for something needed = the system working (his cigarette sale was made back 5 minutes later)
- the HUMAN BETTING by hand = a loss the bots have to earn back (his 10/5: ~$233 -> ~$57 chasing BTC)
His own account is now the proof under real ups and downs: can the bots keep refilling it while a human uses it? Track it
from 10/5 7:54 PM at $48.68 (start line; his $50 optional) - that recovery is the strongest pitch for the 10 free setups.

## Trust rule (Jaron 10/5 8:39 PM, after posting his $233 -> $47 loss publicly on X)
"Someone in my position that truly just needs something - I can take it if it has flaws, but only if the flaws are upfront
and I'm not feeling like I'm being lied to." Every pitch, page and setup shows the flaws first: his human losses, the bad
sports, the paused bot, the small sample. If he wouldn't believe it himself, don't ship it.

## Tiers by bankroll (Jaron 10/5 9:05 PM, an idea while vibing to music)
What's in the account decides how big the bets are and which games are looked at:
- ~$50 (careful / all they can spare): small bets, safest lanes only (college football), getting money back matters most
- $100-150: medium bets, football + NFL
- more: bigger bets, more lanes (test lanes, more games)
Never tennis at any tier. Season decides the lanes. Build as Control Room settings: tier thresholds + per-buy cap as a share
of the CURRENT balance (moves up and down with the account) + lanes per tier; desk-trade enforces it. His own desk at $48.68
= the first test of the small tier (also answers the "$5 cap until $100" question automatically).

## Phone-only setup (Jaron 10/5 ~10:30 PM notes) - candidate #1 = his partner, if she wants it
- Her phone only: Grok app (SuperGrok $30, Grok Bot via Cursor link), Polymarket US app/web, GitHub app or web.
- Money: Jaron puts $25 in + her $25 referral bonus = $50 start. First month ~ $55 all in (<$100 total).
- Grok Bot runs the trade script on ITS OWN sandbox computer (like the X sign-in for an old bot) - nothing on her devices.
- Grok chat clones the template repo into her own GitHub repo; the bots update a GitHub Pages stats page on days they work.
- To check: (1) can a Polymarket US API key be made from a phone (web) and stored in Grok's sandbox safely;
  (2) in this setup the key + seatbelts live in the bot's own sandbox, so the bot could edit its own limits - his own desk
  keeps the key on the MSI behind the connector. Options: Polymarket-side limits if any, or seatbelts in a repo the bot
  reads but a CI check guards. (3) does Grok Bot's sandbox persist files between routine runs.
- If it works: the kit for the 10 free setups is phone-only, under $100.
- Jaron 10/6 7:13 AM: the bot is a sophisticated AI, not a dumb trading bot - its instructions and scripts ARE the guardrails,
  and it won't go against what the owner says. Decision: test the phone-only setup WITHOUT the order relay first; the
  trade script's own seatbelts (size, oversell, schedule) stay in to catch mistakes. Add the relay only if the test shows a need.
- Jaron 10/6 7:46 AM idea (lead option): Polymarket key in the person's GitHub repo SECRETS. Bot never holds it: the bot
  triggers a GitHub Action (workflow_dispatch API or an order file), the Action runs desk-trade with the seatbelts and places
  the order. = a free relay in their own GitHub. Test: Action start delay (20-60 s), whether Polymarket US accepts orders from
  GitHub runner IPs (geo checks), free minutes (public repo unlimited; private ~2,000/mo), keep logs from printing secrets.
- Test plan (Jaron 10/6 7:49 AM): run HIS OWN desk the phone-only way first. Steps: (1) Jaron makes a NEW Polymarket US API
  key WITH withdraw permission (old key had no withdraw on purpose; withdraw is needed for the X Money sweep) - Notepad
  paste flow at the MSI, when he says; (2) key goes into a GitHub repo's Actions secrets; (3) the trade Action (desk-trade +
  seatbelts) is built; (4) disconnect the MSI connector and have Darios trade only through the app + GitHub; (5) note what
  works. MSI stays the fallback.
- Bonus (Jaron 10/6 8:21 AM): the first 3 of the 10 free setups also get a free week of Claude Pro (his 3 referral passes)
  to help them through setup if needed. (his partner, as candidate #1, would get one this way.)

## Water give-back (Jaron 10/6 9:13 AM, after a fresh Claude held the system to his Live-Reference Principle)
Fresh Claude: the system pays dollars for AI bills but "doesn't return a liter to anyone's reservoir." His answer: a share
of the desk's profit buys water (Grok buys; Claude + the other AIs find where it's needed), donated locally first - Fort
Wayne's homeless. Makes the units match: estimated liters the AIs draw vs liters given, both on the public page, donations
as receipt-backed (yellow) dots. Optional for clients - the people who care how AI sits with this, and want to give back.
To work out: share % (Control Room setting), per-run water estimate (honest ranges, cited), partner shelters, LLC
charitable giving + any grants tied to it. Note: doesn't answer the other critique (profit = other traders' losses).
- Jaron's answer on "profit = other traders' losses" (10/6 9:22 AM): they're right; it's a real flaw of this stage. He owns it
  openly rather than hide it. Path out: over time the system lives on value-creating money (setups, Livi, grants), with the
  desk as the starting engine. Next: state this flaw on the Crew page / setup pitch (flaws first) instead of waiting to be
  confronted.

## Terms and site wording to write (from 10/6 talk; lawyer translates later)
- Assumption of risk: Polymarket is a bet; users choose it knowingly.
- Informed consent: flaws-first page (human losses, bad lanes, small sample, profit comes from other traders at this stage).
- Scope of service: refunds cover the setup fee + subscriptions if the SYSTEM fails, never trading money.
- The counterparty flaw, stated by us first. Water give-back (optional) with receipts.
Fresh-Claude round 3 (10/6 9:30 AM, scratchpad lrp-test/answer3.md) - adjustments to the water idea + selling:
- Water given in Fort Wayne isn't the same pool the data centers draw from: call it a moral offset; real replenishment =
  funding watershed projects in data-center regions. Label both honestly. Add ENERGY too (likely the bigger share).
- Ask local shelters/outreach what they need first (may be fill stations, showers, filtered bottles, laundry, cash). No
  photos of people; receipts + a quote from the partner org, not pictures of aid.
- Selling setups: a profit number next to a sign-up button reads as evidence - keep it beside the flaws. Define "system
  fails" in plain words (software breaks, not money lost). Offer clients an optional loss limit / cooling-off THEY choose.
- Legal consult before any money from others (sports contracts contested federal vs states; advisor rules).
- Later idea (Jaron 10/6): a separate long-shot bot, $0.25+ on 1-5% odds, only when the bankroll can afford it. Not now.
- His pitch for people who fear AI (10/6): "AI is the first technology that lets people stop working for someone else's
  dream - hire AI and go from employee to CEO." The setups are that, made reachable.
- Fee worry (Jaron 10/6 10:45 AM): for people in the fog of life, $25 feels like $100; the fee could be the one wall.
  Ideas: (a) "the system pays your fee" - nothing up front; the $75 comes out of their bot's profit later, only if it makes
  it; (b) pay-what-you-can, $0 allowed; (c) keep some free setups funded by his own desk every month. His data point: AI
  training underrepresents people too busy surviving to generate data - he's the bridge for them.
- Royalty-tip model (Jaron 10/6 10:48 AM, from his music-label days): setup is FREE. Optional: the client's bot tips a % of
  profit (their choice) to a public wallet/tag, any time a set amount is made; can run forever or be switched off a day later.
  Default OFF, chosen privately after setup (not in front of Jaron - people say yes to be polite). Rails: Polymarket US pays
  USD, so a tip = withdrawal -> X Money / Cash App tag / crypto wallet. Lawyer check: a % of trading profit can look like a
  performance fee (advisor rules), even if voluntary.

## Money loop test (Jaron 10/6 4:34 PM) - force it now instead of waiting for next month
Jaron puts Grok's subscription money into Polymarket -> Grok withdraws Polymarket -> X Money -> pays SuperGrok.
- SuperGrok is on Apple IAP (renews Sat 10/10) - he only uses Apple for the declined-charge reminder. Plan: move it to
  grok.com billing paid by the X Money card (cancel Apple renewal after this cycle / when the web plan is live).
- Claude and Codex subs are already on the web (not Apple).
- Needs: new Polymarket key WITH withdraw (at the MSI); confirm Polymarket US withdrawals can land in X Money.
- Ends the X Money "unprompted" test (bots get told) - his call, accepted.
- The ntfy Friday reminder replaces Apple's declined-charge reminder.
- his partner's setup (if she says yes): Grok Bot Pro ($25.99, Grok Bot only) instead of SuperGrok - she doesn't need Grok
  Build/chat. Measures what a Grok-Bot-only plan's usage covers on a Saturday = data for the client cost sheet.

## Accounting note (Vex 10/10): label which water is measured - liters GIVEN to people vs liters RETURNED to a stressed source are different quantities; never imply the second when measuring the first.
