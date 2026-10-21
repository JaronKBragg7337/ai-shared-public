import urllib.parse
import json,urllib.request,re
def get(url):
    req=urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode('utf-8','replace')
# sofascore search
for q in ['Aryan Shah','Charlie Robertson','Theo Papamalamis','Hoyoung Roh','Evan Bynoe']:
    try:
        raw=get(f'https://www.sofascore.com/api/v1/search/all?q={urllib.parse.quote(q)}&page=0')
        print('SEARCH', q, raw[:400])
    except Exception as e:
        print('SEARCH fail', q, e)
