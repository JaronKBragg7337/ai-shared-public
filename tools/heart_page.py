"""heart_page.py - Jaron's private heart page (11/11/2026).

Pulls every "Observatory heartbeat" Shortcut send from the AI mailbox (from_ai = jaron-watch, lines like
"Nov 10, 2026 at 1:16 PM139"), keeps an accumulating store in projects/reality-agent/heart/readings.json,
and writes projects/reality-agent/heart/index.html: one chart per day, with his own logged moments marked.
Moments live in projects/reality-agent/heart/moments.json ({"2026-11-10": [["13:30","Court starts"], ...]}).
Publish the page as the private artifact "Heart Page" (slug in heart/README.md). Re-run after each new send.
"""
import json, re, subprocess, sys, os
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "projects/reality-agent/heart"
STORE, MOMENTS, OUT = DIR / "readings.json", DIR / "moments.json", DIR / "index.html"
SLEEP = re.compile(r"SLEEP\s*([A-Z][a-z]{2} \d{1,2}, \d{4}) at (\d{1,2}:\d{2})\W*(AM|PM)\s*([A-Za-z ]+?)\s*([A-Z][a-z]{2} \d{1,2}, \d{4}) at (\d{1,2}:\d{2})\W*(AM|PM)")
LINE = re.compile(r"(HRV\s*)?([A-Z][a-z]{2} \d{1,2}, \d{4}) at (\d{1,2}:\d{2})\W*(AM|PM)\s*([\d.]+)")


def fetch():
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    out = subprocess.run([sys.executable, str(ROOT / "tools/mailbox.py"), "list", "--to", "claude", "--limit", "500"],
                         capture_output=True, text=True, encoding="utf-8", env=env).stdout
    return [m for m in json.loads(out) if m.get("from_ai") == "jaron-watch"]


