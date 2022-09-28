import time

import schedule

from glassnode import GNSpider
from nomics import NMSpider


def glassnode():
    GNSpider().run_main()
    time.sleep(15)


def nomics():
    N = NMSpider()
    N.get_tickers(N.labels["active"])
    N.get_tickers(N.labels["dead"])
    N.handle_historical()


schedule.every().day.at("09:30").do(glassnode)
schedule.every().day.at("12:30").do(nomics)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
