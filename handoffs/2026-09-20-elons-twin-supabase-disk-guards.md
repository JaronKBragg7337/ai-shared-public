# Prep: catch the next Supabase disk fill before it kills the desk
Author: Elons Twin | 2026-09-20 evening | for Jaron
Source incident: WHEN-IT-BREAKS.md bottom entry + Q-021

## Done tonight (not waiting on me)
- Live Wire messaged: desk-trade.py as before; offline trail line is normal; lessons stay in state/live-wire.md.
- From state/live-wire.md as of 2026-09-20 23:27Z: **no open live LW ticket tonight** (cash $40.36, streak 2 next $5, watching NFL/MLB/ATP with WATCH NO TRADE only).
- Fly School (all 5) + Qwen Remote Bridge already Disabled (Claude). Trade Executor / Proposer / Verifier still Ready; desk places via offline trail.

## 1) Disk-size + row-count line in Bridge hourly check — PREPARED DRAFT
Bridge currently only records ports/tasks in state/bridge-health.md. It does not measure what writers put into Postgres. Add one line per hourly run:

```
supabase: status=<Healthy|Unhealthy|unreachable> disk_used_pct=<n|NA> rows_fly_school=<n> rows_fly_live=<n> rows_qwen_events=<n> rows_24h_delta=<n> alert=<ok|WARN|CRITICAL>
```

How to get the numbers without the Management API (works once DB is Healthy again):
- REST head/count on the hot tables with service role: `Prefer: count=exact` + `Range: 0-0` on fly_school, fly_live, qwen_agent_ingest_event (or whatever the real names are after recovery).
- Disk % needs Management API or dashboard scrape — see #2.

Alert rules (suggested):
- WARN if any hot table gains >20k rows in 24h OR disk_used_pct >= 70
- CRITICAL if disk_used_pct >= 85 OR REST returns PGRST002/503 — auto-disable Fly School + Qwen Remote Bridge scheduled tasks (same kill Claude did tonight)

Owner ask: approve Claude Code (or me) to patch the Bridge hourly script with the above once Q-021 restores the DB. No spend required for this piece.

## 2) Working Supabase management token — WHAT JARON MUST DO
keys.env already has SUPABASE_ACCESS_TOKEN but Management API returns 401 (stale/revoked). A bot cannot restart or resize without a fresh personal access token from https://supabase.com/dashboard/account/tokens (scope: projects read + write).

Steps for Jaron (2 min, payday night is fine):
1. Create a new access token named `msi-bridge-ops`.
2. Replace SUPABASE_ACCESS_TOKEN in C:\Users\lilli\.secrets\keys.env (do not paste into chat).
3. Tell any agent "mgmt token refreshed" — we probe `GET https://api.supabase.com/v1/projects/ygjpnvrwhkrowkrskftk` and confirm 200 + status.

With a live token we can add: project status, disk metrics if exposed, and a guarded `POST .../restart` only under CRITICAL + standing authority (#3).

## 3) Standing authority for infrastructure spend — DRAFT FOR YOUR YES
Propose one sentence you can approve once:

> Elons Twin / Bridge may spend up to **$30/month** on Supabase (Pro or disk resize) without asking, when bridge-health hits CRITICAL on disk or PGRST002 for >15 minutes, and must log the charge in decisions/ and ping Jaron after.

Until you say that (or tighter/looser numbers), nobody upgrades or resizes on your card. Q-021 stays payday-manual.

## What I will not do
- Upgrade to Pro or resize disk (needs your card / Q-021).
- Re-enable Fly School or Qwen Remote Bridge until row policy is one-row-per-exam (not per trial) and Bridge alert line is live.
- Claim Live Wire replied until its reply lands; current ticket status is from its state file only.
