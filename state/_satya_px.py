import json, urllib.request
# Polymarket US gamma/clob style - try events by slug
slug = 'aec-cfb-monst-idaho-2026-10-02'
urls = [
  f'https://gamma-api.polymarket.com/events?slug={slug}',
  f'https://gamma-api.polymarket.com/markets?slug={slug}',
]
for u in urls:
  try:
    r = urllib.request.urlopen(u, timeout=15)
    d = json.loads(r.read().decode())
    print('URL', u)
    print(json.dumps(d, indent=2)[:4000])
  except Exception as e:
    print('ERR', u, e)
