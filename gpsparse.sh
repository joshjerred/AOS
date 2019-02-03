#!/bin/bash
gpspipe -w -n 10 |   grep -m 1 mode > gpstmp
mode=$(cat ./gpstmp|jq .mode)
lat=$(cat ./gpstmp|jq .lat)
lon=$(cat ./gpstmp|jq .lon)
alt=$(cat ./gpstmp|jq .alt)
speed=$(cat ./gpstmp|jq .speed)

if [ "$mode" == "3" ]; then
  echo "$mode"
  echo "$lat"
  echo "$lon"
  echo "$alt"
  echo "$speed"
elif [ "$mode" == "2" ]; then
   echo "$mode"
   echo "$lat"
   echo "$lon"
   echo null
   echo "$speed"
elif [ "$mode" == "1" ]; then
   echo NO LOCK
else
   echo "ERR-UNKNOWN"
fi

