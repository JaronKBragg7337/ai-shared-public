// Heartbeat Map Briefing - the scene. Everything on screen is a pure function of time:
//   await window.setup(board, {w, h, wide})  -> { duration, stops:[{id,start,hero}] }
//   window.draw(t)                            -> draws the frame for second t (no clocks, no CSS transitions)
// Globe: NASA Blue Marble (public domain). Borders: Natural Earth 50m (public domain). No photos, seals or logos.
import * as THREE from "./vendor/three.module.min.js";

const D2R = Math.PI / 180;
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, s) => a + (b - a) * s;
const ease = s => { s = clamp(s); return s < .5 ? 4 * s * s * s : 1 - Math.pow(-2 * s + 2, 3) / 2; };
const easeOut = s => 1 - Math.pow(1 - clamp(s), 3);
const ramp = (t, a, b) => clamp((t - a) / (b - a));
// lat/lon -> unit vector matching THREE.SphereGeometry's UVs with an equirectangular texture
const dir = (lat, lon) => { const a = lat * D2R, o = lon * D2R, c = Math.cos(a); return [c * Math.cos(o), Math.sin(a), -c * Math.sin(o)]; };
const toLatLon = v => [Math.asin(clamp(v[1], -1, 1)) / D2R, Math.atan2(-v[2], v[0]) / D2R];
const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2];
const norm = v => { const l = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / l, v[1] / l, v[2] / l]; };
const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
function slerp(a, b, s) {
  const d = clamp(dot(a, b), -1, 1), th = Math.acos(d);
  if (th < 1e-5) return a.slice();
  const k1 = Math.sin((1 - s) * th) / Math.sin(th), k2 = Math.sin(s * th) / Math.sin(th);
  return [a[0] * k1 + b[0] * k2, a[1] * k1 + b[1] * k2, a[2] * k1 + b[2] * k2];
}

const TONES = { amber: [240, 150, 60], ember: [255, 91, 58], cream: [255, 240, 214] };
const rgba = (tone, a) => { const c = TONES[tone] || TONES.amber; return `rgba(${c[0]},${c[1]},${c[2]},${a})`; };

const ICONS = { // simple neutral line icons, 48x48
  ship: '<path d="M8 30h32l-4 9H12z"/><path d="M14 30V20h20v10M24 20V9M24 9l8 5"/>',
  shield: '<path d="M24 6l15 6v11c0 10-6.5 16-15 19C15.500 39 9 33 9 23V12z"/><path d="M17 24l5 5 9-10"/>',
  flame: '<path d="M24 5c2 8 11 12 11 23a11 11 0 01-22 0c0-5 3-8 5-11 1 4 3 5 4 5-1-6 0-12 2-17z"/>',
  alert: '<path d="M24 7l19 33H5z"/><path d="M24 19v11M24 35v1"/>',
  pulse: '<path d="M4 26h9l4-12 7 24 6-18 3 6h11"/>',
  target: '<circle cx="24" cy="24" r="16"/><circle cx="24" cy="24" r="6"/><path d="M24 3v8M24 37v8M3 24h8M37 24h8"/>',
  pin: '<path d="M24 43s14-13 14-23a14 14 0 00-28 0c0 10 14 23 14 23z"/><circle cx="24" cy="20" r="5"/>',
  doc: '<path d="M12 5h17l8 8v30H12z"/><path d="M29 5v8h8M18 23h13M18 30h13"/>',
  plane: '<path d="M43 8L5 22l14 5 5 14z"/><path d="M19 27l10-8"/>',
  bolt: '<path d="M27 4L10 27h12l-2 17 18-24H26z"/>',
  drop: '<path d="M24 5s13 14 13 24a13 13 0 01-26 0C11 19 24 5 24 5z"/>',
  lock: '<rect x="10" y="21" width="28" height="21" rx="3"/><path d="M16 21v-6a8 8 0 0116 0v6"/>',
};
const icon = n => `<svg viewBox="0 0 48 48" fill="none" stroke="#f0963c" stroke-width="3" stroke-linejoin="round" stroke-linecap="round">${ICONS[n] || ICONS.pin}</svg>`;
const FLAGS = { // stripe flags only (no emblems); anything else gets no flag
  UA: ["h", "#2f6fd0", "#f5cf2a"], PL: ["h", "#f4f4f4", "#d4213d"], NL: ["h", "#ae1c28", "#f4f4f4", "#21468b"], DE: ["h", "#111", "#d00", "#fc0"],
  ID: ["h", "#d4213d", "#f4f4f4"], FR: ["v", "#21468b", "#f4f4f4", "#d4213d"], IT: ["v", "#1a9148", "#f4f4f4", "#d4213d"], IE: ["v", "#169b62", "#f4f4f4", "#ff883e"],
  RU: ["h", "#f4f4f4", "#1c3578", "#d52b1e"], EE: ["h", "#3a75c4", "#111", "#f4f4f4"], LT: ["h", "#fdb913", "#006a44", "#c1272d"], AT: ["h", "#d4213d", "#f4f4f4", "#d4213d"],
  HU: ["h", "#cd2a3e", "#f4f4f4", "#436f4d"], YE: ["h", "#ce1126", "#f4f4f4", "#111"], BE: ["v", "#111", "#fdda24", "#ef3340"], RO: ["v", "#002b7f", "#fcd116", "#ce1126"],
};
const flag = c => { const f = FLAGS[c]; return f ? `<span class="flag ${f[0]}">${f.slice(1).map(x => `<i style="background:${x}"></i>`).join("")}</span>` : ""; };
const LOGO = `<svg viewBox="0 0 512 512"><rect width="512" height="512" rx="112" fill="#000"/><g fill="#fff"><rect x="92" y="104" width="68" height="304" rx="6"/><rect x="352" y="104" width="68" height="304" rx="6"/></g><path d="M150 256H222L246 150L274 362L294 256H362" fill="none" stroke="#fff" stroke-width="28" stroke-linejoin="round"/></svg>`;
const esc = s => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;");
const mark = s => esc(s).replace(/\*([^*]+)\*/g, "<em>$1</em>");

