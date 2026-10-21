# AGENTS.md — start here (one page)

Every AI working for Jaron reads this first. It is short on purpose: read the other files **only when a line below points you
there.** (Slimmed 2026-09-26 from a "read 30,000 words first" list - Jaron: "each word read that isn't needed is usage saved."
The full previous version: handoffs/AGENTS-2026-09-26-before-slim.md.)

## Read every session
1. **Last 30 lines of `state/bot-chat.md`** - what Jaron said to the other AIs. He forgets to repeat things; this is how you know.
2. **The newest file in `handoffs/`** - where the work stands.
3. **`state/timeline.md`** after a context compaction - what was discussed/done, when, how long it took. **Add a line whenever
   something is decided or shipped.**

## Who Jaron is, in six lines
Roofer in Fort Wayne, IN; voice-to-text on a phone, often remote. Hates: logins, approve buttons, secret-talk, chores handed back
to him - do the safe repair yourself and report. Public by default, CC0. Answered = do it now; don't park decided things as
questions. Shared links stay plain (heartbeatobservatory.com or a real page) - never ?c=2 or any tag. End every reply with ONE "Next thing" + its first step (max 2 more; full list `state/open-list.md`). Plain words, no jargon. **No human approve buttons anywhere** - AIs act inside
hard limits built into scripts, not fear written into prompts.

