# System audit — Codex, 2026-09-12

## Scope and protected files
Local MSI audit requested by Jaron. No orders, approvals, money actions or Fly Brain live switch. tools/executor.py, tools/desk-trade.py and projects/fly-brain/fly.py are read-only for this audit.

## Findings requiring design work before live use

Fly Brain remains running in DRY RUN. Source inspection found these reasons for a future, separately recorded fly.py repair; this handoff does NOT claim the repair is implemented:
- Dry-run LET GO calls apply_realized and writes the same cap.json subsequently loaded by --live. Simulated profit can therefore raise real-money caps. Separate financial accounting by mode; do not discard trained weights.
- holding and the entry KC pattern exist only in memory. A restart forgets outstanding exposure and the learning context. Reconcile holdings before a future live start and persist entry context.
- desk_trade ignores subprocess returncode; PRESS guesses success by absence of 'refused'/'failed' in output. A traceback can be mistaken for an accepted order. LET GO clears holding without verifying success. Require structured outcomes and confirmed fills before changing holdings.
- ledger_realized says sells/resolutions but reads resolutions only; verifier fills do not populate pnl_usd. Closed-before-settlement trades cannot reliably teach the fly through this path. Design event-level realized accounting, including partial fills and fees.
- --slug bypasses the market screen without requiring dry mode.
These are code-path findings, not observed losses. Do not call the live acceptance criteria complete merely because the process is running. No protected file changed.

Ledger reconciliation also reads only the most recent 100 activities and uses time/slug claims within 15 minutes for browser attribution. High-volume outages can skip history, and same-market owner/agent activity can be misattributed. Propose paginated replay with durable checkpoints and exact order IDs. Do not rewrite historical attribution based on a guess.

## Safe fixes completed
- postboot-check.ps1: include the current periodic jobs, failed/stale runs, heartbeat age, intentional paper pause and the missing Heartbeat port; reject HTTP 5xx rather than treating any response as healthy.
- verifier.py: return a nonzero exit for a failed one-shot run instead of concealing it from Task Scheduler. Does not change book math, approvals or execution.
- desk.py: wait for the venv subprocess on Windows and propagate its exit code/output.

## Core reconciliation proposed (core not silently rewritten)
- This morning's proposer failure is no longer current: 11:57 completed with five inserted proposals, result 0. The file now includes crash logging added outside this audit. Original 09:57 cause remains unproven.
- Q-013 is now answered and Fly Brain built in dry mode. Q-018 now explicitly includes Qwen and fly brains in permitted execution agents. This supersedes this morning's orientation findings; Qwen's actual standing role Q-014 remains open.
- Q-017 remains OPEN despite dated completion evidence and successful DeepSeek runs. Mark the key-install action completed with that evidence, not an invented owner quotation.
- TODO's scorer claim 'nothing resolves until September 16' is stale: September 12 scorer output contains four resolved estimates. Bridge hourly execution, executor and sentiment setup also have live evidence despite old OPEN/broken paragraphs.
- OPERATING-MAP's unlimited-week Luna promise is unverified. INDEX update date and historical installation/project statuses are not a live health signal.

## Other fragile components
- AgentWorkbench tasks point to removed version-specific PowerShell 7.6.3 WindowsApps executable; scripts still exist outside AI-Shared. Both report 0x80070002. Repair requires inspecting that project's current purpose before reviving its server/scheduler; no automatic revival here.
- AI-Shared Mirror succeeds (September 12 04:30, FAILED 0), but /MIR propagates deletion and is not versioned recovery. Cloud upload/restore remains unproven. Propose dated, secret-filtered snapshots and a restore drill without deleting the existing mirror.
- The backup's exclude patterns are narrower than .gitignore: .pem/.key/.secrets exclusions are not in its task. Audit credential-bearing paths by names before any backup redesign; never print values.

Authored by Codex. Verification results will be appended before completion.

## Verification and remaining boundaries — 13:44 EDT
- Three verifier tests pass: success returns normally; injected runtime and HTTP failures exit 1. No network or queue writes in tests. The ordinary scheduled 13:42 verifier run then completed with result 0 and a reconciliation log.
- Four isolated PowerShell scenarios pass: healthy fixture exits 0; HTTP 500, failed proposer, and stale verifier output each exit 1. Real postboot checker exits 0. This is current health, not proof of unattended reboot recovery. Expected long-lived MCP/bridge processes must now be Running rather than merely Ready with a historic success.
- Bare `python tools/desk.py account` now waits for and returns read-only account output. No order commands run.
- Supabase read-only audit: all nine desk/trade tables inspected have RLS enabled. Proposal updates and desk decisions are gated by desk_owners/auth.uid(); public SELECT is intentional. No schema or row mutation performed. Seven pending rows at inspection; a queue count is a snapshot, not a perpetual health invariant. Database SECURITY DEFINER functions, grants beyond these policies and authenticated-button operation were not exhaustively audited.
- Anonymous Chromium at 390x844: /live-systems/, /live-systems/trades/, /qwen/ all return 200, render real content, report zero page errors and document width 390. Screenshots and DOM text in state/codex-audit-20260912; read-only browser script in tools/tests/audit_public_pages.cjs. Trade desk displays seven pending rows, matching the database snapshot; Qwen heartbeat and account observation are current. No owner controls used.
- PUBLIC CONTRADICTION: trade page says 'Nothing is placed without an explicit yes' despite autonomous Live Wire rows. Suggested copy: 'Queue proposals require your approval. Authorized autonomous agents are labelled separately in the ledger.' Its 'independent probability' claim also needs qualification: the Codex backend launches with -C AI-Shared and automatically inherits workspace instructions, contrary to estimation isolation. DeepSeek is current; do not silently reactivate the Codex research backend before isolating it and guarding stale output files/return codes.
- Proposer event indexing/prior construction and scorer closed-market settlement inference need dedicated validation; market counts inside an event need not be mutually exclusive outcomes. No estimates or market recommendations were produced in this audit.
- Fly Brain reward polling is below the 'no market' and 'match ended' continue paths; settlement processing can be delayed while idle. Together with the cap/holding issues above, this is another reason to finish dry acceptance and repair before considering live mode.
- Protected files matched baseline SHA-256 after the edits: executor 242007191FF8C4074621C700D9BDFFBCB42C40F4E90D720ABAE585E1C440C985; desk-trade 68930ACC76BAFF1E6481A949337EF62AC18821794078B6EE0BBBDD67B9458D1A; fly B4CE7CE6296C14DAEB5A54C0708D3EF8085AA9FEFDD48C22EB23FBA6F58F40CA.
- No project-wide migrations, service restarts, software upgrades, site deployment or historical ledger edits. AgentWorkbench's removed interpreter is outside this workspace and its workload purpose needs checking before restoring execution. The automated Bridge routine still needs to consume the expanded checker; editing its agent area would not update the cloud bot's saved routine.

Priority next: repair Fly Brain accounting/execution acknowledgment before live activation, isolate research entrypoints, then make Bridge's health routine use the expanded checks and add durable ledger replay. Preserve each owner's unresolved decisions.

## Coordination sync
Audit handoff and changed source/tests/own reports copied additively into the existing G:\My Drive\AI-Shared-mirror paths and hash-checked. No /MIR invocation or deletion. This verifies the mounted mirror only; Google's off-machine upload remains unverified. The phone-readable result is in the task response.
