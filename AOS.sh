#!/bin/bash
now=$(date +"%Y-%m-%d_%H%M")
TEXT="CALLSIGN"
raspistill -t 1 --width 320 --height 256 -e png -o ./tmpdir/tmp
echo IMAGE TAKEN COPYING
convert -font avantgarde-demi -fill blue -pointsize 36 -draw "text 5,30 '$TEXT'" ./tmpdir/tmp ./tmpdir/tmp.png
cp ./tmpdir/tmp.png ./images/$now.png
echo -------------------
convert ./tmpdir/tmp.png -resize 320x256! ./tmpdir/tmp
mv ./tmpdir/tmp ./tmpdir/tmp.png
echo IMAGE RESIZED CONVERTING TO .WAV FILE
./pisstv ./tmpdir/tmp.png 11050
echo IMAGE CONVERTED: PLAYING AUDIO
mv ./tmpdir/tmp.png.wav ./tmpdir/tmp.wav
aplay ./tmpdir/tmp.wav
