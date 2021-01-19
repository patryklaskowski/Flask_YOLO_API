# utils.py
print('> ./FlaskServer/utils.py')

import numpy as np

def commandline_server():
    '''
    Makes server interactive. Useful for debugging and exploring.
    '''

    while True:
        ans = input('Input command: ')
        if ans == 'q': break
        try:
            print(eval(ans))
        except Exception as e:
            print(f'Exception occured: [{e}]\n')


def print_info(message):
    print(f'[INFO]: {message}')


def get_shape(request):
    rh = request.headers
    return (int(rh['height']), int(rh['width']), int(rh['channels']))


def get_dtype(request):
    return request.headers['dtype']


def get_image(request, shape, dtype):
    filestorage = request.files['image']
    file = filestorage.read()
    img = np.frombuffer(file, dtype=dtype)
    img = np.reshape(img, shape)
    return img
