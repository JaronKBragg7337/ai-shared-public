from pathlib import Path
import re

root = Path('C:/Users/lilli/Projects/heartbeat-observatory')
p = root / 'world3/index.html'
s = p.read_text(encoding='utf-8')
s = s.replace('height:3px; background:rgba(255,255,255,.1)', 'height:8px; background:rgba(255,255,255,.1)')
s = s.replace('  #load h1 { letter-spacing:.3em; }', '''  #load h1 { letter-spacing:.3em; }
  body:not(.dev) .dev-only, body.dev .visitor-only,
  body:not(.dev) .hbs-app[data-id="edit"],
  body:not(.dev) #inspect, body:not(.dev) #editbar,
  body:not(.dev) #orbitbar, body:not(.dev) #tourbar { display:none !important; }
  #load { z-index:100; }
  #load p { max-width:86vw; text-align:center; }''')
s = s.replace('  <h2>ASHGROVE</h2>', '''  <h2>ASHGROVE</h2>
  <div class="visitor-only">
    <p>A walkable town with <span data-town-count>49 founding</span> buildings, residents and pets. New homes can be added as the town grows.</p>
    <p>Walk with <kbd>W</kbd><kbd>A</kbd><kbd>S</kbd><kbd>D</kbd>, look with the mouse, and press <kbd>E</kbd> to use a door or talk to someone. <kbd>Space</kbd> jumps.</p>
    <p>On a phone, drag the left side to walk and the right side to look. Tap Enter when a door or person is within reach.</p>
    <p><kbd>J</kbd> opens town status. The menu holds settings; the phone holds places and messages.</p>
  </div>
  <div class="dev-only">''', 1)
s = s.replace('— 49 in all,', '— 49 founding buildings, plus later growth,')
s = s.replace('</div>\n\n<div id="load">', '  </div>\n</div>\n\n<div id="load">', 1)
s = s.replace('<div class="bar"><i id="loadBar"></i></div>\n  <p id="loadMsg">initialising</p>', '<div class="bar" role="progressbar" aria-label="Loading Ashgrove" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><i id="loadBar"></i></div>\n  <p id="loadMsg" role="status">Loading town files · 0 complete</p>')
s = s.replace('<script>\n/* World 3 shared-world migration.', '''<script>
window.HB_WORLD3 = true;
// Resource completions and finished build stages, never a timer-driven estimate.
window.HBLoading = (() => {
  let completed = 0, current = 0;
  const total = 35;
  function show(p, message) {
    current = Math.max(current, p);
    const percent = Math.round(current * 100);
    document.getElementById("loadBar").style.width = percent + "%";
    document.querySelector("#load .bar").setAttribute("aria-valuenow", percent);
    document.getElementById("loadMsg").textContent = message;
  }
  return {
    resource() { show(0.25 * ++completed / total, `Loaded ${completed} of ${total} town files`); },
    stage(p, message) { show(0.25 + p * 0.75, message); },
    error() { document.getElementById("loadMsg").textContent = "A town file could not load. Reload to try again."; }
  };
})();
// This must also run on a first visit, when there is no saved town to migrate.
try { localStorage.setItem("ashgrove-seen", "1"); } catch (_) {}
/* World 3 shared-world migration.''')
s = re.sub(r'<script src="(town/[^"\n]+|cinema.js[^"\n]*|/shell/shell.js[^"\n]*|destinations.js[^"\n]*|main.js[^"\n]*)"></script>',
           r'<script defer src="\1" onload="HBLoading.resource()" onerror="HBLoading.error()"></script>', s)
count = s.count('onload="HBLoading.resource()"')
s = s.replace('const total = 35;', f'const total = {count};')
for name in ['town/render/main.js', 'town/render/town.js', 'main.js']:
    s = re.sub(r'src="' + re.escape(name) + r'\?v=[^"]+"', f'src="{name}?v=2026-10-28-visitors"', s)
p.write_text(s, encoding='utf-8')
p = root / 'engine/hub/index.html'
s = p.read_text(encoding='utf-8').replace('main.js?v=2026-09-28-holo', 'main.js?v=2026-10-28-visitors')
p.write_text(s, encoding='utf-8')
print(f'Updated loading for {count} deferred scripts')
