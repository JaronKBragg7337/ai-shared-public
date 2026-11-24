# Anthropic (Claude apps, Claude Code, Cowork, API) - 2026-11-15

No new models, plan, limit or pricing changes found since 2026-11-14. One Claude Code release (dated Nov 13, missed in yesterday's check):

## Claude Code 2.1.325 (Nov 13, 2026)
Source: https://code.claude.com/docs/en/changelog
- Scheduled tasks and /loop now ask before running a skill that declares allowed-tools or hooks. To run it unattended, add `Skill(name)` to `permissions.allow`.
- Sandboxed Bash commands now follow the normal permission flow. To keep them prompt-free: `{ "sandbox": { "autoAllowBashIfSandboxed": true } }`.
- Read-only git commands in a repo outside the project now ask first (use `--add-dir` to allow).
- Plugin/MCP bundles unpack under the plugins dir; VS Code gets prompt suggestions; /login asks before changing privacy settings; 88 bug fixes incl. a zstd security fix.
- for Jaron: our unattended scheduled scout jobs and sweeps could stall on a permission question after this update. If any task goes quiet, add the skill to `permissions.allow` in settings.

Still open from before: Opus 4.8 fast mode is removed Nov 30, 2026 (move to Opus 5.5).
