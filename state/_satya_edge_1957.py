import json, urllib.request

# Refresh live board snippet + try desk book via live-board.json
path = r'C:\Users\lilli\AI-Shared\state\live-board.json'
with open(path, encoding='utf-8') as f:
    d = json.load(f)
print('type', type(d).__name__)
if isinstance(d, dict):
    print('keys', list(d.keys())[:40])
    games = d.get('games') or d.get('markets') or d.get('items') or d.get('board') or []
    if not games and 'slugs' in d:
        games = d['slugs']
    print('games_len', len(games) if hasattr(games, '__len__') else games)
    if isinstance(games, list):
        for g in games:
            if isinstance(g, dict):
                slug = g.get('slug') or g.get('marketSlug') or g.get('id') or ''
                print(json.dumps({k: g.get(k) for k in list(g.keys())[:20]}, ensure_ascii=False)[:400])
            else:
                print(g)
    else:
        print(str(d)[:1500])
elif isinstance(d, list):
    print('len', len(d))
    for g in d:
        print(json.dumps(g, ensure_ascii=False)[:400] if isinstance(g, dict) else g)
