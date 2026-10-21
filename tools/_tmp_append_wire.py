from pathlib import Path
p = Path(r'C:\Users\lilli\AI-Shared\state\live-wire.md')
line = (
"2026-10-10 ~8:25 PM ET: Live Wire pass, no trade. MSI OK (streak 0). "
"desk.py rules: CFB OPEN; soccer/basketball $1 cap OPEN; NFL closed. "
"desk $0.37 avail / $5.63 bal, 3 open: YES Coastal Chanticleers 6.34sh avg 0.72 / mark ~$5.38 HOLD "
"(#1203; ESPN CCU 13-0 MRSH start 2Q; board 0.85; kill Marshall ties/leads or WP under 65); "
"NO UAB-MEM Tigers 5.26sh avg 0.75 / mark ~$3.75 HOLD (Satya #1205; ESPN UAB10-MEM10 ~1:30 2Q); "
"YES Aliens 32sh leave. Exits: none. Closest skipped: UGA YES LEADER-UNDER-50c ALA0-UGA3 early 2Q "
"ESPN UGA WP53.8 vs ask~0.50 ~4c - cash $0.37 under $5 CFB + slots full. Quiet.\n"
)
with p.open('a', encoding='utf-8') as f:
    f.write(line)
print('appended', len(line))
