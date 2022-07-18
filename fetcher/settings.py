import configparser
import os
import sys

API_KEY_LIST = ['2BPofIMYS789jEMXbi8dcEiF4Xj', '2BF0rMZPoEZzyDP0v913XREBCsO', '2BY58n2bpVtRxoAGgph2UThtyQa',
                '2BmTVlIqRKYCPrKVdznuO5oFdHq', '2BmTvkJL6zDjTQZpS4xonOKqmVE', '2BmUM2A7xjKlLCqhh8f8HUgDLwC']

curpath = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(curpath, 'config.ini')
cf = configparser.ConfigParser()
cf.read(path, encoding='utf-8')

if sys.platform == 'win32':
    # local
    db_set = cf['local']

else:
    # server
    db_set = cf['server']

HOST = db_set['HOST']
PORT = int(db_set['PORT'])
USER = db_set['USER']
PASSWD = db_set['PASSWD']
DB = 'api_data'

# LOG_ROOT = 'F:/'
LOG_ROOT = './'
