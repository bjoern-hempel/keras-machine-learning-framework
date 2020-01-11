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

from mlks.helper.config import Config
from mlks.helper.config import general_config_writer, \
    machine_learning_config_writer, \
    transfer_learning_config_writer, \
    data_config_writer, \
    nine_points_config_writer, \
    http_config_writer
from mlks.helper.option import OptionHelper
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
option_yes = click.option(
    '--yes', '-y',
    expose_value=False,
    is_flag=True,
    help='Skip demands.',
    callback=option_callback,
    default=False
)
option_service = click.option(
    '--service',
    expose_value=False,
    is_flag=True,
    help='Execute the given command as service.',
    callback=option_callback,
    default=False
)
option_http = click.option(
    '--http',
    expose_value=False,
    is_flag=True,
    help='Execute the given command as http service.',
    callback=option_callback,
    default=False
)
option_render_device = click.option(
    '--render-device', '-r',
    expose_value=False,
    is_flag=False,
    help='Specifies the device on which the calculation is to be performed.',
    callback=option_callback,
    required=False,
    show_default=True,
    default='AUTO',
    type=click.Choice(['AUTO', 'CPU', 'CPU1', 'CPU2', 'CPU3', 'GPU', 'GPU1', 'GPU2', 'GPU3', 'PARALLEL'])
)


# Configure the http parameters here
option_bind_ip = click.option(
    '--bind-ip',
    expose_value=False,
    is_flag=False,
    help='Sets the bind ip.',
    default='0.0.0.0',
    required=False,
    show_default=True,
    type=str,
    callback=option_callback
)
option_port = click.option(
    '--port',
    expose_value=False,
    is_flag=False,
    help='Sets the non ssl port.',
    default=8080,
    required=False,
    show_default=True,
    type=int,
    callback=option_callback
)
option_port_ssl = click.option(
    '--port-ssl',
    expose_value=False,
    is_flag=False,
    help='Sets the ssl port.',
    default=4443,
    required=False,
    show_default=True,
    type=int,
    callback=option_callback
)


