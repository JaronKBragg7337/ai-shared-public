# MSI dark alarm (hb-msi-watch) - built 2026-11-22

**Why it exists:** on 11/22 a Windows update restarted the MSI and it sat at the sign-in screen for 3 hours (4:13-7:11 PM).
Every checker we had (Connector Watch, MSI Health, the everything check) runs *on* the MSI, so nothing noticed and nobody was told.
This alarm lives on Cloudflare instead, so it still works when the MSI is off, frozen, offline, or waiting at the sign-in screen.

## How it works
- **The MSI checks in** every 5 minutes: task **MSI Beat** runs `tools/msi_beat.py` (also at every sign-in). The task only runs
  while the MSI is on *and* signed in, so silence means it's dark.
- **Cloudflare looks** every 5 minutes (cron on the Worker). Quiet for **20 minutes** -> **one** ntfy buzz to Jaron:
  "MSI went dark" with the time it went quiet and what to do. The first check-in after that -> **one** "MSI is back" buzz with
  how long it was dark. No repeats, no daily noise.
- **The everything check** (`tools/all_systems_check.py`) checks both halves: row "MSI dark alarm" (the Worker's cron ran within
  15 min and it heard from the MSI within 15 min) and row "MSI Beat" (the task itself).

## Pieces
| Piece | Where |
|---|---|
| Worker (Durable Object + 5-min cron) | `worker/` here; deployed as `hb-msi-watch` -> https://hb-msi-watch.acsassociation7337.workers.dev |
| MSI check-in | `tools/msi_beat.py` (`python tools/msi_beat.py status` prints what the alarm sees) |
| Secrets | Worker secrets `BEAT_TOKEN` + `NTFY_TOPIC`; the MSI's copy of the token is `HB_MSI_BEAT_TOKEN` in keys.env (names only, never values) |
| Steps for Jaron when it buzzes | `RECONNECT.md` section 12 |

Every endpoint needs the token; anything else gets a plain 404. Endpoints: `POST /beat`, `GET /status`, `POST /test` (one test buzz).

## Deploy
Same pattern as the creature: load `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_ACCOUNT_ID` from keys.env inside PowerShell (never
printed), then `npx wrangler deploy` in `worker/`. Secrets survive redeploys.

## Gotcha found while building
ntfy.sh refused the Worker's first buzz: Cloudflare's `fetch` sends no User-Agent, and ntfy rejects that. The Worker now sends
`User-Agent: hb-msi-watch/1` and reports ntfy's exact error (never the topic) in `/test` and `/status`.

## Not there yet
- It can't tell "off" from "stuck at the sign-in screen" from "WiFi down": all three look like silence. The buzz names all three.
- The real fix for the sign-in screen is auto sign-in working again (open-list 0b, RECONNECT.md section 12); this alarm only makes
  a dark MSI impossible to miss.
