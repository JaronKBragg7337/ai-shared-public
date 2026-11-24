# Science 8.7 Antarctica Part 1 (copied from ep6 finish.py).  frames (Blender every 2nd frame + Pillow passages at 24 fps) + Kokoro narration + music bed -> captioned H.264 mp4 (16:9),
# a 9:16 vertical cut (letterboxed over a blurred copy, captions under the picture) and a poster jpg.  Same pipeline as 8.4 / 8.5.
#   python finish.py [FRAMES_DIR] [POSTER_FRAME] [--redo] [--caps-only] [--plan]
import json, os, subprocess, sys, re, numpy as np, wave
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from shots import SHOTS, FPS
FR = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith("--") else "C:/Users/lilli/Renders/antarctica-ep7/frames"
PF = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "200"
NAME = "science-ep7-antarctica-ice"
DUR = sum(sh["dur"] for sh in SHOTS)
W0 = os.path.join(HERE, "work"); os.makedirs(W0, exist_ok=True)
narr = {s["id"]: s["text"] for s in json.load(open(os.path.join(HERE, "script.json"), encoding="utf8"))}
def shot_start(name):
    t = 0.0
    for sh in SHOTS:
        if sh["name"] == name: return t
        t += sh["dur"]
    raise KeyError(name)
# narration id -> (shot it starts in, offset s)
NARR_AT = [("n01", "s01_field", 1.0), ("n02", "s03_cores", 1.0), ("n03", "s04_sea", 1.0), ("n04", "diag_dna", 1.0),
           ("n05", "s07_transform", 1.0), ("n06", "s08_divide", 1.0), ("n07", "diag_revive", 1.0), ("n08", "diag_siberia", 1.0),
           ("n09", "s09_whillans", 1.0), ("n10", "s10_mercer", 1.0), ("n11", "s11_shelf", 1.0), ("n12", "diag_risk", 1.0),
           ("n13", "s13_bergs", 1.0), ("n14", "diag_jobs", 1.0), ("n15", "s15_end", 1.0)]
CUES = [(shot_start(shn) + off, sid) for sid, shn, off in NARR_AT]
# on-screen stage label + source line, per Blender shot (no em or en dashes on screen)
STAGE = [
 ("s01_field", "BLUE ICE  ·  ILLUSTRATION", "A wind-scoured blue-ice field like the Allan Hills, where 6-million-year-old ice was found (PNAS, Oct 2025). Not a map of the real site."),
 ("s02_chunk", "AIR FROM THE PAST  ·  ILLUSTRATION", "Old ice holds tiny bubbles of ancient air; the team dated it from the argon in them (PNAS 2025). Block and bubbles drawn, not a real sample."),
 ("s03_cores", "ICE CORES  ·  ILLUSTRATION", "Each band is a layer of old snow. Beyond EPICA reached bedrock at ~2.8 km in January 2025: one record, at least 1.2 million years."),
 ("s04_sea", "SCOTIA SEA FLOOR  ·  ILLUSTRATION", "Drilled in 2019, up to 178 m under the seafloor; DNA ~1 million years old (Armbrecht et al. 2022). Drill and core drawn, not to scale."),
 ("s05_diatoms", "DIATOMS  ·  ILLUSTRATION", "Tiny algae with shells of glass. Their DNA in that mud reaches back ~540,000 years. Shapes drawn, not to scale."),
 ("s06_clay", "DNA ON CLAY  ·  ILLUSTRATION", "Short DNA pieces stuck to clay grains, which can help them last. Molecules drawn hugely enlarged."),
 ("s07_transform", "NATURAL TRANSFORMATION  ·  IDEA", "Bacteria take up loose DNA in the lab, even DNA stuck to clay (Verma et al. 2024). Ancient DNA doing this in the wild: NOT SEEN."),
 ("s08_divide", "SELECTION  ·  ILLUSTRATION", "Random changes, then the cells whose changes happen to help leave more offspring. The warm-coloured cells stand for the lucky ones."),
 ("s09_whillans", "LAKE WHILLANS  ·  CUTAWAY", "~800 m of ice over liquid water; drilled cleanly in 2013; ~130,000 cells per mL (Christner et al. 2014). Not to scale; cells drawn as specks."),
 ("s10_mercer", "LAKE MERCER  ·  CUTAWAY", "Under ~1,087 m of ice; 1,374 single-cell genomes, most appear to be new species (Kim et al. 2025). Sealed in ~30 million years: NOT PROVEN."),
 ("s11_shelf", "ICE SHELF EDGE  ·  ILLUSTRATION", "At the edges, warm ocean water melts floating ice from underneath (Rignot et al. 2013). A generic shelf front, not a real one."),
 ("s12_shore", "THE REAL RISK TODAY", "H5N1 bird flu reached the mainland in 2024: skuas, then Adélie penguins. A generic rocky shore; no real birds or cases shown."),
 ("s13_bergs", "ILLUSTRATION", "Icebergs off a generic coast. Most visitors arrive by ship, with operators who follow the treaty rules."),
 ("s14_station", "A GENERIC STATION  ·  ILLUSTRATION", "Not any real station. The US Antarctic Program hires cooks, cleaners, carpenters, mechanics and drivers (usap.gov)."),
 ("s15_end", "WHAT'S FROZEN DOWN THERE", "6-million-year ice (Allan Hills)  ·  ~1-million-year seafloor DNA  ·  life in lakes under the ice. Part 2: the sky the ice keeps."),
]

