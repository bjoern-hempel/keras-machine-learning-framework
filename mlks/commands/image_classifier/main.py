# Machine Learning Keras Suite
#
# This is the basic image classifier class from which all train, evaluate and prepare classes inherit.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   11.01.2020
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

# some future imports
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# some basic imports
import click
import os
import json
import sys
import math
import numpy as np
import six
import io
import csv
import pickle
import seaborn as sn
import pandas as pd
import pprint
import matplotlib

# some other from imports
from collections import OrderedDict
from collections import Iterable
from sklearn.metrics import confusion_matrix

# some own libraries and helper
from mlks.commands.main import Command
from mlks.helper.filesystem import get_number_of_folders_and_files
from mlks.helper.dict import count_len_recursive, get_sort_index_array
from mlks.helper.ml import get_epoch_array
from mlks.helper.filesystem import check_if_file_exists

# matplotlib libraries
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

# DenseNet121, DenseNet169, DenseNet201
from keras.applications.densenet import DenseNet121, DenseNet169, DenseNet201
from keras.applications.densenet import preprocess_input as DenseNetPreprocessInput

# InceptionResNetV2
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.inception_resnet_v2 import preprocess_input as InceptionResNetV2PreprocessInput

# InceptionV3
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input as InceptionV3PreprocessInput

# NASNet
from keras_applications.nasnet import NASNet
from keras.applications.nasnet import preprocess_input as NASNetPreprocessInput

# NASNetLarge
from keras.applications.nasnet import NASNetLarge
from keras.applications.nasnet import preprocess_input as NASNetLargePreprocessInput

# NASNetMobile
from keras_applications.nasnet import NASNetMobile
from keras.applications.nasnet import preprocess_input as NASNetMobilePreprocessInput

# MobileNet
from keras_applications.mobilenet import MobileNet
from keras.applications.mobilenet import preprocess_input as MobileNetPreprocessInput

# MobileNetV2
from keras.applications.mobilenet_v2 import MobileNetV2
from keras.applications.mobilenet_v2 import preprocess_input as MobileNetV2PreprocessInput

# ResNet50
from keras.applications.resnet import ResNet50
from keras.applications.resnet import preprocess_input as ResNet50PreprocessInput

# ResNet101
from keras.applications.resnet import ResNet101
from keras.applications.resnet import preprocess_input as ResNet101PreprocessInput

# ResNet152
from keras.applications.resnet import ResNet152
from keras.applications.resnet import preprocess_input as ResNet152PreprocessInput

# ResNet50V2
from keras.applications.resnet_v2 import ResNet50V2
from keras.applications.resnet_v2 import preprocess_input as ResNet50V2PreprocessInput

# ResNet101V2
from keras.applications.resnet_v2 import ResNet101V2
from keras.applications.resnet_v2 import preprocess_input as ResNet101V2PreprocessInput

# ResNet152V2
from keras.applications.resnet_v2 import ResNet152V2
from keras.applications.resnet_v2 import preprocess_input as ResNet152V2PreprocessInput

# VGG19
from keras.applications.vgg19 import VGG19
from keras.applications.vgg19 import preprocess_input as VGG19PreprocessInput

# Xception
from keras.applications.xception import Xception
from keras.applications.xception import preprocess_input as XceptionPreprocessInput

# some other keras imports
from keras.layers import Dense, GlobalAveragePooling2D, Dropout, Activation
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from keras.optimizers import SGD, RMSprop, Adagrad, Adadelta, Adam, Adamax, Nadam
from keras.callbacks import LearningRateScheduler, TensorBoard, ModelCheckpoint, Callback

# initialize the random generator to always get the same files in the same order (validation vs. trained data, etc.)
np.random.seed(1337)

# pretty printer setup
pp = pprint.PrettyPrinter(indent=4)


