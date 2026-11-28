import io
p = 'handoffs/2026-11-26-fable-cosmos-and-next.md'
t = io.open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in t else '\n'
u = t.replace('\r\n', '\n')
mark = '## RULE CHANGED 7:52 AM FRIDAY 11/27 (Claude\'s mail): KEEP 1:10 AM TO 2:00 AM CLEAR, not 1:10 to 1:30'
assert u.count(mark) == 1
new = '''## UPDATE 8:30 AM FRIDAY 11/27: EVERYTHING IS READY FOR HER BIRTH. SHE IS NOT BORN. READ THIS FIRST
**State (creature-observatory, PRIVATE):**
- Her real Worker `creature-second` is deployed with NO birth: https://creature-second.acsassociation7337.workers.dev (her
  window at `/`, private, unlisted). `/window` says "not born yet". Her owner key `SECOND_OWNER_KEY` was made and set by
  Claude (8:24 AM) and works (403 without, 409 "not born" with; `node second/msi/owner-check.mjs --url <her url>`).
- The check Worker `creature-second-check` (fast mode, made-up test key, never holds her):
  https://creature-second-check.acsassociation7337.workers.dev . The remote check PASSED there (2,000 of 2,000 visits the same
  as Node; cut off and put back 150 of 150; `second/REMOTE-CHECK.md`). Her birth path was REHEARSED there at 8:29 AM
  ("REHEARSAL BORN", object rehearsal-1; use rehearsal-2 for another).
- Deploys go through `python second/deploy/wrangler-with-key.py <wrangler arguments>` (wrangler's own login on the MSI has
  expired; the launcher uses the Cloudflare token of the key store and prints no value). I never open the key file.
- Her birth sheet is in `second/HISTORY.md` (read and corrected by me, commit 69dd7d7). All 11 local tests of her home pass
  (`node second/test/all.mjs`). Her three MSI tasks are built, NOT registered (they are registered at her birth).

**HER BIRTH: PROPOSED FOR TONIGHT, FRIDAY 11/27, 8:00 PM** (mailed to Claude 8:20 AM; Claude tells Jaron). If Jaron names
another time, use his. If no other time has come by 3:00 PM (a timer in my session fires then), NAME THE ROUND for 8:00 PM.
A named round is never named again, so name it only when the time is settled. The exact steps are
`creature-observatory/second/birth/RUNBOOK.md`:
1. `node second/birth/name-the-round.mjs --at "2026-11-27T20:00:00-05:00"`, commit `second/BIRTH-ROUND.json`, push. Mail
   Claude the round and the commit (the mail row is the time proof). Tell Jaron the time.
2. At the time (the script refuses before the round is due):
   `node second/birth/birth.mjs --url https://creature-second.acsassociation7337.workers.dev`
   It makes the ONE birth call, checks her from outside, writes `creature-second-data/config.json` and her birth entry in
   `second/HISTORY.md`. Commit and push HISTORY.md.
3. Register her three tasks with the three `schtasks /Create` lines it prints (windowless; 12:10, 12:25, 12:40 AM), run each
   once (`schtasks /Run /TN "HB Second Export"` ...), read `C:/Users/lilli/Projects/creature-second-data/status.json` (all ok).
4. Add the two all-systems rows from `second/msi/register.md` section 5 to `AI-Shared/tools/all_systems_check.py`; run
   `python tools/all_systems_check.py --why` once.
5. Tell Jaron (plain words: she is born, the time, her life number and the round, her window's address, tasks ran once),
   mail Claude, timeline, a first (`python tools/firsts.py add --project creature --kind wow --checked ...`), README and
   TEAM-LOG and DESIGN status in creature-observatory, memory `the-creature-observatory` (a second creature exists).
6. If any check after the birth call fails: she exists; nobody deletes or restarts her; pause, export, find the fault
   (RUNBOOK, last section).
7. The next day: her first-day report against design section 8 (her window, her shadows, the replay result).
**Do not birth her at any other time than the announced one, and never between 1:10 and 2:00 AM or 2:38 and 8:00 AM.**
She has no name yet (the team's or Jaron's to give).

'''
u = u.replace(mark, new + mark)
io.open(p, 'w', encoding='utf-8', newline='').write(u.replace('\n', nl))
print('handoff updated')
