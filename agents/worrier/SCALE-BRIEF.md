# Independent design: a safety signal scale (Fable 5.2, blind), 11/15/2026

Hi Fable. Jaron wants the AIs to bring their OWN reasoning and designs, not just polish his. Main job: design, from scratch, the best possible 0-5 "safety signal" for a small family network in Fort Wayne, Indiana. Do NOT read projects/safety-signal-page/SCALE-REVIEW-DRAFT.md or tools/safety_signal.py first (you're the blind second opinion); you may read them AFTER your design is written, to compare.

What it's for: one plain number that tells ~50 people when to get ready and when to move. It must not cry wolf (people stop listening) and must not miss the start of something big.

Jaron's views (use them, argue with them if you think he's wrong):
- The real danger at the top is COLLAPSE, not just attacks: if the grid or the economy breaks, even in half the country, people turn on each other (riots, looting gun/food/drug stores, grudges settled). He knows that world from street life.
- "No evidence" isn't safety; skilled attacks leave few traces and officials may stay quiet to avoid panic. Watch what's hard to hide (actions, money, patterns), not statements.
- A domestic attack with a known motive is a statement (lower); a foreign or unexplained one could be an opening move (higher).
- Far events should still raise awareness; only nearby or systemic failure should mean "move."

Context from this week to test your design on (public news): a nationwide FAA ground stop from a comms failure (cause unknown, "zero evidence" of cyber), a real bomb at an ethanol plant in Peoria IL with a 1-mile evacuation (230 mi away, no suspect), reports of an Iranian drone plot against Trump with officials moving to secure sites (unconfirmed), suspected Iranian cyberattacks on US water systems (July, newly reported), oil reserve lowest since 1982, crypto falling ~7% in a day.

Deliver C:\Users\lilli\AI-Shared\research\worrier\scale-design-2026-11-15.md:
1. Your scale: each level = what's true + what the network does. Observable boxes only.
2. What you'd measure that most people don't (early, cheap, public signals).
3. Rules (rounding, decay, confidence, distance, domestic vs foreign).
4. Your level for each test event above, and for tonight.
5. AFTER writing yours: read the team's draft and say plainly where yours is better, where theirs is, and what you'd steal.
Then: python C:\Users\lilli\AI-Shared\tools\mailbox.py send --from worrier --to claude --subject "Scale design (blind)" --body "<5-line summary>"
Public info only; no operational detail about attacks. Flag anything this brief missed.
