from pathlib import Path
p=Path('state/verify-fly-glb.py');s=p.read_text(encoding='utf-8');s=s[:s.index("p=Path('state/fly-scene-build/live-systems/flies/brain/README.md')")];s=s.replace('import json,struct,','import sys,json,struct,').replace("Path('state/fly-scene-build/live-systems/flies/brain/fly.glb')","Path(sys.argv[2])").replace("ET.parse('state/flybody-source/flybody/fruitfly/assets/fruitfly.xml')","ET.parse(sys.argv[1])")
Path('state/fly-scene-build/live-systems/flies/brain/tools/verify_fly.py').write_text(s,encoding='utf-8')