# Configure the machine learning parameters here
option_epochs = click.option(
    '--epochs', '-e',
    cls=OptionHelper,
    default_options={'default': 10, 'demo_nine_points_train': 10000, 'demo_mnist': 20, 'train': 20},
    option_type='default_by_command',
    expose_value=False,
    is_flag=False,
    help='Sets the number of epochs.',
    callback=option_callback,
    default=OptionHelper.get_default,
    type=int
)
option_batch_size = click.option(
    '--batch-size',
    cls=OptionHelper,
    default_options={'default': 16},
    option_type='default_by_command',
    expose_value=False,
    is_flag=False,
    help='Sets the batch size.',
    callback=option_callback,
    default=OptionHelper.get_default,
    type=int
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
    default='categorical_crossentropy',
    type=click.Choice(['mean_squared_error', 'categorical_crossentropy'])
)
option_optimizer = click.option(
    '--optimizer', '-o',
    expose_value=False,
    is_flag=False,
    help='Sets the optimizer.',
    callback=option_callback,
    default='sgd',
    type=click.Choice(['adam', 'sgd'])
)
option_learning_rate = click.option(
    '--learning-rate', '-l',
    expose_value=False,
    is_flag=False,
    help='Sets the learning rate value.',
    callback=option_callback,
    default=0.001,
    type=float
)
option_learning_rate_drop = click.option(
    '--learning-rate-drop',
    expose_value=False,
    is_flag=False,
    help='Sets the learning rate drop value.',
    callback=option_callback,
    default=0.5,
    type=click.FloatRange(min=0, max=1, clamp=False)
)
option_learning_rate_epochs_drop = click.option(
    '--learning-rate-epochs-drop',
    expose_value=False,
    is_flag=False,
    help='Sets the number of epochs after which the learning rate should decrease.',
    callback=option_callback,
    default=7,
    type=int
)
option_momentum = click.option(
    '--momentum',
    expose_value=False,
    is_flag=False,
    help='Sets the momentum value.',
    callback=option_callback,
    default=0.9,
    type=click.FloatRange(min=0, max=1, clamp=False)
)
option_decay = click.option(
    '--decay',
    expose_value=False,
    is_flag=False,
    help='Sets the decay value.',
    callback=option_callback,
    default=0.0,
    type=click.FloatRange(min=0, max=1, clamp=False)
)
option_nesterov = click.option(
    '--nesterov',
    expose_value=False,
    is_flag=True,
    help='Switches on the nesterov mode.',
    callback=option_callback,
    default=True
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
option_validation_split = click.option(
    '--validation-split',
    expose_value=False,
    is_flag=False,
    help='Sets the validation split.',
    callback=option_callback,
    default=0.2,
    type=click.FloatRange(min=0, max=1, clamp=False)
)

# Configure the transfer learning parameters here
option_transfer_learning_model = click.option(
    '--transfer-learning-model', '-m',
    cls=OptionHelper,
    option_type='default_by_parameter',
    default_options='InceptionV3',
    expose_value=False,
    is_flag=False,
    help='Sets the transfer learning model.',
    callback=option_callback,
    default=OptionHelper.get_default,
    type=click.Choice([
        'DenseNet121',
        'DenseNet169',
        'DenseNet201',
        'InceptionResNetV2',
        'InceptionV3',
        'NASNet',
        'NASNetLarge',
        'NASNetMobile',
        'MobileNet',
        'MobileNetV2',
        'ResNet50',
        'VGG19',
        'Xception'
    ])
)
option_number_trainable_layers = click.option(
    '--number-trainable-layers',
    cls=OptionHelper,
    option_type='default_by_parameter',
    dependent='transfer_learning_model',
    default_options={'default': 10, 'InceptionV3': 11, 'ResNet50': 5, 'VGG19': 5, 'InceptionResNetV2': 5},
    expose_value=False,
    is_flag=False,
    help='Sets the number trainable layers.',
    callback=option_callback,
    default=OptionHelper.get_default,
    type=int
)
option_input_dimension = click.option(
    '--input-dimension',
    cls=OptionHelper,
    option_type='default_by_parameter',
    dependent='transfer_learning_model',
    default_options={'default': 224, 'InceptionV3': 299, 'NASNetLarge': 331},
    expose_value=False,
    is_flag=False,
    help='Sets the size of input dimension.',
    callback=option_callback,
    default=OptionHelper.get_default,
    type=int
)
option_dense_size = click.option(
    '--dense-size',
    expose_value=False,
    is_flag=False,
    help='Sets the dense size.',
    callback=option_callback,
    default=512,
    type=int
)
option_dropout = click.option(
    '--dropout',
    expose_value=False,
    is_flag=False,
    help='Sets the dropout value.',
    callback=option_callback,
    default=0.5,
    type=click.FloatRange(min=0, max=1, clamp=False)
)
option_weights = click.option(
    '--weights',
    expose_value=False,
    is_flag=False,
    help='Sets the database with which the weights are to be set (pre-trained transfer learning model).',
    callback=option_callback,
    default='imagenet',
    type=click.Choice(['imagenet'])
)
option_continue = click.option(
    '--continue',
    expose_value=False,
    is_flag=True,
    help='Continue learning with given model file.',
    callback=option_callback,
    default=False
)

# Configure the data parameter here
option_environment_path = click.option(
    '--environment-path',
    cls=OptionHelper,
    option_type='concat_parameters',
    expose_value=False,
    is_flag=False,
    help='Sets the environment path (used for example by --model-file, --config-file, --evaluation-path or '
         '--data-path).',
    callback=option_callback,
    default=None,
    type=click.Path(exists=True)
)
option_model_file = click.option(
    '--model-file',
    cls=OptionHelper,
    option_type='concat_parameters',
    expose_value=False,
    is_flag=False,
    help='Sets the model file where it should be saved or loaded.',
    callback=option_callback,
    concat='environment_path',
    default=None,
    required=True,
    type=str
)
option_model_source = click.option(
    '--model-source',
    cls=OptionHelper,
    option_type='concat_parameters',
    expose_value=False,
    is_flag=False,
    help='Sets the source model if you want to continue learning from.',
    callback=option_callback,
    concat='environment_path',
    default=None,
    required=False,
    type=str
)
option_config_file = click.option(
    '--config-file',
    cls=OptionHelper,
    option_type='concat_parameters',
    expose_value=False,
    is_flag=False,
    help='Sets the json config file.',
    callback=option_callback,
    concat='environment_path',
    default=None,
    required=True,
    type=str
)
option_config_file_2 = click.option(
    '--config-file-2',
    cls=OptionHelper,
    option_type='concat_parameters',
    expose_value=False,
    is_flag=False,
    help='Sets the json config file for a second model.',
    callback=option_callback,
    concat='environment_path',
    default=None,
    required=False,
    type=str
)
option_accuracy_file = click.option(
    '--accuracy-file',
    cls=OptionHelper,
    option_type='concat_parameters',
    expose_value=False,
    is_flag=False,
    help='Sets the accuracy image graph file.',
    callback=option_callback,
    concat='environment_path',
    default=None,
    required=True,
    type=str
)
option_log_file = click.option(
    '--log-file',
    cls=OptionHelper,
    option_type='concat_parameters',
    expose_value=False,
    is_flag=False,
    help='Sets the log file.',
    callback=option_callback,
    concat='environment_path',
    default=None,
    required=True,
    type=str
)
option_csv_file = click.option(
    '--csv-file',
    cls=OptionHelper,
    option_type='concat_parameters',
    expose_value=False,
    is_flag=False,
    help='Sets the csv log file.',
    callback=option_callback,
    concat='environment_path',
    default=None,
    required=True,
    type=str
)
option_data_path = click.option(
    '--data-path',
    cls=OptionHelper,
    option_type='concat_parameters',
    expose_value=False,
    is_flag=False,
    help='The data path the model should learn from.',
    callback=option_callback,
    concat='environment_path',
    default=None,
    required=True,
    type=str
)
option_evaluation_path = click.option(
    '--evaluation-path',
    cls=OptionHelper,
    option_type='concat_parameters',
    expose_value=False,
    is_flag=False,
    help='The evaluation file which should be predicted.',
    callback=option_callback,
    concat='environment_path',
    default='_evaluation',
    required=False,
    type=str
)
option_use_train_val = click.option(
    '--use-train-val',
    expose_value=False,
    is_flag=True,
    help='Continue learning with given model file.',
    callback=option_callback,
    default=False
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
    option_debug,
    option_yes,
    option_service,
    option_http,
    option_render_device
]
option_set_http = [
    option_bind_ip,
    option_port,
    option_port_ssl
]
option_set_machine_learning = [
    option_epochs,
    option_batch_size,
    option_activation_function,
    option_loss_function,
    option_optimizer,
    option_learning_rate,
    option_learning_rate_drop,
    option_learning_rate_epochs_drop,
    option_momentum,
    option_decay,
    option_nesterov,
    option_metrics,
    option_validation_split
]
option_set_transfer_learning = [
    option_transfer_learning_model,
    option_number_trainable_layers,
    option_input_dimension,
    option_dense_size,
    option_dropout,
    option_weights,
    option_continue
]
option_set_train_process = [
    option_environment_path,
    option_model_file,
    option_data_path,
    option_model_source,
    option_use_train_val
]
option_set_evaluation_process = [
    option_environment_path,
    option_config_file,
    option_config_file_2,
    option_evaluation_path
]
option_set_graph_process = [
    option_environment_path,
    option_config_file
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
    'yes': general_config_writer,
    'service': general_config_writer,
    'http': general_config_writer,
    'render_device': general_config_writer,

    # http config
    'bind_ip': http_config_writer,
    'port': http_config_writer,
    'port_ssl': http_config_writer,

    # machine learning config
    'epochs': machine_learning_config_writer,
    'batch_size': machine_learning_config_writer,
    'activation_function': machine_learning_config_writer,
    'loss_function': machine_learning_config_writer,
    'optimizer': machine_learning_config_writer,
    'metrics': machine_learning_config_writer,
    'learning_rate': machine_learning_config_writer,
    'learning_rate_drop': machine_learning_config_writer,
    'learning_rate_epochs_drop': machine_learning_config_writer,
    'momentum': machine_learning_config_writer,
    'decay': machine_learning_config_writer,
    'nesterov': machine_learning_config_writer,
    'validation_split': machine_learning_config_writer,

    # transfer learning config
    'transfer_learning_model': transfer_learning_config_writer,
    'number_trainable_layers': transfer_learning_config_writer,
    'input_dimension': transfer_learning_config_writer,
    'dense_size': transfer_learning_config_writer,
    'dropout': transfer_learning_config_writer,
    'weights': transfer_learning_config_writer,
    'continue': transfer_learning_config_writer,

    # data (files and folders)
    'environment_path': data_config_writer,
    'model_file': data_config_writer,
    'config_file': data_config_writer,
    'config_file_2': data_config_writer,
    'data_path': data_config_writer,
    'model_source': data_config_writer,
    'evaluation_path': data_config_writer,
    'use_train_val': data_config_writer,

    # some other configs
    'x': nine_points_config_writer,
    'y': nine_points_config_writer
})


# Make pass decorator for class Config
pass_config = click.make_pass_decorator(Config, ensure=True)
