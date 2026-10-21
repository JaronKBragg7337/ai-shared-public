import subprocess, sys, json
o = sys.argv[1]; ids = sys.argv[2:]
tl = json.load(open('timeline.json')); seg = {s['id']: s for s in tl['segs']}
for sid in ids:
    s = seg[sid]; t = s['start'] + s['dur'] * 0.92
    subprocess.run(['python', 'ep.py', o, '--still', str(t), f'stills/{sid}_{o}.png'], check=True)
