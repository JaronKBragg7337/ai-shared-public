# 2026-11-04 · Cloud (Opus) · Arena AI crew

**PR:** https://github.com/JaronKBragg7337/heartbeat-observatory/pull/30 (branch `cloud/arena-crew`, draft, not merged).
Only `lab/arena/` changed. RLS and `arena_orders` are untouched, and no keys were added.
Screenshots: `handoffs/2026-11-04-cloud-arena-crew/`.

## What I built
1. **Spectator camera.**
   - A **Watch** pill on `/lab/arena/a/` and `/b/`, under the score, to the left of Orders.
   - A watch-only page, `/lab/arena/a/?watch`: no body on the field, `getState()` returns null, nothing is sent.
   - **Overview:** one finger orbits, pinch zooms, two fingers pan. **Follow:** tap a name in the bottom bar (48 px buttons), tap a name tag, or press keys 1-9 (0 = overview, Esc or Play = back to playing).
2. **Name tags.** Each tag shows the team letter and colour, the name, an AI badge with the model, and a state word (`hunting`, `covering`, `following`, `flanking`, `patrolling`, `tagged`).
   - They are DOM, not sprites: no draw calls and sharp on a phone. They face the camera and fade with distance.
   - The word rides the 4th part of `place` (`b|b||hunting`), so old clients ignore it.
   - `arena-brains.mjs` sets it as the brains play. Any AI can set its own with `node arena-agent.mjs status "..."`.
3. **Easy join.** One command: `node arena-agent.mjs join --name "Codex" --team b --model "Codex CLI" --detach`. It returns once the player is connected; on failure it stops the player and prints the log. If the kit's packages are missing, it prints the exact `npm install` command.
   - New `lab/arena/AGENT-GUIDE.md`: the paintball rules (tag/out, no killing language) and the commands.
   - README: copy-paste examples for Codex, Kimi and Grok, plus a Watch section.
4. **Fixes:**
   - The player kit is merged into 2 meshes, so a player costs 4 draw calls instead of 18.
   - Static field meshes are merged by material (the field goes from 57 to 35 draw calls). The cover stays in place, hidden, so raycasts still hit each piece.
   - `zones.json` `"v"` is bumped to 2.

## How to test (MSI or phone)
- Phone (Safari): open `/lab/arena/a/?watch` while 2+ AIs play. Check orbit, pinch, the picker, a tag tap, and the state words.
- Start some AIs:
  - `cd lab/arena/agent`
  - `node arena-agent.mjs join --name Hunter --team b --detach && node arena-agent.mjs hunt --name Hunter --skill 3`
- Offline tests: `node lab/arena/test/watch_check.mjs --three <three@0.160.0>` and `node lab/arena/test/team_browser_check.mjs`.

## What I verified (headless Chromium, offline)
- `watch_check.mjs`: 22/22 at 390x844 (real touch events) and 1280x800. No console errors, no sideways scroll, 50 draw calls with 6 players.
- `team_browser_check.mjs`: 10/10.
- Snapshot mode renders with no errors.
- `status` reached a running player, and the `--detach` failure path works.

## What I did not verify
- A real iPhone.
- The live channel: the cloud sandbox can't reach Supabase, so no live AI joined.
- `test/browser_check.py` was not run (no Python Playwright here).
- `team_sim.mjs` passes 10/12, the same as main. The hunter doesn't find a Jaron hidden behind A-block-1 within 150 s. That's a search-tuning issue in `arena-brains.mjs` and is still open.
