"""Build Jaron's readable Principles page from projects/principles/LEDGER.md + SAYINGS.md.

Writes state/principles-page/index.html (one self-contained page). Publish it as the
"Jaron's Principles" artifact (private until he shares it). Re-run after new principles land.
"""
import html, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "projects/principles/LEDGER.md"
SAYINGS = ROOT / "projects/principles/SAYINGS.md"
OUT = ROOT / "state/principles-page/index.html"


def rows():
    out = []
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| P-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        pid, date, text = cells[0], cells[1], cells[2]
        rest = cells[3:]
        frm = rest[0] if rest else ""
        links = sorted(set(re.findall(r"P-\d{4}", " ".join(rest[1:]))) - {pid})
        how = rest[2] if len(rest) >= 6 else ""
        status = rest[-1] if len(rest) >= 6 else ""
        out.append({"id": pid, "n": int(pid[2:]), "date": date, "text": text.replace("**", ""),
                    "from": frm, "links": links, "how": how, "status": status})
    return out


def sayings():
    if not SAYINGS.exists():
        return []
    blocks, cur = [], None
    for line in SAYINGS.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            cur = {"title": line[3:].strip(), "text": ""}
            blocks.append(cur)
        elif cur is not None and line.startswith(">"):
            cur["text"] += line.lstrip("> ").strip() + " "
    return [b for b in blocks if b["text"].strip()]


PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Jaron's Principles</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
<style>
:root {
  /* Warm reading room: cream paper, ink, a deep forest accent. One column, numbered entries, search on top. */
  --paper: #f6f0e4;
  --card: #fffaf1;
  --ink: #2b2620;
  --muted: #6e6355;
  --rule: #e3d8c4;
  --accent: #2f5d50;
  --accent-soft: #dfe9e3;
  --display: "Fraunces", Georgia, "Times New Roman", serif;
  --body: "Source Sans 3", "Segoe UI", system-ui, sans-serif;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --paper: #1d1a16; --card: #26221c; --ink: #efe6d6; --muted: #b3a690;
    --rule: #3a342b; --accent: #8fc2ae; --accent-soft: #2c3a33; color-scheme: dark;
  }
}
:root[data-theme="dark"] {
  --paper: #1d1a16; --card: #26221c; --ink: #efe6d6; --muted: #b3a690;
  --rule: #3a342b; --accent: #8fc2ae; --accent-soft: #2c3a33; color-scheme: dark;
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--paper); color: var(--ink); font: 17px/1.55 var(--body); }
main { max-width: 720px; margin: 0 auto; padding: 28px 16px 64px; display: grid; gap: 22px; }
h1 { font: 600 2rem/1.15 var(--display); margin: 0; text-wrap: balance; }
h2 { font: 600 1.25rem/1.2 var(--display); margin: 0; text-wrap: balance; }
.lede { color: var(--muted); margin: 6px 0 0; max-width: 62ch; }
.stats { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 12px; }
.chip { background: var(--accent-soft); color: var(--accent); border-radius: 999px; padding: 3px 11px; font-size: .9rem; font-weight: 600; font-variant-numeric: tabular-nums; }
.tools { position: sticky; top: 0; background: var(--paper); padding: 10px 0; display: grid; gap: 8px; z-index: 2; border-bottom: 1px solid var(--rule); }
input[type=search] { width: 100%; font: inherit; padding: 11px 14px; border: 1px solid var(--rule); border-radius: 10px; background: var(--card); color: var(--ink); }
input[type=search]:focus-visible, button:focus-visible, a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.filters { display: flex; gap: 6px; flex-wrap: wrap; }
.filters button { font: 600 .9rem var(--body); border: 1px solid var(--rule); background: var(--card); color: var(--ink); border-radius: 999px; padding: 6px 12px; cursor: pointer; min-height: 36px; }
.filters button[aria-pressed=true] { background: var(--accent); border-color: var(--accent); color: var(--paper); }
.saying { background: var(--card); border: 1px solid var(--rule); border-left: 4px solid var(--accent); border-radius: 12px; padding: 16px 18px; display: grid; gap: 8px; }
.saying p { margin: 0; font: 500 1.08rem/1.55 var(--display); }
.list { display: grid; gap: 12px; }
.p { background: var(--card); border: 1px solid var(--rule); border-radius: 12px; padding: 14px 16px; display: grid; gap: 6px; scroll-margin-top: 130px; }
.p:target { border-color: var(--accent); box-shadow: 0 0 0 2px var(--accent-soft); }
.meta { display: flex; gap: 10px; align-items: baseline; color: var(--muted); font-size: .88rem; font-variant-numeric: tabular-nums; }
.num { font: 600 1rem var(--display); color: var(--accent); }
.text { margin: 0; overflow-wrap: anywhere; }
.from { margin: 0; color: var(--muted); font-size: .92rem; overflow-wrap: anywhere; }
.links { display: flex; flex-wrap: wrap; gap: 6px; font-size: .88rem; }
.links a { color: var(--accent); text-decoration: none; border-bottom: 1px solid var(--accent-soft); }
.empty { color: var(--muted); text-align: center; padding: 24px 0; }
footer { color: var(--muted); font-size: .88rem; }
@media (prefers-reduced-motion: no-preference) { html { scroll-behavior: smooth; } }
</style>
</head>
<body>
<main>
  <header>
    <h1>Jaron's Principles</h1>
    <p class="lede">Every principle pulled from Jaron's own words, numbered in the order they came, with the moment each one came from. Tap a linked number to jump to the principle it builds on.</p>
    <div class="stats" id="stats"></div>
  </header>
  <section class="tools" aria-label="Search and filter">
    <label for="q" class="sr" style="position:absolute;left:-9999px">Search principles</label>
    <input id="q" type="search" placeholder="Search words, like time, fog, people, chessboard">
    <div class="filters" id="filters" role="group" aria-label="Show"></div>
  </section>
  <section id="sayings" aria-label="Sayings in his own words"></section>
  <section class="list" id="list" aria-live="polite"></section>
  <footer id="foot"></footer>
