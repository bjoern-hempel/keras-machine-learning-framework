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
from http.server import HTTPServer
from mlks.http.simple_http_request_handler import SimpleHTTPRequestHandler
from mlks.helper.filesystem import get_root_project_path


class HttpRunner:

    @staticmethod
    def POST_hook(upload_data):
        # get file to evaluate
        evaluation_file = upload_data['upload_path']
        evaluation_file_web = upload_data['upload_path_web']

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
            'graph_file': evaluation_file,
            'evaluated_file_web': evaluation_file_web,
            'graph_file_web': evaluation_file_web,
            'prediction_overview': prediction_overview,
            'prediction_class': prediction_class,
            'prediction_accuracy': prediction_accuracy,
            'prediction_time': 0.1
        }

        return return_value

    @staticmethod
    def GET_upload_hook(test):
        print(test)

    @staticmethod
    @click.command()
    @click.option('--data-path', '-d', required=True, type=str)
    @click.option('--port', '-p', required=False, type=int, default=8080, show_default=True)
    @click.option('--port-ssl', '-p', required=False, type=int, default=4443, show_default=True)
    @click.option('--bind_ip', '-i', required=False, type=str, default='0.0.0.0', show_default=True)
    def run(data_path, port, port_ssl, bind_ip):
        """This scripts starts a simple demo http service for testing purpose."""
        try:
            SimpleHTTPRequestHandler.set_POST_hook({
                'lambda': HttpRunner.POST_hook,
                'arguments': []
            })
            SimpleHTTPRequestHandler.set_hook('GET_upload', {
                'lambda': HttpRunner.GET_upload_hook,
                'arguments': ['my string']
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

def run():
    http_runner = HttpRunner()
    http_runner.run()
