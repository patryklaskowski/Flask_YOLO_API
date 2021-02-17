# start_streaming.py

import cv2
import datetime
from flask import Flask, Response
from imutils.video import VideoStream
import time

app = Flask(__name__)

def edit(frame):
    timestamp = datetime.datetime.now()
    cv2.putText(frame, timestamp.strftime(
        "%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
    return frame

def generate(cam):
    while True:
        start_time = time.perf_counter()
        frame = cam.read()
        frame = edit(frame)
        _, encodedImage = cv2.imencode('.jpg', frame)
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
            bytearray(encodedImage) + b'\r\n')

@app.route('/')
@app.route('/video')
def video_feed():
	return Response(generate(cam),
        mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    cam = VideoStream(src=0).start()
    time.sleep(1)
    app.run(host='0.0.0.0', port=5005, debug=True,
		threaded=True, use_reloader=True)
    cam.stop()
