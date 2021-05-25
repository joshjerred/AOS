import smbus
import time
from ctypes import c_short
import logging

# logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('./logs/sensor_logs/bmp180.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# class to read the bmp180 sensor
class data:
  def __init__(self):
    logger.debug('starting init()')
    self.DEVICE = 0x77 # Default device I2C address
    self.bus = smbus.SMBus(1)

    self.raw_data = ""
    self.raw_press = 0
    self.raw_backup_temp = 0
    self.pressm = 0
    self.backup_temp = 0
    self.chip_id = ""
    self.chip_version = ""


  # def __convertToString(self, data):
  #   # Simple function to convert binary data into a string
  #   return str((data[1] + (256 * data[0])) / 1.2)

  def __getShort(self, data, index):
    logger.debug('starting __getShort()')
    # return two bytes from data as a signed 16-bit value
    return c_short((data[index] << 8) + data[index + 1]).value

  def __getUshort(self, data, index):
    logger.debug('starting __getUshort')
    # return two bytes from data as an unsigned 16-bit value
    return (data[index] << 8) + data[index + 1]

  def readBmp180Id(self):
    logger.debug('starting readBmp180Id()')
    addr=self.DEVICE
    # Chip ID Register Address
    REG_ID     = 0xD0
    (self.chip_id, chip_version) = self.bus.read_i2c_block_data(addr, REG_ID, 2)
    logger.debug('chip id is: ' + str(self.chip_id))
    return (self.chip_id, chip_version)

  def pull(self):
    logger.debug('starting pull()')
    addr=self.DEVICE
    # Register Addresses
    REG_CALIB  = 0xAA
    REG_MEAS   = 0xF4
    REG_MSB    = 0xF6
    REG_LSB    = 0xF7
    # Control Register Address
    CRV_TEMP   = 0x2E
    CRV_PRES   = 0x34
    # Oversample setting
    OVERSAMPLE = 3    # 0 - 3

    # Read calibration data
    # Read calibration data from EEPROM
    cal = self.bus.read_i2c_block_data(addr, REG_CALIB, 22)

    # Convert byte data to word values
    AC1 = self.__getShort(cal, 0)
    AC2 = self.__getShort(cal, 2)
    AC3 = self.__getShort(cal, 4)
    AC4 = self.__getUshort(cal, 6)
    AC5 = self.__getUshort(cal, 8)
    AC6 = self.__getUshort(cal, 10)
    B1  = self.__getShort(cal, 12)
    B2  = self.__getShort(cal, 14)
    MB  = self.__getShort(cal, 16)
    MC  = self.__getShort(cal, 18)
    MD  = self.__getShort(cal, 20)

    # Read temperature
    self.bus.write_byte_data(addr, REG_MEAS, CRV_TEMP)
    time.sleep(0.005)
    (msb, lsb) = self.bus.read_i2c_block_data(addr, REG_MSB, 2)
    UT = (msb << 8) + lsb

    # Read pressure
    self.bus.write_byte_data(addr, REG_MEAS, CRV_PRES + (OVERSAMPLE << 6))
    time.sleep(0.04)
    (msb, lsb, xsb) = self.bus.read_i2c_block_data(addr, REG_MSB, 3)
    UP = ((msb << 16) + (lsb << 8) + xsb) >> (8 - OVERSAMPLE)
    #print(msb, lsb, xsb)

    # Refine temperature
    X1 = ((UT - AC6) * AC5) >> 15
    X2 = (MC << 11) / (X1 + MD)
    B5 = X1 + X2
    temperature = int(B5 + 8) >> 4

    # Refine pressure
    B6  = B5 - 4000
    B62 = int(B6 * B6) >> 12
    X1  = (B2 * B62) >> 11
    X2  = int(AC2 * B6) >> 11
    X3  = X1 + X2
    B3  = (((AC1 * 4 + X3) << OVERSAMPLE) + 2) >> 2

    X1 = int(AC3 * B6) >> 13
    X2 = (B1 * B62) >> 16
    X3 = ((X1 + X2) + 2) >> 2
    B4 = (AC4 * (X3 + 32768)) >> 15
    B7 = (UP - B3) * (50000 >> OVERSAMPLE)

    P = (B7 * 2) / B4

    X1 = (int(P) >> 8) * (int(P) >> 8)
    X1 = (X1 * 3038) >> 16
    X2 = int(-7357 * P) >> 16
    pressure = int(P + ((X1 + X2 + 3791) >> 4))
    
    self.raw_data = (msb, lsb, xsb)
    self.raw_press = pressure
    self.raw_backup_temp = temperature
    self.backup_temp = temperature / 10
    self.pressm = pressure/100.0
    logging.debug('raw pressure: ' + str(self.raw_press), 'raw temperature: ' + str(self.raw_backup_temp))

  def read_backup_temp(self):
    logger.debug('starting read_back_temp()')
    return self.backup_temp

  def read_raw(self):
    logger.debug('starting read_raw()')
    "raw_data, crc?, raw_press, pressmbar, backup_temp, raw_backup_temp"
    return [self.raw_data, self.raw_press, self.raw_backup_temp]

  def read(self):
    logger.debug('starting read()')
    """returns human readable format for the pressure"""
    return self.pressm

if __name__ == "__main__":
  x = data()
  x.pull()
  print(x.read_raw())
  print(x.read())
  print(x.read_backup_temp())