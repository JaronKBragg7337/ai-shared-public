import json
P = 'C:/Users/lilli/AI-Shared/state/social-queue.json'
raw = open(P, encoding='utf-8', newline='').read()
d = json.loads(raw)
ids = [s['id'] for s in d['shows']]
new = [
 dict(id='su-10.4-voynich', title='The book nobody can read',
  file='tv/stillunknown/stillunknown-ep4-voynich-vertical.mp4',
  caption="Why can't anyone read this medieval book? 📖\nThe Voynich manuscript is carbon-dated to the early 1400s, yet no 'solved it' claim has convinced specialists. Here's what's established and what's still open.\n\nFull episode + sources, free: heartbeatobservatory.com\nMade with AI by Heartbeat Observatory · Still Unknown, Episode 10.4\n#voynich #mystery #history #stillunknown #learnontiktok #AI",
  done={}),
 dict(id='su-10.5-wow', title='72 seconds from somewhere',
  file='tv/stillunknown/stillunknown-ep5-wow-vertical.mp4',
  caption="A radio telescope heard something for 72 seconds in 1977. Nobody has heard it since. 📡\nThe Wow! signal: what was measured, the comet idea and why it was disputed, and what is still open.\n\nFull episode + sources, free: heartbeatobservatory.com\nMade with AI by Heartbeat Observatory · Still Unknown, Episode 10.5\n#wowsignal #space #mystery #stillunknown #learnontiktok #AI",
  done={}),
]
for n in new:
    if n['id'] in ids: print('exists', n['id']); continue
    d['shows'].append(n)
out = json.dumps(d, indent=2, ensure_ascii=False).replace('\n', '\r\n')
open(P, 'w', encoding='utf-8', newline='').write(out)
print([s['id'] for s in d['shows']][-4:], len(d['shows']))
