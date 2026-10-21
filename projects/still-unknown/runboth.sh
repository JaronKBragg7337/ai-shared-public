#!/bin/bash
cd /c/Users/lilli/AI-Shared/projects/still-unknown
(cd ep4-voynich && bash build.sh > build.log 2>&1)
(cd ep5-wow && bash build.sh > build.log 2>&1)
echo finished > runboth.done
