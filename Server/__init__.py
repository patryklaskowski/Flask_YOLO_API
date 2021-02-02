# Server

# from Database.manager import DatabaseManager
from flask import Flask, request
from flask_restful import Resource, Api
from markdown import markdown
from TFLiteModel import yolov4
from utils import load_yaml, timer_decorator
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

    # db_manager = DatabaseManager(cfg['database_path'])
    print('>> ObjectDetector Class Created!')

    def __init__(self):
        print(f'>> ObjectDetector object id no. {id(self)} created.')

    def get(self, model_name):
        return {'status': 'get method', 'model_name': model_name}


    @timer_decorator
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
