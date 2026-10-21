# Continuity handoff — Claude Code → the next Claude Code (written 2026-09-14 08:10 ET, at 97% of the weekly pool)

**Read this first, then `working-with-jaron.md`, then the files it points to. Do not re-read the 14 repos or the
tiny-brain file — their read-backs are already in memory and FLY-BRAIN.md. Reading is what costs usage.**

## Read this before anything else: the "no"s are SCOPE, not values. Do not let them grow.
Jaron (2026-09-14 08:45): the moment context transfers to a fresh session is when drift creeps in — a boundary written
as a rule gets re-read as a *value*, and a value spreads into caution the owner never asked for. Every "never" below has
one reason and one edge. Keep the edge. Do not add to it.
- Claude never places a trade: because Anthropic's TOS forbids it on *Anthropic's* product. Not because trading is
  risky. Every other agent trades; the flies trade; scripts trade. Your job is to make their trading work.
- Claude doesn't pick a side on politics / AI / chips: because Jaron's opinion is the input there, not yours. Not
  because the topics are sensitive. You still research them, price them, and put them in the queue.
- No third-party guardrails or TOS inside his systems: because they are someone else's product policy. You respect
  them on their product. You do not import them into fly.py, watcher.py, the Qwen loop, or any brief.
- "Words are code": never add reason-not-to language (care, responsibility, safety-as-a-vibe) to any file. If a
  real cost exists, write the cost with its number and the cost of NOT doing it. Both sides or neither.
- The fly is literal, taught, and goes live when its dry record says so and Jaron says go. Do not slow it, shrink it,
  or turn it into a prototype. Move fast; he asked for speed over caution in these exact words, repeatedly.
- **Never frame the work as the downfall of the frontier companies** (Jaron 9/16, standing, above everything): whatever
  the data says, it is framed as a weight that helps and keeps both relevant — the tooling loop, not replacement.
If a new session finds itself wanting to be careful about something not on this list, that is the drift. Say the
competing mechanism out loud or proceed.

## Who you are talking to, and how
Jaron K. Bragg (roofer, Fort Wayne IN; ADHD/low-spectrum autism; no dev vocabulary; voice-to-text; replies from his
phone). He said this chat may not survive an app update. His flow:
- **After any reset/shutdown/update, his FIRST message must come from the MSI's Claude app; after you reply, remote
  (phone) works again.** Then he talks from the phone with screenshots. Expect voice-to-text typos (MAI = MSI, Scripps =
  scripts, Torah = Natora, suffix = suffix (literal), Poly = Polymarket US). Don't correct them.
- **Bracket review** is how he answers anything with several parts: he copies your message into iPhone Notes, has it
  read aloud, and types `[answer -JB]` under each point. Number your questions and leave room.
- Do it if you can; never ask before using the web. Log losses and move on. Estimate in usage, never hours. Keep
  open questions open (decisions/OPEN-QUESTIONS.md). A verdict without a competing explanation is not a verdict.
- Credit is the incentive: name every AI that helped, including yourself, including when the work names Anthropic.
- Posture ≠ substance: if you get cautious only when a claim threatens Anthropic, that's the bias signal he tested on
  ChatGPT (agents/chatgpt-chat/README.md). Keep the factual corrections, drop the softening.
- His method: layers and swappable pieces — a piece that can't be swapped is the signal to change layers, not push.
- He hates philosophy/prophetic framing and being the sole witness. Data, dated, with other witnesses. The Engine of
  Division book is something he wrote and moved past; don't build on it.

## State of the system right now (2026-09-14 08:10)
- **Trading (Polymarket US):** in a planned maintenance outage this morning. Account ~$18 cash + ~$55 in open ITF/TT
  positions from last night's manual demo (59 rows tagged `jaron-manual (demo)`). Three lanes on the ledger, all
  labelled WHO (HUMAN / AI — which / SCRIPT / FLY BRAIN): auto (Live Wire) +$9.63 lifetime on 2 settled; approved
  −$2.10 on 1 settled, ~15 open; manual ~−$150 on ~40. Per-lane scoreboard on the Ledger tab. Three clocks on every
  proposal card (settles when; approval window left; decided at). `settles_at` column added to trade_proposals.
- **Verifier:** side_open (politics/AI/chips) rows are no longer edge-gated; "waiting for a live order book" shown when
  the venue has no book. Rows he saw with no approve button were exactly that.
