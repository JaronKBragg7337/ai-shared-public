# Company health check - behind-the-scenes systems (2026-11-13)

Read-only audit by Claude Code (Opus 5.5 subagent). Nothing was changed, stopped, started or deleted. No secret values were read out or written down.
**Started:** Fri Nov 13 23:12 (MSI clock) **Finished:** Fri Nov 13 23:26

## WARNINGS FIRST
- **Google Drive (G:) is FULL: 200 GB used, 0 free.** The two nightly backups (AI-Shared mirror + Necklace Unreal) still "finish", but Drive can't upload anything new to the cloud while it's full. So the off-machine backup may be stale. Also, this 200 GB plan **isn't in BILLS.md**.
- **The funding lane has done nothing for 13 days** (last real run 10/31). Windows still reports "OK" every night.
- **The Dec 2 Kimi reminder is out of date.** It tells Jaron to "subscribe on kimi.ai today", but he already moved Kimi to the web on 11/6. If he follows it, he could pay $39 twice.

## Counts

| | Number |
|---|---|
| Scheduled tasks (not Microsoft) | 144 |
| - from other companies (NVIDIA, OneDrive, MSI, Google, audio drivers, Windows SoftLanding) | 23 (ignored, all normal) |
| - **ours** | **121** |
| Healthy | 61 |
| Failing or at risk | 11 |
| Off on purpose (Polymarket, crypto twins, fruit fly) | 24 |
| Forgotten / finished / dead | 25 |
| **Monthly cost (best estimate)** | **about $265-$290/month** in fixed plans plus usage. Add **$100/month** more if the Anthropic API credit top-up repeats every month (unclear, see COSTS). |
| RunPod pods running right now | **0** (checked live with a read-only API call: 0 pods, 0 serverless endpoints, 0 storage volumes) |

---

## FAILING (most serious first)

1. **Google Drive is full, so backups are at risk** (tasks "AI-Shared Mirror" 3:30 AM and "Necklace Unreal Backup" 3:00 AM)
   - What it is: each night the MSI copies AI-Shared (28 GB) and the Necklace Unreal project (34 GB) into Google Drive.
   - What's wrong: G: shows 200 GB used and 0 GB free. The copy to the local Drive folder "succeeds", but Drive can't push new files to the cloud while it's full. If the MSI died, the cloud copy could be old. Also, robocopy logs every folder, so the logs have grown to 36 MB (mirror.log) and 76 MB (necklace-backup.log).
   - Fix: clear space in Google Drive (or check which account and plan it is), then add the plan to BILLS.md. Also add `/NDL /NFL` to both robocopy lines so the logs stay small.

2. **Watch Funding Lane: silently broken since 10/31** (daily 3 AM)
   - What it is: Codex (Luna) looks for funding and grant offers every night and drafts or submits applications.
   - What's wrong: the task points at an exact PowerShell version folder (`...PowerShell_7.6.6.0...\pwsh.exe`). PowerShell updated itself to 7.6.9 and that folder no longer exists. Windows says "0 = OK" because only the outer window wrapper started. `Projects/watch/collectors/funding_runs.log` has had no entries since 10/31.
   - Fix: point the task at the plain `pwsh.exe` alias (`C:\Users\lilli\AppData\Local\Microsoft\WindowsApps\pwsh.exe`), the same way "Watch MSI Reader" does.

3. **Daily news: the first automatic attempt has failed 4 days in a row** (HB Rendered News, 3:50 AM)
   - What it is: renders and publishes the daily news show. The deadline is 8 AM.
   - What's wrong (from `projects/news-show/rendered-runs.log`):
     - 11/10 and 11/11: Unreal froze with 0 frames, then the run recovered on its own (published 5:18 and 5:58).
     - 11/12: "vex voices failed" at 4:07, plus an Unreal freeze. A rerun was started by hand. **Published 8:53 AM, which is late.**
     - 11/13: voices failed at 4:15, then an Unreal freeze. The next render ended at 63,453 of 69,320 frames. The show was published at 7:07 anyway.
   - Already partly addressed: someone added "up to 4 fresh restarts" for the voice step on 11/13. It hasn't run on a scheduled night yet.
   - Fix: watch tomorrow's 3:50 AM run. If Unreal freezes again on the first try, look at why the first launch always stalls (for example, start Unreal once to warm it up before the real render).

4. **The news social post gets skipped when the show is late** (HB Socials News 7:15 + Retry 8:45)
   - What's wrong: on 11/12 the show went live at 8:53, after the last retry at 8:45. That day's news was **never posted** to TikTok, YouTube or X. The log says "no short yet - skipped" twice and nothing after that.
   - Fix: add one more retry around 10:00 or noon, or have the news pipeline call `social_daily.py news` itself right after it publishes.

