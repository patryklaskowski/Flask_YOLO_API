# manager.py

import datetime
import os
from PIL import Image
import time
from utils import singleton
from .utils import create_connection, execute_query


@singleton
class DatabaseManager:

    def __init__(self, db_path, images_path):
        self.db_path = db_path
        self.images_path = images_path


    def connect(self):
        connection = create_connection(self.db_path)
        self.__create_frames_table(connection)
        return connection

    def __repr__(self):
        return f'DatabaseManager({self.path}, {self.images_path})'

    def __save_frame(self, frame, timestamp):
        format = '%Y-%m-%d'
        date = datetime.datetime.strftime(datetime.date.today(), format)
        path = os.path.join(self.images_path, date)
        os.makedirs(path, exist_ok=True)
        filename = f'frame_{timestamp}.jpg'
        filepath = os.path.join(path, filename)
        img = Image.fromarray(frame)
        img.save(filepath)
        return filepath



    def __create_frames_table(self, connection):
        create_table_schema = '''
        CREATE TABLE IF NOT EXISTS frames (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER NOT NULL,
            host TEXT,
            path TEXT NOT NULL
        );
        '''
        execute_query(connection, create_table_schema, 'create_table_schema')

    def __insert_frame(self, connection, timestamp, host, path):
        insert_shema = '''
        INSERT INTO
            frames (timestamp, host, path)
        VALUES
            ("{timestamp}", "{host}", "{path}");
        '''
        execute_query(connection, insert_shema.format(timestamp=timestamp, host=host, path=path))

    def insert(self, connection, frame, timestamp, host):
        path = self.__save_frame(frame, timestamp)
        self.__insert_frame(connection, timestamp, host, path)
