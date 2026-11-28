"""Fable's timeline helper: add one clock-stamped line to state/timeline.md and push it.

    cd C:/Users/lilli/AI-Shared && python agents/fable/helpers/timeline_add.py <textfile> "<commit subject>"

The time stamp is read from the clock (never typed). The text file's line breaks become spaces.
Kept here, not in a scratch folder: the scratch folder was wiped mid-session on 11/27/2026.
"""
import sys, io, subprocess, datetime

textfile, subject = sys.argv[1], sys.argv[2]
text = ' '.join(io.open(textfile, encoding='utf-8').read().split())
now = datetime.datetime.now()
stamp = now.strftime('%Y-%m-%d ') + now.strftime('%I:%M %p').lstrip('0')
line = '- %s %s' % (stamp, text)
p = 'state/timeline.md'
for attempt in range(3):
    subprocess.run(['git', 'pull', '-q', '--rebase', '--autostash', 'origin', 'main'])
    t = io.open(p, encoding='utf-8', newline='').read()
    if text not in t:
        nl = '\r\n' if '\r\n' in t else '\n'
        if not t.endswith('\n'):
            t += nl
        io.open(p, 'w', encoding='utf-8', newline='').write(t + line + nl)
    subprocess.run(['git', 'add', p])
    subprocess.run(['git', 'commit', '-q', '-m', subject, '-m', 'Co-Authored-By: Claude Fable 5.2 <<email>>'])
    if subprocess.run(['git', 'push', '-q', 'origin', 'main']).returncode == 0:
        h = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()
        print('timeline line pushed', stamp, h)
        break
else:
    print('TIMELINE PUSH FAILED after 3 tries')
