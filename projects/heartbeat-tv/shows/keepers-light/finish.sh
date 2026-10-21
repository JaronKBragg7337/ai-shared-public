#!/bin/bash
# frames + soundtrack -> titled H.264 mp4 (+ poster jpg).   ./finish.sh [EP] [FRAMES_DIR] [POSTER_FRAME]
#   ep.1: ./finish.sh            (frames/, soundtrack.wav, t2.txt)
#   ep.2: ./finish.sh 2 C:/Users/lilli/Renders/keepers-ep2/frames 0790   (soundtrack_ep2.wav, t2_ep2.txt)
cd "$(dirname "$0")"
EP=${1:-1}
FR=${2:-frames}
PF=${3:-0480}
if [ "$EP" = "1" ]; then SND=soundtrack.wav; T2=t2.txt; else SND=soundtrack_ep$EP.wav; T2=t2_ep$EP.txt; fi
OUT=keepers-light-ep$EP
F="C\:/Windows/Fonts"
ffmpeg -y -loglevel error -framerate 24 -i "$FR/f_%04d.png" -i "$SND" -filter_complex "\
[0]drawtext=fontfile='$F/georgia.ttf':textfile=t1.txt:fontsize=64:fontcolor=white:x=(w-tw)/2:y=h*0.2:shadowcolor=black@0.5:shadowx=2:shadowy=2:alpha='if(lt(t,2.5),0,if(lt(t,4),(t-2.5)/1.5,if(lt(t,8),1,if(lt(t,9.5),(9.5-t)/1.5,0))))',\
drawtext=fontfile='$F/georgiai.ttf':textfile=$T2:fontsize=34:fontcolor=white:x=(w-tw)/2:y=h*0.2+84:shadowcolor=black@0.5:shadowx=2:shadowy=2:alpha='if(lt(t,3.5),0,if(lt(t,5),(t-3.5)/1.5,if(lt(t,8),1,if(lt(t,9.5),(9.5-t)/1.5,0))))',\
drawtext=fontfile='$F/georgia.ttf':textfile=t1.txt:fontsize=48:fontcolor=white:x=(w-tw)/2:y=h*0.36:shadowcolor=black@0.45:shadowx=2:shadowy=2:alpha='if(lt(t,36.5),0,if(lt(t,38),(t-36.5)/1.5,1))',\
drawtext=fontfile='$F/segoeuil.ttf':textfile=t3.txt:fontsize=24:fontcolor=white:x=(w-tw)/2:y=h*0.36+66:shadowcolor=black@0.45:shadowx=1:shadowy=1:alpha='if(lt(t,37.5),0,if(lt(t,39),(t-37.5)/1.5,1))',\
fade=t=in:st=0:d=1.5,fade=t=out:st=40.5:d=1.5,format=yuv420p[v];[1]loudnorm=I=-18:TP=-2,afade=t=out:st=40:d=2[a]" \
-map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 21 -profile:v high -movflags +faststart -c:a aac -b:a 160k -shortest $OUT.mp4
ffmpeg -y -loglevel error -i "$FR/f_$PF.png" -vf scale=1280:-1 -q:v 3 $OUT.jpg
ls -la $OUT.mp4 $OUT.jpg
