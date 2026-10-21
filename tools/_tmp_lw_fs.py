from datetime import datetime, timezone
path = r'C:\Users\lilli\AI-Shared\state\live-wire.md'
now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%MZ')
lines = [
  f"{now} | EYES Flashscore return | Rapolu page 404 | Mayot LIVE earlier Mayot 1-0 sets set2 4-4 15-30 Chidekh srv — by follow-up YES already 0.98/0.99 near-locked skip (fav>=0.85)",
  f"{now} | BABYSIT RESTING | Rapolu CJPE8WZTJW22 still NEW 13.89@0.36 | LiveScore S3 sets 1-1 (Rapolu took set2 6-1) games 0-0 | ESPN JSON still shows set2 6-1 linescores | book STILL 0.35/0.36 sticky lag | cash USD36.58 | leave resting",
  f"{now} | WATCH NO TRADE | Kotov YES 0.59/0.62 (was 0.83) spread 3c + no ESPN board this wake - skip",
]
with open(path, 'a', encoding='utf-8') as f:
  for L in lines:
    f.write(L + '\n')
print('ok')
