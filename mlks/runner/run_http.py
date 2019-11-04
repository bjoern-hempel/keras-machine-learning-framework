# Machine Learning Keras Suite
#
# The base http server for debugging purposes
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   13.10.2019
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

import ssl
import click
import os
import sys
from http.server import HTTPServer
from mlks.http.simple_http_request_handler import SimpleHTTPRequestHandler
from mlks.helper.filesystem import get_root_project_path, get_formatted_file_size, get_changed_date, get_database


class HttpRunner:

    @staticmethod
    def POST_prediction_hook(argument, upload_data):
        # only flower and food models are allowed in that moment
        if argument not in ['flower', 'food']:
            raise AssertionError('Unsupported model type "%s".' % argument)

        # get file to evaluate
        evaluation_file = upload_data['upload_path']
        evaluation_file_web = upload_data['upload_path_web']
        prediction_array = HttpRunner.get_fake_prediction_array(argument)

        print(prediction_array)

        prediction_class = prediction_array['prediction_class']
        prediction_accuracy = prediction_array['prediction_accuracy']
        prediction_overview_array = prediction_array['prediction_array']

        return_value = {
            'evaluated_file': evaluation_file,
            'graph_file': evaluation_file,
            'evaluated_file_web': evaluation_file_web,
            'graph_file_web': evaluation_file_web,
            'prediction_overview_array': prediction_overview_array,
            'prediction_class': prediction_class,
            'prediction_accuracy': prediction_accuracy,
            'prediction_time': 0.1
        }

        return return_value

    @staticmethod
    def GET_prediction_get_model_hook(argument):
        return HttpRunner.get_model_data(argument)

    @staticmethod
    def POST_prediction_get_model_hook(argument):
        return HttpRunner.get_model_data(argument)

    @staticmethod
    def get_model_data(argument):
        if argument not in SimpleHTTPRequestHandler.allowed_model_types:
            raise AssertionError('Unknown model type "%s"' % argument)

        model_path = 'C:/Users/bjoern/data/processed/flower_10/flower_10_1.inceptionv3.best.17-0.95.h5'
        model_name = os.path.basename(model_path)
        model_size = get_formatted_file_size(model_path) if os.path.isfile(model_path) else '121.12 MB'
        model_classes = 12
        model_learning_epochs = 20
        model_date = get_changed_date(model_path) if os.path.isfile(model_path) else '2019-10-20T11:54:25.125386+00:00'
        model_version = '1.02'

        return {
            'model_name': model_name,
            'model_size': model_size,
            'model_classes': model_classes,
            'model_learning_epochs': model_learning_epochs,
            'model_date': model_date,
            'model_version': model_version
        }

    @staticmethod
    @click.command()
    @click.option('--data-path', '-d', required=True, type=str)
    @click.option('--port', '-p', required=False, type=int, default=8080, show_default=True)
    @click.option('--port-ssl', '-p', required=False, type=int, default=4443, show_default=True)
    @click.option('--bind_ip', '-i', required=False, type=str, default='0.0.0.0', show_default=True)
    def run(data_path, port, port_ssl, bind_ip):
        """This scripts starts a simple demo http service for testing purpose."""
        try:
            SimpleHTTPRequestHandler.set_hook('POST_prediction', {
                'lambda': HttpRunner.POST_prediction_hook,
                'arguments': []
            })
            SimpleHTTPRequestHandler.set_hook('POST_prediction_get_model', {
                'lambda': HttpRunner.POST_prediction_get_model_hook,
                'arguments': []
            })
            SimpleHTTPRequestHandler.set_hook('GET_prediction_get_model', {
                'lambda': HttpRunner.GET_prediction_get_model_hook,
                'arguments': []
            })
            SimpleHTTPRequestHandler.set_property('root_data_path', data_path)
            SimpleHTTPRequestHandler.set_property('root_data_path_web', '/')
            SimpleHTTPRequestHandler.set_property('root_project_path', get_root_project_path())

            use_ssl = False
            port = port_ssl if use_ssl else port
            httpd = HTTPServer((bind_ip, port), SimpleHTTPRequestHandler)
            print('Webserver started on port %s:%d..' % (bind_ip, port))

            # activate ssl (openssl req -newkey rsa:2048 -new -nodes -keyout key.pem -out csr.pem)
            if use_ssl:
                httpd.socket = ssl.wrap_socket(
                    httpd.socket,
                    keyfile='./key.pem',
                    certfile='./csr.pem',
                    server_side=True
                )

            httpd.serve_forever()

        except KeyboardInterrupt:
            print('^C received, shutting down the web server')
            httpd.socket.close()

    @staticmethod
    def get_fake_prediction_array(model_type):
        prediction_array = {
            'flower': {
                'prediction_class': 'dahlia',
                'prediction_accuracy': 94.21,
                'prediction_array': [
                    {
                        'class_name': 'dahlia',
                        'predicted_value': 0.9421
                    },
                    {
                        'class_name': 'sunflower',
                        'predicted_value': 0.0309
                    },
                    {
                        'class_name': 'rose',
                        'predicted_value': 0.0162
                    },
                    {
                        'class_name': 'coneflower',
                        'predicted_value': 0.0084
                    },
                    {
                        'class_name': 'daisy',
                        'predicted_value': 0.0010
                    }
                ]
            },
            'food': {
                'prediction_class': 'pizza',
                'prediction_accuracy': 94.21,
                'prediction_array': [
                    {
                        'class_name': 'pizza',
                        'predicted_value': 0.9421
                    },
                    {
                        'class_name': 'burger',
                        'predicted_value': 0.0309
                    },
                    {
                        'class_name': 'salad',
                        'predicted_value': 0.0162
                    },
                    {
                        'class_name': 'brownies',
                        'predicted_value': 0.0084
                    },
                    {
                        'class_name': 'martini_on_the_rock',
                        'predicted_value': 0.0010
                    }
                ]
            }
        }

        if model_type not in prediction_array:
            return []

        return prediction_array[model_type]


def run():
    http_runner = HttpRunner()
    http_runner.run()
