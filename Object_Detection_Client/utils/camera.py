# camera.py

import cv2

class Camera:

    print('>> Camera Class Created!')

    def __init__(self, source=0):
        self.source = source
        self.cam = cv2.VideoCapture(source)
        print(f'>> Camera object id no. {id(self)} created.')

    def __repr__(self):
        return f'Camera({self.source})'

    def __del__(self):
        self.cam.release()

    def get_frame(self):
        success, frame = self.cam.read()
        assert success, 'Cannot get frame.'
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def release(self):
        self.cam.release()
