# Machine Learning Keras Suite
#
# A configuration file for parameters and arguments.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   23.09.2019
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

from mlks.helper.config import Config, OptionDefaultChooser, OptionConcat
from mlks.helper.config import general_config_writer, \
    machine_learning_config_writer, \
    transfer_learning_config_writer, \
    nine_points_config_writer
from mlks.helper.config import option_callback
from mlks.helper.config import set_config_translator


# Configure the universal parameters here
option_verbose = click.option(
    '--verbose', '-v',
    expose_value=False,
    is_flag=True,
    help='Switches the script to verbose mode.',
    callback=option_callback
)
option_debug = click.option(
    '--debug', '-d',
    expose_value=False,
    is_flag=True,
    help='Switches the script to debug mode.',
    callback=option_callback
)


# Configure the machine learning parameters here
option_epochs = click.option(
    '--epochs', '-e',
    cls=OptionDefaultChooser,
    default_options={'default': 10, 'demo_nine_points_train': 10000, 'demo_mnist': 20},
    expose_value=False,
    is_flag=False,
    help='Sets the number of epochs.',
    callback=option_callback,
    default=OptionDefaultChooser.get_default,
    type=int
)
option_learning_rate = click.option(
    '--learning-rate', '-l',
    expose_value=False,
    is_flag=False,
    help='Sets the learning rate.',
    callback=option_callback,
    default=0.001,
    type=float
)
option_activation_function = click.option(
    '--activation-function', '-a',
    expose_value=False,
    is_flag=False,
    help='Sets the activation function.',
    callback=option_callback,
    default='tanh',
    type=click.Choice(['tanh', 'sigmoid'])
)
option_loss_function = click.option(
    '--loss-function',
    expose_value=False,
    is_flag=False,
    help='Sets the loss function.',
    callback=option_callback,
    default='mean_squared_error',
    type=click.Choice(['mean_squared_error'])
)
option_optimizer = click.option(
    '--optimizer', '-o',
    expose_value=False,
    is_flag=False,
    help='Sets the optimizer.',
    callback=option_callback,
    default='adam',
    type=click.Choice(['adam'])
)
option_metrics = click.option(
    '--metrics',
    expose_value=False,
    is_flag=False,
    help='Sets the metrics.',
    callback=option_callback,
    default='accuracy',
    type=click.Choice(['accuracy'])
)
option_environment_path = click.option(
    '--environment-path',
    cls=OptionConcat,
    expose_value=False,
    is_flag=False,
    help='Sets the environment path (used for example by --model-file).',
    callback=option_callback,
    default=None,
    type=click.Path(exists=True)
)
option_model_file = click.option(
    '--model-file',
    cls=OptionConcat,
    expose_value=False,
    is_flag=False,
    help='Sets the model file where it should be saved or loaded.',
    callback=option_callback,
    concat='environment_path',
    default=None,
    type=str
)


# Configure the transfer learning parameters here
option_transfer_learning_model = click.option(
    '--transfer-learning-model', '-m',
    expose_value=False,
    is_flag=False,
    help='Sets the transfer learning model.',
    callback=option_callback,
    default='Resnet52',
    type=click.Choice(['Resnet52'])
)
option_number_trainable_layers = click.option(
    '--number-trainable-layers',
    expose_value=False,
    is_flag=False,
    help='Sets the number trainable layers.',
    callback=option_callback,
    default=3,
    type=int
)

# some other parameters here
option_x_0_1 = click.option(
    '--x',
    expose_value=False,
    is_flag=False,
    help='Sets a x value.',
    callback=option_callback,
    default=0.0,
    type=click.FloatRange(min=0, max=1, clamp=False)
)
option_y_0_1 = click.option(
    '--y',
    expose_value=False,
    is_flag=False,
    help='Sets a y value.',
    callback=option_callback,
    default=0.0,
    type=click.FloatRange(min=0, max=1, clamp=False)
)


# Configure some option sets
option_set_general = [
    option_verbose,
    option_debug
]
option_set_machine_learning = [
    option_epochs,
    option_learning_rate,
    option_activation_function,
    option_loss_function,
    option_optimizer,
    option_metrics,
    option_environment_path,
    option_model_file
]
option_set_transfer_learning = [
    option_transfer_learning_model,
    option_number_trainable_layers
]
option_set_nine_points = [
    option_x_0_1,
    option_y_0_1
]


# sets the config translator
set_config_translator({
    # general config
    'verbose': general_config_writer,
    'debug': general_config_writer,

    # machine learning config
    'epochs': machine_learning_config_writer,
    'learning_rate': machine_learning_config_writer,
    'activation_function': machine_learning_config_writer,
    'loss_function': machine_learning_config_writer,
    'optimizer': machine_learning_config_writer,
    'metrics': machine_learning_config_writer,
    'environment_path': machine_learning_config_writer,
    'model_file': machine_learning_config_writer,

    # transfer learning config
    'transfer_learning_model': transfer_learning_config_writer,
    'number_trainable_layers': transfer_learning_config_writer,

    # some other configs
    'x': nine_points_config_writer,
    'y': nine_points_config_writer
})


# Make pass decorator for class Config
pass_config = click.make_pass_decorator(Config, ensure=True)
