# TODO — what is not done yet, so nobody forgets and any agent can pick it up

**Rule:** if it is described somewhere but not built, it goes here. If it is built but not verified,
it goes here. An item leaves this file only when it works and has been seen working.
Written 2026-09-10 late. Owner: whoever reads it next.

---

## CODEX AUDIT 2026-09-12 13:44 → FLY REPAIRS 13:50 (Claude)
Astra sweep (7m21s, 37% of a Codex 5h window) found: verifier hid failures from Task Scheduler (Codex
fixed), postboot-check blind to the proposer and to HTTP 5xx (Codex fixed), desk.py exit-code
propagation (Codex fixed), AND five fly.py faults (Claude fixed, task restarted 13:47): dry-run profit
raised the live cap → per-mode `cap.{dry,live}.json`; holding lost on restart → `holding.{mode}.json`
+ venue reconcile on start; success judged by output text → exit code + JSON `placed`; rewards only
from resolutions → sells teach too; reward poll skipped while idle → runs every tick. Page copy
"nothing is placed without a yes" corrected. Still Codex's: Bridge routine ← expanded health checks;
dated backup snapshots (mirror propagates deletions); AgentWorkbench broken tasks (disable?).
Handoff: `handoffs/2026-09-12-codex-system-audit.md`.

## FLY-LAB: BASELINE SWEEP DONE 02:16 (Claude ran the 7 missing trials; result in Fly-Lab/WATCH.md)
Tonic drive woke the ON relays (Mi1 0→2.4 Hz, linear) with NO runaway at any rate — Jaron's hunch was
necessary. Not sufficient: T4 = 0 at every rate, because CT1 (the brake) rises in step (130→351 Hz).
Next is a design, not a sweep: non-uniform baseline (relays up, CT1 not) — hunger is not a volume knob.

