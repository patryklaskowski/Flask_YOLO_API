# post_request.py

from .client import Client
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--number',
                    help='Number of frames to send',
                    type=int,
                    default=0)
parser.add_argument('-m', '--model',
                    help='Model name to run.',
                    default='coco')
parser.add_argument('-s', '-src', '--source',
                    help='Camera source.',
                    default='0')
args = parser.parse_args()

client = Client()
