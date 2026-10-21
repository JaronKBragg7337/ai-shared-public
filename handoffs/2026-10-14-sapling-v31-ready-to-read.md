# Sapling v3.1 - ready to read documents (prerequisites for step 2) - 2026-10-14 night (Claude Fable 5.1)

Jaron 8 PM: "your call boss" on NEXT.md section 0. Repo C:\Users\lilli\Projects\sapling (pushed, main); phone page
heartbeatobservatory.com/admin/sapling/ (E7L / E1b / E9 columns, "Documents it has read" card).

What was built (DESIGN-CHOICES D16-D19, CHANGELOG v3.1)
- Same individual, grown IN PLACE: the v3 weights got new vocab rows + context 256 -> 512, then level-3 school
  (copy, bridge, prose/docs/longread on public-domain Gutenberg nonfiction). Two `growth` ledger rows
  (gen 178 -> 179 swap A, gen 182 -> 183 swap B "reading drill"); memory.db + chain intact (schema change: `documents`
  table + doc/passage columns, old rows hash as before).
- Vocabulary 3,098 -> 17,660 = old ids kept + 6,000 story words + document words + 1,037 word pieces ("##"): any adult
  word is spellable, E1-E7 stay comparable. "report" is always `re ##port` (forced split = the bridge at token level).
- reader.py: `/read C:\path\file.txt` or `/read: <text>` from the chat -> passages in memory with provenance; questions
  a document covers go passages-first into the 512-token frame, answers cite [doc:N "title" passage K memory:M].
- Exams: E7L long reading (held-out essay, info), E1b bridge (info), E9 = owner_exam.json (his questions/answers/bar;
  empty = "0 items").

Numbers (v3 gen 178 -> v3.1 gen 183): E1 82 -> 85/86, E2-E4 held, E5 7/7, E6 12 -> 21/48 (FAIL vs .60 kept),
E7 25 -> 26/40, E1b 0 -> 83/86 (cold!), E7L 0/40 both swaps. Between the swaps three heartbeat consolidations drifted
E1b 81 -> 59 (watch it, D14). Retrieval demo on the Declaration of Independence (Gutenberg #1): the right passages are
found and cited; the answer is fluent prose, not the copied sentence = E7L. Chat routing bug found and fixed (a fact
sharing one word hijacked grammar/passage questions into "the word X means ...").

Step 2 still needs: Jaron's go; his documents as .txt on the MSI (/read one per file); E9 filled by him; long cold
reading is the weak leg (NEXT.md section 0, item 4) - more task passages never seen as prose, long-span copy tasks.

State: heartbeat running on v3.1 gen 183 (pid in results/heartbeat.pid), relay task up, 40 tests green, docs current.
Unexpected (data): the big core learned the training passages through the reading tasks (docs loss 0.12 even with
disjoint halves) instead of the copying; E6 misses now copy the wrong span instead of a habit object.

Next thing: read E1-E7 + E1b on the phone page over the next day (drift after consolidations on the 512 core);
if E1b slides under ~60 again, raise REHEARSAL3["bridge"] in consolidate.py.
