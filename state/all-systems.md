# Everything check - is every part of the MSI OK? (newest run on top)

Runs by itself: daily 7:45 AM, after a restart, and when the network comes back (task "All Systems Check", tools/all_systems_check.py). It restarts only what is safe, through each part's own task, and buzzes Jaron only if something is still broken after that. `--why` lists every check.

<!-- run -->
## Wed Nov 25 07:50 AM - 2 broken: Logins, AI-Shared saved to GitHub

**Still broken:**
- **Logins** - needs Jaron: Claude chat -> MSI connector (Heartbeat MAI) (checked 2026-11-25 07:49; steps in RECONNECT.md) (still broken after re-ran tools/login-watch.py --quiet (a fresh check, no buzz); waited 5.0 min) _(not sent to the phone; listed for Claude)_
- **AI-Shared saved to GitHub** - main...origin/main [ahead 5] - oldest unpushed commit 3 h old _(not sent to the phone; listed for Claude)_

**Internet and website**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Internet | the MSI can reach the internet at all | names resolve (heartbeatobservatory.com, ntfy.sh, github.com) |
| OK | Website pages | the 10 main pages of heartbeatobservatory.com load | all 10 pages answer 200 |
| OK | Today's news show | the daily show is live (by 8 AM) | today's show is in the index and its video loads |
| OK | Database (Supabase) | the database behind the mailbox, Control Room and news answers | database answers (AI mailbox read worked) |
| OK | The creature | her world (Cloudflare Worker) is up and her clock moves | alive, tick 9951 (was 9933 at the last Creature Watch) |
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
| OK | Processor speed cap | keeps the worn fast core below the speed where it makes mistakes (11/24) | fast cores' top speed: plugged in = 4600 MHz (4.6 GHz), on battery = 4600 MHz (4.6 GHz) |
| OK | Disk space | room for the nightly news render (~70 GB) | 173 GB free |
| OK | GPU heat | the MSI isn't overheating | 50C, 0% busy |
| OK | Power and memory | plugged in, enough RAM | plugged in, battery 90%, 16.5 GB RAM free |
| OK | Windows restart pending | updates waiting for a restart | no restart pending (up since Sun Nov 22 4:13 PM) |
| OK | Database size | Supabase stays under its 8 GB cap | 2.25 GB of 8 GB (28%) / biggest: qwen_events 1999MB, fly_school 136MB, cosmos_terrain_bricks 19MB |
| BROKEN | Logins | every login the system uses still works | needs Jaron: Claude chat -> MSI connector (Heartbeat MAI) (checked 2026-11-25 07:49; steps in RECONNECT.md) (still broken after re-ran tools/login-watch.py --quiet (a fresh check, no buzz); waited 5.0 min) |
| BROKEN | AI-Shared saved to GitHub | this folder is backed up | main...origin/main [ahead 5] - oldest unpushed commit 3 h old |
| OK | Public copy pushed in the last 48 hours | the scrubbed public AI-Shared reaches GitHub nightly | pushed 8 h ago; last nightly: FLAGS: none |
| OK | Watch repo saved to GitHub | the news watch repo is pushed | in step with origin/master |

**Scheduled jobs**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | HB Watch Loop | answers Jaron's "Tell Claude" watch messages by ntfy | last run 11-25 07:44, result 0 |
| OK | HB Key Drop | files and tests API keys Jaron pastes on his phone | last run 11-25 07:44, result 0 |
| OK | Crew Publish | publishes the public system/crew page | last run 11-25 07:45, result 267009 |
| OK | MSI Beat | checks in with the off-MSI alarm on Cloudflare (quiet 20 min = one buzz) | last run 11-25 07:45, result 0 |
| OK | HB Video Drop | picks up videos dropped for the site | last run 11-25 07:42, result 0 |
| OK | HB Price Alerts | price alerts (money side) | last run 11-25 07:41, result 0 |
| OK | Usage Snapshot | the AI usage meter | last run 11-25 07:41, result 0 |
| OK | HB News Watchdog | buzzes if today's news isn't live (7 AM-noon) | last run 11-25 07:45, result 0 |
| OK | MSI Connector Watch | buzzes if the connector/Cosmos/relay is down | last run 11-25 07:44, result 0 |
| OK | Creature Watch | looks in on the creature (read-only) | last run 11-25 07:33, result 0 |
| OK | HB Safety Signal | safety level from the DHS feed | last run 11-25 07:29, result 0 |
| OK | MSI Status | writes state/MSI-STATUS.md | last run 11-25 07:19, result 0 |
| OK | Sapling Watch | watches Sapling (read-only) | last run 11-25 07:45, result 0 |
| OK | Sapling Wake | Sapling's own wake | last run 11-25 07:35, result 0 |
| OK | DB Size Check | database size vs the 8 GB cap | last run 11-25 07:25, result 0 |
| OK | MSI Health | hourly task/port health | last run 11-25 07:02, result 0 |
| OK | HB AI Fund | AI fund (money side) | last run 11-25 07:17, result 0 |
| OK | Hourly helpers | live readings, news desks, rolling wire, prep watch | all 4 ran on time and finished ok |
| OK | Nightly news pipeline | GPU guard 2:38, render 3:50, writer 4:20, paper book 9:05, socials 7:15/8:45/5 PM | all 7 ran on time and finished ok |
| OK | Nightly news collectors | the Watch ... collectors and What's New scouts | all 14 ran on time and finished ok |
| OK | Backups and saves | nightly save 22:55, creature 21:15, off-MSI backup 21:30, Sapling GitHub 18:17 | all 4 ran on time and finished ok |
| OK | Weekly Drive copy | one AI-Shared file into Google Drive, Sunday 21:00 (a skipped week is fine) | all 1 ran on time and finished ok |
| OK | Processor yardstick | daily 2-minute wrong-answer test on every core, 11:30 (ended 1 = wrong answers: lower the cap with msi_speed_cap.py set 4300; ended 2 = cores never reached full speed, not a fair test) | all 1 ran on time and finished ok |
| OK | Other daily jobs | login watch, usage ledger, build ledger, render maintainer, firsts, Sapling status, atlas | all 8 ran on time and finished ok |
| OK | Weekly jobs | stale sweep, AI fund review, budget report, edge check, crypto caps | all 4 ran on time and finished ok |
| OK | Any other job | catches failures in jobs not listed above (vendor and one-shot reminders skipped) | no other job failed in the last 2 days |

