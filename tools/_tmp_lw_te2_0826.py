import urllib.request, re
ua={'User-Agent':'Mozilla/5.0'}

def get(url):
  req=urllib.request.Request(url, headers=ua)
  with urllib.request.urlopen(req, timeout=30) as r:
    return r.read().decode('utf-8','replace')

html=get('https://www.tennisexplorer.com/matches/?type=all&year=2026&month=09&day=27')
# pull table rows containing Nordquist or Singh D
for m in re.finditer(r'<tr[^>]*>.*?(?:Nordquist|Singh D\.|Digvijay|Gaston H\.|Rublev).*?</tr>', html, re.I|re.S):
  row=re.sub(r'\s+',' ', re.sub(r'<[^>]+>',' | ', m.group(0)))
  if 'Nordquist' in row or 'Singh D' in row or 'Gaston' in row or 'Rublev' in row:
    print(row[:500])
    print('====')

# try match detail ids from earlier
for mid in ['3332972','3332720']:
  try:
    h=get(f'https://www.tennisexplorer.com/match-detail/?id={mid}')
    title=re.search(r'<title>([^<]+)', h)
    print('DETAIL', mid, title.group(1) if title else '?')
    # score-ish
    for pat in [r'class="result"[^>]*>([^<]+)', r'class="score"[^>]*>([^<]+)', r'Set \d[^<]{0,40}', r'\b\d:\d\b']:
      ms=re.findall(pat, h)[:8]
      if ms: print(' ', pat, ms)
    # snippet around live
    for key in ['live','retired','finished','1st','2nd']:
      i=h.lower().find(key)
      if i>0:
        print(' snip', key, re.sub(r'\s+',' ', re.sub(r'<[^>]+>',' ', h[i-40:i+80]))[:160])
  except Exception as e:
    print('ERR detail', mid, e)
