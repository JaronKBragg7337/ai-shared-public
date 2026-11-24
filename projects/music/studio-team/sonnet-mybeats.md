# Studio "My beats" (Sonnet 5.5, branch studio-mybeats, worktree C:\Users\lilli\Projects\ho-studio-mybeats)

## What changed
- Beat Lab: every dice roll and every edit auto-saves the recipe (the `o` object, JSON) to localStorage key hb-studio-beats-v1 (debounced, try/catch). Last 30 non-kept entries ("Recent"); "Keep this beat" star pins one forever (also a Keep button per list entry). List shows name, style, key, BPM, time; tap = reopen that exact beat, fully editable; Rename (inline); Delete is two taps (4 s confirm).
- Recipe travels with files (studio/save.js): WAV gets a LIST/INFO ICMT chunk, MP3 an ID3v2.3 TXXX "hbrecipe" frame (ffprobe shows it). Parts WAVs carry it too. Video skipped.
- "Open a saved beat file" button in the Lab and the existing "Upload your own beat" (index.html): if the file has a recipe, the beat still loads to record over as before, plus a button "Open in Beat Lab to edit". No recipe = Lab says so and points to Upload.
- Determinism: the engine used Math.random for drum noise, the reverb impulse and noise start offsets, so every render differed. Now seeded (fixed seed per graph). Notes/structure are identical every time.
- MP3 headroom (coordinator add): before encoding, the buffer is scaled so its sample peak is at most -4 dBFS (only if higher). Measured: -2.9 dBFS in gave -0.6 dBTP out from lame, so the -1.0 dBFS cap would not have been enough; with -4 dBFS the MP3 measures -1.0 dBTP.

## Tested (Chromium 390x844)
- Rolled 3 beats: 3 entries; kept one; reloaded: list and kept state survived; reopened by tap; saved WAV before and after reload.
- Same recipe rendered twice: notes/chords/drums/melody JSON identical; samples match to about 52-61 dB SNR (max diff ~0.002), not bit-identical.
- Saved WAV and MP3, imported into the Lab (recipe restored, entry created, no duplicate on repeat), imported MP3 via Upload (offer button shown, opened Lab), plain WAV without recipe gives the plain message. Delete two-tap works. No page errors, no sideways scroll.

## Known limit
- Not bit-identical: Chromium's offline audio engine leaves tiny float differences between renders (checked: single drum/bass pieces are exact; keys/melody/reverb differ ~1e-8, and some mid pieces ~4e-4). It is inaudible (about -55 dB), the notes are identical. Making it exact would mean replacing the browser's reverb/filters with our own code.

## Needs a real iPhone
- localStorage persistence in Safari (private mode just disables saving), the file pickers showing the saved WAV/MP3, share sheet with the embedded recipe, MP3 true peak check on a new save.
