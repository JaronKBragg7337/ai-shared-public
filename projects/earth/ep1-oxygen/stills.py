import json,subprocess,sys
tl=json.load(open('timeline.json'))
o=sys.argv[1]
for s in tl['segs']:
    t=s['start']+s['dur']*float(sys.argv[2] if len(sys.argv)>2 else 0.85)
    subprocess.run(['python','ep.py',o,'--still',str(t),f"stills/{o}_{s['id']}.png"],check=True)
