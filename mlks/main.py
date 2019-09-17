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
from mlks.test.main import Test


class Config(object):
    """Config class"""

    def __init__(self):
        self.verbose = False


# Make pass decorator for class Config
pass_config = click.make_pass_decorator(Config, ensure=True)


def verbose_option(f):
    """Customized option (verbose): --verbose and -v"""

    def callback(ctx, param, value):
        config = ctx.ensure_object(Config)
        if value:
            config.verbose = value
        return value

    return click.option('-v', '--verbose', expose_value=False, is_flag=True, help='Switch the script to verbose mode.',
                        callback=callback)(f)


def common_options(f):
    """Bundles all options"""
    f = verbose_option(f)
    return f


@click.group()
@common_options
@pass_config
def cli(config):
    """This scripts prepares, trains and validates an image classifier."""
    
    pass


@cli.command()
@common_options
@click.option('--string', default='World', type=click.STRING, help='This is a string.')
@click.option('--repeat', default=1, type=click.INT, show_default=True, help='This is a integer.')
@click.argument('out', default='-', type=click.File('w'), required=False)
@pass_config
def prepare(config, string, repeat, out):
    """This subcommand trains a classifier."""

    prepare_class = Prepare(config, string, repeat, out)
    prepare_class.do()


@cli.command()
@common_options
@pass_config
def train(config):
    """This subcommand trains a classifier."""

    train_class = Train(config)
    train_class.do()


@cli.command()
@common_options
@pass_config
def test(config):
    """This subcommand shows some infos."""

    test_class = Test(config)
    test_class.do()


@cli.command()
def info():
    """This subcommand shows some infos."""

    Info.print()
