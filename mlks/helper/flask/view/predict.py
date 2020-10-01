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
import os
import re
import base64
import magic
import collections

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

    excluded_methods = ['set_config_json_path', 'set_prediction_data', 'set_parameter', 'get_request',
                        'set_image_path', 'save_image', 'set_hook', 'call_hook']

    config_json_path: str = None

    prediction_data: object = None

    parameter_language: str = 'DE'
    parameter_number: int = 5
    parameter_output_type: str = 'simple'

    image_path = None

    ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png']

    hooks = {}

    @staticmethod
    def set_image_path(image_path: str):
        PredictView.image_path = image_path

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
    def set_hook(name, hook):
        if 'lambda' not in hook:
            raise AssertionError('The given hook is invalid (no lambda function given).')

        if not isinstance(hook['lambda'], collections.Callable):
            raise AssertionError('The given hook is invalid (lambda function is not callable).')

        if 'arguments' not in hook:
            hook['arguments'] = []

        if not isinstance(hook['arguments'], list):
            raise AssertionError('The given hook is invalid (parameter argument must be a list).')

        PredictView.hooks[name] = hook

    @staticmethod
    def call_hook(*args):
        name = args[0]

        # check namespace
        if name not in PredictView.hooks:
            return None

        # merge arguments
        arguments = list(args[1:]) + PredictView.hooks[name]['arguments']

        # execute lambda function
        return PredictView.hooks[name]['lambda'](*arguments)

    @staticmethod
    def save_image(output_type: str, return_data: object):
        """Saves the uploaded image to image folder.

        Parameters
        ----------
        output_type : str
        return_data : object

        Returns
        -------
        object

        """
        predict_file_raw = PredictView.get_request('predict-file-raw')
        predict_file_name = PredictView.get_request('predict-file-name')

        if predict_file_name:
            predict_file_raw = None if predict_file_raw == '' else predict_file_raw
            predict_file_name = None if predict_file_name == '' else predict_file_name

            if predict_file_raw is None or predict_file_name is None:
                return_data.update({
                    'success': False,
                    'message': 'No file was uploaded. Please choose a file to predict before uploading it.'
                })
                return return_data

            # check file
            output = re.search('^data:image/([a-z]+);base64,', predict_file_raw, flags=re.IGNORECASE)
            if output is None:
                return_data.update({
                    'success': False,
                    'message': 'Unknown file format from file "%s".' % predict_file_name
                })
                return return_data

            # remove header
            predict_file_raw = re.sub('^data:image/([a-z]+);base64,', '', predict_file_raw)
            predict_file_raw = predict_file_raw.replace(' ', '+')
            predict_file_raw = base64.b64decode(predict_file_raw)

            # save file to upload folder
            upload_path = os.path.join(PredictView.image_path, predict_file_name)
            open(upload_path, 'wb').write(predict_file_raw)

            # check mime type of given image
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(upload_path)

            if mime_type not in PredictView.ALLOWED_MIME_TYPES:
                return_data.update({
                    'success': False,
                    'message': 'The mime type "%s" of uploaded file "%s" is not allowed.' % (
                        mime_type,
                        predict_file_name
                    )
                })

            # add data to return value
            if output_type != 'raw':
                return_data['data']['image'] = {
                    'fullpath': upload_path,
                    'path': '%s' % predict_file_name,
                    'url': '/img/%s' % predict_file_name
                }

            return return_data

    @staticmethod
    def get_request(name: str, default=None, type=None):
        """Returns the posted value if given. Otherwise return the default.

        Parameters
        ----------
        name : str
        default
        type

        Returns
        -------

        """
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
        output_type = self.get_request('output-type', default=self.parameter_output_type)

        self.call_hook('POST_prediction', 'call hook parameter (dynamic)')

        json_data_reader = JsonDataBuilder(json_path=self.config_json_path, prediction=self.prediction_data)
        return_data = json_data_reader.get_info_as_data(number=number, language=language, output_type=output_type)

        self.save_image(output_type=output_type, return_data=return_data)

        return return_data, 200
