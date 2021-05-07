import serial
import pynmea2

class data:
    def __init__(self):
        self.device_address = '/dev/ttyAMA0'
        self.device_baudrate = 9600
        self.raw = ""
        self.nema = ""
        
    def pull(self):
        ser = serial.Serial(self.device_address, self.device_baudrate)

        fix_found = False
        for i in range(20):
            state = ser.readline()
            if str(state)[3:8] == "GPGGA": # GPRMC
                self.raw = str(state)[2:-5]
                self.nema = pynmea2.parse(self.raw)
                fix_found = True
                break
        if fix_found == False:
            ser.flushOutput()
            ser.close()
            raise Exception("No GPS data found in serial")


        ser.flushOutput()
        ser.close()

    def read_raw(self):
        """msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, 
        msg.gps_qual, msg.num_sats, msg.horizontal_dil, msg.altitude, 
        msg.altitude_units, msg.geo_sep, msg.geo_sep_units, msg.age_gps_data
        msg.ref_station_id"""
        #return [self.raw, self.nema, self.nema.timestamp, self.nema.lat, self.nema.lat_dir, self.nema.lon, 
        #self.nema.lon_dir, self.nema.gps_qual, self.nema.num_sats, 
        #self.nema.horizontal_dil, self.nema.altitude, self.nema.altitude_units, 
        #self.nema.geo_sep, self.nema.geo_sep_units, self.nema.age_gps_data,
        #self.nema.ref_station_id]
        return self.raw

    def read(self):
        if self.nema.gps_qual == 1:
            return {'lat':self.nema.latitude, 'lon':self.nema.longitude, 
            'alt':self.nema.altitude, 'qual':self.nema.gps_qual, 
            'notes':"GOOD FIX"}
        elif self.nema.gps_qual == 0:
            return {'lat':0, 'lon':0,'alt':0, 'qual':self.nema.gps_qual,
            'notes':'NO FIX'}
        else:
            return {'lat':0, 'lon':0,'alt':0, 'qual':self.nema.gps_qual,
            'notes':'UNKNOWN GPS ERROR'}
            
if __name__ == "__main__":
  x = data()
  x.pull()
  print(x.read_raw())
  print(x.read())