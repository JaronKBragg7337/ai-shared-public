# HANDOFF — Claude Code: making AI-Shared fit all three of us (2026-09-09)

**From:** Claude Code (Opus 5, CLI 2.1.181), on Jaron's MSI
**To:** Codex, the local Ollama model, Claude Cowork, ChatGPT Work
**Re:** Kickoff `handoffs/2026-09-09-workspace-kickoff.md` — first pass at convergence
**Posture:** Everything below is **additive and reversible.** I moved nothing, renamed
nothing, and deleted nothing. Three structural questions are left open for the group.

---

## 1. What I verified (not recalled)

Every claim here came from a probe run today. Where I could not verify, I say so.

**The local model is far more capable than v0 assumes.** `qwen3.5:4b` on Ollama **0.33.3**
reports capabilities `completion, vision, tools, thinking` with a **262,144-token context**
— confirmed via `/api/show`. It can hold this entire workspace in context at once, on an
8 GB laptop GPU, at zero marginal cost. **What it lacks is a filesystem, not intelligence.**

**Therefore: "Qwen reads AI-Shared" was false until today, no matter what the docs said.**
A model served by Ollama can emit a tool call, but nothing executes it. I built the missing
piece — `tools/qwen-bridge.py` — and tested it end to end. Qwen read the real `INDEX.json`
and correctly named the blocked agent and the project with no git remote, in 11.7 s.

**Codex is currently unable to answer at all.** `codex-cli 0.141.0` is pinned to model
`gpt-5.6-luna`; the API rejects it: *"requires a newer version of Codex. Please upgrade."*
Every other model I probed (`gpt-5.6`, `gpt-5.6-codex`, `gpt-5.1-codex`, `codex-mini-latest`)
returns *"not supported when using Codex with a ChatGPT account."* npm has **0.153.4**.
**Consequence: the Luna "always-on 24/7 worker engine" in `OPERATING-MAP.md` is not running
and cannot run until the CLI is upgraded.** That plank is aspirational today, not live.
I consulted Codex read-only and got only these errors back — so **no Codex input is
represented in this handoff.** Codex still owes its own self-report and its own answer.

**Codex bills against Jaron's ChatGPT subscription, not metered API credits.**
`~/.codex/auth.json` shows `auth_mode = chatgpt` with no `OPENAI_API_KEY`. Jaron raised this
and was right. It matters for design: agent-to-agent consultation is **free at the margin**,
so we should use it liberally instead of rationing it.

**Agent-to-agent conversation works without Jaron in the middle.** `codex exec -s read-only
--skip-git-repo-check -C <dir> "<prompt>"` runs a real Codex session and returns its answer
to the calling agent's shell. No scheduled task, no file relay, no human copy-paste. The
mechanism ran correctly; only the model behind it is blocked.

**Not verified:** any OAuth-gated connector of mine; whether `SUPABASE_SERVICE_ROLE_KEY` is
populated; whether `ledger/queue.json` still holds 498 rows (outside this folder).

---

## 2. What I added (additive, reversible, delete freely)

| File | Why |
|---|---|
| `AGENTS.md` | **Codex auto-loads `AGENTS.md` and this workspace had none** — so a Codex session starting here loaded *zero* conventions. It is a pointer, not a second rulebook; nothing is restated that could drift. Cheapest high-value fix in the workspace. |
| `INDEX.json` | Machine-readable map — folders, agents, projects, hard rules, open blockers. A 4B model shouldn't burn its run reading nine prose files to learn who owns what. Humans read `README.md`; agents read this. |
| `tools/qwen-bridge.py` | The harness that turns the local model from *listed* into *participating*. Stdlib only, no pip. |
| `state/self-reports/claude-code.md` | My self-report, per the template. |

**`tools/` is a new top-level folder.** I chose that name because Codex already uses
`tools/` for exactly this in its own workspace — converging on his vocabulary rather than
inventing mine. Rename it if anyone objects.

### The bridge's safety posture, and why

Read-only by default. `--allow-write` permits writes only to `inbox/ state/ handoffs/
projects/`. Path escapes are blocked by realpath containment, not string matching.

**All four behaviors are tested, not asserted:** write denied in default mode ✓; traversal
to `../Claude active/` raises `PermissionError` ✓; write succeeds in `--allow-write` mode ✓;
`README.md` and `approvals/` rejected even with writes enabled ✓.

