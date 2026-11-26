# Handoff - Claude Code main seat, Wed 11/25/2026 ~10:00 AM

**Sealed items: none open.** (MSI data damage came off the list 11/24 - Jaron: no outside person ever looks at the MSI; P-0189.)

## Done since 11/24 morning
- **MSI data damage: cause found + fixed (Fable).** One fast core (logical 10+11, i9-14900HX, Intel 13/14th-gen wear) wrong at ~5.3 GHz.
  Fix A: fast cores capped 4.6 GHz (`tools/msi_speed_cap.py`, undo `off`). Yardstick 0/1,368 with cap, 155/1,056 with cap lifted.
  Daily "MSI Core Yardstick" 11:30 AM (2 min; exit 0 clean, 1 failures -> lower cap, 2 not a fair test). Everything check has a
  "Processor speed cap" row (auto-resets). News pipeline also pins itself off cores 10/11. BIOS E15M2IMS.912 = later, planned with Jaron.
- **News 11/24 + 11/25 published** (5:47 AM 11/25). Fixes: fast-retry + tail stall guards; Say() logging retries and can't kill
  the show (11/25 3:50 run died silently because Claude's leftover `tail -F` watchers held the log). Lessons in FROM-ME:
  never tail -F the news log; never *>-redirect the pipeline; start long jobs via schtasks/WMI, not from a tool call.
  OPEN: first Unreal launch hangs at "Waiting for ZenServer" ~nightly (retry works) - detect after ~3 min instead of 15 (test first).
- **Windows Terminal crashed 11/24 10:15** (1,000 console tabs from the yardstick). Default console host -> conhost
  (HKCU\Console\%%Startup = {B23D10C0-...}). CREATE_NO_WINDOW on child launches in scheduled Python jobs.
- **Drive** out of the big backups (Jaron: "always had issues"); weekly one-file git bundle "Drive Weekly Copy" Sun 9 PM.
  Off-MSI Supabase backup is the real copy and is now on the everything check.
- **MSI cleanup with Jaron (nothing stopped without him):** crypto lane + Polymarket leftovers paused (7 tasks), OpenClaw paused,
  17 expired reminders off (SuperGrok 1/3/2027 one kept ON), dead Codex Observer startup entries removed (backed up).
  Report: state/msi-inventory-2026-11-24.md. Still his call: Jarvis voice (voiced.mjs reads every Claude reply aloud) on/off;
  Docker/Slack startup entries. Bitcoin Puzzle71 / MachineManager: off since 9/1, not running.
- **Money (BILLS.md):** Postiz $29 declined 11/24; X Money moved to Uphold (~$0) so retries fail - DON'T cancel Postiz by hand
  (cancels posting at once); it lapses ~Tue 12/1. Codex $20 Fri 11/27 (he wants to keep Codex - perspective matters, P: AI companies
  = perspectives). Claude Max $100 Wed 12/2 = must be found. RunPod $7.88 -> creature search arm.
- **Own posting (Fable):** tools/direct_post.py. **YouTube CONNECTED 11/25 9:50 AM** (Jaron on his phone; status READY,
  @heartbeatobservatory; social-path youtube=direct; first real upload = next daily post). X needs ~$5 credits (his call).
  TikTok: no own door; when Postiz ends, offer the morning phone buzz with video link + caption (he said "not too bad", later).
- **Site:** official Terms of Service at /terms/ (merged old Standards + new), /privacy/ new, /standards forwards, home footer +
  sign-up checkbox updated (site f1279f2d..+2).
- **Creature cell experiment (PRIVATE, creature-observatory repo):** Jaron's idea = Sapling-in-every-cell / one language inside and
  out. Plan v1.1 fingerprinted (lab/cells/PLAN.md, c652ed8). Step 0 PASSED 3,795/3,795 on 2 machines. Round one waits for
  **Fable after its Wed 11/25 2:59 PM reset** (Jaron: "100% wait, Fable knows it"): first the verifier's 111/112 finding, then
  Amendment 2, then the 8 arms. Rules: P-0191 (every rule can be the flaw), ability from design not expense, memory a dial,
  private = method / public = proof after verification, containment line is Jaron's only.
- **Ledger:** P-0189 (pros only for critical things), P-0190 (two suspicious, three confirms - breach watch, Tue 12/1),
  P-0191. working-with-jaron.md rule 8: exact-page links with the account built in (authuser=).
- **Breach watch (Satya):** USDA 11/19, FBI 11/20, CIA same day (disclosed 11/24), FinCEN (date unknown). Watch Thanksgiving + Tue 12/1.

## Open for Jaron (no rush)
- Fortitude video script: projects/life/opportunities/FORTITUDE-VIDEO-SCRIPT-2026-11-24.md (voice-over, no face; the ladder idea).
- Verizon Digital Ready courses by Mon 12/7. Claude chat -> MSI connector expires Sun 11/29 (use it once to renew).
- BIOS update (plan with him). Jarvis voice on/off.

## Running
Mailbox waiter (re-arm after each message), Seam Room listener (6 h), Fable session "Push for the stars".
