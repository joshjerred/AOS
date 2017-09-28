#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M")

fswebcam -r 320x256  /SIS/tmpdir/tmp.png
echo IMAGE TAKEN RESIZE
convert /SIS/tmpdir/tmp.png -resize 320x256! /SIS/tmpdir/tmp
echo IMAGE RESIZED CONVERTING TO .WAV FILE
./sstv /SIS/tmpdir/tmp 22050
echo IMAGE CONVERTED: PLAYING AUDIO
aplay /SIS/tmpdir/tmp.wav
