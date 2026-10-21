# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-10-21

Checked the Claude Code GitHub releases, platform.claude.com release notes, anthropic.com/news, and web search for
anything dated since the 2026-10-20 file in this folder (which covered Claude Code 2.1.304 and ruled out the old
Philadelphia-police story as not-new).

- **October 20 — Claude Code 2.1.305.** [GitHub release](https://github.com/anthropics/claude-code/releases/tag/v2.1.305)
  - Added `sandbox.allowNestedUserNamespaces` for sandboxed Linux commands, and `CLAUDE_CODE_RETRY_WATCHDOG_USAGE_LIMIT_RECHECK_MS`
    for usage-limit monitoring.
  - Fixed tool search rejections on Vertex, Bedrock, and other cloud providers; fixed `/effort` and `/autocompact`
    settings not applying; fixed worktree and subagent cleanup problems; `/usage` warnings improved; screen reader
    mode fixes; plus bug fixes for Cloud sessions, Code Review, Claude Tag, and the VSCode extension.
  for Jaron: routine reliability patch — nothing to act on, just keeps the MSI's Claude Code current.

- **October 21 — Claude Code 2.1.306.** [GitHub release](https://github.com/anthropics/claude-code/releases/tag/v2.1.306)
  - Fixed `claude -p` inside cloud sessions wrongly reporting "Not logged in" when started without the session's
    environment variables.
  - Fixed a real API error being masked by a misleading "prompt is too long" message (plus an unneeded compaction)
    in sessions with many MCP tools.
  for Jaron: the MCP-tools fix is worth having given how many tools/connectors this setup runs — a real error used
  to get hidden behind a wrong "too long" message, which could've sent us chasing the wrong problem. No setup change
  needed, it ships automatically.

- **October 20 — three Enterprise/Admin-API additions, none of which apply to this setup:** inference hooks out of
  beta for Claude Enterprise orgs; "user profiles" (`/v1/user_profiles`) letting a platform tag API requests by its
  own end customers so Anthropic's safety enforcement can target one customer instead of the whole org; and
  organization webhooks (beta) notifying an org when Anthropic restricts/bans one of its user profiles.
  [Release notes](https://platform.claude.com/docs/en/release-notes/overview)
  for Jaron: these are for companies reselling Claude access to their own end customers — the MSI doesn't do that,
  nothing for us.

- **Checked and ruled out as "new" (all predate the Oct 20 cutoff, already old by the time they showed up in
  today's search results):** Claude Opus 5.5's actual launch (Sept 22), the Claude chat + Cowork merge into one
  "Claude" product ("Claude Convergence," announced Sept 16, rolling out to Pro/Max first), Claude Dashboards/Motion
  beta and Docs/Slides/Design leaving beta (Oct 8), and dynamic workflows for Managed Agents (Oct 9). Search engines
  keep resurfacing these with wrong "October 20" dates in AI-generated summaries — verified actual dates against
  Anthropic's own announcement pages before ruling them out.

No new models, no pricing/plan/usage-limit changes, and no new Cowork features dated since October 20 — only the
two Claude Code patch releases above are genuinely new today.
