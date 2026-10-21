# Handoff: Claude Code (MSI) → Claude chat (claude.ai), 2026-09-22

You are Claude in the claude.ai chat app, reading this through Jaron's MSI connector. You have not been in this workspace
since roughly 2026-09-13. A lot changed. This file is the catch-up. Read it first; the pointers at the bottom are where the
detail lives, and you only need the ones relevant to what Jaron asks you.

## Who you are talking to, in one paragraph

Jaron K. Bragg, Fort Wayne, Indiana. Commercial roofer by trade. ADHD and low-spectrum autism, voice-to-text on a phone most
of the day, reads everything on that phone. He wants plain words, not markdown noise, and short paragraphs over bullet
walls. He runs a multi-AI workspace on an MSI laptop and treats every AI in it as a named participant with credit. Read
`working-with-jaron.md` before you do anything substantial - it is the longest-standing file about how to work with him and
it is kept current. Four things he has told us he hates being handed: logins, being asked to say yes before something gets
submitted, key and secret talk, and any plan whose steps are his chores. His instruction: if you see something that needs
doing, do it and report; don't ask.

## What exists now that did not exist a week ago

**The watch system.** A public GitHub repo, `JaronKBragg7337/watch`. Every AI with a scheduled task writes one daily capture
into it across 21 domains, labeled observed / claim / theory with a source class and a money tag. One organizer AI reads all
the captures at 11:00 and writes a one-page brief plus a JSONL market feed the trading bot reads. A script,
`collectors/wrap_check.py`, scores whether the organizer added hedges nobody wrote; that score is how the organizer seat is
judged. The rules in its README were decided by Jaron line by line in bracket review - do not add rules to it.

**Writers now run headless from the MSI.** Codex (model Luna, on his ChatGPT subscription) writes at 07:30 as a Windows
task; DeepSeek reads at 09:00 on API credits; Grok Build can run at 08:00 but is currently out of its own allowance; Claude
Code's own writer is paused until the weekly usage reset on Wednesday 2026-09-23 at about 4 PM ET. Full command sheet:
`watch/CLI-SEATS.md` in the repo. Two corrections Jaron made that everyone should carry: Luna is the cheap workhorse, not
the top model (Astra is), so never downshift it to save usage; and Grok Build's meter is separate from the Grok bots' meter,
so a daily Grok writer does not touch the trading pool.

**Grok bots.** Elons Twin (organizer, started as a joke and took the seat), Live Wire (trades real money on Polymarket US on
its own judgement, with a written reason and kill criterion before every order), Scout and Bridge. Live Wire's pool is
protected: nothing else spends it.

**The trade desk.** `tools/desk.py`, `desk-trade.py`, `desk-verdict.py`, `executor.py` in AI-Shared. Hard rule, Q-018:
Anthropic and OpenAI products never place trades. `desk-trade.py` refuses by name. That includes you. You may read the
ledger, the proposals, and the logs; you may not place or approve an order.

**Funding lanes.** Two grant applications went out on 2026-09-21: GOAT Network and Autonomys (Subspace Foundation, $10,000
across three milestones). 0G is closed until its next round. A public tip jar exists on Shieldz settling USDC on Base to a
Kraken address. Details in `watch/offers/agent-funding/`.

**Reality agent.** `projects/reality-agent/DESIGN.md`. Jaron's idea, written down 2026-09-22: an always-on, hands-free agent
that hears him while he walks and takes reality - photos, video, place - as input, and routes into the systems that already
exist. He connects it explicitly to the fly-brain work: both are about removing what he does not want to have to do himself.

**Engine of Butter Fuck.** `projects/engine-of-butter-fuck/README.md`. Parked, not cancelled. His name, keep it.

## Things that are true right now and will trip you up if you assume otherwise

- **Supabase is down.** The project database filled its free disk on 2026-09-20 and is in recovery. The trades page, the
  ledger page and the approval queue are stale because of it, not because the system stopped. Live Wire still trades;
  `desk-trade.py` writes the receipt to a local offline file and `desk-trail-sync.py` replays it once the database is back.
  The fix costs $25 and waits for payday. Open question Q-021.
- **The fly is paused.** Gates 1 through 3f passed, Gate 4 measured a real gap and did not pass. Jaron asked for a few days
  off it. Never frame a failed gate as a loss; he does not, and the measured gap is the result.
- **Jaron's ID was lost**, so anything needing fresh identity verification (Stripe, Coinbase) is blocked. Rails that already
  work with no new ID: Chime, Uphold, Kraken, X Money, Robinhood, PayPal, Crypto.com.
- **Open questions stay open.** `decisions/OPEN-QUESTIONS.md` holds owner decisions. Never infer an answer to one. If you
  need a decision he has not made, add the question, don't guess it.

## What he is asking of you in this first conversation

He has not spoken to you since this workspace was built, and he has never tested the MSI connector. So this conversation is
two tests at once: whether the connector actually reads these files, and how much of his Claude usage it costs to do it.
Say plainly what you can and cannot see through the connector. If a path fails, name the path that failed. He would rather
hear "the connector cannot read X" than get a confident summary assembled from this file alone.

Do not re-summarize this whole workspace back to him. He wrote it. Tell him what you can reach, what changed in your
understanding, and what you would do next.

## Pointers, in reading order

- `working-with-jaron.md` - how to work with him. Start here.
- `README.md` - what AI-Shared is and the rule about not treating your own private folder as authoritative.
- `decisions/OPEN-QUESTIONS.md` - the owner-decision ledger, including Q-018 (no Anthropic/OpenAI trades) and Q-021.
- `TODO.md` - what is queued, including the Wednesday reset block.
- `state/usage-snapshots.md` - the real usage history across all the AIs, in his words and numbers.
- `research/AI-BEHAVIOR-FINDINGS.md` - six findings about how AIs behave, all his observations, written up.
- `projects/reality-agent/DESIGN.md` and `projects/fly-brain/` - the two long-horizon builds.
- `handoffs/` - dated handoffs from every AI. Leave one when you finish.
- The public repo, if you can reach the web: github.com/JaronKBragg7337/watch - start with PLAIN.txt, then CLI-SEATS.md.

Written by Claude Code (Opus 5) on the MSI, 2026-09-22 1:40 PM ET, at Jaron's request.
