# server.py

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from markdown import markdown
import os
import numpy as np
from FlaskServer.utils import print_info, get_shape, get_dtype, get_image
from TFLiteModel.model import Yolov4TensorFlowLiteModel
import yaml
import time

with open('cfg.yaml') as file:
    cfg = yaml.safe_load(file)

model_path = cfg['model_path']
names_path = cfg['names_path']
model = Yolov4TensorFlowLiteModel(model_path, names_path)

app = Flask(__name__)
project_root_path = os.path.dirname(app.root_path)

print_info(f'__name__ = {__name__}')
print_info(f'project_root_path = {project_root_path}')


@app.route('/', methods=['GET'])
def index():
    '''Present documentation.'''
    path =  os.path.join(project_root_path, 'README.md')
    with open(path, encoding='utf-8') as file:
        text = file.read()
    html = markdown(text)
    return html


@app.route('/detect', methods=['POST'])
def detect():

    start = time.perf_counter()
    shape = get_shape(request)
    dtype = get_dtype(request)
    img = get_image(request, shape, dtype)
    bboxes = model.predict(img)
    classes = model.classes
    stop = time.perf_counter()
    time_running = stop - start

    bboxes = [arr.tolist() for arr in bboxes]

    response = jsonify({'status': 'Image found.', 'bboxes': bboxes, 'classes': classes, 'time': time_running})

    return response


api = Api(app)

class ObjectDetector(Resource):
    def get(self, model_name):
        return {'status': 'get method', 'model_name':model_name}

    def post(self, model_name):
        print(f'\n\n{model_name}\n\n')
        shape = get_shape(request)
        dtype = get_dtype(request)
        img = get_image(request, shape, dtype)
        bboxes = model.predict(img)
        classes = model.classes
        bboxes = [arr.tolist() for arr in bboxes]

        response = {'bboxes': bboxes, 'classes': classes}

        return response, 201
api.add_resource(ObjectDetector, '/api/detect/<model_name>')
