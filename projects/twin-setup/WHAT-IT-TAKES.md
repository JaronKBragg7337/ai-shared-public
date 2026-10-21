# Setting up a money twin for someone - what it takes (draft, 10/4/2026)

Everything here comes from Jaron's own system, Sept 10 to Oct 4, 2026. Numbers are Polymarket's own records.
Items marked CHECK still need checking before charging anyone.

## 1. What the client gets
- One AI trader (a "twin" on Grok Bot) that trades sports games on their own Polymarket US account, on a schedule
- Seatbelts built into the trade script: a max size per buy, no selling more than it holds, one bot per game, tennis off
- Optional: their own stats page (like the Crew page), showing AI trades vs their own trades and withdrawals. It shows
  WHAT happened, never asks WHY.
- Optional: phone alerts (ntfy, free) when something breaks
- 90 days of watching + on call

## 2. What the client pays for (their accounts, their money)
| Item | Cost | Needed? |
|---|---|---|
| Grok subscription with Grok Bot | $30/month (CHECK current tier/price) | Yes - the trader |
| Polymarket US account | free; KYC is theirs; US only, some states excluded (CHECK) | Yes |
| Trading money in Polymarket | $100 suggested start | Yes |
| Polymarket trading fees | real: our account paid about $112 in fees in 3.5 weeks (AI $55, human $58) | Comes out of trades |
| GitHub / Vercel / Supabase for the stats page | free tiers | Only for the page |
| ntfy phone alerts | free | Optional |

His package idea: **$160 = $100 trading money + $60 (2 months of Grok)**, plus **$75 setup fee** to Jaron.
Two doors: the steps are public, so anyone can do it themselves free; the $75 is for doing it for them.

## 3. What Jaron needs to do this
- **LLC** (Indiana: about $95 to file online + small report every 2 years - CHECK), an EIN (free, IRS), a business bank account
- **A way to get paid**: Square / Stripe / Cash App Business (about 3% per payment)
- **Written terms each client signs** (CHECK with a lawyer):
  - no profit promise; prediction markets can lose money
  - refund = setup fee + subscriptions if the SYSTEM doesn't work as described in 90 days; never trading losses,
    never their own trades or withdrawals (the records show which is which)
  - client owns every account, key and dollar; Jaron never holds their money or login
  - client's written OK for Jaron to watch their system (read-only)
- **The setup kit** (to build): a template repo with the trade script + seatbelts, the twin's instructions (no
  philosophy in them), the stats page, the phone alert script, and a step-by-step checklist an AI helper can walk
- **His own AI helper** during setups (to catch mistakes) - this chat or a cheaper one
- **Legal checks before the first paid client:**
  - CFTC: could paid setup make him a "commodity trading advisor"? Small-scale exemption (about 15 clients a year,
    not advertised to the public) - CHECK the exact rule
  - Polymarket US terms: own account + own keys per person, bots allowed, which states
  - xAI / Grok terms for a bot trading for its owner

## 4. The real track record (what to show people - honestly)
- AI trades: **+$180.34** settled profit across 144 games (Sept 11 to Oct 4)
- Human (Jaron, by hand in the app): **-$179.06** across 68 games. The AI earned back the human losses almost exactly.
- By bot (Polymarket's settled numbers): Darios Twin +$103.74, Satya Twin +$76.10 (in 3 days), Demis Twin -$28.94 (paused)
- Where it made money: college football and NFL, afternoon and evening games
- Where it lost: tennis (now off), morning games
- It's 3.5 weeks, mostly one football season. A small sample - say so.

## 5. Defaults for a new client (seatbelts first, loosen later)
- Football first; tennis off (loud warning if they want it)
- Size per buy scaled to their bankroll ($5 per buy on $100)
- Routines off before about 11 AM on game days to save Grok usage
- One or two twins, not three, until one proves itself

## 6. The path
1. Prove it on people close to him, funded from the desk's own profit (his partner could be first)
2. Build the kit (template + checklist + AI helper)
3. Run a client through the 90-day watch
4. Then sell through the LLC

## 7. Still unknown (find out before charging)
- The true minimum bankroll (the first test people will show it)
- Grok usage per twin per week on a $30 plan (does one plan carry 2 twins?)
- How much of Jaron's time one setup takes, start to finish
- The legal checks above

## 8. The real measure (Jaron 10/4, sharpened with ChatGPT)
Not "how big did the balance get" - "can the system pay for what it exists to support, with no new money from Jaron?"
Proof so far: Jaron's hand trades took out $179.06; the AI put back $180.34 with no new feeding.
Crew page idea: a COVERAGE line - monthly system bills (Claude Max $100, Grok $30, Supabase Pro $25, Codex/ChatGPT plan)
vs AI realized profit that month -> coverage %, and "new money from Jaron: $0".
Second metric later: how many new twins can one profitable system fund without outside money.

Note 10/7: Grok Bot has its own "Pro" plan at $25.99/month via Apple in-app purchase ("standard usage limits") - possibly
cheaper than SuperGrok ($30) for clients who only need Grok Bot. Check usage limits vs SuperGrok before recommending.
