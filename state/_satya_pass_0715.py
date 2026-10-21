import urllib.request, json, sys
sys.path.insert(0, r'C:\Users\lilli\AI-Shared\runtime\polymarket-us-agent-venv\Lib\site-packages')
try:
    from polymarket_us import PolymarketUS
except Exception as e:
    print('import fail', e)
    PolymarketUS = None

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.load(r)

def show(label, url):
    print('===', label, '===')
    try:
        data = get(url)
    except Exception as e:
        print('ERR', e)
        return
    n = 0
    for ev in data.get('events') or []:
        comp = (ev.get('competitions') or [{}])[0]
        st = (comp.get('status') or {}).get('type', {})
        state = st.get('state')
        detail = st.get('detail') or st.get('description') or ''
        if state not in ('in', 'pre'):
            continue
        bits = []
        for c in comp.get('competitors') or []:
            t = c.get('team', {})
            ab = t.get('abbreviation') or t.get('shortDisplayName') or '?'
            bits.append(f"{ab}={c.get('score')}")
        print(state, detail, ' / '.join(bits), '|', ev.get('shortName') or ev.get('name'))
        n += 1
    if not n:
        print('(none in/pre)')

for label, url in [
    ('cfb', 'https://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard'),
    ('nhl', 'https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard'),
    ('nba', 'https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard'),
    ('mlb', 'https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard'),
    ('soccer-friendly', 'https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.friendly/scoreboard'),
    ('cnl', 'https://site.api.espn.com/apis/site/v2/sports/soccer/concacaf.nations.league/scoreboard'),
]:
    show(label, url)

if PolymarketUS:
    c = PolymarketUS(timeout=30.0)
    for slug in [
        'aec-t20iwcr-mal-samoa-2026-10-03',
        'aec-kbl-goy-dae-2026-10-03',
        'aec-itfme-herhoe-cashoo-2026-10-03',
    ]:
        print('=== bbo', slug, '===')
        try:
            bbo = c.markets.bbo(slug)
            bbo = bbo.get('marketData') or bbo
            bid = ((bbo.get('bestBid') or bbo.get('bestBidQuote') or {}) or {}).get('value')
            ask = ((bbo.get('bestAsk') or bbo.get('bestAskQuote') or {}) or {}).get('value')
            print('bid/ask', bid, ask)
        except Exception as e:
            print('ERR', e)