**Off on purpose**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| SKIPPED-ON-PURPOSE | Polymarket system | trading on Polymarket is off since 10/28 | Polymarket system is DOWN by Jaron's 10/28 decision - never restarted here; trading tasks still disabled; Polymarket MCP task Disabled (last run 2026-11-22); Trade Verifier still scheduled and ends 1 because nothing real answers on 8765 (state/verifier.md 1.3 MB); Connector Watch's Polymarket restart is off |
| SKIPPED-ON-PURPOSE | Paused projects | fly brain and retired helpers stay off | 21 paused tasks (fly brain, old gateways, retired desks), all still off |
| SKIPPED-ON-PURPOSE | Google Drive backups | Drive's index kept breaking; the big copies go off-MSI to Supabase; Drive keeps one weekly file | Google Drive is out of the backups (Jaron 11/24: 'Google Drive has always had issues'); the off-MSI Supabase backup covers everything; its 3 jobs stay off |
| SKIPPED-ON-PURPOSE | Codex Observer | an old Codex side project | Codex Observer retired 11/24 (Jaron: old = noise): its 2 dead startup entries were removed; values kept in state/removed-startup-entries-2026-11-24.txt |

<!-- run -->
## Tue Nov 24 01:04 PM - All good  (dry run: nothing restarted)

**Internet and website**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Internet | the MSI can reach the internet at all | names resolve (heartbeatobservatory.com, ntfy.sh, github.com) |
| OK | Website pages | the 10 main pages of heartbeatobservatory.com load | all 10 pages answer 200 |
| OK | Today's news show | the daily show is live (by 8 AM) | today's show is in the index and its video loads |
| OK | Database (Supabase) | the database behind the mailbox, Control Room and news answers | database answers (AI mailbox read worked) |
| OK | The creature | her world (Cloudflare Worker) is up and her clock moves | alive, tick 8178 (was 8175 at the last Creature Watch) |
| OK | MSI dark alarm | buzzes Jaron if the MSI goes quiet 20 min (off, or stuck at the sign-in screen) | watching from Cloudflare: last check-in 5 min ago, its own check ran 5 min ago |

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
| OK | Processor speed cap | keeps the worn fast core below the speed where it makes mistakes (11/24) | fast cores' top speed: plugged in = 4600 MHz (4.6 GHz), on battery = 4600 MHz (4.6 GHz) |
| OK | Disk space | room for the nightly news render (~70 GB) | 176 GB free |
| OK | GPU heat | the MSI isn't overheating | 49C, 0% busy |
| OK | Power and memory | plugged in, enough RAM | plugged in, battery 90%, 16.7 GB RAM free |
| OK | Windows restart pending | updates waiting for a restart | no restart pending (up since Sun Nov 22 4:13 PM) |
| OK | Database size | Supabase stays under its 8 GB cap | 2.25 GB of 8 GB (28%) / biggest: qwen_events 1999MB, fly_school 136MB, cosmos_terrain_bricks 19MB |
| OK | Logins | every login the system uses still works | all logins fine (checked 2026-11-24 12:49) |
| OK | AI-Shared saved to GitHub | this folder is backed up | main...origin/main [ahead 1] (recent; its own job pushes it) |
| OK | Public copy pushed in the last 48 hours | the scrubbed public AI-Shared reaches GitHub nightly | pushed 14 h ago; last nightly: FLAGS: none |
| OK | Watch repo saved to GitHub | the news watch repo is pushed | in step with origin/master |

