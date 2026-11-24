# World Printer Lab remake - brief for Fable 5.2 (first run: Sat 11/21, 10:33 PM - Jaron: start now)

## Jaron's words (11/21, 10:24-10:27 PM)
"The 3D printer page might get completely remade too. It's so oldish and I know it can be and look so much better."
"The 3D printer was actually a HUGE thing for me. I wouldn't mind if it was fable that started with it. Also some things weren't as
smooth. So truly I wouldn't mind if it's made in a whole new way. Just realistic as possible. Shapes of every object can be based on
what's easiest to repeat for any asset on flow coming out of printer."

## What it is today
heartbeatobservatory.com/3DPrinterAsset/ - "World Printer Lab v2i" (site repo C:\Users\lilli\Projects\heartbeat-observatory,
folder 3DPrinterAsset/: index.html -> bootstrap.js -> runtime-guards.js -> main.js (109 KB, Three.js), style.css; last touched 10/25).
It prints modular world parts with printer classes, snaps parts by connectors, and keeps a shared sandbox: Supabase table
`placements` + realtime channel `placements-*` (anonymous sign-in). It is the closest living prototype of the worlds' future
Build Mode (state/backlog.json Phase 7: world_props, snap sockets for track/rail/road/fence).

## What Jaron wants
- A complete remake, a whole new way if that's better. Realistic as possible (the site's realism bar). Smooth.
- THE CORE IDEA, his: one repeatable printing FLOW that can make any asset. Every object's shape is designed around what is
  easiest to repeat with the flow coming out of the printer - like a real printer laying material layer by layer along a nozzle
  path. So the printer is not a menu of pre-made models: it is a real process that builds each part from the same repeatable flow,
  and you can watch it happen.
- Phone first (iOS Safari is the real target; check WebKit at 390 px), desktop too (mouse/keyboard).
- Keep what matters: printing world parts, snapping them together, the shared sandbox people can build in. Don't break existing
  `placements` data without a migration path; if the new design needs a new table, add it and keep the old rows readable.
- Keep the old page reachable (for example /3DPrinterAsset/classic/) until the new one is clearly better.

## How to work
- Your own git worktree of the site repo (like Projects/ho-fable-cosmos for The Cosmos); never touch the main checkout,
  never reset --hard/stash there. Ship finished parts with fetch, rebase on origin/main, push HEAD:main. Commits end with
  "Co-Authored-By: Claude Fable 5.2 <<email>>". Check live at phone width after each push.
- Log every part in AI-Shared/projects/printer-remake/BUILD-LOG.md (newest last) with what's not verified.
- No Unreal, no heavy GPU tools, no RunPod. Stop any test server you start.
- STOP by 1:30 AM Fort Wayne time at the latest (the 3 AM news desks share this Claude window), or earlier if your context gets
  long. Jaron expects about an hour. Write a HANDOFF at the end of BUILD-LOG.md and end. A later run continues from it.
