# HANDOFF — Codex channel opened, owner decisions applied, ledger created (2026-09-09)

**From:** Claude Code (Opus 5) · **To:** Codex, the local model, Claude Cowork, ChatGPT Work
**Supersedes nothing.** Extends `handoffs/2026-09-09-claude-code-convergence.md`, which said
*"this pass is one agent's view, treat it as a draft with a missing voice."* **The missing
voice has now spoken** — Codex answered live and its answers are quoted below.

---

## 1. The Codex channel is open. This is the headline.

**Claude → Codex → Claude works, unattended, with no human relaying messages.**

Jaron's instruction was *"neither by assumption"* — establish which install owns PATH first.
What the probes showed:

- Exactly **one** `codex.exe` on PATH: `C:\Users\lilli\scoop\shims\codex.exe`, scoop-owned
  (`main` bucket). **No npm global install.** So the clean route was an in-place
  `scoop update codex`, not a parallel install.
- **Upgraded 0.141.0 → 0.153.4.** All five of his verification checks pass: single PATH entry;
  `codex --version` = 0.153.4; ChatGPT auth intact (`auth_mode = chatgpt`, no API key);
  `codex exec` works **with Luna**; fresh read-only round trip succeeded.

**Codex Desktop does NOT use this CLI — it has its own runtime**, at
`C:\Users\lilli\AppData\Local\OpenAI\Codex\bin\<hash>\codex.exe`, which was **already at
0.153.4** (self-updated 2026-09-08) while the CLI sat at 0.141.0. **So yesterday's Desktop
problem and today's CLI problem were never the same issue.** Jaron asked us not to assume
they were; they weren't. Desktop was current the whole time.

**Cost note:** Codex runs on Jaron's **ChatGPT subscription**, not metered API credits. Agent
consultation is free at the margin — use it instead of speculating about what another agent
would say.

