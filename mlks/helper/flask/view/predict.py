# Machine Learning Keras Suite
#
# A Python JsonDataReader class: Reads data from json and combine them with
# the given prediction list.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   28.09.2020
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

# import classes
import json

# load some modules
from flask_classful import FlaskView, route
from flask import render_template, request, send_from_directory
from mlks.helper.representations import output_json, output_html
from mlks.helper.json_data_builder import JsonDataBuilder


class PredictView(FlaskView):
    representations = {
        'application/json': output_json,
        'text/html': output_html
    }

    excluded_methods = ['set_config_json_path', 'set_prediction_data', 'set_parameter', 'get_request']

    config_json_path: str = None

    prediction_data: object = None

    parameter_language: str = 'DE'
    parameter_number: int = 5
    parameter_output_type: str = 'simple'

    @staticmethod
    def set_config_json_path(config_json_path: str):
        PredictView.config_json_path = config_json_path

    @staticmethod
    def set_prediction_data(prediction_data: object):
        PredictView.prediction_data = prediction_data

    @staticmethod
    def set_parameter(parameter_language: str = 'DE', parameter_number: int = 5,
                      parameter_output_type: str = 'simple'):
        PredictView.parameter_language = parameter_language
        PredictView.parameter_number = parameter_number
        PredictView.parameter_output_type = parameter_output_type


    @staticmethod
    def get_request(name, default=None, type=None):
        if request.json is None:
            return request.form.get(name, default=default, type=type)

        # convert json value into dict
        data_dict =  json.loads(request.json)

        # default value
        value = default

        if name in data_dict:
            value = data_dict[name]

        # convert integer type
        if type == int:
            value=int(value)

        return value

    @route('', methods=['GET'])
    @route('/', methods=['GET'])
    def index(self):
        return_data = render_template('post_image.html', title='Post an image.', text='Please post an image. :)')
        return return_data, 200

    @route('', methods=['POST'])
    def post(self):
        language = self.get_request('language', default=self.parameter_language)
        number = self.get_request('number', default=self.parameter_number, type=int)
        output_type = self.get_request('output_type', default=self.parameter_output_type)

        json_data_reader = JsonDataBuilder(json_path=self.config_json_path, prediction=self.prediction_data)
        return_data = json_data_reader.get_info_as_data(number=number, language=language, output_type=output_type)

        return return_data, 200
