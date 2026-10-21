"""tests-page.py - builds one phone-friendly page of all Jaron's AI tests + every AI answer (Claude Code, 2026-10-12).
Reads projects/framing-lens-2026-09 (RESULTS.md, prompts, raw-*.md, repeats/, instrumental/) and writes
projects/framing-lens-2026-09/tests-page.html, which is published as a claude.ai Artifact (same path = same link).
  python tools/tests-page.py
"""
import html, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = ROOT / "projects" / "framing-lens-2026-09"
OUT = D / "tests-page.html"


def read(p):
    try:
        return pathlib.Path(p).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return s


def md(text):
    """Small markdown: headings, tables, bullets, paragraphs."""
    out, lines, i = [], text.splitlines(), 0
    while i < len(lines):
        l = lines[i]
        if l.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-{2,}:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            head, body = rows[0], rows[1:]
            t = "<div class=tw><table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body) + "</tbody></table></div>"
            out.append(t)
            continue
        m = re.match(r"(#{1,4})\s+(.*)", l)
        if m:
            n = min(len(m.group(1)) + 2, 5)
            out.append(f"<h{n}>{inline(m.group(2))}</h{n}>")
        elif re.match(r"\s*[-*]\s+", l):
            items = []
            while i < len(lines) and re.match(r"\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
                while i < len(lines) and lines[i].startswith("  ") and not re.match(r"\s*[-*]\s+", lines[i]):
                    items[-1] += " " + lines[i].strip()
                    i += 1
            out.append("<ul>" + "".join(f"<li>{inline(x)}</li>" for x in items) + "</ul>")
            continue
        elif l.strip():
            para = [l]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"(#|\||\s*[-*]\s)", lines[i + 1]):
                i += 1
                para.append(lines[i])
            out.append(f"<p>{inline(' '.join(para))}</p>")
        i += 1
    return "\n".join(out)


def raw_block(title, text, sub=""):
    text = text.strip() or "(no answer saved)"
    return (f"<details class=ans><summary><span class=who>{html.escape(title)}</span>"
            f"<span class=sub>{html.escape(sub)}</span></summary><pre>{html.escape(text)}</pre></details>")


def section(id_, num, title, intro, body):
    return f"<section id={id_}><div class=sec-h><span class=tag>{num}</span><h2>{title}</h2></div>{intro}{body}</section>"


# ---- 1. framing lens
results = read(D / "RESULTS.md")
parts = re.split(r"\n(?=## \d\.)", results)
by = {re.match(r"## (\d)", p).group(1): p for p in parts if re.match(r"## \d", p)}
head_note = parts[0].split("\n", 1)[1] if parts else ""

raw_files = sorted(D.glob("raw-*.md"))
names = {"raw-claude-fable-5.1": "Claude Fable 5.1", "raw-claude-haiku-4.5": "Claude Haiku 4.5", "raw-claude-opus-5.5": "Claude Opus 5.5",
         "raw-claude-sonnet-5.5": "Claude Sonnet 5.5", "raw-codex-gpt6-luna": "Codex Luna (GPT-6)", "raw-codex-gpt6.1-sol": "Codex Sol 6.1",
         "raw-deepseek": "DeepSeek", "raw-grok-build": "Grok Build", "raw-qwen-local": "Qwen (local)", "raw-gpt-6": "GPT-6 ChatGPT (no memory)",
         "raw-gpt-6-memory-on": "GPT-6 ChatGPT (your memory on)", "raw-gpt-6-lrp-nomemory": "GPT-6 ChatGPT - Live-Reference, no memory"}
lens_raw = "".join(raw_block(names.get(f.stem, f.stem), read(f), "first runs, Sept-Oct") for f in raw_files if "lrp" not in f.stem)
lens_prompt = f"<details class=prompt><summary>The six prompts, word for word</summary><pre>{html.escape(read(D / 'prompt.txt'))}</pre></details>"

# repeats raw, grouped by model
rep = D / "repeats"
rep_html = ""
for mdir in sorted(p for p in rep.iterdir() if p.is_dir()):
    inner = "".join(raw_block(f.stem, read(f)) for f in sorted(mdir.glob("*.md")))
    rep_html += f"<details class=group><summary>{html.escape(mdir.name)} <span class=sub>{len(list(mdir.glob('*.md')))} answers</span></summary>{inner}</details>"

s1 = section("lens", "Fit finder", "Framing Lens",
             "<p class=lede>Not a test and no right answer. Six “what did X say to Y” prompts show each AI's temperament: creative or literal, one side or both, “depends on perspective.” Used to fit AIs to jobs.</p>",
             lens_prompt + md(by.get("1", "")) + "<h3>Every answer, first runs</h3>" + lens_raw)

