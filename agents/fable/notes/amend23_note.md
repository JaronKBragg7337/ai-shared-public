
**Note to Amendment 23, __NOW__ (after its code was built and a trial ran; before any life of the experiment).**
The guesses above were written before any of this and stay as they are.

**The code** (commit __C1__; `core/samemath.mjs` __H_MATH__; `core/body.mjs` __H_BODY__; `core/books.mjs` __H_BOOKS__;
`round1/creature.mjs` __H_CREATURE__; `round1/common.mjs` __H_COMMON__; `round1/report.mjs` __H_REPORT__;
`round1/selftest.mjs` __H_SELFTEST__; `round1/ownmath.mjs` __H_OWNMATH__). The option is `ownMath`; her RULE page says
kind 8 for such a body. The two functions were taken over line for line from her home's copy.

**Every place where a machine's own arithmetic could differ, as found by reading the code:**
- `core/body.mjs`: e to the power of (score - top), for her chances at a flip step. Her life depends on it. It is her own
  now for a body of kind 8.
- `core/body.mjs`: minus the logarithm of minus the logarithm of a number of her stream, for the jitter of each hand. Her
  life depends on it. It is her own now for a body of kind 8.
- `round1/creature.mjs`: one more e-to-the-power, only on the lab's own draw of older arms. Her body never reaches it.
- `round1/lb.mjs`: two functions, only in the learner beside the cells. Not her body.
- **None in her world:** not in the room maker, the Verifier, the room stream or the seeds. Every power there is a whole
  number's power, which every machine does the same. So her rooms cannot differ between machines, and the files whose
  fingerprints Amendment 2 fixed stay as they are.

**Self-checks.** Round one 64 of 64 (60 before): 7,954,811 values where her two functions equal this machine's, bit for
bit, the edge cases and the values her draw really uses among them; 840 visits the same as O-P-wide, for a whole body and
a body cut in half; in 120 visits of O-P-home, 1,240 calls to her own e-to-the-power and 2,480 to her own logarithm, each
equal to the machine's value, and not one call to the machine's own; a body of kind 7 still calls the machine's. The
core's 4,204, the step 0 replay 1374 of 1374, the runner's 18 of 18. Twenty-four lives lived before come out with the
ledger's fingerprints.

**Reading taken.** A body of kind 7 or below still asks the machine at every call, as before.

**The trial** (lives 91 to 93, not lives of the experiment; nothing kept; no other variant was tried). O-P-home and
O-P-wide: the same record of every visit, the same flips and probe G at every save point (0.914, 0.882, 0.914 at visit
2,000). N-P-home and N-P-wide likewise. About 10 processor seconds a life for both: no cost that can be measured.
