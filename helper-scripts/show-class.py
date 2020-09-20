#!/usr/bin/env python

import os
import sys
import pprint
import json

# configure ppprint
pp = pprint.PrettyPrinter(indent=4)

config_path_json: str = 'C:/Users/bjoern/Development/keras-machine-learning-framework-json-editor/data/mushrooms.json'

if len(sys.argv) < 2:
    print('Missing class name in argument')
    sys.exit(1)

config_class_name: str = sys.argv[1]  # 'agaricus_campestris'

config_language: str = 'DE'

if len(sys.argv) > 2:
    config_language: str = sys.argv[2]


class JsonDataReader:
    """A json data reader class"""
    data: object
    path: str

    def __init__(self, path: str):
        self.path = path

        # check file
        if not os.path.isfile(self.path):
            print('File "%s" was not found.' % self.path)
            sys.exit(1)

        # read file
        with open(config_path_json, 'r', encoding='utf-8') as file_handler:
            self.json = file_handler.read()

        # parse file
        self.data = json.loads(self.json)

    @staticmethod
    def convert_array(array, index):
        associative_array = {}

        for entry in array:
            associative_array[entry[index]] = entry

        return associative_array

    @staticmethod
    def convert_data(data, language='DE'):
        return {
            'categories': data['categories'],
            'class': data['class'],
            'edibility': data['edibility'],
            'description': data['description'][language],
            'name': data['name'][language],
            'wikipedia': data['urls']['wikipedia'][language]
        }

    def get_category_path(self, categories, classes, class_name):
        category_path = []

        if len(classes[class_name]['categories']) <= 0:
            return category_path

        # Get first category from current class
        category_name = classes[class_name]['categories'][0]
        category = categories[category_name]

        # Collect category name
        category_path.append(category['category'])

        while len(category['parent-categories']) > 0:
            category_name = category['parent-categories'][0]
            category = categories[category_name]

            category_path.append(category['category'])

        return category_path

    def get_json_wrapper(self, classes, categories, class_name, language='DE', version='v1.0'):
        return_data = {
            'success': False,
            'version': version
        }

        if class_name not in classes:
            return return_data

        data_class = classes[class_name]

        data = self.convert_data(data_class, language)
        data['category_path'] = self.get_category_path(categories, classes, class_name)

        return_data['success'] = True
        return_data['data'] = data

        return return_data

    def get_info(self, class_name: str, language='DE') -> object:
        # read classes and categories
        classes = self.convert_array(self.data['classes'], 'class')
        categories = self.convert_array(self.data['categories'], 'category')

        return self.get_json_wrapper(classes, categories, class_name, language, self.data['version'])


# show data from config file
json_data_reader = JsonDataReader(config_path_json)
info = json_data_reader.get_info(config_class_name, config_language)

pp.pprint(info)
