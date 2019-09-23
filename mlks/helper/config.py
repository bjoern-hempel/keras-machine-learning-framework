# Machine Learning Keras Suite
#
# A Python helper file: config_writer.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   22.09.2019
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
from typing import Dict

# some general variables
debug = False
config_translator: Dict[str, str] = {}


def set_config_translator(ct):
    global config_translator
    config_translator = ct


class Config(object):
    """Config class"""

    def __init__(self):
        if debug:
            click.echo('Config.__init__')

        self.configs = {
            'general': {
                'verbose': False,
                'debug': False
            }
        }

    def set(self, name, value, namespace='general'):
        if namespace not in self.configs:
            self.configs[namespace] = {}

        self.configs[namespace][name] = value

    def get(self, name, namespace='general'):
        if namespace not in self.configs:
            raise AssertionError('Namespace "%s" is not available' % namespace)
            return None

        if name not in self.configs[namespace]:
            return None

        return self.configs[namespace][name]

    def getml(self, name):
        return self.get(name, 'machine_learning')

    def gettl(self, name):
        return self.get(name, 'transfer_learning')


class DefaultChooser(click.Option):
    """A class that can different default options for different commands."""

    def __init__(self, *args, **kwargs):
        # add default_options parameter (allow them) and save the value
        self.default_options = kwargs.pop('default_options', self.get_default_dict(kwargs))

        # check type of argument default_options
        if not isinstance(self.default_options, dict):
            raise AssertionError('Attribute default_options must be a dict object.')

        # call all parent option classes
        super(DefaultChooser, self).__init__(*args, **kwargs)

    @staticmethod
    def get_default_dict(kwargs):
        type_argument = kwargs['type']

        # given type is an integer
        if type_argument == int:
            return {'default': 0}

        # given type is a float
        if type_argument == float:
            return {'default': 0.0}

        # given type is a sring
        if type_argument == str:
            return {'default': ''}

        return {'default': None}

    def get_default(self, ctx):
        command = ctx.info_name

        if command not in self.default_options:
            if 'default' in self.default_options:
                return self.default_options['default']
            else:
                return None

        return self.default_options[command]

    def prompt_for_value(self, ctx):
        default = self.get_default(ctx)

        # only prompt if the default value is None
        if default is None:
            return super(DefaultChooser, self).prompt_for_value(ctx)

        return default


def general_config_writer(ctx, param, value):
    config = ctx.ensure_object(Config)

    if debug:
        click.echo('{object: <30}: {name: <30} {value: <30}'.format(object='Config.general', name=param.name,
                                                                    value=value))
    if value:
        config.set(param.name, value, 'general')
    return value


def machine_learning_config_writer(ctx, param, value):
    config = ctx.ensure_object(Config)

    if debug:
        click.echo('{object: <30}: {name: <30} {value: <30}'.format(object='Config.machine_learning', name=param.name,
                                                                    value=value))
    config.set(param.name, value, 'machine_learning')
    return value


def transfer_learning_config_writer(ctx, param, value):
    config = ctx.ensure_object(Config)

    if debug:
        click.echo('{object: <30}: {name: <30} {value: <30}'.format(object='Config.transfer_learning', name=param.name,
                                                                    value=value))
    config.set(param.name, value, 'transfer_learning')
    return value


def option_callback(ctx, param, value):
    """This function stores the passed values in the configuration classes before returning them."""

    return config_translator[param.name](ctx, param, value)


def add_options(options):
    """The add options function to use as an easy to use decorator: @add_options"""

    def _add_options(func):
        if type(options) is list:
            for option in reversed(options):
                func = option(func)
        elif callable(options):
            func = options(func)
        return func

    return _add_options
