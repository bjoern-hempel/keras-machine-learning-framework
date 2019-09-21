# Machine Learning Keras Suite
#
# A Python submodule that trains a nine points example.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   19.09.2019
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

from mlks.commands.main import Command

from keras.layers import Dense
from keras.models import Sequential

import numpy as np
import matplotlib.pyplot as plt

# some settings
np.random.seed(1337)


class NinePoints(Command):

    def __init__(self, general_config, machine_learning_config):
        self.general_config = general_config
        self.machine_learning_config = machine_learning_config

        # initialize the parent class
        super().__init__()

    def create_model(self, number_input_nodes, number_inner_nodes, number_output_nodes):
        # create the neuronal network 2 (x, y) -> 100 -> 1 (0 or 1) (tanh, SQE, Adam)
        model = Sequential()
        model.add(Dense(number_inner_nodes[0], activation=self.machine_learning_config.activation_function, input_shape=(number_input_nodes,)))
        # model.add(Dense(numberInnerNodes, input_dim=numberInnerNodes, activation=self.machine_learning_config.activationFunction))
        # model.add(Dense(numberInnerNodes, input_dim=numberInnerNodes, activation=self.machine_learning_config.activationFunction))
        model.add(Dense(number_output_nodes, input_dim=number_inner_nodes[len(number_inner_nodes) - 1],
                        activation=self.machine_learning_config.activation_function))
        model.compile(loss=self.machine_learning_config.loss_function, optimizer=self.machine_learning_config.optimizer,
                      metrics=[self.machine_learning_config.metrics])

        return model

    def do(self):
        if not self.is_config_correct(self.machine_learning_config):
            return

        # network settings
        number_input_nodes = 2
        number_inner_nodes = [100]
        number_output_nodes = 1

        # general settings
        verbose = 1 if self.general_config.verbose else 0

        # graphic settings
        range_x = [-0.1, 1.1]
        range_y = [range_x[0], range_x[1]]
        range_x_steps = 10
        range_y_steps = 10

        # train values
        train_values = np.array([
            [0.0, 0.0],
            [0.0, 1.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [0.5, 0.0],
            [0.5, 1.0],
            [0.0, 0.5],
            [1.0, 0.5],
            [0.5, 0.5]
        ])

        # result values
        result_values = np.array([
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [1],
            [0]
        ])

        # create the neuronal network 2 (x, y) -> 100 -> 1 (0 or 1) (tanh, SQE, Adam)
        model = self.create_model(number_input_nodes, number_inner_nodes, number_output_nodes)

        # train the model
        self.start_timer('fit')
        model.fit(x=train_values, y=result_values, epochs=self.machine_learning_config.epochs, verbose=verbose)
        self.finish_timer('fit')

        # create coordinate system from -0.25 to 1.25 for x and y
        x_graphic = np.linspace(range_x[0], range_x[1], range_x_steps)  # 10 means: 10 steps from -0.25 to 1.25
        y_graphic = np.linspace(range_y[0], range_y[1], range_y_steps)  # 10 means: 10 steps from -0.25 to 1.25
        (x1Grid, x2Grid) = np.meshgrid(x_graphic, y_graphic)
        x1_vector = x1Grid.flatten()
        x2_vector = x2Grid.flatten()

        # trainValuesGraphic: a matrix (array of 2-dim-arrays) with x1 and x2 nodes:
        # -0.25 < x1 < 1.25 and -0.25 < x2 < 1.25
        train_values_graphic = np.vstack((x1_vector, x2_vector)).T

        # use the trainValuesGraphic matrix and get all predictions from model
        # 0 and 0 -> 0
        result_values_graphic = model.predict(train_values_graphic).reshape(x1Grid.shape)

        # print the predicted points
        click.echo('resultValuesGraphic:')
        counter_y = 0
        step_x = (range_x[1] - range_x[0]) / (range_x_steps - 1)
        step_y = (range_y[1] - range_y[0]) / (range_y_steps - 1)

        # print out the graphic points
        for x2 in result_values_graphic:
            counter_y += 1
            counter_x = 0

            for x1 in x2:
                counter_x += 1
                print(
                    'x = ',
                    '{0: <10}'.format(round(range_x[0] + step_x * (counter_x - 1), 2)),
                    'y = ',
                    '{0: <10}'.format(round(range_y[0] + step_y * (counter_y - 1), 2)),
                    'value = ',
                    round(x1, 2)
                )

        plt.contourf(x1Grid, x2Grid, result_values_graphic, range_x_steps)
        plt.colorbar()

        # set x1 and x2 range
        plt.xlim(range_x[0], range_x[1])
        plt.ylim(range_y[0], range_y[1])

        # set x1 and x2 label
        plt.xlabel("train value $x_1$")
        plt.ylabel("train value $x_2$")

        # plot the train values (the train points)
        for i in range(len(train_values)):
            x1 = train_values[i][0]
            x2 = train_values[i][1]
            x3 = result_values[i][0]
            color = 'red' if x3 == 1 else 'red'
            marker = '+' if x3 == 1 else '_'
            plt.scatter(np.array([x1]), np.array([x2]), color=color, marker=marker)

        # print the node "lines" (anstieg m and bias n)
        (weights, bias) = model.layers[0].get_weights()
        for i in range(number_inner_nodes[0]):
            plt.plot(x_graphic, - weights[0, i] / weights[1, i] * x_graphic - bias[i] / weights[1, i], color="black",
                     alpha=0.1)

        # show the plot
        plt.show()

        click.echo('expected values:')
        click.echo(result_values)
        click.echo('predicted values:')
        click.echo(model.predict(train_values))

        # save the model to import within dl4j
        #model.save('/Users/bjoern/.spyder-py3/model.h5')
