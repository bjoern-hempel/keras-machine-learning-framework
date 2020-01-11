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

import os
import sys
from pathlib import Path
from mlks.commands.image_classifier.main import ImageClassifier
from mlks.helper.filesystem import check_if_file_exists


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

        # rebuild model dict
        self.config.rebuild_model_dict()
        self.start_timer('save json config file')
        self.config.save_json()
        self.finish_timer('save json config file')

        # get some configs
        model_file = self.config.get_data('model_file_best')['model_file']
        evaluation_files = []

        # check model file
        check_if_file_exists(model_file)

        # the given evaluation path is a folder with file inside
        if os.path.isdir(self.config.get_data('evaluation_path')):
            # load model
            self.start_timer('load model file "%s"' % model_file)
            model = self.load_model(model_file)
            self.finish_timer('load model file "%s"' % model_file)

            # build the generators
            self.start_timer('preparations')
            image_val_generator = self.get_image_generator()
            validation_generator = self.get_validation_generator(image_val_generator)
            self.finish_timer('preparations')

            # evaluate the given path
            self.start_timer('evaluation')
            self.evaluate_path(
                model,
                validation_generator,
                self.config.get_data('evaluation_path'),
                show_image,
                save_image
            )
            self.finish_timer('evaluation')

            return

        # the given evaluation path is a single file
        elif os.path.isfile(self.config.get_data('evaluation_path')):

            check_if_file_exists(self.config.get_data('evaluation_path'))
            evaluation_files.append(self.config.get_data('evaluation_path'))

            # load model
            self.start_timer('load model file "%s"' % model_file)
            model = self.load_model(model_file)
            self.finish_timer('load model file "%s"' % model_file)
        else:
            raise AssertionError('Unknown given path "%s"' % self.config.get_data('evaluation_path'))

        # evaluate all collected files
        for evaluation_file in evaluation_files:
            self.evaluate_file(model, evaluation_file, show_image, save_image)