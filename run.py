# run.py

import sys
import os

project_root_path = os.path.abspath(os.curdir)
sys.path.insert(0, project_root_path)

from FlaskServer.server import app

host = '0.0.0.0'
port = 5000
debug = True

app.run(host, port, debug)
