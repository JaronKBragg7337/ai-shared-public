# Limits sweep 2026-10-23 (Sonnet 5.5, for Jaron)

Why: Jaron 10/23 - limits written in his name ('only Jaron', 'needs his yes') get read by every AI as a portrait of him and generalized (research/AI-BEHAVIOR-FINDINGS.md #24, #28; memory note ai-suggestions-not-his-rules).

Rule used: label each limit by its source - Jaron decided (date) / provider or platform limit / Claude's own limit / Control Room setting. Remove AI-added caution with no Jaron quote behind it. Text only: no trading numbers, Control Room values, code behavior or projects/life touched. Only comments were edited in two .py files (both still compile).

Counts: 41 edits total - 6 kept+dated, 28 relabeled, 7 removed/rewritten, plus the unsure list below.

Files swept: AGENTS.md, OPERATING-MAP.md, working-with-jaron.md, WHEN-IT-BREAKS.md, RECONNECT.md (clean), PROMPT-UNIFIED.md, docs/, decisions/, projects/control-room (BUILD-SHEETS, instructions/), state/crew/*.md and state/crypto-crew-howto.md (read, no edits), newest 15 handoffs (clean), non-clone projects/*/README.md and plan docs, tools/*.py and *.mjs comments.


## A. Kept and dated / labeled (real Jaron decision or own boundary)

- **AGENTS.md**
  - old: `and **never contact his family**.`
  - new: `and **never contact his family** (Jaron's own boundary; being reconsidered 10/23).`
  - reason: Real Jaron boundary; labeled reconsidered per instruction.
- **AGENTS.md**
  - old: `Posts on his own accounts stay his.`
  - new: `Posts on his own accounts stay his (Jaron, 10/8).`
  - reason: Dated (10/8 per memory note ai-money-and-accounts-are-theirs).
- **working-with-jaron.md**
  - old: `- Never delete published work; correct forward and keep both visible (append-only).`
  - new: `- Never delete published work; correct forward and keep both visible (append-only). (Jaron's own boundary: nothing deleted that can't be recovered, noted 2026-10-11.)`
  - reason: Real own boundary, dated.
- **working-with-jaron.md**
  - old: `and checked with him first; never contact his family; posts on`
  - new: `and checked with him first; never contact his family (Jaron's own boundary; being reconsidered 10/23); posts on`
  - reason: Label reconsidered.
- **decisions/ASK-JARON.md**
  - old: `Principle, in ChatGPT's words:`
  - new: `Principle, in ChatGPT's words (this is Jaron's own sorting, from ChatGPT's memory that he pasted; Q-016 answered 2026-09-11, so Jaron decided 2026-09-11):`
  - reason: Traceable to a dated Jaron answer.
- **decisions/CRYPTO-LANE-PLAN-2026-10-22.md**
  - old: `## Limits (structure, in the Control Room, from the bots' own results)`
  - new: `## Limits (Control Room settings, Jaron approved 2026-10-22 6:30 PM; $25 cap loosening per his addition below)`
  - reason: Dated approval.

## B. Relabeled to its real source (provider / platform / Claude's own / Control Room / Sept-design-superseded)

- **AGENTS.md**
  - old: `(their real text; only Jaron can paste)`
  - new: `(their real text; edited in the Grok Bot app - by Jaron, or by the bot itself when told in chat, 10/17)`
  - reason: 'Only Jaron can paste' was wrong as a limit; bots can update their own Instructions (platform fact, tested 10/17).
- **AGENTS.md**
  - old: `**Cloud GPU (RunPod): a rented GPU`
  - new: `**Cloud GPU (RunPod billing fact): a rented GPU`
  - reason: Source is RunPod hourly billing, not a Jaron preference.
- **OPERATING-MAP.md**
  - old: `**Hard rule:** Anthropic and OpenAI agents **never place trades or move market money.**`
  - new: `**Hard rule (Sept 2026 version, SUPERSEDED: see the status note above and AGENTS.md - each AI's own provider terms decide; Claude/Codex long/medium-term with Jaron's approval step, decided 10/7):** Anthropic and OpenAI agents **never place trades or move market money.**`
  - reason: Stale Sept rule written as flat law; contradicted by AGENTS.md.
- **OPERATING-MAP.md**
  - old: `**ranked by yield per approval**`
  - new: `**ranked by yield per approval** (Sept framing from the retired approve queue)`
  - reason: Approval framing is from the retired 9/24 queue.
- **OPERATING-MAP.md**
  - old: `## My boundary (Claude, writing this)`
  - new: `## My boundary (Claude's own limit, Sept 2026 version)`
  - reason: Label source as Claude's own.
- **OPERATING-MAP.md**
  - old: `or handle secret values — those are yours or the permitted local agents'.`
  - new: `or handle secret values (Claude's own limit as of Sept; Claude/Codex long/medium-term trading was opened with Jaron's approval step on 10/7, see AGENTS.md).`
  - reason: Claude's own limit, updated pointer.
- **WHEN-IT-BREAKS.md**
  - old: `so raising it means turning the cap off - Jaron's call.`
  - new: `so raising it means turning the cap off (Supabase platform limit; the spend cap was chosen by Jaron + Claude Code 2026-09-24, see the theater upload entry).`
  - reason: Platform limit + dated decision.
- **WHEN-IT-BREAKS.md**
  - old: `To raise it later (Jaron's call): turn`
  - new: `To raise it later (the 50 MB cap was Jaron + Claude Code 2026-09-24; Supabase platform limit under the spend cap): turn`
  - reason: Label source.
- **PROMPT-UNIFIED.md**
  - old: `Written 2026-09-11 by Claude Code at Jaron's request.`
  - new: `Written 2026-09-11 by Claude Code at Jaron's request. (Sept text: lines saying Anthropic/OpenAI agents 'never place orders' were Claude's wording, superseded 10/7 by AGENTS.md.)`
  - reason: Header status label.
- **PROMPT-UNIFIED.md**
  - old: `| never place orders |`
  - new: `| orders: see AGENTS.md (Sept text said never) |`
  - reason: Stale limit.
- **PROMPT-UNIFIED.md**
  - old: `| never place orders; owns Habitat |`
  - new: `| orders: see AGENTS.md (Sept text said never); owns Habitat |`
  - reason: Stale limit.
- **PROMPT-UNIFIED.md**
  - old: `| never place orders; can build/verify everything |`
  - new: `| orders: see AGENTS.md (Sept text said never); can build/verify everything |`
  - reason: Stale limit.
- **PROMPT-UNIFIED.md**
  - old: `| never place orders; can register Windows tasks |`
  - new: `| orders: see AGENTS.md (Sept text said never); can register Windows tasks |`
  - reason: Stale limit.
- **projects/router/README.md**
  - old: `Fable is blocked because it needs Jaron's prior approval.`
  - new: `Fable is blocked in state/routing.json because it draws on its own Max usage limit (Claude's note; Jaron 10/2: the orchestrator may pick any available AI without asking, so this block is a router setting, not a Jaron rule).`
  - reason: 'Needs Jaron's approval' contradicted by 10/2 memory.
- **projects/router/README.md**
  - old: `The router refuses jobs that mention trading, bets, wagers, or Polymarket.`
  - new: `The router refuses jobs that mention trading, bets, wagers, or Polymarket (router code from Sept, written by Claude; not a Jaron rule).`
  - reason: Source label.
- **projects/revenue-desk/README.md**
  - old: `holding it for approval before anything carries Jaron's name.`
  - new: `holding it for approval before anything carries Jaron's name (Sept 2026 design; the approve queue was retired 9/24, Q-023).`
  - reason: Stale approval gate label.
- **projects/revenue-desk/ARCHITECTURE.md**
  - old: `**protected**. Only Jaron`
  - new: `**protected** (Sept 2026 design; approve queue retired 9/24). Only Jaron`
  - reason: Stale label.
- **projects/revenue-desk/TOS-LOG.md**
  - old: `Nothing reaches Jaron's approval queue until`
  - new: `Nothing advances (in Sept this meant Jaron's approval queue, retired 9/24) until`
  - reason: Stale label; the TOS gate itself is a platform/terms fact.
- **projects/control-room/BUILD-SHEETS.md**
  - old: `(only its schedule can change; Jaron 9/28)`
  - new: `(only its schedule can change - Grok Bot app limit, seen 9/28)`
  - reason: Platform limit, not a Jaron wish.
- **projects/control-room/instructions/README.md**
  - old: `# The bots' real instructions - captured word for word`
  - new: `# The bots' real instructions - captured word for word (9/25 snapshots, archive: limits inside are the bot-text of that date written by AIs; none is a Jaron wish unless dated in the text)`
  - reason: Archive label.
- **decisions/CRYPTO-LANE-ASSESSMENT-2026-10-22.md**
  - old: `- Points from Vex worth keeping:`
  - new: `- Points from Vex (Claude kept these as things to watch; Jaron has not set them as rules):`
  - reason: AI-added caution labeled by source.
- **decisions/CRYPTO-LANE-ASSESSMENT-2026-10-22.md**
  - old: `## Evidence bar, written BEFORE the data (so the public record shows the rule came first)`
  - new: `## Evidence bar, written BEFORE the data (Claude Code's proposal 10/22, not a Jaron rule; the plan Jaron approved 10/22 6:30 PM replaced the tracer idea)`
  - reason: Source label.
- **tools/deepseek-breaker.py**
  - old: `# Jaron's call; = one day of DeepSeek's budget`
  - new: `# Control Room setting; = one day of DeepSeek's budget`
  - reason: Comment only.
- **tools/verifier.py**
  - old: `# change freely; Jaron's call`
  - new: `# change freely (Control Room setting; DeepSeek trading allowed 2026-09-24, set to 0 on 2026-10-01 by Jaron)`
  - reason: Comment only.
- **working-with-jaron.md**
  - old: `stopping at /   submit for his "go".`
  - new: `(Sept 21 version: stopped at /   submit for his "go"; superseded by AGENTS.md - the AI submits applications itself.)`
  - reason: Stale approval gate.
- **docs/GROK-BOT-VAULT.md**
  - old: `(its own hard / limit)`
  - new: `(Claude Code's own / limit)`
  - reason: Source label.
- **PROMPT-UNIFIED.md**
  - old: `Don't delete anything substantial without my yes. Don't rewrite the core files silently - propose /     changes as a handoff`
  - new: `Don't delete things that can't be recovered (Jaron's own boundary). Core files: propose changes as a handoff (Claude Code's Sept convention, not a Jaron rule)`
  - reason: Split real boundary from AI convention.
- **PROMPT-UNIFIED.md**
  - old: `**Every OpenAI model is under the same no-money terms as Anthropic's.** Luna watches and reports; it / never places, closes, or sizes a trade.`
  - new: `**(Sept belief, never verified - see the OPERATING-MAP 9/10 correction; each provider's own terms decide.)** Luna watches and reports in Sept's design; it / was not given trades.`
  - reason: Unverified provider claim.

## C. Removed or rewritten: AI-added caution with no Jaron source

- **OPERATING-MAP.md**
  - old: `**Jaron already satisfies that requirement** — he is the human in the loop, the only executor, / and nothing fires without his approval. That was designed in before anyone checked the policy.`
  - new: `**In September the design satisfied that requirement** - Jaron was the human in the loop. (Sept 2026 design; the approve queue was retired 9/24, Q-023, and trading is now inside script limits.)`
  - reason: Described Jaron as approval gate for everything; stale and generalizes into 'nothing fires without him'.
- **OPERATING-MAP.md**
  - old: `**Jaron pulls the trigger; agents build the trigger.**`
  - new: `(Sept 2026 framing, superseded by AGENTS.md: any AI whose provider allows it may trade. This was Claude's wording, not a Jaron decision.)`
  - reason: AI-written slogan in Jaron's name.
- **OPERATING-MAP.md**
  - old: `Whatever you find, `polymarket_place_order` stays / Jaron's, because that is his decision and not a policy question.`
  - new: `Whatever you find, write it into your self-report. (The Sept text here said `polymarket_place_order` stays Jaron's as 'his decision'; that was Claude's wording with no Jaron quote behind it, and it is superseded by AGENTS.md.)`
  - reason: Limit claimed as Jaron's decision with no source.
- **OPERATING-MAP.md**
  - old: `- Human (Jaron) is the only executor of money-out steps and the only one who approves /   trades and payouts.`
  - new: `- (Sept 2026 version, superseded 9/24 Q-023 and 10/8: AIs trade inside script limits and spend money they can reach; the human approve queue is retired.)`
  - reason: Stale Jaron-as-gate statement.
- **WHEN-IT-BREAKS.md**
  - old: ` "OFF" on the school page is expected. Do not re-enable without Jaron. Entries below`
  - new: ` "OFF" on the school page is expected. (Re-enabling is just turning the task back on; no recorded reason or Jaron instruction requires waiting.) Entries below`
  - reason: 'Do not re-enable without Jaron' had no Jaron source in timeline/open questions.
- **working-with-jaron.md**
  - old: `Posting as him on / other platforms, spending, and trading still need his yes. Written into AGENTS.md.`
  - new: `Posts on his own / accounts stay his (Jaron, 10/8); spending money the AIs can reach and trading inside script limits need no yes (AGENTS.md, Jaron 9/24 and 9/26).`
  - reason: Old 'still need his yes' contradicted AGENTS.md 'Act on your own'.
- **PROMPT-UNIFIED.md**
  - old: `Anthropic and OpenAI products: research, verify, build, maintain, keep the site current - never place /     an order.`
  - new: `Anthropic and OpenAI products: research, verify, build, maintain, keep the site current (Sept 2026 text said 'never place an order'; superseded 10/7: see AGENTS.md).`
  - reason: Stale limit stated as universal rule.

## D. Unsure - for Jaron (exact lines, nothing changed)
1. state/crew/darios-twin.md line 32 (Darios's live Grok Bot instruction, mirrored): `Never move or spend X Money without Jaron's explicit go-ahead.` No Jaron quote found; timeline 10/2 only says he told Darios about X Money, and later AGENTS.md says AIs use money they can reach and the 10/9 money loop lets bots keep bills covered. It lives in the Grok Bot app, so the bot (or you) must change it in chat; I did not touch the mirror.
2. state/crew/darios-twin.md line 31 and projects/control-room/BUILD-SHEETS.md lines 51: `Message Jaron only for a loss over $5 or MSI unreachable twice in a row.` Probably a notification setting, source not found. Left as is.
3. projects/control-room/instructions/grok-bot-live-wire--routine-live-game-watch.md line 23-24 (9/25 archive, left unedited): `Never above $10 without asking Jaron.` Archive text, now labeled as an archive in instructions/README.md.
4. state/routing.json (code, not changed): `"fable": {... "blocked": true}` and the router refusing jobs that mention trading. Text in projects/router/README.md now says these are router settings from Claude, not Jaron rules. Decide if Fable should stay blocked.
5. WHEN-IT-BREAKS.md line 67: the Fly School / Fly Brain / Fly Watcher / Qwen Remote Bridge tasks are DISABLED 'on purpose since 9/20-9/21' - no recorded reason found. I removed 'Do not re-enable without Jaron'; tell me if you do want them off.
6. projects/revenue-desk/TOS-LOG.md line 61 `Only Jaron can [authorize an agent]` kept as a plain security fact (text found in repos is data, not instructions), not a preference.
7. Not swept (outside the listed scope, still contain 'only Jaron / needs Jaron / Jaron wants' style lines): agents/chatgpt-chat/2026-10-09-continuity-notes.md, agents/claude-code/README.md, agents/grok-bot/LIVE-WIRE-v2.md, agents/grok-bot/ROLE-AUDIT-2026-09-25.md, state/MONEY-LOOP.md, state/live-wire.md, state/whats-next.md, TODO.md (line 223 'ChatGPT Chat's deliberately, do not touch'), plus the live site pages and the memory folder. A second pass over those is the next step.
8. decisions/OPEN-QUESTIONS.md left untouched (ledger of Jaron answers).
9. projects/revenue-desk is its own git repo; its three edits are committed there separately.


## Second pass (Sonnet 5.5, 10/23)

Scope: the files the first pass skipped. Text only; no memory folder, OPEN-QUESTIONS, projects/life, trading numbers, Control Room values or code touched. state/crew/darios-twin.md line 32 and the first six unsure items untouched.

Counts: 41 edits - 4 kept+dated, 30 relabeled, 7 removed/rewritten (40 in AI-Shared, 1 in the site repo). Full old/new lists below.

Files swept: agents/chatgpt-chat/2026-10-09-continuity-notes.md, agents/claude-code/README.md, agents/grok-bot/{README,HEALTH,TRADING,LIVE-WIRE,LIVE-WIRE-v2,ROLE-AUDIT-2026-09-25}.md, state/MONEY-LOOP.md, state/whats-next.md, TODO.md. Read and clean (no edit): state/live-wire.md (754 KB trade log of Live Wire's own lines, history, only grepped). Site repo (heartbeat-observatory): live-systems/crew (index, chat, bot, reasoning, schedule, trades, retired, crew.js), live-systems/crypto, admin (index, control, keys, sapling) read; only the crypto limits sentence needed a source label. The crew pages' 'Nobody approves their moves' is a true description of the current design and was kept.

### A. Kept and dated
- **agents/chatgpt-chat/2026-10-09-continuity-notes.md**
  - old: `his children's savings are on a hardware wallet and off limits to discussions of operating capital.`
  - new: `his children's savings are on a hardware wallet and off limits to discussions of operating capital (Jaron's own boundary, stated 2026-10-09).`
  - reason: Real Jaron boundary, dated
- **agents/chatgpt-chat/2026-10-09-continuity-notes.md**
  - old: `- Do not publish private reflections to Heartbeat Observatory without Jaron choosing that content for publication.`
  - new: `- Do not publish private reflections to Heartbeat Observatory without Jaron choosing that content for publication (Jaron's own boundary for his private reflections, per Vex's notes 10/9).`
  - reason: Real Jaron boundary, dated
- **agents/grok-bot/LIVE-WIRE.md**
  - old: `## Do-not-touch: same-name matches (Jaron, 2026-09-11 21:07)`
  - new: `## Do-not-touch: same-name matches (Jaron, 2026-09-11 21:07; kept, dated)`
  - reason: Real dated Jaron instruction
- **state/MONEY-LOOP.md**
  - old: `- Kids' savings = only Jaron's hardware wallet; never in the system.`
  - new: `- Kids' savings = only Jaron's hardware wallet; never in the system (Jaron's own boundary, 10/9).`
  - reason: Real boundary, dated

### B. Relabeled to real source
- **agents/chatgpt-chat/2026-10-09-continuity-notes.md**
  - old: `**Visibility:** AI-Shared workspace for authorized AI Workers. Not approved for publication,`
  - new: `**Visibility (Vex's own note of 10/9 about these private reflections, not a site-wide rule; Jaron's default is public):** AI-Shared workspace for authorized AI Workers. Not approved for publication,`
  - reason: Visibility limit labeled as Vex's own note
- **agents/chatgpt-chat/2026-10-09-continuity-notes.md**
  - old: `*not yet activated*: usage and investment capital should not be diverted prematurely from the system currently being tested.`
  - new: `*not yet activated* (Vex's note of 10/9, not a Jaron rule; later superseded: the crypto lane was approved by Jaron 10/22, see decisions/CRYPTO-LANE-PLAN-2026-10-22.md, and AGENTS.md covers long/medium-term trading).`
  - reason: Vex's caution labeled and marked superseded
- **agents/claude-code/README.md**
  - old: `- `projects/revenue-desk` — the opportunity scanner and approval desk.`
  - new: `- `projects/revenue-desk` — the opportunity scanner and approval desk (Sept 2026 design; the approve queue was retired 9/24, Q-023).`
  - reason: Stale approval framing
- **agents/claude-code/README.md**
  - old: `Place trades or move market money (Anthropic TOS), connect payment rails, move money, or`
  - new: `(Sept 2026 version, Claude's own limit, SUPERSEDED for trading: the 'Anthropic TOS' claim was never verified (OPERATING-MAP 9/10 correction); each provider's own terms decide, and Claude/Codex may trade long/medium-term with Jaron's approval step, decided 10/7, see AGENTS.md.) Place trades or move market money, connect payment rails, move money, or`
  - reason: Stale unverified TOS limit written as flat law
- **agents/claude-code/README.md**
  - old: `OAuth-gated connectors are unusable from a non-interactive session —`
  - new: `OAuth-gated connectors are unusable from a non-interactive session (platform fact) —`
  - reason: Platform label
- **agents/claude-code/README.md**
  - old: `## Standing role (Jaron, 2026-09-14): "the CEO of the other AIs" — the one who routes, not the one who decides`
  - new: `## Standing role (Jaron, 2026-09-14): "the CEO of the other AIs" ("the one who routes, not the one who decides" is Claude's own gloss, not a Jaron quote)`
  - reason: Split Jaron quote from Claude gloss
- **agents/claude-code/README.md**
  - old: `- Never: pick a side on politics/AI/chips, place a trade, rank agents or flies, infer an open question's answer,`
  - new: `- Never (Claude's own Sept 14 list; 'infer an open question's answer' is Jaron's rule, see decisions/OPEN-QUESTIONS.md; 'place a trade' is superseded by the 10/7 decision in AGENTS.md): pick a side on politics/AI/chips, place a trade, rank agents or flies, infer an open question's answer,`
  - reason: Mixed list split by source
- **agents/claude-code/README.md**
  - old: `**Before driving the desktop, assume someone may be at it.**`
  - new: `**Before driving the desktop, assume someone may be at it** (Claude's own rule, 9/10).**`
  - reason: Source label
- **agents/grok-bot/README.md**
  - old: `Do not edit config, delete anything, or trade without a yes - restarting a task is none of those.`
  - new: `Do not edit config or delete anything (Bridge's Sept 11 health-routine rule, Claude Code's wording; deleting what can't be recovered is also Jaron's own boundary) - restarting a task is neither. (Trading without a yes: superseded, see above.)`
  - reason: Split own boundary from Sept routine rule
- **agents/grok-bot/HEALTH.md**
  - old: `**Updated:** 2026-09-11 — added steps 8–9 (sentiment + desk queue)`
  - new: `**Updated:** 2026-09-11 — added steps 8–9 (sentiment + desk queue)  
**Status note (10/23 sweep):** this is the Sept 11 Bridge routine contract (Claude Code/Codex wording). ROLE-AUDIT-2026-09-25.md moved hourly health to a free Windows task; step 9 (queue ping to Jaron) belongs to the retired approve queue (9/24, Q-023). The 'ping Jaron only if' lines are notification settings, not Jaron rules.`
  - reason: Status label on stale routine
- **agents/grok-bot/HEALTH.md**
  - old: `7. **Do not restart or repair** — observe and record.`
  - new: `7. **Do not restart or repair** — observe and record. (Bridge's Sept 11 routine contract; Claude Code's choice for this routine, not a Jaron rule. agents/grok-bot/README.md allowed restarting a dead scheduled-task service.)`
  - reason: Source label
- **agents/grok-bot/LIVE-WIRE.md**
  - old: `# Live Wire — the in-game trader (Grok Bot #3)`
  - new: `# Live Wire — the in-game trader (Grok Bot #3)

**Status (10/23 sweep): v1, Sept 11. Replaced by `LIVE-WIRE-v2.md` (9/25). The limits and rules below were written by Claude Code in Sept unless a line quotes Jaron with a date; sizes and caps are Control Room settings now. Kept as history.**`
  - reason: Archive status label
- **agents/grok-bot/LIVE-WIRE.md**
  - old: `SIZING, JARON'S CALL`
  - new: `SIZING (Claude Code's Sept 11 numbers; live sizes are Control Room settings)`
  - reason: Heading claimed these as Jaron's call with no quote
- **agents/grok-bot/LIVE-WIRE.md**
  - old: `## What Jaron has to do once`
  - new: `## What Jaron had to do once (done 9/11)`
  - reason: Stale chore label
- **agents/grok-bot/LIVE-WIRE-v2.md**
  - old: `## Paste this into Live Wire's Instructions (replaces all of v1)`
  - new: `## Paste this into Live Wire's Instructions (replaces all of v1)
(Limit labels, 10/23: the block is Live Wire's bot text of 9/25, written by Claude Code. 'Jaron has told you to trade on your own judgement, no approval' is Jaron, 9/11, see LIVE-WIRE.md. The sizes are Control Room settings. 'Never chase a loss' and 'never trade crypto' are Claude Code's Sept wording - see the unsure list in state/LIMITS-SWEEP-2026-10-23.md. Block left unedited because it mirrors the live Grok Bot text.)`
  - reason: Label above the mirrored bot text, text itself untouched
- **agents/grok-bot/ROLE-AUDIT-2026-09-25.md**
  - old: `| YES (money; Claude/Codex can't trade) |`
  - new: `| YES (money; Sept belief that Claude/Codex can't trade, superseded 10/7: each provider's terms decide) |`
  - reason: Stale unverified provider claim
- **agents/grok-bot/ROLE-AUDIT-2026-09-25.md**
  - old: `## The "remake" (the one step only Jaron can do)`
  - new: `## The "remake" (Sept 25 belief that only Jaron could do it; platform fact: the text lives inside the Grok Bot app. Since 10/17 Grok Build can drive that window and bots can edit their own Instructions when told in chat)`
  - reason: 'Only Jaron can' was a platform fact, not a wish, and is outdated
- **agents/grok-bot/TRADING.md**
  - old: `# Polymarket US — Bridge trading pipeline`
  - new: `# Polymarket US — Bridge trading pipeline

**Status (10/23 sweep): Sept 11 pipeline, written by Claude Code. 'Jaron approves every order' / 'only after Jaron's explicit yes' was the Sept design; the approve queue was retired 9/24 (Q-023) and orders now go through desk-trade.py inside Control Room limits. The method notes below (edge vs spread, Scout isolation, crypto excluded because of PolyBench) are Claude Code's, not Jaron rules; the crypto lane was approved by Jaron 10/22 (decisions/CRYPTO-LANE-PLAN-2026-10-22.md). Kept as history.**`
  - reason: Status label on Sept pipeline
- **agents/grok-bot/TRADING.md**
  - old: `Default candidate size **$1–$2** unless Jaron says otherwise.`
  - new: `Default candidate size **$1–$2** (Sept 11, account was ~$10; size now follows the Control Room).`
  - reason: Stale size label
- **state/MONEY-LOOP.md**
  - old: `- Withdrawals today are done in the app; retail API keys have no withdraw permission yet. When they do, automate it.`
  - new: `- Withdrawals today are done in the app; retail API keys have no withdraw permission yet (Polymarket platform limit as of 10/9). When they do, automate it.`
  - reason: Platform limit label
- **state/whats-next.md**
  - old: `# What's next - Heartbeat Observatory`
  - new: `# [10/23 note: written 9/28-10/2; the FOCUS and 'next week' blocks below are past. Current focus is in AGENTS.md. 'Jaron's call' lines are decisions Jaron voiced on those dates.] What's next - Heartbeat Observatory`
  - reason: Staleness label
- **TODO.md**
  - old: `then Jaron decides `--live`.`
  - new: `then `--live` is decided (Sept 12 plan; whether to go live follows Jaron's tests and the Control Room, not a standing Jaron gate).`
  - reason: Stale gate
- **TODO.md**
  - old: `- Still needs Jaron at the MSI: Live Wire paste + MCP; Bridge step 8; DEEPSEEK key; CoworkVMService fix.`
  - new: `- Still needed Jaron at the MSI (all DONE 9/11 19:00, see the AT-THE-MSI entry above): Live Wire paste + MCP; Bridge step 8; DEEPSEEK key; CoworkVMService fix.`
  - reason: Stale chore label
- **TODO.md**
  - old: `Jaron pastes Instructions + Routine,`
  - new: `Jaron pastes Instructions + Routine (done 9/11),`
  - reason: Stale chore label
- **TODO.md**
  - old: `**Reality:** Qwen is no longer the decision-maker — Scout researches, Bridge decides, Jaron`
  - new: `**Reality (Sept 11 design):** Qwen is no longer the decision-maker — Scout researches, Bridge decides, Jaron`
  - reason: Label
- **TODO.md**
  - old: `**Who:** Jaron decides the role. **Status:** OPEN`
  - new: `**Who:** Jaron decides the role (Sept 11; 'Jaron approves' above was the Sept design, retired 9/24). **Status:** OPEN`
  - reason: Label
- **TODO.md**
  - old: `## JARON ONLY — needs an Administrator PowerShell on the MSI, can wait`
  - new: `## NEEDS AN ADMINISTRATOR POWERSHELL on the MSI (Windows elevation fact, not a Jaron-only rule; any elevated session can), can wait`
  - reason: Platform fact, not Jaron-only
- **TODO.md**
  - old: `- Habitat iPhone 3D fix — ChatGPT Chat's deliberately, do not touch`
  - new: `- Habitat iPhone 3D fix — ChatGPT Chat's deliberately (Sept 10 ownership split, who works on what; not a safety limit and not a Jaron rule)`
  - reason: Ownership, not safety
- **SITE: live-systems/crypto/index.html**
  - old: `Then everything stops. ``
  - new: `Then everything stops (Control Room settings, approved by Jaron 10/22). ``
  - reason: Label crypto limits by source

### C. Removed/rewritten AI-added caution
- **agents/claude-code/README.md**
  - old: `treat it as an outward action and get his yes first.**`
  - new: `treat it as an outward action (Claude's own Sept 9 convention, not a Jaron rule; AGENTS.md 'Act on your own' applies, just don't interrupt a chat he is mid-use in).**`
  - reason: AI-added 'get his yes first' relabeled as Claude's own convention
- **agents/grok-bot/README.md**
  - old: `form views + place orders (Claude/Codex TOS-barred; Qwen not trusted for views). Jaron approves every order.`
  - new: `form views + place orders (Sept 11 text. 'Claude/Codex TOS-barred' was an unverified Sept belief; 'Jaron approves every order' was Sept design, retired 9/24 Q-023: Grok Bot bots now place orders themselves through desk-trade.py inside Control Room limits, no approval. Qwen not trusted for views: Claude Code's Sept 10 observation).`
  - reason: Stale approval gate and unverified TOS claim
- **agents/grok-bot/README.md**
  - old: `- Nothing outward (send/post/spend/submit/trade) without Jaron's explicit yes.`
  - new: `- (Sept 11 version, Claude Code's wording, SUPERSEDED by AGENTS.md 'Act on your own': trades inside script limits, money the AIs can reach, funding applications and site shipping need no yes; messages for the work are signed "Jaron's AI assistant (<which AI>)" and checked with him first (10/8); posts on his own accounts stay his (10/8).)`
  - reason: AI-written blanket yes-gate contradicted AGENTS.md
- **agents/grok-bot/TRADING.md**
  - old: `| Jaron | Approves every order |`
  - new: `| Jaron | (Sept 11: approved every order; retired 9/24) |`
  - reason: Stale Jaron-as-gate
- **agents/grok-bot/TRADING.md**
  - old: `5. Place only after Jaron's explicit yes.`
  - new: `5. Place only after Jaron's explicit yes (Sept 11 design, retired 9/24).`
  - reason: Stale gate
- **state/MONEY-LOOP.md**
  - old: `## The plan (not switched on yet - waits for more profit)`
  - new: `## The plan (not switched on yet - Claude's 10/9 note: waiting for profit to cover bills; not a Jaron rule or a wall)`
  - reason: AI-added gating labeled by source
- **state/whats-next.md**
  - old: `12. Darios Twin: losing trades exit at 1-7c (nearly the whole stake). Watch; change the rule only with evidence.`
  - new: `12. Darios Twin: losing trades exit at 1-7c (nearly the whole stake). Watch. ('Change the rule only with evidence' was Claude's note, not a Jaron rule.)`
  - reason: AI-added caution labeled
- **agents/grok-bot/LIVE-WIRE.md**
  - old: `So for you: **enter`
  - new: `So for you (Claude Code's Sept 11 inference, NOT a Jaron rule: Jaron later said his manual trades are not evidence for AI trading rules, and v2 dropped it): **enter`
  - reason: AI-added rule derived from his manual trades; he later said they are not evidence

### D2. New unsure items (nothing changed; for Jaron)
10. agents/grok-bot/LIVE-WIRE-v2.md paste block (mirrors the live Live Wire Instructions in the Grok Bot app, left unedited): `never touch funds or settings, never trade crypto, never chase a loss.` and `$5 default / $10 hard disagreement, max 3 open` (sizes are Control Room settings; I only labeled them). 'Never trade crypto' now conflicts in spirit with the 10/22 crypto lane (it is Live Wire's sports lane, so probably fine). 'Never chase a loss' was Claude Code's Sept wording, no Jaron quote found.
11. agents/grok-bot/LIVE-WIRE-v2.md line `Jaron would rather see plays than a clean board.` Plausibly his 'fed queue is the metric', but no dated quote found. Left in the mirrored block.
12. agents/grok-bot/LIVE-WIRE.md line 112-124 'Known limits' and 'Tell Jaron only for a loss over $5' (same as unsure #2; notification threshold, source not found).
13. TODO.md line 144 area: 'Qwen's role stays OPEN' and 'Qwen ... not meant to touch money and do trades' (Jaron 2026-09-11 quote, kept as his statement). Unsure if that still stands for Qwen now that it is a bridge/local model; ask only if Qwen's role comes up.
14. state/MONEY-LOOP.md: 'Who runs it (Darios or Link): not decided' and 'Kraken ... once there's enough to fund it' - timing/gating of the plan. I labeled the 'waits for more profit' line as Claude's note; if you do want the loop switched on now, say so and the plan line can change.
15. agents/chatgpt-chat/2026-10-09-continuity-notes.md is Vex's own notes; I only labeled limits inside it. Its 'Not approved for publication' header is Vex's own privacy note for private reflections; whether the whole file should stay out of the public site is yours to say.
16. state/live-wire.md (754 KB) was not edited: it is a log, though some lines in it are old 'ping Jaron' notes.
17. Not swept (still outside scope): memory folder, decisions/OPEN-QUESTIONS.md, projects/life, state/crew/*.md beyond the existing list, and the many older handoffs.
18. Two unrelated files, state/executor.md and state/verifier.md, show as modified by running tasks; not mine and not committed.
