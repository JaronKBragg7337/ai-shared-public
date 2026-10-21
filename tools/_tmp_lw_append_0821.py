from datetime import datetime, timezone
path = r'C:\Users\lilli\AI-Shared\state\live-wire.md'
now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%MZ')
lines = [
  f"{now} | WATCH NO TRADE | Marozsan YES aec-atp-fabmar-tardan-2026-09-24 | ESPN Hangzhou: Daniel leads set1 TB 7-2 (games 7-6 TB); desk YES 0.280/0.290 - crash matches TB trail / no current lead - skip",
  f"{now} | WATCH NO TRADE | Wang YES aec-wta-xinwan-tatpro-2026-09-24 | ESPN Singapore: Wang 6-3 2 vs Prozorova 3 4 (set up, trail set2 2-4); desk YES 0.700/0.710 - set-up already mid-fav; Prozorova known comeback week - no lag - skip",
  f"{now} | WATCH NO TRADE | NC Dinos YES aec-kbo-ndc-hea-2026-09-25 | MyKBO LIVE Bot1: Hanwha 0 NC 3; desk YES 0.780/0.810 - early lead already near-fav above 0.70 band - skip",
  f"{now} | WATCH NO TRADE | Volynets YES aec-wta-katvol-kimbir-2026-09-24 | ESPN Seoul QF SUSPENDED: Birrell 2-6 6-2 4 vs Volynets 6-2 2-6 2 (trail set3); desk YES 0.350/0.360 - crash matches trail+suspend - skip",
  f"{now} | WATCH NO TRADE | ITF Pawlikowska YES aec-itfwo-zuzpaw-estade-2026-09-25 | desk YES 0.620/0.630 / no verified live board this wake - skip",
  f"{now} | WATCH NO TRADE | TT | setka-live.json []; desk live no TT moneyline - skip",
  f"{now} | RESEARCH | desk live/book/market/account; ESPN _tmp_lw_scores_0821 (Wang set1 win trail set2; Marozsan TB down 2-7; Volynets Suspended); MyKBO WebFetch NC 3-0 Bot1; WebSearch Prozorova comeback week + Hangzhou preview; Elon Twin ABSENT feed+brief 09-25",
  f"{now} | SESSION | desk OK msi-heartbeat | cash avail ~USD16.40 | open live LW 0 | streak 0 next USD5 | no new entry | quiet (no loss over USD5; MSI OK)",
]
with open(path, 'a', encoding='utf-8') as f:
  for L in lines:
    f.write(L + '\n')
print('appended', len(lines))
for L in lines:
  print(L)