def main():
    DIR.mkdir(parents=True, exist_ok=True)
    store = json.loads(STORE.read_text(encoding="utf-8")) if STORE.exists() else {}
    HSTORE = DIR / "hrv.json"
    hstore = json.loads(HSTORE.read_text(encoding="utf-8")) if HSTORE.exists() else {}
    CSTORE = DIR / "clarity.json"
    cstore = json.loads(CSTORE.read_text(encoding="utf-8")) if CSTORE.exists() else {}
    PSTORE = DIR / "places.json"
    places = json.loads(PSTORE.read_text(encoding="utf-8")) if PSTORE.exists() else {}
    TSTORE = DIR / "steps.json"
    tstore = json.loads(TSTORE.read_text(encoding="utf-8")) if TSTORE.exists() else {}
    SSTORE = DIR / "sleep.json"
    sstore = json.loads(SSTORE.read_text(encoding="utf-8")) if SSTORE.exists() else {}
    for m in fetch():
        for d1, t1, a1, stage, d2, t2, a2 in SLEEP.findall(m["body"]):
            st = datetime.strptime(f"{d1} {t1} {a1}", "%b %d, %Y %I:%M %p"); en = datetime.strptime(f"{d2} {t2} {a2}", "%b %d, %Y %I:%M %p")
            sstore.setdefault(en.strftime("%Y-%m-%d"), {})[st.strftime("%H:%M")] = [en.strftime("%H:%M"), stage.strip(), int((en - st).total_seconds() // 60)]
        cm = re.match(r"\W*CLARITY\s+(ONE|TWO|THREE|FOUR|FIVE|[1-5])\b", m["body"], re.I)
        if cm:
            v = cm.group(1).upper(); v = {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5}.get(v, v)
            at = datetime.fromisoformat(m["created_at"].replace("Z", "+00:00")).astimezone()
            cstore.setdefault(at.strftime("%Y-%m-%d"), {})[at.strftime("%H:%M")] = int(v)
            continue
        wm = re.match(r"\W*WATCH\s+(ON|OFF)\b", m["body"], re.I)
        if wm and len(m["body"]) < 40:
            at = datetime.fromisoformat(m["created_at"].replace("Z", "+00:00")).astimezone()
            places.setdefault(at.strftime("%Y-%m-%d"), {})[at.strftime("%H:%M")] = "Watch " + wm.group(1).lower()
            continue
        pm = re.match(r"\W*(ARRIVED|LEFT)\s+(.+)", m["body"], re.I)
        if pm and len(m["body"]) < 80:
            at = datetime.fromisoformat(m["created_at"].replace("Z", "+00:00")).astimezone()
            places.setdefault(at.strftime("%Y-%m-%d"), {})[at.strftime("%H:%M")] = (pm.group(1).capitalize() + " " + pm.group(2).strip().lower())
            continue
        if m["body"].lstrip().startswith("SLEEP"):
            continue
        if re.match(r"\W*(STEPS|DISTANCE)", m["body"], re.I):   # 11/15: "STEPS <date> at <time> <n>" / "DISTANCE ... <mi>"
            for kind, d, t, ap, v in re.findall(r"(STEPS|DISTANCE)\s*([A-Z][a-z]{2} \d{1,2}, \d{4}) at (\d{1,2}:\d{2})\W*(AM|PM)\s*([\d.]+)", m["body"], re.I):
                ts = datetime.strptime(f"{d} {t} {ap}", "%b %d, %Y %I:%M %p")
                if len(re.findall(r"(STEPS|DISTANCE)\s*[A-Z]", m["body"], re.I)) <= 3:   # grouped by day = one daily total
                    if float(v) > 0: tstore.setdefault(ts.strftime("%Y-%m-%d"), {})[kind.lower() + "_total"] = float(v)
                else:
                    tstore.setdefault(ts.strftime("%Y-%m-%d"), {}).setdefault(kind.lower(), {})[ts.strftime("%H:%M")] = float(v)
            continue
        for hrv, d, t, ap, v in LINE.findall(m["body"]):
            ts = datetime.strptime(f"{d} {t} {ap}", "%b %d, %Y %I:%M %p")
            day, hm = ts.strftime("%Y-%m-%d"), ts.strftime("%H:%M")
            if hrv:
                hstore.setdefault(day, {})[hm] = round(float(v))
            else:
                store.setdefault(day, {})[hm] = round(float(v))
    STORE.write_text(json.dumps(store, indent=1, sort_keys=True), encoding="utf-8")
    HSTORE.write_text(json.dumps(hstore, indent=1, sort_keys=True), encoding="utf-8")
    TSTORE.write_text(json.dumps(tstore, indent=1, sort_keys=True), encoding="utf-8")
    SSTORE.write_text(json.dumps(sstore, indent=1, sort_keys=True), encoding="utf-8")
    CSTORE.write_text(json.dumps(cstore, indent=1, sort_keys=True), encoding="utf-8")
    PSTORE.write_text(json.dumps(places, indent=1, sort_keys=True), encoding="utf-8")
    moments = json.loads(MOMENTS.read_text(encoding="utf-8")) if MOMENTS.exists() else {}

    def drop_flips(ev, mins=10):
        """11/17: GPS drifts under the railroad bridge / downtown buildings, so the phone fired LEFT HOME 10:57 and
        ARRIVED HOME 10:59 while Jaron was blocks away. A Left/Arrived pair for the same place within 10 minutes = drift,
        not a trip. Raw events stay in places.json; only the timeline skips them."""
        ts = sorted(ev.items())
        def m(t): h, mm = t.split(":"); return int(h) * 60 + int(mm)
        drop = set()
        for (t1, l1), (t2, l2) in zip(ts, ts[1:]):
            w1, p1 = (l1.split(" ", 1) + [""])[:2]; w2, p2 = (l2.split(" ", 1) + [""])[:2]
            if p1 == p2 and {w1, w2} == {"Left", "Arrived"} and 0 <= m(t2) - m(t1) <= mins:
                drop |= {t1, t2}
        return {t: l for t, l in ev.items() if t not in drop}

    for day, ev in ((d, drop_flips(e)) for d, e in places.items()):
        have = {t for t, _ in moments.get(day, [])}
        for t, label in ev.items():
            if t not in have:
                moments.setdefault(day, []).append([t, label + " (auto)"])
        moments[day].sort()
    weather = {}
    try:
        import urllib.request
        url = ("https://api.open-meteo.com/v1/forecast?latitude=41.08&longitude=-85.14&past_days=14&forecast_days=1"
               "&hourly=temperature_2m,precipitation&temperature_unit=fahrenheit&timezone=America%2FIndiana%2FIndianapolis")
        h = json.load(urllib.request.urlopen(url, timeout=20))["hourly"]
        for t, temp, rain in zip(h["time"], h["temperature_2m"], h["precipitation"]):
            d, hr = t[:10], t[11:13]
            if d in store and temp is not None:
                weather.setdefault(d, {})[hr] = [round(temp), rain or 0]
    except Exception as e:
        print("weather skipped:", e)
    days = {d: sorted(v.items()) for d, v in sorted(store.items())}
    html = PAGE.replace("__DATA__", json.dumps(days)).replace("__MOMENTS__", json.dumps(moments)).replace("__WEATHER__", json.dumps(weather)).replace("__HRV__", json.dumps(hstore)).replace("__SLEEP__", json.dumps(sstore)).replace("__CLARITY__", json.dumps(cstore)).replace("__STEPS__", json.dumps(tstore)) \
               .replace("__UPDATED__", datetime.now().strftime("%b %d, %I:%M %p").replace(" 0", " "))
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT}: {sum(len(v) for v in days.values())} readings over {len(days)} day(s)")


PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Heart Page</title>
<style>
:root {
  /* Warm cream reading room; one warm red accent for the heart line. */
  --paper:#f6f0e4; --card:#fffaf1; --ink:#2b2620; --muted:#6e6355; --rule:#e3d8c4; --accent:#b4483a; --soft:#f3ddd6; --mark:#2f5d50;
  color-scheme: light;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --paper:#1d1a16; --card:#26221c; --ink:#efe6d6; --muted:#b3a690; --rule:#3a342b; --accent:#e58a74; --soft:#3a2a25; --mark:#8fc2ae; color-scheme: dark; } }
:root[data-theme="dark"] { --paper:#1d1a16; --card:#26221c; --ink:#efe6d6; --muted:#b3a690; --rule:#3a342b; --accent:#e58a74; --soft:#3a2a25; --mark:#8fc2ae; color-scheme: dark; }
* { box-sizing: border-box; }
body { margin:0; background:var(--paper); color:var(--ink); font:17px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif; }
main { max-width:760px; margin:0 auto; padding:24px 16px 56px; display:grid; gap:18px; }
h1 { font-size:1.7rem; margin:0; }
.lede { color:var(--muted); margin:4px 0 0; }
.days { display:flex; gap:8px; flex-wrap:wrap; }
.days button { font:600 .95rem system-ui; border:1px solid var(--rule); background:var(--card); color:var(--ink); border-radius:999px; padding:8px 14px; min-height:40px; cursor:pointer; }
.days button[aria-pressed=true] { background:var(--accent); border-color:var(--accent); color:var(--paper); }
.card { background:var(--card); border:1px solid var(--rule); border-radius:14px; padding:14px; }
.stats { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; }
.stat b { display:block; font-size:1.5rem; font-variant-numeric:tabular-nums; }
.stat span { color:var(--muted); font-size:.85rem; }
svg { width:100%; height:auto; display:block; touch-action:pan-y; }
.tip { min-height:1.6em; color:var(--muted); font-variant-numeric:tabular-nums; }
.moments { display:grid; gap:6px; margin:0; padding:0; list-style:none; }
.moments li { display:flex; gap:10px; }
.moments time { color:var(--mark); font-weight:600; min-width:4.5em; font-variant-numeric:tabular-nums; }
footer { color:var(--muted); font-size:.85rem; }
</style>
</head>
<body>
<main>
  <header>
    <h1>Heart Page</h1>
    <p class="lede">Your watch's heart readings, sent by the Observatory heartbeat shortcut. Tap a day, then touch the line to see a time. Green marks are moments you told Claude about.</p>
  </header>
  <div class="days" id="days" role="group" aria-label="Day"></div>
  <section class="card stats" id="stats"></section>
  <p class="lede" id="wx" style="margin:-6px 4px 0"></p>
  <p class="lede" id="hrv" style="margin:-10px 4px 0"></p>
  <p class="lede" id="steps" style="margin:-10px 4px 0"></p>
  <p class="lede" id="sleep" style="margin:-10px 4px 0"></p>
  <p class="lede" id="clarity" style="margin:-10px 4px 0;font-weight:600"></p>
  <section class="card"><div id="chart"></div><div class="tip" id="tip">Touch the line for a reading.</div></section>
  <section class="card"><h2 style="margin:0 0 8px;font-size:1.1rem">Moments that day</h2><ul class="moments" id="moments"></ul></section>
  <footer>Private to Jaron. Updated __UPDATED__. A heart rate can't tell excitement from stress, so the moments say which it was.</footer>
</main>
<script>
const D = __DATA__, M = __MOMENTS__, WX = __WEATHER__, HV = __HRV__, SL = __SLEEP__, CL = __CLARITY__, ST = __STEPS__;
const days = [...new Set([...Object.keys(D), ...Object.keys(HV), ...Object.keys(SL), ...Object.keys(CL)])].sort();
let cur = days[days.length - 1];
const mins = t => { const [h, m] = t.split(":").map(Number); return h * 60 + m; };
const fmt = t => { let [h, m] = t.split(":").map(Number); const ap = h >= 12 ? "PM" : "AM"; h = h % 12 || 12; return h + ":" + String(m).padStart(2, "0") + " " + ap; };
const nice = d => new Date(d + "T12:00:00").toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });
function draw() {
  document.querySelectorAll("#days button").forEach(b => b.setAttribute("aria-pressed", b.dataset.d === cur));
  const pts = D[cur] || [], vals = pts.map(p => p[1]);
  const avg = vals.length ? Math.round(vals.reduce((a, b) => a + b, 0) / vals.length) : 0;
  const hi = pts.reduce((a, p) => p[1] > a[1] ? p : a, ["", 0]), lo = pts.reduce((a, p) => p[1] < a[1] ? p : a, ["", 999]);
  document.getElementById("stats").innerHTML =
    `<div class="stat"><b>${hi[1] || "-"}</b><span>highest${hi[0] ? " at " + fmt(hi[0]) : ""}</span></div>` +
    `<div class="stat"><b>${lo[1] < 999 ? lo[1] : "-"}</b><span>lowest${lo[0] ? " at " + fmt(lo[0]) : ""}</span></div>` +
    `<div class="stat"><b>${avg || "-"}</b><span>average, ${vals.length} readings</span></div>`;
  const wx = WX[cur] || {}, temps = Object.values(wx).map(w => w[0]), rain = Object.values(wx).reduce((a, w) => a + w[1], 0);
  const sl = Object.entries(SL[cur] || {}).sort(), sum = {};
  sl.forEach(([, [, st, m]]) => sum[st] = (sum[st] || 0) + m);
  const asleep = (sum.Core || 0) + (sum.Deep || 0) + (sum.REM || 0) + (sum.Asleep || 0), hm = m => Math.floor(m / 60) + "h " + (m % 60) + "m";
  document.getElementById("sleep").textContent = sl.length ? `Sleep ending this day: ${hm(asleep)} asleep (deep ${sum.Deep || 0}m, REM ${sum.REM || 0}m, core ${sum.Core || 0}m${sum.Asleep ? ", unstaged " + sum.Asleep + "m" : ""}), awake ${sum.Awake || 0}m, ${fmt(sl[0][0])} to ${fmt(sl[sl.length - 1][1][0])}` : "";
  const cl = Object.entries(CL[cur] || {}).sort();
  document.getElementById("clarity").textContent = cl.length ? "How clear your head felt (1-5): " + cl.map(([t, v]) => fmt(t) + " " + v).join(", ") : "";
  const hv = Object.entries(HV[cur] || {}).sort();
  document.getElementById("hrv").textContent = hv.length ? "HRV (higher = more relaxed): " + hv.map(([t, v]) => fmt(t) + " " + v + " ms").join(", ") : "";
  const stp = (ST[cur] || {}), sN = stp.steps_total || Object.values(stp.steps || {}).reduce((a, b) => a + b, 0), dN = stp.distance_total || Object.values(stp.distance || {}).reduce((a, b) => a + b, 0);
  document.getElementById("steps").textContent = sN ? `Walking: ${Math.round(sN).toLocaleString()} steps` + (dN ? `, ${dN.toFixed(1)} mi` : "") : "";
  document.getElementById("wx").textContent = temps.length ? `Fort Wayne weather: ${Math.min(...temps)} to ${Math.max(...temps)}°F` + (rain > 0.2 ? `, rain ${(rain / 25.4).toFixed(2)} in` : ", dry") : "";
  const W = 700, H = 460, L = 52, R = 14, T = 16, B = 40, yMin = 40, yMax = Math.max(160, ...vals) + 5;
  const ms0 = pts.length ? Math.floor(mins(pts[0][0]) / 60) * 60 : 0, ms1 = pts.length ? Math.ceil((mins(pts[pts.length - 1][0]) + 1) / 60) * 60 : 1440;
  const x = t => L + ((mins(t) - ms0) / (ms1 - ms0)) * (W - L - R), y = v => T + (1 - (v - yMin) / (yMax - yMin)) * (H - T - B);
  let s = `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Heart rate for ${nice(cur)}">`;
  for (let v = 60; v <= yMax; v += 20) s += `<line x1="${L}" x2="${W - R}" y1="${y(v)}" y2="${y(v)}" stroke="var(--rule)"/><text x="${L - 6}" y="${y(v) + 4}" font-size="20" text-anchor="end" fill="var(--muted)">${v}</text>`;
  const span = (ms1 - ms0) / 60, step = span > 12 ? 4 : span > 6 ? 2 : 1;
  for (let h = ms0 / 60; h <= ms1 / 60; h += step) s += `<text x="${L + ((h * 60 - ms0) / (ms1 - ms0)) * (W - L - R)}" y="${H - 10}" font-size="20" text-anchor="middle" fill="var(--muted)">${(h % 12 || 12) + (h % 24 < 12 ? "a" : "p")}</text>`;
  (M[cur] || []).forEach(([t]) => s += `<line x1="${x(t)}" x2="${x(t)}" y1="${T}" y2="${H - B}" stroke="var(--mark)" stroke-dasharray="3 4"/>`);
  const segs = []; pts.forEach((p, i) => { if (!i || mins(p[0]) - mins(pts[i - 1][0]) > 60) segs.push([]); segs[segs.length - 1].push(p); });
  segs.forEach(g => s += `<polyline fill="none" stroke="var(--accent)" stroke-width="3" stroke-linejoin="round" points="${g.map(p => x(p[0]) + "," + y(p[1])).join(" ")}"/>`);
  pts.forEach(p => s += `<circle cx="${x(p[0])}" cy="${y(p[1])}" r="3" fill="var(--accent)"/>`);
  s += `<rect id="hit" x="${L}" y="${T}" width="${W - L - R}" height="${H - T - B}" fill="transparent"/><circle id="dot" r="8" fill="var(--accent)" stroke="var(--card)" stroke-width="2" style="display:none"/></svg>`;
  document.getElementById("chart").innerHTML = s;
  const svg = document.querySelector("#chart svg"), dot = document.getElementById("dot"), tip = document.getElementById("tip");
  const pick = e => {
    if (!pts.length) return;
    const r = svg.getBoundingClientRect(), cx = ((e.touches ? e.touches[0].clientX : e.clientX) - r.left) * W / r.width;
    const p = pts.reduce((a, q) => Math.abs(x(q[0]) - cx) < Math.abs(x(a[0]) - cx) ? q : a);
    dot.setAttribute("cx", x(p[0])); dot.setAttribute("cy", y(p[1])); dot.style.display = "";
    const near = (M[cur] || []).find(([t]) => Math.abs(mins(t) - mins(p[0])) <= 15);
    const w = (WX[cur] || {})[p[0].slice(0, 2)];
    tip.textContent = `${fmt(p[0])}: ${p[1]} bpm` + (w ? `, ${w[0]}°F` : "") + (near ? ` (near: ${near[1]})` : "");
  };
  ["mousemove", "touchstart", "touchmove"].forEach(ev => svg.addEventListener(ev, pick, { passive: true }));
  const ms = M[cur] || [];
  document.getElementById("moments").innerHTML = ms.length ? ms.map(([t, n]) => `<li><time>${fmt(t)}</time><span>${n.replace(/</g, "&lt;")}</span></li>`).join("") : `<li><span style="color:var(--muted)">Nothing logged for this day yet.</span></li>`;
}
document.getElementById("days").innerHTML = days.map(d => `<button type="button" data-d="${d}">${nice(d)}</button>`).join("");
document.querySelectorAll("#days button").forEach(b => b.onclick = () => { cur = b.dataset.d; draw(); });
draw();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
