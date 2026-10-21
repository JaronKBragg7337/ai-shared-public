# Handoff — Codex site and Supabase review, 2026-09-23 afternoon

## Scope
Read-only inspection of the public Observatory at a 390 × 844 Chrome viewport and current official Supabase pricing/docs. No code, deployment, billing, or database changes. Browser viewport reset after inspection.

## Highest-impact site findings
1. The home page's primary phone CTA says **Fly School — live**, and its studio text says every student is live. The /school/ page says **REGISTER UNAVAILABLE** and "No student has written a trial yet," while all Fly School Windows tasks are disabled. The explanation still says students are taught around the clock. The /live-systems/ page similarly labels Fly School "taught 24/7" and the flies "live table tennis." These claims should follow actual freshness/paused state, with an explicit temporary status.
2. The /live-systems/trades/ page renders a shell but remains on **Loading…** with blank queue counts while the database returns HTTP 503. The /games/ page retains a literal **…** status because its Supabase-backed status request has no effective unavailable fallback. Public pages should show "Data temporarily unavailable" and the last known update time after a bounded timeout, not indefinite loading or an empty state implying no records.
3. The mobile home page gives its most prominent button to paused Fly School and places Games lower in the directory. The /games/ page leads with a PC Games note and long explanatory text; its new playable titles, including Orbit Salvage, are far down a long page. A visible **Play Games** home button plus a short choose-a-game list near the top would make existing working material discoverable without building new games.
4. The /games/ introduction says "Small games, hosted right here in the page," while the page includes large browser games and mostly links, with only President Sim embedded. A one-sentence copy update would set accurate expectations.

## Supabase pricing checked 2026-09-23
- Official pricing: https://supabase.com/pricing . Free: $0, 500 MB database data, 5 GB egress, 1 GB file storage, inactive projects may pause after a week. Pro: starts at $25/month for first Micro project, 8 GB provisioned database disk, 250 GB egress, 100 GB file storage, 7-day daily backup retention, no inactivity pause. Additional active projects add compute costs; paid organizations receive $10/month compute credit covering one Micro instance.
- Disk distinction: https://supabase.com/docs/guides/platform/database-size . Free's 500 MB is a database-data limit; Pro's 8 GB is overall provisioned disk, which also holds WAL/system files. Upgrading should be followed by a successful read query, disk/usage check, and public-page recheck. Paid disk auto-scaling beyond 8 GB may require spend-cap considerations.
- Current connected project list: Heartbeat management status ACTIVE_HEALTHY despite failed `select 1` TLS connection in prior health check; Pirate World, Fable Survival, and Wasteland Commons listed INACTIVE. Do not promise the base $25 covers reactivating all of them.

## Verification boundaries
Locally verified: site source in clean audit clone at 7bfb033 and disabled Fly School tasks from Task Scheduler (prior health check). Remotely verified: public page text and responsive layout in Chrome, current Supabase pricing/docs. Unverified: physical iPhone, logged-in page behavior, and any post-upgrade recovery. User expects to handle the Supabase subscription today and consult Claude after 4; no purchase authorization was inferred.
