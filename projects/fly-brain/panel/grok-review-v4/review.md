# Grok review — tonight’s unattended v4 chain

Stage A (`results/reading_v4/state.json`) is mid-run (~960M / 1.2B tokens, micro=16, ~35k tok/s), no `kind: done` in `log.jsonl` yet. `tools/teach_v4.py` is waiting on that line. Live core is still v3.2 (~17.6M); the 60.5M file is staged. Heartbeat is assumed down until after the swap.

Most severe first.

---

## Issues

### 1 — Severity: bug
- File: tools/gpu_yield.py:21
- Description: `stop` only writes `results/heartbeat.stop` and returns. It does not wait until the heartbeat process is gone or the GPU is free. The heartbeat only looks at that file **between** ticks (`sapling/heartbeat.py:278`). A 60.5M consolidation (200 steps + exams, a few minutes) keeps the card until the tick finishes. The 3:50 AM news script then starts UnrealEditor immediately (`run_rendered_news.ps1:39-44`). Same machine, 8 GB: this is the freeze that `gpu_yield` was added to prevent.
- Scenario: Swap lands ~12:30–1:00 AM. Heartbeat is up and hits `do_consolidate` around 3:50. News calls `gpu_yield stop`, prints `stopped`, launches Unreal while AdamW + 16×512 activations still sit in VRAM. Both jobs die. `WaitForExit` never returns cleanly; parole may never run. GPU and heartbeat are wedged until someone is at the keyboard.
- Suggestion: After writing the stop file, poll `heartbeat_alive()` until false (with a timeout longer than one consolidation + exams, e.g. 15 min). Then `torch` cannot help from this process — the heartbeat must drop CUDA before exit (already happens in `run()` `finally` once the tick ends). Do not start Unreal until `heartbeat_alive()` is false. Optionally make the heartbeat check the stop file inside `do_consolidate` between steps and abort before `opt.step` / save.

### 2 — Severity: bug
- File: sapling/talk.py:384
- Description: Conversation training loads the 60.5M core onto CUDA (`load_checkpoint`), builds examples, runs `window_losses`, and only then “pauses” every 50 steps (`talk.py:411`). The pause is `time.sleep(60)` with the model **still on the GPU**. Stage A’s `wait_gpu` (`reading.py:491`) does the opposite: save, `m.cpu()`, `del`, `empty_cache`, wait until the hog is gone for two polls, reload. `tools/teach_v4.py:85` `measure()` / `chat_samples.py` also take the GPU with no `gpu_busy` check at all.
- Scenario: Stage A ends while Unreal still holds the card (overrun into 3:50, or Unreal already open). Stage A’s own loop would have paused and freed VRAM, then written `done` once the card was clear *or* crashed in the post-loop probe (`reading.py:588`, no busy check). `teach_v4` then `measure(A_CORE)` on CUDA and/or `talk.train` `load_checkpoint` onto CUDA next to UnrealEditor. Freeze/OOM. Because heartbeat is still down, news `gpu_yield stop` prints `not running` and **does not** arm parole after the render (`run_rendered_news.ps1:46` only starts if `$sapOut` matches `stopped`). `talk.train` has no OOM retry (Stage A does, `reading.py:556`). `teach_v4` is blocked in `sh()` with `timeout=None`. Heartbeat stays down all night.
- Suggestion: Before any CUDA alloc in `measure_core`, `chat_samples`, `talk.train`, and `grow.swap`, wait on `gpu_busy` and yield like `reading.wait_gpu`. In `talk.train`, on pause: save staged/opt, move the model to CPU, empty cache, wait, reload. Check every step (or every micro-batch), not every 50. Mirror Stage A’s OOM retry.

### 3 — Severity: bug
- File: tools/teach_v4.py:92
- Description: If the heartbeat *is* alive at swap time, the script requests stop, immediately runs `grow.swap` (two cores + full exams on GPU, minutes), then `gpu_yield start`. `scheduled_parole.py:47` exits with `already running` if the pid file is still live. The heartbeat then sees the stop file and exits. Nobody starts it again. Swap can also write `results/core_checkpoint.pt` while a finishing consolidation still holds the old weights and then `save_checkpoint`s over the new 60.5M live file (`grow.py:341` vs `consolidate.py:276`).
- Scenario: Anything starts the heartbeat between Stage A `done` and swap (control room Restart, a leftover parole, the 10:30 task if it was still waiting). `teach_v4` only calls `gpu_yield stop` right before swap (`teach_v4.py:90-93`), not before Stage B training. Stop is async (finding 1). Swap and the heartbeat share the card; after swap the heartbeat dies from the stop file and stays dead. `teach_v4` waits 10 h for consolidations that never come.
- Suggestion: At the start of Stage B (before `measure`), and again before `swap`: `gpu_yield stop` then **wait until `not heartbeat_alive()`**. After swap, `gpu_yield start` then wait until `heartbeat_alive()` (or parole finished). Do not treat “stop requested” as “GPU is free.”

