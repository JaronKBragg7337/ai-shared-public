import subprocess, sys
cmds = [
  [sys.executable, r'C:\Users\lilli\AI-Shared\tools\desk-trade.py', '--by', 'grok-bot/satya-twin', '--slug', 'atc-lmx-tig-tol-2026-10-09-tig', '--side', 'yes', '--size', '5', '--why', 'Tigres 3-2 Toluca minute 83 ESPN home lead; YES ask lag check dry-run', '--kill', 'Toluca equalizes or leads', '--dry-run'],
  [sys.executable, r'C:\Users\lilli\AI-Shared\tools\desk-trade.py', '--by', 'grok-bot/satya-twin', '--slug', 'aec-cfb-washst-utahst-2026-10-09', '--side', 'no', '--size', '5', '--why', 'WSU 16-USU 17 end 4Q ESPN USU WP91 dry-run book check', '--kill', 'WSU leads or OT flip', '--dry-run'],
  [sys.executable, r'C:\Users\lilli\AI-Shared\tools\desk-trade.py', '--by', 'grok-bot/satya-twin', '--slug', 'aec-cfb-iowast-byu-2026-10-09', '--side', 'no', '--size', '5', '--why', 'BYU 21-ISU 3 late 3Q ESPN BYU WP99 dry-run book check', '--kill', 'ISU within one score', '--dry-run'],
]
for c in cmds:
    print('CMD', ' '.join(c[3:8]))
    r = subprocess.run(c, capture_output=True, text=True, timeout=90)
    print('code', r.returncode)
    print((r.stdout or '')[-1500:])
    print((r.stderr or '')[-800:])
    print('====')
