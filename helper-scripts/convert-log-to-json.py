# Example:
#
# user$ python helper-scripts/convert-log-to-json.py processed/experiments/best_optimizer/inceptionv3/food-50-80-20-rmsprop-0.01-0.5-7-0.0-0.0
#

import re
import pprint
import json
import os
import sys

pp = pprint.PrettyPrinter(indent=4)


class ConverterLogJson:
    path_root = 'F:/data'
    path_experiment_relative = 'processed/different_models/all/food-50-80-20-densenet201-8'
    file_command_log_name = 'command.txt'
    file_data_json_name = 'data.json'

    total_data_config = [
        # general
        {'search': 'render_device', 'field-name': 'render-device', 'type': 'string', 'section': 'general'},

        # data
        {'search': 'data_path', 'field-name': 'data-path', 'type': 'string', 'section': 'data'},
        {'search': 'use_train_val', 'field-name': 'use-train-val', 'type': 'boolean', 'section': 'data'},

        # transfer learning
        {'search': 'number_trainable_layers', 'field-name': 'number-trainable-layers', 'type': 'string',
         'section': 'transfer-learning'},
        {'search': 'transfer_learning_model', 'field-name': 'transfer-learning-model', 'type': 'string',
         'section': 'transfer-learning'},
        {'search': 'input_dimension', 'field-name': 'input-dimension', 'type': 'string',
         'section': 'transfer-learning'},
        {'search': 'dense_size', 'field-name': 'dense-size', 'type': 'string', 'section': 'transfer-learning'},
        {'search': 'weights', 'field-name': 'weights', 'type': 'string', 'section': 'transfer-learning'},

        # machine learning
        {'search': 'batch_size', 'field-name': 'batch-size', 'type': 'int', 'section': 'machine-learning'},
        {'search': 'momentum', 'field-name': 'momentum', 'type': 'float', 'section': 'machine-learning'},
        {'search': 'activation_function', 'field-name': 'activation-function', 'type': 'string',
         'section': 'machine-learning'},
        {'search': 'loss_function', 'field-name': 'loss-function', 'type': 'string', 'section': 'machine-learning'},
        {'search': 'optimizer', 'field-name': 'optimizer', 'type': 'string', 'section': 'machine-learning'}
    ]

    template_error_text_command_log_file = 'Something is wrong with the command log file "%s"'

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
    depth = 0
    trainable = 0
    best_train = None
    experiment_data = None
    net_name = None
    depth = 0

    def __init__(self):

        # read parameter
        if len(sys.argv) > 1:
            self.path_experiment_relative = sys.argv[1]

        self.path_experiment_absolute = '%s/%s' % (self.path_root, self.path_experiment_relative)
        self.path_experiment_absolute = '%s/%s' % (self.path_root, self.path_experiment_relative)
        self.file_command_log_absolute = '%s/%s' % (self.path_experiment_absolute, self.file_command_log_name)
        self.file_data_json_absolute = '%s/%s' % (self.path_experiment_absolute, self.file_data_json_name)

        # check paths
        if not os.path.exists(self.path_experiment_absolute):
            raise AssertionError('Path "%s" does not exist.' % self.path_experiment_absolute)
        if not os.path.exists(self.file_command_log_absolute):
            raise AssertionError('Config file "%s" does not exists.' % self.file_command_log_absolute)

    def parse_config_data(self, data):
        self.experiment_data = {
            'epochs': [],
            'total': {
                'config': {}
            }
        }

        self.best_train = {
            'val': {
                'accuracy-top-1': 0.0
            }
        }

        iter_data = iter(data)
        for line in iter_data:

            # search for command line
            pattern = re.compile('.+(ml[ ]+train.+)')
            matches = pattern.match(line)
            if matches:
                self.command = matches.group(1)
                continue

            # search for command line
            pattern = re.compile('[0-9]+[ ]:[ ]+(.+)[ ]+\\((not )?trainable\\)')
            matches = pattern.match(line)
            if matches:
                self.layers += 1
                pattern_layer = re.compile('.*_conv')
                matches_layer = pattern_layer.match(matches.group(1))
                if matches_layer:
                    self.depth += 1
                if matches.group(2) != 'not ':
                    self.trainable += 1
                continue

            # collect some total data
            for config in self.total_data_config:
                pattern = re.compile('%s:[ ]+(.+)' % config['search'])
                matches = pattern.match(line)
                if matches:
                    value = matches.group(1)

                    if not config['section'] in self.config_data:
                        self.config_data[config['section']] = {}

                    if config['type'] == 'int':
                        self.config_data[config['section']][config['field-name']] = int(value)
                    elif config['type'] == 'float':
                        self.config_data[config['section']][config['field-name']] = float(value)
                    elif config['type'] == 'boolean':
                        self.config_data[config['section']][config['field-name']] = True if value == 'True' else False
                    else:
                        if config['section'] == 'data':
                            value = value.replace('%s/' % self.path_root, '')
                        if config['section'] == 'general':
                            if value == 'GPU' or value == 'GPU1':
                                value = 'GTX 1060 (1)'
                            if value == 'GPU2':
                                value = 'GTX 1060 (2)'

                        self.config_data[config['section']][config['field-name']] = str(value)

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
                matches_second = pattern_second.match(next(iter_data))

                if not matches_second:
                    raise AssertionError(self.template_error_text_command_log_file % self.file_command_log_absolute)

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
                    raise AssertionError(self.template_error_text_command_log_file % self.file_command_log_absolute)

                if duration_epoch_total_unit == 'ms':
                    duration_epoch_total = duration_epoch_total / 1000
                    duration_epoch_total_unit = 's'

                if duration_epoch_batch_average_unit == 'ms':
                    duration_epoch_batch_average = duration_epoch_batch_average / 1000
                    duration_epoch_batch_average_unit = 's'

                # calculate total properties
                self.epochs += 1
                self.batches_total_learned += batches_epoch_learned
                self.batches_total_total += batches_epoch_total
                self.duration_total_total += duration_epoch_total
                self.duration_total_batch_average += duration_epoch_batch_average

                # get best val epoch
                if accuracy_top_1_val > self.best_train['val']['accuracy-top-1']:
                    self.best_train = {
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

                # add epoch to json data variable
                self.experiment_data['epochs'].append(
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

    @staticmethod
    def get_number_of_folder(absolute_path):
        return len(next(os.walk(absolute_path))[1])

    @staticmethod
    def get_number_of_files(absolute_path):
        return len([name for name in os.listdir(absolute_path) if os.path.isfile(os.path.join(absolute_path, name))])

    def get_classes_of_folder(self, absolute_path):
        class_names = [dI for dI in os.listdir(absolute_path) if os.path.isdir(os.path.join(absolute_path, dI))]

        folders = {}
        for class_name in class_names:
            folders[class_name] = self.get_number_of_files('%s/%s' % (absolute_path, class_name))

        return folders

    def parse_json_from_command_log_file(self):

        # read command log file
        with open(self.file_command_log_absolute, 'r') as file:
            data = file.readlines()

        if data is None:
            raise AssertionError('Could not read command log file')

        # parse command file and write properties
        self.parse_config_data(data)
        self.write_net_name_and_depth()

        data_path_absolute = None
        if 'data' in self.config_data and 'data-path' in self.config_data['data']:
            data_path_absolute = '%s/%s' % (self.path_root, self.config_data['data']['data-path'])

        use_train_val = False
        if 'data' in self.config_data and 'use-train-val' in self.config_data['data']:
            use_train_val = self.config_data['data']['use-train-val']

        if data_path_absolute is None or not os.path.exists(data_path_absolute):
            raise AssertionError('Data path "%s" does not exist.' % data_path_absolute)

        if not use_train_val:
            raise AssertionError('This script only works in use-train-val mode yet.')

        self.config_data['data']['data-path-train'] = '%s/%s' % (self.config_data['data']['data-path'], 'train')
        self.config_data['data']['data-path-val'] = '%s/%s' % (self.config_data['data']['data-path'], 'val')

        data_path_train_absolute = '%s/%s' % (self.path_root, self.config_data['data']['data-path-train'])
        data_path_val_absolute = '%s/%s' % (self.path_root, self.config_data['data']['data-path-val'])

        if not os.path.exists(data_path_train_absolute):
            raise AssertionError('Data train path "%s" does not exist.' % data_path_train_absolute)

        if not os.path.exists(data_path_val_absolute):
            raise AssertionError('Data val path "%s" does not exist.' % data_path_val_absolute)

        self.experiment_data['total'] = {
            'command': self.command,
            'config': self.config_data,
            'epochs': self.epochs,
            'learning-rates': [],
            'duration-total': self.duration_total_total,
            'duration-total-unit': self.duration_total_total_unit,
            'duration-batch-average': round(self.duration_total_batch_average / self.epochs, 3),
            'duration-batch-average-unit': self.duration_total_batch_average_unit,
            'batches-learned': self.batches_total_learned,
            'batches-total': self.batches_total_total,
            'best-train': self.best_train,
            'classes': {
                'train': {
                    'count': self.get_number_of_folder(data_path_train_absolute),
                    'files': self.get_classes_of_folder(data_path_train_absolute)
                },
                'val': {
                    'count': self.get_number_of_folder(data_path_val_absolute),
                    'files': self.get_classes_of_folder(data_path_val_absolute)
                }
            },
            'net': {
                'name': self.net_name,
                'layers': self.layers,
                'depth': self.depth,
                'trainable': self.trainable
            }
        }

        return self.experiment_data

    def build_json(self, print_data_json=False):
        self.parse_json_from_command_log_file()

        # print json
        if print_data_json:
            pp.pprint(self.experiment_data)

        # write json file
        print('')
        print('Write json file to "%s"' % self.file_data_json_absolute)
        with open(self.file_data_json_absolute, 'w') as outfile:
            json.dump(self.experiment_data, outfile, indent=4)
        print('Done...')

    def write_net_name_and_depth(self):
        self.net_name = None
        if 'transfer-learning' in self.config_data and 'transfer-learning-model' in self.config_data['transfer-learning']:
            self.net_name = self.config_data['transfer-learning']['transfer-learning-model']

        if self.net_name == 'DenseNet201':
            self.depth = 201
        elif self.net_name == 'DenseNet169':
            self.depth = 169
        elif self.net_name == 'DenseNet121':
            self.depth = 121
        elif self.net_name == 'InceptionResNetV2':
            self.depth = 164
        elif self.net_name == 'InceptionV3':
            self.depth = 48
        #elif self.net_name == 'NASNet':
        #    self.depth = 0
        #elif self.net_name == 'NASNetLarge':
        #    self.depth = 0
        #elif self.net_name == 'NASNetMobile':
        #    self.depth = 0
        #elif self.net_name == 'MobileNet':
        #    self.depth = 0
        elif self.net_name == 'MobileNetV2':
            self.depth = 53
        elif self.net_name == 'ResNet50':
            self.depth = 50
        elif self.net_name == 'VGG19':
            self.depth = 19
        elif self.net_name == 'Xception':
            self.depth = 71


# create converter
converter_log_json = ConverterLogJson()

# build json file
converter_log_json.build_json(True)
