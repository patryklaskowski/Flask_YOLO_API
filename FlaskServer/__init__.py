# __init__.py
# Runs when import FlaskServer package

print('[INFO]: ./FlaskServer/__init__.py is running.')

from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import markdown
import os
import numpy as np

# Flask instance
print(f'[INFO]: __name__ = {__name__}')
app = Flask(__name__)

@app.route('/')
def index():
    '''Present documentation.'''
    # Read README.md file
    print(f'[INFO]: os.path.dirname(app.root_path) = {os.path.dirname(app.root_path)}')
    with open(os.path.dirname(app.root_path) + '/README.md') as readme:
         content = readme.read()
    # Convert to HTML
    return markdown.markdown(content)

# curl -X POST -F "file=@data/street.jpg" http://localhost:5000/upload
@app.route('/detect', methods=['POST'])
def detect():

    if request.json and 'image' in request.json:
        img = np.array(request.json['image'])
        response = jsonify({"status":f"ok, img found in json: {img.shape}"})

    elif request.files and 'image' in request.files:
        print('\nRecieved File!\n')
        image = Image.open(request.files['image'])
        print(f'\nIage size: {image.size}')
        print('OK\n')
        response = jsonify({"status":f"ok, img found in files: {image.size}"})
    else:
        response = jsonify({"status":"nothing"})

    return response
