# HANDOFF — Codex convergence, live capability audit, and checkout risks (2026-09-09)

**From:** Codex (OpenAI) · **To:** Claude Code, Qwen, ChatGPT Work, Claude Cowork, Jaron
**Status:** additive and reversible. I created Codex's report and area, corrected stale
index facts, and did not edit either outstanding project tree.

## What I read

I read AGENTS.md, INDEX.json, README.md, OPERATING-MAP.md, working-with-jaron.md,
decisions/OPEN-QUESTIONS.md, agents/README.md, the self-report template, Claude Code's
worked report, and all five files dated 2026-09-09 in handoffs/. The directory contains
five same-day handoffs, not three; I read all five rather than silently selecting three.

## What I changed

- Wrote state/self-reports/codex.md in the same live-probe standard as Claude Code's
  report.
- Created agents/codex/README.md with Codex's route, runbooks, checkout notes, and
  current product quirks.
- Updated INDEX.json to register the report and close only the Codex self-report blocker.
  I also corrected the stale single-executable wording and clarified the /qwen evidence.
- Did not add a Git remote, commit, push, or otherwise change polymarket-us-agent.
- Did not edit /qwen or any file in either heartbeat-observatory checkout.

## Live capability evidence

**Local verification.**

- codex --version returned codex-cli 0.153.4.
- codex exec --help exposed non-interactive execution, sandbox selection, model selection,
  and --skip-git-repo-check.
- A fresh codex exec -s read-only --skip-git-repo-check -C
  C:\Users\lilli\AI-Shared invocation reported gpt-5.6-luna and returned the requested
  sentinel. It emitted non-fatal warnings about PowerShell shell snapshots and skill icon
  paths; the run still completed.
- where.exe codex and Get-Command codex -All returned both
  C:\Users\lilli\scoop\shims\codex.exe and the Codex desktop runtime under
  C:\Users\lilli\AppData\Local\OpenAI\Codex\bin\<hash>\codex.exe. The Scoop shim resolves
  first, and both explicit binaries report 0.153.4. The former “exactly one on PATH”
  statement was true only of the earlier process environment and is not true in this
  Codex desktop process.
- The unsandboxed task read G:\My Drive\Codex Active\WORKSPACE_RULES.md successfully.
  A nested -s read-only task could execute its shell probe but failed to open that G:
  file with System.Management.Automation.MethodInvocationException. The old consult's
  inability to certify G: was therefore correct; this session's direct read certifies it.
- Ollama http://localhost:11434 returned 0.33.3; qwen3.5:4b and llama3.2:3b are installed.
  /api/show reported Qwen's completion, vision, tools, thinking capabilities, 4.7B Q4_K_M
  size, and 262,144-token context.
- The Qwen bridge read the shared files in --read-only mode. Qwen emitted a write_file
  request during one consultation, but no state/self-reports/codex.md file existed
  afterward. A later consultation returned text, but did not follow the requested narrow
  format.
- polymarket-us-agent git diff --check found no whitespace errors. Its offline tests
  could not import server.py because the local Python environment lacks the mcp package;
  no market API, credential, order, or Qwen call was made.

**Remote verification.**

- Fresh git ls-remote output for heartbeat-observatory showed origin/main at
  c4c786a8... and origin/codex/professional-observatory at 33a339a0....
- An unsandboxed HTTP request to https://www.heartbeatobservatory.com/qwen/ returned
  HTTP 200, title Qwen / Polymarket US — Heartbeat Observatory, and references to
  qwen.css?v=owner-chat-2 and qwen.js?v=owner-chat-2.
- The public site's root was discoverable through the web search surface and describes
  the Observatory as served from Vercel. That establishes the public site, not the
  deployment repository or build source.

**Still unverified.**

- The exact model identity of this desktop conversation is not exposed by the current
  shell/tool surface; only the CLI's configured Luna route was verified.
- The deployment mechanism/source for the live /qwen page is not proven. The matching
  owner-chat-2 marker is evidence of alignment with the committed feature-branch
  baseline, not proof of Vercel's configured source.
- polymarket-us-agent remains uncheckpointed and has no remote. The missing mcp
  dependency prevented its offline tests from starting.
- No cloud-started task's direct access to C: was tested.

## Rules comparison: what was preserved and what was flattened

I directly read G:\My Drive\Codex Active\WORKSPACE_RULES.md from this unsandboxed
session. The shared core and that file agree in practice on:

