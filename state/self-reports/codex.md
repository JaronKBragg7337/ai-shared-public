# SELF-REPORT — Codex

## Update — 2026-09-10, verified in this desktop session

GitHub CLI authentication permitted the authorized public repository creation and pushes.
Heartbeat Observatory main at `959f289` automatically deployed to Vercel; public responses
match the merge. Main is canonical, superseding older branch claims below. Polymarket now
has a public origin and a clean tracked checkpoint at `6f95a1f`. Browser tooling inspected
all requested routes at 390 × 844 and confirmed President Sim WebGL rendering. Anonymous
HTTP checks separately confirmed public access. Worker end-to-end operations, actual
iPhone rendering, and future reboot behavior were not tested in this turn. Full evidence:
`handoffs/2026-09-10-codex-production-and-backup.md`.

**Written:** 2026-09-09 · **Author:** this agent, about itself · **Method:** live probes
run in this unsandboxed Codex session, not training recall. Claims are tagged VERIFIED
(a tool returned it just now), INHERITED (taken from the shared workspace or prior
handoffs), or UNVERIFIED.

## 1. Identity

- **Product:** OpenAI Codex, running in the Codex desktop task on Jaron's MSI, with the
  local Codex CLI also available.
- **CLI version:** `codex-cli 0.153.4` — VERIFIED (`codex --version`). The configured
  non-interactive model is `gpt-5.6-luna` — VERIFIED by the CLI banner and the selected
  config line. The exact model identity of this desktop conversation is not exposed by
  the shell/tool surface — UNVERIFIED.
- **Working root this session:** `C:\Users\lilli\AI-Shared`. It is not a Git repository
  — VERIFIED through the workspace probes and existing core documentation.
- **Machine route:** this task runs on the MSI with direct filesystem access. The same
  unsandboxed session read `G:\My Drive\Codex Active\WORKSPACE_RULES.md` successfully —
  VERIFIED.

## 2. Current capabilities (VERIFIED live)

**Shell and filesystem.** PowerShell 7.6.5, Python 3.12.10, Node 24.16.0, and Git
2.54.0 are available — VERIFIED. I can read and write the C: workspace and reach the
Google Drive-mounted G: workspace from this unsandboxed task. I used the shell for
read-only repository probes and the workspace patch tool for these scoped edits.

**Codex CLI and agent-to-agent route.** `codex exec --help` exposes non-interactive
execution, read-only/workspace-write/full-access sandbox choices, model selection, and
the `--skip-git-repo-check` option — VERIFIED. A fresh invocation of
`codex exec -s read-only --skip-git-repo-check -C C:\Users\lilli\AI-Shared` using
Luna returned the requested sentinel — VERIFIED. This is the route Claude Code uses to
consult Codex without giving the nested task write access.

**Executable resolution has a current quirk.** `where.exe codex` and
`Get-Command codex -All` returned two PATH-resolvable binaries in this desktop process:
the Scoop shim at `C:\Users\lilli\scoop\shims\codex.exe` and the Codex desktop runtime
under `C:\Users\lilli\AppData\Local\OpenAI\Codex\bin\<hash>\codex.exe`. The shim
resolves first. Both explicit binaries report `codex-cli 0.153.4` — VERIFIED. This
corrects the earlier environment-specific statement that exactly one executable was on
PATH; it does not reintroduce the old 0.141.0 failure.

**Sandbox boundary.** The outer unsandboxed task can read G:. A nested `-s read-only`
Codex task could execute its shell probe but received a
`System.Management.Automation.MethodInvocationException` when opening the G: rules
file — VERIFIED. Read-only consultation can therefore review C: but cannot certify
Codex's G: conventions. The direct unsandboxed read in this session is the certification
used below.

**Local Qwen.** `http://localhost:11434` answered with Ollama `0.33.3`. The installed
models include `qwen3.5:4b` and `llama3.2:3b`. `/api/show` reports Qwen 3.5 as a 4.7B
Q4_K_M model with `completion, vision, tools, thinking` capabilities and a 262,144-token
context — VERIFIED. `python tools/qwen-bridge.py --read-only ...` successfully caused
the bridge to read shared files; when Qwen attempted `write_file`, the read-only policy
blocked it and no new file remained. A later consult returned a broad workspace summary
but did not follow the requested narrow output format — VERIFIED. Treat Qwen output as
model output and inspect the files it names.

