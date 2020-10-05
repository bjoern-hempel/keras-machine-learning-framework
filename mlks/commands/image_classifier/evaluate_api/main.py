# Machine Learning Keras Suite
#
# A Python submodule that evaluate the given data structure.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   03.10.2019
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
import ssl
import click

# import ApiHTTPRequestHandler and HTTPServer
from mlks.http.api_http_request_handler import ApiHTTPRequestHandler
from http.server import HTTPServer

from mlks.commands.image_classifier.main import ImageClassifier
from mlks.helper.filesystem import check_if_file_exists

class EvaluateApi(ImageClassifier):

    def __init__(self, config):
        # initialize the parent class
        super().__init__(config)

    def do_post_hook(self, return_data: object, model: object, debug_mode: bool = True):
        # Some configs
        verbose = self.config.get('verbose')

        # Do something with image path. Prediction? ;)
        evaluation_file = return_data['data']['image']['fullpath']

        # Print some debugging informations
        if verbose:
            click.echo('return_data')
            click.echo(return_data)
            click.echo('model')
            click.echo(model)
            click.echo('Image path: %s' % evaluation_file)

        # Do something with image path. Prediction? ;)
        self.start_timer('prediction')
        evaluation_data = self.evaluate_file(model, evaluation_file, True, True)
        self.finish_timer('prediction')

        if verbose:
            click.echo(evaluation_data)

        # return fake prediction
        return evaluation_data

    def do(self):
        # some configs
        show_image = True
        debug_mode = False
        use_ssl = False

        # load config file
        self.start_timer('load json config file')
        self.config.load_json_from_config_file(self.config.get_data('config_file'))
        self.finish_timer('load json config file')

        # rebuild model dict
        self.config.rebuild_model_dict()
        self.start_timer('save json config file')
        self.config.save_json()
        self.finish_timer('save json config file')

        # Some configs
        verbose = self.config.get('verbose')
        port = self.config.get('port_ssl', 'http') if use_ssl else self.config.get('port', 'http')
        ip = self.config.get('bind_ip', 'http')

        # get some configs
        model_file: str = self.config.get_data('model_file_best')['model_file']
        config_json_path: str = 'C:/Users/bjoern/Development/keras-machine-learning-framework-json-editor/data/mushrooms.json'

        # some other configs
        parameter_language: str = 'DE'
        parameter_number: int = 5
        parameter_output_type: bool = 'simple'

        root_dir = 'C:/Users/bjoern/Development/keras-machine-learning-framework'
        template_folder = '%s/templates' % root_dir
        static_folder = '%s/static' % root_dir
        image_folder = '%s/img' % static_folder

        # check model file
        check_if_file_exists(model_file)
        check_if_file_exists(config_json_path)

        # print environment name
        if verbose:
            click.echo('Environment name: %s' % os.environ['CONDA_DEFAULT_ENV'])

        # load model
        if not verbose:
            click.echo('Load model "%s". Please wait..' % model_file)
        self.start_timer('load model file %s' % model_file)
        model = self.load_model(model_file)
        self.finish_timer('load model file %s' % model_file)

        # set hooks and configs
        ApiHTTPRequestHandler.set_property('config_json_path', config_json_path)
        ApiHTTPRequestHandler.set_property('parameter_language', parameter_language)
        ApiHTTPRequestHandler.set_property('parameter_number', parameter_number)
        ApiHTTPRequestHandler.set_property('parameter_output_type', parameter_output_type)
        ApiHTTPRequestHandler.set_property('root_dir', root_dir)
        ApiHTTPRequestHandler.set_property('template_folder', template_folder)
        ApiHTTPRequestHandler.set_property('static_folder', static_folder)
        ApiHTTPRequestHandler.set_property('image_folder', image_folder)
        ApiHTTPRequestHandler.set_hook('POST_prediction', {
            'lambda': self.do_post_hook,
            'arguments': [model, debug_mode]
        })

        click.echo('')
        click.echo('Ready for evaluation. Now upload some images...')
        click.echo('')

        try:
            httpd = HTTPServer((ip, port), ApiHTTPRequestHandler)
            click.echo('Webserver started: %s:%d' % (ip, port))

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
            click.echo('^C received, shutting down the web server')
            httpd.socket.close()
