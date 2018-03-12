# AOS
Atmospheric Observation System

Credit to KI4MCW for the C script to convert the image to an audio file! It can be found here:
https://sites.google.com/site/ki4mcw/Home/sstv-via-uc


Only the basic bash script that takes a picture with a webcam, changes the size, converts to a Martin1 SSTV .wav file, then plays the audio via the aplay command.

All compiled, requires aplay, imagemagick, fswebcam.

fswebcam can be replaced with raspistill if you want to use a PI cam
Replace line 5 with "raspistill -t 1 --width 320 --height 256 -e png -o ./tmpdir/tmp.png"

___________
How to run:
Simply do "bash AOS.sh"
