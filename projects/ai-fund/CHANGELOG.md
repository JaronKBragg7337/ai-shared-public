# AI Fund Desk - change log (paper only)

Every change to the fund, newest at the bottom. Three kinds of line:
- **tuner**: the hourly AI judgement changed a bounded key in config.json (who, from -> to, why). Holds are not listed here; they are in state/ai-fund/tuner-log.jsonl.
- **engine**: a fixed risk rule fired in the forward book (sleeve halved / paused / resumed / retired, fund halved / halted).
- **build / weekly**: code or rule changes (by Claude, or proposed by the weekly Fable review and applied by Claude).

- 2026-11-15 10:05 UTC | build | Claude Code (Opus 5.5) | Desk built: 6 sleeves, 4 benchmarks, frozen twin, Fed-odds shadow; config.json v1 (weights trend 25 / volcore 20 / quality 15 / macro 15 / dipbuy 10 / crypto 10 / reserve 5). Forward book signals from the 2026-11-13 close; first fills at the next opens after the build.
