#!/bin/bash
gpspipe -w -n 10 |   grep -m 1 lat > gpstmp
echo GETTING GPS DATA
sudo bash gpsparse.sh
NOW=$(date +"%m-%d %H%M")
CALL="KD9GDC"
VOLT="V4.5"
TMP="$(sudo python testscript.py)"
PRES="$(sudo python bmp180.py)"
LAT=""
LON=""
SPEED="50mph"
GPSALT="10"
GPSCLIMB="+5.01 f/s"
GPSFIXES="56"
GPSSTATUS="GO"
raspistill -t 1 --width 320 --height 256 -e png -o ./tmpdir/tmp
echo IMAGE TAKEN COPYING
convert -font avantgarde-demi -fill red -pointsize 20 -draw "text 3,15 '$CALL'" ./tmpdir/tmp ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 20 -draw "text 260,15 '$VOLT'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 20 -draw "text 3,30 '$NOW'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 20 -draw "text 3,45 '$PRES'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 20 -draw "text 3,60 '$TMP'" ./tmpdir/tmp.png ./tmpdir/tmp.png
cp ./tmpdir/tmp.png ./images/$NOW.png
echo -------------------
convert ./tmpdir/tmp.png -resize 320x256! ./tmpdir/tmp
mv ./tmpdir/tmp ./tmpdir/tmp.png
echo IMAGE RESIZED CONVERTING TO .WAV FILE
./pisstv ./tmpdir/tmp.png 11050
echo IMAGE CONVERTED: PLAYING AUDIO
mv ./tmpdir/tmp.png.wav ./tmpdir/tmp.wav
aplay ./tmpdir/tmp.wav
