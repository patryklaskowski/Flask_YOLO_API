# client.py

from .camera import Camera
import requests


class Client:

    url_structure = 'http://localhost:5000/api/detect/%s/%s'
    client_auth_code = 'success'

    def __init__(self, source):
        self.source = source
        self.cam = Camera(source)


    def post_frame(self, frame, treshold=0.4):
        url = url_structure % ('coco', treshold)
        frame = self.cam.get_frame()
        files = self.__create_files(frame, msg='Object_detection')
        headers = self.__create_headers(frame.shape, frame.dtype.name
        
        return requests.post(url, files=files, headers=headers)


    def __create_files(self, frame, msg='Object_detection'):
        return {'frame': frame.tostring(),
                'msg': msg}


    def __create_headers(self, shape, dtype):
        height, width, channels = shape
        return {'client_auth': client_auth_code,
                'height': str(height),
                'width': str(width),
                'channels': str(channels),
                'dtype': str(dtype)}
