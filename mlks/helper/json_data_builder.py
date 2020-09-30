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


class JsonDataBuilder:
    """A json data reader class"""

    CONST_ERROR_NUMBER_HIGHER_THAN_ARRAY_COUNT = 'The wanted class numbers %d is higher than the length of prediction array.'

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
    def get_category_path(categories: object, class_name: str, classes: object = None) -> List:
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

        category_path: List = []

        if classes is not None:
            if len(classes[class_name]['categories']) <= 0:
                return category_path

            # Get first category from current class
            category_name = classes[class_name]['categories'][0]
            category = categories[category_name]

            # Collect category name
            category_path.insert(0, category['category'])
        else:
            # Get first category from current class
            category_name = class_name
            category = categories[category_name]

        while len(category['parent-categories']) > 0:
            category_name = category['parent-categories'][0]
            category = categories[category_name]

            category_path.insert(0, category['category'])

        return category_path

    @staticmethod
    def get_category_names(classes: object) -> List:
        """Returns all category names from given classes.

        Parameters
        ----------
        classes : object

        Returns
        -------
        List

        """

        category_names = {}

        for class_name in classes:
            class_element = classes[class_name]
            if 'category_path' in class_element:
                for category_name in class_element['category_path']:
                    category_names[category_name] = True
            else:
                if len(class_element['categories']) == 0:
                    print(class_element)
                    sys.exit()

                category_names[class_element['categories'][0]] = True

        return list(category_names.keys())

    @staticmethod
    def convert_class_data(class_data: object, class_prediction: object, language: str = 'DE',
                           output_type: str = 'simple') -> object:
        """Builds a data object from given class data.

        Parameters
        ----------
        class_data : object
        language : str
        output_type : str

        Returns
        -------
        object

        """

        return_data = {
            'class': class_data['class'],
            'name': class_data['name'][language],
            'categories': class_data['categories'],
            'prediction': class_prediction['prediction'],
        }

        if output_type == 'full':
            extra_data = {
                'edibility': class_data['edibility'],
                'description': class_data['description'][language],
                'wikipedia': class_data['urls']['wikipedia'][language]
            }

            return_data.update(extra_data)

        return return_data

    @staticmethod
    def convert_category_data(category_data: object, language: str = 'DE', output_type: str = 'simple') -> object:
        """Builds a data object from given category data.

        Parameters
        ----------
        category_data : object
        language : str
        output_type : str

        Returns
        -------
        object

        """
        return_data = {
            'category': category_data['category'],
            'name': category_data['name'][language],
        }

        if output_type == 'full':
            extra_data = {
                'description': category_data['description'][language],
                'wikipedia': category_data['urls']['wikipedia'][language]
            }

            return_data.update(extra_data)

        return return_data

    def combine_class_data(self, classes: object, categories: object, class_prediction: object, language: str = 'DE',
                           output_type: str = 'simple') -> object:
        """Builds the combined data object from given json classes object and class prediction object.

        Parameters
        ----------
        classes : object
        categories : object
        class_prediction : object
        language : str
        output_type : str

        Returns
        -------
        object

        """
        class_name: str = class_prediction['name']
        class_data: object = classes[class_name]

        class_data = self.convert_class_data(class_data=class_data, class_prediction=class_prediction,
                                             language=language,
                                             output_type=output_type)

        if output_type == 'full':
            class_data.update({'category_path': self.get_category_path(categories, class_name, classes)})
            class_data.update({'category_path_string': ' > '.join(class_data['category_path'])})

        return class_data

    def combine_category_data(self, categories: object, category_name: object, language: str = 'DE',
                              output_type: str = 'simple') -> object:

        category_data: object = categories[category_name]

        category_data = self.convert_category_data(category_data=category_data, language=language, output_type=output_type)

        if output_type == 'full':
            category_data.update({'category_path': self.get_category_path(categories, category_name)})
            category_data.update({'category_path_string': ' > '.join(category_data['category_path'])})

        return category_data

    def build_classes_object(self, number: int, classes: object, categories: object, language: str = 'DE',
                             output_type: str = 'simple') -> object:
        """Builds data object.

        Parameters
        ----------
        number : int
        classes : object
        categories : object
        language : str
        output_type : str

        Returns
        -------
        object

        """
        # data dict
        data = {
            'data': {
                'classes': {},
                'categories': {},
            },
            'prediction_order': [],
        }

        # check the number of returned data elements
        if number > len(self.prediction['data']):
            raise Exception(self.CONST_ERROR_NUMBER_HIGHER_THAN_ARRAY_COUNT % number)

        # add each data element
        for i in range(number):
            class_prediction: object = self.prediction['data'][i]
            class_name: str = class_prediction['name']
            data['data']['classes'][class_name] = self.combine_class_data(classes=classes, categories=categories,
                                                                          class_prediction=class_prediction,
                                                                          language=language, output_type=output_type)
            data['prediction_order'].append(class_name)

        return data

    def build_categories_object(self, data: object, categories: object, language: str = 'DE',
                                output_type: str = 'simple') -> object:
        """Build a dict of categories.

        Parameters
        ----------
        data : object
        categories : object

        Returns
        -------
        object

        """

        categories_object = {}
        classes = data['data']['classes']

        category_names = self.get_category_names(classes=classes)

        for category_name in category_names:
            categories_object[category_name] = self.combine_category_data(categories=categories,
                                                                          category_name=category_name,
                                                                          language=language, output_type=output_type)

        return categories_object

    def get_data_wrapper(self, data: object, parameter: object) -> object:
        """Builds the whole data wrapper.

        Parameters
        ----------
        parameter : object
        data : object

        Returns
        -------
        object

        """

        return_data = {
            'success': True,
            'version': self.data['version'],
            'data': data['data'],
            'parameter': parameter
        }

        if 'prediction_order' in data:
            return_data['data'].update({
                'prediction_order': data['prediction_order']
            })

        return return_data

    def get_data_wrapper_raw(self, number: int = 1, parameter: object = {}):
        """Builds the whole data wrapper (raw).

        Parameters
        ----------
        parameter : object
        number : int

        Returns
        -------
        object

        """

        # check the number of returned data elements
        if number > len(self.prediction['data']):
            raise Exception(self.CONST_ERROR_NUMBER_HIGHER_THAN_ARRAY_COUNT % number)

        prediction = self.prediction['data'][:number]

        data = {
            'data': prediction,
        }

        return self.get_data_wrapper(data=data, parameter=parameter)

    def get_info_as_data(self, number: int = 1, language: str = 'DE', output_type: str = 'simple') -> object:
        """Builds the whole json object and returns it.

        Parameters
        ----------
        number : int
        language : str
        output_type: str

        Returns
        -------
        object
            Returns the whole combined object.

        """

        parameter = {
            'number': number,
            'language': language,
            'output_type': output_type
        }

        # print the raw data directly
        if output_type == 'raw':
            return self.get_data_wrapper_raw(number=number, parameter=parameter)

        # read classes and categories
        classes = self.build_associative_array(self.data['classes'], 'class')
        categories = self.build_associative_array(self.data['categories'], 'category')

        # build classes
        data = self.build_classes_object(number=number, classes=classes, categories=categories, language=language,
                                         output_type=output_type)

        # add categories
        data['data']['categories'] = self.build_categories_object(data=data, categories=categories, language=language,
                                                                  output_type=output_type)

        # return complete json object
        return self.get_data_wrapper(data=data, parameter=parameter)
