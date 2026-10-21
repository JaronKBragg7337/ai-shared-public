# Lost Places 22.1 — local test build

**Did we build civilization backward? — Göbekli Tepe**  
Completed 2026-10-18 14:55:53 America/Indianapolis. Length: **6:32** in both orientations.

| Output | Dimensions | Duration | Bytes |
|---|---|---|---|
| lostplaces-ep1-gobekli.mp4 | 1280×720 | 391.772 s | 15,099,784 |
| lostplaces-ep1-gobekli-vertical.mp4 | 1080×1920 | 391.772 s | 17,409,870 |

Poster: `lostplaces-ep1-gobekli.jpg` (1280×720). The build, script, sources, checker verdict and verification logs are in this folder.

## What was verified

- DAI and academic source checks cover dating methods and c. 9500–8000 BCE settlement chronology; carved T pillars and animals; Building D's c. 5.5 m central pair; Schmidt's sanctuary and food-demand hypothesis; Clare's domestic occupation and possible rainwater features; grain processing versus cultivation/domestication; slope-slide versus intentional-fill interpretations; Karahan Tepe and the Taş Tepeler regional context; and local quarry/stone-tool evidence. `SOURCES.md` links the evidence and states access limits.
- Required independent read-only Codex fact-check (gpt-6-luna, high): **0 WRONG narration claims**, twelve segments OK. Corrected two citation details: Karul's issue/pages and the identifiable Uzdurum et al. 2023 on-screen reference. A second pass was not required by the brief's >3-WRONG rule.
- Pillow visual review: every scene sampled in both orientations; all ninety caption phrases checked for fit. Earlier diagram/footer and final-source-list collisions were corrected before rendering. Final MP4 frames were extracted at all twelve scene midpoints for visual review.
- Both final files decode completely without FFmpeg errors; H.264 video and AAC audio, 24 fps, expected aspect ratios and matching duration. Details: `output_checks.json`. Audio in both files measures mean −18.6 dB, peak −3.7 dB (no digital clipping); full logs: `levels-land.log`, `levels-vertical.log`.
- Voice gate run on each final MP4 with the shared, unmodified `verify_voice.py`, default small.en model and default 5% missing-word threshold:
- land: PASS, all 12 segments; 7 unmatched normalized words in total; highest segment missing rate 2.7%.
- vertical: PASS, all 12 segments; 7 unmatched normalized words in total; highest segment missing rate 2.7%.

The first landscape run flagged s6, s9 and s11. The unmatched lists were dominated by Turkish proper names (Göbekli Tepe, Taş Tepeler, Necmi Karul). Added only those names, plus Karahan, to the verifier's documented `verify_ignore.txt` mechanism and reran both cuts. Ordinary narration words remain checked; no threshold, verifier code, or transcript was altered.

## Production method and limits

Copied the working Earth 17.1 script/renderer/build/source files as `template-earth-*`, then adapted the schema and tv-lib caption/timeline method. Original parchment, terracotta and limestone look; generic illustrative diagrams rather than excavation photographs or surveyed reconstructions. The vertical is the full 16:9 picture over a blurred backdrop, with larger captions beneath and repeated readable source credits. Twelve drawing frames per second are encoded at 24 fps; diagrams are mostly held illustrations with crossfades and a moving progress indicator, not a 3D reconstruction.

Narration: local Kokoro `bm_george`, sentence-chunked by shared `tts.mjs`; numeric speech is supplied through `say`. Local prep trims silence and applies an additional 1.04× tempo adjustment, preserving pitch, after the template's 1.1× TTS setting. Music is the template's generated quiet drone, mixed at 0.10. Rendering and speech generation used CPU only; no GPU work was started.

Remaining weaknesses: no human listening pass or independent Gemini/Grok whole-video audiovisual review was performed. The voice gate checks speech completeness, not pronunciation quality, music taste or perfect caption timing. Captions follow the template's proportional phrase timing rather than word-level forced alignment. Some primary paper PDF endpoints were inaccessible; where a catalogue, author-paper mirror, abstract, or indexed full-text passage was used instead, `SOURCES.md` says so. The earliest occupation's permanence, precise water-feature functions, exact ritual uses, transport/workforce and individual fill histories remain uncertain and are qualified in the episode. The opening familiar farming→villages→monuments sequence is explicitly treated as incomplete, not as a universal archaeological chronology.

## Time and usage

Wall-clock start from the supplied runner's `timing.txt`: 2026-10-18 14:38:58. Report written 14:55:53: **16.9 minutes** total, including research, fact-check, writing, TTS, rendering and verification. Pillow render times (land, vertical): 139.5, 139.2 seconds.

The independent fact-check CLI reports **65,750 tokens used** in `factcheck.log`. This is that subprocess's own logged figure; parent-session token usage and billing are not exposed here and are not estimated. TTS and speech verification ran locally.

Nothing was published. No website repository, Supabase, social queue or git was touched. No process was killed. Project writes stayed in this episode folder.
