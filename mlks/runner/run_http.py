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
from http.server import HTTPServer
from mlks.helper.simple_http_request_handler import SimpleHTTPRequestHandler
from mlks.helper.filesystem import add_file_extension, PNG_EXTENSION


class HttpRunner:
    def __init__(self):
        self.name = 'xyz'

    def POST_hook(self, upload_data):
        # get file to evaluate
        evaluation_file = upload_data['upload_path']
        graph_file = add_file_extension(add_file_extension(evaluation_file, PNG_EXTENSION), 'graph', True)

        print(upload_data)

        return {
            'evaluated_file': evaluation_file,
            'graph_file': graph_file
        }

    def run(self):
        try:
            SimpleHTTPRequestHandler.set_POST_hook({
                'lambda': self.POST_hook,
                'arguments': []
            })

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

def run():
    http_runner = HttpRunner()
    http_runner.run()
