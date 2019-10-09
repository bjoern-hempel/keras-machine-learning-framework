# Machine Learning Keras Suite
#
# A Python helper file: Provides some graph output helper.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   09.10.2019
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

from keras.preprocessing.image import load_img
from mlks.helper.filesystem import add_file_extension
import matplotlib.pyplot as plt


def print_image(image_file, title, text, save_graph = False):
    img = load_img(image_file)
    format = img.format
    mode = img.mode
    (width, height) = img.size

    text = '%s - %s - %sx%s\n%s' % (format, mode, width, height, text)

    plt.figure(figsize=(10, 6))
    plt.imshow(img)
    plt.title(title)
    plt.text(
        s=text,
        fontsize=8,
        x=width - round(width * 0.025),
        y=round(width * 0.025),
        color='green',
        bbox=dict(facecolor='white', alpha=0.6, edgecolor='grey', boxstyle='round,pad=0.5'),
        horizontalalignment='right',
        verticalalignment='top'
    )

    # save graph
    if save_graph:
        graph_file = add_file_extension(add_file_extension(image_file, 'graph', True), 'png')
        plt.savefig(graph_file)

    # show graph
    plt.show()


