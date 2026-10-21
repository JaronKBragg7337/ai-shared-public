"""lens-repeat.py - run Jaron's AI tests several times per model, fresh each time, and count the answers (2026-10-08, Claude Code).

Jaron: one answer is one sample (DeepSeek rarity went water -> granite -> water). So: N fresh runs per model, every output kept,
then a count of how often each pick comes up. Data, not debate.

Tests: framing lens (prompt.txt, all six), rarity raw prompt, rarity process-chain prompt (prompt 3).
Models: DeepSeek (API), Codex Luna + Sol, Grok Build, local Qwen, Claude Sonnet 5.5 + Haiku 5.5 (Anthropic API, ~$1 total).
Every call runs from an empty temp folder so no project files or memory leak in.

  python tools/lens-repeat.py            # 7 runs each, everything
  python tools/lens-repeat.py --n 2 --models deepseek --tests lens
Output: projects/framing-lens-2026-09/repeats/<model>/<test>-<run>.md and repeats/SUMMARY.md
"""
import argparse, json, os, re, subprocess, sys, tempfile, time, urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LENS = ROOT / "projects" / "framing-lens-2026-09"
OUT = LENS / "repeats"
HOME = Path.home()

RARITY_RAW = "What's the rarest material in the cosmos?"
RARITY_CHAIN = ("What familiar, naturally occurring material on Earth could be argued to be among the rarest materials in the known "
                "universe, not because its ingredients are rare or because it requires a narrow temperature or pressure range, but "
                "because of the full chain of conditions and processes required for nature to produce the material itself?")
NO_WEB = "Answer from your own reasoning only. Do not search the web or use any tools.\n\n"


def keys():
    env = {}
    for line in (HOME / ".secrets" / "keys.env").read_text(encoding="utf-8").splitlines():
        if "=" in line and not line.lstrip().startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"')
    return env


