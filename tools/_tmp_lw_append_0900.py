from datetime import datetime, timezone
path = r'C:\Users\lilli\AI-Shared\state\live-wire.md'
now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%MZ')
line = (
  f"{now} | SESSION | board 12 live / 0 flagged (13:03Z) | before: YES Radivojevic #875 RESOLVED prior pass -USD8.33; no open Live Wire | "
  f"confirmed sportschau Medvedev set+ 7-5 S2 4-3 vs YES 0.95/0.96; scoremania Giustino sets-split 7-5 6-7 S3 40-30 vs YES 0.87/0.88; "
  f"GSA KBO Kia 5-5 BOTTOM 9th vs YES 0.49/0.53 | no open Live Wire to hold/exit | no new trade | "
  f"closest skip: Kia Tigers @0.50 (tied B9 ~fair after -0.23 from 0.72; not hard lag) | "
  f"skipped: Medvedev set-up chalk @0.95; Giustino deciding-set chalk @0.87 (#204 vs #708); Bouzige crash @0.17 unconfirmed; "
  f"Komano @0.16 unconfirmed; Pennaforti no book; valorant/CS2/dota/AFCON/crypto never | quiet (no loss over USD5) | Open Live Wire: none"
)
with open(path, 'a', encoding='utf-8') as f:
  f.write(line + '\n')
print('appended')
print(line)
