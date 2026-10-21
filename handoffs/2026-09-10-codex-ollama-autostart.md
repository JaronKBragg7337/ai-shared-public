# Ollama autostart — Codex, 2026-09-10

Registered Ollama Server for MSI\lilli interactive AtLogOn, 10-second delay, three retries one minute apart, battery allowed, IgnoreNew. Action uses C:\Users\lilli\AI-Shared\tools\start-ollama.ps1 with an explicit C: working directory. Started the task once while Ollama was already up; it returned 0 and logged API readiness at 15:38:01. This verifies registration and the idempotent scheduled-context path, NOT cold startup.

Corrected the launcher's occupied-port shortcut: it now requires an Ollama API response with a models field, otherwise returns failure if the port is occupied. The Qwen bridge runtime launcher now waits up to five minutes for Ollama's API before starting the bridge, then exits nonzero on timeout; existing task retry is 999 attempts at one-minute intervals. No artificial ordering delay added to the bridge. MCP is independently useful and remains ungated. Existing running processes were not restarted.

Updated postboot-check.ps1: includes Ollama Server, reports task start times and checks logon tasks ran since boot, distinguishes installed models from loaded/generating models, and returns exit 1 for failed checks. Running/Ready task state is explicitly not dependency health. This is a point-in-time check, not a continuous watchdog; dependency failure after launch remains detectable by this check but does not automatically restart the already-running bridge.

Moved the verified Ollama Startup shortcut out of Startup to state/Ollama-startup-shortcut-20260910.lnk after the scheduled task test succeeded. Recoverable, not deleted. One logon mechanism now remains. No Ollama processes were stopped.

Local verification: task registration/readback, scheduled idempotent execution, PowerShell parse checks, and current endpoint checks. Remote verification: none needed/performed. Unverified: cold boot startup, retry on actual outage, inference/end-to-end work. No trading, funding, or model estimation performed.

Claude Code's inbox report says: "The fix is not in place — only the symptom is cleared." This was an inherited report, not a new consultation. Jaron's earlier reboot result independently supplies the first successful reboot report for MCP/bridge; Ollama must still be tested on the next reboot.

NEXT: Jaron controls the pending Windows restart. On resuming this task, before starting or repairing ANY service, run `powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\Users\lilli\AI-Shared\tools\postboot-check.ps1` and preserve output. Do not represent the preboot check as an autostart test. Source launcher change currently lives in the C: runtime; do not overwrite it with the older G: mirror.
