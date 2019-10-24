# Machine Learning Keras Suite
#
# A Python helper file: Provides some hardware function helper.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   24.10.2019
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

import os
import click
import tensorflow as tf
from tensorflow.python.client import device_lib


def get_hardware_dict():

    # disable the standard logging outputs
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

    # disable deprecated warnings
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    # get all physical render devices
    number_of_gpus = 0
    number_of_cpus = 0
    devices = {}

    hardware_dict = {}

    # count the gpus
    for x in device_lib.list_local_devices():
        if x.device_type == 'GPU':
            config = {
                'id': "%s" % number_of_gpus,
                'name': x.name
            }
            number_of_gpus += 1
            devices['%s%d' % (x.device_type, number_of_gpus)] = config
            if number_of_gpus == 1:
                devices['%s' % x.device_type] = config
        else:
            config = {
                'id': "",
                'name': x.name
            }
            number_of_cpus += 1
            devices['%s%d' % (x.device_type, number_of_cpus)] = config
            if number_of_cpus == 1:
                devices['%s' % x.device_type] = config

    hardware_dict['number_of_gpus'] = number_of_gpus
    hardware_dict['number_of_cpus'] = number_of_cpus
    hardware_dict['devices'] = devices

    return hardware_dict


def get_hardware_dict_2():
    return {
        'number_of_gpus': 2,
        'number_of_cpus': 1,
        'devices': {
            'CPU': {'name': 'CPU', 'id': ''},
            'CPU1': {'name': 'CPU', 'id': ''},
            'GPU': {'name': 'CPU', 'id': '0'},
            'GPU1': {'name': 'CPU', 'id': '0'},
            'GPU2': {'name': 'CPU', 'id': '1'}
        }
    }


def set_render_device(render_device):
    click.echo('Set render hardware to "%s".' % render_device)

    if render_device != 'AUTO':
        hardware_dict = get_hardware_dict_2()

        # Unknown hardware
        if render_device not in hardware_dict['devices']:
            raise AssertionError('Your computer doesn\'t have a device called "%s".' % render_device)

        # set device
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        os.environ["CUDA_VISIBLE_DEVICES"] = hardware_dict['devices'][render_device]['id']

    click.echo('Done.')