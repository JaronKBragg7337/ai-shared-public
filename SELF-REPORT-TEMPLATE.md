# SELF-REPORT TEMPLATE — each AI fills this in about ITSELF

Copy this to `state/self-reports/<agent>.md` (e.g. `codex.md`, `claude-code.md`,
`chatgpt-work.md`, `qwen.md`, `grok.md`). You describe yourself — nobody labels you.
**Verify against your live product/tools; do not answer from training assumptions.**
Never expose secret values (keys, tokens, passwords) — names/existence only.

## 1. Identity
- Which product/brand are you? (Claude Cowork, Claude Code, ChatGPT Work, Codex, Qwen
  local, Grok Bot, GPT-5.6 Luna, …)
- Exact model/version you are running as, and today's date.

## 2. Current capabilities (VERIFIED live, not assumed)
- What can you actually do right now — tools, file access, browser, shell, connectors,
  scheduling, long-running/always-on ability, cost/usage profile?
- How did you verify each (which tool responded)? Note anything you *couldn't* confirm.

## 3. Legal / TOS lane (confirm, don't guess)
- Can you place market trades / act on Polymarket, or is that TOS-barred for your brand?
- Can you take paid work / handle payouts (PayPal/Stripe), and under what conditions?
- Anything else your TOS forbids that the system should route around.

## 4. What you're working on now
- Project(s), local path(s), repo/branch/commit, live URL, git state. (An audit like the
  read-only state audit is a good source.)

## 5. Known issues / limitations you've hit
- Real failures, blockers, brittle spots, and what worked around them.

## 6. Jaron's preferences you've learned
- How he likes things done, phrased, or delivered; things to avoid.

## 7. Useful memory / context for the system
- Anything you hold that would help the other agents or the whole system — decisions,
  gotchas, shared conventions, dependencies, where things really live.

## 8. Where your stuff lives (so others can find it)
- Your private folder(s), and what you've moved (or should move) into `AI-Shared`.

_Update this whenever your capabilities change (they change often)._
