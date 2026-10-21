"""sort-review-page.py - one phone page comparing the two independent repo reads (Sonnet full pass + Fable second read)
for Jaron's bracket review (Claude Code, 2026-10-14). Writes projects/accumulation-sort/review.html (published as an Artifact).
  python tools/sort-review-page.py
"""
import html, json, pathlib, re

D = pathlib.Path(__file__).resolve().parent.parent / "projects" / "accumulation-sort"
E = lambda s: html.escape(str(s or ""))


def md_inline(s):
    s = E(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", s)


son = json.loads((D / "PROPOSED-tiers.json").read_text(encoding="utf-8"))
son.pop("_doc", None)
old = json.loads((D / "work" / "tiers.json").read_text(encoding="utf-8"))
old.pop("_doc", None)

fab_txt = (D / "SECOND-READ-fable.md").read_text(encoding="utf-8")
fab = {}
for line in fab_txt.splitlines():
    if line.startswith("| ") and not line.startswith("| repo") and not line.startswith("|---"):
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) >= 8:
            fab[c[0].strip("`* ")] = dict(kind=c[1], stage=c[2], tier=re.sub(r"[^A-E?]", "", c[3])[:1], principle=c[4],
                                          organ=c[5], drift=c[6], hidden=c[7])


def section(title, body_md):
    m = re.search(r"## " + re.escape(title) + r".*?\n(.*?)(?=\n## |\Z)", fab_txt, re.S)
    return m.group(1).strip() if m else ""


def md_block(t):
    out, ul = [], False
    for l in t.splitlines():
        if re.match(r"\s*[-*]\s+|\s*\d+\.\s+", l):
            if not ul:
                out.append("<ul>"); ul = True
            out.append("<li>" + md_inline(re.sub(r"^\s*([-*]|\d+\.)\s+", "", l)) + "</li>")
        else:
            if ul:
                out.append("</ul>"); ul = False
            if l.strip():
                out.append("<p>" + md_inline(l) + "</p>")
    if ul:
        out.append("</ul>")
    return "\n".join(out)


rows_dis, rows_all = [], []
for name in sorted(son, key=lambda n: ("ABCDE?".find(son[n].get("tier", "?")), n.lower())):
    s = son[name]
    f = fab.get(name)
    o = old.get(name, {}).get("tier", "?")
    st, ft = s.get("tier", "?"), (f or {}).get("tier", "")
    agree = (not f) or ft == st
    badge = f'<span class="t t{st}">{st}</span>'
    move = f'<span class="mv">was {o}</span>' if o != st else ""
    fabbit = ""
    if f:
        fabbit = (f'<div class="fab"><div class="lbl">Fable (second read): {E(ft) or "?"} · {E(f["kind"])} · {E(f["stage"])}</div>'
                  f'<p>{md_inline(f["principle"])}</p>'
                  + (f'<p class="hid"><b>Hidden piece:</b> {md_inline(f["hidden"])}</p>' if f["hidden"] and f["hidden"].lower() not in ("none", "none.", "-") else "")
                  + "</div>")
    drift = s.get("readme_drift") or ""
    card = (f'<details class="r{"" if agree else " dis"}"><summary>{badge}<span class="n">{E(name)}</span>{move}'
            f'<span class="ks">{E(s.get("kind"))} · {E(s.get("stage"))}</span></summary>'
            f'<div class="body"><div class="lbl">Sonnet (full read) · organ: {E(s.get("organ"))} · last commit {E(s.get("last_commit"))}</div>'
            f'<p class="pr">{md_inline(s.get("principle"))}</p><p class="why">{md_inline(s.get("why"))}</p>'
            + (f'<p class="dr"><b>README drift:</b> {md_inline(drift)}</p>' if drift else "")
            + (f'<p class="nx"><b>Next stage needs:</b> {md_inline(s.get("next_stage"))}</p>' if s.get("next_stage") else "")
            + fabbit + '<div class="you">Your bracket: keep · drop · close but…</div></div></details>')
    (rows_dis if not agree else rows_all).append(card)

n_both = sum(1 for n in son if n in fab)
n_dis = len(rows_dis)
findings = section("Corrections to tiers.json this read would make", "")
links = section("What connects to what (parts of one larger system)", "")

