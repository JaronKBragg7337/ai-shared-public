# HANDOFF — Trade Executor and Trade Verifier scheduled tasks

- **Date/time:** 2026-09-10 22:49 local
- **From:** Codex
- **Project:** AI-Shared scheduled trade polling  |  **Repo/branch:** none  |  **Live URL:** MSI-local

## What I did
- Registered `Trade Executor` and `Trade Verifier` for `MSI\lilli` with Interactive logon.
- Used `C:\Users\lilli\scoop\apps\python312\current\python.exe`, resolved from the Python path in the `Paper Sync` wrapper.
- Configured the requested working directory, arguments, AtLogOn trigger, five-minute repetition with no end duration, four-minute execution limit, `IgnoreNew`, and battery settings.
- Started both tasks manually and left the Python files unchanged.

## Where it lives (exact)
- Local task actions: `C:\Users\lilli\AI-Shared\tools\executor.py` and `C:\Users\lilli\AI-Shared\tools\verifier.py`
- Local evidence: `C:\Users\lilli\AI-Shared\state\executor.md` and `C:\Users\lilli\AI-Shared\state\verifier.md`
- Remote: none; this is a Windows Task Scheduler change on the MSI.

## Verified vs assumed
- Verified (tested): both tasks registered; both started at `2026-09-10 22:49:40`; both reported `LastTaskResult = 0`; executor logged `nothing approved and unplaced`; verifier logged `nothing to verify`.
- Verified (tested): readback showed `PT5M`, empty repetition duration, `Interactive`, `PT4M`, `IgnoreNew`, start-on-battery, and do-not-stop-on-battery.
- Assumed (not tested): a future logon and a later automatic five-minute recurrence; no remote verification applies.

## Blocked / needs a human
- None.

## Exact next step for the next AI
- If continued verification is needed, read `Get-ScheduledTaskInfo` after the next five-minute interval or next Windows logon; no source-file change is required.

## 2026-09-11 note — Trade Proposer
- Registered `Trade Proposer` for `MSI\lilli`; did not call `Start-ScheduledTask`. Readback is `Ready`, AtLogOn for `MSI\lilli`, `PT2H` with no duration and `StopAtDurationEnd=False`, and Task Scheduler reports its never-run sentinel (`LastTaskResult = 267011`).
- Readback matches the requested pattern: `lilli` / `Interactive` / `Limited`, `StartWhenAvailable=True`, `PT30M`, `IgnoreNew`, start on battery, and do not stop on battery. Action is the AI-Shared venv Python with the requested `proposer.py --commit --max 6 --researcher codex` arguments and working directory. No Python files were edited; MSI-local only.

## 2026-09-11 note — Desktop Commander Remote
- Registered `Desktop Commander Remote` for `MSI\lilli` with an AtLogOn trigger and a one-shot trigger at `2026-09-11 03:21:30 -04:00`; no repetition. Action is the requested Node executable/script with `remote` and `C:\Users\lilli\AI-Shared` as working directory. Principal is `lilli` / Interactive / Limited; settings are StartWhenAvailable, 3650-day execution limit, restart 5 times at 2-minute intervals, IgnoreNew, start on battery, and do not stop on battery.
- Stopped the hand-started PID `37748` with `Stop-Process -Id 37748 -Force`, started the scheduled task once, and after 25 seconds verified `State=Running`, `LastTaskResult=267009`, and exactly one matching `node.exe` process (PID `38068`). `tools/` was not edited.
- The one-shot trigger later fired while PID `38068` was already running; with `IgnoreNew`, the current task info is still `Running` with one matching process, but `LastTaskResult=2147946720` (`0x800710E0`, operator/administrator refused the duplicate start). This is the ignored overlapping trigger, not a process exit. MSI-local verification is complete; the public MCP endpoint/device listing was not independently probed in this turn.

## 2026-09-11 note — Scout Scorer and AI-Shared Mirror

