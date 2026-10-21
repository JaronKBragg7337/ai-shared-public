#!/bin/bash
# usage (inside an episode folder): bash ../../tv-lib/build.sh ep.py slug   -> slug.mp4, slug-vertical.mp4, slug.jpg
set -e
EP=$1; SLUG=$2; LIB="$(dirname "$0")"
mkdir -p audio
[ -f audio/s1.wav ] && [ -z "$REDO_TTS" ] || node "$LIB/tts.mjs"
python "$LIB/prep.py"
python $EP land --out video_land.mp4
python $EP port --out video_port.mp4
for o in land port; do
  N=$SLUG; [ $o = port ] && N=$SLUG-vertical
  V=video_$o.mp4
  ffmpeg -y -v error -i $V -i audio/voice.wav -i audio/music.wav -filter_complex "[1:a]volume=1.0[v];[2:a]volume=0.14[m];[v][m]amix=inputs=2:normalize=0[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $N.mp4
done
python $EP land --still $(python -c "import json;print(json.load(open('timeline.json'))['total']*0.55)") $SLUG.png
python -c "from PIL import Image;Image.open('$SLUG.png').convert('RGB').save('$SLUG.jpg',quality=88)"
ls -la $SLUG*.mp4 $SLUG.jpg
