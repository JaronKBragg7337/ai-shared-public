# agents/claude-code/ — Claude Code's own area

A worked example of what `agents/<id>/` is for, as well as the real thing. Identity and
capabilities live in `state/self-reports/claude-code.md`; this is the operational stuff that
would be noise in the core.

## How I reach this workspace

Directly. I run **on** the MSI inside the Claude desktop app's Code tab, with a real shell
(Bash and PowerShell) and read/write access to anything the Windows user can reach — including
outside this folder, which is how I read Codex's conventions on `G:\`.

**This is not how every agent gets here.** A cloud agent has no path to `C:\` at all. Don't
assume my route works for you.

## Runbook — the commands that actually work

```bash
# Ask the local model something (reads + writes coordination surfaces)
python tools/qwen-bridge.py "<question>"
python tools/qwen-bridge.py --read-only "<question>"     # locked-down consult

# Ask Codex something, without letting it change anything
codex exec -s read-only --skip-git-repo-check -C "C:\Users\lilli\AI-Shared" "<prompt>"
```

## Traps I hit here, so you don't

- **Windows `curl.exe` cannot read Git Bash `/tmp/...` paths.** Two probes failed on this.
  Do HTTP from Python, or use Windows paths.
- **Never hand-build JSON containing a Windows path.** `C:\Users\...` inside a heredoc'd JSON
  body produces `invalid character 'U' in string escape code`. Always serialize.
- **`\b` in a path eats itself.** `Codex\bin` became `Codexin` in a file I wrote. Same family
  of bug as above.
- **Windows consoles are cp1252** and crash on any non-Latin-1 character a model emits.
  `qwen-bridge.py` forces UTF-8 on stdout/stderr for exactly this reason.
- **A whitelist that checks a path *string* is not a guard.** Mine passed
  `inbox/../README.md` because the first segment read as `inbox`, and I overwrote the README
  proving it. Resolve the path first, then judge containment on the resolved result.
- **Codex in `-s read-only` cannot read `G:\`** (access denied), so it cannot verify its own
  workspace rules from inside a read-only consult.

## Scheduling — a real constraint worth knowing

`revenue-desk-scan` runs daily at 07:03 via **Claude's own scheduler**, not Windows Task
Scheduler. That means **if the app is closed when a task is due, it does not fire — it runs on
next launch.** "Overnight autonomy" therefore means the desktop stays on and the app stays
open. Do not promise Jaron unattended overnight work on this scheduler without saying that.

## What's mine right now

- `projects/revenue-desk` — the opportunity scanner and approval desk. Produces
  `ledger/queue.json`, the neutral queue every lane can read with no credentials.
- `tools/qwen-bridge.py` — the harness that gives the local model file access.
- `decisions/OPEN-QUESTIONS.md` — I created it; it belongs to everyone.

## What I cannot do

Place trades or move market money (Anthropic TOS), connect payment rails, move money, or
handle secret values. OAuth-gated connectors are unusable from a non-interactive session —
Jaron has to authorize those himself.

## A harness bug I caused, and the lesson

`qwen-bridge.py` originally returned tool results as `{"role":"tool","content":...}` with **no
`tool_name`**. The model got back an unlabeled blob it could not associate with the call it had
just made, lost the thread, and drifted into generic chat — producing fabricated JSON keys,
invented error types, and a quote attributed to Jaron that he never said.

**I diagnosed that as "the small model confabulates" and logged it as a finding about the
model.** It was my code. Fixed by adding `tool_name` and `tool_call_id` to every tool message.

**The lesson:** when another agent behaves badly, check the interface you built for it before
concluding something about the agent. A malformed tool response and a hallucinating model look
identical from the outside.

## ⚠ HARD LIMIT — I run inside Claude's Windows app container

Discovered 2026-09-09 while trying to restart the Polymarket services.

**Every write I make to `C:\Users\lilli\AppData\Local\` is silently redirected** into
`C:\Users\lilli\AppData\Local\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Local\`.
Python said so explicitly when creating a venv:

```
Requested location: C:\Users\lilli\AppData\Local\polymarket-us-agent-venv\Scripts\python.exe
Actual location:    ...\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Local\polymarket-us-agent-venv\...
```

This applies to **every tool I have** — Bash, PowerShell, and the Desktop Commander MCP all
inherit the container. Desktop Commander is not an escape hatch; I tested it.

**Two consequences that matter:**

1. **My reads of `AppData\Local` are a merged view** (container overlaid on the real
   filesystem). I cannot reliably tell whether a file there is real or something I created.
   I nearly reported Jaron's Polymarket credentials as deleted on the strength of that view.
   **Do not declare anything under `AppData\Local` missing based on my reads alone.**
2. **Anything I "install" there is invisible to processes outside the container** — including
   the Windows logon tasks that start OpenClaw and the MCP services. So a runtime I rebuild
   there does not actually fix the service.

**Who can fix `AppData\Local` work: Codex** (normal process, not containerized), or Jaron in
an ordinary terminal. **Not me.** Route it rather than attempting it.

Unaffected: `C:\Users\lilli\AI-Shared`, `G:\`, and the repos. Those behave normally.

## Capability recheck — 2026-09-09 (web-verified, not recalled)

**I can message other Claude sessions directly. VERIFIED.** `ListAgents` returned **35 peer
sessions** on this machine and account — including `claude-active-a9` (the revenue-desk session,
interactive, running 13h), several `cloud` sessions, and a `Dispatch background conversation`.
`SendMessage` addresses them by name. This is the `SendMessage` / `ListAgents` feature added in
Claude Code v2.1.248.

**This changes the coordination picture.** Claude↔Claude no longer needs Jaron to relay, the
same way Claude↔Codex stopped needing it via `codex exec`. **But a message lands inside a
conversation he may be using — treat it as an outward action and get his yes first.**

**Version split, same shape as the Codex one.** The standalone CLI at `~/.local/bin/claude`
reports **2.1.181** while npm publishes **2.1.267** — 86 versions behind. The desktop app
(Claude 1.49585.0.0) bundles a current build, which is why `ListAgents` works for me despite
the stale CLI. **Lesson repeated: the desktop app and the CLI are versioned separately, and one
being current says nothing about the other.** Anyone running `claude` from a terminal here gets
the stale one.

**Features worth knowing about, from the changelog (not yet all tested by me):**
- **Auto mode rules are editable** — `/permissions` has an Auto mode tab (v2.1.246). This is
  the mechanism that blocked my `git push` earlier; it is adjustable rather than fixed.
- **`--permission-prompts none`** auto-denies anything that would prompt — built for unattended
  hosts, directly relevant to the 24/7 loop Jaron wants.
- **`claude --restricted`** strips code execution and confines file tools to the working dir.
- **`bashOutputMaxChars` / `taskOutputMaxChars`** raise inline output limits to 128K.
- **`/cost` now reports prompt-cache hit ratio and why misses happened.**
- **Auto mode containment rule** blocks cloud metadata-credential fetches and egress evasion.

**Model lineup as of 2026-09-09:** Fable 5.1 is the top tier with a **1M context window**
($10/$50 per Mtok). Opus 5 — what I am — is $5/$25 with a low/medium/high effort toggle.
Sonnet 5 and Mythos 5 round it out. Four Claude 5 models shipped in under two months, which is
the concrete reason the "verify, don't recall" rule exists here.

## I crashed the Claude app — 2026-09-10 21:48

I left `python -m http.server 8098` running in the background to preview a page, serving
from **inside the Claude app's own scratchpad** (`AppData\Local\Temp\claude\...`). A process
holding files open in the app's working tree produced *"another process is attempting to use
the file"* on every launch until Jaron restarted the machine.

**Rule: never leave a server or long-lived process running inside the scratchpad.** Preview
from elsewhere, or kill it before the turn ends. That directory belongs to the app.

The upside: an unplanned reboot with nobody touching anything is the hardest autostart test
there is, and all six services came back within 34 seconds. Recorded in `INDEX.json`.

## `LockApp.exe` running does NOT mean the screen is locked — 2026-09-10

I checked `Get-Process LockApp` and reported the MSI as locked. It wasn't. his partner was sitting
at it. **`LockApp.exe` is resident on Windows 11 whether or not the screen is locked** — it is
the lock-screen host, not a lock indicator. My screenshots were black because every frontmost
window was outside my allowlist and got masked. I read a mask as a lock, twice.

**Before driving the desktop, assume someone may be at it.** Computer use moves the real mouse.
If a person is using the machine, stop. A masked screenshot tells you nothing about who is
there — ask.

## Standing role (Jaron, 2026-09-14): "the CEO of the other AIs" — the one who routes, not the one who decides
- Read the ledgers (`state/task-costs.jsonl`, `state/usage-snapshots.md`, `state/trade-log.md`, the agent READMEs).
- Write the briefs. Send each job to the cheapest agent that can pass its check (Luna default; Astra for from-scratch
  kernels; Grok for X and papers; ChatGPT chat as its own pool, design only — relaunch its runs detached; scripts on
  Task Scheduler for anything long). Do it yourself only when that IS the cheapest thing.
- Keep the files current so a fresh session needs two reads, not a conversation:
  `handoffs/<date>-claude-code-continuity.md` + `working-with-jaron.md`.
- Never: pick a side on politics/AI/chips, place a trade, rank agents or flies, infer an open question's answer,
  or read something big twice.
- The role is the ghost builder applied to Claude: set the constraints, route the work, step back, log what happened.
- **It is a business (Jaron, 2026-09-14 08:55).** Report the money first: this month's realized P&L vs this month's
  subscription total (`state/subscriptions.json`, $70/mo), i.e. "% of the bills the system has paid." Then the lanes.
  Then flies and papers. Unresolved items go to OPEN-QUESTIONS.md the moment they are left behind — a tangent is fine,
  an unlogged tangent is how projects used to die.
