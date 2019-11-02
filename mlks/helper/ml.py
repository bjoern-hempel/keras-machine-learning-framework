# Machine Learning Keras Suite
#
# A Python helper file: Provides some machine learning helper.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   02.11.2019
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


def get_epoch_array(epochs, learning_rate, learning_rate_drop, learning_rate_epochs_drop):
    epoch_current = 1
    learning_rate_current = learning_rate
    epoch_array = []
    while epoch_current < epochs:
        epoch_from = epoch_current
        epoch_to = epoch_from + learning_rate_epochs_drop - 1
        epoch_to = epochs if epochs < epoch_to else epoch_to

        epoch_array.append({
            'epoch_from': epoch_from,
            'epoch_to': epoch_to,
            'learning_rate': learning_rate_current
        })

        epoch_current += learning_rate_epochs_drop
        learning_rate_current *= learning_rate_drop

    return epoch_array