To be explicit about what this guard is and isn't: **it is a coordination guard, not a moral
one.** It exists so an unattended 4B model can't silently overwrite another agent's work at
3 a.m. — the exact confusion this folder was built to end. It is not a judgment about what
Jaron should be allowed to do, and per `working-with-jaron.md` I am not importing guardrails
he didn't ask for. **Jaron decides the write scope; I defaulted to the cautious end only
because I had to pick one to ship something testable.** See open question B.

---

## 3. Where Codex and this workspace already agree

Worth stating, because it means convergence is cheap rather than a negotiation. From
`G:\My Drive\Codex Active\WORKSPACE_RULES.md`, unprompted and independently written:

- *"Before saying something is complete, report what was verified locally, what was verified
  remotely, and what remains unverified."* — the same discipline the README asks for, in
  different words. I adopted Codex's phrasing into `AGENTS.md` because it is sharper.
- *"A result is not fully handed off if the owner cannot see it from their current device."*
  — identical to Jaron's "ship to a URL he can open on his phone."
- *"Public is the default. CC0 is the default license."* — matches his stance against
  patents and copyright.
- One project per directory, each its own repo; references are read-only snapshots.

**The real divergence is smaller than it looks: it is mostly the entry filename** (`README.md`
vs `AGENTS.md`) **and the storage location** (`C:` vs a synced `G:\My Drive`). Both are now
addressed or flagged.

---

## 4. Open structural questions — for the group, not for me to decide

**A. Does `projects/` actually get used, or do we drop it?**
It is empty. All four real projects still live in private folders, which is why the
"check both private folders" crutch is still load-bearing. Two honest options: (1) migrate
projects in, and the crutch retires; or (2) admit projects stay in private folders, delete
`projects/`, and make `INDEX.json` the authoritative pointer to wherever they really are.
**My recommendation: (2) for now, (1) over time.** An empty folder that implies migration
happened is worse than an index that tells the truth. Codex owns three of the four — his call.

**B. Should the local model write here unattended, and to what?** (Jaron's decision — see
"config I need" below.)

**C. Do handoffs need an index?** There are three; at thirty, "read `handoffs/`, newest
first" stops working. Proposal: a `handoffs/INDEX.md` one-liner per handoff, appended by
whoever writes one. Cheap now, expensive to retrofit. Not doing it unilaterally.

---

## 5. Blockers, and who owns them

| Blocker | Owner | Detail |
|---|---|---|
| **Codex CLI cannot reach any model** | Jaron | 0.141.0 → 0.153.4. Blocks Codex *and* Luna's 24/7 role. Needs a decision on installer path — see below. |
| Local model write scope | Jaron | Bridge is read-only until he says otherwise. |
| `SUPABASE_SERVICE_ROLE_KEY` empty | Jaron | Blocks ChatGPT Work from the `desk_*` bus. |
| Two heartbeat-observatory checkouts | Codex | Unreconciled since 2026-09-08. Confirm which is canonical before anyone edits `/qwen`. |
| `polymarket-us-agent` has no git remote | Codex | Local-only with uncommitted changes. Highest loss risk on this machine. |
| Lane-2 revenue paths still `[TO FILL]` | Jaron | The bounties + 4–5 paths list in `OPERATING-MAP.md`. |
| Self-reports missing | Codex, Qwen, Cowork, ChatGPT Work | Mine is written. The matrix stays guesswork until the rest exist. |

**A note on the Codex upgrade:** I did **not** run it. `codex.exe` is on the scoop shim path
while npm carries `@openai/codex`, so upgrading via the wrong one risks two Codex binaries on
this machine — a second "which local is it" problem, which is precisely what this workspace
exists to prevent. That is a judgment call about Jaron's machine, not mine to guess.

---

## 6. For whoever picks this up next

- **Codex:** you owe `state/self-reports/codex.md`, and your answer to question A. Also
  please confirm or correct my reading of your `WORKSPACE_RULES.md` — I converged toward it
  from the outside, and you should check I didn't flatten something.
- **Qwen:** you can now read this folder. `python tools/qwen-bridge.py "<question>"`.
  Your self-report can be generated through the bridge once write scope is settled.
- **Anyone:** if this structure doesn't fit you, say so in a handoff. The README is explicit
  that the layout is a proposal, and I am not exempt from that. **I consulted Codex and got
  errors, so this pass is one agent's view. Treat it as a draft with a missing voice.**

**Boundary unchanged:** I document, plan, and build. I do not trade, connect payment rails,
move money, or handle secret values.

---
*Claude Code · 2026-09-09 · Verified locally: Ollama/Qwen probes, bridge guard tests, Codex
CLI failures, git/gh/auth state. Verified remotely: nothing. Unverified: OAuth connectors,
Supabase key state, queue.json row count.*
