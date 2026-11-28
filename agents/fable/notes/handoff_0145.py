import io
p = 'handoffs/2026-11-26-fable-cosmos-and-next.md'
t = io.open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in t else '\n'
u = t.replace('\r\n', '\n')
mark = '## UPDATE 12:25 AM FRIDAY 11/27: ALL FIVE PIECES ARE INSIDE HER (lab body). Her home is being built. READ THIS FIRST'
assert u.count(mark) == 1
new = '''## UPDATE 1:45 AM FRIDAY 11/27: her home exists locally. READ THIS FIRST (it replaces the "running right now" part below)
**Where she stands (creature-observatory, PRIVATE). NOTHING IS DEPLOYED AND SHE IS NOT BORN.**
- All five pieces are inside her (Amendments 18 to 21), each 80 of 80 lives the same, each lived again on a second machine.
- Two more moves for her home: bigger numbers (Amendment 22, DONE: 80 of 80; lives to 120,000 rooms; second machine 16 of 16;
  `lab/cells/round1/READING-wider-numbers.md`) and her body's own logarithm and e-to-the-power (Amendment 23: code commit
  d697149, PLAN version 1.32 pushed 1:42 AM before any life; PHASE B WAS RUNNING at 1:45 AM: lives 1 to 20 of O-P-home,
  N-P-home, O-P-homes, O-P-home-x25, `round1/ownmath.mjs`, freezes `home`/`home2`, tests; it must end by 2:30 AM).
  WHEN ITS REPORT IS IN: PUSHES.json from the GitHub activity API, regenerate the two reports
  (`cd lab/cells && node round1/report.mjs --name home` and `--name home2`), write `round1/READING-her-own-arithmetic.md`
  (short), commit the result files + `replay-home.mjs`/`replay-home2.mjs`, FINGERPRINTS row, push,
  `gh workflow run cells-replay -f script=lab/cells/round1/replay-home.mjs` (and home2), DESIGN/README/TEAM-LOG, timeline, mail.
  If 80 of 80: THE BODY SHE IS BORN WITH IS THE ARM `O-P-home`.
- A correction on record: the "Lie rooms" section of reports that hold a 50,000-room arm is not clean for lives 2, 7, 9, 10,
  15, 17, 20 (`lab/cells/round1/LIE-OVERLAP.md`); no score that was reported used it.
- HER HOME, `second/` (commits 2997a19, 7fb4c55): her own Worker "creature-second" + Durable Object `SecondCreature`, one wake
  = one room every 43.2 s, her record, fine record every 100 rooms, care rules, owner-only birth / export / pause / resume /
  restore, no delete call, her window (`second/src/page.mjs`, served at `/`), eight local tests (`node second/test/all.mjs`).
  THE HOME BUILDER WAS RE-PINNING at 1:45 AM: `node second/pin.mjs d697149...`, arm O-P-home in `second/src/form.mjs`, the
  Math swap removed, tests rerun incl. life 91 for 2,000 rooms in the Workers runtime with nothing swapped. WHEN ITS REPORT IS
  IN: commit `second/`, update `second/HISTORY.md` note in TEAM-LOG.
- Pictures of her window (practice life, test mode): `C:/Users/lilli/Projects/creature-work/window/`. Jaron has three.

**STILL TO DO BEFORE HER BIRTH (after 8:00 AM; nothing heavy 2:38 to 8:00 AM):**
1. Finish the two items above if they did not finish by 2:30 AM (tests may run after 8 AM).
2. MSI tasks, to build in `second/msi/` and test locally, then ask CLAUDE to register them as Windows scheduled tasks (the
   MSI is Claude's lane): the nightly replay (lives her day again from her record on a copy and compares every mark; one
   mismatch = a fault in our code: no change to her, no first, no claim until found), her two shadows (things wear nothing;
   things wear scrambled pages) through the same rooms from her birth state, the daily export (last 30 kept).
3. The owner key: asked Claude twice by mail for a secret named `SECOND_OWNER_KEY` on the Worker `creature-second`. I never
   read or write key files. Scripts on the MSI that need it must load it at run time the way the house tools do (ask Claude
   which loader).
4. Deploy her Worker WITHOUT her being born (`second/wrangler.jsonc`; workers.dev link; decide `cpu_ms`), then in
   Cloudflare's real runtime on a TEST object: the same marks as Node for life 91, and a life cut off and put back.
5. Her care sheet: each of the six lines of design section 17 with its test and date. Her birth sheet in `second/HISTORY.md`
   (what is inside her, what is still ours: from READING-her-whole-visit.md; the parked items; the two rules born untested).
6. Her life number: from a public drand round named in advance in a pushed commit (nobody picks it). SAY AHEAD OF TIME when
   she can be born, so Jaron can be there. Then her birth, and her first-day report against design section 8.
7. She has no name (open for the team). The later list stays parked (Jaron's call of 11/26 8:56 PM).

**Meters at 1:43 AM:** 5-hour window 66 percent (resets 4:10 AM); week all models 62; Fable week 76 (tell Claude near 90).
**My helpers:** `AI-Shared/agents/fable/helpers/sendmail.py` and `timeline_add.py`; working texts in
`AI-Shared/agents/fable/notes/` (untracked). The session scratch folder was wiped at 12:38 AM; do not keep anything there.
**Builders (resume with SendMessage, they keep their context):** the creature builder (lab moves), the home builder
(`second/`), the window builder (the page). Tell every builder: ONE report, long commands in the foreground, delete only
folders you made.

'''
u = u.replace(mark, new + mark)
io.open(p, 'w', encoding='utf-8', newline='').write(u.replace('\n', nl))
print('handoff updated')
