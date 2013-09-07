#!/usr/bin/python

usePWM = False


import logging
import sys
if usePWM: 
	from Adafruit_PWM_Servo_Driver import PWM
import time

logging.basicConfig(filename='test.log',level=logging.DEBUG)
logging.info('Starting Log file.')


# Initialise the PWM device using the default address
# bmp = PWM(0x40, debug=True)
if usePWM:
	pwm = PWM(0x40, debug=True)
	pwm.setPWMFreq(60)

servoLeftMin = 150  # Min pulse length out of 4096
servoLeftMax = 600  # Max pulse length out of 4096

servoRightMin = 150  # Min pulse length out of 4096
servoRightMax = 600  # Max pulse length out of 4096

servoLeftChan = 0
servoRightChan = 1

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second. Microseconds
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  if usePWM:
  	pwm.setPWM(channel, 0, pulse)

def drive(x,y):
 	logging.debug("We got a drive command: rawX:%02f and rawY:%02f",x,y)  

	servoStartValueLeft = 0
	servoEndValueLeft = 0

	servoStartValueRight = 0
	servoEndValueRight = 0

	left=0.0
	right=0.0

	# TODO: Can this be simplified?
	if x==0 and y==0:
		if usePWM:
			pwm.setPWM(servoLeftChan,0,0)
			pwm.setPWM(servoRightChan,0,0)
	else:
		if y >= 0: 			#We're going forward or stopped.
			if x <= 0:		#We're veering to the left.
				logging.debug("Forward to the Left/Straight")
				right=y
				left=-(y-x)
			else:
				logging.debug("Forward to the Right")
				right=y-x	# We're veering to the right.
				left=-y

		elif y < 0:			# We're going backwards
			if x <= 0:		#We're veering to the left.
				logging.debug("Reverse to the Left/Straight")
				right=y
				left=-(y-x)
			else:
				logging.debug("Reverse to the Right")
				right=y-x
				left=-y

		logging.debug("Left=%2f Right=%2f",left,right)

		# This is an example formula I found for remapping ranges of numbers:
		#OldRange = (OldMax - OldMin)  
		#NewRange = (NewMax - NewMin)  
		#NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin

		oldRangeLeft = 100 - -100
		newRangeLeft =  servoLeftMax - servoLeftMin
		scaledLeft = (((left - -100) * newRangeLeft) / oldRangeLeft + servoLeftMin)

		oldRangeRight = 100 - -100
		newRangeRight =  servoRightMax - servoRightMin
		scaledRight = (((right - -100) * newRangeRight) / oldRangeRight + servoRightMin)

		logging.debug("ScaledLeft: %02f ScaledRight: %02f",scaledLeft,scaledRight)

		if usePWM:
			pwm.setPWM(servoLeftChan,0,int(scaledLeft))
			pwm.setPWM(servoRightChan,0,int(scaledRight))

def emergencyStop():
	logging.info("We got the EMERGENCY STOP command.")
	if usePWM:
		pwm.setPWM(servoLeftChan, 0, 0)	
		pwm.setPWM(servoRightChan, 0, 0)


# Listen for STDIN and control output depending on message. 
# Example: drive:<speed>:<direction>
while 1:
	logging.info('Looping....')
	line = sys.stdin.readline()
	logging.debug("This is the line: " + line)
	#lineString = "drive:100:50"
	data = line.split(':')
	logging.debug("We got command: " + data[0])
	if data[0] == 'drive':
		drive(float(data[2]),float(data[1]))
		
	elif data[0] == 'EMERGENCYSTOP':
		emergencyStop()
		
	else:
		logging.info("We got some other kind of command")




