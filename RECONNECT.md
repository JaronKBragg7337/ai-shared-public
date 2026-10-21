# Reconnect sheet - when something logs out or disconnects, follow the steps

For Jaron. No dev words. Every fix that needs you gets a numbered list here, the first time it happens.
"Black window" = PowerShell: press the Windows key, type **PowerShell**, press Enter.
Never paste a key or token into a chat. The desktop buttons save them for you and clear your clipboard.

---

## 1. Claude login for the MSI's own jobs (the morning Anthropic scout)
**Sign it's needed:** Claude says "Claude login expired" or "claude setup-token". Lasts about a year once done.
1. On the MSI, open the black window.
2. Type `claude setup-token` and press Enter.
3. A browser page opens. Sign in to Claude if it asks, then click **Authorize**.
4. Go back to the black window. It shows a long line starting with `sk-ant-oat`.
5. Highlight that whole line with the mouse and press **Ctrl+C**.
6. Easiest: tell Claude **"copied"**. Claude saves it from the clipboard, tests it, and clears the clipboard.
   (Or yourself: press **Windows key + D** to see the desktop, find the icon named **SAVE CLAUDE TOKEN**, double-click it,
   and a box says "Saved ... and it works.")
7. Close the black window. Done. (Done 2026-10-08 9:06 AM.)

## 2. ChatGPT / Codex login on the MSI
**Sign it's needed:** Claude says Codex (Luna or Sol) is logged out.
1. Open the black window.
2. Type `codex login` and press Enter.
3. A browser page opens. Sign in with your ChatGPT account and allow it.
4. The black window says you're logged in. Close it. Done.

## 3. Claude chat / Grok chat / ChatGPT can't reach the MSI
**Sign it's needed:** the chat app says it can't reach the MSI or can't find tools.
1. Make sure the MSI is on and awake (it may have restarted for an update).
2. Open the black window.
3. Type `Start-ScheduledTask "Grok Machine MCP"` and press Enter.
4. Wait one minute, then try the chat again.
5. ChatGPT's Desktop Commander only: also type `npx @wonderwhy-er/desktop-commander@latest remote` and press Enter. Leave that window open.

## 4. Claude Code on your phone won't connect
1. On the MSI, open the Claude app.
2. Send any message ("hi") in the session.
3. After it answers, the phone works again.

## 5. A new key (Polymarket, Claude API, Kraken...)
Claude opens the right page on the MSI screen and makes a desktop button named **PASTE ... KEY** / **SAVE ... KEY**.
1. On the page, press the site's **Copy** button next to the new key.
2. Tell Claude **"copied"**. Claude saves it, tests it and clears your clipboard.
   (Or yourself: **Windows key + D** shows the desktop; double-click the icon Claude named, and a box says "Saved".)

## 6. Grok Build login on the MSI
**Sign it's needed:** the login watch says "Grok Build login" needs you. Renews itself as long as it's used.
1. Open the black window.
2. Type `C:\Users\lilli\.grok\bin\grok login` and press Enter.
3. A browser page opens. Sign in to your X / Grok account and allow it.
4. The black window says you're signed in. Close it.

## 7. ChatGPT can't reach the MSI (Desktop Commander)
**Sign it's needed:** the login watch says Desktop Commander is "not running". It stops every time the MSI restarts.
1. Open the black window.
2. Type `npx @wonderwhy-er/desktop-commander@latest remote` and press Enter.
3. If it asks you to sign in: a browser page opens, enter your email, get the code from your email, type it in.
4. **Leave that black window open** (minimize it). Closing it disconnects ChatGPT.

