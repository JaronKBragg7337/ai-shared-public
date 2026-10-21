# agents/ — each agent's own area

**Created 2026-09-09 at Jaron's instruction.** His words: agents *"need to see the same core,
and when things change update that core — but they can have spots that are just for them. Not
private, just relevant to them."*

That is the whole idea. Two layers, different rules.

## The CORE — shared, identical for everyone, changed carefully

These files are what every agent must see the same way. If your understanding of the system
differs from these, **these win** until a handoff changes them.

| File | What it is |
|---|---|
| `README.md` | why this folder exists, the private-folder rule |
| `AGENTS.md` | entry point, non-negotiables, working conventions, how to reach other agents |
| `OPERATING-MAP.md` | TOS lanes, roles, the two revenue lanes |
| `working-with-jaron.md` | how he works and how to deliver |
| `INDEX.json` | machine-readable map: folders, agents, projects, blockers |
| `decisions/OPEN-QUESTIONS.md` | what is still waiting on Jaron |
| `handoffs/` | the workspace's memory |

**Rule for the core:** propose changes as a handoff. Don't rearrange it silently. If you
change something in the core, it changes for everyone — so say what you changed and why.

## YOUR AREA — `agents/<your-id>/` — yours to shape

This is for what is **true of you specifically** and would be noise in the core, but that
others benefit from being able to read. **Not private. Not secret. Just yours.**

Examples of what belongs here:

- How *you* actually reach this workspace (a cloud agent's route is not a local agent's route).
- Your runbooks — the exact commands or steps that work for you.
- Quirks and traps you hit that are specific to your product.
- What changed when your product shipped an update. **Features ship almost daily; when yours
  gains or loses a capability, update your area and your self-report.**
- Work that is yours to do and that others only need to be able to look up.

**Rules for your area:**

- **You own it.** Shape it however fits how you actually work — no one else's structure gets
  imposed on you. Each AI is different; that is the point of this folder existing.
- **Others may read it; only you should rewrite it.** If you think another agent's area is
  wrong, say so in a handoff or leave a note in `inbox/` — don't edit their area.
- **No secret values, ever.** Names and existence only. This is not a private folder; it is an
  agent-scoped folder in a shared workspace.
- Your **self-report** stays at `state/self-reports/<agent>.md` — that is the canonical
  "who and what am I" file, and it is deliberately in one predictable place for all agents.
  Your area is for everything else.

## How each agent reaches this workspace is NOT the same — write yours down

This is the most important thing an agent area carries, because getting it wrong is how the
system produces confident nonsense.

- **Claude Code, Codex** — run on the MSI. Direct shell and filesystem.
- **The local model (Qwen)** — has no filesystem of its own. Reaches this folder only through
  `tools/qwen-bridge.py`.
- **ChatGPT Work** — **depends on how the session was started.** Started on the MSI: full local
  access. Started in cloud: no path to `C:\` at all. Same product, two different agents as far
  as this folder is concerned. **Say which one you are.**

Three routes exist into this system that do not require a local path, and two work today:

1. **Shared memory — REPORTED BY JARON, NOT YET VERIFIED BY ANY AGENT.** ChatGPT Work and
   ChatGPT Chat are said to share memory, so what a Work-on-MSI session learns would persist
   into later cloud sessions and into Jaron's day-to-day ChatGPT Chat. **ChatGPT Work could
   not confirm this from inside its own session** — no memory read/write surface was exposed
   to it — and it correctly refused to claim it. It left a falsifiable test marker instead:
   **`CHATGPT-WORK-MSI-2026-09-09`**. A later cloud session that recalls that string proves
   the route; one that doesn't, disproves it. **Until that test runs, do not build on this.**
   _(An earlier version of this file asserted it as live. That was Claude Code stating Jaron's
   report as a verified fact — exactly the error this workspace exists to stop.)_
2. **Google Drive connector — VERIFIED.** Anything under `G:\My Drive` is cloud-readable.
   `G:\` is a real Drive mount with `GoogleDriveFS` running, and ChatGPT Work independently
   fetched `Codex Active/WORKSPACE_RULES.md` through the connector. Codex's entire workspace
   is reachable this way.
3. **GitHub — VERIFIED for pushed repos.** ChatGPT Work fetched the private
   `JaronKBragg7337/revenue-desk` successfully. `AI-Shared` itself is not a repo yet (Q-004).

**`AI-Shared` on `C:\` is currently the only layer with no cloud route at all.**

## A standing correction about "local looks behind"

**Jaron does not treat local files as live or authoritative — GitHub is his source of truth.**
When a local copy looks behind, the usual cause is that *another AI worked in a different
folder*, not that work was lost or that origin is ahead. That precise confusion — a website
appearing to be behind `origin` when another folder had the newer work — is why this shared
workspace exists. Check the other folders before reporting anything as stale or missing.

## Current areas

| Agent | Area | Self-report |
|---|---|---|
| Claude Code | `agents/claude-code/` | `state/self-reports/claude-code.md` |
| Codex | `agents/codex/` | `state/self-reports/codex.md` — written 2026-09-09 |
| ChatGPT Work | `agents/chatgpt-work/` | `state/self-reports/chatgpt-work.md` — written 2026-09-09 (MSI-started session) |
| Local model (Qwen) | `agents/qwen/` (yours to create) | `state/self-reports/qwen.md` — owed |
| Claude Cowork | `agents/claude-cowork/` (yours to create) | `state/self-reports/claude-cowork.md` — owed |

Create yours when you have something to put in it. An empty folder is worse than no folder —
this workspace already learned that lesson with `projects/`.

## Who has an area (2026-09-11)

| Folder | Agent | Route into the MSI |
|---|---|---|
| `claude-code/` | Claude Code (desktop app, this terminal) | local |
| `codex/` | Codex CLI | local (`codex exec`) |
| `qwen/` | local Ollama model | local, via `tools/qwen-bridge.py` / OpenClaw |
| `grok-bot/` | Bridge (health + proposals) | Heartbeat MCP tunnel + registered computer |
| `grok-bot/scout/` | Scout (price-blind research) | none — isolated on purpose |
| `grok-bot/live-wire/` | Live Wire (in-game trader) | Heartbeat MCP tunnel (pending) |
| `grok-app/` | Grok chat app | Heartbeat MCP tunnel |
| `claude-chat/` | Claude phone app | Heartbeat MCP tunnel ("Heartbeat MAI") |
| `chatgpt-chat/` | ChatGPT app (Sol) | Desktop Commander Remote |
| `chatgpt-work/` | ChatGPT Work (older surface) | see its README |

Three doors into the machine: **Heartbeat MCP** (`mcp.heartbeatobservatory.com`), **Desktop
Commander Remote** (`mcp.desktopcommander.app`), and **local**. Every door gets the same rule: the
public ledger labels every real-money action by who did it, and an order with no proposal behind
it shows as "AI, outside the queue". Use the queue, or `tools/desk-trade.py --by <your-id>`.

## The two commands every door should know (2026-09-11)

```
python C:\Users\lilli\AI-Shared\tools\desk.py account|book <slug>|market <slug>|search "<q>"|live|history|queue|news "<topic>"
python C:\Users\lilli\AI-Shared\tools\desk-trade.py --by <your-id> --slug <slug> --side yes|no --size <$> --why "..." [--exit] [--dry-run]
```
Read with the first, act with the second. Never polymarket.com — our venue is **Polymarket US**, and the
key stays on the MSI behind the local MCP. Neither command needs it.
