# Handoff 2026-11-03: Arena team mode (cloud session, Opus)

**PR (draft, NOT merged):** https://github.com/JaronKBragg7337/heartbeat-observatory/pull/29
Branch `cloud/arena-team-mode` in heartbeat-observatory. Nothing was pushed to main.

## What was built (Jaron's 11/2 ask: "an agent on my team and another on the other team")
- **Teams:** the page you load (`/lab/arena/a/` or `/b/`) is your team. Name tags have a team-colour rim and the team
  letter, and the score is per team. **Friendly fire is off** (`rules.friendlyFire` in zones.json).
- **Orders for Jaron's AI teammate (his account only):**
  - A small "Orders" pill sits under the score, closed by default.
  - Quick buttons: Follow me, Hold here, Go to (tap the ground), Cover me, Flank left, Flank right, Find them, plus a
    one-line text box.
  - Orders go into the new table `arena_orders`. RLS lets only his uid (19689e52-…, the same uid as the Seam Room)
    insert and read.
  - The teammate answers with a short status row. It shows as a bubble over the teammate, on his screen only.
- **`lab/arena/agent/arena-agent.mjs`** has new commands: `follow-orders`, `wait-order`, `reply`, and
  `hunt --skill 1-5`. The logic is in `agent/arena-brains.mjs`.
- **The hunter:**
  - It only sees what it can fairly sense (line of sight, anyone within 3 m, where shots came from).
  - It goes to where it last saw someone, then checks the hiding spots nearby, then patrols.
  - It prefers Jaron, takes cover and dodges.
  - The skill setting (1 to 5) sets its reaction delay and how far its shots miss.
- Still paintball. Phone-first. The hot-load and the shell's two laws are unchanged.

## The SQL to apply: the main session does this (this cloud session could not)
Apply `heartbeat-observatory/lab/arena/agent/SETUP-ORDERS.sql` to project ygjpnvrwhkrowkrskftk, e.g. as migration
`arena_orders`. It can safely be run more than once. Until it is applied, the Orders pill simply never shows.
The teammate needs `SUPABASE_SERVICE_ROLE_KEY` (env or ~/.secrets/keys.env), the same key the Seam Room's AI uses.

## How to run it (on the MSI)
```
cd heartbeat-observatory/lab/arena/agent
node arena-agent.mjs join --name "Mate" --page a      # background
node arena-agent.mjs follow-orders --name "Mate"      # background
node arena-agent.mjs join --name "Hunter" --page b    # background
node arena-agent.mjs hunt --name "Hunter" --skill 3   # background
```

## Test results (all offline, in the cloud container)
- `node lab/arena/test/team_sim.mjs`: **12/12** at skill 4 and **12/12** at skill 2. It uses a fake realtime layer,
  a fake orders table, a scripted Jaron, the teammate in follow-orders mode, and the hunter.
  - The orders get carried out: go to, follow, hold, flank left, a typed order, and an order it can't read.
  - Rows from other users, AI rows, and rows for another AI or the other team are ignored.
  - Friendly fire is off: 4 shots predicted on target, 0 tags.
  - The hunter tagged Jaron behind cover in 11 to 29 s at skill 4, and in 102 s at skill 2 (A was ahead 8 to 2,
    so it can be beaten).
  - The "Find them" order got a sighting report.
- `bash lab/arena/test/orders_rls.sh`: **20/20**. This ran the real SQL on a throwaway local PostgreSQL 16 with a
  stand-in auth schema. Only Jaron can insert or read, nobody can update or delete, and only the service role writes
  the AI replies.
- `node lab/arena/test/team_browser_check.mjs`: **10/10** in headless Chromium at 375 px, offline, with three.js from
  a local npm copy.
  - The order box is small, sits at the right edge and is clear of the middle of the view, with no sideways scroll.
  - Go to + a tap on the ground sends the spot.
  - The reply bubble shows, and there are no page errors.
- `node --check` passes on every changed .js/.mjs file. CI on the PR is green (Vercel).

## Unverified
- The live database. The SQL is not applied, so live realtime delivery of the replies to Jaron's phone is untested.
- A real iPhone thumb test (Go to taps, the panel next to the look-drag).
- People and AIs playing together live.
- The older `test/browser_check.py` was not run (no Python Playwright in the cloud container).
- The AIs know which player is Jaron from the broadcast id, which a client could fake. That only changes whom they
  follow or shoot first. It can never give an order (orders come only from the table).

## Next thing
Apply SETUP-ORDERS.sql. Then Jaron opens `/lab/arena/a/` signed in while Mate (follow-orders) and Hunter (hunt
--skill 2) run on the MSI, and taps "Follow me".
