"""publish_tests.py - backs up Jaron's AI tests to their own public repo JaronKBragg7337/AI-Tests (CC0) and its GitHub Page.

Jaron 11/18: "I think it's something I want backed up somewhere. Even its own repo with a GitHub page for it?"
(First put in the old AI-Framing-Study repo by mistake; that one is from an earlier time and was restored exactly as it was.)
This repo holds the whole test notebook:
  index.html                     the full tests page (built by tools/tests-page.py), same page as the claude.ai artifact
  data/framing-lens/...          every prompt, result table and raw answer the page is built from
  data/picture-test/...          the picture (stego) test: the image, the table, the answers
Before copying, a privacy scan stops the push if the page or data contain family names, key-like strings or contact
details (public repo). Run after any new test run:
  python tools/tests-page.py && python tools/publish_tests.py
"""
import re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LENS = ROOT / "projects" / "framing-lens-2026-09"
STEGO = ROOT / "research" / "stego-test"
REPO = Path.home() / "Projects" / "AI-Tests"

# words that must never reach a public page (family, private places, secrets); case-insensitive
BLOCK = [r"his partner", r"his ex-wife", r"the baby", r"one of his kids", r"child support", r"keys\.env", r"sk-ant-[a-z0-9]", r"sb_secret_",
         r"acsassociation", r"kylerbragg", r"@icloud\.com", r"social security"]


def scan(text, where):
    hits = [w for w in BLOCK if re.search(w, text, re.I)]
    if hits:
        sys.exit(f"STOPPED: {where} contains {hits} - not publishing (public repo)")


def scrub(text):
    # the MSI's Windows user folder name stays off the public repo
    return re.sub(r"(?i)\blilli\b", "<user>", text)


def copy_tree(src, dst):
    dst.mkdir(parents=True, exist_ok=True)
    for f in src.rglob("*"):
        if f.is_file() and not f.name.startswith("err-") and f.suffix in (".md", ".txt", ".png", ".json", ".log"):
            if f.suffix != ".png":
                scan(f.read_text(encoding="utf-8", errors="replace"), str(f))
            rel = f.relative_to(src)
            (dst / rel).parent.mkdir(parents=True, exist_ok=True)
            if f.suffix == ".png":
                shutil.copy2(f, dst / rel)
            else:
                (dst / rel).write_text(scrub(f.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")


def main():
    html = (LENS / "tests-page.html").read_text(encoding="utf-8")
    scan(re.sub(r"data:image/[a-z]+;base64,[A-Za-z0-9+/=]+", "", html), "tests-page.html")
    note = ("<p style='margin-top:10px'>Backed up on GitHub (CC0): every prompt and raw answer is in "
            "<a href='https://github.com/JaronKBragg7337/AI-Tests/tree/main/data'>data/</a>.</p>")
    body = html.replace("</footer>", note + "</footer>", 1)
    full = ("<!doctype html><html lang=en><head><meta charset=utf-8>"
            "<meta name=viewport content='width=device-width,initial-scale=1'>" + body + "</html>")
    REPO.mkdir(parents=True, exist_ok=True)
    (REPO / "index.html").write_text(scrub(full), encoding="utf-8")
    copy_tree(LENS, REPO / "data" / "framing-lens")
    copy_tree(STEGO, REPO / "data" / "picture-test")
    museum = ROOT / "projects" / "model-museum"
    for fo in ("round-1-2026-11-09", "new-models"):
        src = museum / fo
        if not src.exists():
            continue
        dst = REPO / "museum" / fo
        (dst / "thumbs").mkdir(parents=True, exist_ok=True)
        for f in src.glob("*.html"):
            if f.name != "index.html":
                scan(f.read_text(encoding="utf-8", errors="replace"), str(f))
                shutil.copy2(f, dst / f.name)
        for f in (src / "thumbs").glob("*.jpg"):
            shutil.copy2(f, dst / "thumbs" / f.name)
    g = lambda *a: subprocess.run(["git", *a], cwd=REPO, capture_output=True, text=True)
    g("add", "-A")
    if g("diff", "--cached", "--quiet").returncode == 0:
        print("nothing new"); return
    g("commit", "-m", "Tests notebook update (auto-published)", "-m", "Co-Authored-By: Claude Opus 5.5 <<email>>")
    r = g("push", "origin", "HEAD:main")
    print("pushed" if r.returncode == 0 else "push failed: " + r.stderr[-300:])


if __name__ == "__main__":
    main()
