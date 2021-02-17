# run.py

import argparse
from utils import API_Client, print_settings

parser = argparse.ArgumentParser()

parser.add_argument('-ip', '--ipaddr',
                    help='Server ip address.',
                    default='0.0.0.0')
parser.add_argument('-n', '-max', '--max_frames',
                    help='Max number of frames to send',
                    type=int,
                    default=0)
parser.add_argument('-w', '--weights',
                    help='Object detection weights to run.',
                    default='coco')
parser.add_argument('-s', '-src', '--source',
                    help='Camera source.',
                    default='0')
parser.add_argument('--size',
                    help='Input size.',
                    type=int)
parser.add_argument('-t', '--threshold',
                    help='Object detection probability threshold.',
                    type=float,
                    default=0.4)
parser.add_argument('-ep', '-enter', '--enterpress', help='If provided, enter key press send new frame.',
                    action='store_true')

args = parser.parse_args()

hostname = 'IAMHOST'

ip = args.ipaddr
max_frames = args.max_frames
weights = args.weights
source = args.source
size = args.size
threshold = args.threshold
is_enterpress = args.enterpress

print_settings(args)
assert max_frames >= 0, 'Frames argument must be positive.'

client = API_Client(ip, source)

fmt = '| {count:5s} | {code:5s} | {elapsed:6s} | {ups:5s} | {message:20s} |'
end = ' ' if is_enterpress else '\n'
print(fmt.format(count='Count', code='Code', elapsed='Elaps.', ups='Req/s', message='Action'), end=end)

counter = 0
while True:
    if is_enterpress:
        key = input('Press Enter to post new frame ["q" to quit].')
        if key.lower()=='q': break
    try:
        response, frame = client.post_frame(hostname, weights, size, threshold)

        counter += 1
        code = response.status_code
        elapsed = 'x'
        ups = 'x'

        if code == 200:
            response_dict = response.json()
            elapsed = str(round(response_dict["time"], 2)) if 'time' in response_dict else 'x'
            ups = str(response_dict["use_per_sec"]) if 'use_per_sec' in response_dict else 'x'

        message = response_dict["message"]
        print(fmt.format(count=str(counter), code=str(code), elapsed=elapsed, ups=ups, message=message), end=end)
    except Exception as e:
        print(f'----------------\nException occured:\n--------\n{e}\n\n----------------')

    if counter >= max_frames: break
