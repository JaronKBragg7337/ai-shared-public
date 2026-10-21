import subprocess, sys, os
from pathlib import Path
tools = Path(r'C:\Users\lilli\AI-Shared\tools')
# find account helpers
cands = list(tools.glob('*account*')) + list(tools.glob('*pos*')) + list(tools.glob('poly*.py')) + list(tools.glob('*book*'))
print('cands', [p.name for p in cands])
# desk.py subcommands
r = subprocess.run([sys.executable, str(tools/'desk.py'), '-h'], capture_output=True, text=True, timeout=30)
print('desk help:', (r.stdout or r.stderr)[:1500])
# try common invocations
for args in [
    ['account'], ['positions'], ['pos'], ['status'], ['bal'], ['balance'],
]:
    r = subprocess.run([sys.executable, str(tools/'desk.py'), *args], capture_output=True, text=True, timeout=60)
    out = (r.stdout or '') + (r.stderr or '')
    if out.strip() and 'unrecognized' not in out.lower() and 'invalid' not in out.lower() and 'usage:' not in out.lower()[:80]:
        print('OK desk.py', args, '->')
        print(out[-2000:])
