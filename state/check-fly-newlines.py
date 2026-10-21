from pathlib import Path
p=Path('state/check-fly-public.py');s=p.read_text(encoding='utf-8').replace("hashlib.sha256(data).digest()==hashlib.sha256(local).digest()","hashlib.sha256(data.replace(b'\\r\\n',b'\\n') if name.endswith(('.html','.js')) else data).digest()==hashlib.sha256(local.replace(b'\\r\\n',b'\\n') if name.endswith(('.html','.js')) else local).digest()")
p.write_text(s,encoding='utf-8')
