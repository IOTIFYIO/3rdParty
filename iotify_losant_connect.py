'''****************************************************************************************
www.iotify.io  Last revision: 11th Feb 2017
Virtualized hardwre elements for IoT
ython code to connect a smart trash can running a raspberry pi to Losant
****************************************************************************************'''   


import RPi.GPIO as GPIO
import time
from losantmqtt import Device

'''****************************************************************************************
losantmqtt can be installed by running the following command in the terminal:

sudo pip install losant-mqtt

More info at: https://github.com/Losant/losant-mqtt-python

****************************************************************************************'''    

'''****************************************************************************************
SET Pin Number
****************************************************************************************'''                                                                                                             
TRIG = 5 # Broadcom pin 18 (P1 pin 12) for Ultrasonic                                                                                    
ECHO = 6 # Broadcom pin 23 (P1 pin 16) for Ultrasonic                                                                                  
LIDCOVER = 15 #Returns 0 if closed, 1 if open
alarmOut = 22 # Broadcom pin 22 (P1 pin 15) 


'''****************************************************************************************
SET GPIOs
****************************************************************************************'''

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.setup(LIDCOVER,GPIO.IN)
GPIO.setup(alarmOut,GPIO.OUT)
GPIO.output(TRIG, False)
GPIO.output(alarmOut,False)
    

'''****************************************************************************************
Connect to Losant using your own Device Id Key, app access key and app access secret. 

By Default, the function is:

device = Device("my-device-id", "my-app-access-key", "my-app-access-secret")

Check it out at: https://docs.losant.com/mqtt/python/
****************************************************************************************'''

# Construct device
device = Device("589ae6a450530f00010319a3", "7ad296ea-ae11-47dd-9a0e-aba70e0eb7d5", "d2e3b0d5441cd22513da1ef64971c5bcc7ff262b09bbc5b876c678eab2354325")

def on_command(device, command):
    print("Command received.")
    print(command["name"])
    print(command["payload"])

# Listen for commands.
device.add_event_observer("command", on_command)

# Connect to Losant.
device.connect(blocking=False)


'''****************************************************************************************
While True loop to run for eternity.. or Answer = 42, you decide
****************************************************************************************'''

# Send values once every second.
while True:
    device.loop()
    if device.is_connected():
        
        # Read Lid state to check if its open
        LidState = GPIO.input(LIDCOVER)
              
        # Ultrasonic Sensor Read only if Lid is closed
        if LidState == 0:
            
            GPIO.output(TRIG, False)
            print "Waiting For Ultrasonic Sensor"
            time.sleep(2)

            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO)==0:
                pulse_start = time.time()

            while GPIO.input(ECHO)==1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            
            #Convert distance to FillLevel
            #226 is Maximum read when empty by ultrasonic
            #40 is minimum read when full by ultrasonic
            distance = pulse_duration * 17150
            FillLevel = ((226-distance)/(226-40))*100
            
            FillLevel = round(FillLevel, 2)
            print "FillLevel:",FillLevel,"%"
            
        else:
            print "Lid is Open, cannot read ultrasonic sensor"
            FillLevel = 0
           
'''****************************************************************************************
Sends Data to Losant
****************************************************************************************'''
        
        device.send_state({"FillLevel": FillLevel})
        device.send_state({"LidState": LidState})

    time.sleep(5)
    
