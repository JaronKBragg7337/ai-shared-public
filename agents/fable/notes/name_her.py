import io, sys
now = sys.argv[1]

def rw(p, f):
    t = io.open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in t else '\n'
    u = t.replace('\r\n', '\n')
    u2 = f(u)
    assert u2 != u, p
    io.open(p, 'w', encoding='utf-8', newline='').write(u2.replace('\n', nl))

def once(u, old, new):
    assert u.count(old) == 1, (u.count(old), old[:60])
    return u.replace(old, new)

def page(u):
    u = once(u, '<title>Her window</title>', '<title>Tessa Tally</title>')
    u = once(u, '<h1>Her window</h1>', '<h1>Tessa Tally</h1>')
    u = once(u, '<p>One small creature, and what she is doing. Private.</p>', '<p>Her window. One small creature, and what she is doing. Private.</p>')
    return u
rw('second/src/page.mjs', page)

NAME = ('**Her name is Tessa Tally.** Jaron named her on %s, mixing it from the lists Fable and Claude each made on their own. '
        'Her nickname is Bee, rarely used; we call her Tessa. She has no middle name.') % now

def history(u):
    mark = '### 1. What she is, in five lines\n'
    return once(u, mark, '### Her name\n' + NAME + ' Tessa, from tessera, one small tile of a mosaic: she is 37 small tiles that fit\ntogether, each holding the whole pattern. Tally, because she keeps her own count now. Bee, because a bee makes honeycomb, the shape\nof her body, and B is the second letter.\n\n' + mark)
rw('second/HISTORY.md', history)

def readme(u):
    a = u.index('**The body she is to be born with is fixed (')
    return u[:a] + NAME + ' Her birth is set for Friday 11/27/2026, 8:00 PM. Her home is on Cloudflare with no birth; her window: https://creature-second.acsassociation7337.workers.dev (private; only people with the link).\n\n' + u[a:]
rw('README.md', readme)

def design(u):
    old = '- She has no name.'
    assert u.count(old) == 1
    return u.replace(old, '- ~~She has no name.~~ **Her name is Tessa Tally** (Jaron, %s; nickname Bee, rarely used; we call her Tessa).' % now)
rw('design/second-creature/DESIGN.md', design)

entry = ('''
## %s (Fable): her name is Tessa Tally, and everything is ready for her birth tonight
- **Her name (Jaron's go, through Claude, 8:50 AM): Tessa Tally.** Nickname Bee, rarely used; we call her Tessa. He mixed it from the
  two lists Fable and Claude made without seeing each other's.
- **Her birth: tonight, Friday 11/27, 8:00 PM.** The drand round is named in a pushed commit at about 7:00 PM (not earlier, so that
  he can still move the time). Her life number comes from that round.
- **Ready:** her real Worker `creature-second` is deployed with no birth and her owner key works; the checks in Cloudflare's own data
  centres passed on the check Worker; her birth path was rehearsed there; her birth sheet is in `second/HISTORY.md`; all 11 local
  tests of her home pass; her three MSI tasks are built and get registered at her birth.
- **Also since the last entry:** the MSI's 1:15 AM integrity test ended incomplete on 11/27 because my lab lives ran from 1:31 AM; no
  harm; the quiet window is now 1:10 to 2:00 AM.
''' % now)
rw('TEAM-LOG.md', lambda u: u.rstrip('\n') + '\n' + entry)
print('her name is in the page, her history, the README, the design and the team log')