## (was) FLY-LAB: BASELINE SWEEP HALF DONE (2026-09-13 01:09, Codex hit its 5h wall)
Jaron's tonic-drive hunch is the first positive signal on vision: at 0 baseline the ON relays
(Mi1/Tm3) are dead; at 1/3/5 events/s they wake (Mi1 0.06→0.20→0.37 Hz) and the lamina does NOT run
away (p95 ~86.7 Hz, quiet after input removal). T4 still zero through rate 5; CT1 (the giant inhibitor)
rises with the baseline (213→242 Hz) — more sugar feeds the brake too. **Rates 10 and 20 unrun.**
All finished trials are files in `C:\Users\lilli\Fly-Lab\results\baseline_study\`; the script has
`run --rate --seed --direction` and `analyze`/`report`. **Any agent can finish it** — no chat needed:
run the missing trials (5, 10, 20 × seeds 0,1 × dir ±1; skip existing JSON), then analyze/report →
WATCH.md. Codex resets 05:03; Grok via connector or Claude Code can do it sooner.

## FLY #1 BUILT 2026-09-12 12:35 — dry run running as task `Fly Brain`
Real MaleCNS brain, 165,122 neurons, on the MSI. Watches live table tennis, smells the match, presses
through desk-trade.py. `projects/fly-brain/README.md`. **Next:** let it watch 3 Setka Cup matches
overnight (dry), read `state/fly-brain/log.md` in the morning, then Jaron decides `--live`.
Open: serving as a sense (feed lacks it); cloud container at the $100 milestone.

## AT-THE-MSI SESSION 2026-09-11 19:00–20:05 — everything on the list DONE
Live Wire (brief+routine+connector) · Bridge (steps 8–9) · DeepSeek (key in, proposer switched) ·
Q-015/Q-016 closed · CoworkVMService won't-fix · **auto sign-in ON** (reboot survival; untested until
the next reboot — run `tools/postboot-check.ps1` then). `PROMPT-UNIFIED.md` written.
Next: Codex / ChatGPT Work standing jobs, then Claude Code's.

## FULL SAVE 2026-09-11 15:45 — read `handoffs/2026-09-11-claude-code-48h-state.md` first
One page with everything that runs, every open question (Q-013..Q-017 added), what needs Jaron at the
MSI, every trap. Connector naming clarified in INDEX: "Grok Machine" and "Heartbeat MAI" are the SAME
server; Desktop Commander is ChatGPT's. `desk.py` now self-selects the venv and `live` means started
within 8h (was showing NFL 2027 futures as "started").

## WHILE JARON ROOFED (2026-09-11 08:36–09:00)
- Systems: all 8 live tasks healthy, 4 ports up, tunnel answering, 497 GB free, zero script errors.
- `agents/` now has an area for every door: qwen, chatgpt-chat, claude-chat, grok-app, grok-bot/scout,
  grok-bot/live-wire (+ table of routes in agents/README.md).
- Proposer mixes horizons: half of each run settles within 48h (games tomorrow, this week's prints),
  half long. Sports use gameStartTime, not the venue's 2-weeks-later endDate. In-progress games are
  excluded (Live Wire's territory).
- `tools/score-estimates.py` + task `Scout Scorer` (daily 06:30): grades every estimate by method
  against the market price at the time. 35 on file, 0 resolved yet. First real read ~Sep 16 (FOMC).
- `AI-Shared Mirror` task: nightly robocopy of the workspace to G: (secrets excluded). First backup.
- Still needs Jaron at the MSI: Live Wire paste + MCP; Bridge step 8; DEEPSEEK key; CoworkVMService fix.

## PROPOSER METHOD — `both` since 2026-09-11 08:35
Overnight the strict split (03:57, 05:57, 07:57 runs) proposed **nothing** in 18 candidates: with no
price it cannot tell "priced in" from "edge", so favourites always look like a fade and it correctly
refuses to fade against the evidence. Sane, but Jaron's metric is a fed queue. Now: split first (rare,
strong, direction-locked), and if it passes, the direct method at the smallest size. Both estimates go
to `state/scout-estimates.md` tagged by method — **score split vs direct when markets resolve.** That
comparison is the real experiment.

## THE QUEUE IS FED NOW (2026-09-11 01:57)

`Trade Proposer` (every 2h) → `Trade Verifier` (5 min) → Jaron taps → `Trade Executor` (5 min).
Researcher is Codex until `DEEPSEEK_API_KEY` is pasted into `~/.secrets/keys.env` — then change the
task's `--researcher codex` to `--researcher deepseek` (or drop the flag; deepseek is the default when
the key exists). **Codex DECLINES election questions** (OpenAI policy) — politics, the PolyBench alpha
category, is silently skipped until DeepSeek is in. Grok/Scout can also cover politics by hand.

**TRAP #2, same night:** a BUY_SHORT limit's `price` is on the YES scale (1 − what you pay for
NO). Learned from Jaron's own app orders in `/v1/portfolio/activities`. executor.py fixed before
any NO order went out. `TRADING.md` note added.

**TRAP found tonight:** an AtLogOn trigger with 5-min repetition does NOT start repeating until the
next logon. Executor/Verifier had run exactly once in 3 hours. Fixed by adding a second, start-now
repeating trigger to all three tasks. Any future task with repetition needs both triggers.

### Who-did-what ledger — DONE 2026-09-11 02:15
Jaron: "if I make a play it should be recorded ... if it wasn't proposed ... it automatically knows
it was me. It should also be reflected on the website." Built: MCP tool `polymarket_activities`,
table `desk_trades`, reconciler in `verifier.py` (every 5 min), ledger section on `/live-systems/trades/`.
The venue labels orders itself (`manualOrderIndicator` MANUAL = app, AUTOMATIC = executor), so the
label is the venue's trail, not an inference. Anything else shows as *unknown* — visible, never hidden.

### Ideas from Jaron, 2026-09-11, not built
- **Grok watching live video.** He watched the table-tennis stream and it helped. Grok Bot has a
  browser; Polymarket US streams matches. A watcher that reads the score/stream mid-match is a
  different edge (live, not pre-match). Park until the pre-match pipeline has data.
- **Claude phone app → Heartbeat MCP.** The Claude app's "Add custom connector" accepts an MCP URL
  with sign-in. `https://mcp.heartbeatobservatory.com/mcp` + Requires sign-in ON would give Claude
  chat on his phone the same 49 MSI tools Grok has. His call; nothing to build.

### Open items from 03:37 — DONE 2026-09-11 03:58
- Qwen page "Positions 0": fixed (`remote_bridge.py` now reads the positions map), bridge restarted.
- Ghost-page sweep: **none found** — all 41 pages linked from the site exist in the repo.
- Home directory: Qwen Observatory and Revenue Desk folded under Live Systems (`HIDDEN` set in
  `index.html`, reversible).
