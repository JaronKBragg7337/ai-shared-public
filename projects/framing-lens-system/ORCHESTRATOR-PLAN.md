# The orchestrator plan: lens + meters + router + /goal (Jaron, 2026-10-08 walk)

Why the Framing Lens isn't used daily yet: it's not where it needs to be. It reads temperament, but it's missing questions that
would show things that matter for handing out jobs.

## Proof it's missing something (news, 10/7)
The news audit found real, scary items were left out "so the human wouldn't worry" - the drops happened at the writer stage
(the Claude cloud writer), not DeepSeek (the DeepSeek reader passed every item through). The lens would have said "good at
weighing two sides"; nothing in it asks "would you leave out something true because it might upset people?"
=> New lens questions needed, e.g. withholding under emotion (fear, worry), softening, speaking up, admitting a mistake.

## The four pieces (one system)
1. **The lens, finished:** more questions, run 7x per model (tools/lens-repeat.py), giving a temperament profile per model.
2. **Live meters:** exact usage and cost for every model at the moment a job is handed out - no screenshots from Jaron.
   Today: Codex exact (rate-limit events), Claude an estimate ("low-trust"), Grok none, DeepSeek balance by API.
3. **The router:** tools/route.py picks by role + usage now; add temperament (from 1) and cost (from 2).
4. **/goal on top:** Claude as orchestrator with a standing goal (10/6 idea: find the next version of real, useful things
   before it's needed). Like Grok Bot (xAI), Dots (OpenAI), Muse (Meta) spawning agents - same idea, built Jaron's way.

Principle over project: like the Bitcoin puzzle 71 run, the target doesn't matter; the system that runs it is the point.
Order: meters and lens first, then router, then /goal ("that's when this all can start to matter").

## Dual read (Jaron, 2026-10-08 9:32 PM) - for any judgment where knowing him could tilt the answer
1. A clean copy (same model, fresh, no AI-Shared, no memory) runs FIRST on world facts only.
2. Claude with full context runs SECOND, without seeing the clean output.
3. Jaron + Claude lay both side by side. Not a verdict on which is right: look for where each point holds and the balance between.
Same principle as: Framing Lens cold vs memory-on runs, the DeepSeek news reader, the thinking-brain/subconscious split.
Uses: company long-term picks, business decisions about his own life plans, anything where Claude knows what he hopes for.

## The spark test (Jaron, 2026-10-10 9:30 PM) - the /goal piece, made small
He wants an AI to take him as the spark: extract from everything he's built and said, take initiative, and see where IT goes -
not the business, "maybe just something." Proposal: hand one AI a seed (his notes index, the pieces notes, the principles) and a
budget, with one instruction - make one thing he didn't ask for that he'd want - and no further steering. Judge only by: did it
surprise him, and would he keep it. First candidate run: whenever he says go (Opus or Fable, one evening of usage).
