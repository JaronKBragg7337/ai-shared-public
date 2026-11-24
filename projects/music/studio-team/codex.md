# Codex lane report - 2026-10-24

Branch: studio-codex. Changed only studio/index.html. No push, deployment, or service settings changed.

COMMIT BLOCKED: git add failed with Permission denied creating C:/Users/lilli/Projects/heartbeat-observatory/.git/worktrees/ho-studio-codex/index.lock. No commit was created. The shared Git metadata is outside this session's writable root. Local studio.patch and commit-message.txt are ready for handoff.

## Found and fixed
- Recording used UI callback time, could open the mic twice, and did not preserve an interrupted take reliably. Added inline AudioWorklet capture with audio-clock timestamps, a ScriptProcessor fallback, guarded mic startup, track cleanup, and pause/review on backgrounding or audio suspension.
- Punch preview silenced the whole old layer, and review could stop before a take beyond the beat ended. Preview now preserves the old audio around the punch and includes pending-take duration. Redo uses the original layer, and recording during playback starts at the current playhead.
- Gain and mute changes did not affect active playback. Added live volume/mute/pan, beat volume, and optional 80 Hz rumble filtering plus gentle compression. Playback and offline export share the voice chain; original takes are unchanged.
- Saving could omit the take under review, report success prematurely, or leave controls stuck after failure. Require keep/delete first, guard concurrent changes, handle errors, and keep a visible download link for retry.
- Older beat fetches could overwrite a newer selection. Added request sequencing, import guards, and Beat Lab load failure handling.
- Headphone sync could count duplicate taps and wrapped longer delays onto the next click. Use wider nonoverlapping click windows, one tap per click, consistent latency subtraction, and honest wording: an estimate for NEW takes, including tap timing.
- Added phone layout constraints, focus outlines, status announcements, and visible left/right labels.

## Tested
26 browser regression checks passed in connected desktop Chrome using a temporary local harness and synthetic microphone stream. Covered 390 px content width (including six layers and Beat Lab), real MP3 fetch/decode, punch preview/keep/undo, live gain/mute, voice processing and stereo 44.1 kHz WAV headers, persistent download link, AudioWorklet capture, fallback capture, take review beyond beat end, mic denial, duplicate/cancelled mic requests, audio suspension, export failure recovery, sync lock/cancel, stale beat fetch, and existing Beat Lab mount. Inline module passes node --check; git diff --check passes. No real microphone permission or beat request was sent. Standalone headless Chrome was unavailable; connected Chrome supplied the browser evidence.

## Still missing / not tested
- Real iPhone Safari, physical mic/headphone routes, Bluetooth timing, perceptual sound quality, actual iOS Files/share behavior, and long-song memory pressure need device testing. The legacy capture fallback still estimates timing from callbacks.
- No recoverable project/autosave: a reload can still lose work. WAV export does not preserve editable layers or undo history. Long recordings and undo copies can consume substantial phone memory.
- Beat Lab musical changes and artist learning/lyrics tools belong to the other lanes. Beat request delivery was left untouched and untested. Updated the stale Beat Lab footer.

API references checked: https://developer.mozilla.org/en-US/docs/Web/API/BaseAudioContext/state and https://www.w3.org/TR/webaudio/ (2026-10-24).

Report delivery: the requested AI-Shared path was denied by the filesystem restriction. This local copy is the completed report.
