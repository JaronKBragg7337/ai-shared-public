# Why Sapling is struggling — read-only diagnosis

**Date:** 2026-11-01  
**Trainer:** Kimi  
**Question:** Is something missing, or is there a reason Sapling is struggling?

## Bottom line

Sapling is **not mainly struggling because its model is too small or because it has not read enough text**. It has already shown that it can learn these skills. The stronger explanation is that learned skills are being lost or diluted, and two useful connections are missing:

1. Long-reading practice was accidentally switched out of everyday training, and the score then fell.
2. The fresh 98.6M model started by forgetting the taught facts; those few facts are now greatly outnumbered by Sapling's own generated notes.
3. An ordinary sentence such as “My name is Jaron” is not saved into long-term memory. Sapling is relying on a weak short chat history instead.

So this is mostly a **retention, data-mix, and memory-wiring problem**. More identical heartbeat training is unlikely to repair it by itself.

**Scope:** I read the latest exam report and history, today's real chat record, recent stop reports, the heartbeat log, the training code and logs, the data manifests and mix, checkpoint details, and the memory database in read-only mode. I did not train anything or stop/restart anything. The memory record's integrity check passed: no broken chains in 20,349 memories, 63,764 recall events, one document record, or 76,969 ledger entries at the time checked. `SWAP-PLAN.md` was not present in the project; I reviewed the available swap logs and the growth/swap event instead.

## 1) What is going well

Latest formal exams, from generation 1546 at 08:02 today:

| Plain exam name | Latest score | What it says |
|---|---:|---|
| Word parts prefixes | **85/86** | Excellent on the practiced word-building format |
| Word parts recall | **23/24** | Very strong, though it can wander instead of giving a short answer |
| Grammar | **47/48** | Excellent on the short, familiar grammar frames |
| Reading a short story | **38/40** | Strong on simple passages with only a few people and facts |
| Long reading — copy a sentence from an unseen passage | **9/40** | Weak and much worse than its earlier best |
| Facts it was taught, held in its weights | **1/7** | The facts remain in memory, but mostly not in the model's weights |
| Remembering a name | **9/12** | Better than before, but below the 10/12 passing mark |

The name score of 9/12 is from the latest saved formal conversation test on October 29, not from today's weights. Today's live chat is the more current warning:

| What Jaron said | Sapling's answer | Reading |
|---|---|---|
| “Hello sapling” | “Hello zoe asks the young tree.” | Short and no longer looping, but not a sensible greeting |
| “My name is Jaron” | “Your name is solved.” | It did not acknowledge or retain the name correctly |
| “What is my name?” | “Your name is beta ky dep knowlastic.” | It invented a name rather than using the prior turn |

Other good signs:

- The older model's roughly 100-times “Jaron” loop is gone. Answers are shorter now, although still unreliable.
- The model reached **22/40 on long reading** immediately after the 98.6M growth run. Its separate long-reading test on unseen documents reached **514/1000**. This proves the current size can learn useful copying behavior.
- The short-story and grammar results show real learning within those formats. They are not evidence that the whole system is broken.
- Checkpoints, exams, owner stops, and restarts are being recorded. Recent stop reports were planned owner/GPU-render stops, not unexplained self-crashes.

The important caution is that the high scores are mostly on **narrow, rehearsed formats**. They do not yet carry over to flexible, natural chat.

## 2) The top three likely reasons for the weak spots

### 1. Long reading: its special practice was silently dropped from consolidation

This is the clearest fault I found.

The conversation-training run did not carry forward the marker saying that the model had received long-reading training. The current checkpoint has that marker set to empty. The backup check looks for the exact phrase “long-reading lesson” in the model label, but the new label says “long-reading interleaved” instead. As a result, the heartbeat treats this as a model that never had the lesson.

| Evidence seen | Why it matters |
|---|---|
| Generations 1397 and 1398 used **20% long-reading replay** in each consolidation batch | The learned copying skill was being rehearsed |
| Generation 1400 onward used **0%**, including all the latest consolidations inspected | The exact skill is no longer being maintained |
| Long reading was **22/40 at generation 1398**, then **16/40 at generation 1399**, and is **9/40 now** | The decline followed the replay loss and continued consolidation |
| The separate “copy a sequence just seen” probe fell from **60/2016** around the growth swap to **14/2016 now** | The more basic look-back/copy behavior also weakened |

