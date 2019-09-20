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
from mlks.info.main import Info
from mlks.prepare.main import Prepare
from mlks.train.main import Train
from mlks.test.mnist.main import Mnist
from mlks.test.simple_perceptron.main import SimplePerceptron
from mlks.test.xor_perceptron.main import XorPerceptron
from mlks.test.nine_points.main import NinePoints


class GeneralConfig(object):
    """Config class"""

    def __init__(self):
        self.verbose = False


class MachineLearningConfig(object):
    """Machine learning config class"""

    def __init__(self):
        self.activation_function = 'tanh'  # ['tanh', 'sigmoid']
        self.loss_function = 'mean_squared_error'
        self.optimizer = 'adam'
        self.metrics = 'accuracy'
        self.epochs = 100


# Make pass decorator for class Config
pass_general_config = click.make_pass_decorator(GeneralConfig, ensure=True)
pass_machine_learning_config = click.make_pass_decorator(MachineLearningConfig, ensure=True)


def option_callback(ctx, param, value):
    def verbose(ctx_inner, value_inner):
        config = ctx_inner.ensure_object(GeneralConfig)
        if value_inner:
            config.verbose = value_inner
        return value_inner

    return verbose(ctx, value)


verbose_option = [
    click.option('--verbose', '-v', expose_value=False, is_flag=True, help='Switch the script to verbose mode.',
                 callback=option_callback)
]


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func

    return _add_options


@click.group()
@add_options(verbose_option)
def cli():
    """This scripts prepares, trains and validates an image classifier."""

    pass


@cli.command()
@add_options(verbose_option)
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
@add_options(verbose_option)
@pass_machine_learning_config
@pass_general_config
def train(general_config, machine_learning_config):
    """This subcommand trains a classifier."""

    train_class = Train(general_config)
    train_class.do()


@cli.group()
@add_options(verbose_option)
@pass_machine_learning_config
@pass_general_config
def test(general_config, machine_learning_config):
    """This subcommand contains some test examples."""
    pass


@test.command()
@add_options(verbose_option)
@pass_machine_learning_config
@pass_general_config
def simple_perceptron(general_config, machine_learning_config):
    """This subcommand from test trains a simple perceptron."""

    test_class = SimplePerceptron(general_config)
    test_class.do()


@test.command()
@add_options(verbose_option)
@pass_machine_learning_config
@pass_general_config
def xor_perceptron(general_config, machine_learning_config):
    """This subcommand from test trains a xor perceptron."""

    test_class = XorPerceptron(general_config)
    test_class.do()


@test.command()
@add_options(verbose_option)
@pass_machine_learning_config
@pass_general_config
def nine_points(general_config, machine_learning_config):
    """This subcommand from test trains a nine point example."""

    test_class = NinePoints(general_config, machine_learning_config)
    test_class.do()


@test.command()
@add_options(verbose_option)
@pass_machine_learning_config
@pass_general_config
def mnist(general_config, machine_learning_config):
    """This subcommand from test trains a mnist database."""

    test_class = Mnist(general_config)
    test_class.do()


@cli.command()
def info():
    """This subcommand shows some infos."""

    Info.print()
