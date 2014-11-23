# 
# l293d.py : Class to use the L293D IC with the Raspberry Pi
# 
# Copyright (c) 2014,
# Antonio Lobato
# Hugo Menna Barreto
# Ulisses Figueiredo
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#            ______
# Enable 1 -|  \/  |- +Vcc
#      IN1 -|      |- IN4
#     OUT1 -|      |- OUT4
#       0V -|      |- 0V
#       0V -|      |- 0V
#     OUT2 -|      |- OUT3
#      IN2 -|      |- IN3
#  +Vmotor -|______|- Enable 2
# 
# This is how the L293D looks.
# We will connect the Enable1, IN1 and IN2 to the Raspberry Pi ports specified
# when we define the motor.
# OUT1 and OUT2 is what goes to the motor.
# 

import RPi.GPIO as gpio

gpio.setmode(gpio.BOARD)
gpio.cleanup()

class Motor:
	def __init__(self, enable, in1, in2, speed=0):
		self.enable = enable
		self.in1 = in1
		self.in2 = in2

		self.__direction = True
		self.__stopControl = False
		
		gpio.setup(self.in1, gpio.OUT)
		gpio.setup(self.in2, gpio.OUT)
		gpio.setup(self.enable, gpio.OUT)

		self.pwm = gpio.PWM(enable, 50)
		self.pwm.start(0)
		self.__refreshMotor()
		self.setSpeed(speed)

	def setSpeed(self, speed):
		if (speed < 0 and self.__direction) or (speed >= 0 and not self.__direction):
			self.reverse()
		speed = abs(speed)
		self.pwm.ChangeDutyCycle(speed)

	def reverse(self):
		self.__direction = not self.__direction
		self.__refreshMotor()

	def stop(self):
		self.__stopControl = True
		self.__refreshMotor()

	def restart(self):
		self.__stopControl = False
		self.__refreshMotor()

	def getDirection(self):
		return self.__direction


	def __refreshMotor(self):
		gpio.output(self.in1, not self.__direction)
		gpio.output(self.in2, self.__stopControl != self.__direction)


	def __del__(self):
		self.pwm.stop()

