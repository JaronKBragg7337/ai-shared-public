import urllib.request, re, json
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
# ESPN tennis scoreboard HTML
for url in ['https://www.espn.com/tennis/scoreboard', 'https://www.espn.com/tennis/scoreboard/_/tour/wta']:
  try:
    req=urllib.request.Request(url, headers=UA)
    html=urllib.request.urlopen(req, timeout=25).read().decode('utf-8','ignore')
    print('URL', url, 'len', len(html))
    for name in ['Bondar','Charaeva','Pankin','Tang','Kalinskaya','Otzturk','Otzt','Beamish','Sasikumar']:
      i=html.lower().find(name.lower())
      print(' ', name, 'idx', i)
      if i>=0:
        print(html[max(0,i-200):i+400].replace('\n',' ')[:500])
  except Exception as e:
    print('ERR', url, e)
# Flashscore live tennis feed? try
try:
  req=urllib.request.Request('https://www.flashscore.com/tennis/', headers={**UA,'Accept-Language':'en-US,en;q=0.9'})
  html=urllib.request.urlopen(req, timeout=25).read().decode('utf-8','ignore')
  print('FS len', len(html))
  for name in ['Bondar','Charaeva','Pankin','Tang']:
    i=html.find(name)
    print(' FS', name, i)
except Exception as e:
  print('FS ERR', e)
