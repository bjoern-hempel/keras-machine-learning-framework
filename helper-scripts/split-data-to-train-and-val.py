import os
import random
import math
import pprint
import subprocess

pp = pprint.PrettyPrinter(indent=4)
random.seed(123)


class DataHolder:
    base_path: str = 'E:\\data'
    raw_data_path = 'raw'
    raw_data_train_path = 'raw-train'
    source_data_path = 'food-50'
    target_data_path = '%s-%d-%d-%s'
    keep_train_data = 13000
    name_train = 'train'
    name_val = 'val'
    ratio_train = 0.9

    @staticmethod
    def get_data_target_path(without_base_path=False):
        percent_train = int(DataHolder.ratio_train * 100)
        percent_val = 100 - percent_train

        name = DataHolder.keep_train_data
        if name is not 'all':
            name = '%05d' % name

        name_target_data_path = DataHolder.target_data_path % (
            DataHolder.source_data_path,
            percent_train,
            percent_val,
            name
        )

        path = '%s\\%s' % (DataHolder.raw_data_train_path, name_target_data_path)

        if not without_base_path:
            path = '%s\\%s' % (DataHolder.base_path, path)

        return path

    @staticmethod
    def get_link_file_path(file_path, type_folder, without_base_path=False):
        path = '%s\\%s\\%s' % (
            DataHolder.get_data_target_path(without_base_path), type_folder, file_path
        )

        return path

    @staticmethod
    def get_target_file_path(file_path, type_folder):
        count_go_back = len(os.path.dirname(DataHolder.get_link_file_path(file_path, type_folder, True)).split('\\'))
        go_back = '..\\' * count_go_back
        return '%s%s\\%s\\%s' % (go_back, DataHolder.raw_data_path, DataHolder.source_data_path, file_path)

    @staticmethod
    def get_absolute_target_folder_path():
        return '%s\\%s\\%s' % (DataHolder.base_path, DataHolder.raw_data_path, DataHolder.source_data_path)


class SymlinkCreator:
    @staticmethod
    def prepare_file_folder(file_path):
        if os.path.isfile(file_path):
            raise AssertionError('File "%s" already exists.' % file_path)

        folder_path = os.path.dirname(file_path)

        if os.path.isfile(folder_path):
            raise AssertionError('Folder "%s" already exists as a file' % folder_path)

        if not os.path.isdir(folder_path):
            os.makedirs(folder_path, exist_ok=True)

        if not os.path.isdir(folder_path):
            raise AssertionError('It was not possible to create the folder "%s".' % folder_path)

    @staticmethod
    def create_ntfs_symlink_file(link, target, debug=False):
        if debug:
            print('%s -> %s' % (link, target))
            return True

        SymlinkCreator.prepare_file_folder(link)

        child = subprocess.Popen(['MKLINK', link, target], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        stream_data = child.communicate()[0]
        print(stream_data)

    @staticmethod
    def get_class_folders():
        path = DataHolder.get_absolute_target_folder_path()
        return [f.name for f in os.scandir(path) if f.is_dir()]

    @staticmethod
    def get_class_files(class_folder):
        path = os.path.join(DataHolder.get_absolute_target_folder_path(), class_folder)
        return [f.name for f in os.scandir(path) if f.is_file()]

    @staticmethod
    def get_files():
        files = {
            'train_classes': {},
            'train_files': [],
            'train': [],
            'val': []
        }

        # Collect all train and val files
        for class_folder in SymlinkCreator.get_class_folders():
            class_files = SymlinkCreator.get_class_files(class_folder)
            number_start_index_val = math.ceil(len(class_files) * DataHolder.ratio_train)
            random.shuffle(class_files)

            for train_name in class_files[0:number_start_index_val]:
                if DataHolder.keep_train_data is not 'all':
                    if not class_folder in files['train_classes']:
                        files['train_classes'][class_folder] = []
                    files['train_classes'][class_folder].append(os.path.join(class_folder, train_name))
                else:
                    files['train'].append(os.path.join(class_folder, train_name))

            for val_name in class_files[number_start_index_val:]:
                files['val'].append(os.path.join(class_folder, val_name))

        # Fill up train part if needed
        if DataHolder.keep_train_data is not 'all':
            if DataHolder.keep_train_data < len(files['train_classes']):
                raise AssertionError('DataHolder.keep_train_data must be higher than %d (currently: %d)' % (
                    len(files['train_classes']),
                    DataHolder.keep_train_data
                ))

            # Make sure we have at least one picture from each class
            for class_folder in files['train_classes']:
                random.shuffle(files['train_classes'][class_folder])
                files['train'].append(files['train_classes'][class_folder].pop(0))
                files['train_files'] += files['train_classes'][class_folder]

            # Shuffle the train files
            random.shuffle(files['train_files'])

            # Fill up to DataHolder.keep_train_data
            for train_name in files['train_files']:
                if len(files['train']) >= DataHolder.keep_train_data:
                    break
                files['train'].append(train_name)

            files['train'].sort()

        # delete unneeded keys
        del files['train_classes']
        del files['train_files']

        return files

    @staticmethod
    def create_symlinks():
        debug = False

        data_target_path = DataHolder.get_data_target_path()

        if os.path.isdir(data_target_path):
            raise AssertionError('Target path "%s" already exists.' % data_target_path)

        train_val = SymlinkCreator.get_files()

        for file in train_val['train']:
            target_file_path = DataHolder.get_target_file_path(file, DataHolder.name_train)
            link_file_path = DataHolder.get_link_file_path(file, DataHolder.name_train)
            SymlinkCreator.create_ntfs_symlink_file(link_file_path, target_file_path, debug)

        for file in train_val['val']:
            target_file_path = DataHolder.get_target_file_path(file, DataHolder.name_val)
            link_file_path = DataHolder.get_link_file_path(file, DataHolder.name_val)
            SymlinkCreator.create_ntfs_symlink_file(link_file_path, target_file_path, debug)


SymlinkCreator.create_symlinks()