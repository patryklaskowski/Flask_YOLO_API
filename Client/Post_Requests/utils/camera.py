# camera.py

import cv2
import os
import time

class Camera:

    print('>> Camera Class Created!')

    def __init__(self, source=0):
        self.source = int(source) if len(source) == 1 else source
        self.cam = cv2.VideoCapture(self.source)
        time.sleep(0.5)
        print(f'>> Camera object id no. {id(self)} created.')

    def __repr__(self):
        return f'Camera({self.source})'

    def get_frame(self, size=None, save_path=None):
        success, frame = self.cam.read()
        assert success, 'Failed getting frame.'
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if size:
            frame = cv2.resize(frame, (size, size))
        if save_path is not None:
            Camera.save_frame(frame, save_path)
        return frame

    @staticmethod
    def save_frame(frame, path='.'):
        assert os.path.exists(path), 'Provided save_path does not exist.'
        timestamp = round(time.time() * 100)
        filename = f'frame_{timestamp}.jpg'
        filepath = os.path.join(path, filename)
        # To overcome color swap while saving image with OpenCv
        cv2.imwrite(filepath, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def release(self):
        self.cam.release()
