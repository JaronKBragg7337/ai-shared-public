# Framing Lens - the usable system (plan, 2026-09-29 night; build starts 9/30 after the 4 PM usage reset)

Jaron: "Let's make this a system that can be used. For more than one thing." Built from his three repos (book = the WHY,
exercise = the TEST, Framing-Lens spec = the TOOL) plus AI-Framing-Study (the RESULTS). Clean, fun first, data underneath.

## The words (his idea, said plainly)
Six small questions, each about two things that need each other. No right answer, so every answer shows how the person
thinks. One answer gives five readings: the pick (root stance: credit the other / credit self / dismiss / stay open / hold
both), the reason (logic, feeling, rules, humor, experience), the first step (ask, measure, fix, run, wait), the blind spot
(self-knowledge), the rewrite (voice: serious, playful, poetic, blunt). Six worlds (kitchen, AI, tools, travel, air, stars)
show whether someone thinks the same everywhere or switches by subject.

## What gets built (lives on heartbeatobservatory.com; data in Supabase; results page reuses AI-Framing-Study data)
1. **Take it** - the six prompts, mobile, a few minutes, fun first (the "love language test" feel).
2. **Your reading** - pattern in plain words (Framing-Lens dimensions: context-dependent, constraint-first, literal,
   risk-first, system-oriented, ambiguity tolerance) + tone read from the rewrite and first step + "how to talk to me":
   serious/playful openers, what to lead with, what to go easy on. Descriptive, never a rank or a score.
3. **Compare two** - partners, business, friends: match / balance / friction (pairing modes from the spec: complementary,
   contrasting, aligned, exploratory).
4. **Teams** - a group code (class, crew); everyone takes it; suggested balanced teams. School use: anonymous by default.
5. **Compare with AIs** - nearest AI pattern, from the AI-Framing-Study runs.
6. **Sparks** - a pattern becomes a character personality seed (games, the Necklace, shows).
7. **Research** - opt-in: add your answers to the anonymous dataset (the "gap in AI training data" angle).

Reading engine: rules-based and readable (each option maps to signals; free-text fields read by simple cues first, an
AI read optional later) - interpretable, not a black box (Framing-Lens spec). Policy per session (spec): private by
default for people; sharing, identity and retention are the taker's choice. Other people's answers are theirs.

## The AI test (after exposure) - WAIT for Jaron's go
Three conditions, fresh sessions, same models: (a) nothing (done 9/29), (b) the one-page rules card (CARD-draft.md, after
Jaron approves it), (c) the full book. Shows whether the rules or the story move the answers. Results go into
AI-Framing-Study as new runs with a `condition` field. Fable only if Jaron OKs the credits.

## Clean-up of the old repos (later, his call)
Each repo gets a one-line "what this is / how it connects" header linking the other three. The exercise repo's
"AI-Responses-Feb2026" file is dated Feb 22, 2025 inside.

## Jaron's additions (9/29 11:44 PM, bracketed on the skeleton - "part of the skeleton") -> design rules
1. **The missing answer.** In school he always felt a perspective was missing from the choices; his brain built its own
   answer and the listed ones felt wrong. -> Every prompt gets a write-in ("none of these - here's mine"); choosing it is a
   reading. And one question can't read anyone: the bank spans silly -> serious and many subjects; more prompts than six.
2. **Skipping is data, not failure.** Nobody has to fill everything; what someone avoids every time is a signal (not a bad
   one) - it shows a role they'll fill, or what a teammate can cover. -> Every field optional; the reading uses gaps.
3. **The first step shows the role:** leader, assistant, builder, thinker (and more).
4. **The blind spot can be a new perspective.** It can show what someone sees that others can't, or a solution they found
   without knowing what else it solves. -> Pairing connects a discoverer with someone who sees where the discovery fits.
5. **Readings lean on each other.** If one field says nothing, another may, and some topics are avoided while others are
   embraced; topic changes openness. -> Read across fields and across topics, never one field alone.
6. **The worlds show experience and imagination:** what someone has lived, observed, or can imagine as real (the sci-fi
   side) - which surfaces creators, system thinkers, leaders, builders, laid-back people. -> Add prompts and possibly one
   more answer field; the old six were a start.
7. **"And so much more."** Why he ran from it: wanting everyone to take it felt like "give me all your information" (the
   alien-touch scene). -> The answer: it gives back first - the taker gets their reading before anything else; sharing is
   their choice, anonymous by default; fun is the front door, data is opt-in underneath.
8. His brain only resurfaces something when it sees a use or an improvement - this came back because it has both now.

## More uses (Jaron 9/29 11:48 PM)
- **Tell the two markets apart:** who wants the AI future and who doesn't - so he can serve each (with AI, or by learning to do
  it without AI for those who don't). See memory jaron-two-sides-is-two-markets.
- **His business's job application = placement, not screening** (Jaron 11:50 PM, correcting my flag): "if someone put an
  application in they're getting hired" - the only reason not to hire is being full. There isn't a person, disability or
  background included, he can't find a role for. They take it because they already got the job; it shows what they're best
  suited for and who to partner them with. Fits his own "not a hiring or firing tool" rule exactly.

## Proposed additions (for Jaron to pick)
New prompts (same shape, silly -> serious, new subjects): seed/soil (growth), lock/key (trust), phone/charger (goofy, modern),
money/wallet (money), boss/crew (authority, work), mirror/face (self-image), joke/silence (humor).
New optional fields: "Which one are you?" (giver or relier), "Where have you seen this?" (lived / watched / imagined),
"Your own answer" write-in on every prompt.
