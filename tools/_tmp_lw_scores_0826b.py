import urllib.request, re, json
ua={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def fetch(url):
  req=urllib.request.Request(url, headers=ua)
  with urllib.request.urlopen(req, timeout=25) as r:
    return r.read().decode('utf-8','replace')

# Sportytrader search-ish pages
urls=[
 'https://www.sportytrader.com/en/scores/tennis/',
 'https://www.sportytrader.de/ergebnisse-live/tennis/',
 'https://www.flashscore.com/tennis/',
 'https://www.tennisexplorer.com/matches/?type=all&year=2026&month=09&day=27',
]
for u in urls:
  try:
    html=fetch(u)
    print('OK', u, 'len', len(html))
    for name in ['Gaston','Rublev','Digvijay','Nordquist','Singh','Solary','Wang']:
      if name.lower() in html.lower():
        # grab nearby snippet
        i=html.lower().find(name.lower())
        snip=re.sub(r'\s+',' ', html[max(0,i-80):i+120])
        print(' ', name, ':', snip[:180])
  except Exception as e:
    print('ERR', u, e)
