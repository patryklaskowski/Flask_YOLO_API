# client.py

import requests
from .camera import Camera


class API_Client:

    url_structure = 'http://{ip}:5000/api/detect/{weights}/{threshold}'
    client_auth_code = 'success'
    print('>> API_Client Class Created!')


    def __init__(self, ip='0.0.0.0', source=0):
        self.source = source
        self.ip = ip
        self.cam = Camera(source)
        print(f'>> API_Client object id no. {id(self)} created.')


    def post_frame(self, weights='coco', threshold=0.4):
        '''
        ______
        INPUT:
        weights: string (default: 'coco')
        threshold: float (default: 0.4)
        ______
        OUTPUT:
        response, frame
        '''
        url = API_Client.url_structure.format(ip=self.ip, weights=weights, threshold=threshold)
        frame = self.cam.get_frame()
        files = self.__create_files(frame, msg='Object_detection')
        headers = self.__create_headers(frame.shape, frame.dtype.name)
        response = requests.post(url, files=files, headers=headers)
        return response, frame


    def __create_files(self, frame, msg='Object_detection'):
        return {'frame': frame.tostring(),
                'msg': msg}


    def __create_headers(self, shape, dtype):
        height, width, channels = shape
        return {'client_auth': API_Client.client_auth_code,
                'height': str(height),
                'width': str(width),
                'channels': str(channels),
                'dtype': str(dtype)}
