# Everything check - is every part of the MSI OK? (newest run on top)

Runs by itself: daily 7:45 AM, after a restart, and when the network comes back (task "All Systems Check", tools/all_systems_check.py). It restarts only what is safe, through each part's own task, and buzzes Jaron only if something is still broken after that. `--why` lists every check.

<!-- run -->
## Mon Nov 23 09:56 AM - 2 broken: Nightly news pipeline, Backups and saves

**Still broken:**
- **Nightly news pipeline** - HB Socials Show last ran 11-21 17:00 _(not sent to the phone; listed for Claude)_
- **Backups and saves** - Sapling GitHub Sync last ran 11-21 18:17; Drive Gentle Fill last ran 11-30 00:00 _(not sent to the phone; listed for Claude)_

**Internet and website**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Internet | the MSI can reach the internet at all | names resolve (heartbeatobservatory.com, ntfy.sh, github.com) |
| OK | Website pages | the 10 main pages of heartbeatobservatory.com load | all 10 pages answer 200 |
| OK | Today's news show | the daily show is live (by 8 AM) | today's show is in the index and its video loads |
| OK | Database (Supabase) | the database behind the mailbox, Control Room and news answers | database answers (AI mailbox read worked) |
| OK | The creature | her world (Cloudflare Worker) is up and her clock moves | alive, tick 5600 (was 5564 at the last Creature Watch) |
| OK | MSI dark alarm | buzzes Jaron if the MSI goes quiet 20 min (off, or stuck at the sign-in screen) | watching from Cloudflare: last check-in 1 min ago, its own check ran 1 min ago |

**Reaching the MSI**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | MSI connector (Grok Machine MCP) | the bots and chat AIs can reach the MSI | server up on 3001, public address answers 401 (401 = up, asking for sign-in) |
| OK | Cloudflare tunnel | carries the connector and Cosmos to the internet | tunnel service running and ready |
| OK | The Cosmos game server | the Cosmos world server and its watchdog | game server healthy on 8390 and public; watchdog running; 1 restarts today |

