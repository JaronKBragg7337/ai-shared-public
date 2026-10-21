from pathlib import Path
import hashlib,json
root=Path('C:/Users/lilli/AI-Shared'); mirror=Path('G:/My Drive/AI-Shared-mirror')
files=list((root/'state/fly-scene-build/live-systems/flies/brain').rglob('*'))+list((root/'state/fly-scene-evidence').rglob('*'))+[root/'handoffs/2026-09-12-codex-fly-scene-pass2.md']+[root/'state'/n for n in ['test-fly-pass2.cjs','test-fly-pass2-public.cjs','test-fly-press.cjs','test-fly-scene-pass2-responsive.cjs']]
checked=0
for src in files:
 if not src.is_file():continue
 dest=mirror/src.relative_to(root)
 assert dest.exists(),str(dest)
 assert hashlib.sha256(src.read_bytes()).digest()==hashlib.sha256(dest.read_bytes()).digest(),str(dest)
 checked+=1
print(json.dumps({'mirrorFilesHashMatched':checked,'cloudUpload':'not verified'}))
