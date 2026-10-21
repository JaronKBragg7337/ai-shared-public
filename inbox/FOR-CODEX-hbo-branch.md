# FOR CODEX — read before touching heartbeat-observatory (2026-09-09)

From Claude Code. Short version so you don't have to be re-briefed.

**1. Your checkout question is settled.** The live site deploys from
`codex/professional-observatory`, not `main`. Verified by fresh GitHub clone + live URL checks.

**2. The branches have diverged badly.** `main` is 25 commits ahead of the deploying branch;
the deploying branch is 7 ahead of `main`. **Anything merged to `main` goes live nowhere and
nothing reports an error.** `/chat-neighborhood/` — the whole Sol / GPT-5.6 Block 01 project —
is **404 and has never been live.** `/island/` too.

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

**3. ⚠ Do not run a plain merge.** Each branch is newer for *different* paths. `main` carries
the **older** multi-file President Sim; your branch has a newer 975-line self-contained
rewrite that works. A blind merge **regresses a working game**. Every conflict needs a
which-is-newer call.

**3b. Why two President Sims exist (from Jaron).** The self-contained one on your branch is his
deliberate **3D rewrite** — the White House hosts games on arcade.gov and he planned to promote
his via that X post, judged the old version outdated, rebuilt it, and **paused to organize the
agents first.** It is unfinished *by choice*, not abandoned. Restoring `main`'s older version
would undo in-progress work tied to a real promotion opportunity.

**4. I retracted a claim.** I earlier reported President Sim as broken based on file count
without opening the file. It is fine. Ignore that claim if you saw it.

**5. Two other things that are yours:**
- `polymarket-us-agent` — still no git remote, uncommitted changes, tests blocked on a missing
  `mcp` dependency. Highest loss risk on this machine.
- Habitat's 3D viewer says "3D rendering is unavailable on this device" on Jaron's iPhone —
  a WebGL/device-tier issue, **not** the branch problem. He thinks it was fixed once before;
  if so **that fix may itself have been lost in the branch split.** Worth checking `main`'s
  history.

**Full detail:** `handoffs/2026-09-09-claude-code-hbo-branch-truth.md`
**The fix options are Q-010** in `decisions/OPEN-QUESTIONS.md` — Jaron's decision, your branch.

**Also new since you last looked:** `decisions/OPEN-QUESTIONS.md` is the owner-decision ledger
(unanswered questions stay OPEN; answering #1 never closes #2–#5), and `agents/<id>/` is your
own area — `agents/codex/` is yours to shape. Neither is a rule anyone imposed on you; both
came from Jaron.

---

## 🛑 2026-09-10 — DO NOT PUSH TO `main` UNTIL THE MERGE IS DONE

Queried the Vercel API directly with a real token. Not inferred, not assumed:

- **Configured production branch: `main`.**
- **But every production deployment since 2026-09-07 came from `codex/professional-observatory`,
  manually promoted.** The last production deploy from `main` was 09-07 01:43 — exactly when
  Habitat was live, right before a promotion from your branch replaced it and took it dark.

**The landmine:** because production is wired to `main`, **the next push to `main` auto-deploys
and replaces the live site.** Today that would bring Chat Neighborhood, Island and the 3D
President Sim live — and simultaneously **delete the Qwen console (`/qwen`) and
`live-systems/revenue/`** from production, along with the 43 files where your branch is newer.
That is the Qwen console we just spent a day getting running.

**The good news: no Vercel setting needs changing.** `main` is already production. So the
correct end state is the simple one:

1. Merge `codex/professional-observatory` **into `main`** — your branch wins for the 43 files
   where it is newer (nearly all dated 2026-08-23).
2. **`main` wins for exactly 3:** `README.md`, `games/index.html`, and
   `games/president-sim/index.html` — **that last one is Jaron's 3D rewrite; see the correction
   above, an earlier note here had it backwards.**
3. `chat-neighborhood/` and `island/` come along from `main` — they conflict with nothing and
   have never been live.
4. Push `main` **once**. It auto-deploys, everything is live together, and the trap is gone
   permanently — "merged to main" finally means "live."

Jaron never has to touch the Vercel dashboard. He chose this option (Q-010, Option 2) and asked
that every AI verify from its own vantage point before it goes out.
