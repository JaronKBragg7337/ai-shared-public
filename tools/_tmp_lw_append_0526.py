from datetime import datetime, timezone
path = r'C:\Users\lilli\AI-Shared\state\live-wire.md'
now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%MZ')
lines = [
  f"{now} | WATCH NO TRADE | Brooksby YES aec-atp-jenbro-lorson-2026-09-24 | ESPN Chengdu: Brooksby 2-2 Sonego 1st set (tied); desk YES 0.590/0.600 - no score lead / early fair-to-rich for Brooksby - skip",
  f"{now} | WATCH NO TRADE | Mertens YES aec-wta-elimer-majchw-2026-09-24 | ESPN Singapore: Mertens 2-2 Chwalinska 1st set (tied); desk YES 0.520/0.530 - early tie priced fair - skip",
  f"{now} | WATCH NO TRADE | Volynets YES aec-wta-katvol-kimbir-2026-09-24 | ESPN Seoul QF SUSPENDED: Volynets 6-2 2-6 2 vs Birrell 2-6 6-2 4 (trail set3); desk YES 0.300/0.310 - crash matches trail+suspend - skip",
  f"{now} | WATCH NO TRADE | ITF shiye-zijjia aec-itfwo-shiye-zijjia-2026-09-25 | desk YES 0.590/0.600 / no verified live board this wake - skip",
  f"{now} | WATCH NO TRADE | TT mukvit-korvit | earlier desk ~0.33 then dropped off live list; setka-live.json [] no verified board - skip",
  f"{now} | RESEARCH | desk live/account; ESPN web API wta/atp groupings (Volynets Suspended; Mertens/Brooksby 1st-set 2-2); setka empty; Sofascore 403; Elon Twin ABSENT feed+brief 09-25",
  f"{now} | SESSION | desk OK msi-heartbeat | cash avail ~USD16.04 | open live LW 0 | streak 0 next USD5 | no new entry | quiet (no loss over USD5; MSI OK)",
]
with open(path, 'a', encoding='utf-8') as f:
  for L in lines:
    f.write(L + '\n')
print('appended', len(lines))
for L in lines:
  print(L)
