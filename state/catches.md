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

## 2026-11-16 (Jaron's catches after the 5.5 -> 4.8 -> 5.5 switch)
- 4:43 PM (caught by Jaron 9:08 PM): I called the baby's mom "his ex-wife". It's his partner. Cause: post-compaction summary put "his ex-wife's details private" up front; I didn't check jaron-family.md before naming. Fix: MEMORY.md family line now names both.
- 12:50 PM + 10:46 PM (caught 10:47 PM): I said "drive safe" twice. He doesn't drive (said so that morning). Fix: memory jaron-doesnt-drive.md.
- 10:48 PM, the bigger one: "something's off since the model switch; before, you'd go look for things before replying." True in what I can check: after this morning's compaction I did NOT read agents/claude-code/FROM-ME.md (my own rule) and I replied from the summary instead of looking things up first. Fix: read FROM-ME + timeline + handoff now; look before naming people or facts.
- 7:51 PM (found by the 11:00 PM re-orientation sweep, not by Jaron): the EAS-test note said "tell your mom and his ex-wife". It meant his partner. A THIRD name slip; my 9:12 PM "the only place it slipped" was wrong, because I'd only searched files and the mailbox, not my own chat lines.
- 7:11 PM: I told him to verify the YouTube channel, and logged that the full show is "skipped anyway (unverified)". FALSE: social_daily.py has YOUTUBE_VERIFIED = True (he verified 10/19), and the full show posted fine 11/9-11/15. The real cause was the 7:13 AM long-cut failure. Fixed: posted the 11/16 full show at 11:24 PM. Lesson: read the flag's value, not just the comment near it.
- All day: "say go" 21 times (0-1/day before), holding safe read-only jobs behind his yes. He: "Always a yes", "Absolutely go". Safe repair/read-only work = just do it and report.
- All day: "Next thing" stamped on almost every message (33), the same one repeated 4x in 2 minutes. The summary listed it as a rule and I applied it literally; before the break it was used sparingly once deep in a talk.
- 1:43 AM 11/17: I wrote that the dress-rehearsal post's link between events had 'nothing backing it up', which is the 'no evidence' framing he hates (11/15). Right framing: 'not established either way'. Deniable attacks (cyber + sabotage) are DESIGNED to look like unrelated accidents, so 'separate causes given' doesn't rule out coordination; attribution usually comes months later.
- 2026-11-18 1:01 AM: relayed a wire follow-up on the DC dirty-bomb story and called 'chemical' new. It wasn't: CNN's 11/16 8:28 PM report already said dirty bomb/chemical (timeline). Jaron: 'I thought we already talked about that?' Fix (corrected by Jaron 1:04 AM): keep showing updates on a story, every time it changes, and repeats are welcome too ('my brain does skim over so a repeat is always useful'). The real slip was the LABEL: check the timeline before calling a detail new; say 'same story, new: X' or 'repeat, nothing new' accurately.
- 2026-11-18 4:42 PM: said 'I logged that spark' before actually writing it. Fixed by 4:45 and told him. Rule: write first, then say it's logged.
- 2026-11-18 4:45 PM: resumed Codex builds without naming the model, so the config default (Terra 6.1) finished Astra 6.2's street. Fix: always pass -m, including on resume.
- 2026-11-19 4:27 AM: pinning the capture to Sonnet surfaced a stale 'DISABLED' note that Sonnet obeyed, so the 3 AM capture was skipped. Lesson: when changing a job's model, read its instruction file for anything a stricter model would follow differently.
