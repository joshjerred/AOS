#!/bin/bash
now=$(date +"%Y-%m-%d_%H%M")
CALL="KD9GDC"
TMP="$(sudo python testscript.py)"
PRES="$(sudo python bmp180.py)"
raspistill -t 1 --width 320 --height 256 -e png -o ./tmpdir/tmp
echo IMAGE TAKEN COPYING
convert -font avantgarde-demi -fill red -pointsize 25 -draw "text 5,30 '$CALL'" ./tmpdir/tmp ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 25 -draw "text 5,50 '$TMP'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 25 -draw "text 5,70 '$PRES'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 25 -draw "text 5,90 '$now'" ./tmpdir/tmp.png ./tmpdir/tmp.png
cp ./tmpdir/tmp.png ./images/$now.png
echo -------------------
convert ./tmpdir/tmp.png -resize 320x256! ./tmpdir/tmp
mv ./tmpdir/tmp ./tmpdir/tmp.png
echo IMAGE RESIZED CONVERTING TO .WAV FILE
./pisstv ./tmpdir/tmp.png 11050
echo IMAGE CONVERTED: PLAYING AUDIO
mv ./tmpdir/tmp.png.wav ./tmpdir/tmp.wav
aplay ./tmpdir/tmp.wav