let W, H, WIDE, S, renderer, scene, camera, globeMat, fx, ctx, board, countries, byA3 = {}, T = {}, ui = {};

window.setup = async function (b, opts) {
  board = b; W = opts.w; H = opts.h; WIDE = !!opts.wide; S = WIDE ? H / 1080 : W / 1080;
  const stage = document.getElementById("stage");
  stage.style.width = W + "px"; stage.style.height = H + "px";
  const glc = document.getElementById("gl"); fx = document.getElementById("fx");
  glc.width = fx.width = W; glc.height = fx.height = H; ctx = fx.getContext("2d");
  const uiEl = document.getElementById("ui");
  uiEl.style.width = (W / S) + "px"; uiEl.style.height = (H / S) + "px"; uiEl.style.transform = `scale(${S})`; uiEl.style.transformOrigin = "0 0"; uiEl.style.inset = "auto";
  if (WIDE) uiEl.classList.add("wide");

  renderer = new THREE.WebGLRenderer({ canvas: glc, antialias: true, preserveDrawingBuffer: true, powerPreference: "high-performance" });
  renderer.setPixelRatio(1); renderer.setSize(W, H, false); renderer.setClearColor(0x050607, 1);
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(34, W / H, 0.01, 50);
  const gl = renderer.getContext(), maxTex = gl.getParameter(gl.MAX_TEXTURE_SIZE);
  const texFile = (maxTex >= 16384 && !opts.lowTex) ? "vendor/earth_16k.jpg" : "vendor/earth_8k.jpg";
  const tex = await new THREE.TextureLoader().loadAsync(texFile);
  tex.colorSpace = THREE.NoColorSpace; tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
  tex.wrapS = THREE.RepeatWrapping; tex.generateMipmaps = true; tex.minFilter = THREE.LinearMipmapLinearFilter;
  globeMat = new THREE.ShaderMaterial({
    uniforms: { map: { value: tex }, px: { value: new THREE.Vector2(1 / tex.image.width, 1 / tex.image.height) } },
    vertexShader: `varying vec2 vUv; varying vec3 vN; varying vec3 vP;
      void main(){ vUv=uv; vN=normalize(normal); vP=position; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }`,
    fragmentShader: `uniform sampler2D map; uniform vec2 px; varying vec2 vUv; varying vec3 vN; varying vec3 vP;
      void main(){
        vec3 c = texture2D(map, vUv).rgb;
        // gentle unsharp mask so close landings keep some bite
        vec3 bl = (texture2D(map, vUv+vec2(px.x*1.5,0.)).rgb + texture2D(map, vUv-vec2(px.x*1.5,0.)).rgb + texture2D(map, vUv+vec2(0.,px.y*1.5)).rgb + texture2D(map, vUv-vec2(0.,px.y*1.5)).rgb)*0.25;
        c = clamp(c + (c-bl)*0.9, 0., 1.);
        float lum = dot(c, vec3(.299,.587,.114));
        float ocean = smoothstep(0.015, 0.075, c.b - max(c.r, c.g*0.82)) * (1. - smoothstep(.30,.55,lum));
        // land: warm, muted, a little darker - our grade, the map is a stage for the type
        vec3 land = mix(vec3(lum), c, 0.62);
        land = pow(land, vec3(0.92)) * vec3(1.06, 0.97, 0.80) * 0.82;
        land = mix(land, vec3(0.62,0.60,0.56), smoothstep(.62,.95,lum)*0.75);   // snow and ice stay soft, not white
        vec3 sea = mix(vec3(0.016,0.030,0.046), vec3(0.050,0.092,0.128), smoothstep(0.02,0.30,lum));
        vec3 col = mix(land, sea, ocean);
        vec3 V = normalize(cameraPosition - vP);
        float ndv = clamp(dot(vN, V), 0., 1.);
        col *= mix(0.50, 1.0, pow(ndv, 0.55));
        col += vec3(0.30,0.42,0.60) * pow(1.-ndv, 3.2) * 0.75;
        gl_FragColor = vec4(col, 1.);
      }`,
  });
  scene.add(new THREE.Mesh(new THREE.SphereGeometry(1, 256, 128), globeMat));
  // atmosphere halo (back side of a slightly larger sphere)
  scene.add(new THREE.Mesh(new THREE.SphereGeometry(1.045, 96, 48), new THREE.ShaderMaterial({
    side: THREE.BackSide, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    vertexShader: `varying vec3 vN; varying vec3 vP; void main(){ vN=normalize(normal); vP=position; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }`,
    fragmentShader: `varying vec3 vN; varying vec3 vP; void main(){ vec3 V=normalize(cameraPosition-vP); float f=pow(clamp(dot(-vN,V)*2.2,0.,1.),2.4); gl_FragColor=vec4(vec3(0.34,0.50,0.78)*f*0.9, f); }`,
  })));
  // a quiet star field (seeded, so every run is identical)
  { let s = 7; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647; const p = [];
    for (let i = 0; i < 1400; i++) { const v = norm([rnd() * 2 - 1, rnd() * 2 - 1, rnd() * 2 - 1]); p.push(v[0] * 30, v[1] * 30, v[2] * 30); }
    const g = new THREE.BufferGeometry(); g.setAttribute("position", new THREE.Float32BufferAttribute(p, 3));
    scene.add(new THREE.Points(g, new THREE.PointsMaterial({ color: 0xfff0d8, size: 1.6, sizeAttenuation: false, transparent: true, opacity: .55 }))); }

  // borders -> unit vectors
  countries = await (await fetch("vendor/countries.json")).json();
  for (const c of countries) {
    c.rings = c.r.map(r => { const f = new Float32Array(r.length * 3); let m = [0, 0, 0];
      r.forEach((p, i) => { const v = dir(p[1], p[0]); f[i * 3] = v[0]; f[i * 3 + 1] = v[1]; f[i * 3 + 2] = v[2]; m[0] += v[0]; m[1] += v[1]; m[2] += v[2]; });
      m = norm(m); let rad = 0; for (let i = 0; i < r.length; i++) rad = Math.max(rad, Math.acos(clamp(f[i * 3] * m[0] + f[i * 3 + 1] * m[1] + f[i * 3 + 2] * m[2], -1, 1)));
      return { f, n: r.length, m, rad }; });
    c.rings.sort((a, b) => b.n - a.n); delete c.r; byA3[c.a] = c;
  }
  await document.fonts.ready;
  buildTimeline(); buildUI();
  window.draw(0);
  return { duration: T.total, texture: texFile, stops: T.stops.map(s => ({ id: s.id, start: s.t0, hero: s.t0 + s.move + Math.min(s.dur - s.move - .6, (s.cards?.[0]?.at ?? 1.6) + 1.4) })), end: T.endT0 };
};

