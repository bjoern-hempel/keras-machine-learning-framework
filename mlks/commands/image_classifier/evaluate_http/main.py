# Machine Learning Keras Suite
#
# A Python submodule that evaluate the given data structure (webserver).
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

import click
import ssl
import os
from http.server import HTTPServer
from mlks.http.simple_http_request_handler import SimpleHTTPRequestHandler
from mlks.commands.image_classifier.main import ImageClassifier
from mlks.helper.filesystem import check_if_file_exists, \
    add_file_extension, \
    get_root_project_path, \
    get_root_data_path, \
    get_formatted_file_size, \
    get_changed_date, \
    PNG_EXTENSION


class EvaluateHttp(ImageClassifier):

    def __init__(self, config):
        # initialize the parent class
        super().__init__(config)

    def POST_prediction_hook(self, argument, upload_data, models):
        # some configs
        show_image = False
        save_image = True

        # get model
        model = models[argument]['model']
        model_json_config = models[argument]['json_config']

        # load json
        self.config.load_json(model_json_config, True)

        # get file to evaluate
        evaluation_file = upload_data['upload_path']
        graph_file = add_file_extension(add_file_extension(evaluation_file, 'graph', True), PNG_EXTENSION)
        evaluation_file_web = upload_data['upload_path_web']
        graph_file_web = add_file_extension(add_file_extension(evaluation_file_web, 'graph', True), PNG_EXTENSION)

        self.start_timer('prediction')
        evaluation_data = self.evaluate_file(model, evaluation_file, show_image, save_image)
        self.finish_timer('prediction')

        prediction_overview_array = evaluation_data['prediction_overview_array']
        prediction_class = evaluation_data['prediction_class']
        prediction_accuracy = evaluation_data['prediction_accuracy']

        return_value = {
            'evaluated_file': evaluation_file,
            'graph_file': graph_file,
            'evaluated_file_web': evaluation_file_web,
            'graph_file_web': graph_file_web,
            'prediction_overview_array': prediction_overview_array,
            'prediction_class': prediction_class,
            'prediction_accuracy': prediction_accuracy,
            'prediction_time': '%.4f' % self.get_timer('prediction')
        }

        return return_value

    def GET_prediction_get_model_hook(self, argument, models):
        return self.get_model_data(argument, models)

    def POST_prediction_get_model_hook(self, argument, models):
        return self.get_model_data(argument, models)

    def get_model_data(self, argument, models):
        # check argument
        if argument not in models:
            return None

        # get model
        model_json_config = models[argument]['json_config']

        # load json
        self.config.load_json(model_json_config, True)

        # get model path
        model_path = models[argument]['model_path']
        model_name = os.path.basename(model_path)
        model_size = get_formatted_file_size(model_path) if os.path.isfile(model_path) else '121.12 MB'
        model_classes = len(self.config.get_environment('classes'))
        model_learning_epochs = self.config.getml('epochs')
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

    def loadConfig(self, config_file):
        # load config file
        self.start_timer('load json config file')
        self.config.load_json_from_config_file(config_file, True)
        self.finish_timer('load json config file')

        # rebuild model dict
        self.config.rebuild_model_dict(config_file)
        self.start_timer('save json config file')
        self.config.save_json()
        self.finish_timer('save json config file')

        return self.config

    def do(self):
        # prepare some vars
        model_files = {}
        models = {}

        config_file = self.config.get_data('config_file')
        config_file_2 = self.config.get_data('config_file_2')

        # add config (in that moment flower)
        models['flower'] = {
            'json_config': self.loadConfig(config_file).get_json()
        }

        # load second config (in that moment food)
        if config_file_2 is not None:
            models['food'] = {
                'json_config': self.loadConfig(config_file_2).get_json()
            }

        # iterate through all models
        for model_type in models:
            # load json config
            self.config.load_json(models[model_type]['json_config'], True)

            # get best model paths
            model_path = self.config.get_data('model_file_best')['model_file']

            # check all model files
            check_if_file_exists(model_path)

            # load models
            self.start_timer('load model "%s" file %s' % (model_type, model_path))
            model = None if self.config.get('debug') else self.load_model(model_path)
            self.finish_timer('load model "%s" file %s' % (model_type, model_path))

            # save model and file
            models[model_type]['model_path'] = model_path
            models[model_type]['model'] = model

        # set hooks
        SimpleHTTPRequestHandler.set_hook('POST_prediction', {
            'lambda': self.POST_prediction_hook,
            'arguments': [models]
        })
        SimpleHTTPRequestHandler.set_hook('POST_prediction_get_model', {
            'lambda': self.POST_prediction_get_model_hook,
            'arguments': [models]
        })
        SimpleHTTPRequestHandler.set_hook('GET_prediction_get_model', {
            'lambda': self.GET_prediction_get_model_hook,
            'arguments': [models]
        })
        SimpleHTTPRequestHandler.set_property('root_data_path', get_root_data_path(self.config.get_data('config_file')))
        SimpleHTTPRequestHandler.set_property('root_data_path_web', '/')
        SimpleHTTPRequestHandler.set_property('root_project_path', get_root_project_path())

        click.echo('')
        click.echo('Ready for evaluation. Now upload some images...')
        click.echo('')

        try:
            use_ssl = False
            port = self.config.get('port_ssl', 'http') if use_ssl else self.config.get('port', 'http')
            ip = self.config.get('bind_ip', 'http')
            httpd = HTTPServer((ip, port), SimpleHTTPRequestHandler)
            print('Webserver started on port %s:%d..' % (ip, port))

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