### 4 — Severity: bug
- File: tools/teach_v4.py:53
- Description: `stage_a_done()` parses every line of `results/reading_v4/log.jsonl` and only catches `OSError`. `json.loads` on a partial last line (Stage A is still appending) or a blank line raises `JSONDecodeError`. That happens in `main()` **before** the `try` (`teach_v4.py:80-82`), so the “restart heartbeat either way” handler never runs.
- Scenario: Poll at 11:50 lands on a torn `probe`/`step`/`done` line. `teach_v4` crashes. Stage A may still finish and free the GPU. Heartbeat is down and nothing in this script starts it. News at 3:50 sees heartbeat not running and will not parole it afterwards (finding 2). Sapling is down until morning.
- Suggestion: Catch `json.JSONDecodeError` / `ValueError` and treat the file as “not done yet.” Ignore blank lines. Prefer “the last complete `kind==done` line whose `staged` path exists and is newer than this process’s start,” so a leftover `done` from an older attempt cannot start Stage B on a stale `core_v4_staged.pt` while a new Stage A still holds the GPU. (Tonight’s `log.jsonl` has no `done` yet, so the stale-`done` half is latent; the parse crash is live.)

### 5 — Severity: bug
- File: sapling/heartbeat.py:278
- Description: Heartbeat never calls `gpu_busy()`. Overnight GPU sharing is entirely “news asks us to stop.” If stop is late, ignored, or the render starts because Unreal was already up (`run_rendered_news.ps1:23` waits at most 1 h then continues), a 60.5M `do_consolidate` / `do_practice` / `do_explore` runs beside Unreal. Tick errors are swallowed (`heartbeat.py:222`) so a CUDA OOM becomes a ledger `error` and the next tick tries again with a model that may still be in `.train()` and with fragmented VRAM.
- Scenario: News stop raced (finding 1) or Unreal was already open from a previous session. Heartbeat keeps consolidating. Card fills. Loop “survives” as error ticks; the card stays unusable; 5 successful consolidations never appear.
- Suggestion: At the top of `do_consolidate` / other `on_gpu=True` actions, if `gpu_busy()`: skip (count as rest) instead of taking the card. After CUDA OOM: `empty_cache`, `model.eval()`, do not keep retrying every 5 s against a hog.

### 6 — Severity: suggestion
- File: sapling/consolidate.py:165
- Description: `talk_replay` swallows every exception and returns `None`. Then `n_talk=0` and reading share jumps to 75% (`consolidate.py:244-245`). Conversation lessons are silently dropped from every heartbeat fold. No ledger field distinguishes “talk replay off because this core never talked” from “talk replay crashed.”
- Scenario: After swap, first consolidation: `load_examples` hits a bad line in `data/talk/lessons.jsonl`, a tokenizer mismatch after vocab growth, or a file lock. Five consolidations train 75% reading + 25% school only. Talking regresses the same way reading did this afternoon, and `talk_share` in the ledger is `0.0` with no error.
- Suggestion: Log the exception on the consolidation row (`talk_replay_error`). Fail the consolidation (tick error) rather than quietly changing the mix. Do not treat `except Exception: return None` as a valid skip unless `brain.talks()` is false.

### 7 — Severity: suggestion
- File: sapling/heartbeat.py:101
- Description: Consolidation is not on a timer. Drive is 0 unless `since_consol > 90` **and** (`pending >= consolidate_min_pending` (2) **or** `worst_misses >= 3`). `grow.swap` inserts one confirmed self fact (`grow.py:363`), so pending starts at 1 unless other unconsolidated rows already exist. `teach_v4.py:107` then waits up to 10 h for 5 new `kind=consolidation` rows. Zero rows → log and return; 1–4 rows → still measures, but not “after 5.”
- Scenario: Heartbeat comes up after midnight with a full 4 h budget, explores a bit, but pending stays at 1 and goals are not missing 3 in a row. Overnight it mostly practises/explores/rests. Morning: no 5-fold measurement, and you do not learn whether reading/talk survived folding on the 60.5M core (the whole point of that wait).
- Suggestion: After a `growth` swap, force or bias N consolidations (or lower `consolidate_min_pending` to 1 for the first night). `teach_v4` should also treat “heartbeat died / self-stopped” as an error and re-arm parole, not sit 10 h on a dead pid.

