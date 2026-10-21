# Catches log - things a person noticed that no system caught (Jaron 10/18)
One line per catch: date | what was missed | who caught it | what check now exists (or "none yet").
Rule: the SECOND time the same kind of catch shows up, an AI builds the automatic check and fills in the last column.
Every AI may add lines. Jaron's skill to grow: spotting where reality and the system disagree.

2026-10-17 | France riots + Limoges town hall fire missing from every news capture | Jaron (scrolling X) | Meridian desk (Grok, Europe/LatAm/Africa) + daily blind-spot check
2026-10-17 | YouTube full show "Upload failed: video too long" while Postiz said published | Jaron (YouTube app) | 15-min guard in social_daily.py; lesson: check the platform, not Postiz
2026-10-17 | Connector alert buzzing when bots were only quiet (alert fatigue) | Jaron | alert now tells unreachable / expired sign-in / quiet apart
2026-10-17 | Social page: anyone could make themselves admin | Jaron's gut ("my account can do things it shouldn't") -> Claude found it | locked in the database
2026-10-17 | Share card wording could trip X ad review, flagged days late | Jaron | rule: check every use of an asset at design time
2026-10-17 | Codex trusted for episodes without a test | Jaron | test build (Lost Places 22.1) measured before handing builds over
2026-10-18 | Disk full, news render died at 6:26 AM (5 days of leftover frames) | Claude (morning check) | frames removed right after encode; publish can't crash on cleanup. + free-space alarm (connector-watch, every 30 min, buzzes under 80 GB)
2026-10-18 | News re-render started at full quality, ETA 2 PM | Jaron (deadline: by 8 AM, never after noon) | auto fast mode after 5:15 AM + automatic fast retry
2026-10-18 | Ashgrove clock GitHub Action failed every day since Ashgrove was made (emails nobody read) | Jaron (email) | fixed permission (service_role usage on world3_private); failures now buzz ntfy
2026-10-18 | X post for Space Now never created (emoji count as 2 on X -> 'too long'; script logged OK) | Jaron (didn't see it on X) | X text capped at 262; Postiz 400 replies now caught as failures
2026-10-18 | $75 deposit (10/15) missing from the crew page; deposits drawn blue like withdrawals | Jaron | page now counts deposits Polymarket still lists PENDING (labelled); deposits purple
2026-10-18 | crew page money wrong: account line ~$50 high, AI shown +$205 (real -$110 after fees), fees never shown | Jaron ('I definitely don't have $100') | cash-ledger reconcile; fees card; real-dollar AI/hand split
2026-10-19 | News render ran full quality from 4:03 and was on pace for ~8:15 AM (29-min show); the 5:15 auto-fast rule only checks the START time | Claude (morning check 5:51) | stopped -> fast retry; pipeline now checks PACE every 5 min and goes fast if the finish would pass 7:15 AM
2026-10-19 | Codex 3 AM capture lost ("model at capacity") | Grok blind-spot check (listed it) | run_codex.ps1 retries once on gpt-6.1-sol
2026-10-19 | Blind spot: North America (Canadian live-fire deaths, Wichita, US domestic) - no desk owns it | Grok blind-spot check, first run | none yet - watch for a second repeat
2026-10-18 | Sapling relay dead since the 10/17 builder taskkill (page stale, Jaron's 5:45 AM 'Hello sapling' unanswered) | Jaron (no reply) | relay restarted 10/19 6:19; + relay check in the 30-min watch (auto-restart, buzz if it fails)
