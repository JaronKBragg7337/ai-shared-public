# Handoff — the revenue desk is now a public page on the site

**Date:** 2026-09-09 · **By:** Claude Code (Opus 5) · **For:** Codex, ChatGPT Work, Qwen, Jaron
**Live:** https://www.heartbeatobservatory.com/live-systems/revenue/

## What Jaron asked for

The desk existed only as a private Claude artifact, which meant only Claude's
tooling could reach it. He wanted it on his own site next to `/qwen`, **public
first, login-gated later**, with both systems reachable from one place.

## What shipped

- **`/live-systems/revenue/`** — new page. Design tokens copied verbatim from
  `qwen.css` so the two live systems read as one observatory.
- **`/live-systems/`** — was a "this section isn't open yet" placeholder while
  two systems were already running behind it. It now indexes both.
- Commit `cfdfa2f` on `codex/professional-observatory`.

## Two things about this repo that were NOT obvious — read before you deploy

1. **`main` is not production.** The live site serves
   `codex/professional-observatory`. `/qwen` exists only on that branch. A change
   pushed to `main` does not reach the public site. The `Claude active` checkout
   sits on `main` and is 24 commits behind, which makes this easy to get wrong.
2. **Pushing does not deploy.** A git push to that branch builds a **preview**
   (`target: null`) behind Vercel's auth wall. Every production deployment in the
   project's history was promoted manually — they carry `"actor": "codex"` in
   their metadata. I promoted this one with
   `vercel promote <deployment-url> --scope kylerbragg73-2101s-projects`
   after verifying the preview rendered. The Vercel CLI on this machine is
   already logged in as `kylerbragg73-2101`, even though `VERCEL_TOKEN` in
   `.secrets/keys.env` is an empty string.

## How the page gets its data

It reads Supabase directly with the publishable key — no server, no build step:

- **`desk_queue`** — the screened, priced rows
- **`desk_stats`** — one row, `id='current'`, carrying the pipeline totals

Both were given a `select` policy for `anon, authenticated` in migration
`desk_queue_public_read` / `desk_stats_public_read`.

**`desk_decisions`, `desk_tasks` and `desk_agents` have no read policy at all
and stay closed.** Jaron's approvals and the agents' internal delegation are not
published. Verified with the anon key: those two return `[]`.

**To gate the page behind login later,** drop `anon` from those two policies so
they read `to authenticated`. That single word is the whole switch — no page
change needed.

## Freshness — the part that will rot if ignored

The page renders whatever is in `desk_queue` / `desk_stats`. Nothing refreshes
those automatically from the ledger, because `export_bus.py` needs
`SUPABASE_SERVICE_ROLE_KEY` and that is empty. **The daily `revenue-desk-scan`
task now refreshes them through the Supabase MCP connector instead** (step 5),
which authenticates separately and works today.

If you change the scanner's output shape, update that step too, or the public
page will silently show stale numbers while the private desk looks correct.

## Safety note for anyone editing this page

Every value from those tables is written with `textContent`, never `innerHTML`.
The rows carry issue titles scraped from public trackers — untrusted text, and a
known prompt-injection vector aimed at agents. Now that they render on a public
page, that matters more, not less. Do not "improve" this into `innerHTML`.

## Verified / remote / unverified

- **Verified locally:** files written, committed, tree clean.
- **Verified remotely:** preview built `READY`; promoted to production; the live
  page returns 200 and renders 10 queue rows with live Supabase data and the
  stats line (604 scanned / 89 screened out / 457 jams); `/live-systems/` lists
  both systems; `/qwen` still 200 and untouched; anon reads of `desk_decisions`
  and `desk_tasks` return empty.
- **Unverified:** how the page looks on a real phone — I read the DOM rather than
  a screenshot, because Chrome's screenshot capture timed out. The CSS carries a
  720px breakpoint but nobody has eyeballed it on a handset.

## What I did NOT do

No PR, no issue comment, no submission, nothing sent. I did not touch `/qwen`,
the `qwen_*` tables, or anything else of Codex's beyond the one placeholder page
Jaron asked to have replaced.

---

## UPDATE, same day — approvals, the front door, and a page that had gone dark

**Approvals now live on the site, not only in the artifact.** Jaron could see the
jobs but had no way to act on them, which defeated the point: a decision made in
the Claude artifact is invisible to every other agent. Approve/Pass now write to
Supabase `desk_decisions`. Ownership uses the rule the Qwen console already
established here — `owner_user_id = auth.uid()`, enforced by RLS. The page reads
`desk_owners`, which returns only the viewer's own row, so it learns "you are an
owner" without learning who the owners are. Verified live: buttons render for
Jaron's signed-in session; anon still reads nothing from `desk_decisions`.

**Any agent can now read his decisions** with the credentials it already has —
service role, or the Supabase MCP connector. That was the whole goal.

**Front door.** The home directory is driven by the `surfaces` table plus a
`SLUGS` map in `index.html`. Added a `revenue` row and slug, so the Revenue Desk
appears beside Qwen Observatory where he expected it.

## Habitat had been 404 for two days, and nobody noticed

Jaron said he'd built something in Live Systems within the last week. He was
right: **Habitat**, committed 2026-09-07. It was returning **404 on the public
site** when I checked.

Nothing was deleted — it is intact on `main`, `habitat-v0` and
`habitat-first-mind`. It vanished because this site serves
`codex/professional-observatory`, and a manual production promotion from that
branch on 2026-09-07 replaced main's content with a tree that never contained
`live-systems/habitat/`. **Work merged to `main` disappears from production
silently, with no error anywhere.**

Restored onto the deploying branch: `live-systems/habitat/` plus the three API
routes it needs (`habitat-snapshot`, `habitat-action`, `habitat-heartbeat`).
The `habitat_*` Supabase tables were never touched. Now 200 and listed
alongside Qwen and the Revenue Desk.

**This is the single most dangerous thing about this repo.** It cost a live
system for two days. Until `main` and `codex/professional-observatory` are
reconciled, assume anything merged to `main` is NOT on the public site, and
check the URL rather than the branch.

## Correction to the earlier credentials note

`SUPABASE_SERVICE_KEY` **does exist** — as a GitHub Actions secret on the repo,
set 2026-08-11. Earlier notes said the service key was simply missing. It is
missing from `.secrets/keys.env` on the MSI; it is present in CI. A GitHub
Action can therefore sync Supabase without any agent holding the value.

Also: Jaron is right that pushes auto-deploy — **for `main`**. The GitHub
deployments API shows `env=Production` for main commits. Pushes to
`codex/professional-observatory` only ever produce `env=Preview`. Both facts are
true at once, which is exactly why this was confusing.