- Grok/X sentiment channel: proposer writes `inbox/sentiment-requests.json`; Bridge's routine step 8
  (agents/grok-bot/HEALTH.md) answers into `state/sentiment/<slug>.json`. **Bridge's routine text
  in the Grok Bot app still needs the step pasted in** — computer use was masked again.
- Live Wire: setup doc ready (`agents/grok-bot/LIVE-WIRE.md`); Jaron pastes Instructions + Routine,
  connects Heartbeat MCP. He confirmed the MCP route beats the browser login (passkey prompt never came).

### Site cleanup — PARTLY DONE 2026-09-11 03:36
Live Systems now lists Trade Desk (one entry) and Revenue Desk (parked). Paper Trading unlisted but
the page stays. **Not done:** the ghost-page sweep (pages live on the site that are not in the repo)
and the home directory page (`/`) still lists Qwen Observatory, Revenue Desk, PAM separately. Jaron
wants "one page for it all" — decide whether `/live-systems/` IS that page or whether the home
directory needs trimming too.

## BROKEN RIGHT NOW — fix before anything else

### 1. Approved trades go nowhere
**Symptom:** Jaron approved proposal #1 (Fed Rate Cut 2026, Yes @ 0.10, $1.75) on
`/live-systems/trades/`. Nothing placed. Bridge does not know.
**Cause:** Claude Code built the page and the `trade_proposals` table, then *described* "Bridge
polls the verdict and places" without building it. The page writes `verdict='approved'` to
Supabase and nothing reads it.
**Fix:** Bridge needs a routine (or a step in its hourly one) that reads
`trade_proposals where verdict='approved' and placed=false`, places each through the local
MCP on 8765, then sets `placed=true, placed_at, fill_note`. Bridge can reach Supabase from its
cloud box directly (public REST, service key lives on the MSI — read it via the tunnel) or via
PowerShell on the MSI.
**Who:** Bridge, briefed by whoever is awake. Claude Code is telling it now.
**Status:** DONE 2026-09-10 22:49. `Trade Executor` and `Trade Verifier` Windows tasks registered by Codex, every 5 min, both ran clean (result 0). First trade filled 02:38 UTC. Next approval needs nobody.

### 2. Qwen has done nothing since $10 landed
**Symptom:** Qwen held twice (correctly) and has not been asked to do anything since.
**Reality:** Qwen is no longer the decision-maker — Scout researches, Bridge decides, Jaron
approves. Qwen's remaining job is undefined. Either give it one (cheap local retrieval, file
consult, first-pass screening) or say plainly it is idle. Idle-by-design is fine; idle-by-neglect
is not.
**Who:** Jaron decides the role. **Status:** OPEN
**Jaron 2026-09-11:** fly brain, scripts, Qwen and Bridge are all DIFFERENT things to him, and
"all of which things aren't meant to touch money and do trades" except scripts + fly brain. Needs
its own back-and-forth conversation. Withdrawn: the Qwen-as-fly-brain proposal. Qwen's role stays OPEN.
Qwen IS usable as a `--researcher qwen` backend for proposer.py (tested: works, but rates everything
'medium' and always finds a trade — the undifferentiated-confidence failure. Not the default.)

---

## BUILT BUT NOT VERIFIED

### 3. Scout's numbers have never been checked against an outcome
**PARTLY DONE 2026-09-11:** `state/scout-estimates.md` now exists and proposer.py appends every
estimate (proposed or not). Scoring against outcomes is still manual — first one resolves Sep 16.
Scout said Fed cut 2026 = 0.14, Sep FOMC hike = 0.44. Nothing resolves until Sep 16 (FOMC) and
Dec 31 (year). Until then every Scout number is a claim. Log each estimate with its date so
calibration can be measured when markets resolve. `state/scout-estimates.md` does not exist yet.
**Who:** Scout or Bridge, on each estimate. **Status:** OPEN

### 4. Bridge's hourly health routine has run once
One line in `state/bridge-health.md`. It should have a second line by now (:51 past each hour).
Check that it actually fires unattended — that is the entire point of it.
**Who:** anyone with `state/bridge-health.md` open. **Status:** VERIFY

