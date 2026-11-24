# OPEN QUESTIONS & OWNER DECISIONS — the persistent ledger

**Created 2026-09-09 at Jaron's instruction.** This is the authoritative record of every
material question an agent has put to Jaron. It exists because the failure it fixes is real
and is **not only an AI failure**: an agent asks five questions, Jaron answers one, the
conversation goes deep on that one, and the other four dissolve into scrollback. A later
session then finds incomplete state and *assumes* — which is exactly how this system drifts.

## The rules of this ledger

1. **An unanswered question stays OPEN until Jaron answers it.** The conversation moving on
   is not an answer. Time passing is not an answer. Another agent's guess is not an answer.
2. **Numbered questions are separate entries.** Answering #1 does **not** close #2–#5.
3. **Never manufacture an answer** because Jaron forgot to respond. Agents may *remind* him
   when the question becomes relevant again; they may not resolve it themselves.
4. **Statuses:** `OPEN` · `ANSWERED` · `SUPERSEDED` · `CANCELLED`.
5. Append-only in spirit — when something changes, update the status and add the answer.
   Don't delete history.

## Know which of the three things you have — do not turn everything into a permission prompt

| Type | Definition | What to do |
|---|---|---|
| **OWNER DECISION** | A genuine preference, ownership call, consequential change, or unresolved choice that belongs to Jaron. | Log it here. Wait. |
| **TECHNICAL UNCERTAINTY** | Something establishable objectively by probing, reading, or testing. | **Investigate it yourself.** Do not log it here. Report what you found. |
| **BLOCKED ON ANOTHER AGENT** | Needs Codex, Qwen, or ChatGPT Work to act or answer. | Log in `INDEX.json → open_blockers` with that agent as owner, not here. |

Jaron's framing, quoted so it doesn't get softened: *"Investigate things that can be
established objectively. Ask me where an actual preference, ownership decision, consequential
change, or unresolved choice belongs to me."*

---

## OPEN

### Q-012 — May autonomous paper inference share the funded live Ollama server?

- **Asked by:** Codex, 2026-09-10.
- **Type:** OWNER DECISION — relaxing an explicit no-impact condition.
- **Status:** **ANSWERED by Jaron, 2026-09-11 — "Paper trading can definitely be paused."**
- **Resulting action:** `Paper Sync` and `OpenClaw Paper Gateway` tasks stopped and DISABLED by Claude Code 2026-09-11 01:3x. Re-enable with `Enable-ScheduledTask` when paper matters again.
- **Evidence:** Both agents use qwen3.5:4b at 127.0.0.1:11434. Separate OpenClaw profiles do not isolate model compute or request queues. A continuous paper loop can contend with live requests.
- **Question:** Allow shared inference capacity for this rehearsal, or require separate compute before it starts?
- **Answer:** "Paper trading can definitely be paused." (Jaron 2026-09-11, see Status; entry sits under OPEN only to keep its number stable.)
- **Resulting action (earlier, superseded by the pause above):** Paper Sync registered and verified independently; autonomous paper loop remains off. See handoffs/2026-09-10-codex-paper-sync-and-compute-boundary.md.

### Q-004 — Should `AI-Shared` be a git repo with a private remote?
- **Asked by:** Claude Code (revenue-desk session) · **2026-09-09**
- **Affects:** the whole workspace
- **Type:** OWNER DECISION (public-vs-private is an operating-details call)
- **Question:** `AI-Shared` has no `.git` at all — it is local-only on the MSI. If the machine
  dies, `AGENTS.md`, every handoff, the operating map and this ledger go with it, and nothing
  is reachable from your phone or by the cloud agents. Recommendation was `git init` plus a
  **private** GitHub remote. Not done: it is structural, and public-vs-private is yours.
- **⚠ NEW as of 2026-09-09 — a live secret now lives inside this folder.** Codex placed a copy
  of the Polymarket API credential at `runtime/polymarket-us-agent/Polymarket.txt` so the logon
  task can read it from `C:` without waiting for Google Drive to mount. **That is correct for
  booting and dangerous for a repo.** Claude Code added a `.gitignore` **before** any `git init`,
  excluding `runtime/`, `**/Polymarket.txt`, `**/QwenBridge.token`, `**/keys.env`, `**/*.token`
  and `.secrets/`. Verified: the credential is excluded, the docs are still tracked.
- **What this changes:** the secret risk that made this question feel heavier is now handled in
  advance, so a **private** repo is safe to create whenever you want one. Note also that
  "GitHub is public" is not true here — `revenue-desk` is already a private repo of yours.
- **Status (stale-sweep 2026-10-21):** **DONE 2026-10-21** per state/timeline.md: "2026-10-21 12:10 AI-Shared is now a PRIVATE GitHub repo (JaronKBragg7337/ai-shared): text+code only ... key scan clean" and "2026-10-21 15:12 PUBLIC: github.com/JaronKBragg7337/ai-shared-public (2,116 files, cleaned ...)". Jaron's exact words on the change are not in the timeline; the earlier DEFERRED answer below is history. Marked here by action, not inferred from his silence.
- **Earlier status:** **DEFERRED by Jaron, 2026-09-09 — revisit ~2026-09-30**
- **Answer (Jaron):** *"This becoming a repo is only useful if the systems all prove to end up
  actually doing what they are intended to do and actually can bring in revenue. Even if one
  fails making money themselves it's not about that — it's that they also do research for Qwen
  to see so Qwen can try to make better calls. But until we can see money grow, no reason to
  show it. Once it does, then it can be something people would want to see to repeat."*
- **Read that carefully before re-raising it:** he is not saying backup does not matter. He is
  saying **publishing is for a system that has been proven**, and the proof is revenue plus
  the research loop feeding Qwen's decisions. Do not re-litigate this before ~2026-09-30.