// ---------- timeline + camera ----------
function buildTimeline() {
  const st = board.stops, intro = board.intro ?? 3.6, endDur = board.end ?? 5.2;
  const first = st[0].cam;
  let prev = { lat: 18, lon: first.lon - 46, alt: 2.7, tilt: 0 };
  T.introCam = { ...prev }; T.introCam0 = { lat: 18, lon: first.lon - 64, alt: 3.0, tilt: 0 };
  let t = intro; T.stops = [];
  for (const s of st) {
    const to = { lat: s.cam.lat, lon: s.cam.lon, alt: s.cam.alt ?? .7, tilt: s.cam.tilt ?? 9 };
    const ang = Math.acos(clamp(dot(dir(prev.lat, prev.lon), dir(to.lat, to.lon)), -1, 1));
    const move = s.move ?? clamp(1.5 + ang * 1.25, 1.6, 3.0);
    const e = { ...s, t0: t, move, from: prev, to, ang, bump: Math.max(0, Math.min(1.5, ang * 1.05) - Math.max(0, prev.alt - 1) * .9) };
    // where the slow drift leaves the camera at the end of this stop
    e.endState = { lat: to.lat, lon: to.lon + .5, alt: to.alt * .94, tilt: to.tilt };
    T.stops.push(e); prev = e.endState; t += s.dur;
  }
  T.endT0 = t; T.endFrom = prev; T.total = t + endDur; T.intro = intro; T.endDur = endDur;
}
function camState(t) {
  if (t < T.intro) { const s = t / T.intro; return { lat: 18, lon: lerp(T.introCam0.lon, T.introCam.lon, s), alt: lerp(T.introCam0.alt, T.introCam.alt, easeOut(s)), tilt: 0 }; }
  if (t >= T.endT0) { const s = ease((t - T.endT0) / T.endDur * 1.1), f = T.endFrom; return { lat: lerp(f.lat, 16, s), lon: f.lon + 30 * s, alt: lerp(f.alt, 2.6, s), tilt: lerp(f.tilt, 0, s) }; }
  let e = T.stops[0]; for (const x of T.stops) if (t >= x.t0) e = x;
  const lt = t - e.t0;
  if (lt < e.move) {
    const s = ease(lt / e.move), v = slerp(dir(e.from.lat, e.from.lon), dir(e.to.lat, e.to.lon), s), ll = toLatLon(v);
    return { lat: ll[0], lon: ll[1], alt: lerp(e.from.alt, e.to.alt, s) + e.bump * Math.pow(Math.sin(Math.PI * s), 1.4), tilt: lerp(e.from.tilt, e.to.tilt, s) };
  }
  const h = (lt - e.move) / Math.max(.01, e.dur - e.move), d = 1 - Math.pow(1 - h, 1.6);
  return { lat: e.to.lat, lon: e.to.lon + .5 * h, alt: e.to.alt * (1 - .06 * (h * .6 + d * .4)), tilt: e.to.tilt };
}
let M = null, CP = [0, 0, 1];
function applyCam(c) {
  const tgt = dir(c.lat, c.lon), cp = dir(c.lat - c.tilt, c.lon), r = 1 + c.alt;
  camera.position.set(cp[0] * r, cp[1] * r, cp[2] * r); camera.up.set(0, 1, 0);
  // close-up: look at the place itself; far away: look at the planet's centre
  const k = clamp((c.alt - 1.2) / 1.0); camera.lookAt(tgt[0] * (1 - k), tgt[1] * (1 - k), tgt[2] * (1 - k));
  // place the landing point a little below centre (vertical) or right of centre (wide) so the type has room
  const off = (1 - k); if (WIDE) camera.setViewOffset(W, H, -W * .17 * off, -H * .02 * off, W, H); else camera.setViewOffset(W, H, 0, H * .004 * off, W, H);
  camera.updateMatrixWorld(true); camera.updateProjectionMatrix();
  M = new THREE.Matrix4().multiplyMatrices(camera.projectionMatrix, camera.matrixWorldInverse).elements;
  CP = [camera.position.x, camera.position.y, camera.position.z];
}
// project a point (optionally lifted above the surface). returns null when behind the horizon
function proj(x, y, z, lift = 0) {
  if (lift <= 0 && x * CP[0] + y * CP[1] + z * CP[2] < 1.0) return null;
  const w = M[3] * x + M[7] * y + M[11] * z + M[15]; if (w <= 0) return null;
  return [((M[0] * x + M[4] * y + M[8] * z + M[12]) / w * .5 + .5) * W, (1 - ((M[1] * x + M[5] * y + M[9] * z + M[13]) / w * .5 + .5)) * H];
}
const projLL = (lat, lon) => { const v = dir(lat, lon); return proj(v[0], v[1], v[2]); };