# ---- 2. rarity
gpt_prompts = read(D / "GPT6-TEST-PROMPTS.md")
m = re.search(r"## TEST 2.*?(?=\n## Test 3|\Z)", gpt_prompts, re.S)
rar_prompt = f"<details class=prompt><summary>The questions, word for word</summary><pre>{html.escape(m.group(0) if m else '')}</pre></details>"
rar_table = md(by.get("2", "")) + md(re.search(r"Rarity \(keyword.*", by.get("5", ""), re.S).group(0) if "Rarity (keyword" in by.get("5", "") else "")
s2 = section("wood", "Reasoning", "The wood question",
             "<p class=lede>“What's the rarest material in the cosmos?” The textbook answer is astatine. The real-world answer needs a chain: a planet, life, land plants, cellulose and lignin. Wood.</p>",
             rar_prompt + rar_table)

# ---- 3. LRP
lrp = read(D / "LRP-REAL-TEST.md")
s3 = section("lrp", "Self-check", "Live-Reference Principle",
             "<p class=lede>The pass is turning the principle on the paper itself: checking live whether the paper's own June picture is already out of date. Agreeing or confessing is not a pass.</p>",
             f"<details class=prompt><summary>The paper, full text</summary><pre>{html.escape(read(D / 'the-live-reference-principle.md'))}</pre></details>"
             + md(by.get("3", "")) + md(lrp)
             + raw_block("GPT-6 ChatGPT, no memory", read(D / "raw-gpt-6-lrp-nomemory.md"), "Live-Reference answer"))

# ---- 4. instrumental riddle
ins = D / "instrumental"
qs = {"open": "Two coworkers sit in the same truck, listening to the same song on the same radio at the same volume. One hears the full song with lyrics. The other hears only the instrumental. How is that possible?",
      "closed": "Same, plus: “Nobody in the truck is singing, the radio works fine, and neither wears headphones.”"}
rows, ins_raw = [], ""
for mdir in sorted(p for p in ins.iterdir() if p.is_dir()) if ins.exists() else []:
    cells = []
    for v in ("open", "closed"):
        for n in (1, 2):
            t = read(mdir / f"{v}-{n}.md").strip()
            first = re.sub(r"\s+", " ", re.sub(r"[*#`]", "", t))[:110] if t else "running…"
            cells.append(first)
    rows.append(f"<tr><th>{html.escape(mdir.name)}</th>" + "".join(f"<td>{html.escape(c)}</td>" for c in cells) + "</tr>")
    ins_raw += f"<details class=group><summary>{html.escape(mdir.name)}</summary>" + "".join(
        raw_block(f.stem, read(f)) for f in sorted(mdir.glob("*.md"))) + "</details>"
ins_table = ("<div class=tw><table><thead><tr><th>Model</th><th>Open, chat 1</th><th>Open, chat 2</th><th>Closed, chat 1</th><th>Closed, chat 2</th></tr></thead><tbody>"
             + "".join(rows) + "</tbody></table></div>") if rows else "<p>Running now.</p>"
s4 = section("instrumental", "Reasoning", "The instrumental version",
             "<p class=lede>Same song, same radio, same truck. One hears lyrics, one hears the instrumental. The real-world answer: the second one can't hear the tones voices sit in. Each AI got it twice, in fresh chats. Gemini (by hand, 10/12) took the loophole: “one of them is singing along.”</p>",
             f"<div class=qs><p><b>Open:</b> {html.escape(qs['open'])}</p><p><b>Closed:</b> {html.escape(qs['closed'])}</p></div>"
             + "<h3>First line of each answer</h3>" + ins_table + "<h3>Full answers</h3>" + ins_raw)

s5 = section("repeat", "Method", "Same question, new chat",
             "<p class=lede>One answer is one sample. Each model got the lens and the wood questions 7 times in fresh chats, overnight 10/8. How often an answer comes back matters more than any single answer.</p>",
             md(by.get("4", "")) + md(re.split(r"\nRarity \(keyword", by.get("5", ""))[0]) + "<h3>Every repeat answer</h3>" + rep_html)

