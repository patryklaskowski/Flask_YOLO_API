# client.py

import requests
from .camera import Camera


class API_Client:

    URL_FMT = 'http://{ip}:5000/api/detect'
    CLIENT_AUTH_CODE = 'success'
    print('>> API_Client Class Created!')


    def __init__(self, ip='0.0.0.0', source=0):
        self.source = source
        self.ip = ip
        self.cam = Camera(source)
        print(f'>> API_Client object id no. {id(self)} created.')


    def post_frame(self, hostname, weights='coco', size=None, threshold=0.4):
        '''
        ______
        INPUT:
        weights: string (default: 'coco')
        size: int (default: None)
        threshold: float (default: 0.4)
        ______
        OUTPUT:
        response, frame
        '''
        url = self._create_url(self.ip)
        frame = self.cam.get_frame(size)
        files = self._create_files(frame, msg='Object_detection')
        headers = self._create_headers(weights, threshold, frame.shape, frame.dtype.name, hostname)
        response = requests.post(url, files=files, headers=headers)
        return response, frame

    def _create_url(self, ip):
        return API_Client.URL_FMT.format(ip=ip)

    def _create_files(self, frame, msg='Object_detection'):
        return {'frame': frame.tostring(),
                'msg': msg}


    def _create_headers(self, weights, threshold, shape, dtype, hostname):
        height, width, channels = shape
        return {'client_auth': API_Client.CLIENT_AUTH_CODE,
                'height': str(height),
                'width': str(width),
                'channels': str(channels),
                'dtype': str(dtype),
                'weights': str(weights),
                'threshold': str(threshold),
                'hostname': str(hostname)}
