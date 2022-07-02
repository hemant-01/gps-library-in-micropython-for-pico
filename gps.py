from machine import Pin, UART
import time

gps_input= UART(0,baudrate=9600, tx=Pin(0), rx=Pin(1),timeout=1000,timeout_char=50)
s= UART(0,baudrate=9600, tx=Pin(0), rx=Pin(1),timeout=1000,timeout_char=50)

print(gps_input)

TIMEOUT = False

FIX_STATUS = False

#Store GPS Coordinates
latitude = None
longitude = None
satellites = None
gpsTime = None


#function to get gps Coordinates
def getPositionData(gps_input):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, gpsTime
    timeout = time.time() + 8   # 8 seconds from now
    while True:
        while True:
            buff = str(gps_input.readline())
            if buff is not None :
                break 
        parts = buff.split(',')
        print(buff)
        if (parts[0] == "b'$GNGGA" and len(parts) == 15 and parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
              
                #print("Message ID  : " + parts[0])
                #print("UTC time    : " + parts[1])
                #print("Latitude    : " + parts[2])
                #print("N/S         : " + parts[3])
                #print("Longitude   : " + parts[4])
                #print("E/W         : " + parts[5])
                #print("Position Fix: " + parts[6])
                #print("n sat       : " + parts[7])
            latitude = convertToDigree(parts[2])
            if (parts[3] == 'S'):
                latitude = -latitude
            longitude = convertToDigree(parts[4])
            if (parts[5] == 'W'):
                longitude = -longitude
            satellites = parts[7]
            gpsTime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
            FIX_STATUS = True
            break
        if (time.time() > timeout):
            TIMEOUT = True
            break
#function to convert raw Latitude and Longitude
#to actual Latitude and Longitude


def convertToDigree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) #degrees
    nexttwodigits = RawAsFloat - float(firstdigits*100) #minutes
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) # to 6 decimal places
    return str(Converted)
     
while True:
    
    getPositionData(gps_input)

    #if gps data is found then print it on lcd
    if(FIX_STATUS == True):
        print("fix......")
        print(latitude)
        print(longitude)
        print(satellites)
        print(gpsTime)
        
        FIX_STATUS = False
        
    if(TIMEOUT == True):
        print("Request Timeout: No GPS data is found.")
        TIMEOUT = False
 