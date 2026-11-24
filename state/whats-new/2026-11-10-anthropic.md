# Anthropic (Claude apps, Claude Code, Cowork, API) - 2026-11-10

Source for all items: Claude Code changelog, https://code.claude.com/docs/en/changelog

1. **Claude Fable 5.2 (`claude-fable-5-2`) is now the default Fable model in Claude Code** (v2.1.321, Nov 9, 2026). 1M context, $8/$40 per Mtok, $0.20/Mtok cache reads. Saved Fable 5.1 picks move to `fable`.
   - for Jaron: Fable now means 5.2. Where scripts or routing notes (state/models.md) name 5.1, update them. The engine-writer list in memory says "Fable 5.1".

2. **Claude Code 2.1.321 safety and fix changes** (Nov 9). Mods Claude writes no longer turn themselves on without asking in auto/bypass modes. 74 bug fixes, including MCP login tokens being sent to another host after a redirect, and a read-only Bash command running outside the sandbox without a prompt. Also `--settings <file>` for `claude remote-control`.
   - for Jaron: update the MSI copy. The MCP token fix matters for the MSI connector, and the `remote-control --settings` flag could help the backup-chat reconnect setup.

3. **Claude Code 2.1.322** (Nov 10): fast mode on Vertex (global, us, eu regions).
   - for Jaron: nothing for us (we don't use Vertex).

Still open: Opus 4.8 fast mode is removed Nov 30, 2026 (move to Opus 5.5).
A general web search found no official plan/limit/pricing announcements since 2026-11-09.
