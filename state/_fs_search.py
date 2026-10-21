import re, os, urllib.request
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
queries=['Jaime Faria','Terence Atmane','Dane Sweeny','Taro Daniel','Yeon-Woo Ku','Gabriela Ruse','Elina Svitolina']
for q in queries:
    url='https://www.tennis365.com/?s='+urllib.parse.quote(q) if False else None
import urllib.parse
for q in ['Faria Atmane','Sweeny Daniel','Ku Ruse','Svitolina']:
    u='https://www.google.com/search?q='+urllib.parse.quote(q+' tennis live score flashscore')
    print('skip google')
# flashscore player search API style
for q in ['Faria','Sweeny','Ku','Svitolina','Atmane','Daniel']:
    u='https://s.livesport.services/search/?q='+urllib.parse.quote(q)+'&lang-id=1&type-ids=1,2,3,4&project-id=2&project-type-id=1'
    req=urllib.request.Request(u, headers={**UA,'Referer':'https://www.flashscore.com/'})
    try:
        raw=urllib.request.urlopen(req, timeout=15).read().decode('utf-8','ignore')
        print('===',q,'len',len(raw))
        print(raw[:500])
    except Exception as e:
        print('===',q,'ERR',e)
