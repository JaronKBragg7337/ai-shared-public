# What runs on the MSI - read-only audit, Tuesday 11/24/2026

Inventory taken 11:41 AM (scheduled tasks, running programs, startup entries, auto-start services). Nothing was changed:
no task disabled, nothing stopped, nothing deleted. No secret files were opened (the Polymarket start script was read with
its key lines blanked out).

## Warnings first

1. **The Polymarket server still starts by itself every time the MSI restarts.** Task "Polymarket MCP" is enabled, runs at
   logon, and loads the live Polymarket key. Its log shows it came up on port 8765 at 7:12 PM Sunday 11/22 after the
   restart. Right now it is not running (nothing is on 8765), but the next restart turns it on again. That goes against
   the 10/28 "Polymarket is DOWN" decision.
2. **"Crypto Consensus" still runs every minute and is wired to place real Polymarket US crypto trades.** Its last real
   trade was 10/25. Since then it has only checked the Polymarket ledger (and failed on most of those checks), but it would
   trade again if a twin bot made a call. Its helpers are still on too: Crypto Notify (every 10 min), Crypto Weekly Caps
   (writes new caps to the Control Room every Monday), Twin Crypto Settle (every 15 min, paper only).
3. **"Desk Schedule Watch" (every 15 min) is in state ON.** It exists to buzz Jaron's phone with "turn Darios + Satya ON"
   for the Polymarket sports desks. "Live Board" (every 5 min) still scrapes Polymarket US game prices for Darios.
4. The all-systems check calls Crypto Consensus, Crypto Notify, Live Board, Desk Schedule Watch and Twin Crypto Settle
   current "money side" jobs, so nothing flags them. The check's Polymarket line also says "Trade Verifier still
   scheduled", but that task is now **disabled**. The wording is out of date.

## Counts

