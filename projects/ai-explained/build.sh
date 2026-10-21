#!/bin/bash
# usage (inside an episode folder): bash ../build.sh slug [land|port|both]  (voice already made by tv-lib/tts.mjs; runs aiprep.py for timeline+music)
set -e
SLUG=$1; WHICH=${2:-both}; LIB="$(cd "$(dirname "$0")" && pwd)"
python "$LIB/aiprep.py"
for o in land port; do
  [ $WHICH = both ] || [ $WHICH = $o ] || continue
  TVCHUNK=2 python ep.py $o --out video_$o.mp4
  N=$SLUG; [ $o = port ] && N=$SLUG-vertical
  ffmpeg -y -v error -i video_$o.mp4 -i audio/voice.wav -i audio/music.wav -filter_complex "[1:a]volume=1.0[v];[2:a]volume=0.14[m];[v][m]amix=inputs=2:normalize=0[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $N.mp4
done
