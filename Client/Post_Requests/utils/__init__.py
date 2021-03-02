# utils package

from .client import API_Client

def print_settings(args):
    fmt = '> {key:10s} : {val:s}'
    sep = '---------'
    print(sep)
    print('Settings:')
    for key, val in args.__dict__.items():
        print(fmt.format(key=key, val=str(val)))
    print(sep)
