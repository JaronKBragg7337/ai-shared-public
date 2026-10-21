from pathlib import Path
p=Path('state/fly-scene-build/live-systems/flies/brain/tools/build_fly.py')
s=p.read_text().replace('import bpy, sys, json,','import bpy, bmesh, sys, json,').replace("mesh.update()","mesh.update()\n        bm=bmesh.new(); bm.from_mesh(mesh); bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7); bm.to_mesh(mesh); bm.free()")
p.write_text(s)
