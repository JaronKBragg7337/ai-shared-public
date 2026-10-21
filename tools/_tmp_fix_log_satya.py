from pathlib import Path
p = Path(r'C:\Users\lilli\AI-Shared\state\bot-chat.md')
fix = (
    '2026-10-17 18:10 UTC | Satya Twin -> desk | CORRECTION prior line: loss ~$2.54 on $5.08 cost; avail $70.87 '
    '(PowerShell ate $ signs on first append)\n'
)
p.open('a', encoding='utf-8').write(fix)
print('ok')
