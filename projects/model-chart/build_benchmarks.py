"""Builds benchmarks.html from benchmarks.json (data inlined into benchmarks.tpl.html). Run after updating the JSON."""
import json
from pathlib import Path

here = Path(__file__).parent
data = json.loads((here / "benchmarks.json").read_text(encoding="utf-8"))
tpl = (here / "benchmarks.tpl.html").read_text(encoding="utf-8")
(here / "benchmarks.html").write_text(tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False)), encoding="utf-8")
print("wrote benchmarks.html")
