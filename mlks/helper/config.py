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
import json
import os
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

    def set(self, name, value, namespace='general', flip=False, flip_as_array=False):
        if namespace not in self.configs:
            self.configs[namespace] = {}

        if flip:
            if isinstance(value, dict):
                if flip_as_array:
                    array = []
                    for k in value.items():
                        array.append(k[0])
                    value = array
                else:
                    value = dict((v, k) for k, v in value.items())

        self.configs[namespace][name] = value

        if name == 'model_file':
            if value is None:
                self.configs[namespace]['config_file'] = None
            else:
                self.configs[namespace]['config_file'] = os.path.splitext(value)[0] + '.json'

    def get(self, name, namespace='general', force=False):
        if namespace not in self.configs:
            if force:
                self.configs[namespace] = {}
            else:
                raise AssertionError('Namespace "%s" is not available' % namespace)

        if name not in self.configs[namespace]:
            return None

        return self.configs[namespace][name]

    def getml(self, name):
        return self.get(name, 'machine_learning')

    def gettl(self, name):
        return self.get(name, 'transfer_learning')

    def get_data(self, name):
        return self.get(name, 'data')

    def set_environment(self, name, value, flip=False, flip_as_array=False):
        self.set(name, value, 'environment', flip=flip, flip_as_array=flip_as_array)

    def get_environment(self, name):
        return self.get(name, 'environment')

    def set_measurement(self, name, value):
        measurements = self.get_environment('measurement')

        if measurements is None:
            measurements = {}

        measurements[name] = value

        self.set_environment('measurement', measurements)

    def set_dict(self, data):
        for config, values in data.items():
            if config in self.configs and isinstance(values, dict):
                # merge config
                for key, value in values.items():
                    if key not in self.configs[config]:
                        self.configs[config][key] = value
            else:
                self.configs[config] = values

    def get_dict(self):
        dictionary = {}

        for config in self.configs:
            dictionary[config] = self.configs[config]

        return dictionary

    def get_json(self):
        return json.dumps(self.get_dict(), sort_keys=True, indent=4, separators=(',', ': '))

    def load_json_from_config_file(self, config_file):
        click.echo(config_file)
        if not os.path.exists(config_file) or not os.path.isfile(config_file):
            raise AssertionError('Model config "%s" does not exist.' % config_file)

        # parse json file
        with open(config_file) as json_file:
            data = json.load(json_file)

        self.load_json(data)

    def load_json(self, data):
        self.set_dict(data)


class OptionDefaultChooser(click.Option):
    """A class that can different default options for different commands."""
    command_path = {}

    def __init__(self, *args, **kwargs):
        # add default_options parameter (allow them) and save the value
        self.default_options = kwargs.pop('default_options', self.get_default_dict(kwargs))

        # check type of argument default_options
        if not isinstance(self.default_options, dict):
            raise AssertionError('Attribute default_options must be a dict object.')

        # call all parent option classes
        super(OptionDefaultChooser, self).__init__(*args, **kwargs)

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
        if self.name not in OptionDefaultChooser.command_path:
            OptionDefaultChooser.command_path[self.name] = ctx.info_name
        else:
            OptionDefaultChooser.command_path[self.name] += '_' + ctx.info_name.replace('-', '_')

        command_path = OptionDefaultChooser.command_path[self.name]
        if command_path not in self.default_options:
            if 'default' in self.default_options:
                return self.default_options['default']
            else:
                return None

        return self.default_options[command_path]


class OptionDefaultChooserByParameter(click.Option):
    """An option class that can defaults according to other parameters."""
    parameters = {}

    def __init__(self, *args, **kwargs):
        self.default_options = kwargs.pop('default_options', None)
        self.dependent = kwargs.pop('dependent', None)

        super(OptionDefaultChooserByParameter, self).__init__(*args, **kwargs)

    def process_value(self, ctx, value):
        if value is not None:
            return_value = self.type_cast_value(ctx, value)

            if self.dependent is None:
                 OptionDefaultChooserByParameter.parameters[self.name] = return_value

            return return_value

    def get_default(self, ctx):
        # no choice given
        if not isinstance(self.default_options, dict) or self.dependent is None:
            OptionDefaultChooserByParameter.parameters[self.name] = self.default_options
            return self.default_options

        if self.dependent not in OptionDefaultChooserByParameter.parameters:
            raise AssertionError('%s was not found' % self.dependent)

        key = OptionDefaultChooserByParameter.parameters[self.dependent]

        if key not in self.default_options:
            if 'default' in self.default_options:
                return self.default_options['default']
            else:
                return None

        return self.default_options[key]


class OptionConcat(click.Option):
    """An option class that can concat given other options."""
    parameters = {}

    def __init__(self, *args, **kwargs):
        self.concat = kwargs.pop('concat', None)
        super(OptionConcat, self).__init__(*args, **kwargs)

    def process_value(self, ctx, value):
        if value is not None:
            return_value = self.type_cast_value(ctx, value)

            if self.concat is None:
                OptionConcat.parameters[self.name] = return_value

            if self.concat in OptionConcat.parameters and OptionConcat.parameters[self.concat] is not None:
                return OptionConcat.parameters[self.concat] + '/' + return_value

            return return_value


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


def data_config_writer(ctx, param, value):
    config = ctx.ensure_object(Config)

    if debug:
        click.echo('{object: <30}: {name: <30} {value: <30}'.format(object='Config.data', name=param.name,
                                                                    value=value))
    config.set(param.name, value, 'data')
    return value


def nine_points_config_writer(ctx, param, value):
    config = ctx.ensure_object(Config)

    if debug:
        click.echo('{object: <30}: {name: <30} {value: <30}'.format(object='Config.nine_points', name=param.name,
                                                                    value=value))
    config.set(param.name, value, 'nine_points')
    return value


def option_callback(ctx, param, value):
    """This function stores the passed values in the configuration classes before returning them."""

    translator = config_translator[param.name]
    return translator(ctx, param, value)


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