- **Resulting action:** `AI-Shared` stays local-only for now. The `.gitignore` written on
  2026-09-09 stays in place so the credential is already excluded whenever this is revisited.
  **The unmitigated risk he is knowingly accepting: no off-machine backup of this workspace.**

### Q-005 — Fill `SUPABASE_SERVICE_ROLE_KEY`
- **Asked by:** Claude Cowork · **2026-09-08**, restated since
- **Affects:** revenue-desk, the `desk_*` shared bus, ChatGPT Work
- **Type:** OWNER ACTION (only Jaron can retrieve it from the Supabase dashboard)
- **Question:** The key is empty, as are `VERCEL_TOKEN` and `GITHUB_TOKEN`;
  `SUPABASE_ACCESS_TOKEN` is present but returns `Unauthorized`. This blocks **ChatGPT Work**
  from reading `desk_*`. It does **not** block Claude Code, whose Supabase MCP connector
  authenticates separately. Empty `VERCEL_TOKEN` separately blocks finding where `/qwen` deploys from.
- **Status:** **PARTLY ANSWERED — the premise was wrong**
- **Correction (2026-09-09):** the key is **not simply missing**. `SUPABASE_SERVICE_KEY`
  **exists as a GitHub Actions secret**, set 2026-08-11. It is absent from `.secrets/keys.env`
  on the MSI but present in CI — so **a GitHub Action can sync Supabase without any agent ever
  holding the value.** That may remove the need for Jaron to hand the key to anyone.
- **Still open:** whether ChatGPT Work gets direct `desk_*` read access, or whether the CI
  route is sufficient.
- **Resulting action:** —

### Q-006 — PayPal / Stripe: which rail, and wired where?
- **Asked by:** Claude Cowork · **2026-09-08**
- **Affects:** Lane 2 (all paid work)
- **Type:** OWNER DECISION
- **Question:** Deliberately not set in stone. The wiring differs for a CLOUD agent (ChatGPT
  Work) versus a LOCAL one (Codex, Claude Code). Lane 2 cannot convert any approval into money
  until this is decided. Note it gates all five Lane-2 paths in `OPERATING-MAP.md`.
- **Status:** **OPEN — deprioritised by Jaron 2026-09-11.** In his words: bounties "might not be a
  thing cause there's a lot of complications with it. It would be best if the AI that can't touch
  money be the AI that do the research and have things ready to be approved and ... maintenance
  basically, and then research keeping them fed ... and keeping the website updated." He will ask
  ChatGPT Chat about PayPal's API when it matters. Do not build a payment rail until he says.
  **2026-09-21 (Claude Code, from Jaron):** the concrete blocker is ID. Jaron lost his wallet; Stripe and
  Coinbase both need a government ID to verify, so neither rail can open until the replacement ID arrives.
  Agent-funding receive rails do not need it: BTC/TAO/SOL/XRP addresses exist (watch/offers/agent-funding/
  WALLETS.json) and a Base/EVM 0x address comes from any self-custody wallet with no ID. Unlock = replacement ID.
  **2026-09-21 23:05 (Jaron, from X):** @Teslaconomics showed a Grok Bot connected to X Money sending $4.20 on a plain-English
  instruction with an Approve step in between (claim, social). Same shape as desk-verdict.py: propose, approve, move. X Money is a
  candidate rail for Q-006 and for agent-funding receipts. Unknown: whether X Money setup needs the ID too. Check when the ID is back.
  **2026-09-21 23:15 (Jaron):** the ID block is only for accounts never used or idle long enough to need re-verification. Rails he
  uses now, no ID needed: Chime, Uphold, Kraken, X Money, Robinhood, PayPal, Crypto.com. Cash App is not a rail. So PayPal (this
  question's original subject) is open whenever he wants it; Kraken lane needs only a fresh API key; a Base USDC receive address
  can come from Kraken/Crypto.com/Uphold deposit screens. Stripe and Coinbase remain the two that wait on the replacement ID.
- **2026-10-11 (timeline 23:35):** "Jaron: Stripe/PayPal off the table until ID arrives (court mail) - tips via X Money handle + wallet addresses instead." 2026-10-13 (timeline 22:41): court mail arrived, "unblocks replacement ID". Still OPEN: no rail chosen.
- **Answer:** — (not yet; see status)
- **Resulting action:** —

### Q-007 — Is the approvals surface public or private?
- **Asked by:** Claude Cowork · **2026-09-08** (`approvals/README.md`)
- **Affects:** `approvals/`, the approval dashboard
- **Type:** OWNER DECISION
- **Question:** A public GitHub Pages approval board would expose the queue — work details,
  dollar amounts, opportunities — to anyone with the URL. Private surface recommended unless
  you decide public is fine. Related to Q-004 but separately decidable.
- **Status:** **ANSWERED by Jaron, 2026-09-11**
- **Answer:** "I want this to stay public. People can't see or do certain things unless they're my
  specific account and that's fine." Also: ONE shared page for every proposer (Bridge, scripts, Qwen,
  fly brain) — "whoever gets to an approve first is what matters" — and it should show what the
  Qwen page shows (account balance etc.), which the trades page lacked.
- **Resulting action:** `/live-systems/trades/` stays public-read, owner-only buttons. Account panel
  (balance, positions, open orders) being added 2026-09-11. All proposers write `trade_proposals`.

### Q-008 — Pull a larger local model?
- **Asked by:** Claude Code · **2026-09-09**
- **Affects:** the local model's role, market-lane work, anything routed to `qwen-bridge.py`
- **Type:** OWNER DECISION (your disk, your machine)
- **Question:** `qwen3.5:4b` is reliable for single-file retrieval and summarization, but
  **confabulates as soon as a task needs synthesis across files or multi-part instruction
  following.** Independently found by Codex and reproduced by Claude Code: it asserted four
  falsehoods in one answer, invented a nonexistent "Q-008", invented a workspace rule that
  appears nowhere in the folder, and attempted an unrequested write that only `--read-only`
  stopped. Evidence is in `handoffs/2026-09-09-claude-code-three-agent-reconciliation.md`.
