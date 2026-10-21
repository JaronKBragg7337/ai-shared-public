# Keeper's Light voice check

Checked 2026-10-15. Live files only. Nothing was re-voiced, re-rendered, or published.

| Episode | File | Duration | Encoded |
|---|---|---|---|
| 1 First Light | `C:\Users\lilli\Projects\heartbeat-observatory\tv\shows\keepers-light-ep1.mp4` | 42.000 s | 2026-09-26 16:57 |
| 2 Storm Night | `...\keepers-light-ep2.mp4` | 42.000 s | 2026-09-29 02:07 |
| 3 The Keeper | `...\keepers-light-ep3.mp4` | 42.000 s | 2026-09-29 05:46 |

No `script.json` anywhere in the show folder, the ep2/ep3 render dirs, or beside the live mp4s, so `verify_voice.py` was not run. Spoken lines were taken from `README.md`, `build.py`, `keeper_audio.py`, `storm_audio.py`, `finish.sh`, the title files (`t1.txt`, `t2.txt`, `t2_ep2.txt`, `t2_ep3.txt`, `t3.txt`), and `C:\Users\lilli\Renders\keepers-ep2\build_ep2_snapshot.py` / `keepers-ep3\build_ep3_snapshot.py`.

Expected speech: none. Ep1 soundtrack is generated surf and a pad (`README.md`: "No voice yet"). Ep2 is rain, wind, surf, thunder, and a pad (`storm_audio.py`). Ep3 is sea, wind, gull cries, a lamp clunk, a door, footsteps, and a pad (`keeper_audio.py`). `finish.sh` mixes that one wav under the picture and burns the titles on screen. The titles are drawtext, not TTS: "The Keeper's Light", the episode name, and "Rendered in Blender · Heartbeat TV".

These encodes are from 9/26 and 9/29, before the 10/14 Kokoro ~512-phoneme cut.

## How it was heard

faster-whisper 1.2.1, model `small.en`, `device="cpu"`, `compute_type="int8"`, `language="en"`, `beam_size=5`, `condition_on_previous_text=False`. `CUDA_VISIBLE_DEVICES` was empty. Two passes per file: `vad_filter=False` (same as `verify_voice.py`) and `vad_filter=True` (Silero).

VAD returned **0 segments** on all three files. The no-VAD pass printed the usual non-speech hallucinations (collapsed word times, a first-word probability of 0.001, "thanks for watching" / "like and subscribe"). Those prints are listed below and are not counted as dialogue.

## Lines that stop around 25–27 s

None. No scripted line exists, and VAD found no speech long enough to hit the phoneme cap. Two no-VAD spans cross that window and were rejected:

- Ep2, 5.24–29.98 s, text "This is the end of the video." The span ends at 29.98 s. Seven words are smeared across the rain; the first word probability is 0.001; `no_speech_prob` is 0.429. Thunder in `storm_audio.py` is timed at about 6.1 s, 16.8 s, and 26.0 s (`FLASHES` 3.1 / 14.6 / 24.2 plus the delay). VAD: empty.
- Ep3, 23.68–29.38 s, text "No, no, no, no, no." This sits on the scripted gull cries at 24.5 s and 27.0 s (`keeper_audio.py`). It is the same word repeated, not a sentence cut mid-clause. `no_speech_prob` 0.454. VAD: empty.

## Episode 1 — PASS

Expected: no narration and no dialogue.

Heard (VAD): nothing, 0.0–42.0 s.

No-VAD prints, discarded: 8.42–20.30 s "This is the end of this video, I hope you enjoyed this video, and if you enjoyed it, don't forget to like, comment, and subscribe!" (`no_speech_prob` 0.575, most word times stuck on one timestamp); 40.58–41.98 s "Thanks for watching!" (`no_speech_prob` 0.867).

No cut line. No missing line. No line that stops near 25–27 s.

## Episode 2 — PASS

Expected: no narration and no dialogue. Soundtrack events are rain, gusts, surf, and thunder after the flashes at 3.1 s, 14.6 s, 24.2 s, and 35.4 s.

Heard (VAD): nothing, 0.0–42.0 s.

No-VAD prints, discarded: 5.24–29.98 s "This is the end of the video." (see above); 39.60–41.00 s "You" (`no_speech_prob` 0.821, one word, probability 0.107).

No cut line. No missing line. The 29.98 s hallucination is not a Kokoro stop.

## Episode 3 — PASS

Expected: no narration and no dialogue. Gull cries are written at 4.2, 6.1, 24.5, 27.0, 35.0, and 36.1 s. Door latch at 11.95 s, creak from 12.05 s. Lamp clunk at 8.52 s. Footsteps only inside the door shot.

Heard (VAD): nothing, 0.0–42.0 s.

No-VAD prints, discarded, each one on a sound effect:

| Heard | Time | Lines up with |
|---|---|---|
| "No No!" | 3.08–4.90 | gull at 4.2 s |
| "No No!" | 5.86–6.78 | gull at 6.1 s |
| "No No!" | 12.00–12.76 | door creak at 12.05 s |
| "No, no, no, no, no." | 23.68–29.38 | gulls at 24.5 s and 27.0 s |
| "No, no, no, no." | 34.18–36.98 | gulls at 35.0 s and 36.1 s |

No cut line. No missing line. Nothing in that list is a sentence that stops at the phoneme cap.

First step: Leave the three live mp4s as they are. There is no spoken line to recut.
Blind spot: I did not listen by ear. The call is faster-whisper `small.en` on CPU, VAD on and off, read against the audio scripts. A voice buried under the surf that Silero missed would not show up here, and the scripts do not ask for one.
Rewrite: Do any of the three live Keeper's Light episodes contain narration or dialogue that is cut off, missing, or different from the script, including a line that dies around 25–27 seconds the way the Kokoro phoneme cap did?
