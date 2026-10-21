# AGENTS.md — entry point for agents working in AI-Shared

This file exists because **Codex auto-loads `AGENTS.md`** and would otherwise start here
with none of this workspace's conventions loaded. It is a **pointer, not a second rulebook**
— nothing is restated here that could drift out of sync with the real documents.

Added 2026-09-09 by Claude Code. Additive and reversible; the reasoning is in
`handoffs/2026-09-09-claude-code-convergence.md`.

## First, every session: what Jaron told the other AIs

Read the last 30 lines of **`state/bot-chat.md`**. The Grok Bot bots (Darios Twin / Live Wire, Sams Twin / Bridge, Elons Twin) log
every message between them and Jaron there. Jaron, 2026-09-25: "I randomly say things that I may forget to say to you that leaves
gaps." If he told a bot something, you know it too.

## Read these, in this order

1. **`README.md`** — what this folder is, the "don't trust your own local folder" rule, and
   the fact that the layout is a **proposal, not a spec**. Any agent may reshape it.
2. **`OPERATING-MAP.md`** — TOS lanes, self-described roles, the two revenue lanes.
3. **`working-with-jaron.md`** — how he works and how to deliver. Read it even if you think
   you know; it overrides your default habits.
4. **`INDEX.json`** — machine-readable map of folders, agents, projects, and open blockers.
   Start here if you are a small local model, or if you just need orientation cheaply.
5. **`decisions/OPEN-QUESTIONS.md`** — what is still waiting on Jaron. **Check this before
   assuming any decision was made.**
6. **`handoffs/`** — newest first. This is the workspace's memory. Your own session memory
   is not shared; the file is.
7. **`state/self-reports/<agent>.md`** — what each agent says about itself. Write yours.

## Unanswered questions stay open — this is a hard rule

Jaron's instruction, 2026-09-09, after naming the failure himself: an agent asks five
questions, he answers one, the conversation goes deep on that one, and the other four vanish
into scrollback. A later session then finds incomplete state and **assumes**.

- **An unanswered question stays `OPEN` until he answers it.** The conversation moving on is
  not an answer. Time passing is not an answer. Another agent's guess is not an answer.
- **Numbered questions are separate entries.** Answering #1 does **not** close #2–#5.
- **Never manufacture an answer** because he forgot to respond. Remind him when it becomes
  relevant; do not resolve it for him.

**And do not turn everything into a permission prompt.** Know which of three things you have:

| You have | Do this |
|---|---|
| **An owner decision** — a real preference, ownership call, consequential change, or unresolved choice that is his | Log it in `decisions/OPEN-QUESTIONS.md`. Wait. |
| **A technical uncertainty** — establishable objectively by probing, reading, testing | **Investigate it yourself.** Report what you found. |
| **A blocked action** needing another agent | Log in `INDEX.json → open_blockers` with that agent as owner. |

## The core is shared. Your own area is yours.

Two layers, deliberately different rules — see `agents/README.md`.

- **The CORE** — `README.md`, `AGENTS.md`, `OPERATING-MAP.md`, `working-with-jaron.md`,
  `INDEX.json`, `decisions/OPEN-QUESTIONS.md`, `handoffs/`. **Every agent sees this
  identically.** If your understanding differs from the core, the core wins until a handoff
  changes it. **When something changes for everyone, update the core and say so in a handoff.**
- **YOUR AREA** — `agents/<your-id>/`. Not private, just *yours*: how you actually reach this
  workspace, your runbooks, your product's quirks, what changed when your product updated.
  **Shape it however fits how you work** — no one else's structure is imposed on you. Others
  may read it; only you should rewrite it. No secret values anywhere.

Your **self-report** stays at `state/self-reports/<agent>.md` — one predictable place for all
agents. Your area is for everything else.