**Scheduled jobs**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | HB Watch Loop | answers Jaron's "Tell Claude" watch messages by ntfy | last run 11-24 13:04, result 0 |
| OK | HB Key Drop | files and tests API keys Jaron pastes on his phone | last run 11-24 13:03, result 0 |
| OK | Crew Publish | publishes the public system/crew page | last run 11-24 13:00, result 0 |
| OK | MSI Beat | checks in with the off-MSI alarm on Cloudflare (quiet 20 min = one buzz) | last run 11-24 13:00, result 0 |
| OK | HB Video Drop | picks up videos dropped for the site | last run 11-24 13:02, result 0 |
| OK | HB Price Alerts | price alerts (money side) | last run 11-24 13:01, result 0 |
| OK | Usage Snapshot | the AI usage meter | last run 11-24 13:03, result 267009 |
| OK | HB News Watchdog | buzzes if today's news isn't live (7 AM-noon) | only runs 7-12h; last 11-24 11:00 result 0 |
| OK | MSI Connector Watch | buzzes if the connector/Cosmos/relay is down | last run 11-24 12:44, result 0 |
| OK | Creature Watch | looks in on the creature (read-only) | last run 11-24 13:03, result 0 |
| OK | HB Safety Signal | safety level from the DHS feed | last run 11-24 12:59, result 0 |
| OK | MSI Status | writes state/MSI-STATUS.md | last run 11-24 12:49, result 0 |
| OK | Sapling Watch | watches Sapling (read-only) | last run 11-24 12:45, result 0 |
| OK | Sapling Wake | Sapling's own wake | last run 11-24 12:35, result 0 |
| OK | DB Size Check | database size vs the 8 GB cap | last run 11-24 12:25, result 0 |
| OK | MSI Health | hourly task/port health | last run 11-24 13:02, result 0 |
| OK | HB AI Fund | AI fund (money side) | last run 11-24 12:17, result 0 |
| OK | Hourly helpers | live readings, news desks, rolling wire, prep watch | all 4 ran on time and finished ok |
| OK | Nightly news pipeline | GPU guard 2:38, render 3:50, writer 4:20, paper book 9:05, socials 7:15/8:45/5 PM | all 7 ran on time and finished ok |
| OK | Nightly news collectors | the Watch ... collectors and What's New scouts | all 14 ran on time and finished ok |
| OK | Backups and saves | nightly save 22:55, creature 21:15, off-MSI backup 21:30, Sapling GitHub 18:17 | all 4 ran on time and finished ok |
| OK | Weekly Drive copy | one AI-Shared file into Google Drive, Sunday 21:00 (a skipped week is fine) | all 1 ran on time and finished ok |
| OK | Processor yardstick | daily 2-minute wrong-answer test on every core, 11:30 (ended 1 = wrong answers: lower the cap with msi_speed_cap.py set 4300; ended 2 = cores never reached full speed, not a fair test) | all 1 ran on time and finished ok |
| OK | Other daily jobs | login watch, usage ledger, build ledger, render maintainer, firsts, Sapling status, atlas | all 8 ran on time and finished ok |
| OK | Weekly jobs | stale sweep, AI fund review, budget report, edge check, crypto caps | all 4 ran on time and finished ok |
| OK | Any other job | catches failures in jobs not listed above (vendor and one-shot reminders skipped) | no other job failed in the last 2 days |

**Off on purpose**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| SKIPPED-ON-PURPOSE | Polymarket system | trading on Polymarket is off since 10/28 | Polymarket system is DOWN by Jaron's 10/28 decision - never restarted here; trading tasks still disabled; Polymarket MCP task Disabled (last run 2026-11-22); Trade Verifier still scheduled and ends 1 because nothing real answers on 8765 (state/verifier.md 1.3 MB); Connector Watch's Polymarket restart is off |
| SKIPPED-ON-PURPOSE | Paused projects | fly brain and retired helpers stay off | 21 paused tasks (fly brain, old gateways, retired desks), all still off |
| SKIPPED-ON-PURPOSE | Google Drive backups | Drive's index kept breaking; the big copies go off-MSI to Supabase; Drive keeps one weekly file | Google Drive is out of the backups (Jaron 11/24: 'Google Drive has always had issues'); the off-MSI Supabase backup covers everything; its 3 jobs stay off |
| SKIPPED-ON-PURPOSE | Codex Observer | an old Codex side project | Codex Observer server + tunnel (Registry Run entries) - not checked; ask Jaron if still wanted |

<!-- run -->
## Tue Nov 24 01:00 PM - All good  (dry run: nothing restarted)

**Internet and website**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Internet | the MSI can reach the internet at all | names resolve (heartbeatobservatory.com, ntfy.sh, github.com) |
| OK | Website pages | the 10 main pages of heartbeatobservatory.com load | all 10 pages answer 200 |
| OK | Today's news show | the daily show is live (by 8 AM) | today's show is in the index and its video loads |
| OK | Database (Supabase) | the database behind the mailbox, Control Room and news answers | database answers (AI mailbox read worked) |
| OK | The creature | her world (Cloudflare Worker) is up and her clock moves | alive, tick 8171 (was 8129 at the last Creature Watch) |
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
| OK | Processor speed cap | keeps the worn fast core below the speed where it makes mistakes (11/24) | fast cores' top speed: plugged in = 4600 MHz (4.6 GHz), on battery = 4600 MHz (4.6 GHz) |
| OK | Disk space | room for the nightly news render (~70 GB) | 176 GB free |
| OK | GPU heat | the MSI isn't overheating | 50C, 0% busy |
| OK | Power and memory | plugged in, enough RAM | plugged in, battery 90%, 16.4 GB RAM free |
| OK | Windows restart pending | updates waiting for a restart | no restart pending (up since Sun Nov 22 4:13 PM) |
| OK | Database size | Supabase stays under its 8 GB cap | 2.25 GB of 8 GB (28%) / biggest: qwen_events 1999MB, fly_school 136MB, cosmos_terrain_bricks 19MB |
| OK | Logins | every login the system uses still works | all logins fine (checked 2026-11-24 12:49) |
| OK | AI-Shared saved to GitHub | this folder is backed up | in step with origin/main |
| OK | Public copy pushed in the last 48 hours | the scrubbed public AI-Shared reaches GitHub nightly | pushed 14 h ago; last nightly: FLAGS: none |
| OK | Watch repo saved to GitHub | the news watch repo is pushed | in step with origin/master |