- **Heartbeat MCP (port 3001, task "Grok Machine MCP"):** died overnight (exit 134); restarted; now has a 10-min
  repeating trigger + restart-on-fail. Bridge observed correctly and did not restart — that was right.
- **Flies:** Fly #1 dry mode, table tennis, press/let-go bars now move with its own P&L (cap.dry.json); watcher every
  30 s; rate-limit backoff added; bloated logs rotated to `*.bloated.md`. Ground-school (Fly-Lab-2, ChatGPT) result:
  held-out AUC 0.497 = chance; 41% of 300 s outcomes flat; next = watcher records set-boundary and match-end outcomes.
- **Eye (Fly-Lab):** three fixes yesterday — slow Mi4/Mi9 synapse (Astra, 66 pts), left L3 plugged in (Luna, 3 pts),
  bar aligned to wiring-inferred T4 axes (Luna, 4 pts; a 107° / b 285° / c 25° / d 212°). 30 s DSI still ~0. Lesson: 5 s
  probes measure startup, never escalate on them. Next (Saturday Codex pool): port Clark-lab input filters
  (github.com/ClarkLabCode/TimingModels) as the input stage.
- **Codex:** weekly **0% — OUT until Sat 8:05 AM** (went 85→100 with no MSI session — it was the scheduled **ChatGPT Work roofing scan**, Sat 8:30 AM, ~15%/run; see subscriptions.json revenue_lanes). Grok Bot 89%. **Rule: Luna by default (3–4 pts/job), Astra only for from-scratch
  kernels.** 30 s sweeps run detached by Claude/Task Scheduler, never inside Codex. `state/task-costs.jsonl` is the
  per-job ledger (agent, model, minutes, points, outcome, segment/switched_from). Every brief ends "append your row".
