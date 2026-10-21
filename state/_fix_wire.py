from pathlib import Path
p = Path(r'C:\Users\lilli\AI-Shared\state\live-wire.md')
text = p.read_text(encoding='utf-8')
lines = text.splitlines(True)
while lines and not lines[-1].strip():
    lines.pop()
if lines:
    lines.pop()
line = (
    '2026-10-10 ~4:54 PM ET: Live Wire EXIT+1. MSI OK (streak 0). desk.py rules: CFB OPEN; soccer/basketball $1 cap OPEN; NFL closed. '
    'EXIT #1193 NO UCLA-ORE (closes Satya #1192): ESPN UCLA 10-6 ORE ~2:57 2Q edge gone vs ORE-lead entry @0.80, exit ~0.46 filled (uPnL about -$1.3). '
    'NEW #1194 YES HOU 5.62sh @0.885 FILLED: ESPN HOU 21-3 KSU 3:17 2Q Cougars ~0.88 vs ~0.93 WP +18 mid-2Q. '
    'UCLA YES leader-under-50c Bruins 0.45 REFUSED (satya-twin already holds this game). '
    'desk $7.22 avail, 2 open: YES HOU + YES Aliens leave. Quiet.\n'
)
p.write_text(''.join(lines) + line, encoding='utf-8')
print('fixed')
