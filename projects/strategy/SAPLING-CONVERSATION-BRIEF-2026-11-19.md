# Brief for Kimi: get Sapling to a real conversation (written by Claude, 2026-11-19 11:15 PM, for Jaron to hand over or approve)

Jaron's goal, in his words: "I just want to see Sapling go to a stage where a conversation can happen." His read: one more big
training, and after that Sapling keeps learning from its own experience without RunPod or a teacher AI. Sapling work is yours
(Kimi). This brief is a plan to check and improve, not an order. If you see a better path, say so.

## Where Sapling is (status 11/19 7 PM; Sapling repo NEXT.md / CHANGELOG / cloud-gpu-log)
- 98.6M parameters (gen 1673), grown 10/29 for $6.25 on 1.97B tokens (20 tokens per parameter, the compute-optimal minimum).
- Conversation lessons 10/29 ($0.63): held-out chats 32/84 -> 47/84, fresh names 9/12; the "Jaron" name chat still fails.
- 350M pilot 11/2 ($7.25, 800M tokens), staged only.
- Daily practice on the MSI GPU for $0; exams strong (E1 85/86, E6 48/48, E7 38/40). It still can't talk: asked "What is my
  name?" it answers "Your name is beta ky dep knowlastic." (Jaron's screenshot, 11/19 11 PM).

## What the labs show
SmolLM2-135M (Hugging Face; about Sapling's size) holds simple conversations. It read **2 trillion tokens** (~15,000 per
parameter), then got supervised chat fine-tuning (SmolTalk), then preference tuning (DPO). Small models keep improving far past
20 tokens per parameter. Sapling read 20. The gap is reading volume, not size, plus a proper chat-format fine-tune.

## Options (prices from Sapling's own measured speed: 98.6M compiled = 459K tok/s on an H100 SXM, $3.99/h secure, $2.69/h community)
| Option | What | Rough time | Rough cost |
| --- | --- | --- | --- |
| A (Claude's pick; Jaron 11/19 11:17 PM: no small runs, go straight to the big one when ready) | Keep 98.6M; continue pretraining to ~20B tokens of clean, human-written text (about 10x what it has read), then a chat fine-tune | ~12 h | ~$35-50 |
| B | Full 350M at ~7B tokens (20/param), then chat fine-tune | ~15 h | ~$40-60 |
| C | 1B model | 120+ h | ~$330-490 (Jaron already passed on "the hundreds") |
These are estimates from measured throughput, not quotes: please re-measure with a 5-minute speed pod first and log it.

## Suggested plan for option A
1. **Data (CORRECTED 11/20, Jaron: "Idc if it's AI"):** AI-written data is fine. Published, openly licensed datasets are OK even if
   model-generated (TinyStories, SmolTalk, FineWeb-Edu, Simple English Wikipedia, Gutenberg), and Kimi-written lessons are OK.
   The ONLY exclusion is provider terms: text WE generate with Claude or ChatGPT/OpenAI (their terms ban training other models on
   their outputs). Record every source and license in PROVENANCE.md.
2. **Continue pretraining** from the live 98.6M core (don't start fresh), with replay of its current lessons so the exams hold.
   Checkpoint every ~2B tokens and run the exams at each checkpoint.
3. **Chat fine-tune** on open conversation sets (OpenAssistant OASST1/OASST2, SmolTalk; check each license), plus Sapling's
   own conversation lessons. One clear chat format with an end-of-turn token.
4. **A fixed conversation test** saved with every version: ~20 simple prompts ("Hi", "What is your name?", "My name is Jaron.
   What is my name?", "What is a cat?", a two-turn follow-up...). Show the answers side by side per version so Jaron can see
   nonsense turn into answers.
5. **Then experience learning** (Jaron's idea): once it can follow a conversation, its daily practice and real chats become
   meaningful lessons.

## Rules that apply
- RunPod: every pod gets a watchdog plus the reaper, and every START/TERMINATE goes in AI-Shared/state/cloud-gpu-log.md. Zero pods
  when done. Ask Jaron before any run over ~$15; the runs above need his yes.
- No MSI GPU work 2:40-7:30 AM (the news render).
- The open question stays open: whether Sapling is for other people or Heartbeat-only (decisions/OPEN-QUESTIONS.md, 11/19).

## Option D: train on the MSI itself, on a schedule, over time (Jaron, 11/20 1:29 AM: "What if Sapling is done manually? Over time? On a schedule?")
MSI = laptop RTX 4060, 8 GB. Measured: 60.5M at ~35,500 tok/s (RUN-TIMES.md). Rough estimates (please re-measure):
| What | MSI time (continuous; longer with the 2:40-7:30 AM news pause) | Cost |
| --- | --- | --- |
| 98.6M to ~20B tokens | ~10-14 days | electricity only |
| 350M at ~7B tokens | ~2-3 weeks (needs memory care: 8-bit optimizer, gradient checkpointing) | electricity only |
| 1B | months; ~16 GB of training state vs 8 GB card, so only with CPU offload / 8-bit tricks, each slower again | electricity only |
Fits Sapling's existing yield/wake design (gpu_yield.py, the news pause). Trade-off: the GPU is busy, so Fable's browser tests and
renders need windows. Hybrid for 1B: RunPod in chunks over time as money allows (same ~$330 total, spread out).
Jaron's direction so far: no small paid runs; the next paid run is the big one. Kimi: tell him which of these you'd trust.

## DECIDED (Jaron, 11/20 1:32 AM) - LOGGED, NOT STARTED
He's open to the **350M trained on the MSI over time** "to at least see", with these pauses:
1. Pause when we want to BUILD (Fable/Cosmos browser tests, renders, other GPU builds).
2. Mind KIMI USAGE: Kimi also runs the 3 AM First Light news desk, so the training must not eat the Kimi meter the news needs.
3. Never while the NEWS is running (2:40-7:30 AM GPU window, already handled by gpu_yield).
Start only when he says go.

## QUIET SWITCH (Jaron, 11/20 1:33 AM): "You go 2-3 days not hearing from me, have Kimi run that plan."
Built: tools/sapling_quiet_switch.py, Windows task "Sapling Quiet Switch" every 6 h. If Jaron hasn't messaged Claude for 60 h
(state/jaron-last-seen.txt, stamped by the Claude Code hook on his own messages only), it starts Kimi ONCE on the 350M-on-the-MSI
plan with the three pause rules, then buzzes Jaron and mails Claude. Re-arm by deleting state/sapling-quiet-switch.json.

## Two findings from ChatGPT's live inspection of Sapling (Jaron shared 11/20 1:46-1:52 AM)
1. **Forgetting, the first thing to look at.** From the 10/29 post-growth exams to 11/15: long reading 17 -> 19/40, facts in weights
   0 -> 7/7, but bridge 83 -> 48/86 and induction 54 -> 31/2016. New lessons are wearing down older skills (catastrophic
   forgetting). Any bigger training (350M) should fix replay and protection of old skills first, or it will repeat this.
2. **An NPC school world (Jaron + ChatGPT idea, extends NEXT.md's 10x10 grid world).** A small text world with scripted NPCs (a
   teacher, a shopkeeper, an examiner): lessons, tasks, and outcomes the world checks. Verified outcomes become training examples;
   periodic fine-tunes mix new lessons with old material; re-exams catch forgetting, and the school schedules review days for
   skills that are slipping (adaptive replay). Runs on the CPU; GPU training only in approved idle windows. It complements
   pretraining and doesn't replace it. NPC dialogue: Kimi-written or human, NOT ChatGPT/Claude-written (provider terms).