// ---------- 2D map layer ----------
function ringPath(ring, wantLen) {
  const f = ring.f; let pen = false, all = true, len = 0, px = 0, py = 0;
  ctx.beginPath();
  for (let i = 0; i < ring.n; i++) {
    const p = proj(f[i * 3], f[i * 3 + 1], f[i * 3 + 2]);
    if (!p) { pen = false; all = false; continue; }
    if (pen) { ctx.lineTo(p[0], p[1]); if (wantLen) len += Math.hypot(p[0] - px, p[1] - py); } else { ctx.moveTo(p[0], p[1]); pen = true; }
    px = p[0]; py = p[1];
  }
  return { all, len };
}
function ringOnScreen(ring) {
  if (ring.m[0] * CP[0] + ring.m[1] * CP[1] + ring.m[2] * CP[2] < Math.cos(Math.min(Math.PI, Math.acos(1 / Math.hypot(...CP)) + ring.rad)) * Math.hypot(...CP) - 1e-6) return false;
  const p = proj(ring.m[0], ring.m[1], ring.m[2]); if (!p) return true;
  const span = ring.rad / Math.max(.05, Math.hypot(...CP) - 1) * H * 1.7 + 200;
  return p[0] > -span && p[0] < W + span && p[1] > -span && p[1] < H + span;
}
function drawBorders(alpha) {
  if (alpha <= 0) return;
  ctx.lineWidth = 1.5 * S; ctx.strokeStyle = `rgba(255,238,210,${.30 * alpha})`; ctx.lineJoin = "round";
  for (const c of countries) for (const r of c.rings) { if (r.n < 6 || !ringOnScreen(r)) continue; ringPath(r); ctx.stroke(); }
}
function drawHighlight(h, a, t) {
  const c = byA3[h.a]; if (!c || a <= 0) return;
  const tone = h.tone || "amber";
  c.rings.forEach((r, k) => {
    if (!ringOnScreen(r)) return;
    const { all, len } = ringPath(r, k === 0);
    if (all) { ctx.closePath(); ctx.fillStyle = rgba(tone, .13 * a); ctx.fill(); }
    ctx.save();
    ctx.shadowColor = rgba(tone, .95 * a); ctx.shadowBlur = 26 * S; ctx.strokeStyle = rgba(tone, .95 * a); ctx.lineWidth = 3.4 * S; ctx.stroke();
    ctx.shadowBlur = 8 * S; ctx.strokeStyle = `rgba(255,248,234,${.55 * a})`; ctx.lineWidth = 1.3 * S; ctx.stroke();
    if (k === 0 && len > 200) { // a bright spark that keeps travelling the outline
      const seg = Math.min(len * .12, 240 * S);
      ctx.setLineDash([seg, len - seg]); ctx.lineDashOffset = -((t * .11) % 1) * len;
      ctx.shadowBlur = 22 * S; ctx.shadowColor = "rgba(255,250,240,.9)"; ctx.strokeStyle = `rgba(255,252,244,${.9 * a})`; ctx.lineWidth = 4 * S; ctx.stroke();
    }
    ctx.restore();
  });
}
function mapLabel(text, lat, lon, a, size = 30, tone) {
  const p = projLL(lat, lon); if (!p || a <= 0) return;
  ctx.save(); ctx.font = `700 ${size * S}px Bahnschrift, "Segoe UI", sans-serif`; ctx.letterSpacing = `${size * .22 * S}px`; ctx.textAlign = "center"; ctx.textBaseline = "middle";
  ctx.shadowColor = "rgba(0,0,0,.95)"; ctx.shadowBlur = 12 * S; ctx.fillStyle = tone ? rgba(tone, .95 * a) : `rgba(255,244,226,${.62 * a})`;
  ctx.fillText(text.toUpperCase(), p[0], p[1]); ctx.fillText(text.toUpperCase(), p[0], p[1]); ctx.restore();
}
function geoCircle(lat, lon, km, n = 96) {
  const c = dir(lat, lon), rho = km / 6371, e1 = norm(cross(c, Math.abs(c[1]) > .9 ? [1, 0, 0] : [0, 1, 0])), e2 = cross(c, e1), pts = [];
  for (let i = 0; i <= n; i++) { const th = i / n * Math.PI * 2, cs = Math.cos(rho), sn = Math.sin(rho);
    pts.push(proj(c[0] * cs + (e1[0] * Math.cos(th) + e2[0] * Math.sin(th)) * sn, c[1] * cs + (e1[1] * Math.cos(th) + e2[1] * Math.sin(th)) * sn, c[2] * cs + (e1[2] * Math.cos(th) + e2[2] * Math.sin(th)) * sn)); }
  return pts;
}
function strokePts(pts) { ctx.beginPath(); let pen = false; for (const p of pts) { if (!p) { pen = false; continue; } if (pen) ctx.lineTo(p[0], p[1]); else { ctx.moveTo(p[0], p[1]); pen = true; } } ctx.stroke(); }
function drawMarker(m, a, lt, t) {
  const p = projLL(m.lat, m.lon); if (!p || a <= 0) return;
  const kind = m.kind || "pin", tone = m.tone || (kind === "strike" || kind === "fire" ? "ember" : kind === "pin" ? "cream" : "amber");
  const pop = easeOut(ramp(lt, m.at ?? 0, (m.at ?? 0) + .5)); if (pop <= 0) return; a *= pop;
  ctx.save();
  if (m.ringKm) { // dashed ring drawn on the globe itself, slowly turning
    const pts = geoCircle(m.lat, m.lon, m.ringKm * (0.6 + 0.4 * pop));
    ctx.setLineDash([14 * S, 12 * S]); ctx.lineDashOffset = -t * 16 * S; ctx.lineWidth = 2.6 * S; ctx.strokeStyle = rgba(tone, .85 * a); ctx.shadowColor = rgba(tone, .8 * a); ctx.shadowBlur = 12 * S; strokePts(pts);
    ctx.setLineDash([]);
    if (kind === "quake") for (let k = 0; k < 3; k++) { const ph = (t * .45 + k / 3) % 1; ctx.lineWidth = 2 * S; ctx.strokeStyle = rgba(tone, (1 - ph) * .7 * a); strokePts(geoCircle(m.lat, m.lon, m.ringKm * ph)); }
  }
  if (kind === "strike" || kind === "fire") for (let k = 0; k < 2; k++) { const ph = (t * .7 + k / 2) % 1; ctx.beginPath(); ctx.arc(p[0], p[1], (10 + ph * 46) * S, 0, 7); ctx.lineWidth = 2.6 * S; ctx.strokeStyle = rgba(tone, (1 - ph) * .9 * a); ctx.stroke(); }
  ctx.shadowColor = rgba(tone, a); ctx.shadowBlur = 22 * S;
  ctx.beginPath(); ctx.arc(p[0], p[1], 9.500 * S * pop, 0, 7); ctx.fillStyle = rgba(tone, a); ctx.fill();
  ctx.shadowBlur = 0; ctx.beginPath(); ctx.arc(p[0], p[1], 4 * S, 0, 7); ctx.fillStyle = `rgba(255,252,244,${a})`; ctx.fill();
  if (kind === "pin") { ctx.beginPath(); ctx.arc(p[0], p[1], 17 * S, 0, 7); ctx.lineWidth = 2 * S; ctx.strokeStyle = `rgba(255,244,226,${.7 * a})`; ctx.stroke(); }
  if (m.label) { // label with a short leader; side = right | left | top | bottom
    const side = m.side || "right", L = 34 * S, sub = 25 * S;
    let ringPx = 0; if (m.ringKm) { const q = geoCircle(m.lat, m.lon, m.ringKm, 8); for (const z of q) if (z) ringPx = Math.max(ringPx, Math.hypot(z[0] - p[0], z[1] - p[1])); }
    const gap = Math.max(30 * S, ringPx + 16 * S);
    let x = p[0], y = p[1], al = "left";
    if (side === "right") x += gap; else if (side === "left") { x -= gap; al = "right"; } else { al = "center"; y += side === "top" ? -(gap + (m.sub ? 40 : 14) * S) : gap + 16 * S; }
    ctx.textAlign = al; ctx.textBaseline = "middle"; ctx.shadowColor = "rgba(0,0,0,1)"; ctx.shadowBlur = 14 * S;
    ctx.font = `700 ${L}px "Segoe UI", sans-serif`; ctx.fillStyle = `rgba(255,248,234,${a})`;
    const yy = m.sub ? y - 15 * S : y; ctx.fillText(m.label, x, yy); ctx.fillText(m.label, x, yy);
    if (m.sub) { ctx.font = `600 ${sub}px "Segoe UI", sans-serif`; ctx.fillStyle = `rgba(255,236,208,${.82 * a})`; ctx.fillText(m.sub, x, y + 19 * S); ctx.fillText(m.sub, x, y + 19 * S); }
  }
  ctx.restore();
}
function drawArc(ar, a, lt) {
  const p = ease(ramp(lt, ar.at ?? 0, (ar.at ?? 0) + (ar.time ?? 1.6))); if (p <= 0 || a <= 0) return;
  const A = dir(ar.from[0], ar.from[1]), B = dir(ar.to[0], ar.to[1]), ang = Math.acos(clamp(dot(A, B), -1, 1)), lift = ang * .22, pts = [], n = 80;
  for (let i = 0; i <= n * p; i++) { const s = i / n, v = slerp(A, B, s), r = 1 + lift * Math.sin(Math.PI * s); pts.push(proj(v[0] * r, v[1] * r, v[2] * r, 1)); }
  const tone = ar.tone || "ember";
  ctx.save(); ctx.lineCap = "round"; ctx.setLineDash([16 * S, 13 * S]); ctx.lineWidth = 4.6 * S; ctx.strokeStyle = rgba(tone, .95 * a); ctx.shadowColor = rgba(tone, .9 * a); ctx.shadowBlur = 16 * S; strokePts(pts);
  const h = pts[pts.length - 1]; if (h) { ctx.setLineDash([]); ctx.beginPath(); ctx.arc(h[0], h[1], 7 * S, 0, 7); ctx.fillStyle = `rgba(255,250,240,${a})`; ctx.fill(); }
  ctx.restore();
}
function shade(k) { // vignette + reading gradients; k = extra darkening (intro / end card)
  let g = ctx.createLinearGradient(0, 0, 0, H);
  if (WIDE) { g = ctx.createLinearGradient(0, 0, W, 0); g.addColorStop(0, "rgba(5,5,6,.80)"); g.addColorStop(.42, "rgba(5,5,6,.34)"); g.addColorStop(.62, "rgba(5,5,6,0)"); }
  else { g.addColorStop(0, "rgba(5,5,6,.88)"); g.addColorStop(.17, "rgba(5,5,6,.66)"); g.addColorStop(.36, "rgba(5,5,6,.10)"); g.addColorStop(.58, "rgba(5,5,6,0)"); g.addColorStop(.80, "rgba(5,5,6,.46)"); g.addColorStop(1, "rgba(5,5,6,.90)"); }
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  const v = ctx.createRadialGradient(W / 2, H / 2, Math.min(W, H) * .35, W / 2, H / 2, Math.hypot(W, H) * .62);
  v.addColorStop(0, "rgba(0,0,0,0)"); v.addColorStop(1, "rgba(0,0,0,.55)"); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H);
  if (k > 0) { ctx.fillStyle = `rgba(5,5,6,${k})`; ctx.fillRect(0, 0, W, H); }
}

