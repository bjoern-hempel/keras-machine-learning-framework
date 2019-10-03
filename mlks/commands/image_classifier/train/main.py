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
from mlks.helper.filesystem import get_number_of_folders_and_files


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

        # get some needed configuration parameters
        number_trainable = self.config.gettl('number_trainable_layers')
        data_path = self.config.getData('data_path')

        # check folder
        if not os.path.isdir(data_path):
            raise AssertionError('"%s" does not exists or seems not to be a folder.')

        data_path_info = get_number_of_folders_and_files(data_path)
        categories = data_path_info['folders']

        # timer - preparations
        self.start_timer('preparations')
        model = self.get_model(categories, number_trainable)

        # prints the used layers of the current model
        if self.config.get('verbose'):
            for i, layer in enumerate(model.layers):
                print(i, ': ', layer.name, '(trainable)' if layer.trainable else '(not trainable)')

        train_generator = self.get_train_generator()
        self.config.set_environment('classes', train_generator.class_indices, flip=True, flip_as_array=True)
        self.finish_timer('preparations')
        # timer - preparations

        # train the model
        step_size_train = train_generator.n // train_generator.batch_size
        self.start_timer('fit')
        model.fit_generator(generator=train_generator,
                            steps_per_epoch=step_size_train,
                            epochs=10, verbose=1)
        self.finish_timer('fit')

        # save the model to import within dl4j
        model_path = self.config.getData('model_file')
        if model_path is not None:
            self.start_timer('save model')
            model.save(model_path)
            self.finish_timer('save model')

        # save config data from model to import within dl4j
        model_config = self.config.getData('model_config')
        if model_config is not None:
            #self.config.set_measurement('fit', 12345)
            #self.config.set_measurement('preparation', 987)

            if self.config.get('verbose'):
                click.echo('Write config file to %s' % model_config)
            with open(model_config, 'w') as json_file:
                json.dump(self.config.get_dict(), json_file, sort_keys=True, indent=4, separators=(',', ': '))
