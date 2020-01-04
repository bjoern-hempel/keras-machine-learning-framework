# Example:
#
# user$ python helper-scripts/convert-log-to-json.py processed/number_train_files/inceptionv3/food-50-80-20-all-16
#

import re
import pprint
import json
import os
import sys

pp = pprint.PrettyPrinter(indent=4)

path_root = 'F:/data'
path_experiment_relative = 'processed/different_models/all/food-50-80-20-densenet201-8'
path_experiment_absolute = '%s/%s' % (path_root, path_experiment_relative)

# read parameter
if len(sys.argv) > 1:
    path_experiment_relative = sys.argv[1]
    path_experiment_absolute = '%s/%s' % (path_root, path_experiment_relative)

file_command_log_name = 'command.txt'
file_command_log_absolute = '%s/%s' % (path_experiment_absolute, file_command_log_name)

file_data_json_name = 'data.json'
file_data_json_absolute = '%s/%s' % (path_experiment_absolute, file_data_json_name)

total_data_config = [
    # general
    {'search': 'render_device', 'field-name': 'render-device', 'type': 'string', 'section': 'general'},

    # data
    {'search': 'data_path', 'field-name': 'data-path', 'type': 'string', 'section': 'data'},

    # transfer learning
    {'search': 'number_trainable_layers', 'field-name': 'number-trainable-layers', 'type': 'string', 'section': 'transfer-learning'},
    {'search': 'transfer_learning_model', 'field-name': 'transfer-learning-model', 'type': 'string', 'section': 'transfer-learning'},
    {'search': 'input_dimension', 'field-name': 'input-dimension', 'type': 'string', 'section': 'transfer-learning'},
    {'search': 'dense_size', 'field-name': 'dense-size', 'type': 'string', 'section': 'transfer-learning'},
    {'search': 'weights', 'field-name': 'weights', 'type': 'string', 'section': 'transfer-learning'},

    # machine learning
    {'search': 'batch_size', 'field-name': 'batch-size', 'type': 'int', 'section': 'machine-learning'},
    {'search': 'momentum', 'field-name': 'momentum', 'type': 'float', 'section': 'machine-learning'},
    {'search': 'activation_function', 'field-name': 'activation-function', 'type': 'string', 'section': 'machine-learning'},
    {'search': 'loss_function', 'field-name': 'loss-function', 'type': 'string', 'section': 'machine-learning'},
    {'search': 'optimizer', 'field-name': 'optimizer', 'type': 'string', 'section': 'machine-learning'}
]

# check paths
if not os.path.exists(path_experiment_absolute):
    raise AssertionError('Path "%s" does not exist.' % path_experiment_absolute)
if not os.path.exists(file_command_log_absolute):
    raise AssertionError('Config file "%s" does not exists.' % file_command_log_absolute)