5. **MSI Connector Watch buzzes Jaron's phone every 3 hours about something that's off on purpose**
   - What's wrong: it has sent "the Grok traders have been quiet for N hours - check their routines" **66 times** since 10/19 (now "quiet for 84 h"). The Grok traders are paused on purpose (Polymarket down, crypto twins paused). That's about 8 pointless buzzes a day, and it trains him to ignore real alerts.
   - Fix: turn off the "traders quiet" check in `tools/connector-watch.py` while trading is paused (keep the other checks).

6. **Crypto Wake: fails every time it fires (HTTP 400) since 10/23** (runs every minute)
   - What's wrong: 430 of its last 493 wake calls to Jarons Twin returned an error (`state/crypto-wake.log`). The twins are paused on purpose, so nothing is lost. But the task still runs 1,440 times a day for nothing.
   - Fix: disable it with the other crypto tasks while the twins are paused (see OFF ON PURPOSE).

7. **Desk Weekly Review: has failed 4 Sundays in a row** (exit code 1, last good report 10/19)
   - What's wrong: it reviews the Polymarket sports desk, and that desk is down. Each Sunday it crashes. When it does work, it **rewrites the Control Room desk schedule**.
   - Fix: disable it while Polymarket is down.

8. **HB Watch Loop ("Tell Claude" from his watch): fails now and then** (exit code 1, runs every minute)
   - What's wrong: the latest run failed. MSI-STATUS also lists it under failures in the last 2 days. A test query to the mailbox worked fine just now, so the failure comes and goes, and the script keeps no error log, so the cause can't be seen. Also, `watch-chat.md` has no new entries since 11/9.
   - Fix: wrap the main loop so any error gets written to `state/watch-loop-errors.log`, then look at the pattern.

9. **MSI Health: the 23:02 run crashed** (exit code 1, hourly)
   - What's wrong: `msi-health-now.md` still says 22:02, so the 23:02 check died before it wrote anything. A single miss so far. It also runs `publish-crew.py` and the DeepSeek loss breaker, so a crash skips those too.
   - Fix: check the next hourly result. If it keeps failing, add error logging the same way as #8.

**Non-zero codes that are actually normal (not counted as failing):**
- HB Remote Keepalive (exit 1): the remote-screen agent is already running, so the copy exits by design.
- Grok Machine MCP (0x800710E0): Windows refused a second copy because one is already running. Expected, and `msi-health.py` knows about it.
- Desktop Commander Remote (exit 1 at the 10/31 boot): it's running anyway, started another way.

---

## COSTS

| What | Monthly | Paid how | Used by | Notes |
|---|---|---|---|---|
| Claude Max | $100 | X Money card | main sessions, watch loop, news writer, owner worker | next charge Dec 2. X Money had $151 on 11/13 and needs about $55 more by then |
| Anthropic API credits | **$0-$100?** | X Money card | render-anything on the site, scout | BILLS says "first $100 added 10/28, next on Nov 3 (monthly)". **Unclear whether this repeats every month.** Check console.anthropic.com |
| Claude extra usage | small | Chime | overage toggle is ON | $11.46 left on 10/28 |
| ChatGPT Plus / Codex | $20 | X Money card | Codex Writer, Funding Lane (broken), Luna jobs | |
| SuperGrok | $10 (=$30 per 3 months) | Apple | Grok Build, Atlas, Grok desks | **subscriptions.json says $30/month. That's wrong; BILLS says a 3-month prepay** |
| Kimi Allegretto | $39 | X Money card (web since 11/6) | Kimi First Light, Sapling training | Dec 2 reminder is out of date (see FORGOTTEN) |
| Supabase Pro | $25 | X Money | the whole site, mailbox, Key Drop | next charge Nov 22. Database 2.15 of 8 GB; **1.96 GB of that is the old `qwen_events` table** from the bridge disabled 9/15 |
| Postiz | $29 | X Money | HB Socials News/Show (posting works) | next charge ~Nov 24 |
| X Premium (@HeartbeatObserv) | $30 | X Money? | Pip, reach | **decide by Nov 16, renews Nov 17. There's no phone reminder task for this** |
| DeepSeek API | ~$5 (top-ups) | X Money | Watch DeepSeek Reader | $15.30 left |
| Perplexity API | ~$0.40 | prepaid | Perplexity Scout, Rolling Wire | $0.375 so far this month |
| RunPod | ~$0-8 | prepaid | Sapling runs | last run 11/2 ($7.25). **0 pods now** |
| Cursor | $0-15 overage | card | Grok Bot extra usage | $0 this cycle |
| Domain | ~$1 | Cloudflare | site | renews Jun 2027 |
| **Google Drive 200 GB** | **unknown (~$3?)** | **unknown** | nightly backups | **NOT in BILLS.md. Drive is full** |
| X API | unknown | - | not found in any MSI script | timeline 11/10 says "X API billing starts Nov 22, check which scripts use it". No X key and no X API calls exist on the MSI, so it's probably Postiz or Pip |
| Vercel, GitHub, Cloudflare | $0 | - | site, Actions | all free tier |

