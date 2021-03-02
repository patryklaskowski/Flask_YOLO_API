import cv2
import time

class Camera:

    def __init__(self, src):
        self.src = int(src) if len(str(src)) == 1 else str(src)
        self.cam = cv2.VideoCapture(self.src)
        time.sleep(1)
        print(f'Camera id: {id(self)} initialized.')

    def get_frame(self, size, encode=False):
        success, frame = self.cam.read()
        if not success: raise Exception('Get frame failed.')

        if size > 0:
            frame = cv2.resize(frame, (size, size))

        if encode:
            _, frame = cv2.imencode('.jpg', frame)

        return frame