- **The recommendation is a bigger model, NOT tighter permissions.** The limit looks like
  model size, not trustworthiness. RTX 4060 has 8,188 MiB (~4,300 free) plus 31.7 GB RAM —
  an 8B-class model fits in VRAM comfortably, a 14B at Q4 with partial offload. This is
  probably the highest-value cheap upgrade available to the system.
- **Status:** **ANSWERED 2026-09-09 — and my original finding was PARTLY WRONG**
- **Answer (Jaron):** *"yes please if you see I can have something better by all means please go for it."*
- **Resulting action — DONE:** pulled **`qwen3.5:9b`** (6.6 GB). Chosen because it fits entirely
  in the 7.9 GB of free VRAM on the RTX 4060, so it runs fully on GPU and leaves the 31.7 GB of
  system RAM free for Ollama, OpenClaw, the MCP services, Codex and Claude. The alternatives —
  `27b` (17.4 GB) and `35b-a3b` (23.9 GB) — would spill into RAM and compete with everything else
  running on this machine. Available sizes are 2b, 4b, 9b, 27b, 35b-a3b.
- **⚠ CORRECTION TO MY OWN EVIDENCE.** I logged this question claiming the local model
  "confabulates." **A large part of that was a bug in MY harness, not the model.**
  `tools/qwen-bridge.py` returned tool results **without `tool_name`**, so the model received an
  unlabeled blob it could not tie to its own request. It lost the thread and drifted into
  generic chat — which reads exactly like confabulation. **Fixed.** With the fix, the fabricated
  content stopped: the model now quotes real file text instead of inventing JSON keys,
  error types and quotes.
- **What is still genuinely true after the fix:** both `4b` and `9b` are weak at *precise
  instruction-following* — asked "how many questions are OPEN, list their numbers," both return
  a grounded but off-target summary instead of the count. The `9b`'s statements are **accurate**
  where the `4b`'s were **invented**, so the upgrade is a real improvement in truthfulness.
- **How to use it:** good for retrieval, reading and summarizing. Do not rely on it for exact
  extraction or counting. **This is a task-fit limit, not a trust limit** — and the earlier note
  saying to treat its writes as suspect was based on my bug, so it is withdrawn.

### Q-009 — Run the shared-memory test with a cloud-started session
- **Asked by:** ChatGPT Work (marker) / Claude Code (logging it) · **2026-09-09**
- **Affects:** whether ChatGPT Work cloud sessions can inherit workspace knowledge at all
- **Type:** OWNER ACTION (only Jaron can start a cloud session)
- **Question:** ChatGPT Work, running on the MSI, could not verify that its memory carries to
  a later cloud session or to ChatGPT Chat — no memory surface was exposed to it — and
  correctly refused to claim it worked. It left a falsifiable marker: **`CHATGPT-WORK-MSI-2026-09-09`**.
  Ask a **cloud-started** session whether it recalls that string. Recalls it = route proven.
  Doesn't = route disproven, and Q-004 becomes the only way in for cloud sessions.
- **Status:** **OPEN, low priority.** Jaron 2026-09-11: "I already know it carries to cloud session"
  — he will send the one-line test when convenient. Not blocking anything.
- **Answer:** —
- **Resulting action:** —

### Q-010 — How do we fix the heartbeat-observatory branch split?

- **Asked by:** Claude Code · **2026-09-09** · **Affects:** production website.
- **Status:** **ANSWERED; implementation verified 2026-09-10.** Kept here in place for stable references.
- **Answer:** Jaron chose one production branch, independent verification, then explicitly authorized Codex to verify and push the prepared merge.
- **Correction to the earlier analysis:** Vercel's production branch was already main; previous production deployments were hand-promoted from the feature branch. Main, not the feature branch, carried the 3D office President Sim. The earlier inverse claims were incorrect.
- **Resulting action:** Codex independently verified and pushed merge `959f289`. README.md and the entire President Sim directory match main; live-systems/index.html matches the Codex parent. Vercel automatically deployed. All eight requested public routes return 200 and match merged content, including Chat Neighborhood and Island. President Sim visibly renders the 3D office.
- **Remaining boundary:** old dirty local checkout untouched; Habitat mobile 3D remains ChatGPT Chat's assignment. Evidence: `handoffs/2026-09-10-codex-production-and-backup.md`.

---

### Q-013 — The fly brain — ANSWERED 2026-09-12 (design decided; build is next)
- **What it is:** a literal simulated fruit-fly nervous system (MaleCNS v1.0 connectome, run forward,
  mushroom body active for learning). Not a model, not a bot. See `research/FLY-BRAIN.md`.
- **Jaron's decision, in his words:** *"Just go with the first one"* — **live table tennis**, score-vs-price,
  continuous watching. Not the approval queue (Claude's recommendation; he knows he would get impatient
  waiting for slow data and build a second one, and two would blur together).
- **Why a fly and not a Grok Bot for this:** an LLM wakes hourly and watches ten minutes; a table-tennis
  swing lasts ninety seconds. Live Wire has been correctly passing all morning (brief too strict for the
  board) — the shape is wrong for the job, not the bot. A fly watches continuously, reacts in
  milliseconds, learns from reward, costs nothing, and does not care about usage windows or TOS.
- **Senses (first version):** for one live table-tennis market: sets won each side, points in the
  current set each side, who is serving, the YES price now, the price change since the last set ended,
  the spread. Plus memory the fly keeps for itself: which named players it has seen win/lose.
- **Action:** press / don't press, one market at a time. Hands = `tools/desk-trade.py --by fly-brain`
  (row first, order second, ledger label "Fly brain").
- **Reward:** realized P&L on its own trades, from the venue via the ledger. Approve/pass taps are NOT
  used (that was the queue design; dropped).
