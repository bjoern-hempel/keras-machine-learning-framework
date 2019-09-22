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
from mlks.helper.config import Config
from mlks.helper.config import general_config_writer
from mlks.helper.config import machine_learning_config_writer
from mlks.helper.config import transfer_learning_config_writer

# Make pass decorator for class Config
pass_config = click.make_pass_decorator(Config, ensure=True)

config_translator: Dict[str, str] = {
    # general config
    'verbose': 'general_config_writer',
    'debug': 'general_config_writer',

    # machine learning config
    'epochs': 'machine_learning_config_writer',
    'learning_rate': 'machine_learning_config_writer',
    'activation_function': 'machine_learning_config_writer',
    'loss_function': 'machine_learning_config_writer',
    'optimizer': 'machine_learning_config_writer',
    'metrics': 'machine_learning_config_writer',

    # transfer learning config
    'transfer_learning_model': 'transfer_learning_config_writer',
    'number_trainable_layers': 'transfer_learning_config_writer'
}


def option_callback(ctx, param, value):
    """This function stores the passed values in the configuration classes before returning them."""

    return globals()[config_translator[param.name]](ctx, param, value)


# Configure the universal parameters here
option_verbose = click.option('--verbose', '-v',
                              expose_value=False,
                              is_flag=True,
                              help='Switches the script to verbose mode.',
                              callback=option_callback)
option_debug = click.option('--debug', '-d',
                            expose_value=False,
                            is_flag=True,
                            help='Switches the script to debug mode.',
                            callback=option_callback)

# Configure the machine learning parameters here
option_epochs = click.option('--epochs', '-e',
                             expose_value=False,
                             is_flag=False,
                             help='Sets the number of epochs.',
                             callback=option_callback,
                             default=10,
                             type=int)
option_learning_rate = click.option('--learning-rate', '-l',
                                    expose_value=False,
                                    is_flag=False,
                                    help='Sets the learning rate.',
                                    callback=option_callback,
                                    default=0.001,
                                    type=float)
option_activation_function = click.option('--activation-function', '-a',
                                          expose_value=False,
                                          is_flag=False,
                                          help='Sets the activation function.',
                                          callback=option_callback,
                                          default='tanh',  # ['tanh', 'sigmoid']
                                          type=str)
option_loss_function = click.option('--loss-function',
                                    expose_value=False,
                                    is_flag=False,
                                    help='Sets the loss function.',
                                    callback=option_callback,
                                    default='mean_squared_error',
                                    type=str)
option_optimizer = click.option('--optimizer', '-o',
                                expose_value=False,
                                is_flag=False,
                                help='Sets the optimizer.',
                                callback=option_callback,
                                default='adam',
                                type=str)
option_metrics = click.option('--metrics',
                              expose_value=False,
                              is_flag=False,
                              help='Sets the metrics.',
                              callback=option_callback,
                              default='accuracy',
                              type=str)

# Configure the transfer learning parameters here
option_transfer_learning_model = click.option('--transfer-learning-model', '-m',
                                              expose_value=False,
                                              is_flag=False,
                                              help='Sets the transfer learning model.',
                                              callback=option_callback,
                                              default='Resnet52',
                                              type=str)
option_number_trainable_layers = click.option('--number-trainable-layers',
                                              expose_value=False,
                                              is_flag=False,
                                              help='Sets the number trainable layers.',
                                              callback=option_callback,
                                              default=3,
                                              type=int)

# Configure some option sets
option_set_general = [option_verbose, option_debug]
option_set_machine_learning = [option_epochs, option_learning_rate, option_activation_function, option_loss_function,
                               option_optimizer, option_metrics]
option_set_transfer_learning = [option_transfer_learning_model, option_number_trainable_layers]


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
@pass_config
def prepare(config, string, repeat, out):
    """This subcommand trains a classifier."""

    prepare_class = Prepare(config, string, repeat, out)
    prepare_class.do()


@cli.command()
@add_options(option_set_transfer_learning)
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_config
def train(config):
    """This subcommand trains a classifier."""

    train_class = Train(config)
    train_class.do()


@cli.group()
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_config
def test(config):
    """This subcommand contains some test examples."""

    pass


@test.command()
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_config
def simple_perceptron(config):
    """This subcommand from test trains a simple perceptron."""

    test_class = SimplePerceptron(config)
    test_class.do()


@test.command()
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_config
def xor_perceptron(config):
    """This subcommand from test trains a xor perceptron."""

    test_class = XorPerceptron(config)
    test_class.do()


@test.command()
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_config
def nine_points(config):
    """This subcommand from test trains a nine point example."""

    test_class = NinePoints(config)
    test_class.do()


@test.command()
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_config
def mnist(config):
    """This subcommand from test trains a mnist database."""

    test_class = Mnist(config)
    test_class.do()


@cli.command()
@add_options(option_verbose)
@pass_config
def info(config):
    """This subcommand shows some infos."""

    info_class = Info(config)
    info_class.print()
