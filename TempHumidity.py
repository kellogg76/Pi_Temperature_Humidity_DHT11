#!/usr/bin/python

# requires RPi_I2C_driver.py
import RPi_I2C_driver
from time import *
import sys
import datetime
import time
import logging
import Adafruit_DHT
import RPi.GPIO as GPIO
#from time import sleep
import urllib2


# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }

if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#')
    print('example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4')
    sys.exit(1)

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
temperature = temperature * 0.8

# Configure Logging Format and Location
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s, %(message)s',
                    datefmt='%m-%d-%Y %H:%M:%S',
                    filename='/home/pi/scripts/temperature.txt',
                    filemode='w')

# Log the temperature data to a file and wait until the next read
logging.info(str(temperature) + "," + str(humidity))

#Upload data to Thingspeak
baseURL = 'https://api.thingspeak.com/update?api_key=INSERT_API_KEY_HERE'
f = urllib2.urlopen(baseURL + "&field1=%s&field2=%s" % (humidity, temperature))
f.close()

##Update LCD
#Read from temperature.txt file
fo = open("/home/pi/scripts/temperature.txt", "r+")
temp = fo.read(30)

mylcd = RPi_I2C_driver.lcd()
mylcd.lcd_display_string("Temp: " + temp[21:25] + "C", 1)
mylcd.lcd_display_string("Hum : "+ temp[26:30] + "%", 2)

sleep(2) # 2 sec delay

#Close File
fo.close

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if humidity is not None and temperature is not None:
    print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
else:
    print('Failed to get reading. Try again!')
    sys.exit(1)
