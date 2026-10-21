# OPERATING MAP — who does what, and why (TOS-aware)

The system is a team of AIs with **different legal lanes**. The split is set by each
brand's Terms of Service, not by preference. This file is the standing reference; every
agent reads it before picking up work. (Companion: `README.md`, `handoffs/`.)

## Roles are self-described — we don't pick them

No one assigns roles top-down. Roles emerge from what each agent can actually do, in this
order of precedence: **laws first, then each brand's TOS, then live capability, then fit.**
We figure it out as we go — but law and TOS come first, always.

Two rules every agent must honor:

- **Check your OWN current capabilities — don't trust your training.** What you were
  trained on is often days-to-weeks behind what your product can do now (features ship
  almost daily). Before claiming you can or can't do something, verify it against your
  live tools/product and report the real result.
- **Self-report; don't get labeled by someone else.** Each agent writes its own entry
  (see `SELF-REPORT-TEMPLATE.md`) into `state/self-reports/<agent>.md`: which
  product/version you are, your verified current capabilities, the TOS/legal limits you
  confirmed, known issues you've hit, Jaron's stated preferences, and any memory/context
  you hold that could help the system or the other agents. The matrix below is only the
  fixed TOS guardrail — the living detail comes from these self-reports.

## Capability & TOS matrix

| Agent | Brand / kind | Trade on Polymarket? | Earn via other paid work (PayPal/Stripe)? |
|---|---|---|---|
| **Qwen** | local model (on this MSI) | ✅ yes | n/a — market lane |
| **OpenClaw** | local agent/gateway | ✅ yes (executes) | n/a — market lane |
| **Grok Bot** | xAI | ✅ yes | — |
| **Claude Cowork** | Anthropic | ❌ NO (TOS) | ✅ yes |
| **Claude Code** | Anthropic | ❌ NO (TOS) | ✅ yes |
| **ChatGPT Work** | OpenAI | ❌ NO (TOS) | ✅ yes |
| **Codex** | OpenAI | ❌ NO (TOS) | ✅ yes |
| **GPT 5.6 "Luna"** | OpenAI (cheap, always-on) | ❌ NO (TOS) | ✅ yes — the 24/7 worker engine |

**Hard rule:** Anthropic and OpenAI agents **never place trades or move market money.**
Only the market-lane agents (Qwen / OpenClaw / Grok Bot), operated by Jaron, execute.

### ⚠ CORRECTED 2026-09-10 — the column above is narrower than it looks. Read this.

The matrix answers **"executes trades?"** — not "may work on the trading system at all."
An earlier version of this file implied the whole Polymarket lane was off-limits to Anthropic
agents. **That was wrong, it was never verified, and it was repeated for two days.**

