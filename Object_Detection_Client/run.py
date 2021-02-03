# run.py

import argparse
from utils.client import API_Client

parser = argparse.ArgumentParser()
parser.add_argument('-ip', '--ipaddr',
                    help='Server ip address.',
                    default='0.0.0.0')
parser.add_argument('-n', '--frames',
                    help='Max number of frames to send',
                    type=int,
                    default=0)
parser.add_argument('-w', '--weights',
                    help='Object detection weights to run.',
                    default='coco')
parser.add_argument('-s', '-src', '--source',
                    help='Camera source.',
                    default='0')
parser.add_argument('-t', '--threshold',
                    help='Object detection probability threshold.',
                    type=float,
                    default=0.4)
args = parser.parse_args()

ip = args.ipaddr
source = args.frames
weights = args.weights
max_frames = args.source
threshold = args.threshold

client = API_Client(ip, source)
while True:
    key = input('Press Enter to post frame.')
    if key.lower()=='q':
        break
    try:
        response, frame = client.post_frame(weights, threshold)
        print(f'status_code: {response.status_code}')
        response_dict = response.json()
        if 'time' in response_dict:
            print(f'Prediction took: {response_dict["time"]} second(s).')
    except Exception as e:
        print(f'----------------\nException occured:\n--------\n{e}\n\n----------------')