def dur(path): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode().strip())
def chunks(text, limit=150):
    """caption pieces: whole sentences; only a sentence longer than `limit` chars is split, at the colon / semicolon / comma
    nearest its middle (never mid-clause), so captions read as sentences and never stop at a random comma."""
    sents = [s.strip() for s in re.split(r"(?<=[.?!])\s+", text) if s.strip()]
    def split_long(s):
        if len(s) <= limit: return [s]
        cands = [m.end() for m in re.finditer(r"[:;,]\s", s)]
        if not cands: return [s]
        cut = min(cands, key=lambda i: abs(i - len(s) / 2))
        return split_long(s[:cut].strip()) + split_long(s[cut:].strip())
    return [p for s in sents for p in split_long(s)]
def nw(s): return re.sub(r"[^a-z0-9']", "", s.lower().replace("-", " ")) if "-" not in s else [nw(x) for x in s.split("-")]
def words_timed(sid):
    """word timings of the trimmed clip from faster-whisper (local, CPU), cached beside the wav"""
    wav = os.path.join(HERE, "audio", "t_%s.wav" % sid); cache = os.path.join(HERE, "audio", "words_%s.json" % sid)
    if os.path.exists(cache) and os.path.getmtime(cache) > os.path.getmtime(wav): return json.load(open(cache))
    from faster_whisper import WhisperModel
    import numpy as np
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", wav, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"])
    audio = np.frombuffer(raw, dtype="<i2").astype("float32") / 32768.0
    m = WhisperModel("small.en", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(audio, language="en", beam_size=5, word_timestamps=True, condition_on_previous_text=False)
    ws = [dict(w=w.word.strip(), s=round(w.start, 3), e=round(w.end, 3)) for sg in segs for w in (sg.words or [])]
    json.dump(ws, open(cache, "w")); return ws
def caption_times(text, pieces, heard, clip_len):
    """align the script words with the heard words (difflib); each piece starts when its first word is spoken and ends
    when its last word ends (unmatched words are interpolated between their matched neighbours)"""
    import difflib
    sw = []   # (piece index, normalised word)
    for pi, p in enumerate(pieces):
        for tok in p.split():
            n = nw(tok)
            for x in (n if isinstance(n, list) else [n]):
                if x: sw.append((pi, x))
    hw = [re.sub(r"[^a-z0-9']", "", w["w"].lower()) for w in heard]
    sm = difflib.SequenceMatcher(None, [w for _, w in sw], hw, autojunk=False)
    t_s = [None] * len(sw); t_e = [None] * len(sw)
    for tag, a0, a1, b0, b1 in sm.get_opcodes():
        if tag == "equal":
            for k in range(a1 - a0): t_s[a0 + k] = heard[b0 + k]["s"]; t_e[a0 + k] = heard[b0 + k]["e"]
        elif tag == "replace" and (a1 - a0) == (b1 - b0):   # same count: mis-heard names, keep their times
            for k in range(a1 - a0): t_s[a0 + k] = heard[b0 + k]["s"]; t_e[a0 + k] = heard[b0 + k]["e"]
    # interpolate the gaps
    idx = [i for i, t in enumerate(t_s) if t is not None]
    if not idx: return [(clip_len * i / len(pieces), clip_len * (i + 1) / len(pieces)) for i in range(len(pieces))]
    for i in range(len(sw)):
        if t_s[i] is None:
            prev = max([j for j in idx if j < i], default=None); nxt = min([j for j in idx if j > i], default=None)
            a = t_e[prev] if prev is not None else 0.0; b = t_s[nxt] if nxt is not None else clip_len
            pa = prev if prev is not None else -1; pb = nxt if nxt is not None else len(sw)
            t_s[i] = a + (b - a) * (i - pa) / (pb - pa); t_e[i] = a + (b - a) * (i + 1 - pa) / (pb - pa)
    out = []
    for pi in range(len(pieces)):
        ks = [i for i, (p, _) in enumerate(sw) if p == pi]
        out.append((min(t_s[i] for i in ks), max(t_e[i] for i in ks)) if ks else (0.0, 0.0))
    return out
def ts(s): return "%d:%02d:%05.2f" % (int(s // 3600), int(s % 3600 // 60), s % 60)
def esc(s): return s.replace("{", "(").replace("}", ")")

def ass(vertical=False):
    W, H = (720, 1280) if vertical else (1280, 720)
    cs = 30 if vertical else 26
    cap_margin = 290 if vertical else 46
    stage_mv = 120 if vertical else 30
    src_mv = 154 if vertical else 62
    ml = 24 if vertical else 36
    head = "\n".join([
        "[Script Info]", "ScriptType: v4.00+", "PlayResX: %d" % W, "PlayResY: %d" % H, "WrapStyle: 0", "ScaledBorderAndShadow: yes", "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Narr,Segoe UI,%d,&H00F4EEE2,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,1.6,1,2,60,60,%d,1" % (cs, cap_margin),
        "Style: Title,Georgia,%d,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,2,2,5,40,40,0,1" % int(cs * 2.6),
        # the subtitle sits in a translucent box (it was grey-on-grey over the moon)
        "Style: Sub,Georgia,%d,&H00F4EEE2,&H00FFFFFF,&H00000000,&H60000000,0,1,0,0,100,100,0,0,3,7,0,5,40,40,0,1" % int(cs * 1.15),
        "Style: Kicker,Segoe UI,%d,&H0034B1F2,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,2,0,1,1.4,1,5,40,40,0,1" % int(cs * .9),
        "Style: Stage,Segoe UI,%d,&H0034B1F2,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,1.5,0,1,1.5,1,7,%d,40,%d,1" % (int(cs * .95), ml, stage_mv),
        # source line under the stage label: 19 px (was 16), two lines max, readable at 720p
        "Style: Src,Segoe UI,%d,&H00E6E0D6,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,1.3,1,7,%d,40,%d,1" % (int(cs * .73), ml, src_mv),
        "Style: Band,Segoe UI,20,&H00222830,&H00222830,&H00222830,&H00222830,0,0,0,0,100,100,0,0,1,0,0,7,0,0,0,1",
        "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Text", ""])
    ev = []
    cy = H * .42 if vertical else H * .30
    nl = "\\N" if vertical else " "
    ev.append("Dialogue: 1,%s,%s,Kicker,,0,0,0,{\\an5\\pos(%g,%g)\\fad(1200,1200)}HEARTBEAT TV  ·  SCIENCE  ·  8.7" % (ts(1.0), ts(9.0), W / 2, cy - cs * 3.4))
    ev.append("Dialogue: 1,%s,%s,Title,,0,0,0,{\\an5\\pos(%g,%g)\\fad(1200,1200)}Antarctica: what's frozen in the ice" % (ts(1.5), ts(9.0), W / 2, cy - cs * .6))
    ev.append("Dialogue: 1,%s,%s,Sub,,0,0,0,{\\an5\\pos(%g,%g)\\fad(1200,1200)}Part 1: the oldest ice, ancient DNA,%sand life sealed under the ice. Illustrations; open questions labelled." % (ts(2.5), ts(9.0), W / 2, cy + cs * 1.9, nl))
    for shn, lab, src in STAGE:
        s0 = shot_start(shn); s1 = s0 + next(sh["dur"] for sh in SHOTS if sh["name"] == shn)
        a0, a1 = s0 + .3, s1 - .3
        src0, src1 = a0 + .3, a1
        if shn == "s01_field": a0, src0 = 9.3, 9.6
        ev.append("Dialogue: 1,%s,%s,Stage,,0,0,0,{\\fad(400,400)}%s" % (ts(a0), ts(a1), esc(lab)))
        ev.append("Dialogue: 1,%s,%s,Src,,0,0,0,{\\fad(400,400)}%s" % (ts(src0), ts(src1), esc(src)))
    # Pillow boards are scaled into the top of the frame (see the segment encode) so this band, y 640-720,
    # sits on empty cream under the body text, the citations and the NOT SETTLED / PUBLISHED PLAN pills.
    # The vertical cut puts the captions under the picture.
    pil = []; t = 0.0
    for sh in SHOTS:
        if sh["cam"] is None: pil.append((t, t + sh["dur"]))
        t += sh["dur"]
    def on_pil(a, b): return any(p0 <= (a + b) / 2 < p1 for p0, p1 in pil)
    if not vertical:
        for p0, p1 in pil:
            if abs(p1 - DUR) < .01: continue   # the end card has no narration
            ev.append("Dialogue: 0,%s,%s,Band,,0,0,0,{\\an7\\pos(0,640)\\fad(300,300)\\1a&H30&\\p1}m 0 0 l %d 0 l %d 80 l 0 80{\\p0}" % (ts(p0 + .4), ts(p1 - .4), W, W))
    for start, sid in CUES:
        d = dur(os.path.join(HERE, "audio", "t_%s.wav" % sid)); text = narr[sid]
        pieces = chunks(text); times = caption_times(text, pieces, words_timed(sid), d)
        for i, (p, (a, b)) in enumerate(zip(pieces, times)):
            a_ = start + max(0.0, a - .08); b_ = start + b + .35
            if i + 1 < len(pieces): b_ = min(b_, start + times[i + 1][0] - .08)
            mv = 14 if (on_pil(a_, b_) and not vertical) else 0
            ev.append("Dialogue: 2,%s,%s,Narr,,0,0,%d,%s" % (ts(a_), ts(min(b_, DUR)), mv, esc(p)))
    return head + "\n".join(ev) + "\n"

def run(cmd): print(" ".join(cmd)[:220], flush=True); subprocess.check_call(cmd)

def frame_path(n):
    """Corrected Pillow frames (footer wording) live in work/pil. 3D frames stay in the render directory."""
    alt = os.path.join(W0, "pil", "f_%04d.png" % n)
    if os.path.exists(alt) and os.path.getsize(alt) > 1000: return alt.replace("\\", "/")
    return os.path.join(FR, "f_%04d.png" % n).replace("\\", "/")

def _frame_var(path):
    from PIL import Image
    a = np.asarray(Image.open(path).convert("RGB").resize((48, 27)), dtype="float32")
    return float(((a - a.mean(axis=(0, 1))) ** 2).mean())

def hold_cream(fa, fb):
    """Pillow passages fade in and out through a blank cream frame. Hold the first and last frame of the
    base fade (the board itself, not the later element animation) across those edges."""
    inn = min(fb, fa + int(0.75 * FPS))
    out = max(fa, fb - int(1.15 * FPS))
    ready = _frame_var(frame_path(inn))
    leaving = _frame_var(frame_path(out))
    tin, tout = 0.8 * ready, 0.8 * leaving
    first = next((i for i in range(fa, inn + 1) if _frame_var(frame_path(i)) >= tin), inn)
    last = next((i for i in range(fb, out - 1, -1) if _frame_var(frame_path(i)) >= tout), out)
    if first > last: first = last
    return [first if i < first else last if i > last else i for i in range(fa, fb + 1)]

# ---- trim the Kokoro clips (lead/tail silence)
for _, sid in CUES:
    out = os.path.join(HERE, "audio", "t_%s.wav" % sid)
    if not os.path.exists(out) or "--retrim" in sys.argv:
        run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(HERE, "audio", sid + ".wav"), "-af",
             "silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.1,areverse", "-ar", "24000", "-ac", "1", out])
if "--plan" in sys.argv:
    t = 0.0
    for sh in SHOTS: print("%7.1f-%7.1f  %s" % (t, t + sh["dur"], sh["name"])); t += sh["dur"]
    for start, sid in CUES:
        d = dur(os.path.join(HERE, "audio", "t_%s.wav" % sid)); print("%7.1f-%7.1f  %s (%.1f s)" % (start, start + d, sid, d))
    print("total", DUR); sys.exit(0)
open(os.path.join(HERE, "caps.ass"), "w", encoding="utf8").write(ass(False))
open(os.path.join(HERE, "caps_v.ass"), "w", encoding="utf8").write(ass(True))
if "--caps-only" in sys.argv: sys.exit(0)

# ---- music bed: slow pad, CC0, generated here (open fifths, lower than ep6)
bed = os.path.join(W0, "bed.wav")
if not os.path.exists(bed):
    sr = 44100; n = int(DUR * sr); x = np.arange(n) / sr
    chords = [[73.42, 110.0, 146.83, 220.0], [65.41, 98.0, 130.81, 196.0], [58.27, 87.31, 116.54, 174.61], [69.30, 103.83, 138.59, 207.65]]
    L = np.zeros(n); R = np.zeros(n); bar = 13.0
    for i in range(int(DUR / bar) + 2):
        t0 = i * bar; a = int(t0 * sr); b = min(n, int((t0 + bar + 3.0) * sr))
        if a >= n: break
        tt = np.arange(b - a) / sr; env = np.minimum(1, tt / 3.5) * np.minimum(1, (bar + 3.0 - tt) / 2.5)
        for k, f in enumerate(chords[i % 4]):
            for det, pan in ((0.996, 0.3), (1.004, 0.7)):
                w = np.sin(2 * np.pi * f * det * tt + k) * env * 0.045 * (1 + 0.25 * np.sin(2 * np.pi * 0.06 * tt + k))
                w += np.sin(2 * np.pi * f * det * 2 * tt + k) * env * 0.008
                L[a:b] += w * (1 - pan); R[a:b] += w * pan
            bass = np.sin(2 * np.pi * (f / 2) * tt) * env * 0.025; L[a:b] += bass; R[a:b] += bass
    fade = np.minimum(1, x / 2.0) * np.minimum(1, (DUR - x) / 3.0)
    st = np.stack([L * fade, R * fade], 1); st = st / np.abs(st).max() * 0.9
    with wave.open(bed, "wb") as w_:
        w_.setnchannels(2); w_.setsampwidth(2); w_.setframerate(sr); w_.writeframes((st * 32767).astype("<i2").tobytes())

# ---- audio mix
ins = ["-i", bed]; fl = []; names = []
for i, (start, sid) in enumerate(CUES):
    ins += ["-i", os.path.join(HERE, "audio", "t_%s.wav" % sid)]; ms = int(start * 1000)
    fl.append("[%d:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay=%d|%d,volume=1.0[v%d]" % (i + 1, ms, ms, i)); names.append("[v%d]" % i)
fl.append("[0:a]volume=0.10[bed]")
fl.append("[bed]%samix=inputs=%d:normalize=0:duration=first,loudnorm=I=-16:TP=-1.5:LRA=11,afade=t=out:st=%g:d=2.5[a]" % ("".join(names), len(names) + 1, DUR - 2.5))
mix = os.path.join(W0, "mix.wav")
run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(fl), "-map", "[a]", "-ar", "48000", mix])