| What | Total | Current | Polymarket / trading | Stale or unknown | Broken |
|---|---|---|---|---|---|
| Scheduled tasks, enabled (ours) | 116 | 87 | 11 (8 Polymarket, 3 paper/alerts) | 18 | 0 real (1 false alarm, counted under current) |
| Scheduled tasks, enabled (vendor: NVIDIA, MSI, OneDrive, Chrome, Windows) | 24 | n/a | - | - | NvNodeLauncher 0x1, OneDrive updater 0x8004EE04 (vendor, ignore) |
| Scheduled tasks, disabled | 30 | all off on purpose (on the check's OFF lists or Drive backups) | 6 trading tasks, all off | - | - |
| Startup entries (Run keys + Startup folder) | 18 | 1 ours (The Cosmos Authority) + 13 vendor apps | 0 | 2 to ask about (Docker Desktop, Slack: set to start but not running) | 2 (Codex Observer x2) |
| Auto-start services (non-Windows) | 25 | 1 ours (Cloudflared tunnel), the rest vendor | 0 | 0 | 0 |
| Our running programs | ~20 | most | 0 running now | 3 groups (see below) | 0 |

## Polymarket / trading items still enabled

| Name | What it does | Evidence | Suggested action |
|---|---|---|---|
| Polymarket MCP (task) | Starts the Polymarket US server on port 8765 with the live key | Trigger = every logon, "run as soon as possible" on. Log: "Uvicorn running on 127.0.0.1:8765" at 11/22 7:12 PM. Task enabled. | **Disable** (keep the files, per "kept, not deleted"). Matches the 10/28 decision. |
| Crypto Consensus (task, every 1 min) | Decides and places real Polymarket US crypto up/down trades from the 3 twin bots' calls | tools/crypto_decide.py, mode LIVE in its log. Last trade placed 10/25. Since then it has only run ledger checks ("fill reconcile skipped" errors on 11/22, 11/23, 11/24). Runs 1,440 times a day. The script's own note says every 5 min, but the task fires every minute. | **Ask Jaron**: is the crypto lane part of "Polymarket DOWN"? If yes, disable. |
| Crypto Notify (task, every 10 min) | Buzzes about crypto lane milestones or "too quiet" | Reads Crypto Consensus results. Its state file last changed today 11:43 AM. | Same answer as Crypto Consensus. |
| Crypto Weekly Caps (task, weekly Mon 5 AM) | Re-sizes each twin's crypto trade cap and writes it to the Control Room | Log on 11/23: "0 settled calls ... cap $29/$29/$31". It has had nothing to do for 4 weeks. | Same answer as Crypto Consensus. |
| Twin Crypto Settle (task, every 15 min) | Scores the twins' PAPER crypto calls (no money moves) | tools/crypto_paper.py settle, summary updated today | Keep if Jaron still wants the paper scores. Otherwise it goes with the crypto lane. |
| Desk Schedule Watch (task, every 15 min) | Buzzes Jaron to turn Darios + Satya ON/OFF in the Grok app for the Polymarket sports desks | state/desk-schedule-watch.json = "ON", written today 11:41 AM | **Ask Jaron**. With Polymarket down these buzzes point him at a dead system. |
| Live Board (task, every 5 min) | Free scoreboard of live Polymarket US games and prices for Darios | Uses the Polymarket venv. state/live-board.md updated 16:43 UTC today. 288 runs a day. | **Ask Jaron** (likely disable while Polymarket is down). |
| Edge Check (task, weekly Mon 5 AM) | Weekly report: did the traders' own estimates match what happened? | Reads old placed trades from Supabase, read-only | Keep (harmless) or retire with the trading desk. |
| HB AI Fund + HB AI Fund Weekly Review (tasks, hourly / weekly) | AI Fund desk, PAPER ONLY, no real orders (built 11/15) | Header: "No GPU, no real orders, no money moves" | Keep (current, not Polymarket). |
| HB Price Alerts (task, every 5 min) | Phone alerts when a coin crosses a price. Never trades. | Coinbase public price only | Keep. |
| Disabled and staying off | Trade Executor, Trade Proposer, Trade Verifier, Polymarket Watchdog, Crypto Wake, Scout Scorer | All disabled | Keep off. Nothing to do. |

## Broken

| Name | What it does | Evidence | Suggested action |
|---|---|---|---|
| CodexObserverServer (startup entry) | Was meant to start an old "Codex Observer" side project at sign-in | Points to G:\My Drive\Codex Coworker\...\start-observer.ps1, which no longer exists. Its Cloudflare relay Worker was deleted 10/28. Fails silently at every sign-in. | **Delete-later** (the all-systems check already says "ask Jaron if still wanted"). |
| CodexObserverCloudflareTunnel (startup entry) | The tunnel half of the same old project | G:\...\start-cloudflare-tunnel.ps1 is missing | Delete-later, together with the one above. |
| HB Remote Keepalive (task, every 5 min) | Restarts the remote-screen helper if it died | Last result 0x1 on every run. That is the script saying "Remote agent already running", which is the normal case, not a fault. It still shows up as "failed" in MSI-STATUS.md. | Keep. Optional fix: make the "already running" exit count as success so the status page stops flagging it. |

No task points at a script that is missing. Every enabled task's file exists.

## Stale / unknown

| Name | What it does | Evidence | Suggested action |
|---|---|---|---|
| Sapling Conversation Restart (one-shot) | Runs `nvidia-smi` then `python -m sapling.heartbeat start` | Set for 10/29 7:31 AM, never repeats. Was triggered again 11/22 12:52 PM (refused, "already running"). If it ever fires it starts Sapling without Sapling's own wake deciding. | **Delete-later** (first one to clean up) |
| Luna phone-setup research (one-shot) | Ran a one-time Codex/Luna research script (Projects\run-luna-phone.sh) | Set for 10/6, script dated 10/5 | Delete-later |
| Sapling Parole 1030 (one-shot) | One-time Sapling "parole" run | 10/15, done | Delete-later |
| Remind LLC filing, Remind SuperGrok renewal (one-shots) | Old phone reminders | Dated 10/7 and 10/9. Both were triggered again 11/22 12:52 PM, during the Windows-update restart. | Delete-later |
| Court 11-10 day before, Court 11-10 week before | Phone reminders for court on 11/10 | Past, ran ok | Delete-later |
| CS Callback Reminder AM / PM | Child-support callback reminders | Ran 11/2, no next run | Delete-later |
| HB BMV Reminder 1113 | BMV buzz (scratch\bmv-buzz.ps1) | Ran 11/13 | Delete-later |
| HB Moment Artifact hb-render, HB Moment MMX Launch | One-time social posts | Ran 10/19 and 10/20 | Delete-later |
| HB Reminder Fog Test, HB Reminder X Premium 1116 | Phone reminders | Ran 11/18 and 11/16 | Delete-later |
| Remind Christmas lights giveaway, Remind Kimi renewal decision, Remind remove X Money card from Apple | Phone reminders | Ran 11/10, 10/30, 10/20 | Delete-later |
| OpenClaw Gateway (task at logon + running program on port 18789) | Starts the OpenClaw gateway (version 2026.7.1, from August) | The all-systems check watches it and restarts it. No doc says what uses it today. Its sibling "OpenClaw Paper Gateway" (paper trading) is off. Running now: 60 MB, light CPU. | **Ask Jaron** whether anything still uses OpenClaw |
| voiced.mjs (running program, no task) | Local voice daemon: keeps the Kokoro-82M speech model loaded and speaks text on request | File in C:\Users\lilli\.claude\voice, dated 8/28. Started at the 11/22 sign-in. **778 MB RAM, ~6,900 CPU-seconds** in 40 h. No AI-Shared doc mentions it. What launches it was not found. | **Ask Jaron** (it holds a lot of memory) |
| 2 leftover log watchers (tail -F + grep, running programs) | Watched today's news render log (rendered-runs.log) for PUBLISH/FAIL | Started 5:20 AM and 5:50 AM today from Claude sessions. `tail -F` never ends by itself. Tiny CPU. | Stop once today's news is confirmed (left over from sessions) |
| Extra Desktop Commander copies (running programs) | Each Claude window/session gets its own copy | 4 local copies besides the "remote" one ChatGPT uses. One set dates from 11/23 8:34 AM. | Keep. They close with their session (restart clears them). |
| Docker Desktop, Slack (startup entries) | Set to open at sign-in | Neither is running now, and no doc lists Docker as a current tool | Ask Jaron. Docker is heavy if it ever does start. |

The 30 disabled tasks are all off on purpose: fly brain x7, AgentWorkbench x2, MachineManager (its Puzzle71 config is
gone), Unfinished Island, Qwen Remote Bridge, OpenClaw Paper Gateway, Paper Sync, Revenue Desk, the 6 trading tasks,
Heartbeat Courier, Postiz Trial Check, HB Socials Outage Retry, Desk Weekly Review, HB Fog Book Research, and the <address> backups (out since 11/24). They cost nothing. Under the "kept, not deleted" rule they can stay. The ones whose
project is gone (MachineManager, Fly School, Unfinished Island) are fine to delete later if Jaron wants a cleaner list.

## Jobs that fire every few minutes

- **Every 1 min:** HB Watch Loop, HB Key Drop, Crypto Consensus (the Polymarket one)
- **Every 5 min:** Crew Publish, MSI Beat, HB Video Drop, HB Price Alerts, Live Board (Polymarket), HB Remote Keepalive
- **Every 10 min:** Crypto Notify, Desktop Commander Remote, Grok Machine MCP (restart check)
- **Every 15 min:** Usage Snapshot, Desk Schedule Watch, Twin Crypto Settle

That comes to about 5,000 short Python starts a day. Each one is small. Turning off the 4 Polymarket-only ones (Crypto
Consensus, Live Board, Desk Schedule Watch, Crypto Notify) would remove about 1,900 of them.

## What keeps the processor busy

- **The Cosmos game server** (node index.mjs): about 15,600 CPU-seconds since 11/23 9:25 AM. That is roughly one sixth of
  one core, all the time. It is current, and it is the biggest steady load of our own.
- **voiced.mjs** (voice daemon): 778 MB RAM, about 6,900 CPU-seconds. It is unknown (see above).
- **Integrity Test Nightly** (1:15 AM, 30 minutes, 30 workers, 8 GB): heavy on purpose (a hardware self-test, 11/22). It
  runs before the "heavy work 3-6 AM only" window. It is not on the all-systems check's lists, but the check's "any other
  job" row still catches it if it fails.
- **MSI Core Yardstick** (11:30 AM daily, a 2-3 minute per-core test): heavy for those few minutes in the middle of the day.
- Sapling heartbeat (python, about 1,600 CPU-seconds) and Ollama are light right now.

## Current (watched by all_systems_check.py or clearly part of a live system)

Scheduled tasks: All Systems Check, HB Watch Loop, HB Key Drop, Crew Publish, MSI Beat, HB Video Drop, Usage Snapshot, HB
News Watchdog, MSI Connector Watch, Creature Watch, HB Safety Signal, MSI Status, Sapling Watch, Sapling Wake, DB Size
Check, MSI Health, HB Live Readings, HB News Desks, Watch Rolling Wire, HB Prep Watch, HB News GPU Guard, HB Rendered News,
Heartbeat News Writer, HB News Paper Book, HB Socials News, HB Socials News Retry, HB Socials Show, the 14 Watch collectors
(Claude Desk, Codex Writer, Funding Lane, MSI Reader, Kimi First Light, Grok Meridian, Grok Blind Spots, DeepSeek Reader,
Perplexity Scout, Missed Story Check, Source Gate, Source Gate Final, Top Stories) + Whats New Scouts, AI-Shared Nightly
Save, Creature Backup, Offsite Backup, Sapling GitHub Sync, Drive Weekly Copy, MSI Core Yardstick, Login Watch, HB Usage
Ledger, HB Build Ledger, HB Render Maintainer, Firsts Roundup, Sapling Status, HB Atlas Convergence, Sapling Quiet Switch,
Stale Sweep, AI Budget Report, Grok Machine MCP, Ollama Server, Sapling Heartbeat, Sapling Relay, Desktop Commander Remote,
HB Remote Keepalive, HB Remote Screen, HB Render Owner Worker, Fable Transcript (new 11/23), Integrity Test Nightly (11/22
self-test), and the future phone reminders: 15 birthday tasks, Court 1-12 day/week before, HB Reminder Google One 0206,
HB Reminder Kimi Web Dec2, Remind SuperGrok move to web.

Running programs: remote_agent.py (one agent; its second python process is the normal venv child), hb-render
owner-worker, Grok Machine MCP server (port 3001), Cosmos server (port 8390) + start-authority + its watchdog, Sapling
heartbeat (7337) + relay (7338), Ollama (11434), Desktop Commander remote, mailbox_wait.py --to fable, the Seam Room
room-agent.mjs waiters (Claude session), usage.py tick.

Startup and services: The Cosmos Authority (cosmos-watchdog.ps1), Cloudflared tunnel service.

## Done 11/24 after going through it with Jaron (12:59 PM - 1:15 PM)
- PAUSED (disabled, files + data kept): Polymarket MCP, Crypto Consensus, Crypto Notify, Crypto Weekly Caps, Twin Crypto Settle, Desk Schedule Watch, Live Board; OpenClaw Gateway (process on 18789 stopped). All in the everything check's off-on-purpose list; OpenClaw dropped from msi-health.py and postboot-check.ps1 port lists.
- TURNED OFF (not deleted): 17 expired one-time reminders. ("Remind SuperGrok move to web" was caught in the sweep by mistake and turned back ON: it fires Sun 1/3/2027.)
- REMOVED: the 2 dead Codex Observer startup entries (values saved in state/removed-startup-entries-2026-11-24.txt); 2 leftover tail -F log watchers; Fable's 2 temp yardstick folders.
- voiced.mjs = Jaron's "Jarvis" read-aloud (Claude Code hooks: SessionStart start-voice, Stop speak-response, Notification speak-notification; daemon on 127.0.0.1:8848, voice bm_george). Reads every Claude reply on the MSI out loud. LEFT RUNNING - Jaron's call.
- Still open for Jaron: Docker Desktop + Slack startup entries (not running).