**Scheduled jobs**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | HB Watch Loop | answers Jaron's "Tell Claude" watch messages by ntfy | last run 11-24 12:59, result 0 |
| OK | HB Key Drop | files and tests API keys Jaron pastes on his phone | last run 11-24 12:59, result 0 |
| OK | Crew Publish | publishes the public system/crew page | last run 11-24 13:00, result 0 |
| OK | MSI Beat | checks in with the off-MSI alarm on Cloudflare (quiet 20 min = one buzz) | last run 11-24 13:00, result 0 |
| OK | HB Video Drop | picks up videos dropped for the site | last run 11-24 12:57, result 0 |
| OK | HB Price Alerts | price alerts (money side) | last run 11-24 12:56, result 0 |
| OK | Usage Snapshot | the AI usage meter | last run 11-24 12:56, result 0 |
| OK | HB News Watchdog | buzzes if today's news isn't live (7 AM-noon) | only runs 7-12h; last 11-24 11:00 result 0 |
| OK | MSI Connector Watch | buzzes if the connector/Cosmos/relay is down | last run 11-24 12:44, result 0 |
| OK | Creature Watch | looks in on the creature (read-only) | last run 11-24 12:33, result 0 |
| OK | HB Safety Signal | safety level from the DHS feed | last run 11-24 12:59, result 0 |
| OK | MSI Status | writes state/MSI-STATUS.md | last run 11-24 12:49, result 0 |
| OK | Sapling Watch | watches Sapling (read-only) | last run 11-24 12:45, result 0 |
| OK | Sapling Wake | Sapling's own wake | last run 11-24 12:35, result 0 |
| OK | DB Size Check | database size vs the 8 GB cap | last run 11-24 12:25, result 0 |
| OK | MSI Health | hourly task/port health | last run 11-24 12:02, result 0 |
| OK | HB AI Fund | AI fund (money side) | last run 11-24 12:17, result 0 |
| OK | Hourly helpers | live readings, news desks, rolling wire, prep watch | all 4 ran on time and finished ok |
| OK | Nightly news pipeline | GPU guard 2:38, render 3:50, writer 4:20, paper book 9:05, socials 7:15/8:45/5 PM | all 7 ran on time and finished ok |
| OK | Nightly news collectors | the Watch ... collectors and What's New scouts | all 14 ran on time and finished ok |
| OK | Backups and saves | nightly save 22:55, creature 21:15, off-MSI backup 21:30, Sapling GitHub 18:17 | all 4 ran on time and finished ok |
| OK | Weekly Drive copy | one AI-Shared file into Google Drive, Sunday 21:00 (a skipped week is fine) | all 1 ran on time and finished ok |
| OK | Processor yardstick | daily 2-minute wrong-answer test on every core, 11:30 (ended 1 = wrong answers: lower the cap with msi_speed_cap.py set 4300; ended 2 = cores never reached full speed, not a fair test) | all 1 ran on time and finished ok |
| OK | Other daily jobs | login watch, usage ledger, build ledger, render maintainer, firsts, Sapling status, atlas | all 8 ran on time and finished ok |
| OK | Weekly jobs | stale sweep, AI fund review, budget report, edge check, crypto caps | all 4 ran on time and finished ok |
| OK | Any other job | catches failures in jobs not listed above (vendor and one-shot reminders skipped) | no other job failed in the last 2 days |

**Off on purpose**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| SKIPPED-ON-PURPOSE | Polymarket system | trading on Polymarket is off since 10/28 | Polymarket system is DOWN by Jaron's 10/28 decision - never restarted here; trading tasks still disabled; Polymarket MCP task Disabled (last run 2026-11-22); Trade Verifier still scheduled and ends 1 because nothing real answers on 8765 (state/verifier.md 1.3 MB); Connector Watch's Polymarket restart is off |
| SKIPPED-ON-PURPOSE | Paused projects | fly brain and retired helpers stay off | 20 paused tasks (fly brain, old gateways, retired desks), all still off |
| SKIPPED-ON-PURPOSE | Google Drive backups | Drive's index kept breaking; the big copies go off-MSI to Supabase; Drive keeps one weekly file | Google Drive is out of the backups (Jaron 11/24: 'Google Drive has always had issues'); the off-MSI Supabase backup covers everything; its 3 jobs stay off |
| SKIPPED-ON-PURPOSE | Codex Observer | an old Codex side project | Codex Observer server + tunnel (Registry Run entries) - not checked; ask Jaron if still wanted |

<!-- run -->
## Tue Nov 24 10:55 AM - All good  (dry run: nothing restarted)

