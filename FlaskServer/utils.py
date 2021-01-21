# utils.py

import numpy as np
import time

def get_frame(request, shape, dtype):
    filestorage = request.files['frame']
    file = filestorage.read()
    frame = np.frombuffer(file, dtype=dtype)
    frame = np.reshape(frame, shape)
    return frame


def timer(func):
    '''Measure function runtime.'''
    def inner_function(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        stop = time.perf_counter()
        elapsed_time = round(stop - start, 4)
        return {'result': result, 'time': elapsed_time}
    return inner_function
