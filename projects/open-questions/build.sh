#!/bin/bash
# usage (inside an episode folder): bash ../build.sh ep.py slug [land|port|both]   -> slug.mp4 (16:9) and/or slug-vertical.mp4 (9:16), slug.jpg poster
set -e
EP=$1; SLUG=$2; WHICH=${3:-both}; LIB="$(cd "$(dirname "$0")" && pwd)"
mkdir -p audio
[ -f audio/s1.wav ] || [ -f audio/q1.wav ] && [ -z "$REDO_TTS" ] || node "$LIB/oqtts.mjs"
python "$LIB/oqprep.py"
for o in land port; do
  [ $WHICH = both ] || [ $WHICH = $o ] || continue
  python $EP $o --out video_$o.mp4
  N=$SLUG; [ $o = port ] && N=$SLUG-vertical
  ffmpeg -y -v error -i video_$o.mp4 -i audio/voice.wav -i audio/music.wav -filter_complex "[1:a]volume=1.0[v];[2:a]volume=0.14[m];[v][m]amix=inputs=2:normalize=0[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $N.mp4
done
