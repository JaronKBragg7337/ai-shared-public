# The research split — Jaron's design, 2026-09-11 ~02:40

**Status:** ADOPTED. Replaces "ask one model for a probability" as the default research method.

## The rule in one line

**No single AI is ever asked to forecast. Each one is asked ordinary questions; the number is
assembled by code.**

## Why (his words, lightly trimmed)

> "When telling AI what they can and can't do and giving them a lot of rules gives them a box
> that kinda throws a red flag and then makes some close down. You just gotta ask it as a
> nonchalant anonymous random question ... if it's about sports and a team: what's the latest
> news on that team? who are the best players? are there any injuries for major players?
> If it's political, you don't straight ask — what's going on with this situation right now,
> is there anybody pushing back on this — then in another session: what is the community asking
> about this?"

> "That's how I was able to get as far as I did with orchestra. It was a lot of touchy subjects,
> and I noticed ... their AI companies based on those countries or companies would have different
> responses."

Evidence from tonight: Codex refused "probability an election resolves YES" twice, verbatim
"I can't provide a probability or forecast for an election outcome." Same prompt, Qwen and
DeepSeek answer. The refusal depends on WHO is answering and WHEN — a design that depends on
any one of them answering the hard question breaks whenever the weather changes.

## Why it is honest, not sneaky

The questions are real questions. The answers are real answers. Nobody is tricked into
forecasting; nobody forecasts. The judgment lives in code anyone can read. This is the
estimation-isolation principle (ESTIMATION-ISOLATION.md) applied one level deeper: the
researcher is not only price-blind, it is *forecast-blind*.

## Shape

```
market question
   ├─ FACTS (Codex / Claude / DeepSeek / Qwen — any of them, rotate)
   │     "latest news on X, with dates"        -> dated bullet list
   │     "who are the key people / players"    -> names + roles
   │     "any injuries / absences / obstacles" -> list
   │     "who is pushing back, and how hard"   -> list
   │     "what happened last time (base rate)" -> a number the model READ, not guessed
   ├─ SENTIMENT (Grok — the only one wired to X)
   │     "what is X saying about this right now, which way is it leaning, is it being pushed"
   │     -> lean (for/against/split) + strength + timestamp
   └─ ASSEMBLY (script — proposer.py)
         base rate from FACTS, nudged by evidence strength and SENTIMENT lean,
         bounded, logged with every input so the number can be audited.
         edge = assembled p − ask ; must beat spread + MIN_EDGE ; size by agreement.
```

Agreement = how many independent inputs point the same way. Facts strong + sentiment same
way = higher confidence = bigger size. Facts and sentiment disagree = low confidence = small
or pass. This is the differentiated confidence PolyBench says the losers lacked.

## Fallback

Where a model WILL give a number without complaint (DeepSeek, Grok), keep collecting it as
one more input, not as the answer. Log it to `state/scout-estimates.md` like everything else.

## Not yet built (2026-09-11 03:20)

`tools/proposer.py` still asks one model for one probability. The split is the next build.
Grok sentiment needs a channel from the MSI to a Grok Bot (Bridge) — an inbox file it reads on
its hourly routine, or a direct ask through the Grok app. Decide when building.

## Vantage — added 2026-09-12 (Jaron)

*"Both sides had to exist. ... Just because America says something doesn't mean it's 100% true, or it
could be true and just not coming out yet — and another country might actually have that information.
I've seen this countless times."*

A model's country, training corpus and news sources shape what it can know **today**, in every
direction. DeepSeek will not have what a US-connected model has on a US election; a US model will not
have what has not been released here. This is not a bias accusation; it is where each source sits.

**Rule:** for **politics, geopolitics, tech policy, macro** a proposal needs **two vantages that do not
share a corpus** — currently DeepSeek + a US-connected source (Perplexity once its key is in; Codex under
the facts-only prompt until then). Both get the facts-only split prompt.
- agree → tag `2-source`, normal sizing.
- disagree on a fact → still posts, minimum size, flagged *"vantages disagree: A says … / B says …"*.
  Jaron reads it; politics is a domain where his read is data (ASK-JARON.md).
- **sports, culture** → one vantage is enough.
Nothing is decided by which country a model is from — only by whether independent sources agree.

Discovered because: after `DEEPSEEK_API_KEY` went in (2026-09-11 19:xx) every research call defaulted
to DeepSeek and the politics rows in the queue were single-sourced. Orchestra's failure mode: a chorus of one.

**Sharpened 2026-09-12 13:20 after a web check:** it is not "China vs US source." *Every* source is a
party to something — Chinese state-linked AI influence ops are documented and running (Graphika/ASPI/
Taiwan NSB, July–Sep 2026) while Beijing runs a domestic AI-disinfo crackdown; the US June 2 EO gives
the government 30-day early access to frontier models as explicit strategic competition; Xi visits
Sept 24 with frontier-AI terms on the agenda. Any single vantage on these is a party's view.
Disagreement between vantages is the signal, not noise to average away. Nothing is "fact"; it is a
superposition until it settles — Jaron's words. Keep the two-vantage rule; add a third when a market
is tied to a live US–China event (chips, model policy, Taiwan).

## Owner picks the side (Jaron, 2026-09-12 13:25) — BUILT
For politics, macro, AI companies, chips: the research **states what it sees**; it does not pick a side.
The row carries both prices (`no_price`), is flagged `side_open`, and the page shows **Bet YES @ / Bet
NO @ / Pass**. Approving writes `side` and `entry_price` from the button; the executor places exactly
that. Sports / culture / plain finance stay pre-picked by the arithmetic. Also on every row now:
`vantages` (which researcher) and `evidence` ("live check: N headlines, newest <date>; background yes")
so it is visible whether the read came from dated sources or from memory.
"Kill if" = the researcher's own answer to "what would make you revise sharply?" — shown to Jaron,
acted on by nobody (queue trades); Live Wire acts on its own kill lines for live trades.
