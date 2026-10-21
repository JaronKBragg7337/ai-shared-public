#!/bin/bash
# Open Questions 9.2 build: run from this folder. Needs script.json.  CPU/Pillow only.
set -e
SLUG=openquestions-ep2-no-brain
export OQ_EP=9.2 TVCHUNK=1
[ -f audio/s1.wav ] || node ../oqtts.mjs
python ../oqprep.py
python ep.py land --out video_land.mp4
python ep.py port --out video_port.mp4
for o in land port; do
  N=$SLUG; [ $o = port ] && N=$SLUG-vertical
  ffmpeg -y -v error -i video_$o.mp4 -i audio/voice.wav -i audio/music.wav -filter_complex "[1:a]volume=1.0[v];[2:a]volume=0.14[m];[v][m]amix=inputs=2:normalize=0[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $N.mp4
done
python ep.py land --still $(python -c "import json;print(json.load(open('timeline.json'))['total']*0.30)") $SLUG.png
python -c "from PIL import Image;Image.open('$SLUG.png').convert('RGB').save('$SLUG.jpg',quality=88)"
ls -la $SLUG*.mp4 $SLUG.jpg
