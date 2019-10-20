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
import base64
import collections
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
from mlks.helper.filesystem import get_formatted_file_size, PNG_EXTENSION


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    TEXT_UPLOAD = 'Your image is currently being uploaded and evaluated. Please wait...'
    TEXT_EMPTY_IMAGE = 'No picture was given...'
    TEXT_IMAGE_WAS_NOT_FOUND = 'The given image "%s" was not found...'
    TEXT_FILE_WAS_NOT_FOUND = 'The given file "%s" was not found...'

    ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png']

    TEMPLATE_FILE_EXTENSION = 'tpl'

    hooks = {}

    properties = {}

    html_template_path = '%s/mlks/http/templates'
    css_template_path = '%s/mlks/http/css'
    file_template_path = '%s/mlks/http'

    def __init__(self, request, client_address, server):
        self.root_data_path = self.get_property('root_data_path')
        self.root_data_path_web = self.get_property('root_data_path_web')
        self.root_project_path = self.get_property('root_project_path')
        self.html_template_path = self.html_template_path % self.root_project_path
        self.css_template_path = self.css_template_path % self.root_project_path
        self.file_template_path = self.file_template_path % self.root_project_path

        super().__init__(request, client_address, server)

    def get_template(self, template_name):
        full_template_path = '%s/%s.%s' % (self.html_template_path, template_name, self.TEMPLATE_FILE_EXTENSION)

        with open(full_template_path, 'r') as file:
            # add google analytics
            if template_name == 'body':
                gaaccess_file = '%s/.gaaccess' % self.root_project_path
                gaaccess_content = ''

                if os.path.isfile(gaaccess_file):
                    with open(gaaccess_file, 'r') as ga_file:
                        gaaccess_content = ga_file.read()

                return file.read() % {
                    'CONTENT': '%(CONTENT)s',
                    'GOOGLE_ANALYTICS': gaaccess_content
                }
            else:
                return file.read()

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
    def set_property(name, value):
        SimpleHTTPRequestHandler.properties[name] = value

    @staticmethod
    def get_property(name):
        if name not in SimpleHTTPRequestHandler.properties:
            return None

        return SimpleHTTPRequestHandler.properties[name]

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
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', len(response))
        self.end_headers()
        self.wfile.write(bytes(response, 'utf-8'))

    def respond_file(self, folder, path, content_type='text/plain; charset=utf-8', status=200):
        if path == '' or path is None:
            html_content = self.get_template('404') % ('%s/%s' % (folder, path))
            self.respond_html(html_content, 404)
            return

        file_path = '%s/%s/%s' % (self.file_template_path, folder, path)

        if not os.path.isfile(file_path):
            html_content = self.get_template('404') % ('%s/%s' % (folder, path))
            self.respond_html(html_content, 404)
            return

        # read file content
        file_content = ''
        with open(file_path, 'r') as file:
            file_content = file.read()

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Content-length', len(file_content))
        self.end_headers()
        self.wfile.write(bytes(file_content, 'utf-8'))

    def respond_picture(self, picture_path, path, content_type='image/jpg', status=200):
        if picture_path == '' or picture_path is None:
            html_body = self.get_template('body') % {'CONTENT': self.TEXT_EMPTY_IMAGE}
            self.respond_html(html_body)
            return

        upload_image_path = '%s/%s/%s' % (self.root_data_path, path, picture_path)

        if not os.path.isfile(upload_image_path):
            html_body = self.get_template('body') % {'CONTENT': self.TEXT_IMAGE_WAS_NOT_FOUND % upload_image_path}
            self.respond_html(html_body)
            return

        picture_info = os.stat(upload_image_path)
        img_size = picture_info.st_size

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Content-length', img_size)
        self.end_headers()

        f = open(upload_image_path, 'rb')
        self.wfile.write(f.read())
        f.close()

    def respond_picture_raw(self, picture_path, content_type='auto', status=200):
        if picture_path == '' or picture_path is None:
            html_body = self.get_template('body') % {'CONTENT': self.TEXT_EMPTY_IMAGE}
            self.respond_html(html_body)
            return

        full_image_path = '%s/%s' % (self.file_template_path, picture_path)

        if content_type == 'auto':
            mime = magic.Magic(mime=True)
            content_type = mime.from_file(full_image_path)

        if not os.path.isfile(full_image_path):
            html_body = self.get_template('body') % {'CONTENT': self.TEXT_IMAGE_WAS_NOT_FOUND % full_image_path}
            self.respond_html(html_body)
            return

        picture_info = os.stat(full_image_path)
        img_size = picture_info.st_size

        self.send_response(status)
        self.send_header('Content-type', content_type)
        self.send_header('Content-length', img_size)
        self.end_headers()

        f = open(full_image_path, 'rb')
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

        predict_file_raw = form['predict-file-raw'].value
        predict_file_name = form['predict-file-name'].value

        if predict_file_raw == '' or predict_file_name == '':
            return {
                'error': True,
                'message': 'No file was uploaded.'
            }

        # check file
        output = re.search('^data:image/([a-z]+);base64,', predict_file_raw, flags=re.IGNORECASE)
        if output is None:
            return {
                'error': True,
                'message': 'Unknown file format from file "%s".' % predict_file_name
            }

        # remove header
        predict_file_raw = re.sub('^data:image/([a-z]+);base64,', '', predict_file_raw)
        predict_file_raw = predict_file_raw.replace(' ', '+')
        predict_file_raw = base64.b64decode(predict_file_raw)

        # save file to upload folder
        upload_path = '%s/%s/%s' % (self.root_data_path, 'upload', predict_file_name)
        upload_path_web = '%s%s/%s' % (self.root_data_path_web, 'upload', predict_file_name)
        open(upload_path, 'wb').write(predict_file_raw)

        # check mime type of given image
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(upload_path)

        if mime_type not in self.ALLOWED_MIME_TYPES:
            return {
                'error': True,
                'message': 'The mime type "%s" of uploaded file "%s" is not allowed.' % (
                    mime_type,
                    predict_file_name
                )
            }

        return {
            'upload_path': upload_path,
            'upload_path_web': upload_path_web,
            'mime_type': mime_type,
            'error': False,
            'message': None
        }

    def get_empty_model_data(self):
        model_name = 'NONE'
        model_size = '0 Bytes'
        classes = 0
        learning_epochs = 0
        model_date = 'NONE'
        version = '0.00'

        return {
            'model_name': model_name,
            'model_size': model_size,
            'model_classes': classes,
            'model_learning_epochs': learning_epochs,
            'model_date': model_date,
            'model_version': version
        }

    def do_GET_index(self):
        html_content = self.get_template('index')
        html_body = self.get_template('body') % {'CONTENT': html_content}
        self.respond_html(html_body)
        return True

    def do_GET_imprint(self, argument, hook_results):
        html_content = self.get_template('imprint')
        html_body = self.get_template('body') % {'CONTENT': html_content}
        self.respond_html(html_body)
        return True

    def do_GET_file(self, path, argument, hook_results):
        """ route GET /default """

        # some configs and type tables
        image_types = ['image/png', 'image/x-icon']
        text_types = ['text/plain', 'text/xml']

        # create full file path
        full_file_path = '%s/%s' % (self.file_template_path, '%s/%s' % (path, argument))

        # file was not found -> 404
        if not os.path.isfile(full_file_path):
            return False

        # get mime type
        mime = magic.Magic(mime=True)
        mime_type = mime.from_file(full_file_path)

        # image was found
        if mime_type in image_types:
            self.respond_picture_raw('%s/%s' % (path, argument), mime_type)
            return True

        # text was found
        if mime_type in text_types:
            self.respond_file(path, argument, '%s; charset=utf-8' % mime_type)
            return True

        # unknown file type was found
        print('unknown file type "%s"' % mime_type)
        return False

    def do_GET_favicon(self, argument, hook_results):
        """ route GET /favicon """
        print('favicon')
        return self.do_GET_file('favicon', argument, hook_results)

    def do_GET_css(self, argument, hook_results):
        """ route GET /css """
        self.respond_file('css', argument, 'text/css; charset=utf-8')
        return True

    def do_GET_js(self, argument, hook_results):
        """ route GET /js """
        self.respond_file('js', argument, 'application/javascript; charset=utf-8')
        return True

    def do_GET_tmp(self, argument, hook_results):
        """ route GET /tmp """
        self.respond_picture(argument, 'tmp')
        return True

    def do_GET_prediction(self, argument, hook_results):
        """ route GET /prediction """
        model_data = None

        if 'GET_prediction' in hook_results:
            model_data = hook_results['GET_prediction']

        if model_data is None:
            model_data = self.get_empty_model_data()

        used_model = self.get_template('used_model') % {
            'MODEL_NAME': model_data['model_name'],
            'MODEL_SIZE': model_data['model_size'],
            'CLASSES': model_data['model_classes'],
            'LEARNING_EPOCHS': model_data['model_learning_epochs'],
            'MODEL_DATE': model_data['model_date'],
            'VERSION': model_data['model_version']
        }

        if argument == 'flower':
            html_form = self.get_template('form') % {'ERROR_MESSAGE': '', 'TEXT_UPLOAD': self.TEXT_UPLOAD}
            html_content = self.get_template('flower') % {
                'PREDICTION_FORM': html_form,
                'USED_MODEL': used_model
            }
            html_body = self.get_template('body') % {'CONTENT': html_content}
            self.respond_html(html_body)
            return True

        if argument == 'food':
            html_content = self.get_template('food') % {
                'USED_MODEL': used_model
            }
            html_body = self.get_template('body') % {'CONTENT': html_content}
            self.respond_html(html_body)
            return True

        return False

    def do_GET_learning_overview(self, argument, hook_results):
        learning_overview_items = [
            'flower_10_1.inceptionv3',
            'flower_10_2.densenet169',
            'flower_10_3.resnet50',
            'flower_10_4.densenet201',
            'flower_10_5.nasnetlarge',
            'flower_10_6.xception',
            'flower_10_7.mobilenetv2'
        ]

        learning_overview_content = ''
        for learning_overview_item in learning_overview_items:
            learning_overview_content += self.get_template('learning_overview_item') % (
                learning_overview_item,
                '%s.%s' % (learning_overview_item, PNG_EXTENSION)
            )

        html_content = self.get_template('learning_overview') % learning_overview_content
        html_body = self.get_template('body') % {'CONTENT': html_content}
        self.respond_html(html_body)

        return True

    def do_GET_upload(self, argument, hook_results):
        """ route GET /upload """
        self.respond_picture(argument, 'upload')
        return True

    def do_GET(self):
        parsed = urlparse(self.path)
        url_path = parsed.path

        # Routes to check
        routes = ['learning-overview', 'tmp', 'prediction', 'upload', 'css', 'js', 'favicon', 'manifest', 'imprint']

        # hook results
        hook_results = {}

        # call index page
        if url_path == '/':
            # call hook
            GET_result = self.call_hook('GET')
            if GET_result is not None:
                print(GET_result)

            # call index page
            self.do_GET_index()
            return

        # ignore /favicon.ico
        if url_path == '/favicon.ico':
            url_path = '/favicon/favicon.ico'

        # Try to find a special route
        for route in routes:
            output = re.search('^/%s(/(.+)?)?$' % route, url_path, flags=re.IGNORECASE)
            if output is not None:
                route_function_name = 'do_GET_%s' % route.replace('-', '_')
                hook_name = 'GET_%s' % route.replace('-', '_')
                argument = output.group(2)

                if not hasattr(self, route_function_name):
                    raise AssertionError('Please add method "SimpleHTTPRequestHandler.%s()"' % route_function_name)

                # call hook
                if route == 'prediction':
                    GET_result = self.call_hook(hook_name, argument)
                else:
                    GET_result = self.call_hook(hook_name)

                # add hook result
                if GET_result is not None:
                    hook_results[hook_name] = GET_result

                # Call special GET function
                success = getattr(self, route_function_name)(argument, hook_results)
                if not success:
                    self.respond_html('', 404)
                    return

                return

        # Unknown page
        self.respond_html('', 404)

    def do_POST_prediction(self, argument, hook_results):
        upload_data = self.write_upload_file()
        model_data = None

        if 'POST_prediction' in hook_results:
            model_data = hook_results['POST_prediction']

        if model_data is None:
            model_data = self.get_empty_model_data()

        used_model = self.get_template('used_model') % {
            'MODEL_NAME': model_data['model_name'],
            'MODEL_SIZE': model_data['model_size'],
            'CLASSES': model_data['model_classes'],
            'LEARNING_EPOCHS': model_data['model_learning_epochs'],
            'MODEL_DATE': model_data['model_date'],
            'VERSION': model_data['model_version']
        }

        if upload_data['error']:
            html_error = self.get_template('error') % upload_data['message']
            html_form = self.get_template('form') % {'ERROR_MESSAGE': html_error, 'TEXT_UPLOAD': self.TEXT_UPLOAD}
            html_content = self.get_template('flower') % {
                'PREDICTION_FORM': html_form,
                'USED_MODEL': used_model
            }
            html_body = self.get_template('body') % {'CONTENT': html_content}
        else:
            # call post hook
            hook_name = 'POST_%s_%s' % ('prediction', 'get_model')
            evaluation_data = self.call_hook(hook_name, argument, upload_data)

            # get data from post hook
            evaluated_file_web_size = get_formatted_file_size(evaluation_data['evaluated_file'])
            evaluated_file_web = evaluation_data['evaluated_file_web']
            graph_file_web = evaluation_data['graph_file_web']
            prediction_class = evaluation_data['prediction_class']
            prediction_accuracy = evaluation_data['prediction_accuracy']
            upload_form = self.get_template('form') % {'ERROR_MESSAGE': '', 'TEXT_UPLOAD': self.TEXT_UPLOAD}
            prediction_time = evaluation_data['prediction_time']
            prediction_overview_array = evaluation_data['prediction_overview_array']
            prediction_overview_html = '<tr><th>Class</th><th>Prediction</th></tr>'

            i = 0
            while i < len(prediction_overview_array):
                prediction_overview_html += '<tr><td><b>%s</b></td><td>%.2f %%</td></tr>' % (
                    prediction_overview_array[i]['class_name'],
                    prediction_overview_array[i]['predicted_value'] * 100
                )
                i += 1

            html_content = self.get_template('prediction') % {
                'EVALUATED_FILE_WEB_SIZE': evaluated_file_web_size,
                'EVALUATED_FILE_WEB': evaluated_file_web,
                'PREDICTION_CLASS': prediction_class,
                'PREDICTION_ACCURACY': '%.2f' % prediction_accuracy,
                'GRAPH_FILE_WEB': graph_file_web,
                'PREDICTION_OVERVIEW': prediction_overview_html,
                'UPLOAD_FORM': upload_form,
                'PREDICTION_TIME': prediction_time,
                'USED_MODEL': used_model
            }
            html_body = self.get_template('body') % {'CONTENT': html_content}

        self.respond_html(html_body)
        return True

    def do_POST(self):
        argument = 'flower'
        hook_results = {}
        route_function_name = 'do_POST_%s' % 'prediction'
        hook_name = 'POST_%s' % 'prediction'

        if not hasattr(self, route_function_name):
            raise AssertionError('Please add method "SimpleHTTPRequestHandler.%s()"' % route_function_name)

        # call hook
        POST_result = self.call_hook(hook_name, argument)
        if POST_result is not None:
            hook_results[hook_name] = POST_result

        # Call special GET function
        success = getattr(self, route_function_name)(argument, hook_results)
        if not success:
            self.respond_html('', 404)
            return
