# Studio save options (Sonnet 5.5, branch studio-save, worktree C:\Users\lilli\Projects\ho-studio-save)

## What changed
- New studio/save.js: one bottom sheet used by the Beat Lab ("Save / share beat", "Save parts") and the finished song (step 4, "Save / share my song" and "Save vocals only").
- Order (per Jaron's iPhone result): MP3 first and highlighted ("best for sharing, about 4 MB"), Share or save to Files, Save as video (Photos / Gallery; 30 s clip or full song), WAV ("big file, for mixing", ~33 MB for 3 min), Save the parts.
- Every result shows a Share now button (only if navigator.canShare({files})), a visible Download link (anchor + download, never opens the blob in the tab), and the note: iPhone Files app > Recents (usually iCloud Drive, or Downloads); Android Files > Downloads.
- Share is always a fresh tap on a ready file (user activation safe); AbortError is ignored quietly.
- Parts: one navigator.share with all 4 files if supported, else 4 separate cards with their own buttons/links.
- MP3: lamejs 1.2.1 (LGPL-3.0) vendored at studio/vendor/lame.min.js, loaded only when MP3 is chosen. 192 kbps stereo.
- Video: 540x960 canvas (warm dark, pulse, waveform, progress, name, Heartbeat Observatory) + MediaRecorder; mp4 (H.264/AAC) preferred, WebM fallback. Real time; Cancel button.
- Object URLs are revoked 5 min after the sheet closes.
- index.html: old downloadLink removed; save() mixes then opens the sheet. beatlab.js: dl() removed.

## Tested (Chromium, 390x844, headless)
- node --check OK; no page errors; no sideways scroll (page or sheet).
- Beat Lab: sheet opens, WAV 32 MB (pcm 2ch), MP3 4.4 MB (ffprobe: mp3 stereo, 184 s, matches WAV), 30 s video (ffprobe: h264 540x960 + aac stereo, 30.2 s), parts = 4 cards. Share path absent in headless so the Download-link fallback is what ran.

## Needs a real iPhone / Android test
- navigator.share with files: Save to Files, and Save Video into Photos (iPhone), Android share sheet.
- Video recording on iOS Safari (MediaRecorder mp4, audio capture from AudioContext, screen must stay on and page open); iOS may mute/pause when the screen locks.
- The finished-song path (step 4) was not exercised end to end (needs a recorded take); it uses the same sheet.
- Android WebM video may not play in some gallery apps; MP3 is the safe choice there.