### 8 — Severity: suggestion
- File: sapling/train.py:210
- Description: `save_checkpoint` does `torch.save` straight onto `results/core_checkpoint.pt` (same for the staged talk core). A crash mid-write leaves a truncated live file. Swap writes that path after copying the old core aside (`grow.py:328` then `341`), so the backup exists, but the live path the heartbeat will load is the one being written.
- Scenario: Swap or a consolidation is killed by the Unreal collision (finding 1) during `torch.save` of the 242 MB live 60.5M file. Heartbeat restart loads a broken checkpoint, `Brain.ok` is false, practice/consolidate drives go to 0 (`heartbeat.py:108`), it rests and may self-stop. The kept `core_v3.2_gen_*.pt` is fine but not auto-restored.
- Suggestion: Write to `path + ".tmp"` then `os.replace`. On heartbeat start, if load fails, refuse to clobber and surface it in the stop report.

---

## No finding (checked, clean for tonight)

**Swap keeps the old core.** `grow.swap` copies live `results/core_checkpoint.pt` to `results/checkpoints/core_v{version}_gen_{N}.pt` before replacing live (`grow.py:327-329`). Copy happens after the “before growth” exams and before the new weights are saved.

**Heartbeat restart on a failed Stage B step (inside the `try`).** `teach_v4.py:99-102` logs and `gpu_yield start`s on exception, then returns. That path is real. Holes are outside it: the Stage A wait loop (finding 4), async stop/start (findings 1 and 3), and the post-`try` `gpu_yield start` at line 103 (if that `sh()` itself raises, uncaught — `gpu_yield start` is a `Popen` and almost always returns 0).

**`sapling/talk.py` format vs `session.py`.** Chat and training share `encode_turns`. Session conversation path (`session.py:214-218`) builds `q : … a :` with `answer_last=False`; training uses the same function with answers + `<eos>`. Tests in `tests/test_v4.py:57-74` lock the token layout and the open last turn.

**Loss only on Sapling’s answers.** `encode_turns` sets targets to `-1` on prompt tokens and to the answer ids + `<eos>` on its turns (`talk.py:301-316`). `model.forward` uses `ignore_index=-1` (`model.py:132`). `test_conversation_format_masks_everything_but_its_answers` checks this.

**No AI-written self-lessons without `data/talk/owner_self_lessons.json`.** That file is not in `data/talk/` tonight (only `lessons.jsonl` and empty `self_only.jsonl`). `owner_answers()` returns `{}` on missing file; `self_lessons()` skips empty answers; `ai_examples()` is display-only. Tests cover both (`test_v4.py:87-106`). `build()` tonight will train oasst1+dolly only. Changelog already expects “what is your name?” not to say Sapling until Jaron writes the card.

**Talk-train replay mix.** Default 16 conversation + 12 reading + 4 school. Reading replay uses `READ_REPLAY_SPLIT` (includes `web`). Fine for Stage B itself.

**Consolidation mix on the 60.5M core (when talk replay actually loads).** `n_talk = int(32 * 0.25) = 8`, `n_read = int(32 * (0.75 - 0.25)) = 16`, school/facts = 8. Adds up to 32. `READ_REPLAY_SPLIT` is stories 11/29, adult 4/29, web 14/29 — matches v4 `V4_SHARES` new-token mix (11+4+14=29). Web shards exist and are ~50M tokens; `randrange` will not blow up on short shards. `MICRO = 16` is what Stage A is already using on this card (`reading_v4` start row: `"micro": 16`). School tensor is 1-D concatenated sentences, not 32×512×mix on GPU. No second wipe mechanism in the share math.

**`ignore_index` mixed batches.** School/reading windows have dense labels; talk has `-1` pads. Same `CrossEntropyLoss`. Not a crash.

---

## Overnight GPU / heartbeat state (summary)

| Time (planned) | Who has the GPU | Risk |
|---|---|---|
| now → ~11:50 PM | Stage A reading | Stage A *does* free VRAM on Unreal (`wait_gpu`). Final probe/save after the token loop does not. |
| 11:50 → ~12:45 | `teach_v4` measure + `talk.train` | No yield before CUDA alloc; pause does not free VRAM. |
| after swap | heartbeat | No `gpu_busy`; stop is async. |
| 3:50 AM | UnrealEditor | News stop does not wait; start only if stop printed `stopped`. |

Worst terminal states: (a) Unreal + 60.5M freeze, heartbeat down; (b) `teach_v4` dead on JSON parse, heartbeat down; (c) stop-file race, heartbeat exits after swap and stays down; (d) chain “finishes” with 0 consolidations and no post-fold measurement.

---

First step: Make `gpu_yield stop` wait until the heartbeat pid is dead, and do not launch Unreal (or `grow.swap` / `talk.train`) until it is.
Blind spot: I did not run the news script or watch a live consolidation on the 60.5M core; freeze risk is from control flow plus the 10/15 D23 incident, not a reproduced OOM tonight.
Rewrite: What in this overnight Stage A → talk → swap → heartbeat path can freeze the 8 GB card with Unreal, drop the heartbeat, skip the swap, or fold the new 60.5M core until reading or talking disappears again?
