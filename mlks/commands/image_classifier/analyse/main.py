# Machine Learning Keras Suite
#
# A Python submodule that evaluate the given data structure.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   11.09.2020
# Web:    https://github.com/bjoern-hempel/machine-learning-keras-suite
#
# LICENSE
#
# MIT License
#
# Copyright (c) 2020 Björn Hempel <bjoern@hempel.li>
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

import sys
from mlks.commands.image_classifier.main import ImageClassifier


class Analyse(ImageClassifier):

    def __init__(self, config):

        # initialize the parent class
        super().__init__(config)

    def do(self):

        # some configs
        show_image = False

        save_image = True
        save_svg = True
        save_pdf = True

        save_evaluation_file = True
        evaluate_type = self.config.get_data('analyse_type')

        # load config file
        self.start_timer('load json config file')
        self.config.load_json_from_config_file(self.config.get_data('config_file'))
        self.finish_timer('load json config file')

        # get some configs
        model_file = self.config.get_data('model_file_best')['model_file']
        files_all = self.config.get_environment('files')
        files_validation = files_all[evaluate_type]
        data_path = self.config.get_data('data_path')

        # get evaluated data
        data = self.get_evaluation_data(model_file, data_path, files_validation, evaluate_type, save_evaluation_file)

        # build confusion matrix
        self.build_confusion_matrix(data, evaluate_type, show_image, save_image, save_svg, save_pdf)