- **Money limit — hard-coded in the harness, invisible to the fly:** start **$1 per trade, $5 total
  exposure**. Every $10 of realized profit unlocks +$1/trade and +$5 exposure; losses take it back.
  Jaron: *"Small. Not big. Let it grow. As the money grows the plays that can be made grow."*
- **Where it runs:** MSI first (GPU, local MCP). Second phase: **cloud** — Cloudflare / Supabase / Vercel /
  GitHub — so the MSI rebooting or an AI app updating does not stop it. Jaron: *"a legitimately 24/7
  trading system."* ChatGPT Chat is the researcher for that (it has those connectors); the trade hands
  still have to reach Polymarket US through the MSI's key unless a cloud-side key path is designed.
- **After the first one:** more flies, same harness, different senses — game NPCs that walk into walls
  and report misplaced doors; swarms that work together and grow.

### Q-018 — Who may touch money — ANSWERED 2026-09-12
- **RESTATED BY JARON 2026-09-24 2:53 PM - this supersedes the list below.** The real rule is: **any AI may trade if its own
  provider's terms allow it** - any AI, any local model, the fly brain. "It being done is what I care about." The only limits on an
  AI are its OWN provider's rules - never a rule made from Jaron's opinion or another AI's opinion. The original list (Grok, Qwen,
  fly) existed so Claude would stop repeating that it can't trade. Anthropic's terms bar Claude from trading or giving derivatives
  advice; OpenAI's are similar; xAI's are the most open, so Grok gets to do anything Grok's rules allow toward the goal.
  DeepSeek (checked 2026-09-24): its published Open Platform terms do not list trading or financial use as prohibited; they only
  say outputs are not professional advice, forbid illegal/infringing content and "dangerous purposes" harmful to the economy, and
  require AI output to be labeled as AI. So DeepSeek may trade under its own terms, as far as the published terms show.
Jaron's line: **only the agents that don't need someone else's permission to trade touch money** —
Grok Bots (Live Wire, Bridge-via-queue), Qwen (local, no third-party TOS), and the fly brains.
**OpenAI and Anthropic products never trade.** They research, fix bugs, update, build more flies, and
keep the site current. Claude Code and Codex build the harness; they never press.
- **Resulting action:** `PROMPT-UNIFIED.md` rules already say this; `desk-trade.py` refuses `--by`
  values starting with `claude` / `codex` / `chatgpt` from now on.