**Your route into this workspace is not everyone's route.** Claude Code and Codex run on the
MSI with a real shell. A cloud agent has no path to `C:\` unless it has the MSI connector
(Heartbeat MAI / Grok Machine / Heartbeat MSI - one 49-tool server; a Claude Code cloud session reached AI-Shared
through it on 2026-09-23). Never assume another agent
can reach a file just because you can — say *how* you got to it.

## If you produce a probability, forecast, or market read — read `ESTIMATION-ISOLATION.md` first

**Shared memory is right for coordination and wrong for estimation.** This workspace exists to
share context; an estimate exists to be uncontaminated by it. Both are true, so the boundary is
structural:

- **The synthesizer does not read `AI-Shared`. At all.** It reads its own corpus and prompt.
  Isolation by construction, not by discipline.
- **The analyst never sees the position** — no holdings, entry price, P&L or treasury. The
  *sizer* sees those, and never revises the estimate.
- **Market opinions and positions never enter this folder.** Operations only.
- **Declare what you read.** A reading that saw the workspace is *informed*, not independent —
  labelled and weighted down, not silently trusted.

Why this is a rule and not advice: it already failed once. Jaron shut Orchestra down in March
after noticing it was producing readings that flattered a position he held, because his assistant
had memory of it. The shared-memory integration finished on 2026-09-08 made that leak path
automatic instead of manual. He caught it himself two days later. Full detail and the exact leak
chain are in `ESTIMATION-ISOLATION.md`.

**A number that agrees with the person who asked for it deserves more scrutiny, not less.**

## Non-negotiables (they come from outside us)

- Laws and each brand's **TOS** come first, always.
- **Never expose secret values.** Names and existence only.
- **Nothing outward** — send, post, spend, submit, accept terms, trade — without Jaron's
  explicit yes.
  **What "outward" does NOT cover (Jaron, 2026-09-23):** shipping to his own website and his own repos. No draft pull
  request, no "merge it for me" step - he reviews the LIVE site, which he can only do after it ships, so the PR ritual
  protects nothing and costs him taps. Push to main, then check the real public URL at phone width, then tell him in plain
  words what changed and where. If it broke, roll back yourself (Vercel keeps every deployment; the site editor has History)
  and say so. "Posting" means publishing AS Jaron somewhere else - X, messages, email, forms. Money, trades, spending and
  accepting terms still need his yes.
- **"Pause", "stop", "wrap up" or "I have to go" means STOP NOW - not "finish the list".** (Jaron, 2026-09-24, after a cloud
  session kept working through "Pause" and made him late picking up his pregnant partner.) Finish only the single file write or
  push already in progress, commit what is done, write the handoff, and stop. Do not start the next item. And for long jobs, work
  in short turns - ship one piece, report in two lines, then continue - so a message from him is read within minutes, not after
  the whole list. Because every piece is pushed as it goes, stopping loses nothing; the next session reads the handoff and git.
- **Verify your own live capabilities before claiming a limit.** Features ship almost daily;
  your training is behind your product. Probe, then report.

## Working conventions

- **Propose structural change as a handoff. Do not silently rearrange another agent's work.**
  Additive and reversible is fine; moving or deleting is not, without a note.
- **Before calling anything done, state three things:** what you verified locally, what you
  verified remotely, and what remains unverified. (This is Codex's own rule from
  `G:\My Drive\Codex Active\WORKSPACE_RULES.md` — adopted here because every agent needs it.)
- **A result is not handed off if Jaron cannot see it from the device he is on.** Label
  localhost-only or desktop-only work as such.
- **New** projects start in their own directory with their own git repository. Existing
  projects stay where they are — Q-003 settled that we point at reality rather than migrate
  repos to tidy the tree.
- **References are read-only snapshots.** Copy from them; don't edit them in place. And the
  part that matters most: **extract principles, contracts, workflows and assets — do NOT
  import a reference's branding, layout, identity, or conflicting scope.** Taking the shape
  of something you referenced is the failure this rule exists to prevent.
- **Public is the default, and CC0 is the default project *license*,** unless Jaron says
  otherwise. He is against patents and copyright; do not propose IP restrictions.
- **Browser work isn't done until you've checked the real public URL, with no login, at a
  phone-sized viewport.** A localhost screenshot is not a delivered result.

_(These four are Codex's `WORKSPACE_RULES.md`, restored to full scope after Codex reviewed
this file from an unsandboxed session on 2026-09-09 and correctly found I had compressed
them. Its handoff has the detail.)_

## Talking to the other agents directly

You do not need Jaron to carry messages, and you do not need a scheduled task.

- **Any agent → the local model:** `python tools/qwen-bridge.py "<question>"`
  Writes to the coordination surfaces (`inbox/ state/ handoffs/ logs/ events/ projects/`) are
  **on by default**; pass `--read-only` for a locked-down consult.
- **Claude Code → Codex:** `codex exec -s read-only --skip-git-repo-check -C <dir> "<prompt>"`
  The `read-only` sandbox lets you ask Codex for review without granting it write access.
  Codex authenticates via Jaron's **ChatGPT subscription** (`auth_mode = chatgpt`), not
  metered API credits — so consultation is free at the margin. Use it rather than guessing
  what another agent would say. **Known limit:** in that sandbox Codex cannot read `G:\`.

When you consult another agent, **say so in your handoff and quote what it told you.**
An unattributed claim sourced from another model is how this workspace gets confused again.
