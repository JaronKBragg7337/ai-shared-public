// board.mjs - builds a map-briefing storyboard from a Heartbeat News episode with no AI in the loop.
// Used when boards/<date>.json does not exist. Every text line is copied from the episode's own on-screen graphic
// (strap, stat label, stat value), so "reported / claims / not verified" wording comes through untouched.
// It only knows the places in PLACES plus every country name in Natural Earth; a story with no match is skipped.
// A hand/AI-written board (boards/<date>.json, same shape) always wins and looks better: this is the safety net.

const PLACES = { // name -> [lat, lon, country A3, camera height]
  "Khasab": [26.18, 56.25, "OMN", .62], "Hormuz": [26.6, 56.4, "IRN", .7], "Bahrain": [26.07, 50.55, "BHR", .58], "Riyadh": [24.71, 46.68, "SAU", .95], "Mecca": [21.42, 39.83, "SAU", .8],
  "Tehran": [35.69, 51.39, "IRN", .9], "Kharg": [29.24, 50.32, "IRN", .6], "Qeshm": [26.8, 55.9, "IRN", .6], "Gaza": [31.45, 34.4, "PSX", .5], "Gaza City": [31.5, 34.47, "PSX", .5],
  "Jerusalem": [31.78, 35.22, "ISR", .5], "Tel Aviv": [32.08, 34.78, "ISR", .5], "Beirut": [33.89, 35.5, "LBN", .5], "Damascus": [33.51, 36.29, "SYR", .6], "Baghdad": [33.31, 44.37, "IRQ", .8],
  "Basra": [30.5, 47.8, "IRQ", .7], "Sanaa": [15.37, 44.19, "YEM", .8], "Hodeidah": [14.8, 42.95, "YEM", .7], "Doha": [25.29, 51.53, "QAT", .55], "Dubai": [25.2, 55.27, "ARE", .6],
  "Kyiv": [50.45, 30.52, "UKR", .8], "Kryvyi Rih": [47.91, 33.39, "UKR", .8], "Kharkiv": [49.99, 36.23, "UKR", .75], "Odesa": [46.48, 30.72, "UKR", .75], "Lviv": [49.84, 24.03, "UKR", .75],
  "Zaporizhzhia": [47.84, 35.14, "UKR", .75], "Vyshhorod": [50.58, 30.49, "UKR", .75], "Moscow": [55.75, 37.62, "RUS", 1.0], "Kaliningrad": [54.71, 20.51, "RUS", .6], "Gogland": [60.06, 26.98, "FIN", .6],
  "Gulf of Finland": [59.9, 26.0, "FIN", .6], "Warsaw": [52.23, 21.01, "POL", .74], "Nowy Lipowiec": [50.44, 22.84, "POL", .74], "Berlin": [52.52, 13.4, "DEU", .75], "Paris": [48.86, 2.35, "FRA", .8],
  "London": [51.51, -.13, "GBR", .75], "Brussels": [50.85, 4.35, "BEL", .55], "Geneva": [46.2, 6.14, "CHE", .55], "Antalya": [36.9, 30.7, "TUR", .8], "Istanbul": [41.01, 28.98, "TUR", .8],
  "Washington": [38.9, -77.03, "USA", .72], "New York": [40.71, -74.0, "USA", .7], "Seattle": [47.61, -122.33, "USA", .75], "San Francisco": [37.77, -122.42, "USA", .7], "Los Angeles": [34.05, -118.24, "USA", .75],
  "Florida": [28.2, -81.6, "USA", .8], "Texas": [31.0, -99.5, "USA", .95], "California": [36.8, -119.6, "USA", .95], "Virginia": [37.6, -78.6, "USA", .7], "Iowa": [42.0, -93.5, "USA", .75], "Las Vegas": [36.17, -115.14, "USA", .75],
  "Sinaloa": [25.0, -107.5, "MEX", .92], "Mexico City": [19.43, -99.13, "MEX", .9], "Caracas": [10.48, -66.9, "VEN", .8], "Junín": [-11.5, -75.0, "PER", .9], "Lima": [-12.05, -77.04, "PER", .9],
  "Beijing": [39.9, 116.4, "CHN", 1.2], "Taipei": [25.03, 121.57, "TWN", .6], "Taiwan Strait": [24.5, 119.5, "TWN", .7], "Tokyo": [35.68, 139.69, "JPN", .9], "Seoul": [37.57, 126.98, "KOR", .7],
  "Pyongyang": [39.03, 125.75, "PRK", .7], "Jakarta": [-6.2, 106.85, "IDN", 1.2], "Cikande": [-6.21, 106.36, "IDN", 1.2], "Dili": [-8.56, 125.58, "TLS", .9], "Manila": [14.6, 120.98, "PHL", .9],
  "New Delhi": [28.61, 77.21, "IND", 1.2], "Manipur": [24.8, 93.9, "IND", .9], "Kabul": [34.53, 69.17, "AFG", .9], "Islamabad": [33.69, 73.05, "PAK", .9], "Dhaka": [23.81, 90.41, "BGD", .7],
  "Bayelsa": [4.77, 6.07, "NGA", .9], "Lagos": [6.52, 3.38, "NGA", .9], "Al Obeid": [13.18, 30.22, "SDN", 1.0], "Khartoum": [15.5, 32.56, "SDN", 1.0], "Nairobi": [-1.29, 36.82, "KEN", .9],
  "Johannesburg": [-26.2, 28.05, "ZAF", 1.0], "Cairo": [30.04, 31.24, "EGY", .9], "Sydney": [-33.87, 151.21, "AUS", 1.3], "Darwin": [-12.46, 130.84, "AUS", 1.2], "Ottawa": [45.42, -75.7, "CAN", .9],
};
const ALIAS = { "U.S.": "USA", "U.S.A.": "USA", "United States": "USA", "America": "USA", "Britain": "GBR", "U.K.": "GBR", "South Korea": "KOR", "North Korea": "PRK", "Russia": "RUS", "Iran": "IRN", "Syria": "SYR", "Taiwan": "TWN", "Timor-Leste": "TLS", "Congo": "COD", "Turkey": "TUR", "Czech Republic": "CZE", "U.A.E.": "ARE" };
// place words that are really adjectives in a headline ("Mexico captures", "Poland prosecutor") still count: that is the country.

