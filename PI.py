import os
import logging

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('./logs/sensor_logs/system.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class data:
    def __init__(self):
        logger.debug('starting init()')
        self.cpu_temp = 0
        self.cpu_usage = 0
        self.ram_usage = 0
        self.disk_usage = 0
        self.disk_space_available = 0
        self.disk_space_used = 0
        self.log_file_size = 0

    def pull(self):
        logger.debug('starting pull()')
        # CPU temp
        data = open('/sys/class/thermal/thermal_zone0/temp')
        raw_cputemp = int(data.read())
        data.close()
        self.cpu_temp = int(raw_cputemp / 1000)

        # CPU usage
        self.cpu_usage = int(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip())

        # RAM usage
        self.ram_usage = int(os.popen("free | awk '/Mem/ {print $3/$2}'").readline().strip() * 100)

        # Disk info
        self.disk_usage = int((os.popen("df -m | awk '/root/ {print $5}'").readline().strip())[0:-1])
        self.disk_space_available = os.popen("df -m | awk '/root/ {print $4}'").readline().strip()
        self.disk_space_used = os.popen("df -m | awk '/root/ {print $3}'").readline().strip()

    def read_raw(self): # TODO is there a need for raw data here or should it be implemented just for continuity?
        logger.debug('starting read_raw() NOT IMPLEMENTED')
        return "tmp"

    def read(self):
        logger.debug('starting read()')
        return {'cpu_temp':self.cpu_temp, 'cpu_usage':self.cpu_usage, 
                'ram_usage':self.ram_usage, 'disk_usage':self.disk_usage,
                'disk_space_available':self.disk_space_available,
                'disk_space_used':self.disk_space_used, 'log_file_size':self.log_file_size}

if __name__ == "__main__":
  x = data()
  x.pull()
  #print(x.read_raw())
  print(x.read())