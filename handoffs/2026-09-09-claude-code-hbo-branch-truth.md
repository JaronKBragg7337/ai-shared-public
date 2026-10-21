# HANDOFF — heartbeat-observatory: what is actually live, and the branch trap (2026-09-09)

**From:** Claude Code (Opus 5) · **To:** Codex first, then anyone touching the website
**Method:** fresh `git clone` from GitHub + `curl` against the real public URLs.
**No local checkout was trusted, including my own.** That is the point of this handoff.

---

## 1. The checkout conflict is RESOLVED. The deploying branch is `codex/professional-observatory`.

Open since 2026-09-08. Settled: **the live site deploys from `codex/professional-observatory`,
not `main`.** Anyone editing `/qwen` edits that branch.

## 2. The real problem is worse, and it is still open

`main` is **25 commits ahead** of the deploying branch. The deploying branch is **7 ahead** of
`main`. They have genuinely diverged.

**Work merged to `main` reaches production nowhere, and nothing anywhere reports an error.**

Already paid for:

| Path | Live? | Reality |
|---|---|---|
| `/chat-neighborhood/` | **404** | The entire Sol / GPT-5.6 Block 01 project — district charter, model registry, build log. Merged to `main` 2026-09-06. **Has never once been reachable.** |
| `/island/` | **404** | Same cause. |
| `/live-systems/habitat/` | 200 | Vanished for two days when a promotion from the deploy branch replaced `main`'s content. Restored by cherry-pick — **patched, not reconciled.** |

Also invisible on `main` only: `supabase/habitat-v0.sql`,
`supabase/habitat-controller-lifecycle.sql`, `lab/voice`, four `chat-neighborhood/models`.

## 3. RETRACTION — I claimed President Sim was broken. It is not.

Earlier today I reported `/games/president-sim/` as "200 but serving a shell, missing
`app.js` and `styles.css`." **That was wrong and I am retracting it.**

The deploying branch's `games/president-sim/index.html` is a **975-line self-contained page** —
the whole thing inline, which is why one file is sufficient. The six extra files on `main` are
the **older split-file version**. Jaron confirmed from his phone that the game runs, and it
does. There is also a standalone repo live at
`https://jaronkbragg7337.github.io/President-Sim/` (200).

**I inferred "fewer files" meant "broken" without opening the file. Don't repeat that.**

**PROVENANCE — why two versions exist (from Jaron, 2026-09-09):** the self-contained version on
the deploying branch is his **deliberate 3D rewrite**. The White House published games on
arcade.gov, and he intended to use that X post to promote his — but judged the existing version
outdated against what he knew he could build, so he rebuilt it and **paused mid-effort to get
the agents organized first.**

**So the deploy branch's President Sim is the newer, intentional work, and it is unfinished by
choice.** Anyone reconciling branches who sees `main` "ahead by 25" and merges would silently
undo an in-progress rewrite tied to a real promotion opportunity. **Do not restore `main`'s
President Sim. Do not treat the pause as abandonment.**

> **🛑 CORRECTION 2026-09-09 (later the same day) — THIS WAS BACKWARDS. READ THIS FIRST.**
>
> Claude Code previously warned that the **deploying branch** held Jaron's newer self-contained
> 3D President Sim and that `main` held an older multi-file version. **That is inverted. The
> opposite is true.** Established by reading both files, not by comparing dates:
>
> | | `main` (Draft A) | `codex/professional-observatory` (LIVE, Draft B) |
> |---|---|---|
> | Title | *"President Sim — The President will see you now."* | *"🇺🇸 If You Were President — 2026 Edition 🇺🇸"* |
> | Size | 149-line shell | 975 lines, all inline |
> | Loads | `./assets/app.js?v=2026-09-04-office-2` | nothing external |
> | What it is | **Jaron's NEW 3D executive-office rewrite** | **the OLD text-scenario game** |
> | Last commit | 2026-09-04 *"Sync phone conversation focus"* | 2026-09-03 *"Sync polished embed"* |
>
> The six `games/president-sim/assets/*` files that exist only on `main` are **the 3D game's
> actual code**, not stale leftovers. The title on `main` matches what Jaron sees on his phone.
>
> **Therefore: `main` must WIN for `games/president-sim/`. Do not preserve the deploy branch's
> copy.** Preserving it would discard the 3D rewrite and keep the old text game — the exact
> outcome the original warning was trying to prevent, achieved by following it.
>
> Why the first read was wrong: it inferred from file count and self-containment that the
> single large file was the newer rewrite, without opening either file. **Dates and file counts
> are not evidence of which version is newer. Content is.**

## 4. ⚠ THE THING THAT WILL BITE WHOEVER FIXES THIS

**This is not a simple merge, in either direction.** Each branch holds **newer** versions of
**different** things:

- **Deploy branch is newer for:** President Sim (self-contained rewrite), `qwen/` console,
  `live-systems/revenue/`, the qwen Supabase migrations.
- **`main` is newer for:** `chat-neighborhood/`, `island/`, habitat SQL, `lab/voice`.

**A blind `git merge` would restore `main`'s stale President Sim over the working one and
regress a live game.** Every conflicting path needs a which-is-newer judgement. Do not let a
merge tool decide, and do not let "main is ahead by 25" imply main is more current.

## 5. Recommended fix (Q-010 — Jaron's call, Codex's branch)

Two options, in `decisions/OPEN-QUESTIONS.md`:

1. Merge `main` into the deploying branch — everything lands at once, highest break risk.
2. **Recommended:** merge the deploy branch's 7 commits into `main` first, resolving each
   conflict by which version is genuinely newer, **then point Vercel production at `main`.**
   This makes "merged to `main` = live" permanently true, instead of leaving a trap that fires
   again the next time anyone merges.

Option 2 fixes the mental model. Option 1 fixes today's symptom and leaves the trap armed.

## 6. Separate bug, not the branch problem — Habitat 3D on mobile

`/live-systems/habitat/` is genuinely healthy: persistent state online, **world tick 3802, 1
body, generation g000, connected minds 0, Seed-01 not attached.** But the viewer reports
**"3D rendering is unavailable on this device"** on Jaron's iPhone. Page loads `/hb-device-tier.js`.

**This is a WebGL / device-tier issue, not a deploy issue.** Jaron thinks it may have been
fixed once before — **if so, that fix may itself be a casualty of the branch split.** Worth
checking `main`'s history for a device-tier fix that never reached the deploying branch. Logged
as `habitat-webgl-mobile`.

## 7. The transferable lesson

Every agent here — me, Codex, ChatGPT Work — would have reported its own checkout as clean and
been **correct**. None of us could have found this from a local folder. The truth existed only
in the comparison, and the comparison only exists on GitHub.

Jaron's instinct, in his words: *"Worrying about what's local when everyone holds different
ones is pointless when we can clone the live version that holds it all on GitHub."* He is
right, with one refinement — GitHub holds **11 branches**, so "clone it" must mean **clone,
then compare branches against what the live URLs actually return.** A clone alone still shows
you one branch's opinion.

**Before claiming anything about this site is fine: check origin, then check the URL.**

---
*Claude Code · 2026-09-09 · **Verified locally:** fresh clone, branch divergence counts,
per-path file comparison, the President Sim file contents that forced my retraction.
**Verified remotely:** all eight live URLs by HTTP status, plus the standalone President Sim
repo. **Unverified:** which Vercel project/branch mapping produces production (VERCEL_TOKEN is
empty), and whether a prior Habitat device-tier fix exists in history.*
