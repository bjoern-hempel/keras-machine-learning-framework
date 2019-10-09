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
import time
from mlks.commands.image_classifier.main import ImageClassifier
from mlks.helper.filesystem import check_if_file_exists


class EvaluateService(ImageClassifier):

    def __init__(self, config):

        # initialize the parent class
        super().__init__(config)

    def do(self):
        # some configs
        show_image = True

        # load config file
        self.start_timer('load json config file')
        self.config.load_json_from_config_file(self.config.get_data('config_file'))
        self.finish_timer('load json config file')

        # get some configs
        model_file = self.config.get_data('model_file')
        evaluation_path = self.config.get_data('evaluation_path')

        # check model file
        check_if_file_exists(model_file)

        # check given evaluation path
        if not os.path.isdir(evaluation_path):
            raise AssertionError('The given evaluation path "%s" must be a direcory.' % evaluation_path)

        # check given evaluation path
        number_of_files = sum([len(files) for r, d, files in os.walk(evaluation_path)])
        if number_of_files > 0:
            raise AssertionError('The given evaluation path "%s" must be empty.' % evaluation_path)

        # load model
        self.start_timer('load model file')
        model = self.load_model(model_file)
        self.finish_timer('load model file')

        # start service
        while True:
            # wait some time
            time.sleep(0.5)

            # get evaluation files
            files = os.listdir(evaluation_path)

            # predict if we found some images
            if len(files) > 0:
                evaluation_file = '%s/%s' % (evaluation_path, files[0])

                # check that the file is ready
                if 'crdownload' in evaluation_file:
                    continue

                self.evaluate_file(model, evaluation_file, show_image)
                os.remove(evaluation_file)
