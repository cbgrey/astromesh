#!/usr/bin/python

import logging
import sys
from Adafruit_PWM_Servo_Driver import PWM
import time

logging.basicConfig(filename='test.log',level=logging.DEBUG)
logging.info('Starting Log file.')


# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
pwm = PWM(0x40, debug=True)

servoLeftMin = 150  # Min pulse length out of 4096
servoLeftMax = 600  # Max pulse length out of 4096

servoRightMin = 150  # Min pulse length out of 4096
servoRightMax = 600  # Max pulse length out of 4096

servoLeftChan = 0
servoRightChan = 1

pwm.setPWMFreq(60)

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second. Microseconds
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

# Listen for STDIN and control output depending on message. 
# Example: drive:<speed>:<direction>
while 1:
	logging.info('Looping....')
	line = sys.stdin.readline()
	logging.info("This is the line: " + line)
	#lineString = "drive:100:50"
	data = line.split(':')
	#logging.info("We got command: " + data[0])
	if data[0] == 'drive':
		speed = float(data[1])

		logging.info("We got a drive command")
		logging.info("Speed is: %02f",speed)
		
		direction = float(data[2])
		if speed == 0:
			pwm.setPWM(0, 0, 0)
		elif speed > 0:							
			pwm.setPWM(servoLeftChan, 0, servoLeftMin)
		elif speed < 0:
			pwm.setPWM(servoLeftChan, 0, servoLeftMax)
	elif data[0] == 'EMERGENCYSTOP':
		logging.info("We got the EMERGENCY STOP command.")

		pwm.setPWM(servoLeftChan, 0, 0)	
		pwm.setPWM(servoRightChan, 0, 0)
	else:
		logging.info("We got some other kind of command")




