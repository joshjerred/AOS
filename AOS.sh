#!/bin/bash

now=$(date +"%Y-%m-%d_%H%M")
TEXT="CALLSIGN"

fswebcam -r 320x256  ./tmpdir/tmp.png
echo IMAGE TAKEN COPYING
convert -font avantgarde-demi -fill blue -pointsize 36 -draw "text 5,30 '$TEXT'" ./tmpdir/tmp.png ./tmpdir/tmp.png
cp ./tmpdir/tmp.png ./images/$now.png
echo -------------------
convert ./tmpdir/tmp.png -resize 320x256! ./tmpdir/tmp
echo IMAGE RESIZED CONVERTING TO .WAV FILE
./sstv ./tmpdir/tmp 22050
echo IMAGE CONVERTED: PLAYING AUDIO
aplay ./tmpdir/tmp.wav
