# Machine Learning Keras Suite
#
# This is the basic image classifier class from which all train, evaluate and prepare classes inherit.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   02.10.2019
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

import click
from mlks.commands.main import Command
from keras.applications.inception_v3 import InceptionV3


class ImageClassifier(Command):

    def __init__(self, config):
        self.config = config

        # initialize the parent class
        super().__init__(config)
        pass

    def get_tl_model(self):
        transfer_learning_model = self.config.gettl('transfer_learning_model')

        if transfer_learning_model not in self.tl_models:
            raise AssertionError('Model "%s" was not assigned within tl_models.' % transfer_learning_model)

        if self.config.get('verbose'):
            click.echo('Use tl model "%s".' % transfer_learning_model)

        return self.tl_models[transfer_learning_model](self)

    def get_tl_inceptionv3(self):
        dim = self.config.gettl('input_dimension')
        weights = self.config.gettl('weights')
        return InceptionV3(weights=weights, include_top=False, input_shape=(dim, dim, 3))
