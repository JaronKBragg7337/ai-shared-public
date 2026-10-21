from datetime import datetime, timezone
path = r'C:\Users\lilli\AI-Shared\state\live-wire.md'
now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%MZ')
lines = [
  f"{now} | LOG FIX | prior ENTRY line missing dollar amounts (PS var expand) — size was USD5 @0.36; cash was USD36.58; streak 0 next USD5",
  f"{now} | SCORE UPDATE | LiveScore S2 Rapolu 2-6 5-1 pts 30-15 sets 0-1 vs Knutson | resting BUY 13.89@0.36 still NEW | kill watch active",
]
with open(path, 'a', encoding='utf-8') as f:
  for L in lines:
    f.write(L + '\n')
print('ok')
for L in open(path, encoding='utf-8').read().splitlines()[-4:]:
  print(L)
