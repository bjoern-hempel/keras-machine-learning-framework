# Machine Learning Keras Suite
#
# A Python helper file: Provides some dict helper.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   02.11.2019
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

import sys


def count_len_recursive(dict):
    number = 0
    for dict_set in dict:
        number += len(dict[dict_set])
    return number


def get_sort_index_array(dict, reverse=False):
    return sorted(range(len(dict)), key=lambda k: dict[k], reverse=reverse)


def get_best_value(dict):
    best_value = 0
    for accuracy in dict:
        best_value = accuracy if accuracy > best_value else best_value
    return best_value


def get_best_index(dict):
    best_value = 0
    best_index = None
    index = 0
    for accuracy in dict:
        if accuracy > best_value:
            best_index = index
            best_value = accuracy
        index += 1
    return best_index