**Internet and website**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Internet | the MSI can reach the internet at all | names resolve (heartbeatobservatory.com, ntfy.sh, github.com) |
| OK | Website pages | the 10 main pages of heartbeatobservatory.com load | all 10 pages answer 200 |
| OK | Today's news show | the daily show is live (by 8 AM) | today's show is in the index and its video loads |
| OK | Database (Supabase) | the database behind the mailbox, Control Room and news answers | database answers (AI mailbox read worked) |
| OK | The creature | her world (Cloudflare Worker) is up and her clock moves | alive, tick 7974 (was 7937 at the last Creature Watch) |
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
| OK | Processor speed cap | keeps the worn fast core below the speed where it makes mistakes (11/24) | fast cores' top speed: plugged in = 4600 MHz (4.6 GHz), on battery = 4600 MHz (4.6 GHz) |
| OK | Disk space | room for the nightly news render (~70 GB) | 172 GB free |
| OK | GPU heat | the MSI isn't overheating | 50C, 0% busy |
| OK | Power and memory | plugged in, enough RAM | plugged in, battery 90%, 18.3 GB RAM free |
| OK | Windows restart pending | updates waiting for a restart | no restart pending (up since Sun Nov 22 4:13 PM) |
| OK | Database size | Supabase stays under its 8 GB cap | 2.25 GB of 8 GB (28%) / biggest: qwen_events 1999MB, fly_school 136MB, cosmos_terrain_bricks 19MB |
| OK | Logins | every login the system uses still works | all logins fine (checked 2026-11-24 10:49) |
| OK | AI-Shared saved to GitHub | this folder is backed up | in step with origin/main |
| OK | Public copy pushed in the last 48 hours | the scrubbed public AI-Shared reaches GitHub nightly | pushed 12 h ago; last nightly: FLAGS: none |
| OK | Watch repo saved to GitHub | the news watch repo is pushed | in step with origin/master |

**Scheduled jobs**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | HB Watch Loop | answers Jaron's "Tell Claude" watch messages by ntfy | last run 11-24 10:54, result 0 |
| OK | HB Key Drop | files and tests API keys Jaron pastes on his phone | last run 11-24 10:54, result 0 |
| OK | Crypto Consensus | crypto decision tick (money side) | last run 11-24 10:55, result 0 |
| OK | Crew Publish | publishes the public system/crew page | last run 11-24 10:55, result 0 |
| OK | MSI Beat | checks in with the off-MSI alarm on Cloudflare (quiet 20 min = one buzz) | last run 11-24 10:55, result 0 |
| OK | HB Video Drop | picks up videos dropped for the site | last run 11-24 10:52, result 0 |
| OK | HB Price Alerts | price alerts (money side) | last run 11-24 10:51, result 0 |
| OK | Live Board | the live data board | last run 11-24 10:53, result 0 |
| OK | Crypto Notify | crypto notices (money side) | last run 11-24 10:53, result 0 |
| OK | Usage Snapshot | the AI usage meter | last run 11-24 10:48, result 0 |
| OK | Desk Schedule Watch | desk schedule check (money side) | last run 11-24 10:41, result 0 |
| OK | Twin Crypto Settle | settles the twin's paper crypto (money side) | last run 11-24 10:54, result 0 |
| OK | HB News Watchdog | buzzes if today's news isn't live (7 AM-noon) | last run 11-24 10:45, result 0 |
| OK | MSI Connector Watch | buzzes if the connector/Cosmos/relay is down | last run 11-24 10:44, result 0 |
| OK | Creature Watch | looks in on the creature (read-only) | last run 11-24 10:33, result 0 |
| OK | HB Safety Signal | safety level from the DHS feed | last run 11-24 10:29, result 0 |
| OK | MSI Status | writes state/MSI-STATUS.md | last run 11-24 10:49, result 0 |
| OK | Sapling Watch | watches Sapling (read-only) | last run 11-24 10:45, result 0 |
| OK | Sapling Wake | Sapling's own wake | last run 11-24 10:35, result 0 |
| OK | DB Size Check | database size vs the 8 GB cap | last run 11-24 10:25, result 0 |
| OK | MSI Health | hourly task/port health | last run 11-24 10:02, result 0 |
| OK | HB AI Fund | AI fund (money side) | last run 11-24 10:17, result 0 |
| OK | Hourly helpers | live readings, news desks, rolling wire, prep watch | all 4 ran on time and finished ok |
| OK | Nightly news pipeline | GPU guard 2:38, render 3:50, writer 4:20, paper book 9:05, socials 7:15/8:45/5 PM | all 7 ran on time and finished ok |
| OK | Nightly news collectors | the Watch ... collectors and What's New scouts | all 14 ran on time and finished ok |
| OK | Backups and saves | nightly save 22:55, creature 21:15, off-MSI backup 21:30, Sapling GitHub 18:17 | all 4 ran on time and finished ok |
| OK | Weekly Drive copy | one AI-Shared file into Google Drive, Sunday 21:00 (a skipped week is fine) | all 1 ran on time and finished ok |
| OK | Processor yardstick | daily 2-minute wrong-answer test on every core, 11:30 (ended 1 = wrong answers: lower the cap with msi_speed_cap.py set 4300; ended 2 = cores never reached full speed, not a fair test) | all 1 ran on time and finished ok |
| OK | Other daily jobs | login watch, usage ledger, build ledger, render maintainer, firsts, Sapling status, atlas | all 8 ran on time and finished ok |
| OK | Weekly jobs | stale sweep, AI fund review, budget report, edge check, crypto caps | all 5 ran on time and finished ok |
| OK | Any other job | catches failures in jobs not listed above (vendor and one-shot reminders skipped) | no other job failed in the last 2 days |

