import json, os
from datetime import datetime, timezone, timedelta
req_path=r'C:\Users\lilli\AI-Shared\inbox\sentiment-requests.json'
sent_dir=r'C:\Users\lilli\AI-Shared\state\sentiment'
with open(req_path, encoding='utf-8') as f:
    data=json.load(f)
now=datetime.now(timezone.utc)
cutoff=now-timedelta(hours=24)
need=[]
for slug, meta in data.items():
    path=os.path.join(sent_dir, slug+'.json')
    fresh=False
    if os.path.exists(path):
        mtime=datetime.fromtimestamp(os.path.getmtime(path), tz=timezone.utc)
        # also check 'at' field if present
        try:
            with open(path, encoding='utf-8') as sf:
                sj=json.load(sf)
            at=sj.get('at')
            if at:
                # parse ISO
                at_dt=datetime.fromisoformat(at.replace('Z','+00:00'))
                if at_dt >= cutoff:
                    fresh=True
            elif mtime >= cutoff:
                fresh=True
        except Exception:
            if mtime >= cutoff:
                fresh=True
    if not fresh:
        need.append((meta.get('requested_at', 0), slug, meta.get('question',''), meta.get('outcome','')))
need.sort(key=lambda x: x[0])
print('NEED', len(need))
for row in need[:6]:
    print('---')
    print(row[1])
    print(row[2])
    print(row[3])
    print(row[0])
