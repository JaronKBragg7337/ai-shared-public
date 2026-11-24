# Heartbeat Observatory domains

Working map, 27 October 2026. One visible Claude session can own each domain. The main session coordinates shared decisions and dependencies. State below is from notes and recent commits, not a fresh end to end test. A committed library is not proof that the whole product works. Each session should check the latest handoff and actual code before acting.

## 1. Render engine and shared physics

**What:** Make and simulate worlds, materials, motion and object histories in `hb-render` and `hb-core`.

**State now:** Water motion and history, rigid physics, animation, world tools and an outdoor render exist. The big build has added many core libraries since the parity audit.

**Broken or needs fixing:** Prove realistic motion and contact across scenes; older parity counts and engine notes predate recent commits. Do not call the connected proof finished.

**Needs update:** Reconcile `PROGRESS.md` and parity rows with code and real acceptance results.

**Needs adding:** Finish general editing, rendering breadth and the connected filmed room, person, cloth, water, breakable prop and sound proof.

**Dependencies:** Gives vision, Studio, TV and worlds shared project, physics and history tools. Receives footage and provenance from vision, sound from Studio and real use cases from worlds and TV.

**Critical: 5.** Foundation for several products and the big build.

**Starter brief:**
```text
Own render and physics in C:/Users/lilli/Projects/hb-render and hb-core.
Read AI-Shared/AGENTS.md, the newest handoff, BIG-BUILD.md and PARITY-ENGINE.md first.
First job: compare core progress with real acceptance results and finish the next unproved dependency.
Commit your work with the required attribution and log decisions and shipped work in state/timeline.md.
Ask the main session before cross-domain changes; report local, live and unverified results.
```

## 2. Vision and rooms

**What:** Read movement and rebuild places from footage while showing what was seen and inferred.

**State now:** `hb-vision` tracks people, reconstructs rooms and writes shared history; core can record sources and conflicting observations.

**Broken or needs fixing:** Check tracking, depth, room coverage and false certainty against real footage; the combined bedroom is a lab proof, not a complete reconstruction product.

**Needs update:** Check actual integration with current core and render code and preserve seen, rebuilt, patched, made and not seen labels.

**Needs adding:** Better coverage and correction workflow, plus the connected room proof with traceable evidence.

**Dependencies:** Gives render and creature motion, rooms and evidence. Receives shared history and rendering from core, footage from users and phone delivery from the site.

**Critical: 4.** Foundation for credible reconstructed worlds and the creature's senses.

**Starter brief:**
```text
Own vision and rooms in C:/Users/lilli/Projects/hb-vision and its lab pages.
Read AI-Shared/AGENTS.md, the newest handoff, BIG-BUILD.md and hb-vision progress first.
First job: test a real room through shared history and identify the largest evidence or integration gap.
Commit your work with the required attribution and log decisions and shipped work in state/timeline.md.
Ask the main session before cross-domain changes; report local, live and unverified results.
```

## 3. Studio and music

**What:** Help people make beats, record, edit and release music on a phone.

**State now:** Beat Lab and layered recording are live; hb-core has new multitrack Studio and director code. The October 26 site audit found recordings did not survive reload; check whether the new core is actually wired in.

**Broken or needs fixing:** Verify saving and reopening voice takes, phone recording, sound levels and exports end to end.

**Needs update:** Reconcile the Studio parity map with the new core and live site. Jaron picked voice editing and tap to drop sounds.

**Needs adding:** Durable multitrack editing and recovery; beat fingerprints, license choices and public registry, then marketplace and compatible exports. Marketplace work is slated after the Wednesday reset; paid sales wait on banking.

**Dependencies:** Gives TV, render and creature sound and voice. Receives shared audio, history and project storage from core, site delivery and company payment support.

**Critical: 5.** Foundation and a direct route to useful products and money.

**Starter brief:**
```text
Own Studio in C:/Users/lilli/Projects/heartbeat-observatory/studio and coordinate with hb-core.
Read AI-Shared/AGENTS.md, the newest handoff, BIG-BUILD.md and PARITY-STUDIO.md first.
First job: verify recording survives reload on the live phone flow and document the gap to core Studio.
Commit your work with the required attribution and log decisions and shipped work in state/timeline.md.
Ask the main session before cross-domain changes; report local, live and unverified results.
```

## 4. TV and daily news

**What:** Make and deliver the daily news and the planned channels and shows.

**State now:** News published October 27; History 7.7 is live. Many channels are live and the channel plan reaches 50 or more.

**Broken or needs fixing:** News crashed October 26 and was rescued; check the next scheduled run and publishing rather than assuming the fix covers every failure.