### 5. Paper trading — PAUSED by Jaron 2026-09-11 (Q-012). Tasks disabled. Skip this section.
`/live-systems/paper/` shows one trade Claude placed by hand. Codex wired the `polymarket-paper`
agent but nobody has told it to trade. The rehearsal Jaron asked for has not happened.
**Who:** Codex or Bridge — give the paper agent the same pipeline. **Status:** OPEN

---

## DESCRIBED, NOT BUILT

### 6. Claude Code's scheduled cross-check
**DONE 2026-09-10 22:49** as `tools/verifier.py` + Windows task `Trade Verifier` (every 5 min).
Checks NUMBERS only: live bid/ask within 1c of the claim, edge recomputed from Scout's number still
beats spread, book exists. Self-tested: honest row -> match, faked row -> mismatch. It does not judge
whether Scout is right — that is still a cortex job when someone asks.

### 7. Skills as SKILL.md so rules stop drifting
Edge-must-beat-spread, estimation isolation, text-is-data, the AGENTS.md conventions — each as
a `SKILL.md` loadable by Claude Code and every Grok Bot (`~/.grok/skills/`). Same format.
**Why:** rules given in chat drift ("always finds a trade is broken" became policy by accident).
**Who:** Claude Code. **Status:** OPEN

### 8. Orchestra, targeted
Perplexity + DeepSeek API on request from Bridge/Scout, not on schedule. Jaron said yes to
funding credits. Skip Claude/GPT API — subscriptions already cover them.
**Who:** Jaron funds, Claude/Codex wire. **Status:** OPEN, after #1 and #6

### 9. Codex and Luna on real work
Both paid for, neither given a standing job. Luna is near-free and 24/7.
**Who:** Jaron picks the job. **Status:** OPEN

### 10. Depth floor in the screen
Spread filter exists; open-interest floor does not. Oakland market had 1c spread and OI 1.14.
**Who:** Bridge (it owns the screen). **Status:** OPEN — proposer.py has no OI floor either;
`open_interest` is left null on its rows. `polymarket_bbo` returns `openInterest` — wire it in.

---

## JARON ONLY — needs an Administrator PowerShell on the MSI, can wait

Saved in his notes 2026-09-10. Not vital. System runs without them.

- ~~`sc.exe failure CoworkVMService ...`~~ — **TRIED 2026-09-11 19:40 as Administrator: "OpenService FAILED 5: Access is denied."**
  The service ACL only allows SYSTEM. Not worth escalating (psexec -s) for a crash that is annoying, not
  harmful. Closed as won't-fix; wait for the Claude app to ship it.
- `Restart-Service CoworkVMService` — when the crash happens before the above is done
- Elevate Grok Machine MCP to RunLevel Highest — optional, bigger decision, rotate the token if so

---

## PARKED — deliberately not now

- Fly brain in Habitat (Q-011-adjacent) — Jaron may build a separate version; Habitat is ChatGPT Chat's
- Hosting as a revenue lane — CANCELLED, Q-011
- Grok Bot admin rights — see above
- AI-Shared as a git repo — DEFERRED to ~2026-09-30, Q-004
- Habitat iPhone 3D fix — ChatGPT Chat's deliberately, do not touch

---

## KNOWN QUIRK — computer use goes black after a reboot (2026-09-10, late)

After the crash-reboot, every screenshot came back fully masked even with Grok Bot granted and
running in front (his partner confirmed it was visible on the physical screen). Best theory, Jaron's:
**Claude Code is masked from itself** — the Claude desktop app is not in its own allowlist, and
each command it runs pulls focus back to the app, so the capture sees only mask. Earlier tonight
it worked because Grok Bot stayed on top between actions.

Not fixed, not vital, not worth usage. Next time it matters: try adding the Claude app itself
to the allowlist, or drive the desktop from Codex (which is not containerised) instead.
**Do not fight this at the cost of a session.**

## Parked for after the 2026-09-17 reset (Jaron, 2026-09-13 14:05)
- **AI-proofread connectome mapping.** Jaron: "that's how long it took humans; now we make a system so AI can do it."
  Honest scope: EM segmentation is already ML (FlyWire / Google FFN); the decade of human work was *proofreading*
  merge/split errors. The target is a self-proofreading pipeline, not "map a brain from scratch." Start by reading how
  FlyWire's proofreading queue worked and what public EM volumes + segmentations exist (MICrONS, larva, H01).
