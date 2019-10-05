# Machine Learning Keras Suite
#
# A Python helper file: log machine learning data.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   05.10.2019
# Web:    https://github.com/bjoern-hempel/machine-learning-keras-suite
#
# LICENSE
#
# MIT License
#
# Copyright (c) 2019 Björn Hempel <bjoern@hempel.li>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import keras


class MlLogger(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.validation_losses = []
        self.validation_accuracies = []
        self.train_losses = []
        self.train_accuracies = []

    def on_batch_end(self, batch, logs={}):
        self.validation_losses.append(logs.get('val_loss'))
        self.validation_accuracies.append(logs.get('val_acc'))
        self.train_losses.append(logs.get('loss'))
        self.train_accuracies.append(logs.get('acc'))
