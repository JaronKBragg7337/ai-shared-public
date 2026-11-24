# MSI stack health — Bridge routine

**Routine folder:** `msi-stack-health`  
**Schedule:** `51 * * * *` America/Indianapolis (hourly at :51, all days)  
**Log:** `state/bridge-health.md` (append-only)  
**Updated:** 2026-09-11 — added steps 8–9 (sentiment + desk queue)  
**Status note (10/23 sweep):** this is the Sept 11 Bridge routine contract (Claude Code/Codex wording). ROLE-AUDIT-2026-09-25.md moved hourly health to a free Windows task; step 9 (queue ping to Jaron) belongs to the retired approve queue (9/24, Q-023). The 'ping Jaron only if' lines are notification settings, not Jaron rules.

## Why all-day hourly

Local agents die on reboot/login. On 2026-09-10 Ollama silently failed to restart while other services looked fine. Bridge is the agent that can notice unprompted.

## Each wake

1. If `msi-heartbeat` needsAuth → pause this routine, tell Jaron once, stop.
2. Ports on MSI loopback: **11434** Ollama, **18789** OpenClaw, **8765** Polymarket MCP, **3001** Heartbeat MCP origin.
3. Scheduled tasks: Ollama Server, Polymarket MCP, Qwen Remote Bridge, Revenue Desk Daily, Grok Machine MCP — State + LastTaskResult.
4. Append one short dated line to `bridge-health.md`. Never overwrite.
5. If MSI unreachable: one "dark" line, no retry loop.
6. Ping Jaron only if: port down, real task fault, or MSI dark >2 consecutive hours.
7. **Do not restart or repair** — observe and record. (Bridge's Sept 11 routine contract; Claude Code's choice for this routine, not a Jaron rule. agents/grok-bot/README.md allowed restarting a dead scheduled-task service.)
8. **Sentiment:** read `inbox/sentiment-requests.json`; for up to 6 oldest slugs lacking a fresh (`<24h`) `state/sentiment/<slug>.json`, search X on the market's own question/outcome wording (no prices, no probabilities), write lean/strength/note JSON; quiet → split/1/"quiet".
9. **Desk queue:** `python C:\Users\lilli\AI-Shared\tools\desk.py queue`; if pending+verified exist and no queue ping in last 4h, one message to Jaron with count, best proposal, and https://www.heartbeatobservatory.com/live-systems/trades/ — never ping empty.

## Result-code notes

- `0` = success
- `267009` (`0x41301`) while State=Running = still running (healthy for long-lived tasks)
- `2147942667` (`0x8007010B`) = historic Drive working-directory race
