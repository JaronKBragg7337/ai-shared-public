# Anthropic (Claude apps, Claude Code, Cowork, API) — 2026-10-22

Checked platform.claude.com release notes, GitHub Claude Code releases, anthropic.com/news, and web search for anything
dated since the 2026-10-21 file in this folder (which covered Claude Code 2.1.305/2.1.306 and ruled out Enterprise-only
API additions).

- **October 21 — Claude Duet launched (research preview).** [Anthropic's own writeup](https://claude.com/resources/articles/claude-duet) /
  [CNBC](https://www.cnbc.com/2026/10/21/anthropic-preview-of-claude-duet-personal-ai-agent-take-on-muse-dots.html)
  A new standalone app (web, iOS, Android) where Claude runs as a proactive agent built on Opus 5.5: it sends a morning
  brief, checks your connected apps every few hours on its own, and only pings you when something actually needs a
  decision. Asks for approval before sending messages, paying, signing, or deleting — won't trade securities or move
  money between accounts on its own. Waitlist-gated, US only, Pro/Max subscribers only; no separate price, usage comes
  out of your plan's normal limits.
  for Jaron: this is close to the "reality agent"/always-on idea already in projects/reality-agent — worth a waitlist
  signup to see how Anthropic built the "ping me only when it matters" judgment call, since that's the same problem
  we're solving for him. Not a replacement for anything on the MSI, just worth watching.

- **October 21 — New Claude API version `2026-10-21`, first versioned API release since 2023.** [Platform release notes](https://platform.claude.com/docs/en/release-notes/overview)
  Breaking changes behind an explicit version switch (old `2023-06-01` keeps working, nothing breaks by default):
  `temperature`/`top_p`/`top_k` are removed from the Messages API (requests specifying them get a 400 once you opt into
  the new version); a couple of odd message shapes (documents in assistant turns, citations in user turns) now 400 too;
  some Admin/Enterprise Analytics fields renamed. New major-version SDKs shipped alongside it (Python 2.0, TypeScript
  1.0, Go 2.0, others), now Apache 2.0 licensed instead of MIT.
  for Jaron: nothing to act on unless one of our own scripts calls the Messages API directly with a temperature/top_p
  parameter — those would need to stay pinned to the old API version (default behavior) or get updated. Worth a quick
  grep of our tools/ folder for `temperature=` on raw API calls next time someone's in there, not urgent.

- **October 21 — Claude Code 2.1.307.** [GitHub release](https://github.com/anthropics/claude-code/releases/tag/v2.1.307)
  Adds `/claude-api api-version` to opt a Claude Code session into the new 2026-10-21 API version above. Stops
  double-sending HTTP MCP tool calls on disconnect (only idempotent/read-only tools get retried now — fixes a real risk
  of a tool firing twice). Also: new safety-event telemetry, fixed `CLAUDE_CODE_AUTO_COMPACT_WINDOW`, fixed Ctrl+C in
  the agents view, VSCode startup-hook spinner.
  for Jaron: the MCP double-send fix is the one that matters here — this setup runs a lot of MCP tools/connectors, and
  a tool firing twice on disconnect (e.g. a post or a trade call) is exactly the kind of bug that could cause real
  damage. Ships automatically, no setup change needed.

- **Checked and ruled out as "not new" (search engines keep resurfacing these with wrong October dates):** the Sonnet
  5.5 prompt-cache price cut ($0.20 → $0.10/MTok) is from **October 7**, not this week. Computer Use GA and the
  separate Browser Use tool are from **August 19**. Both already old, already covered in earlier files or simply stale
  by the time they show up in today's results.

No new models dated since October 21. Claude Duet and the new API version are the two genuinely new items today.