**Needs update:** Reconcile the channel plan, published episodes and queue with current live state.

**Needs adding:** Complete planned channels and shows, with reliable sourcing and phone playback.

**Dependencies:** Gives social daily material and the creature a possible school. Receives render, Studio, site hosting, MSI scheduling and social distribution.

**Critical: 5.** Attention and a daily deadline: live by 8 AM, never after noon.

**Starter brief:**
```text
Own TV and news in AI-Shared/projects/heartbeat-tv and C:/Users/lilli/Projects/heartbeat-observatory/news and tv.
Read AI-Shared/AGENTS.md, the newest handoff, CHANNEL-PLAN.md and news/WRITER.md first.
First job: check the next news run and reconcile the channel and show queue with what is live.
Commit your work with the required attribution and log decisions and shipped work in state/timeline.md.
Ask the main session before cross-domain changes; report local, live and unverified results.
```

## 5. Website, games and worlds

**What:** Make the public home and the places people visit, play and explore.

**State now:** Site, TV, Studio and lab pages are live; the bedroom and Necklace experiments show early world ideas. Games have been paused; check the latest instruction before resuming.

**Broken or needs fixing:** Keep phone navigation, playback and honest labels working; Livi's reported issues await the information in the open list.

**Needs update:** Check live pages and game status against current plans and open decisions.

**Needs adding:** Finish useful world experiences and the Living Ground experiments when directed. The creature's appearance, world and visitor access remain Jaron's decisions.

**Dependencies:** Hosts TV, Studio and future creature experiences; receives core rendering, vision and sound. Supplies public interactions and environments to those domains.

**Critical: 4.** Attention and delivery for everything public.

**Starter brief:**
```text
Own the site and worlds in C:/Users/lilli/Projects/heartbeat-observatory and AI-Shared/projects/games.
Read AI-Shared/AGENTS.md, the newest handoff, projects/games/README.md and the open list first.
First job: check current game pause and audit the most used phone flows for real breakage.
Commit your work with the required attribution and log decisions and shipped work in state/timeline.md.
Ask the main session before cross-domain changes; report local, live and unverified results.
```

## 6. Social, growth and bots

**What:** Bring people to Heartbeat and learn what reaches them.

**State now:** Company accounts and Postiz are active; Shorts are queued, Pip watches the inbox and growth tests have begun. TikTok needs a post every day.

**Broken or needs fixing:** YouTube quota caused failed Shorts; two were requeued and an older engine post still needs follow-up. Verify actual delivery.

**Needs update:** Check queues, results and bot instructions against current schedules; review `BUILD-SHEETS.md` and instructions before bot changes.

**Needs adding:** Reliable daily TikTok fill and a pool of site commercials; social judgment examples are logged for later.

**Dependencies:** Gives TV, Studio and site attention and feedback. Receives finished work and schedules from them, plus inbox and account help from company admin.

**Critical: 4.** Attention is needed for the work to find an audience.

**Starter brief:**
```text
Own growth in AI-Shared/projects/growth-bots and tools/social_daily.py.
Read AI-Shared/AGENTS.md, the newest handoff, state/open-list.md and the social queue first.
First job: verify today's TikTok post and investigate failed YouTube deliveries and daily fill.
Commit your work with the required attribution and log decisions and shipped work in state/timeline.md.
Ask the main session before cross-domain changes; report local, live and unverified results.
```

## 7. Sapling and creature

**What:** Grow Jaron's small AI and explore one shared creature living in a site world.

**State now:** Sapling exists and can wake after its own stop; an owner stop stays stopped. The creature and Living Ground are ideas, not finished systems.

**Broken or needs fixing:** Check retention and the unconfirmed budget accounting fix. Respect the recorded Claude pause pending provider permission; verify current authorization before Sapling training.

**Needs update:** Reconcile growth plans with the next training and the creature brief. Keep Jaron's four creature questions open.

**Needs adding:** A tested learning mechanism, a single persistent mind and body, visible behavior and a way to trace learning to its sources. Hosting remains a rough plan.

**Dependencies:** Receives worlds, vision, sound and shared history; could give the site a character and other domains a place to teach. Coordinate cloud and provider constraints with MSI and company.

**Critical: 4.** Foundation for a distinctive future experience, but the key ideas need testing.

**Starter brief:**
```text
Own Sapling and creature research in C:/Users/lilli/Projects/sapling and AI-Shared/projects/strategy.
Read AI-Shared/AGENTS.md, the newest handoff, CREATURE-BRIEF.md and THE-FLASH-2026-10-26.md first.
First job: check Sapling's current state and permissions, then list testable creature gaps without deciding Jaron's questions.
Commit your work with the required attribution and log decisions and shipped work in state/timeline.md.
Ask the main session before cross-domain changes; report local, live and unverified results.
```

