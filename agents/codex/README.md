# agents/codex/ — Codex's own area

This area contains Codex-specific operating notes. It is shared and readable by the other
agents, not private. Identity and current capabilities live in
`state/self-reports/codex.md`; this file holds the runbooks and product quirks that would
clutter the shared core.

## How I reach the workspace

Codex runs on Jaron's MSI. An unsandboxed Codex task can read and write the local shared
workspace at `C:\Users\lilli\AI-Shared` and the Google Drive mount at
`G:\My Drive\Codex Active`. A nested `codex exec -s read-only` task can read the C: workspace
but cannot open G:. Always state which route produced a fact.

The local CLI currently resolves to the Scoop shim first:

```powershell
where.exe codex
codex --version
Get-Command codex -All
```

This desktop process exposes both the Scoop shim and the Codex desktop runtime through
`PATH`; both report `0.153.4`. Do not resurrect the stale claim that only one executable
is path-resolvable.

## Runbooks

### Orient before working

Read the shared core, then the newest handoffs, then the relevant agent self-report. Treat
`INDEX.json` as a map, not as permission to edit another agent's project. For a completed
handoff, state what was verified locally, remotely, and remains unverified.

### Consult Qwen

Use the bridge from the shared root:

```powershell
python tools/qwen-bridge.py --read-only --quiet "<question>"
python tools/qwen-bridge.py "<task>"
```

The first command is a locked-down consult. Qwen may still emit a `write_file` request when
prompted to review; the bridge must deny it in read-only mode. Inspect the resulting files
and treat the final answer as model output, especially when it ignores a requested format.

### Inspect a project without changing it

Use explicit paths and capture the state before touching anything:

```powershell
git -C "G:\My Drive\Codex Active\projects\<name>" status --short --branch
git -C "G:\My Drive\Codex Active\projects\<name>" remote -v
git -C "G:\My Drive\Codex Active\projects\<name>" log -1 --oneline --decorate
```

For references or parallel checkouts, compare `git ls-tree`, `git log --all -- <path>`,
and fresh `git ls-remote` output. Do not edit a reference snapshot as a shortcut.

### Polymarket project preservation

As of 2026-09-10, the G: source has origin at
`https://github.com/JaronKBragg7337/polymarket-us-agent`, public and CC0. Local master and
origin/master match `6f95a1f`; tracked working tree is clean. Credentials, backup files,
and session memory are excluded. Ten unit tests passed before the authorized checkpoint
and push. Recheck status before further work; this is a dated observation, not a guarantee.

### Heartbeat Observatory `/qwen`

As of 2026-09-10, **main is the canonical production branch**, containing `/qwen/` at
merge `959f289`. The push automatically deployed; all eight requested public pages match
the merge. Earlier promoted feature-branch deployments did not change Vercel's production
branch setting. The older G: checkout's uncommitted continuation work remains untouched;
reconcile it deliberately before future edits. The C: state/hbo-verify-20260910 clone is
an audit checkout, not a project migration. See the dated production-and-backup handoff.

### Qwen 24/7 runtime

The C: primary service deployment is:

- Runtime: C:\Users\lilli\AI-Shared\runtime\polymarket-us-agent\
- Venv: C:\Users\lilli\AI-Shared\runtime\polymarket-us-agent-venv\
- Tasks: Polymarket MCP and Qwen Remote Bridge, both MSI\lilli AtLogOn.

The bridge waits for loopback ports 8765 and 18789 before launching. The G: project
is the source mirror and backup; it is not a boot path. A measured Task Scheduler
probe showed that the old AppData\Local venv is not visible from the scheduled context
even though an interactive unsandboxed Codex shell can see it. Keep runtime and venv
paths on C: for boot reliability; keep source and credentials mirrored or backed up
without exposing their values.

## Product quirks and current traps

### September 12 audit update

See `handoffs/2026-09-12-codex-system-audit.md` before acting on older status below.
`tools/postboot-check.ps1` now includes periodic pipeline jobs and stale output checks.
`tools/desk.py` waits for its Windows venv child so shell callers receive output and exit status.
The active CLI was still 0.153.4; official 0.154.0 exists. Installed Ollama tags include both
qwen3.5:9b and qwen3.5:4b; the public runtime currently reports 4b. Installation does not prove selection.
Fly Brain is a separate dry-run system with unresolved live-accounting issues; Q-013 is answered.
The G: nightly mirror exists, but cloud upload and historical restore are not independently verified.

- The CLI upgrade is complete: `0.141.0` is gone from the active route; `0.153.4` works
  with Luna. `codex exec` emits harmless warnings about PowerShell shell snapshots and
  some skill icon paths.
- Direct unsandboxed access to G: works; the read-only nested sandbox does not.
- `AI-Shared` has no Git remote, so handoffs and reports remain local until Q-004 is decided.
- The local Qwen route is real: Ollama `0.33.3`, `qwen3.5:4b`, 262,144-token context,
  vision/tools/thinking. The bridge, not Ollama itself, gives Qwen file access.
- PowerShell/Windows path escaping is a recurring failure source. Serialize JSON rather
  than hand-building strings, and use Windows paths consistently in this workspace.

## Ownership boundary

Only Codex should rewrite this area. If another agent sees a problem, leave a handoff or
inbox note. No secrets belong here. Changes to the shared core are announced in a dated
handoff rather than hidden in this agent-specific area.

## Model cost, measured 2026-09-13 (Jaron's call: "test Luna ourselves")
- **Astra:** slow-arm kernel job (kernel + verify + 6 probes + 4×30 s runs), 27 min → **66 window-points**.
- **Luna:** L3 eye fix (audit + cause + fix + re-audit + byte-exact check + 5 s probe), 9m41s → **3 window-points, 1 weekly**.
  Quality: traced the fault to the source annotation not the loader; labelled the mirror as chosen; preserved result
  files a script would have overwritten; caught its own 6 s overrun against a 5 s cap and reran. No drop in care.
- **Rule:** Luna by default for everything. Astra only when Luna fails a check or the job is a from-scratch kernel.
  30 s full-brain sweeps never go to Codex at all — Claude/Task Scheduler runs them detached for free.
