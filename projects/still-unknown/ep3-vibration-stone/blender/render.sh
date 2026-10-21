#!/bin/bash
cd "$(dirname "$0")"
B="/c/Program Files/Blender Foundation/Blender 5.1/blender.exe"
python /c/Users/lilli/Projects/sapling/tools/gpu_yield.py stop "TV render Still Unknown 10.3"
for s in usm saw; do "$B" -b -P shots.py -- $s "$(pwd -W)/$s" > render_$s.log 2>&1; done
python /c/Users/lilli/Projects/sapling/tools/gpu_yield.py start "TV render done" --if-ours
echo ALLDONE > render_done.txt
