import argparse
import cv2
from flask import Flask, Response

from camera import Camera

flask_app = Flask(__name__)

def generate_frames(cam, size):
    while True:
        encoded_frame = cam.get_frame(size, encode=True)

        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encoded_frame) + b'\r\n')


@flask_app.route('/')
def video_feed():

    global args

    cam = Camera(args.source)

    return Response(generate_frames(cam, args.size),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-src', '--source', default='0')
    parser.add_argument('--size', default=0, type=int)
    parser.add_argument('-p', '--port', default=5005, type=int)
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()

    return args

if __name__ == '__main__':
    args = parse_arguments()
    flask_app.run(host='0.0.0.0',
                  port=args.port,
                  debug=args.debug,
                  threaded=True)
