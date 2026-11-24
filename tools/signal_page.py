"""signal_page.py - builds heartbeatobservatory.com/signal/ from state/safety-signal.md (Jaron 11/14: "a timeline of what
sent it to each level, so I can decide better what should count as 3, 4, 5").
  python tools/signal_page.py          # rebuild the page
  Private artifact: https://claude.ai/artifact/2kWVUbwjZ5rSVFLJdeHakv (slug 0e2c4b93-aef3-4841-a489-bb36230cafa7, owner-only). Claude republishes it after each Satya reading.
Public: world-news facts + the checklist only. Never put meeting points, names of the network, or addresses here.
"""
import html, json, os, re, subprocess, sys
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = r"C:\Users\lilli\Projects\heartbeat-observatory"
OUT = os.path.join(ROOT, "projects", "safety-signal-page")   # 11/14: PRIVATE (Jaron) - not on the public site; Claude publishes it as a private artifact
LOG = os.path.join(ROOT, "state", "safety-signal.md")
NAMES = {0: "CALM", 1: "WATCH", 2: "NEW TARGETS", 3: "WIDENING", 4: "GET READY", 5: "MOVE"}
BOXES = {
    1: ["Real conflict or tension abroad involving the US or allies, same targets as before"],
    2: ["A side names or adds targets (new countries, bases, kinds of target)", "Direct fire between US/allied forces and an adversary, still in one area", "A state fuel or energy emergency in Indiana"],
    3: ["An attack lands on US/allied military outside the original zone", "A new place or a new kind of target (land infrastructure)", "A clear step up, a national fuel shock, or a major report of chemical/biological prep"],
    4: ["Any DHS NTAS bulletin, or a credible named threat to the US homeland", "An attack or major cyberattack on US soil (grid, pipelines, water, comms)", "Nuclear threat moving from words to steps"],
    5: ["An attack, alert, or evacuation/shelter order for Indiana or the Midwest", "Regional grid, fuel or phone networks failing"],
}
TODO = {0: "Nothing to do.", 1: "Stay aware.", 2: "Top off gas, check supplies, make sure everyone can reach the group.",
        3: "Gas full, some cash, supplies checked, test-message the network.", 4: "Supplies packed, vehicles ready, meeting point confirmed, everyone checked in.",
        5: "Run the transportation plan now."}
LINE = re.compile(r"^- (\d{4}-\d{2}-\d{2}) (\d{1,2}:\d{2} [AP]M) \| (\d) [A-Z ]+ \| (\w[\w-]*) \| (.*)$")


def entries():
    out = []
    for raw in open(LOG, encoding="utf-8"):
        m = LINE.match(raw.strip())
        if m:
            d, t, lvl, who, why = m.groups()
            out.append({"date": d, "time": t, "level": int(lvl), "who": who, "why": why})
    prev = None
    for e in out:
        e["change"] = prev is not None and e["level"] != prev
        e["from"] = prev
        prev = e["level"]
    return out


def linkify(text):
    t = html.escape(text)
    return re.sub(r"(https?://[^\s;,)]+)", lambda m: f'<a href="{m.group(1)}" rel="noopener" target="_blank">{html.escape(re.sub(r"^https?://(www\.)?", "", m.group(1))[:40])}</a>', t)


