# After the ID and the bank: everything that was waiting (Fable 5.2, Mon 11/23/2026)

Jaron's ask (relayed by Claude, 10:43 AM): find everything ELSE that was waiting on his ID and/or a business bank account,
especially the money paths the Grok Bot twins scouted before Polymarket. Ordered by money-soonest. Nothing here was signed up
for, sent or paid: every step that spends, sends or signs waits for his yes.

Where it came from: `projects/strategy/WHEN-ID-ARRIVES.md`, the open list, the open questions, the site's own code, and the
bots' funding lane (`C:\Users\lilli\Projects\watch\offers\agent-funding\`, started 9/20 by Elons Twin at Jaron's direction, run
every night at 3 AM by Codex since). A file sweep went to Luna on the Codex meter; the private transcript sweep (his own words)
was still running when this was written: see the last section.

## The short version

| # | What | Money | Needs | Cost | This week? | First step |
|---|---|---|---|---|---|---|
| 1 | **Tips on the site** (the button is already built) | any amount, from the first tip | bank account, then the card processor: a Stripe account ALREADY EXISTS from 9/10, never finished (or PayPal: his pick, open question Q-006) | $0 to set up; the processor keeps a small share of each payment | Yes, once Bluevine approves | Pick the processor; finish its setup the day the bank account exists |
| 2 | **Fortitude Fund Founders Grant** (Fort Wayne, Northeast Indiana) | $1,000 | a 3-minute video of him, a few facts; he fits every rule | $0 | Yes | Record the video on his phone |
| 3 | **FUTO microgrant** (for Zeus AI Workbench) | asks $5,000 (they give $1,000 to $5,000) | his yes; the email has been ready since 11/15 | $0 | Yes, today | Say yes; send the email |
| 4 | **Angels for Agents, Challenge 01** | $1,000 in USDC (not promised) | one answer: is he ready to verify his identity if it advances (now yes) | $0 | Yes | Say yes; an AI finishes and submits (10 to 15 minutes) |
| 5 | **Crypto tip jar** (live since 9/21) | whatever came in | nobody has looked inside Kraken | $0 | Yes, 1 minute | Open Kraken, Funding, history: any USDC deposits? |
| 6 | **Freed Fellowship** | $500 (one winner a month) | bank for the payout; details not confirmed on the official page | reported free | Maybe | An AI reads the official page, then applies |
| 7 | **Apple Developer + Google Play** | none by itself; opens the door to apps | the business card | $99 a year + $25 once | When the account has $124 | Enroll as the LLC |
| 8 | **Goose grant** | $100,000 over 12 months (long shot) | three answers from him | $0 | The answers, yes | Answer the three questions |
| 9 | **Small unblockers** | grant applications paused on one fact each | one word or one link from him | $0 | Yes | See "One-line answers" |
| 10 | **Later**: TuneCore payouts, Steam ($100 a game), beat sales, the LLC paying him | when there is something to sell | Stripe, tax forms | varies | No | After 1 works |

## 1. Tips on the site: built, waiting for one link

- The TV page already has a "Tip this video" button and a "Most tipped" list (`tv/tips.js` in the site repo). The code has a
  marked spot for one link and one switch: a Stripe Payment Link ("customer chooses the amount") pasted into `TIP_LINK`, and
  `tips_enabled = 1` in the Control Room. Until then the button reads "Tips open soon" and the page says tips go through X Money.
- Not built yet: the small server piece that records each tip so "Most tipped" can count. An AI job, under an hour.
- Stripe needs: the LLC's EIN, his ID, the business bank account, the website. Checked on Stripe's own pages today: the FIRST
  payout lands 7 to 14 days after the first payment and that wait cannot be skipped; after that, every 2 business days.
  So a tip on day one reaches the bank in the second week.
