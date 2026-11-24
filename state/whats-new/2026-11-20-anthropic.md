# Anthropic (Claude apps, Claude Code, Cowork, API) - 2026-11-20

## Claude Code 2.1.329 (Nov 19, 2026, shipped after the 2.1.328 entry)
Source: https://code.claude.com/docs/en/changelog
- `/tasks` now lists scheduled tasks, `/loop` wakeups, goals and forks.
- `/code-review` with no target reviews the whole branch against the default branch.
- Fixes: `~/.claude.json` being reset, repeated macOS Keychain sign-outs, `/terminal-setup` corrupting VS Code settings.
- Saved scheduled tasks from older versions mostly need rescheduling in new signed-in sessions.
- A PreToolUse hook that errors no longer refuses a script's tool call. Use `"onFailure": "block"` on hooks that must refuse.
- The automatic retry at the `max_tokens` limit (added in 2.1.326) is removed.
- for Jaron: small. `/tasks` gives one place to see scheduled work. Check that his saved scheduled tasks on the MSI still fire after updating.

## Anthropic news page
Source: https://www.anthropic.com/news
- No posts dated Nov 19 or 20. Newest: Nov 18 IPO pricing, Nov 10 IPO roadshow, Nov 9 Claude Fable 5.2 / Mythos 5.2 (already known).
- for Jaron: nothing for us.

## Not new, still open
- Opus 4.8 fast mode is removed Nov 30, 2026 (move to Opus 5.5).

Checked: Claude Code changelog and the Anthropic news page. No new models, plan/limit or pricing changes found.
