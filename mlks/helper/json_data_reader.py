# Machine Learning Keras Suite
#
# A Python JsonDataReader class: Reads data from json and combine them with
# the given prediction list.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   25.09.2020
# Web:    https://github.com/bjoern-hempel/machine-learning-keras-suite
#
# LICENSE
#
# MIT License
#
# Copyright (c) 2020 Björn Hempel <bjoern@hempel.li>
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
import sys
import json

from typing import List


class JsonDataReader:
    """A json data reader class"""
    data: object
    json_path: str

    def __init__(self, json_path: str, prediction: object):
        """Constructor of class JsonDataReader.

        Parameters
        ----------
        json_path : str
        prediction : object
        """

        self.json_path = json_path
        self.prediction = prediction

        # check file
        if not os.path.isfile(self.json_path):
            print('File "%s" was not found.' % self.json_path)
            sys.exit(1)

        # read file
        with open(self.json_path, 'r', encoding='utf-8') as file_handler:
            self.json = file_handler.read()

        # parse file
        self.data = json.loads(self.json)

    @staticmethod
    def build_associative_array(array_list: List, index: str) -> object:
        """Builds an associative array.

        Parameters
        ----------
        array_list : List
        index : str

        Returns
        -------
        object

        """
        associative_array = {}

        for entry in array_list:
            associative_array[entry[index]] = entry

        return associative_array

    @staticmethod
    def convert_data(class_data: object, language: str = 'DE', verbose: bool = True) -> object:
        """Builds a data object from given class data.

        Parameters
        ----------
        class_data : object
        language : str
        verbose : bool

        Returns
        -------
        object

        """

        return_data = {
            'class': class_data['class'],
            'name': class_data['name'][language],
            'categories': class_data['categories']
        }

        if verbose:
            extra_data = {
                'edibility': class_data['edibility'],
                'description': class_data['description'][language],
                'wikipedia': class_data['urls']['wikipedia'][language]
            }

            return_data.update(extra_data)

        return return_data

    @staticmethod
    def get_category_path(categories: object, classes: object, class_prediction: object) -> List:
        """Builds the category path from given class_name.

        Parameters
        ----------
        categories : object
        classes : object
        class_prediction : object

        Returns
        -------
        object

        """

        class_name: str = class_prediction['name']

        category_path: List = []

        if len(classes[class_name]['categories']) <= 0:
            return category_path

        # Get first category from current class
        category_name = classes[class_name]['categories'][0]
        category = categories[category_name]

        # Collect category name
        category_path.insert(0, category['category'])

        while len(category['parent-categories']) > 0:
            category_name = category['parent-categories'][0]
            category = categories[category_name]

            category_path.insert(0, category['category'])

        return category_path

    def get_json_wrapper(self, data: object, language: str = 'DE') -> object:
        """Builds the whole json wrapper.

        Parameters
        ----------
        data : object
        language : str

        Returns
        -------
        object

        """

        return {
            'success': True,
            'version': self.data['version'],
            'data': data['data'],
            'prediction_order': data['prediction_order'],
        }

    def combine_data(self, classes: object, categories: object, class_prediction: object, language: str = 'DE',
                     verbose: bool = True) -> object:
        """Builds the combined data object from given json classes object and class prediction object.

        Parameters
        ----------
        classes : object
        categories : object
        class_prediction : object
        language : str
        verbose : bool

        Returns
        -------
        object

        """
        class_name: str = class_prediction['name']
        data_class: object = classes[class_name]

        data = self.convert_data(class_data=data_class, language=language, verbose=verbose)

        data.update({'prediction': class_prediction['prediction']})

        if verbose:
            data.update({'category_path': self.get_category_path(categories, classes, class_prediction)})
            data.update({'category_path_string': ' > '.join(data['category_path'])})

        return data

    def get_info_as_json(self, number: int = 1, language: str = 'DE', verbose: bool = True) -> object:
        """Builds the whole json object and returns it.

        Parameters
        ----------
        number : int
        language : str
        verbose: bool

        Returns
        -------
        object
            Returns the whole combined object.

        """

        # read classes and categories
        classes = self.build_associative_array(self.data['classes'], 'class')
        categories = self.build_associative_array(self.data['categories'], 'category')

        # data dict
        data = {
            'data': {
                'classes': {}
            },
            'prediction_order': [],
        }

        # check the number of returned data elements
        if number > len(self.prediction['data']):
            raise Exception('The wanted class numbers %d is higher than the length of prediction array.' % number)

        # add each data element
        for i in range(number):
            class_prediction: object = self.prediction['data'][i]
            class_name: str = class_prediction['name']
            data['data']['classes'][class_name] = self.combine_data(classes=classes, categories=categories,
                                                 class_prediction=class_prediction,
                                                 language=language, verbose=verbose)
            data['prediction_order'].append(class_name)

        # return complete json object
        return self.get_json_wrapper(data, language)
