"""Independent AI review panel for Sapling questions (read-only).

Each AI gets the same BRIEFING.md + one question framing, separately; nobody sees another's answer; every answer is
kept word for word in answers/<model>-<framing>.md. Two framings (Q-A, Q-B) per AI = Jaron's Framing Lens on the reviewers.
Usage: python run_panel.py <panel-folder>      (Claude Code, 10/15/2026, Jaron: "Run the panel boss")
"""
import json
import pathlib
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

SAPLING = r"C:\Users\lilli\Projects\sapling"
HOME = pathlib.Path.home()
# Jaron 10/15 4:42 PM: borrow the Framing Lens answer fields - every reviewer also names its first real step, its blind
# spot, and rewrites the question in its own words (shows whether it understood the question it answered).
FRAMING = ("\n\nEnd your answer with three short lines:\nFirst step: what you would do first, for real.\n"
           "Blind spot: what your answer might miss.\nRewrite: the question in your own words, as you understood it.\n")
RULES = FRAMING + ("\n\nRules: read-only. Do not create, edit or delete any file. Do not run training or start/stop anything. "
                   "Answer in plain text only.\n")


def keys():
    p = HOME / ".secrets" / "keys.env"
    out = {}
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"')
    return out


def run(cmd, prompt=None, cwd=None, timeout=900):
    r = subprocess.run(cmd, input=prompt, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout)
    return (r.stdout or "") + (("\n[stderr]\n" + r.stderr[-1500:]) if r.returncode else "")


def codex(prompt, folder):
    return run(["codex", "exec", "-m", "gpt-6-luna", "-s", "read-only", "--skip-git-repo-check", "-C", SAPLING, "-"],
               prompt=prompt)


def grok(prompt, folder):
    pf = folder / f".grok-prompt-{time.time_ns()}.txt"
    pf.write_text(prompt, encoding="utf-8")
    try:
        return run(["grok", "--prompt-file", str(pf), "--always-approve", "--max-turns", "30", "--no-memory",
                    "--no-subagents", "--no-plan", "--cwd", SAPLING])
    finally:
        pf.unlink(missing_ok=True)


def kimi(prompt, folder):
    return run([str(HOME / ".kimi-code" / "bin" / "kimi.exe"), "-p", prompt], cwd=str(folder))


def deepseek(prompt, folder):
    body = {"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}
    req = urllib.request.Request("https://api.deepseek.com/chat/completions", data=json.dumps(body).encode(),
                                 method="POST", headers={"Content-Type": "application/json",
                                                         "Authorization": "Bearer " + keys()["DEEPSEEK_API_KEY"]})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)["choices"][0]["message"]["content"]


def qwen(prompt, folder):
    return run([sys.executable, r"C:\Users\lilli\AI-Shared\tools\qwen-bridge.py", prompt])


def claude_model(model):
    def fn(prompt, folder):
        # fresh session: no memory of the orchestrator's conversation; read-only tools in the Sapling repo
        return run(["claude", "-p", "--model", model, "--allowedTools", "Read,Glob,Grep", "--max-turns", "20"],
                   prompt=prompt, cwd=SAPLING)
    return fn


CLAUDES = {"claude-fable-5-1": claude_model("claude-fable-5-1"), "claude-sonnet-5-5": claude_model("claude-sonnet-5-5"),
           "claude-haiku-5-5": claude_model("claude-haiku-5-5")}

MODELS = {"codex-gpt6-luna": codex, "grok-build": grok, "kimi": kimi, "deepseek-chat": deepseek}  # qwen dropped 10/15: Jaron, after it answered off-topic


def one(folder, name, fn, q):
    brief = (folder / "BRIEFING.md").read_text(encoding="utf-8")
    question = (folder / f"{q}.txt").read_text(encoding="utf-8").replace("Read BRIEFING.md", "Using the briefing above")
    prompt = brief + "\n\n---\n\n" + question + RULES
    t0 = time.time()
    try:
        text = fn(prompt, folder)
    except Exception as e:  # kept as data
        text = f"[error] {type(e).__name__}: {e}"
    out = folder / "answers" / f"{name}-{q}.md"
    out.write_text(f"# {name} - {q}\nTime: {time.strftime('%Y-%m-%d %H:%M')} | {time.time() - t0:.0f}s\n\n{text.strip()}\n",
                   encoding="utf-8")
    return name, q, len(text)


def main():
    folder = pathlib.Path(sys.argv[1]).resolve()
    (folder / "answers").mkdir(exist_ok=True)
    qs = sorted(p.stem for p in folder.glob("Q-*.txt"))
    pool = {**MODELS, **CLAUDES}
    pick = sys.argv[2].split(",") if len(sys.argv) > 2 else list(MODELS)   # Claude models only when named (shared limit)
    jobs = [(n, pool[n], q) for n in pick for q in qs]
    with ThreadPoolExecutor(max_workers=6) as ex:
        for name, q, n in ex.map(lambda j: one(folder, *j), jobs):
            print(f"{name} {q}: {n} chars", flush=True)


if __name__ == "__main__":
    main()
