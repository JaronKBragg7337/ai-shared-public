#!/bin/bash
# Derived from Earth 17.1; CPU-only, sequential render, local outputs only.
set -euo pipefail
cd "$(dirname "$0")"
LIB='C:/Users/lilli/AI-Shared/projects/tv-lib'
SLUG=lostplaces-ep1-gobekli
if [ ! -f audio/s12.wav ] || [ "${REDO_TTS:-}" = 1 ]; then
  node "$LIB/tts.mjs" bm_george
fi
python prep.py
python ep.py land --qa
python ep.py land --out video_land.mp4
python ep.py port --out video_port.mp4
for o in land port; do
  N=$SLUG
  if [ "$o" = port ]; then N=$SLUG-vertical; fi
  ffmpeg -y -v error -i "video_$o.mp4" -i audio/voice.wav -i audio/music.wav \
    -filter_complex '[1:a]volume=1.0[v];[2:a]volume=0.10[m];[v][m]amix=inputs=2:normalize=0[a]' \
    -map 0:v -map '[a]' -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$N.mp4"
done
python "$LIB/verify_voice.py" "$SLUG.mp4" script.json --json verify_voice-land.json
python "$LIB/verify_voice.py" "$SLUG-vertical.mp4" script.json --json verify_voice-vertical.json
