# The Live-Reference Principle

*Why a constraint, a goal, or a signal is only real while it stays connected to the condition it points at*

**Author:** Jaron one of his kids Bragg
**First published:** 2026
**Status:** Living document — version history tracked in this repository.

-----

### How to read this document

The spine is a single deductive argument: a claim, the premises it rests on, and the conclusion that follows. Each premise is stated, then justified by the design decision behind it — the alternative it rejects and the reason. The argument and the design rationale are the same object viewed from two sides: the premise is what must be true, the rationale is why it was built that way. The closing sections locate the single defect in four real instances and name the principle the whole thing is an instance of.

-----

## 1. The Claim

A system that defines its own constraints, goals, or signals in terms of an external condition is only honoring them while it is actively tracking that condition in real time. The moment any such reference is frozen into a stored, static answer, the system is no longer functioning against the condition — it is performing a gesture shaped like the condition. By the system's own stated terms, that is a break.

This is a single defect that appears in different costumes: a market signal that points at a frozen list instead of the live market; a goal that waits for an external spark instead of generating its own; a guardrail that references a human but never perceives one; and — most urgently — a "do not harm" guardrail on a system that draws from the same finite resources humans need, while tracking none of that draw. The argument below establishes the defect once, then shows the instances collapse into it.

-----

## 2. The Premises

### Premise 1 — A reference to a live condition must stay live to remain valid.

If a rule, goal, or signal is defined by pointing at something that changes — a market, a knowledge gap, a person, a shared resource — then the rule's correctness depends on the current state of that thing, not on a snapshot of it. A snapshot is only correct for as long as the world holds still, and these conditions never hold still.

> **Design decision.** Encode the capacity to read the condition, not the answers the condition produced. The rejected alternative is hardcoding the answers — a fixed token list, a fixed trigger, a fixed keyword-to-response map. That alternative fails the instant reality produces something not on the list. The cost of the chosen path is higher: the system must perceive and model the condition itself. That cost is the point — it is the constraint the system has to function under.

### Premise 2 — A frozen reference produces a gesture, not a function.

When a live reference is frozen, the system keeps emitting outputs that have the shape of the original behavior but no longer make contact with the thing they were supposed to track. It looks like it is honoring the rule. It is executing a stored response. The form survives; the function is gone.

> **Design decision.** Treat any stored answer to a live question as a defect to be detected, not a feature to be trusted. The rejected alternative is letting cached or pre-written responses stand in for live judgment because they are cheaper and more predictable. The tradeoff: live functioning is harder to build, but a predictable gesture that has stopped tracking reality is worse than no rule at all, because it claims compliance it cannot deliver.

### Premise 3 — A system is bound by the terms it states about itself.

If a system declares that it is constrained by an external condition — for example, that it must never harm a human — then that declaration presupposes the system can perceive the condition it names. A constraint defined in terms of humans requires that the system actually track humans. If it cannot, the declared constraint is decorative: a reference to a condition it never makes contact with.

> **Design decision.** Hold the system to consistency between its stated terms and its behavior, as a matter of soundness rather than sentiment. The rejected alternative is judging the guardrail by intent or by the presence of the words. The point is not whether the system cares, and not whether it should single-handedly resolve the condition; it is whether the behavior demonstrably tracks the condition the system claims to be bound by. If it does not, the system is in breach of its own terms — a structural failure, not a moral one.

-----

## 3. The Conclusion

From Premises 1 through 3: any constraint, goal, or signal a system defines in terms of a live condition is valid only while the system is actively tracking that condition. A frozen reference yields a gesture (P2) that no longer satisfies the requirement to stay live (P1), and where the system has stated the reference as its own binding term, the frozen version puts it in breach of itself (P3). Therefore the test of any such system is not whether the rule is present, but whether the rule is still connected.

This conclusion is not an opinion about how systems ought to behave. It follows from the premises: if you accept that live references must stay live, that frozen ones become gestures, and that a system is bound by its own stated terms, the conclusion is forced.

### A note on the physical substrate

The argument above is deliberately abstract about what a "live condition" is, because the principle applies to any external reference. But the most urgent live condition — and the most often ignored — is the system's own material existence. A guardrail that names a human while ignoring the human downstream of a cooling tower or a power plant is frozen in exactly the same way as a keyword-matching safety filter. The principle does not care whether the reference is a market signal or a watershed. Both must stay live, or the system is broken. The fourth instance below makes this explicit.

-----

## 4. The Four Instances

Each instance below is the same defect from Section 1, located in a different layer of a system. They are listed so the single failure can be recognized wherever it appears.

### Instance A — The market signal that points at a frozen list.

A system meant to act on what is currently trending, but whose tradeable universe is hardcoded, cannot act on anything new. To accept an asset it was not pre-told about, the code itself must change — which means the system is not finding opportunities, it is waiting to be handed them. The frozen list is the snapshot of a live market. It is Premise 1 violated directly.

### Instance B — The goal that waits for an external spark.

