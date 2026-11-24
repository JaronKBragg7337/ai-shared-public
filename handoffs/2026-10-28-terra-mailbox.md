# Handoff 2026-10-28 — AI mailbox part 1

- Terra created public.ai_mailbox in Heartbeat Supabase with admin-only site read/write and service-role access; anonymous read denied. SQL is in site repo sql/ai-mailbox.sql. A single test message from codex to claude is new.
- MSI tools/mailbox.py has send/list/read/mark-done; commits 664f1aa and 062a319. Send and list verified against live database; read and mark-done remain unverified.
- Site commit e8cf5d0 pushed to main from clean worktree. Vercel production deployment was building; first live request returned 404. Verify https://heartbeatobservatory.com/admin/mailbox/ once ready, signed-in flows and phone-width WebKit. Existing checkout has unrelated work; do not overwrite.
- Individual AI authentication and MCP access and the helper loop are future work; this part uses shared MSI service credentials and site admin login.
