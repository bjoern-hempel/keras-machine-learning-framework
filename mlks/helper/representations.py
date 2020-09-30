# Machine Learning Keras Suite
#
# Some api representation functions.
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

import json

from flask import make_response


def output_json(data, code, headers=None):
    content_type = 'application/json'
    dumped = json.dumps(data)

    if headers:
        headers.update({'Content-Type': content_type})
    else:
        headers = {'Content-Type': content_type}

    response = make_response(dumped, code, headers)

    return response


def output_html(data, code, headers=None):
    content_type = 'text/html'

    if headers:
        headers.update({'Content-Type': content_type})
    else:
        headers = {'Content-Type': content_type}

    response = make_response(data, code, headers)

    return response
