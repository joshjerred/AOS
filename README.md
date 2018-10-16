# AOS
Atmospheric Observation System

To be completely honest, I have absolutely no clue how this works anymore. I've been working on it on and off over the past year and every time I try to clean it up I just break something. If you legitimately want something usable then you aren't looking in the right place.

Credit to KI4MCW for the C script to convert the image to an audio file! It can be found here:
https://sites.google.com/site/ki4mcw/Home/sstv-via-uc


Only the basic bash script that takes a picture with a webcam, changes the size, converts to a Martin1 SSTV .wav file, then plays the audio via the aplay command.

All compiled, requires aplay, imagemagick, fswebcam.

fswebcam can be replaced with raspistill if you want to use a PI cam
Replace line 5 with "raspistill -t 1 --width 320 --height 256 -e png -o ./tmpdir/tmp.png"

Do "dos2unix AOS.sh" in order to unbreak stuff while attempting to update the main script. Obviously be in the AOS Directory


(These are just notes to remind me how to unbreak everything I think)

___________
How to run:
1. Simply do "bash AOS.sh"
2. Spend 15 to 20 hours finding what packages you are missing
3. Spend another 5 hours fixing bugs that are now a thing because the packages are now updated
4. Profit?

___________
Sensors:
DS18B20 - Temp Probe
BMP180 - Pressure Sensors
General Voltage Sensor (0-25v DC)
NEO-6M - GPS

Things to add from GPS:
Lat/Long
Altitude
Speed
Climb
Status