There is also conflicting practice: everyday consolidation includes older, shorter school reading formats while omitting the special long-reading lesson. Earlier project tests already showed that this kind of mismatch can wear the newer skill away.

**Conclusion:** the first fix is to restore the missing training link and verify the replay share, not to buy a larger model.

### 2. Taught facts: the fresh model wiped them, and the current mix makes them hard to relearn

The facts themselves are not gone. All seven are still intact in the memory database as user-taught memories. The problem is getting them to stick in the weights.

| Evidence seen | Why it matters |
|---|---|
| The older 60.5M model scored **6/7** just before growth; the fresh 98.6M model scored **0/7 immediately afterward** | The fresh training reset a working ability rather than improving it |
| The fresh growth mix had long reading, stories, adult text, web text, conversation, and school — but no protected user-fact replay | Forgetting at the swap was built into the recipe |
| It had previously reached **7/7** on October 27 | A smaller model could hold these facts, so size is not the main barrier |
| The latest consolidation trained on **2,750 self-generated memories versus only 7 user-taught facts** | Human-taught facts are a tiny part of the fact pool |
| Only 25% of the latest batch was school plus facts; reading and conversation took the other 75% | The seven facts receive still less of the total training attention |
| Current answers include placeholders such as “the word `<m3>` means `<m4>`” and unrelated word definitions | The model has learned the answer shape without reliably attaching the right fact |

Sapling also saves its own free-generated text as unconfirmed memories and trains on them again. Recent examples include repeated story fragments and malformed statements such as “the root cred means break.” That creates a noisy feedback stream which can crowd out the few correct human facts.

**Conclusion:** facts need explicit, protected rehearsal through growth and consolidation, with less competition from unreviewed self-output. Simply running more of the present mix is as likely to reinforce the noise as the facts.

### 3. Holding a name in live chat: ordinary chat is not wired into lasting memory, and the short-term model is still weak

There are two separate issues here.

First, the chat system only writes a memory directly when someone uses the explicit `/teach` command. Normal conversation is searched against memory, but the new sentence itself is not saved there. The database contains **no Jaron/name memory at all**. Its only seven user memories are the old “the word … means …” facts from October 14.

Second, Sapling does have a temporary chat history of up to six turns, so the name should have been available during today's short exchange. Its failure shows that the model's use of that history is also unreliable.

| Evidence seen | Why it matters |
|---|---|
| “My name is Jaron” did not create a persistent name record | A restart or `/new` would lose it anyway |
| The next live answer invented “beta ky dep knowlastic” | Even the temporary in-session history is not being used dependably |
| The main practice set has 8,000 template conversations using only **24 names**, mostly two-turn exchanges | It has limited variety in names, wording, delays, and distractions |
| The formal test scored **9/12**, below its 10/12 pass mark, and **0/12** for “what did I just say?” | The weakness existed before today's chat |
| The formal test uses greedy, core-only answers; live chat uses sampled answers with memory routes | A good formal score would not guarantee the same result in the real chat path |

**Conclusion:** a direct, durable memory path for user facts is missing, and the model also needs more realistic multi-turn practice. Either alone would leave part of the problem in place.

## 3) What is missing

| Area | What is already present | What is missing or not working well |
|---|---|---|
| Reading data | About 1.41B tokens in the local reading shards; the fresh run processed about 1.97B mixed tokens | Not more raw prose. The missing piece is reliable retention of targeted skills |
| Human-taught data | Seven old word facts and Jaron's self-description lessons | Recent owner facts, names, preferences, natural multi-turn chats, varied phrasing, and delayed recall with distractions |
| Model size | **98,584,320 parameters**, 12 layers | No evidence that another size increase is the first need; the 60.5M model previously held facts better |
| Context length | **512 tokens**, enough for the present passage-plus-question design | Not the main limit. Live chat keeps only six turns, and long answer generation has a separate cap |
| Long-term memory wiring | Append-only memory, retrieval, citations, and `/teach` | Automatic capture of ordinary user facts such as names, plus a reliable way to answer directly from those facts |
| Skill retention | Reading and conversation replay in every consolidation | Long-reading replay after the conversation swap; protected user-fact replay through fresh growth and later folds |
| Exam-to-chat connection | Narrow school exams and a synthetic conversation test | A recurring test through the exact live path, with real names, varied wording, sampling, interruptions, and current weights |
| Owner-specific evaluation | A place for Jaron's own questions | The owner's exam is still empty, so it cannot catch failures on his actual documents and requests |
| Data-governance record | A detailed provenance audit | Agreement between that audit and the files currently present and read by training code |

