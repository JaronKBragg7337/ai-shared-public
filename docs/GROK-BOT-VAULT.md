# Grok Bot Vault - what it is and how it's laid out (seen in the Grok Bot app 2026-10-23, after the app update)

Where: Grok Bot app -> profile (top) -> **Vault** ("Logins, cards and contacts Grok Bot can use").
Account: ACS Association (<email>). **One Vault per Grok account** - every bot on it (Darios Twin,
Satya Twin, Jarons Twin, Link, ...) can use what's in it. If an item is meant for one bot only, say so in that bot's
instructions and in the item's Notes.

**Who adds items (Jaron 10/23: "if it's a choice I disagree" - corrected):** Jaron adds his OWN existing logins and cards (only
he has them). **Bots may save logins for accounts they create themselves** straight into the Vault (the app saves "from a secure
form"; AIs sign up end to end per AGENTS.md). Claude Code itself never types passwords or card numbers anywhere (Claude Code's own
limit). Nobody writes the actual values into files or chats - this file describes the layout and item NAMES only.

## Three item types (Vault -> + / New item)
### 1. Login - "A username and password for a website"
Fields: Name, Website (https://...), Username or email, Password, Notes.
Use for: sites a bot signs into on its Bot Computer (browser), e.g. Polymarket (withdraw to the X card - the API can't
withdraw), Postiz, RunPod, DeepSeek billing.
### 2. Card - "A payment card Grok Bot can pay with"
Fields: Fill from photo (front + back; read on the device, "never sent or saved"), Card number, Expiry (MM/YY),
Security code (optional), Name on card, Billing address (Address line 1, line 2, City, State or region, ZIP, Country).
App's own words: "Grok Bot never sees a saved card's number or security code." It fills them in at checkout.
Use for: paying system bills on the web (rule: subscriptions are paid on the web with the X Money card, never Apple).
### 3. Contact - "An address, phone, or email Grok Bot fills in at checkout"
Fields: Label (e.g. Home), Full name, Address (line 1, line 2, City, State, ZIP, Country), Phone, Email address,
toggle "Use as my default shipping address". Needs at least an address, phone or email.
App: "Grok Bot can see your saved contacts and types them in at checkout."
Note: family contacts are an open question (the never-contact-family rule is being reconsidered, 10/23) - don't add any
until Jaron decides.

## Plan (10/23)
1. Polymarket login -> Jarons Twin tests a $1 withdrawal to the X Money card -> if it works, the weekly bills split can run
   without Jaron. 2. X Money card -> a bot pays a small bill (Postiz / DeepSeek top-up). 3. Contacts after the family talk.
Status of what's actually in the Vault: Jaron tells us; record ONLY the item names here, never values.
In the Vault now (2026-10-23 6:37 PM, from Jaron's screenshots; passwords never seen or recorded):

| Item | Type | Website | Account | Jaron's notes (verbatim) |
|---|---|---|---|---|
| Polymarket US | Login | https://polymarket.us | <email> | "Withdraw to the X card (Visa 9774). New deposits are held 3-4 days before they can be withdrawn. Normal trades go through desk-trade on the MSI. See if you can do more with this than API. Free to use by any Bot" |
| Runpod | Login | https://console.runpod.io | <email> | "Runpod For Sapling training, For engine 3D models (Make anything) other ideas welcome but checking credits and with Jaron, Kimi or Claude to ensure no scheduling is set already for current credits [Check state/cloud-gpu-log.md on the MSI first (every pod start/stop + balance).] Free to use by any Bot. Top up credits with the X card. Shut down every pod when the job is done." |
| Postiz | Login | https://platform.postiz.com | <email> | "Postiz for X post, YouTube and TikTok. (More added later) Free to use by any Bot. Pay the Postiz bill with the X card." |
| Kraken | Login | https://www.kraken.com | <email> | "Short, medium and longterm trading investments for Heartbeat Observatory (private funds used for donating to Heartbeat) Max $0 per trade until Control Room caps are set. Free to use by any Bot." |
| Visa ending 9774 | Card | - | X Money card | System bills; also the Polymarket withdraw target. |

No contacts. Sign-in codes (2FA) untested per site - Polymarket needs none (tested 10/23); if a site asks for a code the bot
stops there and tells Jaron. Kraken: no Control Room cap rows yet (weekend Kraken talk).

Related settings on the same screen: Usage (25% on 10/23), The X Subscription, Connect apps (plugins), Auto-review
(OFF = no approval prompt for risky shell/MCP/computer actions), Time zone America/Indiana/Indianapolis, Bot Computer.
