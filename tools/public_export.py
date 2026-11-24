"""Public copy of AI-Shared (Jaron 10/21: "anything being private will always kill it" - any AI chat must be able to read it).
Builds C:\\Users\\lilli\\Projects\\ai-shared-public from the private repo's tracked files, cleaned every run:
  - whole folders/files left out: other people's lives (court/support/family files, day log, partner guide), raw bot transcripts
  - names of other people -> neutral words (his own story stays: his choice)
  - secrets in disguise -> placeholders (phone-alert topic, emails, phone numbers, street addresses, court case numbers)
Then scans the result and prints anything suspicious. Jaron's own name and story are kept on purpose.
   python tools/public_export.py          -> build + report (no push)
   python tools/public_export.py --push   -> build + commit + push (after the report is clean)"""
import functools, os, re, shutil, subprocess, sys

SRC = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DST = r"C:\Users\lilli\Projects\ai-shared-public"

LEAVE_OUT = (
    "projects/life/", "projects/reality-agent/day-log/",   # transcripts IN (Jaron 10/21); name-bearing paths: leave: lines in the hide list
    "state/twin-log.md", "agents/claude-code/FROM-ME.md", "projects/reality-agent/",
    "From Jaron- What I had AIs doing and where at/",
    # the creature stays private (Jaron 10/28 4:13 PM: "protect it")
    "projects/strategy/CREATURE-BRIEF.md", "projects/strategy/CREATURE-NEEDS.md", "projects/strategy/THE-FLASH-2026-10-26.md",
    "projects/strategy/THE-FLASH-2026-10-27-creature.md",
)
# Names of other people live in a PRIVATE file (projects/life/ never goes public), so this script carries none of them.
# Missing or empty file = no push (fails closed). Format: see the file's header.
HIDE_FILE = os.path.join(SRC, "projects", "life", "public-export-hide.txt")
WB_L = r"(?:(?<![A-Za-z0-9])|(?<=\\[bB]))"   # start of a word, also right after a literal backslash-b in code text (the 10/21-11/22 bug)
WB_R = r"(?![A-Za-z0-9])"


