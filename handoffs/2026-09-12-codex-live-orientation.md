# Live orientation — Codex, 2026-09-12

Local Codex desktop task on MSI; no connector. Web clock confirmed 2026-09-12 09:59:45 EDT (America/Indianapolis). Read the requested system documents and newest three handoffs; checked live task state and read-only desk output. No trades, queue writes, service restarts, software upgrades, or site changes performed.

## Verified locally
- Polymarket MCP, Qwen Remote Bridge, Grok Machine MCP and Desktop Commander tasks running. Ports 11434, 18789, 8765 and 3001 listening.
- Trade Verifier and Executor last runs 09:57 returned 0. Trade Proposer last run 09:57 returned 1. Its final log line at 09:57:35 reports a proposed candidate, but no insertion or completion follows. Queue has no pending or approved-unplaced rows. Failure cause NOT established; inspect persistence/error capture next. Maintenance owner: Claude Code's proposer, Codex can investigate.
- Bridge heartbeat through 09:52; Live Wire session through 13:34Z reports no new entry and no open live sports. These are agent reports, not independent browser observation.
- Scout Scorer ran 06:30 result 0. Mirror ran 04:30 result 1; robocopy log confirms FAILED 0, 48 copied. G: is a local Drive mount, cloud upload not verified.
- Paper tasks disabled as requested. Last boot September 10 21:48, so September 11 auto-sign-in changes remain untested by reboot.
- Bare python desk.py calls returned no captured account/queue output in this tool session. Direct venv Python calls succeeded. Avoid interpreting silent output as an empty account.
- Active CLI remains 0.153.4.

## Verified remotely
- Anonymous HTTP GET returned 200 for /live-systems/trades/, /live-systems/, /qwen/. Web search fetch failed internally; direct MSI HTTPS succeeded. Rendered phone layout and browser-fetched live data not verified.
- Official changelog https://learn.chatgpt.com/docs/changelog lists CLI 0.154.0 September 9: Astra picker, experimental worktrees, inline questions, Windows shared background server, plugin refresh and authorization-context fixes. September 5 removed codex mcp-server. September 10 SDK adds ExternalMessage and max/ultra effort. Local CLI is behind. No verified new universal allowance guarantee found.

## Proposed corrections to core; not silently applied
- Q-017 still OPEN although September 11 completed-session notes say DeepSeek key installed and current proposer logs confirm researcher=deepseek. Preserve the supplied historical answer/evidence rather than ask for the key again.
- INDEX agents.qwen may_trade=true and OPERATING-MAP execution rows conflict with Jaron's current restriction to permitted Grok Bots; follow current instruction. Qwen role and literal fly-brain design remain owner decisions.
- TODO contains completed work under old broken/open headings (executor, Bridge wakes, sentiment setup, scorer existence). Latest dated notes and live probes supersede those descriptions.
- OPERATING-MAP's guaranteed week-long unlimited Luna work is not established by current documentation. Do not repeat it as a promise.
- Old CLI/Qwen version claims in agent notes are dated snapshots, not current guarantees.

## Next
Diagnose and repair the proposer failure without submitting an order; verify the repair with non-writing checks first. No estimate or market opinion produced here. Standing-job choices, Qwen role and fly-brain design remain Jaron's; parked decisions stay parked.

Authored by Codex. This handoff is MSI-local; the findings were delivered in chat for phone access.
