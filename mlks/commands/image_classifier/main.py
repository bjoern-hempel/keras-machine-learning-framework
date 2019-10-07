# Machine Learning Keras Suite
#
# This is the basic image classifier class from which all train, evaluate and prepare classes inherit.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   02.10.2019
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
import os
import math

from mlks.commands.main import Command
from mlks.helper.filesystem import get_number_of_folders_and_files

# DenseNet121, DenseNet169, DenseNet201
from keras.applications.densenet import DenseNet121, DenseNet169, DenseNet201
from keras.applications.densenet import preprocess_input as DenseNetPreprocessInput

# InceptionResNetV2
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras.applications.inception_resnet_v2 import preprocess_input as InceptionResNetV2PreprocessInput

# InceptionV3
from keras.applications.inception_v3 import InceptionV3
from keras.applications.inception_v3 import preprocess_input as InceptionV3PreprocessInput

# MobileNet
from keras_applications.mobilenet import MobileNet
from keras.applications.mobilenet import preprocess_input as MobileNetPreprocessInput

# MobileNetV2
from keras.applications.mobilenetv2 import MobileNetV2
from keras.applications.mobilenetv2 import preprocess_input as MobileNetV2PreprocessInput

# ResNet50
from keras.applications.resnet50 import ResNet50
from keras.applications.resnet50 import preprocess_input as ResNet50PreprocessInput

# VGG19
from keras.applications.vgg19 import VGG19
from keras.applications.vgg19 import preprocess_input as VGG19PreprocessInput

from keras.layers import Dense, GlobalAveragePooling2D, Dropout, Activation
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
from keras.optimizers import SGD

from keras.callbacks import LearningRateScheduler, TensorBoard, CSVLogger, ModelCheckpoint


class ImageClassifier(Command):

    def __init__(self, config):
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
            'resnet50': {
                'class': ResNet50,
                'preprocess_input': ResNet50PreprocessInput
            },
            'vgg19': {
                'class': VGG19,
                'preprocess_input': VGG19PreprocessInput
            }
        }

        # initialize the parent class
        super().__init__(config)

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
        activation = 'relu'

        # get the transfer learning model
        base_model = self.get_tl_model()

        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(dense_size, activation=activation)(x)
        x = Dropout(dropout)(x)

        if categories == 2:
            probabilities = Dense(1)(x)
            predictions = Activation('sigmoid')(probabilities)
        else:
            probabilities = Dense(categories)(x)
            predictions = Activation('softmax')(probabilities)

        model = Model(inputs=base_model.input, outputs=predictions)

        # set the first number_trainable layers of the network to be non-trainable
        if number_trainable >= 0:
            number_not_trainable = len(model.layers) - number_trainable
            for layer in model.layers[:number_not_trainable]:
                layer.trainable = False
            for layer in model.layers[number_not_trainable:]:
                layer.trainable = True

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
        if self.config.getml('optimizer') == 'sgd':
            learning_rate = self.config.getml('learning_rate')
            momentum = self.config.getml('momentum')
            decay = self.config.getml('decay')
            nesterov = self.config.getml('nesterov')
            optimizer = SGD(lr=learning_rate, momentum=momentum, decay=decay, nesterov=nesterov)
        else:
            optimizer = 'Adam'

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

        model.compile(optimizer=optimizer, loss=loss, metrics=[metrics])

    def get_image_generator(self):
        validation_split = self.config.getml('validation_split')
        transfer_learning_model = self.config.gettl('transfer_learning_model')

        if self.config.get('verbose'):
            click.echo('Validation split: %s' % validation_split)

        return ImageDataGenerator(
            preprocessing_function=self.transfer_learning_wrapper[transfer_learning_model.lower()]['preprocess_input'],
            validation_split=validation_split
        )

    def get_train_generator(self, image_generator):
        dim = self.config.gettl('input_dimension')
        data_path = self.config.get_data('data_path')
        batch_size = self.config.getml('batch_size')

        return image_generator.flow_from_directory(
            data_path,
            target_size=(dim, dim),
            color_mode='rgb',
            batch_size=batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )

    def get_validation_generator(self, image_generator):
        dim = self.config.gettl('input_dimension')
        data_path = self.config.get_data('data_path')
        batch_size = self.config.getml('batch_size')

        return image_generator.flow_from_directory(
            data_path,
            target_size=(dim, dim),
            color_mode='rgb',
            batch_size=batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=True
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
            batch_size=batch_size,
            write_graph=True,
            write_grads=False,
            write_images=False,
            embeddings_freq=0,
            embeddings_layer_names=None,
            embeddings_metadata=None,
            embeddings_data=None,
            update_freq='epoch'
        )
        csv_logger = CSVLogger(
            csv_file,
            separator=',',
            append=False
        )
        model_checkpoint = ModelCheckpoint(
            best_model_file,
            monitor='val_acc',
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

        # check folder
        if not os.path.isdir(data_path):
            raise AssertionError('"%s" does not exists or seems not to be a folder.')

        data_path_info = get_number_of_folders_and_files(data_path)

        return data_path_info['folders']
