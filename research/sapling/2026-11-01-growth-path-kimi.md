# Sapling's growth path: general ability first

**Date:** 2026-11-01  
**Written by:** Kimi, Sapling's trainer  
**For:** Jaron (plain words; no coding knowledge needed)

## My recommendation in one paragraph

**Fix and measure the 98.6M model before buying a bigger one.** Its weak long reading followed a broken replay link, not proof that it ran out of brain capacity. The smaller 60.5M model also held some facts better, so size alone was not the cure. I have repaired the data and retention wiring and started a copied-checkpoint test. Next, build a broad, reviewed general-data pipeline and run small comparison experiments at 98.6M. If those show that the recipe retains skills but still leaves broad ability weak, **350M is the next sensible size experiment**, initially as a short pilot rather than a full run. **Do not fund 1B now.** It costs too much for the evidence we have, and the current $22 cannot complete a 350M Chinchilla-style run, let alone a 1B run.

## Retention result from this repair

The final all-Kimi run made five folds from a copied generation-1548 checkpoint in **23.5 minutes**. Every fold used exactly **20% long-reading replay** and excluded unreviewed self-notes. E7L improved **12→14/40**, E5 **2→6/7**, E1 **81→84/86**, E6 **46→48/48**, and E1b **74→78/86**. E7 stayed **37/40**. E10 declined **14→12/2016**, so the candidate is **mixed and was not installed**. This supports fixing 98.6M further before buying growth; it does not prove the recipe is finished. Full comparison: `results/teacher/retention_2026-11-01/final_comparison.json`.

## What labs actually do

Labs do not usually begin by training their largest model and hoping the data works.

1. **Try the recipe on smaller models.** Change one thing, such as a data filter or mixture, and compare held-out loss and downstream tests. A small failed experiment is cheaper than a large failed one. Promising small-model results still need confirmation at the target size.
2. **Pretrain on broad text.** This teaches language, facts, reasoning patterns, and different styles before assistant behavior is added. Data quality, deduplication, mixture, and evaluation matter as much as raw volume.
3. **Scale model size and tokens together when compute is limited.** The Chinchilla result gives the familiar reference of about **20 processed tokens per parameter**. It is a compute-allocation guide, not a magic finish line.
4. **Post-train the assistant.** Instruction tuning and preference training teach answering, following directions, and behavior. Identity and character can be added here instead of dominating the broad pretraining data.
5. **Keep checking earlier abilities.** A later lesson is not a win if it erases earlier reading, grammar, or chat skills.

