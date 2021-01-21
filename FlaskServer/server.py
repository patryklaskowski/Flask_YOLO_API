# server.py

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from markdown import markdown
import os
import numpy as np
from .utils import get_frame, timer
from TFLiteModel.model import yolov4
import time
import yaml
from Database.manager import DatabaseManager


app = Flask(__name__)
api = Api(app)

project_root_path = os.path.dirname(app.root_path)


with open('cfg.yaml') as file:
    cfg = yaml.safe_load(file)


@app.route('/')
@app.route('/docs')
def docs():
    '''Present documentation.'''
    path =  os.path.join(project_root_path, 'README.md')
    with open(path, encoding='utf-8') as file:
        text = file.read()
    html = markdown(text)

    return html


class ObjectDetector(Resource):

    db_manager = DatabaseManager(cfg['database_path'])
    print('>> ObjectDetector: Class Instance Initialization Success!')

    def get(self, model_name):
        return {'status': 'get method', 'model_name':model_name}


    @timer
    def post(self, model_name, treshold=0.4):
        header = request.headers
        shape = int(header['height']), int(header['width']), int(header['channels'])
        dtype = header['dtype']
        frame = get_frame(request, shape, dtype)
        bboxes = yolov4.predict(frame, treshold)
        classes = yolov4.classes
        bboxes = [arr.tolist() for arr in bboxes]
        response = {'bboxes': bboxes, 'classes': classes}

        return response

api.add_resource(ObjectDetector, '/api/detect/<model_name>/<float:treshold>')
