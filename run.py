# run.py

from Server import app

host = '0.0.0.0'
port = 5000
debug = True

if __name__ == '__main__':
    app.run(host, port, debug)