def read_command_log_file(file_path):
    error_text_command_log_file = 'Something is wrong with the command log file "%s"' % file_path

    # read command log file
    data = None
    with open(file_path, 'r') as file:
        data = file.readlines()

    if data is None:
        raise AssertionError('Could not read command log file')

    experiment_data = {
        'epochs': [],
        'total': {
            'config': {}
        }
    }

    epochs = 0
    batches_total_learned = 0
    batches_total_total = 0
    duration_total_total = 0.0
    duration_total_total_unit = 's'
    duration_total_batch_average = 0.0
    duration_total_batch_average_unit = 's'
    config_data = {}
    command = None
    layers = 0
    deepth = 0
    trainable = 0
    best_train = {
        'val': {
            'accuracy-top-1': 0.0
        }
    }

    # parse command file
    idata = iter(data)
    for line in idata:

        # search for command line
        pattern = re.compile('.+(ml[ ]+train.+)')
        matches = pattern.match(line)
        if matches:
            command = matches.group(1)
            continue

        # search for command line
        pattern = re.compile('[0-9]+[ ]:[ ]+(.+)[ ]+\\((not )?trainable\\)')
        matches = pattern.match(line)
        if matches:
            layers += 1
            pattern_layer = re.compile('.*_conv')
            matches_layer = pattern_layer.match(matches.group(1))
            if matches_layer:
                deepth += 1
            if matches.group(2) != 'not ':
                trainable += 1
            continue

        # collect some total data
        for config in total_data_config:
            pattern = re.compile('%s:[ ]+(.+)' % config['search'])
            matches = pattern.match(line)
            if matches:
                value = matches.group(1)

                if not config['section'] in config_data:
                    config_data[config['section']] = {}

                if config['type'] == 'int':
                    config_data[config['section']][config['field-name']] = int(value)
                elif config['type'] == 'float':
                    config_data[config['section']][config['field-name']] = float(value)
                else:
                    if config['section'] == 'data':
                        value = value.replace('%s/' % path_root, '')
                    if config['section'] == 'general':
                        if value == 'GPU' or value == 'GPU1':
                            value = 'GTX 1060 (1)'
                        if value == 'GPU2':
                            value = 'GTX 1060 (2)'

                    config_data[config['section']][config['field-name']] = str(value)

                continue

        # collect all epochs
        pattern_first = re.compile('Epoch ([0-9]+):[ ]+LearningRateScheduler setting learning rate to ([0-9]+\\.[0-9]+)')
        matches_first = pattern_first.match(line)

        if matches_first:
            epoch = int(matches_first.group(1))
            learning_rate = float(matches_first.group(2))

            pattern_second = re.compile(
                '^([0-9]+)/([0-9]+).+[ ]-[ ]([0-9]+[\\.]?[0-9]*)([m]?s) ([0-9]+[\\.]?[0-9]*)([m]?s).+' +
                'loss:[ ]*([0-9]+[\\.]?[0-9]*).+' +
                'acc:[ ]*([0-9]+[\\.]?[0-9]*).+' +
                'top_k_categorical_accuracy:[ ]*([0-9]+[\\.]?[0-9]*).+' +
                'val_loss:[ ]*([0-9]+[\\.]?[0-9]*).+' +
                'val_acc:[ ]*([0-9]+[\\.]?[0-9]*).+' +
                'val_top_k_categorical_accuracy:[ ]*([0-9]+[\\.]?[0-9]*).+'
            )
            matches_second = pattern_second.match(next(idata))

            if not matches_second:
                raise AssertionError(error_text_command_log_file)

            batches_epoch_learned = int(matches_second.group(1))
            batches_epoch_total = int(matches_second.group(2))
            duration_epoch_total = float(int(matches_second.group(3)))
            duration_epoch_total_unit = matches_second.group(4)
            duration_epoch_batch_average = float(int(matches_second.group(5)))
            duration_epoch_batch_average_unit = matches_second.group(6)
            loss_train = float(matches_second.group(7))
            accuracy_top_1_train = float(matches_second.group(8))
            accuracy_top_5_train = float(matches_second.group(9))
            loss_val = float(matches_second.group(10))
            accuracy_top_1_val = float(matches_second.group(11))
            accuracy_top_5_val = float(matches_second.group(12))

            # some assertions
            if batches_epoch_learned != batches_epoch_total:
                raise AssertionError(error_text_command_log_file)

            if duration_epoch_total_unit == 'ms':
                duration_epoch_total = duration_epoch_total / 1000
                duration_epoch_total_unit = 's'

            if duration_epoch_batch_average_unit == 'ms':
                duration_epoch_batch_average = duration_epoch_batch_average / 1000
                duration_epoch_batch_average_unit = 's'

            # calculate total
            epochs += 1
            batches_total_learned += batches_epoch_learned
            batches_total_total += batches_epoch_total
            duration_total_total += duration_epoch_total
            duration_total_batch_average += duration_epoch_batch_average

            if accuracy_top_1_val > best_train['val']['accuracy-top-1']:
                best_train = {
                    'epoch': epoch,
                    'train': {
                        'loss': loss_train,
                        'accuracy-top-1': accuracy_top_1_train,
                        'accuracy-top-5': accuracy_top_5_train
                    },
                    'val': {
                        'loss': loss_val,
                        'accuracy-top-1': accuracy_top_1_val,
                        'accuracy-top-5': accuracy_top_5_val
                    }
                }

            experiment_data['epochs'].append(
                {
                    'epoch': epoch,
                    'learning-rate': learning_rate,
                    'duration-total': duration_epoch_total,
                    'duration-total-unit': duration_epoch_total_unit,
                    'duration-batch-average': duration_epoch_batch_average,
                    'duration-batch-average-unit': duration_epoch_batch_average_unit,
                    'batches-learned': batches_epoch_learned,
                    'batches-total': batches_epoch_total,
                    'train': {
                        'loss': loss_train,
                        'accuracy-top-1': accuracy_top_1_train,
                        'accuracy-top-5': accuracy_top_5_train
                    },
                    'val': {
                        'loss': loss_val,
                        'accuracy-top-1': accuracy_top_1_val,
                        'accuracy-top-5': accuracy_top_5_val
                    }
                }
            )

    net_name = None
    if 'transfer-learning' in config_data and 'transfer-learning-model' in config_data['transfer-learning']:
        net_name = config_data['transfer-learning']['transfer-learning-model']

    if net_name == 'DenseNet201':
        deepth = 201
    elif net_name == 'DenseNet169':
        deepth = 169
    elif net_name == 'DenseNet121':
        deepth = 121
    elif net_name == 'InceptionResNetV2':
        deepth = 164
    elif net_name == 'InceptionV3':
        deepth = 48
    #elif net_name == 'NASNet':
    #    deepth = 0
    #elif net_name == 'NASNetLarge':
    #    deepth = 0
    #elif net_name == 'NASNetMobile':
    #    deepth = 0
    #elif net_name == 'MobileNet':
    #    deepth = 0
    elif net_name == 'MobileNetV2':
        deepth = 53
    elif net_name == 'ResNet50':
        deepth = 50
    elif net_name == 'VGG19':
        deepth = 19
    elif net_name == 'Xception':
        deepth = 71

    experiment_data['total'] = {
        'command': command,
        'config': config_data,
        'epochs': epochs,
        'learning-rates': [],
        'duration-total': duration_total_total,
        'duration-total-unit': duration_total_total_unit,
        'duration-batch-average': round(duration_total_batch_average / epochs, 3),
        'duration-batch-average-unit': duration_total_batch_average_unit,
        'batches-learned': batches_total_learned,
        'batches-total': batches_total_total,
        'best-train': best_train,
        'net': {
            'name': net_name,
            'layers': layers,
            'deepth': deepth,
            'trainable': trainable
        }
    }

    return experiment_data


# convert command log file to json data
data_json = read_command_log_file(file_command_log_absolute)

# print json
pp.pprint(data_json)

# write json file
print('')
print('Write json file to "%s"' % file_data_json_absolute)
with open(file_data_json_absolute, 'w') as outfile:
    json.dump(data_json, outfile, indent=4)
print('Done...')
