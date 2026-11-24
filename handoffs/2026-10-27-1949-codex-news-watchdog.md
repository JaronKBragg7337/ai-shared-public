# Handoff 2026-10-27 7:49 PM — Codex news watchdog

- Today's rendered news recovered and was published at 3:10 PM ET, after the deadline; public index and MP4 are accessible. Extras logged 3:16 PM.
- Added `tools/news_watchdog.py`: 7 AM to noon, checks the public index and current day's video; warns on missing or unreachable; alert state is written only after successful ntfy delivery, so failed sends retry. A separate warning can occur if the status changes from unreachable to missing. No secrets are logged.
- Windows task `HB News Watchdog` runs hidden as lilli every 15 minutes, 7 AM–noon, including on battery; next run 10/28 7 AM. Manual task run outside the alert window returned 0. Five unit tests passed and live `--dry-run` confirmed today's video; no real phone alert was sent, and the first scheduled morning run remains unverified.
- Logs of existing news render: `projects/news-show/rendered-runs.log`. Check task history / `Get-ScheduledTaskInfo 'HB News Watchdog'` after 7 AM. Use `python tools/news_watchdog.py --dry-run` for a safe current live check.
