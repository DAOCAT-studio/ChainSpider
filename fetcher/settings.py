import sys

API_KEY_LIST = ['2BPofIMYS789jEMXbi8dcEiF4Xj', '2BF0rMZPoEZzyDP0v913XREBCsO', '2BY58n2bpVtRxoAGgph2UThtyQa',
                '2BmTVlIqRKYCPrKVdznuO5oFdHq', '2BmTvkJL6zDjTQZpS4xonOKqmVE', '2BmUM2A7xjKlLCqhh8f8HUgDLwC']

if sys.platform == 'win32':
    # local
    HOST = '127.0.0.1'
    USER = 'root'
    PASSWD = 'hwt123'
    PORT = 3306
else:
    # server
    HOST = '43.158.211.160'
    PORT = 3306
    USER = 'admin'
    PASSWD = 'admin'

DB = "api_data"

# LOG_ROOT = "F:/"
LOG_ROOT = "./"

