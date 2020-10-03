#!/usr/bin/env python

# import mlks loader

# import some libraries
from flask import Flask

# import flask view classes
from mlks.helper.flask.view.predict import PredictView
from mlks.helper.flask.view.static import StaticView

# import fixtures
from fixtures import prediction as fake_prediction
from mlks_loader import root_dir
from helper.arguments import read_parameter

# import classes

# some configs
config_json_path: str = '%s-json-editor/data/mushrooms.json' % root_dir.replace('\\', '/')

# read parameters
parameter_language: str = read_parameter('string', 1, 'DE', ['DE', 'GB'])
parameter_number: int = read_parameter('integer', 2, 1)
parameter_output_type: bool = read_parameter('string', 3, 'simple', ['simple', 'full', 'raw'])

# create api service
template_folder = '%s/templates' % root_dir
static_folder = '%s/static' % root_dir
image_folder = '%s/img' % static_folder

# create flask app
app = Flask(__name__, template_folder=template_folder)


def do_post_hook(return_data, model):
    image_path = return_data['data']['image']['fullpath']

    # Do something with image path. Prediction? ;)
    print('Image path: %s' % image_path)

    prediction = fake_prediction

    # return fake prediction
    return prediction


model = None

# register and init PredictView
PredictView.set_config_json_path(config_json_path=config_json_path)
PredictView.set_parameter(parameter_language=parameter_language, parameter_number=parameter_number,
                          parameter_output_type=parameter_output_type)
PredictView.set_image_path(image_folder)
PredictView.set_hook('POST_prediction', {
    'lambda': do_post_hook,
    'arguments': [model]
})
PredictView.register(app, route_prefix='/v1.0/')

# register and init PublicView
StaticView.set_static_path(static_folder)
StaticView.register(app)

if __name__ == '__main__':
    app.run(debug=True)