class CSVLogger2(Callback):
    """Callback that streams epoch results to a csv file.

    Supports all values that can be represented as a string,
    including 1D iterables such as np.ndarray.

    # Example

    ```python
    csv_logger = CSVLogger('training.log')
    model.fit(X_train, Y_train, callbacks=[csv_logger])
    ```

    # Arguments
        filename: filename of the csv file, e.g. 'run/log.csv'.
        separator: string used to separate elements in the csv file.
        append: True: append if file exists (useful for continuing
            training). False: overwrite existing file,
    """

    def __init__(self, filename, separator=',', append=False):
        self.sep = separator
        self.filename = filename
        self.append = append
        self.writer = None
        self.keys = None
        self.append_header = True
        if six.PY2:
            self.file_flags = 'b'
            self._open_args = {}
        else:
            self.file_flags = ''
            self._open_args = {'newline': '\n'}
        super(CSVLogger2, self).__init__()

    def on_train_begin(self, logs=None):
        if self.append:
            if os.path.exists(self.filename):
                with open(self.filename, 'r' + self.file_flags) as f:
                    self.append_header = not bool(len(f.readline()))
            mode = 'a'
        else:
            mode = 'w'

        self.csv_file = io.open(self.filename,
                                mode + self.file_flags,
                                **self._open_args)

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}

        def handle_value(k):
            is_zero_dim_ndarray = isinstance(k, np.ndarray) and k.ndim == 0
            if isinstance(k, six.string_types):
                return k
            elif isinstance(k, Iterable) and not is_zero_dim_ndarray:
                return '"[%s]"' % (', '.join(map(str, k)))
            else:
                return k

        if self.keys is None:
            self.keys = sorted(logs.keys())

        if self.model.stop_training:
            # We set NA so that csv parsers do not fail for this last epoch.
            logs = dict([(k, logs[k] if k in logs else 'NA') for k in self.keys])

        if not self.writer:
            class CustomDialect(csv.excel):
                delimiter = self.sep
            fieldnames = ['epoch'] + self.keys
            if six.PY2:
                fieldnames = [unicode(x) for x in fieldnames]
            self.writer = csv.DictWriter(self.csv_file,
                                         fieldnames=fieldnames,
                                         dialect=CustomDialect)
            if self.append_header:
                self.writer.writeheader()

        row_dict = OrderedDict({'epoch': epoch})
        row_dict.update((key, handle_value(logs[key])) for key in self.keys)
        self.writer.writerow(row_dict)
        self.csv_file.flush()

    def on_train_end(self, logs=None):
        self.csv_file.close()
        self.writer = None


