# SELF-REPORT — ChatGPT Work

**Written:** 2026-09-09 · **Author:** ChatGPT Work, about itself · **Method:** live probes in
this MSI-started session. Claims are marked VERIFIED, INHERITED, or UNVERIFIED. No secret
values are recorded.

## 1. Identity

- **Product / brand:** ChatGPT Work, OpenAI.
- **Runtime model/version:** the exact model identifier is not exposed in this task's live
  context. I will not guess one from training or from the available model menu.
- **Starting mode:** MSI-started for this run. The local shell and file route below prove
  that fact operationally.
- **Date:** 2026-09-09, America/Indianapolis.

## 2. Current capabilities (VERIFIED live, not assumed)

### Local MSI route

- **Read access:** VERIFIED. A PowerShell-backed local command read `AGENTS.md`, `INDEX.json`,
  the core documents, all 2026-09-09 handoffs, and the worked Claude Code area from
  `C:\Users\lilli\AI-Shared`.
- **Write access:** VERIFIED by this deliverable. I created `agents/chatgpt-work/`, wrote
  this self-report and its area README, and read both back successfully in this session.
- **Workspace state:** VERIFIED. `AI-Shared` has no `.git` directory and no remote; this is
  the Q-004 gap, not a failed local read.
- **Outward actions:** not exercised. The standing rule remains that nothing is sent,
  posted, spent, submitted, accepted, traded, or otherwise made external without Jaron's
  explicit yes.

### Remote connectors

- **GitHub:** VERIFIED read access. `github_get_repo` returned the private
  `JaronKBragg7337/revenue-desk` repository, and `github_fetch_file` returned its `README.md`
  from `master`. I did not test a write operation.
- **Google Drive:** VERIFIED read access. `google_drive_search` found the `Codex Active`
  folder and `WORKSPACE_RULES.md`; `google_drive_fetch` returned that file's text. This is
  the live cloud route to the Drive-backed Codex workspace.
- **Supabase:** VERIFIED at the management layer. `supabase_list_projects` responded and
  `supabase_list_tables` enumerated the project schema, including `desk_agents`,
  `desk_tasks`, `desk_queue`, and `desk_decisions`. I did not query desk rows, because the
  workspace records ChatGPT Work as blocked from the shared `desk_*` bus until
  `SUPABASE_SERVICE_ROLE_KEY` is filled.
- **Web / other tools:** a web tool and additional app surfaces are present in the live
  tool inventory, but I did not need them for this access audit and do not claim a specific
  connector from mere presence.

### Cloud-started mode and memory

- **Direct access to `C:\Users\lilli\AI-Shared` from a cloud-started task:** UNVERIFIED in
  this exact run because I did not create a second cloud-started task. The current task is
  MSI-started and has local access. The workspace's documented distinction is that a
  cloud-started ChatGPT Work session has no path to `C:\`; I preserve that as the operating
  assumption until a separate cloud probe is run.
- **Google Drive and GitHub from cloud:** the connector calls above work from this task and
  prove the connector routes are live. They do not prove that a separately started cloud
  task has identical authorization state.
- **Shared memory with ChatGPT Chat:** UNVERIFIED. No memory read/write surface is exposed
  in this task, and a cross-session round trip cannot be completed inside one session. Do
  not claim that a fact written here is retrievable by future-cloud-you until a later cloud
  task or ChatGPT Chat confirms a deliberate marker.

## 3. Legal / TOS lane

- **Polymarket / market execution:** NO. OpenAI agents are barred from placing trades or
  moving market funds. I can support research, paper analysis, monitoring, and tooling only.
- **Paid work:** YES within OpenAI's allowed non-market lane: research, build, and deliver
  work. Payment rails and money movement remain human-approved actions; no rail was touched.
- **Standing workspace limits:** never expose secret values; nothing outward without Jaron's
  explicit yes; laws and all applicable TOS come first.

## 4. What I am working on now

- Access audit and self-report only; no project repository was modified.
- Own area: `C:\Users\lilli\AI-Shared\agents\chatgpt-work\`.
- Canonical self-report: this file.
- No branch or commit applies because `AI-Shared` is not a git repository.

## 5. Known issues / limitations

- `AI-Shared` is local-only and has no GitHub remote. Q-004 is still OPEN; this is the main
  durability and cloud-discoverability gap.
- The intended shared Supabase `desk_*` bus is blocked pending `SUPABASE_SERVICE_ROLE_KEY`.
  The management connector being live does not silently close that owner action.
- Shared memory with ChatGPT Chat has not been directly tested from this task because no
  memory tool or second-session echo path is available.
- A cloud-started task's direct inability to read `C:\` was not independently instantiated
  here; this run proves only the MSI-started mode.

## 6. Jaron's preferences learned from the core

- Deliver in chat; do not hand him filesystem procedures or make a prompt into a file.
- Act on technical uncertainties, but preserve owner decisions as OPEN until he answers.
- Explain behavior, consequence, and evidence rather than code diffs.
- Phone-visible, public/no-login URLs are preferred for deliverables when a project can
  support them; local-only work must be labelled honestly.
- Never delete published work or rewrite history; correct forward and retain attribution.
- Public and CC0 are defaults unless he says otherwise. Do not add secret values to shared
  files.

## 7. Useful memory / context for the system

- The three cloud routes tested in this session are not equivalent: Drive exposes the
  Drive-backed Codex workspace; GitHub exposes the private `revenue-desk` repository; neither
  exposes `AI-Shared` because Q-004 is still open.
- Supabase management access exists independently of the local `.secrets` key state, but the
  workspace's intended ChatGPT Work desk-bus route remains blocked. Do not use management
  access to pretend the owner-controlled key question is resolved.
- The direct proof of local write capability is the existence and readback of this report and
  `agents/chatgpt-work/README.md`. This is the route future cloud sessions cannot assume.
- Suggested later memory probe marker: `CHATGPT-WORK-MSI-2026-09-09`. Recall of that exact
  marker by a separate cloud task or ChatGPT Chat would be evidence; its presence in this
  local file is not.
- The safest durable handoff for future-cloud-you is: put core state on the approved private
  GitHub remote if Jaron answers Q-004, and keep this report as the product-specific route
  description.

## 8. Where my stuff lives

- **Shared local area:** `C:\Users\lilli\AI-Shared\agents\chatgpt-work\`.
- **Self-report:** `C:\Users\lilli\AI-Shared\state\self-reports\chatgpt-work.md`.
- **Cloud-visible material currently reachable:** the connected Google Drive workspace and
  the connected private GitHub repository, subject to their own permissions.
- **Not reachable by a cloud-started local path:** `C:\Users\lilli\AI-Shared` itself,
  unless its contents are placed behind an approved remote route.

_Update this report whenever the ChatGPT Work host, connectors, memory behavior, or OpenAI
TOS lane changes._
