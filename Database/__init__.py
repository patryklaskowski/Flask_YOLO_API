# Database

from .manager import DatabaseManager
from .utils import create_connection
import os
from utils import load_yaml


path = 'cfg.yaml'
cfg = load_yaml(path)


db_path = cfg['database_path']
images_path = cfg['images_path']

if not os.path.exists(images_path):
    os.makedirs(images_path)
    print(f'Created images path: {images_path}.')


manager = DatabaseManager(db_path, images_path)