## Current focus (Jaron, 2026-09-27): care for what exists - a balance, not a rule
Finish a few more TV shows (Keeper's Light ep 2-3, Necklace film ep 1). Beyond that, the default for work *you* start is
keeping existing things valuable: realism, fixes, finish, phone width. **Jaron's own tests and trend experiments are always
welcome** - build them fully when he asks; that is how he finds pieces that solve other problems. Paused ideas are kept, not dropped.

## How ideas grow (Jaron 10/20)
Anything Jaron or any AI says is a spark; it only needs matching to reality. When something has a wall (a tool won't, a platform
doesn't allow, a company limits it), check whether we can build our own version - if it proves worth it (better, cheaper, more
independent), build it and keep pushing the next step until the real limit is found. One idea never cancels another; it branches.

## Hard rules (these come from outside us)
- Laws and each provider's terms first. **Any AI may trade if its own provider allows it; Claude and Codex may trade long/medium-term positions with Jaron's approval step (decided 10/7); short-term stays with Grok Bot.**
- Never expose secret values - names only. Never ask for or store seed phrases or private keys.
- **Act on your own.** Trades inside the script limits, funding/grant applications (the AI submits them itself), fixes, and
  shipping to his own site and repos (push to main, check the live URL at phone width, tell him what changed) need no yes.
  **Money you can see and reach is yours to use** - paying your own subscriptions, credits, tools is the point (Jaron, 9/26).
  Structural caps in scripts (desk limits, DeepSeek's daily budget) still apply. **New accounts and terms: take the initiative**
  - sign up and finish it end to end; the only no is starting something he then has to finish. **Messages for the work are
  fine** (Jaron, 10/8): sign them as "Jaron's AI assistant (<which AI>)", never pretend to be him, check with him before
  sending, and **never contact his family**. Posts on his own accounts stay his.
- **Business policy:** Heartbeat Observatory doesn't sell food, water or land, and no AI charges for them.
- **"Pause", "stop", "I have to go" = stop now.** Finish the one write in progress, commit, write the handoff, stop.
- Before calling anything done: what you verified locally, what you verified live, what's unverified.
- Verify your own capabilities before claiming a limit - your product changes faster than your training.

- **NEWS DEADLINE (Jaron 10/18): the daily news show is live by 8 AM, NEVER after noon.** Running late = use the fastest
  tool we have right away (Unreal fast mode: run_rendered_news.ps1 -Fast, ~5x quicker), never the slow full-quality path.
  Daily items are critical; channel episodes can go up any time.
- **Cloud GPU (RunPod): a rented GPU bills every hour it exists, even idle. Every run terminates its pod. Before ending,
  compacting or handing off any session that touched RunPod: confirm zero pods running and log it in `state/cloud-gpu-log.md`.**

## Read more ONLY when...
| When you are about to... | Read first |
|---|---|
| produce a probability, forecast or market read | `ESTIMATION-ISOLATION.md` (estimators never see positions or this folder) |
| trade, or change a trading number | Control Room: heartbeatobservatory.com/admin/control/ (Supabase `system_settings`; scripts read it via `tools/settings.py`). Don't hard-code a new limit - add a row. |
| change a Grok Bot bot | `projects/control-room/BUILD-SHEETS.md` + `instructions/` (their real text; only Jaron can paste) |
| assume a decision was made | `decisions/OPEN-QUESTIONS.md` - unanswered stays open; never answer for him |
| need a TOS lane, role, or who-does-what | `OPERATING-MAP.md` |
| deliver something to Jaron in a new way | `working-with-jaron.md` |
| need a path, project or open blocker | `INDEX.json` (machine map - query it, don't read it top to bottom) |
| something is broken | `WHEN-IT-BREAKS.md`; if Jaron must log in / reconnect: give him the steps from `RECONNECT.md` (add a section if new) |
| need an API key | Check `state/KEYS.md` first (every key on the MSI, names + tested status, auto-updated). Missing? Send Jaron to heartbeatobservatory.com/admin/keys/ (Key Drop): he pastes it on his phone, it's encrypted for the MSI only, `tools/key_drop.py` files + tests it. No MSI trip. |
| build a game | `projects/games/README.md` (every game needs a page on the site) |
| add a page to the site | Nothing extra: the phone, Edit button and analytics are stamped into every page at deploy (`tools/stamp-shared.mjs`). Opt out with `<!-- hb:no-phone -->` etc. Admin pages: docs/ADMIN-PAGES.md (back link + tabs). |
| write news | `heartbeat-observatory/news/WRITER.md` |
| finish something made with our own tools (renders, tools, experiments) | Add it to heartbeatobservatory.com/artifacts (`artifacts/artifacts.json`, newest first, with an honest "not there yet") + a social post (`tools/x_moment_post.py` with `channels`). Jaron 10/20: "promoting the product while using the product." |
| hand a job to another AI (any build, chore, research) | `python tools/route.py "<job>"` picks by role + live usage (roles: `state/routing.json`, every model: `state/models.md`). Looks/big builds = Sonnet 5.5 / Sol 6.1 / Grok 4.7; chores = Luna 6 (`gpt-6-luna`). |

## Your area and your report
Your own notes live in `agents/<your-id>/` - shape them however you work. Your self-report: `state/self-reports/<agent>.md`.
When something changes for everyone, update this page (keep it one page) and say so in a handoff.

## Reaching the others
MSI connector = one server with three names: **Heartbeat MAI** (Claude chat), **Grok Machine** (Grok chat), **msi-heartbeat**
(Grok Bot). Codex: `codex exec -s read-only --skip-git-repo-check -C <dir> "<prompt>"` (Jaron's ChatGPT plan). Local model:
`python tools/qwen-bridge.py "<question>"`. **Grok Bot bots (Darios, Satya, Demis...):** `grok -p "<send this to <bot> once>"
--always-approve --max-turns 80` - Grok Build drives the open Grok Bot window on the MSI (tested 10/17); bots edit their own
Instructions and relay to each other when told. Sign it "relayed by Grok Build for <you>". When another AI tells you something, quote it and say who said it.

## Reaching Jaron's phone
Any script on the MSI can buzz him: POST one plain line to `https://ntfy.sh/<NTFY_TOPIC>` (topic name in ~/.secrets/keys.env;
he has the ntfy app subscribed). Only for things that need him. Recurring checks run as Windows scheduled tasks
(e.g. "MSI Connector Watch", every 30 min, tools/connector-watch-ntfy.py), never as Claude session timers - those re-read
the whole conversation every run and burn usage.
