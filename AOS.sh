#!/bin/bash
gpspipe -w -n 10 |   grep -m 1 mode > gpstmp
NOW=$(date +"%m-%d--%H%M")
CALL="KD9GDC"
TMP="$(sudo python testscript.py)"
PRES="$(sudo python bmp180.py)"
GPSLAT=$(cat ./gpstmp|jq .lat)
GPSLON=$(cat ./gpstmp|jq .lon)
GPSSPEED=$(cat ./gpstmp|jq .speed)
GPSALT=$(cat ./gpstmp|jq .alt)
GPSCLIMB=$(cat ./gpstmp|jq .climb)
GPSSTATUS=$(cat ./gpstmp|jq .mode)
raspistill -t 1 --width 320 --height 256 -e png -o ./tmpdir/tmp
echo IMAGE TAKEN COPYING
convert -font avantgarde-demi -fill red -pointsize 20 -draw "text 3,15 '$CALL'" ./tmpdir/tmp ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 15 -draw "text 160,15 '$GPSSPEED kph'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 15 -draw "text 160,30 'VSI $GPSCLIMB m/min'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 20 -draw "text 3,30 '$NOW'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 20 -draw "text 3,45 '$PRES'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 20 -draw "text 3,60 '$TMP'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 20 -draw "text 3,205 'Lat $GPSLAT'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 20 -draw "text 3,220 'Lon $GPSLON'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 20 -draw "text 3,235 '$GPSALT M'" ./tmpdir/tmp.png ./tmpdir/tmp.png
convert -font avantgarde-demi -fill green3 -pointsize 20 -draw "text 3,250 'Mode $GPSSTATUS'" ./tmpdir/tmp.png ./tmpdir/tmp.png
cp ./tmpdir/tmp.png ./images/$NOW.png
echo -------------------
convert ./tmpdir/tmp.png -resize 320x256! ./tmpdir/tmp
mv ./tmpdir/tmp ./tmpdir/tmp.png
echo IMAGE RESIZED CONVERTING TO .WAV FILE
./pisstv ./tmpdir/tmp.png 11050
echo IMAGE CONVERTED: PLAYING AUDIO
mv ./tmpdir/tmp.png.wav ./tmpdir/tmp.wav
aplay ./tmpdir/tmp.wav
