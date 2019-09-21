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
import sys


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

    @staticmethod
    def query_yes_no(question, default="yes"):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")

    @staticmethod
    def repeat_to_length(string_to_expand, length):
        return (string_to_expand * (int(length / len(string_to_expand)) + 1))[:length]

    @staticmethod
    def show_config(config):
        """Prints out all configuration settings of given config class."""
        class_name = config.__class__.__name__

        click.echo('')
        click.echo(class_name)
        click.echo(Command.repeat_to_length('-', len(class_name)))

        attributes = vars(config)

        for key in attributes:
            key_name = key + ':'
            click.echo('{key: <25} {attribute}'.format(key=key_name, attribute=attributes[key]))

        click.echo('')

    def is_config_correct(self, configs,
                          question='Are these configurations correct? Continue?',
                          negative='Cancelled by user.'):
        """Shows all configuration classes and asks if this is correct."""

        if isinstance(configs, list):
            for config in configs:
                self.show_config(config)
        elif isinstance(configs, object):
            self.show_config(configs)
        else:
            raise AssertionError('Unsupported config parameter.')

        positive = self.query_yes_no(question)

        if not positive:
            if negative is not None:
                click.echo(negative)
            return False

        click.echo('')
        return True