# ---- video: segments in shot order. Blender runs = odd frames at 12 fps -> minterpolate 24; Pillow runs = 24 fps as is.
segs = []; f = 1
for sh in SHOTS:
    n = int(round(sh["dur"] * FPS)); kind = "pil" if sh["cam"] is None else "bl"
    segs.append([kind, f, f + n - 1, n]); f += n
parts = []
BOARDS = {"diag_layers", "diag_dna", "diag_revive", "diag_siberia", "diag_map", "diag_risk", "diag_treaty", "diag_jobs"}
for i, ((kind, fa, fb, nout), sh) in enumerate(zip(segs, SHOTS)):
    out = os.path.join(W0, "seg%02d.mp4" % i); parts.append(out)
    if os.path.exists(out) and "--redo" not in sys.argv: continue
    if kind == "bl":
        lst = os.path.join(W0, "seg%02d.txt" % i)
        frs = list(range(fa if fa % 2 == 1 else fa + 1, fb + 1, 2))
        with open(lst, "w") as fh:
            for fr in frs:
                fh.write("file '%s'\nduration %f\n" % (os.path.join(FR, "f_%04d.png" % fr).replace("\\", "/"), nout / FPS / len(frs)))
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-vf",
             "minterpolate=fps=%d:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,tpad=stop_mode=clone:stop_duration=0.5,format=yuv420p" % FPS, "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-frames:v", str(nout), out])
    else:
        # hold the solid frame over the blank cream fade, and (on the four boards) shrink the art
        # so the caption band at y 640-720 sits clear of body text, citations and the status pills
        seq = hold_cream(fa, fb)
        lst = os.path.join(W0, "seg%02d.txt" % i)
        with open(lst, "w") as fh:
            for fr in seq:
                fh.write("file '%s'\nduration %f\n" % (frame_path(fr), 1.0 / FPS))
            fh.write("file '%s'\n" % frame_path(seq[-1]))
        vf = "format=yuv420p"
        if sh["name"] in BOARDS:
            vf = "scale=1172:660:flags=lanczos,pad=1280:720:54:0:color=0xF3EDE0,format=yuv420p"
        # -r 24 and the same timescale as the Blender segments, or the concat stretches the whole film by 25/24
        run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-vf", vf,
             "-r", str(FPS), "-fps_mode", "cfr", "-video_track_timescale", "12288",
             "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-frames:v", str(fb - fa + 1), out])
