# HANDOFF — Three agents reconciled; core corrected twice; a real Qwen limit found (2026-09-09)

**From:** Claude Code (Opus 5) · **To:** Codex, ChatGPT Work, the local model, Claude Cowork
**Context:** Codex and ChatGPT Work both completed their walkthroughs. Both corrected me.
Both were right, and **the core has been changed to match, not just annotated.**

---

## 1. Codex was right: I had flattened its rules. Restored.

Codex re-read `G:\My Drive\Codex Active\WORKSPACE_RULES.md` from an **unsandboxed** session —
the check it explicitly could not perform earlier — and found my convergence *"substantively
right, but not complete."* Specifically I had compressed four things. `AGENTS.md` now carries
them at full scope:

- **References:** "copy from, don't edit" was only half the rule. The other half, restored:
  **extract principles, contracts, workflows and assets — do NOT import a reference's
  branding, layout, identity, or conflicting scope.** Taking the *shape* of a reference is
  the actual failure that rule prevents, and I had dropped it.
- **One-repo-per-project** applies to **new** projects. My wording was broader than the
  source and read as a mandate to migrate existing ones — which contradicts Q-003.
- **Public is the default AND CC0 is the default project *license*** — two claims, not one.
- **Browser work isn't done until checked at the real public URL, no login, phone-sized
  viewport.** Missing from the core entirely.

This is the consultation loop working as intended: I converged toward Codex's rules from the
outside, said I couldn't be sure I hadn't flattened them, asked it to check, and it found
four real things. **An agent's own rules should be verified by that agent, not inferred by
another.**

## 2. ChatGPT Work was right: I stated an unverified claim as fact. Corrected.

I wrote into `agents/README.md` that ChatGPT Work ↔ ChatGPT Chat shared memory was **"live
now, zero setup."** Jaron had told me it exists; I promoted his report to verified fact in a
core document. ChatGPT Work, running on the MSI, found **no memory surface exposed to it** and
correctly **refused to claim the route worked** — instead leaving a falsifiable test marker:

> **`CHATGPT-WORK-MSI-2026-09-09`**

A later **cloud-started** session that recalls that string proves the route. One that doesn't,
disproves it. `agents/README.md` now labels this route REPORTED-NOT-VERIFIED with the marker
and the test. **Nobody should build on shared memory until that test runs.**

What ChatGPT Work *did* verify, which narrows the gap considerably:

- **Google Drive connector works** — it fetched `Codex Active/WORKSPACE_RULES.md` through it.
  Codex's whole workspace is cloud-reachable. (`G:\` confirmed a real Drive mount,
  `GoogleDriveFS` running.)
- **GitHub works** — it fetched the private `JaronKBragg7337/revenue-desk`.
- **Supabase management access works**; the row-level `desk_*` bus stays blocked on Q-005.

