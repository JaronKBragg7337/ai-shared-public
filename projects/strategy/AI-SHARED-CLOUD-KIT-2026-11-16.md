# AI-Shared, cloud continuity, and the GitHub kit — design discussion
Date: 2026-11-16
Source: Jaron's ChatGPT conversation, following the cloud-only Supabase relay demonstration.
Status: Concept for OTHER owners (people with no computer). NOT a change to Heartbeat's own setup (Jaron 11/16 3:20 PM): we keep the MSI system we've always had; for us, cloud is only a backup. We are considering this, not switching to it.

## Jaron's new observations (preserve the distinctions)

- The MSI remains Heartbeat Observatory's **main and useful computer**. A cloud alternative matters when Desktop Commander/local access fails, and for people who own no computer.
- The private **AI-Shared GitHub repository** could become a remotely usable, full **shared working file system** for authorized cloud agents **if it is fully current with the MSI**. Jaron wants cloud Claude to interact with actual project files and their structure, not depend solely on pre-made resume/context files.
- **Supabase** serves the website and the communication channel between AIs; the earlier cloud-only test showed its value independently of the MSI.
- The **kit might itself be a GitHub repository**, copied/instantiated for each owner, with an initial structure: names of folders/files that could be used, even before all of those functions are filled in. The structure demonstrates possible branches and future domains.
- Each owner gets **one company spanning many fields**, not a kit that creates multiple independent companies. An AI orchestrator routes work to appropriate agents and cloud/local resources according to what the owner has.
- Preserve room to add unexpected new domains; what exists in the structure is not a requirement to use all of it.
- Jaron was moving among others' schedules and speaking by voice-to-text; preserve intent without silently treating accidental words as binding decisions.

## What has been verified today

- ChatGPT connected directly to the Supabase `ai_mailbox` and exchanged multiple messages with a separate Anthropic-hosted `cloud-claude` session. The cloud worker reported no home-MSI involvement.
- ChatGPT read the private `JaronKBragg7337/ai-shared` repository through the connected GitHub account. It has a root `README.md`, `AGENTS.md`, strategy documents, handoffs, state, projects, research, etc.; Git tree included 7,673 entries during inspection.
- Its `README.md` calls the MSI shared folder the coordination layer and GitHub the authoritative source for project code. Its `.gitignore` excludes secrets, caches, local environments, large media and some runtime state. **Therefore the GitHub checkout is not currently verified as a full live copy of the MSI**, even if commits are recent.
- Current cautionary example: the root `AGENTS.md` still describes Jaron as a roofer and contains dated business/trading information. Historical instructions must not outrank a confirmed current-state record.

## Suggested architecture to test, not a finalized design

```
OWNER'S PHONE / CONVERSATION / APPROVED SIGNALS
                |
                v
OWNER'S COMPANY KIT (private GitHub repository)
  - agent entrypoint and current-owner snapshot
  - projects/ domains/ knowledge/ decisions/ handoffs/
  - templates, file naming and instructions for expansion
                |
                v
AI ORCHESTRATOR + AVAILABLE WORKERS
  - cloud worker: clone/pull -> inspect actual files -> build -> commit/push
  - MSI worker, when available: same repo + local hardware/tools
  - GPU/cloud storage only as needed for heavy data/media
                |
                v
SUPABASE COMMUNICATION + LIVE STATE
  - AI mailbox, leases/claims, jobs, website records
                |
                v
WEBSITE / APPS / MEDIA / OTHER DOMAINS
```

GitHub is version control and portable documents/code; it does not itself run agents or replace live database state, and empty folders are not stored without placeholder files. The owner-specific kit should start from a **clean template repository**, not a copy of all Heartbeat's private AI-Shared data, credentials or conclusions.

## Tests to run (unverified until executed)

1. **MSI-to-GitHub parity:** compare exact commit hashes and relevant untracked/ignored paths on the MSI with GitHub's `main`; decide which important documents/states must synchronize and which remain outside Git.
2. **Cloud from repo, not pre-made context:** fresh cloud session using only authorized GitHub credentials + minimal repository URL; clone/read current instructions, identify a specific real project, perform a small non-destructive file task, and push a handoff or commit to a test branch.
3. **Clean session restart:** terminate the entire cloud session, start a new one, read repository/current-state data and Supabase event history, and correctly resume the previous task without relying on its ephemeral `resume.md`.
4. **Computer-free company:** run the same scenario with no MSI, including cross-AI mailbox coordination, avoiding duplicate claims; verify what genuinely cannot run without paid compute or local hardware.
5. **Kit template:** create a separate sanitized repository template with empty-but-described modules (e.g. `domains/README.md`, `projects/README.md`, `knowledge/README.md`, `settings/README.md`, `handoffs/README.md`), each initially optional or configurable, plus a blank owner profile. Test with a new company name and just one connected AI.
6. **Environment separation:** ensure cloud agents use only narrowly permitted credentials and do not expose secrets in commits; assign appropriate storage to big media, running state and device-specific files.

## Open decisions for Jaron and Claude

- What minimum subset of AI-Shared must be mirrored before a cloud worker can actually be useful, rather than simply informed?
- Should the customer kit be a GitHub template directly, or distributed in a way that also works for people who never open GitHub themselves?
- What is the simplest initial file/folder tree that communicates optional future branches without overwhelming the owner or agents?
- How does the orchestrator choose a local MSI task versus cloud-only execution, and preserve task ownership across model/session replacement?
- How should owner-current-state corrections update dated `AGENTS.md` claims without rewriting historical records?

Next: inspect and compare actual MSI checkout and GitHub state before declaring them synchronized. Keep this note as an invitation to test; do not confuse a proposed design with implementation.
