import subprocess, sys
py = sys.executable
trade = r'C:\Users\lilli\AI-Shared\tools\desk-trade.py'
desk = r'C:\Users\lilli\AI-Shared\tools\desk.py'

def run(args, timeout=120):
    r = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
    print('RC', r.returncode)
    if r.stdout: print(r.stdout[-2000:])
    if r.stderr: print('ERR', r.stderr[-1000:])
    return r.returncode

print('=== TENN BOOK ===')
run([py, desk, 'book', 'aec-cfb-tenn-ark-2026-10-10'], timeout=90)
print('=== TENN DRY ===')
rc = run([py, trade,
    '--by', 'grok-bot/satya-twin',
    '--slug', 'aec-cfb-tenn-ark-2026-10-10',
    '--side', 'yes',
    '--size', '5',
    '--why', 'TENN0-ARK0 early 2Q ESPN TENN WP89.6 vs Volunteers ask~0.80 about 10c under; mid-game ride',
    '--kill', 'ARK leads or ESPN TENN WP under 70',
    '--dry-run'], timeout=120)
if rc == 0:
    print('=== TENN LIVE ===')
    run([py, trade,
        '--by', 'grok-bot/satya-twin',
        '--slug', 'aec-cfb-tenn-ark-2026-10-10',
        '--side', 'yes',
        '--size', '5',
        '--why', 'TENN0-ARK0 early 2Q ESPN TENN WP89.6 vs Volunteers ask~0.80 about 10c under; mid-game ride',
        '--kill', 'ARK leads or ESPN TENN WP under 70'], timeout=120)
else:
    print('dry failed, no live')