| Research example | What it tells Sapling |
|---|---|
| [Kaplan et al., Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361) | Loss often improves smoothly with model size, data, and compute. This supports small scaling experiments, but does not promise that every skill scales automatically. |
| [Hoffmann et al., Chinchilla](https://arxiv.org/abs/2203.15556) | More than 400 models from 70M to 16B parameters showed that model size and training tokens should grow together for compute-optimal training. Chinchilla used about 20 tokens per parameter. |
| [Muennighoff et al., Scaling Data-Constrained Language Models](https://arxiv.org/abs/2305.16264) | In their experiments, up to about four passes over limited data lost little; more repetition gave diminishing returns. This was one research setup, not permission to repeat every corpus four times. |
| [FineWeb datasets](https://arxiv.org/abs/2406.17557) | The team used 1.71B ablation models on 28B and 350B tokens to compare data choices. It is a direct example of testing data pipelines before committing to large runs. |
| [Meta, The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783) | Meta tried data mixtures on small models before large training, used about 15T pretraining tokens, then did supervised and preference post-training. |
| [SmolLM2](https://arxiv.org/abs/2502.02737) | A fixed 1.7B model used about 11T training tokens, far beyond 20 per parameter. Modern small models may be deliberately overtrained when inexpensive inference matters. |
| [Anthropic, Claude's Character](https://www.anthropic.com/research/claude-character) | Character and identity-related behavior can be shaped during alignment fine-tuning after initial training. This supports leaving Jaron-specific identity work for a later, measured phase. |

**Important distinction:** “tokens processed” counts every training exposure, including repeats. “Unique tokens” counts different text after deduplication. Sapling needs both numbers in every run record.

## Is 98.6M worth fixing?

**Yes.** It has already produced 85/86 on word parts, 47/48 on grammar, 38/40 on short reading, and 22/40 immediately after long-reading growth. Those are narrow tests, not general AI, but they show useful learning capacity. The fall to 9/40 followed the accidental loss of long-reading replay.

| Choice | Why it makes sense now | Main risk |
|---|---|---|
| **Keep and repair 98.6M** | Cheapest way to learn whether clean data and retention fixes work. A full 20x-token reference run is affordable. | It may remain limited by 512-token context and narrow data. |
| **Run a 350M pilot next** | More capacity for broader language and reasoning; full reference cost is about $60 before overhead. | A larger model can still forget or learn noisy data. It does not repair a bad recipe. |
| **Go straight to 1B** | Much more capacity in principle. | About $490 for the reference run, weeks or months locally, and no evidence yet that size is the bottleneck. Not recommended now. |

A fresh run also has a data-governance benefit: existing checkpoints have historical exposure to quarantined text. Changing future data cannot remove that history. A genuinely clean-core claim requires a new core trained only on reviewed inputs.

## Data and token needs

The token targets below use **parameters × 20** only as a common comparison point. They are not promises of general AI.

| Model | Chinchilla-style processed tokens | Data needed | Does our current local text suffice? |
|---|---:|---|---|
| **98.6M** | **1.97B** | Broad web and reference prose, books, original simple stories, long-reading tasks, and reviewed general instruction data. | Roughly 0.90B tokenized adult + web tokens are active, plus books and the small Kimi school set. A 2B run would include repeats. It is enough for a controlled experiment, not a broad final model. |
| **350M** | **7B** | Prefer about 5–7B deduplicated tokens with broader knowledge, math, code, science, and instructions; retain reading and school replay. | Not for a strong one-pass run. The active adult + web set would need about eight passes, beyond the useful range found in the repetition study. Add and review several billion unique tokens. |
| **1B** | **20B** | Prefer 15–20B or more unique, carefully filtered tokens and much broader evaluations. | No. It would require roughly 22 passes over the active adult + web set. Do not do that. |

For every size, the next data pack should record source, license, author/provenance limits, unique tokens, duplicates removed, train/validation separation, and mixture percentage. Owner identity and personal memories stay out of this phase. Add them later as a small, reviewed post-training set while replaying general skills.

FineWeb-Edu's full dataset is large enough in principle, but our single local parquet is only part of it. “Download more” is not the whole job: filtering, deduplication, quality checks, and broad held-out tests come first.

## GPU hours and dollar cost

### What is measured versus estimated

- **Measured on our RunPod H100:** 98,584,320 parameters, compiled, 459,389 tokens/sec. The recorded 1.9716864B-token target equals **1.192 hours**. See `results/cloud/20261028-224312/benchmark.json`.
- **Measured local RTX 4060 reference:** about **19,000 tokens/sec** for a roughly 99M core in the earlier benchmark recorded in `DESIGN-CHOICES.md`.
- **350M and 1B below are estimates.** They scale tokens/sec inversely with parameter count, using roughly constant compute per token per parameter. Real speed will differ with memory, micro-batch, compilation, context, and implementation. Run a short benchmark before promising a finish time.
- Dollar figures use **$3.99/H100-hour**, exclude storage/download/setup time, and assume the pod is terminated immediately after training.

| Model | Tokens for 20x reference | H100 hours | H100 cost | RTX 4060 time estimate |
|---|---:|---:|---:|---:|
| **98.6M** | 1.97B | **1.19 measured** | **$4.76** | **28.8 hours** (~1.2 days) |
| **350M** | 7B | **15.0 estimated** | **$60.0** | **363 hours** (~15.1 days) |
| **1B** | 20B | **122.7 estimated** | **$489** | **2,966 hours** (~124 days) |

The current **$22 balance buys at most 5.51 H100 hours** before overhead. That can fund the 98.6M reference run or a useful 350M pilot, but not the full 350M or 1B reference runs. A 350M pilot of 1B tokens would be roughly **2.15 H100 hours / $8.58** under the same scaling estimate; it is an experiment, not a Chinchilla-complete model.

Local GPU money cost is near zero, but calendar time and the daily news window matter. The 4060 is best for evaluations, retention folds, and small pilots—not a full 1B pretraining run.

## Recommended sequence

| Order | Action | Decision it protects us from making blindly |
|---:|---|---|
| 1 | Finish the copied-checkpoint five-fold test. Verify 20% long-reading replay, zero unreviewed self-note training, and before/after exam retention. | Whether the 98.6M wiring repair works. |
| 2 | Complete the reviewed broad-data pipeline and full Kimi story replacement. Keep all quarantined text out of new runs. | Whether a fresh clean-core claim is possible. |
| 3 | Train matched 98.6M candidates on the repaired recipe. Compare general held-out loss, reading, grammar, flexible chat, and five-fold retention against the current core. | Whether better data alone is enough. |
| 4 | If capacity is still limiting, benchmark 350M and run a roughly 1B-token pilot. Compare against 98.6M at equal tokens and equal dollars. | Whether 350M buys real improvement rather than just a larger number. |
| 5 | Only after a successful pilot, fund the roughly 7B-token 350M run. Reconsider 1B only with new evidence and a much larger budget. | Whether full growth is justified. |
| 6 | After general ability is reliable, add owner identity and personal memory as a separate post-training phase with general replay and regression tests. | Whether personal facts damage general skills or dominate training. |

## RunPod migration: completed 2026-11-01

Jaron's notice says the old API becomes limited on **November 2** and shuts off on **November 16**. RunPod's [official v1 migration guide](https://docs.runpod.io/api-reference-v2/migrate-from-v1) says REST v1 retires **November 15, 2026**. We should treat the earliest notice as the operational deadline.

**Done:** all three entry points now use REST v2, nested pod creation, wrapped pod lists, catalog pricing, and v2 status/cost fields. Offline tests passed for all three. Real read-only v2 price and pod-list calls also passed and showed zero pods; a dry run then stopped at the incomplete clean bundle before upload or creation. No SDK dependency was added because the current scripts use HTTP directly.

| Previous code | Completed replacement |
|---|---|
| `tools/runpod_run.py`: REST v1 at `https://rest.runpod.io/v1` and GraphQL pricing | REST v2 at `https://api.runpod.io/v2`; pricing from `GET /v2/catalog/gpus/{id}` |
| Pod creation with flat `imageName`, `gpuTypeIds`, `gpuCount`, `containerDiskInGb`, `dockerStartCmd` | Nested v2 body: `image`, `gpu: {id, count}`, `disk`, `args`, and `cloud` |
| `tools/runpod_growth.py`: old flat create body and old response fields | Same v2 create/response migration; read `status`, `gpu`, and `cost` shapes |
| `tools/runpod_talk.py`: old SDK-style flat creation and old response fields | Same v2 migration; keep dry-run free of any pod creation |
| Pod deletion and listing | `DELETE /v2/pods/{id}`; unwrap `{"pods": [...]}` and accept 204/404 on deletion |
| Old SDK installations, if used on a pod | Pin and test `runpod` SDK 2.x; SDK 2.0 uses REST v2 for pod/GPU calls |

Useful official references: [REST v2 overview](https://docs.runpod.io/api-reference-v2/overview), [create a pod](https://docs.runpod.io/api-reference-v2/pods/create-a-pod), [list pods](https://docs.runpod.io/api-reference-v2/pods/list-pods), [terminate a pod](https://docs.runpod.io/api-reference-v2/pods/terminate-a-pod), [GPU catalog](https://docs.runpod.io/api-reference-v2/catalog/list-gpu-types), and [SDK overview](https://docs.runpod.io/sdk/overview).

**Cloud safety remains unchanged:** dry-run first, verify the clean bundle and price, set the pod watchdog and Windows reaper, terminate in `finally`, list pods afterward, and record zero running pods in `state/cloud-gpu-log.md`. No cloud run should start while `data/cloud/bundle/bundle.json` says INCOMPLETE.

## Bottom line

Sapling does not need a personal-memory campaign or a 1B purchase right now. It needs proof that a clean, broad training recipe can teach and retain general skills. Repair 98.6M, measure honestly, then try 350M as a controlled next step. Keep identity and owner facts for post-training, after the general foundation works.

## Data point, 11/1 evening (logged by Claude at Jaron's ask: "that might've been useful data")
After Kimi's morning fixes (11:17 AM: data swap, restored long-reading replay, self-notes excluded), Sapling then trained by itself for about 11 hours with no other changes. Kimi's steps 1-2 had not started yet.

| Exam | Before fixes (gen1548 copy) | Gen 1589, 10:30 PM |
|---|---|---|
| Facts it was taught | 2/7 | 7/7 |
| Long reading | 12/40 | 19/40 |
| Grammar | 46/48 | 48/48 |
| Prefixes | 81/86 | 73/86 |

**Reading:** the wiring fixes keep paying off on their own over time; the one loss is Prefixes, which looks like forgetting. This is the baseline Kimi's step 1 starts from.
