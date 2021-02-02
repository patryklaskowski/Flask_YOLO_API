# utils.py

import numpy as np

def get_frame(request, shape, dtype):
    filestorage = request.files['frame']
    file = filestorage.read()
    frame = np.frombuffer(file, dtype=dtype)
    frame = np.reshape(frame, shape)
    return frame
