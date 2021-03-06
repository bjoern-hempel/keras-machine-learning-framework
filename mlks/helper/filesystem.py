# Machine Learning Keras Suite
#
# A Python helper file: Provides some file system helper.
#
# Author: Björn Hempel <bjoern@hempel.li>
# Date:   29.09.2019
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

import os
import shutil
import re
import json
from pathlib import Path
from datetime import datetime
from mlks.helper.time import SimpleUtc

PNG_EXTENSION = 'png'
JPG_EXTENSION = 'jpg'


def clear_folder(path):
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def get_root_project_path():
    split_string = '/%s/' % __package__
    parts = re.split(split_string, str(Path(__file__)).replace('\\', '/'))
    return parts[0]


def get_database_path(model_type):
    database_path = '%s/data/translations-%s.json' % (get_root_project_path(), model_type)

    # check if json database exists
    if not os.path.isfile(database_path):
        raise AssertionError('The database "%s" does not exists.' % database_path)

    return database_path


def get_database(model_type):
    database_path = get_database_path(model_type)

    # try to read the json database file
    with open(database_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except ValueError as e:
            print('invalid json: %s' % e)
            return None


def get_root_data_path(path):
    split_string = '/data/'
    parts = re.split(split_string, str(path).replace('\\', '/'))
    return '%s/data' % parts[0]


def get_changed_date(path):
    timestamp = os.path.getmtime(path)
    return str(datetime.fromtimestamp(timestamp).utcnow().replace(tzinfo=SimpleUtc()).isoformat())


def get_formatted_file_size(path):
    if os.path.isfile(path):
        file_size = os.path.getsize(path)
    else:
        file_size = 0

    if file_size < 1024:
        return '%d Byte' % file_size

    file_size /= 1024
    if file_size < 1024:
        return '%.1f kB' % file_size

    file_size /= 1024
    return '%.2f MB' % file_size


def get_number_of_folders_and_files(path):
    files = 0
    folders = 0

    for _, dir_names, file_names in os.walk(path):
        files += len(file_names)
        folders += len(dir_names)

    return {
        'files': files,
        'folders': folders
    }


def check_if_file_exists(file_path):
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise AssertionError('File "%s" does not exists.' % file_path)

    return True


def add_file_extension(file, extension, before=False, replace=True):
    if before:
        return os.path.splitext(file)[0] + '.' + extension + os.path.splitext(file)[1]

    if replace:
        return os.path.splitext(file)[0] + '.' + extension
    else:
        return file + '.' + extension