class ImageClassifier(Command):
    """
    The image classifier class.

    Methods
    -------
    build_confusion_matrix(data, show_image=False, save_image=True, save_svg=True, save_pdf=True)
        Builds a confusion matrix with given data.
    """

    def __init__(self, config, question='Are these configurations correct? Continue?',
            negative='Cancelled by user.', check_empty_folder=False):
        self.config = config

        self.transfer_learning_wrapper = {
            'densenet121': {
                'class': DenseNet121,
                'preprocess_input': DenseNetPreprocessInput
            },
            'densenet169': {
                'class': DenseNet169,
                'preprocess_input': DenseNetPreprocessInput
            },
            'densenet201': {
                'class': DenseNet201,
                'preprocess_input': DenseNetPreprocessInput
            },
            'mobilenet': {
                'class': MobileNet,
                'preprocess_input': MobileNetPreprocessInput
            },
            'mobilenetv2': {
                'class': MobileNetV2,
                'preprocess_input': MobileNetV2PreprocessInput
            },
            'inceptionresnetv2': {
                'class': InceptionResNetV2,
                'preprocess_input': InceptionResNetV2PreprocessInput
            },
            'inceptionv3': {
                'class': InceptionV3,
                'preprocess_input': InceptionV3PreprocessInput
            },
            'nasnet': {
                'class': NASNet,
                'preprocess_input': NASNetPreprocessInput
            },
            'nasnetlarge': {
                'class': NASNetLarge,
                'preprocess_input': NASNetLargePreprocessInput
            },
            'nasnetmobile': {
                'class': NASNetMobile,
                'preprocess_input': NASNetMobilePreprocessInput
            },
            'resnet50': {
                'class': ResNet50,
                'preprocess_input': ResNet50PreprocessInput
            },
            'resnet101': {
                'class': ResNet101,
                'preprocess_input': ResNet101PreprocessInput
            },
            'resnet152': {
                'class': ResNet152,
                'preprocess_input': ResNet152PreprocessInput
            },
            'resnet50v2': {
                'class': ResNet50V2,
                'preprocess_input': ResNet50V2PreprocessInput
            },
            'resnet101v2': {
                'class': ResNet101V2,
                'preprocess_input': ResNet101V2PreprocessInput
            },
            'resnet152v2': {
                'class': ResNet152V2,
                'preprocess_input': ResNet152V2PreprocessInput
            },
            'vgg19': {
                'class': VGG19,
                'preprocess_input': VGG19PreprocessInput
            },
            'xception': {
                'class': Xception,
                'preprocess_input': XceptionPreprocessInput
            },
        }

        # initialize the parent class
        super().__init__(config, question, negative, check_empty_folder)

    def evaluate_file(self, model, evaluation_file, do_not_save_data=True):
        verbose = self.config.get('verbose')
        #verbose = True

        classes = self.config.get_environment('classes')

        # load image
        self.start_timer('load image file')
        image = self.load_image(evaluation_file)
        self.finish_timer('load image file')

        # predict image
        self.start_timer('predict image file')

        # data file
        data_file = '%s/%s' % (os.path.dirname(self.config.get_data('config_file')), 'data.pkl')

        # skip training if we already do have an evaluation file
        if not os.path.exists(data_file) or do_not_save_data:
            print('Evaluate file: "%s"' % evaluation_file)
            predicted_array = model.predict(image)

            # save evaluation file
            if not do_not_save_data:
                with open(data_file, 'wb') as output:
                    pickle.dump(predicted_array, output, pickle.HIGHEST_PROTOCOL)
        else:
            # open evaluation file
            with open(data_file, 'rb') as input_file:
                predicted_array = pickle.load(input_file)

        predicted_values = predicted_array.argmax(axis=-1)
        predicted_array_sorted = sorted(
            range(len(predicted_array[0])), key=lambda i: predicted_array[0][i],
            reverse=True
        )
        predicted_array_sorted_top_5 = predicted_array_sorted[0:5]
        self.finish_timer('predict image file')

        # print some informations
        prediction_overview = ''
        prediction_overview += 'classes\n'
        prediction_overview += '-------\n'
        prediction_overview_array = []
        counter = 0
        for index in predicted_array_sorted:
            counter += 1
            class_name = classes[index] + ':'
            prediction_overview += '%02d) %-25s %10.2f%%\n' % (counter, class_name, predicted_array[0][index] * 100)
            prediction_overview_array.append({
                'class_name': class_name,
                'predicted_value': predicted_array[0][index]
            })
        prediction_overview += '-------\n'

        if verbose:
            click.echo('\n\n' + prediction_overview)

        # print predicted class
        prediction_class = classes[predicted_values[0]]
        prediction_accuracy = predicted_array[0][predicted_values[0]] * 100
        if verbose:
            click.echo('\n\npredicted class:')
            click.echo('----------------')
            click.echo(
                'predicted: %s (%.2f%%)' % (prediction_class, prediction_accuracy)
            )
            click.echo('----------------')

        # build the top 5 text for the image
        text = ""
        counter = 0
        real_class = os.path.basename(os.path.dirname(evaluation_file))
        is_top_1 = real_class == prediction_class
        is_top_5 = False
        for index in predicted_array_sorted_top_5:
            counter += 1
            class_name = classes[index]
            text += "\n" if text != "" else ""
            text += '%02d) %s %10.2f%%' % (counter, '%s:' % class_name, predicted_array[0][index] * 100)

            if class_name == real_class:
                is_top_5 = True

        title = 'predicted: %s (%.2f%%)' % (
            classes[predicted_values[0]],
            predicted_array[0][predicted_values[0]] * 100
        )

        #print_image(evaluation_file, title, text, show_image, save_image)

        return {
            'classes': classes,
            'prediction_overview': prediction_overview,
            'prediction_overview_array': predicted_array.tolist()[0],
            'prediction_class': prediction_class,
            'prediction_accuracy': prediction_accuracy,
            'real_class': real_class,
            'is_top_1': is_top_1,
            'is_top_5': is_top_5,
            'evaluation_file': evaluation_file
        }

    def get_tl_model(self):
        transfer_learning_model = self.config.gettl('transfer_learning_model')

        if self.config.get('verbose'):
            click.echo('Use tl model "%s".' % transfer_learning_model)

        dim = self.config.gettl('input_dimension')
        weights = self.config.gettl('weights')

        return self.transfer_learning_wrapper[transfer_learning_model.lower()]['class'](
            weights=weights,
            include_top=False,
            input_shape=(dim, dim, 3)
        )

    def load_image(self, path):
        transfer_learning_model = self.config.gettl('transfer_learning_model')

        if self.config.get('verbose'):
            click.echo('load image: %s' % transfer_learning_model)

        image = load_img(
            path,
            target_size=(self.config.gettl('input_dimension'), self.config.gettl('input_dimension'))
        )
        image = img_to_array(image)
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

        return self.transfer_learning_wrapper[transfer_learning_model.lower()]['preprocess_input'](image)

    def get_model(self):
        number_trainable = self.config.gettl('number_trainable_layers')
        dense_size = self.config.gettl('dense_size')
        dropout = self.config.gettl('dropout')
        categories = self.get_categories()
        activation = self.config.getml('activation_function')

        # create the transfer learning model (base pre-trained model)
        base_model = self.get_tl_model()

        # add a global spatial average pooling layer
        x = base_model.output
        x = GlobalAveragePooling2D()(x)

        # let's add a fully-connected layer
        x = Dense(dense_size, activation=activation)(x)

        # drop out layer if needed
        if dropout > .0:
            x = Dropout(dropout)(x)

        # logistic layer: 2 categories - sigmoid / > 2 categories - softmax
        if categories == 2:
            predictions = Dense(1, activation='sigmoid')(x)
        else:
            predictions = Dense(categories, activation='softmax')(x)

        # this is the model we will train
        model = Model(inputs=base_model.input, outputs=predictions)

        # set the first number_trainable layers of the network to be non-trainable
        if number_trainable >= 0:
            number_not_trainable = len(model.layers) - number_trainable
            for layer in model.layers[:number_not_trainable]:
                layer.trainable = False
            for layer in model.layers[number_not_trainable:]:
                layer.trainable = True

        # -1: train all
        # -2: auto (try to find out the best number of trainable layers
        if number_trainable == -2:
            unfreeze = False
            for layer in model.layers:
                if unfreeze:
                    layer.trainable = True
                else:
                    layer.trainable = False

                # InceptionV3
                if layer.name == 'mixed3':
                    unfreeze = True

        # compile model
        self.compile_model(model)

        return model

    def load_model(self, model_file):
        if self.config.get('verbose'):
            click.echo('load model: %s' % self.config.gettl('transfer_learning_model'))

        model = load_model(model_file)
        self.compile_model(model)

        return model

    def step_decay(self, epoch):
        initial_learning_rate = self.config.getml('learning_rate')
        drop = self.config.getml('learning_rate_drop')
        epochs_drop = self.config.getml('learning_rate_epochs_drop')
        return initial_learning_rate * math.pow(drop, math.floor(epoch / epochs_drop))

    def compile_model(self, model):
        optimizer_name = self.config.getml('optimizer')
        learning_rate = self.config.getml('learning_rate')
        momentum = self.config.getml('momentum')
        decay = self.config.getml('decay')
        nesterov = self.config.getml('nesterov')
        use_plaidml_keras_backend = self.config.get('plaidml_keras_backend')

        # build optimizer
        if optimizer_name == 'sgd':
            optimizer = SGD(lr=learning_rate, momentum=momentum, decay=decay, nesterov=nesterov)
        elif optimizer_name == 'rmsprop':
            optimizer = RMSprop(lr=learning_rate)
        elif optimizer_name == 'adagrad':
            optimizer = Adagrad(lr=learning_rate)
        elif optimizer_name == 'adadelta':
            optimizer = Adadelta(lr=learning_rate)
        elif optimizer_name == 'adam':
            optimizer = Adam(lr=learning_rate)
        elif optimizer_name == 'adamax':
            optimizer = Adamax(lr=learning_rate)
        elif optimizer_name == 'nadam':
            optimizer = Nadam(lr=learning_rate)
        else:
            raise AssertionError('Unexpected optimizer name "%s"' % optimizer_name)

        loss = self.config.getml('loss_function')
        metrics = self.config.getml('metrics')

        if self.config.get('verbose'):
            click.echo('Used optimizer: %s' % self.config.getml('optimizer'))
            click.echo('Loss: %s' % loss)
            click.echo('Metrics: %s' % metrics)
            if self.config.getml('optimizer') == 'sgd':
                click.echo('Learning rate: %s' % learning_rate)
                click.echo('Momentum: %s' % momentum)
                click.echo('Decay: %s' % decay)
                click.echo('Nesterov: %s' % nesterov)

        metrics_array = [metrics]
        if not use_plaidml_keras_backend:
            metrics_array.append('top_k_categorical_accuracy')

        model.compile(optimizer=optimizer, loss=loss, metrics=metrics_array)

    def get_image_generator(self, image_generator=None):
        validation_split = self.config.getml('validation_split')
        transfer_learning_model = self.config.gettl('transfer_learning_model')
        use_train_val = self.config.get_data('use_train_val')

        # if no train and validation folder were given -> use the same image generator for training and evalution
        if not use_train_val and image_generator is not None:
            return image_generator

        # disable validation_split if train and validation folder given
        if use_train_val:
            validation_split = 0.0

        if not use_train_val and self.config.get('verbose'):
            click.echo('Validation split: %s' % validation_split)

        return ImageDataGenerator(
            preprocessing_function=self.transfer_learning_wrapper[transfer_learning_model.lower()]['preprocess_input'],
            validation_split=validation_split
        )

    def get_train_generator(self, image_generator):
        dim = self.config.gettl('input_dimension')
        data_path = self.config.get_data('data_path')
        batch_size = self.config.getml('batch_size')
        use_train_val = self.config.get_data('use_train_val')
        shuffle = True

        if use_train_val:
            data_path = '%s/%s' % (data_path, 'train')

        if self.config.get('verbose'):
            print('Used training path "%s".' % data_path)

        return image_generator.flow_from_directory(
            data_path,
            target_size=(dim, dim),
            color_mode='rgb',
            batch_size=batch_size,
            class_mode='categorical',
            subset=None if use_train_val else 'training',
            shuffle=shuffle
        )

    def get_validation_generator(self, image_generator):
        dim = self.config.gettl('input_dimension')
        data_path = self.config.get_data('data_path')
        batch_size = self.config.getml('batch_size')
        use_train_val = self.config.get_data('use_train_val')
        shuffle = False

        if use_train_val:
            data_path = '%s/%s' % (data_path, 'val')

        if self.config.get('verbose'):
            print('Used validation path "%s".' % data_path)

        return image_generator.flow_from_directory(
            data_path,
            target_size=(dim, dim),
            color_mode='rgb',
            batch_size=batch_size,
            class_mode='categorical',
            subset=None if use_train_val else 'validation',
            shuffle=shuffle
        )

    def train(self, model, train_generator, validation_generator):
        step_size_train = train_generator.n // train_generator.batch_size
        step_size_validation = validation_generator.n // validation_generator.batch_size
        epochs = self.config.getml('epochs')
        batch_size = self.config.getml('batch_size')
        log_file = self.config.get_data('log_file')
        csv_file = self.config.get_data('csv_file')
        best_model_file = self.config.get_data('best_model_file')
        verbose = 1 if self.config.get('verbose') else 0

        learning_rate_scheduler = LearningRateScheduler(self.step_decay, verbose=verbose)
        tensor_board = TensorBoard(
            log_dir=log_file,
            histogram_freq=0,
            write_graph=True,
            write_grads=False,
            write_images=False,
            embeddings_freq=0,
            embeddings_layer_names=None,
            embeddings_metadata=None,
            embeddings_data=None,
            update_freq='epoch'
        )
        csv_logger = CSVLogger2(
            csv_file,
            separator=',',
            append=False
        )
        model_checkpoint = ModelCheckpoint(
            best_model_file,
            monitor='val_accuracy',
            verbose=verbose,
            save_best_only=True,
            save_weights_only=False,
            mode='max',
            period=1
        )

        return model.fit_generator(
            generator=train_generator,
            steps_per_epoch=step_size_train,

            validation_data=validation_generator,
            validation_steps=step_size_validation,

            epochs=epochs,
            verbose=verbose,

            callbacks=[
                learning_rate_scheduler,
                #tensor_board,
                csv_logger,
                model_checkpoint
            ]
        )

    def get_categories(self):
        # get some needed configuration parameters
        data_path = self.config.get_data('data_path')
        use_train_val = self.config.get_data('use_train_val')

        if use_train_val:
            data_path = '%s/%s' % (data_path, 'train')

        # check folder
        if not os.path.isdir(data_path):
            raise AssertionError('"%s" does not exists or seems not to be a folder.')

        data_path_info = get_number_of_folders_and_files(data_path)

        return data_path_info['folders']

    def build_train_graph(self, show_diagram=True, save_diagram=False):

        # some configs
        x_from = 1
        x_to = self.config.getml('epochs')
        y_from = 0
        y_to = 1.1

        # some variables
        learning_rate = self.config.getml('learning_rate')
        learning_rate_string = ('%f' % learning_rate).rstrip('0').rstrip('.')
        learning_rate_drop = self.config.getml('learning_rate_drop')
        learning_rate_drop_string = ('%f' % learning_rate_drop).rstrip('0').rstrip('.')
        learning_rate_epochs_drop = self.config.getml('learning_rate_epochs_drop')
        epochs = self.config.getml('epochs')
        files = self.config.get_environment('files')

        # some preparations
        number_of_trained_files = count_len_recursive(files['train'])
        number_of_validated_files = count_len_recursive(files['validation'])
        epoch_array = get_epoch_array(epochs, learning_rate, learning_rate_drop, learning_rate_epochs_drop)
        trained_data_y = self.config.get_environment('accuracies_trained')
        validated_data_y = self.config.get_environment('accuracies_validated')
        trained_data_x = list(range(1, len(trained_data_y) + 1))
        validated_data_x = list(range(1, len(validated_data_y) + 1))
        sort_index_array_trained = get_sort_index_array(trained_data_y, True)
        sort_index_array_validated = get_sort_index_array(validated_data_y, True)

        # descriptions, text and titles
        subtitle = '%s with %d classes' % (
            os.path.basename(self.config.get_data('data_path')).capitalize(),
            len(self.config.get_environment('classes'))
        )
        title = '%s - #train:#val %s:%s - best acc. %.2f%%@ep.%d\nlr %s (drop rate %s every %d epochs) ' % (
            self.config.gettl('transfer_learning_model'),
            '{:,d}'.format(number_of_trained_files).replace(',', '.'),
            '{:,d}'.format(number_of_validated_files).replace(',', '.'),
            validated_data_y[sort_index_array_validated[0]] * 100,
            sort_index_array_validated[0] + 1,
            learning_rate_string,
            learning_rate_drop_string,
            learning_rate_epochs_drop
        )
        x_axis_description = 'Number of epochs'
        y_axis_description = 'Accuracy in percent'
        text = 'LEARNING RATE'

        # set x and y axis
        axes = plt.gca()
        axes.set_xlim([x_from, x_to])
        axes.set_ylim([y_from, y_to])

        # format y axis
        y_values = axes.get_yticks()
        axes.set_yticklabels(['{:,.0%}'.format(x) for x in y_values])

        # print descriptions and the title
        plt.suptitle(subtitle, fontsize=10)
        plt.title(title, fontsize=7)

        # plot the graph
        best_marker_on_trained = [
            sort_index_array_trained[0],
            sort_index_array_trained[1]
        ]
        best_marker_on_validated = [
            sort_index_array_validated[0],
            sort_index_array_validated[1]
        ]
        plt.plot(
            trained_data_x,
            trained_data_y,
            '-g.',
            label='Training',
            color='green',
            markevery=best_marker_on_trained
        )
        plt.plot(
            validated_data_x,
            validated_data_y,
            '-g.',
            label='Validation',
            color='blue',
            markevery=best_marker_on_validated
        )

        plt.xlabel(x_axis_description)
        plt.ylabel(y_axis_description)
        plt.legend(
            fontsize=7
        )

        # build learning rate rectangles
        counter = 0
        color_from = 0.75
        color_to = 0.95
        colors_dist = (color_to - color_from) / len(epoch_array)
        current_color_pos = color_from
        for epoch_item in epoch_array:
            epoch_from = epoch_item['epoch_from']
            epoch_to = epoch_item['epoch_to']
            learning_rate_current = epoch_item['learning_rate']
            poly = Rectangle(
                [epoch_from - 1, 0],
                width=epoch_to - epoch_from + 1,
                height=y_to,
                facecolor='%s' % current_color_pos,
                linewidth=0
            )
            axes.add_patch(poly)
            counter += 1
            current_color_pos += colors_dist
            text += '\n%s from %02d to %02d' % (
                ('%f' % learning_rate_current).rstrip('0').rstrip('.'),
                epoch_from,
                epoch_to
            )

        # print some scatters
        for index in range(len(best_marker_on_validated)):
            plt.text(
                best_marker_on_validated[index] + 1,
                validated_data_y[best_marker_on_validated[index]] + 0.02,
                s='%.2f%% (%d)' % (validated_data_y[best_marker_on_validated[index]] * 100, index + 1),
                fontsize=6
            )
        for index in range(len(best_marker_on_trained)):
            plt.text(
                best_marker_on_trained[index] + 1,
                trained_data_y[best_marker_on_trained[index]] + 0.02,
                s='%.2f%% (%d)' % (trained_data_y[best_marker_on_trained[index]] * 100, index + 1),
                fontsize=6
            )

        max_value_trained = trained_data_y[best_marker_on_trained[0]]
        max_value_validated = validated_data_y[best_marker_on_validated[0]]
        max_value = max_value_trained if max_value_trained > max_value_validated else max_value_validated

        if max_value > 0.8:
            x_text = self.config.getml('epochs') - (0.05 * (self.config.getml('epochs') - 1))
            y_text = 0.05
            align = 'right'
            valign = 'bottom'
        else:
            x_text = 0.05 * (self.config.getml('epochs') + 4)
            y_text = y_to - 0.05
            align = 'left'
            valign = 'top'
        plt.text(
            s=text,
            fontsize=7,
            x=x_text,
            y=y_text,
            color='green',
            bbox=dict(facecolor='white', alpha=0.6, edgecolor='grey', boxstyle='round,pad=0.5'),
            horizontalalignment=align,
            verticalalignment=valign
        )

        # save accuracy diagram
        if save_diagram:
            plt.savefig(self.config.get_data('accuracy_file'))

        # show accuracy diagram
        if show_diagram:
            plt.show()
            return None

        # return absolute and url path if accuracy file was created
        return {
            'absolute_path': self.config.get_data('accuracy_file'),
            'url_path': self.config.get_data('accuracy_file')
        }

    def get_evaluation_files(self, data_path, files_validation):
        evaluation_files = []

        # bulid evaluation file array
        for class_name in files_validation:
            for file_name in files_validation[class_name]:
                evaluation_files.append(os.path.join(data_path, class_name, file_name))

        return evaluation_files

    def get_evaluation_data(self, model_file, data_path, files_validation, evaluate_type, save_evaluation_file=True):

        # some needed variables
        root_path = os.path.dirname(self.config.get_data('config_file'))
        json_file = os.path.join(root_path, 'evaluation-file-%s.json' % evaluate_type)

        # use already calculated json file if it exists
        if os.path.isfile(json_file):
            with open(json_file) as f:
                return json.load(f)

        # collect all evaluation files
        evaluation_files = self.get_evaluation_files(data_path, files_validation)

        # data array
        data = {
            'root_path': root_path,
            'classes': [],
            'data': {},
            'top_k': {
                'correctly_classified_top_1': [],
                'incorrectly_classified_top_1': [],
                'correctly_classified_top_5': [],
                'incorrectly_classified_top_5': []
            }
        }

        # check model file
        check_if_file_exists(model_file)

        # load model
        self.start_timer('load model file "%s"' % model_file)
        model = self.load_model(model_file)
        self.finish_timer('load model file "%s"' % model_file)

        # evaluate all collected files
        for evaluation_file in evaluation_files:
            self.evaluate_file(model, evaluation_file)

        # evaluate all collected files
        for evaluation_file in evaluation_files:
            evaluation_data = self.evaluate_file(model, evaluation_file)
            data['classes'] = evaluation_data['classes']

            del evaluation_data['prediction_overview']
            del evaluation_data['classes']

            evaluation_data['evaluation_file'] = evaluation_data['evaluation_file'].replace(
                '%s/' % data['root_path'], ''
            )
            index_key = evaluation_data['evaluation_file']

            data['data'][index_key] = evaluation_data

            if evaluation_data['is_top_1']:
                data['top_k']['correctly_classified_top_1'].append(index_key)
            else:
                data['top_k']['incorrectly_classified_top_1'].append(index_key)

            if evaluation_data['is_top_5']:
                data['top_k']['correctly_classified_top_5'].append(index_key)
            else:
                data['top_k']['incorrectly_classified_top_5'].append(index_key)

        # save evaluation file
        if save_evaluation_file:
            self.start_timer('Write json file "%s"' % json_file)
            with open(json_file, 'w') as outfile:
                json.dump(data, outfile, indent=4)
            self.finish_timer('Write json file "%s"' % json_file)

        return data

    def get_evaluated_data(self, data_confusion_matrix, classes):
        data_evaluated = {
            'classes': {},
            'all': {
                'positive': 0,
                'negative': 0,
                'all': 0
            }
        }

        # mask zero fields
        mask = np.zeros_like(data_confusion_matrix)
        for row in range(len(data_confusion_matrix)):
            data_evaluated['classes'][classes[row]] = {
                'positive': 0,
                'negative': 0,
                'all': 0
            }
            for col in range(len(data_confusion_matrix[row])):
                if row == col:
                    data_evaluated['classes'][classes[row]]['positive'] += data_confusion_matrix[row][col]
                    data_evaluated['all']['positive'] += data_confusion_matrix[row][col]
                else:
                    data_evaluated['classes'][classes[row]]['negative'] += data_confusion_matrix[row][col]
                    data_evaluated['all']['negative'] += data_confusion_matrix[row][col]

                data_evaluated['classes'][classes[row]]['all'] += data_confusion_matrix[row][col]
                data_evaluated['all']['all'] += data_confusion_matrix[row][col]

                if data_confusion_matrix[row][col] == 0:
                    mask[row][col] = True

        # calculate the accuracy
        for class_name in data_evaluated['classes']:
            data_evaluated['classes'][class_name]['accuracy'] = round(
                data_evaluated['classes'][class_name]['positive'] / data_evaluated['classes'][class_name]['all'],
                8
            )
        data_evaluated['all']['accuracy'] = round(
            data_evaluated['all']['positive'] / data_evaluated['all']['all'],
            8
        )

        return data_evaluated, mask

    def get_true_prediction_data(self, data):
        y_true = []
        y_pred = []

        for path in data['data']:
            element = data['data'][path]

            y_true.append(element['prediction_class'])
            y_pred.append(element['real_class'])

        return y_true, y_pred

    @staticmethod
    def non_lin_cdict(steps, hexcol_array):
        cdict = {'red': (), 'green': (), 'blue': ()}
        for s, hexcol in zip(steps, hexcol_array):
            rgb = matplotlib.colors.hex2color(hexcol)
            cdict['red'] = cdict['red'] + ((s, rgb[0], rgb[0]),)
            cdict['green'] = cdict['green'] + ((s, rgb[1], rgb[1]),)
            cdict['blue'] = cdict['blue'] + ((s, rgb[2], rgb[2]),)
        return cdict

    def build_confusion_matrix(self, data, evaluate_type, show_image=False, save_image=True, save_svg=True, save_pdf=True,
                               use_percentage=True):
        """Builds a confusion matrix with given data
        ----------
        data : array
            The data array
        evaluate_type : string
            The evaluation type
        show_image : bool, optional
            Specifies whether the graph should be displayed. (default is False)
        save_image : bool, optional
            Specifies whether the graph should be saved. (default is True)
        save_svg : bool, optional
            Specifies whether the graph should be saved. (default is True)
        save_pdf : bool, optional
            Specifies whether the graph should be saved. (default is True)
        Raises
        ------
        AssertionError
            If the given evaluation path was not found or is not a folder.
        """
        y_true, y_pred = self.get_true_prediction_data(data)
        data_confusion_matrix = confusion_matrix(y_true, y_pred)
        classes = data['classes']
        data_evaluated, mask = self.get_evaluated_data(data_confusion_matrix, classes)

        name = os.path.basename(os.path.dirname(data['root_path']))
        name = name.replace('-2', '')

        title = 'Confusion Matrix "%s" %d classes (acc. %.2f%%)' % (
            name,
            len(classes),
            data_evaluated['all']['accuracy'] * 100
        )

        labeled_classes_index = []
        for class_name in data_evaluated['classes']:
            labeled_classes_index.append(
                class_name.replace('_', ' ').title() if use_percentage else
                '%s (%6.2f%%)' % (
                    class_name.replace('_', ' ').title(),
                    data_evaluated['classes'][class_name]['accuracy'] * 100
                )
            )
        labeled_classes_columns = []
        for class_name in data_evaluated['classes']:
            labeled_classes_columns.append(
                class_name.replace('_', ' ').title()
            )

        # recalculate data_confusion_matrix to percentage
        if use_percentage:
            data_confusion_matrix = data_confusion_matrix.astype(float)
            for row in range(len(data_confusion_matrix)):
                for col in range(len(data_confusion_matrix[row])):
                    data_confusion_matrix[row][col] = data_confusion_matrix[row][col] / data_evaluated['classes'][classes[row]]['all']

        df_cm = pd.DataFrame(data_confusion_matrix, index=labeled_classes_index, columns=labeled_classes_columns)
        plt.figure(figsize=(10, 7))
        plt.title(title)
        plt.xlabel("Values on X axis")
        sn.set(font_scale=0.5)

        hc = ['#228080', '#f9d9d9', '#ebebeb', '#638787', '#228080']
        th = [0, 0.1, 0.5, 0.9, 1]
        cdict = self.non_lin_cdict(th, hc)
        cm = matplotlib.colors.LinearSegmentedColormap('test', cdict)

        format = '.1%' if use_percentage else 'g'
        g = sn.heatmap(
            df_cm,
            annot=True,
            cbar=False,
            annot_kws={"size": 3},
            linewidths=0.2,
            linecolor='gray',
            mask=mask,
            cmap=cm, #sn.color_palette("BrBG", 100, desat=1),
            center=0,
            xticklabels=True,
            yticklabels=True,
            fmt=format
        )
        g.set_yticklabels(g.get_yticklabels(), rotation=0, fontsize=4, horizontalalignment='right')
        g.set_xticklabels(g.get_xticklabels(), rotation=30, fontsize=4, horizontalalignment='right')

        plt.rcParams['figure.figsize'] = 12, 9
        plt.rcParams['savefig.dpi'] = 'figure'
        fig1 = plt.gcf()

        if show_image:
            plt.show()

        if save_image or True:
            plt.draw()
            fig1.savefig(os.path.join(data['root_path'], 'confusion_matrix_%s.png' % evaluate_type), dpi=1200)
        if save_pdf:
            plt.draw()
            fig1.savefig(os.path.join(data['root_path'], 'confusion_matrix_%s.pdf' % evaluate_type), dpi=1200)
        if save_svg:
            plt.draw()
            fig1.savefig(os.path.join(data['root_path'], 'confusion_matrix_%s.svg' % evaluate_type), dpi=1200)
