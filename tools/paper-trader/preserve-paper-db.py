"""One-time SQLite-consistent copy; refuses to overwrite an existing target."""
import sqlite3
from pathlib import Path

source = Path('C:/Users/lilli/.pm-trader/default/paper.db')
target = Path(__file__).resolve().parent / 'data/default/paper.db'
if target.exists():
    raise SystemExit('Target already exists; preserved without modification.')
if not source.is_file():
    raise SystemExit('Source missing; no account initialized.')
target.parent.mkdir(parents=True, exist_ok=True)
with sqlite3.connect(source.as_uri() + '?mode=ro', uri=True) as src:
    with sqlite3.connect(target) as dst:
        src.backup(dst)
        assert dst.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
print('SQLite backup preserved existing paper database; integrity_check ok. Original retained.')
