# manager.py

from .utils import create_connection


class DatabaseManager:

    def __init__(self, path):
        self.path = path
        connection = create_connection(path)

    def __repr__(self):
        return f'DatabaseManager({self.path})'
