import json, re
raw=open(r'C:\Users\lilli\AI-Shared\tools\_tmp_espn.json',encoding='utf-8').read()
# find Rapolu event in JSON
i=raw.find('Rapolu')
print('idx', i)
print(raw[i-500:i+1500])