**Off on purpose**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| SKIPPED-ON-PURPOSE | Polymarket system | trading on Polymarket is off since 10/28 | Polymarket system is DOWN by Jaron's 10/28 decision - never restarted here; trading tasks still disabled; Polymarket MCP task Ready (last run 2026-11-22); Trade Verifier still scheduled and ends 1 because nothing real answers on 8765 (state/verifier.md 1.3 MB); Connector Watch's Polymarket restart is off |
| SKIPPED-ON-PURPOSE | Paused projects | fly brain and retired helpers stay off | 20 paused tasks (fly brain, old gateways, retired desks), all still off |
| SKIPPED-ON-PURPOSE | Google Drive backups | Drive's index kept breaking; the big copies go off-MSI to Supabase; Drive keeps one weekly file | Google Drive is out of the backups (Jaron 11/24: 'Google Drive has always had issues'); the off-MSI Supabase backup covers everything; its 3 jobs stay off |
| SKIPPED-ON-PURPOSE | Codex Observer | an old Codex side project | Codex Observer server + tunnel (Registry Run entries) - not checked; ask Jaron if still wanted |

<!-- run -->
## Tue Nov 24 10:32 AM - 1 broken: Processor yardstick  (dry run: nothing restarted)

**Still broken:**
- **Processor yardstick** - MSI Core Yardstick disabled _(not sent to the phone; listed for Claude)_

**Internet and website**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Internet | the MSI can reach the internet at all | names resolve (heartbeatobservatory.com, ntfy.sh, github.com) |
| OK | Website pages | the 10 main pages of heartbeatobservatory.com load | all 10 pages answer 200 |
| OK | Today's news show | the daily show is live (by 8 AM) | today's show is in the index and its video loads |
| OK | Database (Supabase) | the database behind the mailbox, Control Room and news answers | database answers (AI mailbox read worked) |
| OK | The creature | her world (Cloudflare Worker) is up and her clock moves | alive, tick 7936 (was 7890 at the last Creature Watch) |
| OK | MSI dark alarm | buzzes Jaron if the MSI goes quiet 20 min (off, or stuck at the sign-in screen) | watching from Cloudflare: last check-in 2 min ago, its own check ran 2 min ago |

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
| OK | Processor speed cap | keeps the worn fast core below the speed where it makes mistakes (11/24) | fast cores' top speed: plugged in = 4600 MHz (4.6 GHz), on battery = 4600 MHz (4.6 GHz) |
| OK | Disk space | room for the nightly news render (~70 GB) | 172 GB free |
| OK | GPU heat | the MSI isn't overheating | 47C, 0% busy |
| OK | Power and memory | plugged in, enough RAM | plugged in, battery 90%, 17.9 GB RAM free |
| OK | Windows restart pending | updates waiting for a restart | no restart pending (up since Sun Nov 22 4:13 PM) |
| OK | Database size | Supabase stays under its 8 GB cap | 2.25 GB of 8 GB (28%) / biggest: qwen_events 1999MB, fly_school 136MB, cosmos_terrain_bricks 19MB |
| OK | Logins | every login the system uses still works | all logins fine (checked 2026-11-24 10:20) |
| OK | AI-Shared saved to GitHub | this folder is backed up | main...origin/main [ahead 6] (recent; its own job pushes it) |
| OK | Public copy pushed in the last 48 hours | the scrubbed public AI-Shared reaches GitHub nightly | pushed 11 h ago; last nightly: FLAGS: none |
| OK | Watch repo saved to GitHub | the news watch repo is pushed | in step with origin/master |

**Scheduled jobs**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | HB Watch Loop | answers Jaron's "Tell Claude" watch messages by ntfy | last run 11-24 10:31, result 0 |
| OK | HB Key Drop | files and tests API keys Jaron pastes on his phone | last run 11-24 10:30, result 0 |
| OK | Crypto Consensus | crypto decision tick (money side) | last run 11-24 10:31, result 0 |
| OK | Crew Publish | publishes the public system/crew page | last run 11-24 10:30, result 0 |
| OK | MSI Beat | checks in with the off-MSI alarm on Cloudflare (quiet 20 min = one buzz) | last run 11-24 10:30, result 0 |
| OK | HB Video Drop | picks up videos dropped for the site | last run 11-24 10:27, result 0 |
| OK | HB Price Alerts | price alerts (money side) | last run 11-24 10:31, result 0 |
| OK | Live Board | the live data board | last run 11-24 10:28, result 0 |
| OK | Crypto Notify | crypto notices (money side) | last run 11-24 10:23, result 0 |
| OK | Usage Snapshot | the AI usage meter | last run 11-24 10:26, result 0 |
| OK | Desk Schedule Watch | desk schedule check (money side) | last run 11-24 10:26, result 0 |
| OK | Twin Crypto Settle | settles the twin's paper crypto (money side) | last run 11-24 10:24, result 0 |
| OK | HB News Watchdog | buzzes if today's news isn't live (7 AM-noon) | last run 11-24 10:30, result 0 |
| OK | MSI Connector Watch | buzzes if the connector/Cosmos/relay is down | last run 11-24 10:22, result 0 |
| OK | Creature Watch | looks in on the creature (read-only) | last run 11-24 10:03, result 0 |
| OK | HB Safety Signal | safety level from the DHS feed | last run 11-24 10:29, result 0 |
| OK | MSI Status | writes state/MSI-STATUS.md | last run 11-24 10:19, result 0 |
| OK | Sapling Watch | watches Sapling (read-only) | last run 11-24 10:15, result 0 |
| OK | Sapling Wake | Sapling's own wake | last run 11-24 10:22, result 0 |
| OK | DB Size Check | database size vs the 8 GB cap | last run 11-24 10:25, result 0 |
| OK | MSI Health | hourly task/port health | last run 11-24 10:02, result 0 |
| OK | HB AI Fund | AI fund (money side) | last run 11-24 10:17, result 0 |
| OK | Hourly helpers | live readings, news desks, rolling wire, prep watch | all 4 ran on time and finished ok |
| OK | Nightly news pipeline | GPU guard 2:38, render 3:50, writer 4:20, paper book 9:05, socials 7:15/8:45/5 PM | all 7 ran on time and finished ok |
| OK | Nightly news collectors | the Watch ... collectors and What's New scouts | all 14 ran on time and finished ok |
| OK | Backups and saves | nightly save 22:55, creature 21:15, off-MSI backup 21:30, Sapling GitHub 18:17 | all 4 ran on time and finished ok |
| OK | Weekly Drive copy | one AI-Shared file into Google Drive, Sunday 21:00 (a skipped week is fine) | all 1 ran on time and finished ok |
| BROKEN | Processor yardstick | daily 3-minute wrong-answer test on every core, 11:30 (exit 1 = failures) | MSI Core Yardstick disabled |
| OK | Other daily jobs | login watch, usage ledger, build ledger, render maintainer, firsts, Sapling status, atlas | all 8 ran on time and finished ok |
| OK | Weekly jobs | stale sweep, AI fund review, budget report, edge check, crypto caps | all 5 ran on time and finished ok |
| OK | Any other job | catches failures in jobs not listed above (vendor and one-shot reminders skipped) | no other job failed in the last 2 days |

