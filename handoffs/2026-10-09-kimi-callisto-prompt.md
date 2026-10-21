Paste this into Kimi Work (model K3, thinking High), with the project folder set to C:\Users\lilli\Projects\heartbeat-observatory:

---

You're building one new world for The Cosmos, a 3D space game that runs in the browser (three.js). The game is live at
https://www.heartbeatobservatory.com/games/the-cosmos/ and lives in games/the-cosmos in this repo. Other AIs (Claude, Codex)
work on it too, so you work on your own branch.

THE JOB: build CALLISTO (Jupiter's moon) as a full, landable start world. Today it's listed as "coming".

READ FIRST, IN THIS ORDER:
1. games/the-cosmos/docs/ADD-A-WORLD.md - the exact recipe for adding a world. Follow it; you touch no shared file.
2. src/worlds/earth/, src/worlds/moon/, src/worlds/ceres/ - finished worlds to copy the pattern from.
3. C:\Users\lilli\AI-Shared\projects\syl\BIBLE-v3.md - the design. Callisto: the Mystara faction (maps, data, the only safe routes
   in the Jupiter system, strange tech) and the open "Unbound" seat; Valhalla basin camp; Jupiter in the sky; prospectors' camp;
   sealed sites. Also section 17 (rules for builders).
4. src/opening/worlds.js (the start board) and how Earth and Ceres were made "open" start worlds.

WHAT DONE LOOKS LIKE:
- Real Callisto: real radius, gravity, day length, its orbit around Jupiter, Jupiter huge in the sky, icy cratered ground.
- The Valhalla camp: a landing pad and a few real-looking Mystara buildings (instruments, dishes), one thing worth finding.
- Callisto open on the start board with its own opening lines and voices (node tools/gen-voices.mjs), the way Earth was done.
- A few jobs with a short story thread, the way the other worlds have them (docs/MISSIONS.md).
- Realistic look. No blocky people - leave people out rather than make blocky ones. It must run on an iPhone.
- Tests: node test/validate.mjs and node test/phone-check.mjs both green. Add test/pkg-callisto.mjs per the recipe.

RULES:
- You are in a git worktree already on branch kimi/callisto (C:\Users\lilli\Projects\heartbeat-observatory-kimi). All paths
  above are inside it. Commit there and push that branch (git push -u origin kimi/callisto). Do NOT push to main, do not merge.
- Do not change Cloudflare, Vercel or Supabase settings, and do not restart any server. Claude reviews and ships it.
- When done, write games/the-cosmos/docs/callisto-kimi-report.md: what you built, what works, what's unfinished, test results.

---