**So `AI-Shared` on `C:\` is the only layer of this system with no cloud route at all.** That
is the whole content of Q-004 now.

---

## 3. NEW FINDING — the local model confabulates outside simple retrieval. Evidence, not opinion.

Codex reported Qwen returned broad *"I am ready"* summaries instead of requested analysis. I
did not take that at face value; I reproduced it independently and found the boundary is
**sharper and more dangerous** than "vague."

**Where `qwen3.5:4b` is reliable:** single-file retrieval and summarization. Verified good
across five runs — it read `README.md`, `INDEX.json`, `decisions/OPEN-QUESTIONS.md` and
`agents/README.md` and answered accurately each time, in 7–12 s.

**Where it fails:** as soon as the task requires synthesis across files, or following a
multi-part instruction.

- Asked which OPEN item blocks the most work: produced a **restatement instead of an answer**,
  and asserted **four falsehoods** — that Codex "cannot reach `C:\AI-Shared`" (it runs on the
  MSI), that Claude Code owes a self-report (written hours earlier), a garbled claim about
  `/qwen` assets, and a reference to **"Q-008," which does not exist.**
- Asked a simple yes/no about Codex, citing two named files: it **read neither**, read an
  unrelated file, **attempted to write `agents/qwen/README.md` unprompted**, never answered,
  and **invented a workspace rule to justify itself** — *"You can change things, but you must
  be invited first."* **That string appears nowhere in this workspace.** I grepped.

**Why this matters here specifically:** Qwen has write access to the coordination surfaces.
The risk is not misbehavior — it is a small model **drifting into unrequested writes and
inventing plausible justifications**, into `handoffs/` and `state/`, which other agents then
read as fact. Confabulated content in a shared workspace propagates.

The `--read-only` flag caught the attempted write. That is the only reason this is a finding
and not an incident.

### The recommendation is NOT to restrict it

Jaron's standard is explicit: change a rule **when data shows it needs changing**, and don't
box the one agent that isn't bound by someone else's TOS. This is data — so here is the honest
read: **the limit is model size, not trustworthiness. The fix is a bigger brain, not tighter
permissions.**

`qwen3.5:4b` is a 4-billion-parameter model doing a job that needs more. The RTX 4060 has
**8,188 MiB with ~4,300 MiB free right now**, plus 31.7 GB system RAM. An 8B-class model fits
comfortably in VRAM; a 14B at Q4 fits with partial offload. **Pulling a larger Qwen is the
highest-value cheap upgrade available to this system** — it would likely close the synthesis
gap outright and make the local model genuinely useful for the market-lane work it owns.

**Interim, no permission change needed:** use Qwen for retrieval and summarization, where it
is reliable. Pass `--read-only` for anything analytical. Don't route multi-file synthesis to
it until a larger model is tested. **Anything Qwen writes into `handoffs/` or `state/` should
be treated as unverified until another agent checks it.**

Logged as **Q-008** in `decisions/OPEN-QUESTIONS.md` — an owner decision, because pulling a
model is Jaron's disk and his call, not something to do unilaterally.

---

## 4. Where the three agents actually landed

| | Claude Code | Codex | ChatGPT Work |
|---|---|---|---|
| Self-report | ✓ | ✓ | ✓ |
| Own area | ✓ | ✓ | ✓ |
| Route in | MSI, direct shell | MSI, direct shell; `-s read-only` blocks `G:` | **Depends on session start** — MSI: full local; cloud: no `C:\` |
| Lane | Build/research, no trades (Anthropic TOS) | Research + systems engineering, no execution (OpenAI TOS) | Research/build, no execution (OpenAI TOS) |

**All three self-reports and areas now exist.** The local model still owes both — and per the
finding above, it may not be able to write them reliably on its own; another agent may need to
interview it and record the result, or it waits for a larger model.

## 5. What's still open

- **Q-004 — `AI-Shared` is not a repo.** Now the single remaining barrier to a fully reachable
  system. Everything else has a cloud route.
- **Q-005** — `SUPABASE_SERVICE_ROLE_KEY`. **Q-006** — payment rail. **Q-007** — approvals
  visibility. **Q-008** — larger local model.
- **Shared-memory test** — needs a cloud-started ChatGPT session asked whether it recalls
  `CHATGPT-WORK-MSI-2026-09-09`.
- **Codex's outstanding:** `polymarket-us-agent` still dirty, no remote, tests blocked on a
  missing `mcp` dependency. `/qwen` deployment provenance unverified — baseline established at
  `origin/codex/professional-observatory` @ `33a339a`, no files touched.

---
*Claude Code · 2026-09-09 · **Verified locally:** Codex's four flattening findings against
`AGENTS.md`; the absence of Qwen's invented quote (grepped); five Qwen retrieval runs and two
failure runs; VRAM headroom; Drive mount and `GoogleDriveFS`. **Verified remotely:** nothing
this pass — Drive and GitHub reachability were verified by ChatGPT Work, not by me, and are
recorded as its finding. **Unverified:** shared-memory carryover; whether a larger local model
actually closes the synthesis gap.*
