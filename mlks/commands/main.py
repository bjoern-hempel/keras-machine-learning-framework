# Machine Learning Keras Suite
#
# This is the basic command class from which all command classes inherit.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   21.09.2019
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
import time


class Command:

    def __init__(self):
        self.start_time = {}
        self.finish_time = {}
        pass

    def __del__(self):
        for name in self.start_time:
            self.print_timer(name)

    def start_timer(self, name='default'):
        self.start_time[name] = time.time()
        self.finish_time[name] = 0

    def finish_timer(self, name='default'):
        if name not in self.start_time:
            raise AssertionError('You have not started the timer "%s" yet.' % name)

        self.finish_time[name] = time.time()

    def print_timer(self, name='default'):
        if name not in self.start_time:
            raise AssertionError('You have not started the timer "%s" yet.' % name)

        if self.finish_time[name] == 0:
            self.finish_timer(name)

        click.echo('')
        click.echo('--- time measurement for "{}": {:.4f}s ---'.
                   format(name, self.finish_time[name] - self.start_time[name]))