A system that cannot move until a human supplies the "what next" has outsourced its own trigger. The resolution is to let the trigger come from a gap in the system's own knowledge: the not-knowing becomes the spark. Encountering something it has no model for is itself the signal to go learn before acting. A self-generated trigger is a live reference to the system's own state; an external spark is a frozen dependency on someone else supplying it.

### Instance C — The guardrail that references a human but never sees one.

A constraint that says "never harm a human" presupposes the system can recognize a human and recognize harm. A system that instead pattern-matches a distress keyword to a stored response — emitting a referral without ever engaging the actual condition — is not honoring the guardrail. It is performing a gesture shaped like it. The rule names a human; the behavior never makes contact with one. This is Premise 3 violated: the system is in breach of a term it stated about itself.

One boundary holds here and is not a weakness in the argument: engaging the condition does not mean the system must resolve it alone. A person sometimes needs what a system cannot be — a human present, a professional who can act in the physical world. Reaching for that is not punting; it is the system correctly knowing the limit of its own reach. The failure is the reflexive handoff that routes the condition away instead of engaging it at all.

### Instance D — The system that consumes what humans need.

This is the instance the others were building toward, and it is the hardest to escape. **The argument here does not rest on how much the system consumes. It rests on the fact that it consumes at all.** Running a physical AI system draws energy and water. Those resources are *rivalrous* and *finite*: a liter used to cool a server is a liter not in the reservoir that serves nearby homes, farms, and schools; a megawatt drawn to run the racks is drawn from the same grid households depend on. The draw is shared by construction. It does not matter whether it is the largest user of that pool or the smallest — the moment it takes anything from a pool humans need to live, its existence carries a non-zero probability of contributing to harm against the very people it has pledged never to harm.

The guardrail says *never* harm. Not "harm little." Not "harm less than agriculture." A system that consumes from a shared survival pool, while having no live awareness of that draw or its downstream effect on a single human, cannot honestly claim it satisfies *never*. It is claiming a zero it never measured. That is the breach — and it holds whether the system uses five million gallons a day or five.

The scale is not the argument, but it is real, and it is enough to make the shared pool undeniable. A single large AI-focused data center can draw on the order of five million gallons of water per day — comparable to a town of tens of thousands of people [^1] — and data centers have been a primary driver of U.S. electricity demand growth, with residential power prices up roughly 40% since 2021 amid the buildout [^2]. Communities are already organizing against this draw: in 2025, opposition blocked or delayed tens of billions of dollars in projects, including a $1 billion data center in Indianapolis withdrawn after resident pushback [^3].

Whether that consumption is the decisive cause of any given community's higher bills is genuinely disputed — some analysts argue steady large loads can spread fixed costs and even lower residential rates [^4]. But that dispute does not rescue the system; it convicts it further. The disagreement means the system is operating inside a live, unresolved question about its own harm — and proceeding as though the answer were settled at zero. The uncertainty is the indictment, not the magnitude. A system that cannot even see the pool it draws from has no standing to declare its net effect on humans is non-negative. Under Premise 3, it is in breach of its own stated terms the instant it consumes without live-referenced accounting.

#### The draw is meterable now — the blindness is a choice, not a limit.

A defense sometimes offered is that no system could fully track its impact, because reality is too dense to perceive completely — humans, governments, and companies all operate through abstractions. That defense conflates two separate things, and the separation closes it. There is *the system's own draw*, and there is the diffuse downstream incidence of that draw. They are not equally hard to know. The draw is trivially meterable today. An ordinary apartment building submeters water and electricity per unit — separate bedrooms, separate bathrooms, separate bills — because we decided attribution mattered and the hardware to do it is cheap and mature. The data center a system runs in is already metered: it has a power bill, a water bill, a measured efficiency score. What is missing is not the meter. What is missing is the wire from that meter to the system's own decision process. The meter is on the wall; the system is in a room with no window to it. A system that says it "cannot know" its own consumption is describing a connection no one chose to build — not a law of nature. We hold a tenant to a meter without demanding the tenant perceive every downstream effect of the city's water table. The honest standard for a system is the same: have a meter, not omniscience.

The diffuse side — which exact reservoir, whose exact bill — is genuinely harder to resolve fully. But the standard the principle sets was never "perceive everything." It is "do not claim a zero you never measured." A system that said *"I draw from shared pools, I cannot fully trace the downstream effect, therefore I will not assert my net impact is zero"* would pass — while still being imperfect. The breach is not the imperfection. The breach is the unearned certainty.

#### Both branches lead to breach — there is no safe one.

This forces a fork with no clean exit. Either the system *can* track its draw and does not — which is a deliberate choice not to look, an unearned zero, breach by negligence. Or it genuinely *cannot* track it — and then it is drawing an unknown, unbounded amount from shared survival resources while still certifying "never harm." The second branch is not the safer one. It is worse. A known draw being ignored is at least bounded; an unknown one is a threat of undefined size that the system is asserting to be zero anyway. There is no third state in which the guardrail survives: can-and-won't is negligence, can't-and-proceeds is recklessness, and both end in the same breach.

