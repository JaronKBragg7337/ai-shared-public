# Runs without Jaron - 30-day check (started 10/19 6:52 AM, Jaron on a job-site morning)
Why: court Nov 10 (outcome unknown), the baby due Dec 9. Everything should keep running if Jaron is away or buried in newborn life.
## Decided (Jaron 10/19)
- Bills: THE SYSTEM PAYS (goal). his partner = backup only, and NOT expected: she's 19, a first-time mom; she could, but he won't
  put that on her. So: design for zero human steps; anything his partner-only must be optional, tiny and written step by step.
## To build (next session)
1. Inventory: every recurring bill/subscription (state/subscriptions.json), renewal date, card, and whether it auto-renews from
   money the system controls. Gap list = what still needs a human.
2. Everything that needs a login/reconnect (RECONNECT.md) - which can AIs redo themselves, which can't.
3. What breaks in 30 days with no one checking (alerts go to his phone - who sees them if he can't? second ntfy subscriber?).
4. Decisions only Jaron makes - pre-decide defaults so the system doesn't stall.
5. his partner-GUIDE.md: short, optional, "only if you want to" version.
## Jaron 10/19 6:55 AM
- Grok paid up for a few months; Claude $100/mo; he'll prepay everything for the month he's away.
- Plan: know how long a court absence could last -> keep enough on the auto-pay card for that many months.
  Research (10/19, not legal advice): Indiana civil contempt for support must leave a way to "purge" (pay a set amount and get
  out); jail with no purge path gets reversed on appeal; one Indiana example = 30 days stayed if payments kept; one guide says
  contempt can reach up to 180 days (unverified). -> plan for 1 month, cushion for up to 6.
- Polymarket: needs an API key that can WITHDRAW, so the system can move profit to the bill card on its own. Check what
  Polymarket US's API allows (withdrawals may need his login/2FA) - next session.
## Jaron 7:01 AM (in the truck to Indy)
- All system bills on the X Money card, except Grok: prepaid ~3 months (cancel offer: pay 1 month, get 2 free).
- Polymarket: he'll make a new API key WITH withdrawal enabled (other people's systems do this; his old caution came from AIs
  treating money withdrawals cautiously - not his own rule). Then the system can move money to the X card itself.
- 1-6 months away would be "easy" for him personally; the one hard part is missing the baby's first months. That's the real stake.
- Withdrawal cap: Jaron 10/19 7:04 AM = NO cap. He trusts the AIs to move bigger amounts when something calls for it (e.g. several subscriptions due the same day). Log every withdrawal with its reason (visible on the crew page as yellow 'bill paid').

## Who can move money out (10/19)
- Claude doesn't press withdrawals itself (its own limit, not a rule for the others).
- Polymarket US: no withdraw API for retail keys (tested 10/19) -> only an AI with a browser logged into polymarket.us could do it
  (Grok Bot's cloud computer). Needs Jaron's login on that computer = his call.
- Kraken: withdraw API exists (to destinations saved in the account) -> a plain script on the MSI can do it, and any AI whose
  terms allow it (Grok, DeepSeek, Kimi) can run that script. Best route for automatic bill top-ups.