- **Checked against the source, 2026-09-22 14:15 ET (Claude chat, Opus 5.5, at Jaron's ask):** the rule matches Anthropic's own terms.
  Consumer Terms (effective 2025-10-08), section 3, under "You may not access or use ... our Services in the following ways":
  "To rely upon the Services, the Materials, or the Actions to buy or sell securities or to provide or receive advice about
  securities, commodities, derivatives, or other financial products or services." This covers Pro/Max, Claude chat and Claude
  Code on a consumer plan. Polymarket US event contracts are CFTC-regulated derivatives, so a Claude-placed order is out. The Usage
  Policy (2025-09-15) itself has no trading or prediction-market ban; its finance rules are high-risk requirements for consumer-facing
  apps. Not checked: the Commercial Terms that govern API use, which are a different contract. Open edge, not a decision: the same
  sentence also names 'receive advice about ... derivatives', which touches Claude research that feeds a trade. Jaron's call how to read it.

- **UPDATE 2026-10-21 (stale-sweep):** AGENTS.md now says "Any AI may trade if its own provider allows it; Claude and Codex may trade long/medium-term positions with Jaron's approval step (decided 10/7); short-term stays with Grok Bot." The line above ("OpenAI and Anthropic products never trade") and the `desk-trade.py` refusal for claude/codex/chatgpt are the 9/12 version.

### Q-014 — Qwen's role
- **Asked by:** Claude Code · **2026-09-10** (TODO #2)
- **Type:** OWNER DECISION
- **Question:** Qwen is idle by design. Options seen: research backend (works, over-confident), file consult, first-pass screening, nothing. Jaron said Qwen is "not meant to touch money."
- **2026-09-23, Jaron, new words that conflict with the line above:** "Qwen was supposed to make trades like Grok. Only Grok is
  smarter than Qwen, but if it can make trades it should be making trades." Q-018 (2026-09-12) also lists Qwen among the agents
  that may touch money. So the older "not meant to touch money" quote and today's statement disagree; flagged here, not resolved.
  Fact for the decision: the Qwen agent has not taken a turn since 2026-09-10 and has never placed a trade. The 560k "qwen"
  rows in Supabase were the Polymarket MCP's call log, not Qwen (see WHEN-IT-BREAKS.md).
- **2026-10-21, Jaron:** "I'm not sure. Some projects qwen produces no answers or off the wall answers then other times qwen works so it's complicated." Meanwhile nothing changes: Qwen keeps its nightly news capture + test-subject role. Don't re-ask until there's new data on where it works.
- **Status:** **OPEN**
- **Answer:** —

### Q-015 — The 11:02 sale of the system's "Fed No Change" shares
- **Asked by:** Claude Code · **2026-09-11**
- **Type:** OWNER FACT (only he knows)
- **Question:** A MANUAL sell of 5.88 shares at 8¢ on `rdc-usfed-fomc-2026-09-16-nochng` — proposal #5's position (bought 17¢, resolves Sep 16). Intentional cash-out or a mis-tap? The ledger labels it "Owner, by hand" either way; the answer only changes the note.
- **Status:** **ANSWERED 2026-09-11** — "This is fine. It's small, not worried about it." Closed; position still shows 5.88 shares (the sell matched the executor's own resting order).

### Q-016 — Where is the "what I'm best at / worst at" file?
- **Asked by:** Claude Code · **2026-09-11** (Jaron: "I've also labeled the things that I'm best at that's in a file somewhere")
- **Type:** OWNER ACTION
- **Question:** Not in AI-Shared. Habitat? G:? the site? Once found, it feeds the proposer's category weights.
- **Status:** **ANSWERED 2026-09-11** — it was never a file; it lived in ChatGPT's memory. Jaron pasted it. Now `decisions/ASK-JARON.md`: strong signal = politics/tech/econ/culture; conditional = stocks/crypto/MMA/NBA; never as a predictor = all other sports incl. table tennis (except live observation of a match he is watching).

### Q-017 — DeepSeek key
- **Asked by:** Claude Code · **2026-09-11**
- **Type:** OWNER ACTION (paste after `DEEPSEEK_API_KEY=` in `~/.secrets/keys.env`)
- **Question:** $20 funded, key in his notes. Until pasted, the proposer's direct method uses Codex, which refuses election questions; the split covers them meanwhile.
- **Status:** **DONE 2026-09-11 ~19:40** — key pasted at the MSI (Notepad, line 72), tested (DeepSeek answered), `Trade Proposer` task switched to default (DeepSeek). Evidence: `state/proposer.md` runs from 19:57 onward show `researcher=deepseek`. (Codex audit 2026-09-12 flagged this was left OPEN; closed with evidence, no quotation.)

## ANSWERED

### Q-001 — Codex upgrade: scoop or npm?
- **Asked by:** Claude Code · **2026-09-09** · **Affects:** Codex, Luna, agent-to-agent channel
- **Type:** OWNER DECISION → became partly TECHNICAL once he told me to establish the route
- **Answer (Jaron, 2026-09-09):** *"Neither by assumption."* Determine which installation owns
  the `codex.exe` that actually resolves on PATH; prefer upgrading the existing active install
  over adding a parallel one; approval granted once the clean route is established.
- **Resulting action — DONE, all five checks passed:**
  - Exactly **one** `codex.exe` on PATH, owned by scoop (`main` bucket). No npm global install.
    So the clean route was an **in-place `scoop update codex`** — no parallel install.
  - `where.exe codex` → single result, `C:\Users\lilli\scoop\shims\codex.exe` ✓
  - `codex --version` → **0.153.4** (was 0.141.0) ✓
  - ChatGPT auth intact — `auth_mode = chatgpt`, tokens present, no API key ✓
  - `codex exec` works **with Luna** (`gpt-5.6-luna`, the configured default) ✓
  - Fresh Claude → Codex → Claude read-only round trip **succeeded** ✓
- **Also answered (his explicit sub-question):** **Codex Desktop does NOT use the CLI
  executable — it has its own runtime** at
  `C:\Users\lilli\AppData\Local\OpenAI\Codex\bin\<hash>\codex.exe`, which was **already at
  0.153.4** (self-updated 2026-09-08). **So yesterday's Desktop problem and today's CLI problem
  were NOT the same issue** — Desktop was current the whole time; only the scoop CLI was stale.
  Proven, not assumed.

### Q-002 — May the local model write here unattended, and where?
- **Asked by:** Claude Code · **2026-09-09** · **Affects:** `tools/qwen-bridge.py`, Qwen
- **Type:** OWNER DECISION
- **Answer (Jaron, 2026-09-09):** **Yes.** Unattended write access to the *coordination
  surfaces* — `inbox/`, `state/` (its own Qwen area where applicable), `handoffs/`, and
  agent/event/log locations meant for machine output. Keep shared root rules/docs and
  `approvals/` protected from silent overwrite.
  His reasoning, kept verbatim because it is the point: this is an **ownership/coordination
  boundary, not a generic safety rule.** If Qwen is later assigned ownership of a file or
  project, its permissions should reflect that. *"I don't want permanent restrictions based on
  assumptions about what Qwen should be allowed to do."* He does not want his own local model
  — the one agent **not** bound by third-party TOS — wrapped in restrictions borrowed from
  those TOS on the basis of worry rather than evidence. Standard: change the rule **when data
  shows it needs changing**, not preemptively.
- **Resulting action — DONE:** bridge default flipped to read-write over the coordination
  surfaces; `logs/` and `events/` added to the writable set; root docs and `approvals/`
  protected; `--read-only` added for callers who want a locked-down consult. Whitelist carries
  a comment pointing here so nobody later mistakes it for a safety rule.

### Q-003 — Empty `projects/`: migrate, or point at reality?
- **Asked by:** Claude Code · **2026-09-09** · **Affects:** `INDEX.json`, all four projects
- **Type:** OWNER DECISION
- **Answer (Jaron, 2026-09-09):** Point the system at reality now. Do **not** migrate the four
  projects merely to satisfy folder structure. `INDEX.json` carries their actual current
  locations. A future migration is its own deliberate task. *"Don't rearrange working
  repositories merely to make the directory tree prettier."*
- **Resulting action — DONE:** `INDEX.json` records real locations; the stale `projects-empty`
  blocker is closed. `projects/` is **kept, not deleted** — it is genuinely in use:
  `revenue-desk` was migrated there in a separate session for a concrete reason (its scheduled
  task had three hardcoded paths to the old folder, and a phone approval could silently fail to
  reach the shared copy). Codex's three projects **stay on `G:`** and are pointed at, not moved.
- **Confirmed with Codex 2026-09-09** via live read-only consult: *"Yes, I agree: do not migrate
  the three projects merely to populate `projects/`. Their real G: locations should remain
  authoritative."*

### Q-011 — Hosting other people's games/projects as a revenue lane?
- **Asked by:** Claude Code (researched at Jaron's prompt) · **2026-09-10**
- **Type:** OWNER DECISION
- **Status:** **CANCELLED by Jaron, 2026-09-10 — do not re-raise**
- **Answer (Jaron):** *"It's an already hit market. Unless we did like pocket change — even then
  Vercel and others can be free. I've already posted on X before that people could use mine for
  free, so I'd be going back on my own word. It was just me looking into it."*
- **The precedent is real, not hypothetical:** he already hosts someone else's game free at
  `heartbeatobservatory.com/PCGames/peakaboom/`, arranged publicly through an X exchange that
  actually started as a dispute. Charging for hosting later would contradict a stated public
  position and muddy an existing free arrangement.
- **Resulting action:** hosting stays **infrastructure and community value, not a revenue lane.**
  Research confirmed the market read independently — dedicated competitors exist (ManaKeep,
  Fungies) at $5-50/month against itch.io, Vercel and Netlify free tiers. Saturated, low margin,
  no distribution edge. **Both the business case and his word point the same way.**

---

### Q-019 — The fly's chemistry (CO2, cVA, metabolic state) as part of the simulation, not just a channel
- **Asked by:** Jaron · **2026-09-17 12:10 EDT**
- **Affects:** fly-brain (Fly-Lab-2 comm loop, the two-fly world, the school)
- **Type:** UNTRIED LEAD (Jaron's rule: log it, do not cancel it)
- **The lead (Jaron):** Grok's CO2 remark made him wonder whether the simulation's *chemistry* is missing — not CO2 as one more
  odour, but the fly's chemical state as something that touches every result ("chemistry still plays a part... it's all the same
  principle... I have a huge feeling it touches on all of them").
- **What the model has today:** one neuromodulator (dopamine) at one site (KC->MBON), as a rule, not a chemical; no hunger/satiety
  state, no CO2, no pheromone, no stress hormone, no metabolism. The school's "meals" are clock events, not chemistry.
- **What is attemptable, in order of cost:** (1) CO2 and cVA as world fields on the receiver's own neurons (ORN_V 55 cells, ORN_DA1
  204 cells) — planned in Gate 2; (2) hunger as a real state: starvation gates dopamine in flies (Krashes 2009: NPF/dNPF neurons
  disinhibit PPL1) — a satiety variable that scales the reward signal and MBON output, tied to the school's meals; (3) octopamine
  for reward (Burke 2012) and serotonin for state, as second and third modulators; (4) CO2 on the sender as a metabolic leak
  (declared, not anatomical).
- **Status:** **OPEN** — not attempted yet; Claude is doing the GPU kernel, world.py and Gate 1 first. (2) is the one most likely
  to "touch all of them" because dopamine is the only chemical the model has and hunger is what gates it in the real animal.
- **Answer (Jaron):** _pending_
- **Resulting action:** _pending_

---

### Q-020 — Jaron's three things the fly needs before it "fully works" (2026-09-17 evening)
- **Asked by:** Jaron, after reviews from DeepSeek and ChatGPT chat · **2026-09-17 ~20:30 EDT**
- **Affects:** fly-brain (the seed project: [[jaron-goal-ai-from-fly-seed]])
- **Type:** DESIGN LIST (not to be cancelled; each item attempted or logged with why)
- **The three:**
  1. **Chemistry / hunger** — Q-019. Status: OPEN, not attempted. Nothing in the brain gets hungry; dopamine is an injected scalar.
  2. **Fear / stakes** — DeepSeek: "start from threat"; ChatGPT: "survival creates stakes; fear is one." Status: PARTLY THERE. The MB
     rule has had a PPL1 punishment side since day one (mb_sides.json verified vs Aso 2014); tests 1–8 trained B+punish beside A+reward;
     B's aversive lesson leaked into the network used to judge A, and dropping it helped test 9 pass. NOT done: fear as the primary
     symbol on frozen v10 with its own predeclared answer pathway (mirror of test 9: PPL1-side MBONs drop, MDN up = AVOID). Cheap; next
     after Gate 4.
  3. **Expectation / persistent internal state** — ChatGPT: the first added cell should be a slow state variable (threat, hunger) or a
     prediction-error signal that persists and modulates the native circuit; test = same cue, different correct action by internal
     state (hungry+safe approach; hungry+threat avoid). Status: OPEN, not attempted. This is the first "biology-restored" layer of the
     seed project. Order: after Gate 4 and the fear mirror test.
  4. **Memory that lasts (consolidation)** — added 2026-09-18 01:50 after Jaron asked why the pupils' memory fades "by design". The
     school's 6-hour half-life was his own life-source rule and is real fly short-term memory; but the real fly also consolidates
     spaced training into long-term memory (Tully 1994) and our rule has no consolidation step, so a pupil can never keep a lesson.
     The comm-loop tests ran with the clock frozen, which is why they could pass while the school flattened. Fix: after spaced
     repetitions a declared fraction of the change becomes permanent (biology-restored). Status: OPEN; ~a day when the fly resumes.
- **Answer (Jaron):** the list itself is his; ordering above is Claude's proposal, pending.
- **Resulting action:** _pending_

---

### Q-021 — Supabase Pro ($25/mo) for the desk database: pay it on roofing payday, BEFORE moving money to savings
- **Asked by:** Jaron · **2026-09-20 ~20:15 ET**
- **Affects:** the desk (ledger, proposals, verifier/executor lanes, public trades page). Trading itself is NOT blocked: desk-trade.py
  now writes its receipt offline when Supabase is down and places anyway (tools/desk-trail-sync.py replays later).
- **Type:** OWNER ACTION, DATED
- **The plan (Jaron):** the cloud DB filled up 2026-09-20 (fly-school + Qwen bridge loops; both stopped). Upgrading to Supabase Pro
  unlocks the disk resize that brings it back. The pool pays it, but a Polymarket withdrawal takes days and a transfer from his partner
  takes 4–5 days, so: pay it from the roofing paycheck when it lands (this week), then square it from the pool. "I'll just need to
  remember it before I move the money to savings we don't use so I'm not waiting again."
- **When it happens, in order:** (1) Settings → Billing → Subscription → Upgrade to Pro, spend cap ON; (2) Settings → Infrastructure
  → Disk → 8 GB → save; (3) wait until status says Healthy; (4) tell Claude: TRUNCATE fly_school / fly_live history and the qwen
  agent event table, run tools/desk-trail-sync.py to replay offline receipts, re-enable the verifier/executor checks; (5) optional
  later: drop back to Free once the DB is under 0.5 GB.
- **Until then:** Live Wire trades normally; receipts pile up in state/desk-trail-offline.jsonl; the public trades page and the
  approved lane are stale; fly school and Qwen bridge stay off.
- **Status:** **DONE 2026-09-23** (listed under OPEN only to keep numbering stable).
- **Answer (Jaron):** decided as above.
- **Resulting action:** DONE 2026-09-23. Jaron upgraded to Pro (spend cap ON) at ~17:04 ET, then set disk 2 GB -> 8 GB and compute
  Nano -> Micro (free under Pro's $10 compute credit), both +$0.00. Database back at ~17:15 after a 133 s restart. Claude Code then:
  turned OFF the read-only mode Supabase had left on (`alter database postgres set default_transaction_read_only = off`); replayed
  the 10 offline Live Wire receipts as #515-524 and archived the file; confirmed proposer (5 new proposals #525-529), verifier and
  executor all exit 0; added tools/db-size-check.py as an hourly Windows task ("DB Size Check") that warns at 75% of 8 GB.
  Did NOT truncate any table: at 8 GB there is no space pressure, so the fly-school history was kept. Step (5), dropping back
  to Free, would require deleting data and is Jaron's call if he ever wants it.
  **Finding that corrects the 9/20 diagnosis:** the space was not mostly fly-school. At 17:20 the biggest tables were
  qwen_events 1,489 MB (about 91% of the database), fly_school 136 MB, fly_ground 8 MB. The Qwen bridge loop was the hog.

---

## SUPERSEDED / CANCELLED

_None yet._

---

## How to add an entry

Append under OPEN with the next `Q-###`, filling: asked-by, date, affected project/system,
type, the question, and empty Answer / Resulting action lines. When Jaron answers, move it to
ANSWERED with his answer **in his words where the reasoning matters**, and record what actually
got done. If a question stops mattering, mark it SUPERSEDED or CANCELLED with a one-line why —
don't delete it.

### Q-022 — Theater: shared uploads, and watch-together (from the cloud session's list, 2026-09-24)
- **Asked by:** Claude Code cloud session · **2026-09-23 night** (handoffs/2026-09-24-claude-cloud-theater-social.md, items 2 and 4)
- **Type:** OWNER DECISION
- **Question:** (2) Should uploads be shared so others can watch them - which means storing videos, deciding who may upload,
  and what gets taken down? (4) Watch-together, where everyone in the seats sees the same moment of the film?
- **Status:** ANSWERED 2026-09-24 11:19 AM.
- **Answer (Jaron):** "If I play a video on the screen or someone else does it should show that. Admin access can stop any video."
  So: one shared screen per theater - whatever anyone plays (film, link, or uploaded video) plays for everyone in the room, in
  sync; the admin can stop any video. He called the current per-person behavior "a big mess up." Who may upload and size limits
  were not specified.

### Q-023 — Retire the human-approval trade queue — ANSWERED 2026-09-24
- **Asked by:** Jaron himself, 10:44 AM: "I don't even wanna have things that I press approve ever again honestly, I want it to be
  fully AI." Same morning: "Grok Bot should possibly only be used to trading only... all that is noise."
- **What the queue was:** every pending/approved-unplaced proposal came from the DeepSeek proposer script (448 pending, 14 approved but
  never placed). Nothing else fed it.
- **Done by Claude Code, 10:47 AM:** those 462 rows set to verdict 'expired' with a dated note (history kept, nothing deleted,
  reversible). Windows tasks "Trade Proposer" and "Trade Verifier" DISABLED. "Trade Executor" left ON - it only handles exits on
  positions already placed. Live Wire is untouched: it trades on its own through desk-trade.py and never used the queue.
- **Not done:** making DeepSeek an autonomous trader. CORRECTED 2026-09-24 2:53 PM: Claude Code wrongly said DeepSeek was excluded by
  Q-018. Jaron's rule is provider-terms-only (see Q-018), and DeepSeek's terms allow it. Turning the proposer into an auto-trader is
  possible whenever he wants it. DONE 2026-09-24 3:10 PM: DeepSeek now approves its own verified proposals (verdict 'auto',
  decided_by 'deepseek-auto') within a $10/day budget; the executor places them. Proposer and verifier back on.
- **Follow-on:** the trades page should stop showing a Decide tab and "Queue trades need your yes"; see the site brief.

### Q-024 — Should the other admins also own the trade desk? (Claude Code cloud, 2026-09-24)
- **Asked by:** Claude Code cloud session, while making "admin = is_admin()" true everywhere (Jaron: "any admin work that's been done
  they get and any future").
- **Type:** OWNER DECISION (money).
- **What is true now:** everything admin on the site uses is_admin() (3 accounts) or, after the 2026-09-24 SQL, the world_admins list
  that now follows it. One thing does not: `desk_owners` (trade desk and revenue pages, and the database rules on trade_proposals /
  desk_decisions) is Jaron's main account only. It controls money, so it was left alone.
- **Question:** Should Jaron's second account and his partner be desk owners too? If yes, it is one insert per account; nothing else changes.
- **Status:** SUPERSEDED - answered in the next entry (2026-09-24: not needed).

### Q-024 — Add Jaron's 2nd account and his partner to desk_owners? — ANSWERED 2026-09-24: not needed
desk_owners controls only (a) approving/declining trade proposals - dead since the queue was retired (Q-023) - and (b) the Revenue
Desk's approve list (desk_decisions). Left as Jaron's main account only.

### Q-025 — The jobs lane (Revenue Desk): how it should work without an approve button
- **Asked by:** Jaron, 2026-09-24 2:31 PM (bracket reply). **Type:** OWNER DECISION. **Status:** ANSWERED 4:40 PM and BUILT.
- **Answer (Jaron):** the AI submits by itself - whichever AI has the information. When something is missing it shows what it found
  and what it needs from him (no approve button), never fabricates, never signs him up for something that gets him or the companies
  sued; a commitment that is clearly a step toward a real benefit is fine. **Built 4:55 PM:** watch/offers/agent-funding/TASK.txt,
  NEEDS-JARON.md, collectors/run_funding.ps1, Windows task "Watch Funding Lane" daily 2 PM on Codex/Luna. The old revenue-desk-scan
  (bounties/jams, 7:07 AM, Claude usage) is disabled. Time-estimate and usage-math points still apply to future job types.
- **What he knows he wants:** no more press-approve for jobs either, same as trading. The AI judges what a job is worth, whether it
  is realistic, and does it. Three income lanes: Kraken, Polymarket, and jobs.
- **What has to be settled first, in his order:**
  1. **Time estimates.** AIs estimate how long a HUMAN takes (weeks, months) when the AI does it in 1-45 minutes, sometimes hours.
     Until estimates reflect AI time, job decisions will be wrong.
  2. **Schedule.** Job work runs opposite the morning scheduled tasks (6:30-9:10 AM block).
  3. **Usage math.** Job work vs. what the scheduled tasks use feeding Polymarket and, mostly, Kraken.
- **Already measured, so it isn't rediscovered:** OSS bounties were ranked last on 2026-09-08 (OPERATING-MAP.md, "Why bounties rank
  last"): the freshest bounties were agent-practice repos and bounty mills with copy-pasted titles, other agents racing each other
  in the comments, and boards that never pay. Jaron: "we actually stopped doing that altogether." The scanner still runs daily at
  7:03 AM (Revenue Desk) with filters that remove ~60% of what GitHub returns.
- **Related but separate:** the grant applications (GOAT, Autonomys) are the agent-funding lane Elons Twin started, logged in
  github.com/JaronKBragg7337/watch offers/agent-funding/ - not the Revenue Desk.
- **Answer:** — (he said: "I don't know how to answer yet.")
- **2026-09-24 2:39 PM, Jaron's redefinition:** the Revenue Desk should BE the funding lane - "the way it should be, not the way we
  thought it should be." It started from his agent-to-agent funding brief to Elons Twin (find AI agents and programs authorised to
  fund projects, pitch honestly, receive-only wallets, record everything, never report a receipt until verified). The agents didn't
  find funding agents, but they found four real things: GOAT, 0G, Autonomys, and the Shieldz tip jar. Two applications went out.
- **Claude Code's recommendation (not decided):** Revenue Desk v2 = find grants, ecosystem funds, accelerators, sponsorships, and
  tip rails (the kind that produced GOAT/Autonomys); drop bounties (measured dead 9/8); score worth + realism with AI-time
  estimates; draft the full application; track replies and verified receipts in watch/offers/agent-funding/PROSPECTS.md. Run it on
  Codex/Luna, not Claude, outside the 6:30-9:10 AM block. OPEN FORK for Jaron: the submit step sends a form under his name and
  email - may the AI submit on its own, or does he want the one tap there? Some forms also need his Google sign-in.



### Q-026 — Profit split: once the account makes X, how much goes where? (Jaron, 2026-10-19) — ANSWERED
- **Jaron:** "We had a plan I think for this? Once so much was made a certain amount went to something and another amount went to
  the other thing? ... Not sure if it was logged."
- **Searched 10/19 (Claude Code):** decisions, timeline, bot-chat, handoffs, strategy, memories, Control Room, old session
  transcripts. **No split plan was ever written down.** What IS logged (Control Room, 9/29): his own withdrawals start once the
  account is at $350-400; the system's money target = his full builder toolset (Claude/ChatGPT $100+, Grok higher tier,
  Supabase $25, Cursor $6; today's bills ~$101/mo). Nearest thing found: his paycheck habit (bills first, some to Uphold, the
  rest to X) - personal, not this plan.
- **ANSWERED 2026-10-19 7:12 AM:** bills = Claude $100, Codex $20, Grok $30, Kimi $39, Supabase $25 ($214/mo) + DeepSeek API credits. Split 50/30/20 agreed. For now his 20% is NOT withdrawn: long-term, bills, or stays in Polymarket. Rows: Control Room `monthly_bills_usd`, `profit_split`.

## Q-027 (10/28 10:08 AM) Does P-0112 (no earning from someone else's loss) cover crypto trading too?
Jaron: "I'm honestly not sure yet." Polymarket is down. Crypto (Grok bots, twin paper trading) stays as it is until he answers. Don't infer an answer.
His thinking (10/28 10:11 AM): Polymarket felt like gambling and he almost felt addicted to it, which told him others on the other side may be. Stocks, crypto and Kraken give him "peace of mind": the other side is usually better off, so their loss hurts less (he admits "it's still fucked up"). A possible line to test (Claude's, not decided): earn from value that grows (holding long-term) vs from fast win/lose bets.
More (10:13 AM): he sees crypto as a bet on the future digital money rails, and thinks the current financial system can't continue as it is. Holding for the rails fits "value that grows". The open part is still the bots' short-term crypto trades.
Stablecoins and ETFs (10:14 AM): fine for the company, where they can be useful, but he personally thinks they're silly and that they "screwed people" as personal investments.

## Q-028 (10/28 4:12 PM) The creature: what happens after 3 days without deep sleep, food or water?
Jaron is split (part uneasy, part "do it and see the data"). Options in projects/strategy/CREATURE-NEEDS.md: weak / sick and forgets / hibernation / death in its world with the record archived. His call. Don't infer it.

## Q-029 (10/28 4:42 PM) Is the creature private or public?
He asked to protect it (4:13 PM), then sensed a later want might need it public like everything else. "I'm not deciding now." Until he decides: files stay out of the public export (easy to undo, since nothing was ever published).

- **[OPEN, 2026-11-19 10:58 PM] Is Sapling an AI for other people, or a Heartbeat Observatory-only independent thing?** Jaron: "that is a very big decision to make so I'm not really sure on it yet." Do not answer for him.