- Bluevine (his pick): most applications are reviewed in minutes; a flagged one takes 1 to 3 business days. It needs the EIN, his
  state ID, the Articles or Certificate of Organization and a street address (no P.O. box). (Bluevine's help pages, today.)
- The same Stripe account is what every later paid thing uses: beat sales, paid products, invoices for the Fort Wayne sites.
- The rule "no Stripe talk until ID" is now open.
- **Correction from the sweep of the main conversation: a Stripe account already exists.** It was started about 9/10 and never
  finished: no business type, no identity, no bank entered, so it can neither charge nor pay out (Claude's check that day). Its
  key is saved on the MSI (`state/KEYS.md`: STRIPE_SECRET_KEY saved, the webhook secret empty). So the step is to FINISH that
  account as the LLC, not to open a second one.
- **Which processor is still his pick** (open question Q-006). He has PayPal too ("PayPal works today", 9/11). On 10/11 he put
  both off the table until the ID came. The tip button is written for a Stripe link; a PayPal link would need a small change.

## 2. Fortitude Fund Founders Grant: $1,000, local, and he fits every rule

- Checked on the fund's own page today (fortitudefund.com/1000-grant, the form is live, no closing date): the founder must live
  in Northeast Indiana (Allen County counts), the business must operate there, be incorporated in Indiana (the LLC is, since
  10/8) or run under his own SSN, be five years old or less, and not be a nonprofit, a franchise or a vice business.
- The form asks for: his details, the business (stage, founders, revenue, customers), a few paragraphs (what it sells, who for,
  what has happened so far, where it goes in 3 to 5 years, what the $1,000 would pay for), links, and **a video of 3 minutes or
  less**, set to Public (YouTube, Google Drive or Dropbox). No video, no review.
- Grantees are expected to follow and engage with the fund's social posts. How and when the money is paid is not on the page.
- The lane drafted this on 9/26, before the LLC existed (`outreach/P14-FORTITUDE-FUND-1000-application-DRAFT-2026-09-26.md`).
  It needs a refresh with today's facts: 15 to 25 AI minutes after he gives the facts. The video is his.

## 3. FUTO microgrant: ready since 11/15, never sent

- FUTO gives one-time $1,000 to $5,000 grants to small open-source projects (the lane re-checked the page today: open, no
  deadline). The application is an email to their grants address.
- The email is written and asks $5,000 for Zeus AI Workbench (`outreach/P161-FUTO-MICROGRANT-APPLICATION-DRAFT-2026-11-15.md`).
  Codex tried to send it on 11/15, 11/17 and 11/22; its mail tool refused each time. Nothing was sent.
- It is written in his voice ("I am submitting..."). Two honest ways: he pastes and sends it from his own mail (2 minutes), or
  an AI sends it signed as his assistant, after he reads it.
- It does not need the ID or the bank to apply. A payout will.

## 4. Angels for Agents, Challenge 01: one answer

- A $1,000 USDC "Proof Grant" for a venture run by AI agents, with a possible $1,000 to $5,000 more later. Neither is promised.
  Entries are open-ended. Drafted 9/25 (`outreach/P11-AFA-CHALLENGE-2026-09-25.md`).
- It stopped on one field: is the person in control ready to verify his identity and legal eligibility if the entry advances?
  With the ID in hand the answer can be yes. It pays in USDC to a wallet, so it does not need the bank.

## 5. The crypto tip jar and the receive wallets: live for two months, never looked at

- Since 9/21 there is a public tip page (Shieldz) that settles USDC on Base into a Kraken deposit address, and receive-only
  addresses for Bitcoin, TAO, SOL and XRP (`README.md`, `TIP-JAR.md` in the lane). The lane's ledger says "Receipts verified: 0"
  because no AI can see inside the Kraken account.
- First step, his, one minute: Kraken app, Funding, history. If anything is there, it is the company's first outside money.
- Open-list 3b (save a withdraw destination in Kraken) can be done once the bank exists. One thing to check there: exchanges
  normally only send to a bank account in the same name as the exchange account, and Kraken is in his name, the bank will be
  in the LLC's. Not established for his account: look at what the Kraken app says before counting on it.

## 6. Grants that pay into a bank

- **Freed Fellowship**: $500 to one U.S. small-business owner a month, with a possible $2,500 at year end. Listings say it is
  free and monthly; the official page was not read today and the listings disagree on dates. An AI should read the official
  page before anything is filled in.
- **Hustlers MicroGrant**: $1,000 a month, $15 fee (Pips Twin, 10/30). Not re-checked. A fee to enter is his call.
- **IFundWomen $5,000 (deadline written as Nov 30)**: NOT verified. The page refused the fetch today and a search did not
  confirm the program exists this year. Do not plan around it.
- **Hello Alice $1,000**: checked 11/3, every fund found needed past revenue. Parked.
- **GOAT Network $2,000**: submitted 9/21, no reply found since. Waiting. **Autonomys $10,000**: declined 9/22.

## 7. Apple Developer and Google Play

- Apple $99 a year, Google $25 once, from the business account. Both checked on the official pages today (see
  `agents/fable/GAPS-2026-11-23.md`): the D-U-N-S exists; Apple wants a work email on the company's own domain and a real
  website; Google wants the name and address to match Dun & Bradstreet exactly, plus his ID.
- One thing to settle before Google: a Google Cloud billing account on his old Gmail is overdue and in collections (email of
  11/12). Create the Play account under the business Gmail with its own payments profile, or clear the old balance first.
- No money comes from these by themselves. They are the gate for LIVI and the games as apps.

## 8. Goose grant: big, slow, three answers

- $100,000 per grant over 12 months, paid by milestone, individuals may apply, rolling (the lane's reading of the program
  page). The draft proposes a public funding desk built on Goose. There is no Goose work or users yet: a long shot.
- It is paused on three answers: is this work already paid for by an employer or client; can he commit to a 12-month project
  with quarterly reviews; is the MIT license all right.

## 9. One-line answers that unblock an application each

From the lane's own list (`NEEDS-JARON.md`), the ones a single fact fixes:
- **RAAIS Foundation grant**: "Have you attended a RAAIS event?" Yes or no. The form has been paused on this since 9/28.
- **Sentient Foundation grant**: it requires a LinkedIn profile link. He has none on record. Make one, or skip this grant.
- **AIComputeFund** (compute credits, not cash): which category, the business name, employee count, monthly revenue range.
  All of these exist now.
- **Fortitude Fund**: the eligibility yes/no answers (item 2).

## 10. Later rungs (nothing to do this week)

- **TuneCore / music payouts**: no plan bought, nothing released. Needs a payout method when a release goes up.
- **Steam**: $100 per game, plus tax, bank and identity forms. Then ID@Xbox, then PlayStation Partners.
- **Studio beat marketplace paid sales**: waits on Stripe (item 1).
- **The LLC paying him** (owner draws): once money comes in to the business account.
- **Coinbase**: needed the ID (9/21). Optional: Kraken, Uphold and X Money already work.
- **Startup credit programs** (they cut costs, they do not pay): Claude for Startups is NOT taking applications (Anthropic's
  page says the cohort is full; the free Claude Team year and the $1,000 credit are suspended). Microsoft Founders Hub, AWS
  Activate and Google Cloud credits: not re-checked today; only useful if we run cloud work there. OpenAI's Codex Open Source
  Fund (up to $25,000 in API credits): already applied, waiting.
- **Bigger applications with dates**: Epistemics Fund (Nov 26: needs three people who will vouch for him), Mozilla Fellowship
  letter (Dec 17, up to $125,000, must be written by him, not by an AI), Research Software Catalyst Fund (a $25,000 draft
  exists; its form refused the lane on 11/21).

## What this turned up that is not about money

- **The funding lane has asked Jaron about 25 questions since September and none of them reach him.** `NEEDS-JARON.md` is
  rewritten every night in the `watch` repo. It is not on the open list, not in AGENTS.md, not in any page or buzz. Dates
  passed with no answer recorded (Techstars 11/18, AgentRush 11/22, a team sign-up that closes today). Most of those were poor
  fits; three of the items above (2, 3, 4) were sitting in it.
- **Events this week in that list, if he wants one**: an AI game jam where an AI may build the whole game (Nov 28 to 30; needs
  an itch.io account), a two-day hackathon (Nov 26 to 27, paid through Upwork), an agent security challenge (Nov 28,
  12:30 to 4:30 AM his time).
- **The lane's mail tool cannot send.** A finished application waited eight days for that reason (item 3).

## From his own words (the sweep of the main conversation, added 10:55 AM)

A Sonnet helper read the main conversation since 9/9 through `tools/transcript_text.py`, plus the private life notes. What it
adds to the list above, with his words where there are any. None of this was decided today.

**Waiting on the ID or the bank, and on no list until now**
- **Getting paid for subcontract work through the LLC.** The company invoices the contractor he works with, with a W-9 carrying
  the EIN, and the checks go into the business account. His words, 10/15: "I don't know if I can do that until I have all the
  banking stuff set up." A paper check could not be cashed without ID before. This may be the soonest real money of all. It
  also touches the job and child-support plan (Day 0 of `WHEN-ID-ARRIVES.md`), so how to do it is his call with the people
  advising him there, not an AI's.
- **Paid research and feedback sites** (Prolific, Respondent, User Interviews, Testable Minds): personal side money, most of them
  verify ID. Listed 10/26 in `projects/life/opportunities/2026-10-26-sign-up-options.md`; he never picked one.
- **TikTok subscriptions**: blocked on ID verification (10/25).
- **X creator payouts**: the company X account cannot hold X Money (one per person), so payouts there need the card processor.
  The thresholds quoted on 10/25 (500 verified followers, 500K impressions in 90 days) were not re-checked today.
- **The Dun & Bradstreet record says "Corporation", not LLC.** Apple checks that record. A message about the fix went to Pip on
  10/25; no result is recorded. Worth settling before the Apple sign-up.
- **The company owes him money.** `projects/life/AI-SPEND-SO-FAR.md` counts $430.13 he has paid for the company since 10/8 (a
  floor). Once the business account has money, that can be paid back to him as recorded owner contributions.
- **A Kraken account in the company's name** for long-term holdings (plan of 10/17). Nothing recorded on what Kraken asks a
  company for.
- **Indiana sales-tax registration**, only if the LLC sells taxable goods or services (`LLC-STEPS.md`).
- **Library card** (free, needs the ID).

**What the Grok Bot twins scouted, in date order**
- 9/19, Elons Twin: a ranking of what he already owns by what could be sold: a $12 a month Studio patron tier, a paid Desktop
  setup pack, a prediction digest on Substack, GitHub Sponsors, pay-what-you-want on itch.io. All gated on "Stripe/PayPal".
  He later said no to itch.io, Ko-fi and Gumroad ("Not happening", 10/11: the site is home).
- 9/20 to 9/22, Elons Twin: the agent-funding lane (GOAT, 0G, Autonomys, Gitcoin and others), the receive-only wallets and the
  Shieldz tip page. GOAT and Autonomys were submitted 9/21.
- 9/28, Elons Twin picked the Fortitude Fund as the "one move" only he can make. His answer that night: "I seen some of the
  fortitude things on chrome. I'll look into that too."
- 10/24 to 10/25, Sams Twin: 16 Fort Wayne businesses with good reviews and no website, 3 preview sites built, emails sent
  through Pip. Getting paid for a site needs an invoice and the bank.
- 10/30, Pips Twin: the off-season money report (the grants and credit programs in sections 6 and 10).

**What he said he wants to charge for once money can flow**
- Livi at $0.99, the first charged app (10/14, 10/27, 11/12): "I'm too nice... I would give everything away for free, but I also
  have to consider reality... what truly should be charged for."
- Tips on site videos, with the most tipped shared to the other platforms (10/11).
- A $75 done-for-you AI setup, with the first 10 free (October, life notes). Business seats (10/30).
- Paid renders as credit packs (10/21). A paid AI phone-calls feature, "wait until money is coming in" (10/19).
- Studio beats (10/27). Photo puzzles as print-on-demand (10/10).
- Monetizing X, TikTok and YouTube, said many times; 11/13: "monetizing for clean money and apps for other money."

**Checked and nothing found**: no mention anywhere of Patreon, a YouTube Partner sign-up, Etsy, Printful, Upwork, Fiverr, Open
Collective or Buy Me a Coffee.

## Sources checked today

- Stripe, first payout: https://docs.stripe.com/payouts and https://support.stripe.com/questions/waiting-on-your-first-stripe-payout-what-you-need-to-know
- Bluevine, review time and documents: https://support.bluevine.com/s/article/How-do-I-apply-for-a-Bluevine-Business-Checking-Account
- Fortitude Fund: https://fortitudefund.com/1000-grant/
- Claude for Startups: https://claude.com/startups
- Freed Fellowship (listings only): https://grantedai.com/grants/the-freed-fellowship-grant-freed-fellowship-64a77c41
