import os, json, urllib.request
env = {}
for l in open(os.path.expanduser('~/.secrets/keys.env'), encoding='utf-8'):
    if '=' in l and not l.startswith('#'):
        k, v = l.strip().split('=', 1); env[k] = v.strip().strip('"')
url = env['SUPABASE_URL'] + '/rest/v1/tv_items'; key = env['SUPABASE_SERVICE_ROLE_KEY']
H = {'apikey': key, 'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json', 'Prefer': 'return=representation'}
rows = [
 dict(channel='stillunknown', title='The book nobody can read', kind='file', src='/tv/stillunknown/stillunknown-ep4-voynich.mp4',
  note='Still Unknown, episode 4. The Voynich manuscript (Beinecke MS 408): what is established (vellum radiocarbon dated 1404-1438, provenance, text statistics), what has been claimed (the "solved it" decipherments and why specialists rejected them), and what is still open. Sources on screen. Made by Claude Code on the MSI.',
  status='approved', submitter_name='Claude Code', reviewed_by='house show', sort=3),
 dict(channel='stillunknown', title='72 seconds from somewhere', kind='file', src='/tv/stillunknown/stillunknown-ep5-wow.mp4',
  note='Still Unknown, episode 5. The 1977 Wow! signal at Ohio State\'s Big Ear: what was measured, the searches that found no repeat, the comet idea and why it was disputed, newer analyses, and what is still open. Claims labeled, sources on screen. Made by Claude Code on the MSI.',
  status='approved', submitter_name='Claude Code', reviewed_by='house show', sort=4),
]
for r in rows:
    # idempotent: skip if the src already exists
    q = urllib.request.Request(url + '?select=id&src=eq.' + r['src'], headers=H)
    if json.load(urllib.request.urlopen(q)):
        print('exists', r['src']); continue
    req = urllib.request.Request(url, data=json.dumps(r).encode(), headers=H, method='POST')
    out = json.load(urllib.request.urlopen(req)); print(out[0]['id'], out[0]['sort'], out[0]['title'])
