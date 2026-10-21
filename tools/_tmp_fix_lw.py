from pathlib import Path
p = Path(r'C:\Users\lilli\AI-Shared\state\live-wire.md')
lines = p.read_text(encoding='utf-8').splitlines()
lines[-1] = '2026-09-30 08:08Z | SESSION | board 19 live / 3 flagged (07:58Z) | before: flat Live Wire (NO Snigur exited prior) | confirmed ESPN Bai 2-6 0-0 Fruhvirtova 2nd YES 0.34/0.35; ESPN Cerundolo 2-5 Bu 1st YES 0.12/0.13; ESPN Fils 6-3 1-0 Van Assche YES 0.97/0.98; Inglis book 0.93/0.94 (ESPN blank; board had set-up); Lehecka Suspended book 0.85/0.87; SD series after G1 8-0 SD 0.75/0.80 CHC 0.22/0.25 | no exits | no new trade | closest skip: NO Bai post-set1 6-2 @YES0.34 mild (home Q) / YES Inglis chalk @0.94 / Lehecka settle skipped still Suspended / Cerundolo 2-5 NO chalk / Fils chalk | quiet (no loss over $5) | Open Live Wire: 0'
p.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(lines[-1])
