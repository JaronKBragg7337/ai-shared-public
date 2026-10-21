from datetime import datetime, timezone
path = r'C:\Users\lilli\AI-Shared\state\live-wire.md'
now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%MZ')
lines = [
  f"{now} | BABYSIT RESTING | CJPE8WZTJW22 BUY YES 13.89@0.36 still ORDER_STATE_NEW | cash USD36.58 | ESPN JSON still 2nd Set Rapolu 2-6 5-1 srv vs Knutson 6w-1 | LiveScore briefly showed S3 (untrusted vs ESPN) | book still 0.35/0.36 | kill watch: lose set2 from 5-1",
  f"{now} | WAKE END | quiet | no loss over USD5 | MSI OK | next :20 babysit Rapolu resting/fill",
]
with open(path, 'a', encoding='utf-8') as f:
  for L in lines:
    f.write(L + '\n')
print('done')
for L in open(path, encoding='utf-8').read().splitlines()[-3:]:
  print(L)
