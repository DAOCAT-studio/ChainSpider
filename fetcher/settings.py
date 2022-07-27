import configparser
import os
import sys

BANNER = r"""

 ___  ___  ___       __   _________   
|\  \|\  \|\  \     |\  \|\___   ___\ 
\ \  \\\  \ \  \    \ \  \|___ \  \_| 
 \ \   __  \ \  \  __\ \  \   \ \  \  
  \ \  \ \  \ \  \|\__\_\  \   \ \  \ 
   \ \__\ \__\ \____________\   \ \__\
    \|__|\|__|\|____________|    \|__|
                                      
                                      
"""

VERSION = "1.0.0"

API_KEY_LIST = ['2BPofIMYS789jEMXbi8dcEiF4Xj', '2BF0rMZPoEZzyDP0v913XREBCsO', '2BY58n2bpVtRxoAGgph2UThtyQa',
                '2BmTVlIqRKYCPrKVdznuO5oFdHq', '2BmTvkJL6zDjTQZpS4xonOKqmVE', '2BmUM2A7xjKlLCqhh8f8HUgDLwC']

cur_path = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(cur_path, 'config.ini')
cf = configparser.ConfigParser()
cf.read(config_path, encoding='utf-8')

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

