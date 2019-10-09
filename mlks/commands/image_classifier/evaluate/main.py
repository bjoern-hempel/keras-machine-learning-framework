# Machine Learning Keras Suite
#
# A Python submodule that evaluate the given data structure.
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
import sys
from mlks.commands.image_classifier.main import ImageClassifier
from mlks.helper.filesystem import check_if_file_exists
from mlks.helper.graph import print_image
from keras.preprocessing.image import load_img
import matplotlib.pyplot as plt


class Evaluate(ImageClassifier):

    def __init__(self, config):

        # initialize the parent class
        super().__init__(config)

    def do(self):

        show_image = True
        save_image = True

        # load config file
        self.start_timer('load json config file')
        self.config.load_json_from_config_file(self.config.get_data('config_file'))
        self.finish_timer('load json config file')

        # get some configs
        model_file = self.config.get_data('model_file')
        evaluation_file = self.config.get_data('evaluation_file')
        classes = self.config.get_environment('classes')

        # check files
        check_if_file_exists(model_file)
        check_if_file_exists(evaluation_file)

        # load model
        self.start_timer('load model file')
        model = self.load_model(model_file)
        self.finish_timer('load model file')

        # load image
        self.start_timer('load image file')
        image = self.load_image(evaluation_file)
        self.finish_timer('load image file')

        # predict image
        self.start_timer('predict image file')
        predicted_array = model.predict(image)
        predicted_values = predicted_array.argmax(axis=-1)
        self.finish_timer('predict image file')

        # print some informations
        text = ""
        if self.config.get('verbose'):
            click.echo('\n\nclasses')
            click.echo('-------')
            for i in range(len(predicted_array[0])):
                className = classes[i] + ':'
                print('%s %10.2f%%' % (className.ljust(15), predicted_array[0][i] * 100))

                text += "\n" if text != "" else ""
                text += '%s %10.2f%%' % (className, predicted_array[0][i] * 100)
            click.echo('-------')

        # print predicted class
        click.echo('\n\npredicted class:')
        click.echo('----------------')
        click.echo('predicted: %s (%10.2f%%)' % (classes[predicted_values[0]], predicted_array[0][predicted_values[0]] * 100))
        click.echo('----------------')

        # show image
        if show_image:
            title = 'predicted: %s (%.2f%%)' % (classes[predicted_values[0]], predicted_array[0][predicted_values[0]] * 100)
            print_image(evaluation_file, title, text, save_image)
