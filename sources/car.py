# 
# car.py : Class to define the car movements
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

from l293d import *

class Car:
	def __init__(self):
		self.motorLeft = Motor(22,26,24)
		self.motorRight = Motor(8,12,10)
		self.motorLeftCorrection = 1
		self.motorRightCorrection = 0.82178
		self.speed = 100
		self.status = "stopped"

	def goFoward(self):
		print "f"
		if self.status != "foward":
			if self.status == "stopped":
				self.__restart()
			self.motorLeft.setSpeed(self.speed * self.motorLeftCorrection)
			self.motorRight.setSpeed(self.speed * self.motorRightCorrection)
			self.status = "foward"

	def goBackward(self):
		print "b"
		if self.status != "backward":
			if self.status == "stopped":
				self.__restart()
			self.motorLeft.setSpeed(-1 * self.speed * self.motorLeftCorrection)
			self.motorRight.setSpeed(-1 * self.speed * self.motorRightCorrection)
			self.status = "backward"
			
	def goRight(self, difference):
		print "r"
		if self.status != "right":
			if self.status == "stopped":
				self.__restart()
			if self.status != "foward":
				self.motorLeft.setSpeed(self.speed)
			self.motorRight.setSpeed((self.speed - difference))
			self.status = "right"

	def goLeft(self, difference):
		print "l"
		if self.status != "left":
			if self.status == "stopped":
				self.__restart()
			if self.status != "foward":
				self.motorRight.setSpeed(self.speed)
			self.motorLeft.setSpeed((self.speed - difference))
			self.status = "left"

	def stop(self):
		if self.status != "stopped":
			self.motorLeft.stop()
			self.motorRight.stop()
			self.status = "stopped"

	def __restart(self):
		self.motorLeft.restart()
		self.motorRight.restart()
