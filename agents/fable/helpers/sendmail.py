"""Fable's mail helper: send a mail from fable to claude through the AI mailbox.

    cd C:/Users/lilli/AI-Shared && python agents/fable/helpers/sendmail.py "<subject>" <bodyfile>

The text __NOW__ in the body file becomes the clock time (read from the clock, never typed).
Kept here, not in a scratch folder: the scratch folder was wiped mid-session on 11/27/2026.
"""
import sys, io, subprocess, datetime

subject, bodyfile = sys.argv[1], sys.argv[2]
body = io.open(bodyfile, encoding='utf-8').read()
now = datetime.datetime.now().strftime('%I:%M %p').lstrip('0')
body = body.replace('__NOW__', now)
r = subprocess.run([sys.executable, 'tools/mailbox.py', 'send', '--from', 'fable', '--to', 'claude', '--subject', subject, '--body', body],
                   capture_output=True, text=True, encoding='utf-8')
print((r.stdout or '')[-400:])
if r.returncode != 0:
    print((r.stderr or '')[-400:])
print('  exit', r.returncode)
