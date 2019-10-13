# Machine Learning Keras Suite
#
# A Python helper file: Provides the SimpleHTTPRequestHandler class.
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

import cgi
import re
import os
import magic
import collections
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    HTML_BODY = """<html>
        <head>
            <title>Keras Machine Learning Framework - Evaluation Form</title>
            <style>
                .waitdiv {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%%;
                    height: 100%%;
                    background-color: #fff;
                    display: none;
                }
            </style>
            <script>
                window.pleaseWait = function () {
                    document.getElementById("waitdiv").style.display = "block";
                }
            </script> 
        </head>
        <body>
            <div class="waitdiv" id="waitdiv">%s</div>
            %s
        </body>
    </html>"""

    HTML_FORM = """<div>
        <form action="" method="post" enctype="multipart/form-data">
            <p>Select image to upload:</p>
            <p>
                <input type="file" name="file">
                <input
                    type="submit"
                    value="Upload Image"
                    onclick="window.pleaseWait()"
                >
            </p>
        </form>
    </div>"""

    HTML_PREDICTION = """<div>
        <h3>Source image</h3>
        <p><img src="%s" style="width: 500px;"></p>
        <h3>Predicted image (%s - %.2f%%)</h3>
        <p><img src="%s"></p>
        <h3>Prediction overview</h3>
        <pre>%s</pre>
    </div>"""

    HTML_ERROR = """<div>
        <p style="padding: 5px; background-color: red;">%s</p>
    </div>"""

    TEXT_UPLOAD = 'Your image is currently being uploaded and evaluated. Please wait...'

    ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png']

    hooks = {}

    def __init__(self, request, client_address, server):
        self.upload_path = 'F:/data/upload'
        self.upload_path_web = '/upload'

        super().__init__(request, client_address, server)

    @staticmethod
    def set_GET_hook(hook):
        SimpleHTTPRequestHandler.set_hook('GET', hook)

    @staticmethod
    def set_POST_hook(hook):
        SimpleHTTPRequestHandler.set_hook('POST', hook)

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

        SimpleHTTPRequestHandler.hooks[name] = hook

    @staticmethod
    def call_hook(*args):
        name = args[0]

        # check namespace
        if name not in SimpleHTTPRequestHandler.hooks:
            return None

        # merge arguments
        arguments = list(args[1:]) + SimpleHTTPRequestHandler.hooks[name]['arguments']

        # execute lambda function
        return SimpleHTTPRequestHandler.hooks[name]['lambda'](*arguments)

    def respond_html(self, response, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-length', len(response))
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))

    def respond_picture(self, picture_path, status=200):
        picture_info = os.stat(picture_path)
        img_size = picture_info.st_size

        self.send_response(status)
        self.send_header('Content-type', 'image/jpg')
        self.send_header('Content-length', img_size)
        self.end_headers()

        f = open(picture_path, 'rb')
        self.wfile.write(f.read())
        f.close()

    def write_upload_file(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )

        filename = form['file'].filename

        if filename == '':
            return {
                'error': True,
                'message': 'No file was uploaded.'
            }

        data = form['file'].file.read()
        upload_path = '%s/%s' % (self.upload_path, filename)
        upload_path_web = '%s/%s' % (self.upload_path_web, filename)
        open(upload_path, 'wb').write(data)

        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(upload_path)

        if mime_type not in self.ALLOWED_MIME_TYPES:
            return {
                'error': True,
                'message': 'The mime type "%s" of uploaded file "%s" is not allowed.' % (
                    mime_type,
                    filename
                )
            }

        return {
            'upload_path': upload_path,
            'upload_path_web': upload_path_web,
            'mime_type': mime_type,
            'error': False,
            'message': None
        }

    def do_GET(self):
        parsed = urlparse(self.path)
        url_path = parsed.path

        output = re.search('/upload/(.+)', url_path, flags=re.IGNORECASE)
        if output is not None:
            upload_image = output.group(1)
            upload_image_path = '%s/%s' % (self.upload_path, upload_image)
            self.respond_picture(upload_image_path)
            return

        # call hook
        GET_result = self.call_hook('GET')
        if GET_result is not None:
            print(GET_result)

        html_form = self.HTML_FORM
        html_body = self.HTML_BODY % (self.TEXT_UPLOAD, html_form)
        self.respond_html(html_body)
        return

    def do_POST(self):
        upload_data = self.write_upload_file()

        if upload_data['error']:
            html_content = self.HTML_ERROR % upload_data['message']
            html_content += self.HTML_FORM
            html_body = self.HTML_BODY % (self.TEXT_UPLOAD, html_content)
        else:
            # call post hook
            evaluation_data = self.call_hook('POST', upload_data)
            evaluated_file_web = evaluation_data['evaluated_file_web']
            graph_file_web = evaluation_data['graph_file_web']
            prediction_overview = evaluation_data['prediction_overview']
            prediction_class = evaluation_data['prediction_class']
            prediction_accuracy = evaluation_data['prediction_accuracy']

            html_content = self.HTML_PREDICTION % (
                evaluated_file_web,
                prediction_class,
                prediction_accuracy,
                graph_file_web,
                prediction_overview
            )
            html_content += self.HTML_FORM
            html_body = self.HTML_BODY % (self.TEXT_UPLOAD, html_content)

        self.respond_html(html_body)
