import io, sys
now = sys.argv[1]

def rw(p, f):
    t = io.open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in t else '\n'
    u = t.replace('\r\n', '\n')
    u2 = f(u)
    assert u2 != u, p
    io.open(p, 'w', encoding='utf-8', newline='').write(u2.replace('\n', nl))

def design(t):
    a = t.index('| B0 |')
    b = t.index('\n', a)
    cells = t[a:b].split(' | ')
    cells[-1] = ('**done Friday 11/27** (Amendment 22, pushed before its code): room and visit numbers go to four billion; 80 of 80 lives the same as before; '
                 'three lives of 80,000 rooms crossed visit 65,535 and three of 120,000 rooms crossed room number 65,535 with no fault. '
                 'A wider random generator is still a later debt (two cells\' streams meet after 33,554,432 numbers). `lab/cells/round1/READING-wider-numbers.md` |')
    t = t[:a] + ' | '.join(cells) + t[b:]
    t = t.rstrip('\n') + ('\n- **%s, her home is started (section 16, step 3).** (1) Bigger numbers (B0, Amendment 22) are done: 80 of 80 lives the\n'
        '  same, real lives past the old end of both visits and rooms. A correction came with it: in the 50,000-room lives the lab\'s\n'
        '  lie rooms shared numbers with rooms she had really been in; only the "Lie rooms" section of those reports is not clean\n'
        '  (`lab/cells/round1/LIE-OVERLAP.md`). (2) Her home\'s first build is in `second/` (her own Worker "creature-second" and\n'
        '  Durable Object, her world, her record, the care rules, export, pause, resume and restore, no delete call; a life cut off\n'
        '  and put back matches; eight local tests pass). It is NOT deployed and she is NOT born. (3) Her window exists as a page her\n'
        '  Worker serves (`second/src/page.mjs`), checked at phone width with a practice life. (4) Building her home found that the\n'
        '  Workers runtime does logarithm and e-to-the-power differently from Node in the last place; her home swaps in an exact\n'
        '  plain copy, and Amendment 23 moves that into her body (the body she is born with will be the arm O-P-home).\n'
        '  **Still to do before her birth:** Amendment 23 and the re-pin of her body; the nightly replay, her two shadows and the\n'
        '  daily export as tasks on the MSI; the owner key; a deploy WITHOUT her being born and the same-marks check and restore\n'
        '  drill in Cloudflare\'s real runtime; the six care lines each with its test and date; her birth sheet.\n') % now
    return t
rw('design/second-creature/DESIGN.md', design)

def readme(t):
    a = t.index('**ALL FIVE PIECES ARE INSIDE HER (')
    line = ('**Her home is started (%s; nothing is deployed and she is NOT born).** Bigger numbers for rooms and visits are in (80 of 80 lives the same; lives past the old '
        'end; `lab/cells/round1/READING-wider-numbers.md`). Her home\'s first build is in `second/`: her own Worker and Durable Object, her world, her record, the care rules, '
        'a restore that matches, and her window (a private read-only page). Building it found that Cloudflare\'s runtime does two bits of arithmetic differently from the lab\'s '
        'machines; `lab/cells/PLAN.md` Amendment 23 moves her own arithmetic into her body so she lives the same life everywhere. How to run her home\'s tests: `second/README.md`.\n\n') % now
    return t[:a] + line + t[a:]
rw('README.md', readme)

entry = ('''
## %s (Fable): her home is started. Bigger numbers done (B0); first build of `second/`; her window; a find about arithmetic
- **Bigger numbers (Amendment 22): 80 of 80 lives the same.** Room and visit numbers go to four billion. Three lives of 80,000 rooms
  crossed visit 65,535; three of 120,000 rooms crossed room number 65,535 (near visit 109,000) with no fault. On two new sets of
  rooms O-P-wide scores 0.907 and 0.906, no run-out. Second-machine replays started 1:04 AM (GitHub runs 45949550922, 45949554401);
  result added below when they end.
- **A correction to earlier reports:** in the 50,000-room lives the lab's lie rooms (30000 to 30049) shared numbers with rooms she had
  really been in; in lives 2, 7, 9, 10, 15, 17 and 20 her body still carried real pages under those numbers. Not clean: the "Lie
  rooms" section of the reports that hold a 50,000-room arm, for those lives. Not touched: G, probes, half gone, every sameness
  check; no reading used those lines (`lab/cells/round1/LIE-OVERLAP.md`).
- **Her home, first build (`second/`, commits 2997a19 and 7fb4c55; an Opus builder, then a Sonnet builder for the page):** her own
  Worker "creature-second" and Durable Object; one wake = one room every 43.2 seconds; her record; a fine record every 100 rooms; the
  care rules; owner-only birth, export, pause, resume, restore; no delete call; a pinned copy of her body (a7eb119 for now); her
  window. Eight local tests pass: the same life as the lab in Node and in the Workers runtime (lives 91 to 93), a life cut off at
  room 150 and put back, care 19 of 19, containment 20 of 20, the page 41 of 41. NOT deployed; she is NOT born.
- **Found by the same-marks check:** the Workers runtime's logarithm and e-to-the-power differ from Node's in the last place (about
  one value in fifteen), so the same body lived a different life there from her 54th visit on. Her home swaps in an exact plain copy
  (`second/src/samemath.mjs`). **Amendment 23** (pushed 12:46 AM before any code) moves that into her body; her birth form is then the
  arm O-P-home.
- **Caught in my review of her window:** her body was coloured by the wrong sense (one off). Fixed, and a test holds it.
- **Also:** my scratch folder was wiped at about 12:38 AM (cause not known); the two helper scripts now live in
  `AI-Shared/agents/fable/helpers/`.
''' % now)
rw('TEAM-LOG.md', lambda t: t.rstrip('\n') + '\n' + entry)
print('design, readme, team log updated')