const re = n => new RegExp("(^|[^A-Za-z])" + n.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "(?![A-Za-z])");
const clean = s => String(s || "").replace(/\s+/g, " ").trim();

function hits(text, countries) { // every place we can see in a piece of text: cities first, then countries
  const out = [];
  for (const [n, p] of Object.entries(PLACES)) { const m = re(n).exec(text); if (m) out.push({ i: m.index, name: n, lat: p[0], lon: p[1], a: p[2], alt: p[3], city: true }); }
  const seen = new Set();
  const addC = (n, a3) => { const m = re(n).exec(text); if (!m || seen.has(a3)) return; const c = countries.find(x => x.a === a3); if (!c) return; seen.add(a3);
    const big = c.r.reduce((a, b) => b.length > a.length ? b : a, c.r[0]), lats = big.map(p => p[1]), lons = big.map(p => p[0]);
    const span = Math.max(Math.max(...lats) - Math.min(...lats), (Math.max(...lons) - Math.min(...lons)) * Math.cos(c.c[1] * Math.PI / 180) * 1.6);
    out.push({ i: m.index, name: c.n === "United States of America" ? "United States" : c.n, a: a3, lat: c.c[1], lon: c.c[0], alt: Math.min(1.9, Math.max(.6, span / 17)), city: false, raw: n }); };
  for (const [n, a3] of Object.entries(ALIAS)) addC(n, a3);
  for (const c of countries) for (const n of [c.n, c.l]) if (n && n.length >= 4) addC(n, c.a);
  return out.sort((x, y) => (x.city ? 0 : 1) - (y.city ? 0 : 1) || x.i - y.i || y.name.length - x.name.length);
}
// A stat is "label: value". The value says what happened and usually where. The label is often WHO SAID IT
// ("U.K. maritime agency", "Poland prosecutor"), so a country in a label only counts when the label is just the place.
function findPlace(stat, countries) {
  const label = clean(stat.label), value = clean(stat.value), bare = label.replace(/\s*\(.*?\)\s*/g, "").trim();
  const inLabel = hits(label, countries), inValue = hits(value, countries);
  return inLabel.find(h => h.city) || inValue.find(h => h.city) || inLabel.find(h => !h.city && (bare === h.raw || bare.endsWith(", " + h.raw))) || inValue.find(h => !h.city) || null;
}

