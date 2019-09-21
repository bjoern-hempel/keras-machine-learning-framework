# Machine Learning Keras Suite
#
# A Python module that trains and evaluate an image classifier.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   15.09.2019
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
from mlks.commands.info.main import Info
from mlks.commands.prepare.main import Prepare
from mlks.commands.train.main import Train
from mlks.commands.test.mnist.main import Mnist
from mlks.commands.test.simple_perceptron.main import SimplePerceptron
from mlks.commands.test.xor_perceptron.main import XorPerceptron
from mlks.commands.test.nine_points.main import NinePoints


class GeneralConfig(object):
    """Config class"""

    def __init__(self):
        self.verbose = False
        self.test = False


class MachineLearningConfig(object):
    """Machine learning config class"""

    def __init__(self):
        self.activation_function = 'tanh'  # ['tanh', 'sigmoid']
        self.loss_function = 'mean_squared_error'
        self.optimizer = 'adam'
        self.metrics = 'accuracy'
        self.epochs = 100
        self.learning_rate = 0.001


class TransferLearningConfig(MachineLearningConfig):
    """Transfer learning config class"""

    def __init__(self):
        super().__init__()

        self.transfer_learning_model = 'Resnet50'


# Make pass decorator for class Config
pass_general_config = click.make_pass_decorator(GeneralConfig, ensure=True)
pass_machine_learning_config = click.make_pass_decorator(MachineLearningConfig, ensure=True)
pass_transfer_learning_config = click.make_pass_decorator(TransferLearningConfig, ensure=True)


def general_config_writer(ctx, value, ensure_object=True):
    config = ctx.ensure_object(GeneralConfig) if ensure_object else GeneralConfig
    if value:
        config.verbose = value
    return value


def machine_learning_config_writer(ctx, value, ensure_object=True):
    config = ctx.ensure_object(MachineLearningConfig) if ensure_object else MachineLearningConfig
    if value:
        config.epochs = value
    return value


def transfer_learning_config_writer(ctx, value, ensure_object=True):
    config = ctx.ensure_object(TransferLearningConfig) if ensure_object else TransferLearningConfig
    if value:
        config.epochs = value
    return value


config_translator: Dict[str, str] = {
    # general config
    'verbose': 'general_config_writer',
    'test': 'general_config_writer',

    # machine learning config (then inherit writers must be the last!!! because of the ctx.ensure_object call)
    'epochs': ['machine_learning_config_writer', 'transfer_learning_config_writer'],
    'learning_rate': ['machine_learning_config_writer', 'transfer_learning_config_writer'],
    'transfer_learning_model': 'transfer_learning_config_writer'
}


def option_callback(ctx, param, value):
    """This function stores the passed values in the configuration classes before returning them."""

    translators = config_translator[param.name]

    if isinstance(translators, list):
        translators_copy = translators.copy()
        translator = translators_copy.pop(0)

        for translator_copy in translators_copy:
            globals()[translator_copy](ctx, value, False)
    else:
        translator = translators

    return globals()[translator](ctx, value)


# Configure the universal parameters here
option_verbose = click.option('--verbose', '-v', expose_value=False, is_flag=True,
                              help='Switch the script to verbose mode.',
                              callback=option_callback)
option_test = click.option('--test', '-t', expose_value=False, is_flag=True,
                           help='Switch the script to test mode.',
                           callback=option_callback)
option_epochs = click.option('--epochs', '-e', expose_value=False, is_flag=False,
                             help='Set the number of epochs.',
                             callback=option_callback, type=int)
option_learning_rate = click.option('--learning-rate', '-l', expose_value=False, is_flag=False,
                                    help='Set the learning rate.',
                                    callback=option_callback, type=float)
option_transfer_learning_model = click.option('--transfer-learning-model', '-m', expose_value=False, is_flag=False,
                                              help='Sets the transfer learning model.',
                                              callback=option_callback, type=str)

# Configure some option sets (the inherited options should be the last!!! because of the ctx.ensure_object call)
option_set_general = [option_verbose, option_test]
option_set_machine_learning = [option_epochs, option_learning_rate]
option_set_transfer_learning = option_set_machine_learning + [option_transfer_learning_model]


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


@click.group()
@add_options(option_set_general)
def cli():
    """This scripts prepares, trains and validates an image classifier."""

    pass


@cli.command()
@add_options(option_set_general)
@click.option('--string', default='World', type=click.STRING, help='This is a string.')
@click.option('--repeat', default=1, type=click.INT, show_default=True, help='This is a integer.')
@click.argument('out', default='-', type=click.File('w'), required=False)
@pass_machine_learning_config
@pass_general_config
def prepare(general_config, machine_learning_config, string, repeat, out):
    """This subcommand trains a classifier."""

    prepare_class = Prepare(general_config, string, repeat, out)
    prepare_class.do()


@cli.command()
@add_options(option_set_transfer_learning)
@add_options(option_set_general)
@pass_transfer_learning_config
@pass_general_config
def train(general_config, transfer_learning_model):
    """This subcommand trains a classifier."""

    train_class = Train(general_config, transfer_learning_model)
    train_class.do()


@cli.group()
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_machine_learning_config
@pass_general_config
def test(general_config, machine_learning_config):
    """This subcommand contains some test examples."""
    pass


@test.command()
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_machine_learning_config
@pass_general_config
def simple_perceptron(general_config, machine_learning_config):
    """This subcommand from test trains a simple perceptron."""

    test_class = SimplePerceptron(general_config, machine_learning_config)
    test_class.do()


@test.command()
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_machine_learning_config
@pass_general_config
def xor_perceptron(general_config, machine_learning_config):
    """This subcommand from test trains a xor perceptron."""

    test_class = XorPerceptron(general_config, machine_learning_config)
    test_class.do()


@test.command()
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_machine_learning_config
@pass_general_config
def nine_points(general_config, machine_learning_config):
    """This subcommand from test trains a nine point example."""

    test_class = NinePoints(general_config, machine_learning_config)
    test_class.do()


@test.command()
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_machine_learning_config
@pass_general_config
def mnist(general_config, machine_learning_config):
    """This subcommand from test trains a mnist database."""

    test_class = Mnist(general_config, machine_learning_config)
    test_class.do()


@cli.command()
@add_options(option_verbose)
@pass_general_config
def info(general_config):
    """This subcommand shows some infos."""

    info_class = Info(general_config)
    info_class.print()