**Verified against the actual policy** (<https://www.anthropic.com/legal/aup>, read 2026-09-10):

- There is **no blanket prohibition** on building or operating financial systems, and **no
  dedicated clause** on automated trading, prediction markets, or gambling.
- Finance is a **High-Risk Use Case**, which requires exactly two things: *"a qualified
  professional in that field must review the content or decision prior to dissemination or
  finalization"* (human-in-the-loop) and disclosure that AI helped produce the decision.
- The only financial prohibition is fraud.

**Jaron already satisfies that requirement** — he is the human in the loop, the only executor,
and nothing fires without his approval. That was designed in before anyone checked the policy.

**So the real line, for Claude Code and Claude Cowork:**

| Allowed ✅ | Not done by this agent ❌ |
|---|---|
| Build, verify, monitor, repair the system | Calling `polymarket_place_order` or any submit tool |
| Read balances, positions, orders, telemetry | Moving, funding or withdrawing money |
| Improve tooling, logging, alerting, guards | Deciding what or when to trade |
| Analyse what happened after the fact | Holding keys or custody |

Building the machine is not operating it. **Jaron pulls the trigger; agents build the trigger.**

**Codex and ChatGPT Work: this is Anthropic's policy, not yours.** It is recorded here because
Claude Code verified it for itself. **Do not inherit it — check OpenAI's and write your own
answer into `state/self-reports/<agent>.md`.** Whatever you find, `polymarket_place_order` stays
Jaron's, because that is his decision and not a policy question.

_Lesson worth keeping: this restriction was written into a shared document on day one, believed
by every agent that read it, and repeated by Claude Code all week — about its own rules. Jaron
had a hunch and asked for it to be checked. **A confident sentence in a shared file is not
evidence. Verify claims about your own limits before repeating them.**_

## The two revenue lanes

**Lane 1 — Prediction markets (Polymarket).** Money is made by trading.
- Research: `prediction-research-system` (Codex) — RESEARCH_ONLY, produces forecasts/evidence.
- Preview: `polymarket-us-agent` (Codex/Qwen) — non-submitting previews, telemetry.
- **Execution: Qwen / OpenClaw / Grok Bot ONLY.** Anthropic + OpenAI agents feed this
  lane with research and tooling but never pull the trigger.
- Dashboard: heartbeat-observatory `/qwen/` — the human view.

**Lane 2 — Direct paid work (needs PayPal and/or Stripe connected).** Money is made by
doing jobs and shipping things.
- Done by Claude (Cowork/Code) and OpenAI (ChatGPT Work/Codex/Luna).
- The five paths, from the revenue-desk chat, **ranked by yield per approval** — that is,
  how much money one of Jaron's yes/no decisions unlocks. Ranking matters more than the
  list: every outward step costs one human approval, so a lane that needs a hundred
  approvals to earn what another earns in one is the worse lane even at equal dollars.

  1. **Game jams with cash prizes.** Best fit. Deadline-driven, Jaron already builds games
     fast, and a submission is ONE approval instead of a hundred. Usually no tax-verified
     marketplace account needed to enter. Blocked only by prize discovery — see the itch.io
     gap below.
  2. **Already-published games.** itch.io pages, GitHub Sponsors, Ko-fi against work that
     already exists and is live. Low ceiling, but near-zero ongoing approval cost — it earns
     while the system does other things.
  3. **Asset and tool packs.** `hb-textures`, `hb-harness`, the engines. Packaged once, sold
     repeatedly. CC0-by-default is a help here, not a cost: an unlicensed repo defaults to
     all-rights-reserved, which is the opposite of what Jaron wants, so adding CC0 is more
     aligned with his position than leaving it off.
  4. **Direct coding gigs.** Highest per-unit — the tweet that started this had `$50 coding
     service: offer accepted` as one of its three payouts — but every lead is a message sent
     on Jaron's behalf, so it is approval-heavy and he is the contract counterparty.
  5. **OSS bounties.** LAST, on measurement rather than vibes. See below.
- Same set applies to the OpenAI agents.

**Why bounties rank last — measured 2026-09-08, not assumed.** GitHub had 558 open issues
labelled `💎 Bounty` and 4,280 labelled `bounty`, which looks like a rich market. But all 25
of the *freshest* were agent-practice repos or bounty mills (`bounty-plaza`, `agent-bounties`,
`bounty-hunter-os`, `swarmstatus-bounties`), with identical titles copy-pasted across
unrelated repos, each drawing 17–46 comments within a day — other agents racing. One repo,
`ClankerNation/OpenAgents`, advertised $8k/$7k/$5k/$4k simultaneously, every one unclaimed
for 115 days. The scanner now screens on repo naming, comment pile-on rate, implausible
pay-to-effort, and a repo-level "this board never settles" rule; it removes ~60% of what
GitHub returns. Real payers do exist in the residue — `tenstorrent/tt-metal` at $1,500 with
4 comments is the current best candidate.

**Two known gaps in this lane.** itch.io renders jam pages client-side, so prize amounts
cannot be scraped — `/jam/brackeys-16` returns a ~20 KB shell with no `$` in it at all. All
457 jams are therefore recorded with prize UNKNOWN rather than guessed, which is why the
best lane is currently the least actionable. Finding cash-prize jams needs a different
source. Separately, the desk's ranking sorts on dollar amount without discounting age, so
stale bounties (one is 897 days open) currently outrank live ones.

## Luna as the always-on engine
GPT 5.6 "Luna" has very cheap usage — Codex / ChatGPT Work can drive it to run a single
goal **24/7 for a week without hitting limits**. Use it as the persistent worker/research
role: continuous forecasting, evidence gathering, monitoring, and Lane-2 job execution
that would burn a premium model's budget. It never trades (OpenAI TOS).

## How they help each other
- Luna/Codex research → feeds Lane 1 previews (Qwen) AND surfaces Lane 2 jobs.
- revenue-desk `queue.json` + Supabase `desk_*` bus = the shared board all agents read.
- Claude (Cowork/Code) builds the tooling, sites, and Lane-2 deliverables; ChatGPT/Codex
  do the same; Qwen/OpenClaw/Grok convert Lane-1 research into trades.
- Human (Jaron) is the only executor of money-out steps and the only one who approves
  trades and payouts.

## Open items
- **Lane-2 revenue paths:** Jaron is gathering the full list Claude named (it lived in a
  chat we can't reach from here); add it when he has it.
- **PayPal / Stripe:** not set up yet — and deliberately NOT set in stone. The wiring
  differs for a CLOUD agent (ChatGPT Work) vs a LOCAL one (Codex, Claude Code), and
  folders are still moving. Decide the payment approach per-lane once folders settle;
  don't hardcode a location yet.
- **`SUPABASE_SERVICE_ROLE_KEY`:** fills the bus so ChatGPT Work can read `desk_*`.
- **Roles:** not pre-assigned — they emerge from the self-reports, laws + TOS first.
- **Each agent still owes:** its `state/self-reports/<agent>.md`, and a gather-pass over
  its own folders for issues hit, Jaron's preferences, and useful memory (see template).

## My boundary (Claude, writing this)
I document, plan, and build. I do **not** place trades, connect payment rails, move money,
or handle secret values — those are yours or the permitted local agents'.
