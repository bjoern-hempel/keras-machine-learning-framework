# Machine Learning Keras Suite
#
# A flask view class: public files
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   28.09.2020
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

# import classes
from flask_classful import FlaskView, route
from flask import send_from_directory, render_template


class StaticView(FlaskView):
    route_base = '/'
    route_prefix = '/'

    excluded_methods = ['set_static_path']

    static_path = None

    @staticmethod
    def set_static_path(static_path: str):
        StaticView.static_path = static_path

    @route('/js/<path>', methods=['GET'])
    def send_js(self, path):
        return send_from_directory('%s/%s' % (self.static_path, 'js'), path)

    @route('/css/<path>', methods=['GET'])
    def send_css(self, path):
        return send_from_directory('%s/%s' % (self.static_path, 'css'), path)

    @route('/img/<path>', methods=['GET'])
    def send_img(self, path):
        return send_from_directory('%s/%s' % (self.static_path, 'img'), path)

    @route('/favicon.ico', methods=['GET'])
    def send_favicon_ico(self):
        return send_from_directory(self.static_path, 'favicon.ico')

    @route('/', methods=['GET'])
    def send_index_html(self):
        return_data = render_template('post_image.html', title='Post an image.', text='Please post an image. :)')
        return return_data, 200
