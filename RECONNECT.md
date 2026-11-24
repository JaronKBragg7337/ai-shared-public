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

## 5. A new key (Polymarket, Claude API, Kraken...) - Key Drop, from your phone (since 10/19)
1. On your phone open **heartbeatobservatory.com/admin/keys/** (admin login) and pick the key's name (or "Other").
2. Paste the key there. It is encrypted in your browser for the MSI only; the MSI task "HB Key Drop" (every 2 min) files it, tests it, wipes it and buzzes you.
3. Done. The list of keys on the MSI (names + tested status, never values) is state/KEYS.md.
   (Older way, still works at the MSI: press the site's **Copy** button, tell Claude **"copied"**, or double-click the desktop icon Claude made.)

## 6. Grok Build login on the MSI
**Sign it's needed:** the login watch says "Grok Build login" needs you. Renews itself as long as it's used.
1. Open the black window.
2. Type `C:\Users\lilli\.grok\bin\grok login` and press Enter.
3. A browser page opens. Sign in to your X / Grok account and allow it.
4. The black window says you're signed in. Close it.

## 7. ChatGPT can't reach the MSI (Desktop Commander)
**Sign it's needed:** the login watch says Desktop Commander is "not running". **Since 11/16 this should fix itself:** the "Desktop Commander Remote" task (tools/dc_remote_keepalive.ps1) checks at login and every 10 min and restarts it if it's gone (log: scratch/dc-keepalive.log). Only do the steps below if that log says START FAILED.
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
| Polymarket / Kraken keys | until revoked (new ones 10/19 via Key Drop) |
| Postiz channels (TikTok / YouTube / X) | until a platform asks you to sign in again (section 10) |

**The MSI itself going dark (since 11/22):** an alarm that lives on Cloudflare, not on the MSI, buzzes your phone once
("MSI went dark") if the MSI stops checking in for 20 minutes, and once more ("MSI is back") when it returns. Then follow section 12.

---
Not sure which one it is? Tell Claude what you see. If it's a new kind of break, Claude adds a numbered section here the same day.

## 8. Kimi Code CLI login on the MSI
**Sign it's needed:** Claude says Kimi CLI is logged out.
1. Claude starts `kimi login --region global` and sends you a link + code.
2. Open the link on your phone, sign in to Kimi (the Allegretto account), enter the code, approve.
3. Claude sees "Logged in" and tests it. Done.

## 10. Postiz (company socials auto-posting) - first setup DONE 10/17; use this only if a channel drops
(Postiz free trial ends 10/24, then $29/mo; Jaron knows. TikTok, YouTube and X are connected; Claude's CLI is signed in.)
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

## Claude Code sign-in on the MSI (hb-render owner lane) - added 2026-10-21
**UPDATE 10/21 9:40 PM (Claude Code): not needed for the owner lane any more** - the worker now uses CLAUDE_CODE_OAUTH_TOKEN (long-lived, from `claude setup-token`) from keys.env. Only redo this if that token stops working (then: `claude setup-token` on the MSI, paste via Key Drop).
The owner lane at heartbeatobservatory.com/render/anything/ runs your own "make anything" requests through
Claude Code on the MSI (your subscription, no API credits). It stopped with "OAuth access token has expired.
Re-authenticate to continue." - the saved CLI login needs a refresh. One-time, on the MSI:
1. Open a terminal (Windows key, type "PowerShell", Enter).
2. Type `claude auth login` and press Enter. A browser window opens on claude.ai.
3. Sign in with your Claude account (<email>) and press Allow.
4. Back in the terminal it prints "logged in". Close it. The hidden worker (task "HB Render Owner Worker")
   picks the next request up by itself within 5 s; nothing else to restart.
Check: `claude auth status` shows loggedIn true; a request on the page then says "your lane (subscription): working".

## Phone shows "session archived" / "Remote control session is offline" (fixed 10/23)
Usually the chat is NOT archived on the MSI - only the phone link dropped. Any other Claude Code session on the MSI can fix it, no MSI trip:
1. Find the chat: session list tool (main thread = the pinned one, running since 9/9).
2. Send it one short message (wakes it - Remote Control needs an active turn first).
3. Turn Remote Control on for that session; check it reads "on".
4. Jaron backs out of the dead screen on his phone and reopens the chat from the list.

## Cloud Claude can't reach a repo ("repo_access_denied" / push 403) - added 11/4/2026
Cause: the Claude GitHub app is set to "Only select repositories" and the repo isn't on the list (since the Fable repo was added, only that one is).
1. On your phone, open github.com/settings/installations (signed in as JaronKBragg7337).
2. Tap **Configure** next to **Claude**.
3. Under **Repository access**, either pick **All repositories**, or tap **Select repositories** and add **heartbeat-observatory** and **ai-shared** (keep Claude-cloud---fable-).
4. Tap **Save**. Tell Claude "done" and it relaunches the cloud jobs.

## 12. The MSI is stuck at the sign-in screen after a restart - added 11/22/2026
**Sign it's needed:** your phone buzzes "MSI went dark", or everything on the MSI stops after a Windows update. The MSI is on
but shows the sign-in screen (press the power button first if the screen is black).
**Right now:** sign in on the MSI like normal. Everything comes back by itself within about 5 minutes - the everything check
runs at every sign-in and restarts each part.

**So it stops happening (one time, about 2 minutes, at the MSI, signed in).** Why: auto sign-in was turned on 9/11, but the
boot records show it has never worked once since - every restart waited for a person (9/15 1h20m, 9/23 1h30m, 10/11 33 min,
11/22 3 hours). The saved password most likely doesn't match (the PIN typed instead of the password, or the password changed).
1. Press the **Windows key + R**, type `netplwiz`, press Enter. Click **Yes** if Windows asks.
2. Click the account (**lilli**) in the list.
3. The box **"Users must enter a user name and password to use this computer"**: if it's empty, check it and click **Apply**
   first. Then uncheck it.
4. Click **Apply**. A small box asks for the password twice. Type the account **password** (not the PIN), both times.
   Click **OK**, then **OK**. (Only know the PIN, not the password? Stop and tell Claude - don't guess.)
5. Open **Settings > Accounts > Sign-in options**, find **"Use my sign-in info to automatically finish setting up after an
   update"** (under Additional settings) and turn it **On**.
6. Test it: **Start > Power > Restart**, then walk away. Tell Claude "restarted". Claude watches from the outside; it should
   come back to the desktop on its own in about 2 minutes. If it stops at the sign-in screen again, tell Claude.
Nobody else needs to touch the MSI for this. Claude never sees or types the password.
After signing in, Chrome may ask "who's using Chrome". You don't need to pick: within about 3 minutes the everything check opens Chrome in Jaron's profile (where the AIs' Claude, Kimi and ChatGPT browser extensions live) and closes the picker.
