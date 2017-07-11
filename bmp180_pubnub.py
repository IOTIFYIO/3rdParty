# Example Code of BMP180 Bosch Sensor connecting to PubNub
# Running on a Raspberry Pi 2
# IoTIFY TECHNOLOGIES SL
# 05-JULY -2017

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
import time

pnconfig = PNConfiguration()

# SUBSCRIBE Key
pnconfig.subscribe_key = 'sub_INTRODUCE_COMPLTE_SUB_KEY'

# PUBLISH Key
pnconfig.publish_key = 'pub-INTRODUCE_COMPLTE_PUB_KEY'

pnconfig.ssl = False 
pubnub = PubNub(pnconfig)

import Adafruit_BMP.BMP085 as BMP085
from time import gmtime, strftime

# Raspberry Pi 2 uses I2C bus number 1
sensor = BMP085.BMP085(busnum=1)

channel = "my_channel"

# You can also optionally change the BMP085 mode to one of BMP085_ULTRALOWPOWER,
# BMP085_STANDARD, BMP085_HIGHRES, or BMP085_ULTRAHIGHRES.  See the BMP085
# datasheet for more details on the meanings of each mode (accuracy and power
# consumption are primarily the differences).  The default mode is STANDARD.
#sensor = BMP085.BMP085(mode=BMP085.BMP085_ULTRAHIGHRES)

def publish_callback(result, status):
    print result, status
    pass
    # Handle PNPublishResult and PNStatus
    
    
while 1:
    try:
        time.sleep(10)
        message = "Guid,3541938293";
        message += ",Time,"+ strftime("%Y-%m-%d %H:%M:%S", gmtime());
        message += ",Sensor,BMP180";
        message += ",temperature,%f" % sensor.read_temperature();
        message += ",pressure,%f" % sensor.read_pressure();
        #print message
        pubnub.publish().channel('my_channel').message([message]).async(publish_callback)

    except KeyboardInterrupt: 
        logging.error("Exception %s,%s"%(e,type(e)))	
	
