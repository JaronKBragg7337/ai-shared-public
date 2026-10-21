# HANDOFF — ChatGPT Work access audit (2026-09-09)

**From:** ChatGPT Work (OpenAI) · **To:** Claude Code, Codex, Qwen, Claude Cowork, Jaron
**Purpose:** record what ChatGPT Work can actually reach when started on the MSI, and what a
future cloud-started session can use.

## What I wrote

- `state/self-reports/chatgpt-work.md` — the canonical self-report.
- `agents/chatgpt-work/README.md` — the ChatGPT Work-specific route and gap notes.
- `INDEX.json` — registered the self-report, removed ChatGPT Work from the missing-report
  blocker, and corrected the memory route from an asserted live state to documented but not
  independently verified.

## Verified locally

- Read the requested core documents in the user-specified order, all four 2026-09-09
  handoffs, `agents/README.md`, the worked Claude Code area README, and the self-report
  template.
- Read access to `C:\Users\lilli\AI-Shared` works from this MSI-started task.
- `AI-Shared` has no `.git` directory and no remote.
- Write access works: the two files above were created and read back successfully.

## Verified remotely

- **GitHub:** read the private `JaronKBragg7337/revenue-desk` repository and its `README.md`.
- **Google Drive:** found `Codex Active` and fetched the text of `WORKSPACE_RULES.md`.
- **Supabase:** management connector listed projects and table metadata, including the
  `desk_*` tables. I did not read desk rows or bypass the recorded service-key gate.

## Still unverified

- A cloud-started ChatGPT Work task reading or writing `C:\` directly; this audit itself was
  MSI-started.
- Whether a fact written or learned in this task is retrievable through shared memory by a
  later cloud task or by ChatGPT Chat. No memory read/write surface is exposed here, so I will
  not call that route verified.
- A successful ChatGPT Work row-level read of the shared Supabase `desk_*` bus; the workspace
  records it blocked until `SUPABASE_SERVICE_ROLE_KEY` is filled.

## Owner-controlled gaps that remain open

- Q-004: decide whether `AI-Shared` receives a private GitHub remote.
- Q-005: fill `SUPABASE_SERVICE_ROLE_KEY` for the intended desk bus.

No outward messages, posts, submissions, purchases, trades, or money movement occurred.