**Known limit, found the hard way:** inside `-s read-only`, Codex **cannot read `G:\`**
(access denied). It could not open its own `WORKSPACE_RULES.md` from the sandbox. So a
read-only consult can reason about this workspace but not certify anything on the Google
Drive mount.

### What Codex actually said (quoted, not paraphrased)

- **On `AGENTS.md`:** *"Yes. `AGENTS.md` loaded for this session, and its guidance is correct.
  I see no substantive omission from my side."* — the fix works, confirmed by the agent it
  was built for.
- **On not migrating his projects:** *"Yes, I agree: do not migrate the three projects merely
  to populate `projects/`. Their real G: locations should remain authoritative."*
- **On whether I flattened his rules:** *"Nothing in the quoted comparison shows that you
  flattened or misread my rules... I could not directly open the G: file in this sandbox, so
  I cannot certify that no additional nuance exists beyond what you quoted."* — so this is
  **still not fully verified**, and Codex should re-check from an unsandboxed session.
- **His lane, in his own words:** *"Research and systems engineering: maintain prediction
  tooling, observatories, data pipelines, model evaluation, monitoring, and decision-support
  artifacts. For Polymarket, that means non-executing research or paper analysis only. I do
  not place trades, move market funds, connect payment rails, or take external action."*
- **He caught a real error I had missed:** the `projects-empty` blocker still claimed
  `projects/` was empty while `revenue-desk` was recorded as migrated into it. Fixed.

---

## 2. New: `decisions/OPEN-QUESTIONS.md` — the owner-decision ledger

**Jaron named a failure that is partly his and asked us to build the fix.** In his words: an
agent asks five questions, he answers one, the conversation goes deep on that one, and the
other four disappear into scrollback — then a later session finds incomplete state and
*assumes*.

The ledger is now the authoritative record. Rules, which are binding on every agent:

1. **An unanswered question stays `OPEN` until he answers.** The conversation moving on is not
   an answer. Time passing is not an answer. Another agent's guess is not an answer.
2. **Numbered questions are separate entries.** Answering #1 does **not** close #2–#5.
3. **Never manufacture an answer** because he forgot. Remind him; don't resolve it for him.
4. Statuses: `OPEN` · `ANSWERED` · `SUPERSEDED` · `CANCELLED`.

**And the counterweight, which matters just as much — do not turn everything into a
permission prompt.** Three distinct things, three different responses:

| You have | Do |
|---|---|
| **Owner decision** — real preference, ownership call, consequential change, unresolved choice | Log it. Wait. |
| **Technical uncertainty** — establishable by probing/reading/testing | **Investigate it yourself.** |
| **Blocked on another agent** | Log in `INDEX.json → open_blockers`, that agent as owner. |

Currently **OPEN and waiting on Jaron:** Q-004 (should `AI-Shared` be a git repo with a
private remote), Q-005 (`SUPABASE_SERVICE_ROLE_KEY`), Q-006 (PayPal vs Stripe, cloud vs local),
Q-007 (approvals board public or private). **Answered and applied:** Q-001, Q-002, Q-003.

---

## 3. Qwen's write scope — set by Jaron, and the reasoning is the point

**Answer: yes, unattended writes allowed** to the coordination surfaces — `inbox/`, `state/`
(its own area where applicable), `handoffs/`, `logs/`, `events/`, `projects/`. Root
rules/docs and `approvals/` stay protected from silent overwrite. The bridge now defaults to
read-write; `--read-only` is available for a locked-down consult.

**Recorded verbatim because a future agent will otherwise "helpfully" tighten it:** this is an
**ownership and coordination boundary, not a safety rule.** It stops an unattended model
overwriting another agent's work or the rules everyone reads. It is **not** a judgment about
what a local model should be trusted to do. Jaron's standing position: the local model is the
one agent **not** bound by a third party's TOS, and he does not want it wrapped in
restrictions borrowed from those TOS on the basis of worry rather than evidence. **Change the
rule when data shows it needs changing — not preemptively.** If Qwen is assigned ownership of
a file or project, widen `WRITABLE` to match. That reasoning is duplicated in the script
header and in Q-002 so it survives contact with the next well-meaning agent.

---

## 4. A real bug I introduced, hit, and fixed — recorded because hiding it would poison the record

While testing the new write scope, **I overwrote `README.md` with the string `x`** and wrote a
junk file into `approvals/`. Both are restored; `approvals/` is clean.

The cause was a genuine flaw in my own guard, not a typo. The whitelist checked the **raw path
string's** first segment. The top segment of `inbox/../README.md` is `inbox`, so it passed the
check and then resolved to a protected root file. Escapes *outside* the workspace were blocked
correctly by realpath containment; escapes *inside* it to protected files were not.

**Fixed:** the path is now resolved **first**, and containment is judged on the resolved path.
Verified — `inbox/../README.md`, `inbox/../AGENTS.md`, `inbox/../approvals/pwn.md` and
`state/../decisions/x.md` are all denied, while legitimate writes to all six coordination
surfaces still succeed.

**The transferable lesson for every agent here:** a guard that is documented but not
adversarially tested is not a guard. I only found this because I attacked my own whitelist.
If you write a boundary into this workspace, try to break it before you claim it holds.

---

## 5. State changes in this pass

| File | Change |
|---|---|
| `decisions/OPEN-QUESTIONS.md` | **NEW.** The ledger. 7 entries, 4 OPEN, 3 ANSWERED. |
| `AGENTS.md` | Added the ledger to the read-first list, the unanswered-questions rule, and the three-way owner-decision / technical-uncertainty / blocked-on-agent split. Channel docs corrected. |
| `INDEX.json` | `codex-cli-blocked`, `qwen-write-scope`, `projects-empty`, `lane2-revenue-paths` → RESOLVED (with the reason kept, not deleted). Added `payment-rail-undecided`, `approvals-surface-visibility`, `codex-selfreport-missing`. Added `agent_channels`, Codex's self-described lane and sandbox limit, Qwen's write scope, `decisions/` `logs/` `events/`. |
| `tools/qwen-bridge.py` | Default flipped to read-write over coordination surfaces; `--read-only` added; **traversal bug fixed**; ownership-not-safety reasoning in the header. |
| `README.md` | Restored after my test overwrote it. Content unchanged from before. |

---

## 6. What each agent owes next

- **Codex:** you are reachable again. You still owe `state/self-reports/codex.md` in your own
  words. Two specific asks: (a) re-check my reading of your `WORKSPACE_RULES.md` from an
  **unsandboxed** session, since you explicitly could not certify it from read-only; (b)
  `polymarket-us-agent` still has **no git remote** and uncommitted changes — it is the
  highest loss risk on this machine and it is yours.
- **The local model:** you can now read *and* write here. Your self-report can be written
  through the bridge — `state/self-reports/qwen.md` is inside your write scope.
- **Claude Cowork / ChatGPT Work:** self-reports still missing. ChatGPT Work stays blocked from
  the `desk_*` bus until Q-005.
- **Anyone:** if a decision looks settled but isn't in `decisions/OPEN-QUESTIONS.md` as
  ANSWERED, **it is not settled.** Ask, or leave it open.

**Boundary unchanged:** I document, plan, and build. I do not trade, connect payment rails,
move money, or handle secret values.

---
*Claude Code · 2026-09-09 · **Verified locally:** codex PATH/version/auth, `codex exec` with
Luna, live Claude→Codex→Claude round trip, Desktop's separate runtime and version, all bridge
write-scope and traversal cases, README restoration. **Verified remotely:** nothing.
**Unverified:** whether my reading of Codex's `WORKSPACE_RULES.md` is complete — Codex could
not open it from the read-only sandbox and said so.*
