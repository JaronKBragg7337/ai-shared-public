import pathlib
p = pathlib.Path(r'C:\Users\lilli\AI-Shared\state\live-wire.md')
lines = p.read_text(encoding='utf-8').splitlines()
for i in range(len(lines)-1, -1, -1):
    if lines[i].startswith('2026-09-29 01:15Z') and 'no loss over )' in lines[i]:
        lines[i] = lines[i].replace('no loss over )', 'no loss over $5)')
        p.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        print('fixed:', lines[i][-90:])
        break
else:
    print('no match')
    for ln in lines[-3:]:
        print(repr(ln[-100:]))