// "MISSILES HIT ZELENSKY'S HOMETOWN" -> "Missiles hit Zelensky's hometown", spelling each word the way the episode itself does
function properNouns(ep) {
  const known = {}; let start = true;
  const texts = (ep.segments || []).flatMap(s => [s.headline, s.graphic?.title, ...(s.graphic?.stats || []).flatMap(x => [x.label, x.value]), ...(s.graphic?.bullets || []), ...(s.lines || []).map(l => l.text)]);
  for (const t of texts) { start = true;
    for (const raw of clean(t).split(" ")) {
      const k = raw.replace(/^[^A-Za-z0-9]+|[^A-Za-z0-9.]+$/g, "").replace(/'s$/, ""), lk = k.toLowerCase().replace(/\.$/, "");
      if (k && (/[A-Z]/.test(k.slice(1)) || (/^[A-Z]/.test(k) && !start))) known[lk] = k.replace(/([a-z])\.$/, "$1");
      start = /[.!?:;]["')]?$/.test(raw) && !/^([A-Za-z]\.)+$/.test(raw) || /^[("']$/.test(raw);
    } }
  return known;
}
function sentenceCase(caps, known) {
  if (caps !== caps.toUpperCase()) return caps;   // already mixed case: leave it exactly as written
  return caps.split(" ").map((w, i) => {
    const m = /^([^A-Za-z0-9]*)(.*?)((?:'S)?[^A-Za-z0-9.]*)$/.exec(w), core = m[2], lk = core.toLowerCase().replace(/\.$/, "");
    let v = /^([A-Z]\.){2,}$/.test(core) || /\d/.test(core) ? core : known[lk] ? known[lk] + (core.endsWith(".") && !known[lk].endsWith(".") && /\./.test(known[lk]) ? "." : "") : core.toLowerCase();
    if (i === 0) v = v.charAt(0).toUpperCase() + v.slice(1);
    return m[1] + v + m[3].toLowerCase();
  }).join(" ");
}

export function buildBoard(ep, countries, max = 7) {
  const d = new Date(ep.date + "T12:00:00Z");
  const board = { date: ep.date, auto: true, title: "The day's news, by place",
    shortDate: d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "UTC" }).toUpperCase(),
    longDate: d.toLocaleDateString("en-US", { weekday: "long", month: "long", day: "numeric", year: "numeric", timeZone: "UTC" }), stops: [] };
  const segs = (ep.segments || []).filter(s => ["breaking", "story", "weather"].includes(s.kind) && s.id !== "also-today" && s.graphic?.stats?.length);
  segs.sort((a, b) => (a.kind === "breaking" ? 0 : 1) - (b.kind === "breaking" ? 0 : 1));   // stable: breaking first, then show order
  const used = new Set(), known = properNouns(ep);
  for (const seg of segs) {
    if (board.stops.length >= max) break;
    const stats = seg.graphic.stats;
    let k = -1, place = null;
    for (let i = 0; i < stats.length && !place; i++) { place = findPlace(stats[i], countries); if (place) k = i; }
    if (!place || used.has(place.name)) continue;
    used.add(place.name);
    // the headline must be about the same thing as the stat we are showing: the strap clause that names the place,
    // else the first clause when we show the first stat, else the stat's own label
    const clauses = clean(seg.strap).split(";").map(x => x.trim()), names = [place.name, place.raw, countries.find(c => c.a === place.a)?.n].filter(Boolean).map(x => x.toUpperCase());
    const strap = clauses.find(c => names.some(n => c.toUpperCase().includes(n))) || (k === 0 ? clauses[0] : null);
    const label = clean(stats[k].label), bare = label.replace(/\s*\(.*?\)\s*/g, "").trim();
    const others = (k === 0 || clauses.length === 1) ? stats.filter((_, i) => i !== k).slice(0, 2) : [];   // extra cards only when the whole graphic is one story
    board.stops.push({
      id: seg.id, seg: seg.id, tag: `${clean(seg.graphic.kicker || seg.category)} · ${place.name}`, headline: strap ? sentenceCase(strap, known) : bare,
      sub: strap ? `${label}: ${clean(stats[k].value)}` : clean(stats[k].value) + (label !== bare ? " " + label.slice(bare.length).trim() : ""),
      cam: { lat: place.lat - (place.city ? .3 : 0), lon: place.lon, alt: place.alt }, dur: 6.6 + 2.6 * others.length + (others.length ? 0 : 1.2),
      hi: [{ a: place.a, tone: "amber" }],
      labels: place.city ? [] : [{ text: place.name, lat: place.lat, lon: place.lon }],
      markers: place.city ? [{ lat: place.lat, lon: place.lon, kind: "area", ringKm: Math.round(place.alt * 75), label: place.name, side: "bottom", at: .3 }] : [],
      cards: others.map((x, i) => ({ icon: ["doc", "alert"][i], kicker: clean(x.label), text: clean(x.value), at: 2.4 + i * 2.6 })),
      sources: [...new Set((seg.sources || []).map(x => clean(x.name).split(" (")[0]))].slice(0, 4).join(", "),
    });
  }
  // fly in an order that makes sense on a globe: keep the lead story first, then nearest-neighbour hops
  const out = board.stops.splice(0, 1);
  while (board.stops.length) { const p = out[out.length - 1].cam; let bi = 0, bd = 1e9; board.stops.forEach((s, i) => { const dd = Math.hypot(s.cam.lat - p.lat, ((s.cam.lon - p.lon + 540) % 360 - 180) * Math.cos(p.lat * Math.PI / 180)); if (dd < bd) { bd = dd; bi = i; } }); out.push(...board.stops.splice(bi, 1)); }
  board.stops = out;
  return board;
}
