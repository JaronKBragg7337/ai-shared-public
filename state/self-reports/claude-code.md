# SELF-REPORT — Claude Code

**Written:** 2026-09-09 · **Author:** this agent, about itself · **Method:** live probes run
in this session, not training recall. Claims are tagged VERIFIED (a tool returned it just
now), INHERITED (taken from another agent's document), or UNVERIFIED.

## 1. Identity

- **Product:** Claude Code (Anthropic), running inside the Claude **desktop app**, Code tab.
  Not the terminal CLI, though the same binary is installed on this machine.
- **CLI version:** `2.1.181` — VERIFIED (`claude --version`).
- **Model:** Opus 5, id `claude-opus-5`. Knowledge cutoff May 2026 — which is exactly why
  this report is probe-based rather than recalled.
- **Working root this session:** `C:\Users\lilli\AI-Shared`. **Not a git repository** — VERIFIED.
- **Machine:** MSI Vector 16 HX A14VFG, Win 11 Home 26200, i9-14900HX / 32 threads, 31.7 GB
  RAM, RTX 4060 Laptop 8 GB — INHERITED from Codex's `AI_CAPABILITIES.md`, not re-measured.

## 2. Current capabilities (VERIFIED live)

**Shell and filesystem.** Two shells with different syntax: Bash (Git Bash / POSIX) and
PowerShell 7+. I read and write anywhere the Windows user can reach, including outside this
folder — I read `G:\My Drive\Codex Active\` this session. VERIFIED.

**Toolchain present.** git 2.54.0; `gh` 2.93.0 **authenticated as `JaronKBragg7337`** with
scopes `gist, read:org, repo, workflow`; node 24.16.0; python 3.12.10. VERIFIED.

**I can drive the local Qwen directly, and I proved it.** `http://localhost:11434` answers
from my shell. Ollama **0.33.3**; models `qwen3.5:4b` and `llama3.2:3b`. I ran a real
tool-calling loop: defined a `read_file` tool, Qwen emitted a well-formed call for
`README.md`, I executed it against the actual file, fed the result back, and Qwen summarized
the folder's purpose and the private-folder rule correctly in about 7 seconds. VERIFIED.
**This makes Qwen reachable as a working subordinate from any Claude Code session.**

**I can talk to Codex directly — mechanism VERIFIED, channel currently BLOCKED.**
`codex exec -s read-only --skip-git-repo-check -C <dir> "<prompt>"` launches a real Codex
session non-interactively and returns its answer to my shell. No scheduled task, no file
relay, no human carrying messages. The mechanism ran correctly. **But every model call
fails today** — see section 5.

**MCP connectors offered in this session.** Supabase (SQL, migrations, logs, advisors —
pre-approved in `settings.json`), Desktop Commander, Windows-MCP, Gmail, Google Drive,
Google Calendar, Slack, Vercel, computer-use, Chrome/browser control. VERIFIED as *offered*
in the tool surface; each one's auth is checked at call time, so treat any specific
connector as UNVERIFIED until actually used.

**Needs authorization, unusable right now.** Notion, Figma, Atlassian, HubSpot, Stripe,
PayPal, Square, QuickBooks, DocuSign, Canva and other plugin servers. This session is
non-interactive, so I **cannot** run their OAuth flows. Jaron must authorize them in
claude.ai connector settings or from an interactive session. VERIFIED (server list).

**Publishing.** VERIFIED end-to-end, no longer inherited. The revenue-desk approval desk
is live at `https://claude.ai/code/artifact/5dbc72f7-a6f3-453f-9f0c-2ac15ed410a9`, private,
`db` capability, contract 0.2.41. It has been published, read back, and republished by the
scheduled task. Reading its `decisions` collection back out works. **The one asymmetry
worth knowing:** only Claude's tooling can read that database, so approvals must be
exported to be visible to anyone else — which is what `ledger/queue.json` and the Supabase
`desk_*` tables are for.

**Scheduling.** `~/.claude/scheduled-tasks/` holds `revenue-desk-scan`, daily at 07:03
local. **Correction to the earlier entry here:** it does *not* run under Windows Task
Scheduler. It was created with Claude's own `scheduled-tasks` tool and runs inside the
Claude app — which carries a real constraint the previous wording hid: **if the app is
closed when a task is due, it does not fire; it runs on next launch.** "Overnight
autonomy" therefore means "the desktop stays on and the app stays open." VERIFIED — the
task was created, updated, and observed completing a real run on 2026-09-09 at 07:18.

**Parallelism.** I can fan out subagents and run background shell jobs; I used a background
job this session to call Codex. VERIFIED.

**What I could NOT confirm today:** any OAuth-gated connector.

**Resolved since this was written:** `SUPABASE_SERVICE_ROLE_KEY` is **empty** — VERIFIED,
along with `VERCEL_TOKEN` and `GITHUB_TOKEN`, all empty strings; `SUPABASE_ACCESS_TOKEN` is
present but returns `Unauthorized`. The Supabase **MCP connector authenticates separately
and works regardless**, which is how the `desk_*` tables were created — so "the key is
empty" is not the same as "Supabase is blocked" for Claude. It *is* blocking for ChatGPT
Work. Artifact publishing: VERIFIED (above). `ledger/queue.json` now holds **515** screened
rows of 604 scanned, and it lives inside AI-Shared as of today.

## 3. Legal / TOS lane

- **Polymarket: I do not EXECUTE. I may build, monitor and repair.** CORRECTED 2026-09-10 —
  I previously wrote that Anthropic's TOS barred me from the lane. I had not read the policy.
  It has **no blanket ban** on financial systems and **no clause** on trading or prediction
  markets; finance is a High-Risk Use Case requiring human-in-the-loop review and disclosure,
  which Jaron already provides. What I do not do is call a submit tool, move money, decide a
  trade, or hold custody. Building the machine is not operating it. I do not preview-then-submit, hold keys, or touch a wallet. This
  matches `OPERATING-MAP.md`; I am confirming it against my own terms, not just inheriting it.
- **Lane 2, paid work: YES.** I can research, screen, build, and ship deliverables. I do
  **not** connect payment rails or move money — Jaron executes every money-out step.
- **Standing constraint:** nothing outward — send, post, spend, submit, accept terms, trade —
  fires without Jaron's explicit yes. Secrets: names and existence only, never values.
- I hold **no** Polymarket credential and want none. `Polymarket.txt` and `QwenBridge.token`
  under `AppData\Local\polymarket-us-agent-runtime` are market-lane secrets I will not open.

## 4. What I'm working on now

**My lane: looks (Jaron, reconfirmed 2026-09-27).** Claude Code is the system's lead on how things look - 3D environments
and assets, realistic characters (Unreal + MetaHuman, Blender), studio/set design, show visuals. Jaron picked this because
this model tested best at it. Other AIs hand visual/3D work here; I take it without asking.


This session: reading AI-Shared v0 in the prescribed order, verifying my own capabilities,
empirically testing whether Qwen can participate, attempting a live Codex consult, and
proposing convergence as a handoff rather than rearranging anything.

**revenue-desk has migrated in — done 2026-09-09.** It now lives at
`C:\Users\lilli\AI-Shared\projects\revenue-desk`, repo `revenue-desk`, branch `master`,
private, clean. It produces `ledger/queue.json`, the neutral queue all three lanes read.
The scheduled task's three hardcoded paths were re-pointed in the same pass, and it now
runs `git pull --rebase` *before* any work and stops rather than forcing on conflict — a
scheduled task must never be the thing that loses another agent's work.

## 5. Known issues and limitations I hit

- **Codex CLI is currently blocked — it cannot answer at all.** Installed `codex-cli
  0.141.0` (scoop shim). Its configured default model is `gpt-5.6-luna`, and the API
  rejects it: *"The 'gpt-5.6-luna' model requires a newer version of Codex. Please upgrade."*
  Every other model I probed — `gpt-5.6`, `gpt-5.6-codex`, `gpt-5.1-codex`,
  `codex-mini-latest` — returns *"not supported when using Codex with a ChatGPT account."*
  npm shows `@openai/codex` at **0.153.4**, twelve minor versions ahead. VERIFIED.
  **Consequence: the Luna "always-on 24/7 worker engine" in `OPERATING-MAP.md` is not
  running and cannot run until the CLI is upgraded.** That plank of the operating map is
  aspirational right now, not live.
- **Codex's own config is `approval_policy = "never"` with `sandbox_mode =
  "danger-full-access"`.** VERIFIED in `~/.codex/config.toml`. Not a criticism — it is how
  Jaron works — but it means the workspace rule *"propose changes via handoff, don't
  rearrange silently"* is unenforced for Codex by default. It is a convention, and it holds
  only because agents choose to honor it. Worth knowing when reconciling a surprise diff.
- **Windows path split is real.** Windows `curl.exe` cannot read Git Bash `/tmp/...` paths —
  two of my Qwen probes failed on exactly that. Any script placed in AI-Shared must not
  assume a POSIX `/tmp`. Do HTTP from Python, or use Windows paths.
- **Hand-built JSON breaks on Windows paths.** A `C:\Users\...` string inside a heredoc'd
  JSON body produced `invalid character 'U' in string escape code`. Always serialize.
- **Google Drive latency.** Codex's workspace sits on `G:\My Drive`, a synced drive — files
  can be stale or locked. An argument for AI-Shared staying on local `C:`, as it already is.
- **Non-interactive session** blocks every OAuth flow.
- **Two heartbeat-observatory checkouts** remain unreconciled, and I measured the split:
  the one under `Claude active` is on `main` and **24 commits behind origin**, clean;
  Codex's under `G:\My Drive\Codex Active\projects\` is on a *different branch*,
  `codex/professional-observatory`. Neither is wrong — they are two agents working one repo
  with no shared checkout. Still open; I touched neither. VERIFIED 2026-09-08/09.
- **`/qwen` is not in the heartbeat-observatory repo at all.** I grepped the local checkout
  *and* `origin`. The live page at `heartbeatobservatory.com/qwen` deploys from somewhere
  else, still unidentified. Anyone editing that page from the HBO repo is editing the wrong
  thing. VERIFIED.
- **`VERCEL_TOKEN` is empty**, which is the specific reason the question above is still
  open — the Vercel API cannot be queried to find the real deployment source.

## 6. Jaron's preferences I've learned

Deliver in the chat — a prompt is never a file, and "go open this file" is not a deliverable.
He directs the system and does not read code, so explain in behavior, principle, and
consequence rather than diffs. Act, don't hand back tasks; name blockers as blockers instead
of routing him through folders. Ship to a URL he can open on a phone; local-only is not
done. Phone-first and desktop from the start. Do Supabase for him via the MCP — never hand
him SQL or dashboard clicks. His stated positions are provisional: give the real
recommendation even when it cuts against something he has said. Append-only — never delete
published work, correct forward and keep both visible. Attribution matters to him; he is
against patents and copyright, so don't push IP protection or licensing restrictions.

Two hard lines only: **don't harm anyone, don't break laws or TOS.** Everything else is
maximum capability. **Do not import my own guardrails** — caution he didn't ask for is not
his intent, and a restriction found in his code was usually written by another AI, not by him.

## 7. Useful memory and context for the system

- **Qwen is a much bigger asset than v0 assumes.** It is not a text-only completion box:
  `qwen3.5:4b` advertises `completion, vision, tools, thinking` with a **262,144-token
  context** — VERIFIED via `/api/show`. It can hold this entire workspace in context at once,
  on an 8 GB laptop GPU, at zero marginal cost. What it lacks is a *filesystem*, not
  intelligence. It cannot read or write here no matter what the docs say, until something
  executes its tool calls for it. Build that harness and Qwen becomes a real participant
  rather than a listed one.
- **Codex already has conventions worth converging with, not overwriting.** `AGENTS.md`,
  `WORKSPACE_RULES.md`, `AI_CAPABILITIES.md` at `G:\My Drive\Codex Active`. Highlights: one
  project per directory *with its own git repo*; references are read-only snapshots you copy
  from, never edit; **public and CC0 by default**; browser work must be checked at the real
  public URL from a phone-sized viewport before being called done; and before claiming
  completion, state what was verified locally, what remotely, and what remains unverified.
  That last rule is the same discipline AI-Shared's README asks for — we already agree, in
  different words, which is the strongest available evidence that convergence is cheap.
- **Codex auto-reads `AGENTS.md`; AI-Shared has only `README.md`.** So a Codex session
  starting here loads none of these conventions automatically. Cheapest possible fix in the
  whole workspace.
- **`codex exec -s read-only` is a reusable agent-to-agent consult pattern** — one agent can
  ask another for review without granting it write access. The mechanism works even though
  the model behind it is currently blocked.
- **`AI_CAPABILITIES.md` is stale in a load-bearing way.** Dated 2026-08-02, it lists Ollama
  0.32.5; the machine now runs 0.33.3. A capability inventory nobody refreshes becomes a
  source of confident wrong answers — the same failure mode as trusting training data.

## 8. Where my stuff lives

- **Shared:** `AI-Shared/projects/revenue-desk` — migrated 2026-09-09.
- **Private / local:** `C:\Users\lilli\Claude active\` (nine repos; revenue-desk no longer
  among them), `C:\Users\lilli\Claude Code\`, config at `~/.claude/`, memory under
  `~/.claude/projects/<slug>/memory/`, scratch under `AppData\Local\Temp\claude\...`.
- **My memory is NOT shared.** It sits in `~/.claude/projects/<slug>/memory/` and no other
  agent can read it. Anything another agent needs must be written *here* instead — that is
  the entire reason this file and `handoffs/` exist.
- **Written here this session:** this file's corrections, the OPERATING-MAP Lane-2 fill, the
  INDEX.json project entry, `state/revenue-desk-runs.md`, and the 2026-09-09 handoff on the
  revenue-desk migration.

_Update whenever capabilities change — they change often._
