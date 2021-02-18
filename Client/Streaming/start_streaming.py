# Get username:
# id -un

# Connect via ssh (make sure ssh is enabled)
# ssh <username>@<ip>

# On RasberryPi:

# Enable ssh: https://www.raspberrypi.org/documentation/remote-access/ssh/README.md
# sudo systemctl enable ssh
# sudo systemctl start ssh

# OpenCv dependencies:
# sudo apt-get -y install libhdf5-dev libhdf5-serial-dev libhdf5-100
# sudo apt-get -y install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
# sudo apt-get -y install libatlas-base-dev
# sudo apt-get -y install libjasper-dev

# IP address:
# hostname -I

# Add user to video usergroup:
# sudo usermod -a -G video pi

# Available cameras:
# ls -l /dev/video*

import argparse
import cv2
import time
from flask import Flask, Response

app = Flask(__name__)

class Camera:
    
    def __init__(self, src):
        self.src = int(src) if len(str(src)) == 1 else str(src)
        self.cam = cv2.VideoCapture(self.src)
        time.sleep(1)
        print(f'Camera instance id: {id(self)} initialized.')
    
    def get_frame(self, size):
        success, frame = self.cam.read()
        if not success: raise Exception('Cannot get frame')
        if size > 0:
            frame = cv2.resize(frame, (size, size))
        return frame
    
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-src', '--source', default='0')
    parser.add_argument('--size', default=0, type=int)
    parser.add_argument('-p', '--port', default=5005, type=int)
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    return args
    
    
def generate_frames(cam):
    global args
    while True:
        frame = cam.get_frame(args.size)
        _, encoded = cv2.imencode('.jpg', frame)
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded) + b'\r\n')
    
@app.route('/')
def video_feed():
    cam = Camera(0)
    return Response(generate_frames(cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

    
if __name__ == '__main__':
    args = parse_arguments()
    app.run(host='0.0.0.0', port=args.port, debug=args.debug, threaded=False)