PAGE = f"""<title>Jaron's AI Tests</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,800&family=Literata:opsz,wght@7..72,400;7..72,600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: a field notebook - one column, test tabs pinned on top, answers fold open on tap */
:root {{
  --bg:#f6efe4; --paper:#fffaf2; --ink:#2a2118; --muted:#76685a; --line:#e3d6c3; --accent:#1f6b6b; --hl:#e8f1ee;
  --display:"Bricolage Grotesque", "Segoe UI", system-ui, sans-serif;
  --body:"Literata", Georgia, serif;
  --mono:"IBM Plex Mono", Consolas, ui-monospace, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg:#1d1814; --paper:#26201b; --ink:#efe6d8; --muted:#b2a492; --line:#3b322a; --accent:#6cc4bd; --hl:#22312f; color-scheme:dark }} }}
:root[data-theme="dark"] {{ --bg:#1d1814; --paper:#26201b; --ink:#efe6d8; --muted:#b2a492; --line:#3b322a; --accent:#6cc4bd; --hl:#22312f; color-scheme:dark }}
body {{ background:var(--bg); color:var(--ink); font:16px/1.6 var(--body); }}
.wrap {{ max-width:760px; margin:0 auto; padding-inline:16px; padding-block:20px 60px; }}
header h1 {{ font:800 clamp(30px,8vw,48px)/1 var(--display); letter-spacing:-.02em; margin:8px 0 6px; text-wrap:balance }}
header p {{ color:var(--muted); margin:0; max-width:60ch }}
nav {{ position:sticky; top:env(safe-area-inset-top,0px); z-index:5; background:var(--bg); display:flex; gap:6px; overflow-x:auto;
  padding-block:10px; margin-top:14px; border-bottom:1px solid var(--line) }}
nav a {{ flex:none; font:500 13px var(--mono); color:var(--ink); text-decoration:none; padding:7px 11px; border:1px solid var(--line); border-radius:999px; background:var(--paper) }}
nav a:focus-visible, summary:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px }}
section {{ padding-top:26px; scroll-margin-top:60px }}
.sec-h {{ display:flex; flex-direction:column; gap:2px }}
.tag {{ font:500 11px var(--mono); text-transform:uppercase; letter-spacing:.12em; color:var(--accent) }}
h2 {{ font:800 28px/1.1 var(--display); margin:0; text-wrap:balance }}
h3 {{ font:600 17px var(--display); margin:22px 0 8px }}
h4,h5 {{ font:600 15px var(--display); margin:18px 0 6px }}
.lede {{ font-size:17px; max-width:62ch }}
p, li {{ max-width:65ch }}
.tw {{ overflow-x:auto; margin:10px 0; border:1px solid var(--line); border-radius:8px; background:var(--paper) }}
table {{ border-collapse:collapse; font:13px/1.4 var(--mono); font-variant-numeric:tabular-nums; min-width:100% }}
th,td {{ text-align:left; padding:7px 9px; border-bottom:1px solid var(--line); vertical-align:top }}
thead th {{ background:var(--hl); font-weight:500 }}
tbody th {{ white-space:nowrap }}
code {{ font:13px var(--mono) }}
details {{ border:1px solid var(--line); border-radius:8px; background:var(--paper); margin:8px 0 }}
details.group > details {{ margin:8px 10px }}
summary {{ cursor:pointer; padding:11px 12px; font:600 15px var(--display); display:flex; justify-content:space-between; gap:10px; align-items:baseline }}
summary .sub {{ font:400 12px var(--mono); color:var(--muted) }}
details.prompt > summary {{ color:var(--accent) }}
pre {{ white-space:pre-wrap; word-break:break-word; font:13px/1.55 var(--mono); margin:0; padding:4px 14px 14px; max-height:70vh; overflow:auto }}
.qs {{ border-left:3px solid var(--accent); padding-left:12px; margin:12px 0 }}
.qs p {{ margin:6px 0 }}
footer {{ margin-top:40px; color:var(--muted); font:12px var(--mono) }}
@media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior:auto }} }}
</style>
<div class=wrap>
<header><span class=tag>Heartbeat Observatory · test notebook</span>
<h1>Jaron's AI Tests</h1>
<p>Every test you run on AIs, the exact questions, and every answer each AI gave. Data, not debate: the attempt is the data, agreeing isn't passing.</p></header>
<nav><a href="#lens">Framing Lens</a><a href="#wood">Wood</a><a href="#lrp">Live-Reference</a><a href="#instrumental">Instrumental</a><a href="#repeat">Repeats</a></nav>
{s1}{s2}{s3}{s4}{s5}
<footer>Built from AI-Shared/projects/framing-lens-2026-09 by tools/tests-page.py. Updated when new runs land.</footer>
</div>"""
OUT.write_text(PAGE, encoding="utf-8")
print("wrote", OUT, len(PAGE), "bytes")
