# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-10-24

Checked the Claude Code changelog, platform.claude.com release notes, support.claude.com release notes, anthropic.com/news,
and web search for anything dated since the 2026-10-23 file in this folder (which covered the bypass-permissions `rm`/`rmdir`
block, Claude Models on Google Cloud, and Anthropic donating Agent Skills to the Agentic AI Foundation).

- **October 23 — Claude Code 2.1.310.** [Changelog](https://code.claude.com/docs/en/changelog)
  Two fixes worth knowing about for how this crew runs Claude Code unattended:
  - An MCP tool call that times out in a non-interactive session while the server is still waiting for an answer
    (elicitation) now tells Claude plainly "no answer came, don't repeat the call" instead of leaving it to guess and
    maybe fire the same tool twice.
  - Compaction after a "Prompt is too long" error used to keep too much dense text and could cause the very next
    message to fail the same way; that's fixed. Also: better memory use during compaction of very large transcripts.
  Everything else in this release (Monitor tool on Bedrock/Vertex/Foundry, Enterprise custom-role permissions for
  cloud sessions, VS Code panel fixes) is Enterprise or Bedrock/Vertex-specific — not how this setup connects.
  for Jaron: both top fixes land squarely on the way this crew works — long-running sessions (the one he keeps open
  for weeks) and lots of MCP/connector calls (Grok Bot, RunPod). The double-call risk on a stuck MCP call going away
  matters most since a repeated call could mean a repeated trade or post; ships automatically, nothing to change.

- **Checked and ruled out:** the Anthropic S-1/IPO filing (reported as early as Oct 23) is finance news, not a
  product change — same call as yesterday's file. The Claude Cowork "double limits" and "Cowork on web/mobile"
  stories that keep surfacing in searches are old (June and July 2026), not new this week — search engines keep
  resurfacing them with misleading dates. "Enterprise unifies Claude chat and Cowork" (Oct 23) is Enterprise-plan
  only, doesn't apply to Pro/Max. No new model, no new Cowork feature on Pro/Max, no plan/pricing/usage-limit
  change confirmed since October 22.

Nothing urgent, nothing that needs a phone buzz. The two 2.1.310 fixes are the only real item, and they're both
"already working better" with no setup change needed.
