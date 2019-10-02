# Machine Learning Keras Suite
#
# A Python submodule that trains the given data structure.
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
import os
import json
from keras.layers import Dense, GlobalAveragePooling2D, Dropout, Activation
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from mlks.commands.main import Command
from mlks.helper.filesystem import get_number_of_folders_and_files


class Train(Command):

    def __init__(self, config):
        self.tl_models = {
            'InceptionV3': Train.get_tl_inceptionv3,
        }

        # initialize the parent class
        super().__init__(config)

    def get_tl_model(self):
        transfer_learning_model = self.config.gettl('transfer_learning_model')

        if transfer_learning_model not in self.tl_models:
            raise AssertionError('Model "%s" was not assigned within tl_models.' % transfer_learning_model)

        if self.config.get('verbose'):
            click.echo('Use tl model "%s".' % transfer_learning_model)

        return self.tl_models[transfer_learning_model](self)

    def get_tl_inceptionv3(self):
        dim = self.config.gettl('input_dimension')
        weights = self.config.gettl('weights')
        return InceptionV3(weights=weights, include_top=False, input_shape=(dim, dim, 3))

    def do(self):
        if not self.is_config_correct(self.config):
            return

        # get some needed configuration parameters
        dim = self.config.gettl('input_dimension')
        dense_size = self.config.gettl('dense_size')
        dropout = self.config.gettl('dropout')
        number_trainable = self.config.gettl('number_trainable_layers')
        data_path = self.config.gettl('data_path')

        # check folder
        if not os.path.isdir(data_path):
            raise AssertionError('"%s" does not exists or seems not to be a folder.')

        data_path_info = get_number_of_folders_and_files(data_path)
        categories = data_path_info['folders']

        # timer
        self.start_timer('preparations')

        # get the transfer learning model
        base_model = self.get_tl_model()

        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(dense_size, activation='relu')(x)
        x = Dropout(dropout)(x)

        if categories == 2:
            probabilities = Dense(1)(x)
            predictions = Activation('sigmoid')(probabilities)
        else:
            probabilities = Dense(categories)(x)
            predictions = Activation('softmax')(probabilities)

        model = Model(inputs=base_model.input, outputs=predictions)

        # set the first number_trainable layers of the network to be non-trainable
        for layer in model.layers[:number_trainable]:
            layer.trainable = False
        for layer in model.layers[number_trainable:]:
            layer.trainable = True

        # prints the used layers of the current model
        if self.config.get('verbose'):
            for i, layer in enumerate(model.layers):
                print(i, ': ', layer.name, '(trainable)' if layer.trainable else '(not trainable)')

        # build the train generator
        train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
        train_generator = train_datagen.flow_from_directory(
            data_path,
            target_size=(dim, dim),
            color_mode='rgb',
            batch_size=32,
            class_mode='categorical',
            shuffle=True
        )

        # set current classes to config class
        self.config.set_environment('classes', train_generator.class_indices, flip=True, flip_as_array=True)

        # compile the model
        model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

        # timer
        self.finish_timer('preparations')

        # train the model
        step_size_train = train_generator.n // train_generator.batch_size
        self.start_timer('fit')
        model.fit_generator(generator=train_generator,
                            steps_per_epoch=step_size_train,
                            epochs=10, verbose=1)
        self.finish_timer('fit')

        # save the model to import within dl4j
        model_path = self.config.getml('model_file')
        if model_path is not None:
            self.start_timer('save model')
            model.save(model_path)
            self.finish_timer('save model')

        # save config data from model to import within dl4j
        model_config = self.config.getml('model_config')
        if model_config is not None:
            #self.config.set_measurement('fit', 12345)
            #self.config.set_measurement('preparation', 987)

            if self.config.get('verbose'):
                click.echo('Write config file to %s' % model_config)
            with open(model_config, 'w') as json_file:
                json.dump(self.config.get_dict(), json_file, sort_keys=True, indent=4, separators=(',', ': '))
