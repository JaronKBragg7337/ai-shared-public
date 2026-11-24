# Anthropic (Claude apps, Claude Code, Cowork, API) - 2026-11-17

## Claude Code 2.1.326 (Nov 16, 2026)
Source: https://code.claude.com/docs/en/changelog
- Code Mode now works with agent teams.
- Permissions and safety got stricter:
  - The PowerShell tool asks before more commands, and some are refused.
  - Some tool calls in bypass-permissions mode now ask for approval, or are denied where nobody can be asked.
  - Hooks that return "decision": "block" now hold in more cases.
  - Claude's file tools refuse to write to Claude Code's sign-in files (.credentials.json).
  - Sandboxed commands no longer write to some sensitive home folders by default.
- Plugin uninstall now also deletes the files extracted from the plugin's MCP bundles.
- New startup warning when an --allowedTools / --disallowedTools / --tools entry isn't a complete rule.
- 59 improvements and 233 bug fixes (sign-in, MCP, permissions, terminal UI). I read only the top of the page, so the full list is not reviewed.
- for Jaron: this matters for the unattended scheduled scouts and watch loops on the MSI. The stricter PowerShell and bypass-mode checks could make a headless job stall or get denied. If a scheduled task goes quiet after updating, check this first, and add the rule to `permissions.allow`.

## Not new, still open
- Opus 4.8 fast mode is removed Nov 30, 2026 (move to Opus 5.5).

Checked: the Claude Code changelog and one general web search. The search found no other Anthropic announcements after 11/16: no new models, plan or limit changes, or pricing changes.
