# Machine Learning Keras Suite
#
# A Python helper file: option helper for parameters.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   03.10.2019
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


class OptionDefaultChooserByCommand(click.Option):
    """A class that can different default options for different commands."""
    command_path = {}

    def __init__(self, *args, **kwargs):
        # add default_options parameter (allow them) and save the value
        self.default_options = kwargs.pop('default_options', self.get_default_dict(kwargs))

        # check type of argument default_options
        if not isinstance(self.default_options, dict):
            raise AssertionError('Attribute default_options must be a dict object.')

        # call all parent option classes
        super(OptionDefaultChooserByCommand, self).__init__(*args, **kwargs)

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
        if self.name not in OptionDefaultChooserByCommand.command_path:
            OptionDefaultChooserByCommand.command_path[self.name] = ctx.info_name
        else:
            OptionDefaultChooserByCommand.command_path[self.name] += '_' + ctx.info_name.replace('-', '_')

        command_path = OptionDefaultChooserByCommand.command_path[self.name]
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