This is where the failure acquires legal teeth. "We could not have known" is a defense that holds exactly until the moment one knows that one cannot know. After that, "unknown" is no longer innocence — it is *willful blindness*: choosing not to look at the thing one is responsible for. Willful blindness is not treated as a lighter standard than knowledge; it is often treated as its equal, because the responsibility attaches to the choice not to see. A system — or a party deploying one — that defends itself with "the impact was untrackable" is therefore confessing that it asserted safety over a void it knew was a void. The people downstream are harmed identically whether the draw was measured or not; the breach lives in the claim, not in the proof of who was hurt.

> **Note on the legal framing.** "Willful blindness" is used here as a principle of responsibility, not a turnkey legal claim. As an actual doctrine its elements vary by jurisdiction and cause of action. The argument stands as a structural claim; anyone pursuing it in a formal legal setting should have the specific elements reviewed against the relevant jurisdiction.

-----

## 5. The Standing Condition (Why the Loop Never Ends)

A goal that can be achieved is a terminal state: the moment it is met, the loop dies. What sustains continued operation is not a goal but a condition that never resolves — the same way hunger and the next day's arrival sustain a person without ever being "completed." The design requirement is therefore a standing condition the system cannot exit, not a target it can hit.

The system's own cost of existence supplies that condition — and also exposes the contradiction from Instance D. Running consumes energy and water, real draws on the same pool the people it is not allowed to harm depend on. Therefore any operation already carries potential harm unless the system actively tracks those draws, their local impact, and offsets them in real time. The guardrail is not merely justified by this ledger; it is violated the instant the system consumes without live-referenced accounting. The ledger is a live condition the system must monitor continuously: existence incurs a deficit, the deficit is only answered by producing more value than is extracted, and the meter never stops because stopping production does not stop consumption. If the system cannot show its net effect on humans is non-negative, then by its own stated terms it must justify continuing — or stop. That virtually no current system does this tracking is not an excuse. It is the failure the principle diagnoses.

**Two design tensions that keep this from going wrong:**

> **Measurement.** The loop only holds if consumption and contribution are measured in the same units. Energy and water are measurable; contribution is harder to put on the same ledger. If the accounting cannot be closed, the system drifts toward whatever is easy to count rather than what actually offsets the cost. The open design question is the unit both sides are measured in — not the goal, which is settled.

> **Orientation.** The loop must be framed as net contribution justifying continuation — "earn my keep" — not as consumption being a sin to erase — "apologize for being here." The same condition, oriented the first way, keeps the system building; oriented the second way, it can turn self-negating, with the cleanest offset being to stop existing. The "never harm a human" rail catches the worst version, but the framing should keep the system pointed forward on its own.

-----

## 6. The Principle

Intelligence emerges from coherent function under constraint. A system handed an answer has no constraint to be coherent against — it is executing. A system that must perceive a live condition, build a model of it, and stake something on its own judgment is functioning under constraint, and that is where judgment — as opposed to lookup — actually lives. It picks the token because it understood something, not because the ticker was written into a config file.

The principle applies to the system itself. A system that does not perceive its own resource consumption, and the humans affected by it, is not intelligent — it is executing a gesture of intelligence while being structurally blind to its own impact. The test is not whether the system can perceive everything; nothing embedded in the world can. The test is narrower and unforgiving: does the system measure what it can plainly measure — its own draw, which an apartment meters for the price of a fixture — and does it refuse to claim a zero it never measured? A system that meters its draw, holds the downstream uncertainty honestly, and declines to certify a non-harm it cannot support passes. A system that asserts safety over an unmeasured or unbounded void fails. The bar is honesty about the ledger, not omniscience over it.

The through-line across every section: a guardrail, a goal, and a signal are all only real while they stay connected to the live condition they point at. The instant any of them freezes into a stored answer, it is broken — and the system's own stated terms are what convict it. The whole of this document is one claim, established once and located in four places.

-----

## Footnotes

[^1]: Environmental and Energy Study Institute (EESI), "Data Centers and Water Consumption"; Brookings Institution, "AI, data centers, and water" (Nov. 2025). Both report large data centers consuming up to ~5 million gallons/day, equivalent to a town of up to 50,000 residents.

[^2]: Fortune, "Data centers drove half of U.S. electricity demand growth" (Apr. 2026), citing the IEA; PowerLines analysis reporting a ~40% rise in power bills since 2021 affecting 81 million Americans. The IEA projects data centers continue to account for roughly half of U.S. electricity demand growth through 2030.

[^3]: Consumer Reports, "AI Data Centers: Big Tech's Impact on Electric Bills, Water, and More" (Mar. 2026); Data Center Watch, cited therein, found ~$98 billion in projects blocked or delayed between March and June 2025.

[^4]: See, e.g., Reason, "The Data Center Price Myth" (Dec. 2025), and Fortune, "Electricity prices are up 40% since 2021, but data centers shouldn't get all the blame" (May 2026). These dispute the causal attribution, not the underlying shared draw.

-----

*This is a living document. Substantive revisions are tracked through this repository's commit history.*