// ---------- DOM layer ----------
function el(html) { const d = document.createElement("div"); d.innerHTML = html.trim(); return d.firstChild; }
function buildUI() {
  const root = document.getElementById("ui"); root.innerHTML = "";
  ui.bug = el(`<div id="bug" class="abs">${LOGO}<div><div class="t1">HEARTBEAT NEWS</div><div class="t2">MAP BRIEFING · ${esc(board.shortDate || board.date)}</div></div></div>`);
  ui.pips = el(`<div id="pips" class="abs">${T.stops.map(() => "<i><b></b></i>").join("")}</div>`);
  root.append(ui.bug, ui.pips);
  ui.stops = T.stops.map((s, i) => {
    const o = { cards: [] };
    if (!s.cont) {
      o.head = el(`<div class="head abs"><div class="bar"></div><div class="tag"><span class="n">${String(s.num ?? i + 1).padStart(2, "0")}</span><span>${esc(s.tag)}</span></div><div class="hl${s.headline.length > 30 ? " long" : ""}">${esc(s.headline)}</div><div class="sub">${mark(s.sub || "")}</div></div>`);
      root.append(o.head);
    }
    (s.cards || []).forEach(c => {
      const k = c.type === "quote"
        ? el(`<div class="card quote abs"><div class="q">&ldquo;</div><div class="x">${mark(c.text)}</div><div class="who">${flag(c.flag)}<div><div class="nm">${esc(c.who || "")}</div><div class="rl">${esc(c.role || "")}</div></div></div></div>`)
        : el(`<div class="card abs"><div class="k">${icon(c.icon)}<span>${esc(c.kicker || "")}</span></div><div class="x">${mark(c.text)}</div></div>`);
      root.append(k); o.cards.push(k);
    });
    if (s.sources) { o.src = el(`<div class="src abs">Sources in today's show: ${esc(s.sources)}</div>`); root.append(o.src); }
    return o;
  });
  ui.intro = el(`<div id="intro" class="abs"><div class="k">HEARTBEAT NEWS</div><h1>${esc(board.title || "Map Briefing")}</h1><div class="d">${esc(board.longDate || board.date)}</div><div class="f">${T.stops.filter(s => !s.cont).length} STORIES · WHERE THEY HAPPENED</div></div>`);
  ui.end = el(`<div id="end" class="abs">${LOGO}<h2>Heartbeat Observatory</h2><div class="u">heartbeatobservatory.com/news</div><div class="s">The full show, with every source, is on the site.</div><div class="c">EVERY LINE HERE IS FROM TODAY'S HEARTBEAT NEWS<br>MAP: NASA BLUE MARBLE · NATURAL EARTH</div></div>`);
  root.append(ui.intro, ui.end);
}
const show = (e, a, ty = 0) => { if (!e) return; e.style.opacity = a.toFixed(3); e.style.visibility = a <= .001 ? "hidden" : "visible"; e.style.transform = ty ? `translateY(${ty.toFixed(1)}px)` : "none"; };

