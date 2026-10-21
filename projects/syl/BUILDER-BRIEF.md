# Read this first - every builder on The Cosmos (Jaron, 10/3)

## Where the game is supposed to go
1. `BIBLE-v3.md` (v3.1) - the design. When it is silent, invent - that is welcome - but never contradict it.
2. `DECISIONS.md` - Jaron's decisions, newest first. They override the bible.
3. `WORLD-MAP.md` - the inventory and packages. `REAL-DATA.md` - free real data and its traps (OpenStreetMap and HYG
   are share-alike; WorldClim is non-commercial: avoid; JPL Horizons has no CORS: pre-compute; host our own copies;
   no NASA logo or implied endorsement; keep credits in credits.json).
4. In the game repo: `docs/ADD-A-WORLD.md`, `docs/ADD-A-SHIP.md`, `docs/WORLD-STATE.md`, `README.md`.
5. Builder-only surprises: `SPOILER-opening-for-builders.md` - never put its details in anything Jaron reads.

## The bar
- Looks: the MSV Meridian, the rebuilt freighter wreck and the four built ships. Real-looking people (Loft people), never
  boxes and shapes. Old SYL builds give ideas only - never their art, assets or textures (they looked fake).
- Real where it counts: real sizes, shapes, distances, day and night. Sci-fi where real knowledge is thin (say so).
- Phone first: Jaron plays in Safari on an iPhone. Test with Playwright WebKit iPhone profile and real taps;
  `test/phone-check.mjs` and `node test/validate.mjs` green before publishing. Server tick stays light.

## Tone (Jaron, 10/3 10:54 AM)
People like comedy. Give characters humor; some are assholes. Keep it spicy, keep it fun, keep it challenging.
Easter eggs and surprises are welcome. Every speaking line gets a voice (`node tools/gen-voices.mjs`).

## How to work
- Your own worktree from origin/main; your own folder (`src/worlds/<name>/`, `src/ships/<name>/`, ...). Mark small
  shared-file edits with your package name.
- Publish as soon as green: commit (end with your Co-Authored-By line), `git fetch && git rebase origin/main`, push.
  If server code changed: in C:/Users/lilli/Projects/heartbeat-observatory `git pull --ff-only`, stop node on 8390 (the
  watchdog restarts it), confirm https://cosmos.heartbeatobservatory.com/health shows SupabaseAdapter.
- Screenshots + REVIEW.md in `docs/qa/<date>/<package>/`. One line in `C:/Users/lilli/AI-Shared/state/timeline.md`.
- Report honestly: what works, what doesn't, what you couldn't verify.
