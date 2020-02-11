import os
import sys
import random
import pprint
import json
import shutil
from typing import Dict, Any

pp = pprint.PrettyPrinter(indent=4)
random.seed(1337)


class ConfusionMatrixBuilder:
    # Data path where the data can be found
    path = None

    # json file name
    evaluation_json_file = 'evaluation.json'

    # json file name
    data_json_file = 'data.json'

    # model json file
    model_json_file = 'model.inceptionv3.json'

    # The path to save the pgf files
    latex_path = 'F:/latex/version-3/images/pgf'

    # the number of wanted image files in each class
    number_target_per_class = 1000

    # latex save path
    latex_path = 'F:/latex/pages/python-%s.tex'

    latex_target_path = 'F:/latex/images/evaluation-images'

    def __init__(self, paths):
        self.paths = paths

    @staticmethod
    def get_class_name(class_name):
        return class_name.replace('_', ' ').capitalize().title()

    def get_class_accuracy_array(self, class_names, top_1_classified_1, not_top_1_classified_1):
        class_accuracy: Dict[Any, Dict[str, float]] = {}
        for class_name in class_names:
            class_accuracy[class_name] = {
                'number-correct': 0,
                'number-incorrect': 0,
                'accuracy': 0
            }

        for name in top_1_classified_1:
            class_name = os.path.dirname(name)
            class_accuracy[class_name]['number-correct'] += 1
        for name in not_top_1_classified_1:
            class_name = os.path.dirname(name)
            class_accuracy[class_name]['number-incorrect'] += 1

        for class_name in class_accuracy:
            number_correct = class_accuracy[class_name]['number-correct']
            number_all = class_accuracy[class_name]['number-correct'] + class_accuracy[class_name]['number-incorrect']
            class_accuracy[class_name]['accuracy'] = number_correct / number_all

        return class_accuracy

    def build(self):
        evaluation_json_file_absolute_1 = '%s/%s' % (self.paths[0], self.evaluation_json_file)
        data_json_file_absolute_1 = '%s/%s' % (self.paths[0], self.data_json_file)
        model_json_file_absolute_1 = '%s/%s' % (self.paths[0], self.model_json_file)
        evaluation_json_file_absolute_2 = '%s/%s' % (self.paths[1], self.evaluation_json_file)
        data_json_file_absolute_2 = '%s/%s' % (self.paths[1], self.data_json_file)
        model_json_file_absolute_2 = '%s/%s' % (self.paths[1], self.model_json_file)

        if not os.path.isfile(evaluation_json_file_absolute_1):
            raise AssertionError('The given json file "%s" does not exist.' % evaluation_json_file_absolute_1)
        if not os.path.isfile(evaluation_json_file_absolute_2):
            raise AssertionError('The given json file "%s" does not exist.' % evaluation_json_file_absolute_2)

        with open(data_json_file_absolute_1) as json_file:
            data_1 = json.load(json_file)
        with open(data_json_file_absolute_2) as json_file:
            data_2 = json.load(json_file)

        with open(evaluation_json_file_absolute_1) as json_file:
            data_from_evaluation_file_1 = json.load(json_file)
        with open(evaluation_json_file_absolute_2) as json_file:
            data_from_evaluation_file_2 = json.load(json_file)

        with open(model_json_file_absolute_1) as json_file:
            data_from_model_file_1 = json.load(json_file)
        with open(model_json_file_absolute_2) as json_file:
            data_from_model_file_2 = json.load(json_file)

        top_1_classified_1 = data_from_evaluation_file_1['top_k']['correctly_classified_top_1']
        not_top_1_classified_1 = data_from_evaluation_file_1['top_k']['incorrectly_classified_top_1']
        top_1_classified_2 = data_from_evaluation_file_2['top_k']['correctly_classified_top_1']
        not_top_1_classified_2 = data_from_evaluation_file_2['top_k']['incorrectly_classified_top_1']

        config_1 = data_1['total']['config']
        best_train_1 = data_1['total']['best-train']
        config_2 = data_2['total']['config']
        best_train_2 = data_2['total']['best-train']

        class_accuracy_1 = self.get_class_accuracy_array(
            data_from_evaluation_file_1['classes'],
            top_1_classified_1,
            not_top_1_classified_1
        )
        class_accuracy_2 = self.get_class_accuracy_array(
            data_from_evaluation_file_2['classes'],
            top_1_classified_2,
            not_top_1_classified_2
        )

        for class_name in class_accuracy_1:
            print('%s (%d -> %d): %.2f -> %.2f' % (
                class_name,
                len(data_from_model_file_1['environment']['files']['train'][class_name]),
                len(data_from_model_file_2['environment']['files']['train'][class_name]),
                class_accuracy_1[class_name]['accuracy'],
                class_accuracy_2[class_name]['accuracy']
            ))


confusion_matrix_builder = ConfusionMatrixBuilder([
    'F:/data/processed/experiments/data_augmentation/inceptionv3/food-50-80-20-without-data-augmentation',
    'F:/data/processed/experiments/data_augmentation/inceptionv3/food-50-80-20-data-augmentation-1000'
])
confusion_matrix_builder.build()
