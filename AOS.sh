#!/bin/bash
NOW=$(date +"%m-%d_%H%M")
CALL="KD9GDC"
VOLT="V4.5"
TMP="$(sudo python testscript.py)"
PRES="$(sudo python bmp180.py)"
GPSLATLONG="33.45817N 79.566635W"
GPSSPEED="50mph"
GPSCLIMB="+5.01 f/s"
GPSFIXES="56"
GPSSTATUS="GO"
raspistill -t 1 --width 320 --height 256 -e png -o ./tmpdir/tmp
echo IMAGE TAKEN COPYING
convert -font avantgarde-demi -fill red -pointsize 25 -draw "text 5,30 '$CALL'" ./tmpdir/tmp ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 25 -draw "text 270,30 '$VOLT'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 25 -draw "text 5,50 '$NOW'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 25 -draw "text 5,70 '$PRES'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 25 -draw "text 5,90 '$TMP'" ./tmpdir/tmp.png ./tmpdir/tmp.png
cp ./tmpdir/tmp.png ./images/$now.png
echo -------------------
convert ./tmpdir/tmp.png -resize 320x256! ./tmpdir/tmp
mv ./tmpdir/tmp ./tmpdir/tmp.png
echo IMAGE RESIZED CONVERTING TO .WAV FILE
./pisstv ./tmpdir/tmp.png 11050
echo IMAGE CONVERTED: PLAYING AUDIO
mv ./tmpdir/tmp.png.wav ./tmpdir/tmp.wav
aplay ./tmpdir/tmp.wav