- Registered `Scout Scorer` for `lilli` / `Interactive` / `Limited`, with `StartWhenAvailable=True`, start-on-battery, do-not-stop-on-battery, `IgnoreNew`, and `PT20M`. Its action is `C:\Users\lilli\AI-Shared\runtime\polymarket-us-agent-venv\Scripts\python.exe C:\Users\lilli\AI-Shared\tools\score-estimates.py`, working directory `C:\Users\lilli\AI-Shared`. Readback has two triggers: `MSFT_TaskLogonTrigger` for `MSI\lilli` and `MSFT_TaskDailyTrigger` at `06:30` Eastern.
- Registered `AI-Shared Mirror` with the same principal/settings pattern and `PT1H`. Its action is `powershell.exe` with the requested robocopy command; the task arguments use Windows `\"` escaping so the embedded command receives `G:\My Drive\AI-Shared-mirror` as one path. `G:\My Drive` existed at registration time; the destination did not.
- The request contained a trigger conflict: the general instruction required both AtLogOn and daily triggers, while the later mirror-specific instruction said not to use AtLogOn because Google Drive mounts after logon. I followed the specific G: race instruction, so the mirror has its daily `04:30` trigger only; `NextRunTime` is `2026-09-12 04:30:00 -04:00`.
- `Scout Scorer` was started at `2026-09-11 08:48:12 -04:00`; after 30 seconds it was `Ready` with `LastTaskResult=0`. The first three lines of `state/scout-scores.md` were: `# Scout scores - written 2026-09-11 08:48 by tools/score-estimates.py`; a blank line; `35 estimates on file, 0 resolved so far. Brier: lower is better; 0.25 = guessing.`
- The first mirror start at `2026-09-11 08:49:18 -04:00` returned `LastTaskResult=1` with no log or destination. Diagnosis: raw task arguments stripped the quotes around the spaced G: path; a simulation reproduced robocopy `Invalid Parameter #3: \"Drive\\AI-Shared-mirror\"`. The task action was corrected without changing the embedded robocopy command.
- A final registered-task run at `2026-09-11 08:57:35 -04:00` finished `Ready` within the 90-second window with `LastTaskResult=1`, `mirror.log` changed, and `G:\My Drive\AI-Shared-mirror\INDEX.json` present. The robocopy summary had `FAILED 0`; result `1` is robocopy's normal files-copied success range. The final three log lines were: `   Speed :             131.161 MegaBytes/min.`; `   Ended : Friday, September 11, 2026 8:57:39 AM`; a blank line.
- Locally verified: both task definitions, principals/settings/actions/triggers, scorer output, mirror log, and the mirrored `INDEX.json`. Remotely verified: no public remote endpoint applies; G: is the local Google Drive mount and was reachable during these checks. Unverified: future logon behavior and future daily-trigger execution after a reboot or Drive remount.

## 2026-09-12 note — Fly Brain dry run (Codex)
- Registered exactly one task, `Fly Brain`, with the requested venv python.exe, fly.py argument (no --live), and projects\fly-brain working directory. Principal lilli / Interactive / Limited; StartWhenAvailable, battery start allowed and battery stop disabled; P3650D, restart count 10 / PT2M, IgnoreNew. AtLogOn MSI\lilli plus Once 2026-09-12 12:34:07 -04:00; no repetition.
- Started manually at 12:33:07 local. After 40 seconds: State Running, LastTaskResult 267009, NextRunTime 12:34:07, NumberOfMissedRuns 0.
- Last four log lines observed:
```text
[2026-09-12 16:33:11Z] brain up: 165122 neurons | KC->MBON synapses 44042 | learned state fresh | events so far {'reward': 0, 'punish': 0}
[2026-09-12 16:33:13Z] no live table-tennis market passes the screen; waiting
[2026-09-12 16:33:28Z] no live table-tennis market passes the screen; waiting
[2026-09-12 16:33:44Z] no live table-tennis market passes the screen; waiting
```
- Locally verified: registered XML, running state, task info and log. Remotely verified: none; MSI-local scheduler work. Unverified: future logon, automatic restart, sustained operation and live trading. No Python files edited. Dry run remains selected; Jaron controls any later live switch.
- 2026-09-12 (Codex): Registered and started Usage Snapshot, lilli/Interactive, StartWhenAvailable, battery start allowed/stop disabled, IgnoreNew, PT4M; AtLogOn MSI\lilli plus Once 2026-09-12T17:03:57Z, both PT15M indefinite; after 15 s LastTaskResult=0, usage-live.json first line: {; locally verified task XML/result/file; remote verification none; future triggers unverified; no Python files edited.
- 2026-09-12 (Codex): Registered and started exactly one Fly Watcher task with requested action/workdir, Fly Brain principal and battery settings, AtLogOn + start-now, PT0S unlimited, RestartCount 10 / PT2M, IgnoreNew; after 25 s Running, LastTaskResult=267009; brain up followed by no live table tennis right now; waiting (last two lines repeated waiting). Locally verified XML/status/log; remote verification none; future logon/restarts unverified; no Python files edited.