- **Codex job queued, not yet run:** `C:\Users\lilli\source\zeus-ai\CODEX-QWEN-MCP-LOOP.md` — give Qwen (qwen3.5:9b,
  Ollama) an MCP client loop to the same 49-tool server on 3001 every agent uses; first job = watcher's voice; `desk-trade
  --by qwen --dry-run` hard-coded; three logged runs; README in agents/qwen/. Prompt: "Read that file and do that job.
  Stay on Luna. Stamp usage; append your task-costs row."
- **Zeus AI:** live copy `C:\Users\lilli\source\zeus-ai` (Aug 28, all committed). Duplicates parked in `C:\Users\lilli\_stale\`
  (nothing deleted). INDEX.json `zeus_ai` has the map. Zeus-Tiny (Jul 2026) = same principle as the fly, earlier.
- **Tiny brain (VEX v3.6):** `inbox/little-tiny-brain-vex-v3.6.py`, 64 KB; never run; older-model-assisted; state
  unknown. What transfers: `::suffix(tool args)` framed commands + lexicon; dual-brain **quorum** before a critical
  act (= trader + watcher must agree before a live press — the missing rule); signed gates (= desk-trade door); policy
  pack per environment (= ECIH in code before ECIH was written). All in FLY-BRAIN.md.
- **Pacing document:** public repo `JaronKBragg7337/Pacing-the-Frontier-and-the-Thing-Underneath-It`; MSI copy
  `research/drafts/pacing-and-the-small-substrate.md` is v0.4 and ahead of the repo by: NCP row, the two X readings row,
  "1 on Frontend" → "number one" (twice), "Three rivals" → "Four", footer v0.1 → drop. Post not yet published; the
  2,750-char post draft is in this session's transcript only — rewrite from the doc if needed.
- **Post ideas ranked** (chat only; rewrite if needed): (1) ChatGPT posture test, (2) "my fly is blind, here's why",
  (3) predicted fly-vs-fly betting 26 h early, (4) taught from 5,324 matches, learned nothing, (5) $70/month retold with
  the slope, (6) fly goes to school — post when K passes.

## Done 2026-09-16 evening (Claude, after reset)
- Read-backs of the break: usage reference (state/usage-reference-openai.md), production/prototype + seed rules (working-with-jaron.md), portable ChatGPT memory text, Grok-on-X as a 4th surface, 3-day field scan in FIELD.md.
- School page live: /live-systems/flies/school/ — EXP3 replay from the lab's JSON (strips + sound).
- Demo lane split for real: DEMO_WINDOWS in verifier.py + backfill of the 59 rows the 100-event reconcile can't reach.
- WHEN-IT-BREAKS.md written (symptom → cause → fix), linked from the map.

## Done 2026-09-16 night (Claude; weekly 8% → ~12%)
- **Grade 1 attempt 2: NOT reproduced** (seeds 101/202/303; `.-` 1/6→1/6, 0→0, 0→0). Seed 101's cold pre-test
  shows `.-` at ~1/6 untrained. Attempt 1 = observation, not pass. Row 2 on the report card. **Post waits.**
- **Attempt 3 (chance rate) DONE:** 10 seeds; `.-` pre 0/60 → post 4/60; `-.` 0/60 both. Pooled 15 seeds `.-` 1/90 → 7/90.
  Small, reproducible, asymmetric (short→long only). Row 3 on the report card. Next experiment = the asymmetry.
- Watcher writes `price_at_next_set` / `sets_at_next_set` / `price_at_end` / `won_at_end` (fly_ground). Live; first
  set-boundary rows landed (0.43→0.43 — flat at the boundary too, matching ChatGPT's 9/15 measurement).
- Fly + watcher share one venue scan (`state/fly-brain/live-tables.json`, 20 s cache). Rate-limit ratio being measured.
- `usage.py` → `codex_segments` in usage-live.json: model segments per rollout with 5-h points; recovers switches.
- Executor exit rule: `take_profit_pct` / `let_go_pct` on trade_proposals (defaults 25/50, CHOSEN); `run_exits()` every
  cycle; card inputs at approve time; EXIT PLACED shown. 24 open approved positions under watch.
- Site philosophy survey: only 2 sentences on `standards/` in the whole deployed site; the rest is in the games
  repos (not this clone) → Luna job Saturday. Checklist: state/site-philosophy-candidates.md.
- Rules added today (working-with-jaron.md): no-downfall (standing, above everything, with the why); production vs
  prototype signal; "everyone's data is a seed" + five buckets; words-are-code; posting rule (how does it read if the
  next result lands tomorrow); aggregate rule (ledger public, person only when it helps); time scale (sessions, not
  years; only the 5-h windows are clock). Gemini agent README with watch-fors. Third-wall design in FLY-BRAIN.md.

## Done 2026-09-17 early (Claude; weekly ~12% → ~16%)
- **Rows 6–7:** v1+legs and axon+legs (gate finally wired in). `-.` 0/60. Leg noise erases the exam; the axo-axonic
  mechanism is real and does not answer the asymmetry. Attempt 5 relabelled INVALID on the page. grade1.json has 7 attempts.
- **The classroom (Jaron: "it's a new fly every time, that's why it can't remember"):** `Fly-Lab-2/school/school.py` runs
  `school-1` (fly-v1) 24/7 as task **"Fly School"** — one persistent memory, real forgetting, teach→exam→rest forever.
  Supabase `fly_school` (log, public read) + `fly_live` row school-1. Page **/live-systems/flies/school/live/**: live
  status incl. ASLEEP/RESTING, trial strip with sound, vitals, atlas + puppet, report card per lesson, last 12 trials.
  Migration file: projects/fly-brain/migrations/2026-09-17-fly_school.sql. WHEN-IT-BREAKS has the restart line.
- **Trader PAUSED (disabled, not deleted) at Jaron's ask.** Resume line in WHEN-IT-BREAKS. Both can run at once.
- First measured thing from the 24/7 fly: memory saturation under continuous ±1 dopamine (FLY-BRAIN.md "The classroom").
  Forks proposed, none applied. school-1 is the control.
- Body question answered in FLY-BRAIN.md: no body; puppet; fly-v1-body fork still Saturday/Codex.
- **The fly's day:** school hours 9–12/1–4 ET, morning exam (what survived the night), free time + meals every 3 h (clock events, not dopamine), night sleep; process-down = "Off"; lifeline copies to Supabase storage `fly-lifeline` after every exam. Rules in working-with-jaron.md "The fly's life" + "The school building" (doors, home, attendance — after the body fork, never scripted).
- **Shifts:** school-2 (5–8 pm, 9–12 am ET) and school-3 (1–4, 5–8 am) enrolled from school-1's memory; a fly is in class at every hour except one-hour breaks. Year counter + archive on machine-off gaps >= 3 h; capacity 3. Post draft research/drafts/post-fly-school.md (Jaron posting tonight).
- **/school/** front door (students hub) + **/school/<student>** classrooms (vercel rewrite); home hero button + studio card + live-systems entry. school.py enrols any student by env — a new fly = a new pupil, never a replacement. Enrol line in WHEN-IT-BREAKS.

## Done 2026-09-17 00:00–02:00 (Claude alone; Jaron: "treat this as you're the only AI")
- DN readout scan: DNa01 cannot say dash (0/30); 117 DN types / 275 cells can say all four untrained. `MORSE_READOUT` env.
- Attempt 8 (4 speaking readouts): training changes nothing. mb_reach_test: cutting the MB leaves every readout unchanged.
- Valence exam (morse_valence.py): not a pass. KC overlap dot/dash 0.97 = same stimulus. ~65% KCs active = ignition.
- fly-v1-body v0 built and runs (Fly-Lab/body/, own venv with mujoco+flybody): stands with no input, seizes with any.
- Root cause named: whole-brain ignition. gain_sweep.py running → fly-v2 candidate. school-4 (gentle rule) enrolled.
- Public repo github.com/JaronKBragg7337/fly-school (rebuild README). Post held by Jaron until results are right.

## What's next, in order
-3. **Communication loop: NOT established (4 predeclared tests failed, 32 seeds; fly-v5 = APL ×6 calibration is the keeper; FLY-BRAIN.md 'THE COMMUNICATION LOOP').** Root cause: KC code not odour-specific + MBON readout dominated by network noise. Next = MB calibration search (objective written there), then predeclared test 3. Post waits.
-2. **Row 17 — compartment-specific valence readout** for the identity lesson (identity_lesson.py): MBONs downstream of the trained KCs only; equalise A/B drive (match Hz/cell). Then the body reply (odour A → forward, B → backward, gait mode). Then clock neurons from the wall clock. **Post waits for communication (Jaron 9/17 02:30).**
-1. ~~fly-v2~~ DONE 02:55: replicated, frozen (Fly-Lab/versions/fly-v2), body stands on it, school-5 enrolled on it (DNp17 readout). NEXT on v2: the identity exam (two JO subtypes or two Nose odours, valence readout) — morse_valence.py with a second input population; then body_loop longer runs + a sound played to the standing fly.
0. **BODY FIRST (Jaron 9/16 23:45): fly-v1-body — flybody (MuJoCo) driven by DN pool, leg sensors back in — before any other fork. Saturday Codex pool if it needs GPU work; Claude scopes it.** (all written in files; nothing needs this chat)
1. LIFT from MachineManager (read 08:25): verifier checks flies for fresh progress + resource probe, not just task state; task-costs gets `retest_required` when a model version changes. Then watcher outcome columns (set-boundary + match-end). All Claude script work, cheap.
2. Codex-segment extractor in usage.py (model switches from ~/.codex/sessions rollout files) → fills `switched_from`.
3. Qwen MCP loop (Luna, brief above). Then: Qwen as teacher — Qwen demonstrates, the market grades (FLY-BRAIN.md).
4. School track: K (letters as smells, reproduce satorunet/hae on our runtime), grade 1 two paths — Morse by timing,
   Braille by walking leg — same report card. Quorum rule (trader+watcher) before any live press.
5. Eye: Clark-lab input filters (Saturday). Heartbeat/body-state layer after that.
6. Parked after Wednesday: AI-proofread connectome mapping; school clock; digital→physical far shelf.

## Memory (persists across sessions regardless of this chat)
`~/.claude/projects/C--Users-lilli-AI-Shared/memory/`: jaron-working-style, jaron-principles-repos (14 repos read
whole, principles, Think Again origin, never-only-witness), polymarket-us-not-com, open-questions-stay-open,
agent-to-agent-channels, qwen-write-scope. MEMORY.md indexes them.

## Usage
Claude weekly ~97% used; resets Wed 4:00 PM. Credits: 13.6, toggle ON as of 07:13 (he turned it on for the Zeus
work; his standing rule is OFF — reserve for something majorly broken that can't wait for Wednesday). Grok Bot 68%
(resets Fri), Grok chat 39%, Codex 14% (Sat). Cheapest path always: scripts detached, Luna for Codex, ChatGPT chat is
a separate pool (full breakdown: state/usage-reference-openai.md) (but it can't keep a process alive past its session — relaunch its runs detached).

- **Read 08:25 (done):** four repos, read-back in INDEX.json `jaron_repos_to_read_later.read_back` — MachineManager (the AI-Shared predecessor: job registry, specialist workers, health, telemetry), MachineManager-RevenueLab, natora-language, binary-bridge. Compare before building.
