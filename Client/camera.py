# camera.py

import cv2

class Camera:

    def __init__(self, source=0):
        self.source = source
        self.cam = cv2.VideoCapture(source)

    def __del__(self):
        self.cam.release()

    def get_frame(self):
        success, frame = self.cam.read()
        if success:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGR)

        return frame
