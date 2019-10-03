# Machine Learning Keras Suite
#
# A Python submodule that trains the given data structure.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   15.09.2019
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
import os
import json
from mlks.commands.image_classifier.main import ImageClassifier


class Train(ImageClassifier):

    def __init__(self, config):
        self.tl_models = {
            'InceptionV3': Train.get_tl_inceptionv3,
        }

        # initialize the parent class
        super().__init__(config)

    def do(self):
        if not self.is_config_correct(self.config):
            return

        # preparations
        self.start_timer('preparations')
        model = self.get_model()
        train_generator = self.get_train_generator()
        self.finish_timer('preparations')

        # prints out some informations
        if self.config.get('verbose'):
            click.echo('LAYERS')
            click.echo('------')
            for i, layer in enumerate(model.layers):
                print(i, ': ', layer.name, '(trainable)' if layer.trainable else '(not trainable)')
            click.echo('------\n\n')

            click.echo('CLASSES')
            click.echo('-------')
            click.echo(train_generator.class_indices)
            click.echo('-------\n\n')

        # train the model
        self.start_timer('fit')
        self.train(model, train_generator)
        self.finish_timer('fit')

        # save the model to import within dl4j
        model_file = self.config.get_data('model_file')
        if model_file is not None:
            self.start_timer('save model')
            model.save(model_file)
            self.finish_timer('save model')

        # save config data from model to import within dl4j
        config_file = self.config.get_data('config_file')
        if config_file is not None:
            self.config.set_environment('classes', train_generator.class_indices, flip=True, flip_as_array=True)
            #self.config.set_measurement('fit', 12345)
            #self.config.set_measurement('preparation', 987)

            if self.config.get('verbose'):
                click.echo('Write config file to %s' % config_file)
            with open(config_file, 'w') as json_file:
                json.dump(self.config.get_dict(), json_file, sort_keys=True, indent=4, separators=(',', ': '))
