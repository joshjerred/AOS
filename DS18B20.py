import os
import logging

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('./logs/sensor_logs/bs18b20.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# class to read the ds18b20 sensor
class data:
    def __init__(self):
        logger.debug('starting init()')

        for i in os.listdir('/sys/bus/w1/devices'):
            if i != 'w1_bus_master1':
                self.sensor_serial_number = i
        
        logger.debug('sensor serial number: ' + str(self.sensor_serial_number))
        
        self.raw_data = ""
        self.data_line = ""
        self.crc = ""
        self.raw_temp = 0
        self.tempf = 0
        self.tempc = 0

    def pull(self):
        logger.debug('starting pull()')
        data = open('/sys/bus/w1/devices/' + self.sensor_serial_number + '/w1_slave')
        raw = data.read().strip()
        logger.debug('raw data: ' + str(raw))
        data.close()
        if len(raw) != 74:
            self.raw_data = raw
            self.crc = "NULL"
            self.raw_temp = "NULL"
            self.tempf = "NULL"
            self.tempc = "NULL"
            print(raw)
            return

        firstline = raw.split("\n")[0]
        self.crc = firstline.split(" ")[-2] + " " + firstline.split(" ")[-1]
        self.data_line = firstline.split(":")[0]

        secondline = raw.split("\n")[1]
        self.raw_temp = secondline.split(" ")[-1]
        
        temperature = float(self.raw_temp[2:])

        self.raw_data = raw.split(":")[0]
        self.tempc = round(temperature / 1000, 2)
        self.tempf = round((self.tempc * 1.8) + 32, 2)
    
    def read_raw(self):
        logging.debug('starting read_raw()')
        """raw_data, crc, raw_temp, tempf, tempc"""
        return [self.raw_data, self.crc, self.raw_temp, self.tempf, self.tempc]

    def read(self):
        logging.debug('starting read()')
        """returns human readable format for the temperature"""
        return self.tempf

if __name__ == "__main__":
  x = data()
  x.pull()
  print(x.read_raw())
  print(x.read())