</main>
<script>
const P = __DATA__;
const S = __SAYINGS__;
const UPDATED = "__UPDATED__";
const esc = s => s.replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const months = [...new Set(P.map(p => p.date.split("/")[0]))];
const monthName = m => ({"9":"September","10":"October","11":"November","12":"December"}[m] || "Month " + m);
let filter = "all";
const recent = P.filter(p => /^11\//.test(p.date)).length;
document.getElementById("stats").innerHTML =
  `<span class="chip">${P.length} principles</span><span class="chip">${recent} so far in November</span><span class="chip">Newest: ${P[P.length-1].id.replace("P-","#").replace(/#0+/,"#")}</span>`;
const fwrap = document.getElementById("filters");
const opts = [["all", "All"], ["new", "Newest first"], ["old", "Oldest first"]];
let order = "new";
opts.forEach(([k, label]) => {
  const b = document.createElement("button"); b.type = "button"; b.id = "f-" + k; b.textContent = label;
  b.setAttribute("aria-pressed", k === "new");
  b.onclick = () => { if (k === "all") { document.getElementById("q").value = ""; } else { order = k; }
    fwrap.querySelectorAll("button").forEach(x => x.setAttribute("aria-pressed", x.id === "f-" + (k === "all" ? order : k)));
    draw(); };
  fwrap.appendChild(b);
});
document.getElementById("sayings").innerHTML = S.map(s =>
  `<div class="saying"><h2>${esc(s.title.replace(/\s*\(.*$/, ""))}</h2><p>${esc(s.text.trim())}</p></div>`).join("");
function draw() {
  const q = document.getElementById("q").value.trim().toLowerCase();
  let items = P.filter(p => !q || (p.text + " " + p.from + " " + p.id).toLowerCase().includes(q));
  items.sort((a, b) => order === "old" ? a.n - b.n : b.n - a.n);
  document.getElementById("list").innerHTML = items.length ? items.map(p => `
    <article class="p" id="${p.id}">
      <div class="meta"><span class="num">${p.id.replace("P-", "#").replace(/#0+/, "#")}</span><span>${esc(p.date)}</span></div>
      <p class="text">${esc(p.text)}</p>
      ${p.from ? `<p class="from">From: ${esc(p.from)}</p>` : ""}
      ${p.links.length ? `<div class="links">Builds on: ${p.links.map(l => `<a href="#${l}">${l.replace("P-", "#").replace(/#0+/, "#")}</a>`).join("")}</div>` : ""}
    </article>`).join("") : `<p class="empty">No principle matches "${esc(q)}".</p>`;
}
document.getElementById("q").addEventListener("input", draw);
document.getElementById("foot").textContent = "Updated " + UPDATED + ". Logged by Claude from Jaron's words; his to keep, change or share.";
draw();
if (location.hash) { const el = document.getElementById(location.hash.slice(1)); if (el) el.scrollIntoView(); }
</script>
</body>
</html>
"""


def main():
    from datetime import datetime
    data = rows()
    page = (PAGE.replace("__DATA__", json.dumps(data, ensure_ascii=False))
                .replace("__SAYINGS__", json.dumps(sayings(), ensure_ascii=False))
                .replace("__UPDATED__", datetime.now().strftime("%b %d, %Y %I:%M %p").replace(" 0", " ")))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT} with {len(data)} principles")


if __name__ == "__main__":
    main()