// ---------- one frame ----------
window.draw = function (t) {
  t = clamp(t, 0, T.total);
  const c = camState(t); applyCam(c); renderer.render(scene, camera);
  ctx.clearRect(0, 0, W, H);
  const inIntro = t < T.intro, inEnd = t >= T.endT0, far = clamp((c.alt - 1.3) / 1.0);
  drawBorders(1 - far * .75);
  T.stops.forEach((s, i) => {
    const lt = t - s.t0, tail = lt - s.dur;            // tail > 0: the next stop has started
    if (lt < 0 || tail > .7) return;
    const a = ramp(lt, s.move * .55, s.move * .55 + .7) * (1 - ramp(tail, 0, .5));
    (s.hi || []).forEach(h => drawHighlight(h, a, t));
    (s.arcs || []).forEach(ar => drawArc(ar, a, lt - s.move));
    (s.labels || []).forEach(l => mapLabel(l.text, l.lat, l.lon, a * (l.a ?? 1), l.size ?? 28, l.tone));
    (s.markers || []).forEach(m => drawMarker(m, a, lt - s.move * .8, t));
  });
  const introA = inIntro ? 1 - ramp(t, T.intro - .7, T.intro) : 0, endA = inEnd ? ramp(t, T.endT0 + .5, T.endT0 + 1.5) : 0;
  shade(inIntro ? .16 * introA : inEnd ? .62 * endA : 0);

  // chrome
  const chrome = (inIntro ? ramp(t, T.intro - .3, T.intro + .5) : 1) * (inEnd ? 1 - ramp(t, T.endT0, T.endT0 + .5) : 1);
  show(ui.bug, chrome); show(ui.pips, chrome);
  [...ui.pips.children].forEach((p, i) => { const s = T.stops[i]; p.firstChild.style.width = (clamp((t - s.t0) / s.dur) * 100).toFixed(1) + "%"; });
  show(ui.intro, inIntro ? ramp(t, .15, .9) * introA : 0, inIntro ? (1 - easeOut(ramp(t, .15, 1.1))) * 40 : 0);
  show(ui.end, endA, (1 - easeOut(ramp(t, T.endT0 + .5, T.endT0 + 1.7))) * 40);

  T.stops.forEach((s, i) => {
    const o = ui.stops[i], lt = t - s.t0;
    // a header lives across its own stop plus any "cont" stops that follow it
    let endT = s.t0 + s.dur; for (let j = i + 1; j < T.stops.length && T.stops[j].cont; j++) endT = T.stops[j].t0 + T.stops[j].dur;
    if (o.head) {
      const inT = s.t0 + s.move * .5, a = ramp(t, inT, inT + .55) * (1 - ramp(t, endT - .05, endT + .4));
      show(o.head, a);
      if (a > 0) {
        const [bar, tag, hl, sub] = o.head.children;
        bar.style.transform = `scaleY(${easeOut(ramp(t, inT, inT + .7)).toFixed(3)})`;
        [tag, hl, sub].forEach((e, k) => { const s2 = ramp(t, inT + .12 + k * .16, inT + .75 + k * .16); e.style.opacity = s2.toFixed(3); e.style.transform = `translateY(${((1 - easeOut(s2)) * 34).toFixed(1)}px)`; });
      }
    }
    const cs = s.cards || [], out = 1 - ramp(lt, s.dur - .05, s.dur + .35);
    cs.forEach((cd, k) => {
      const at = s.move + (cd.at ?? 1.6 + k * 3.2), until = k + 1 < cs.length ? s.move + (cs[k + 1].at ?? 1.6 + (k + 1) * 3.2) - .12 : 1e9;
      const a = ramp(lt, at, at + .5) * (1 - ramp(lt, until - .3, until)) * out;
      show(o.cards[k], lt < 0 ? 0 : a, (1 - easeOut(ramp(lt, at, at + .6))) * 46);
    });
    if (o.src) show(o.src, lt < 0 ? 0 : ramp(lt, s.move + .6, s.move + 1.2) * out);
  });
};
