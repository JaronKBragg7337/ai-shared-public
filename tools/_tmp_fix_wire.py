import pathlib
p = pathlib.Path(r'C:\Users\lilli\AI-Shared\state\live-wire.md')
lines = p.read_text(encoding='utf-8').splitlines()
fix = (
"2026-09-29 01:08Z | SESSION | board 84 live / 0 flagged (00:58Z) | before: no Live Wire open | "
"confirmed ESPN CHI 7-0 PHI [~12:00 2nd] (Keenum-Burden TD; Bears failed 4th&G; PHI driving after DPI; ESPN WP PHI 42.3 then ~47) "
"vs YES Eagles 0.34 then ripped to 0.46/0.56; BBC JAM 0-1 HON [49 min] (Figueroa 14; HT 0-1; HON 64 pct poss) vs Hnd YES 0.63/0.65 | "
"attempted YES Eagles $10 #848 @0.48 unfilled as book jumped; canceled CSDVR7ZGRYBE | no fill | "
"closest skip: YES Eagles @0.56 (now over ESPN WP; lag closed) | skipped: YES Hnd @0.65 (0-1@49 already priced); ITF unconfirmed; crypto never | "
"quiet (no loss over $5) | Open Live Wire: none"
)
if lines and lines[-1].startswith('2026-09-29 01:08Z'):
    lines[-1] = fix
else:
    lines.append(fix)
p.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(lines[-1])
