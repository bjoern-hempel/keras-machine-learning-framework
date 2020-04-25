# Machine Learning Keras Suite
#
# A Python helper file: Provides the logger class.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   12.04.2020
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


class LoggerClass(object):
    """
    LoggerClass
    """
    def __init__(self, log_file=None):
        command_line_input = '(base) Users> '
        command_line_input += ' '.join([str(i) for i in sys.argv])

        self.terminal = sys.stdout

        if log_file is not None:
            self.log = open(log_file, 'w')
            self.log.write(command_line_input + '\n')
        else:
            self.log = None

    def write(self, message):
        self.terminal.write(message)

        if self.log is not None:
            self.log.write(message)

    def flush(self):
        pass

    def isatty(self):
        return True

    def fileno(self):
        return 0