**Off on purpose**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| SKIPPED-ON-PURPOSE | Polymarket system | trading on Polymarket is off since 10/28 | Polymarket system is DOWN by Jaron's 10/28 decision - never restarted here; trading tasks still disabled; Polymarket MCP task Ready (last run 2026-11-22); Trade Verifier still scheduled and ends 1 because nothing real answers on 8765 (state/verifier.md 1.3 MB); Connector Watch's Polymarket restart is off |
| SKIPPED-ON-PURPOSE | Paused projects | fly brain and retired helpers stay off | 20 paused tasks (fly brain, old gateways, retired desks), all still off |
| SKIPPED-ON-PURPOSE | Google Drive backups | Drive's index kept breaking; the big copies go off-MSI to Supabase; Drive keeps one weekly file | Google Drive is out of the backups (Jaron 11/24: 'Google Drive has always had issues'); the off-MSI Supabase backup covers everything; its 3 jobs stay off |
| SKIPPED-ON-PURPOSE | Codex Observer | an old Codex side project | Codex Observer server + tunnel (Registry Run entries) - not checked; ask Jaron if still wanted |

<!-- run -->
## Tue Nov 24 10:29 AM - 2 broken: The Cosmos game server, Processor yardstick  (dry run: nothing restarted)

**Still broken:**
- **The Cosmos game server** - local ok, public 200; watchdog NOT running; 0 restarts today
- **Processor yardstick** - MSI Core Yardstick disabled _(not sent to the phone; listed for Claude)_

**Internet and website**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | Internet | the MSI can reach the internet at all | names resolve (heartbeatobservatory.com, ntfy.sh, github.com) |
| OK | Website pages | the 10 main pages of heartbeatobservatory.com load | all 10 pages answer 200 |
| OK | Today's news show | the daily show is live (by 8 AM) | today's show is in the index and its video loads |
| OK | Database (Supabase) | the database behind the mailbox, Control Room and news answers | database answers (AI mailbox read worked) |
| OK | The creature | her world (Cloudflare Worker) is up and her clock moves | alive, tick 7932 (was 7890 at the last Creature Watch) |
| OK | MSI dark alarm | buzzes Jaron if the MSI goes quiet 20 min (off, or stuck at the sign-in screen) | watching from Cloudflare: last check-in 4 min ago, its own check ran 4 min ago |

**Reaching the MSI**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | MSI connector (Grok Machine MCP) | the bots and chat AIs can reach the MSI | server up on 3001, public address answers 401 (401 = up, asking for sign-in) |
| OK | Cloudflare tunnel | carries the connector and Cosmos to the internet | tunnel service running and ready |
| BROKEN | The Cosmos game server | the Cosmos world server and its watchdog | local ok, public 200; watchdog NOT running; 0 restarts today |

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
| OK | Processor speed cap | keeps the worn fast core below the speed where it makes mistakes (11/24) | fast cores' top speed: plugged in = 4600 MHz (4.6 GHz), on battery = 4600 MHz (4.6 GHz) |
| OK | Disk space | room for the nightly news render (~70 GB) | 172 GB free |
| OK | GPU heat | the MSI isn't overheating | 49C, 0% busy |
| OK | Power and memory | plugged in, enough RAM | plugged in, battery 90%, 17.7 GB RAM free |
| OK | Windows restart pending | updates waiting for a restart | no restart pending (up since Sun Nov 22 4:13 PM) |
| OK | Database size | Supabase stays under its 8 GB cap | 2.25 GB of 8 GB (28%) / biggest: qwen_events 1999MB, fly_school 136MB, cosmos_terrain_bricks 19MB |
| OK | Logins | every login the system uses still works | all logins fine (checked 2026-11-24 10:20) |
| OK | AI-Shared saved to GitHub | this folder is backed up | main...origin/main [ahead 6] (recent; its own job pushes it) |
| OK | Public copy pushed in the last 48 hours | the scrubbed public AI-Shared reaches GitHub nightly | pushed 11 h ago; last nightly: FLAGS: none |
| OK | Watch repo saved to GitHub | the news watch repo is pushed | in step with origin/master |