## 4) Three concrete next steps, ranked by value against cost

These are recommendations only; none was run during this diagnosis.

| Rank | Step | Why it is worth doing | GPU time and rough cost |
|---:|---|---|---|
| **1** | **Repair the wiring and measurement before any retraining.** Carry the long-reading marker through conversation runs and prove that replay returns to 20%. Save ordinary user facts such as names into memory and answer direct recall from that record. Raise the long-reading answer cap. Add a live-path chat test using Jaron and several new names, with a distracting turn in between. | Highest value for the least spend. It addresses the exact long-reading and name faults, and prevents the exam from hiding part of the problem. | **No training GPU.** Mostly CPU/code review and tests. Roughly 10–20 minutes on the local GPU to rerun evaluations. |
| **2** | **Run one controlled retention experiment on a copied checkpoint and copied memory, not the live individual.** Restore long-reading replay, explicitly rehearse the seven user facts, and reduce or pause unreviewed self-generated training text. Compare five normal consolidations against the current scores. | This tests the actual repair before spending on a cloud lesson. It should show whether facts and long copying can both recover without losing grammar and short reading. | **Needed.** About **45–75 minutes on the local RTX 4060** for five folds plus before/after checks, based on recent 7.5–8.2-minute folds. A rented GPU is unnecessary for this test. |
| **3** | **If the retention test shows the recipe works but the skills remain weak, run a focused refresher on reviewed data.** Emphasize exact long-span copying, realistic multi-turn name/object recall, and protected user facts, while replaying every existing skill. Do not start another fresh 2B-token growth run yet. | Useful only after the wiring is fixed; otherwise the next heartbeat phase can erase the new gain again. | **Needed if step 2 is insufficient.** Roughly **45–90 minutes on one H100**, about **$3–$6 at $3.99/hour**, plus setup. Earlier comparable lessons took 50–79 minutes. Data review/preparation is separate CPU/human time. |

I would **not** make a larger model or a 1024-token context the next purchase. First show that the 98.6M model can retain what it already learned.

## 5) Anything that looks broken

| Item | Status and evidence |
|---|---|
| Long-reading replay detection | **Definitely broken.** The conversation checkpoint lost the training marker, the label fallback does not match, and replay is 0%. |
| Long-reading exam answer limit | **Definitely too small for three questions.** It allows 44 new tokens, while three expected answers contain 46, 50, and 55 whitespace-separated words before any subword splitting. Even a perfect model could score no more than 37/40 on this version. This is not the cause of the 9/40 score, but it contaminates the measurement. |
| Ordinary chat memory | **Missing, not merely weak.** Normal chat does not save “My name is Jaron” as a user memory; only `/teach` writes directly. |
| Provenance versus live files | **Records disagree.** `PROVENANCE.md` says several datasets were quarantined, but the quarantine folders currently contain no files and the same datasets are present at their original active paths. The current consolidation code reads those active paths. Reconcile this before another training run. |
| `SWAP-PLAN.md` | **Not found.** No file with that name exists in the project. The available growth swap event and stdout logs were readable. |
| Heartbeat log | **Very noisy.** It was about 25 MB and 398,000 lines during inspection, dominated by repeated browser-disconnect stack traces from the control room. This is not causing bad answers, but it makes real errors harder to find. |
| Owner's own exam | **Empty.** It provides no protection against regressions on Jaron's real needs. |
| Negative daily budget | **Not itself a bug.** The project deliberately allows work after the budget reaches zero and records the overspend. The latest negative number should not be mistaken for the cause of the quality problems. |
| Memory database | **No corruption found.** The read-only hash-chain check passed. The issue is what is or is not being stored and later trained, not a broken database. |

### Final judgment

There is no single missing magic ingredient. Sapling has enough model and enough general reading to demonstrate the wanted abilities. The immediate work is to **stop losing skills, protect the small amount of human-taught truth, and connect ordinary conversation to memory**. Fix those links first, measure through the real chat path, and only then pay for more training.
