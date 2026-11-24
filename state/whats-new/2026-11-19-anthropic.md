# Anthropic (Claude apps, Claude Code, Cowork, API) - 2026-11-19

## Claude Code 2.1.328 (Nov 19, 2026)
Source: https://code.claude.com/docs/en/changelog
- Interactive sessions with no permission mode set now start in auto mode. Auto mode also reaches Opus 4.6 / Sonnet 4.6 on Bedrock, Google, Foundry.
- MCP tool hooks accept `"onFailure": "block"` (a hook that fails blocks the action).
- `/code-review` now reports only bugs and CLAUDE.md violations on most models; use `/simplify` for cleanups.
- UserPromptSubmit hooks no longer run on Code Mode script output (use a PostToolUse hook with `updatedToolOutput` to redact).
- `/bug` asks Yes/No before sending. If the sandbox can't start, the next sandboxed Bash command is refused with a clear message.
- 91 bug fixes.
- for Jaron: small. Starting in auto mode by default means fewer approve prompts, which fits his "no approve buttons" rule. `onFailure: block` is a hard-limit tool for hooks.

## Not new, still open
- Opus 4.8 fast mode is removed Nov 30, 2026 (move to Opus 5.5).

Checked: Claude Code changelog (first part) and one web search. No new models, plan/limit, or pricing changes found after 11/18.
