import json,struct
from pathlib import Path
b=Path('state/fly-scene-build/live-systems/flies/brain/fly.glb').read_bytes();j=json.loads(b[20:20+struct.unpack_from('<I',b,12)[0]])
for n in j['nodes']:
 if n.get('name') in ['flybody','wing_left','coxa_T1_left','thorax']:print(n)
