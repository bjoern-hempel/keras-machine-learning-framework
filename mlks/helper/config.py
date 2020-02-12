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
import glob
import re
import sys
from typing import Dict
from mlks.helper.filesystem import add_file_extension

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

    def build_data(self):
        if 'transfer_learning' not in self.configs:
            transfer_learning_model = None
        else:
            transfer_learning_model = self.gettl('transfer_learning_model').lower()

        data_files = [
            'model_file',
            'config_file',
            'best_model_file',
            'accuracy_file',
            'log_file',
            'csv_file'
        ]

        extension_wrapper = {
            'config_file': 'json',
            'model_file': 'h5',
            'best_model_file': 'best.{epoch:02d}-{val_acc:.2f}.h5',
            'accuracy_file': 'png',
            'log_file': 'log',
            'csv_file': 'csv'
        }

        for data_file_main in data_files:
            if data_file_main in self.configs['data']:
                if transfer_learning_model is not None:
                    self.set_data(
                        data_files[0],
                        add_file_extension(self.get_data(data_files[0]), transfer_learning_model, True)
                    )
                data_files.remove(data_file_main)

                for data_file in data_files:
                    self.set_data(
                        data_file,
                        add_file_extension(self.get_data(data_file_main), extension_wrapper[data_file])
                    )

            return None

    def set_data(self, name, value):
        self.set(name, value, 'data')

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

    def rebuild_model_dict(self, config_file=None):
        model_file = self.get_data('model_file')

        # convert model file if needed (from other training system)
        if not os.path.isfile(model_file) and config_file is not None and os.path.isfile(config_file):
            self.set_data('config_file', config_file)
            model_file_tmp = add_file_extension(config_file, 'h5')
            if os.path.isfile(model_file_tmp):
                model_file = model_file_tmp
                self.set_data('config_file', config_file)

        if not os.path.isfile(model_file):
            raise AssertionError('model file "%s" was not found' % model_file)

        model_path = os.path.dirname(model_file)
        model_base = add_file_extension(os.path.basename(model_file), '*', True)
        model_files = []
        model_file_best = None
        model_file_best_val_acc = 0

        # search for all best models
        os.chdir(model_path)
        for file in glob.glob(model_base):
            output = re.search('\.([0-9]{1,})-([0-9]{1,}\.[0-9]{1,})\.', file, flags=re.IGNORECASE)
            if output is not None:
                epoch = int(output.group(1))
                val_acc = float(output.group(2))

                # build current model dict
                model_file_current = {
                    'val_acc': val_acc,
                    'epoch': epoch,
                    'model_file': '%s/%s' % (model_path, file)
                }

                # remember the best model
                if val_acc > model_file_best_val_acc:
                    model_file_best_val_acc = val_acc
                    model_file_best = model_file_current

                model_files.append(model_file_current)

        # set new model dict
        self.set_data('model_files', model_files)
        self.set_data('model_file_best', model_file_best)

    def set_dict(self, data, force=False):
        for config, values in data.items():
            if config in self.configs and isinstance(values, dict):
                # merge config
                for key, value in values.items():
                    if key not in self.configs[config] or force:
                        self.configs[config][key] = value
            else:
                self.configs[config] = values

    def get_dict(self):
        dictionary = {}

        for config in self.configs:
            dictionary[config] = self.configs[config]

        return dictionary

    def get_config(self):
        config_file = self.get_data('config_file')

        if config_file is None:
            return {}

        if not os.path.exists(config_file):
            raise AssertionError('The config json file "%s" does not exist.' % config_file)

        if self.get('verbose'):
            click.echo('Read config file from %s' % config_file)

        with open(config_file) as json_file:
            return json.load(json_file)

    def save_json(self):
        config_file = self.get_data('config_file')
        if config_file is not None:
            if self.get('verbose'):
                click.echo('Write config file to %s' % config_file)
            with open(config_file, 'w') as json_file:
                dict_content = self.get_dict()

                if not self.get('log_verbose'):
                    if 'files' in dict_content['environment']:
                        del dict_content['environment']['files']
                json.dump(dict_content, json_file, sort_keys=True, indent=4, separators=(',', ': '))

    def save_model(self, model):
        model_file = self.get_data('model_file')
        if model_file is not None:
            model.save(model_file)

    def get_json(self, beautified=False):
        if beautified:
            return json.dumps(self.get_dict(), sort_keys=True, indent=4, separators=(',', ': '))

        return json.dumps(self.get_dict(), sort_keys=True)

    def load_json_from_config_file(self, config_file, force=False):
        if not os.path.exists(config_file) or not os.path.isfile(config_file):
            raise AssertionError('Model config "%s" does not exist.' % config_file)

        # parse json file
        with open(config_file) as json_file:
            data = json.load(json_file)

        self.load_data(data, force)

    def load_data(self, data, force=False):
        self.set_dict(data, force)

    def load_json(self, json_string, force=False):
        self.set_dict(json.loads(json_string), force)

    def load_from_other_config(self, config, force=False):
        self.load_json(config.get_json(), force)


def general_config_writer(ctx, param, value):
    config = ctx.ensure_object(Config)

    if debug:
        click.echo('{object: <30}: {name: <30} {value: <30}'.format(object='Config.general', name=param.name,
                                                                    value=value))
    if value:
        config.set(param.name, value, 'general')
    return value


def http_config_writer(ctx, param, value):
    config = ctx.ensure_object(Config)

    if debug:
        click.echo('{object: <30}: {name: <30} {value: <30}'.format(object='Config.http', name=param.name,
                                                                    value=value))
    if value:
        config.set(param.name, value, 'http')
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
