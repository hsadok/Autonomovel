# 
# predict.py : Predict command based on the Neural Network thetas.
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

import numpy

def sigmoid(z):
	return 1.0 / (1.0 + numpy.exp(-1.0 * z))

#PREDICT Predict the label of an input given a trained neural network
#   p = PREDICT(Theta1, Theta2, X) outputs the predicted label of X given the
#   trained weights of a neural network (Theta1, Theta2)
def predict(Theta1, Theta2, X):
	
	m = X.shape[0]

	h1 = sigmoid(numpy.dot(numpy.concatenate((numpy.ones((m, 1)),  X), axis=1), Theta1.T))
	h2 = sigmoid(numpy.dot(numpy.concatenate((numpy.ones((m, 1)), h1), axis=1), Theta2.T))

	return numpy.argmax(h2)
