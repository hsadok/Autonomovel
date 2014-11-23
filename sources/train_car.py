# 
# train_car.py : Program to train the car, based on the commands given by the 
#                user and the camera photos.
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
from PIL import Image

from car import *
from KeyMonitoring import *

# Create a pool of image processors
done = False
lock = threading.Lock()
pool = []
imageListLock = threading.Lock()
imageList = []
numberOfImages = 100000
imageCounter = 0

programStartTime = time.time()

car = Car()

class ImageProcessor(threading.Thread):
    def __init__(self):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.validKeys = ['w', 'a', 'd', 's']
        self.difference = 100
        self.start()

    def run(self):
        # This method runs in a separate thread
        global done
        global numberOfImages
        global imageCounter
        global char
        global keyMonitor
        while not self.terminated:
            if self.event.wait(1):
                try:
                    self.stream.seek(0)

                    with imageListLock:
                        if not done:
                            self.currentKey = keyMonitor.getCurrentKey()
                            if self.currentKey in self.validKeys:
                                if self.currentKey == self.validKeys[0]:#foward
                                    car.goFoward()
                                    command = 'f'
                                elif self.currentKey == self.validKeys[1]:#right
                                    car.goRight(self.difference)
                                    command = 'r'
                                elif self.currentKey == self.validKeys[2]:#left
                                    car.goLeft(self.difference)
                                    command = 'l'
                                elif self.currentKey == self.validKeys[3]:#back
                                    car.goBackward()
                                    continue
                                
                                imageList.append(IndexedImage(Image.open(self.stream).convert('L'), imageCounter, command))
                                imageCounter += 1
                                if imageCounter >= numberOfImages:
                                    done = True

                            else:
                                Image.open(self.stream)#just get the image out of the stream
                                car.stop()
                                if (self.currentKey == 'q'):
                                    done = True
                            

                finally:
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    with lock:
                        pool.append(self)

class SavingThread(threading.Thread):
    def __init__(self):
        super(SavingThread, self).__init__()

    def run(self):
        counter = 0
        while not done:
            if(len(imageList) > 0):
                with imageListLock:
                    imageToSave = imageList.pop()
                imageToSave.save()
                counter +=1
            else:
                time.sleep(1)
        print "saved images during work: " + str(counter)

class IndexedImage:
    def __init__(self, image, index, command):
        self.image = image
        self.index = index
        self.command = command

    def save(self):
        imageName = 'image_sample-' + str(programStartTime) + '-' + "%06d" % self.index + '--' + self.command + '.png'
        self.image.save(imageName)#that must be PNG or other lossless format JPEG will not be a good idea

def streams():
    saving = SavingThread()
    saving.start()
    while not done:
        with lock:
            processor = pool.pop()
        yield processor.stream
        processor.event.set()

keyMonitor = KeyMonitoring()
with picamera.PiCamera() as camera:
    pool = [ImageProcessor() for i in range (10)]
    camera.resolution = (100, 100)
    camera.framerate = 10
    time.sleep(2)
    timeBegin = time.time()

    camera.capture_sequence(streams(), use_video_port=True)

timeEnd = time.time()
keyMonitor.stop()
for i in imageList:
    i.save()
logFile = open('log.txt', 'w')
logFile.write('Duration: ' + str(timeEnd - timeBegin) + '\n')
logFile.close()


while pool:
    with lock:
        processor = pool.pop()
    processor.terminated = True
    processor.join()
