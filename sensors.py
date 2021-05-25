import sys
import json
import datetime
import logging

import ds18b20
import bmp180
import neo6m
import pi


# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('./logs/sensor_logs/sensors.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# class to define and read all sensors
class Sensors:
    def __init__(self):
        logger.debug("starting init()")
        # Diagnostic
        self.time = 0
        self.known_errors = ""
        self.alerts = ""
        # Environmental
        self.temperature = 0
        self.pressure = 0
        # GPS
        self.latitude = 0
        self.longitude = 0
        self.altitude = 0
        self.gps_quality = 0
        # System
        self.cpu_temp = 0
        self.cpu_usage = 0
        self.ram_usage = 0
        self.disk_usage = 0
        self.disk_space_available = 0
        self.disk_space_used = 0
        self.log_file_size = 0

    def read_temp(self):
        """reads temperature data and checks for errors"""
        
        logger.debug("starting read_temp()")
        try:
            temp = ds18b20.data()
            temp.pull()
            self.temperature = temp.read()
            logger.debug('read_temp complete without error')
        except:
            logger.exception('read_temp() error')
            self.temperature = "NO_DATA"
            self.known_errors += "read_temp function error -"

    def read_pressure(self):
        """reads pressure data and checks for errors"""

        logger.debug("starting read_pressure()")
        try:
            press = bmp180.data()
            press.pull()
            self.pressure = press.read()
            logger.debug('read_pressure() complete without error')
        except:
            logger.exception('read_pressure() error')
            self.pressure = "NO_DATA"
            self.known_errors += "read_pressure function error -"

    def read_gps(self):
        """reads gps data and checks for errors"""

        logger.debug("starting read_gps()")
        try:
            gps = neo6m.data()
            gps.pull()
            coordinates = gps.read()
            self.latitude = coordinates['lat']
            self.longitude = coordinates['lon']
            self.altitude = coordinates['alt']
            self.gps_quality = coordinates['qual']
            if int(self.gps_quality) == 0:
                self.known_errors += "No GPS Fix -"
                logger.error('No GPS Fix')
            logger.debug('read_gps complete without error')
        except:
            logger.exception('read_gps error')
            self.latitude = "NO_DATA"
            self.longitude = "NO_DATA"
            self.altitude = "NO_DATA"
            self.gps_quality = "NO_DATA"
            self.known_errors += "read_gps function error -"

    def read_system(self):
        """reads system data and checks for errors"""
        logger.debug("starting read_system()")
        try:
            system = pi.data()
            system.pull()
            system_info = system.read()
            self.cpu_temp = system_info['cpu_temp']
            self.cpu_usage = system_info['cpu_usage']
            self.ram_usage = system_info['ram_usage']
            self.disk_usage = system_info['disk_usage']
            self.disk_space_available = system_info['disk_space_available']
            self.disk_space_used = system_info['disk_space_used']
            self.log_file_size = system_info['log_file_size']
            if int(self.cpu_usage) > 90:
                self.alerts += "high CPU usage -"
                logger.warning('high CPU usage')
            if float(self.ram_usage) > 90:
                self.alerts += "high RAM usage -"
                logger.warning('high RAM usage')
            logger.debug('read_system complete without error')
        except:
            logger.exception('read_system error')
            self.cpu_temp = "NO_DATA"
            self.cpu_usage = "NO_DATA"
            self.ram_usage = "NO_DATA"
            self.disk_usage = "NO_DATA"
            self.disk_space_available = "NO_DATA"
            self.disk_space_used = "NO_DATA"
            self.log_file_size = "NO_DATA"
            self.known_errors += "read_system function error -"

    def read_all(self):
        """runs the read function on all of the sensors, will log errors"""

        logger.debug("starting read_all()")
        try:
            self.time = datetime.datetime.now().strftime("%m-%d %H:%M:%S")
            self.read_temp()
            self.read_pressure()
            self.read_gps()
            self.read_system()
        except:
            logger.critical('error within read_all')

    def return_HR(self):
        """returns human readable data from the sensors"""

        logger.debug("starting read_HR()")
        return {'time':self.time,'temperature' : self.temperature, 
        'pressure' : self.pressure, 'latitude' : self.latitude, 
        'longitude': self.longitude, 'altitude':self.altitude, 
        'gps_quality':self.gps_quality,'cpu_temp':self.cpu_temp, 
        'cpu_usage':self.cpu_usage, 'ram_usage':self.ram_usage, 
        'disk_usage':self.disk_usage, 
        'disk_space_available':self.disk_space_available,
        'disk_space_used':self.disk_space_used, 
        'log_file_size':self.log_file_size,
        'known_errors':self.known_errors, 'alerts':self.alerts}

if __name__ == '__main__':
    x = Sensors()
    x.read_all()
    print(x.return_HR())