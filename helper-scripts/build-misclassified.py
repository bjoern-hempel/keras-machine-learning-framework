import os
import sys
import random
import pprint
import json
import shutil


pp = pprint.PrettyPrinter(indent=4)
random.seed(1337)


class ConfusionMatrixBuilder:
    # Data path where the data can be found
    path = None

    # json file name
    evaluation_json_file = 'evaluation.json'

    # json file name
    data_json_file = 'data.json'

    # The path to save the pgf files
    latex_path = 'F:/latex/version-3/images/pgf'

    # the number of wanted image files in each class
    number_target_per_class = 1000

    # latex save path
    latex_path = 'F:/latex/pages/python-%s.tex'

    latex_target_path = 'F:/latex/images/evaluation-images'

    latex_template_introduction = """
\\section{%s}

%s\\\\

\\raggedright
\\begin{tabularx}{\\textwidth}{X r}
    \\textbf{Used dataset} & \\texttt{%s}\\\\
    \\textbf{Experiment} & \\texttt{%s}
\end{tabularx}

\\raggedright
\\vspace{6pt}
\\begin{tabularx}{\\textwidth}{X r}
    \\textbf{Number of trained files} & 49.943\\\\
    \\textbf{Number of validated files} & 2.953
\end{tabularx}

\\raggedright
\\vspace{6pt}
\\begin{tabularx}{\\textwidth}{X r}
    \\textbf{Used CNN model} & %s\\\\
    \\textbf{Used weights (transfer learning)} & %s
\end{tabularx}

\\raggedright
\\vspace{6pt}
\\begin{tabularx}{\\textwidth}{X r}
    \\textbf{Accuracy} & %.2f \%%\\\\
    \\textbf{Best epoch} & %d
\end{tabularx}
    """

    latex_template_description = """
        In the following %d images are listed, which are not correctly classified in
        the top-1 or top-5 classification.
    """

    latex_template_chapter = """
\\subsection{%s}
    """

    latex_template_item = """
\\subsubsection{%s}

\\begin{minipage}[t]{0.4\\textwidth}
	\\vspace{0pt}
	\\includegraphics[width=\\linewidth]{%s}
\\end{minipage}
\\hfill
\\begin{minipage}[t]{0.5\\textwidth}
	\\vspace{0pt}\\raggedright
	\\begin{tabularx}{\\textwidth}{X r}
		\\small \\textbf{Real class} & \\small %s\\\\
		\\small \\textbf{Predicted class} & \\small %s\\\\
		\\small \\textbf{Predicted accuracy} & \\small %.2f \%%
    \end{tabularx}\\\\
    
    \\vspace{6pt}
	\\begin{tabularx}{\\textwidth}{X r}
        \\small \\textbf{Top-5} & \\small \\textbf{Accuracy} \\\\
        \\hline
		%s
    \end{tabularx}
\\end{minipage}
    """

    def __init__(self, path):
        self.path = path

    def get_latex(self, path, real_class, prediction_class, prediction_accuracy, top_5_cells):

        latex_string = self.latex_template_item % (
            path.replace('_', '\\textunderscore '),
            'images/evaluation-images/%s' % path,
            self.get_class_name(real_class),
            self.get_class_name(prediction_class),
            prediction_accuracy,
            top_5_cells
        )

        return latex_string

    @staticmethod
    def get_class_name(class_name):
        return class_name.replace('_', ' ').capitalize().title()

    def build(self):
        evaluation_json_file_absolute = '%s/%s' % (self.path, self.evaluation_json_file)
        data_json_file_absolute = '%s/%s' % (self.path, self.data_json_file)

        if not os.path.isfile(evaluation_json_file_absolute):
            raise AssertionError('The given json file "%s" does not exist.' % evaluation_json_file_absolute)

        with open(data_json_file_absolute) as json_file:
            data = json.load(json_file)

        with open(evaluation_json_file_absolute) as json_file:
            data_from_evaluation_file = json.load(json_file)

            not_top_1_classified = data_from_evaluation_file['top_k']['incorrectly_classified_top_1']
            not_top_5_classified = data_from_evaluation_file['top_k']['incorrectly_classified_top_5']
            top_5_classified = data_from_evaluation_file['top_k']['correctly_classified_top_5']
            not_top_1_and_not_top_5_classified = [x for x in not_top_1_classified if x not in top_5_classified]

            classes = data_from_evaluation_file['classes']

            current_class = None

            config = data['total']['config']
            best_train = data['total']['best-train']

            latex_string = self.latex_template_introduction % (
                'Misclassified images',
                self.latex_template_description % len(not_top_1_and_not_top_5_classified),
                config['data']['data-path'],
                os.path.basename(self.path).replace('_', '\\textunderscore '),
                config['transfer-learning']['transfer-learning-model'],
                config['transfer-learning']['weights'].title(),
                best_train['val']['accuracy-top-1'] * 100,
                best_train['epoch']
            )

            for file_path_relative in not_top_1_and_not_top_5_classified:
                file_path_absolute = '%s/%s' % (data_from_evaluation_file['root_path'], file_path_relative)
                file_path_absolute_latex = '%s/%s' % (self.latex_target_path, file_path_relative)
                prediction_class = data_from_evaluation_file['data'][file_path_relative]['prediction_class']
                real_class = data_from_evaluation_file['data'][file_path_relative]['real_class']
                evaluation_data = data_from_evaluation_file['data'][file_path_relative]
                prediction_accuracy = evaluation_data['prediction_accuracy']
                prediction_overview_array = evaluation_data['prediction_overview_array']
                top_5_indices = sorted(
                    range(len(prediction_overview_array)), key=lambda i: prediction_overview_array[i],
                    reverse=True
                )[:5]

                top_5_cells = ''
                counter = 0
                for top_5_index in top_5_indices:
                    if top_5_cells != '':
                        top_5_cells += '\\\\'

                    counter += 1
                    top_5_cells += '\\small %d) %s & \\small %.2f \\%%' % (
                        counter,
                        self.get_class_name(classes[top_5_index]),
                        prediction_overview_array[top_5_index] * 100
                    )

                # check if folder exists
                if not os.path.exists(os.path.dirname(file_path_absolute_latex)):
                    os.mkdir(os.path.dirname(file_path_absolute_latex))

                # copy file
                shutil.copyfile(file_path_absolute, file_path_absolute_latex)

                if current_class != real_class:
                    current_class = real_class
                    latex_string += self.latex_template_chapter % self.get_class_name(current_class)

                latex_string += self.get_latex(
                    file_path_relative,
                    real_class,
                    prediction_class,
                    prediction_accuracy,
                    top_5_cells
                )

                # print('%-50s %s -> %s (%.2f%%)' % (
                #     '%s:' % file_path_relative, real_class, prediction_class, prediction_accuracy
                # ))
                # for top_5_index in top_5_indices:
                #     print('- %s: %.2f%%' % (classes[top_5_index], prediction_overview_array[top_5_index] * 100))

        # save latex file
        latex_file = open(self.latex_path % os.path.basename(self.path), "w")
        latex_file.write(latex_string)
        latex_file.close()


path_to_use = sys.argv[1]
confusion_matrix_builder = ConfusionMatrixBuilder(path_to_use)
confusion_matrix_builder.build()
