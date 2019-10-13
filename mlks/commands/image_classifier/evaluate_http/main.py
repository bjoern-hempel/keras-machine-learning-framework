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
from http.server import HTTPServer
from mlks.helper.simple_http_request_handler import SimpleHTTPRequestHandler
from mlks.commands.image_classifier.main import ImageClassifier
from mlks.helper.filesystem import check_if_file_exists, add_file_extension, PNG_EXTENSION


class EvaluateHttp(ImageClassifier):

    def __init__(self, config):
        # initialize the parent class
        super().__init__(config)

    def POST_hook(self, upload_data, model):
        show_image = False
        save_image = True

        # get file to evaluate
        evaluation_file = upload_data['upload_path']
        graph_file = add_file_extension(add_file_extension(evaluation_file, 'graph', True), PNG_EXTENSION)
        evaluation_file_web = upload_data['upload_path_web']
        graph_file_web = add_file_extension(add_file_extension(evaluation_file_web, 'graph', True), PNG_EXTENSION)

        self.evaluate_file(model, evaluation_file, show_image, save_image)

        prediction_overview = """classes
-------
01) dahlia:                        94.21%
02) sunflower:                      3.09%
03) rose:                           1.62%
04) coneflower:                     0.84%
05) daisy:                          0.10%
06) poppy:                          0.04%
07) middayflower:                   0.04%
08) tulip:                          0.02%
09) dandelion:                      0.02%
10) ranunculus:                     0.01%
-------"""

        prediction_class = 'dahlia'
        prediction_accuracy = 94.21

        return_value = {
            'evaluated_file': evaluation_file,
            'graph_file': graph_file,
            'evaluated_file_web': evaluation_file_web,
            'graph_file_web': graph_file_web,
            'prediction_overview': prediction_overview,
            'prediction_class': prediction_class,
            'prediction_accuracy': prediction_accuracy
        }

        return return_value

    def do(self):
        # some configs
        show_image = True

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

        # check model file
        check_if_file_exists(model_file)

        # load model
        self.start_timer('load model file %s' % model_file)
        model = self.load_model(model_file)
        self.finish_timer('load model file %s' % model_file)

        # set hooks
        SimpleHTTPRequestHandler.set_POST_hook({
            'lambda': self.POST_hook,
            'arguments': [model]
        })

        click.echo('')
        click.echo('Ready for evaluation. Now upload some images...')
        click.echo('')

        try:
            use_ssl = False
            port = 4443 if use_ssl else 8000
            httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
            print('Webserver started on port %d..' % port)

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
