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
from mlks.helper.filesystem import check_if_file_exists


class EvaluateHttp(ImageClassifier):

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

        # rebuild model dict
        self.config.rebuild_model_dict()
        self.start_timer('save json config file')
        self.config.save_json()
        self.finish_timer('save json config file')

        # get some configs
        model_file = self.config.get_data('model_file_best')['model_file']
        evaluation_path = self.config.get_data('evaluation_path')

        # check model file
        check_if_file_exists(model_file)

        # load model
        self.start_timer('load model file %s' % model_file)
        model = self.load_model(model_file)
        self.finish_timer('load model file %s' % model_file)

        click.echo('')
        click.echo('Ready for evaluation. Now add the images to be evaluated to the folder "%s"...' % self.config.get_data('evaluation_path'))
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

        # # start service
        # while True:
        #     # wait some time
        #     time.sleep(0.5)
        #
        #     # get evaluation files
        #     files = os.listdir(evaluation_path)
        #
        #     # predict if we found some images
        #     if len(files) > 0:
        #         evaluation_file = '%s/%s' % (evaluation_path, files[0])
        #
        #         # check that the file is ready
        #         if 'crdownload' in evaluation_file:
        #             continue
        #
        #         self.evaluate_file(model, evaluation_file, show_image)
        #         os.remove(evaluation_file)
