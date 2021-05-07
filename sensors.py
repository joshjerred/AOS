import sys
import json
import datetime

import DS18B20
import BMP180
import NEO6M
import PI

class Sensors:
    def __init__(self):
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
        try:
            temp = DS18B20.data()
            temp.pull()
            self.temperature = temp.read()
        except:
            self.temperature = "NO_DATA"
            self.known_errors += "read_temp function error -"

    def read_pressure(self):
        try:
            press = BMP180.data()
            press.pull()
            self.pressure = press.read()
        except:
            self.pressure = "NO_DATA"
            self.known_errors += "read_pressure function error -"

    def read_gps(self):
        try:
            gps = NEO6M.data()
            gps.pull()
            coordinates = gps.read()
            self.latitude = coordinates['lat']
            self.longitude = coordinates['lon']
            self.altitude = coordinates['alt']
            self.gps_quality = coordinates['qual']
            if int(self.gps_quality) == 0:
                self.known_errors += "No GPS Fix -"
        except:
            self.latitude = "NO_DATA"
            self.longitude = "NO_DATA"
            self.altitude = "NO_DATA"
            self.gps_quality = "NO_DATA"
            self.known_errors += "read_gps function error -"

    def read_system(self):
        try:
            system = PI.data()
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
            if float(self.ram_usage) > 90:
                self.alerts += "high RAM usage -"
        except:
            self.cpu_temp = "NO_DATA"
            self.cpu_usage = "NO_DATA"
            self.ram_usage = "NO_DATA"
            self.disk_usage = "NO_DATA"
            self.disk_space_available = "NO_DATA"
            self.disk_space_used = "NO_DATA"
            self.log_file_size = "NO_DATA"
            self.known_errors += "read_system function error -"



    def read_all(self):
        self.time = datetime.datetime.now().strftime("%m-%d %H:%M:%S")
        self.read_temp()
        self.read_pressure()
        self.read_gps()
        self.read_system()

    def return_HR(self):
        return {'time':self.time,'temperature' : self.temperature, 'pressure' : self.pressure, 
        'latitude' : self.latitude, 'longitude': self.longitude, 
        'altitude':self.altitude, 'gps_quality':self.gps_quality,
        'cpu_temp':self.cpu_temp, 'cpu_usage':self.cpu_usage, 
        'ram_usage':self.ram_usage, 'disk_usage':self.disk_usage,
        'disk_space_available':self.disk_space_available,
        'disk_space_used':self.disk_space_used, 'log_file_size':self.log_file_size,
        'known_errors':self.known_errors, 'alerts':self.alerts}

if __name__ == '__main__':
    x = Sensors()
    x.read_all()
    print(json.dumps(x.return_HR(), indent = 4))