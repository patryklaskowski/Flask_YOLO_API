# server.py
print('> ./FlaskServer/server.py')

from flask import Flask, jsonify, request
import markdown
import os
import numpy as np
from FlaskServer.utils import print_info, get_shape, get_dtype, get_image
from TFLiteModel import Yolov4TensorFlowLiteModel

tflite = '/Users/patryklaskowski/Desktop/yolov4-coco-416.tflite'
names = '/Users/patryklaskowski/Desktop/coco.names'
model = Yolov4TensorFlowLiteModel(tflite, names)

# Flask instance
app = Flask(__name__)
root = os.path.dirname(app.root_path)

print_info(f'__name__ = {__name__}')
print_info(f'root = {root}')


@app.route('/', methods=['GET'])
def index():
    '''Present documentation.'''
    path =  os.path.join(root, 'README.md')
    html = markdown.markdownFromFile(path, encoding='utf8')
    return html


@app.route('/detect', methods=['POST'])
def detect():

    shape = get_shape(request)
    dtype = get_dtype(request)
    img = get_image(request, shape, dtype)

    bboxes = model.predict(img)
    classes = model.classes

    bboxes = [arr.tolist() for arr in bboxes]

    response = jsonify({'status': 'Image found.', 'bboxes': bboxes, 'classes': classes})

    return response
