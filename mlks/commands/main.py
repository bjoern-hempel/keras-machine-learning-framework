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
import pprint
import os
import shutil

from mlks.helper.log import disable_warnings
from mlks.helper.hardware import set_render_device
from mlks.helper.logger import LoggerClass


class Command:

    def __init__(self, config, question='Are these configurations correct? Continue?',
            negative='Cancelled by user.', check_empty_folder=False):
        self.config = config

        # check config
        if not self.is_config_correct(self.config, question, negative, check_empty_folder):
            sys.exit()

        # Some configs
        verbose = self.config.get('verbose')

        # set render device
        set_render_device(self.config.get('render_device'), verbose=verbose)

        # disable warnings
        disable_warnings()

        # start timer
        self.start_time = {}
        self.finish_time = {}
        self.start_timer('overall')

    def __del__(self):
        if hasattr(self, 'start_time'):
            self.finish_timer('overall')
            for name in self.start_time:
                self.print_timer(name)

    def start_timer(self, name='default'):
        self.start_time[name] = time.time()
        self.finish_time[name] = 0

        if self.config.get('verbose'):
            print('\n\n-> Start "%s".' % name)

    def finish_timer(self, name='default'):
        if name not in self.start_time:
            raise AssertionError('You have not started the timer "%s" yet.' % name)

        self.finish_time[name] = time.time()

        if self.config.get('verbose'):
            click.echo('<- Finished "{}" ({:.4f}s).'.
                       format(name, self.finish_time[name] - self.start_time[name]))

    def get_timer(self, name='default'):
        if name not in self.start_time:
            raise AssertionError('You have not started the timer "%s" yet.' % name)

        if self.finish_time[name] == 0:
            self.finish_timer(name)

        return self.finish_time[name] - self.start_time[name]

    def print_timer(self, name='default'):
        time_needed = self.get_timer(name)

        click.echo('')
        click.echo('--- time measurement for "{}": {:.4f}s ---'.
                   format(name, time_needed))

    @staticmethod
    def query_yes_no(question, default='yes', next_line=True):
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
            str = question + prompt

            if next_line:
                str += '\n'

            sys.stdout.write(str)
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write('Please respond with "yes" or "no" (or "y" or "n").\n')

    @staticmethod
    def repeat_to_length(string_to_expand, length):
        return (string_to_expand * (int(length / len(string_to_expand)) + 1))[:length]

    @staticmethod
    def delete_all_files_in_given_folder(folder, force=False):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    if force or Command.query_yes_no(
                        'Do you really want to delete the file "%s"' % file_path.replace('\\', '/'),
                        'no',
                        False
                    ):
                        os.unlink(file_path)
                elif os.path.isdir(file_path):
                    if force or Command.query_yes_no(
                        'Do you really want to delte the folder "%s"' % file_path.replace('\\', '/'),
                        'no',
                        False
                    ):
                        shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    @staticmethod
    def get_number_of_files_in_given_folder(folder):
        return len([name for name in os.listdir(folder)])

    @staticmethod
    def show_config(config, register_logger=True, check_empty_folder=True, verbose: bool = False, yes: bool = False):
        """Prints out all configuration settings of given config class."""

        # build data config
        config.build_data()

        if check_empty_folder:
            config.configs['data']['process_folder'] = os.path.dirname(config.configs['data']['model_file'])

            # create folder if it not already exists
            if not os.path.exists(config.configs['data']['process_folder']):
                os.makedirs(config.configs['data']['process_folder'])

            number_of_files = Command.get_number_of_files_in_given_folder(config.configs['data']['process_folder'])

            if number_of_files > 0:
                question = 'The given path "%s" is not empty (%d elements). Do you want to empty the directory and continue?' % (
                    config.configs['data']['process_folder'],
                    number_of_files
                )
                positive = Command.query_yes_no(question, 'no', False)

                if not positive:
                    print('Canceled by user.')
                    sys.exit()

                # delete all files in
                Command.delete_all_files_in_given_folder(config.configs['data']['process_folder'])

            number_of_files = Command.get_number_of_files_in_given_folder(config.configs['data']['process_folder'])

            if number_of_files > 0:
                print('The given path "%s" is not empty (%d elements). Abort.' % (
                    config.configs['data']['process_folder'],
                    number_of_files
                ))
                sys.exit()

        # # Register logger class
        pp = None
        if register_logger:
            logger = LoggerClass(config.get_data('log_file'))
            sys.stdout = logger
            sys.stderr = logger
            pp = pprint.PrettyPrinter(indent=4, stream=logger)

        # skip print config
        if yes and not verbose:
            return pp

        # Print config
        if len(config.configs) > 0:
            click.echo('')

        # Print config
        for namespace in config.configs:
            click.echo(namespace)
            click.echo(Command.repeat_to_length('-', len(namespace)))

            for key in config.configs[namespace]:
                click.echo('{key: <30} {attribute}'.format(key=key+':', attribute=config.configs[namespace][key]))
            click.echo('')
        click.echo('')

        return pp

    def is_config_correct(self, configs,
                          question='Are these configurations correct? Continue?',
                          negative='Cancelled by user.',
                          check_empty_folder=False):
        """Shows all configuration classes and asks if this is correct."""

        # Some configs
        verbose = self.config.get('verbose')
        yes = self.config.get('yes')

        # prints out the given configuration
        self.pp = self.show_config(config=configs, register_logger=True, check_empty_folder=check_empty_folder, verbose=verbose, yes=yes)

        # skip demand
        if self.config.get('yes'):
            return True

        positive = self.query_yes_no(question)

        if not positive:
            if negative is not None:
                click.echo(negative)
            return False

        click.echo('')
        return True
