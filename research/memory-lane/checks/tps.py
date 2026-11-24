"""Measure how fast the local models talk on the MSI's RTX 4060 (tokens per second), then unload them."""
import json, sys, urllib.request

PROMPT = "Explain in plain words how a sailboat can sail against the wind. Write about 200 words."


def run(model):
    body = json.dumps({"model": model, "prompt": PROMPT, "stream": False, "keep_alive": 0,
                       "options": {"num_predict": 220, "seed": 7, "temperature": 0}}).encode()
    req = urllib.request.Request("http://127.0.0.1:11434/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        d = json.loads(r.read())
    n, ns = d.get("eval_count", 0), d.get("eval_duration", 1)
    pn, pns = d.get("prompt_eval_count", 0), d.get("prompt_eval_duration", 1)
    print(f"{model}: wrote {n} tokens at {n / (ns / 1e9):.1f} tokens/second "
          f"(read the prompt at {pn / (pns / 1e9):.0f}/s; load {d.get('load_duration', 0) / 1e9:.1f} s)")


for m in sys.argv[1:]:
    try:
        run(m)
    except Exception as e:
        print(f"{m}: FAILED {e!r}")
