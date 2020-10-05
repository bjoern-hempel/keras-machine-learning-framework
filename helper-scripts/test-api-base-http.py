#!/usr/bin/env python

# import mlks loader
import sys
import ssl

# import ApiHTTPRequestHandler and HTTPServer
from mlks.http.api_http_request_handler import ApiHTTPRequestHandler
from http.server import HTTPServer

# import fixtures
from fixtures import prediction as fake_prediction
from mlks_loader import root_dir
from helper.arguments import read_parameter

from keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array

# InceptionV3
from keras.applications.inception_v3 import preprocess_input as InceptionV3PreprocessInput

# some configs
debug_mode: bool = False
config_json_path: str = '%s-json-editor/data/mushrooms.json' % root_dir.replace('\\', '/')

# read parameters
parameter_language: str = read_parameter('string', 1, 'DE', ['DE', 'GB'])
parameter_number: int = read_parameter('integer', 2, 1)
parameter_output_type: bool = read_parameter('string', 3, 'simple', ['simple', 'full', 'raw'])

# create api service
template_folder = '%s/templates' % root_dir
static_folder = '%s/static' % root_dir
image_folder = '%s/img' % static_folder

model_file: str = 'C:/Users/bjoern/data/processed/mushrooms/v1.0/model.best.10-0.78.h5'

# load model
print('Start load model')
if debug_mode:
    model = None
else:
    model = load_model(model_file)
print('Finish load model')


def do_post_hook(return_data: object, model: object, debug_mode: bool = True):

    # Some config
    verbose = True

    # Get image path
    image_path = return_data['data']['image']['fullpath']

    # Do something with image path. Prediction? ;)
    if verbose:
        print('return_data')
        print(return_data)
        print('model')
        print(model)
        print('Image path: %s' % image_path)

    # debug mode
    if debug_mode:
        return fake_prediction

    # load image
    image = load_img(
        image_path,
        target_size=(299, 299)
    )
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

    # predict image
    predicted_array = model.predict(InceptionV3PreprocessInput(image))

    predicted_array_sorted = sorted(
        range(len(predicted_array[0])), key=lambda i: predicted_array[0][i],
        reverse=True
    )

    return_data = {
        'classes': {},
        'data': []
    }

    # get classes
    classes = list(fake_prediction['classes'].keys())
    classes.sort()

    counter = 0
    for index in predicted_array_sorted:
        class_name = classes[index]
        return_data['classes'][class_name] = counter
        return_data['data'].append({
            'name': class_name,
            'prediction': round(predicted_array[0][index].item(), 8)
        })
        counter += 1

    prediction = return_data

    # return prediction
    return prediction


# set hooks
ApiHTTPRequestHandler.set_property('config_json_path', config_json_path)
ApiHTTPRequestHandler.set_property('parameter_language', parameter_language)
ApiHTTPRequestHandler.set_property('parameter_number', parameter_number)
ApiHTTPRequestHandler.set_property('parameter_output_type', parameter_output_type)
ApiHTTPRequestHandler.set_property('root_dir', root_dir)
ApiHTTPRequestHandler.set_property('template_folder', template_folder)
ApiHTTPRequestHandler.set_property('static_folder', static_folder)
ApiHTTPRequestHandler.set_property('image_folder', image_folder)
ApiHTTPRequestHandler.set_hook('POST_prediction', {
    'lambda': do_post_hook,
    'arguments': [model, debug_mode]
})

print('')
print('Ready for evaluation. Now upload some images...')
print('')

try:
    use_ssl = False
    port = 5000
    ip = '0.0.0.0'
    httpd = HTTPServer((ip, port), ApiHTTPRequestHandler)
    print('Webserver started on port %s:%d..' % (ip, port))

    # activate ssl (openssl req -newkey rsa:2048 -new -nodes -keyout key.pem -out csr.pem)
    if use_ssl:
        httpd.socket = ssl.wrap_socket(
            httpd.socket,
            keyfile='./key.pem',
            certfile='./csr.pem',
            server_side=True
        )

    httpd.serve_forever()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    httpd.socket.close()
