from datetime import datetime, timezone
path = r"C:\Users\lilli\AI-Shared\state\live-wire.md"
now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")
lines = [
"{t} | WATCH NO TRADE | TT absent on desk live this wake",
"{t} | WATCH NO TRADE | IND YES aec-nfl-ind-kc-2026-09-20 YES 0.285/0.290 | ESPN/CBS IND0-KC0 ~10:54 1Q - IND drive to KC20 false start - score not moved; early fair underdog - no lag",
"{t} | WATCH NO TRADE | MIA YES atc-mls-mia-sdg-2026-09-20-mia YES 0.610/0.620 | FotMob/ESPN MIA1-SD1 49' (Dreyer 12 Messi 24) - tied 2H fair not sticky lag",
"{t} | WATCH NO TRADE | TIJ YES atc-lmx-pac-tij-2026-09-20-tij YES 0.400/0.410 | ESPN TIJ1-PAC0 27' - away lead early priced ~fair; no verified post-goal lag",
"{t} | WATCH NO TRADE | TOL YES atc-lmx-tol-san-2026-09-20-tol YES 0.920/0.930 | ESPN TOL1-SAN0 28' - ask above 0.85 - skip",
"{t} | WATCH NO TRADE | MIL YES aec-mlb-mil-bal-2026-09-20 YES 0.805/0.810 | MLB API MIL2-BAL0 Bot4 - leading fair fav near 0.85 band - no lag",
"{t} | WATCH NO TRADE | DET total tsc-mlb-det-cws-2026-09-20-8pt5 0.340/0.355 | MLB API DET1-CWS6 Top8 - late blowout; DET ML longshot band - skip",
"{t} | WATCH NO TRADE | POR YES aec-wnba-por-la-2026-09-20 YES 0.040/0.050 | ESPN POR49-LA66 7:29 3Q - under 0.10 longshot - skip",
"{t} | WATCH NO TRADE | Quevedo aec-wta-kaique-nadpod-2026-09-20 YES 0.550/0.560 | TNT/Tennis.com Not started - no set score - skip",
"{t} | WATCH NO TRADE | cricket aec-cplcr-aabf-jka-2026-09-20 YES 0.530/0.550 | no verified live score this wake - skip",
"{t} | WATCH NO TRADE | IND-KC spreads/totals/props | ESPN IND0-KC0 1Q - early fair; no ML-style score lag",
"{t} | RESEARCH | desk live/book/account; ESPN site.web.api (NFL/MLS/LMX/WNBA/NHL); MLB statsapi; CBS IND-KC PBP; FotMob MIA-SD; TNT Quevedo; Elon Twin ABSENT 2026-09-20",
"{t} | SESSION | desk OK msi-heartbeat | cash avail USD40.36 | open live LW 0 | streak 2 next USD5 | no new trade | quiet (no loss over USD5; MSI OK)",
]
with open(path, "a", encoding="utf-8") as f:
    for ln in lines:
        f.write(ln.format(t=now) + "\n")
print("appended", len(lines), "lines at", now)
