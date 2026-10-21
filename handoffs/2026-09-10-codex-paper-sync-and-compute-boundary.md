# Codex — Paper Sync registered; autonomous rehearsal held

Paper Sync is registered and running: MSI\lilli AtLogOn, PT45S delay,
StartWhenAvailable, battery allowed, IgnoreNew, unlimited duration, 999 one-minute
failure retries. It uses tools/run-paper-sync.ps1 and the existing --loop 120 command.
Added explicit propagation of the Python exit code to the wrapper so fatal failures
can trigger Task Scheduler retries. The Python loop catches individual sync errors
and retries internally after sleep; these do not make the task fail.

Stopped only the re-verified ad-hoc paper-sync.py process 26712 and started the task.
New task started 2026-09-10 16:43:45 local; remote paper_state.synced_at advanced to
2026-09-10T20:43:47.203092+00:00. Exactly one paper-sync Python process observed.
No schemas/RLS/credentials/live agent settings changed. Supabase skill used to check
the existing API path; no Supabase feature or policy was implemented.

IMPORTANT: 120 seconds is the sleep AFTER each sync, not a strict two-minute deadline.
Market-data lookup and HTTP work add duration, and errors can delay updates.

Autonomous Qwen paper operation NOT enabled. Direct config probes show both live
polymarket and polymarket-paper use ollama/qwen3.5:4b at http://127.0.0.1:11434.
The separate gateway protects config/tool/session separation, not compute availability.
A continuous paper inference loop can contend with funded live requests. Jaron said
to stop if a change could affect the funded stack. Await Q-012 before starting it.
No trading prompt, cadence, size/frequency rules, or autonomous orders were introduced.

Another gap to cover before claiming full rehearsal visibility: existing paper-sync
publishes state, positions, and trades only. It does not publish Qwen reasoning,
no-trade decisions, model/tool errors, or pending-order lifecycle events. Claude's
dashboard needs those operational event surfaces for Jaron's 'everything it does'
requirement. This was not silently treated as already implemented.

Locally verified: registration/readback, task running, single sync process, live config
SHA256 unchanged D7D2997AB5F9C2CA6094E5A0D0D37F1BEE3D4A36EFA27131FA9AA41B6A43239E.
Remotely verified: paper_state timestamp after the scheduled task start.
Unverified: new task cold boot, sustained sync cadence, full dashboard event visibility,
and autonomous rehearsal (not started). No model/market estimates produced.
