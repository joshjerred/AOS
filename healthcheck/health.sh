gpspipe -w -n 10 |   grep -m 1 mode > gpstmp
#GPS VARIABLES
GPSSTATUS=$(cat ./gpstmp|jq .mode)
GPSLAT=$(cat ./gpstmp|jq .lat)
GPSLON=$(cat ./gpstmp|jq .lon)
GPSALT=$(cat ./gpstmp|jq .alt)
GPSSPEED=$(cat ./gpstmp|jq .speed)
GPSCLIMB=$(cat ./gpstmp|jq .climb)

#SENSOR VARIABLES
TMP="$(sudo python testscript.py)"
PRES="$(sudo python bmp180.py)"
SENSORHEALTH="sensorhealth good"


DATE=$(date "+%D")
TIME=$(date "+%T")
AOSSCRIPTSTATUS="test"
result=`ps aux | grep -i "AOS.sh" | grep -v "grep" | wc -l`
if [ $result -ge 1 ]
   then
        AOSSCRIPTSTATUS="RUNNING"
   else
        AOSSCRIPTSTATUS="NOT RUNNING"
fi
CPUTEMP=$(/opt/vc/bin/vcgencmd measure_temp | grep -Eo '[0-9]+\.[0-9]+')
CPUCLOCKSPEED=$(cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq)
RAMUSAGE=$(free -m | awk 'NR==2{printf "Memory Usage: %s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }')
CPUUSAGE=$(top -bn1 | grep load | awk '{printf "CPU Load: %.2f\n", $(NF-2)}')
DISKUSAGE=$(df -h | awk '$NF=="/"{printf "Disk Usage: %d/%dGB (%s)\n", $3,$2,$5}')

xmlstarlet ed --inplace -u "/data/gps/lockhealth" -v "$GPSSTATUS" telemetrydata.xml
xmlstarlet ed --inplace -u "/data/gps/latitude" -v "$GPSLAT" telemetrydata.xml
xmlstarlet ed --inplace -u "/data/gps/longitude" -v "$GPSLON" telemetrydata.xml
xmlstarlet ed --inplace -u "/data/gps/gpsalt" -v "$GPSALT" telemetrydata.xml
xmlstarlet ed --inplace -u "/data/gps/gpsspeed" -v "$GPSSPEED" telemetrydata.xml
xmlstarlet ed --inplace -u "/data/gps/gpsclimb" -v "$GPSCLIMB" telemetrydata.xml


xmlstarlet ed --inplace -u "/data/weatherdata/sensorhealth" -v "$SENSORHEALTH" telemetrydata.xml
xmlstarlet ed --inplace -u "/data/weatherdata/temp" -v "$TMP" telemetrydata.xml
xmlstarlet ed --inplace -u "/data/weatherdata/pres" -v "$PRES" telemetrydata.xml

xmlstarlet ed --inplace -u "/data/systems/systemdate" -v "$DATE" telemetrydata.xml
xmlstarlet ed --inplace -u "/data/systems/systemtime" -v "$TIME" telemetrydata.xml
xmlstarlet ed --inplace -u "/data/systems/aosstatus" -v "$AOSSCRIPTSTATUS" telemetrydata.xml
xmlstarlet ed --inplace -u "/data/systems/cputemp" -v "$CPUTEMP" telemetrydata.xml
xmlstarlet ed --inplace -u "/data/systems/cpuclockspeed" -v "$CPUCLOCKSPEED" telemetrydata.xml
xmlstarlet ed --inplace -u "/data/systems/ramusage" -v "$RAMUSAGE" telemetrydata.xml
xmlstarlet ed --inplace -u "/data/systems/cpuusage" -v "$CPUUSAGE" telemetrydata.xml
xmlstarlet ed --inplace -u "/data/systems/diskusage" -v "$DISKUSAGE" telemetrydata.xml

echo done