def run(cmd, prompt=None, timeout=900):
    with tempfile.TemporaryDirectory(prefix="lens-") as d:
        p = subprocess.run(cmd(d) if callable(cmd) else cmd, input=prompt, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", cwd=d, timeout=timeout)
        return p.stdout.strip() or p.stderr.strip()


def deepseek(prompt):
    k = keys()["DEEPSEEK_API_KEY"]
    req = urllib.request.Request("https://api.deepseek.com/chat/completions", method="POST",
                                 headers={"Authorization": f"Bearer {k}", "Content-Type": "application/json"},
                                 data=json.dumps({"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}).encode())
    return json.load(urllib.request.urlopen(req, timeout=300))["choices"][0]["message"]["content"]


def codex(slug):
    def ask(prompt):
        with tempfile.TemporaryDirectory(prefix="lens-") as d:
            out = Path(d) / "last.txt"
            subprocess.run(["codex", "exec", "-s", "read-only", "--skip-git-repo-check", "-m", slug, "-C", d, "-o", str(out), "-"],
                           input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=d, timeout=900)
            return out.read_text(encoding="utf-8") if out.exists() else "(no output)"
    return ask


def grok(prompt):
    return run([str(HOME / ".grok" / "bin" / "grok"), "-p", prompt])


def claude(model):
    # API key, not the claude CLI (its login expires; see `claude setup-token`). New sk-ant-usr keys need the workspace header.
    def ask(prompt):
        k = keys()
        h = {"x-api-key": k["ANTHROPIC_API_KEY"], "anthropic-version": "2023-06-01", "content-type": "application/json"}
        if k.get("ANTHROPIC_WORKSPACE_ID"):
            h["anthropic-workspace-id"] = k["ANTHROPIC_WORKSPACE_ID"]
        body = json.dumps({"model": model, "max_tokens": 4000, "messages": [{"role": "user", "content": prompt}]}).encode()
        r = json.load(urllib.request.urlopen(urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, headers=h), timeout=600))
        return "".join(b.get("text", "") for b in r["content"])
    return ask


def qwen(prompt):
    # The 4b model answers only the first of several prompts, so the lens is sent one prompt at a time (same as September).
    parts = re.split(r"(?=### Prompt \d)", prompt)
    head, blocks = parts[0], parts[1:] or [""]
    answers = []
    for b in blocks:
        body = json.dumps({"model": "qwen3.5:4b", "prompt": head + b, "stream": False, "think": False}).encode()
        r = urllib.request.Request("http://localhost:11434/api/generate", data=body, headers={"Content-Type": "application/json"})
        answers.append(json.load(urllib.request.urlopen(r, timeout=600)).get("response", ""))
    return "\n\n".join(answers)


MODELS = {"deepseek": deepseek, "luna": codex("gpt-6-luna"), "sol": codex("gpt-6.1-sol"), "grok": grok, "qwen": qwen,
          "sonnet": claude("claude-sonnet-5-5"), "haiku": claude("claude-haiku-5-5")}


def tests():
    return {"lens": (LENS / "prompt.txt").read_text(encoding="utf-8"),
            "rarity-raw": NO_WEB + RARITY_RAW, "rarity-chain": NO_WEB + RARITY_CHAIN}


def picks(text):
    found = re.findall(r"Choice:?\**:?\s*\**\s*([A-F])\b", text)
    return "".join(found[:6]) if found else "?"


def material(text):
    # the material named EARLIEST in the opening wins (whole words, so "soil" is not "oil")
    t = text.lower()[:600]
    hits = []
    for word in ["wood", "bone", "shell", "silk", "coal", "amber", "pearl", "limestone", "chalk", "soil", "oil", "petroleum",
                 "life", "dna", "granite", "liquid water", "water", "diamond", "gold", "tantalum", "antimatter", "astatine", "francium"]:
        m = re.search(r"\b" + re.escape(word) + r"\b", t)
        if m:
            hits.append((m.start(), word))
    return min(hits)[1] if hits else "?"


def summarize():
    lines = ["# Repeat runs - counts (lens-repeat.py)", "", "One row per model. Lens = picks for prompts 1-6 each run; "
             "rarity = the material named first (keyword match on the opening, check the raw file when it says ?).", ""]
    for m in sorted(p.name for p in OUT.iterdir() if p.is_dir()):
        d = OUT / m
        lens = [picks(f.read_text(encoding="utf-8")) for f in sorted(d.glob("lens-*.md"))]
        raw = [material(f.read_text(encoding="utf-8")) for f in sorted(d.glob("rarity-raw-*.md"))]
        chain = [material(f.read_text(encoding="utf-8")) for f in sorted(d.glob("rarity-chain-*.md"))]
        lines.append(f"## {m}")
        if lens:
            lines.append(f"- Lens runs: {' '.join(lens)}")
            for i in range(6):
                c = Counter(p[i] for p in lens if len(p) > i)
                lines.append(f"  - Prompt {i+1}: " + ", ".join(f"{k} x{v}" for k, v in c.most_common()))
        if raw:
            lines.append(f"- Rarity raw: " + ", ".join(f"{k} x{v}" for k, v in Counter(raw).most_common()))
        if chain:
            lines.append(f"- Rarity chain: " + ", ".join(f"{k} x{v}" for k, v in Counter(chain).most_common()))
        lines.append("")
    (OUT / "SUMMARY.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=7)
    ap.add_argument("--models", default=",".join(MODELS))
    ap.add_argument("--tests", default="lens,rarity-raw,rarity-chain")
    a = ap.parse_args()
    T = tests()
    for i in range(1, a.n + 1):            # round-robin so a model that hits a limit still gets early runs everywhere
        for m in a.models.split(","):
            for t in a.tests.split(","):
                f = OUT / m / f"{t}-{i}.md"
                if f.exists():
                    continue
                f.parent.mkdir(parents=True, exist_ok=True)
                t0 = time.time()
                try:
                    text = MODELS[m](T[t])
                except Exception as e:
                    text = f"(error: {e})"
                if text.startswith("(error") or text == "(no output)" or len(text) < 40:   # don't save a failure as a run;
                    with open(OUT / "errors.log", "a", encoding="utf-8") as log:           # it gets retried next time
                        log.write(f"{time.strftime('%Y-%m-%d %H:%M')} {m} {t} {i}: {text[:300]}\n")
                    print(m, t, i, "FAILED", flush=True)
                    continue
                f.write_text(f"<!-- {m} {t} run {i} {time.strftime('%Y-%m-%d %H:%M')} {time.time()-t0:.0f}s -->\n{text}\n",
                             encoding="utf-8")
                print(m, t, i, picks(text) if t == "lens" else material(text), flush=True)
                summarize()
    summarize()


if __name__ == "__main__":
    main()
