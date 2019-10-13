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
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    HTML_BODY = """<html>
        <head>
            <title>Keras Machine Learning Framework - Evaluation Form</title>
        </head>
        <body>
            %s
        </body>
    </html>"""

    HTML_FORM = """<div>
        <form action="" method="post" enctype="multipart/form-data">
            <p>Select image to upload:</p>
            <p>
                <input type="file" name="file">
                <input type="submit" value="Upload Image">
            </p>
        </form>
    </div>"""

    HTML_PREDICTION = """<div>
        <p>%s</p>
        <p><img src="%s" style="width: 500px;"></p>
    </div>"""

    def __init__(self, request, client_address, server):
        self.upload_path = 'F:/data/upload'
        self.upload_path_web = '/upload'

        super().__init__(request, client_address, server)

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
        data = form['file'].file.read()
        upload_path = '%s/%s' % (self.upload_path, filename)
        upload_path_web = '%s/%s' % (self.upload_path_web, filename)
        open(upload_path, 'wb').write(data)

        return {
            'upload_path': upload_path,
            'upload_path_web': upload_path_web
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

        html_body = self.HTML_BODY % self.HTML_FORM
        self.respond_html(html_body)
        return

    def do_POST(self):
        upload_data = self.write_upload_file()

        html_content = self.HTML_PREDICTION % (
            upload_data['upload_path_web'],
            upload_data['upload_path_web']
        )
        html_body = self.HTML_BODY % html_content

        self.respond_html(html_body)
