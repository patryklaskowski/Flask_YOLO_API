# Server

from Database import manager as db_manager
from flask import Flask, request
from flask_restful import Resource, Api
from markdown import markdown
from TFLiteModel import yolov4
import time
from utils import load_yaml, timer, draw_bboxes
from .utils import get_frame


app = Flask(__name__)
api = Api(app)

path = 'cfg.yaml'
cfg = load_yaml(path)


@app.route('/')
@app.route('/doc')
def doc():
    '''Documentation.'''
    path = 'README.md'
    with open(path, encoding='utf-8') as file:
        text = file.read()
    html = markdown(text)
    return html


class ObjectDetector(Resource):

    print('>> ObjectDetector Class Created!')

    def __init__(self):
        print(f'>> ObjectDetector object id no. {id(self)} created.')

    def get(self, model_name):
        return {'status': 'get method', 'model_name': model_name}


    @timer
    def post(self, model_name, treshold=0.4):
        header = request.headers
        shape = int(header['height']), int(header['width']), int(header['channels'])
        dtype = header['dtype']
        frame = get_frame(request, shape, dtype)

        bboxes = yolov4.predict(frame, treshold)
        classes = yolov4.classes
        bboxes = [arr.tolist() for arr in bboxes]

        ############
        frame = draw_bboxes(frame, bboxes, classes)
        precision = 3
        timestamp = round(time.time() * 10**precision)
        host = 'my_host_13'
        connection = db_manager.connect()
        db_manager.insert(connection, frame, timestamp, host)
        ############

        response = {'bboxes': bboxes, 'classes': classes}
        return response
api.add_resource(ObjectDetector, '/api/detect/<model_name>/<float:treshold>')