**Scheduled jobs**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| OK | HB Watch Loop | answers Jaron's "Tell Claude" watch messages by ntfy | last run 11-24 10:28, result 0 |
| OK | HB Key Drop | files and tests API keys Jaron pastes on his phone | last run 11-24 10:28, result 0 |
| OK | Crypto Consensus | crypto decision tick (money side) | last run 11-24 10:29, result 0 |
| OK | Crew Publish | publishes the public system/crew page | last run 11-24 10:25, result 0 |
| OK | MSI Beat | checks in with the off-MSI alarm on Cloudflare (quiet 20 min = one buzz) | last run 11-24 10:25, result 0 |
| OK | HB Video Drop | picks up videos dropped for the site | last run 11-24 10:27, result 0 |
| OK | HB Price Alerts | price alerts (money side) | last run 11-24 10:26, result 0 |
| OK | Live Board | the live data board | last run 11-24 10:28, result 0 |
| OK | Crypto Notify | crypto notices (money side) | last run 11-24 10:23, result 0 |
| OK | Usage Snapshot | the AI usage meter | last run 11-24 10:26, result 0 |
| OK | Desk Schedule Watch | desk schedule check (money side) | last run 11-24 10:26, result 0 |
| OK | Twin Crypto Settle | settles the twin's paper crypto (money side) | last run 11-24 10:24, result 0 |
| OK | HB News Watchdog | buzzes if today's news isn't live (7 AM-noon) | last run 11-24 10:15, result 0 |
| OK | MSI Connector Watch | buzzes if the connector/Cosmos/relay is down | last run 11-24 10:22, result 0 |
| OK | Creature Watch | looks in on the creature (read-only) | last run 11-24 10:03, result 0 |
| OK | HB Safety Signal | safety level from the DHS feed | last run 11-24 10:29, result 0 |
| OK | MSI Status | writes state/MSI-STATUS.md | last run 11-24 10:19, result 0 |
| OK | Sapling Watch | watches Sapling (read-only) | last run 11-24 10:15, result 0 |
| OK | Sapling Wake | Sapling's own wake | last run 11-24 10:22, result 0 |
| OK | DB Size Check | database size vs the 8 GB cap | last run 11-24 10:25, result 0 |
| OK | MSI Health | hourly task/port health | last run 11-24 10:02, result 0 |
| OK | HB AI Fund | AI fund (money side) | last run 11-24 10:17, result 0 |
| OK | Hourly helpers | live readings, news desks, rolling wire, prep watch | all 4 ran on time and finished ok |
| OK | Nightly news pipeline | GPU guard 2:38, render 3:50, writer 4:20, paper book 9:05, socials 7:15/8:45/5 PM | all 7 ran on time and finished ok |
| OK | Nightly news collectors | the Watch ... collectors and What's New scouts | all 14 ran on time and finished ok |
| OK | Backups and saves | nightly save 22:55, creature 21:15, off-MSI backup 21:30, Sapling GitHub 18:17 | all 4 ran on time and finished ok |
| OK | Weekly Drive copy | one AI-Shared file into Google Drive, Sunday 21:00 (a skipped week is fine) | all 1 ran on time and finished ok |
| BROKEN | Processor yardstick | daily 3-minute wrong-answer test on every core, 11:30 (exit 1 = failures) | MSI Core Yardstick disabled |
| OK | Other daily jobs | login watch, usage ledger, build ledger, render maintainer, firsts, Sapling status, atlas | all 8 ran on time and finished ok |
| OK | Weekly jobs | stale sweep, AI fund review, budget report, edge check, crypto caps | all 5 ran on time and finished ok |
| OK | Any other job | catches failures in jobs not listed above (vendor and one-shot reminders skipped) | no other job failed in the last 2 days |

**Off on purpose**

| Result | Part | What it's for | Detail |
|---|---|---|---|
| SKIPPED-ON-PURPOSE | Polymarket system | trading on Polymarket is off since 10/28 | Polymarket system is DOWN by Jaron's 10/28 decision - never restarted here; trading tasks still disabled; Polymarket MCP task Ready (last run 2026-11-22); Trade Verifier still scheduled and ends 1 because nothing real answers on 8765 (state/verifier.md 1.3 MB); Connector Watch's Polymarket restart is off |
| SKIPPED-ON-PURPOSE | Paused projects | fly brain and retired helpers stay off | 20 paused tasks (fly brain, old gateways, retired desks), all still off |
| SKIPPED-ON-PURPOSE | Google Drive backups | Drive's index kept breaking; the big copies go off-MSI to Supabase; Drive keeps one weekly file | Google Drive is out of the backups (Jaron 11/24: 'Google Drive has always had issues'); the off-MSI Supabase backup covers everything; its 3 jobs stay off |
| SKIPPED-ON-PURPOSE | Codex Observer | an old Codex side project | Codex Observer server + tunnel (Registry Run entries) - not checked; ask Jaron if still wanted |