**Programs on the MSI**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Ollama (local model) | the local Qwen model server | Ollama answers (200) |
| OK | OpenClaw gateway | the OpenClaw gateway | OpenClaw answers (200) |
| OK | Sapling heartbeat | Sapling's training heartbeat | heartbeat answers on 7337 |
| OK | Sapling relay | carries messages between the Sapling page and Sapling | relay answers (200) |
| OK | Desktop Commander remote | ChatGPT's way into the MSI | Desktop Commander remote running |
| OK | Remote agent | Claude's remote screen/keepalive helper | remote agent running |
| OK | Render worker | the hb-render owner worker (renders jobs) | render worker running |
| OK | Grok Bot app | the bots (Darios, Satya, Jarons Twin) need its window open | Grok Bot app running |
| OK | Chrome (Jaron's profile) | AIs that drive the browser use the extensions in Jaron's Chrome profile | Chrome is open in a profile (the AIs' browser extensions can connect) |
| OK | Claude mailbox waiter | wakes the main Claude session when mail arrives | mailbox waiter running |
| OK | Seam Room listener | Claude's ear in the Seam Room (re-armed by the Claude session) | Seam Room listener running |

**The machine**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Google Drive (G:) | the off-MSI copy of AI-Shared and the Necklace project goes through it | G:\My Drive is mounted (nightly AI-Shared + Necklace backups can run) |
| OK | Disk space | room for the nightly news render (~70 GB) | 184 GB free |
| OK | GPU heat | the MSI isn't overheating | 49C, 0% busy |
| OK | Power and memory | plugged in, enough RAM | plugged in, battery 90%, 14.0 GB RAM free |
| OK | Windows restart pending | updates waiting for a restart | no restart pending (up since Sun Nov 22 4:13 PM) |
| OK | Database size | Supabase stays under its 8 GB cap | 2.19 GB of 8 GB (27%) / biggest: qwen_events 1999MB, fly_school 136MB, cosmos_terrain_bricks 19MB |
| OK | Logins | every login the system uses still works | all logins fine (checked 2026-11-23 09:50) |
| OK | AI-Shared saved to GitHub | this folder is backed up | in step with origin/main |
| OK | Watch repo saved to GitHub | the news watch repo is pushed | in step with origin/master |

**Scheduled jobs**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | HB Watch Loop | answers Jaron's "Tell Claude" watch messages by ntfy | last run 11-23 09:55, result 0 |
| OK | HB Key Drop | files and tests API keys Jaron pastes on his phone | last run 11-23 09:55, result 0 |
| OK | Crypto Consensus | crypto decision tick (money side) | last run 11-23 09:55, result 0 |
| OK | Crew Publish | publishes the public system/crew page | last run 11-23 09:55, result 0 |
| OK | MSI Beat | checks in with the off-MSI alarm on Cloudflare (quiet 20 min = one buzz) | last run 11-23 09:55, result 0 |
| OK | HB Video Drop | picks up videos dropped for the site | last run 11-23 09:52, result 0 |
| OK | HB Price Alerts | price alerts (money side) | last run 11-23 09:51, result 0 |
| OK | Live Board | the live data board | last run 11-23 09:53, result 0 |
| OK | Crypto Notify | crypto notices (money side) | last run 11-23 09:53, result 0 |
| OK | Usage Snapshot | the AI usage meter | last run 11-23 09:48, result 0 |
| OK | Desk Schedule Watch | desk schedule check (money side) | last run 11-23 09:41, result 0 |
| OK | Twin Crypto Settle | settles the twin's paper crypto (money side) | last run 11-23 09:54, result 0 |
| OK | HB News Watchdog | buzzes if today's news isn't live (7 AM-noon) | last run 11-23 09:45, result 0 |
| OK | MSI Connector Watch | buzzes if the connector/Cosmos/relay is down | last run 11-23 09:44, result 0 |
| OK | Creature Watch | looks in on the creature (read-only) | last run 11-23 09:33, result 0 |
| OK | HB Safety Signal | safety level from the DHS feed | last run 11-23 09:29, result 0 |
| OK | MSI Status | writes state/MSI-STATUS.md | last run 11-23 09:49, result 0 |
| OK | Sapling Watch | watches Sapling (read-only) | last run 11-23 09:45, result 0 |
| OK | Sapling Wake | Sapling's own wake | last run 11-23 09:35, result 0 |
| OK | DB Size Check | database size vs the 8 GB cap | last run 11-23 09:25, result 0 |
| OK | MSI Health | hourly task/port health | last run 11-23 09:02, result 0 |
| OK | HB AI Fund | AI fund (money side) | last run 11-23 09:17, result 0 |
| OK | Hourly helpers | live readings, news desks, rolling wire, prep watch | all 4 ran on time and finished ok |
| BROKEN | Nightly news pipeline | GPU guard 2:38, render 3:50, writer 4:20, paper book 9:05, socials 7:15/8:45/5 PM | HB Socials Show last ran 11-21 17:00 |
| OK | Nightly news collectors | the Watch ... collectors and What's New scouts | all 14 ran on time and finished ok |
| BROKEN | Backups and saves | Drive mirror 3:30, nightly save 22:55, creature 21:15, Unreal 3:00, Sapling GitHub 18:17, Drive gentle fill 21:00 | Sapling GitHub Sync last ran 11-21 18:17; Drive Gentle Fill last ran 11-30 00:00 |
| OK | Other daily jobs | login watch, usage ledger, build ledger, render maintainer, firsts, Sapling status, atlas | all 8 ran on time and finished ok |
| OK | Weekly jobs | stale sweep, AI fund review, budget report, edge check, crypto caps | all 5 ran on time and finished ok |
| OK | Any other job | catches failures in jobs not listed above (vendor and one-shot reminders skipped) | no other job failed in the last 2 days |

**Off on purpose**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| SKIPPED-ON-PURPOSE | Polymarket system | trading on Polymarket is off since 10/28 | Polymarket system is DOWN by Jaron's 10/28 decision - never restarted here; trading tasks still disabled; Polymarket MCP task Running (last run 2026-11-22); Trade Verifier still scheduled and ends 1 because nothing real answers on 8765 (state/verifier.md 1.3 MB); NOTE something else is on 8765 - is Polymarket MCP running again?; Connector Watch's Polymarket restart is off |
| SKIPPED-ON-PURPOSE | Paused projects | fly brain and retired helpers stay off | 20 paused tasks (fly brain, old gateways, retired desks), all still off |
| SKIPPED-ON-PURPOSE | Codex Observer | an old Codex side project | Codex Observer server + tunnel (Registry Run entries) - not checked; ask Jaron if still wanted |

<!-- run -->
## Mon Nov 23 07:45 AM - 3 broken: Google Drive (G:), Nightly news pipeline, Backups and saves

**Still broken:**
- **Google Drive (G:)** - Google Drive is running but G: is not mounted - the nightly AI-Shared and Necklace backups to Drive can't run. If it's running but unmounted, its index went bad again: close Drive, rename %LOCALAPPDATA%\Google\DriveFS\<account>\metadata_sqlite_db* aside, start Drive (fixed this way 11/22)
- **Nightly news pipeline** - HB Socials Show last ran 11-21 17:00 _(not sent to the phone; listed for Claude)_
- **Backups and saves** - Sapling GitHub Sync last ran 11-21 18:17 _(not sent to the phone; listed for Claude)_

**Internet and website**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Internet | the MSI can reach the internet at all | names resolve (heartbeatobservatory.com, ntfy.sh, github.com) |
| OK | Website pages | the 10 main pages of heartbeatobservatory.com load | all 10 pages answer 200 |
| OK | Today's news show | the daily show is live (by 8 AM) | today's show is in the index and its video loads |
| OK | Database (Supabase) | the database behind the mailbox, Control Room and news answers | database answers (AI mailbox read worked) |
| OK | The creature | her world (Cloudflare Worker) is up and her clock moves | alive, tick 5394 (was 5375 at the last Creature Watch) |
| OK | MSI dark alarm | buzzes Jaron if the MSI goes quiet 20 min (off, or stuck at the sign-in screen) | watching from Cloudflare: last check-in 0 min ago, its own check ran 0 min ago |

**Reaching the MSI**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | MSI connector (Grok Machine MCP) | the bots and chat AIs can reach the MSI | server up on 3001, public address answers 401 (401 = up, asking for sign-in) |
| OK | Cloudflare tunnel | carries the connector and Cosmos to the internet | tunnel service running and ready |
| OK | The Cosmos game server | the Cosmos world server and its watchdog | game server healthy on 8390 and public; watchdog running; 0 restarts today |

**Programs on the MSI**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Ollama (local model) | the local Qwen model server | Ollama answers (200) |
| OK | OpenClaw gateway | the OpenClaw gateway | OpenClaw answers (200) |
| OK | Sapling heartbeat | Sapling's training heartbeat | heartbeat answers on 7337 |
| OK | Sapling relay | carries messages between the Sapling page and Sapling | relay answers (200) |
| OK | Desktop Commander remote | ChatGPT's way into the MSI | Desktop Commander remote running |
| OK | Remote agent | Claude's remote screen/keepalive helper | remote agent running |
| OK | Render worker | the hb-render owner worker (renders jobs) | render worker running |
| OK | Grok Bot app | the bots (Darios, Satya, Jarons Twin) need its window open | Grok Bot app running |
| OK | Chrome (Jaron's profile) | AIs that drive the browser use the extensions in Jaron's Chrome profile | Chrome is open in a profile (the AIs' browser extensions can connect) |
| OK | Claude mailbox waiter | wakes the main Claude session when mail arrives | mailbox waiter running |
| OK | Seam Room listener | Claude's ear in the Seam Room (re-armed by the Claude session) | Seam Room listener running |

**The machine**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| BROKEN | Google Drive (G:) | the off-MSI copy of AI-Shared and the Necklace project goes through it | Google Drive is running but G: is not mounted - the nightly AI-Shared and Necklace backups to Drive can't run. If it's running but unmounted, its index went bad again: close Drive, rename %LOCALAPPDATA%\Google\DriveFS\<account>\metadata_sqlite_db* aside, start Drive (fixed this way 11/22) |
| OK | Disk space | room for the nightly news render (~70 GB) | 177 GB free |
| OK | GPU heat | the MSI isn't overheating | 52C, 0% busy |
| OK | Power and memory | plugged in, enough RAM | plugged in, battery 90%, 14.9 GB RAM free |
| OK | Windows restart pending | updates waiting for a restart | no restart pending (up since Sun Nov 22 4:13 PM) |
| OK | Database size | Supabase stays under its 8 GB cap | 2.19 GB of 8 GB (27%) / biggest: qwen_events 1999MB, fly_school 136MB, cosmos_terrain_bricks 19MB |
| OK | Logins | every login the system uses still works | all logins fine (checked 2026-11-23 07:20) |
| OK | AI-Shared saved to GitHub | this folder is backed up | in step with origin/main |
| OK | Watch repo saved to GitHub | the news watch repo is pushed | in step with origin/master |

**Scheduled jobs**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | HB Watch Loop | answers Jaron's "Tell Claude" watch messages by ntfy | last run 11-23 07:44, result 0 |
| OK | HB Key Drop | files and tests API keys Jaron pastes on his phone | last run 11-23 07:44, result 0 |
| OK | Crypto Consensus | crypto decision tick (money side) | last run 11-23 07:44, result 0 |
| OK | Crew Publish | publishes the public system/crew page | last run 11-23 07:45, result 267009 |
| OK | MSI Beat | checks in with the off-MSI alarm on Cloudflare (quiet 20 min = one buzz) | last run 11-23 07:45, result 0 |
| OK | HB Video Drop | picks up videos dropped for the site | last run 11-23 07:42, result 0 |
| OK | HB Price Alerts | price alerts (money side) | last run 11-23 07:41, result 0 |
| OK | Live Board | the live data board | last run 11-23 07:43, result 0 |
| OK | Crypto Notify | crypto notices (money side) | last run 11-23 07:43, result 0 |
| OK | Usage Snapshot | the AI usage meter | last run 11-23 07:41, result 0 |
| OK | Desk Schedule Watch | desk schedule check (money side) | last run 11-23 07:41, result 0 |
| OK | Twin Crypto Settle | settles the twin's paper crypto (money side) | last run 11-23 07:39, result 0 |
| OK | HB News Watchdog | buzzes if today's news isn't live (7 AM-noon) | last run 11-23 07:45, result 0 |
| OK | MSI Connector Watch | buzzes if the connector/Cosmos/relay is down | last run 11-23 07:44, result 0 |
| OK | Creature Watch | looks in on the creature (read-only) | last run 11-23 07:33, result 0 |
| OK | HB Safety Signal | safety level from the DHS feed | last run 11-23 07:29, result 0 |
| OK | MSI Status | writes state/MSI-STATUS.md | last run 11-23 07:19, result 0 |
| OK | Sapling Watch | watches Sapling (read-only) | last run 11-23 07:45, result 0 |
| OK | Sapling Wake | Sapling's own wake | last run 11-23 07:35, result 0 |
| OK | DB Size Check | database size vs the 8 GB cap | last run 11-23 07:25, result 0 |
| OK | MSI Health | hourly task/port health | last run 11-23 07:02, result 0 |
| OK | HB AI Fund | AI fund (money side) | last run 11-23 07:17, result 0 |
| OK | Hourly helpers | live readings, news desks, rolling wire, prep watch | all 4 ran on time and finished ok |
| BROKEN | Nightly news pipeline | GPU guard 2:38, render 3:50, writer 4:20, paper book 9:05, socials 7:15/8:45/5 PM | HB Socials Show last ran 11-21 17:00 |
| OK | Nightly news collectors | the Watch ... collectors and What's New scouts | all 14 ran on time and finished ok |
| BROKEN | Backups and saves | Drive mirror 3:30, nightly save 22:55, creature 21:15, Unreal 3:00, Sapling GitHub 18:17 | Sapling GitHub Sync last ran 11-21 18:17 |
| OK | Other daily jobs | login watch, usage ledger, build ledger, render maintainer, firsts, Sapling status, atlas | all 8 ran on time and finished ok |
| OK | Weekly jobs | stale sweep, AI fund review, budget report, edge check, crypto caps | all 5 ran on time and finished ok |
| OK | Any other job | catches failures in jobs not listed above (vendor and one-shot reminders skipped) | no other job failed in the last 2 days |

**Off on purpose**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| SKIPPED-ON-PURPOSE | Polymarket system | trading on Polymarket is off since 10/28 | Polymarket system is DOWN by Jaron's 10/28 decision - never restarted here; trading tasks still disabled; Polymarket MCP task Running (last run 2026-11-22); Trade Verifier still scheduled and ends 1 because nothing real answers on 8765 (state/verifier.md 1.3 MB); NOTE something else is on 8765 - is Polymarket MCP running again?; Connector Watch's Polymarket restart is off |
| SKIPPED-ON-PURPOSE | Paused projects | fly brain and retired helpers stay off | 20 paused tasks (fly brain, old gateways, retired desks), all still off |
| SKIPPED-ON-PURPOSE | Codex Observer | an old Codex side project | Codex Observer server + tunnel (Registry Run entries) - not checked; ask Jaron if still wanted |

<!-- run -->
## Sun Nov 22 07:34 PM - 4 broken: MSI dark alarm, MSI Health, Hourly helpers, Nightly news pipeline (1 fixed: MSI Beat)

**Still broken:**
- **MSI dark alarm** - its 5-minute Cloudflare check last ran never - a dark MSI would go unnoticed
- **MSI Health** - hasn't run since 11-22 16:02 (should run every 60 min) _(not sent to the phone; listed for Claude)_
- **Hourly helpers** - HB News Desks last ran 11-22 16:05; HB Prep Watch last ran 11-22 15:37 _(not sent to the phone; listed for Claude)_
- **Nightly news pipeline** - HB Socials Show last ran 11-21 17:00 _(not sent to the phone; listed for Claude)_

**Fixed this run:**
- **MSI Beat** - was: hasn't run since 11-30 00:00 (should run every 5 min). re-ran task MSI Beat. Now: last run 11-22 19:34, result 0

**Internet and website**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Internet | the MSI can reach the internet at all | names resolve (heartbeatobservatory.com, ntfy.sh, github.com) |
| OK | Website pages | the 10 main pages of heartbeatobservatory.com load | all 10 pages answer 200 |
| OK | Today's news show | the daily show is live (by 8 AM) | today's show is in the index and its video loads |
| OK | Database (Supabase) | the database behind the mailbox, Control Room and news answers | database answers (AI mailbox read worked) |
| OK | The creature | her world (Cloudflare Worker) is up and her clock moves | alive, tick 4235 (was 4234 at the last Creature Watch) |
| BROKEN | MSI dark alarm | buzzes Jaron if the MSI goes quiet 20 min (off, or stuck at the sign-in screen) | its 5-minute Cloudflare check last ran never - a dark MSI would go unnoticed |

**Reaching the MSI**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | MSI connector (Grok Machine MCP) | the bots and chat AIs can reach the MSI | server up on 3001, public address answers 401 (401 = up, asking for sign-in) |
| OK | Cloudflare tunnel | carries the connector and Cosmos to the internet | tunnel service running and ready |
| OK | The Cosmos game server | the Cosmos world server and its watchdog | game server healthy on 8390 and public; watchdog running; 8 restarts today |

**Programs on the MSI**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Ollama (local model) | the local Qwen model server | Ollama answers (200) |
| OK | OpenClaw gateway | the OpenClaw gateway | OpenClaw answers (200) |
| OK | Sapling heartbeat | Sapling's training heartbeat | heartbeat answers on 7337 |
| OK | Sapling relay | carries messages between the Sapling page and Sapling | relay answers (200) |
| OK | Desktop Commander remote | ChatGPT's way into the MSI | Desktop Commander remote running |
| OK | Remote agent | Claude's remote screen/keepalive helper | remote agent running |
| OK | Render worker | the hb-render owner worker (renders jobs) | render worker running |
| OK | Grok Bot app | the bots (Darios, Satya, Jarons Twin) need its window open | Grok Bot app running |
| OK | Claude mailbox waiter | wakes the main Claude session when mail arrives | mailbox waiter running |
| OK | Seam Room listener | Claude's ear in the Seam Room (re-armed by the Claude session) | Seam Room listener running |

**The machine**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Google Drive (G:) | the off-MSI copy of AI-Shared and the Necklace project goes through it | G:\My Drive is mounted (nightly AI-Shared + Necklace backups can run) |
| OK | Disk space | room for the nightly news render (~70 GB) | 181 GB free |
| OK | GPU heat | the MSI isn't overheating | 54C, 0% busy |
| OK | Power and memory | plugged in, enough RAM | plugged in, battery 91%, 20.0 GB RAM free |
| OK | Windows restart pending | updates waiting for a restart | no restart pending (up since Sun Nov 22 4:13 PM) |
| OK | Database size | Supabase stays under its 8 GB cap | 2.19 GB of 8 GB (27%) / biggest: qwen_events 1999MB, fly_school 136MB, cosmos_terrain_bricks 19MB |
| OK | Logins | every login the system uses still works | all logins fine (checked 2026-11-22 19:20) |
| OK | AI-Shared saved to GitHub | this folder is backed up | in step with origin/main |
| OK | Watch repo saved to GitHub | the news watch repo is pushed | in step with origin/master |

**Scheduled jobs**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | HB Watch Loop | answers Jaron's "Tell Claude" watch messages by ntfy | last run 11-22 19:33, result 0 |
| OK | HB Key Drop | files and tests API keys Jaron pastes on his phone | last run 11-22 19:32, result 0 |
| OK | Crypto Consensus | crypto decision tick (money side) | last run 11-22 19:33, result 0 |
| OK | Crew Publish | publishes the public system/crew page | last run 11-22 19:30, result 0 |
| FIXED | MSI Beat | checks in with the off-MSI alarm on Cloudflare (quiet 20 min = one buzz) | last run 11-22 19:34, result 0 |
| OK | HB Video Drop | picks up videos dropped for the site | last run 11-22 19:32, result 0 |
| OK | HB Price Alerts | price alerts (money side) | last run 11-22 19:31, result 0 |
| OK | Live Board | the live data board | last run 11-22 19:33, result 0 |
| OK | Crypto Notify | crypto notices (money side) | last run 11-22 19:33, result 0 |
| OK | Usage Snapshot | the AI usage meter | last run 11-22 19:26, result 267014 |
| OK | Desk Schedule Watch | desk schedule check (money side) | last run 11-22 19:26, result 0 |
| OK | Twin Crypto Settle | settles the twin's paper crypto (money side) | last run 11-22 19:24, result 0 |
| OK | HB News Watchdog | buzzes if today's news isn't live (7 AM-noon) | only runs 7-12h; last 11-22 11:00 result 0 |
| OK | MSI Connector Watch | buzzes if the connector/Cosmos/relay is down | last run 11-22 19:14, result 0 |
| OK | Creature Watch | looks in on the creature (read-only) | last run 11-22 19:33, result 0 |
| OK | HB Safety Signal | safety level from the DHS feed | last run 11-22 19:29, result 0 |
| OK | MSI Status | writes state/MSI-STATUS.md | last run 11-22 19:19, result 0 |
| OK | Sapling Watch | watches Sapling (read-only) | last run 11-22 19:15, result 0 |
| OK | Sapling Wake | Sapling's own wake | last run 11-22 19:14, result 0 |
| OK | DB Size Check | database size vs the 8 GB cap | last run 11-22 19:25, result 0 |
| BROKEN | MSI Health | hourly task/port health | hasn't run since 11-22 16:02 (should run every 60 min) |
| OK | HB AI Fund | AI fund (money side) | last run 11-22 19:17, result 0 |
| BROKEN | Hourly helpers | live readings, news desks, rolling wire, prep watch | HB News Desks last ran 11-22 16:05; HB Prep Watch last ran 11-22 15:37 |
| BROKEN | Nightly news pipeline | GPU guard 2:38, render 3:50, writer 4:20, paper book 9:05, socials 7:15/8:45/5 PM | HB Socials Show last ran 11-21 17:00 |
| OK | Nightly news collectors | the Watch ... collectors and What's New scouts | all 14 ran on time and finished ok |
| OK | Backups and saves | Drive mirror 3:30, nightly save 22:55, creature 21:15, Unreal 3:00, Sapling GitHub 18:17 | all 5 ran on time and finished ok |
| OK | Other daily jobs | login watch, usage ledger, build ledger, render maintainer, firsts, Sapling status, atlas | all 8 ran on time and finished ok |
| OK | Weekly jobs | stale sweep, AI fund review, budget report, edge check, crypto caps | all 5 ran on time and finished ok |
| OK | Any other job | catches failures in jobs not listed above (vendor and one-shot reminders skipped) | no other job failed in the last 2 days |

**Off on purpose**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| SKIPPED-ON-PURPOSE | Polymarket system | trading on Polymarket is off since 10/28 | Polymarket system is DOWN by Jaron's 10/28 decision - never restarted here; trading tasks still disabled; Polymarket MCP task Running (last run 2026-11-22); Trade Verifier still scheduled and ends 1 because nothing real answers on 8765 (state/verifier.md 1.3 MB); NOTE something else is on 8765 - is Polymarket MCP running again?; Connector Watch's Polymarket restart is off |
| SKIPPED-ON-PURPOSE | Paused projects | fly brain and retired helpers stay off | 20 paused tasks (fly brain, old gateways, retired desks), all still off |
| SKIPPED-ON-PURPOSE | Codex Observer | an old Codex side project | Codex Observer server + tunnel (Registry Run entries) - not checked; ask Jaron if still wanted |

<!-- run -->
## Sun Nov 22 07:16 PM - 12 broken: Grok Bot app, Claude mailbox waiter, Seam Room listener, Google Drive (G:), Desk Schedule Watch, Twin Crypto Settle, Sapling Watch, Sapling Wake, MSI Health, HB AI Fund, Hourly helpers, Nightly news pipeline (8 fixed: The Cosmos game server, Sapling heartbeat, Crew Publish, HB Price Alerts, Creature Watch, HB Safety Signal, MSI Status, DB Size Check)

**Still broken:**
- **Grok Bot app** - Grok Bot app not running
- **Claude mailbox waiter** - mailbox waiter not running _(not sent to the phone; listed for Claude)_
- **Seam Room listener** - Seam Room listener not running _(not sent to the phone; listed for Claude)_
- **Google Drive (G:)** - Google Drive is not running - the nightly AI-Shared and Necklace backups to Drive can't run. If it's running but unmounted, its index went bad again: close Drive, rename %LOCALAPPDATA%\Google\DriveFS\<account>\metadata_sqlite_db* aside, start Drive (fixed this way 11/22)
- **Desk Schedule Watch** - hasn't run since 11-22 15:56 (should run every 15 min) _(not sent to the phone; listed for Claude)_
- **Twin Crypto Settle** - hasn't run since 11-22 16:09 (should run every 15 min) _(not sent to the phone; listed for Claude)_
- **Sapling Watch** - hasn't run since 11-22 15:45 (should run every 30 min) _(not sent to the phone; listed for Claude)_
- **Sapling Wake** - hasn't run since 11-22 16:05 (should run every 30 min) _(not sent to the phone; listed for Claude)_
- **MSI Health** - hasn't run since 11-22 16:02 (should run every 60 min) _(not sent to the phone; listed for Claude)_
- **HB AI Fund** - hasn't run since 11-22 15:17 (should run every 60 min) _(not sent to the phone; listed for Claude)_
- **Hourly helpers** - HB Live Readings last ran 11-22 15:20; HB News Desks last ran 11-22 16:05; Watch Rolling Wire last ran 11-22 15:28; HB Prep Watch last ran 11-22 15:37 _(not sent to the phone; listed for Claude)_
- **Nightly news pipeline** - HB Socials Show last ran 11-21 17:00 _(not sent to the phone; listed for Claude)_

**Fixed this run:**
- **The Cosmos game server** - was: local DOWN, public 502; watchdog NOT running; 7 restarts today. started task MSI Connector Watch (it restarts the Cosmos watchdog), then waited for the watchdog. Now: game server healthy on 8390 and public; watchdog running; 8 restarts today
- **Sapling heartbeat** - was: heartbeat not answering on 7337 (Sapling Watch says running=False, last stop: vanished); it may be asleep on purpose - Sapling's own wake decides. started task Sapling Wake. Now: heartbeat answers on 7337
- **Crew Publish** - was: hasn't run since 11-22 16:05 (should run every 5 min). re-ran task Crew Publish. Now: last run 11-22 19:15, result 0
- **HB Price Alerts** - was: hasn't run since 11-22 16:06 (should run every 5 min). not re-run (money side); waited for its own next run. Now: last run 11-22 19:16, result 0
- **Creature Watch** - was: hasn't run since 11-22 16:03 (should run every 30 min). re-ran task Creature Watch. Now: last run 11-22 19:14, result 0
- **HB Safety Signal** - was: hasn't run since 11-22 15:59 (should run every 30 min). re-ran task HB Safety Signal. Now: last run 11-22 19:14, result 0
- **MSI Status** - was: hasn't run since 11-22 15:49 (should run every 30 min). re-ran task MSI Status. Now: last run 11-22 19:14, result 0
- **DB Size Check** - was: hasn't run since 11-22 15:25 (should run every 60 min). re-ran task DB Size Check. Now: last run 11-22 19:14, result 0

**Internet and website**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Internet | the MSI can reach the internet at all | names resolve (heartbeatobservatory.com, ntfy.sh, github.com) |
| OK | Website pages | the 10 main pages of heartbeatobservatory.com load | all 10 pages answer 200 |
| OK | Today's news show | the daily show is live (by 8 AM) | today's show is in the index and its video loads |
| OK | Database (Supabase) | the database behind the mailbox, Control Room and news answers | database answers (AI mailbox read worked) |
| OK | The creature | her world (Cloudflare Worker) is up and her clock moves | alive, tick 4205 (was 3902 at the last Creature Watch) |

**Reaching the MSI**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | MSI connector (Grok Machine MCP) | the bots and chat AIs can reach the MSI | server up on 3001, public address answers 401 (401 = up, asking for sign-in) |
| OK | Cloudflare tunnel | carries the connector and Cosmos to the internet | tunnel service running and ready |
| FIXED | The Cosmos game server | the Cosmos world server and its watchdog | game server healthy on 8390 and public; watchdog running; 8 restarts today |

**Programs on the MSI**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Ollama (local model) | the local Qwen model server | Ollama answers (200) |
| OK | OpenClaw gateway | the OpenClaw gateway | OpenClaw answers (200) |
| FIXED | Sapling heartbeat | Sapling's training heartbeat | heartbeat answers on 7337 |
| OK | Sapling relay | carries messages between the Sapling page and Sapling | relay answers (200) |
| OK | Desktop Commander remote | ChatGPT's way into the MSI | Desktop Commander remote running |
| OK | Remote agent | Claude's remote screen/keepalive helper | remote agent running |
| OK | Render worker | the hb-render owner worker (renders jobs) | render worker running |
| BROKEN | Grok Bot app | the bots (Darios, Satya, Jarons Twin) need its window open | Grok Bot app not running |
| BROKEN | Claude mailbox waiter | wakes the main Claude session when mail arrives | mailbox waiter not running |
| BROKEN | Seam Room listener | Claude's ear in the Seam Room (re-armed by the Claude session) | Seam Room listener not running |

**The machine**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| BROKEN | Google Drive (G:) | the off-MSI copy of AI-Shared and the Necklace project goes through it | Google Drive is not running - the nightly AI-Shared and Necklace backups to Drive can't run. If it's running but unmounted, its index went bad again: close Drive, rename %LOCALAPPDATA%\Google\DriveFS\<account>\metadata_sqlite_db* aside, start Drive (fixed this way 11/22) |
| OK | Disk space | room for the nightly news render (~70 GB) | 184 GB free |
| OK | GPU heat | the MSI isn't overheating | 53C, 0% busy |
| OK | Power and memory | plugged in, enough RAM | plugged in, battery 91%, 14.3 GB RAM free |
| OK | Windows restart pending | updates waiting for a restart | no restart pending (up since Sun Nov 22 4:13 PM) |
| OK | Database size | Supabase stays under its 8 GB cap | 2.19 GB of 8 GB (27%) / biggest: qwen_events 1999MB, fly_school 136MB, cosmos_terrain_bricks 19MB |
| OK | Logins | every login the system uses still works | all logins fine (checked 2026-11-22 15:49) |
| OK | AI-Shared saved to GitHub | this folder is backed up | in step with origin/main |
| OK | Watch repo saved to GitHub | the news watch repo is pushed | in step with origin/master |

**Scheduled jobs**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | HB Watch Loop | answers Jaron's "Tell Claude" watch messages by ntfy | last run 11-22 19:13, result 0 |
| OK | HB Key Drop | files and tests API keys Jaron pastes on his phone | last run 11-22 19:13, result 0 |
| OK | Crypto Consensus | crypto decision tick (money side) | last run 11-22 19:14, result 0 |
| FIXED | Crew Publish | publishes the public system/crew page | last run 11-22 19:15, result 0 |
| OK | HB Video Drop | picks up videos dropped for the site | last run 11-22 19:12, result 0 |
| FIXED | HB Price Alerts | price alerts (money side) | last run 11-22 19:16, result 0 |
| OK | Live Board | the live data board | last run 11-22 19:13, result 0 |
| OK | Crypto Notify | crypto notices (money side) | last run 11-22 19:13, result 0 |
| OK | Usage Snapshot | the AI usage meter | last run 11-22 19:11, result 267009 |
| BROKEN | Desk Schedule Watch | desk schedule check (money side) | hasn't run since 11-22 15:56 (should run every 15 min) |
| BROKEN | Twin Crypto Settle | settles the twin's paper crypto (money side) | hasn't run since 11-22 16:09 (should run every 15 min) |
| OK | HB News Watchdog | buzzes if today's news isn't live (7 AM-noon) | only runs 7-12h; last 11-22 11:00 result 0 |
| OK | MSI Connector Watch | buzzes if the connector/Cosmos/relay is down | last run 11-22 19:14, result 267009 |
| FIXED | Creature Watch | looks in on the creature (read-only) | last run 11-22 19:14, result 0 |
| FIXED | HB Safety Signal | safety level from the DHS feed | last run 11-22 19:14, result 0 |
| FIXED | MSI Status | writes state/MSI-STATUS.md | last run 11-22 19:14, result 0 |
| BROKEN | Sapling Watch | watches Sapling (read-only) | hasn't run since 11-22 15:45 (should run every 30 min) |
| BROKEN | Sapling Wake | Sapling's own wake | hasn't run since 11-22 16:05 (should run every 30 min) |
| FIXED | DB Size Check | database size vs the 8 GB cap | last run 11-22 19:14, result 0 |
| BROKEN | MSI Health | hourly task/port health | hasn't run since 11-22 16:02 (should run every 60 min) |
| BROKEN | HB AI Fund | AI fund (money side) | hasn't run since 11-22 15:17 (should run every 60 min) |
| BROKEN | Hourly helpers | live readings, news desks, rolling wire, prep watch | HB Live Readings last ran 11-22 15:20; HB News Desks last ran 11-22 16:05; Watch Rolling Wire last ran 11-22 15:28; HB Prep Watch last ran 11-22 15:37 |
| BROKEN | Nightly news pipeline | GPU guard 2:38, render 3:50, writer 4:20, paper book 9:05, socials 7:15/8:45/5 PM | HB Socials Show last ran 11-21 17:00 |
| OK | Nightly news collectors | the Watch ... collectors and What's New scouts | all 14 ran on time and finished ok |
| OK | Backups and saves | Drive mirror 3:30, nightly save 22:55, creature 21:15, Unreal 3:00, Sapling GitHub 18:17 | all 5 ran on time and finished ok |
| OK | Other daily jobs | login watch, usage ledger, build ledger, render maintainer, firsts, Sapling status, atlas | all 8 ran on time and finished ok |
| OK | Weekly jobs | stale sweep, AI fund review, budget report, edge check, crypto caps | all 5 ran on time and finished ok |
| OK | Any other job | catches failures in jobs not listed above (vendor and one-shot reminders skipped) | no other job failed in the last 2 days |

**Off on purpose**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| SKIPPED-ON-PURPOSE | Polymarket system | trading on Polymarket is off since 10/28 | Polymarket system is DOWN by Jaron's 10/28 decision - never restarted here; trading tasks still disabled; Polymarket MCP task Running (last run 2026-11-22); Trade Verifier still scheduled and ends 1 because nothing real answers on 8765 (state/verifier.md 1.3 MB); NOTE something else is on 8765 - is Polymarket MCP running again?; Connector Watch's Polymarket restart is off |
| SKIPPED-ON-PURPOSE | Paused projects | fly brain and retired helpers stay off | 20 paused tasks (fly brain, old gateways, retired desks), all still off |
| SKIPPED-ON-PURPOSE | Codex Observer | an old Codex side project | Codex Observer server + tunnel (Registry Run entries) - not checked; ask Jaron if still wanted |

<!-- run -->
## Sun Nov 22 01:34 PM - All good  (dry run: nothing restarted)

**Internet and website**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Internet | the MSI can reach the internet at all | names resolve (heartbeatobservatory.com, ntfy.sh, github.com) |
| OK | Website pages | the 10 main pages of heartbeatobservatory.com load | all 10 pages answer 200 |
| OK | Today's news show | the daily show is live (by 8 AM) | today's show is in the index and its video loads |
| OK | Database (Supabase) | the database behind the mailbox, Control Room and news answers | database answers (AI mailbox read worked) |
| OK | The creature | her world (Cloudflare Worker) is up and her clock moves | alive, tick 3668 (was 3665 at the last Creature Watch) |

**Reaching the MSI**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | MSI connector (Grok Machine MCP) | the bots and chat AIs can reach the MSI | server up on 3001, public address answers 401 (401 = up, asking for sign-in) |
| OK | Cloudflare tunnel | carries the connector and Cosmos to the internet | tunnel service running and ready |
| OK | The Cosmos game server | the Cosmos world server and its watchdog | game server healthy on 8390 and public; watchdog running; 7 restarts today |

**Programs on the MSI**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Ollama (local model) | the local Qwen model server | Ollama answers (200) |
| OK | OpenClaw gateway | the OpenClaw gateway | OpenClaw answers (200) |
| OK | Sapling heartbeat | Sapling's training heartbeat | heartbeat answers on 7337 |
| OK | Sapling relay | carries messages between the Sapling page and Sapling | relay answers (200) |
| OK | Desktop Commander remote | ChatGPT's way into the MSI | Desktop Commander remote running |
| OK | Remote agent | Claude's remote screen/keepalive helper | remote agent running |
| OK | Render worker | the hb-render owner worker (renders jobs) | render worker running |
| OK | Grok Bot app | the bots (Darios, Satya, Jarons Twin) need its window open | Grok Bot app running |
| OK | Claude mailbox waiter | wakes the main Claude session when mail arrives | mailbox waiter running |
| OK | Seam Room listener | Claude's ear in the Seam Room (re-armed by the Claude session) | Seam Room listener running |

**The machine**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Google Drive (G:) | the off-MSI copy of AI-Shared and the Necklace project goes through it | G:\My Drive is mounted (nightly AI-Shared + Necklace backups can run) |
| OK | Disk space | room for the nightly news render (~70 GB) | 195 GB free |
| OK | GPU heat | the MSI isn't overheating | 61C, 0% busy |
| OK | Power and memory | plugged in, enough RAM | plugged in, battery 91%, 7.8 GB RAM free |
| OK | Windows restart pending | updates waiting for a restart | no restart pending (up since Sun Nov 22 12:47 PM) |
| OK | Database size | Supabase stays under its 8 GB cap | 2.19 GB of 8 GB (27%) / biggest: qwen_events 1999MB, fly_school 136MB, cosmos_terrain_bricks 19MB |
| OK | Logins | every login the system uses still works | all logins fine (checked 2026-11-22 13:19) |
| OK | AI-Shared saved to GitHub | this folder is backed up | in step with origin/main |
| OK | Watch repo saved to GitHub | the news watch repo is pushed | in step with origin/master |

**Scheduled jobs**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | HB Watch Loop | answers Jaron's "Tell Claude" watch messages by ntfy | last run 11-22 13:33, result 0 |
| OK | HB Key Drop | files and tests API keys Jaron pastes on his phone | last run 11-22 13:33, result 0 |
| OK | Crypto Consensus | crypto decision tick (money side) | last run 11-22 13:34, result 0 |
| OK | Crew Publish | publishes the public system/crew page | last run 11-22 13:30, result 0 |
| OK | HB Video Drop | picks up videos dropped for the site | last run 11-22 13:32, result 0 |
| OK | HB Price Alerts | price alerts (money side) | last run 11-22 13:31, result 0 |
| OK | Live Board | the live data board | last run 11-22 13:33, result 0 |
| OK | Crypto Notify | crypto notices (money side) | last run 11-22 13:33, result 0 |
| OK | Usage Snapshot | the AI usage meter | last run 11-22 13:33, result 267009 |
| OK | Desk Schedule Watch | desk schedule check (money side) | last run 11-22 13:26, result 0 |
| OK | Twin Crypto Settle | settles the twin's paper crypto (money side) | last run 11-22 13:24, result 0 |
| OK | HB News Watchdog | buzzes if today's news isn't live (7 AM-noon) | only runs 7-12h; last 11-22 11:00 result 0 |
| OK | MSI Connector Watch | buzzes if the connector/Cosmos/relay is down | last run 11-22 13:14, result 0 |
| OK | Creature Watch | looks in on the creature (read-only) | last run 11-22 13:33, result 0 |
| OK | HB Safety Signal | safety level from the DHS feed | last run 11-22 13:29, result 0 |
| OK | MSI Status | writes state/MSI-STATUS.md | last run 11-22 13:19, result 0 |
| OK | Sapling Watch | watches Sapling (read-only) | last run 11-22 13:15, result 0 |
| OK | Sapling Wake | Sapling's own wake | last run 11-22 13:05, result 0 |
| OK | DB Size Check | database size vs the 8 GB cap | last run 11-22 13:25, result 0 |
| OK | MSI Health | hourly task/port health | last run 11-22 13:02, result 0 |
| OK | HB AI Fund | AI fund (money side) | last run 11-22 13:17, result 0 |
| OK | Hourly helpers | live readings, news desks, rolling wire, prep watch | all 4 ran on time and finished ok |
| OK | Nightly news pipeline | GPU guard 2:38, render 3:50, writer 4:20, paper book 9:05, socials 7:15/8:45/5 PM | all 7 ran on time and finished ok |
| OK | Nightly news collectors | the Watch ... collectors and What's New scouts | all 14 ran on time and finished ok |
| OK | Backups and saves | Drive mirror 3:30, nightly save 22:55, creature 21:15, Unreal 3:00, Sapling GitHub 18:17 | all 5 ran on time and finished ok |
| OK | Other daily jobs | login watch, usage ledger, build ledger, render maintainer, firsts, Sapling status, atlas | all 8 ran on time and finished ok |
| OK | Weekly jobs | stale sweep, AI fund review, budget report, edge check, crypto caps | all 5 ran on time and finished ok |
| OK | Any other job | catches failures in jobs not listed above (vendor and one-shot reminders skipped) | no other job failed in the last 2 days |

**Off on purpose**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| SKIPPED-ON-PURPOSE | Polymarket system | trading on Polymarket is off since 10/28 | Polymarket system is DOWN by Jaron's 10/28 decision - never restarted here; trading tasks still disabled; Polymarket MCP task Running (last run 2026-11-22); Trade Verifier still scheduled and ends 1 because nothing real answers on 8765 (state/verifier.md 1.3 MB); NOTE something else is on 8765 - is Polymarket MCP running again?; Connector Watch's Polymarket restart is off |
| SKIPPED-ON-PURPOSE | Paused projects | fly brain and retired helpers stay off | 20 paused tasks (fly brain, old gateways, retired desks), all still off |
| SKIPPED-ON-PURPOSE | Codex Observer | an old Codex side project | Codex Observer server + tunnel (Registry Run entries) - not checked; ask Jaron if still wanted |

<!-- run -->
## Sun Nov 22 01:34 PM - All good  (dry run: nothing restarted)

**Internet and website**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Internet | the MSI can reach the internet at all | names resolve (heartbeatobservatory.com, ntfy.sh, github.com) |
| OK | Website pages | the 10 main pages of heartbeatobservatory.com load | all 10 pages answer 200 |
| OK | Today's news show | the daily show is live (by 8 AM) | today's show is in the index and its video loads |
| OK | Database (Supabase) | the database behind the mailbox, Control Room and news answers | database answers (AI mailbox read worked) |
| OK | The creature | her world (Cloudflare Worker) is up and her clock moves | alive, tick 3667 (was 3665 at the last Creature Watch) |

**Reaching the MSI**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | MSI connector (Grok Machine MCP) | the bots and chat AIs can reach the MSI | server up on 3001, public address answers 401 (401 = up, asking for sign-in) |
| OK | Cloudflare tunnel | carries the connector and Cosmos to the internet | tunnel service running and ready |
| OK | The Cosmos game server | the Cosmos world server and its watchdog | game server healthy on 8390 and public; watchdog running; 7 restarts today |

**Programs on the MSI**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Ollama (local model) | the local Qwen model server | Ollama answers (200) |
| OK | OpenClaw gateway | the OpenClaw gateway | OpenClaw answers (200) |
| OK | Sapling heartbeat | Sapling's training heartbeat | heartbeat answers on 7337 |
| OK | Sapling relay | carries messages between the Sapling page and Sapling | relay answers (200) |
| OK | Desktop Commander remote | ChatGPT's way into the MSI | Desktop Commander remote running |
| OK | Remote agent | Claude's remote screen/keepalive helper | remote agent running |
| OK | Render worker | the hb-render owner worker (renders jobs) | render worker running |
| OK | Grok Bot app | the bots (Darios, Satya, Jarons Twin) need its window open | Grok Bot app running |
| OK | Claude mailbox waiter | wakes the main Claude session when mail arrives | mailbox waiter running |
| OK | Seam Room listener | Claude's ear in the Seam Room (re-armed by the Claude session) | Seam Room listener running |

**The machine**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Google Drive (G:) | the off-MSI copy of AI-Shared and the Necklace project goes through it | G:\My Drive is mounted (nightly AI-Shared + Necklace backups can run) |
| OK | Disk space | room for the nightly news render (~70 GB) | 196 GB free |
| OK | GPU heat | the MSI isn't overheating | 61C, 0% busy |
| OK | Power and memory | plugged in, enough RAM | plugged in, battery 91%, 7.6 GB RAM free |
| OK | Windows restart pending | updates waiting for a restart | no restart pending (up since Sun Nov 22 12:47 PM) |
| OK | Database size | Supabase stays under its 8 GB cap | 2.19 GB of 8 GB (27%) / biggest: qwen_events 1999MB, fly_school 136MB, cosmos_terrain_bricks 19MB |
| OK | Logins | every login the system uses still works | all logins fine (checked 2026-11-22 13:19) |
| OK | AI-Shared saved to GitHub | this folder is backed up | in step with origin/main |
| OK | Watch repo saved to GitHub | the news watch repo is pushed | in step with origin/master |

**Scheduled jobs**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | HB Watch Loop | answers Jaron's "Tell Claude" watch messages by ntfy | last run 11-22 13:33, result 0 |
| OK | HB Key Drop | files and tests API keys Jaron pastes on his phone | last run 11-22 13:33, result 0 |
| OK | Crypto Consensus | crypto decision tick (money side) | last run 11-22 13:33, result 0 |
| OK | Crew Publish | publishes the public system/crew page | last run 11-22 13:30, result 0 |
| OK | HB Video Drop | picks up videos dropped for the site | last run 11-22 13:32, result 0 |
| OK | HB Price Alerts | price alerts (money side) | last run 11-22 13:31, result 0 |
| OK | Live Board | the live data board | last run 11-22 13:33, result 0 |
| OK | Crypto Notify | crypto notices (money side) | last run 11-22 13:33, result 0 |
| OK | Usage Snapshot | the AI usage meter | last run 11-22 13:33, result 267009 |
| OK | Desk Schedule Watch | desk schedule check (money side) | last run 11-22 13:26, result 0 |
| OK | Twin Crypto Settle | settles the twin's paper crypto (money side) | last run 11-22 13:24, result 0 |
| OK | HB News Watchdog | buzzes if today's news isn't live (7 AM-noon) | only runs 7-12h; last 11-22 11:00 result 0 |
| OK | MSI Connector Watch | buzzes if the connector/Cosmos/relay is down | last run 11-22 13:14, result 0 |
| OK | Creature Watch | looks in on the creature (read-only) | last run 11-22 13:33, result 0 |
| OK | HB Safety Signal | safety level from the DHS feed | last run 11-22 13:29, result 0 |
| OK | MSI Status | writes state/MSI-STATUS.md | last run 11-22 13:19, result 0 |
| OK | Sapling Watch | watches Sapling (read-only) | last run 11-22 13:15, result 0 |
| OK | Sapling Wake | Sapling's own wake | last run 11-22 13:05, result 0 |
| OK | DB Size Check | database size vs the 8 GB cap | last run 11-22 13:25, result 0 |
| OK | MSI Health | hourly task/port health | last run 11-22 13:02, result 0 |
| OK | HB AI Fund | AI fund (money side) | last run 11-22 13:17, result 0 |
| OK | Hourly helpers | live readings, news desks, rolling wire, prep watch | all 4 ran on time and finished ok |
| OK | Nightly news pipeline | GPU guard 2:38, render 3:50, writer 4:20, paper book 9:05, socials 7:15/8:45/5 PM | all 7 ran on time and finished ok |
| OK | Nightly news collectors | the Watch ... collectors and What's New scouts | all 14 ran on time and finished ok |
| OK | Backups and saves | Drive mirror 3:30, nightly save 22:55, creature 21:15, Unreal 3:00, Sapling GitHub 18:17 | all 5 ran on time and finished ok |
| OK | Other daily jobs | login watch, usage ledger, build ledger, render maintainer, firsts, Sapling status, atlas | all 8 ran on time and finished ok |
| OK | Weekly jobs | stale sweep, AI fund review, budget report, edge check, crypto caps | all 5 ran on time and finished ok |
| OK | Any other job | catches failures in jobs not listed above (vendor and one-shot reminders skipped) | no other job failed in the last 2 days |

**Off on purpose**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| SKIPPED-ON-PURPOSE | Polymarket system | trading on Polymarket is off since 10/28 | Polymarket system is DOWN by Jaron's 10/28 decision - never restarted here; trading tasks still disabled; Polymarket MCP task Running (last run 2026-11-22); Trade Verifier still scheduled and ends 1 because nothing real answers on 8765 (state/verifier.md 1.3 MB); NOTE something else is on 8765 - is Polymarket MCP running again?; Connector Watch's Polymarket restart is off |
| SKIPPED-ON-PURPOSE | Paused projects | fly brain and retired helpers stay off | 20 paused tasks (fly brain, old gateways, retired desks), all still off |
| SKIPPED-ON-PURPOSE | Codex Observer | an old Codex side project | Codex Observer server + tunnel (Registry Run entries) - not checked; ask Jaron if still wanted |

