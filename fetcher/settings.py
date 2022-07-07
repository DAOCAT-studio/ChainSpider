import random
API_KEY_LIST = ['2BPofIMYS789jEMXbi8dcEiF4Xj', '2BF0rMZPoEZzyDP0v913XREBCsO', '2BY58n2bpVtRxoAGgph2UThtyQa']
SYMBOL = 'BTC'
PARAMS = {
    'a': SYMBOL,
    'i': '24h',
    'api_key': random.choice(API_KEY_LIST)
}

# local
# HOST = '127.0.0.1'
# PASSWD = 'hwt123'
# PORT = 3306

# server
HOST = '172.17.0.1'
PORT = 3307
PASSWD = '123456'

USER = 'root'
DB = "api_data"

# LOG_ROOT = "F:/"
LOG_ROOT = "./"
