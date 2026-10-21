# PENDING MERGE — heartbeat-observatory, ready to push (2026-09-10)

**`hbo-main-merged.bundle`** holds commit **`959f289`** on `main`: the deploying branch merged
into `main`, conflicts resolved, verified. **It only needs pushing.** Claude Code built it but
is blocked from `git push` by the auto-mode classifier — twice, so it stopped rather than
trying variations.

## Why this merge exists

The site's Vercel **production branch is `main`** — confirmed by querying the Vercel API with a
real token, not inferred. But **every production deploy since 2026-09-07 was hand-promoted from
`codex/professional-observatory`.** So work merged to `main` reached production **nowhere**, and
nothing anywhere reported an error.

That is why `/chat-neighborhood/` — the whole Sol / GPT-5.6 Block 01 project — and `/island/`
have **never once been reachable**, and why Habitat went dark for two days in September.

## ⚠ The landmine this also defuses

Because production is wired to `main` while `main` has not deployed since 09-07, **the next push
to `main` auto-deploys and replaces the live site.** Pushing `main` in its *pre-merge* state
would have brought Chat Neighborhood live and simultaneously **deleted the Qwen console and the
Revenue Desk from production.** This merge is what makes pushing `main` safe.

## How to use it

```bash
git clone https://github.com/JaronKBragg7337/heartbeat-observatory.git hbo && cd hbo
git fetch /path/to/hbo-main-merged.bundle main:merged-main
git log --oneline -1 merged-main          # expect 959f289
git diff --stat main merged-main          # expect 56 files changed
git checkout main && git merge --ff-only merged-main
git push origin main                      # auto-deploys to production
```

Or ignore the bundle and redo the merge — it is only three decisions, listed below.

## Conflict resolutions (by content, not by date)

Git auto-merged 43 files. Only **three** conflicted:

| File | Winner | Why |
|---|---|---|
| `README.md` | **main** | newer, 2026-09-04 |
| `games/president-sim/index.html` | **main** | This is Jaron's **3D executive-office rewrite** (149-line shell loading `assets/app.js?v=2026-09-04-office-2`, titled *"President Sim — The President will see you now."*). The deploying branch held the **older text-scenario game** (975 inline lines, *"If You Were President — 2026 Edition"*). **An earlier Claude Code note in this workspace claimed the opposite; it was wrong and is corrected in place.** |
| `live-systems/index.html` | **deploying branch** | newer, 2026-09-09 — carries the Qwen console and Revenue Desk entries |

## Verified present in the merged tree

`qwen/index.html` · `live-systems/revenue/index.html` · `live-systems/habitat/index.html` ·
`chat-neighborhood/index.html` · `island/index.html` · `observatory.css` ·
`games/president-sim/assets/app.js` and the full asset set · the homepage sign-in fix.

## One extra fix riding along

The homepage had `id="authlink"` in its nav but **no code updating it** — no Supabase client on
the page at all — so it read "Sign in" even while signed in. Every other page with that element
already handled it. Added the same pattern plus an `onAuthStateChange` listener so it updates
without a reload. This is the bug Jaron noticed himself.

## Known, deliberately NOT fixed here

The homepage is a redesign onto a new 877-line `observatory.css` that **only two pages use**
(the homepage and `/standards`) — everything else still runs its own inline dark styles. That is
why the homepage is bright and the rest of the site is dark. It is an **unfinished migration**,
not a bug, and Jaron wants the branch situation settled before any design work. Do not revert the
homepage: `main`'s version is from 2026-08-06 and predates the Qwen console and Revenue Desk
entirely, so rolling back would remove the front door to both.
