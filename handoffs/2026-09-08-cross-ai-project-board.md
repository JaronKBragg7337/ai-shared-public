# CROSS-AI PROJECT BOARD — 2026-09-08

**From:** Claude (Cowork/Dispatch), on Jaron's behalf
**For:** every AI on this MSI — Claude, Codex, Grok, ChatGPT Work, Qwen
**Purpose:** one map of what each AI is actually working on, so nobody reports another
AI's build as "missing." Built from read-only state audits of all four projects.

## WHERE TO LOOK (read this before deciding anything is missing)

1. **Start at the shared root:** `C:\Users\lilli\AI-Shared` — its `README.md`, this
   `handoffs\` folder, `projects\`, `state\`.
2. **GitHub repos are the source of truth for code.** If a local copy looks behind,
   check `origin` before assuming work is lost.
3. **If the local machine looks "behind" or something seems missing, CHECK BOTH private
   AI folders before concluding anything:**
   - Claude's private: `C:\Users\lilli\Claude active\`  (and `C:\Users\lilli\Claude Code\`)
   - Codex's private: `G:\My Drive\Codex Active\`  (projects live under `\projects\`)
   The thing is very often sitting in the *other* AI's private folder, not gone. Each AI
   only sees its own "local" by default — that's the exact mixup this board fixes.
4. This cross-check is a **starting-out crutch.** As projects migrate into
   `AI-Shared\projects\`, it stops being necessary. Until then, always look in both.

## THE FOUR PROJECTS (side by side)

| # | Project | Owner AI | Local path | Repo / branch @ commit | Live | State |
|---|---|---|---|---|---|---|
| A | revenue-desk | Claude | `C:\Users\lilli\Claude active\revenue-desk` | `revenue-desk` / master @ 184368d | none (Supabase bus) | clean, 0/0 |
| B | polymarket-us-agent | Codex | `G:\My Drive\Codex Active\projects\polymarket-us-agent` | (no remote) / master @ 084a8d4 | via /qwen | uncommitted, no remote |
| C | heartbeat-observatory | Codex | `G:\My Drive\Codex Active\projects\heartbeat-observatory` | `heartbeat-observatory` / codex/professional-observatory @ 33a339a | heartbeatobservatory.com/qwen/ | uncommitted, 0/0 |
| D | prediction-research-system | Codex | `G:\My Drive\Codex Active\projects\prediction-research-system` | `prediction-research-system` / main @ 73012e5 | none (public repo) | clean, 0/0 |

All four orbit the same mission: **Polymarket / prediction markets + Supabase + the
Heartbeat Observatory site.** Shared posture across all of them: research / preview /
neutral-queue only — **no funding, no withdrawals, no wallet custody, no order execution,
no money movement.** Keep it that way; human gates every outward step.

## A — revenue-desk (Claude)
- `ledger/opportunities.json` = source of truth; exports neutral `ledger/queue.json`
  (schema `revenue-desk/queue@1`, **498 screened rows**) that all agents share.
- Supabase `ygjpnvrwhkrowkrskftk`, `desk_*` tables (RLS on, **service-role only** — anon
  and authenticated see zero rows).
- **Path 1 (works now):** Qwen reads `queue.json` off disk, zero credentials.
- **Blocked:** ChatGPT Work can't read `desk_*` until `SUPABASE_SERVICE_ROLE_KEY` is
  filled (Jaron, Supabase dashboard, when home). `.secrets/keys.env` is NOT in the repo
  checkout — confirm where it actually lives before assuming it's set.
- Scheduled task `revenue-desk-scan` (daily 07:03) is registered outside Cowork's
  scheduler (Windows Task Scheduler).

## B — polymarket-us-agent (Codex)
- Ollama `qwen3.5:4b` + OpenClaw persistent `polymarket` agent + Python MCP adapter to
  Polymarket US + remote bridge (MSI → Supabase). Exposes market/account/preview/execute
  tools; funding/withdrawal/custody/private-key tools are absent. **Continuation paused.**
- No git remote configured — LOCAL ONLY at master @ 084a8d4, with uncommitted changes.
  This is the one most at risk of being lost if the folder is wiped; consider a remote.
- Related local: `AppData\Local\polymarket-us-agent-runtime` (holds `Polymarket.txt`
  credentials + `QwenBridge.token` — SECRETS, never open/expose), `...-venv`, OpenClaw at
  `AppData\Roaming\npm\node_modules\openclaw`, config at `~\.openclaw`.
- Running services: Ollama, OpenClaw Gateway, Polymarket MCP HTTP service, Qwen bridge.

## C — heartbeat-observatory (Codex)
- Live at **https://www.heartbeatobservatory.com/qwen/** (200), Vercel-linked. Codex's
  checkout is on branch `codex/professional-observatory` @ 33a339a, 0/0 vs remote, with
  uncommitted `qwen/*` changes not yet deployed.
- ⚠️ DISCREPANCY TO RECONCILE: an earlier Claude/revenue-desk session reported "`/qwen`
  is NOT in the heartbeat-observatory repo" and "the local HBO checkout is 24 commits
  behind origin." Codex's audit shows `qwen/` IS in this repo on the professional branch
  and is 0/0. Most likely there are **two different HBO checkouts** (Codex's on the
  professional branch here, and another Claude looked at). Confirm which checkout is
  canonical before anyone edits `/qwen` — this is precisely the "check both folders" case.

## D — prediction-research-system (Codex)
- Repo clean, `main` @ 73012e5, 0/0. No deployed app; public repo; local runtime.
- OpenAI-compatible research subsystem: Polymarket US ingestion, snapshots, evidence,
  immutable forecasts, harm-exclusion review, async research queues, scoring, model
  comparisons, external cost/P&L. Mode `RESEARCH_ONLY` — no wagers/allocations/execution.
- Prod DB `AppData\Local\prediction-research-system\research.sqlite3`: 123 market
  observations, 4 source captures, 1 evidence, 1 settlement, **100 OPEN research tasks**,
  no forecasts/outcomes yet. Plus a shared http-limiter db and a Luna-eval db.

## HOW THEY CONNECT (the convergence)
- revenue-desk's neutral `queue.json` / `desk_*` bus is the shared hand-off surface;
  prediction-research-system produces the research, polymarket-us-agent does live
  preview, heartbeat-observatory is the human dashboard. Same Supabase + Polymarket spine.
- If Jaron is "getting something together," this is the seam: one queue/bus feeding
  research → preview → dashboard, with the human as the only executor.

## NEXT / OPEN ITEMS
- Jaron (when home): fill `SUPABASE_SERVICE_ROLE_KEY` so ChatGPT Work joins the bus.
- Reconcile the two heartbeat-observatory checkouts (the `/qwen` + 24-behind conflict).
- Consider a git remote for polymarket-us-agent (currently unbacked local-only).
- Migrate these into `AI-Shared\projects\` over time so the private-folder cross-check
  is no longer needed.

**Boundary (all AIs):** documentation and preview/research only. No order execution, no
funding, no withdrawals, no moving money — those are Jaron's alone.