def load_hide():
    """-> (rules [(compiled, replacement, plain_name_or_None)], extra leave-out prefixes). Raises if the list is missing."""
    if not os.path.isfile(HIDE_FILE): raise SystemExit(f"STOP: hide list missing ({HIDE_FILE}) - nothing built, nothing pushed")
    plain, raw, leave = [], [], []
    for line in open(HIDE_FILE, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"): continue
        if line.startswith("leave:"): leave.append(line[6:].strip()); continue
        if "=>" not in line: raise SystemExit(f"STOP: bad hide-list line: {line[:20]}...")
        pat, rep = (x.strip() for x in line.rsplit("=>", 1))
        case = rep.endswith("[case]")
        if case: rep = rep[:-6].strip()
        if pat.startswith("regex:"): raw.append((re.compile(pat[6:].strip()), rep, None))
        else: plain.append((pat, rep, case))
    plain.sort(key=lambda x: -len(x[0]))   # full names before first names
    def rx(n, case):   # [case] names match as written or ALL CAPS ("Name", "NAME"), never the lowercase common word
        body = "|".join(r"\s+".join(re.escape(w) for w in v.split()) for v in ({n, n.upper()} if case else {n}))
        return re.compile(WB_L + "(?:" + body + ")" + WB_R, 0 if case else re.I)
    rules = [(rx(n, c), r, n) for n, r, c in plain] + raw
    if len([r for r in rules if r[2]]) < 5: raise SystemExit("STOP: hide list looks empty - nothing built, nothing pushed")
    return rules, tuple(leave)


TEXT = (".md", ".txt", ".py", ".ps1", ".mjs", ".js", ".json", ".html", ".css", ".yml", ".yaml", ".toml", ".sh", ".csv", ".wgsl")


@functools.lru_cache(maxsize=None)   # read once per run, not once per file
def env_value(name):
    for p in (os.path.expanduser("~/.secrets/keys.env"),):
        for l in open(p, encoding="utf-8"):
            if l.startswith(name + "="): return l.split("=", 1)[1].strip()
    return ""


def scrub(text, rules):
    topic = env_value("NTFY_TOPIC")
    if topic: text = text.replace(topic, "<ntfy-topic>")
    for rx, rep, _ in rules: text = rx.sub(rep, text)
    text = re.sub(r"[A-Za-z0-9._%+-]+@(?!heartbeatobservatory\.com)[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "<email>", text)
    text = re.sub(r"(?<![\d.])\(?\d{3}\)?[-. ]\d{3}[-. ]\d{4}(?!\d|\.\d)", "<phone>", text)
    text = re.sub(r"\b\d{1,5}\s+(?:[NSEW]\.?\s+)?[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\s+(?:St|Street|Ave|Avenue|Rd|Road|Dr|Drive|Ln|Lane|Blvd|Ct|Court|Way|Pl)\b\.?", "<address>", text)
    text = re.sub(r"\b\d{2}[A-Z]\d{2}-\d{4}-[A-Z0-9]{2,3}-\d{3,6}\b", "<case-number>", text)
    text = re.sub(r"\b(sk-ant-|sk-proj-|ghp_|github_pat_|sb_secret_|xai-|rpa_)[A-Za-z0-9_-]{16,}", r"\1<redacted>", text)
    return text


def main():
    rules, extra_leave = load_hide()
    leave_out = LEAVE_OUT + extra_leave
    files = subprocess.run(["git", "-C", SRC, "ls-files"], capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
    keep_git = os.path.join(DST, ".git")
    if os.path.isdir(DST):
        for n in os.listdir(DST):
            if n != ".git": p = os.path.join(DST, n); shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    os.makedirs(DST, exist_ok=True)
    n_in = n_out = 0
    for f in files:
        if f.startswith(leave_out) or not f.lower().endswith(TEXT): n_out += 1; continue
        src = os.path.join(SRC, f); dst = os.path.join(DST, f)
        if not os.path.isfile(src): continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try: t = open(src, encoding="utf-8").read()
        except UnicodeDecodeError: n_out += 1; continue
        open(dst, "w", encoding="utf-8", newline="").write(scrub(t, rules)); n_in += 1
    open(os.path.join(DST, "README.md"), "w", encoding="utf-8").write(README)
    # scan what came out: every hidden name (same list, so nothing can slip past a list the scan doesn't know), key shapes, paths
    names = [rx for rx, _, _ in rules]   # every hide rule, plain names and regex (EIN, dates) alike
    other = [re.compile(p) for p in (r"sk-ant-[A-Za-z0-9_-]{16,}", r"sb_secret_[A-Za-z0-9_-]{16,}", r"<ntfy-topic>(?:NEVER)")]
    flags = []
    for root, _, fs in os.walk(DST):
        if ".git" in root: continue
        for fn in fs:
            rel = os.path.relpath(os.path.join(root, fn), DST)
            t = rel + "\n" + open(os.path.join(root, fn), encoding="utf-8", errors="ignore").read()
            if any(rx.search(t) for rx in names + other): flags.append(rel)
    print(f"public copy: {n_in} files in, {n_out} left out -> {DST}")
    print("FLAGS:", sorted(set(flags)) or "none")
    if "--push" in sys.argv and not flags:
        subprocess.run(["git", "-C", DST, "add", "-A"]); subprocess.run(["git", "-C", DST, "commit", "-q", "-m", "public export (cleaned)", "-m", "Co-Authored-By: Claude Opus 5.5 <<email>>"])
        subprocess.run(["git", "-C", DST, "push", "-q"])


README = """# AI-Shared (public copy)

The working brain of **Heartbeat Observatory** (heartbeatobservatory.com): how one builder in Fort Wayne, Indiana runs an
AI-built company with a crew of AIs (Claude, Grok, Codex, Kimi, DeepSeek, Qwen and his own, Sapling), mostly from one long
conversation and a laptop at home called the MSI.

Start with **AGENTS.md**: the one page every AI reads first. Then:
- `state/timeline.md` - everything decided and built, by date
- `state/build-ledger/` - what each AI built, week by week
- `projects/` - every project: TV channels, the news show, the render engine, trading, the runbook
- `tools/` - the scripts that run it all
- `handoffs/` - notes one AI leaves for the next

Any AI (ChatGPT, Claude, Grok, anyone) can read this repo and pick up where things stand.

**What's not here, on purpose:** keys and passwords (never stored here), videos and images, and other people's lives -
family, partner and kids' names are replaced with neutral words, and private files (court, family, personal day log) are left
out. The owner's own story is public by his choice.

Updated automatically from the private workspace. Public domain (CC0) unless a file says otherwise.
"""

if __name__ == "__main__":
    main()
