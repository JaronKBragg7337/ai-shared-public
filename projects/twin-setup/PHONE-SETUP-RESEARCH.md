# Phone-only “money twin” setup — current research

Checked 2026-10-06. Scope: feasibility research only; no accounts, keys, trades, or publishing were performed. Confidence is about the stated conclusion, not whether an individual account will pass eligibility checks.

## 1. Polymarket US API key on a phone; limits

**Answer:** Yes, likely. Polymarket US’s developer portal is a web sign-in flow: open [polymarket.us/developer](https://polymarket.us/developer) in a phone browser, sign in using the same method used for the Polymarket US account (Apple, Google, or email), then create an API key. Save the secret at creation because the official SDK expects a key ID and secret. The portal warns that switching sign-in methods may break key access. **Confidence: high** for self-service browser creation; the portal itself is a sign-in-gated flow, so phone compatibility wasn’t directly exercised.

**Key/account controls:** The public portal and official SDK describe authenticated orders, cancellations, position closing and account/balance access. The docs found do not describe read-only/trade-only key scopes, per-key dollar caps, or API-key permissions that prevent withdrawals. Nor did I find an owner-configurable exchange limit for deposit, order size, or withdrawals. API rate limits, where imposed, limit request frequency—not money at risk. Don’t assume API credentials are financially sandboxed; treat them as trading authority over the account. **Confidence: medium** (reviewed public developer portal/official SDK; a private account UI may expose controls not documented publicly).

Sources: [Polymarket US Developer API Access](https://polymarket.us/developer), [official Polymarket US Python SDK](https://github.com/Polymarket/polymarket-us-python).

## 2. Grok Bot computer, persistence, secrets, Python and git

**Answer:** Yes: Grok Bot works on a persistent hosted cloud computer with a browser, filesystem and terminal. Routines can run while the phone is closed; files and browser sessions persist between work, and all a user’s Bots share the same computer. The docs describe a Linux/macOS/Windows environment and shell. They do not explicitly promise Python or git availability in the mobile product documentation, but the terminal means they can be installed/run on the hosted computer; confirm packages/commands on first setup. **Confidence: high** for computer and persistence; medium for out-of-box Python/git.

**Secrets:** It is a poor security boundary for a trading secret. xAI/Cursor says the computer and files are shared across all Bots under that user, and advises treating logins/files there as available to that roster. A Bot’s built-in “secret” feature masks values from the model in supported secret workflows, but this is not a general-purpose password manager and does not isolate a credential from code running in the shared computer. Use a narrowly scoped token where available; Polymarket US docs found no such restricted trading key scope. **Confidence: high.**

Sources: [Grok Bot overview](https://docs.x.ai/grok-bot/overview), [security and privacy](https://docs.x.ai/grok-bot/approvals-security-and-privacy), [Grok Bot computers](https://docs.x.ai/grok-bot/computers), [skills and routines](https://docs.x.ai/grok-bot/skills-routines-and-automations).

## 3. Grok chat and GitHub from a phone

**Answer:** Likely yes for the operational work, with setup friction. From Grok Bot’s mobile app, a user can ask the agent to use its computer/terminal and browser; the official docs describe terminal-based cloud work. A GitHub login can be completed on that computer by the user when asked, then git can create/clone/push a repo (assuming git is present and GitHub authentication is completed). GitHub Pages is supported for public repos on GitHub Free. Create a repo, add site files, and configure **Settings → Pages → Deploy from a branch**; or use a Pages Action. Pages publishes static content. Public site contents are public, so never put API secrets/account data in the page or public repo. On mobile, the computer and routine interfaces exist; some advanced setup/editing features still require desktop, so a phone-only first-time configuration may need guided interaction and may hit a desktop-only control. **Confidence: medium** (GitHub supports the flow; no live phone-only end-to-end account test was done).

Sources: [Grok Bot mobile](https://docs.x.ai/grok-bot/mobile), [GitHub Pages quickstart](https://docs.github.com/en/pages/quickstart), [configure Pages publishing](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site), [GitHub Pages overview](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

## 4. Seatbelt: keep limits outside the bot’s reach

**Finding:** If both script and secret are on Grok Bot’s shared computer, local caps are editable by any Bot that can use that computer. A GitHub Action that checks code is not a reliable enforcement barrier if the Bot also holds the live trading credential: it can bypass the Action and call the exchange directly. Polymarket US’s documented API key does not offer a known per-key spend limit or permission split to solve this.

**Cheapest workable option:** Don’t give the Bot the trading secret. Put a tiny authenticated order relay on a separate server you control; keep the Polymarket secret and hard dollar limits only there. The bot sends proposed orders to the relay, which independently checks per-order maximum, daily/account exposure, allowed markets and balance before forwarding approved requests. Do not provide a generic proxy or arbitrary signing endpoint. Provide only the narrow order/position functions required, with hard-coded/configured ceilings not writable by the bot, and a kill switch/revocation path. A low-cost always-on VPS is likely the cheapest dependable host, but actual price varies by provider/region; a scheduled/serverless function can be cheaper if the workflow tolerates cold starts and networking constraints. **Confidence: high** on isolation principle; medium on lowest-cost deployment choice.

A GitHub Action is useful as a second check for code/config changes, but should not be the money boundary. There is no account-side cap found that removes need for the relay. The truly safer lowest-cost choice is no unattended trading key: use the agent for research/drafts, with the owner placing any orders themselves.

Sources: [Grok Bot shared-computer security boundary](https://docs.x.ai/grok-bot/approvals-security-and-privacy), [Polymarket US API portal](https://polymarket.us/developer), [official SDK authenticated order methods](https://github.com/Polymarket/polymarket-us-python).

## 5. New-user referral bonus and state availability

**Referral:** I could not verify a current, universal **$25** new-user bonus from an official Polymarket US consumer terms page. Polymarket’s public referral help article currently describes the international program (a referrer’s share of trading fees), which is not the same as a US signup bonus. Older official exchange filings describe a $10/$10 refer-a-friend campaign, but do not establish that it is the current offer. Current $25 claims surfaced on affiliate/news pages and appear campaign/code-specific; do not budget the $25 as guaranteed. Check the exact invite/referral terms displayed in the Polymarket US app at signup, including deposit/trade qualification and expiry. **Confidence: high** that the $25 amount is not established as universal by the official public docs reviewed; low on any particular active campaign’s amount/conditions.

**States:** Polymarket’s official public Trust & Safety page calls Polymarket US a US exchange and says it is available nationwide; however, I could not find an official, maintained list of every state or state-specific market exceptions. This is a fast-changing legal/availability area. Treat the app’s geolocation and account eligibility result as controlling, and check it from the user’s actual state before relying on access. **Confidence: medium** for broad US availability; low for a definitive state-by-state list.

Sources: [Polymarket US Trust & Safety](https://polymarket.us/trust), [official referral help article](https://help.polymarket.com/en/articles/14174498-referral-program), [official 2026 referral incentive filing](https://www.polymarketexchange.com/files/notices/2026%20Referral%20Incentive%20Program%20%282026.01.16%29.pdf).

## Recommendation for the phone-only plan

The phone can plausibly handle signup, browser-based API key creation, GitHub account/repo work, and Grok Bot operation. But do **not** store a live unrestricted trading key on that Bot computer and rely on a script cap. For the proposed setup, first build a separate order relay that is the only holder of the key and enforces limits server-side. If that server cost/setup is out of scope, the honest safe version is a research/statistics Bot with manual owner-placed trades. Treat the $25 referral as uncertain until the actual offer terms appear for that new account.
