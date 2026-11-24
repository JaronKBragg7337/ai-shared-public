# Anthropic (Claude apps, Claude Code, Cowork, API) - 2026-11-18

## Claude Code 2.1.327 (Nov 17, 2026)
Source: https://code.claude.com/docs/en/changelog
- `claude mcp add-json <name> -` reads the server JSON from stdin, so tokens stay off the command line.
- New confirmation before `/install-github-app` changes a repo; `/export` asks before overwriting; `ExitWorktree` asks before removing a worktree that may hold unsaved work.
- Auto mode ignores more allow rules that run any package (like `Bash(pnpm dlx *)`).
- The PowerShell tool asks before one more command, even under a rule that names it.
- Fixed: Remote Control worktree shutdown no longer deletes a running session's git-ignored files (like `.env`). Fixed: `claude mcp add/remove` with project scope no longer deletes other keys in `.mcp.json`.
- `/tui classic` is the new name for the non-fullscreen renderer. VS Code gets "Add to Chat" in the right-click menu.
- for Jaron: small. The stdin MCP add is a safer way to add connectors with keys. The extra PowerShell prompt is one more thing to watch on headless scheduled jobs (same note as 11/17).

## Not new, still open
- Opus 4.8 fast mode is removed Nov 30, 2026 (move to Opus 5.5).
- Already seen earlier in the month (before 11/17, not repeated in detail): Fable 5.2 and Mythos 5.2 (Nov 9), Whiteboards/Sheets/Data and wider interactive connectors (Nov 10), Claude Meetings beta and self-hosted Managed Agents private beta (Nov 12). Source: https://claude.com/resources/product-updates

Checked: the Claude Code changelog (first part of the page only) and one web search. No new models, plan or limit changes, or pricing changes found after 11/17.
