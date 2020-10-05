# Machine Learning Keras Suite
#
# A Python helper file: Provides the ApiHTTPRequestHandler class.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   04.10.2020
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

# import some packages
import cgi
import re
import os
import magic
import base64
import collections
import json
import sys

# import some classes and functions
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from mlks.helper.json_data_builder import JsonDataBuilder


class ApiHTTPRequestHandler(BaseHTTPRequestHandler):

    hooks: dict = {}

    properties: dict = {}

    MIME_TYPES_IMAGES: list = ['image/png', 'image/jpeg', 'image/x-icon']

    MIME_TYPES_ALLOWED_UPLOAD: list = ['image/jpeg', 'image/png']

    MIME_TYPES_TEXT: list = ['text/plain', 'text/xml']

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

        ApiHTTPRequestHandler.hooks[name] = hook

    @staticmethod
    def set_property(name, value):
        ApiHTTPRequestHandler.properties[name] = value

    @staticmethod
    def get_property(name):
        if name not in ApiHTTPRequestHandler.properties:
            return None

        return ApiHTTPRequestHandler.properties[name]

    @staticmethod
    def call_hook(*args):
        name = args[0]

        # check namespace
        if name not in ApiHTTPRequestHandler.hooks:
            return None

        # merge arguments
        arguments = list(args[1:]) + ApiHTTPRequestHandler.hooks[name]['arguments']

        # execute lambda function
        return ApiHTTPRequestHandler.hooks[name]['lambda'](*arguments)

    def get_json_data(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        # refuse to receive non-json content
        if ctype != 'application/json':
            return {'success': False}

        # read the message and convert it into a python dictionary
        length = int(self.headers.get('content-length'))
        post_vars = json.loads(self.rfile.read(length))

        # sometimes the payload is a string value
        if isinstance(post_vars, str):
            post_vars = json.loads(post_vars)

        return post_vars

    def get_template(self, template_name: str, parameters: dict = {}):
        """Returns the translated template

        Parameters
        ----------
        template_name : str
        parameters : dict

        Returns
        -------
        str

        """
        full_template_path = '%s/%s' % (self.get_property('template_folder'), template_name)

        if not os.path.exists(full_template_path):
            raise AssertionError('File "%s" does not exists.' % full_template_path)

        with open(full_template_path, 'r') as file:
            template_content = file.read()

            for key in parameters:
                template_content = template_content.replace('{{ %s }}' % key, parameters[key])

            return template_content

    @staticmethod
    def save_image(form: object):
        """Saves the uploaded image to image folder.

        Returns
        -------
        object

        """

        predict_file_raw = form['predict-file-raw'] if 'predict-file-raw' in form else None
        predict_file_name = form['predict-file-name'] if 'predict-file-name' in form else None

        predict_file_raw = None if predict_file_raw == '' else predict_file_raw
        predict_file_name = None if predict_file_name == '' else predict_file_name

        # no image file was given
        if predict_file_raw is None or predict_file_name is None:
            return {
                'success': False,
                'code': 400,
                'message': 'No file was uploaded. Please choose a file to predict before uploading it.'
            }

        # image file was given
        if predict_file_name:

            # check file
            output = re.search('^data:image/([a-z]+);base64,', predict_file_raw, flags=re.IGNORECASE)
            if output is None:
                return {
                    'success': False,
                    'code': 400,
                    'message': 'Unknown file format from file "%s".' % predict_file_name
                }

            # remove header
            predict_file_raw = re.sub('^data:image/([a-z]+);base64,', '', predict_file_raw)
            predict_file_raw = predict_file_raw.replace(' ', '+')
            predict_file_raw = base64.b64decode(predict_file_raw)

            # save file to upload folder
            upload_path = os.path.join(ApiHTTPRequestHandler.get_property('image_folder'), predict_file_name)
            open(upload_path, 'wb').write(predict_file_raw)

            # check mime type of given image
            mime = magic.Magic(mime=True)
            mime_type = mime.from_file(upload_path)

            if mime_type not in ApiHTTPRequestHandler.MIME_TYPES_ALLOWED_UPLOAD:
                # TODO: delete the uploaded file, because its wrong

                return {
                    'success': False,
                    'code': 400,
                    'message': 'The mime type "%s" of uploaded file "%s" is not allowed.' % (
                        mime_type,
                        predict_file_name
                    )
                }

            # add data to return value
            return {
                'success': True,
                'code': 200,
                'message': None,
                'data': {
                    'image': {
                        'fullpath': upload_path,
                        'path': '%s' % predict_file_name,
                        'url': '/img/%s' % predict_file_name
                    }
                }
            }

    def respond_html(self, response: str, status: int = 200):
        """Returns html code and status

        Parameters
        ----------
        response : str
        status : int

        Returns
        -------
        bool

        """
        self.send_response(status)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', len(response))
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))
        return True

    def respond_json(self, response: object, status: int = 200):
        json_content = json.dumps(response, indent=4)

        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Content-length', len(json_content))
        self.end_headers()
        self.wfile.write(bytes(json_content, 'utf-8'))
        return True

    def respond_file(self, folder, path, content_type='text/plain; charset=utf-8', status=200):

        # build full file path
        if folder is None:
            file_path = '%s/%s' % (self.get_property('static_folder'), path)
        else:
            file_path = '%s/%s/%s' % (self.get_property('static_folder'), folder, path)

        # is image
        is_image = content_type in self.MIME_TYPES_IMAGES

        if is_image:
            picture_info = os.stat(file_path)
            img_size = picture_info.st_size

            self.send_response(status)
            self.send_header('Content-type', content_type)
            self.send_header('Content-length', img_size)
            self.end_headers()

            f = open(file_path, 'rb')
            self.wfile.write(f.read())
            f.close()
        else:
            with open(file_path, 'r') as file:
                file_content = file.read()

            self.send_response(status)
            self.send_header('Content-type', content_type)
            self.send_header('Content-length', len(file_content))
            self.end_headers()
            self.wfile.write(bytes(file_content, 'utf-8'))

        return True

    def do_GET_img(self, argument, hook_results):
        return self.do_GET_file('img', argument, hook_results)

    def do_GET_file(self, path, argument, hook_results):
        """ do_GET_file """

        # build full file path
        if path is None:
            full_file_path = '%s/%s' % (self.get_property('static_folder'), argument)
        else:
            full_file_path = '%s/%s/%s' % (self.get_property('static_folder'), path, argument)

        print(full_file_path)

        # file was not found -> 404
        if not os.path.isfile(full_file_path):
            return False

        # get mime type
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(full_file_path)

        # image was found
        if mime_type in self.MIME_TYPES_IMAGES:
            return self.respond_file(path, argument, mime_type)

        # text was found
        if mime_type in self.MIME_TYPES_TEXT:
            return self.respond_file(path, argument, '%s; charset=utf-8' % mime_type)

        # unknown file type was found
        print('unknown file type "%s"' % mime_type)
        return False

    def do_GET_favicon(self, argument, hook_results):
        """ @route GET /favicon """
        return self.do_GET_file(None, argument, hook_results)

    def do_GET_css(self, argument, hook_results):
        """ @route GET /css """
        self.respond_file('css', argument, 'text/css; charset=utf-8')
        return True

    def do_GET_js(self, argument, hook_results):
        """ @route GET /js """
        self.respond_file('js', argument, 'application/javascript; charset=utf-8')
        return True

    def do_GET(self):
        """ @route GET /

        Returns
        -------
        None

        """
        parsed = urlparse(self.path)
        url_path = parsed.path

        # Routes to check
        routes = ['css', 'js', 'favicon', 'manifest', 'img']

        # hook results
        hook_results = {}

        # Get root
        if url_path == '/':
            return self.respond_html(self.get_template('post_image.html', {'title': 'Upload image to predict.'}), 200)

        # Get root
        if url_path == '/v1.0':
            return self.respond_html(self.get_template('post_image.html', {'title': 'Upload image to predict.'}), 200)

        # Get favicon
        if url_path == '/favicon.ico':
            return self.do_GET_favicon('favicon.ico', hook_results)

        # Try to find a special route
        for route in routes:
            output = re.search('^/%s(/(.+)?)?$' % route, url_path, flags=re.IGNORECASE)
            if output is not None:
                route_function_name = 'do_GET_%s' % route.replace('-', '_')
                argument = output.group(2)

                if not hasattr(self, route_function_name):
                    raise AssertionError('Please add method "SimpleHTTPRequestHandler.%s()"' % route_function_name)

                # Call special GET function
                success = getattr(self, route_function_name)(argument, hook_results)
                if not success:
                    self.respond_html('', 404)
                    return

                return

        return self.respond_html('', 404)

    def do_POST(self):
        form = self.get_json_data()

        predict_file_raw = form['predict-file-raw'] if 'predict-file-raw' in form else None
        predict_file_name = form['predict-file-name'] if 'predict-file-name' in form else None

        predict_file_raw = None if predict_file_raw == '' else predict_file_raw
        predict_file_name = None if predict_file_name == '' else predict_file_name

        number = int(form['number'])
        language = form['language']
        output_type = form['output-type']

        # save image
        image_data = self.save_image(form)

        # error occurred while uploading image
        if image_data['code'] != 200:
            return self.respond_json(image_data, image_data['code'])

        # call prediction from image data
        prediction_data = self.call_hook('POST_prediction', image_data)
        config_json_path = self.get_property('config_json_path')

        # convert prediction_data to output (add informations from json)
        json_data_reader = JsonDataBuilder(json_path=config_json_path, prediction=prediction_data)
        return_data = json_data_reader.get_info_as_data(number=number, language=language, output_type=output_type)

        # add image data
        return_data['data']['image'] = image_data['data']['image']

        return self.respond_json(return_data, return_data['code'])
