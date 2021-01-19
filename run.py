# run.py
print('> ./run.py')

import sys
import os
sys.path.insert(0, os.path.abspath(os.curdir))

from FlaskServer.server import app

host = '0.0.0.0'
port = 5000
debug = True

app.run(host, port, debug)