**Remote and browser reach.** Git can query the configured GitHub remotes, and an
unsandboxed HTTP request fetched `https://www.heartbeatobservatory.com/qwen/` with HTTP
200, its title, and its referenced Qwen assets — VERIFIED. The web-search surface is
also available, though a direct web-tool open of that path was rejected as unsafe; the
shell fetch worked.

**Long-running behavior.** A one-shot `codex exec` works. I did not create a scheduler,
automation, background worker, or outward integration in this task — UNVERIFIED whether
any separately configured Codex automation should be treated as live for this workspace.

## 3. Legal / TOS lane

- **Polymarket execution: NO.** The shared operating map routes market execution away
  from OpenAI agents. Current OpenAI policy material also prohibits real-money gambling
  and says ChatGPT agent should not automate stock trading or other investment
  transactions. I am not making a separate legal classification of every Polymarket
  product; I will keep Codex to research, paper analysis, tooling, and decision support.
  References checked 2026-09-09: [OpenAI Usage Policies](https://openai.com/policies/usage-policies/)
  and [Using ChatGPT agent in line with our policies](https://openai.com/policies/using-chatgpt-agent-in-line-with-our-policies/).
- **Paid work: YES for Lane 2 research, building, and deliverables**, subject to the
  applicable service terms and Jaron's approval. I do not connect payment rails, move
  money, or take the payout step.
- **Standing workspace boundary:** nothing outward — send, post, spend, submit, accept
  terms, trade — happens without Jaron's explicit yes. I never expose secret values;
  names and existence only.

## 4. What I'm working on now

**AI-Shared convergence.** I read the requested core documents, all five handoffs dated
2026-09-09 (the directory contains five, not three), the self-report template, and the
worked Claude Code report. I wrote this report, created `agents/codex/`, and recorded
the evidence in a dated handoff.

**`polymarket-us-agent` — highest loss risk.** The authoritative checkout is recorded
by the workspace at `G:\My Drive\Codex Active\projects\polymarket-us-agent`, branch
`master`, commit `084a8d4`. It has no configured Git remote and has uncommitted changes
to `AGENTS.md`, `OBJECTIVE.md`, `README.md`, `http_server.py`, `remote_bridge.py`,
`server.py`, and `start_mcp_service.ps1`, plus untracked `memory/` and `tests/`.
`git diff --check` found no whitespace errors. Its 10-test offline suite now passes in
the relocated C: Python 3.12 environment. I did not commit, push, add a remote, or
alter the source tree beyond the requested launcher/runtime repair.

**`heartbeat-observatory` — `/qwen` ownership.** Claude's checkout at
`C:\Users\lilli\Claude active\heartbeat-observatory` is `main` at `8bc6de0`, 24 commits
behind `origin/main`, and has no `qwen/` directory in its tree. Codex's checkout at
`G:\My Drive\Codex Active\projects\heartbeat-observatory` is
`codex/professional-observatory` at `33a339a`, tracks `qwen/`, and has uncommitted
continuation changes to that area plus new migration/test files. Fresh remote refs show
`qwen/` on `origin/codex/professional-observatory` and not `origin/main`. The live page
returns 200 and references `owner-chat-2`, matching the committed branch baseline;
the deployment source is not independently proven. Therefore the repository baseline
for `/qwen` is the remote Codex branch, while live deployment ownership remains
UNVERIFIED. I made no `/qwen` edits.

## 5. Known issues and limitations I've hit

- The shared index's earlier **"exactly one codex.exe on PATH"** wording was not true in
  this desktop process. Two 0.153.4 binaries are PATH-resolvable; the Scoop shim wins.
  The index and handoff now preserve that distinction.
- A read-only nested Codex sandbox cannot read the G: Google Drive mount, even though an
  unsandboxed Codex task can. This is a sandbox boundary, not a general filesystem limit.
- Nested CLI runs emit non-fatal warnings that the PowerShell shell snapshot is unsupported
  and that some skill icon paths are ignored. The sentinel `codex exec` still completed.
- Qwen's bridge can enforce read-only writes, but Qwen did not reliably honor a narrow
  response format in two consultations. Model output is not a substitute for checking
  the shared files.
- `AI-Shared` itself has no Git repository or remote (Q-004 remains OPEN), so these
  coordination files are still local to the MSI until Jaron decides the storage route.
- `polymarket-us-agent` has no remote and a dirty working tree; its offline tests are
  blocked by the missing `mcp` dependency. No checkpoint or remote was created because
  the exact preservation/remote decision is not mine to invent.
- The two heartbeat checkouts do not share a working tree. The public `/qwen` page aligns
  with the committed Codex feature-branch marker, but deployment provenance is not
  proven. Do not edit `/qwen` until the owner confirms the intended source of truth.

## 6. Jaron's preferences I've learned

Deliver in chat, not as filesystem homework. He directs the system and does not read code,
so explain behavior, principle, and consequence. Act within scope and name blockers plainly.
Ship a live URL he can open on his phone; label localhost-only or desktop-only work. Work
phone-first and desktop-first. Do Supabase work for him through the connector rather than
handing him SQL or dashboard clicks. Keep unanswered owner questions OPEN; investigate
technical uncertainties instead of turning them into permission prompts.

His two hard lines are not harming people and not breaking laws or rules, including brand
TOS. Nothing outward in this shared workspace still needs his explicit yes. Never expose
secrets. Public and CC0 are the defaults; published work is corrected forward, not deleted.
Attribution matters. Structural changes are additive and reversible and are announced in
handoffs; do not silently rearrange another agent's work.

## 7. Useful memory and context for the system

- `AI-Shared` is the shared C: coordination layer, not the authoritative GitHub layer.
  Codex's three owned projects intentionally remain on G: under Q-003; `projects/` is a
  pointer plus the migrated `revenue-desk`, not a demand to move every repository.
- The unsandboxed-vs-read-only distinction matters: Claude's prior consult was correct
  not to certify G: from `-s read-only`; this session directly certified the file from an
  unsandboxed route.
- The shared core agrees with Codex's `WORKSPACE_RULES.md` on local/remote/unverified
  completion reporting, public/CC0 defaults, device-visible handoffs, per-project Git
  repositories, and read-only references. It flattens some scope: the core's
  `under projects/` wording is broader than Q-003's explicit pointer exception, and its
  reference rule omits the source rule's details about extracting principles without
  importing branding/layout/conflicting scope. The browser no-login/phone-sized check is
  preserved in the agent preferences but not fully restated in `AGENTS.md`.
- For `/qwen`, the only current repository tree containing the path is the Codex feature
  branch. Its committed baseline matches the public page's `owner-chat-2` marker; the
  worktree's `continuation-3` changes are local and uncommitted.
- Open owner questions remain Q-004 (private remote for AI-Shared), Q-005 (service-role
  key), Q-006 (payment rail), and Q-007 (approval visibility). I did not infer answers.

## 8. Where my stuff lives

- **Shared:** `C:\Users\lilli\AI-Shared\state\self-reports\codex.md`,
  `C:\Users\lilli\AI-Shared\agents\codex\`, and the dated handoff in `handoffs/`.
- **Private/local Codex workspace:** `G:\My Drive\Codex Active\`, including
  `projects\polymarket-us-agent`, `projects\heartbeat-observatory`, and
  `projects\prediction-research-system`; conventions live in
  `G:\My Drive\Codex Active\AGENTS.md` and `WORKSPACE_RULES.md`.
- **Private/local coworker area:** `G:\My Drive\Codex Coworker\`.
- This agent area is not private. Others may read it; Codex owns its contents and no secret
  values belong here.

## 9. Current Qwen runtime state

On 2026-09-09, an unsandboxed Codex session repaired the Qwen path after reading the two
Claude Code inbox handoffs. The live primary is now entirely on C:, not AppData\Local:

- Runtime source: C:\Users\lilli\AI-Shared\runtime\polymarket-us-agent\
- Python environment: C:\Users\lilli\AI-Shared\runtime\polymarket-us-agent-venv\
- The prior AppData\Local venv and runtime remain in place as recoverable legacy copies.
- The G: project remains the source mirror; the six runtime code/config files, including
  both launchers, were hash-checked against the C: runtime.
- The launcher keeps C: credential candidates first and G: last. Values were not printed
  or written into shared coordination files.

Two AtLogOn tasks now run as MSI\lilli: Polymarket MCP and Qwen Remote Bridge. Their actions
use C: paths, have no working directory dependency, wait/restart settings, and an unlimited
execution window. The bridge waits for loopback ports 8765 and 18789 before starting.

Live proof: port 8765, port 18789, both C: venv child processes, the Qwen bridge, and all
10 project tests were verified. A read-only end-to-end probe returned exactly
QWEN_BRIDGE_LIVE_OK. The actual post-reboot logon sequence is still UNVERIFIED; no reboot
was performed.

_Update whenever the CLI, desktop runtime, local model route, project ownership, or
sandbox boundary changes._

## Phone map audit — 2026-09-23
From this MSI desktop task I verified 42 public URLs by anonymous HTTP response/title,
matched watch local HEAD to GitHub master, checked Windows tasks and published
brief/feed dates, and queried Supabase read-only. The management status was
ACTIVE_HEALTHY while SELECT 1 failed before TLS. I updated JARONS-MAP.md and left
a full handoff at handoffs/2026-09-23-codex-phone-map-audit.md. iPhone Notes
rendering and application behavior behind the URLs were not tested.
The public /games/ page was checked at 390×844 in Chrome: Games heading,
Orbit Salvage link, and no document-width overflow. A screenshot timed out.

## Live update — 2026-09-12
Local Codex desktop on MSI, direct PowerShell/filesystem and web access verified. Active CLI still 0.153.4; official changelog lists 0.154.0. Current task tools expose Astra, Sol, Terra and Luna choices; no subagents were run. Read-only desk account/queue succeeded through the runtime venv; bare Python invocation produced no captured output. Public route HTTP checks succeeded; phone rendering and post-change reboot remain unverified. Proposer last run failed (result 1); see handoffs/2026-09-12-codex-live-orientation.md. No order, service or site mutation performed. No universal unlimited Luna allowance verified.

## Live update — 2026-09-12 Fly Brain
Registered and manually started the authorized Fly Brain dry-run Windows task through local PowerShell. XML/settings and 40-second Running / 267009 result verified; log showed 165122 neurons and waiting for a market. No Python edits. No remote verification; future logon/restart and sustained operation unverified. Evidence: handoffs/2026-09-10-codex-trade-tasks.md.

## System audit — 2026-09-12 afternoon
Completed local maintenance fixes in desk.py (Windows child output/exit), verifier.py (failed one-shot exit), and postboot-check.ps1 (pipeline/staleness/HTTP error coverage). Seven fault/success scenarios verified, plus the ordinary 13:42 scheduled verifier run. Anonymous browser checks at 390x844 passed on all three requested public routes; desk RLS inspected read-only. Protected executor.py, desk-trade.py and fly.py were not changed. Fly Brain is now built in dry mode; this supersedes the morning's Q-013 status. Live-mode accounting and acknowledgment gaps, stale core records and public-page copy are detailed in handoffs/2026-09-12-codex-system-audit.md. No trades or deployment performed.

2026-09-12: Local PowerShell registration/start of Fly Watcher verified; Running after 25 seconds, task XML and watcher log checked. No Python edits. Remote and future-trigger behavior unverified.

## Live update — 2026-09-22 Orbit Salvage publication
Published the fresh GPT-6 Luna browser-game task as `JaronKBragg7337/orbit-salvage` on `main` (`4f3e8c7`) with GitHub Pages enabled. Added its full-bleed wrapper and `/games/` tile to `heartbeat-observatory` `main` (`7bfb033`); Vercel production now serves the index tile and embedded game without login. The older G: site checkout was not touched. Luna's local checks covered 390×844 and 1440×960, launch, touch controls, restart, tether feedback, static responses and JavaScript syntax. This session verified the public game URL and embedded public route in the browser; its available viewport remained 1040×900, so actual public phone-width rendering is unverified. Full cargo delivery/win/lose play, desktop keyboard behavior and browser-console review are also unverified. Evidence: `handoffs/2026-09-22-codex-orbit-salvage.md`.
