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

from mlks.commands.info.main import Info as CliInfo
from mlks.commands.image_classifier.prepare.main import Prepare as CliImageClassifierPrepare
from mlks.commands.image_classifier.evaluate.main import Evaluate as CliImageClassifierEvaluate
from mlks.commands.image_classifier.train.main import Train as CliImageClassifierTrain
from mlks.commands.demo.mnist.main import Mnist as CliDemoMnist
from mlks.commands.demo.simple_perceptron.main import SimplePerceptron as CliDemoSimplePerceptron
from mlks.commands.demo.xor_perceptron.main import XorPerceptron as CliDemoXorPerceptron
from mlks.commands.demo.nine_points.train.main import Train as CliDemoNinePointsTrain
from mlks.commands.demo.nine_points.execute.main import Execute as CliDemoNinePointsExecute
from mlks.helper.config import add_options
from mlks.config.parameter import pass_config
from mlks.config.parameter import option_set_general, \
    option_set_machine_learning, \
    option_set_transfer_learning, \
    option_set_train_process, \
    option_set_evaluation_process, \
    option_set_nine_points


@click.group(name='cli')
@add_options(option_set_general)
def cli():
    """This scripts prepares, trains and validates an image classifier."""

    pass


@cli.command(name='prepare')
@add_options(option_set_general)
@click.option('--string', default='World', type=click.STRING, help='This is a string.')
@click.option('--repeat', default=1, type=click.INT, show_default=True, help='This is a integer.')
@click.argument('out', default='-', type=click.File('w'), required=False)
@pass_config
def cli_prepare(config, string, repeat, out):
    """This subcommand trains a classifier."""

    prepare_class = CliImageClassifierPrepare(config, string, repeat, out)
    prepare_class.do()


@cli.command(name='train')
@add_options(option_set_transfer_learning)
@add_options(option_set_machine_learning)
@add_options(option_set_train_process)
@add_options(option_set_general)
@pass_config
def cli_train(config):
    """This subcommand trains a classifier."""

    train_class = CliImageClassifierTrain(config)
    train_class.do()


@cli.command(name='evaluate')
@add_options(option_set_evaluation_process)
@add_options(option_set_general)
@pass_config
def cli_evaluate(config):
    """This subcommand evaluate a classifier."""

    prepare_class = CliImageClassifierEvaluate(config)
    prepare_class.do()


@cli.group(name='demo')
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_config
def cli_demo(config):
    """This subcommand contains some demo examples."""

    pass


@cli_demo.command(name='simple-perceptron')
@add_options(option_set_general)
@pass_config
def cli_demo_simple_perceptron(config):
    """This subcommand from demo trains a simple perceptron."""

    demo_class = CliDemoSimplePerceptron(config)
    demo_class.do()


@cli_demo.command(name='xor-perceptron')
@add_options(option_set_general)
@pass_config
def cli_demo_xor_perceptron(config):
    """This subcommand from demo trains a xor perceptron."""

    demo_class = CliDemoXorPerceptron(config)
    demo_class.do()


@cli_demo.group(name='nine-points')
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_config
def cli_demo_nine_points(config):
    """This subcommand from demo trains or execute a nine point example."""

    pass


@cli_demo_nine_points.command(name='train')
@add_options(option_set_machine_learning)
@add_options(option_set_train_process)
@add_options(option_set_nine_points)
@add_options(option_set_general)
@pass_config
def cli_demo_nine_points_train(config):
    """This subcommand from demo trains a nine point example."""

    demo_class = CliDemoNinePointsTrain(config)
    demo_class.do()


@cli_demo_nine_points.command(name='execute')
@add_options(option_set_machine_learning)
@add_options(option_set_evaluation_process)
@add_options(option_set_nine_points)
@add_options(option_set_general)
@pass_config
def cli_demo_nine_points_execute(config):
    """This subcommand from demo execute a nine point example."""

    demo_class = CliDemoNinePointsExecute(config)
    demo_class.do()


@cli_demo.command(name='mnist')
@add_options(option_set_machine_learning)
@add_options(option_set_general)
@pass_config
def cli_demo_mnist(config):
    """This subcommand from demo trains a mnist database."""

    demo_class = CliDemoMnist(config)
    demo_class.do()


@cli.command(name='info')
@add_options(option_set_general)
@pass_config
def cli_info(config):
    """This subcommand shows some infos."""

    info_class = CliInfo(config)
    info_class.print()