## 0. The Claude app itself logged you out (the one you already know)
1. Open the Claude app. It asks for your email.
2. Type your email, open the code Claude emails you, type the code in.
3. Done. (This is different from section 1, which is only for the MSI's background jobs.)

---
## 9. Sapling (the seed AI on the MSI) from your phone
**URL:** https://heartbeatobservatory.com/admin/sapling/  (also linked from the /admin page as "Sapling").
**Sign in:** the same owner login as the Control Room: open https://heartbeatobservatory.com/admin, enter your email and
password, then open the Sapling link. Signed out or not admin = the page only shows "Sign in at /admin". Nobody else can read
it or talk to it (the data is locked to admins; the MSI has no open door - it reaches out to the site itself).
What you can do there: chat, flip a rule switch (that is your edit of the rule file, logged), see heartbeat/energy/exams/tick
log/stop reports, see the checkpoint archive and bring one back ("Restore"), and **Restart (parole)** after it stopped itself.
**If the page says "relay silent since ..." or chat gets no answer in 90 s:**
1. On the MSI, open the black window.
2. Type `Start-ScheduledTask "Sapling Relay"` and press Enter.
3. Wait 20 seconds, reload the page. (On the MSI itself the page is http://127.0.0.1:7338/ - no login there, it is your machine.)
**If the heartbeat itself is down** (page says "heartbeat process is down"): press **Restart (parole)** on the page. That is the
only way it comes back after a self-stop - on purpose (you decide parole). Logged as parole_start next to its stop report.

## How you find out (so nothing sits broken for days)
The **Login Watch** checks all of these once a day (5:50 AM) and buzzes your phone with the section number to follow.
Full list with dates: `state/logins.md`.
| What | Lasts |
|---|---|
| Claude login for MSI jobs | about 1 year (made 10/8/2026) |
| Codex (Luna/Sol) | renews itself when used |
| Grok Build | renews itself when used |
| Claude chat / Grok chat / Grok Bot -> MSI connector | 30 days from last use, renews when used |
| ChatGPT -> MSI (Desktop Commander) | until the MSI restarts or the window closes |
| GitHub | until revoked |
| DeepSeek / Claude API keys | until the money runs out |

---
Not sure which one it is? Tell Claude what you see. If it's a new kind of break, Claude adds a numbered section here the same day.

## 8. Kimi Code CLI login on the MSI
**Sign it's needed:** Claude says Kimi CLI is logged out.
1. Claude starts `kimi login --region global` and sends you a link + code.
2. Open the link on your phone, sign in to Kimi (the Allegretto account), enter the code, approve.
3. Claude sees "Logged in" and tests it. Done.

## 10. Postiz (company socials auto-posting) - first setup, then only if a channel drops
**Sign it's needed:** ntfy buzz "Socials: Postiz isn't connected yet", or state/social-posts.log says "not signed in".
First setup (one sitting, ~10 min, on the phone or the MSI):
1. Open platform.postiz.com > Sign up > **Continue with Google** > pick **<email>**.
2. Plan: **Standard** (5 channels, about $29/mo, 7-day free trial). Pay on the web with the **X Money card** (never through Apple).
3. In Postiz: **Add Channel > TikTok** > sign in as **@heartbeat.observa** > Allow.
4. **Add Channel > YouTube** > pick the **Heartbeat Observatory** brand channel > Allow.
5. **Add Channel > X** > sign in as **@HeartbeatObserv** > Authorize app. (If Postiz asks for X developer keys instead, stop and tell Claude.)
6. Tell Claude "Postiz is set". Claude starts `postiz auth:login` and sends you a link + code; open it, approve. Claude posts one test and checks all three.
If later one channel shows "disconnected" in Postiz: tap it > Reconnect > sign in as that company account again.

## 11. The Claude Code conversation disappeared from your phone (remote session dropped)
**Sign it's needed:** the session is gone from the Claude app on your phone.
1. At the MSI, type any short message in the Claude Code conversation (e.g. "back") and send it.
2. The remote session reconnects; the conversation shows up on your phone again.
Read-only fallback (untested): Steering > Tools > AI Tests opens a claude.ai link that may bring you back into the conversation to read it.
