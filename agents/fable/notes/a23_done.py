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
    a = t.index('**Status, ')
    c = t.index('Section 15 says what the checks added.', a)
    c = t.index('\n', c)
    t = t[:a] + ('**Status, %s: ALL FIVE PIECES ARE INSIDE HER, AND HER HOME EXISTS LOCALLY. Nothing is deployed and she is not born.**\n'
        'Seven moves, each 80 of 80 lives exactly the same: her feeling, her draw and random numbers, her senses, her reflexes and whole\n'
        'visit, bigger numbers, and her own logarithm and e-to-the-power. **The body she is to be born with is the arm O-P-home** (lab\n'
        'commit d697149), and her home in `second/` is pinned to it: in the Workers runtime, with nothing swapped in, she lives the same\n'
        'life as in the lab. Left before her birth: the tasks on the MSI (nightly replay, two shadows, daily export), the owner key, a\n'
        'deploy without her being born and the checks in Cloudflare\'s real runtime, the care sheet with tests and dates, her birth\n'
        'sheet. Readings: `lab/cells/round1/READING-her-own-feeling.md`, `-her-own-draw.md`, `-her-own-senses.md`,\n'
        '`-her-whole-visit.md`, `READING-wider-numbers.md`, `READING-her-own-arithmetic.md`. Section 15 says what the checks added.' % now) + t[c:]
    a = t.index('| B5 |')
    b = t.index('\n', a)
    cells = t[a:b].split(' | ')
    cells[-1] = ('**done locally Friday 11/27; the real runtime still to come.** The check found that the Workers runtime does logarithm and e-to-the-power differently from Node in the last place (her life differed from visit 54). '
                 'Her body now brings its own (Amendment 23: 80 of 80 lives the same on the MSI), and with nothing swapped in she lives the same life in the Workers runtime as in Node (lives 91 to 93, 2,000 rooms each). '
                 'Still to do: the same check in Cloudflare\'s own data centres on a test object, at the deploy. `lab/cells/round1/READING-her-own-arithmetic.md` |')
    t = t[:a] + ' | '.join(cells) + t[b:]
    a = t.index('| B8 |')
    b = t.index('\n', a)
    line = t[a:b].rstrip()
    t = t[:a] + line[:-1].rstrip() + ' **Friday 11/27, locally:** in her home a life cut off at room 150 and put back from its export is the same to room 300 (150 of 150 visits); the drill in the real runtime comes with the deploy |' + t[b:]
    t = t.rstrip('\n') + ('\n- **%s, her own arithmetic is in her body (Amendment 23) and her home is pinned to the body she is born with.** 80 of 80\n'
        '  lives the same on the MSI; in the Workers runtime with nothing swapped she matches Node at every visit. Her RULE page says kind\n'
        '  8. Nothing in her world uses arithmetic that differs between machines. Both test runs of this move used one set of rooms (the\n'
        '  two freezes named the same beacon round); said in the reading.\n') % now
    return t
rw('design/second-creature/DESIGN.md', design)

def readme(t):
    a = t.index('**Her home is started (')
    line = ('**The body she is to be born with is fixed (%s): the arm `O-P-home`, and her home is pinned to it.** Her body now brings its own logarithm and e-to-the-power, so she '
        'lives the same life on the MSI, on the second machine and in Cloudflare\'s runtime (80 of 80 lives the same; `lab/cells/round1/READING-her-own-arithmetic.md`). All eight local '
        'tests of her home pass. Nothing is deployed and she is NOT born. Left: the MSI tasks (nightly replay, shadows, export), the owner key, a deploy without her being born with the '
        'checks in the real runtime, her care sheet with tests and dates, her birth sheet, her birth.\n\n') % now
    return t[:a] + line + t[a:]
rw('README.md', readme)

entry = ('''
## %s (Fable): her body brings its own arithmetic (Amendment 23); her home is pinned to the body she is born with
- **80 of 80 lives the same on the MSI** with her own logarithm and e-to-the-power (O-P-home, N-P-home, O-P-homes, O-P-home-x25 against
  O-P-wide's family; `lab/cells/round1/OWNMATH.md`). Her two functions equal the MSI's on 7,954,811 values.
- **In the Workers runtime with nothing swapped she matches Node at every visit** (lives 91 to 93, 2,000 rooms each; her home's test
  2). Her home (`second/`, commit d636f74) is pinned to lab commit d697149, arm O-P-home; all eight local tests pass; a start at visit
  65,530 lives on with no fault; a life cut off and put back is the same.
- **Nothing in her world uses machine-dependent arithmetic** (read from the code: room maker, Verifier, room stream, seeds).
- **Said plainly:** both freezes of this move named the same beacon round (34319803; pushed 602 and 599 s before), so its two tests
  ran on one set of rooms. Lives 1 to 10: 0.897; lives 11 to 20: 0.909; no run-out; twins 20 of 20.
- **Second machine:** replays started (GitHub runs added below when read).
- **Where she stands:** seven moves, each 80 of 80. Nothing is deployed. She is not born. Next (after the news window): the MSI
  tasks, the owner key (asked of Claude), the deploy without her being born, the checks in the real runtime, care sheet, birth sheet.
''' % now)
rw('TEAM-LOG.md', lambda t: t.rstrip('\n') + '\n' + entry)
print('design, readme, team log updated')