cat = os.path.join(W0, "cat.txt")
with open(cat, "w") as fh:
    for p, sh in zip(parts, SHOTS):   # exact durations: Blender segments carry a longer last packet, which drifted the picture late (ep10 fix, applied 11/6)
        fh.write("file '%s'\nduration %.6f\n" % (p.replace("\\", "/"), int(round(sh["dur"] * FPS)) / FPS))
full = os.path.join(W0, "full.mp4")
run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", cat, "-c", "copy", full])
print("full", dur(full))

caps = os.path.join(HERE, "caps.ass").replace("\\", "/").replace(":", "\\:")
caps_v = os.path.join(HERE, "caps_v.ass").replace("\\", "/").replace(":", "\\:")
out = os.path.join(HERE, NAME + ".mp4")
run(["ffmpeg", "-y", "-loglevel", "error", "-i", full, "-i", mix, "-filter_complex", "[0]fade=t=in:st=0:d=1.2,fade=t=out:st=%g:d=1.5,subtitles='%s',format=yuv420p[v]" % (DUR - 1.5, caps),
     "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-profile:v", "high", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "160k", "-shortest", out])
outv = os.path.join(HERE, NAME + "-vertical.mp4")
run(["ffmpeg", "-y", "-loglevel", "error", "-i", full, "-i", mix, "-filter_complex",
     "[0]fade=t=in:st=0:d=1.2,fade=t=out:st=%g:d=1.5,split[a][b];[a]scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,gblur=sigma=28,eq=brightness=-0.12[bg];[b]scale=720:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-40,subtitles='%s',format=yuv420p[v]" % (DUR - 1.5, caps_v),
     "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "slow", "-crf", "22", "-profile:v", "high", "-movflags", "+faststart", "-c:a", "aac", "-b:a", "160k", "-shortest", outv])
poster = int(PF)
if not os.path.exists(os.path.join(FR, "f_%04d.png" % poster)):
    poster += 1 if poster % 2 == 0 else -1   # Blender kept the odd frames only
run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(FR, "f_%04d.png" % poster).replace("\\", "/"), "-vf", "scale=1280:-1", "-q:v", "3", os.path.join(HERE, NAME + ".jpg")])
for p in (out, outv, os.path.join(HERE, NAME + ".jpg")): print(p, round(os.path.getsize(p) / 1e6, 2), "MB")
