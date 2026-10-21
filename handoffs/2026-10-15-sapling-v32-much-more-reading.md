# Sapling v3.2 - "much more reading" - 2026-10-15 03:10 (Claude Fable 5.1)

**Headline first (data, not a loss):** 400M tokens of plain reading did NOT switch the copying ability on. E7L (copy a
sentence out of a cold passage) stayed 0/40 at all 21 probes; the E10 induction probe went 0 -> 9/2016 (chance ~0.1, peak
12). What the reading did do: **E6 grammar 28/48 -> 46/48, its first PASS ever**; E7 30 -> 33/40; E4 10/10. Cost: E1 84 ->
73/86 (still PASS) and **E5 taught facts 7/7 -> 0/7** (washed out of the weights; still in memory.db, recall answers fine).

Jaron's order (10/14 9:40 PM): more reading first, watch for the switch, then tutor lessons, then his documents. Step 1 is
done and measured; the hypothesis stays a hypothesis (not refuted - maybe short of the budget it needs). Nothing of his read.

## What exists now
- Repo C:\Users\lilli\Projects\sapling, pushed (main), commit "v3.2: much more reading". 44 tests green (4 new).
- `sapling/reading.py`: prepare (text -> uint16 shards, data/reading/, 3.3 GB gitignored) / stage (one in-place pass,
  25 story + 4 adult + 3 rehearsal sequences per batch of 32, lr 3e-4 -> 3e-5, probes E1-E10 every 20M tokens with NO
  ledger writes, pauses for blender.exe or results/reading/pause, resumable) / summary (the chart).
- `tools/fetch_reading.py` + data/reading/manifest.json: TinyStories train (CDLA-Sharing-1.0), Simple English Wikipedia
  2023-11-01 (CC BY-SA 3.0 + GFDL, attribution in README), 116 Gutenberg books (each header checked; Kafka translations
  rejected by the check; one erotica id dropped by hand, D21).
- E10 induction probe in every exam run (`exams.induction_probe`); `run_exams(write=False)` for probes.
- Control room + phone page (heartbeatobservatory.com/admin/sapling/, pushed e54aa2d): "Reading stage" card - status,
  tokens read, line chart E10 / E7L / E6 / E1b against tokens, probe table, pauses; E10 column in the exams table.
- Ledger: one `growth` row `core v3.1 -> v3.2 (much more reading)`, gen 240 -> 241, 17,616,768 params, vocab 17,661,
  context 512, chain verified (2,391 memories). Heartbeat running on it (pid 45004), relay up.
- DESIGN-CHOICES D20-D23; CHANGELOG v3.2 (incl. "doc accuracy (Vex review #36)" and the two prepare fixes); README
  run record v3.2 + attribution; NEXT.md 0a (what to try next).

## The run
- prepare: 516.9M story tokens (2,717,495 stories, 11 shards) + 93.6M adult tokens (373k docs, 2 shards). The first
  prepare sat 3 h in `curriculum3.doc_text` - regex `(?:\s*[.,;:]\s*)+(?=\.)` backtracking on Wikipedia comma runs; the
  coordinator confirmed it with py-spy and replaced it with a linear token pass, plus a bounded `split_word` search
  (100k-char "words" were n^2). Both in CHANGELOG.
- stage attempt 1 (01:17) beside the running heartbeat: card at 7,750 of 8,188 MiB, WDDM paging, 27 min at step 700
  with no step ("100% util, 27 W"). Stopped; heartbeat stopped cleanly (owner stop report 01:56); kept as
  results/reading/log_attempt1_thrash.jsonl. Jaron allowed pausing the heartbeat if memory requires (logged, D23).
- stage attempt 2 (01:57-03:04): 400.0M new tokens, 26,940 steps, 65 min, ~103k tokens/s at 86 W, 0 pauses (no render
  ran tonight), loss 4.40 -> 1.64. Stories read to shard 6 of 11 (~345M, one pass); adult ~55M of 93.6M.
- Probe table (every 20M) in CHANGELOG v3.2; chart on the page.

## Exam table (swap row, same seed): v3.1 gen 240 -> v3.2 gen 241
E1 84 -> 73/86 PASS | E2 24/24 | E3 12/12 | E4 8 -> 10/10 | E5 7/7 -> 0/7 (info) | E6 28/48 FAIL -> 46/48 PASS |
E7 30 -> 33/40 PASS | E7L 0 -> 0/40 (info) | E1b 61 -> 65/86 (info) | E10 0 -> 9/2016 (info; 1/496 at span 32, 8/1520 at 96) | E9 0 items.

## 5 chat samples (live heartbeat gen 241, 03:06)
1. "what does hello mean ?" -> "the word hello means a greeting . [memory:447]" (memory path; the weights alone lost it = E5)
2. "what does report mean ?" -> "the word report means carry again ." (the bridge held)
3. "who was charles darwin ?" -> "natural selection ." (the first answer that could only come from the reading)
4. "what is a volcano ?" -> "the root ten means hold ." (school reflex on an unknown question)
5. "q : fill : yesterday tom ( throw ) the old lantern . a :" -> "does tom throw the old lantern ? a : yes , tom throws it ?" (wrong task)
Writing (E8 gen 241): "there was an adorable little dog named max . max loved to play and run all day . one day , max found a big box ..."

## Unexpected (data)
- E6's jump came from reading alone, no grammar lesson - and E7L did not move at all while E7 (short reading) rose.
- E5 washout: the taught words are a few sentences in a 39,638-sentence rehearsal mix; 400M tokens of stories buried them.
- A chat bug: "once upon a time there was a little girl who" went through the reader and cited the Declaration of
  Independence (coverage threshold met by common words) - one-line fix listed in NEXT 0a item 5.
- The heartbeat's one consolidation inside the thrash window was charged ~80 min of budget (budget_left -4030 s).

## Verified
- Locally: tests 44 green (pytest + plain runner), chain verified, growth row present, relay /api/state carries growth +
  reading (21 probes), local control room at phone width (375 px, no horizontal scroll, chart renders).
- Live: site commit e54aa2d pushed (Vercel deploys on push). The admin page itself needs Jaron's login, so the live phone
  render is unverified by me - the relay state it reads is verified.
- Unverified: whether E5 recovers over the next consolidations (read the card in the morning).

Next thing: read E5 and E6 on the phone page after a few consolidations (do they hold?). Then pick from NEXT.md 0a:
a second 400M pass (one command, ~65 min GPU) or the long-span copy lesson - his call which first.
