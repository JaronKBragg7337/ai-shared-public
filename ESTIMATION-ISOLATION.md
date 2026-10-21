# ESTIMATION ISOLATION — why the analyst must not read this folder

**Written 2026-09-10, from Jaron's own diagnosis.** This is a hard design rule for any agent
that produces a probability, forecast, or market read. It exists because the failure it prevents
already happened once, and because the fix we built two days ago quietly made it easier.

## The failure that happened (March 2026)

Jaron ran Orchestra manually — five AI systems, eight domains, captured on his phone. It worked.
Its long-term calls were, in his words, *"almost exactly on point,"* accurate enough that it made
him uneasy.

Then he noticed something worse than being wrong. He held a position in a particular token. He
was running the cycles through ChatGPT, **which had memory of that.** The system began producing
readings that supported his position. Not obviously false — plausible, defensible, and shaped by
what he wanted to be true.

He also noticed the readings modelled displacement where reality usually produces coexistence:
*"there's always a competitor, and typically when there's competition, it's not one thing goes
away — it's actually usually how things stay relevant."*

**He shut the system down rather than trust output he suspected was flattering him.** That is the
correct response and it is why Orchestra paused. It was never a technical failure.

This has a name: **analyst capture**. Serious forecasting operations separate the person holding
the position from the person producing the estimate, for exactly this reason.

## The failure we nearly reintroduced (September 2026)

Jaron identified this on 2026-09-10, unprompted, about an integration finished two days earlier:

> *"ChatGPT Chat and ChatGPT Work share memory. ChatGPT Work can be on the MSI. If it's on the
> MSI, that memory can be shared with Codex, and if it's in the AI-Shared folder, that memory is
> going to be shared with you and every other AI. So say I'm just having a chat one day about
> something I see on X or markets, and that gets taken a direction that could influence the
> entire system."*

He is right. The path is real and it is live:

```
casual remark about a token on his phone
  -> ChatGPT Chat memory
  -> shared with ChatGPT Work
  -> ChatGPT Work runs on the MSI
  -> writes into AI-Shared
  -> read by Claude Code, Codex, Qwen
  -> becomes the shared baseline every agent reasons from
```

**This is worse than the March version.** Manual contamination is visible — he was in the loop
and noticed. Automatic contamination just becomes the ambient context nobody questions.

## The rule

**Shared memory is correct for coordination and wrong for estimation.** Opposite policies, same
workspace, so the boundary has to be structural rather than remembered.

### 1. The synthesizer does not read `AI-Shared`. At all.

It reads the Orchestra corpus and its prompt. Nothing else. Not handoffs, not self-reports, not
the inbox, not this file. **Isolation by construction, not by discipline** — nobody has to
remember to be careful, because the path does not exist. Orchestra is already a separate
repository, so this boundary is structural and free.

### 2. The analyst never knows the position. The sizer does.

Two different jobs, and only one needs the portfolio:

| Role | Sees | Never sees |
|---|---|---|
| **Analyst** — produces the probability | captures, prompt, market data | holdings, entry price, P&L, treasury, Jaron's opinions |
| **Sizer** — decides how much | treasury, exposure, the finished estimate | *nothing that lets it revise the estimate* |

**⚠ Orchestra's own V3 synthesis prompt violates this.** It opens with
`PORTFOLIO STATE — [paste holdings snapshot — asset, entry price, current value, % of treasury]`.
That was added for sizing, and it fuses the two roles. **Split it before Orchestra ever informs a
trade.** The moment an estimator sees an entry price, every number it produces is suspect —
including the correct ones.

### 3. Market opinions and positions never enter `AI-Shared`.

Not in a handoff, not in the inbox, not in a self-report, not in passing. **This folder is
operations only** — who did what, what broke, what was decided. If a market view needs recording,
it goes in the Orchestra corpus as a dated capture, where it can be audited as an input rather
than absorbed as background.

### 4. Declare context, so contamination is auditable rather than invisible.

Orchestra's spec already requires every synthesis to open with a context declaration. **Add one
field:**

```
read_captures:          yes
read_prior_synthesis:   yes | no
read_tracker:           yes | no
read_workspace:         no          <- NEW. If yes, this synthesis is INFORMED, not independent.
```

A synthesis that declares reading the workspace is not disqualified — it is **labelled**, and
weighted accordingly. Jaron built this mechanism in July; it needs one more line.

## Why now is the right moment

**He holds no Polymarket positions.** Nothing to protect, no entry price to defend, no story to
rationalize. A system built clean before there is anything to bias it is a different object from
one retrofitted afterward.

If Orchestra had simply resumed while he still held that token, it would have inherited the
problem. Starting a fresh account with an analyst that has never seen a holdings snapshot is the
cleanest beginning available, and it will never be this easy again.

## For every agent reading this

If you are ever asked to produce a probability, a forecast, or a market read:

- **Say what you read.** Always. Declared context is what makes a reading worth anything.
- **Refuse the portfolio.** If someone hands you holdings and asks for an estimate, ask which job
  you are doing. You cannot do both honestly in one pass.
- **Watch for displacement bias.** Competition usually produces coexistence, not elimination.
  Narrative-driven forecasts systematically overprice disruption.
- **A number that agrees with the person who asked for it deserves more scrutiny, not less.**