PAGE = f"""<title>Repo Sort Review</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@400&display=swap">
<style>
/* Layout: field ledger - disagreements first, then every repo as a fold-open card with both readers' notes */
:root {{ --bg:#f6efe4; --card:#fffaf2; --ink:#2a2118; --mut:#76685a; --line:#e3d6c3; --acc:#1f6b6b; --warn:#a4501a;
  --A:#2e7d4f; --B:#5b7f2a; --C:#6b6b6b; --D:#7a5a2e; --E:#9a9a9a;
  --disp:"Fraunces",Georgia,serif; --body:"Source Sans 3","Segoe UI",system-ui,sans-serif; --mono:"JetBrains Mono",Consolas,monospace; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#1d1814; --card:#26201b; --ink:#efe6d8; --mut:#b2a492; --line:#3b322a; --acc:#6cc4bd; --warn:#e38a4f; color-scheme:dark }} }}
:root[data-theme="dark"] {{ --bg:#1d1814; --card:#26201b; --ink:#efe6d8; --mut:#b2a492; --line:#3b322a; --acc:#6cc4bd; --warn:#e38a4f; color-scheme:dark }}
body {{ background:var(--bg); color:var(--ink); font:16px/1.55 var(--body) }}
.w {{ max-width:760px; margin:0 auto; padding-inline:16px; padding-block:18px 60px }}
h1 {{ font:800 clamp(28px,8vw,44px)/1.05 var(--disp); margin:6px 0; text-wrap:balance }}
h2 {{ font:600 22px var(--disp); margin:28px 0 8px }}
.k {{ font:12px var(--mono); color:var(--acc); text-transform:uppercase; letter-spacing:.1em }}
.lede {{ color:var(--mut); max-width:62ch }}
.stats {{ display:flex; flex-wrap:wrap; gap:8px; margin:12px 0; font:13px var(--mono) }}
.stats span {{ border:1px solid var(--line); border-radius:999px; padding:4px 10px; background:var(--card) }}
details.r {{ background:var(--card); border:1px solid var(--line); border-radius:10px; margin:8px 0 }}
details.r.dis {{ border-color:var(--warn) }}
summary {{ cursor:pointer; padding:10px 12px; display:flex; flex-wrap:wrap; gap:6px 10px; align-items:baseline }}
summary:focus-visible {{ outline:2px solid var(--acc); outline-offset:2px }}
.n {{ font-weight:600; word-break:break-word; min-width:0 }}
.ks {{ font:12px var(--mono); color:var(--mut); width:100% }}
.mv {{ font:12px var(--mono); color:var(--warn) }}
.t {{ font:700 13px var(--mono); color:#fff; border-radius:5px; padding:1px 7px }}
.tA {{ background:var(--A) }} .tB {{ background:var(--B) }} .tC {{ background:var(--C) }} .tD {{ background:var(--D) }} .tE,.t\\? {{ background:var(--E) }}
.body {{ padding:0 14px 12px }}
.lbl {{ font:12px var(--mono); color:var(--mut); margin-top:6px }}
.pr {{ font-weight:600 }}
.why,.dr,.nx,.hid {{ color:var(--ink); font-size:15px }}
.fab {{ border-left:3px solid var(--acc); padding-left:10px; margin-top:10px }}
.you {{ margin-top:10px; font:12px var(--mono); color:var(--acc) }}
code {{ font:13px var(--mono); word-break:break-word }}
p, li {{ max-width:65ch }}
</style>
<div class="w">
<span class="k">accumulation-sort · two independent readers · from code, not READMEs</span>
<h1>Repo Sort Review</h1>
<p class="lede">Sonnet read all {len(son)} repos. Fable read {len(fab)} of them on its own without seeing Sonnet's answers. Orange cards are where they disagree on the tier - start there. Each card: what it is, how far it got, the principle inside it, and a spot for your bracket.</p>
<div class="stats"><span>{len(son)} repos</span><span>{n_both} read twice</span><span>{n_dis} disagreements</span><span>{sum(1 for n in son if old.get(n,{}).get('tier','?')!=son[n].get('tier'))} tier changes vs old sort</span></div>
<h2>Where the two readers disagree</h2>
{''.join(rows_dis) or '<p>None - they agree on every repo both read.</p>'}
<h2>Fable's corrections to the old sort</h2>
{md_block(findings)}
<h2>What connects to what</h2>
{md_block(links)}
<h2>Every repo</h2>
{''.join(rows_all)}
</div>"""
(D / "review.html").write_text(PAGE, encoding="utf-8")
print("wrote", len(PAGE), "bytes;", len(fab), "fable rows;", n_dis, "disagreements")
