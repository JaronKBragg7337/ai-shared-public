# Fable report - Beat Lab (studio/beatlab.js), 2026-10-24

Worktree C:\Users\lilli\Projects\ho-studio-fable, branch studio-fable, one commit. Not pushed, main untouched.

## Found wrong or missing (whole Studio)
- Beat Lab: every dice press kept tempo, bounce, energy, kit and all four sounds; only the seeds and key changed. Pools were small
  (6-7 chord moves per mood, 3 tune rhythms per style, 2-3 drum templates, one hat pattern). That is why rolls "sounded close" (Jaron, iPhone).
- Beat Lab mix: highs (2-8 kHz) sat 16 dB under the sub, so on a phone speaker the beat was mostly a dull thump: -12.8 LUFS full,
  -18.3 LUFS through a 250 Hz highpass (phone speaker simulation).
- Beat Lab: no fills, no risers, no drop into the hook, verse 2 identical to verse 1; bass always one note per kick.
- Drum grid at 390 px: 16 squares plus a 44 px label in one row = 17 px squares, too small to tap.
- Studio (index.html, not my file, not changed): "Save parts" fires 4 downloads in a row; iOS Safari usually only allows one per tap.
  The "Hear it" button has no position/time while it plays. A Lab beat loaded with "Use this beat" is not shown as the selected
  card in the beat list (status line says it loaded, the list still shows no selection).

## What I changed (studio/beatlab.js only)
- Variety per dice press (new `roll()`, also exported): inside the chosen style every press picks key, 14 chord moves per mood
  (was 6-7), chord inversions that move the least note to note, drum template from a wider pool, hat pattern (per-style pool +
  common pool), kit, bass/chords/melody sounds from per-style pools, tempo nudge, bounce nudge, energy, bass mode (locked to kick /
  one note per half bar / off-beat root-fifth line / walking line), tune rhythm (style pool + 8 common), tune shape (steps,
  leaps, riff = one bar cell moved with the chords), note lengths, and arrangement flags (which verse phrases carry the tune,
  hook octave lift, double-time hats, intro tune, chord stab rhythm). One press in four flips major/minor.
- Measured check (node variety.mjs, 10 dice presses per style, distinct results):
  style   | chords | drums | hats | sound set | bpm | tune rhythm | tune | bass mode | arrangement
  trap    |   8    |   9   |  5   |     9     |  9  |      8      |  10  |     2     |     7
  drill   |   8    |  10   |  6   |     5     |  5  |      8      |  10  |     2     |     7
  boombap |   8    |   7   |  6   |     9     |  6  |      8      |  10  |     2     |     7
  lofi    |   8    |   9   |  6   |     7     |  8  |      8      |  10  |     3     |     7
  rnb     |   8    |   9   |  5   |     9     |  7  |      8      |  10  |     2     |     7
  afro    |   8    |   9   |  6   |    10     |  6  |      8      |  10  |     2     |     7
  Before: chords 6-7 pool, drums 2-5 pool, hats 1, sound set 1, bpm 1, tune rhythm 3, bass mode 1, arrangement 1.
- Three new styles: Drill (sliding 808s, off-beat snares, skipping hats, dark saw lead), Lo-fi (soft kit, wobbling electric piano,
  vinyl crackle), Afrobeats (bouncy kick, shakers, percussion, log-drum bass, plucked chords, bright by default). Each has a one-line
  plain description under the chips.
- Drum sounds: kick = sub sweep + mid "knock" + click (the knock is what a phone plays); snare = body + separate 4 kHz snap + tone;
  clap = 4 layers + snap; hats two layers, panned a touch; new rim, shaker, perc, crash, riser, crackle. 808 = pitch-drop body +
  a triangle harmonic so the note is heard without sub; slides glide into the next chord and a long slide into every hook; log drum.
- Arrangement: snare roll + riser into every hook, crash on hook bar 1, verse 2 opens stripped (4 bars, no bass, quiet keys), the
  last bar before a change drops out, melody gets a dotted-eighth echo, few-ms humanize on hats/snares/tune.
- Mix: drum bus saturation + high shelf, master presence bump at 3.2 kHz, 15.5 kHz lowpass, then in plain JS on the stitched
  mix: gated-RMS loudness normalize (sparse R&B lands as loud as busy trap), glue compressor, soft saturation, lookahead limiter with
  a smooth 1.5 ms ramp and a between-sample peak estimate (ceiling -2.9 dBFS so true peak stays under 0).
- Lab page: three numbered steps, style description line, Full song / Short (half the bars) choice, drum grid labels above each
  row so the 16 squares get the full width (34 px tall, gap every beat), aria-pressed on steps, length line updates when tempo moves.
- API unchanged: compose, render, mount({getCtx, onUse, wav}); index.html needs no change.

## Measured (ffmpeg loudnorm / astats on WAVs saved through the real page in headless Chromium at 390x844, seed 7)
  style    | LUFS full | true peak | phone sim (HP 250 Hz) | 2-8 kHz vs sub | render 3 min
  before trap | -12.8 | -0.4 dBTP | -18.3 LUFS | -16 dB | 4.9 s
  trap     | -12.8 | -0.7 | -17.0 | -10.4 dB | 6.4 s (3:35)
  drill    | -12.5 | -0.8 | -17.9 | -10.7 | 6.1 s
  boombap  | -13.6 | -0.6 | -17.0 | -11.2 | 4.9 s
  lofi     | -13.3 | -0.5 | -15.6 | -8.8 | 6.6 s
  rnb      | -14.1 | -0.6 | -17.9 | -11.2 | 6.0 s
  afro     | -13.9 | -1.2 | -19.7 | -10.9 | 4.6 s
  Sample peaks never over -2.9 dBFS. The sub band is still the loudest on headphones (on purpose).

## Tested
- node --check; direct render probe for all 6 styles (no errors); page click-through at 390 px: styles, dice, Short, grid tap,
  Mute, Hear it (plays/stops), Use this beat (status "Your beat is loaded"), Save WAV download; scrollWidth 390 (no sideways scroll).

## Not tested
- Real iPhone Safari (no WebKit AudioContext headless here). Listening: I cannot hear; everything above is by measurement + theory.
- Render speed on a real phone (desktop Chromium is 4.6-6.6 s for a full song; was 2.9-4.9 s; the new master stage is ~0.5 s of that).
- True peak is measured by ffmpeg; the one place I could not get under -0.5 dBTP without the lower ceiling was dense hat bursts.