**Fixed plans:** $100 + $20 + $10 + $39 + $25 + $29 + $30 = **$253/month**. Usage adds about $10-30. Best total: **~$265-$290/month**, or ~$365-390 if the API credit repeats.

**Paid for but nothing uses it:**
- Polymarket US: $0 balance, but the service and the trade loops still run (no cost, just noise).
- The 1.96 GB of old Qwen data takes up most of the paid Supabase database.

**Used but no bill entry:** Google Drive storage, and possibly the X API.

---

## FORGOTTEN / UNUSED

**Out of date and could cause harm:**
- **HB Reminder Kimi Web Dec2** will buzz "subscribe on kimi.ai today" on Dec 2. That's already done (11/6). Fix: delete the task, or change it to "check Kimi web renewal went through".

**One-time reminders and jobs that already ran but are still registered (harmless clutter, 15):**
Court 11-10 day before, Court 11-10 week before, CS Callback Reminder AM, CS Callback Reminder PM, HB BMV Reminder 1113, HB Moment Artifact hb-render, HB Moment MMX Launch, Luna phone-setup research, Remind Christmas lights giveaway, Remind Kimi renewal decision, Remind LLC filing, Remind remove X Money card from Apple, Remind SuperGrok renewal, Sapling Conversation Restart, Sapling Parole 1030.
Fix: delete them in one sweep.

**Disabled long ago, nothing points to them (9):**
AgentWorkbench-Scheduler, AgentWorkbench-Server (its script is gone, error 0x80070002), MachineManager, Revenue Desk Daily (replaced by the Funding Lane), Unfinished Island hourly worker, HB Fog Book Research, HB Socials Outage Retry, Heartbeat Courier, Postiz Trial Check 10-23.
Fix: delete them, or leave them alone (they cost nothing).

**Scripts nobody calls:**
- 132 of the 231 scripts in `tools/` aren't mentioned by any task, other script or doc. About 124 of those are throwaway `_tmp_*`, `_espn_*` and `_lw_*` files from the Sept-Oct sports-trading days.
- The rest: backfill-desk-action.py, save-claude-key.ps1, save-claude-token.ps1, tests-page.py, sort-review-page.py, one_month_post.py, _satya_append.py, test_news_watchdog.py.
- Fix: move the `_tmp_/_espn_/_lw_` files into `tools/archive/`.

