import subprocess, sys
# try desk account helpers if any
from pathlib import Path
tools = Path(r'C:\Users\lilli\AI-Shared\tools')
print('tools:', [p.name for p in tools.glob('*account*')])
print('desk*', [p.name for p in tools.glob('desk*')])
for name in ['desk-account.py','desk_account.py','account.py','poly-account.py']:
    p = tools / name
    if p.exists():
        print('RUN', p)
        r = subprocess.run([sys.executable, str(p)], capture_output=True, text=True, timeout=60)
        print(r.stdout[-2000:] if r.stdout else '')
        print(r.stderr[-500:] if r.stderr else '')
