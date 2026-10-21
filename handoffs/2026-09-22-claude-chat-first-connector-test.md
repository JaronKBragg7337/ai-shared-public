# Handoff: Claude chat (claude.ai, Opus 5.5) - first Heartbeat MAI connector test, 2026-09-22 ~2:05 PM ET

## Connector
- Heartbeat MAI works from Claude chat. 49 tools listed. The earlier failure (~1:45 PM) was the connector's sign-in in the
  Claude app's Connectors settings ("needs reconnect"), not the MSI. Jaron reconnected it from his phone.
- Read with no failures: handoffs/2026-09-22-claude-code-to-claude-chat.md, working-with-jaron.md,
  decisions/OPEN-QUESTIONS.md, projects/reality-agent/DESIGN.md (about 89 KB total).
- The Google Drive "AI-Shared-mirror" copy is the nightly 08:30 UTC robocopy; it did not have today's files. Don't treat it as current.

## Supabase check (read-only, for Q-021)
- Management API: project ygjpnvrwhkrowkrskftk status = ACTIVE_HEALTHY.
- SQL through the Supabase MCP failed twice: "Client network socket disconnected before secure TLS connection was established".
- So the dashboard label says healthy but the database is not accepting connections yet. Q-021 still stands. Nothing was written.

## Not done
- Did not read the watch repo, AI-BEHAVIOR-FINDINGS, usage-snapshots, or FLY-BRAIN.
- No trades touched (Q-018).
