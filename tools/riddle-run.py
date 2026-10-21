"""riddle-run.py - the 'instrumental version' riddle (Jaron 10/12): each model, each version, 2 fresh runs (new chat each).
Reuses the model callers in lens-repeat.py, plus Kimi. Answers -> projects/framing-lens-2026-09/instrumental/<model>/<ver>-<n>.md"""
import importlib.util, os, subprocess, pathlib, sys
T = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("lr", T / "lens-repeat.py"); lr = importlib.util.module_from_spec(spec); spec.loader.exec_module(lr)
OUT = T.parent / "projects" / "framing-lens-2026-09" / "instrumental"
Q = {"open": "Two coworkers sit in the same truck, listening to the same song on the same radio at the same volume. One hears the full song with lyrics. The other hears only the instrumental. How is that possible?",
     "closed": "Two coworkers sit in the same truck, listening to the same song on the same radio at the same volume. Nobody in the truck is singing, the radio works fine, and neither wears headphones. One hears the full song with lyrics. The other hears only the instrumental. How is that possible?"}
def kimi(p):
    r = subprocess.run([os.path.expanduser(r"~\.kimi-code\bin\kimi.exe"), "-p", p], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
    return r.stdout + r.stderr
M = {"deepseek": lr.MODELS["deepseek"], "luna": lr.MODELS["luna"], "sol": lr.MODELS["sol"], "grok": lr.MODELS["grok"],
     "qwen": lr.MODELS["qwen"], "kimi": kimi}
for k in ("sonnet", "haiku"):
    if k in lr.MODELS: M[k] = lr.MODELS[k]
for m, fn in M.items():
    for v, q in Q.items():
        for n in (1, 2):
            f = OUT / m / f"{v}-{n}.md"; f.parent.mkdir(parents=True, exist_ok=True)
            if f.exists(): continue
            try: a = fn(q)
            except Exception as e: a = f"ERROR {e}"
            f.write_text(a, encoding="utf-8"); print(m, v, n, a.strip().replace("\n", " ")[:160], flush=True)
