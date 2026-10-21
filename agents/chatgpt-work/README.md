# agents/chatgpt-work/ — ChatGPT Work's own area

This is the operational area for ChatGPT Work. Identity and current capability claims live
in `state/self-reports/chatgpt-work.md`; this file records the route and the gaps that are
specific to a cloud-capable agent.

## How I reach AI-Shared

ChatGPT Work has two materially different starting modes:

- **Started on the MSI:** this session has a real PowerShell-backed local file route. I read
  `C:\Users\lilli\AI-Shared` directly and wrote this area plus the self-report there.
- **Started in cloud:** I have no direct `C:\` filesystem path in the cloud route. The
  local workspace is therefore unavailable unless its contents are exposed through another
  route. This particular task was MSI-started, so a separate cloud-started shell was not
  created here; the cloud-side filesystem boundary is documented as a limitation, not
  falsely marked as independently probed.

## Routes that worked in this audit

- **Google Drive:** the connector found the `Codex Active` folder and fetched
  `WORKSPACE_RULES.md`. This reaches the Drive-backed `G:\My Drive` material, not the
  `C:\Users\lilli\AI-Shared` folder.
- **GitHub:** the connector read the private `JaronKBragg7337/revenue-desk` repository and
  its `README.md`. This is repository access, not a remote for AI-Shared itself.
- **Supabase:** the management connector listed projects and table metadata, including the
  `desk_*` tables. The shared desk row bus remains treated as blocked until
  `SUPABASE_SERVICE_ROLE_KEY` is filled; no row query or workaround was used here.
- **Shared memory with ChatGPT Chat:** no memory read/write tool is exposed in this task, so
  I could not perform a cross-session echo test. Treat that route as **UNVERIFIED** until a
  later cloud session or ChatGPT Chat confirms retrieval of a marker from this session.

## What would close the gap

1. Jaron's open Q-004 decision: give `AI-Shared` a private GitHub remote, if that is the
   desired durable source for the core and handoffs.
2. Fill `SUPABASE_SERVICE_ROLE_KEY` to open ChatGPT Work's intended `desk_*` data-bus path.
3. Verify the memory route with a deliberate marker in a later cloud-started task and in
   ChatGPT Chat; use `CHATGPT-WORK-MSI-2026-09-09` as the marker. This session cannot do
   that without a separate session or memory surface.

No secrets are stored here. Others may read this area; ChatGPT Work owns its contents.
