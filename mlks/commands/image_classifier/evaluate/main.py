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
import json
import sys
from pathlib import Path
from mlks.commands.image_classifier.main import ImageClassifier
from mlks.helper.filesystem import check_if_file_exists


class Evaluate(ImageClassifier):

    def __init__(self, config):

        # initialize the parent class
        super().__init__(config)

    def do(self):

        # some configs
        show_image = True
        save_image = True
        evaluate_type = 'validation' # validation or train
        save_evaluation_file = True
        do_not_cache = False
        rebuild_model_dict = False

        # load config file
        self.start_timer('load json config file')
        self.config.load_json_from_config_file(self.config.get_data('config_file'))
        self.finish_timer('load json config file')

        # rebuild model dict
        if rebuild_model_dict:
            self.config.rebuild_model_dict()
            self.start_timer('save json config file')
            self.config.save_json()
            self.finish_timer('save json config file')

        # get some configs
        model_file = self.config.get_data('model_file_best')['model_file']
        files_all = self.config.get_environment('files')
        files_validation = files_all[evaluate_type]
        data_path = self.config.get_data('data_path')
        root_path = os.path.dirname(self.config.get_data('config_file'))
        evaluation_files = []

        # data array
        data = {
            'root_path': root_path,
            'classes': [],
            'data': {},
            'top_k': {
                'correctly_classified_top_1': [],
                'incorrectly_classified_top_1': [],
                'correctly_classified_top_5': [],
                'incorrectly_classified_top_5': []
            }
        }

        # bulid evaluation file array
        for class_name in files_validation:
            for file_name in files_validation[class_name]:
                evaluation_files.append(os.path.join(data_path, class_name, file_name))

        # check model file
        check_if_file_exists(model_file)

        # load model
        self.start_timer('load model file "%s"' % model_file)
        model = self.load_model(model_file)
        self.finish_timer('load model file "%s"' % model_file)

        # evaluate all collected files
        for evaluation_file in evaluation_files:
            self.evaluate_file(model, evaluation_file, show_image, save_image)

        # evaluate all collected files
        for evaluation_file in evaluation_files:
            evaluation_data = self.evaluate_file(model, evaluation_file, show_image, save_image, do_not_cache)
            data['classes'] = evaluation_data['classes']

            del evaluation_data['prediction_overview']
            del evaluation_data['classes']

            evaluation_data['evaluation_file'] = evaluation_data['evaluation_file'].replace(
                '%s/' % data['root_path'], ''
            )
            index_key = evaluation_data['evaluation_file']

            data['data'][index_key] = evaluation_data

            if evaluation_data['is_top_1']:
                data['top_k']['correctly_classified_top_1'].append(index_key)
            else:
                data['top_k']['incorrectly_classified_top_1'].append(index_key)

            if evaluation_data['is_top_5']:
                data['top_k']['correctly_classified_top_5'].append(index_key)
            else:
                data['top_k']['incorrectly_classified_top_5'].append(index_key)

        # save evaluation file
        if save_evaluation_file:
            json_file = os.path.join(root_path, 'evaluation-file-%s.json' % evaluate_type)
            self.start_timer('Write json file "%s"' % json_file)
            with open(json_file, 'w') as outfile:
                json.dump(data, outfile, indent=4)
            self.finish_timer('Write json file "%s"' % json_file)
