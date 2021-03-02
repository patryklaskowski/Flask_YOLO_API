import argparse

def parse_arguments():
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
    return args


def print_settings(args):
    fmt = '> {key:10s} : {val:s}'
    sep = '---------'
    print(sep)
    print('Settings:')
    for key, val in args.__dict__.items():
        print(fmt.format(key=key, val=str(val)))
    print(sep)