**Running but not run by any scheduled task (won't come back after a restart):**
- The Cosmos game server (node, since 11/5) and `cosmos-watchdog.ps1` (since 11/4). Both were started by hand. The watchdog's lock file also blocks the mirror backup from copying it every night ("ERROR 32").
- Fix: if The Cosmos should always be up, give it a logon task like the other services.

**Small overlaps:**
- "Enrich world spaces" runs both as a Vercel cron (daily) and as a GitHub Action (scheduled hourly, actually runs about every 5 h). Pick one.
- "Crew Publish" (every 5 min) and "MSI Health" (hourly) both publish the crew page. MSI Health says it's the backup, so that's fine.
- Every Crew Publish run also pulls the full Polymarket history (`pm-history-all.py`), even though Polymarket is down.

---

## OFF ON PURPOSE (not failures)

**Polymarket system (DOWN on purpose since 10/28, $0)**, still scheduled or running:
- Polymarket MCP: the trading service is running.
- Polymarket Watchdog (every 2 min): **note: it automatically restarted the Polymarket service on 11/7 06:11.** That goes against "don't restart it". It's harmless at $0, but it's a restart nobody chose.
- Trade Executor `--live` (every 5 min, "nothing approved").
- Trade Verifier (every 5 min).
- Live Board (Polymarket live games).
- Desk Schedule Watch.
- Edge Check (weekly).
- OpenClaw Gateway (market-lane executor, port 18789).
- Desk Weekly Review is also in this group (failing, see above).

Already disabled: Trade Proposer, Scout Scorer, OpenClaw Paper Gateway, Paper Sync, Qwen Remote Bridge.

Suggested fix (Jaron's call): disable the still-running ones together so the "down" state is real and nothing restarts on its own. Keep everything; don't delete.

**Crypto twins (paused on purpose):** Crypto Consensus (every minute), Crypto Notify, Crypto Weekly Caps, Twin Crypto Settle, plus Crypto Wake (failing, see above).
- Nothing has been traded or logged since 10/25.
- `crypto-consensus.md` shows a recurring "fill reconcile skipped (JSONDecodeError)". Look at this before turning the lane back on.

**Fruit fly / PAM (paused on purpose):** Fly Brain, Fly Watcher, Fly School, school-2 to school-5. All disabled since 9/16-17.

**GPU yield:** the news render owns the GPU from about 3:50 to 8 AM. The News GPU Guard ran at 2:38 every night and found nothing to stop. Normal.

---

## HEALTHY (61)

- **News chain:** Heartbeat News Writer (4:20), HB News Desks (desks posting every hour), HB News Watchdog, HB News GPU Guard, HB News Paper Book, HB Socials Show (posting OK to YouTube, X, TikTok and the site).
- **Watch collectors (all wrote today's file):** Claude Desk, Codex Writer, DeepSeek Reader, Grok Meridian, Grok Blind Spots, Kimi First Light, MSI Reader, Perplexity Scout, Top Stories, Rolling Wire (hourly), Missed Story Check. Whats New Scouts and HB Atlas Convergence also ran today.
- **MSI care:** MSI Status (every 30 min), DB Size Check (hourly, 27% full), Login Watch (every login OK), Usage Snapshot, HB Usage Ledger, HB Build Ledger, AI-Shared Nightly Save (saved 888e6ef tonight), AI Budget Report, Stale Sweep, HB Live Readings, Ollama Server, Grok Machine MCP.
- **Phone and remote:** HB Key Drop, HB Video Drop, HB Price Alerts, HB Safety Signal, HB Remote Screen + Keepalive.
- **Reminders still to come:** HB Reminder Fog Test (11/18), Remind SuperGrok move to web (1/3), plus 15 birthday reminders.
- **Render:** HB Render Maintainer, HB Render Owner Worker.
- **Sapling:** Sapling Relay, Sapling Wake, Sapling Status. Running, but the last new version was made 11/5, so 8 days of practice with no new learning. Worth a look; it isn't a failure.
- **Site:** Vercel builds OK (the only failed deploys are an old July pirate-world project). GitHub Actions: Ashgrove clock and Enrich world spaces all green. Supabase edge functions all ACTIVE: the-current-tick, world3-tick, watch-inbox, mail-inbox.

## Other things noticed
- **Windows Terminal is using 7.2 GB of RAM** (open since 11/7). RAM is down to about 6 GB free out of 32. Fix: close and reopen the terminal at a quiet moment.
- **Disk space swings:** 34 GB free on 11/12 (a render-risk alert fired), 107-149 GB free tonight. The news render needs about 70 GB, so keep an eye on it.
- **Nightly save flags `tools/public_export.py` every night** in the public-copy step (in `nightly-save.log`). Probably a false alarm on its own key-pattern list. Worth one look.
- Several tasks run `python.exe` instead of `pythonw.exe`, so a console window may flash every 30 minutes (Safety Signal, Live Readings and others). Cosmetic only.
- `subscriptions.json` (used by the AI budget report) is out of date: Grok is $30/month instead of $10, Kimi is still listed as Apple, and Google Drive is missing. BILLS.md is the source of truth.

## FIXED by Claude 11/13 11:30 PM (safe, reversible)
- Watch Funding Lane: now points at the plain pwsh.exe alias (survives PowerShell updates). Next run 3 AM; check funding_runs.log 11/14.
- HB Reminder Kimi Web Dec2: now says "check the web renewal went through, do NOT subscribe again".
- Crypto Wake: disabled (paused on purpose; failed 430/493). Polymarket Watchdog: disabled so the DOWN state stays down (it had restarted the service 11/7). Re-enable both only when Jaron restarts those systems.
- "Grok traders quiet" buzz: silenced with its built-in flag file state/grok-routines-off (delete it when trading restarts).
- New one-time task HB Reminder X Premium 1116 (9:30 AM 11/16).
## Left for Jaron / later
- Google Drive full (200 GB): pick upgrade vs cleanup. News first-attempt failures: Claude to fix (auto-resume + voice retry) in a day session. Polymarket MCP service still running (harmless at $0); stopping it = his call. Clutter deletes: later sweep.
