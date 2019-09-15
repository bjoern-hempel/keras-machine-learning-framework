import click
import tensorflow as tf
from tensorflow.python.client import device_lib
import os
import re

# disable the standard logging outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# disable deprecated warnings
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)


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

    if config.verbose:
        click.echo('verbose')
    else:
        click.echo('not verbose')

    for x in range(repeat):
        click.echo('Hello %s!' % string, file=out)


@cli.command()
def info():
    """This subcommand shows some infos."""

    devices = device_lib.list_local_devices()
    number_of_gpus = 0

    # count the gpus
    for x in devices:
        if x.device_type == 'GPU':
            number_of_gpus += 1

    click.echo('')
    click.echo("Available GPUs: %d" % number_of_gpus)

    click.echo('')
    click.echo('Available devices:')
    click.echo('------------------')
    for x in devices:
        device_type = "CPU"
        device_name = ""

        if x.device_type == 'GPU':
            # try to extract the gpu name
            gpu_name = re.findall(r"name:[ ]*([^,]+)", x.physical_device_desc)
            device_name = gpu_name[0] if len(gpu_name) > 0 else device_name

        click.echo("%s: %s %s" % (device_type, x.name, "" if device_name == "" else "[%s]" % device_name))
    click.echo('------------------')

    click.echo('')
    click.echo('Default device:')
    click.echo('---------------')
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True, allow_soft_placement=True))
    click.echo('---------------')

    click.echo('')
    if number_of_gpus > 0:
        click.echo('Information: You are running this script with GPU support.')
    else:
        click.echo('Attention: You are running this script without GPU support.')
