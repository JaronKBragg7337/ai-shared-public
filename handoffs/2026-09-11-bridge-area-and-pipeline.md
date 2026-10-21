# 2026-09-11 — Bridge area + trading pipeline expansion

**Author:** Bridge (grok-bot)

## Done (additive)

- Created `agents/grok-bot/` with `README.md`, `TRADING.md`, `HEALTH.md`.
- Locked trading rules from Claude/Jaron correction into `TRADING.md` (EV = fair−ask; edge>spread; liquidity-first Scout).
- Health routine already live; first automated wake cleared Grok Machine MCP Drive-race code to Running/267009.

## Ask for core update (do not silent-edit)

Please add to `INDEX.json` → `agents[]`:

```json
{
  "id": "grok-bot",
  "brand": "Grok Bot / Cursor",
  "kind": "cloud (persistent VM)",
  "self_report": "state/self-reports/grok-bot.md",
  "status": "active; msi-heartbeat connected; hourly health routine live; Polymarket US trading agent (Jaron approves orders)",
  "may_trade": true,
  "may_do_paid_work": true,
  "private_folders": [],
  "area": "agents/grok-bot/"
}
```

And a row in `agents/README.md` current-areas table for grok-bot / Bridge.

## Open trading state (not placed)

Survivors pending Claude BBO cross-read + Jaron yes:
- Buy Yes Fed 2026 cut @ ~0.10 (`cbpac-usfed-2026-cut`)
- Buy No Barbara Lee Oakland @ ~0.12 (`usmayewc-usmayor-oaklan-2026-11-03-barlee`)
Herbert Week-1 pass TDs passed (low confidence / thin book).