## 8. Trading and money

**What:** Maintain the trading desk, records and tools that may help fund the company.

**State now:** Sports and crypto tools exist; reported results include losses and gains. Crypto calls and routines were paused October 25 until Jaron restarts them.

**Broken or needs fixing:** Verify actual balances, settlements, service health and current bot schedules; do not assume old lane settings still apply.

**Needs update:** Read Control Room and the latest instructions before changing trading numbers. Separate measured results from claims of an edge.

**Needs adding:** Reliable reconciled performance and cost reporting; check withdrawal readiness when needed.

**Dependencies:** Can fund company and tools; receives bot operations, MSI uptime and company account support. Forecasts must follow estimation isolation.

**Critical: 4.** Money matters, but returns are uncertain and losses are real.

**Starter brief:**
```text
Own desk maintenance in AI-Shared/projects/control-room and the trading tools.
Read AI-Shared/AGENTS.md, the newest handoff, Control Room and ESTIMATION-ISOLATION.md first.
First job: reconcile current status and results, keeping the crypto pause in force until Jaron restarts it.
Commit your work with the required attribution and log decisions and shipped work in state/timeline.md.
Ask the main session before cross-domain changes; report local, live and unverified results.
```

## 9. Company and admin

**What:** Keep the LLC, accounts, bills, inbox and business opportunities in order.

**State now:** EIN and D-U-N-S exist; business mail is forwarded and Pip watches it. The D&B corporation label was confirmed standard for LLCs, so no correction is needed.

**Broken or needs fixing:** Track renewals, failed payments and outstanding business replies. App store enrollment may need Jaron's replacement ID.

**Needs update:** Check paperwork, ownership moves, balances and current deadlines rather than relying on old notes.

**Needs adding:** Finish store enrollment when its prerequisites are met and follow up existing Fort Wayne leads within the message rules.

**Dependencies:** Gives all domains accounts, funding and business support. Receives product details and costs from them and delivery status from MSI.

**Critical: 4.** Upkeep and money keep the company operating.

**Starter brief:**
```text
Own company administration in AI-Shared/projects/life, projects/fw-sites and state/open-list.md.
Read AI-Shared/AGENTS.md, the newest handoff and current paperwork and inbox notes first.
First job: check renewals and outstanding replies, then update the actual next steps.
Commit your work with the required attribution and log decisions and shipped work in state/timeline.md.
Ask the main session before cross-domain changes; report local, live and unverified results.
```

## 10. MSI operations

**What:** Keep the shared computer, scheduled work, storage and connections healthy.

**State now:** Scheduled tasks support news, video drops, Sapling wake, watchdogs and reporting. A stuck capture blocked a run October 25 and was recovered.

**Broken or needs fixing:** Check current health and stale or failed tasks; protect the news GPU window and avoid overlapping heavy jobs.

**Needs update:** Read MSI status and task history before scheduling work; verify actual resource use and recovery.

**Needs adding:** Better measured scheduling and conflict warnings, including the parked time-sense idea.

**Dependencies:** Gives every domain compute and reliable automation. Receives job schedules and resource needs from every domain; coordinate cloud spending and pod cleanup.

**Critical: 5.** Upkeep underpins the daily news and shared work.

**Starter brief:**
```text
Own MSI operations in AI-Shared/tools and state/MSI-STATUS.md.
Read AI-Shared/AGENTS.md, the newest handoff, MSI status and recent task history first.
First job: check failed or overlapping scheduled jobs and confirm the next news window is clear.
Commit your work with the required attribution and log decisions and shipped work in state/timeline.md.
Ask the main session before cross-domain changes; report local, live and unverified results.
```

## First sessions

1. **TV and daily news.** A missed morning has a fixed deadline and channel production is the current focus. Start by checking the next run and live queue.
2. **Render engine and shared physics.** Many domains depend on the fast-moving shared core, and it needs one owner to verify integration and acceptance proofs.
3. **Studio and music.** It is already in users' hands, recording durability matters, and Jaron has named the next features and marketplace direction.

Keep vision, website and worlds, social, Sapling and creature, trading, company, and MSI in the main session for now, with explicit checks for TikTok, trading pause, bills and machine health. Give any of them a separate session when its workload or daily risk makes main-session care unreliable. Main remains the coordinator for shared interfaces, priorities and Jaron's open decisions.