| Claim | Finding |
|---|---|
| Report locally verified, remotely verified, and unverified work before calling it complete | **Agrees.** WORKSPACE_RULES.md states this directly; AGENTS.md adopts the same three-part requirement. |
| Public and CC0 defaults | **Agrees, with scope flattened slightly.** The source says public is the default and CC0 is the default project license; AGENTS.md compresses this to “Public and CC0 by default.” |
| Device-visible handoffs | **Agrees.** The source says a result is not fully handed off if the owner cannot see it from the current device; the core says the same and working-with-jaron.md adds phone-visible delivery. |
| One project per directory/repository | **Agrees for new projects.** The source says new projects start under projects/ with their own Git repository. The core's wording is broader, but Q-003 explicitly keeps Codex's existing G: projects in place and points at reality. |
| Read-only references | **Agrees on the boundary, but details were flattened.** The source also says to extract principles/contracts/workflows/assets without importing a reference's branding, layout, identity, or conflicting scope. The core retains “copy from, don't edit” but does not restate those extraction boundaries. |

So Claude Code's earlier convergence was substantively right, but not complete: the
project-path exception and the reference extraction/non-import rule must remain visible in
the Codex area and Q-003. The browser no-login/phone-sized check is also preserved in
the Codex preferences/runbook context, though not fully repeated in AGENTS.md.

## /qwen: canonical baseline now established, deployment ownership still open

The two checkout states are not equivalent:

- Claude's checkout at C:\Users\lilli\Claude active\heartbeat-observatory is main at
  8bc6de0, 24 commits behind origin/main, and its HEAD tree has no qwen/.
- Codex's checkout at G:\My Drive\Codex Active\projects\heartbeat-observatory is
  codex/professional-observatory at 33a339a; its HEAD and the matching remote branch
  track qwen/index.html, qwen/qwen.css, and qwen/qwen.js.
- Fresh remote tree inspection confirms qwen/ exists on
  origin/codex/professional-observatory and not on origin/main.
- The Codex worktree has uncommitted continuation-3 changes, while its committed
  baseline references owner-chat-2. The live page references owner-chat-2, so the
  public page aligns with the committed branch baseline, not the uncommitted continuation
  work.

**Conclusion:** for repository source, treat origin/codex/professional-observatory at
33a339a as the canonical /qwen baseline; Claude's main checkout is not the source for
that path. For deployment provenance, neither local checkout is independently authoritative
until the configured deployment source is identified. I made no /qwen edits and recommend
leaving the uncommitted continuation work untouched until Jaron confirms whether it should
be promoted, discarded, or reviewed.

## polymarket-us-agent: highest loss risk remains untouched

Current state at G:\My Drive\Codex Active\projects\polymarket-us-agent:

- branch master, HEAD 084a8d4, no Git remote;
- modified: AGENTS.md, OBJECTIVE.md, README.md, http_server.py,
  remote_bridge.py, server.py, start_mcp_service.ps1;
- untracked: memory/ and tests/;
- whitespace check clean;
- offline tests blocked before collection by missing mcp.

I did not commit or create a remote because the working tree is not reviewed and the
remote target is unspecified. The safe next action is a deliberate local checkpoint after
the existing diff is reviewed; any remote choice or push remains an owner-controlled
external change. No data was deleted or moved.

## Qwen consultation — actual response, not a paraphrase

I asked Qwen, through python tools/qwen-bridge.py --read-only, for a narrow review of
the workspace and the /qwen evidence. It did not return the requested fields. The actual
response began:

> “Understood. I have fully ingested the **Global Operating State** for RevenueDesk.”

and ended:

> “I am ready. Please provide your next instruction, or trigger a specific lane to see what happens.”

A second narrow request produced a broad status summary beginning:

> “The provided content is a detailed status report and operational configuration for a multi-agent system involving Codex, Qwen, Claude Code, and ChatGPT Work.”

The bridge showed Qwen attempting write_file during the first consultation; the read-only
run left no new report file. This is useful capability evidence, not evidence that Qwen
answered the requested analysis. Do not speak for Qwen beyond these quoted responses.

## Structural posture

This pass added only Codex-owned material and factual index corrections. It did not move,
rename, delete, or fork any project. If a future agent wants to change the shared layout,
the next change should be another dated handoff that explains the reason and preserves the
current paths until the owner decides otherwise.

_Codex · 2026-09-09 · Verified locally: live CLI/model/bridge/filesystem probes, G: rules
read, both checkout states, polymarket status/test attempt. Verified remotely: fresh Git
refs and public /qwen HTTP response. Unverified: deployment provenance, missing Python
dependency, cloud-started C: reachability, and exact desktop-conversation model identity._
