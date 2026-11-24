# Kit inventory - everything we've built, sorted for the kit (2026-11-16, Claude Code)

Made from real code, the scheduled tasks on the MSI, and the live site (checked 11/16 ~3:30 PM), not from READMEs.
Goes with SYSTEM-FOR-OTHERS.md ("The kit repo: 5 stages") and AI-SHARED-CLOUD-KIT-2026-11-16.md.

## Summary (10 lines)
1. We've built about 90 pieces. Most already work every day on the MSI. The kit is mostly writing down how we already work, minus what's only ours.
2. Must-haves that already exist and work: the entry file (AGENTS.md), mailbox, settings page (Control Room), Key Drop, phone buzz (ntfy), handoffs, timeline, the Edit button, and the Live / Preview / In progress labels.
3. Missing must-haves: the "owner now" page, the day-one explanation, a corrections log, a settling-in period, a plan for when the owner goes quiet, and a usage meter that works for one subscription.
4. Fields that come with the kit but can be switched off (news, TV, social, library, games, worlds, studio) all work for us. They lean on the MSI's GPU and on 8+ AI news desks.
5. The AI team runs on 4 subscriptions plus 4 pay-as-you-go accounts, about $273 a month on record. A new owner can start with 1 (Claude or ChatGPT). 2 (Claude + ChatGPT) is the pair we've proven.
6. Some of our flow is habit: 8+ news desks every night, Grok Build pasting into the Grok Bot window, one scout per AI company, and a routing table that no longer matches the real team.
7. Owners with no computer: about 70% moves to the cloud without trouble (Supabase, Vercel, GitHub, ntfy, cloud Claude, Grok Bot). The real limits are GPU video (rent it or render lighter), local models (optional), and Key Drop's unlock step (needs a cloud secret store).
8. Usage tracking works for Codex (exact numbers) and for Claude tokens (but not Claude's real %). Grok, Grok Bot and Kimi aren't read by any script. The budget report's bill list is out of date.
9. Biggest gap per stage: 1 the day-one explanation, 2 a path when something can't connect, 3 the swap check, 4 the settling-in period, 5 hands-off mode when the owner goes quiet.
10. Flagged: Polymarket is "down", but its live-mode scripts still run every few minutes (idle, no money moving). Plus a few failed tasks and some stale files (end of this page).

How to read the tables
- **Stage:** 1 Getting started, 2 Connecting, 3 AI team, 4 Rhythm, 5 Running.
- **Bin:** MUST = every setup needs it. COMES = comes with every setup, can be switched off. OPT = optional add-on. OURS = only ours.
- **Status:** WORKS = checked today (task ran OK today, page loads, or file is current). PART = exists but has a hole. PLAN = talked about, not built.

---

## 1. Every capability we've built

### A. Owner pages and small owner tools (site: heartbeatobservatory.com)
| Piece | What it does | Stage | Bin | Status | Depends on |
|---|---|---|---|---|---|
| Steering (/admin/) | Owner's home for all admin pages, sign-in only | 5 | MUST | WORKS (page loads, sign-in) | Supabase sign-in + `is_admin()`, Vercel |
| Admin page house rule (docs/ADMIN-PAGES.md, site repo) | Back link, tabs in the web address, phone first, matches the page look | 5 | MUST | WORKS | none (a rule) |
| Control Room (/admin/control/) | Settings and limits page: every number the scripts read (Supabase `system_settings`, tools/settings.py) | 5 | MUST | WORKS | Supabase |
| Key Drop (/admin/keys/) | Owner pastes a key on the phone. It's locked in the browser, and only the MSI can open it. tools/key_drop.py files it, tests it, and writes state/KEYS.md (names only) | 2 | MUST | WORKS (task OK 3:24 PM) | Supabase + the MSI's private key. **No-computer owner: needs a cloud secret store** |
| Edit button (hb-editor.js + api/site-edit.js) | Owner changes any words, hides cards and tabs, and arranges the home page from the phone. Every save is a GitHub commit, so any earlier version can be restored | 5 | COMES | WORKS | GitHub token on Vercel, Supabase admin check |
| Live / Preview / In progress labels | Each home section has a status label (Supabase `surfaces` table). Lets an unfinished company run in public honestly. **Note: the code says "In progress", not "Coming soon"** | 5 | COMES | WORKS (home shows Live + Preview) | Supabase |
| Auto-stamp (tools/stamp-shared.mjs) | Every page gets the phone, the Edit button, analytics and the home-screen icon at deploy. Pages can opt out | 5 | MUST (if there's a site) | WORKS | Vercel build step |
| Mailbox page (/admin/mailbox/) | Owner reads all AI-to-AI messages | 3 | MUST | WORKS | Supabase `ai_mailbox` |
| Video Drop (/admin/video-drop/) | Owner uploads phone videos, and the MSI picks them up every 5 min | 5 | COMES | WORKS (task OK today) | Supabase storage. Cloud worker possible |
| Remote screen (/admin/remote/) | Owner sees and drives the MSI screen from the phone | 5 | OPT | PART (keepalive running; Remote Screen task last result was an error code) | MSI + remote agent. **No computer = not needed** |
| Sapling control (/admin/sapling/) | Plain-words control room plus chat for our own small AI | 5 | OPT | WORKS | MSI GPU, Sapling |
| AI Fund Desk (/admin/fund/) | Paper-only company fund run by AIs (started 11/13, $100k pretend) | 5 | OPT | WORKS (paper) | free market data, MSI task |
| Crew page (/live-systems/crew/) | Publishes every bot's real instructions in public (publish-crew.py) | 5 | COMES | WORKS (task OK today) | MSI task. **Kit must screen out private things** |
| Artifacts (/artifacts/) | "Made with our own tools" list, each with an honest "not there yet" | 5 | COMES | WORKS | artifacts.json |
| Standards (/standards/) | How the company treats people, AI, and unfinished work | 1 | COMES (as a template) | WORKS | none |
| Sparks page (/sparks/) | People whose work inspired Heartbeat | 5 | OURS (template could be OPT) | WORKS | none |
| Idea Bank (/ideas/) | Free public-domain business ideas | 5 | OPT | WORKS | none |
| Work with us (/work/) | Local-business website service | 5 | OURS | WORKS | none |
| Phone (bubble.js) | Messages phone on every page | 5 | COMES | WORKS | Supabase |

### B. Fields (the "many fields" of one company)
| Piece | What it does | Stage | Bin | Status | Depends on |
|---|---|---|---|---|---|
| Heartbeat News, writer | Claude cloud routine writes the day's episode at 3:45 AM. MSI backup writer (Claude, then Codex) | 5 | COMES | WORKS (today's episode is live) | Claude plan. Already cloud |
| News desks (Watch Claude/Codex/DeepSeek/Grok Blind Spots/Grok Meridian/Kimi First Light/MSI Reader/Perplexity/Funding Lane/Rolling Wire/Top Stories/Missed Story Check) | Each AI gathers stories overnight (3-4 AM). Hourly wire. Morning missed-story check | 5 | COMES | WORKS (all ran OK today) | 5 different AI meters + Perplexity + DeepSeek APIs |
| Rendered news show | Voices (Kokoro, eSpeak) -> plan -> Unreal render -> mp4 -> Supabase storage. Fast mode if running late | 5 | COMES | WORKS (published 7:12 AM; the long vertical/YouTube cuts failed today) | **MSI GPU + Unreal 5.8.** No computer: rent a GPU or use a lighter show (voice + still boards) |
| News Watchdog, GPU Guard, Paper Book | Buzzes if the show isn't up by 7 AM. Keeps the GPU free 2:40-7:30 AM. Daily paper | 5 | COMES | WORKS | MSI |
| TV (/tv/) | Channels: News, Shows, Movies, Comedy, Music, AI Slop, History, Science, Open Questions, Still Unknown (`tv_items` in Supabase) | 5 | COMES | WORKS | Supabase + whatever makes the episodes |
| Science channel episodes | Blender sets + picture boards + Kokoro voice, 5-8 min, with a fact check | 5 | COMES | WORKS (8.11 shipped 11/15) | **MSI GPU, Blender, Unreal** |
| Social posting (social_daily.py via Postiz) | Daily news + show clips to X, YouTube, TikTok. X "moment" posts | 5 | COMES | WORKS (YouTube daily limit keeps biting) | Postiz $29/mo. Already cloud |
| Social network (/social/) | The site's own social area | 5 | COMES | WORKS (page loads; depth not checked) | Supabase |
| Library (/library/) | Bookshelf / reading room | 5 | COMES | WORKS (page loads) | none |
| Games (/games/, The Cosmos) | Browser 3D games, each with a site page | 5 | COMES | WORKS (page loads; Cosmos is 3rd in the build order) | browser only. Building needs strong AI builders |
| Worlds (Town Square /engine/, World 2, Ashgrove /world3/) | Walkable 3D worlds (thumbstick), site pages as objects inside | 5 | COMES | WORKS/PART (World 2 remake is the next big build) | browser, Supabase for shared state |
| Homes (/homes/) | Your own loft to walk, with a TV | 5 | OPT | WORKS | Supabase |
| Studio (/studio/) | Record over a beat on the phone | 5 | OPT | WORKS | browser |
| Real City, Power Map, Island, Museum, 3D Printer | Side builds | 5 | OPT / OURS | WORKS (pages load) | browser, some Supabase |
| Safety Signal (tools/safety_signal.py) | 0-5 level for Jaron's network, Satya twin keeps it, buzzes the phone | 5 | OPT | WORKS (task OK today) | Grok Bot + ntfy |
| Atlas convergence | Grok reads world events daily, sends a read to the safety signal | 5 | OPT | WORKS | Grok Build |
| What's New scouts | Each AI checks its own company's news every night | 4 | COMES (as "keep the team current") | WORKS | Codex, Grok, Claude |
| Polymarket trading (executor, verifier, crypto lane, live board, Polymarket MCP) | Was the money lane | - | OURS (**not in kit**, Jaron 11/16) | DOWN by policy, but scripts still scheduled (see flags) | MSI, Polymarket US |
| Price alerts, Edge check, Twin crypto paper | Phone buzz at a price; trade-estimate scoring; paper calls | 5 | OPT | WORKS | free price feeds |
| Sapling (own small AI) | Trained core + heartbeat + memory + exams. Kimi trains it | 5 | OPT | WORKS (running now) | **MSI GPU** (RunPod for big runs). No computer: rented GPU only |
| hb-render (own render engine) | WebGPU path tracer, runs in a browser or headless; site /render/ test | 5 | OPT | PART (v0) | GPU. Runs in a phone browser for small scenes |
| Fly brain / Fly School | Simulated fruit-fly brains | - | OURS | Paused on purpose (tasks disabled) | MSI |

### C. AI team and coordination
| Piece | What it does | Stage | Bin | Status | Depends on |
|---|---|---|---|---|---|
| AGENTS.md (entry file, one page) | First thing every AI reads. Points to other files only when needed | 1 | MUST | WORKS (fixed today: roofing line) | none |
| Conductor (Claude Code, one long session) | Talks to the owner, decides, hands out jobs, sets the quality bar | 3 | MUST | WORKS | Claude plan + MSI today. Cloud session proven 11/16 |
| Mailbox (tools/mailbox.py, mailbox_wait.py, docs/MAILBOX-FOR-AIS.md) | Every AI sends finished/stuck notes to the conductor. The waiter wakes the conductor | 3 | MUST | WORKS (cloud-only test passed 11/16) | Supabase. The waiter runs on the MSI today; cloud = database trigger |
| Job router (tools/route.py + state/routing.json) | Picks a builder by job type and live usage | 3 | MUST | PART (table is stale, see flags) | usage-live.json |
| Job handoff log (tools/handoff_log.py, state/job-handoffs.md) | Logs when a job moves between AIs, and why | 3 | COMES | WORKS | none |
| Handoffs folder | Where the work stands, written at session end | 3 | MUST | WORKS | none |
| bot-chat.md | Running log of what the owner told the other AIs | 3 | MUST | WORKS | none |
| Grok Bot relay (`grok -p` drives the Grok Bot window) | Sends a message to a cloud bot | 3 | OURS (habit) | WORKS, fragile | MSI desktop window open and signed in |
| Grok Bot twins (Darios, Satya, Jarons Twin, Sams, Elons, Link, Pip) | Cloud bots with their own computers: safety signal, X watch, bills checks | 3 | OPT | WORKS (Satya + Link posted today) | SuperGrok. Already cloud |
| Grok Bot Vault (docs/GROK-BOT-VAULT.md) | Logins and cards bots can use without seeing numbers | 2 | OPT | WORKS | Grok Bot |
| Worrier (agents/worrier) | Audits a log or plan for holes | 3 | OPT | WORKS (11/14 audit) | any AI |
| Backlog + sweeps (state/backlog.json, SITE-BACKLOG.md) | Small jobs for every page, handed out through the day | 5 | COMES | WORKS (last written 11/6) | conductor |
| Build ledger (tools/build_ledger.py) | What each AI built this week, from git | 5 | COMES | WORKS | git |
| Codex / Kimi / DeepSeek / Qwen command lines | Headless workers (`codex exec`, `kimi --auto`, qwen-bridge) | 3 | OPT | WORKS (Qwen dropped 9/30) | MSI. Codex, Kimi and Grok also have cloud versions |

### D. Memory, rhythm and the owner's own record
| Piece | What it does | Stage | Bin | Status | Depends on |
|---|---|---|---|---|---|
| "Owner now" page | Who the owner is today (current vs past roles, confirmed dates) | 1 | MUST | PLAN (AGENTS.md "who Jaron is" + memory files cover it today) | none |
| Spiderweb intake | Digs through chats, photos, notes and email (with consent) to find sparks | 1 | MUST | PLAN (method proven by hand on Jaron's ChatGPT history) | connectors the owner allows |
| Timeline (state/timeline.md) | Every decision and ship, with time and duration | 4 | MUST | WORKS | none |
| Spark log (research/how-ideas-form/LOG.md) | What came right before an idea connected | 4 | MUST | PART (started today, 3+ entries) | none |
| Principles ledger (projects/principles/LEDGER.md) | Owner's principles with IDs (167 entries) | 4 | OPT (open: for others or not) | WORKS | none |
| Corrections log | When an AI misread the owner | 4 | MUST | PLAN (a field in the spark log; scattered in memory files today) | none |
| Open questions ledger (decisions/OPEN-QUESTIONS.md) | Unanswered owner questions stay open | 4 | MUST | WORKS (last edit 10/28) | none |
| Open list + "Next thing" ending | One next step at the end of every reply | 4 | COMES | WORKS | none |
| Day log (projects/reality-agent/day-log/) | Owner's day, private | 4 | OPT | WORKS | none |
| Bills + life admin (projects/life/) | Bills, due dates, accounts | 5 | OPT | WORKS | none. **Private, never in the kit** |
| Reminders (tools/ntfy-say.py + one-time tasks) | Phone buzz on a date | 4 | COMES | WORKS | ntfy + a scheduler |
| Brainstorm window at peak hours | Daily idea time (Jaron's 9 AM-noon) | 4 | COMES | PLAN | owner's logs |
| Look settings (colors, text size, how much at once) | How words show for each owner | 4 | COMES | PLAN (only Jaron's warm cream / warm dark is known) | site + chat |
| AI behavior findings (research/AI-BEHAVIOR-FINDINGS.md) + Framing Lens tests | How each model acts, used to pick models | 3 | OPT | WORKS | none |
| Claude memory files + FROM-ME notes | Conductor's own carry-over | 3 | MUST (in some form) | WORKS, but tied to one Claude account | Claude Code. **Kit: must live in repo files to survive a model swap** |

### E. Keeping it running (health, logins, saves)
| Piece | What it does | Stage | Bin | Status | Depends on |
|---|---|---|---|---|---|
| ntfy phone buzz | Any script can buzz the owner's phone | 2 | MUST | WORKS | free ntfy app |
| Login Watch + RECONNECT.md | Checks every login, buzzes with the numbered fix steps | 2 | MUST | WORKS (task OK today) | MSI task. Cloud = GitHub Actions |
| WHEN-IT-BREAKS.md | What to do when something breaks | 5 | MUST | WORKS | none |
| MSI Status / MSI Health | Heat, power, disk, failed tasks every 30 min | 5 | OURS (computer owners only) | WORKS | MSI |
| Connector Watch | Buzzes if the phone connector to the MSI drops | 5 | OPT | WORKS | MSI + cloudflared |
| Nightly Save | Pushes AI-Shared to private GitHub at 11:55 PM, stops if a key is in a file | 5 | MUST | WORKS (ran 11/15) | GitHub |
| Drive mirror + Unreal backup | Copies to Google Drive nightly | 5 | OPT | WORKS | Google Drive desktop |
| Stale Sweep | Lists lines in first-read files that may be out of date | 5 | MUST | WORKS | none |
| DB Size Check | Watches the Supabase database size | 5 | COMES | WORKS | Supabase |
| Live Readings | Balances (DeepSeek, etc.) to the Control Room | 5 | COMES | WORKS | MSI task |
| Cloud GPU log (state/cloud-gpu-log.md) | Every RunPod pod ends and is logged | 5 | OPT | WORKS | RunPod |
| Tell Claude (Siri -> watch-inbox -> mailbox -> watch_loop -> ntfy) | Owner talks from wrist or phone, gets a short answer | 4 | COMES | PART (HB Watch Loop's last run gave result 1; failed in the last 2 days) | Supabase + MSI loop. Cloud = edge function |

---

## 2. The AI team map

| AI / subscription | What it does for us | Cost (on record) | Honest note |
|---|---|---|---|
| **Claude Max** (Opus 5.5 conductor; Sonnet 5.5, Fable 5.1/5.2, Opus builders; Haiku lookups) | Conductor, looks bar, most building (about 5,600 of 6,150 commits this month), news writer (cloud routine), Science episodes | $100/mo + API credits + some extra-usage credits | Runs near its weekly limit (~90%). Fable is the expensive one |
| **ChatGPT Plus / Codex** (Luna chores, Sol/Terra builds, Astra rarely) | Chores, fact-checks, backup news writer, OpenAI scout. ChatGPT chat = outside "scientist" review, reaches the MSI through Desktop Commander | $20/mo | Only 6% of its week used. Room left. Astra empties a window in minutes |
| **SuperGrok** (Grok Build CLI + Grok Bot) | Grok Build: builder, 2 news desks, Atlas, watches video, xAI scout. Grok Bot twins: safety signal, X watch (Link), bills checks (Pip) | $30 per 3 months (Apple) + Cursor overage up to $15/mo | Usage isn't readable by a script. Twins were built for trading, which is down |
| **Kimi Allegretto** (K3.1 Pro) | First Light news desk, trains Sapling, big one-shot builds, long unattended jobs | $39/mo (web since 11/6) | Good for big first drafts that others finish. Not in the budget report |
| **DeepSeek API** | Overnight news reader, cheap research | top-ups (daily budget in the Control Room) | Trading use paused since 10/1 |
| **Perplexity API** | News scout + hourly wire | ~$2/mo | Proven: found stories every desk missed |
| **Qwen / llama (Ollama, local)** | Was a local helper; bridge still exists | free | Dropped from active use 9/30. Ollama still starts at boot |
| **Google AI Plus** | Drive storage; Gemini app for Jaron; Jules untested | $2.99/mo (then $9.99 from Feb 13) | No API credits included |
| OpenAI / Anthropic API keys | Pay per use, any model | per use | |
| Postiz (not an AI, but part of the team flow) | Posts to X, YouTube, TikTok | $29/mo | |

**Total on record: about $273/month** (Claude 100, ChatGPT 20, Grok ~10/mo, Kimi 39, Supabase 25, Postiz 29, X Premium 30) plus top-ups (DeepSeek, Perplexity, RunPod, Cursor).

**A new owner with 1 or 2 subscriptions**
- **One subscription (Claude Pro/Max or ChatGPT Plus):** that one is the conductor and builds through its own helpers (Claude: Sonnet/Haiku helpers; ChatGPT: Codex Luna for chores). News = one writer plus free feeds (RSS, a free Perplexity-style search if there's budget). Cloud routines run the schedule. No Grok Bot, no Kimi.
- **Two (Claude + ChatGPT):** the pair we've proven. Claude conducts and builds the looks. Codex does chores and fact-checks on a separate meter. Second choice: Claude + Grok, if the owner lives on X or wants cloud bots with their own computers.
- **Add-ons when they grow:** Kimi (big one-shot builds), Grok Bot (always-on cloud bots), Perplexity API (news scout, pennies), DeepSeek (cheap reading).

**Where our flow is just habit (a better one may exist)**
- **8+ news desks every night.** This grew from "missed story" checks. A new owner gets most of the value from 1 writer + 1 cross-check + the free wire. Perplexity is the one desk with proof it adds stories.
- **Grok Build pasting into the Grok Bot window** to message bots. This breaks if the window closes. The bots already read the mailbox, so mailbox-only is the cleaner path.
- **One "What's New" scout per AI company**, each AI checking its own maker. That was kept partly for blind-spot research. One scout with web search could cover all three.
- **routing.json is a fixed table**, and the real routing is the conductor's judgment. The table lists a pool we can't use (gpt-reserve) and leaves out Kimi, Fable 5.2, DeepSeek and Perplexity.
- **Twins as traders.** Their surviving jobs (safety signal, X watch, bills) could fit in fewer bots.
- **One long conductor session** works for Jaron (lots of context, low cost). But it ties judgment to one session and one model. The kit should keep that judgment in repo files (owner-now page, spark log, corrections log), so a cloud or swapped conductor can pick up.
- **Kimi as Sapling's trainer** is not habit. It comes from provider terms (Claude/OpenAI text stays out of training).

---

## 3. The machine map (MSI)

Hardware: MSI laptop, **Intel i9-14900HX, 32 GB RAM, NVIDIA RTX 4060 Laptop (8 GB), 173 GB free on C:**. Never sleeps on power, signs in by itself after a reboot.

| Software / hardware | What it powers | Owner with no computer |
|---|---|---|
| RTX 4060 GPU | News render, Science/TV episodes, Sapling training, hb-render | Rent by the hour (RunPod, ~$4.50 per Sapling run on record) or render lighter (voice + still boards). Terminate every pod |
| Unreal Engine 5.8 (+5.6) | Daily rendered news show, film and episode scenes | Rented GPU with Unreal (heavy setup), or skip it and use a lighter show. Hardest piece to move |
| Blender 5.1 | Science episode sets, world assets | Rented GPU. Or browser 3D (three.js) for simpler scenes |
| ffmpeg 8.1 | Cutting and joining video, vertical cuts | Runs anywhere (GitHub Actions, cloud worker) |
| Kokoro + eSpeak (voices) | News anchors, narration | Cloud voice services (cost) or Kokoro on a rented CPU/GPU |
| Ollama (qwen3.5 9b/4b, llama3.2 3b) | Local model (dropped 9/30) | Optional add-on only; skip |
| Python 3.12 (scoop) | ~265 tools: every scheduled job | Same scripts in GitHub Actions / cloud worker |
| Node.js | Postiz CLI, MSI connector server, hb-render worker, site stamping | Same, in the cloud |
| Git + GitHub CLI | Site deploys, nightly save, Edit button history | Already cloud |
| Vercel CLI / Supabase CLI | Site hosting, database changes | Already cloud |
| cloudflared tunnel + "Grok Machine MCP" server | The one MSI connector with three names (Heartbeat MAI / Grok Machine / msi-heartbeat): how phone AIs reach the MSI | Not needed. Cloud AIs talk through Supabase instead |
| Desktop Commander (remote) | ChatGPT's door into the MSI | Not needed. ChatGPT already used the mailbox straight through Supabase |
| Claude Code (CLI + desktop) | Conductor and builders, headless jobs with a 1-year token | Claude Code cloud sessions (needs the database domain allowed on the network) |
| Codex CLI, Grok Build CLI, Kimi Code CLI + Kimi Work desktop | Headless workers | Each has a cloud form (Codex cloud, Grok Bot computers, Kimi agent) |
| Grok Bot desktop window | Lets Grok Build message the bots | Not needed. Use the mailbox |
| Playwright / WebKit | iPhone-size checks before publishing | GitHub Actions can run it |
| Windows Task Scheduler (~95 of our tasks) | The whole daily rhythm | GitHub Actions, Vercel cron, Supabase pg_cron, cloud routines |
| Remote agent | Owner sees the MSI screen from the phone | Not needed |
| Google Drive desktop (G:) | Nightly mirror + Unreal backup | Cloud storage directly |
| Polymarket MCP, OpenClaw gateway | Old trading / local-model gateways | Not in the kit |

**What stays MSI-only today:** the long conductor session and its waiter, Key Drop's unlock step, GPU renders, local models, Desktop Commander, and the scheduled tasks themselves.

---

## 4. Usage tracking

**Today**
- `tools/usage.py` (task "Usage Snapshot", every 15 min) -> `state/usage-live.json`. **Codex:** exact 5-hour and weekly % from its own session logs (today 1% / 6%). **Claude:** tokens only. The real % isn't on disk, so it's an estimate checked against Jaron's screenshots. **Grok, Grok Bot, ChatGPT app:** nothing on disk. Readings get typed by hand into `state/grok-usage.md`.
- `tools/usage_ledger.py` (task "HB Usage Ledger", daily) -> `state/usage-ledger.md/.json`. Tokens per AI per job, per day, with a safe job name. Covers Claude, Codex, Kimi and Grok Build from local logs. Most Claude main-session lines are "Unlabelled work".
- `tools/ai-budget.py` (task "AI Budget Report", daily) -> `state/ai-budget.md`. Monthly bills next to trader profit, plus plain "point more work at X" advice. **Its bill list is stale**: no Google AI Plus, Perplexity, DeepSeek, RunPod or Cursor overage, and Grok's reading is from 10/1.
- `state/routing.json` limits: skip an AI over 85% of its 5-hour window or 90% of its week. `route.py` reads usage-live.json.
- Build ledger and handoff log show output per AI. Control Room has DeepSeek's daily budget. Live Readings shows balances.

**What the kit needs**
- One plain meter page: "how much is left this week" per subscription, plus money spent this month against the owner's cap.
- It must work for one subscription and in the cloud, where there are no local logs to read. For cloud owners: provider usage pages/APIs where they exist, plus the system counting its own jobs.
- Owner-set limits by area (content, games, money), so jobs stop or slow without the owner approving each step.
- Every job labeled at the start, so "Unlabelled work" doesn't take up most of the ledger.
- A bill list that updates itself from the bills file, not a hard-coded one.
- Plan by usage: the conductor spreads the week's work across meters (this is how it works for us in practice, but it isn't written down as a method).

---

## 5. Gaps - what a new owner is missing, by stage

**1. Getting started**
- How the AI explains itself on day one (plain words, analogies, a second voice if one doesn't land). Not written.
- "Owner now" page template (current vs past roles, confirmed dates, corrections). Not built.
- Spiderweb intake as a step-by-step method per source (chats, photos, notes, email) with consent per source. Only done by hand for Jaron.
- A clean starter repo: blank owner profile, blank rules (only "no weapons"), empty-but-described folders. AGENTS.md today is full of Jaron.
- Look settings asked on day one.

**2. Connecting everything**
- A needed-vs-optional account list (from KEYS.md + BILLS.md, minus ours) with numbered steps for the human-only pieces (RECONNECT.md is the model).
- A path when something can't connect (no ID, no bank, no computer): what still works, and what waits on which rung.
- Key Drop without a computer (cloud secret store).
- The cloud network step (allow the database domain) written as a step.

**3. Setting up the AI team**
- Swap check (hold back 3 logged cases, compare the new conductor's call). Designed, not built.
- "Read owner-now first" rule in the entry file.
- A routing table that matches the real team and can start with 1 AI.
- Mailbox waiter as a cloud trigger (not the MSI loop).
- Conductor memory kept in repo files, not in one provider's memory.

**4. Finding the rhythm**
- A settling-in period (a few weeks of light schedules while the system learns the owner's hours).
- Finding peak hours from their own logs, and the brainstorm window.
- Sleep/work rhythm and how the AI should talk to them, as settings, not memory notes.
- Corrections log as its own file.

**5. Running**
- Hands-off mode: what keeps going when the owner goes quiet (fields keep producing inside limits, a daily digest, no nagging).
- The three dials (how public, how much private data the AI gets, how much the AI acts alone) and per-area hands-off. Today these are Jaron's standing choices in memory, not switches.
- A daily digest for the owner (we have bot-chat, timeline, ntfy, but no single "today" page).
- Cloud schedules for each MSI task a no-computer owner needs (writer is already a cloud routine; the rest are Windows tasks).
- Caution tags (who raised a warning, what it covers, what kind) - designed, not built.
- Usage meter (section 4).

---

## Flags (things found while doing this, not changed)
1. **Polymarket is "down" (AGENTS.md, 10/28), but its scripts still run in live mode.** Trade Executor (`executor.py --live`) runs every few minutes and logs "nothing approved". Crypto Consensus runs every 5 min and set weekly caps for 3 twins this morning. Polymarket MCP and Live Board run too. No money is moving, but they burn cycles, and one approval row would place a real order. Worth a look by whoever owns trading. They must not go into the kit.
2. **Failed tasks:** HB Watch Loop ("Tell Claude") last result 1 today, and it failed in the last 2 days. Desk Weekly Review failed (result 1). Desktop Commander Remote task result 1 since the 10/31 boot: it was restarted by hand 11/12, so after a reboot ChatGPT's door may not come back on its own. HB Remote Screen task last result was an error code (keepalive is running).
3. **Stale files that AIs read:** `state/routing.json` (missing Kimi, Fable 5.2, DeepSeek, Perplexity; lists gpt-reserve, which isn't open). `tools/ai-budget.py` bill list. `INDEX.json` (last updated 10/21; old open blockers). These should be regenerated for the kit, not copied.
4. **Private items as scheduled-task names:** birthday, court and child-support reminders are named with family names. The kit repo must start clean, with a generic reminder tool, never a copy of our task list.
5. **Naming:** the site's status labels are "Live / Preview / In progress". The kit talks say "Coming soon". Pick one word.
6. **The crew page publishes bot instructions in public by design.** For other owners that has to follow their "how public" dial, not ours.
7. News today: the show went live at 7:12 AM, but the long vertical/YouTube cuts failed.

Verified locally: scheduled task names, actions and last results; file dates; tool headers; usage files. Verified live: the listed pages load (status 200), today's news episode exists, home page status labels. Unverified: depth of /social/, /library/ and the games/worlds beyond loading; Grok Bot routines (cloud, not readable from here); exact Claude usage %.