- **School clock.** The school runs on lesson count, not calendar time; the report card records the date each grade
  passed. Pace is set by growth between grades (held back → brain changes → retake), not by the calendar.

## From the manual-trading week (2026-09-16)
- **Executor exit rule for approved positions.** Today an approved trade rides to resolution. Add: take-profit and
  let-go thresholds per row (chosen defaults, written as chosen; owner can edit on the card like size), watched by the
  executor every cycle, closed via the same order path desk-trade.py `--exit` uses. Jaron: "sell into the spike."
- Split demo rows out of the "by hand" lane on RESOLUTION rows too (fills were tagged Sunday; resolutions weren't).

### PAYDAY THIS WEEK — Supabase Pro before the money moves to savings (Jaron, 2026-09-20)
Pay the $25 Supabase Pro upgrade from the roofing paycheck the day it lands, before anything goes to savings; square it from the
Polymarket pool after. Then: disk to 8 GB, wait for Healthy, tell Claude to clean the tables and replay the offline trail. Full
steps in decisions/OPEN-QUESTIONS.md Q-021. Trading is not waiting on this; the ledger and the public page are.

## WEDNESDAY 2026-09-23, ~4 PM ET (Claude usage resets - checked against the app, not guessed)
- [ ] Unpause the `watch-collect` scheduled task (Claude daily writer for the watch repo). Jaron 09-21: "Would be nice if you could do this
      for yourself too, Opus preferably. Not till Wednesday reset."
- [ ] Codex daily writer already runs on Luna from the MSI (see watch/codex/); Astra stays reserved for fly-brain work when the pause ends.

## FROM CODEX'S FULL-WORKSPACE AUDIT, 2026-09-22 (GPT-5.6 Luna, 9m32s, 38,888 files / 7.1 GB)
Its six priorities, with what is already true as of this afternoon:
- [ ] 1. Supabase: still down, offline trail working, $25 fix waits for payday. Unchanged (Q-021).
- [x] 2a. "One file claims Supabase Pro was added; Q-021 says pending." Codex was right and the file was mine.
      state/subscriptions.json now marks that row NOT YET PURCHASED and separates the planned total from the charged total.
- [ ] 2b. Revenue Desk queue integrity: the queue file has 809 rows, the run log and commit message say 55, today's scan
      found 1,065. Do not trust the queue until those three agree. Needs someone to read the exporter, not a guess.
- [ ] 2c. Bridge health stopped updating after 2026-09-15. Nobody noticed for a week, which is its own finding: a health
      signal that can go stale silently is not a health signal.
- [ ] 4. G:\ checkout of polymarket-us-agent has a corrupted git HEAD with missing objects, while the workspace index calls
      it clean. The C: runtime is fine, so nothing is on fire; the index is lying and should be corrected or the checkout
      re-cloned.
- [ ] 5. Qwen's role (Q-014) and the payment rail (Q-006) remain owner decisions. Still open, still not inferred.
- [ ] 6. Reality agent: keep developing the concept, do not prematurely turn it into an app. Agreed; DESIGN.md is a register,
      not a plan with dates.
Not reverified in that pass and still unverified: public website behaviour, phone rendering, Vercel deployment state,
Supabase billing/disk status, post-reboot persistence.


## JARON EDITS HIS OWN SITE (asked 2026-09-23 7:01 PM)
His words: a way to "change and edit my own website myself. Each page, each text, each background color, shape of things."
"I want to pick the words... I'm so picky about words. The website is full of things that honestly make me cringe a bit."
Wants it professional, not philosophical; cut anything pointless or redundant. The one thing he named as important: his terms.
Plan (not started): an admin-only edit mode on heartbeatobservatory.com - tap text/heading/color, change it, save, live;
works from his phone. Build it ONCE, then he writes the words, not an AI. Build it as a Claude Code CLOUD SESSION on the
heartbeat-observatory repo: $100 cloud-session credit claimed 9/23, expires Nov 5 2:59 AM EST, separate from plan usage,
repo-only (no MSI/AI-Shared access), ends in a PR he reviews. Don't let an AI rewrite his copy while building it.