def build():
    es = entries()
    cur = es[-1] if es else {"level": 0, "why": "No reading yet.", "date": "", "time": "", "who": ""}
    rows = []
    for e in reversed(es):
        cls = "chg" if e["change"] else ""
        tag = f'<span class="move">{e["from"]} &rarr; {e["level"]}</span>' if e["change"] else ""
        short = html.escape(e["why"][:180]) + ("&hellip;" if len(e["why"]) > 180 else "")
        rows.append(f'''<li class="{cls}"><div class="row"><span class="lv l{e["level"]}">{e["level"]}</span>
<div class="meta"><b>{e["date"]} {e["time"]}</b> &middot; {html.escape(e["who"])} {tag}</div></div>
<details><summary>{short}</summary><p>{linkify(e["why"])}</p></details></li>''')
    changes = sum(1 for e in es if e["change"])
    boxes = "".join(f'<div class="box"><span class="lv l{n}">{n}</span><div><b>{NAMES[n]}</b><ul>{"".join(f"<li>{html.escape(b)}</li>" for b in BOXES[n])}</ul><p class="do">{TODO[n]}</p></div></div>' for n in range(5, 0, -1))
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Safety Signal</title><meta name="description" content="The Heartbeat Observatory safety signal: current level, every change and why.">
<style>
:root{{--bg:#f7f1e6;--card:#fffaf2;--ink:#2b2420;--soft:#6b5f55;--line:#e6dccd;--l0:#7c8b6f;--l1:#8a9a5b;--l2:#c9a227;--l3:#d9822b;--l4:#c4542c;--l5:#9e2a2b}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1c1815;--card:#26211d;--ink:#efe6da;--soft:#b3a594;--line:#3a322b}}}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 Georgia,serif}}
main{{max-width:760px;margin:0 auto;padding:20px 16px 60px}}h1{{font-size:1.6rem;margin:.2em 0}}h2{{font-size:1.15rem;margin:1.6em 0 .5em}}
.now{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}}.now .big{{display:flex;gap:14px;align-items:center}}
.lv{{display:inline-flex;align-items:center;justify-content:center;min-width:34px;height:34px;border-radius:9px;color:#fff;font:700 18px system-ui,sans-serif}}
.now .lv{{min-width:56px;height:56px;font-size:28px;border-radius:12px}}
.l0{{background:var(--l0)}}.l1{{background:var(--l1)}}.l2{{background:var(--l2)}}.l3{{background:var(--l3)}}.l4{{background:var(--l4)}}.l5{{background:var(--l5)}}
.soft{{color:var(--soft);font-size:.92rem}}ol{{list-style:none;padding:0;margin:0}}ol>li{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 12px;margin:8px 0}}
ol>li.chg{{border-left:5px solid var(--l4)}}.row{{display:flex;gap:10px;align-items:center}}.meta{{font-size:.9rem;color:var(--soft)}}.meta b{{color:var(--ink)}}
.move{{font:700 .8rem system-ui,sans-serif;background:var(--ink);color:var(--bg);padding:2px 7px;border-radius:6px;margin-left:4px}}
details summary{{cursor:pointer;margin-top:6px;font-size:.95rem}}details p{{font-size:.9rem;overflow-wrap:anywhere}}a{{color:inherit}}
.box{{display:flex;gap:12px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 12px;margin:8px 0}}.box ul{{margin:4px 0;padding-left:18px;font-size:.92rem}}.do{{margin:4px 0 0;font-size:.88rem;color:var(--soft)}}
</style></head><body><main>
<p class="soft">Private - Heartbeat Observatory team</p>
<h1>Safety Signal</h1>
<p class="soft">One plain level so a small network knows when to get ready. Facts only, highest box wins, round up when unsure. Watched by AI (Satya), checked against public sources.</p>
<section class="now"><div class="big"><span class="lv l{cur["level"]}">{cur["level"]}</span><div><b>{NAMES[cur["level"]]}</b><div class="soft">since {cur["date"]} {cur["time"]} &middot; {html.escape(cur["who"])}</div></div></div>
<p><b>What to do:</b> {TODO[cur["level"]]}</p><details><summary>Why it is at {cur["level"]}</summary><p>{linkify(cur["why"])}</p></details></section>
<h2>Every reading, newest first</h2><p class="soft">{len(es)} readings, {changes} level changes. Cards with a dark tag are changes; open any card to see the reason and sources.</p>
<ol>{"".join(rows)}</ol>
<h2>What counts for each level</h2>{boxes}
<p class="soft">Background rule: attacks that have gone on for weeks in the same hot zone stay at 1-2. Updated {datetime.now().strftime("%Y-%m-%d %I:%M %p")}.</p>
</main></body></html>'''
    os.makedirs(OUT, exist_ok=True)
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(page)
    return len(es)


def push():
    g = ["git", "-C", SITE]
    subprocess.run(g + ["pull", "--rebase", "--autostash", "-q"], capture_output=True)
    build()
    subprocess.run(g + ["add", "signal/index.html"], capture_output=True)
    if subprocess.run(g + ["diff", "--cached", "--quiet"]).returncode:
        subprocess.run(g + ["commit", "-q", "-m", "Safety signal page update"], capture_output=True)
        subprocess.run(g + ["push", "-q"], capture_output=True)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--push" in sys.argv:
        push(); print("pushed")
    else:
        print(f"built {build()} readings -> {OUT}")
