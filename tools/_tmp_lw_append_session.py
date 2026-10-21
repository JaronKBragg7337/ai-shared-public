from datetime import datetime, timezone
path = r'C:\Users\lilli\AI-Shared\state\live-wire.md'
ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%MZ')
line = (
  f"{ts} | SESSION | board 129 live / 2 flagged (23:18Z) | before: YES Ravens 27.78 + YES Vikings 41.73 + NO Saints dust | "
  f"confirmed ESPN MIN 23-16 TB Final WP99 (HOLD YES Vikings mark +13.5) | "
  f"ESPN BAL 24-28 DAL 1:47 Q4 1st&Goal then false start to DAL7 WP58.9 vs ~0.58 | "
  f"EXIT YES Ravens $10 #798 CRQWMHA4EYC6 FILLED ~17.09@0.58 leftover 10.69 (WP50 matched then) | "
  f"TRADE YES Ravens $10 #799 CRQWYG2C4YBE resting@0.58 then CANCEL after false start WP58.9 edge gone | "
  f"skipped: Over36.5 no book (total already 39); Mystics leader-under-50c but ESPN ATL WP66 fair; Raiders fair; -4.5 ask already 0.99 | "
  f"quiet (no loss over $5; MSI OK)\n"
)
with open(path, 'a', encoding='utf-8') as f:
    f.write(line)
print('appended', ts)
print(line[:200])
