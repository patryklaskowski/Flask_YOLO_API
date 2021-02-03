# utils.py

import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print(">> Connection to SQLite DB successful")
    except Error as e:
        print(f">> The error '{e}' occurred while creating connection.")
    return connection


def execute_query(connection, query, name=''):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print(f">> Query {name} executed successfully")
    except Error as e:
        print(f">> The error '{e}' occurred while executing query.")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except Error as e:
        print(f">> The error '{e}' occurred")
    return result
