#!/bin/bash
# Still Unknown ep3 build (after TTS + prep + music): render land + port (Pillow + Blender loops), mux, poster.   usage: bash build.sh
set -e
SLUG=stillunknown-ep3-vibration-stone
(cat ep_head.py; echo; cat ep_body.py) > ep.py
python ep.py land --out video_land.mp4 > land.log 2>&1
python ep.py port --out video_port.mp4 > port.log 2>&1
for o in land port; do
  N=$SLUG; [ $o = port ] && N=$SLUG-vertical
  ffmpeg -y -v error -i video_$o.mp4 -i audio/voice.wav -i audio/music.wav -filter_complex "[1:a]volume=1.0[v];[2:a]volume=0.16[m];[v][m]amix=inputs=2:normalize=0[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart $N.mp4
done
python ep.py land --still 2.6 $SLUG.png
python -c "from PIL import Image;Image.open('$SLUG.png').convert('RGB').save('$SLUG.jpg',quality=88)"
ls -la $SLUG*.mp4 $SLUG.jpg
