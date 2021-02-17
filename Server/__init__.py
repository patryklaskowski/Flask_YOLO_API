# Server

import cv2
import datetime
from Database import manager as db_manager
from flask import Flask, request, render_template, Response
from flask_restful import Resource, Api
import json
from markdown import markdown
import os
from TFLiteModel import Yolov4TensorFlowLiteModel
import time
from utils import load_yaml, timer, draw_bboxes, use_per_sec
from .utils import get_frame


app = Flask(__name__, template_folder='templates')
api = Api(app)

path = 'cfg.yaml'
cfg = load_yaml(path)
routes = cfg['endpoints']

# Documentation
@app.route('/')
@app.route(routes['doc'])
def doc():
    '''Documentation.'''
    path = 'README.md'
    with open(path, encoding='utf-8') as file:
        text = file.read()
    html = markdown(text)
    return html

# Get list of available models
# Models are stored in server's filesystem
@app.route(routes['model_available'], methods=['GET'])
def available_models():
    path = cfg['models']
    models = [model for model in os.listdir(path) if model.startswith('model')]
    return json.dumps(models)

# Upload new model to server's filesystem
@app.route(routes['model_upload'], methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        architecture = request.form['architecture']
        name = request.form['name']
        size = request.form['size']
        tflite_file = request.files['tflite_file']
        names_file = request.files['names_file']

        models_path = cfg['models']
        fmt = 'model-{architecture:s}-{name:s}-{size:s}'
        new_dirname = fmt.format(architecture=architecture,
                                 name=name,
                                 size=size)
        new_dirpath = os.path.join(models_path, new_dirname)

        if not names_file.filename.endswith('.names') or not tflite_file.filename.endswith('.tflite'):
            response = render_template('upload_fail.html',
                                        reason='Names file or tflite file has wrong format [.names, .tflite].')
        elif os.path.exists(new_dirpath):
            response = render_template('upload_fail.html',
                                        reason='This model is already existing.')
        else:
            os.makedirs(new_dirpath)
            tflite_path = os.path.join(new_dirpath, f'{new_dirname}.tflite')
            tflite_file.save(tflite_path)
            names_path = os.path.join(new_dirpath, f'{new_dirname}.names')
            names_file.save(names_path)
            response = render_template('upload_success.html')
        return response


# Run object detection on frame
class FrameObjectDetectorAPI(Resource):

    yolo_models = {}

    @staticmethod
    def draw_timestamp(frame):
        timestamp = datetime.datetime.now()
        cv2.putText(frame, timestamp.strftime(
            "%A %d %B %Y %I:%M:%S.%f %p"), (10, frame.shape[0] - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
        return frame

    print('>> FrameObjectDetectorAPI Class Created!')

    def __init__(self):
        self.connection = db_manager.connect()
        print(f'>> ObjectDetector object id no. {id(self)} created.')

    def get(self):
        return {'status': 'get method', 'model_name': 'model_name'}

    @use_per_sec
    @timer
    def post(self):
        header = request.headers
        shape = int(header['height']), int(header['width']), int(header['channels'])
        dtype = header['dtype']
        frame = get_frame(request, shape, dtype)
        weights = header['weights']
        threshold = float(header['threshold'])
        hostname = header['hostname']

        if weights.lower() != 'empty':
            if weights in self.yolo_models:
                model = self.yolo_models[weights]
            else:
                dirname = [model for model in os.listdir(cfg['models']) if weights in model]
                if len(dirname) == 1:
                    dirname = dirname[0]
                    tflite = os.path.join(cfg['models'], dirname, f'{dirname}.tflite')
                    names = os.path.join(cfg['models'], dirname, f'{dirname}.names')
                    model = Yolov4TensorFlowLiteModel(tflite, names)
                    self.yolo_models[weights] = model
                else:
                    print('No model like that')

            bboxes = model.predict(frame, threshold)
            classes = model.classes
            bboxes = [arr.tolist() for arr in bboxes]
            frame = draw_bboxes(frame, bboxes, classes)
            response = {'message': f'Predict {weights}.',
                        'bboxes': bboxes, 'classes': classes}
        else:
            response = {'message': 'No predict'}
        precision = 3
        timestamp = round(time.time() * 10**precision)
        frame = self.draw_timestamp(frame)
        db_manager.insert(self.connection, frame, timestamp, hostname)
        return response
api.add_resource(FrameObjectDetectorAPI, routes['object_detection'])


@app.route('/stream', methods=['GET'])
def streaming_page():
    return render_template('stream.html')

@app.route('/video_feed')
def video_feed():
    return Response(frame_generator('camera'),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def frame_generator(cam):
    path = cfg['images']
    today = datetime.date.today().strftime('%Y-%m-%d')
    dirpath = os.path.join(path, today)
    while True:
        filenames = os.listdir(dirpath)
        filenames = sorted(filenames, reverse=True)
        img_path = os.path.join(dirpath, filenames[1])
        frame = open(img_path, 'rb').read()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# class StreamingObjectDetector(Resource):
#     print('>> StreamingObjectDetector Class Created!')
#
#     single_endpoint = None
#
#     def post(self):
#         print('Recieved POST request!')
#         key = 'video_source'
#         data = request.json
#         if key in data:
#             self.single_endpoint = data[key]
#             # if endpoint not in self.endpoints: self.endpoints.append(endpoint)
#             print(f'New endpoint: {self.single_endpoint}.')
#             message = 'success'
#         else:
#             message = f'{key} agument not found in json request.'
#         return {'message': message}
#
#     def get(self):
#         return {'endpoints': self.endpoints}
# api.add_resource(StreamingObjectDetector, '/api/endpoint')
#
#
# ##########
