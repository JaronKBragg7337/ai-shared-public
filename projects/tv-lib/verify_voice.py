#!/usr/bin/env python
"""SHIP GATE: every Heartbeat TV episode must pass this before it ships.
Transcribes the narration in the FINAL mp4 with a local speech-to-text model (faster-whisper, CPU, no network after the
first model download) and compares it word-for-word with the episode's script.json.  Any segment missing more than 5% of
its words FAILS (exit code 1) and blocks shipping.  Catches the kokoro-js ~510-token silent truncation (long segments that
stop mid-sentence) and anything else that drops speech (bad mix, clipped cue, wrong file).

  python verify_voice.py <episode.mp4> <script.json> [--key text] [--threshold 0.05] [--model small.en] [--json out.json]
        [--ids n01,n02]   only judge these segment ids (others still used for alignment)

Method: whisper transcript -> normalised words; the script segments are laid end to end and aligned with difflib;
words in a segment that are matched exactly, or by a close spelling (names whisper mis-hears, ratio >= 0.7), count as
spoken.  Numbers are ignored on both sides (digits, and number words such as 'eighteen thirty' / 'percent' - whisper writes digits, scripts may spell them).  Segments under 20 words also need >= 3 missing
words to fail (one mis-heard word in a short line is not a cut).  Proper names whisper cannot spell go in verify_ignore.txt
beside script.json."""
import argparse, difflib, json, re, subprocess, sys, os, tempfile

NUMW = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion trillion percent point oh and half quarter".split())

def norm_words(text):
    text = text.lower().replace("’", "'").replace("-", " ").replace("–", " ").replace("—", " ")
    out = []
    for w in re.findall(r"[a-z0-9']+", text):
        w = w.strip("'")
        if not w or any(c.isdigit() for c in w) or w in NUMW: continue
        out.append(w)
    return out

def transcribe(mp4, model_name):
    from faster_whisper import WhisperModel
    import numpy as np
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", mp4, "-vn", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"])
    audio = np.frombuffer(raw, dtype="<i2").astype("float32") / 32768.0     # (array input: avoids PyAV version issues)
    m = WhisperModel(model_name, device="cpu", compute_type="int8")
    segs, _ = m.transcribe(audio, language="en", beam_size=5, vad_filter=False, condition_on_previous_text=False)
    text = " ".join(s.text for s in segs)
    return text

def check(mp4, script, key=None, threshold=0.05, model="small.en", only=None, transcript=None):
    raw = open(script, "rb").read()
    try: data = json.loads(raw.decode("utf8"))
    except UnicodeDecodeError: data = json.loads(raw.decode("cp1252"))
    ign = set()   # proper names whisper can't spell: put them (one per line) in verify_ignore.txt beside script.json
    ip = os.path.join(os.path.dirname(os.path.abspath(script)), "verify_ignore.txt")
    if os.path.exists(ip): ign = set(norm_words(open(ip, encoding="utf8").read()))
    if isinstance(data, dict): data = data.get("segments") or data.get("script") or list(data.values())[0]
    segs = []
    for s in data:
        k = key or next((c for c in ("text", "narration", "narr", "line", "vo") if isinstance(s, dict) and c in s), None)
        if not k or not s.get(k): continue
        segs.append((str(s.get("id", len(segs))), [w for w in norm_words(s[k]) if w not in ign], s[k]))
    heard = norm_words(transcript if transcript is not None else transcribe(mp4, model))
    flat = []; owner = []
    for si, (sid, ws, _) in enumerate(segs):
        flat += ws; owner += [si] * len(ws)
    sm = difflib.SequenceMatcher(None, flat, heard, autojunk=False)
    ok = [False] * len(flat)
    for tag, a0, a1, b0, b1 in sm.get_opcodes():
        if tag == "equal":
            for i in range(a0, a1): ok[i] = True
        elif tag == "replace":   # close spellings count (mis-heard names, plurals)
            pool = heard[b0:b1]
            for i in range(a0, a1):
                if any(difflib.SequenceMatcher(None, flat[i], h).ratio() >= 0.7 for h in pool): ok[i] = True
    rows = []; pos = 0
    for si, (sid, ws, raw) in enumerate(segs):
        n = len(ws); flags = ok[pos:pos + n]; pos += n
        miss = [w for w, f in zip(ws, flags) if not f]
        frac = len(miss) / n if n else 0
        # trailing run of unspoken words = a cut-off ending
        tail = 0
        for f in reversed(flags):
            if f: break
            tail += 1
        fail = (frac > threshold and (n >= 20 or len(miss) >= 3)) and (only is None or sid in only)
        rows.append(dict(id=sid, words=n, missing=len(miss), missing_pct=round(100 * frac, 1), tail_missing=tail, fail=fail,
                         missing_tail_text=" ".join(ws[n - tail:]) if tail else "", missing_words=miss[:40]))
    return rows

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("mp4"); ap.add_argument("script")
    ap.add_argument("--key"); ap.add_argument("--threshold", type=float, default=0.05); ap.add_argument("--model", default="small.en")
    ap.add_argument("--json"); ap.add_argument("--ids"); ap.add_argument("--transcript", help="text file instead of running whisper (testing)")
    a = ap.parse_args()
    tr = open(a.transcript, encoding="utf8").read() if a.transcript else None
    rows = check(a.mp4, a.script, a.key, a.threshold, a.model, set(a.ids.split(",")) if a.ids else None, tr)
    bad = [r for r in rows if r["fail"]]
    print("%s vs %s  (threshold %.0f%% missing words)" % (os.path.basename(a.mp4), os.path.basename(os.path.dirname(os.path.abspath(a.script))) , a.threshold * 100))
    for r in rows:
        print("  %-5s %3d words  missing %3d (%4.1f%%)  %s%s" % (r["id"], r["words"], r["missing"], r["missing_pct"], "FAIL" if r["fail"] else "ok",
              ("  tail never spoken: ..." + r["missing_tail_text"][-70:]) if r["tail_missing"] >= 4 else ""))
        if r["fail"] and r["tail_missing"] < 4: print("        not heard:", " ".join(r["missing_words"]))
    print("RESULT:", "FAIL - %d segment(s): %s" % (len(bad), ", ".join(r["id"] for r in bad)) if bad else "PASS")
    if a.json: json.dump(rows, open(a.json, "w"), indent=1)
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
