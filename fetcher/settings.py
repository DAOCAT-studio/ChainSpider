import random
API_KEY_LIST = ['2BPofIMYS789jEMXbi8dcEiF4Xj', '2BF0rMZPoEZzyDP0v913XREBCsO', '2BY58n2bpVtRxoAGgph2UThtyQa']
SYMBOL = 'BTC'
PARAMS = {
    'a': SYMBOL,
    'i': '24h',
    'api_key': random.choice(API_KEY_LIST)
}

HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
# PASSWD = 'hwt123'
PASSWD = 'Hwt123456!'
DB = "api_data"

# LOG_ROOT = "F:/"
LOG_ROOT = "./"
