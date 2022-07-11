import sys

API_KEY_LIST = ['2BPofIMYS789jEMXbi8dcEiF4Xj', '2BF0rMZPoEZzyDP0v913XREBCsO', '2BY58n2bpVtRxoAGgph2UThtyQa',
                '2BmTVlIqRKYCPrKVdznuO5oFdHq', '2BmTvkJL6zDjTQZpS4xonOKqmVE', '2BmUM2A7xjKlLCqhh8f8HUgDLwC']
# SYMBOL = 'BTC'
# PARAMS = {
#     'a': SYMBOL,
#     'i': '24h',
#     'api_key': random.choice(API_KEY_LIST)
# }

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

SYMBOL_LIST = ['BTC', 'ETH', 'AAVE', 'ABT', 'AMPL', 'ANT', 'ARMOR', 'BADGER', 'BAL', 'BAND',
               'BAT', 'BIX', 'BNT', 'BOND', 'BRD', 'BUSD', 'BZRX', 'CELR', 'CHSB', 'CND', 'COMP', 'CREAM', 'CRO', 'CRV',
               'CVC', 'CVP', 'DAI', 'DDX', 'DENT', 'DGX', 'DHT', 'DMG', 'DODO', 'DOUGH', 'DRGN', 'ELF', 'ENG', 'ENJ',
               'EURS', 'FET', 'FTT', 'FUN', 'GNO', 'GUSD', 'HEGIC', 'HOT', 'HPT', 'HT', 'HUSD', 'INDEX', 'KCS', 'LAMB',
               'LBA', 'LDO', 'LEO', 'LINK', 'LOOM', 'LRC', 'MANA', 'MATIC', 'MCB', 'MCO', 'MFT', 'MIR', 'MKR', 'MLN',
               'MTA', 'MTL', 'MX', 'NDX', 'NEXO', 'NFTX', 'NMR', 'Nsure', 'OCEAN', 'OKB', 'OMG', 'PAY', 'PERP',
               'PICKLE', 'PNK', 'PNT', 'POLY', 'POWR', 'PPT', 'QASH', 'QKC', 'QNT', 'RDN', 'REN', 'REP', 'RLC', 'ROOK',
               'RPL', 'RSR', 'SAI', 'SAN', 'SNT', 'SNX', 'STAKE', 'STORJ', 'sUSD', 'SUSHI', 'TEL', 'TOP', 'UBT', 'UMA',
               'UNI', 'USDC', 'USDK', 'USDP', 'USDT', 'UTK', 'VERI', 'WaBi', 'WAX', 'WBTC', 'WETH', 'wNXM', 'WTC',
               'YAM', 'YFI', 'ZRX']
