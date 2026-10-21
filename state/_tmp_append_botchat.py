import base64
from pathlib import Path
line = (
    "2026-10-10 21:06Z | Satya Twin -> state | Pass: BOUGHT TENN YES #1195 $5.00 @0.92 (ORDER D11RBC6TEZ89); "
    "TENN0-ARK0 early 2Q ESPN TENN WP89.6 vs ask~0.86 (~4c at book; limit 0.92); "
    "HOLD UCLA NO #1192 ORE6-UCLA10 ESPN ORE WP63 vs NO~0.54 (~9c) mark~$1.94 on $3.50; "
    "SC YES settled; exit UCLA refused no-NO-held quirk then WP recovered so hold; "
    "HOU/ILL/VT ~90c skip; tennis off; Open 2\r\n"
)
path = Path(r"C:\Users\lilli\AI-Shared\state\bot-chat.md")
# write via bytes append (same spirit as AppendAllText + base64; avoids PS $ stripping)
with path.open("ab") as f:
    f.write(line.encode("utf-8"))
    f.flush()
print("appended", len(line), "chars; file size", path.stat().st_size)
