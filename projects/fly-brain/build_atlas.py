#!/usr/bin/env python3
"""
build_atlas.py - one-time: every neuron's MEASURED soma position + which circuit it belongs to,
as a compact binary the 3D scene loads once. Anatomy, not a shape (the runtime author's phrase).

Output: state/fly-brain/atlas.json  (index, x, y, z in 0..1, region code) + atlas.bin (float16 xyz)
Regions the scene can colour: ORN (nose), PN, KC (mushroom body), MBON, PAM (reward dopamine),
PPL1 (punishment dopamine), DN (descending / motor), other.
"""
import json, sys, numpy as np, pandas as pd
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "runtime"))
from flysim import FlyBrain
STATE = HERE.parent.parent / "state" / "fly-brain"

fb = FlyBrain(graph_path=HERE / "runtime" / "build" / "graph.npz")
ann = pd.read_feather(HERE / "runtime" / "data" / "body-annotations.feather").drop_duplicates("bodyId").set_index("bodyId")
loc = ann["somaLocation"].reindex(fb.bodies)
xyz = np.full((fb.n, 3), np.nan, dtype=np.float32)
for i, v in enumerate(loc.to_numpy()):
    if isinstance(v, (list, tuple, np.ndarray)) and len(v) >= 3:
        xyz[i] = (float(v[0]), float(v[1]), float(v[2]))
ok = ~np.isnan(xyz[:, 0])
lo, hi = np.nanmin(xyz[ok], 0), np.nanmax(xyz[ok], 0)
xyz = (xyz - lo) / np.maximum(hi - lo, 1e-6)
REG = [("ORN", r"^ORN_"), ("PN", r"^(?:[lvm]?PN|VP\d)"), ("KC", r"^KC"), ("MBON", r"^MBON"), ("PAM", r"^PAM"), ("PPL1", r"^PPL1"), ("DN", r"^(?:DNa|DNp|DNb|DNg|MDN)")]
import re
region = np.full(fb.n, 7, dtype=np.uint8)
for code, (name, rx) in enumerate(REG):
    m = np.array([bool(re.match(rx, t)) for t in fb.types])
    region[m & (region == 7)] = code
keep = np.flatnonzero(ok)
STATE.mkdir(parents=True, exist_ok=True)
xyz[keep].astype(np.float16).tofile(STATE / "atlas.bin")
json.dump({"n": int(len(keep)), "index": keep.tolist(), "region": region[keep].tolist(),
           "regions": [n for n, _ in REG] + ["other"], "note": "xyz normalised 0..1 from measured soma positions (MaleCNS v1.0); atlas.bin = float16 xyz triples in this order"},
          open(STATE / "atlas.json", "w"), separators=(",", ":"))
counts = {n: int((region == i).sum()) for i, (n, _) in enumerate(REG)}
print(f"atlas: {len(keep)} of {fb.n} neurons have a soma position | regions {counts}")
