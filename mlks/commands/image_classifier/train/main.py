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
import sys
import pathlib

from matplotlib import pyplot as plt

from mlks.commands.image_classifier.main import ImageClassifier
from mlks.helper.filesystem import check_if_file_exists


class Train(ImageClassifier):

    def __init__(self, config):

        # initialize the parent class
        super().__init__(config)

    def do(self):

        show_diagram = True
        model_file = None

        if self.config.gettl('continue'):
            model_file = self.config.get_data('model_source')
            click.echo('Continue learning from model %s' % model_file)

        # load the model the model
        if model_file is None:
            self.start_timer('load model "%s"' % self.config.getml('transfer_learning_model'))
            model = self.get_model()
            self.finish_timer('load model "%s"' % self.config.getml('transfer_learning_model'))
        else:
            self.start_timer('load model file %s' % model_file)
            check_if_file_exists(model_file)
            model = self.load_model(model_file)
            self.finish_timer('load model file %s' % model_file)

        # preparations
        self.start_timer('preparations')
        image_generator = self.get_image_generator()
        train_generator = self.get_train_generator(image_generator)
        validation_generator = self.get_validation_generator(image_generator)

        files = {
            'train': {},
            'validation': {}
        }

        # generate train list
        for file in train_generator.filenames:
            namespace = 'train'
            p = pathlib.Path(file)
            if p.parts[0] not in files[namespace]:
                files[namespace][p.parts[0]] = []
            files[namespace][p.parts[0]].append(' '.join(p.parts[1:]))

        # generate validation list
        for file in validation_generator.filenames:
            namespace = 'validation'
            p = pathlib.Path(file)
            if p.parts[0] not in files[namespace]:
                files[namespace][p.parts[0]] = []
            files[namespace][p.parts[0]].append(' '.join(p.parts[1:]))

        self.config.set_environment('files', files)
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

        # save the model to import within dl4j
        self.start_timer('save config')
        self.config.save_json()
        self.finish_timer('save config')

        # train the model
        self.start_timer('fit')
        history = self.train(model, train_generator, validation_generator)
        self.finish_timer('fit')

        # save the model to import within dl4j
        self.start_timer('save model')
        self.config.save_model(model)
        self.finish_timer('save model')

        # save config data from model to import within dl4j
        self.config.rebuild_model_dict()
        self.start_timer('save config')
        self.config.set_environment('classes', train_generator.class_indices, flip=True, flip_as_array=True)
        self.config.set_environment('accuracies_trained', history.history['acc'], flip=True, flip_as_array=True)
        self.config.set_environment('accuracies_validated', history.history['val_acc'], flip=True, flip_as_array=True)
        self.config.save_json()
        self.finish_timer('save config')

        # save accuracy diagram
        plt.plot(history.history['acc'], label='train')
        plt.plot(history.history['val_acc'], label='test')
        plt.legend()
        plt.savefig(self.config.get_data('accuracy_file'))

        # show accuracy diagram
        if show_diagram:
            plt.show()
