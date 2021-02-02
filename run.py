# run.py

from Server import app


host = '0.0.0.0'
port = 5000
debug = True

print('\n\n-------------\n\n')
app.run(host, port, debug)
