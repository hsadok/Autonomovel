# 
# self_driving.py : Program to drive the car based on the Neural Network decisions
# 
# This code has influence from a recipe in this page:
#        http://picamera.readthedocs.org/en/release-1.8/recipes2.html
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

import io
import time
import threading
import picamera
import numpy as np
from PIL import Image

from car import *
from predict import predict

done = False
lock = threading.Lock()
pool = []
imageLock = threading.Lock()

programStartTime = time.time()

car = Car()

print 'carregando os thetas...'
Theta1 = np.genfromtxt('theta1.txt', delimiter=' ')
Theta2 = np.genfromtxt('theta2.txt', delimiter=' ')
print 'thetas carregados!'
class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.difference = 100
        self.start()

    def run(self):
        global done
        while not self.terminated:
            if self.event.wait(1):
                try:
                    self.stream.seek(0)

                    with imageLock:
                        if not done:
                            X = np.array(Image.open(self.stream).convert('L').getdata())
                            X = X.reshape(1, X.size)
                            
                            self.currentKey = predict(Theta1, Theta2, X)

                            print self.currentKey

                            if self.currentKey == 0:#foward
                                car.goFoward()
                            elif self.currentKey == 1:#right
                                car.goRight(self.difference)
                            elif self.currentKey == 2:#left
                                car.goLeft(self.difference)
                except KeyboardInterrupt as e:
                    raise e
                    done = True

                finally:
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    with lock:
                        pool.append(self)

def streams():
    while not done:
        with lock:
            processor = pool.pop()
        yield processor.stream
        processor.event.set()

with picamera.PiCamera() as camera:
    pool = [ImageProcessor() for i in range (10)]
    camera.resolution = (100, 100)
    camera.framerate = 5
    time.sleep(2)
    timeBegin = time.time()

    camera.capture_sequence(streams(), use_video_port=True)

timeEnd = time.time()

logFile = open('log.txt', 'w')
logFile.write('Duration: ' + str(timeEnd - timeBegin) + '\n')
logFile.close()

while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()