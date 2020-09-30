#!/usr/bin/env python

import sys
import pprint
import json
import mlks_loader

# import fixtures
from fixtures import prediction
from mlks_loader import root_dir
from helper.arguments import read_parameter

# import classes
from mlks.helper.json_data_builder import JsonDataBuilder

# configure ppprint
pp = pprint.PrettyPrinter(indent=4)

# some configs
config_path_json: str = '%s-json-editor/data/mushrooms.json' % root_dir.replace('\\', '/')

# read parameters
parameter_language: str = read_parameter('string', 1, 'DE', ['DE', 'GB'])
parameter_number: int = read_parameter('integer', 2, 1)
parameter_output_type: bool = read_parameter('string', 3, 'simple', ['simple', 'full', 'raw'])

# show data from config file
json_data_reader = JsonDataBuilder(json_path=config_path_json, prediction=prediction)
info = json_data_reader.get_info_as_data(number=parameter_number, language=parameter_language,
                                         output_type=parameter_output_type)

# print the info json
print(json.dumps(info, indent=4))
