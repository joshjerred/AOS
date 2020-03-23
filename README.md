# AOS
Atmospheric Observation System

This is a simple bash script that reads data from sensors connected to a raspberry pi (Mainly through Python). It takes an image with a raspberry pi camera, then overlays the data onto the image. This image is then converted to an audio file in the SSTV format. The image in then played with aplay. Connect it to a UV-5R radio and boom, you have a remote station.

You do need a ham radio license for the weather balloon side of things, but it's worth it!

This is primarily used for a weather balloon project but could also be used for a weather station with SSTV reporting.

Credit to KI4MCW for the C script to convert the image to an audio file! It can be found here:
https://sites.google.com/site/ki4mcw/Home/sstv-via-uc

REQUIRED PACKAGES:
aplay
imagemagick
gpsd with gpspipe
sox
jq

Interfacing:
Enable I2C
Enable 1-wire
Enable Camera

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
NEO-6M - GPS
