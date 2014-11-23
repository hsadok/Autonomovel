# 
# moviment.py : This program is used to move the car freely without training
#               capabilities.
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


import sys, tty, termios, time, threading
from car import *

char = None

def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

class KeyThread(threading.Thread):
	charCounter = 0
	def __init__(self):
		super(KeyThread, self).__init__()
		self.terminated = False
		self.start()

	def run(self):
		global char
		while not self.terminated:
			tempChar = getch()
			if tempChar == char:
				charCounter += 1
			else:
				charCounter = 0
			char = tempChar
			keyWaiting.event.set()


class KeyWaiting(threading.Thread):
	def __init__(self):
		super(KeyWaiting, self).__init__()
		self.terminated = False
		self.event = threading.Event()
		self.start()

	def run(self):
		global char
		while not self.terminated:
			if self.event.wait(0.5):
				self.event.clear()
			else:
				if KeyThread.charCounter != 1:
					char = None


keyWaiting = KeyWaiting()
keyThread = KeyThread()

validKeys = ['w', 'd', 'a', 's']

car = Car()
difference = 50

while True:
	if char in validKeys:
		if char == validKeys[0]:
			car.goFoward()
		elif char == validKeys[1]:
			car.goRight(difference)
		elif char == validKeys[2]:
			car.goLeft(difference)
		elif char == validKeys[3]:
			car.goBackward()
	else:
		car.stop()
		if (char == 'q'):
			keyThread.terminated = True
			keyWaiting.terminated = True
			break
	time.sleep(0.01)
