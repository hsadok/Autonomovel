# 
# artificial_images.py : Create new images from existing images with different
#                        brightness. This is useful to get more samplings making
#                        the neural network more robust.
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

import glob

from PIL import Image
import ImageEnhance

for image_file in glob.glob('*.png'):
    image = Image.open(image_file)
    enhancer = ImageEnhance.Brightness(image)
    for factor in [0.5, 0.75, 1.25, 1.75]:
        name = image_file[:-7] + '-' + str(factor) + image_file[-7:]
        enhancer.enhance(factor).save(name)
