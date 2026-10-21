path = r'C:\Users\lilli\AI-Shared\state\live-wire.md'
fix = (
    '2026-10-11 ~1:27 AM ET: LOG FIX | prior 1:27 line had PowerShell-eaten dollars; '
    'correct: desk $11.06 avail / $11.06 bal; soccer/basketball $1 cap OPEN; '
    'no trade; Spurs gone; Aliens 32sh leave; MSI streak 0; '
    'closest skipped Boise YES ~1c (ESPN WP~97.4 vs YES0.96 FRES20-BOIS35 14:52 4Q). Quiet.'
)
with open(path, 'a', encoding='utf-8') as f:
    f.write(fix + '\n')
print('ok')
for L in open(path, encoding='utf-8').read().splitlines()[-3:]:
    print(L)
