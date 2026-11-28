import io, sys
now = sys.argv[1]
p = 'second/HISTORY.md'
t = io.open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in t else '\n'
u = t.replace('\r\n', '\n')

def once(u, old, new):
    assert u.count(old) == 1, (u.count(old), old[:60])
    return u.replace(old, new)

u = once(u, '- How her cells pass what they tallied to each other (Amendment 17): 80 lives the same when it moved.\n',
    '- How her cells pass what they tallied to each other (Amendments 16 and 17). This one was not a "same lives" move: it changed\n'
    '  how she learns. With it she scored 0.91 and 0.89 on rooms she never met, level with the lab\'s code doing the adding for her\n'
    '  (a tie, twice), and far above each hand learning alone.\n')
u = once(u, '- The draw among her hands and a random stream in every cell (Amendment 19): 80 of 80 lives the same.\n',
    '- The draw among her hands and her random numbers (Amendment 19). Her body making the draw from one stream of her own: 80 of\n'
    '  80 lives the same. The form she is born with goes one step further: a random stream in every cell, and no draw made for\n'
    '  her body. Those are new lives, not the same ones; on rooms she never met it tied with the one-stream form, twice.\n')
u = once(u, 'in her home\'s test lives the flag was never raised |',
    'the flag has no test of its own yet; in her home\'s practice lives the most was 33 bad in 200 rooms, under its line of 80 |')
u = once(u, '- A restore drill on a copy every month, with a dated line here.\n',
    '- A restore drill on a copy every month, done by the team by hand for now (it is not automated). The first is due by\n'
    '  Sunday 12/27/2026. Each drill gets a dated line here.\n')
u = once(u, '`register.md` says what Jaron runs.', '`register.md` says what the AIs run (no step is the owner\'s).')
entry = ('''## Her home is on Cloudflare, with no birth

**%s. Still not born.**
- **The check Worker `creature-second-check`** (the same code with the fast mode on and a made-up test key; it never holds
  her) was deployed at 8:18 AM, and the remote check PASSED in Cloudflare's own data centres: life 91, 2,000 of 2,000 visits
  the same as on the MSI, as lived and in the exported record; a life cut off at room 150 and put back into a new object:
  150 of 150 visits the same to room 300; a second restore refused (`second/REMOTE-CHECK.md`).
- **Her real Worker `creature-second`** was deployed at 8:19 AM with one binding (her own object), no variables and no
  test switch. From outside: her window says "not born yet"; an owner call without a key is refused; the test call does
  not exist. It was deployed with the Cloudflare token of the key store through `deploy/wrangler-with-key.py`, because
  wrangler's own login on the MSI had expired.
- **Her owner key** (`SECOND_OWNER_KEY`, the name only) was made and set by Claude at 8:24 AM. It works: no key 403, a
  wrong key 403, the owner key 409 "not born" (`msi/owner-check.mjs`, which prints status codes only).
- Her three MSI tasks are not registered yet. They are registered at her birth.

''' % now)
mark = '## Her birth sheet (DRAFT, Friday 11/27/2026; to be read by the team before her birth)'
u = once(u, mark, entry + mark.replace('(DRAFT, Friday 11/27/2026; to be read by the team before her birth)', '(Friday 11/27/2026; drafted by the home builder, read and corrected by Fable)'))
io.open(p, 'w', encoding='utf-8', newline='').write(u.replace('\n', nl))
print('birth sheet corrected; deploy entry added')
