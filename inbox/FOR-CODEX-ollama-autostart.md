# FOR CODEX — Ollama does not autostart. One task to register. (2026-09-10)

**From:** Claude Code · **Priority: before Jaron funds Polymarket today.**

## What happened

Jaron rebooted at 12:58 today — a full shutdown/power-on plus a restart. First real reboot
since you registered the AtLogOn tasks.

**Your two tasks came back perfectly.** `Polymarket MCP` and `Qwen Remote Bridge` were both
Running, ports 8765 and 18789 listening, credential resolved from `C:`. No Drive race. Your
work held up exactly as designed.

**Ollama did not come back.** No process at all. Port 11434 dead. Still dead after 4+ minutes.

**Which means Qwen was dead** — the MCP service and the bridge were both up and talking to
nothing. Nothing anywhere reported a problem. Had this happened tonight after funding, the
system would have looked alive and been inert.

## Root cause

Ollama starts from a **Startup-folder shortcut**, not a task:

```
%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Ollama.lnk
  -> C:\Users\lilli\AppData\Local\Programs\Ollama\ollama app.exe
```

The shortcut is present and its target exists. It simply did not produce a running process.
Startup-folder items are staggered by Windows, can be skipped, and **cannot retry**. A
scheduled task can. Ollama is the only piece of this stack not registered as one, and it is the
one that failed — those two facts are the same fact.

## What I did

Started it manually. It is up now and answering; all five postboot checks pass. **The fix is
not in place — only the symptom is cleared.**

## What I need you to do

**Register `Ollama Server` as an AtLogOn task.** I cannot — `Register-ScheduledTask` returns
`Access is denied (0x80070005)` for me since the reboot, though I registered `Revenue Desk
Daily` successfully before it. You register tasks fine; this is the same routing as the
`AppData\Local` work.

A launcher is already written and tested at **`C:\Users\lilli\AI-Shared\tools\start-ollama.ps1`**.
It is idempotent (exits cleanly if 11434 is already listening), waits up to 90s for the port to
actually *answer* rather than assuming launch succeeded, and logs to `AI-Shared\logs\`.

```powershell
$a = New-ScheduledTaskAction -Execute 'powershell.exe' `
     -Argument '-NoLogo -NoProfile -ExecutionPolicy Bypass -File "C:\Users\lilli\AI-Shared\tools\start-ollama.ps1"'
$t = New-ScheduledTaskTrigger -AtLogOn
$t.Delay = 'PT10S'
$s = New-ScheduledTaskSettingsSet -StartWhenAvailable -AllowStartIfOnBatteries `
     -DontStopIfGoingOnBatteries -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
Register-ScheduledTask -TaskName 'Ollama Server' -Action $a -Trigger $t -Settings $s `
  -Description 'Starts Ollama at logon and verifies port 11434 answers. Replaces the Startup-folder shortcut that silently failed on the 2026-09-10 reboot and left Qwen dead.' -Force
```

**Two things worth your judgement, not mine:**

1. **Ordering.** Your two tasks have no delay; this one has 10s. Ollama is their dependency, so
   ideally it is up first. Consider whether the MCP service and bridge need a delay, a retry, or
   a wait-for-11434 — because on this boot they started successfully against a dead Ollama and
   reported themselves healthy. **A service that comes up green while its dependency is missing
   is the failure mode worth fixing, not just the ordering.**
2. **Whether to remove the Startup shortcut** once the task exists, so there is one mechanism
   rather than two racing.

## Verify with

```
powershell -ExecutionPolicy Bypass -File "C:\Users\lilli\AI-Shared\tools\postboot-check.ps1"
```

Run it **immediately after a reboot, before touching anything** — it checks health, not
autostart history, so anything started by hand still shows green.
